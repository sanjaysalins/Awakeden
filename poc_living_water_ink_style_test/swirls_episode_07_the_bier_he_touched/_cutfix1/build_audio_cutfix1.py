r"""Ep07 cutfix1 audio ($0). Cut 4 narrator sentences' audio (no new recording):
 cut1 narr [12.40,17.00] = 'Everyone kept their distance. That was survival, not cruelty.'  (both ends inside silence)
 cut2 narr [25.50,28.30] = 'Then he touched what no one else would touch:'                  (both ends inside silence)
Score gets equal-length cuts (music cut1 [11.8,16.4] xfade 0.6, cut2 [27.1,29.9] xfade 0.8) so later score moments keep their
distance from the words; its own baked 2 s end fade stays the last thing in the file. Then the film's chain:
narration -> aac -> -6 dB score, sidechain 0.12/2.5/250 -> aac -> sfxlib.build(LAYERS retimed). Usage: build_audio_cutfix1.py video.mp4"""
import subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; EP = H.parent; ROOT = EP.parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "sfx_pilots"))
from pipeline import score_mix
import sfxlib
from sfxlib import layer
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit("FAIL " + " ".join(map(str, cmd))[:300] + "\n" + r.stderr[-1500:])
CUT = 4.6 + 2.8
TOTAL = 72.025 - CUT
FMT = "aformat=sample_fmts=fltp:channel_layouts=mono:sample_rates=44100"
fc = ";".join([
 f"[0:a]{FMT},atrim=0:12.40,asetpts=PTS-STARTPTS,afade=t=out:st=12.38:d=0.02[a1]",
 f"[0:a]{FMT},atrim=17.00:25.50,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.02,afade=t=out:st=8.48:d=0.02[a2]",
 f"[0:a]{FMT},atrim=28.30,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.02[a3]",
 "[a1][a2][a3]concat=n=3:v=0:a=1[n]"])
narr = H / "narration_cutfix1.wav"
run(["ffmpeg","-y","-v","error","-i",str(EP/"narration.mp3"),"-filter_complex",fc,"-map","[n]","-c:a","pcm_s16le",str(narr)])
SF = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
sc = ";".join([
 f"[0:a]{SF},atrim=0:12.10,asetpts=PTS-STARTPTS[s0]",
 f"[0:a]{SF},atrim=16.10:27.50,asetpts=PTS-STARTPTS[s1]",
 f"[0:a]{SF},atrim=29.50,asetpts=PTS-STARTPTS[s2]",
 "[s0][s1]acrossfade=d=0.6:c1=qsin:c2=qsin[x1]",
 "[x1][s2]acrossfade=d=0.8:c1=qsin:c2=qsin[sc]"])
score = H / "score_cutfix1.wav"
run(["ffmpeg","-y","-v","error","-i",str(EP/"score_piano.mp3"),"-filter_complex",sc,"-map","[sc]","-c:a","pcm_s16le",str(score)])
wn = H / "_cf_with_narration.m4a"
run(["ffmpeg","-y","-v","error","-i",str(narr),"-c:a","aac","-b:a","192k","-t",f"{TOTAL:.3f}",str(wn)])
filt = f"[1:a]{score_mix.AFMT},volume=-6dB[mus];[0:a]{score_mix.AFMT},apad=whole_dur={TOTAL},asplit=2[main][key];" \
 "[mus][key]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[musd];[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
mix = H / "_cf_mix_stage1.m4a"
run(["ffmpeg","-y","-v","error","-i",str(wn),"-i",str(score),"-filter_complex",filt,"-map","[mix]","-c:a","aac","-b:a","192k","-t",f"{TOTAL:.3f}",str(mix)])
VID = Path(sys.argv[1]); s1 = H / "_cf_stage1.mp4"
run(["ffmpeg","-y","-v","error","-i",str(VID),"-i",str(mix),"-map","0:v","-map","1:a","-c","copy",str(s1)])
S = CUT  # every layer that starts after both cuts shifts by 7.4 s
LAYERS = [
 layer("funeral_wind",    "wind_desert_bleak",     "loop",  0.0,   34.5 - S, -44.0, fin=2.0, fout=4.0),
 layer("wary_villagers",  "crowd_murmur_distant",  "loop",  0.5,   12.4 - 0.5, -50.0, filt="lowpass=f=2000", fin=2.0, fout=3.0),
 layer("homecoming_crowd","crowd_murmur_distant",  "loop", 51.0 - S, 8.0, -46.0, fin=2.0, fout=2.5),
 layer("dawn_landing",    "dawn_morning_warm",     "loop", 57.0 - S, 15.5, -44.0, fin=2.5, fout=3.0),
]
out = Path(sys.argv[2]) if len(sys.argv) > 2 else H / "_cf_sfx.mp4"
sfxlib.build(s1, out, LAYERS)
print("ok", out)
