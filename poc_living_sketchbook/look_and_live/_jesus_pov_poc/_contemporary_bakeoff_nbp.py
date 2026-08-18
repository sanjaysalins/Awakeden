"""Jesus-POV style pivot, round 3 -- render Fable's 3 "contemporary animation"
takes on the round-2 winner (Ember & Ink) via NBP, same fixed Bible scene
(Moses raising the bronze serpent over the dying wilderness camp, Numbers 21:8).

Sequential on purpose, same pattern as rounds 1 and 2.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_jesus_pov_poc/_contemporary_bakeoff_nbp.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "_contemporary_bakeoff"
EPISODE = "look_and_live"

STYLES = [
    ("e_emberpress", "Emberpress",
     "Vertical 9:16 epic animated-feature establishing shot, contemporary theatrical CG-meets-print style. A vast Israelite encampment at dusk: hundreds of tents receding to a dust-hazed horizon under an enormous molten-amber sky, one low golden sun sitting on the skyline. Foreground: Moses, an aged powerful man in ochre and deep-red robes, strains to plant a tall rough wooden pole upright in the sand, both hands gripping the timber, body angled with real effort; a bronze serpent effigy coils at the pole's top, catching the last sunlight as the hottest highlight in frame. Middle distance: afflicted Israelites across the camp — some collapsed in dust, some rising on one elbow, faces turning upward toward the pole. Style: painterly matte-painting background with no outlines; characters carry bold variable-weight ink contour lines; expressive dry-brush smears on his straining forearms and the kicked-up sand; printed halftone dot texture sits inside the shadow rolloff of every dimensionally lit form, coarse in foreground, fine in distance; subtle teal chromatic-fringe ghost edges only on the sick figures and the serpent's glint. Palette: burnt amber, sienna, dusty rose, deep umber shadows breaking to cool teal. Cinematic volumetric dusk light, long shadows. AVOID: any text, lettering, numerals, captions, watermarks; flat 2D paper texture; comic panels or borders; photorealism; gore; misregistration on Moses."),
    ("f_struck_bronze", "Struck Bronze",
     "Vertical 9:16 cinematic wide establishing shot, epic biblical scale. Dusk over a vast desert wilderness: a sprawling encampment of dark goat-hair tents stretches to a hazy horizon beneath an enormous sky. Low foreground angle: Moses, an older powerfully built Hebrew man in dust-worn layered robes, plants a tall rough-hewn wooden pole upright in the sand with visible physical strain — back bent, shoulders taut, both hands gripping the timber. At the pole's top, a bronze serpent effigy catches the last low sun and burns molten orange. Across the middle distance, afflicted Israelites: some collapsed in the dust, some rising on one elbow, many turning their faces upward toward the pole. Style: prestige adult animation, hand-painted — thick visible oil-impasto brushstrokes describing fully dimensional, volumetrically lit forms; brushwork wraps around anatomy and terrain; no cartoon outlines, no flat cel shading; painterly texture on skin, cloth, sand, and clouds. Grading: moody, desaturated slate-umber-and-bone palette, deep sculptural shadows, subtle film grain; the only saturated color in the entire frame is the hot bronze-orange of the serpent and its reflected sunlight. Single low golden-hour key light, long raking shadows, layered dust haze for depth. AVOID: any text, lettering, numerals, captions, watermarks, logos; cartoon outlines; flat cel shading; smooth airbrush gloss; gore, wounds, or blood; oversaturated multicolor palette; photorealism."),
    ("g_cold_ember", "Cold Ember",
     "Epic vertical wide establishing shot, 9:16 portrait. A vast Bronze Age wilderness encampment at dusk: hundreds of low dark goat-hair tents receding toward a hazy horizon beneath an enormous sky. Foreground: Moses, an older bearded Hebrew man in heavy travel-worn robes, strains with both hands to plant a tall rough wooden pole upright in the sand, body braced against its weight; fixed at the pole's top, a coiled bronze serpent effigy catches the last low sun — the single hottest, most saturated point of light in the frame. Middle distance: afflicted Israelites scattered across the camp, some collapsed in the dust, some rising on one elbow, some turning their faces upward toward the pole. Medium: hand-painted matte-painting background in soft gouache with no outlines; characters rendered cel-shaded with clean dark contour lines, composited over the painting. Grading: contemporary prestige-cinema look — shadows cooled to desaturated steel-teal, blacks crushed deep and clean, midtones muted to dusty clay; only a narrow ember-orange horizon band and the serpent's bronze glint remain saturated. Backlit dust haze reads as anamorphic lens atmosphere with a faint horizontal bloom off the sun; fine 35mm film grain overall. AVOID: any text, lettering, numerals, captions, watermarks, or logos anywhere; no cartoon cuteness, no rainbow palette, no photorealism, no modern objects, no additional divine figures."),
]


def render_one(client, slug, prompt):
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

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    print(f"[contemporary-bakeoff] {len(STYLES)} styles -> {OUT_DIR}")
    ok, failed = [], []
    for slug, name, prompt in STYLES:
        out_path = OUT_DIR / f"{slug}.png"
        if out_path.exists():
            print(f"  [skip] {slug} (already rendered)")
            ok.append((slug, name))
            continue
        print(f"  [render] {slug} -- {name} ...", end=" ", flush=True)
        try:
            image_bytes = render_one(client, slug, prompt)
            out_path.write_bytes(image_bytes)
            cost.record_nbp(EPISODE, "still", "contemporary_style_bakeoff", units=1, note=f"jesus_pov contemporary-style plate: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[contemporary-bakeoff] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
