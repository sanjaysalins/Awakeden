"""Animate the 21 approved 16:9 stills with veo3_1_lite (HF). Slow camera on a frozen
Baroque tableau; anti-morph prompt protects faces/hands. Idempotent (skips existing mp4).
Cross scenes are robed -> veo should pass; on NSFW block, falls back to direct-Kling."""
import sys, time, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
from pipeline import video_render
from _test_gate import apply_test_gate  # noqa: E402

config.VIDEO_HF_MODEL = "veo3_1_lite"
config.VIDEO_HF_ASPECT = "16:9"

OUT = ROOT / "longform" / "01_Isaiah_53_Suffering_Servant" / "v1" / "visual_16x9"

# per-scene (camera move, atmospheric drift). Faces/hands always protected by the base.
MOTION = {
    1:  ("very slow push-in",            "wind-blown dust and slowly drifting clouds"),
    2:  ("very slow drift across the scroll", "a gently flickering candle flame"),
    3:  ("slow rise",                    "softly radiating golden light"),
    4:  ("extremely slow push-in to the face", "a faint shift of shadow only"),
    5:  ("slow pull-back",               "distant figures barely shifting"),
    6:  ("very slow push-in",            "hair and cloth barely stirring, somber stillness"),
    7:  ("slow lateral drift",           "a faint shift of light"),
    8:  ("slow pan across the hillside", "sheep grazing slightly and grass moving in the wind"),
    9:  ("slow follow of the lamb",      "gentle dust and light"),
    10: ("slow push-in",                 "shadowed figures still, faint flame light"),
    11: ("slow lateral track",           "the procession slowly walking, dust"),
    12: ("slow approach to the tomb",    "drifting dusk haze"),
    13: ("slow tracking alongside",      "the chariot and horses moving along the road, wheels turning, dust"),
    14: ("slow push-in to the meeting",  "warm low sun, faint dust"),
    15: ("slow tilt up into the light",  "gentle growing radiance"),
    16: ("very slow push-in",            "the shaft of heaven's light steady, clouds churning slowly, robe faintly moving"),
    17: ("slow rise with the brightening dawn", "drifting morning mist"),
    18: ("slow push-in",                 "golden light gently glowing, robe still"),
    19: ("slow reveal",                  "light softly shifting"),
    20: ("very slow push-in to the offered hand", "a faint halo glow"),
    21: ("very slow settle and hold",    "a gentle reverent glow"),
}

def base(move, atmos):
    return (f"Cinematic {move}. Keep it a FROZEN Baroque oil painting tableau — preserve the "
            f"exact faces, hands and composition, NO morphing of faces or hands, NO new elements, "
            f"NO invented body motion. Only {atmos}.")

def slugof(t): return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")[:40]

plan = json.loads((OUT / "scene_plan.json").read_text(encoding="utf-8"))

# TEST GATE: animate 1-2 test clips, STOP for QC + approval, THEN batch the rest.
gate_ids, gate_stop, gate_banner = apply_test_gate(
    sys.argv, OUT, stage="animation",
    all_ids=[s["id"] for s in plan["scenes"]],
    default_test=[2, 13],  # a CALM scene (motion must feel alive, not dead) + a directional one
    qc_hint="Watch the WHOLE clip (>=6 frames): living motion, no morph/glitter, no comical reverse.",
)

vp = video_render.HFVideoProvider()
kling = None
ok = fail = skip = 0
for s in plan["scenes"]:
    if s["id"] not in gate_ids:
        continue
    png = OUT / f"{s['id']:02d}_{slugof(s['title'])}.png"
    mp4 = png.with_suffix(".mp4")
    if mp4.exists():
        print(f"[skip] {mp4.name}"); skip += 1; continue
    if not png.exists():
        print(f"[MISS png] {png.name}"); fail += 1; continue
    move, atmos = MOTION.get(s["id"], ("very slow push-in", "subtle atmosphere"))
    prompt = base(move, atmos)
    print(f"[anim] {s['id']:02d} {s['title'][:38]} ...", flush=True)
    t = time.time()
    try:
        vp.animate(png, mp4, prompt, 8)
        print(f"       ok ({mp4.stat().st_size:,} b, {time.time()-t:.0f}s)")
        ok += 1
    except Exception as e:
        msg = str(e)[:160]
        print(f"       veo FAILED: {msg}")
        if "nsfw" in msg.lower() or "blocked" in msg.lower() or "moderation" in msg.lower():
            try:
                if kling is None:
                    kling = video_render.KlingDirectProvider()
                print("       -> falling back to direct-Kling ...", flush=True)
                kling.animate(png, mp4, prompt, 8); ok += 1
                print(f"       ok via Kling ({mp4.stat().st_size:,} b)")
            except Exception as e2:
                print(f"       Kling FAILED too: {str(e2)[:160]}"); fail += 1
        else:
            fail += 1
print(f"\n[done] animated {ok}, skipped {skip}, failed {fail} -> {OUT}")
if gate_stop:
    print(gate_banner); sys.exit(0)
