r"""Endfix1 audio: fix2 audio kept EXACTLY up to 49.18 s (silent gap after 'there.'), then
  new narrator line (take a, atempo 1.1299, -1 dB to match the other narrator turns) at 49.70 s
  + the original 'dawn' ambience layer (sfx map: dawn_morning_warm -36 dB, lowpass 3400, fin 2.0), sidechain-ducked like sfxlib
  + the fix2 landing tail (the gentle +4 dB lifted score + its 2.5 s fade, cut 58.78..end) moved to follow the new line.
Writes narration_endfix1_mix.wav (exactly the video length)."""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
PIECE = HERE.parents[1]
ROOT = HERE.parents[4]
FIX2 = PIECE / "visual" / "woman_behold_john1926_uplift_fix2.mp4"
NAR = HERE / "15_narrator_a__atempo.mp3"
DAWN = ROOT / "sound_library" / "clips" / "dawn_morning_warm.mp3"
raw = {e["slug"]: e["raw_mean_db"] for e in json.loads((ROOT / "sound_library" / "index.json").read_text(encoding="utf-8"))}
gain = -36.0 - raw["dawn_morning_warm"]
CUT, NAR_AT = 49.18, 49.70
TAIL_O = 58.78                 # fix2 tail start (old narration 'tore.' ends 58.70 incl. 15 ms lag)
VID_END = 1694 / 30.0          # 56.4667
FIX2_END = 62.1710
TAIL_LEN = FIX2_END - TAIL_O
TAIL_AT = VID_END + 0.0043 - TAIL_LEN      # tail ends with the video (aac length 4 ms longer, like fix2)
fmt = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
dawn_len = VID_END - 49.2
fc = ";".join([
    f"[0:a]{fmt},atrim=0:{CUT},asetpts=PTS-STARTPTS,afade=t=out:st={CUT-0.04}:d=0.04[head]",
    f"[1:a]{fmt},volume=-1dB,adelay={int(NAR_AT*1000)}|{int(NAR_AT*1000)},asplit=2[nv][nk]",
    f"[2:a]{fmt},aloop=loop=-1:size=2e9,atrim=0:{dawn_len:.3f},lowpass=f=3400,volume={gain}dB,"
    f"afade=t=in:st=0:d=2.0,afade=t=out:st={dawn_len-1.5:.3f}:d=1.5,adelay=49200|49200[dawn]",
    "[dawn][nk]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=320[dd]",
    "[nv][dd]amix=inputs=2:normalize=0:duration=longest[nd]",
    f"[0:a]{fmt},atrim={TAIL_O}:{FIX2_END},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.03,"
    f"adelay={int(round(TAIL_AT*1000))}|{int(round(TAIL_AT*1000))}[tail]",
    "[head][nd][tail]amix=inputs=3:normalize=0:duration=longest,alimiter=limit=0.89:level=disabled,aresample=44100[mix]",
])
out = HERE / "narration_endfix1_mix.wav"
cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(FIX2), "-i", str(NAR), "-i", str(DAWN),
       "-filter_complex", fc, "-map", "[mix]", "-t", f"{VID_END:.4f}", "-c:a", "pcm_s16le", str(out)]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode:
    sys.exit(r.stderr[-1500:])
print("ok", out, "tail_at", round(TAIL_AT, 3), "dawn gain", round(gain, 1))
