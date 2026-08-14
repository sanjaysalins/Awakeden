"""Her Seed -- NBP side-by-side test on s06 (Mary near the empty cross),
same prompt as _s1_stills.py, direct Google `gemini-3-pro-image-preview`
instead of HF (seedream_v4_5). NOT wired into the main render script -- a
one-off comparison. Same STYLE+SCENE text already used for the HF render,
so the comparison isolates the rendering engine, not the prompt.

Google-billed, ~$0.50/still (est) -- separate from the HF credit ledger.

  .venv\\Scripts\\python.exe poc_living_sketchbook/her_seed/_nbp_test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
MARY_S04_OUTPUT = OUT / "s04_mary_annunciation.png"

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge."
)

MARY = (
    "A young woman of Nazareth, modest and plain, no halo, no crown, no "
    "royal dress. Garment: a simple pale homespun robe with a plain veil "
    "covering her hair, drawn loosely over her head and shoulders. Her "
    "face stays AVERTED and bowed, looking down and away -- never turned "
    "to face the viewer, never a clear frontal likeness."
)

SHOTS = [
    ("s06_mary_close",
     f"{MARY} Mary stands in the foreground at a respectful distance, "
     "veiled, her face raised upward toward something unseen ahead of "
     "her -- quiet grief held with reverence, calm contained sorrow, "
     "not despair, not weeping openly. Her hands stay low and close, "
     "clasped quietly together at her waist or held gently against "
     "herself -- NOT raised, NOT outstretched, NOT open to the sky, no "
     "wide gesture of any kind, her whole posture still and folded "
     "inward, a mother's silent grief, not a triumphant or worshipful "
     "pose. Far behind her, a plain wooden cross rises against a "
     "darkening dusk sky -- the cross itself EMPTY, bare, no figure on "
     "it or near it, just the bare wooden cross alone against the sky. "
     "The whole scene is hushed and muted -- deep dusky blues and "
     "violets in the sky, the ground in soft shadow."),
]


def main():
    if not config.GEMINI_API_KEY:
        raise SystemExit("GEMINI_API_KEY not set")
    from google import genai
    from google.genai import types as genai_types
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    uploaded = client.files.upload(
        file=str(MARY_S04_OUTPUT),
        config=genai_types.UploadFileConfig(display_name="s04_mary_annunciation.png", mime_type="image/png"),
    )

    only = set(sys.argv[1:]) or None
    for name, scene in SHOTS:
        if only and name not in only:
            continue
        out = OUT / f"{name}_NBP.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[nbp] {name} ...", flush=True)
        resp = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[{"parts": [
                {"fileData": {"mimeType": "image/png", "fileUri": uploaded.uri}},
                {"text": prompt},
            ]}],
            config={"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}},
        )
        candidates = getattr(resp, "candidates", None) or []
        if not candidates:
            print("   FAILED: no candidates")
            continue
        parts = candidates[0].content.parts if candidates[0].content else []
        image_bytes = None
        for p in parts:
            if hasattr(p, "inline_data") and p.inline_data and p.inline_data.data:
                image_bytes = p.inline_data.data
                break
        if not image_bytes:
            finish = getattr(candidates[0], "finish_reason", "?")
            print(f"   FAILED: no image bytes (finish_reason={finish})")
            continue
        out.write_bytes(image_bytes)
        try:
            cost.record_nbp("LS_HerSeed", "short", "stills",
                             note=f"[nbp-test] {name}")
        except Exception as e:
            print(f"   (ledger skipped: {e})")
        print(f"   ok -> {out}")


if __name__ == "__main__":
    main()
