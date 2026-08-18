"""The Second Look, step 2 of the production plan -- render the 4 Act-1 "plant" stills
only (no animation spend), for the blind-read test in _PLANT_SPEC.md section 4. Plant 2
(the serpent coil) gets two angle variants since it's flagged as highest-risk.

Reference-image-matched to the established Noon Frieze technique (a_pole.png), per the
round-7/8 lesson: text description alone drifts, so we anchor to the real render.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_second_look_format/_plants_nbp.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
from pipeline import cost  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "_plants"
EPISODE = "look_and_live"

REF_IMAGE = (ROOT / "poc_living_sketchbook" / "look_and_live" / "_jesus_pov_poc"
             / "_noon_frieze" / "a_pole.png")

_MATCH = (
    "Match the exact rendering technique of the attached reference image: the same "
    "elongated angular Hercules-lineage silhouette figures, the same weight of dark "
    "contour ink linework, robed figures reading as one continuous flat dark "
    "silhouette mass (only simple cloth-fold lines, no anatomical modeling), the same "
    "warm sun-bleached cream-to-gold daylight palette and gradient sky, the same "
    "minimal negative-space composition discipline. This must look like the same "
    "artist made both images. "
)

_AVOID = (" AVOID: any text, lettering, numerals, captions, or watermarks; muscle or "
          "anatomical linework on any bare skin; photorealism; gore; a crossbar or "
          "cross literally built into the pole itself (a plain vertical pole only) "
          "unless the prompt explicitly describes a shadow reading as a cross.")

STYLES = [
    ("1_moses_raises", "Plant 1 — Moses raises the pole",
     _MATCH +
     "Vertical 9:16 composition, camera at a low frontal angle near Moses's knee "
     "height. Moses, full-length, plants a tall bare wooden pole upright in the sand "
     "with visible physical strain, both hands gripping the timber, dead center in "
     "the frame. A bronze serpent effigy is fixed at the pole's top. In the "
     "background, two smaller wooden tent-support poles stand naturally as ordinary "
     "camp structure, positioned symmetrically roughly 30 degrees to the left and "
     "right of the main pole, far enough back to read as unremarkable camp furniture. "
     "Warm cream-to-gold sky, generous negative space above." + _AVOID),
    ("2a_serpent_coil_a", "Plant 2a — serpent coil, angle A",
     _MATCH +
     "Vertical 9:16 composition, a closer shot on just the top of the pole against "
     "the open sky. A coiled bronze serpent effigy fixed to the pole, its body "
     "curling so that the coil's silhouette, at this exact angle, could be read "
     "either as a serpent's coils OR, ambiguously, as a slumped head and shoulders "
     "resting against a horizontal crossbar shape formed by the serpent's own raised "
     "loop. Warm gold backlight behind it. Minimal, graphic, poster-clean." + _AVOID),
    ("2b_serpent_coil_b", "Plant 2b — serpent coil, angle B",
     _MATCH +
     "Vertical 9:16 composition, a closer shot on just the top of the pole against "
     "the open sky, camera slightly lower than plant 2a for a more frontal read. A "
     "coiled bronze serpent effigy fixed to the pole, its coils arranged so the "
     "silhouette reads first as a serpent, but the topmost coil droops in a way that "
     "could also read as a bowed head, with two lower coils suggesting drooping "
     "shoulders on either side of the pole. Warm gold backlight behind it. Minimal, "
     "graphic, poster-clean." + _AVOID),
    ("3_shadow_cross", "Plant 3 — the pole's shadow",
     _MATCH +
     "Vertical 9:16 composition, low warm sun near the horizon casting very long "
     "shadows across the sand. The bare pole and the serpent effigy's raised coiled "
     "arm together cast one combined long shadow across the ground that unmistakably "
     "reads as a cross shape — a long vertical shadow bar crossed by a shorter "
     "horizontal shadow bar from the serpent's raised coil. The shadow-cross falls "
     "directly across a single suffering figure lying in the sand, full-length, "
     "silhouette only. The pole and serpent themselves, upright, remain plain and "
     "ordinary — only their cast shadow reads as a cross. Warm cream-to-gold ground, "
     "wide negative space." + _AVOID),
    ("4_cruciform_pose", "Plant 4 — Moses's cruciform pose",
     _MATCH +
     "Vertical 9:16 composition, full-length figure. Moses at the exact peak of "
     "raising the pole upright, caught in a held moment: both arms spread wide and "
     "extended at full stretch to either side, one hand still touching the base of "
     "the pole beside him, his body's silhouette at this held instant reading as "
     "cruciform, arms outstretched like a crossbar. The pole stands just to one side "
     "of him, already upright, bronze serpent at its top. Warm cream-to-gold sky, "
     "generous negative space around the figure." + _AVOID),
]


def render_one(client, genai_types, slug, prompt):
    uploaded = client.files.upload(
        file=str(REF_IMAGE),
        config=genai_types.UploadFileConfig(display_name=REF_IMAGE.name, mime_type="image/png"),
    )
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

    print(f"[plants] {len(STYLES)} stills -> {OUT_DIR} (ref: {REF_IMAGE.name})")
    ok, failed = [], []
    for slug, name, prompt in STYLES:
        out_path = OUT_DIR / f"{slug}.png"
        if out_path.exists():
            print(f"  [skip] {slug} (already rendered)")
            ok.append((slug, name))
            continue
        print(f"  [render] {slug} -- {name} ...", end=" ", flush=True)
        try:
            image_bytes = render_one(client, genai_types, slug, prompt)
            out_path.write_bytes(image_bytes)
            cost.record_nbp(EPISODE, "still", "second_look_plants", units=1, note=f"second-look plant: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[plants] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
