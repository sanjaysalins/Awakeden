"""DNA-lock POC — Stage 1: animate the 4 chosen Seedream 4.5 beats (frozen tableau,
camera + living light). Dots are already baked into the seedream plates, so they
move WITH the art = no dot-crawl. Normalized to 1920x1080/30fps into
_remotion/public/dnapoc/. ~$3.70 (2 Kling + 2 Seedance).
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_dnapoc_animate.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
from pipeline.video_render import _hf_duration
HF = str(config.HF_CLI_PATH)
HERE = Path(__file__).resolve().parent
PUB = ROOT / "_remotion" / "public" / "dnapoc"
PUB.mkdir(parents=True, exist_ok=True)
CB = HERE / "_complex_bakeoff"
FROZEN = ("Every figure stays perfectly frozen the entire time -- no limbs move, no heads turn, no "
          "faces change, no morphing, no new figures or objects appear. INVENT NOTHING: show only "
          "what is already drawn in this exact image. ")
BASE = ("A still finished retro comic-book illustration on flat aged newsprint, 16:9, filmed as {move}. "
        + FROZEN + "Only the light and the air are alive: {living}.")
PUSH = "ONE slow, steady push-in toward the centre"
WIDE = "ONE slow, gentle push-in across the scene"
HERO = "ONE very slow, gentle push-in toward Christ"

# id, source still, model, move, living-light
BEATS = [
    ("01_establish", CB / "atonement_crowd__seedream_v4_5.png", "kling3_0", WIDE,
     "thin altar smoke rises, dust drifts in the dawn light, the crowd's robes stir almost imperceptibly, the light breathes"),
    ("02_event", CB / "crucifixion_crowd__seedream_v4_5.png", "kling3_0", WIDE,
     "the dark storm clouds drift slowly, a pale shaft of light breathes brighter and dimmer, fine dust drifts"),
    ("03_reaction", HERE / "_true_retro_finished" / "reaction_finished.png", "seedance1_5", PUSH,
     "fine dust motes drift, the light breathes brighter and dimmer"),
    ("04_welcome", HERE / "_seedream_ref" / "sr_welcome.png", "seedance1_5", HERO,
     "warm daylight breathes gently, fine dust drifts, his robe stirs faintly -- his hand and gaze never move"),
]


def animate(png, model, prompt, raw):
    dur = _hf_duration(model, 5)
    cmd = [HF, "generate", "create", model, "--start-image", str(png), "--prompt", prompt,
           "--duration", str(dur), "--aspect_ratio", "16:9", "--wait"]
    if model == "kling3_0":
        cmd += ["--mode", "pro", "--sound", "off"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW"); return None
    m = re.search(r'https?://\S+?\.mp4', blob)
    if not m:
        print(f"   no url: {blob.strip()[-160:]}"); return None
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(raw)], check=True)
    return dur if raw.exists() and raw.stat().st_size > 0 else None


def normalize(raw, out):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-vf",
                    "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an", str(out)], check=True)


def main():
    for bid, png, model, move, living in BEATS:
        out = PUB / f"{bid}.mp4"
        if out.exists() and out.stat().st_size > 0:
            print(f"[skip] {out.name}"); continue
        if not png.exists():
            print(f"[FAIL] missing still {png}"); continue
        prompt = BASE.format(move=move, living=living)
        raw = PUB / f"{bid}_raw.mp4"
        print(f"[clip] {bid} / {model} ...", flush=True); t = time.time()
        dur = animate(png, model, prompt, raw)
        if dur:
            normalize(raw, out); raw.unlink(missing_ok=True)
            cost.record_hf("EW01_Two_Goats", "long", "animate", model, note=f"[dnapoc] {bid}",
                           params={"duration": dur, "aspect_ratio": "16:9", **({"mode": "pro", "sound": "off"} if model == "kling3_0" else {})})
            print(f"   ok ({time.time()-t:.0f}s) -> {out.name}")
        else:
            print("   FAILED")
    print(f"[out] {PUB}")


if __name__ == "__main__":
    main()
