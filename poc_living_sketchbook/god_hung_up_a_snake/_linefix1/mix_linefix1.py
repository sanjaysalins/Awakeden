"""god_hung_up_a_snake linefix1 score+sfx: SAME recipe as ../_s5_score_sfx.py, every cue shifted by D = -17 frames (-0.5667 s);
rumble window = new s01 slot (3.7 s). Narration = narration_linefix1.wav. Then mux with the new video."""
import subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; FILM = H.parent; ROOT = FILM.parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN
MUS = ROOT/"music_library"/"clips"; SND = ROOT/"sound_library"/"clips"
d = -17/30
TOTAL = round(62.0 + d, 4)         # 61.4333 = 1843 frames
def f(x): return f"{x:.3f}"
ms = lambda x: int(round(x*1000))
filt = (
 f"[1:a]{AFMT},atrim=0:{f(52.7+d)},afade=t=in:st=0:d=1.5,afade=t=out:st={f(45.66+d)}:d=6.0,volume=-9dB[musA];"
 f"[2:a]{AFMT},adelay={ms(51.657+d)}|{ms(51.657+d)},atrim=0:{TOTAL},afade=t=in:st={f(51.66+d)}:d=6.0,afade=t=out:st={f(59.0+d)}:d=3.0,volume=-8dB[musB];"
 f"[3:a]{AFMT},atrim=0:{TOTAL},afade=t=in:st=0:d=2,volume=-20dB[wind];"
 f"[4:a]{AFMT},atrim=0:3.7,afade=t=in:st=0:d=0.8,afade=t=out:st=2.9:d=0.8,volume=-17dB[rumble];"
 f"[5:a]{AFMT},atrim=0:5.46,adelay={ms(10.291+d)}|{ms(10.291+d)},afade=t=in:st={f(10.29+d)}:d=0.8,afade=t=out:st={f(14.95+d)}:d=0.8,volume=-15dB[crowd];"
 f"[6:a]{AFMT},atrim=0:4.91,adelay={ms(15.745+d)}|{ms(15.745+d)},afade=t=in:st={f(15.75+d)}:d=0.8,afade=t=out:st={f(19.86+d)}:d=0.8,volume=-14dB[fire];"
 f"[7:a]{AFMT},atrim=0:0.6,adelay={ms(16.968+d)}|{ms(16.968+d)},volume=-10dB[nail1];"
 f"[8:a]{AFMT},atrim=0:0.6,adelay={ms(18.988+d)}|{ms(18.988+d)},volume=-10dB[nail2];"
 "[musA][musB][wind][rumble][crowd][fire][nail1][nail2]amix=inputs=8:normalize=0[bed];"
 f"[0:a]{AFMT},apad=whole_dur={TOTAL},asplit=2[main][key];"
 f"[bed][key]sidechaincompress={SIDECHAIN}[bedd];"
 "[main][bedd]amix=inputs=2:normalize=0,alimiter=limit=0.85:level=disabled,aresample=44100[mix]")
out = FILM/"GODHUNGUPASNAKE_living_sketchbook_cc_scored_sfx_v5hook_linefix1.mp4"
subprocess.run(["ffmpeg","-y","-v","error","-i",str(H/"narration_linefix1.wav"),
 "-i",str(MUS/"lonely_searching_a.mp3"),"-i",str(MUS/"sacred_grace_rise_a.mp3"),
 "-stream_loop","-1","-i",str(SND/"wind_desert_bleak.mp3"),"-i",str(SND/"rumble_deep_sub.mp3"),"-i",str(SND/"crowd_murmur_distant.mp3"),
 "-i",str(SND/"fire_crackling.mp3"),"-i",str(SND/"nail_strike_single.mp3"),"-i",str(SND/"nail_strike_single.mp3"),
 "-i",str(H/"video_linefix1_noaudio.mp4"),
 "-filter_complex",filt,"-map","9:v","-map","[mix]","-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{TOTAL}","-movflags","+faststart",str(out)],check=True)
print("ok", out)
