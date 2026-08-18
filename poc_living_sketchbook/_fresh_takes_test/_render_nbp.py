"""Fresh-takes proof pass -- one representative test image per idea from the
"Four Fresh Takes" round, all built on the same Genesis 22 (Abraham/Isaac) example
each agent independently worked, for a fair look:

  1. Pentimento       -- one oil-painting still, half grimed / half just-cleaned.
  2. Shadow & Body     -- top-half source (Abraham+Isaac ascending with wood).
  3. Shadow & Body     -- bottom-half source (Christ ascending with the cross).
  4. The Emmaus Loop   -- the hook tableau (boy carries wood, father behind him).

(2) and (3) get composited locally (no extra spend) into the actual split-screen
demo frame by _composite.py, once rendered.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_fresh_takes_test/_render_nbp.py
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

_NOON_FRIEZE_MATCH = (
    "Match the exact rendering technique of the attached reference image: the same "
    "elongated angular Hercules-lineage silhouette figures, the same weight of dark "
    "contour ink linework, robed figures reading as one continuous flat dark "
    "silhouette mass (only simple cloth-fold lines, no anatomical modeling), the same "
    "warm sun-bleached cream-to-gold daylight palette and gradient sky, the same "
    "minimal negative-space composition discipline. "
)
_NOON_AVOID = (" AVOID: any text, lettering, numerals, captions, or watermarks; "
               "muscle or anatomical linework on bare skin; photorealism; gore.")

ITEMS = [
    ("1_pentimento", "Pentimento — grimed/clean split", None,
     "Extreme macro overhead photograph of an aged Baroque oil painting on canvas, "
     "depicting Abraham laying a bundle of wood across his son Isaac's back on a "
     "dawn hillside, a stone altar visible in the middle distance. The LEFT half of "
     "the canvas is covered in centuries of dark yellowed varnish, grime, and fine "
     "cracked craquelure, details barely visible through the murk. The RIGHT half "
     "has just been cleaned by a conservator: vivid, richly saturated restored oil "
     "paint, warm skin tones, deep color, visible fine brushwork. A sharp diagonal "
     "wipe boundary runs down the middle of the frame where grime meets clean paint; "
     "at that boundary, a real human hand in a white cotton glove holds a small "
     "cotton swab mid-stroke, the swab tip stained dark. Raking museum gallery "
     "light. Photorealistic canvas texture, visible craquelure cracks, varnish "
     "sheen on the dirty side. Vertical 9:16 composition. AVOID: any text, "
     "lettering, numerals, or watermarks; modern objects; gore."),
    ("2_top_ascent", "Shadow & Body — top source (Abraham & Isaac)", REF_IMAGE,
     _NOON_FRIEZE_MATCH +
     "Vertical 9:16 composition, low camera angle looking up a bare hillside at "
     "dawn. Full-length figures ascending the hill from lower-frame toward the "
     "upper-frame horizon: Isaac walking ahead, a bundle of wood bound across his "
     "back and shoulders, Abraham following a few steps behind carrying fire and a "
     "knife. The hillside's silhouette rises at a steady diagonal from lower-left "
     "to upper-right. Warm dawn cream-to-gold sky filling the upper half of the "
     "frame, generous negative space above the horizon line, horizon positioned at "
     "roughly the vertical center of the frame." + _NOON_AVOID),
    ("3_bottom_ascent", "Shadow & Body — bottom source (Christ)", REF_IMAGE,
     _NOON_FRIEZE_MATCH +
     "Vertical 9:16 composition, low camera angle looking up a bare hillside, same "
     "framing and hillside silhouette angle as a matching companion image (rising "
     "diagonal from lower-left to upper-right, horizon at roughly the vertical "
     "center of the frame). Full-length figure of Jesus ascending the hill alone, "
     "walking in the same direction and screen position as the companion image's "
     "lead figure, a rough wooden crossbeam bound across his shoulders and back, "
     "head bowed slightly under the weight, full-length, visible head to feet. "
     "Warm dawn cream-to-gold sky filling the upper half of the frame, generous "
     "negative space above the horizon." + _NOON_AVOID),
    ("4_emmaus_hook", "The Emmaus Loop — hook tableau", REF_IMAGE,
     _NOON_FRIEZE_MATCH +
     "Vertical 9:16 composition, dawn hillside. A boy, full-length, walks up a bare "
     "hill path carrying a bundle of wood bound across his shoulders and back. A "
     "few steps behind him, an older man follows, carrying a small torch/firepot in "
     "one hand and a knife tucked at his belt. Ahead of them at the frame's upper "
     "edge, a plain empty thicket of bare thornbush sits beside the path, no animal "
     "in it. Warm dawn cream-to-gold sky, generous negative space, wide establishing "
     "framing with both figures small against the hillside." + _NOON_AVOID),
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

    print(f"[fresh-takes] {len(ITEMS)} stills -> {OUT_DIR}")
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
            cost.record_nbp(EPISODE, "still", "fresh_takes_poc", units=1, note=f"fresh-takes test: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[fresh-takes] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
