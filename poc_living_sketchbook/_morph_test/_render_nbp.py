"""Morph mechanic test -- "Knew It Not" (Emmaus, Luke 24). Render a composition-
matched before/after pair: a photoreal modern kitchen frame and a painted biblical
frame, same hand position and table geometry, so the crossfade composite (_blend.py)
can preview what the actual on-screen morph would look like before any animation
spend.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_morph_test/_render_nbp.py
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

REF_IMAGE = (ROOT / "poc_living_sketchbook" / "look_and_live" / "_jesus_pov_poc"
             / "_noon_frieze" / "a_pole.png")

ITEMS = [
    ("a_modern", "Modern frame — kitchen table", None,
     "Photorealistic close-up POV shot, shallow depth of field, shot on a modern "
     "phone camera, warm late-afternoon light through a kitchen window. A pair of "
     "hands hovers over a fresh loaf of bread on a plain wooden kitchen table, mid "
     "gesture, about to break it. Across the small table, one chair sits empty. "
     "Ordinary modern kitchen background, softly out of focus: a tile backsplash, a "
     "kettle, a phone face-down on the table. Vertical 9:16 composition, the hands "
     "and bread positioned in the lower-center third of the frame, the empty chair "
     "visible on the far side of the table in the middle distance, camera angle "
     "low and close as if the viewer is sitting at the table. Muted, natural, "
     "unremarkable color grading -- this is meant to look like real ordinary life, "
     "not stylized. AVOID: any text, lettering, numerals, or watermarks; visible "
     "faces; stylized or illustrated rendering; dramatic lighting."),
    ("b_biblical", "Biblical frame — the supper at Emmaus", REF_IMAGE,
     "Match the exact rendering technique of the attached reference image: the same "
     "elongated angular Hercules-lineage silhouette figures, the same weight of dark "
     "contour ink linework, robed figures reading as one continuous flat dark "
     "silhouette mass, warm lamp-lit palette (not the bright daylight register -- "
     "this is an evening interior scene). Vertical 9:16 composition, same camera "
     "angle and table geometry as a companion modern photograph: a pair of hands "
     "hovers over a fresh loaf of bread on a plain wooden table, mid gesture, about "
     "to break it, positioned in the lower-center third of the frame. Across the "
     "small table, seated in the same chair position as the companion image's empty "
     "chair, a robed full-length figure -- Christ, though his face is turned slightly "
     "down and partly in shadow, not the focus of this frame. A small clay oil lamp "
     "on the table casts warm amber light across both sets of hands and the bread. "
     "Plain plastered interior wall behind, minimal detail, generous warm shadow. "
     "AVOID: any text, lettering, numerals, or watermarks; muscle or anatomical "
     "linework on bare skin; a fully lit or centrally staged face; photorealism; "
     "modern objects."),
]


def render_one(client, genai_types, ref_image, prompt):
    parts = []
    if ref_image is not None:
        uploaded = client.files.upload(
            file=str(ref_image),
            config=genai_types.UploadFileConfig(display_name=ref_image.name, mime_type="image/png"),
        )
        parts.append({"fileData": {"mimeType": "image/png", "fileUri": uploaded.uri}})
    parts.append({"text": prompt})
    resp = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[{"parts": parts}],
        config={"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}},
    )
    candidates = getattr(resp, "candidates", None) or []
    if not candidates:
        raise RuntimeError("NBP returned no candidates")
    result_parts = candidates[0].content.parts if candidates[0].content else []
    for p in result_parts:
        if hasattr(p, "inline_data") and p.inline_data and p.inline_data.data:
            return p.inline_data.data
    raise RuntimeError(f"NBP returned no image bytes (finish_reason={getattr(candidates[0], 'finish_reason', '?')})")


def main() -> None:
    from google import genai
    from google.genai import types as genai_types

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    print(f"[morph-test] {len(ITEMS)} stills -> {OUT_DIR}")
    ok, failed = [], []
    for slug, name, ref, prompt in ITEMS:
        out_path = OUT_DIR / f"{slug}.png"
        if out_path.exists():
            print(f"  [skip] {slug} (already rendered)")
            ok.append((slug, name))
            continue
        print(f"  [render] {slug} -- {name} ...", end=" ", flush=True)
        try:
            image_bytes = render_one(client, genai_types, ref, prompt)
            out_path.write_bytes(image_bytes)
            cost.record_nbp(EPISODE, "still", "morph_mechanic_test", units=1, note=f"morph test: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[morph-test] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
