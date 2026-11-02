"""Jacob's Ladder v3 assembly: NEW locked narration (2026-11-02), slots from real line timing.
Reuses assemble_book_v2 helpers (make_freeze/make_boomerang/AFMT/duck). Score = score_final.mp3 trimmed+faded to new length.
Back cover ("HE IS THAT LADDER") and F07 ("You are not") are NOT used: baked captions contradict the new words."""
import json, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
PILOT = H.parents[2] / "poc_living_water_ink_style_test" / "swirls_pilot_01_jacobs_ladder"
sys.path.insert(0, str(PILOT))
import assemble_book_v2 as B
T = json.loads((H / "audio" / "timing.json").read_text())
st = {l["name"]: l["start"] for l in T["lines"]}
narr = B.dur(H / "audio" / "narration.mp3"); total = narr + B.OUTRO_HOLD
C = PILOT / "_style_test_durer_woodcut"
work0 = H / "video" / "_work"; work0.mkdir(parents=True, exist_ok=True)
F02 = work0 / "f02_720.mp4"
if not F02.exists(): B.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(PILOT / "the_ladder_f02_9x16.mp4"), "-vf", "scale=720:1280:flags=lanczos,setsar=1", "-r", "24", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", str(F02)])
UNITS = [  # (tag, src, start, mode)
 ("front", C / "front_cover_woodcut.mp4", 0.0, "freeze"),
 ("f02", F02, st["l2"], "boomerang"),
 ("f03a", PILOT / "the_ladder_f03_9x16.mp4", st["l3"], "freeze"),
 ("f04a", PILOT / "the_ladder_f04_9x16.mp4", st["l4"], "boomerang"),
 ("f05", PILOT / "the_ladder_f05_9x16.mp4", st["l7"], "freeze"),
 ("f06", PILOT / "the_ladder_f06_9x16.mp4", st["l8"], "freeze"),
 ("f03b", PILOT / "the_ladder_f03_9x16.mp4", st["l9"], "freeze"),
 ("f04b", PILOT / "the_ladder_f04_9x16.mp4", st["l9"] + 0.48 * (st["l10"] - 1.5 - st["l9"]), "boomerang"),
# landing: Jacob asleep
 ("f02b", F02, st["l10"], "boomerang"),
]
work = H / "video" / "_work"; work.mkdir(parents=True, exist_ok=True)
held = []
for i, (tag, src, s, mode) in enumerate(UNITS):
    e = UNITS[i + 1][2] if i + 1 < len(UNITS) else total
    slot = e - s; cd = B.dur(src); out = work / f"{tag}__held.mp4"
    (B.make_boomerang(src, out, slot, cd, work, tag) if mode == "boomerang" else B.make_freeze(src, out, slot, cd))
    print(f"[{tag}] {s:.2f}-{e:.2f} slot={slot:.2f} native={cd:.2f} {mode}", flush=True); held.append(out)
(work / "concat.txt").write_text("\n".join(f"file '{p.resolve()}'" for p in held), encoding="utf-8")
sil = work / "silent.mp4"
B.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-f", "concat", "-safe", "0", "-i", str(work / "concat.txt"), "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", str(sil)])
wn = work / "with_narration.mp4"
B.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(sil), "-i", str(H / "audio" / "narration.mp3"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(wn)])
OUT = H / "video" / "jacobs_ladder_v3.mp4"
fo = total - 4.0
filt = (f"[1:a]{B.AFMT},atrim=0:{total:.3f},afade=t=out:st={fo:.3f}:d=4,volume={B.MUSIC_GAIN_DB}dB[mus];"
        f"[0:a]{B.AFMT},apad=whole_dur={total:.3f},asplit=2[main][key];"
        f"[mus][key]sidechaincompress=threshold={B.DUCK_THRESHOLD}:ratio={B.DUCK_RATIO}:attack=20:release={B.DUCK_RELEASE}[musd];"
        f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix];"
        f"[0:v]tpad=stop_mode=clone:stop_duration={B.OUTRO_HOLD}[vout]")
B.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(wn), "-i", str(PILOT / "score_final.mp3"), "-filter_complex", filt, "-map", "[vout]", "-map", "[mix]", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", str(OUT)])
print("[done]", OUT, round(B.dur(OUT), 2), "s")
