"""Contemporary prestige-animation register test -- 4 techniques explicitly
banned from classical fine-art painting media, all on the same beat (Luke 22:61)
in period-locked dress. Reset after the 10-way classical bake-off read as "seen."

  .venv\\Scripts\\python.exe poc_living_sketchbook/_contemporary_register/_render_nbp.py
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
    ("1_knifelight", "Knifelight — prestige impasto",
     "Contemporary prestige-animation still, the look of a 2020s adult animated series: a dimensional, volumetrically lit 3D character form finished entirely in bold visible digital paint strokes — palette-knife scrapes and dry-bristle drags that wrap around the geometry of the face, no outlines, no linework, the brushwork itself is the surface. Close-up framing the face and upper shoulders, three-quarter view: Peter, a weathered first-century Judean fisherman in his fifties, grey-streaked beard, rough-spun undyed wool tunic, coarse woolen mantle pulled over one shoulder, rope belt just visible — strict first-century Judean dress. Night courtyard. Firelight from below-left is the single saturated ember-orange note in an otherwise desaturated slate, umber, and bone palette; the shadow side of his face cools to grey-green. The exact instant of being seen after his denial: eyes just lifted and locked off-frame left, brows knotted, lips parted, tears welling but not falling — grief, shame, recognition, restrained and specific, not exaggerated. Shallow painted depth of field, background smeared into abstract stroke-bokeh; fine digital grain. 9:16 vertical. AVOID: oil painting, watercolor, classical fine art, canvas texture, varnish, photorealism, live-action, modern clothing, any text or lettering."),
    ("2_emberline", "Emberline — graphic novel prestige",
     "Prestige adult graphic-novel streaming-animation still, 9:16 vertical, staged with cinematic widescreen weight. Extreme close-up: Peter, a weathered Galilean fisherman, face and upper shoulders in three-quarter view, at night beside a courtyard fire. Strict first-century Judean dress: rough-spun undyed wool tunic, heavy woolen mantle pulled up over one shoulder, coarse visible weave. The exact instant of being seen after his third denial — eyes just lifting, brows knotting, lips barely parting, grief and recognition arriving together; restrained, specific, aching, fully human expression, not exaggerated. Bold confident brush-ink contour, thick on silhouette and shadow edges, thin on interior facial planes, breaking open where light strikes; rich painterly volumetric rendering inside the line, not flat cel fill. Limited palette: firelight from below-left rendered as bruised rose-copper, shadows deep petrol green-black, one thin pale celadon rim light on the far cheek from off-frame. Background collapsed to flat graphic dark shapes, soft painted ember bokeh, fine film grain, gentle halation. AVOID: oil painting, watercolor, classical fine art, canvas texture, photorealism, modern clothing, any lettering or text."),
    ("3_strokeform", "Strokeform — volumetric CG hybrid",
     "A still from a contemporary prestige animated feature, 9:16 vertical frame. Stylized volumetric CG character with hand-painted brushstroke texture baked directly onto the sculpted 3D forms — dimensional depth, cinematic lighting, painterly surface, the new hybrid theatrical-animation look, not a painting. Close-up: Peter, a weathered Galilean fisherman around sixty, face and upper shoulders in three-quarter view, night, firelit from below-left, warm orange key against cool darkness. The exact instant of being seen — the Lord has turned and looked at him after his third denial: eyes just widening and glassing wet, lips barely parting, brow folding from defiance into grief; a specific, restrained, aching expression, not exaggerated. Grey-streaked curly beard. Strict first-century Judean dress: rough-spun undyed wool tunic, coarse woven mantle drawn over one shoulder, rope belt hinted at frame bottom. Brushstrokes follow the facial planes; highlights stepped into painterly dabs; volumetric fire glow with drifting embers; coarse hatched shading only inside the shadowed half of his face. Background: dark courtyard blur, distant fire. AVOID: oil painting, watercolor, classical fine art, canvas texture, photorealism, photographic skin, modern clothing, any lettering or text."),
    ("4_cockcrow_silver", "Cockcrow Silver — bleach-bypass grade",
     "Vertical 9:16 cinematic frame, a still from a contemporary prestige animated drama series. Clean stylized character rendering, simplified sculpted planes, expressive but not photoreal. Extreme close-up: Peter the fisherman, face and upper shoulders, three-quarter view, night, a high priest's courtyard, lit from below-left by an off-frame charcoal fire. Strict first-century Judean dress: rough-spun undyed wool tunic, a coarse woven mantle pulled up over one shoulder, grey-streaked beard, weathered wind-burned skin. The exact instant of being seen after his third denial — brows drawn upward and inward, lips just parted, eyes wet and fixed past camera, a small devastated stillness; specific, restrained, aching, never exaggerated. GRADE: bleach-bypass silver-retention look — heavily desaturated, high contrast, crushed dense blacks with faint milky edge-bloom, hot bloomed highlights; firelight rendered pale bone-amber, drained of warmth. Anamorphic lens character: very shallow depth of field, oval ember-spark bokeh behind him, one subtle horizontal amber flare low in frame, slight edge distortion, fine pushed film grain in the shadows. AVOID: oil painting, watercolor, classical fine art, canvas texture, visible brushstrokes, photorealism, modern or ambiguous clothing, any lettering or text."),
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

    print(f"[contemporary-register] {len(ITEMS)} stills -> {OUT_DIR}")
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
            cost.record_nbp(EPISODE, "still", "contemporary_register_test", units=1, note=f"contemporary register: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[contemporary-register] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
