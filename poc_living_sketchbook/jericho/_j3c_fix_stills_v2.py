"""linefix2: 3 replacement stills -> stills/<name>_v2.png (old kept). HF nano_banana_pro, same STYLE, old still as image ref."""
import sys, importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location("_j3", Path(__file__).parent/"_j3_stills.py")
J = importlib.util.module_from_spec(spec); spec.loader.exec_module(J)
from pipeline import cost
S = J.OUT
SC = {
 "j11_spared": ([J.RAHAB_REF, S/"j11_spared.png"],
  f"{J.RAHAB} She stands calm and upright in the open rubble field in the morning gold light, with her family standing close beside and behind her: exactly one older bearded man (her father), one older woman with a head covering (her mother), and two younger men (her brothers), all clearly separate from each other, normal adult proportions, calm faces. Behind them stands ONE tall fragment of the fallen wall with a small square WINDOW high in it, and a single thin scarlet cord hangs straight down from that window ledge (tied at the window, no loop, no coil, nothing over any door; there is no doorway in the picture). Rubble and settled dust around. First-century Canaanite clothing, no anachronisms. Quiet, spared, still."),
 "j10_stage_c": ([S/"j10_stage_c.png"],
  "THE SAME view as the reference image, same framing: tumbled rubble and settling dust in blue-grey ink wash, ONE tall fragment of wall standing alone with its small square window, and a single thin scarlet cord hanging perfectly straight down from the window ledge, one clean uniform line, thin, ending in a plain end above the ground with no blob and no splash; first warm light on the fragment; plenty of rubble around."),
 "j12_line": ([],
  "A tall page FILLED with a vertical family-tree drawing in loose graphite-and-ink sketch: five or six small modest, fully clothed sketch vignettes stacked top to bottom and filling most of the page, each showing one generation of an ancient family (a robed figure at a window, a farmer with sheaves of grain, a shepherd boy with a small harp, a robed king seated on a stool, a carpenter at a bench, and at the bottom a mother in a long robe and head covering holding her small child, who is fully wrapped in a swaddling cloth, in warm gold light), one single scarlet thread running continuously from the top of the page down through every vignette to the mother and child. Sketches bold and clear, margins small. No readable words anywhere."),
}
for name,(refs,scene) in SC.items():
    out = S/f"{name}_v2.png"
    if out.exists(): print("skip", name); continue
    ok = J.run(J.STYLE+"\n\nSCENE: "+scene, out, refs)
    print(name, ok)
    if ok: cost.record_hf("LS_Jericho","short","stills",J.MODEL,note=f"[jericho-linefix2] {name}_v2")
