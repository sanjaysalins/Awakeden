"""Minimal dialogue-driven scene setup, in "The Keyframe Register" (the strongest
candidate from the 10-way exhaustive bake-off) -- proving the STORY can be told,
not just a single portrait. Four shots covering the real blocking/cutting pattern:
wide establishing, dialogue two-shot, Peter's reaction in profile (no-lip-sync
discipline), and the climactic wordless close-up.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_chosen_scene_setup/_render_nbp.py
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

_REGISTER = (
    "Finished animated-feature key frame, muted cinematic gouache matte-painting "
    "style, painterly but fully resolved -- theatrical animation drama polish, not "
    "concept art, not photoreal. Near-monochrome desaturated slate-blue night "
    "palette with one warm amber practical firelight source carrying all "
    "saturation. Strict first-century Judean dress throughout: rough-spun undyed "
    "wool tunics, coarse woven mantles, rope belts, leather sandals, simple head "
    "coverings -- no modern clothing of any kind. "
)
_AVOID = (" AVOID: modern clothing, zippers, buttons, photorealism, photographic "
           "skin, 3D render look, sketch lines, exaggerated cartoon expression, "
           "any text or lettering.")

ITEMS = [
    ("a_wide_establishing", "Shot A — wide establishing (the courtyard)",
     _REGISTER +
     "Vertical 9:16 wide establishing shot: a small stone courtyard at night, "
     "walled in on three sides, one low fire burning at its center as the only "
     "light source. Four or five men in tunics and mantles sit or crouch loosely "
     "around the fire, most in silhouette against the flames. One man -- Peter, "
     "older, grey-streaked beard -- sits slightly apart from the others at the "
     "fire's edge, hood of his mantle up, posture tense and withdrawn. Generous "
     "dark negative space fills the upper two-thirds of the frame -- night sky, "
     "rough stone walls barely visible at the edges. Minimal staging, only the "
     "fire and the seated figures, nothing decorative." + _AVOID),
    ("b_dialogue_twoshot", "Shot B — dialogue two-shot (the accusation)",
     _REGISTER +
     "Vertical 9:16 medium two-shot across the fire: in the foreground, slightly "
     "out of focus and seen from behind/three-quarter back, a young woman (a "
     "servant maid) stands near the flames, her head turned toward Peter, one "
     "hand gesturing slightly as if mid-sentence -- her face turned enough away "
     "from camera that her mouth is not the focus of the shot. In sharper focus "
     "beyond the fire, Peter sits looking back at her, guarded, firelight catching "
     "one side of his face. The fire itself sits between them in the middle of "
     "the frame. Minimal courtyard background, soft dark negative space above." + _AVOID),
    ("c_peter_profile_reaction", "Shot C — Peter's reaction (profile, denying)",
     _REGISTER +
     "Vertical 9:16 medium-close shot: Peter in strict profile, three-quarter "
     "turned away from camera so his mouth is not the focus, firelight catching "
     "the ridge of his brow, nose, and cheekbone from below, the rest of his face "
     "and the back of his head falling into shadow. His posture is stiff, "
     "shoulders drawn up defensively, one hand gripping the edge of his own "
     "mantle. Behind him, soft out-of-focus firelight and the dark suggestion of "
     "the courtyard wall. The framing emphasizes his closed-off body language over "
     "any facial detail -- this is a reaction shot, not a talking shot." + _AVOID),
    ("d_the_look_climax", "Shot D — the climactic look (wordless)",
     _REGISTER +
     "Vertical 9:16 close-up, the emotional peak of the sequence: Peter's face and "
     "upper shoulders, three-quarter view, firelit from below-left, the exact "
     "instant of being seen and recognized -- eyes wide, lips just parted, a real "
     "aching wordless expression, not exaggerated. Deep soft-focus night darkness "
     "fills most of the frame around him; only his face and shoulder catch the "
     "warm firelight, with the faint suggestion of a robed figure's silhouette at "
     "the very edge of frame, turned toward him. Minimal, uncluttered, this shot "
     "carries no dialogue at all." + _AVOID),
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

    print(f"[scene-setup] {len(ITEMS)} stills -> {OUT_DIR}")
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
            cost.record_nbp(EPISODE, "still", "chosen_scene_setup", units=1, note=f"scene-setup: {name}")
            print("ok")
            ok.append((slug, name))
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append((slug, name, str(exc)))
        time.sleep(1)

    print(f"\n[scene-setup] done. {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        for slug, name, err in failed:
            print(f"  FAILED: {slug} ({name}) -- {err}")


if __name__ == "__main__":
    main()
