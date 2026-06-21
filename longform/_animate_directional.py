"""Chain-extend the DIRECTIONAL scenes (real onward motion that can't boomerang).
For each, the existing veo clip is clip[0]; we extract its last frame and animate
FORWARD from it, then chain (each clip's last frame seeds the next) until the
scene window is covered. Continuation clips -> <stem>_cont1.mp4, _cont2.mp4 ...
The assembler concats [orig, cont1, cont2, ...] forward-only (no reverse).

EPISODE-GENERIC: pass an episode slug/dir (bare = Isaiah, back-compat). The set of
directional scenes and their continuing-motion phrase are read from the scene plan
(scene.directional + scene.camera + scene.atmos), not a hardcoded table.

  python longform/_animate_directional.py "<episode>"            # full batch
  python longform/_animate_directional.py "<episode>" --only 13 --n 1   # TEST
"""
import sys, time, json, re, math, argparse, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
from pipeline import video_render
from _episode import resolve  # noqa: E402

config.VIDEO_HF_MODEL = "veo3_1_lite"
config.VIDEO_HF_ASPECT = "16:9"

CLIP_SECONDS = 8


def cont_motion(s):
    """The continuing forward motion for a directional scene, from the plan."""
    return (f"continue the camera move — {s.get('camera', 'a slow steady onward movement')}; "
            f"{s.get('atmos', 'subtle atmosphere only')}")


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
    ap.add_argument("episode", nargs="?", help="episode slug/dir (bare = Isaiah)")
    ap.add_argument("--only", type=int, help="run a single scene id")
    ap.add_argument("--n", type=int, help="cap continuation clips (test)")
    args = ap.parse_args()

    ep = resolve(sys.argv)
    OUT = ep.out
    plan = {s["id"]: s for s in ep.scenes}
    CONT = {s["id"]: cont_motion(s) for s in ep.scenes if s.get("directional")}
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
