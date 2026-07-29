"""Build the EW01 Two Goats cold-open TRAILER video (2026-07-22).

Rapid hard-cut montage over the trailer audio master: full-bleed slams + 2x2
comic grids + bold caption slams (house BookAntiquaBold), cut to the VO beat
grid, with a dramatic STOP-then-reveal. All $0 (ffmpeg over the 25 inked clips +
_trailer_audio.mp3). v1 — deliberately simple captions (fade-in, not kinetic);
grid-choreography / impact-burst / print-grade polish come after direction is
blessed.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_trailer_build.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked"
CLIPS = OUT / "clips"
TRAILER = OUT / "_trailer"
WORK = TRAILER / "_work"
WORK.mkdir(parents=True, exist_ok=True)
AUDIO = TRAILER / "trailer_audio.mp3"
FILM = TRAILER / "EW01_Two_Goats_TRAILER.mp4"

W, H, FPS = 1920, 1080, 30
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", str(FPS), "-pix_fmt", "yuv420p"]
FONT = "C\\:/Windows/Fonts/BOOKOSB.TTF"   # BookAntiquaBold (house display face)

# beat = (t0, t1, kind, ids, caption, flash)
#   kind: "black" | "full" | "grid" | "title"
#   flash: None | "white" (quick white flash at beat start, e.g. the veil tear)
B = [
    (0.00,  1.46, "black", [],            None,                          None),
    (1.46,  2.81, "full",  [1],           "ONCE A YEAR",                 None),
    (2.81,  4.11, "full",  [4],           "ONE MAN",                     None),
    (4.11,  5.45, "full",  [3],           "ONE DOOR",                    None),
    (5.45,  7.63, "full",  [5],           "A HOLINESS THAT COULD KILL",  None),
    (7.63,  9.61, "grid",  [1, 3, 4, 5],  None,                          None),
    (9.61, 11.05, "grid",  [7, 8, 9, 10], "TWO GOATS",                   None),
    (11.05,12.66, "full",  [8],           "ONE KILLED",                  None),
    (12.66,13.92, "full",  [10],          "ONE SET FREE",                None),
    (13.92,15.34, "full",  [7],           "WHY TWO?",                    None),
    (15.34,16.78, "full",  [6],           "SAME BLOOD",                  None),
    (16.78,18.77, "full",  [14],          "SAME DOOR",                   None),
    (18.77,20.29, "grid",  [6, 14, 15, 12],"EVERY YEAR",                 None),
    (20.29,22.54, "full",  [15],          "IT WAS NEVER ENOUGH",         None),
    (22.54,23.98, "full",  [17],          "UNTIL ONE PRIEST WALKED IN",  None),   # STOP begins
    (23.98,25.69, "full",  [20],          "…AND SAT DOWN",          None),   # the lean-in hold
    (25.69,27.02, "full",  [23],          "THE VEIL TORE",               "white"),# reveal
    (27.02,29.35, "full",  [23],          "FROM THE TOP",                None),
    (29.35,30.91, "full",  [24],          "THE DOOR NEVER CLOSED AGAIN", None),
    (30.91,32.75, "full",  [11],          "ONE GOAT DIED",               None),
    (32.75,33.92, "full",  [10],          "ONE GOAT WENT FREE",          None),
    (33.92,35.40, "full",  [25],          None,                          None),
    (35.40,38.00, "title", [25],          "TWO GOATS",                   None),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(str(c) for c in cmd[:8])}...\n{r.stderr[-1400:]}")


def clip_for(cid):
    m = sorted(CLIPS.glob(f"{cid:02d}_*.mp4"))
    if not m:
        raise SystemExit(f"missing clip for scene {cid:02d}")
    return m[0]


def cap_filter(text, big=False):
    """A bold caption slam, lower-centre, white with a heavy ink border + soft
    shadow, quick alpha fade-in. Returns a drawtext filter string (or '')."""
    if not text:
        return ""
    t = text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")
    fs = 132 if big else 96
    y = "(h*0.70)"
    return (f"drawtext=fontfile='{FONT}':text='{t}':fontcolor=white:fontsize={fs}:"
            f"borderw=7:bordercolor=black@0.92:shadowx=0:shadowy=4:shadowcolor=black@0.7:"
            f"x=(w-text_w)/2:y={y}:alpha='if(lt(t,0.22),t/0.22,1)'")


def build_full(beat, dst):
    t0, t1, _, ids, cap, flash = beat
    dur = t1 - t0
    src = clip_for(ids[0])
    vf = [f"scale={W}:{H}:force_original_aspect_ratio=increase",
          f"crop={W}:{H}", f"fps={FPS}", "format=yuv420p"]
    if flash == "white":
        # quick white flash over the first ~0.28s (the tear)
        vf.append("geq=lum='lum(X,Y)+ (255-lum(X,Y))*max(0\\,(0.28-T)/0.28)':cb='cb(X,Y)':cr='cr(X,Y)'")
    cf = cap_filter(cap)
    if cf:
        vf.append(cf)
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0", "-t", f"{dur:.3f}", "-i", str(src),
         "-vf", ",".join(vf), "-an", *ENC, str(dst)])


def build_grid(beat, dst):
    t0, t1, _, ids, cap, _ = beat
    dur = t1 - t0
    ins = []
    for cid in ids:
        ins += ["-ss", "0", "-t", f"{dur:.3f}", "-i", str(clip_for(cid))]
    # 2x2 with a 6px ink gutter: each cell scaled to 957x537, padded to 960x540
    pre = "".join(
        f"[{i}:v]scale=957:537:force_original_aspect_ratio=increase,crop=957:537,"
        f"pad=960:540:(ow-iw)/2:(oh-ih)/2:color=0x0a0806,setsar=1[c{i}];"
        for i in range(4))
    grid = "[c0][c1][c2][c3]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0,fps={fps},format=yuv420p".format(fps=FPS)
    cf = cap_filter(cap)
    fc = pre + grid + ("[g];[g]" + cf + "[v]" if cf else "[v]")
    run(["ffmpeg", "-y", "-loglevel", "error", *ins,
         "-filter_complex", fc, "-map", "[v]", "-an", *ENC, str(dst)])


def build_black(beat, dst):
    t0, t1, *_ = beat
    dur = t1 - t0
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
         "-i", f"color=c=0x0a0806:s={W}x{H}:d={dur:.3f}:r={FPS}",
         "-vf", "format=yuv420p", "-an", *ENC, str(dst)])


def build_title(beat, dst):
    t0, t1, _, ids, cap, _ = beat
    dur = t1 - t0
    src = clip_for(ids[0])
    title = cap
    sub = "the day the veil tore"
    dt_title = (f"drawtext=fontfile='{FONT}':text='{title}':fontcolor=white:fontsize=170:"
                f"borderw=6:bordercolor=black@0.85:x=(w-text_w)/2:y=(h*0.40):"
                f"alpha='if(lt(t,0.5),t/0.5,1)'")
    dt_sub = (f"drawtext=fontfile='{FONT}':text='{sub}':fontcolor=0xe9c877:fontsize=58:"
              f"borderw=3:bordercolor=black@0.85:x=(w-text_w)/2:y=(h*0.40+200):"
              f"alpha='if(lt(t,1.0),max(0\\,(t-0.5)/0.5),1)'")
    vf = [f"scale={W}:{H}:force_original_aspect_ratio=increase", f"crop={W}:{H}",
          "eq=brightness=-0.18", f"fps={FPS}", "format=yuv420p", dt_title, dt_sub]
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0", "-t", f"{dur:.3f}", "-i", str(src),
         "-vf", ",".join(vf), "-an", *ENC, str(dst)])


def main():
    if not AUDIO.exists():
        raise SystemExit(f"missing audio master: {AUDIO} (run _trailer_audio.py first)")
    segs = []
    for i, beat in enumerate(B):
        kind = beat[2]
        dst = WORK / f"beat_{i:02d}.mp4"
        if kind == "black":
            build_black(beat, dst)
        elif kind == "grid":
            build_grid(beat, dst)
        elif kind == "title":
            build_title(beat, dst)
        else:
            build_full(beat, dst)
        segs.append(dst)
        print(f"  beat {i:02d}  {beat[0]:5.2f}-{beat[1]:5.2f}s  {kind:5}  {beat[4] or ''}")

    lst = WORK / "beats.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
    vonly = WORK / "video_only.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(vonly)])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vonly), "-i", str(AUDIO),
         "-map", "0:v", "-map", "1:a", *ENC, "-c:a", "aac", "-b:a", "192k", "-shortest", str(FILM)])
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", str(FILM)], capture_output=True, text=True).stdout.strip())
    print(f"\n[done] {FILM}  ({d:.1f}s)")


if __name__ == "__main__":
    main()
