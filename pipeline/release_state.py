"""pipeline/release_state.py — ONE computation of per-piece release state.

The catalogue (`_website/manifest.yaml`, hard-joined via `source:`/`read_source:`/
`study_source:`), the final video (pipeline/finality.py, sha-anchored), the publish
pack, the thumbnails, the website read page, and the posting ledger
(`data/release_ledger.json`) — resolved into one PieceState per catalogue item.

Consumed by release_check.py (the SYNC gate) and production_board.py (the human
board): same state, two views. See v2/RELEASE_SYNC.md.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from pipeline import finality

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_website"
MANIFEST = SITE / "manifest.yaml"
LEDGER = ROOT / "data" / "release_ledger.json"

PLATFORMS = ["youtube", "tiktok", "facebook", "instagram"]
LONG_POST_PLATFORMS = ["youtube"]  # matches LONG_PLATFORMS in publish_pack

# public_status tiers that MUST be fully wired (fail-closed)
_SHIPPED = {"studio_complete", "live"}


@dataclass
class PieceState:
    slug: str
    kind: str = "short"
    title: str = ""
    ref: str = ""
    cluster: str | None = None
    cluster_order: int | None = None
    parent: str | None = None
    status: str = "planned"
    join: str | None = None            # which manifest field joined us to the folder
    source_dir: Path | None = None
    finality: str = finality.NO_VIDEO
    video: Path | None = None
    video_sha: str = ""
    pack_exists: bool = False
    pack_sha: str = ""                 # _source.json.final_sha ('' = unstamped)
    pack_copy_sha: str = ""            # _source.json.copy_final_sha (what the COPY was authored against)
    rivals: list = field(default_factory=list)   # same-lane candidate finals not picked
    has_read_source: bool = False      # manifest read_source: present (G5 arming)
    thumbs_exist: bool = False
    thumbs_sha: str = ""               # thumbs/_meta.json.final_sha
    read_page: bool = False            # read/<slug>.html exists
    read_video: Path | None = None     # the *_scored video read frames come from
    read_video_sha: str = ""
    read_meta_sha: str = ""            # assets/study/read/<slug>/_meta.json.source_sha
    read_url_meta: str = ""            # publish_meta.json.read_url
    youtube_id: str | None = None
    ledger: dict = field(default_factory=dict)   # platform -> {url, posted, final_sha,...}
    dangling: list = field(default_factory=list)  # *_source fields set but folder missing

    @property
    def post_platforms(self) -> list[str]:
        return LONG_POST_PLATFORMS if self.kind == "long" else PLATFORMS

    @property
    def pack_fresh(self) -> bool:
        return bool(self.pack_sha) and self.pack_sha == self.video_sha

    @property
    def thumbs_fresh(self) -> bool:
        return bool(self.thumbs_sha) and self.thumbs_sha == self.video_sha

    @property
    def read_fresh(self) -> bool:
        return bool(self.read_meta_sha) and self.read_meta_sha == self.read_video_sha


def load_manifest() -> dict:
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


def load_ledger() -> dict:
    if LEDGER.is_file():
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    return {}


def atomic_write(path: Path, text: str) -> None:
    """Temp-file + os.replace so a crash mid-write never corrupts the store.
    Unique tmp name (concurrent writers don't collide) + retry on Windows
    PermissionError (destination briefly open in a reader)."""
    tmp = path.with_suffix(f"{path.suffix}.{os.getpid()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    for _ in range(5):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            time.sleep(0.2)
    os.replace(tmp, path)  # last try — let a real failure raise


def save_ledger(data: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(LEDGER, json.dumps(data, indent=2, sort_keys=True))


def resolve_source(item: dict) -> tuple[Path | None, str | None]:
    """Hard join: catalogue item -> piece folder. NO fuzzy matching, ever."""
    for key in ("source", "read_source", "study_source"):
        rel = item.get(key)
        if rel:
            p = (SITE / rel).resolve()
            if p.is_dir():
                return p, key
            return None, key  # named but missing = a real defect, keep the field name
    return None, None


def _read_video(item: dict, source_dir: Path) -> Path | None:
    """The video read-page frames are cut from (build_readpage.py's rule)."""
    if item.get("read_video"):
        p = source_dir / item["read_video"]
        return p if p.is_file() else None
    hits = [h for h in sorted((source_dir / "visual").glob("*_scored.mp4"))
            if ".bak" not in h.name]
    return hits[0] if hits else None


def _json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def gather() -> tuple[list[PieceState], list[str], list[str]]:
    """All catalogue items resolved -> (states, orphan lane folders, orphan read pages)."""
    m = load_manifest()
    ledger = load_ledger()
    read_pages = {p.stem for p in (SITE / "read").glob("*.html")} - {"index"}
    states: list[PieceState] = []
    joined_dirs: set[Path] = set()

    for it in m["items"]:
        st = PieceState(
            slug=it.get("slug", ""), kind=it.get("kind", "short"),
            title=it.get("title", ""), ref=it.get("ref", ""), cluster=it.get("cluster"),
            cluster_order=it.get("cluster_order"), parent=it.get("parent"),
            status=it.get("public_status", "planned"),
            youtube_id=it.get("youtube_id"),
            ledger=ledger.get(it.get("slug", ""), {}),
        )
        st.source_dir, st.join = resolve_source(it)
        # EVERY named *_source must exist, not just the winning one (a dangling
        # pointer is a real defect even when a higher-precedence field works)
        st.dangling = [k for k in ("source", "read_source", "study_source")
                       if it.get(k) and not (SITE / it[k]).resolve().is_dir()]
        if st.source_dir:
            joined_dirs.add(st.source_dir)
            st.finality, st.video = finality.final_video(st.source_dir)
            if st.video:
                st.video_sha = finality.content_sha(st.video)
            if st.video:
                st.rivals = [p.name for p in finality.rival_finals(st.source_dir)]
            pub = st.source_dir / "publish"
            st.pack_exists = (pub / "PUBLISH_INDEX.html").is_file()
            _src = _json(pub / "_source.json")
            st.pack_sha = _src.get("final_sha", "")
            st.pack_copy_sha = _src.get("copy_final_sha", "")
            st.thumbs_exist = bool(list((pub / "thumbs").glob("thumb_*.jpg"))) \
                if (pub / "thumbs").is_dir() else False
            st.thumbs_sha = _json(pub / "thumbs" / "_meta.json").get("final_sha", "")
            st.read_url_meta = _json(st.source_dir / "publish_meta.json").get("read_url", "")
        # the read-frame anchor mirrors build_readpage.py exactly: frames are cut
        # from the read_source folder's scored video, never the `source` folder's
        rs = it.get("read_source")
        st.has_read_source = bool(rs)
        read_dir = (SITE / rs).resolve() if rs else None
        if read_dir and read_dir.is_dir():
            st.read_video = _read_video(it, read_dir)
            if st.read_video:
                st.read_video_sha = finality.content_sha(st.read_video)
        st.read_page = st.slug in read_pages
        st.read_meta_sha = _json(
            SITE / "assets" / "study" / "read" / st.slug / "_meta.json").get("source_sha", "")
        states.append(st)

    lane_dirs = {p.parent.resolve() for p in (ROOT / "batches").glob("*/*/piece.json")}
    lane_dirs |= {p.parent.resolve() for p in (ROOT / "longform").glob("*/v1/narration.md")}
    orphans = sorted(d.name if d.name != "v1" else d.parent.name
                     for d in lane_dirs - joined_dirs)
    orphan_pages = sorted(read_pages - {s.slug for s in states})
    return states, orphans, orphan_pages


# ----------------------------------------------------------------------------
# the SYNC gates — $0 deterministic. Returns [(gate, level, slug, msg)].
# ----------------------------------------------------------------------------
def run_gates(states: list[PieceState], orphans: list[str],
              orphan_pages: list[str] = ()) -> list[tuple[str, str, str, str]]:
    out: list[tuple[str, str, str, str]] = []
    longs = {s.cluster: s.slug for s in states if s.kind == "long" and s.cluster}
    by_slug = {s.slug: s for s in states}

    for s in states:
        shipped = s.status in _SHIPPED
        live = s.status == "live"

        # G7 long<->short linkage (manifest-only: must fire even with no folder/video)
        if s.kind == "short" and s.cluster in longs:
            if not s.parent:
                out.append(("SYNC-G7", "FAIL", s.slug,
                            f"cluster '{s.cluster}' has a long ({longs[s.cluster]}) but parent: is not set"))
            elif s.parent != longs[s.cluster]:
                out.append(("SYNC-G7", "FAIL", s.slug,
                            f"parent={s.parent} but the cluster's long is {longs[s.cluster]}"))
        if s.parent:
            p = by_slug.get(s.parent)
            if p is None:
                out.append(("SYNC-G7", "FAIL", s.slug, f"parent '{s.parent}' is not a catalogue slug"))
            elif p.kind != "long":
                out.append(("SYNC-G7", "FAIL", s.slug, f"parent '{s.parent}' is kind={p.kind}, must be a long"))
            elif s.cluster != p.cluster:
                # closes the gap the first G7 block misses: it only fires when
                # s.cluster already matches SOME long's cluster, so a short with
                # cluster: null (or a typo) and an accidental/copy-pasted parent:
                # sailed through undetected (red-team 2026-07-15)
                out.append(("SYNC-G7", "FAIL", s.slug,
                            f"parent={s.parent} (cluster={p.cluster!r}) but this short's own "
                            f"cluster={s.cluster!r} - mismatched, check for a copy-paste typo"))

        # G6 published coherence (manifest x ledger: must fire even with no folder/video)
        yt = s.ledger.get("youtube", {})
        if s.youtube_id and not yt:
            out.append(("SYNC-G6", "FAIL", s.slug,
                        "manifest has youtube_id but the release ledger has no dated entry "
                        "(re-record via upload_tracker.py --set)"))
        if yt and s.youtube_id and yt.get("video_id") and yt["video_id"] != s.youtube_id:
            out.append(("SYNC-G6", "FAIL", s.slug,
                        f"ledger video_id {yt.get('video_id')} != manifest youtube_id {s.youtube_id}"))
        if s.youtube_id and not live:
            out.append(("SYNC-G6", "FAIL", s.slug, f"youtube_id set but public_status={s.status} (not live)"))
        if live and not s.youtube_id:
            out.append(("SYNC-G6", "FAIL", s.slug, "public_status=live but no youtube_id"))
        if yt and not s.youtube_id:
            # the crash window between the ledger write and the manifest write in
            # upload_tracker._set, or a hand-edit — without this reverse check the
            # piece re-lists as "READY, NOT YET UPLOADED" (red-team M1/M3)
            out.append(("SYNC-G6", "FAIL", s.slug,
                        "ledger says posted on youtube but manifest has no youtube_id "
                        "(interrupted --set? re-run upload_tracker.py --set with the same URL)"))
        for plat, entry in s.ledger.items():
            # POSTED sha vs current final: FAIL by design — the public copy and the
            # repo's final have diverged; re-post, or restore the final. (Policy in
            # v2/RELEASE_SYNC.md; only checkable when the final exists.)
            if entry.get("final_sha") and s.video_sha and entry["final_sha"] != s.video_sha:
                out.append(("SYNC-G6", "FAIL", s.slug,
                            f"{plat}: the POSTED video's sha differs from the current final "
                            "(final changed after posting - re-post or restore)"))
            if not entry.get("final_sha"):
                out.append(("SYNC-G6", "WARN", s.slug,
                            f"{plat}: ledger entry has no final_sha - divergence is "
                            "UNDETECTABLE for this post (was there a final when --set ran?)"))
            if not entry.get("posted"):
                out.append(("SYNC-G6", "WARN", s.slug, f"{plat}: ledger entry has no posted date"))

        # G1 hard join
        for k in s.dangling:
            out.append(("SYNC-G1", "FAIL", s.slug, f"{k} points at a missing folder"))
        if s.source_dir is None:
            if not s.dangling:
                if shipped:
                    out.append(("SYNC-G1", "FAIL", s.slug, "no source join (add source: to manifest.yaml)"))
                elif s.status == "in_production":
                    out.append(("SYNC-G1", "WARN", s.slug, "no source join yet (add when the folder exists)"))
            continue  # folder-dependent checks below are unreachable

        # G2 finality
        if shipped and not s.finality.startswith("FINAL"):
            out.append(("SYNC-G2", "FAIL", s.slug, f"status={s.status} but video is '{s.finality}'"))
        if shipped and s.rivals:
            out.append(("SYNC-G2", "WARN", s.slug,
                        f"multiple candidate finals in the lane - picked {s.video.name if s.video else '?'}, "
                        f"rivals: {s.rivals} - pin the postable with FINAL_VIDEO.txt"))
        # G5 website (read_page + read-frame anchor don't need the final video)
        if s.read_page and not s.has_read_source:
            out.append(("SYNC-G5", "WARN", s.slug,
                        "read page exists but manifest has no read_source: - frame "
                        "freshness is UNGATED (restore the field)"))
        if s.read_page:
            if s.read_video and not s.read_fresh:
                out.append(("SYNC-G5", "WARN", s.slug,
                            "read-page frames not provably from the current scored video "
                            "(re-run _website/build_readpage.py --force)"))
            want = f"https://awakeden.com/read/{s.slug}.html"
            if s.read_url_meta and s.read_url_meta != want:
                out.append(("SYNC-G5", "FAIL", s.slug,
                            f"publish_meta.json read_url = {s.read_url_meta} but the page is {want}"))
            if not s.read_url_meta and shipped:
                out.append(("SYNC-G5", "WARN", s.slug, "publish_meta.json has no read_url (footer loses the site link)"))
        elif live:
            out.append(("SYNC-G5", "WARN", s.slug, "live but no read page (set read_source: + build_readpage.py)"))
        if not s.video:
            continue
        # G3 pack freshness
        if shipped:
            if not s.pack_exists:
                out.append(("SYNC-G3", "FAIL", s.slug, "no publish pack (run cli_publish.py)"))
            elif not s.pack_sha:
                out.append(("SYNC-G3", "FAIL", s.slug,
                            "pack not sha-stamped (re-run cli_publish.py --index to refresh + stamp)"))
            elif not s.pack_fresh:
                out.append(("SYNC-G3", "FAIL", s.slug,
                            "pack STALE: built from a different final (re-run cli_publish.py --index)"))
            elif s.pack_copy_sha and s.pack_copy_sha != s.video_sha:
                # mechanicals are fresh but the COPY was authored against an older
                # final — a bare --index restamp must not launder the human step
                # (red-team M1: "fresh only proves someone ran --index")
                out.append(("SYNC-G3", "WARN", s.slug,
                            "pack COPY authored against an older final - re-read the .md "
                            "copy, then cli_publish.py --copy-ok (or --redraft)"))
        # G4 thumbnails
        if shipped:
            lvl = "FAIL" if live else "WARN"
            if not s.thumbs_exist:
                out.append(("SYNC-G4", lvl, s.slug, "no thumbnails (run pipeline/thumbnails.py)"))
            elif not s.thumbs_sha:
                out.append(("SYNC-G4", lvl, s.slug, "thumbnails not sha-stamped (re-run pipeline/thumbnails.py)"))
            elif not s.thumbs_fresh:
                out.append(("SYNC-G4", lvl, s.slug, "thumbnails STALE vs the final (re-run pipeline/thumbnails.py)"))

    for name in orphans:
        out.append(("SYNC-G1", "WARN", name, "lane piece has no catalogue item (add it to manifest.yaml)"))
    for name in orphan_pages:
        out.append(("SYNC-G5", "WARN", name,
                    "read page on the site has no catalogue item (renamed slug? stale page?)"))
    return out


def to_post(states: list[PieceState]) -> list[tuple[PieceState, list[str]]]:
    """The posting queue: shipped pieces with a FINAL video and missing platforms.
    Longs first, then their shorts by cluster_order (shorts funnel to the long)."""
    q = []
    for s in states:
        if s.status not in _SHIPPED or not s.finality.startswith("FINAL"):
            continue
        missing = [p for p in s.post_platforms if p not in s.ledger]
        if missing:
            q.append((s, missing))
    q.sort(key=lambda x: (x[0].cluster or "~", x[0].kind != "long", x[0].cluster_order or 99))
    return q
