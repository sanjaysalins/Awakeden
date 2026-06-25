"""One-off A/B: render 3 Two Goats scenes at 16:9 using the SHORTS style base/tail
(config.VISUAL_STYLE_BASE/TAIL default = Flemish-Rubens cinematic) instead of the
long-form aged-oil style. Output -> v1/visual_16x9/_style_compare/short_*.png so we can
set them beside the long-form short-* siblings. Read-only on the locked plan."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render

# SHORTS look at 16:9 (default config base/tail is the shorts style; swap the --ar)
config.VISUAL_STYLE_TAIL = config.VISUAL_STYLE_TAIL.replace("9:16", "16:9")
visual_render.HFProvider.ASPECT = "16:9"
prov = visual_render.HFProvider()

OUT = Path(__file__).resolve().parent / "v1" / "visual_16x9" / "_style_compare"
OUT.mkdir(parents=True, exist_ok=True)

# plain CONTENT only (no oil-painting boilerplate — the shorts style_base carries the look)
SCENES = [
    ("06_two_goats", "the high priest of Israel in plain undyed white linen garments and a linen turban, "
     "standing at the door of the ancient Israelite tabernacle and presenting two calm, still goats side by "
     "side, the dim waiting congregation behind in shadow, one warm shaft of light, ancient near-eastern "
     "setting, reverent and grave, no modern or medieval anything, no text"),
    ("19_cross", "Christ crucified and suspended on a tall wooden cross, both arms nailed wide along the "
     "crossbeam, the body hanging, head fallen and face shadowed, a cloth wound about the waist, seen from a "
     "low angle with the cross off-centre against a vast dawn sky of warm gold and soft rose breaking through "
     "parting cloud, 1st-century Judea, reverent, restrained, not gory, no text"),
    ("25_hero", "the living risen Christ standing within a great torn temple veil, the heavy curtain pulled "
     "wide on either side, robed in white and deep crimson, a dark-haired bearded man with a serene glorified "
     "face, both open pierced hands extended toward the viewer in welcome (clear nail-wounds in the palms, five "
     "fingers each), behind Him only empty radiant golden light and drifting incense haze, no ark, no furniture, "
     "reverent and tender, no text"),
]

for stem, content in SCENES:
    png = OUT / f"short_{stem}.png"
    if png.exists():
        print(f"[skip] {png.name}"); continue
    sc = Scene(index=0, slug=stem, title=stem, scene_type="single", arc_position="", framing="cinematic wide",
               purpose=stem, rationale="", visible_elements=content[:200], emotional_tone="reverent",
               subject_block=content, mood_block="reverent, sacred, intimate, cinematic", jesus_variant=None)
    print(f"[img ] short-style {stem} ...", flush=True)
    png.write_bytes(prov.generate(sc))
    print(f"       ok -> {png.name}")

print(f"\n[done] -> {OUT}")
