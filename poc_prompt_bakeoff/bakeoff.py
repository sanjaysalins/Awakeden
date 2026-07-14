"""bakeoff.py — POC: which LLM panel writes the best text-to-image prompt?

The experiment: for each hard scene (cross / walking-on-water / a consistency
pair) hand ONE identical grounded brief to N LLM authors (cursor, claude, gemini,
codex, grok — via the user's local CLI subscriptions, $0). Each writes its own
image prompt. We FREEZE everything else — the inked style wrapper, the negatives,
the NBP renderer, and the character reference — so the ONLY variable is the
author's scene description. Then render every prompt through NBP and lay them out
blind, side by side, per scene.

  Phase 1 (author, $0):   .venv\\Scripts\\python.exe poc_prompt_bakeoff\\bakeoff.py --author
  Phase 2 (render, ~$10): .venv\\Scripts\\python.exe poc_prompt_bakeoff\\bakeoff.py --render
  Gallery (any time):     .venv\\Scripts\\python.exe poc_prompt_bakeoff\\bakeoff.py --gallery

Phase 1 and 2 are split on purpose: review the authored prompts (and the blind
key) before spending a cent on renders.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
sys.path.insert(0, str(REPO))

import config  # noqa: E402
from independent_review import PROVIDERS, run_one  # noqa: E402  (reuse the 5-CLI machinery)
from pipeline.visual_render import _detect_media_type  # noqa: E402

AUTHORS = ["cursor", "claude", "gemini", "codex", "grok"]
STYLE = config.STYLE_REGISTRY["graphic_novel"]  # frozen: inked graphic-novel
BRIEFS_PATH = ROOT / "briefs.json"
AUTHORS_DIR = ROOT / "authors"
RENDERS_DIR = ROOT / "renders"
LOOSE = False  # set by --loose in main(); swaps briefs + dirs + template + render
FULL = False   # set by --full in main(): full brief -> ONE complete paste-ready prompt, rendered verbatim + ref

# --------------------------------------------------------------------------
# The identical author brief (fairness: byte-for-byte the same for every LLM).
# --------------------------------------------------------------------------
AUTHOR_TEMPLATE = """You are a MASTER text-to-image PROMPT ENGINEER for a reverent, biblically
faithful short-video pipeline. Your prompt will be rendered by Google's Nano
Banana Pro (Gemini image model) into ONE vertical 9:16 still.

FIXED — DO NOT REWRITE OR REPEAT THESE. The renderer already wraps your text with
this exact style and these negatives, so do NOT put style words, medium, art
movement, or negatives in your output:
  STYLE (fixed, prepended): {style_base}
  STYLE (fixed, appended):  {style_tail}
  NEGATIVES (fixed):        {negative}

A CHARACTER REFERENCE IMAGE of the canonical face(s) WILL be attached to the
render to lock identity. So do NOT over-describe the face; name the person and
give only light identity anchors (garment, hair, age) — let the reference carry
the likeness.

HARD RULES for the prompt you write:
- FROZEN TABLEAU / state-only: describe ONE held instant, like a photograph.
  Never describe motion, action-in-progress, or a sequence. The camera moves
  later; the scene itself must be frozen.
- ONE dominant subject with a clear focal hierarchy; any extra figures recede
  into shadow and never compete for the eye.
- ANCIENT first-century biblical world only: period-accurate dress, objects,
  architecture, light.
- GROUND every visible detail in the FACT CARD. Honour every directive in it and
  include NONE of its banned anachronisms.
- NO legible text, letters, signs, numerals or writing anywhere in the image.
- Keep hands simple or shadowed (complex finger poses render as garbled blobs).
- POSITIVE phrasing only — never write "no X" or "without X"; instead describe
  the correct end-state.
- 35-70 words, one flowing sentence-like description.

SCENE: {title}
VERSE: {verse_ref}
NARRATION BEAT (what this still must serve):
{beat}

FACT CARD (Scripture-grounded — obey it):
{fact_card}

IDENTITY: {identity_note}
{output_spec}"""

OUTPUT_SINGLE = (
    "\nOutput ONLY the final image prompt, on ONE line, prefixed EXACTLY with "
    "`PROMPT:` and nothing else after it."
)
OUTPUT_PAIR = (
    "\nThis scene has TWO beats (A then B). Output TWO prompts, each on its own "
    "line: first `PROMPT_A:` then `PROMPT_B:`. CRITICAL: the SAME people must be "
    "visually IDENTICAL across both — carry the exact same identity anchors "
    "(ages, garment colours, hair) in BOTH prompts so they read as the same "
    "individuals. Output nothing but the two PROMPT_ lines."
)

# TRUE-INDEPENDENCE template: verse + one bare line, nothing else.
LOOSE_TEMPLATE = """Write the best text-to-image prompt you can for a single vertical 9:16 still
that depicts this Bible moment.

VERSE ({verse_ref}, KJV):
{kjv_text}

MOMENT TO DEPICT: {beat}
{output_spec}"""
LOOSE_OUT_SINGLE = "\nOutput ONLY the prompt, on ONE line, prefixed EXACTLY with `PROMPT:`."
LOOSE_OUT_PAIR = (
    "\nThere are TWO moments (A then B). Output TWO prompts: first `PROMPT_A:` "
    "then `PROMPT_B:`, each on its own line, and nothing else."
)

# FULL template: complete brief in -> ONE finished, paste-ready prompt out.
FULL_TEMPLATE = """You are the PROMPT ENGINEER for a reverent, biblically faithful short-video
pipeline. From the brief below, write ONE complete, self-contained text-to-image
prompt that I will paste DIRECTLY into the image generator (Google Nano Banana
Pro / Gemini image, vertical 9:16) with NO edits. Put EVERYTHING the generator
needs into your prompt — style, subject, mood, quality guards.

REQUIRED STYLE (your prompt MUST specify this look): inked biblical graphic-novel
/ cinematic-manga illustration — bold clean black ink linework and outlines, flat
cel-shaded comic colour, hand-drawn 2D artwork, dramatic ink shadows, reverent and
holy, ancient Near-Eastern period-accurate. NOT an oil painting, NOT
photorealistic, NOT a 3D render, NOT soft airbrushed anime.

A CHARACTER REFERENCE IMAGE of the canonical face(s) is attached at render time,
so name the person and give light anchors (garment, hair, age) but do NOT
over-describe the face — the reference carries the likeness.

RULES your prompt must obey:
- Frozen tableau / state-only: one held instant, no motion or sequence.
- EXACTLY the figures the beat calls for, faces visible to camera, no extra
  people; one dominant subject; extras recede into shadow.
- Ancient first-century biblical world; ground every detail in the FACT CARD and
  include NONE of its banned anachronisms.
- No legible text, letters or signs anywhere; keep hands simple or shadowed.
- Positive phrasing — describe the correct end-state, never "no X".

SCENE: {title}
VERSE: {verse_ref}
NARRATION BEAT: {beat}

FACT CARD: {fact_card}

IDENTITY: {identity_note}
{output_spec}"""
FULL_OUT_SINGLE = (
    "\nOutput ONLY the finished prompt, ready to paste, prefixed EXACTLY with "
    "`PROMPT:` (a single flowing description, up to ~110 words)."
)
FULL_OUT_PAIR = (
    "\nThis scene is TWO beats (A then B). Output TWO complete prompts, `PROMPT_A:` "
    "then `PROMPT_B:`, each on its own line. The SAME people must be visually "
    "IDENTICAL across both — repeat the exact same per-person anchors (age, "
    "garment colour, hair) in BOTH so they read as the same individuals."
)


def load_briefs() -> dict:
    path = (ROOT / "briefs_loose.json") if LOOSE else BRIEFS_PATH
    return json.loads(path.read_text(encoding="utf-8"))


def build_author_prompt(brief: dict, negative: str) -> str:
    if LOOSE:
        if brief["mode"] == "pair":
            beat = f"A) {brief['beat_a']}\nB) {brief['beat_b']}"
            spec = LOOSE_OUT_PAIR
        else:
            beat = brief["beat"]
            spec = LOOSE_OUT_SINGLE
        return LOOSE_TEMPLATE.format(
            verse_ref=brief["verse_ref"], kjv_text=brief["kjv_text"],
            beat=beat, output_spec=spec)
    if FULL:
        if brief["mode"] == "pair":
            beat = f"{brief['beat_a']}\n\n{brief['beat_b']}"
            spec = FULL_OUT_PAIR
        else:
            beat = brief["beat"]
            spec = FULL_OUT_SINGLE
        return FULL_TEMPLATE.format(
            title=brief["title"], verse_ref=brief["verse_ref"], beat=beat,
            fact_card=brief["fact_card"], identity_note=brief["identity_note"],
            output_spec=spec)
    common = dict(
        style_base=STYLE["style_base"],
        style_tail=STYLE["style_tail"],
        negative=negative,
        title=brief["title"],
        verse_ref=brief["verse_ref"],
        identity_note=brief["identity_note"],
        fact_card=brief["fact_card"],
    )
    if brief["mode"] == "pair":
        beat = f"{brief['beat_a']}\n\n{brief['beat_b']}"
        return AUTHOR_TEMPLATE.format(beat=beat, output_spec=OUTPUT_PAIR, **common)
    return AUTHOR_TEMPLATE.format(beat=brief["beat"], output_spec=OUTPUT_SINGLE, **common)


# --------------------------------------------------------------------------
# Extract the prompt(s) from a CLI's raw reply.
# --------------------------------------------------------------------------
def _clean(s: str) -> str:
    s = s.strip().strip("`").strip()
    # take the first non-empty line only (prompts are one line)
    for line in s.splitlines():
        line = line.strip().strip("`").strip()
        if line:
            return line
    return s


def extract_single(raw: str) -> str:
    idx = raw.rfind("PROMPT:")
    body = raw[idx + len("PROMPT:"):] if idx >= 0 else raw
    return _clean(body)


def extract_pair(raw: str) -> tuple[str, str]:
    ia, ib = raw.rfind("PROMPT_A:"), raw.rfind("PROMPT_B:")
    if ia >= 0 and ib > ia:
        a = _clean(raw[ia + len("PROMPT_A:"):ib])
        b = _clean(raw[ib + len("PROMPT_B:"):])
        return a, b
    # fallback: split on the marker however it appears
    parts = raw.split("PROMPT_B:")
    a = _clean(parts[0].split("PROMPT_A:")[-1]) if parts else ""
    b = _clean(parts[1]) if len(parts) > 1 else ""
    return a, b


# --------------------------------------------------------------------------
# Phase 1 — author (run every CLI on every brief, $0).
# --------------------------------------------------------------------------
def phase_author(briefs: dict, authors: list[str]) -> None:
    AUTHORS_DIR.mkdir(parents=True, exist_ok=True)
    negative = briefs["negative"]
    for brief in briefs["briefs"]:
        sid = brief["id"]
        prompt = build_author_prompt(brief, negative)
        (AUTHORS_DIR / f"_brief__{sid}.txt").write_text(prompt, encoding="utf-8")
        print(f"\n=== scene '{sid}' — {len(authors)} authors ===")
        results: dict[str, str] = {}
        with ThreadPoolExecutor(max_workers=len(authors)) as ex:
            futs = {ex.submit(run_one, a, prompt, AUTHORS_DIR): a for a in authors}
            for f in as_completed(futs):
                name, ok, out, dur = f.result()
                results[name] = out
                (AUTHORS_DIR / f"{sid}__{name}.raw.txt").write_text(out, encoding="utf-8")
                print(f"  [{'ok ' if ok else 'FAIL'}] {name:<7} {dur:4.0f}s  ({len(out)} chars)")
        # parse into clean prompt file(s)
        for name in authors:
            raw = results.get(name, "")
            if brief["mode"] == "pair":
                a, b = extract_pair(raw)
                (AUTHORS_DIR / f"{sid}__{name}__A.prompt.txt").write_text(a, encoding="utf-8")
                (AUTHORS_DIR / f"{sid}__{name}__B.prompt.txt").write_text(b, encoding="utf-8")
            else:
                p = extract_single(raw)
                (AUTHORS_DIR / f"{sid}__{name}.prompt.txt").write_text(p, encoding="utf-8")
    print(f"\n[author] done -> {AUTHORS_DIR}")
    print("[author] REVIEW the *.prompt.txt files, then run --render to spend on NBP.")


# --------------------------------------------------------------------------
# Phase 2 — render every authored prompt through NBP (frozen style + ref).
# --------------------------------------------------------------------------
def _render_units(briefs: dict, authors: list[str]) -> list[dict]:
    """Flatten to a list of render jobs: {sid, author, beat, prompt, refs, out}."""
    units = []
    for brief in briefs["briefs"]:
        sid = brief["id"]
        for a in authors:
            if brief["mode"] == "pair":
                for beat, refs_key in (("A", "refs_a"), ("B", "refs_b")):
                    pf = AUTHORS_DIR / f"{sid}__{a}__{beat}.prompt.txt"
                    if not pf.exists() or not pf.read_text(encoding="utf-8").strip():
                        continue
                    units.append(dict(
                        sid=sid, author=a, beat=beat,
                        prompt=pf.read_text(encoding="utf-8").strip(),
                        refs=[] if LOOSE else brief[refs_key],
                        stem=f"{sid}__{a}__{beat}",
                    ))
            else:
                pf = AUTHORS_DIR / f"{sid}__{a}.prompt.txt"
                if not pf.exists() or not pf.read_text(encoding="utf-8").strip():
                    continue
                units.append(dict(
                    sid=sid, author=a, beat="",
                    prompt=pf.read_text(encoding="utf-8").strip(),
                    refs=[] if LOOSE else brief["refs"],
                    stem=f"{sid}__{a}",
                ))
    return units


def phase_render(briefs: dict, authors: list[str]) -> None:
    RENDERS_DIR.mkdir(parents=True, exist_ok=True)
    units = _render_units(briefs, authors)
    est = len(units) * 0.50
    print(f"[render] {len(units)} renders queued (~${est:.2f} at ~$0.50/img). "
          f"Frozen style=inked graphic-novel, model={config.STYLE_REGISTRY['graphic_novel']['still_model']}.")

    # Build one genai client + a ref-upload cache (mirrors NBPProvider).
    from google import genai
    from google.genai import types as gtypes
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    ref_cache: dict[str, str] = {}

    def upload_ref(rel: str) -> str:
        if rel in ref_cache:
            return ref_cache[rel]
        p = REPO / rel
        up = client.files.upload(
            file=str(p),
            config=gtypes.UploadFileConfig(display_name=Path(rel).name, mime_type="image/png"),
        )
        ref_cache[rel] = up.uri
        return up.uri

    base, tail, negative = STYLE["style_base"], STYLE["style_tail"], briefs["negative"]
    done = skipped = failed = 0
    for u in units:
        # idempotent: skip if any image for this stem already exists
        existing = list(RENDERS_DIR.glob(f"{u['stem']}.*"))
        existing = [e for e in existing if e.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
        if existing:
            print(f"  [skip] {u['stem']} — exists")
            skipped += 1
            continue

        if LOOSE or FULL:  # render the author's finished prompt VERBATIM (no wrap)
            full_prompt = u["prompt"]                      # LOOSE: no ref · FULL: ref attached below
        else:
            full_prompt = f"{base} {u['prompt'].rstrip(' ,.')}, {tail}\n\nAvoid: {negative}"
        parts: list = []
        for rel in u["refs"]:
            parts.append({"fileData": {"mimeType": "image/png", "fileUri": upload_ref(rel)}})
        parts.append({"text": full_prompt})

        print(f"  [nbp] {u['stem']} ...", end="", flush=True)
        t0 = time.monotonic()
        try:
            resp = client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=[{"parts": parts}],
                config={"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}},
            )
            cands = getattr(resp, "candidates", None) or []
            img = None
            if cands and cands[0].content:
                for p in cands[0].content.parts:
                    if getattr(p, "inline_data", None) and p.inline_data.data:
                        img = p.inline_data.data
                        break
            if not img:
                finish = getattr(cands[0], "finish_reason", "?") if cands else "no-candidates"
                raise RuntimeError(f"no image bytes (finish={finish})")
            if isinstance(img, str):
                img = base64.b64decode(img)
            ext = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}.get(
                _detect_media_type(img), ".png")
            out = RENDERS_DIR / f"{u['stem']}{ext}"
            out.write_bytes(img)
            (RENDERS_DIR / f"{u['stem']}.prompt.txt").write_text(full_prompt, encoding="utf-8")
            print(f" {len(img):,}b {time.monotonic()-t0:.1f}s -> {out.name}")
            done += 1
        except Exception as e:
            print(f" FAIL: {str(e)[:160]}")
            (RENDERS_DIR / f"{u['stem']}.ERROR.txt").write_text(str(e), encoding="utf-8")
            failed += 1
    print(f"\n[render] done: {done} rendered, {skipped} skipped, {failed} failed -> {RENDERS_DIR}")


# --------------------------------------------------------------------------
# Blind gallery.
# --------------------------------------------------------------------------
RUBRIC = [
    ("Biblical accuracy", "Honours the fact card; no banned anachronism; period-true."),
    ("Faithful theming", "Reads as the right beat; reverent, not sensational."),
    ("Animation-clean", "One dominant subject; simple hands; no legible text; frozen tableau."),
    ("Composition", "Strong focal hierarchy, depth, 9:16 framing."),
    ("Consistency", "(pair only) same people across both frames."),
]


def phase_gallery(briefs: dict, authors: list[str], reveal: bool = False) -> None:
    # stable blind mapping per scene (seeded by scene id, no wall-clock)
    keymap: dict[str, dict[str, str]] = {}
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for brief in briefs["briefs"]:
        rng = random.Random(brief["id"])
        shuffled = authors[:]
        rng.shuffle(shuffled)
        keymap[brief["id"]] = {a: letters[i] for i, a in enumerate(shuffled)}
    (ROOT / "blind_key.json").write_text(json.dumps(keymap, indent=2), encoding="utf-8")
    if reveal:  # show real author names instead of blind letters
        keymap = {b["id"]: {a: a for a in authors} for b in briefs["briefs"]}

    def img_tag(stem: str) -> str:
        hits = [e for e in RENDERS_DIR.glob(f"{stem}.*")
                if e.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
        if not hits:
            return '<div class="miss">— not rendered —</div>'
        rel = f"renders/{hits[0].name}"
        return f'<img loading="lazy" src="{html.escape(rel)}">'

    def prompt_of(stem: str) -> str:
        pf = AUTHORS_DIR / f"{stem}.prompt.txt"
        return pf.read_text(encoding="utf-8").strip() if pf.exists() else ""

    parts = ["""<!doctype html><meta charset=utf-8><title>Prompt bake-off</title>
<style>
 body{background:#111;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:0;padding:24px}
 h1{font-size:22px} h2{margin-top:40px;border-bottom:1px solid #333;padding-bottom:6px}
 .beat{color:#9cf;font-size:13px;max-width:900px;line-height:1.5}
 .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;margin-top:14px}
 .card{background:#1b1b1b;border:1px solid #2a2a2a;border-radius:8px;overflow:hidden}
 .card img{width:100%;display:block;background:#000} .miss{padding:40px;text-align:center;color:#a55}
 .lab{font-weight:700;padding:6px 10px;background:#222;font-size:15px}
 .pr{font-size:11px;color:#9a9;padding:8px 10px;line-height:1.4;max-height:150px;overflow:auto}
 .rub{background:#181818;border:1px solid #333;border-radius:8px;padding:12px 18px;max-width:900px}
 .rub li{margin:4px 0;font-size:13px} code{color:#fc9}
</style>
<h1>POC — which LLM writes the best still-prompt?</h1>
<p class="beat">__INTRO__ __LABELMODE__</p>
<div class="rub"><b>Scoring rubric (1-5 each):</b><ul>"""]
    for name, desc in RUBRIC:
        parts.append(f"<li><b>{name}:</b> {html.escape(desc)}</li>")
    parts.append("</ul></div>")

    for brief in briefs["briefs"]:
        sid = brief["id"]
        km = keymap[sid]
        # order cards by blind letter so the author identity isn't guessable from position
        ordered = sorted(authors, key=lambda a: km[a])
        parts.append(f'<h2>{html.escape(brief["title"])} <span style="color:#666;font-size:13px">({sid})</span></h2>')
        if brief["mode"] == "pair":
            parts.append(f'<p class="beat">{html.escape(brief["beat_a"])}<br>{html.escape(brief["beat_b"])}</p>')
            for beat in ("A", "B"):
                parts.append(f'<h3 style="color:#ccc">Beat {beat}</h3><div class="grid">')
                for a in ordered:
                    stem = f"{sid}__{a}__{beat}"
                    parts.append(
                        f'<div class="card"><div class="lab">{km[a]}</div>{img_tag(stem)}'
                        f'<div class="pr">{html.escape(prompt_of(stem))}</div></div>')
                parts.append("</div>")
        else:
            parts.append(f'<p class="beat">{html.escape(brief["beat"])}</p><div class="grid">')
            for a in ordered:
                stem = f"{sid}__{a}"
                parts.append(
                    f'<div class="card"><div class="lab">{km[a]}</div>{img_tag(stem)}'
                    f'<div class="pr">{html.escape(prompt_of(stem))}</div></div>')
            parts.append("</div>")

    label_line = ("Cards are labelled with the REAL author name."
                  if reveal else
                  "Labels are BLIND (mapping in <code>blind_key.json</code>).")
    if LOOSE:
        intro = ("TRUE-INDEPENDENCE run: each author got ONLY the verse + a one-line beat "
                 "(no fact card, style, anchors, negatives or rules); prompts rendered VERBATIM "
                 "through NBP (no reference, no style injection). This shows each model's own instincts.")
    elif FULL:
        intro = ("FULL-WORKFLOW run: each author got the complete brief and returned ONE finished, "
                 "paste-ready prompt (style and all); rendered VERBATIM + character reference, zero "
                 "touch-up. This is production: brief in -> working prompt out -> still.")
    else:
        intro = ("Frozen: inked graphic-novel style + negatives + NBP renderer + character reference. "
                 "Only the prompt author varies.")
    html_str = "\n".join(parts).replace("__INTRO__", intro).replace("__LABELMODE__", label_line)
    tag = "_loose" if LOOSE else ("_full" if FULL else "")
    out = ROOT / (f"index{tag}_named.html" if reveal else f"index{tag}.html")
    out.write_text(html_str, encoding="utf-8")
    print(f"[gallery] -> {out}")
    if not reveal:
        print(f"[gallery] blind key -> {ROOT / 'blind_key.json'}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--author", action="store_true", help="Phase 1: run the LLM authors ($0)")
    ap.add_argument("--render", action="store_true", help="Phase 2: render via NBP (spends)")
    ap.add_argument("--gallery", action="store_true", help="Build the blind gallery HTML")
    ap.add_argument("--reveal", action="store_true", help="With --gallery: label cards with real author names")
    ap.add_argument("--loose", action="store_true",
                    help="TRUE-INDEPENDENCE run: verse+beat only, verbatim render, separate *_loose dirs")
    ap.add_argument("--full", action="store_true",
                    help="FULL-WORKFLOW run: full brief -> ONE paste-ready prompt, rendered verbatim + ref")
    ap.add_argument("--authors", default=",".join(AUTHORS), help="comma list of author CLIs")
    args = ap.parse_args()
    global LOOSE, FULL, AUTHORS_DIR, RENDERS_DIR
    LOOSE, FULL = args.loose, args.full
    if LOOSE:
        AUTHORS_DIR = ROOT / "authors_loose"
        RENDERS_DIR = ROOT / "renders_loose"
    elif FULL:
        AUTHORS_DIR = ROOT / "authors_full"
        RENDERS_DIR = ROOT / "renders_full"
    authors = [a.strip() for a in args.authors.split(",") if a.strip() in PROVIDERS]
    briefs = load_briefs()
    if not (args.author or args.render or args.gallery):
        ap.error("pick at least one of --author / --render / --gallery")
    if args.author:
        phase_author(briefs, authors)
    if args.render:
        phase_render(briefs, authors)
    if args.gallery:
        phase_gallery(briefs, authors, reveal=args.reveal)
    return 0


if __name__ == "__main__":
    sys.exit(main())
