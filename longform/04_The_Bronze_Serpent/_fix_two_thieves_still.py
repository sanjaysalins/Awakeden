"""One-off: render a NATIVE 16:9 graphic-novel still to replace the mismatched
reuse_two_thieves_wide asset (flat black/white manga-ink, pulled from
body_foretold_ps2214) at beats 22 and 32 of livingpage_full.spec.json.

New slug: two_thieves_foreground (no "reuse_" prefix -- it's native to this
piece, not sourced from the corpus). Composition deliberately distinct from
this piece's other three-crosses assets (reuse_golgotha_hill_wide = crowd
kneeling below; 13_... = city dim below, storm light; 32_... = respectful
distance, golden evening light): a LOW-ANGLE view from the foot of the hill
with the two thieves' crosses in the foreground, Christ's cross rising behind
and between them.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render
from pipeline import cost

HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked"
SLUG = "04_The_Bronze_Serpent"

NAIL_CLAUSE = (
    "each bare wrist pressed flat against the plain wood with clean skin visible all "
    "around it, a single flat button-sized iron nail head lying flush against the centre "
    "of each wrist, a thin trickle of blood below each nail, plain wood grain touching "
    "skin directly on every other side of the wrist, no bracelet, no wristband, no "
    "wrap, no cuff, no cord anywhere on either arm"
)

SUBJECT_BLOCK = (
    "a single seamless full-bleed inked graphic-novel panel, bold black linework, "
    "wide reverent composition seen from a low angle at the foot of the hill: two "
    "condemned thieves crucified on rough-hewn wooden crosses in the foreground to "
    "either side, clearly two different older men, NOT the same face as the central "
    "figure and NOT the same face as each other -- on the left an older heavy-set "
    "thief with a shaved balding head, a broad weathered face and short grey stubble, "
    "on the right a lean thief with close-cropped dark curly hair, a gaunt hollow-"
    f"cheeked face and no beard, {NAIL_CLAUSE}, their forms turned inward toward the "
    "taller central cross rising behind and between them, the robed Christ CRUCIFIED "
    f"on the central cross with long wavy brown hair and a full beard, both arms "
    f"outstretched along the crossbeam, {NAIL_CLAUSE}, body hanging, head bowed, NOT "
    "standing NOT leaning on the cross, robed at the waist, hands anatomically "
    "correct with five fingers each, pale grey morning "
    "light breaking through thinning storm cloud overhead, bare rock and scattered "
    "stones underfoot, no crowd, no onlookers, grave and majestic, one continuous "
    "image, no frame, no panels, no border, no text, no lettering, no watermark"
)

visual_render.HFProvider.ASPECT = "16:9"
prov = visual_render.HFProvider()
print(f"[provider] hf {config.still_model()} @ 16:9 (VISUAL_STYLE={config.VISUAL_STYLE})")

scene = Scene(
    index=99, slug="two_thieves_foreground", title="Two thieves, foreground -- Christ's cross behind",
    scene_type="single", arc_position="reuse-replacement", framing="low-angle wide",
    purpose="replace mismatched-style reuse_two_thieves_wide (beats 22, 32)",
    rationale="style-mismatch fix, 2026-07-19",
    visible_elements=SUBJECT_BLOCK[:200], emotional_tone="grave, majestic",
    subject_block=SUBJECT_BLOCK, mood_block="reverent, sacred, solemn",
    jesus_variant="passion",
)

png = OUT / "two_thieves_foreground.png"
print(f"[img ] two_thieves_foreground ...", flush=True)
png_bytes = prov.generate(scene)
png.write_bytes(png_bytes)
print(f"       ok ({len(png_bytes):,} b) -> {png}")
cost.record_hf(SLUG, "long", "stills", config.still_model(), note="two_thieves_foreground (reuse fix)")
