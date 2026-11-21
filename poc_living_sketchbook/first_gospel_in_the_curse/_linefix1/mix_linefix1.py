"""first_gospel_in_the_curse linefix1 score+sfx: SAME recipe as ../_s5_score_sfx.py, every cue after the head shifted by D = -155 frames (-5.1667 s);
head-bound cues (air 0->turn, musA) shortened by |D|; musB fade-out re-keyed to the new end (3.0 s, silent on the last frame). Then mux with the new video."""
import subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; FILM = H.parent; ROOT = FILM.parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN
MUS = ROOT/"music_library"/"clips"; SND = ROOT/"sound_library"/"clips"
d = -155/30
TOTAL = round(1709/30, 4)         # 56.9667
f = lambda x: f"{x:.3f}"
ms = lambda x: int(round(x*1000))
T = 18.42 + d                      # the turn (musB in / musA out / air out)
filt = (
 f"[1:a]{AFMT},atrim=0:{f(24+d)},afade=t=in:st=0:d=1.5,afade=t=out:st={f(T)}:d=6.0,volume=-9dB[musA];"
 f"[2:a]{AFMT},adelay={ms(T)}|{ms(T)},atrim=0:{TOTAL},afade=t=in:st={f(T)}:d=6.0,afade=t=out:st={f(TOTAL-3.0)}:d=3.0,volume=-8dB[musB];"
 f"[3:a]{AFMT},atrim=0:{f(T)},afade=t=in:st=0:d=1.5,afade=t=out:st={f(16.5+d)}:d=1.9,volume=-20dB[air];"
 f"[4:a]{AFMT},atrim=0:7.0,adelay={ms(35.27+d)}|{ms(35.27+d)},afade=t=in:st={f(35.27+d)}:d=1.0,afade=t=out:st={f(41.5+d)}:d=1.4,volume=-16dB[thunder];"
 "[musA][musB][air][thunder]amix=inputs=4:normalize=0[bed];"
 f"[0:a]{AFMT},apad=whole_dur={TOTAL},asplit=2[main][key];"
 f"[bed][key]sidechaincompress={SIDECHAIN}[bedd];"
 "[main][bedd]amix=inputs=2:normalize=0,alimiter=limit=0.85:level=disabled,aresample=44100[mix]")
out = FILM/"FIRSTGOSPELINTHECURSE_living_sketchbook_cc_scored_sfx_v5hook_linefix1.mp4"
subprocess.run(["ffmpeg","-y","-v","error","-i",str(H/"narration_linefix1.wav"),
 "-i",str(MUS/"lonely_searching_a.mp3"),"-i",str(MUS/"sacred_grace_rise_a.mp3"),
 "-i",str(SND/"air_hollow_desolate.mp3"),"-i",str(SND/"thunder_low_roll.mp3"),
 "-i",str(H/"video_linefix1_noaudio.mp4"),
 "-filter_complex",filt,"-map","5:v","-map","[mix]","-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{TOTAL}","-movflags","+faststart",str(out)],check=True)
print("ok", out)
