"""Even So Must the Son of Man Be Lifted Up -- NBP side-by-side test on the
2 hero-tier shots (s08 cross hero, s13 landing), same prompts as
_s1_stills.py, direct Google `gemini-3-pro-image-preview` instead of HF
(kling_omni_image/seedream_v4_5). NOT wired into the main render script --
a one-off comparison. Reuses pipeline.visual_render.NBPProvider's own
proven API-call shape (upload ref -> multi-part contents -> generate_content
with responseModalities=[IMAGE]) but bypasses its Scene/assemble_final_prompt
coupling (that machinery injects the OLDER Baroque-oil style block, wrong
for this sketchbook episode) -- same STYLE+SCENE text already used for the
HF renders, so the comparison isolates the rendering engine, not the prompt.

Google-billed, ~$0.50/still (est) -- separate from the HF credit ledger.

  .venv\\Scripts\\python.exe poc_living_sketchbook/son_of_man_lifted_up/_nbp_test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
JESUS_REF = ROOT / "poc_living_sketchbook" / "cast" / "jesus_ref.png"

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge."
)

JESUS = (
    "Jesus: a Judean man in his early thirties. Face geometry: a strong "
    "straight nose, defined cheekbones, a broad calm forehead, an angular "
    "jaw beneath the beard. Hair: long dark wavy hair falling past the "
    "shoulders, parted center. Beard: short, close-cropped, dark, well-kept. "
    "Skin: sun-weathered olive Mediterranean complexion. Build: lean and "
    "wiry-strong. Eyes: warm deep brown, level and calm. Garment: simple "
    "undyed homespun ankle-length tunic with a woven cord sash -- the same "
    "every appearance. THE SAME man as the reference image -- identical "
    "face, beard, hair, and clothing."
)

SHOTS = [
    ("s03_jesus_split_light", f"{JESUS} CLOSE portrait, cropped at the "
     "chest -- Jesus's head, face, and neck are drawn at natural, "
     "realistic adult human proportions relative to His shoulders and "
     "chest, the SAME head-to-shoulder scale as the reference image, NOT "
     "enlarged, NOT a close-up crop that makes the head read oversized. "
     "Dramatic CHIAROSCURO single-source lighting: an ordinary hand-sized "
     "oil lamp glows from frame-left only, sitting on a stone ledge at a "
     "normal small scale relative to Jesus (not miniature, not toy-"
     "sized) -- the LEFT half of Jesus's face is bright warm gold and the "
     "RIGHT half of his face is in deep, clearly darker shadow -- a "
     "stark, high-contrast half-lit/half-dark split down the center of "
     "his face, not an even wash of light, calm, direct, unflinching "
     "expression."),

    ("s11_christ_face_reverent", f"{JESUS} CLOSE portrait, Christ's face "
     "on the cross, head bowed, eyes closed, soft even light, reverent "
     "and still, no visible wounds, no blood."),

    ("s08_cross_hero", f"{JESUS} HERO, wide, LOW ANGLE looking steeply "
     "upward: Christ genuinely ELEVATED and lifted high on a tall plain "
     "wooden cross, His feet raised well off the ground and resting "
     "together on a small wooden footrest partway up the upright beam -- "
     "His whole body is clearly hoisted into the air above the hilltop, "
     "not standing on the ground in front of the cross. The cross stands "
     "tall enough that the crowd-level ground and rocky hilltop are "
     "visible far BELOW His feet, small in the distance. Arms outstretched "
     "along the crossbeam, head bowed in reverent stillness, against a "
     "darkening Golgotha sky, torn storm clouds gathering behind Him, no "
     "visible wounds, no blood, the whole tableau held as a single iconic "
     "near-still image."),

    ("s13_landing_christ_glory", f"{JESUS} LANDING, sacred stillness: "
     "Christ lifted up on the cross, seen from a respectful distance, arms "
     "extended along the crossbeam, head bowed, radiant warm gold light "
     "surrounding His whole figure, the sky behind Him breaking open with "
     "light, held as a single iconic image, no visible wounds, no blood."),
]


def main():
    if not config.GEMINI_API_KEY:
        raise SystemExit("GEMINI_API_KEY not set")
    from google import genai
    from google.genai import types as genai_types
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    uploaded = client.files.upload(
        file=str(JESUS_REF),
        config=genai_types.UploadFileConfig(display_name="jesus_ref.png", mime_type="image/png"),
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
            cost.record_nbp("LS_SonOfManLiftedUp", "short", "stills",
                             note=f"[nbp-test] {name}")
        except Exception as e:
            print(f"   (ledger skipped: {e})")
        print(f"   ok -> {out}")


if __name__ == "__main__":
    main()
