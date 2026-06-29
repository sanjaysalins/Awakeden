"""Assemble the EW04 Bronze Serpent inked-style short.
12 inked clips -> speech-aligned slots -> hard-cut concat -> mux the real
narration.mp3 (69.31s). Each clip is normalized to 1080x1920 / 30fps CFR and
speed-fit to its slot (setpts). Slots longer than a smooth 1.7x slowdown play at
1.7x then clone-hold the last frame (no stutter) — used only for the contemplative
cross + risen landings. POC/scratchpad output under ew04/cut/."""
import json, subprocess
from pathlib import Path

ROOT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible")
POC = ROOT / "longform" / "_style_poc"
ANIM = POC / "ew04" / "anim"
JES = POC / "anim_jesus"
NARR = ROOT / "longform" / "EW04_Bronze_Serpent" / "v1" / "short" / "narration.mp3"
OUT = POC / "ew04" / "cut"
TMP = OUT / "_t"
OUT.mkdir(parents=True, exist_ok=True); TMP.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1080, 1920, 30
NATIVE = 5.0417          # native clip seconds
MINTERP = 1.85          # above this slowdown factor, motion-interpolate (no freeze, no judder)

# (clip path, slot seconds) — narrative order, speech-aligned.
# a_03 (03_bronze_lifted) DROPPED: it shows the caduceus coil (unfixed still). Beat 3
# keeps only the fixed 3b hero. No clone-hold freezes anywhere — long closing clips
# (cross, risen) are motion-interpolated slow-mo.
SLOTS = [
 (ANIM / "EW04__01_hook_moses.mp4",        3.60),
 (ANIM / "EW04__01b_moses_close.mp4",      3.20),
 (ANIM / "EW04__02_judgment_plague.mp4",   5.50),
 (ANIM / "EW04__02b_serpents_spread.mp4",  4.70),
 (ANIM / "EW04__03b_serpent_atop_sky.mp4", 8.00),   # bronze beat (only the fixed hero now)
 (ANIM / "EW04__04_look_and_live.mp4",     3.30),
 (ANIM / "EW04__04b_face_to_life.mp4",     3.20),
 (ANIM / "EW04__05_night_teacher.mp4",     5.50),
 (ANIM / "EW04__05b_jesus_speaks.mp4",     6.40),
 (JES  / "JESUS__cross__a.mp4",           12.10),   # "lifted on a Roman pole, made a curse"
 (JES  / "JESUS__risen__b.mp4",           13.81),   # CTA: "Lift your eyes to Jesus... Look, and live"
]


def ffprobe_dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def norm(src, slot, idx):
    """Normalize + speed-fit one clip to exactly `slot` seconds at 1080x1920/30.
    Mild factors use setpts; heavy slowdowns are motion-interpolated (smooth, no freeze)."""
    n = ffprobe_dur(src)
    dest = TMP / f"{idx:02d}.mp4"
    k = slot / n                           # PTS factor; >1 = slower
    pad = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
           f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,setsar=1")
    if k <= MINTERP:
        vf = f"{pad},fps={FPS},setpts=PTS*{k:.6f}"
        mode = "setpts"
    else:
        vf = (f"{pad},setpts=PTS*{k:.6f},minterpolate=fps={FPS}:mi_mode=mci:"
              f"mc_mode=aobmc:me_mode=bidir:vsbmc=1")
        mode = "mci"
    args = ["ffmpeg", "-y", "-i", str(src), "-an", "-vf", vf, "-t", f"{slot:.3f}",
            "-r", str(FPS), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
            "-preset", "medium", str(dest)]
    subprocess.run(args, capture_output=True, text=True, check=True)
    out = ffprobe_dur(dest)
    print(f"[{idx:02d}] {src.name:32s} native={n:.2f} slot={slot:.2f} k={k:.2f} {mode:7s} -> {out:.2f}", flush=True)
    return dest


def main():
    parts = []
    for i, (src, slot) in enumerate(SLOTS):
        if not src.exists():
            raise SystemExit(f"MISSING clip: {src}")
        parts.append(norm(src, slot, i))
    listf = TMP / "list.txt"
    listf.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    silent = OUT / "_video_only.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listf),
                    "-c", "copy", str(silent)], capture_output=True, text=True, check=True)
    vdur = ffprobe_dur(silent); adur = ffprobe_dur(NARR)
    print(f"\nvideo={vdur:.2f}s  audio={adur:.2f}s", flush=True)
    final = OUT / "EW04_bronze_serpent_cut.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(silent), "-i", str(NARR),
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", str(final)], capture_output=True, text=True, check=True)
    print(f"\nDONE -> {final}  ({ffprobe_dur(final):.2f}s)", flush=True)


if __name__ == "__main__":
    main()
