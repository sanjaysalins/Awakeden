r"""Woman at the well - film build ($0). Trim-only, 1.0x, hard cuts (owner rule: no freeze/boomerang/zoom fill).
Film time = voice time, +1.0 s silence after 'He is the Christ' (54.10), +3.0 s landing hold.
  .venv\Scripts\python.exe poc_pop_halftone\woman_at_well\build_film.py"""
import subprocess, json
from pathlib import Path
H = Path(__file__).resolve().parent; C = H/"clips"; W = H/"_work_v3"; W.mkdir(exist_ok=True)
P, PAUSE_AT, VOICE = 1.0, 56.19, 87.04   # v3 voice: film-panel fixes lines 07/14/15 (+3.21 s)
END = VOICE + P + 3.0
ft = lambda a: a if a < PAUSE_AT else a + P
# (clip, film_start) in order; c08/c09 cut moved 32.10 -> 32.70 (c09 shawl flap after 5.0 s)
# v3 (2026-11-13): line 07 +2.09 s spread over c10 (to clip max) / c11 (max) / c12; line 14 +0.41 into c17; line 15 +0.69 -> c19 = clip max
CUTS = [("c01",0.00),("c02",4.40),("c03",8.00),("c04",11.59),("c05",14.47),("c06",18.95),("c07",22.78),
        ("c08",26.70),("c09",32.70),("c10",37.49),("c11",45.53),("c12",50.57),("c13",54.36),("c14",57.19),
        ("c15",59.99),("c16",67.99),("c17",72.99),("c18",77.96),("c19",84.00)]
dur = lambda f: float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(f)],capture_output=True,text=True).stdout)
segs, report = [], []
for i, (c, s0) in enumerate(CUTS):
    s1 = CUTS[i+1][1] if i+1 < len(CUTS) else END
    slot = round(s1 - s0, 3); src = C/f"{c}.mp4"; have = dur(src)
    assert have >= slot - 0.01, f"{c}: clip {have:.2f}s shorter than slot {slot:.2f}s (no fill allowed)"
    out = W/f"{c}.mp4"
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(src),"-t",f"{slot:.3f}","-vf","scale=1080:1920:flags=lanczos,fps=30,setsar=1",
                    "-an","-c:v","libx264","-crf","17","-preset","medium","-pix_fmt","yuv420p",str(out)],check=True)
    segs.append(out); report.append({"clip": c, "start": round(s0,2), "slot": slot, "clip_len": round(have,2)})
(W/"list.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(W/"list.txt"),"-c","copy",str(W/"video.mp4")],check=True)
# audio: voice with 1.0 s silence spliced at 54.10, padded to END; two-pass-free simple loudness to ~-14 LUFS
A = H/"audio"/"narration.mp3"
fc = (f"[0:a]atrim=0:{PAUSE_AT},asetpts=PTS-STARTPTS[a];[0:a]atrim={PAUSE_AT},asetpts=PTS-STARTPTS[b];"
      f"anullsrc=r=44100:cl=mono,atrim=0:{P}[s];[a][s][b]concat=n=3:v=0:a=1,apad=whole_dur={END},"
      f"loudnorm=I=-14:TP=-1.5:LRA=11[out]")
subprocess.run(["ffmpeg","-y","-v","error","-i",str(A),"-filter_complex",fc,"-map","[out]","-ar","48000","-ac","2",str(W/"voice.wav")],check=True)
FILM = H/"WOMAN_AT_WELL_POC_v3.mp4"
subprocess.run(["ffmpeg","-y","-v","error","-i",str(W/"video.mp4"),"-i",str(W/"voice.wav"),"-map","0:v","-map","1:a","-c:v","copy",
                "-c:a","aac","-b:a","192k","-t",f"{END:.3f}","-movflags","+faststart",str(FILM)],check=True)
(W/"build_report.json").write_text(json.dumps({"end": END, "cuts": report}, indent=1), encoding="utf-8")
print("film", FILM, "video", round(dur(W/"video.mp4"),2), "film", round(dur(FILM),2), "target", round(END,2))
