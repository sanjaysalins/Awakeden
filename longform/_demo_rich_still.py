"""Render ONE rich multi-story 9:16 painting (the whole Day of Atonement in a single
vertical canvas) for the hard-cut gallery-edit demo. ~$0.40."""
import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render

OUT = ROOT / "longform/EW01_Two_Goats/v1/short/visual_9x16_test/gallery_demo"
OUT.mkdir(parents=True, exist_ok=True)
config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
    "Rembrandt lighting, deep shadow and warm golden light, reverent sacred art, muted "
    "earth tones, fine visible brushwork")
config.VISUAL_STYLE_TAIL = "no text, no modern elements, vertical 9:16 composition"

SUBJ = (
    "A single rich multi-story Baroque oil painting, tall vertical canvas, telling the "
    "whole Day of Atonement at once, the elements stacked top to bottom and bleeding softly "
    "into one dim golden scene: at the TOP, the great embroidered temple veil and beyond it "
    "a vast pale desert where a tiny lone goat vanishes toward the horizon; in the MIDDLE, "
    "two goats standing before a smoking stone altar, and beside them a bronze basin of "
    "blood catching the light; in the FOREGROUND at the bottom, the high priest in plain "
    "white linen with his hands raised, his face lifted, and a single oil lamp burning at "
    "his feet. Multiple connected vignettes in one deep chiaroscuro canvas, soft "
    "transitions, no panels or frames, immense and reverent.")

sc = Scene(index=1, slug="atonement_whole", title="The whole Day of Atonement",
    scene_type="unified", arc_position="hero", framing="wide",
    purpose="rich multi-story painting for the gallery hard-cut demo",
    rationale="demo", visible_elements="veil, vanishing goat, two goats, altar, blood basin, priest, lamp",
    emotional_tone="awe, reverent, solemn", subject_block=SUBJ,
    mood_block="reverent, period, multi-story, vertical", jesus_variant=None)

prov = visual_render.HFProvider()   # 9:16
png = OUT / "rich_atonement.png"
print("[img] rendering rich multi-story 9:16 ...", flush=True); t = time.time()
png.write_bytes(prov.generate(sc))
print(f"[img] {png}  ({png.stat().st_size:,} b, {time.time()-t:.0f}s)")
