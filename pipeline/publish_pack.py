"""pipeline/publish_pack.py — render a built UploadKit into a paste-ready PUBLISH PACK.

Stage 6 (the publisher). This is the Furgiven `build_publish_pack` *pattern*, on
JITB content with JITB's engine: per-platform copy files + a `captions.srt` built
from the finished video's forced-aligned `words.json` + a self-contained
`PUBLISH_INDEX.html` with a copy button per field. It NEVER uploads — paste only.

The kit is AUTO-DRAFTED by `upload_engine` (then panel-refined); this module is the
mechanical packaging + the clickable index. `publish_check.py` is the gate.

Layout written under `<media>/publish/`:
    PUBLISH_INDEX.html            clickable, self-contained, copy-buttons
    captions.srt                  from <final video>.words.json
    _source.json  _seo.json       the facts + suggested keywords
    youtube_short.md              TITLE/DESCRIPTION/TAGS/HASHTAGS              (short)
    tiktok.md / instagram.md      CAPTION/HASHTAGS                            (short)
    facebook.md                   TITLE/DESCRIPTION/HASHTAGS                  (short)
    youtube_long.md               TITLE/DESCRIPTION/TAGS/HASHTAGS/CHAPTERS/PINNED_COMMENT (long)
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

from pipeline.upload_models import PlatformMeta, UploadKit

# ----------------------------------------------------------------------------
# per-unit platform -> file + section layout
# ----------------------------------------------------------------------------
# Each platform file is "## SECTION\n<text>\n## SECTION ..." parsed by header.
SHORT_PLATFORMS = ["youtube_short", "tiktok", "facebook", "instagram"]
LONG_PLATFORMS = ["youtube_long"]

PLATFORM_FILE = {
    "youtube_short": "youtube_short.md",
    "youtube_long": "youtube_long.md",
    "tiktok": "tiktok.md",
    "facebook": "facebook.md",
    "instagram": "instagram.md",
}
# platforms whose body section is labelled CAPTION (caption-only feeds); the rest = DESCRIPTION
_CAPTION_PLATFORMS = {"tiktok", "instagram"}
# platforms that carry a separate keyword TAGS field (YouTube only)
_TAGS_PLATFORMS = {"youtube_short", "youtube_long"}

PLACEHOLDER = "TODO  <-- write this; delete this line"

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
SEC_HDR_RE = re.compile(r"^##\s+(\w+)\s*$", re.M)


def parse_copy(path: Path) -> dict[str, str]:
    """Parse a '## SECTION' copy file -> {SECTION: text} (HINT comments stripped)."""
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    ms = list(SEC_HDR_RE.finditer(raw))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(raw)
        out[m.group(1)] = COMMENT_RE.sub("", raw[m.end():end]).strip()
    return out


# ----------------------------------------------------------------------------
# finished video + its forced-aligned words.json
# ----------------------------------------------------------------------------
_FINAL_VIDEO_ORDER = [
    "viral_cut_sfx_music_captioned.mp4",
    "viral_cut_sfx_captioned.mp4",
    "viral_cut_captioned.mp4",
]


def final_video_and_words(media_dir: str | Path) -> tuple[str, str]:
    """Best finished captioned video + its sibling <stem>.words.json (both '' if absent)."""
    a = Path(media_dir).resolve() / "assembly"
    if not a.is_dir():
        # batch living-page layout: visual/. + audio/alignment.json
        # (alignment.json is the same [{w,start,end},...] shape build_srt expects)
        # Finality per the caption policy (2026-07-08): _sfx.mp4 IS the postable final
        # (comic boxes are the captions); the pilot lives under _byteplus/.
        root = Path(media_dir).resolve()
        v = root / "visual"
        if v.is_dir():
            for pat in ("*_sfx.mp4", "_byteplus/*_scored.mp4", "*_scored.mp4"):
                hits = sorted(v.glob(pat))
                if hits:
                    words = root / "audio" / "alignment.json"
                    return str(hits[0].resolve()), (str(words) if words.is_file() else "")
        return "", ""
    for name in _FINAL_VIDEO_ORDER:
        v = a / name
        if v.is_file():
            words = v.with_suffix(".words.json")
            return str(v), (str(words) if words.is_file() else "")
    # fall back to any *_captioned.mp4
    for v in sorted(a.glob("*_captioned.mp4")):
        words = v.with_suffix(".words.json")
        return str(v.resolve()), (str(words) if words.is_file() else "")
    return "", ""


# ----------------------------------------------------------------------------
# captions.srt  (from the forced-aligned words.json)
# ----------------------------------------------------------------------------
def _ts(seconds: float) -> str:
    total_ms = int(round(max(0.0, seconds) * 1000))   # carry .9995s -> +1s, never ',1000'
    ms = total_ms % 1000
    s = total_ms // 1000
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_srt(words_json: str | Path, *, max_chars: int = 42, max_dur: float = 6.0) -> str:
    """Group the per-word [{w,start,end},...] list into readable SRT cues.

    A cue closes on sentence-ending punctuation, ~42 chars, or ~6s — whichever first.
    """
    words = json.loads(Path(words_json).read_text(encoding="utf-8"))
    cues: list[tuple[float, float, str]] = []
    cur: list[str] = []
    start: float | None = None
    last_end = 0.0
    for it in words:
        w = str(it.get("w", "")).strip()
        if not w:
            continue
        s = float(it.get("start", last_end))
        e = float(it.get("end", s))
        if start is None:
            start = s
        cur.append(w)
        last_end = e
        line = " ".join(cur)
        if w.endswith((".", "?", "!")) or len(line) >= max_chars or (e - start) >= max_dur:
            cues.append((start, e, line))
            cur, start = [], None
    if cur and start is not None:
        cues.append((start, last_end, " ".join(cur)))

    out = []
    for i, (a, b, txt) in enumerate(cues, 1):
        out.append(f"{i}\n{_ts(a)} --> {_ts(max(b, a + 0.3))}\n{txt}\n")
    return "\n".join(out)


# ----------------------------------------------------------------------------
# per-platform copy file (rendered FROM the auto-drafted/paneled kit)
# ----------------------------------------------------------------------------
def _section(name: str, text: str) -> str:
    return f"## {name}\n{(text or PLACEHOLDER).strip()}\n"


def render_platform_md(meta: PlatformMeta, *, is_long: bool,
                       chapters: str = "", pinned: str = "") -> str:
    body_label = "CAPTION" if meta.platform in _CAPTION_PLATFORMS else "DESCRIPTION"
    title = f"{PLATFORM_FILE[meta.platform].replace('.md', '')} — {meta.label}"
    out = [f"# {title}", ""]
    if meta.title:
        out.append(_section("TITLE", meta.title))
    out.append(_section(body_label, meta.description))
    if meta.platform in _TAGS_PLATFORMS:
        out.append(_section("TAGS", ", ".join(meta.tags)))
    out.append(_section("HASHTAGS", " ".join(meta.hashtags)))
    if is_long and meta.platform == "youtube_long":
        out.append(_section("CHAPTERS", chapters))
        out.append(_section("PINNED_COMMENT", pinned))
    return "\n".join(out).rstrip() + "\n"


def _meta_by_platform(kit: UploadKit) -> dict[str, PlatformMeta]:
    return {p.platform: p for p in kit.platforms}


# ----------------------------------------------------------------------------
# facts + suggested SEO seeds
# ----------------------------------------------------------------------------
def build_source(kit: UploadKit, video: str, words: str) -> dict:
    s = kit.source
    return {
        "media_dir": s.media_dir,
        "episode_title": s.episode_title,
        "format": s.format,
        "series": s.series_name,
        "anchor_ref": s.anchor_ref,
        "video": video or s.video_path,
        "words_json": words,
        "thumbnail": "",  # JITB has no thumbnail stage yet -> WARN in the gate
    }


def suggest_seo(kit: UploadKit) -> dict:
    s = kit.source
    book = re.split(r"\s*\d", s.anchor_ref, 1)[0].strip() if s.anchor_ref else ""
    kws = [k for k in [s.anchor_ref, book, "bible", "jesus", "gospel", "kjv"] if k]
    return {
        "_note": "Suggested SEO keywords - REFINE before posting. UK-G7 front-loads the anchor ref.",
        "keywords": list(dict.fromkeys(kws)),
    }


# ----------------------------------------------------------------------------
# the clickable index (parsed FROM the on-disk pack, so it reflects edits)
# ----------------------------------------------------------------------------
def _esc(x: str) -> str:
    return html.escape(x or "", quote=True)


_CSS = """
body{font-family:system-ui,Segoe UI,Arial,sans-serif;background:#14110f;color:#f3ece4;margin:0;padding:24px;line-height:1.5}
h1{font-size:26px;margin:0 0 4px}.sub{color:#b59e86;margin:0 0 22px}
h2{margin:30px 0 10px;color:#e8b96b;border-bottom:1px solid #3a322b;padding-bottom:6px}
.card{background:#1e1a16;border:1px solid #352d26;border-radius:12px;padding:14px 16px;margin:12px 0}
.card h3{margin:0 0 8px;font-size:17px}.src{color:#7d6e5e;font-size:12px;font-weight:400}
.media{font-size:13px;margin-bottom:8px}.media a{color:#7fb5e6;margin-right:10px}
.field{margin:9px 0;border-left:3px solid #4a8f4a;padding-left:10px}
.field.todo{border-left-color:#c0612f}
.flabel{font-size:12px;letter-spacing:.06em;color:#b59e86;text-transform:uppercase;display:flex;align-items:center;gap:8px}
pre{white-space:pre-wrap;word-break:break-word;background:#14110f;border:1px solid #2c251f;border-radius:8px;padding:10px;margin:6px 0 0;font-family:inherit;font-size:14px}
.copy{background:#3a4a2f;color:#dfe8c0;border:0;border-radius:6px;padding:2px 9px;font-size:11px;cursor:pointer}
.copy:hover{background:#4d6440}.copy.done{background:#2f6f4a}
.legend{font-size:13px;color:#b59e86;margin:8px 0 0}.legend b.g{color:#7bd07b}.legend b.r{color:#e08a55}
"""

_JS = """
document.querySelectorAll('.copy').forEach(function(b){
  b.addEventListener('click',function(){
    navigator.clipboard.writeText(b.getAttribute('data-copy')||'').then(function(){
      var o=b.textContent;b.textContent='copied';b.classList.add('done');
      setTimeout(function(){b.textContent=o;b.classList.remove('done');},1200);
    });
  });
});
"""


def _is_placeholder(txt: str) -> bool:
    t = (txt or "").strip().lower()
    return (not t) or t.startswith("todo") or "<-- write this" in t


def _render_card(label: str, copy_path: Path, video: str) -> str:
    fields = parse_copy(copy_path)
    rows = []
    for sec, txt in fields.items():
        cls = "field todo" if _is_placeholder(txt) else "field"
        rows.append(
            f'<div class="{cls}"><div class="flabel">{_esc(sec)}'
            f'<button class="copy" data-copy="{_esc(txt)}">copy</button></div>'
            f'<pre>{_esc(txt) or "(empty - author this)"}</pre></div>'
        )
    head = f'<h3>{_esc(label)} <span class="src">{_esc(copy_path.name)}</span></h3>'
    media = (f'<div class="media"><a href="file:///{video.replace(chr(92), "/")}">video</a></div>'
             if video else "")
    return f'<section class="card">{head}{media}{"".join(rows)}</section>'


def build_index(pub: Path, units: list[dict]) -> Path:
    """units = [{'title','platforms':[(label, md_path)], 'video'}]. Cards are parsed
    FROM the on-disk md files, so the index always reflects the current copy."""
    parts = [
        "<!doctype html><meta charset='utf-8'>",
        f"<title>Publish pack</title><style>{_CSS}</style>",
        "<h1>Publish pack</h1>",
        "<p class='legend'>Each field has a <b>copy</b> button. "
        "<b class='g'>green</b> = written, <b class='r'>orange</b> = TODO. "
        "Edit the .md files, re-run the builder, then run publish_check.</p>",
    ]
    for u in units:
        parts.append(f"<h2>{_esc(u['title'])}</h2>")
        for label, md_path in u["platforms"]:
            parts.append(_render_card(label, Path(md_path), u.get("video", "")))
    parts.append(f"<script>{_JS}</script>")
    out = pub / "PUBLISH_INDEX.html"
    out.write_text("\n".join(parts), encoding="utf-8")
    return out


# ----------------------------------------------------------------------------
# write one unit's pack
# ----------------------------------------------------------------------------
def write_unit_pack(kit: UploadKit, *, chapters: str = "", pinned: str = "",
                    force: bool = False) -> dict:
    """Write the per-platform files + captions.srt + _source/_seo for ONE unit.

    Returns {'pub','platforms':[(label, md_path)], 'video', 'is_long', 'srt_note'}.
    Filled copy files are NOT clobbered unless force=True (so panel/hand edits survive
    a rebuild); the mechanical files (srt, _source, index) are always refreshed.
    """
    media = Path(kit.source.media_dir).resolve()
    pub = media / "publish"
    pub.mkdir(exist_ok=True)
    is_long = kit.source.format == "long"
    platforms = LONG_PLATFORMS if is_long else SHORT_PLATFORMS
    by = _meta_by_platform(kit)

    written: list[tuple[str, str]] = []
    for plat in platforms:
        meta = by.get(plat)
        if not meta:
            continue
        path = pub / PLATFORM_FILE[plat]
        if path.exists() and not force:
            written.append((meta.label, str(path)))
            continue
        path.write_text(render_platform_md(meta, is_long=is_long,
                                           chapters=chapters, pinned=pinned),
                        encoding="utf-8")
        written.append((meta.label, str(path)))

    video, words = final_video_and_words(media)
    srt_note = ""
    if words:
        (pub / "captions.srt").write_text(build_srt(words), encoding="utf-8")
    else:
        srt_note = "no <final video>.words.json found — captions.srt not built"

    (pub / "_source.json").write_text(
        json.dumps(build_source(kit, video, words), indent=2, ensure_ascii=False), encoding="utf-8")
    seo_p = pub / "_seo.json"
    if not seo_p.exists() or force:
        seo_p.write_text(json.dumps(suggest_seo(kit), indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "pub": str(pub),
        "platforms": written,
        "video": video,
        "is_long": is_long,
        "srt_note": srt_note,
    }
