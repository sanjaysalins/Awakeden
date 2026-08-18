"""Thread-tracing systems proof pass -- 2 representative stills per system (a mid-
episode "stop" and the Christ resolution), using each system's own worked example
from the design pass: Rubrica ("The Door"), Meridian ("Where Is the Lamb?"),
The Scarlet Line (kaphar / atonement).

  .venv\\Scripts\\python.exe poc_living_sketchbook/_thread_systems_test/_render_nbp.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent
EPISODE = "fresh_takes_poc"

ITEMS = [
    ("1a_rubrica_stop", "Rubrica — stop (Exodus 12, the doorframe)",
     "Extreme macro overhead photograph of an aged illuminated manuscript scroll, "
     "warm raking candlelight from one side, visible parchment fiber and slight "
     "cockling. A stitched seam runs across the frame where two parchment panels "
     "join. Dense lines of black iron-gall calligraphy fill the page. A single "
     "line of wet vermilion-red ink, glossy where fresh and matte where dried, "
     "traces from the text and runs directly onto a small painted doorframe motif "
     "sketched in the margin -- the red ink line itself forms two vertical marks "
     "and one horizontal mark across the little doorframe drawing, like blood "
     "struck on doorposts and a lintel. A real steel-nib pen rests beside the "
     "wet ink, faint reflection of candlelight on the nib. Rich texture: fibrous "
     "paper, ink bleed, feathering at the line's edges. Vertical 9:16 composition. "
     "AVOID: any modern text, watermarks; a full readable English sentence "
     "(illegible calligraphic density only); photorealistic gore; modern objects."),
    ("1b_rubrica_gold", "Rubrica — resolution (gold flare)",
     "Extreme macro overhead photograph of an aged illuminated manuscript, warm "
     "candlelight. A line of vermilion-red ink runs across the parchment and "
     "arrives at a burnished gold-leaf panel -- the moment it touches the gold "
     "leaf, the gold catches raking candlelight and flares brilliantly, small "
     "specular highlights scattered across the leaf's hammered texture. A small "
     "painted door-shaped glyph sits within the gold panel, the red line passing "
     "through its center. Rich warm palette: cream parchment, lamp black ink, "
     "vermilion red, brilliant burnished gold, deep shadow at the frame edges. "
     "Vertical 9:16 composition, the gold panel positioned in the upper-center of "
     "frame. AVOID: any readable modern text or watermarks; photorealistic faces; "
     "modern objects; harsh even lighting."),
    ("2a_meridian_stop", "Meridian — stop (Genesis 22, the plate)",
     "A clean modern data-visualization video frame, dark ink-navy chart "
     "background. A thin horizontal baseline with slender proportional vertical "
     "bars representing books of the Bible, rendered in flat slate-grey, "
     "labeled beneath in small letterspaced cream grotesk type. A bright scarlet "
     "line has drawn itself along the baseline and stops at one bar, forming a "
     "small ring marker on it; beside the ring, a small typeset coordinate label "
     "reads clean and legible: 'GEN 22:8'. A circular plate has opened beside the "
     "marker via a compass-arc wipe, containing a warm oil-painted illustration "
     "(Baroque devotional painting style) of a boy carrying a bundle of wood up a "
     "hillside, an older man following -- rendered with real painterly brushwork, "
     "contrasting richly against the cold flat vector chart around it. Vertical "
     "9:16 composition. AVOID: any other readable text; illegible or garbled "
     "lettering in the coordinate label; modern objects; gore."),
    ("2b_meridian_gold", "Meridian — resolution (gold kindle-back)",
     "A clean modern data-visualization video frame, dark ink-navy chart "
     "background, full-bleed moment. A proportional timeline of slender vertical "
     "bars representing books of the Bible runs across the frame; a scarlet line "
     "that has been drawing along the baseline now ignites into brilliant gold "
     "light at one bar near the right side of the chart, and the gold light is "
     "visibly spreading backward along the line toward the left, each earlier "
     "ringed stop-marker along the line flashing gold in sequence like a chain "
     "reaction of light. One circular plate near the golden point holds a warm "
     "oil-painted illustration of a lamb, glowing warmly where the gold light "
     "touches it. Palette: ink-navy ground, cream linework, brilliant gold light, "
     "scarlet line. Vertical 9:16 composition. AVOID: any readable text or "
     "watermarks; modern objects; photorealism outside the painted plate."),
    ("3a_scarletline_stop", "The Scarlet Line — stop (the mercy-seat lid)"
     , "Photorealistic macro photograph, extreme close focus, warm single-source "
     "brass lamplight against near-total black background. A pair of real weathered "
     "hands (no face visible) place a small palm-sized gilded object shaped like a "
     "flat lid with two small facing winged figures on it, onto a dark waxed oak "
     "table surface. Beside the object, a turned brass pin sits in a shallow "
     "brass-rimmed socket set into a groove in the wood. A strand of scarlet linen "
     "cord twisted with fine gold wire loops loosely around the pin, catching the "
     "lamplight. A small slate strip beside it has a chapter-and-verse reference "
     "freshly chalked in white. Visible dust motes drift through the lamp beam. "
     "Rich macro texture: oak grain, gold leaf, linen fiber, chalk dust. Vertical "
     "9:16 composition. AVOID: any modern text or watermarks; visible faces; "
     "modern objects; gore."),
    ("3b_scarletline_pull", "The Scarlet Line — resolution (the pull)",
     "Photorealistic macro photograph, warm single brass lamplight against total "
     "black background, slight motion blur suggesting a fast camera move down the "
     "length of a taut cord. A single straight line of scarlet linen cord twisted "
     "with gold wire runs the full length of the frame, perfectly taut, catching "
     "the lamplight in a bright specular highlight along its length, every loop "
     "and slack point pulled tight. At the far end of the frame, small and in "
     "sharp focus, an old scarred olive-wood block holds one hand-forged iron "
     "nail, the cord's end tied off around it, warm brass lamp glowing just beside "
     "it. The near end of the frame is a soft blur of dark oak table. Vertical "
     "9:16 composition, the nail positioned in the upper third. AVOID: any modern "
     "text or watermarks; visible faces; modern objects; gore."),
]


def render_one(client, genai_types, prompt):
    resp = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[{"parts": [{"text": prompt}]}],
        config={"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}},
    )
    candidates = getattr(resp, "candidates", None) or []
    if not candidates:
        raise RuntimeError("NBP returned no candidates")
    parts = candidates[0].content.parts if candidates[0].content else []
    for p in parts:
        if hasattr(p, "inline_data") and p.inline_data and p.inline_data.data:
            return p.inline_data.data
    raise RuntimeError(f"NBP returned no image bytes (finish_reason={getattr(candidates[0], 'finish_reason', '?')})")


def main() -> None:
    from google import genai
    from google.genai import types as genai_types

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    print(f"[thread-systems] {len(ITEMS)} stills -> {OUT_DIR}")
    ok, failed = [], []
    for slug, name, prompt in ITEMS:
        out_path = OUT_DIR / f"{slug}.png"
        if out_path.exists():
            print(f"  [skip] {slug} (already rendered)")
            ok.append((slug, name))
            continue
        print(f"  [render] {slug} -- {name} ...", end=" ", flush=True)
        try:
            image_bytes = render_one(client, genai_types, prompt)
            out_path.write_bytes(image_bytes)
            cost.record_nbp(EPISODE, "still", "thread_systems_test", units=1, note=f"thread-system test: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[thread-systems] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
