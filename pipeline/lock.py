"""The fail-closed LOCK chokepoint (Phase C).

A standalone CLI that nobody is *required* to run reproduces the org failure that
shipped the templated Psalm 22 cluster. So this is the one gate every narration —
engine-generated or hand-authored, short or long — must pass before it is locked
or its audio is rendered:

  run_lock(folder)  →  deterministic KJV-strict (Phase B) + Rule-8 (short-only) +
                       md↔tagged parity + cross-artifact cluster check (Phase A) vs
                       the folder's SIBLINGS. On 0 blocking it writes <folder>/.locked
                       (speaker-bound hash of the SPOKEN text actually rendered) and
                       registers the artifact. Otherwise it refuses.
                       (Catalogue-wide cluster + a real anchor-verse check are
                       documented follow-ups; today the cluster scope is siblings.)

  Known residual doors (documented, not yet closed): direct invocation of the
  sibling-repo per_turn_synth.py (--no-gate / manifest-absent) bypasses the guard;
  the engine generate path self-locks in runner.py before audio.

  is_locked(folder) →  True only if .locked exists AND its hash matches the current
                       spoken text (a re-tag / edit staleness-busts the lock).

  require_lock(folder) is the guard `handoff.run_audio_pipeline` calls so audio is
  never rendered for unlocked/stale text (the enforcement the standalone CLI lacked).

The `.locked` hash binds `narration-tagged.md` when present (what synth actually
consumes), else `narration.md` — so a stale tagged file can't be certified.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from pipeline import cluster_gate, doctrine_gate, kjv_strict
from pipeline import narration_parse as NP
from pipeline.kjv_strict import _canon as _kjv_canon  # punctuation-PRESERVING

_REPO = Path(__file__).resolve().parent.parent
_REGISTRY = _REPO / "data" / "learning" / "freshness_registry.json"


def require_lock_enabled() -> bool:
    enabled = os.getenv("JITB_REQUIRE_LOCK", "1") not in ("0", "false", "no")
    if not enabled:
        print("  [lock] WARNING: JITB_REQUIRE_LOCK is OFF — lock enforcement bypassed.")
    return enabled


# ---- spoken-text hash (binds what is rendered) -------------------------------
def _spoken_source(folder: Path) -> Path | None:
    for name in ("narration-tagged.md", "narration.md"):
        p = folder / name
        if p.is_file():
            return p
    return None


def _canon_spoken(path: Path) -> str:
    """Punctuation-PRESERVING canonical of a narration(-tagged) file, binding the
    SPEAKER to its text (so a voice swap busts the lock too — gemini). Uses the KJV
    strict canon (NOT narration_parse.normalize, which strips punctuation — that
    would make the lock blind to a dropped comma)."""
    nar = NP.parse(path.read_text(encoding="utf-8"))  # fail-closed on empty
    # merge consecutive same-speaker blocks so the canonical is segmentation-agnostic
    # (markdown splits per beat; the XML tagged file merges runs) — but a VOICE SWAP
    # changes the speaker sequence and so busts hash + parity.
    runs: list[tuple[str, list[str]]] = []
    for b in nar.blocks:
        if not b.text:
            continue
        if runs and runs[-1][0] == b.speaker:
            runs[-1][1].append(b.text)
        else:
            runs.append((b.speaker, [b.text]))
    return _kjv_canon(" || ".join(f"{spk}: {' '.join(txts)}" for spk, txts in runs))


def spoken_hash(folder: Path) -> str:
    """Hash the SPOKEN text that is actually rendered (narration-tagged.md when
    present), punctuation-preserving so a comma edit busts the lock."""
    p = _spoken_source(folder)
    if p is None:
        raise FileNotFoundError(f"no narration(-tagged).md in {folder}")
    return hashlib.sha256(_canon_spoken(p).encode("utf-8")).hexdigest()


def parity_mismatch(folder: Path) -> str | None:
    """If both narration.md (verified, with refs) and narration-tagged.md (rendered)
    exist, their spoken text MUST match — else the lock would certify text that is
    not what synth renders (split-brain). Returns a reason if they diverge."""
    src, tagged = folder / "narration.md", folder / "narration-tagged.md"
    if not (src.is_file() and tagged.is_file()):
        return None
    try:
        if _canon_spoken(src) != _canon_spoken(tagged):
            return ("narration.md and narration-tagged.md spoken text differ — the "
                    "verified source != the rendered file; re-tag before locking")
    except NP.EmptyNarrationError as e:
        return f"cannot parse for parity: {e}"
    return None


def is_locked(folder: Path) -> tuple[bool, str]:
    lk = folder / ".locked"
    if not lk.is_file():
        return (False, "no .locked token")
    try:
        data = json.loads(lk.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return (False, ".locked is unreadable")
    try:
        cur = spoken_hash(folder)
    except Exception as e:  # noqa
        return (False, f"cannot hash spoken text: {e}")
    if data.get("spoken_sha256") != cur:
        return (False, "stale: spoken text changed since lock — re-run cli_lock")
    pm = parity_mismatch(folder)
    if pm:
        return (False, f"stale: {pm}")
    return (True, "locked")


def require_lock(folder: Path) -> None:
    """Raise unless `folder` holds a current lock (the enforcement guard)."""
    if not require_lock_enabled():
        return
    ok, why = is_locked(folder)
    if not ok:
        raise PermissionError(
            f"REFUSING to proceed: {folder.name} is not locked ({why}). "
            f"Run:  .venv\\Scripts\\python.exe cli_lock.py \"{folder}\"  first. "
            f"(set JITB_REQUIRE_LOCK=0 to override — discouraged.)"
        )


# ---- the checks --------------------------------------------------------------
def _kjv_findings(md: str) -> list[str]:
    out = []
    for f in kjv_strict.verify_narration(md):
        if f.get("blocking"):
            out.append(f"KJV {f['status']}: {f['detail']}")
    return out


def _rule8_findings(md: str, form: str) -> list[str]:
    """Rule-8: a 60s short can't pace >2 SUBSTANTIAL KJV quotes (KJV reads at a fixed
    speed). Short re-echoes (<5 words, e.g. 'my God.', 'Let him deliver him,') add
    negligible time and are NOT counted — only spans of >=5 words."""
    if form != "short":
        return []
    spans = [s for s in NP.quoted_spans_with_refs(md)
             if s["klass"] in ("tagged_kjv", "inline_kjv")
             and len(NP.normalize(s["text"]).split()) >= 5]
    if len(spans) > 2:
        return [f"Rule-8: {len(spans)} substantial KJV quote spans (>2) — a 60s short can't pace that many"]
    return []


def _anchor_findings(folder: Path, md: str) -> list[str]:
    """Best-effort: if a primary ref is discoverable, it should be quoted somewhere."""
    # the narration header may name a primary ref; if none discoverable, skip (advisory only)
    return []  # advisory-only in Phase C; tightened when a manifest schema exists


def _sibling_folders(folder: Path) -> list[Path]:
    parent = folder.parent
    return sorted(
        d for d in parent.iterdir()
        if d.is_dir() and d != folder and (d / "narration.md").is_file()
    )


def run_lock(folder: Path, *, form: str = "short", check_cluster: bool = True) -> dict:
    """Run all lock checks. Writes .locked + registers on pass. Returns a report."""
    md_path = folder / "narration.md"
    if not md_path.is_file():
        return {"ok": False, "folder": folder.name, "blocking": ["no narration.md"]}
    md = md_path.read_text(encoding="utf-8")

    blocking: list[str] = []
    try:
        blocking += _kjv_findings(md)
    except NP.EmptyNarrationError as e:
        return {"ok": False, "folder": folder.name, "blocking": [f"parse: {e}"]}
    blocking += _rule8_findings(md, form)
    blocking += _anchor_findings(folder, md)

    # split-brain guard: the rendered tagged file must match the verified source
    pm = parity_mismatch(folder)
    if pm:
        blocking.append(f"parity: {pm}")

    cluster_block: list[str] = []
    cluster_skipped: list[str] = []
    if check_cluster:
        sibs = _sibling_folders(folder)
        if sibs:
            arts = [(folder.name, md)]
            for s in sibs:
                try:
                    s_md = (s / "narration.md").read_text(encoding="utf-8")
                    NP.parse(s_md)  # validate parseable before feeding the cluster check
                    arts.append((s.name, s_md))
                except (OSError, NP.EmptyNarrationError):
                    cluster_skipped.append(s.name)  # one bad sibling must not crash the lock
            if len(arts) > 1:
                rep = cluster_gate.cluster_check(arts, within_cluster=True)
                for f in rep.blocking:
                    if folder.name in f.members:
                        cluster_block.append(f"cluster {f.kind}: {f.phrase!r} shared with {sorted(set(f.members)-{folder.name})}")
        else:
            cluster_skipped.append("(no sibling cluster — locked WITHOUT cross-artifact scrutiny)")
    blocking += cluster_block

    # doctrine-landmine scan (WARN, non-blocking — surfaced for the human audio guard)
    doctrine = doctrine_gate.scan(NP.parse(md).spoken_text)

    ok = not blocking
    if ok:
        checks = ["kjv_strict", "parity", "doctrine_scan"] + (["rule8"] if form == "short" else []) + \
                 (["cluster"] if check_cluster else [])
        write_lock(folder, checks=checks)
        register(folder, form=form)
    return {"ok": ok, "folder": folder.name, "blocking": blocking,
            "warnings": cluster_skipped, "doctrine": doctrine}


def write_lock(folder: Path, *, checks: list[str] | None = None) -> None:
    (folder / ".locked").write_text(
        json.dumps({"version": 1, "spoken_sha256": spoken_hash(folder),
                    "checks_run": checks or [], "require_lock_env": os.getenv("JITB_REQUIRE_LOCK", "1")},
                   indent=2),
        encoding="utf-8",
    )


# ---- registry (rebuild-from-disk authority) ----------------------------------
def register(folder: Path, *, form: str = "short") -> None:
    """Append/refresh this artifact in the freshness registry (rebuilt from disk,
    so a rewrite/delete never leaves a phantom)."""
    # only record real repo content (keeps the registry clean + isolates tests, whose
    # folders live under a temp dir, not the repo tree).
    try:
        folder.resolve().relative_to(_REPO)
    except ValueError:
        return
    reg = rebuild_registry()
    nar = NP.parse((folder / "narration.md").read_text(encoding="utf-8"))
    reg[str(folder)] = {"folder": folder.name, "form": form,
                        "hook": nar.hook, "cta": nar.cta}
    _REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    _REGISTRY.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")


def rebuild_registry() -> dict:
    """Authority = the set of on-disk .locked folders (no append-only phantoms)."""
    reg: dict = {}
    for lk in _REPO.glob("longform/**/.locked"):
        folder = lk.parent
        md = folder / "narration.md"
        if not md.is_file():
            continue
        try:
            nar = NP.parse(md.read_text(encoding="utf-8"))
        except NP.EmptyNarrationError:
            continue
        reg[str(folder)] = {"folder": folder.name, "hook": nar.hook, "cta": nar.cta}
    return reg
