"""Re-animate ONE 16:9 scene with a LIVELIER motion prompt (more real motion in
living elements - flame, smoke, dust, water, light, cloth edges - plus a stronger
camera move) while still protecting faces/hands from morphing. Backs up the current
clip to <stem>.prev.bak.mp4 so we can revert. veo3_1_lite via HF.

  python longform/_reanimate_one.py 2
"""
import sys, time, json, re, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import video_render

config.VIDEO_HF_MODEL = "veo3_1_lite"
config.VIDEO_HF_ASPECT = "16:9"

OUT = ROOT / "longform" / "01_Isaiah_53_Suffering_Servant" / "v1" / "visual_16x9"

# id -> (camera move, LIVING motion to actually animate). Faces/hands stay frozen.
LIVELY = {
    1:  ("a slow, deliberate push-in over the ridge",
         "wind drives the dust in visible gusts, clouds roll and churn across the sky, the prophet's robe and hair stir in the wind, grasses bend"),
    2:  ("a slow, deliberate push-in across the open scroll toward the hand",
         "the candle flame flickers and dances, throwing shifting warm light and curling wisps of smoke; fine dust drifts through the lamplight; warm highlights shimmer as living light"),
    3:  ("a slow majestic rise",
         "shafts of golden light pulse and sweep, radiance blooms and breathes, luminous motes of light drift upward, atmosphere glows and shifts"),
    4:  ("an extremely slow push-in to the face",
         "shadows shift across the face, faint breath of dust, a slow living play of light and dark"),
    5:  ("a slow pull-back",
         "distant figures and dust stir, light flickers, atmosphere drifts"),
    7:  ("a slow lateral drift",
         "light sweeps and shifts across the scene, faint dust and atmosphere move"),
    10: ("a slow push-in",
         "low flame light flickers across the shadowed figures, dust and haze drift, light breathes"),
    12: ("a slow approach to the tomb",
         "dusk haze rolls and drifts, the last light shifts and fades, fine dust moves on the air"),
    16: ("a slow push-in",
         "the shaft of heaven's light pulses and sweeps, storm clouds churn and roll, the robe and cloth edges stir, light breathes"),
    17: ("a slow rise with the brightening dawn",
         "morning mist rolls and drifts, dawn light grows and pulses, luminous motes drift upward"),
    18: ("a slow reverent push-in",
         "very subtle: only the robe and cloth edges faintly stir; keep the painted warm background light EXACTLY as it is, steady and unchanged — NO twinkling, NO growing glow, NO brightening, NO glitter, NO sparkles, NO floating particles, NO bokeh, NO light specks"),
    19: ("a slow reverent reveal",
         "the light softly blooms and gently breathes, warm radiance swells and fades, the robe and cloth edges faintly stir — soft painted light only, NO glitter, NO sparkles, NO floating particles, NO bokeh, NO falling light specks"),
    20: ("a slow continued push-in to the offered hand",
         "very subtle: only the robe and cloth edges faintly stir; keep the painted light EXACTLY as it is, steady and unchanged — NO growing glow, NO brightening, NO light burst, NO flare, NO new light, NO glitter, NO sparkles, NO floating particles"),
    21: ("a very slow reverent settle and hold",
         "the halo glows and gently breathes, the golden light softly swells and fades, the robe edge barely stirs — soft painted light only, NO glitter, NO sparkles, NO floating particles, NO bokeh, NO falling light specks"),
}


def prompt_for(move, living):
    return (f"Cinematic {move}. Keep it a Baroque oil painting — preserve the EXACT "
            f"face, hands and composition, NO morphing of faces or hands, NO new "
            f"characters or objects, NO invented body motion. Bring the scene to life "
            f"with real, visible motion in the living elements only: {living}.")


def slugof(t): return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")[:40]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id", type=int)
    args = ap.parse_args()
    plan = {s["id"]: s for s in json.loads((OUT/"scene_plan.json").read_text(encoding="utf-8"))["scenes"]}
    s = plan[args.id]
    stem = f"{s['id']:02d}_{slugof(s['title'])}"
    png = OUT / f"{stem}.png"
    mp4 = OUT / f"{stem}.mp4"
    if not png.exists():
        raise SystemExit(f"no PNG: {png}")
    if mp4.exists():
        bak = OUT / f"{stem}.prev.bak.mp4"
        if not bak.exists():
            bak.write_bytes(mp4.read_bytes())
            print(f"[backup] {bak.name}")
        mp4.unlink()
    move, living = LIVELY.get(args.id, ("a slow deliberate push-in",
                    "atmosphere, light, dust and cloth edges move with real, visible motion"))
    prompt = prompt_for(move, living)
    print(f"[anim] S{s['id']:02d} {s['title'][:40]}\n  {prompt}\n", flush=True)
    t = time.time()
    try:
        video_render.HFVideoProvider().animate(png, mp4, prompt, 8)
    except Exception as e:
        # never leave a scene with no base clip: restore the previous render
        bak = OUT / f"{stem}.prev.bak.mp4"
        if not mp4.exists() and bak.exists():
            mp4.write_bytes(bak.read_bytes())
            print(f"[restore] render failed; put back {mp4.name} from backup")
        raise
    print(f"[ok] {mp4.name} ({mp4.stat().st_size:,} b, {time.time()-t:.0f}s)")


if __name__ == "__main__":
    main()
