"""Jesus-POV style pivot, round 8 -- diagnosis from round 7: Moses (round 5) reads
as one flat dark mass because he's fully robed, almost no bare skin. Christ on the
cross is traditionally bare-chested, and that exposed skin is where NBP keeps adding
muscle/rib linework and skin-tone gradient modeling, even with the round-5 reference
image attached. This round forces the same flat-silhouette treatment onto the skin
itself -- no anatomical modeling at all, treated exactly like robed cloth.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_jesus_pov_poc/_cross_flat_skin_nbp.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "_cross_flat_skin"
EPISODE = "look_and_live"

REF_IMAGE = Path(__file__).resolve().parent / "_noon_frieze" / "a_pole.png"

PROMPT = (
    "Match the EXACT rendering technique of the attached reference image: the same "
    "elongated angular Hercules-lineage silhouette figures, the same weight and "
    "confident quality of dark contour ink linework, the same warm minimal "
    "negative-space composition discipline. In the reference, Moses's entire robed "
    "body reads as ONE continuous flat dark silhouette shape -- no muscle definition, "
    "no anatomical modeling, no interior linework beyond a few simple cloth-fold "
    "lines, just a flat dark mass with a soft outer light-to-shadow gradient at its "
    "very edge. Apply that EXACT same flat-silhouette treatment to Christ's body on "
    "the cross, INCLUDING his bare skin -- his exposed torso, arms, and legs must "
    "read as one continuous flat dark silhouette shape exactly like Moses's robe "
    "does, with NO ab or rib linework, NO muscle contour lines, NO skin-tone "
    "gradient modeling, NO anatomical shading of any kind. Treat his skin with the "
    "identical flat-shape treatment cloth gets in the reference. Only the loincloth "
    "gets one or two simple fold lines, same as Moses's robe folds.\n\n"
    "Vertical 9:16 composition. A vast, warm sun-bleached cream-to-gold gradient sky "
    "and ground, same palette family as the reference image. Centered, a tall simple "
    "wooden cross bearing the full-length figure of Jesus, entire body clearly "
    "visible head to feet, arms outstretched along the crossbeam, head inclined "
    "gently, one continuous flat dark silhouette shape. The cross and the rim of "
    "Christ's silhouette carry a warm reserved bronze-gold glow, the single most "
    "saturated color in the frame, echoing the bronze on the serpent effigy earlier "
    "in the story. Generous open negative space around the figure. Monumental, "
    "reverent, still.\n\n"
    "AVOID: any text, lettering, numerals, captions, watermarks, or logos anywhere; "
    "any muscle, rib, or ab linework on the torso; any anatomical shading or "
    "skin-tone gradient modeling; a crown of thorns rendered as separate fine "
    "linework (omit it or keep it as a simple flat dark shape if included); "
    "photorealism; gore; the figure must be full-length, head to feet, never "
    "cropped to a headshot."
)


def render_one(client, genai_types):
    uploaded = client.files.upload(
        file=str(REF_IMAGE),
        config=genai_types.UploadFileConfig(display_name=REF_IMAGE.name, mime_type="image/png"),
    )
    resp = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[{"parts": [
            {"fileData": {"mimeType": "image/png", "fileUri": uploaded.uri}},
            {"text": PROMPT},
        ]}],
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

    if not REF_IMAGE.exists():
        sys.exit(f"reference image not found: {REF_IMAGE}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    out_path = OUT_DIR / "cross_flat_skin.png"

    if out_path.exists():
        print(f"[skip] {out_path} already rendered")
        return

    print(f"[render] cross, flat-skin technique (ref: {REF_IMAGE.name}) ...", end=" ", flush=True)
    image_bytes = render_one(client, genai_types)
    out_path.write_bytes(image_bytes)
    cost.record_nbp(EPISODE, "still", "cross_flat_skin_fix", units=1, note="jesus_pov cross, flat-silhouette-on-skin fix")
    print("ok")
    print(f"[done] {out_path}")


if __name__ == "__main__":
    main()
