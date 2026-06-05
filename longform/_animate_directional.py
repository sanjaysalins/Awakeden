"""Chain-extend the DIRECTIONAL scenes (real onward motion that can't boomerang).
For each, the existing veo clip is clip[0]; we extract its last frame and animate
FORWARD from it, then chain (each clip's last frame seeds the next) until the
scene window is covered. Continuation clips -> <stem>_cont1.mp4, _cont2.mp4 ...
The assembler concats [orig, cont1, cont2, ...] forward-only (no reverse).

  python longform/_animate_directional.py            # full batch (10 clips)
  python longform/_animate_directional.py --only 13 --n 1   # TEST: 1 cont clip for S13
"""
import sys, time, json, re, math, argparse, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import video_render

config.VIDEO_HF_MODEL = "veo3_1_lite"
config.VIDEO_HF_ASPECT = "16:9"

OUT = ROOT / "longform" / "01_Isaiah_53_Suffering_Servant" / "v1" / "visual_16x9"
CLIP_SECONDS = 8

# directional scene id -> phrase describing the CONTINUING forward motion
CONT = {
    8:  "the flock keeps grazing and slowly drifting, grass and cloth moving in the wind, the camera continuing its slow pan across the hillside",
    9:  "the lamb continues being led gently forward along the path, a slow steady onward movement, soft dust and sorrowful light",
    11: "the procession keeps walking forward, the long column steadily advancing, lowered banners swaying, dust rising, the camera tracking with them",
    13: "the chariot and horses keep moving forward along the dry road, wheels turning, hooves stepping, dust trailing, the camera tracking smoothly alongside",
    14: "the meeting continues, the traveler settling alongside the chariot, faint gestures, warm low sun and drifting dust, a slow continued push-in",
    20: "the tender moment continues, the pierced hand held out steady, the kneeling figure receiving it, a faint halo glow, a very slow continued push-in",
}


def base(atmos):
    return ("Cinematic continuation of a Baroque oil painting in motion. Continue the "
            f"existing movement smoothly and naturally: {atmos}. Preserve the exact painted "
            "faces, hands and oil-paint brushwork and composition — NO morphing of faces or "
            "hands, NO new characters or objects, NO style change, NO text.")


def slugof(t): return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")[:40]


def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",str(p)], capture_output=True, text=True).stdout.strip())


def last_frame(clip: Path, png: Path):
    subprocess.run(["ffmpeg","-y","-sseof","-0.12","-i",str(clip),"-frames:v","1",str(png)],
                   capture_output=True, text=True, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=int, help="run a single scene id")
    ap.add_argument("--n", type=int, help="cap continuation clips (test)")
    args = ap.parse_args()

    plan = {s["id"]: s for s in json.loads((OUT/"scene_plan.json").read_text(encoding="utf-8"))["scenes"]}
    vp = video_render.HFVideoProvider()
    ids = [args.only] if args.only else sorted(CONT)
    made = 0
    for sid in ids:
        s = plan[sid]
        stem = f"{sid:02d}_{slugof(s['title'])}"
        orig = OUT / f"{stem}.mp4"
        win = s["t"][1] - s["t"][0]
        need = max(0, math.ceil((win - 0.8) / CLIP_SECONDS) - 1)   # continuations beyond clip[0]
        if args.n is not None:
            need = min(need, args.n)
        print(f"[S{sid:02d}] win={win:.1f}s -> {need} continuation clip(s)  ({s['title'][:34]})")
        prev = orig
        for k in range(1, need+1):
            cont = OUT / f"{stem}_cont{k}.mp4"
            if cont.exists():
                print(f"   [skip] {cont.name} exists"); prev = cont; continue
            seed = OUT / "_assembly" / f"_seed_{stem}_{k}.png"
            seed.parent.mkdir(exist_ok=True)
            last_frame(prev, seed)
            print(f"   [anim] cont{k} from {prev.name} last frame ...", flush=True)
            t = time.time()
            vp.animate(seed, cont, base(CONT[sid]), CLIP_SECONDS)
            print(f"          ok ({cont.stat().st_size:,} b, {dur(cont):.1f}s, {time.time()-t:.0f}s)")
            prev = cont; made += 1
    print(f"\n[done] generated {made} continuation clip(s)")


if __name__ == "__main__":
    main()
