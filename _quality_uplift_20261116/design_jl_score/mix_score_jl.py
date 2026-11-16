r"""DRAFT ($0, local ffmpeg). Mix the new score under Jacob's Ladder. Design: DESIGN.md.
Picture = stream copy of the newest film. Voice = audio/narration.mp3, no gain, no EQ. SFX = the same 5 layers as build_sfx_jl.py.
  F:\slk\PycharmProjects\JesusInTheBible\.venv\Scripts\python.exe mix_score_jl.py [score.mp3] [--audio-only]"""
import subprocess, sys
from pathlib import Path
import numpy as np
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
JL = ROOT / "poc_living_sketchbook" / "_rewrite_v4" / "panel_jl"
OV = Path(r"C:\Users\sanjay\JesusInTheBible_overflow\uplift_fix\jl")
VID, NARR = OV / "uplift" / "jl_uplift_fix1.mp4", JL / "audio" / "narration.mp3"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
SCORE = Path(args[0]) if args else OV / "score_cine" / "score.mp3"
WORK = OV / "score_cine"; TMP, OUT = WORK / "_narr_score.mp4", OV / "uplift" / "jl_uplift_fix1_cine.mp4"
TOTAL, TARGET, N = 56.5, 16.0, 226   # TARGET = dB the voice sits over the music while speaking (house band 14-18); N = 0.25 s windows
AF = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"


def seg(a, b, db, ramp=0.3): return f"({db})*min(1,max(0,min((t-{a:.2f})/{ramp},({b:.2f}-t)/{ramp})))"


SHAPE = "+".join([seg(23.2, 24.6, -8),   # "I will not leave thee" - stillness, not zero
                  seg(31.8, 35.6, -4),   # Jacob's KJV line
                  seg(35.5, 37.5, 4),    # dawn silence: music speaks
                  seg(44.0, 49.7, -3),   # John 1:51 (the swell is in the writing, the words stay on top)
                  seg(50.4, 53.2, 2),    # last two lines
                  seg(53.2, 58.0, 6)])   # landing hold opens up; the 2.5 s fade is baked into score.mp3


def chain(base, voice=True):  # voice=False -> music stem only (an anullsink on the voice leg cuts the tail short, so no split then)
    key = "asplit=2[v][sc]" if voice else "anull[sc]"
    return (f"[0:a]{AF},apad=whole_dur={TOTAL},{key};[1:a]{AF},apad,volume='pow(10,(({base:.2f})+{SHAPE})/20)':eval=frame[m];"
            "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md]")


LIM = ";[v][md]amix=inputs=2:duration=first:normalize=0[a]"   # no limiter here: voice peak 0.53 + music 16 dB under cannot clip (M7 checks); a limiter moved voice windows by up to 1 dB


def pcm(src, fc=None, lab=None):
    cmd = ["ffmpeg", "-v", "error"] + sum([["-i", str(s)] for s in src], [])
    cmd += (["-filter_complex", fc, "-map", lab] if fc else ["-vn"]) + ["-t", str(TOTAL), "-ac", "1", "-ar", "22050", "-f", "s16le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.int16).astype(float) / 32768


def q(x):  # per-0.25 s RMS in dB, padded to the film length
    n = 22050 // 4
    r = np.array([20 * np.log10(max(np.sqrt(np.mean(x[i:i + n] ** 2)), 1e-9)) for i in range(0, len(x) - n + 1, n)])
    return np.pad(r, (0, max(0, N - len(r))), constant_values=-180.0)[:N]


def w(a, b): return slice(int(a * 4), int(b * 4))


nv = q(pcm([NARR])); talk = nv > -30
raw = q(pcm([SCORE])); print(f"raw score mean {np.mean(raw[w(1, 53)]):.1f} dB, voice mean while speaking {np.mean(nv[talk]):.1f} dB")
bed0 = q(pcm([NARR, SCORE], chain(-13, False), "[md]"))
base = -13 + (np.median(nv[talk] - bed0[talk]) - TARGET)   # bed gain is linear -> one exact correction
bed = q(pcm([NARR, SCORE], chain(base, False), "[md]"))
mg = nv[talk] - bed[talk]
print(f"BASE {base:.1f} dB | voice over music while speaking: median {np.median(mg):.1f}  p10 {np.percentile(mg, 10):.1f}  min {mg.min():.1f} dB")
G = {}
G["M1 voice 14-18 dB over music (median), p10 >= 10"] = bool(14 <= np.median(mg) <= 18 and np.percentile(mg, 10) >= 10)
G["M2 no dead air 0.5-54.0 s (every 0.25 s > -55 dB)"] = bool((bed[w(0.5, 54.0)] > -55).all())
G["M3 stillness: music under 'I will not leave thee' >= 5 dB below 21.0-22.5, not zero"] = bool(
    np.mean(bed[w(21, 22.5)]) - np.mean(bed[w(23.5, 24.25)]) >= 5 and bed[w(23.5, 24.25)].min() > -55)
G["M4 hold 53.25-54.0 lifts >= 4 dB over 50.5-53.0"] = bool(np.mean(bed[w(53.25, 54)]) - np.mean(bed[w(50.5, 53)]) >= 4)
tail = bed[w(54.0, 56.5)]
G["M5 end fade: falls every 0.25 s from 54.25, no rise > 1.5 dB, last < -45 dB"] = bool((np.diff(tail[1:]) < 1.5).all() and tail[-1] < -45)
vo = q(pcm([NARR, SCORE], chain(-200) + LIM, "[a]")); full = pcm([NARR, SCORE], chain(base) + LIM, "[a]")
G["M6 voice untouched by the chain (score muted vs raw voice, <= 0.3 dB)"] = bool(np.abs(vo[talk] - nv[talk]).max() <= 0.3)
G["M7 mix peak <= 0.89 (-1 dBFS) with no limiter"] = bool(np.abs(full).max() <= 0.89)
print("music per 0.25 s, last 5 s:", np.round(bed[w(51.5, 56.5)], 1).tolist())
for k, v in G.items(): print("PASS" if v else "FAIL", k)
if "--audio-only" in sys.argv or not all(G.values()): sys.exit(0 if all(G.values()) else 1)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(NARR), "-i", str(SCORE), "-i", str(VID), "-filter_complex", chain(base) + LIM,
                "-map", "2:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(TOTAL), str(TMP)], check=True)
sys.path.insert(0, str(ROOT / "sfx_pilots")); sys.path.insert(0, str(JL))
import sfxlib  # noqa: E402
from build_sfx_jl import LAYERS  # noqa: E402  same 5 SFX layers, same levels
sfxlib.build(TMP, OUT, LAYERS); TMP.unlink()
print("[done]", OUT, "-> now run check_landing_hold.py and listen")
