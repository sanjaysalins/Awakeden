"""$0 Cinematic-Orchestral music bed for '24 The Answer Was a Gift' — chains two approved
music_library Suno tracks under viral_cut_sfx.mp4 (no metered Eleven Music).

Arc: lonely_searching (the searching crowd / the poll) crossfading into sacred_grace_rise, whose
swell (track 130-168s) is sliced so the crescendo LANDS on the Father-reveals / hero close
('come to the Christ the Father is showing you'). -11 dB, ducked under the voice (ratio 5).
No choir pad (SFX/score only).
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "music_library" / "clips"
ASM = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\24 The Answer Was a Gift\v1\assembly")
SRC = ASM / "viral_cut_sfx.mp4"
OUT = ASM / "viral_cut_sfx_music.mp4"
LONELY = LIB / "lonely_searching_a.mp3"
GRACE = LIB / "sacred_grace_rise_a.mp3"

OUTRO, GAIN, XF = 2.5, -11.0, 4.0

def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())

D = dur(SRC); T = D + OUTRO
AF = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
fc = (
    f"[1:a]{AF},atrim=0:30,asetpts=PTS-STARTPTS[s0];"
    f"[2:a]{AF},atrim=130:168,asetpts=PTS-STARTPTS[s1];"
    f"[s0][s1]acrossfade=d={XF}:c1=exp:c2=exp[mus0];"
    f"[mus0]atrim=0:{T:.2f},afade=t=in:st=0:d=2,afade=t=out:st={T-2.5:.2f}:d=2.5,volume={GAIN}dB[mus];"
    f"[0:v]tpad=stop_mode=clone:stop_duration={OUTRO}[v];"
    f"[0:a]{AF},apad=pad_dur={OUTRO},asplit=2[main][key];"
    f"[mus][key]sidechaincompress=threshold=0.10:ratio=5:attack=20:release=260[musd];"
    f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
)
cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(SRC),
       "-i", str(LONELY), "-i", str(GRACE), "-filter_complex", fc,
       "-map", "[v]", "-map", "[mix]", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{T:.2f}", str(OUT)]
print(f"[music] chaining lonely_searching -> sacred_grace_rise under {SRC.name} ({D:.1f}s)")
p = subprocess.run(cmd, capture_output=True, text=True)
print(p.stderr[-800:] if p.returncode else f"[ok] {OUT}")
