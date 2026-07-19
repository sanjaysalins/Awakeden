#!/usr/bin/env python
"""run_piece.py — ONE manifest-driven runner for a living-page batch piece (P1 keystone).

Replaces the per-piece copy-paste quartet (_render_stills.py / _animate.py / _score.py /
_register_assets.py) with a single tested path driven by <piece>/piece.json. Behavior is
byte-compatible with the old scripts (proven on into_thy_hands_luke2346 — same request
bodies, same Kling prompts, same ffmpeg argv, same asset rows) with every P0 guard on
by construction: lint gate + guard_prompt + arm_audit on stills; PASS-sidecar gate +
budget ceiling + ledger row on animate (via _hf_animate_short.hf_animate); ledger rows
on stills too.

Usage:
  .venv\\Scripts\\python.exe run_piece.py "<piece dir>" --stage stills            # $0 lint dry-run
  .venv\\Scripts\\python.exe run_piece.py "<piece dir>" --stage stills --render   # spend
  .venv\\Scripts\\python.exe run_piece.py "<piece dir>" --stage animate           # spend (gated)
  .venv\\Scripts\\python.exe run_piece.py "<piece dir>" --stage score             # $0 ffmpeg
  .venv\\Scripts\\python.exe run_piece.py "<piece dir>" --stage register          # $0 index
  Flags: --force (re-render existing) --only slug1,slug2
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from pipeline import score_mix  # noqa: E402 — the ONE shared score-mix tail (INV-26)

BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
SEEDREAM_USD_PER_IMG = 0.05          # ledger estimate per BytePlus still

# The shared INK camera-only animation contract (was copy-pasted per piece).
INK_BASE = ("A finished inked graphic-novel comic panel - flat printed art with bold black ink "
            "outlines, cel-flat color and cross-hatching. Animate it as {move}. The drawing itself "
            "never moves, redraws, repaints, breathes or changes; the ink lines and flat colors stay "
            "exactly as printed; only the camera moves. No hard cuts, no dissolves, no morphing, no "
            "subject motion, no limbs moving, no new lines drawn. INVENT NOTHING: show ONLY what is "
            "already inked in this exact panel. Keep the subject whole in frame.")

# LIVING-LIGHT contract (2026-07-14 pilot, memory feedback-kling-native-effects-hybrid):
# figures frozen, ONLY light/air move. The three locks the pilot's failures taught:
# expression inside the frozen contract (v1 sternface), dry-wound (v2 bleeding palm),
# whole-figure push (never enlarge a wound). No particle words (veo-glitter lesson).
LIVING_LIGHT_BASE = (
    "A finished inked graphic-novel comic panel - flat printed art with bold black ink outlines, "
    "cel-flat color and cross-hatching, filmed as ONE very slow, gentle push-in toward {target}, "
    "keeping the subject whole in frame. Every figure stays perfectly frozen - no limbs move, no "
    "heads turn; every painted face keeps its exact same expression from first frame to last, the "
    "eyes, brows and mouths NEVER shift, harden, frown or blink. Any wound marks stay exactly as "
    "painted, dry and still - no blood flows, drips, spreads or grows. INVENT NOTHING: no new "
    "figures, hands, wings, objects or lines appear; show ONLY what is already inked in this exact "
    "panel. ONLY the light and the air are alive: {light}")
_GLITTER_WORDS = ("sparkle", "glitter", "particle", "firefl", "bokeh", "shimmering dots")


def load_piece(piece_dir: Path) -> dict:
    return json.loads((piece_dir / "piece.json").read_text(encoding="utf-8"))


def _bp(piece_dir: Path):
    """The shared BytePlus module (style tail + key loader). Canonical copy lives in
    the cluster-1 pilot folder; pieces in OTHER clusters fall back to it (caught the
    hard way on the cluster-2 pilot)."""
    for p in (piece_dir.parent / "father_forgive_them" / "byteplus_seedream.py",
              ROOT / "batches" / "cluster_01_cross" / "father_forgive_them" / "byteplus_seedream.py"):
        if p.is_file():
            spec = importlib.util.spec_from_file_location("bp", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    raise FileNotFoundError("byteplus_seedream.py not found in any cluster pilot folder")


# ---------------------------------------------------------------- stage: stills
def stills_bodies(piece_dir: Path, pj: dict, bp=None,
                  slugs: set[str] | None = None) -> dict[str, tuple[dict, Path]]:
    """slug -> (request body, dest png). Pure — no network, no writes. `slugs` limits
    which jobs are built (a job whose ref is a sibling still not rendered yet would
    crash the eager base64 encode)."""
    from render_lint import guard_prompt
    bp = bp or _bp(piece_dir)
    st = pj["stills"]
    out = {}
    for slug, job in st["jobs"].items():
        if slugs is not None and slug not in slugs:
            continue
        prompt = guard_prompt(job["prompt"])
        body = {"model": st["model"], "prompt": prompt + bp.STYLE + bp.ONE,
                "size": st["size"], "response_format": "url", "watermark": False}
        if job["ref"]:
            ref = (piece_dir / job["ref"]).resolve()
            body["image"] = bp._ref_to_field(str(ref))
            body["sequential_image_generation"] = "disabled"
        out[slug] = (body, piece_dir / "visual" / f"{slug}.png")
    return out


def reuse_check(piece_dir: Path, slug: str, job: dict) -> Path | None:
    """REUSE PRE-FLIGHT (P1-3): before paying for a render, find an identical,
    PASS-audited render of this slug in a sibling piece (same raw prompt + same
    resolved ref). Shared plates used to be paid for 5-8x across the cluster."""
    from render_lint.verify import _sidecar_verdict
    my_ref = (piece_dir / job["ref"]).resolve() if job.get("ref") else None
    for sib in sorted(piece_dir.parent.iterdir()):
        if sib == piece_dir or not (sib / "piece.json").is_file():
            continue
        try:
            sjob = load_piece(sib)["stills"]["jobs"].get(slug)
        except Exception:  # noqa - a malformed sibling manifest must not block a render
            continue
        if not sjob or sjob["prompt"] != job["prompt"]:
            continue
        sib_ref = (sib / sjob["ref"]).resolve() if sjob.get("ref") else None
        if sib_ref != my_ref:
            continue
        png = sib / "visual" / f"{slug}.png"
        if png.exists() and _sidecar_verdict(png) == "PASS":
            return png
    return None


def check_world(pj: dict) -> list[str]:
    """WORLD-CONSISTENCY check: piece.json stills.world maps a recurring subject to its
    canonical phrase + the slugs that show it. Each listed prompt must carry the phrase
    VERBATIM, so the same tomb/stone/face renders in every still (one episode = one world)."""
    problems = []
    jobs = pj["stills"]["jobs"]
    for name, w in pj["stills"].get("world", {}).items():
        for slug in w.get("applies_to", []):
            if slug not in jobs:
                problems.append(f"world:{name} lists unknown slug '{slug}'")
            elif w["canon"] not in jobs[slug]["prompt"]:
                problems.append(f"world:{name} — '{slug}' prompt is missing the canonical phrase")
    return problems


# Every still of a recurring PEOPLED subject must attach a character ref, or the faces
# render generic/duplicated across the episode (feedback-peopled-stills-need-character-ref;
# proven again by the prompt-author POC 2026-07-12). check_world forces the canonical PHRASE
# into each prompt; this forces the ANCHOR too. A recurring subject counts as "people" when
# its world canon names any of these — a tomb/stone/landscape group is exempt.
_PEOPLE_CANON = __import__("re").compile(
    r"\b(wom[ae]n|m[ae]n|messengers?|angels?|disciples?|apostles?|children|child|boys?|"
    r"girls?|fathers?|mothers?|priests?|shepherds?|soldiers?|crowds?|people|witnesses?|"
    r"figures?)\b", __import__("re").I)


def check_refs(pj: dict) -> list[str]:
    """Fail-closed: a peopled recurring subject's stills must each carry a (non-null) ref
    so the same faces render across the episode. The world map declares the recurring
    subjects; for any whose canon describes people, every listed slug's job needs a ref.
    Catches the ref:null trap (e.g. a front-facing women shot rendered with generic faces)."""
    problems = []
    jobs = pj["stills"]["jobs"]
    for name, w in pj["stills"].get("world", {}).items():
        if not _PEOPLE_CANON.search(w.get("canon", "")):
            continue
        for slug in w.get("applies_to", []):
            job = jobs.get(slug)
            if job is not None and not job.get("ref"):
                problems.append(f"world:{name} — peopled still '{slug}' has ref:null; attach a "
                                f"character anchor so faces stay consistent across the episode")
    return problems


# A peopled world canon should LOCK a distinct garment colour per person, so the same
# people wear the same clothes in every frame (check_world copies the canon verbatim into
# each prompt). This teaches the scene-planner at the $0 dry-run — advisory, never blocks,
# because colour is fuzzy (hair-grey vs garment-grey). Adjacency to a clothing noun (±20
# chars) is what keeps 'grey-haired' from counting as a garment colour.
_GARMENT_NOUN = __import__("re").compile(
    r"\b(tunics?|mantles?|robes?|cloaks?|garments?|veils?|wraps?|headscar(?:f|ves)|"
    r"vestments?|shawls?|sash|girdles?|dress|linen)\b", __import__("re").I)
_GARMENT_COLOR = __import__("re").compile(
    r"\b(terracotta|ochre|olive|sage|indigo|crimson|scarlet|umber|sienna|russet|teal|"
    r"saffron|gr[ea]y|brown|blue|green|red|cream|tan|beige|charcoal|maroon|mustard|rust|"
    r"amber|azure|violet|purple|white|black|gold|golden)\b", __import__("re").I)


def _garment_colors(canon: str) -> set[str]:
    """Colours sitting within ~20 chars of a clothing noun — so 'white-and-gold garments'
    counts but 'grey-haired woman, in wool tunics' does not."""
    cols: set[str] = set()
    for m in _GARMENT_NOUN.finditer(canon):
        window = canon[max(0, m.start() - 20):m.end() + 20]
        for c in _GARMENT_COLOR.finditer(window):
            cols.add(c.group(0).lower())
    return cols


def check_world_colors(pj: dict) -> list[str]:
    """Advisory (non-blocking): a peopled recurring subject should lock a DISTINCT garment
    colour per person in its world canon. Flags a peopled group whose canon pins NO garment
    colour at all — the residual 'same people, different outfits' drift the prompt-author POC
    surfaced (2026-07-12)."""
    out = []
    for name, w in pj["stills"].get("world", {}).items():
        canon = w.get("canon", "")
        if _PEOPLE_CANON.search(canon) and not _garment_colors(canon):
            out.append(f"world:{name} — peopled canon pins no garment colour; lock a DISTINCT "
                       f"colour per person (e.g. terracotta / olive-sage / stone-grey) so the "
                       f"same people wear the same clothes across every still")
    return out


def run_stills(piece_dir: Path, pj: dict, *, render: bool, force: bool, only: set[str],
               no_reuse: bool = False) -> int:
    from render_lint import arm_audit, lint
    jobs = pj["stills"]["jobs"]
    block = False
    for p in check_world(pj):
        print(f"WORLD BLOCK: {p}")
        block = True
    for p in check_refs(pj):
        print(f"REF BLOCK: {p}")
        block = True
    for p in check_world_colors(pj):
        print(f"COLOR NUDGE: {p}")   # advisory — teaches the planner, never blocks
    for slug, job in jobs.items():
        finds = lint(job["prompt"], stage="still")
        bad = [f for f in finds if str(f.get("level", f.get("severity", "warn"))).lower() == "block"]
        print(f"{slug:24} lint: {len(finds)} finding(s){' BLOCK' if bad else ''}")
        for f in finds:
            print("   !", json.dumps(f)[:110])
        block |= bool(bad)
    if block:
        sys.exit("BLOCKED by lint")
    if not render:
        pending = [s for s in jobs if (not only or s in only)
                   and not (piece_dir / "visual" / f"{s}.png").exists()]
        reusable = [] if no_reuse else \
            [s for s in pending if reuse_check(piece_dir, s, jobs[s])]
        paid = len(pending) - len(reusable)
        print(f"\n$0 dry-run. --render to spend (~${paid * SEEDREAM_USD_PER_IMG:.2f}"
              + (f"; {len(reusable)} reusable from siblings: {reusable}" if reusable else "")
              + ").")
        return 0

    from pipeline import cost
    bp = _bp(piece_dir)
    todo = [s for s in jobs if (not only or s in only)
            and (force or not (piece_dir / "visual" / f"{s}.png").exists())]
    bodies = stills_bodies(piece_dir, pj, bp, slugs=set(todo))
    cost.check_budget(pj["piece"], "short", len(todo) * SEEDREAM_USD_PER_IMG)
    for slug in jobs:
        if only and slug not in only:
            continue
        dest = piece_dir / "visual" / f"{slug}.png"
        if dest.exists() and not force:
            print(f"[skip] {slug}")
            continue
        body, _ = bodies[slug]
        if not no_reuse:
            src = reuse_check(piece_dir, slug, jobs[slug])
            if src is not None:
                from render_lint.verify import write_audit
                dest.write_bytes(src.read_bytes())
                write_audit(dest, "PASS", [f"reused byte-identical from {src}"],
                            reviewer=f"reuse:{src.parent.parent.name}")
                cost.record(pj["piece"], "still", "stills", "reuse", pj["stills"]["model"], 1,
                            est_usd=0.0, note=f"{dest.name} reused from "
                            f"{src.parent.parent.name} (saved ~${SEEDREAM_USD_PER_IMG})")
                print(f"{slug:24} -> reused from {src.parent.parent.name} ($0)")
                continue
        req = urllib.request.Request(
            BASE_URL, data=json.dumps(body).encode(),
            headers={"Authorization": f"Bearer {bp._load_key()}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                resp = json.loads(r.read())
        except urllib.error.HTTPError as e:
            print(f"{slug:24} -> HTTP {e.code}: {e.read().decode()[:200]}")
            continue
        url = resp.get("data", [{}])[0].get("url")
        if not url:
            print(f"{slug:24} -> no-url")
            continue
        with urllib.request.urlopen(url, timeout=240) as im:
            dest.write_bytes(im.read())
        arm_audit(dest)   # fail-closed: pending-FAIL sidecar until a real PASS is recorded
        cost.record(pj["piece"], "still", "stills", "byteplus", pj["stills"]["model"], 1,
                    est_usd=SEEDREAM_USD_PER_IMG, est_only=True, note=dest.name)
        print(f"{slug:24} -> ok")
    print("DONE")
    return 0


# ---------------------------------------------------------------- stage: animate
def animate_prompts(pj: dict) -> dict[str, str]:
    an = pj.get("animate") or {"moves": {}}
    base = an.get("base") or INK_BASE   # per-piece verbatim override (e.g. em-dash variant)
    out = {slug: base.format(move=move) for slug, move in an["moves"].items()}
    # living_light channel: {slug: {"target": ..., "light": ...}} — wins over moves for a slug.
    # Prompt change -> clip_src_hash mismatch -> the normal gated re-render. Fail-closed on
    # glitter words (they bloom AI-sparkle; light must be beams/glow/haze/mist, never dots).
    for slug, ll in (an.get("living_light") or {}).items():
        # "prompt" = verbatim override (e.g. a QC'd pilot clip whose exact wording differs
        # from the template — the hash must bind to the words that PRODUCED the clip)
        text = ll.get("prompt") or LIVING_LIGHT_BASE.format(target=ll["target"], light=ll["light"])
        bad = [w for w in _GLITTER_WORDS if w in text.lower()]
        if bad:
            raise ValueError(f"living_light[{slug}]: banned particle word(s) {bad} — "
                             f"describe beams/glow/haze/mist, not dots")
        out[slug] = text
    return out


def clip_src_hash(still: Path, prompt: str, duration: int, aspect_ratio: str) -> str:
    """Content hash binding a clip to exactly what produced it. Any change to the
    still bytes, the motion prompt, or the render params re-renders that clip."""
    import hashlib
    h = hashlib.sha256()
    h.update(still.read_bytes())
    h.update(prompt.encode("utf-8"))
    h.update(f"|{duration}|{aspect_ratio}".encode())
    return h.hexdigest()


def _clip_state(still: Path, out: Path, prompt: str, an: dict) -> str:
    if not out.exists():
        # the QC re-roll mechanic (panel round-4): parking a rejected mp4 in _rejected/
        # (sha left behind) must trigger a re-render, not a hash-current skip
        return "missing"
    """'fresh' (hash matches) | 'stale' (source changed) | 'unhashed' (pre-P1 clip,
    judged by mtime: clip older than its still = stale) | 'missing'."""
    if not (out.exists() and out.stat().st_size > 0):
        return "missing"
    sha_file = out.with_suffix(".src.sha")
    if sha_file.exists():
        want = clip_src_hash(still, prompt, an["duration"], an["aspect_ratio"])
        return "fresh" if sha_file.read_text(encoding="utf-8").strip() == want else "stale"
    # grandfathered clip with no sidecar — the still being newer means it was re-rendered
    # after this clip (the exact shape of the 6 pending audit-fix clips)
    return "stale" if still.exists() and still.stat().st_mtime > out.stat().st_mtime else "unhashed"


def run_animate(piece_dir: Path, pj: dict, *, only: set[str]) -> int:
    if not pj.get("animate"):
        print("(no animate section — this piece's clips come from elsewhere)")
        return 0
    # ROLLOUT GATE (panel fixes 2026-07-14, rounds 2+6): ANY living-page piece must meet
    # the gold-master bar before paid animate. Keyed on ROLLOUT_EPISODES membership OR
    # spec presence (round-6: spec-file-only keying meant a spec renamed mid-A(a)-rewrite
    # stripped every spend control — exactly the window the rewrite creates; a missing
    # spec on a rollout episode now FAILS the gate rather than skipping it).
    # JITB_SKIP_ROLLOUT_GATE=1 = loud escape for a surgical repair on an unupgraded piece.
    import os
    from pipeline.rollout_spend import ROLLOUT_EPISODES
    if (piece_dir.name in ROLLOUT_EPISODES
            or (piece_dir / "visual" / "livingpage_short.spec.json").is_file()):
        if os.getenv("JITB_SKIP_ROLLOUT_GATE", "0") in ("0", "false", "no"):
            from pipeline.rollout_gate import check_piece
            fails = check_piece(piece_dir)
            if fails:
                print("ROLLOUT GATE FAIL - refusing paid animate until the spec meets the bar")
                print("(JITB_SKIP_ROLLOUT_GATE=1 to bypass for a surgical repair - discouraged):")
                for f in fails:
                    print(f"  - {f}")
                return 3
        else:
            print("[gate] ROLLOUT GATE BYPASSED via JITB_SKIP_ROLLOUT_GATE=1 - surgical repairs only")
        # 485cr batch stop-loss at the SAME chokepoint (panel round-3: "run manually at
        # wave gates" was a human-discipline control; this is the fail-closed version).
        from pipeline.rollout_spend import check as rollout_spend_check
        if rollout_spend_check(verbose=False):
            print("ROLLOUT STOP-LOSS BREACHED - refusing paid animate; re-quote the user "
                  "(python -m pipeline.rollout_spend for the breakdown)")
            return 4
    from _hf_animate_short import hf_animate   # carries the PASS-sidecar + budget gates
    pool = piece_dir / "visual"
    clips = pool / "clips"
    clips.mkdir(exist_ok=True)
    an = pj["animate"]
    # BULK GUARD (panel round-5): after a gold-master spec rewrite MANY clips go stale;
    # a bare `--stage animate` would pay for all of them, not the 2 living-light slugs
    # the wave budgeted. Rollout pieces must name their targets (or loudly override).
    from pipeline.rollout_spend import ROLLOUT_EPISODES as _REPS
    if (piece_dir.name in _REPS
            or (piece_dir / "visual" / "livingpage_short.spec.json").is_file()) and not only:
        import os as _os
        if _os.getenv("JITB_ALLOW_BULK_ANIMATE", "0") in ("0", "false", "no"):
            pending = [s for s, p in animate_prompts(pj).items()
                       if _clip_state(pool / f"{s}.png", clips / f"{s}.mp4", p, an)
                       not in ("fresh", "unhashed")]
            if len(pending) > 2:
                print(f"BULK GUARD - {len(pending)} clips would render ({', '.join(pending[:6])}"
                      f"{'...' if len(pending) > 6 else ''}). Name targets with --only, or set "
                      f"JITB_ALLOW_BULK_ANIMATE=1 if a full re-render is truly intended.")
                return 5
    for slug, prompt in animate_prompts(pj).items():
        if only and slug not in only:
            continue
        still, out = pool / f"{slug}.png", clips / f"{slug}.mp4"
        state = _clip_state(still, out, prompt, an)
        if state == "fresh":
            print(f"[skip] {slug} (hash-current)")
            continue
        if state == "unhashed":
            print(f"[skip] {slug} (pre-hash clip, still older than clip — run --stage "
                  f"hash-backfill to bind it)")
            continue
        if state == "stale":
            stale_dir = clips / "_stale_from_bad_stills"
            stale_dir.mkdir(exist_ok=True)
            dest = stale_dir / out.name
            if dest.exists():
                dest.unlink()
            out.replace(dest)
            print(f"[stale] {slug} — old clip moved to {stale_dir.name}/, re-rendering")
        # re-check the batch cap before EACH paid render — one green pre-loop check let a
        # multi-clip run overshoot 485cr (panel round-4, 3 voices; round-6: keyed on
        # episode membership so a mid-rewrite spec rename cannot strip the cap)
        from pipeline.rollout_spend import check as _slcheck, ROLLOUT_EPISODES as _RE2
        if (piece_dir.name in _RE2
                or (piece_dir / "visual" / "livingpage_short.spec.json").is_file()) \
                and _slcheck(verbose=False):
            print(f"ROLLOUT STOP-LOSS hit mid-batch - stopping before {slug}")
            return 4
        ok = hf_animate(still, out, prompt, an["duration"], aspect_ratio=an["aspect_ratio"])
        if ok:
            out.with_suffix(".src.sha").write_text(
                clip_src_hash(still, prompt, an["duration"], an["aspect_ratio"]),
                encoding="utf-8")
        print(f"SAVED {slug}" if ok else f"FAILED {slug}")
    print("DONE")
    return 0


def run_hash_backfill(piece_dir: Path, pj: dict) -> int:
    """One-time: bind existing clips that are demonstrably current (clip newer than its
    still) to their source hash. Clips older than their still are reported STALE and
    left unhashed — animate will re-render them. Clips with no entry in animate.moves
    (borrowed from a sibling / animated ad hoc) can't be hash-bound but their
    still-newer-than-clip staleness is still reported."""
    pool = piece_dir / "visual"
    an = pj.get("animate")
    n_ok = n_stale = 0
    moves = animate_prompts(pj)
    for slug, prompt in moves.items():
        still, out = pool / f"{slug}.png", pool / "clips" / f"{slug}.mp4"
        if not (out.exists() and still.exists()):
            continue
        if out.with_suffix(".src.sha").exists():
            continue
        if still.stat().st_mtime > out.stat().st_mtime:
            print(f"[STALE] {slug}: still is newer than clip — re-animate it")
            n_stale += 1
            continue
        out.with_suffix(".src.sha").write_text(
            clip_src_hash(still, prompt, an["duration"], an["aspect_ratio"]),
            encoding="utf-8")
        print(f"[bound] {slug}")
        n_ok += 1
    clips_dir = pool / "clips"
    if clips_dir.is_dir():
        for mp4 in sorted(clips_dir.glob("*.mp4")):
            if mp4.stem in moves:
                continue
            png = pool / f"{mp4.stem}.png"
            if png.exists() and png.stat().st_mtime > mp4.stat().st_mtime:
                print(f"[STALE:unmanaged] {mp4.stem}: still is newer than clip and no "
                      f"animate.moves entry — re-animate by hand or add a move")
                n_stale += 1
    print(f"backfill: {n_ok} bound, {n_stale} stale")
    return 0


# ---------------------------------------------------------------- engine policy
# choose_engine (P2-2, 2026-07-08): the paid-vs-$0 decision used to live in the
# human's head (which slugs got an animate.moves entry). This encodes the value
# rule so future clusters don't blanket-pay Kling for panel filler:
#   static  — writing/coins (Kling garbles text: feedback-never-animate-writing)
#   dyncam  — used only in grid/inset panels or flash inserts ($0 PIL camera)
#   kling   — hook (first beat) / close (last two) / Christ-sacred subject /
#             long full-bleed holds (>=3s) — the beats that carry the piece
import re as _re

# legible-TEXT surfaces garble under Kling; coins in motion shipped fine (2026-07-06),
# so bare "coins" does NOT trigger — only script-bearing surfaces do.
_WRITING_TOKENS = _re.compile(
    r"\b(scrolls?|script|writing|letters?|lettering|inscriptions?|inscribed|"
    r"titulus|parchment|manuscripts?)\b", _re.I)
_SACRED_TOKENS = _re.compile(r"\b(jesus|christ|crucified|risen|lord)\b", _re.I)


def _slug_usage(spec: dict) -> dict[str, list[dict]]:
    """slug -> [{beat, dur, full, first, last}] from a living-page spec."""
    beats = spec.get("beats") or []
    out: dict[str, list[dict]] = {}
    for i, b in enumerate(beats):
        sources = list(b.get("clips") or []) + list(b.get("panels") or [])
        t = b.get("t") or [0, 0]
        for src in sources:
            slug = (src.get("slug") or "") if isinstance(src, dict) else str(src)
            if not slug:
                continue
            out.setdefault(slug, []).append({
                "beat": i + 1, "dur": round(float(t[1]) - float(t[0]), 2),
                "full": (b.get("tpl") == "full") or (len(sources) == 1),
                "first": i == 0, "last": i >= len(beats) - 2,
            })
    return out


def choose_engine(slug: str, pj: dict, usage: dict[str, list[dict]]) -> tuple[str, str]:
    """-> (engine, reason). Deterministic; advisory (the human keeps final say)."""
    job = pj["stills"]["jobs"].get(slug, {})
    reg = (pj.get("register") or {}).get("stills", {}).get(slug, {})
    text = " ".join([job.get("prompt", ""), reg.get("subject", ""),
                     " ".join(reg.get("elements", []))])
    if _WRITING_TOKENS.search(text):
        return "static", "writing/coins — Kling garbles text"
    uses = usage.get(slug, [])
    if not uses:
        return "dyncam", "not used in the spec"
    full = [u for u in uses if u["full"]]
    if not full:
        return "dyncam", "grid/inset panels only"
    if any(u["first"] for u in full):
        return "kling", "carries the HOOK (first beat)"
    if any(u["last"] for u in full):
        return "kling", "carries the CLOSE (last beats)"
    if _SACRED_TOKENS.search(text):
        return "kling", "Christ/sacred subject"
    longest = max(u["dur"] for u in full)
    if longest >= 3.0:
        return "kling", f"long full-bleed hold ({longest:.1f}s)"
    return "dyncam", f"short full-bleed ({longest:.1f}s)"


def run_engine_plan(piece_dir: Path, pj: dict) -> int:
    """Advisory report: policy engine per slug vs what is currently paid, with the
    projected spend against the episode ceiling. $0, changes nothing."""
    from pipeline import cost
    spec_path = piece_dir / "visual" / "livingpage_short.spec.json"
    if not spec_path.is_file():
        print(f"(no {spec_path.name} — engine plan needs the beats spec)")
        return 1
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    usage = _slug_usage(spec)
    moves = (pj.get("animate") or {}).get("moves") or {}
    n_policy = n_current = 0
    print(f"{'slug':28} {'current':8} {'policy':8} reason")
    for slug in pj["stills"]["jobs"]:
        current = "kling" if slug in moves else (
            "clip" if (piece_dir / "visual" / "clips" / f"{slug}.mp4").exists() else "static/dyncam")
        engine, reason = choose_engine(slug, pj, usage)
        n_current += current in ("kling", "clip")
        n_policy += engine == "kling"
        mark = "" if (engine == "kling") == (current in ("kling", "clip")) else "  <-- differs"
        print(f"{slug:28} {current:8} {engine:8} {reason}{mark}")
    cur_usd = n_current * cost.KLING_USD_PER_CLIP
    pol_usd = n_policy * cost.KLING_USD_PER_CLIP
    spent = cost.episode_total_usd(pj["piece"])
    print(f"\ncurrent Kling: {n_current} clips ~${cur_usd:.2f} · policy: {n_policy} "
          f"~${pol_usd:.2f} (delta ${cur_usd - pol_usd:+.2f})")
    print(f"episode ledger so far: ${spent:.2f} of ${cost.CEILING_USD['short']:.0f} cap")
    return 0


# ---------------------------------------------------------------- score retiming
# The dip windows in piece.json are hand-tuned absolute seconds bound to ONE synth of
# the narration. A re-voice silently desyncs them (the engine audit's biggest silent-
# desync risk). enrich-dips stores WHAT each window covers (the spoken phrase + the
# hand-tuned pre/post padding, derived from the current alignment); retime recomputes
# the windows from those phrases against a fresh audio/alignment.json.
def _load_alignment(piece_dir: Path) -> list[dict] | None:
    p = piece_dir / "audio" / "alignment.json"
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _norm_word(w: str) -> str:
    import re
    return re.sub(r"[^a-z']", "", w.lower())


def _words_in_window(align: list[dict], a: float, b: float) -> list[dict]:
    return [w for w in align if a <= (w["start"] + w["end"]) / 2 <= b]


def _find_span(align: list[dict], phrase: str) -> tuple[float, float]:
    """Start/end of the phrase as a contiguous normalized word run. Fails loud if the
    phrase no longer exists (the narration text changed — retune by hand)."""
    want = [_norm_word(w) for w in phrase.split() if _norm_word(w)]
    have = [_norm_word(w["w"]) for w in align]
    for i in range(len(have) - len(want) + 1):
        if have[i:i + len(want)] == want:
            return align[i]["start"], align[i + len(want) - 1]["end"]
    raise SystemExit(f"retime: phrase not found in fresh alignment: {phrase!r} — "
                     f"the narration changed; re-enrich or hand-tune this dip")


def run_enrich_dips(piece_dir: Path, pj: dict) -> int:
    """One-time per piece: attach phrase + padding meta under each dip window."""
    align = _load_alignment(piece_dir)
    if align is None:
        print("(no audio/alignment.json — cannot enrich)")
        return 1
    sc = pj["score"]
    if sc.get("dips_meta"):
        print("(already enriched)")
        return 0
    metas = []
    for a_s, b_s, _v in sc["dips"]:
        a, b = float(a_s), float(b_s)
        words = _words_in_window(align, a, b)
        if not words:
            raise SystemExit(f"enrich: no words inside dip [{a},{b}]")
        phrase = " ".join(w["w"] for w in words)
        metas.append({"phrase": phrase,
                      "pre": round(words[0]["start"] - a, 2),
                      "post": round(b - words[-1]["end"], 2)})
    cta_a = float(sc["cta_dip"][0])
    cta_words = _words_in_window(align, cta_a, sc["base_seconds"] + sc["outro_hold"])
    sc["dips_meta"] = metas
    sc["cta_meta"] = {"phrase": " ".join(w["w"] for w in cta_words),
                      "pre": round(cta_words[0]["start"] - cta_a, 2) if cta_words else 0.0}
    (piece_dir / "piece.json").write_text(
        json.dumps(pj, indent=2, ensure_ascii=False), encoding="utf-8")
    for m in metas:
        print(f"  dip: pre={m['pre']:+.2f} post={m['post']:+.2f}  \"{m['phrase'][:70]}\"")
    print(f"  cta: pre={sc['cta_meta']['pre']:+.2f}  \"{sc['cta_meta']['phrase'][:70]}\"")
    return 0


def retime_score(piece_dir: Path, pj: dict) -> dict:
    """Recompute base_seconds + every dip window from the piece's stored phrases
    against the CURRENT audio/alignment.json + narration.mp3. Returns the new score
    dict (does not write)."""
    align = _load_alignment(piece_dir)
    sc = dict(pj["score"])
    enriched = (len(sc.get("dips_meta", [])) == len(sc.get("dips", []))
                and bool(sc.get("cta_meta", {}).get("phrase")))
    if align is None or not enriched:
        raise SystemExit("retime: needs audio/alignment.json and enriched dips_meta "
                         "(run --stage enrich-dips first)")
    mp3 = piece_dir / "audio" / "narration.mp3"
    if not mp3.is_file():
        raise SystemExit(f"retime: {mp3} missing — synth the narration first")
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(mp3)], capture_output=True, text=True)
    sc["base_seconds"] = round(float(r.stdout.strip()), 2)
    total = sc["base_seconds"] + sc["outro_hold"]
    # pre/post were stored as (word_start - window_start) / (window_end - word_end),
    # so the window re-derives as [span_start - pre, span_end + post]
    new_dips = []
    for (_a, _b, vol), meta in zip(sc["dips"], sc["dips_meta"]):
        s, e = _find_span(align, meta["phrase"])
        new_dips.append([f"{s - meta['pre']:.2f}", f"{e + meta['post']:.2f}", vol])
    sc["dips"] = new_dips
    s, _e = _find_span(align, sc["cta_meta"]["phrase"])
    sc["cta_dip"] = [f"{s - sc['cta_meta']['pre']:.2f}", sc["cta_dip"][1]]
    if float(sc["dark_trim_end"]) > total:
        print(f"  ! dark_trim_end {sc['dark_trim_end']} exceeds new total {total:.2f} — check the crossfade point")
    return sc


def run_retime(piece_dir: Path, pj: dict) -> int:
    old = pj["score"]
    new = retime_score(piece_dir, pj)
    print(f"  base_seconds: {old['base_seconds']} -> {new['base_seconds']}")
    for (oa, ob, _), (na, nb, _) in zip(old["dips"], new["dips"]):
        print(f"  dip: [{oa},{ob}] -> [{na},{nb}]")
    print(f"  cta: {old['cta_dip'][0]} -> {new['cta_dip'][0]}")
    pj["score"] = new
    (piece_dir / "piece.json").write_text(
        json.dumps(pj, indent=2, ensure_ascii=False), encoding="utf-8")
    print("piece.json retimed — re-run --stage score")
    return 0


# ---------------------------------------------------------------- stage: score
def score_cmd(piece_dir: Path, pj: dict) -> list[str]:
    """The exact ffmpeg argv the old _score.py built (byte-compatible: the numeric
    tokens live in piece.json as VERBATIM strings — "56.0" stays "56.0")."""
    sc = pj["score"]
    mus = ROOT / "music_library" / "clips"
    src = piece_dir / Path(sc["src"])
    out = piece_dir / Path(sc["out"])
    total = sc["base_seconds"] + sc["outro_hold"]
    dips = "".join(
        f"volume=volume={v}:enable='between(t,{a},{b})'," for a, b, v in sc["dips"])
    cta_start, cta_vol = sc["cta_dip"]
    # music prep (2-track dark->grace crossfade + dips) stays here; the
    # narration-pad + duck + mix tail is the SHARED score_mix fragment --
    # the exact place the 2026-07-19 no-apad bug lived, now single-sourced.
    fc = (
        f"[1:a]atrim=0:{sc['dark_trim_end']},{score_mix.AFMT}[d];"
        f"[2:a]atrim={sc['grace_trim'][0]}:{sc['grace_trim'][1]},{score_mix.AFMT}[g];"
        f"[d][g]acrossfade=d={sc['crossfade']}:c1=exp:c2=exp[mch];"
        f"[mch]atrim=0:{total},afade=t=in:st=0:d=1.5,afade=t=out:st={total - 1.5:.2f}:d=1.5,volume=-13dB,"
        + dips +
        f"volume=volume={cta_vol}:enable='between(t,{cta_start},{total})'[mus];"
        + score_mix.mix_tail(total, sc["tpad"])
    )
    return ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
            "-i", str(mus / sc["dark"]), "-i", str(mus / sc["grace"]),
            "-filter_complex", fc,
            *score_mix.output_args(out, preset="medium")]


def run_score(piece_dir: Path, pj: dict) -> int:
    # staleness guard: a re-synth after the windows were set means they may be desynced
    align = piece_dir / "audio" / "alignment.json"
    manifest = piece_dir / "piece.json"
    if align.is_file() and align.stat().st_mtime > manifest.stat().st_mtime:
        print("  ! audio/alignment.json is NEWER than piece.json — the dip windows may "
              "be desynced. Run --stage retime first.")
    r = subprocess.run(score_cmd(piece_dir, pj), capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"score failed:\n{r.stderr[-800:]}")
    print(f"DONE -> {piece_dir / Path(pj['score']['out'])}")
    return 0


# ---------------------------------------------------------------- stage: register
def register_rows(piece_dir: Path, pj: dict) -> list[dict]:
    rg = pj["register"]
    v = piece_dir / "visual"
    common = dict(aspect=rg["aspect"], style=rg["style"], cluster=pj["cluster"],
                  piece=pj["piece"], piece_title=pj["title"], verse=pj["verse"],
                  source=rg["source"], created=rg["created"])
    rows = []
    for slug, s in rg["stills"].items():
        rows.append({**common, "id": f"{rg['id_prefix']}_{slug}", "type": "still",
                     "media": "image", "path": v / f"{slug}.png",
                     "title": s["subject"], "subject": s["subject"],
                     "characters": s["characters"], "elements": s["elements"],
                     "setting": s["setting"], "palette": rg["palette"], "mood": rg["mood"],
                     "doctrine": s["doctrine"], "reuse_scope": s["scope"],
                     "tags": rg["tags_still"], "used_in": rg["used_in"]})
    # clip rows: an explicit kling_slugs list registers exactly those (unconditional,
    # matching the KLING = [...] variant scripts); otherwise scan for existing mp4s
    kling = rg.get("kling_slugs")
    clip_slugs = kling if kling is not None else \
        [s for s in rg["stills"] if (v / "clips" / f"{s}.mp4").exists()]
    for slug in clip_slugs:
        s = rg["stills"][slug]
        clip = v / "clips" / f"{slug}.mp4"
        rows.append({**common, "id": f"{rg['id_prefix']}_{slug}_clip", "type": "clip",
                     "media": "video", "path": clip,
                     "title": s["subject"] + rg["clip_title_suffix"],
                     "subject": s["subject"], "characters": s["characters"],
                     "elements": s["elements"], "setting": s["setting"],
                     "source": rg["clip_source"], "doctrine": s["doctrine"],
                     "reuse_scope": s["scope"], "tags": rg["tags_clip"],
                     "used_in": rg["used_in"]})
    # bespoke extra rows (e.g. a clip borrowed from a sibling piece) — registered only
    # if the referenced file exists, matching the old scripts' `if <path>.exists():`
    for extra in rg.get("extra_rows", []):
        p = piece_dir / extra["path"]
        if not p.exists():
            continue
        rows.append({**common, **extra, "path": p})
    return rows


def run_register(piece_dir: Path, pj: dict) -> int:
    import asset_index as ax
    rows = register_rows(piece_dir, pj)
    for row in rows:
        ax.register(row)
    stills = sum(1 for r in rows if r["type"] == "still")
    print(f"registered {stills} stills + {len(rows) - stills} clips")
    return 0


# ---------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="manifest-driven living-page piece runner")
    ap.add_argument("piece", help="piece folder containing piece.json")
    ap.add_argument("--stage", required=True,
                    choices=["stills", "animate", "score", "register", "all",
                             "hash-backfill", "enrich-dips", "retime", "engine-plan"])
    ap.add_argument("--render", action="store_true", help="stills: actually spend")
    ap.add_argument("--force", action="store_true", help="stills: re-render existing")
    ap.add_argument("--only", default="", help="comma slugs subset")
    ap.add_argument("--no-reuse", action="store_true",
                    help="stills: always render, never copy a sibling's identical PASS still")
    a = ap.parse_args(argv)
    piece_dir = Path(a.piece).resolve()
    pj = load_piece(piece_dir)
    only = {s for s in a.only.split(",") if s.strip()}
    stages = ["stills", "animate", "score", "register"] if a.stage == "all" else [a.stage]
    for st in stages:
        print(f"== {pj['piece']} :: {st} ==")
        rc = 0
        if st == "stills":
            rc = run_stills(piece_dir, pj, render=a.render, force=a.force, only=only,
                            no_reuse=a.no_reuse)
        elif st == "animate":
            rc = run_animate(piece_dir, pj, only=only)
        elif st == "score":
            rc = run_score(piece_dir, pj)
        elif st == "register":
            rc = run_register(piece_dir, pj)
        elif st == "hash-backfill":
            rc = run_hash_backfill(piece_dir, pj)
        elif st == "enrich-dips":
            rc = run_enrich_dips(piece_dir, pj)
        elif st == "retime":
            rc = run_retime(piece_dir, pj)
        elif st == "engine-plan":
            rc = run_engine_plan(piece_dir, pj)
        # gate/stop-loss refusals (3/4) MUST reach the shell — automation was seeing
        # exit 0 on refused paid stages (panel round-4 codex catch)
        if rc:
            return rc
    return 0


if __name__ == "__main__":
    sys.exit(main())
