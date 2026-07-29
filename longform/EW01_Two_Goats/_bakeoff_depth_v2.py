"""Stratified bake-off of the REVISED depth discipline (2026-07-22), per the
red-team + external panel (4/4 REVISE). Changes vs v1:
  - DROP "shallow depth of field" -> INK-NATIVE depth (overlap + ink line-weight +
    atmospheric recession), explicit anti-photoreal guard.
  - Foreground = objects / silhouette-crowd, NOT near-lens live hands/faces
    (animation-safety: near-lens live subjects invite i2v invention).
  - SACRED/HERO beats = GUARDED calm variant that PRESERVES doctrinal content
    (Christ on the golden throne, plain robe) and uses a steady reverent framing.
10 stills across strata (establishing / action / teaching / sacred / crowd) to
measure the real defect + style-purity + doctrine-preservation rate. ~$3.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_bakeoff_depth_v2.py
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
OUT = HERE / "v1" / "visual_16x9_inked" / "_depth_test" / "bakeoff_v2"
OUT.mkdir(parents=True, exist_ok=True)

# the ink-native depth clause (replaces "shallow depth of field")
DEPTH = (
    "Strong graphic-novel depth built from OVERLAPPING LAYERS and INK LINE-WEIGHT, never "
    "photographic blur: a bold heavily-inked dark foreground shape overlaps into the frame, thick "
    "confident black ink lines in front thinning to fine delicate lines and pale atmospheric haze "
    "in the far distance; flat cel-shaded comic art throughout, crisp clean linework everywhere, "
    "NO depth-of-field blur, NO soft focus, NO photoreal rendering, NO rendered skin detail."
)

# (id, stratum, subject_block)  — foregrounds are objects/silhouettes (animation-safe)
JOBS = [
    (1, "establishing",
     "A deep layered establishing composition. Bold dark heavily-inked foreground: the silhouetted "
     "backs and shoulders of a hushed multitude of Israelites overlapping the lower frame. Mid-ground: "
     "the high priest Aaron, small in golden vestments, alone on the pale stone before the court. Deep "
     "background fading to fine lines and haze: the towering curtained Tabernacle court rising into a "
     "vast pale dawn sky. Low three-quarter angle looking up past the crowd, dramatic scale between the "
     "tiny priest and the colossal tent. " + DEPTH),
    (10, "establishing",
     "A deep layered composition. Bold dark heavily-inked foreground: a rocky desert ledge and boulders "
     "overlapping the near edge. Mid-ground: a lone robed man seen from behind, motionless, dwarfed. "
     "Deep background fading to fine lines and pale haze: a vast bleached desert wadi to a hazy horizon, "
     "far off a single small goat reduced to a dark speck on the cracked valley floor; a held silence. "
     "High wide angle over the ledge. " + DEPTH),
    (7, "action",
     "A deep layered composition. Bold dark heavily-inked foreground: the edge of the bronze altar and a "
     "bronze vessel overlapping the near lower frame. Mid-ground, sharp: Aaron in plain white linen (aged "
     "high priest, long gray hair and full gray beard) holds up two small marked lot-stones over the "
     "vessel, the markings only illegible scratches, not readable text. Deep background fading to fine "
     "lines and haze: two goats standing close together and the tabernacle court in shadow; Aaron alone. "
     "A low committed angle. " + DEPTH),
    (9, "action",
     "A deep layered composition. Bold dark heavily-inked foreground: the silhouetted back and shoulder of "
     "a single robed attendant overlapping the near edge. Mid-ground, sharp: Aaron in plain white linen "
     "(aged high priest, long gray hair and full gray beard) laying both hands on the head of a living "
     "goat, head bowed low in confession, in profile and half-shadowed. Deep background fading to fine "
     "lines and pale haze: the open camp gate and vast pale wilderness beyond; no other priests. Low "
     "three-quarter angle. " + DEPTH),
    (3, "teaching",
     "A deep layered composition down a dim colonnaded passage. Bold dark heavily-inked foreground: a "
     "hanging oil lamp and its chain overlapping the near upper frame. Mid-ground: Aaron in plain white "
     "linen (aged high priest, gray hair and beard) seen from behind, arrested and still before a great "
     "heavy veil at the passage end, head slightly bowed, not walking. Deep background fading to fine "
     "lines and warm haze: the great curtain lit by oil lamps. One-point perspective receding to the "
     "veil. " + DEPTH),
    (12, "teaching",
     "A deep layered composition at dusk. Bold dark heavily-inked foreground: the edge of a stone altar "
     "and a single low flame overlapping the near lower frame. Mid-ground, sharp: Aaron in plain white "
     "linen (aged high priest, gray hair and beard) standing alone and contemplative, lined face lit by "
     "the low flame, eyes calm and human, no other priests. Deep background fading to fine lines and haze: "
     "one faintly smoking altar and one empty road into the darkening waste, the small setting sun well "
     "away from his face. Low reverent angle. " + DEPTH),
    (13, "crowd",
     "A deep layered composition at evening. Bold dark heavily-inked foreground: the silhouetted backs and "
     "shoulders of people overlapping the near lower frame. Mid-ground: a great multitude of Israel "
     "standing at rest in the golden dusk, faces lifted and unburdened, kept soft and in shadow, no one "
     "mid-stride, quiet stillness. Deep background fading to fine lines and golden haze: the open field "
     "and dusk sky. Low three-quarter angle through the crowd. " + DEPTH),
    (20, "sacred",
     "A deep but CALM and REVERENT layered composition. Soft dark foreground (an object, NO figures near "
     "the lens): the torn frayed edge of the great temple veil overlapping the near side. Mid-ground, "
     "sharp central and holy: the glorified Christ SEATED UPRIGHT ON A GOLDEN THRONE — the chair Aaron "
     "never had — at rest in glory, both feet on a footstool, in a simple luminous undyed white robe, NOT "
     "in any high-priestly breastplate or ornate vestments, calm and dignified. Deep background fading to "
     "pale light and haze: a clean shaft of light through the painted rip in the veil, receding columns. "
     "Steady eye-level reverent framing, sacred holy stillness, NO aggressive angle. " + DEPTH),
    (17, "sacred",
     "A REVERENT layered composition. Soft dark foreground (an object): the heavy parted curtain edge "
     "overlapping the near side. Mid-ground, sharp: Christ the true High Priest seen from behind and side, "
     "arrested at the torn radiant veil, one hand laid on the parted curtain, paused at the threshold, not "
     "walking, in a simple luminous undyed white robe, the risen Lord, NOT in any breastplate or ornate "
     "vestments. Deep background fading to bright light and haze: holy glory opening ahead, darkness "
     "behind. Calm reverent angle. " + DEPTH),
    (25, "sacred",
     "A CALM reverent hero composition with gentle layered depth. Soft dark foreground (objects, NO figures "
     "near the lens): the torn veil edge and doorway frame overlapping the near sides. Mid-ground, central "
     "sharp and warm: the risen Christ standing in the full open doorway of light, one hand extended toward "
     "the viewer in welcome, in a simple luminous undyed white robe, NOT in any breastplate or ornate "
     "vestments, face gentle and reverent. Deep background fading to pale light and haze: the way wide open "
     "behind him. Steady eye-level reverent framing on his face and open hand, warm and holy, NO aggressive "
     "macro or angle. " + DEPTH),
]


def main():
    visual_render.HFProvider.ASPECT = "16:9"
    prov = visual_render.HFProvider()
    print(f"[provider] hf {config.still_model()} @ 16:9  ({len(JOBS)} stills)")
    for sid, stratum, subj in JOBS:
        scene = Scene(
            index=sid, slug=f"bo2_{sid:02d}_{stratum}", title=f"{stratum} #{sid}",
            scene_type="single", arc_position="", framing="cinematic", purpose="", rationale="",
            visible_elements=subj[:200], emotional_tone="", subject_block=subj,
            mood_block="reverent, sacred, solemn", jesus_variant=None,
        )
        print(f"[img ] {sid:02d} [{stratum}] ...", flush=True)
        t = time.time()
        png = OUT / f"bo2_{sid:02d}_{stratum}.png"
        png.write_bytes(prov.generate(scene))
        cost.record_hf("EW01_Two_Goats", "long", "stills", config.still_model(),
                       note=f"[depth-bakeoff-v2] #{sid} {stratum}")
        print(f"       ok ({time.time()-t:.0f}s) -> {png.name}")
    print(f"\n[done] -> {OUT}")


if __name__ == "__main__":
    main()
