"""RED-TEAM of the depth-discipline still prompt (2026-07-22). Attacks my own
"this is the win" verdict (n=2, cherry-picked). Renders a harder, fairer sample:
  - REVERENT scene (20, Christ enthroned + veil rent) — does depth cheapen the holy?
  - MULTI-FIGURE scene (24, crowd at the opened veil) — does it handle a crowd or make a mess?
  - VARIANCE: scene 1 x2 more + scene 7 x1 (SAME prompts) — measure the real failure/defect rate.
Same seedream pipeline + ink style block. ~$1.50 (5 stills). Records to the ledger.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_redteam_depth.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render, cost

HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked" / "_depth_test" / "redteam"
OUT.mkdir(parents=True, exist_ok=True)

SCENE1 = (
    "Deep three-layer cinematic composition. Extreme foreground, close to the lens and "
    "slightly out of focus: the dark silhouetted backs, heads and shoulders of a vast hushed "
    "multitude of Israelites, kept in shadow, framing the lower edge of the frame. Sharp "
    "mid-ground: the high priest Aaron, small in golden vestments, stands alone on the pale "
    "stone before the court. Deep background: the towering curtained Tabernacle court rises "
    "severe and dominant into an immense pale dawn sky. Strong shallow depth of field with the "
    "foreground crowd soft and Aaron in crisp focus, a low three-quarter angle looking up past "
    "the crowd toward the lone priest, dramatic scale contrast between the tiny priest and the "
    "colossal sacred tent"
)
SCENE7 = (
    "Extreme macro foreground, huge and close to the lens and in sharp focus: Aaron's two "
    "weathered hands in plain white linen sleeves hold up two small marked lot-stones directly "
    "toward the camera, filling the lower frame; the markings on the stones are only illegible "
    "scratches, not readable text. Mid-ground, soft with shallow depth of field: Aaron's aged "
    "bearded face and a bronze vessel, gently out of focus behind the stones. Deep background, "
    "softest: two goats standing close together before the bronze altar, the tabernacle court "
    "in shadow. Strong shallow depth of field racking all attention onto the lots, a low angle, "
    "Aaron alone, no other priests"
)
SCENE20 = (
    "Deep reverent composition. Foreground, softly framing the lower edge close to the lens: the "
    "torn frayed edge of the great temple veil, its ripped threads catching pale light. Sharp "
    "mid-ground, calm and central: the seated glorified Christ at rest in glory, in a simple "
    "luminous undyed white robe, NOT in any high-priestly breastplate or ornate vestments. Deep "
    "background: a clean shaft of pale light pouring through the painted rip in the veil, drifting "
    "dust, receding columns in shadow. Gentle shallow depth of field keeping Christ crisp, a "
    "steady low reverent angle, sacred holy stillness"
)
SCENE24 = (
    "Deep three-layer composition. Extreme foreground, close to the lens and slightly soft: the "
    "dark silhouetted backs, heads and shoulders of ordinary people in ancient Near-Eastern robes, "
    "tunics and simple head-coverings, framing the lower edge. Sharp mid-ground: more ordinary "
    "people of every kind gathered close at the opened veil, standing still in quiet awe, unafraid. "
    "Deep background: the torn veil blazing with pouring light. Shallow depth of field, a low angle "
    "looking up through the crowd toward the light, a held hush, no single face dominates, no one "
    "mid-stride, all in period ancient dress, no European or medieval dress"
)

# (out_name, scene_id, subject_block)
JOBS = [
    ("rt_20_reverent",  20, SCENE20),
    ("rt_24_multifig",  24, SCENE24),
    ("rt_01b_variance",  1, SCENE1),
    ("rt_01c_variance",  1, SCENE1),
    ("rt_07b_variance",  7, SCENE7),
]


def main():
    visual_render.HFProvider.ASPECT = "16:9"
    prov = visual_render.HFProvider()
    print(f"[provider] hf {config.still_model()} @ 16:9")
    for name, sid, subj in JOBS:
        scene = Scene(
            index=sid, slug=name, title=name, scene_type="single", arc_position="",
            framing="cinematic", purpose="", rationale="", visible_elements=subj[:200],
            emotional_tone="", subject_block=subj, mood_block="reverent, sacred, solemn",
            jesus_variant=None,
        )
        print(f"[img ] {name} ...", flush=True)
        t = time.time()
        png = OUT / f"{name}.png"
        png.write_bytes(prov.generate(scene))
        cost.record_hf("EW01_Two_Goats", "long", "stills", config.still_model(),
                       note=f"[depth-redteam] {name}")
        print(f"       ok ({time.time()-t:.0f}s) -> {png.name}")
    print(f"\n[done] -> {OUT}")


if __name__ == "__main__":
    main()
