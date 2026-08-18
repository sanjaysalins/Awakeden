"""One-off: render the Noah-template-style Jesus/Good-Shepherd prompt via NBP
(Nano Banana Pro, gemini-3-pro-image-preview), attaching the existing
ref_jesus_01_ministry.png character reference for consistency with this
project's canonical Jesus look. Standalone -- NOT part of the scene_plan
pipeline, raw prompt sent as-is (no VISUAL_STYLE_BASE/TAIL wrapping).

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_jesus_pov_poc/_gen_shepherd_nbp.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT = Path(__file__).resolve().parent / "jesus_good_shepherd_nbp.png"
REF = Path(
    r"F:\slk\PycharmProjects\PythonProject1\jesus\nano_banana_pro_batch_output"
    r"\jesus_harmony_v1\refs\ref_jesus_01_ministry.png"
)

PROMPT = (
    "Jesus of Nazareth standing outdoors on a grassy hillside near a low dry-stone "
    "sheepfold, with a small flock of sheep gathered calmly around him in a natural "
    "setting. Jesus is a lean, thirty-something Judean man of medium-tall build, with "
    "shoulder-length wavy dark brown hair parted in the middle, a full neat dark beard, "
    "warm dark brown eyes calm and steady, a gentle compassionate expression, and an "
    "olive Mediterranean complexion weathered by outdoor life. He has a straight nose, "
    "an unlined forehead, and strong, roughened hands from ordinary manual work. He is "
    "wearing a simple seamless off-white linen tunic, a deep terracotta-brown mantle "
    "draped over one shoulder, a plain rope belt, and worn leather sandals.\n\n"
    "Show Jesus in the foreground in a three-quarter view, standing with calm, "
    "unhurried presence, one hand resting gently near a nearby sheep. Place a low "
    "dry-stone sheepfold and a few scattered olive trees behind him, clearly visible "
    "in the midground. Arrange the flock of sheep naturally around him, resting and "
    "grazing, calm and orderly, with balanced spacing so the scene feels clear and not "
    "overcrowded.\n\n"
    "Use a normal natural background with grass, bare earth, and open sky, with a "
    "simple distant hillside landscape and soft clouds. The mood should feel ancient, "
    "grounded, and dignified. Illustrative, not photorealistic.\n\n"
    "AVOID: paper texture, collage effects, editorial styling, photorealistic "
    "rendering, modern CGI look, excessive stylization, duplicate figures, cluttered "
    "composition, invented symbols or icons, any lettering, numerals, words, or "
    "captions anywhere, glowing halo or fantasy light effects, and an idealized "
    "bodybuilder physique."
)


def main() -> None:
    from google import genai
    from google.genai import types as genai_types

    client = genai.Client(api_key=config.GEMINI_API_KEY)
    uploaded = client.files.upload(
        file=str(REF),
        config=genai_types.UploadFileConfig(display_name=REF.name, mime_type="image/png"),
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
        sys.exit("NBP returned no candidates")
    parts = candidates[0].content.parts if candidates[0].content else []
    image_bytes = None
    for p in parts:
        if hasattr(p, "inline_data") and p.inline_data and p.inline_data.data:
            image_bytes = p.inline_data.data
            break
    if not image_bytes:
        sys.exit(f"NBP returned no image bytes (finish_reason={getattr(candidates[0], 'finish_reason', '?')})")
    OUT.write_bytes(image_bytes)
    print(f"[ok] {OUT}")
    cost.record("jesus_good_shepherd_poc", "still", "render", "nbp", "gemini-3-pro-image-preview",
                units=1, est_usd=0.5, mode="metered", note="Noah-template-style Good Shepherd render")


if __name__ == "__main__":
    main()
