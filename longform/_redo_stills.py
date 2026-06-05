"""Re-render specific 16:9 stills from their (edited) scene_plan.json subject_blocks.
Backs up the stale PNG + MP4 (+ directional _cont clips) into _redo_backup/ FIRST so the
idempotent batch scripts don't skip them. Does NOT auto-bank (keeps the image_library plates
intact until the film is re-locked). I QC each render at full res myself.

  python longform/_redo_stills.py 1 3 7
"""
import sys, json, re, time, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render

V1 = ROOT / "longform" / "01_Isaiah_53_Suffering_Servant" / "v1"
OUT = V1 / "visual_16x9"
BACKUP = OUT / "_redo_backup"
BACKUP.mkdir(exist_ok=True)

config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
    "Rembrandt lighting, deep shadow and warm golden light, reverent sacred art, muted "
    "earth tones, fine visible brushwork")
config.VISUAL_STYLE_TAIL = "no text, no modern elements, cinematic 16:9 widescreen composition"
visual_render.NBPProvider.ASPECT_RATIO = "16:9"

# jesus ref variants (only where the central subject IS the canon Christ)
JESUS = {6: "passion", 15: "resurrection", 16: "passion", 18: "resurrection",
         19: "resurrection", 20: "resurrection", 21: "resurrection"}

def slug(t): return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")[:40]

argv = sys.argv[1:]
ref_paths = []
if "--ref" in argv:
    i = argv.index("--ref")
    ref_paths = [Path(argv[i + 1])]
    argv = argv[:i] + argv[i + 2:]
ids = [int(a) for a in argv]
if not ids:
    sys.exit("usage: _redo_stills.py <id> [<id> ...] [--ref <continuity_png>]")
if ref_paths:
    print(f"[ref] continuity reference: {ref_paths[0]}")

plan = json.loads((OUT / "scene_plan.json").read_text(encoding="utf-8"))
prov = visual_render.NBPProvider()
scenes = {s["id"]: s for s in plan["scenes"]}

for sid in ids:
    s = scenes[sid]
    stem = f"{sid:02d}_{slug(s['title'])}"
    png = OUT / f"{stem}.png"
    # back up stale png + mp4 + directional continuations (so the batch scripts won't skip)
    stamp = time.strftime("%H%M%S")
    for p in [png, png.with_suffix(".mp4"), *OUT.glob(f"{stem}_cont*.mp4")]:
        if p.exists():
            dst = BACKUP / f"{p.stem}.{stamp}{p.suffix}"
            shutil.move(str(p), str(dst))
            print(f"  [backup] {p.name} -> _redo_backup/{dst.name}")
    scene = Scene(
        index=sid, slug=slug(s["title"]), title=s["title"], scene_type="single",
        arc_position=s["mvt"], framing="cinematic wide", purpose=s["title"], rationale=s["mvt"],
        visible_elements=s["subject_block"][:200], emotional_tone=s["mvt"],
        subject_block=s["subject_block"], mood_block="reverent, sacred, solemn, Baroque",
        jesus_variant=JESUS.get(sid),
    )
    print(f"[img ] {sid:02d} {s['title'][:42]} (jesus={JESUS.get(sid) or '-'}"
          f"{', +ref' if ref_paths else ''}) ...", flush=True)
    t = time.time()
    png.write_bytes(prov.generate(scene, extra_ref_paths=ref_paths or None))
    print(f"       ok ({png.stat().st_size:,} b, {time.time()-t:.0f}s) -> {png}")

print("\n[done] re-rendered:", ids, "— QC each at full res before animating.")
