"""Round 3 proof pass -- one representative photoreal macro still per idea. These
formats (tutorial, ASMR, unboxing) are inherently real-hands/real-object content,
not the illustrated Noon Frieze house style used elsewhere -- so this batch tests
a different production register on purpose.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_round3_test/_render_nbp.py
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
    ("1_unfinishable_tutorial", "The Unfinishable Tutorial — Mark 16",
     "Photorealistic overhead macro shot, shot like a cooking/craft tutorial video, "
     "shallow depth of field, soft window light. A plain stone burial slab, empty, "
     "with a neat pile of folded white linen grave-cloth resting on one corner. "
     "Beside the slab: a small stone mortar and pestle with dried myrrh resin "
     "residue, an unstoppered small clay jar, and a wooden spoon, all clearly "
     "unused in this frame -- laid out and ready, but abandoned mid-preparation. "
     "Numbered step-tutorial graphic style: a small clean on-screen text card in "
     "the lower third reading 'STEP 4' in plain sans-serif (this is the only "
     "lettering allowed in the frame). Dawn light, cool stone textures, dust "
     "motes visible in a light shaft. Vertical 9:16 composition. AVOID: any other "
     "text, numerals, or watermarks; visible faces; a body present anywhere in "
     "frame; stylized or illustrated rendering; gore."),
    ("2_oldest_tutorial", "The Oldest Tutorial — John 13",
     "Photorealistic overhead macro shot, shot like a craft tutorial video, warm "
     "lamplight, shallow depth of field. A pair of real hands (no face visible) "
     "cradling a bare human foot over a wide shallow clay basin of water, mid-pour "
     "from a clay pitcher, water catching the light. A rough linen towel is tied "
     "and knotted around the kneeling person's waist, visible at the top edge of "
     "frame. Stone floor, sandals set aside just outside the frame. A small clean "
     "on-screen text card in the lower third reading 'STEP 3' in plain sans-serif "
     "(the only lettering allowed). Warm intimate lamplight, tactile water and "
     "linen texture. Vertical 9:16 composition. AVOID: any other text, numerals, "
     "or watermarks; visible faces; stylized or illustrated rendering; modern "
     "objects."),
    ("3_earwitness", "Earwitness — Mark 4, the great calm",
     "Photorealistic cinematic still, near-total darkness with one small area of "
     "dim natural light. The interior of a wooden fishing boat at night, seen from "
     "low inside the hull looking toward the stern: a plain wooden pillow or "
     "folded cloak where someone was resting, now empty, water utterly still and "
     "glassy around the boat, faint moonlight breaking through parting storm "
     "clouds on the horizon. Wet rope coiled on the deck, water droplets on the "
     "wood catching the last light. Extremely low-key lighting, most of the frame "
     "in near-black shadow, one soft source of light on the horizon. Vertical 9:16 "
     "composition. AVOID: any text, lettering, numerals, or watermarks; visible "
     "faces or figures; stylized or illustrated rendering; bright even lighting."),
    ("4_appraised", "Appraised — Mark 14, the alabaster flask",
     "Photorealistic macro unboxing-style shot, shallow depth of field, dark "
     "linen surface, single warm key light. A pair of real hands (no face "
     "visible) holding a broken alabaster flask, its slender neck snapped clean "
     "off, thick pale oil pouring and pooling on the dark linen below, catching "
     "the light. The broken neck fragment sits beside the pool of oil. A small "
     "clean on-screen price-card graphic in the upper third reading '300 DENARII' "
     "in plain sans-serif (the only lettering allowed). Rich tactile texture: "
     "alabaster stone grain, glistening oil, dark linen weave. Vertical 9:16 "
     "composition. AVOID: any other text, numerals, or watermarks; visible faces; "
     "stylized or illustrated rendering; modern objects."),
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

    print(f"[round3-test] {len(ITEMS)} stills -> {OUT_DIR}")
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
            cost.record_nbp(EPISODE, "still", "round3_test", units=1, note=f"round3 test: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[round3-test] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
