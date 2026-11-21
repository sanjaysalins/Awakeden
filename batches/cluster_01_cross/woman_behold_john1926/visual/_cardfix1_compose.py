r"""woman_behold cardfix1 compose ($0, ffmpeg only; run with the JesusInTheBible .venv python).
Pinned film = woman_behold_john1926_uplift_endfix1.mp4 (audio kept byte-for-byte via stream copy).
 1. HOOK  frames 0..124 (keyframe 4.1667): stock-engine beat 1 (uplift_v1/_livingpage_work/seg_01.mp4, pixel-identical to the
    film outside the card) + NEW hook card made of words the narrator says in the first 2 s (AN OLD MAN / HELD A BABY), same look
    as the old card (Impact, white then gold, black@0.64 boxes at y 170 / 320). The old card text was never spoken.
 2. GLOSS frames 862..1092 (keyframes 28.7333 .. 36.4333): stock-engine beats 7+8 of the fix1 spec rebuilt WITHOUT the
    'BEHOLD = HERE IS' card (_cardfix1_pool), then the film's own frames for the 6 page-flip frames at the end.
 Everything else = stream copy. Output: woman_behold_john1926_uplift_endfix1_cardfix1.mp4"""
import subprocess, sys
from pathlib import Path
V = Path(__file__).resolve().parent
POOL = V / "_cardfix1_pool"
W = V / "_cardfix1_work"; W.mkdir(exist_ok=True)
OLD = V / "woman_behold_john1926_uplift_endfix1.mp4"
SEG_HOOK = V / "uplift_v1" / "_livingpage_work" / "seg_01.mp4"
SEGS_BEH = [POOL / "_livingpage_work" / "seg_01.mp4", POOL / "_livingpage_work" / "seg_02.mp4"]
OUT = V / "woman_behold_john1926_uplift_endfix1_cardfix1.mp4"
FONT = "C\\:/Windows/Fonts/impact.ttf"
ENC = ["-c:v", "libx264", "-crf", "14", "-preset", "medium", "-profile:v", "high", "-level", "4.0", "-pix_fmt", "yuv420p", "-r", "30", "-an", "-threads", "3"]
K_HOOK_END = 125            # frame of keyframe 4.1667
K_G0, K_G1, K_FLIP = 862, 1093, 1087  # keyframes 28.7333 / 36.4333; page-flip starts at frame 1087


def run(c):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True)
    if r.returncode:
        sys.exit("FAIL " + " ".join(map(str, c))[:300] + "\n" + r.stderr[-1500:])
    return r.stdout


def dt(text, size, color, y, t0, t1):
    return (f"drawtext=fontfile='{FONT}':text='{text}':fontsize={size}:fontcolor={color}:box=1:boxcolor=black@0.64:"
            f"boxborderw=20:x=(w-text_w)/2:y={y}:enable='between(t,{t0},{t1})'")


def nframes(p):
    return int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", p]).strip().strip(","))


def hook():
    vf = ",".join([dt("AN OLD MAN", 104, "white", 170, 0.12, 2.40), dt("HELD A BABY", 104, "0xF2C14E", 320, 1.16, 2.40)])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", SEG_HOOK, "-vf", vf] + ENC + [W / "hook.mp4"])
    assert nframes(W / "hook.mp4") == K_HOOK_END


def gloss():
    segs = [str(s) for s in SEGS_BEH]
    n = sum(nframes(s) for s in SEGS_BEH)
    print("engine frames beats 7+8:", n)
    assert K_G0 + n <= K_FLIP + 3, n
    # engine frames for beats 7+8, then the film's own frames from there to the keyframe at 1093
    lst = W / "beh_list.txt"; lst.write_text("".join(f"file '{s}'\n" for s in segs).replace("\\", "/"))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-vf", "setpts=PTS-STARTPTS"] + ENC + [W / "beh_new.mp4"])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", OLD, "-vf", f"trim=start_frame={K_G0 + n}:end_frame={K_G1},setpts=PTS-STARTPTS"] + ENC + [W / "beh_tail.mp4"])
    (W / "beh2.txt").write_text("file 'beh_new.mp4'\nfile 'beh_tail.mp4'\n")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", W / "beh2.txt", "-c", "copy", W / "gloss.mp4"])
    assert nframes(W / "gloss.mp4") == K_G1 - K_G0, nframes(W / "gloss.mp4")


def compose():
    # copy parts of the old film at keyframe boundaries (segment muxer, times just before each keyframe)
    t = lambda k: k / 30 - 0.01
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", OLD, "-an", "-c:v", "copy", "-f", "segment", "-reset_timestamps", "1",
         "-segment_times", f"{t(K_HOOK_END)},{t(K_G0)},{t(K_G1)}", W / "o%d.mp4"])
    counts = [nframes(W / f"o{i}.mp4") for i in range(4)]
    print("old parts frames:", counts)
    assert counts[0] == K_HOOK_END and counts[1] == K_G0 - K_HOOK_END and counts[2] == K_G1 - K_G0, counts
    (W / "all.txt").write_text("file 'hook.mp4'\nfile 'o1.mp4'\nfile 'gloss.mp4'\nfile 'o3.mp4'\n")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", W / "all.txt", "-c", "copy", W / "video_only.mp4"])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", W / "video_only.mp4", "-i", OLD, "-map", "0:v", "-map", "1:a", "-c", "copy",
         "-movflags", "+faststart", OUT])
    print("ok", OUT)


if __name__ == "__main__":
    st = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name in (["hook", "gloss", "compose"] if st == "all" else [st]):
        globals()[name]()
