"""Score for the words-v4 film ($0, no generation). Re-cuts the two cinematic raw parts (cine_part1_raw / cine_part2_raw)
to the words-v4 timing, then mixes them under film/BETHLEHEM_FILM_v9.mp4 the way mix_score_cine.py does.
Cut plan (real film seconds, narration_v41.words.json):
  part 1  0-16.2 as-is (timpani 4.0, solo-horn promise tune lands near 'from everlasting' 12.2), then jumps to part-1 t=21.4
          so the bigger 'promise tune again' lands on 'There, God's promise came true' (16.7-18.3); runs to 29.6.
  silence 29.6-30.7 (the 1 s true silence after 'Bethlehem was close by', done in the mix).
  part 2  starts 30.7: journey drive under 'The wise men went' (33.7); the long warm chords (part-2 6.45-9.0) are looped
          4x under the Galilee beat; 'sacred and still' enters at 46.9 ('He came down'); the huge swell lands on 'He rose' (51.9);
          the tune resolves ~55.9 and rings out to the 59.0 end.
Mix: base -13 dB, voice-keyed sidechain duck, alimiter; dips under both KJV lines + scribe, lifts, drop under 'Him, He came to us.'"""
import json, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
FILM = H.parent / "film"
VID = FILM / "BETHLEHEM_FILM_v9.mp4"
P1, P2, FIT, OUT = H / "cine_part1_raw.mp3", H / "cine_part2_raw.mp3", H / "score_v41.mp3", FILM / "BETHLEHEM_SCORED_v9.mp4"
TOTAL, SILENT_FROM, P2_START = 59.4, 31.2, 32.0
F = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"

def build():
    n_loop, L0, L1, xf = 4, 6.675, 9.0, 0.5
    parts = [f"[1:a]{F},atrim=0:9.0,asetpts=N/SR/TB[a0]"]
    chain = "[a0]"
    for i in range(n_loop):
        parts.append(f"[1:a]{F},atrim={L0}:{L1},asetpts=N/SR/TB[l{i}]")
    cur = "a0"
    for i in range(n_loop):
        parts.append(f"[{cur}][l{i}]acrossfade=d={xf}:c1=tri:c2=tri[x{i}]")
        cur = f"x{i}"
    parts.append(f"[1:a]{F},atrim=9.5,asetpts=N/SR/TB[b]")
    parts.append(f"[{cur}][b]acrossfade=d={xf}:c1=tri:c2=tri[p2full]")
    l2 = TOTAL - P2_START
    parts.append(f"[p2full]atrim=0:{l2:.3f},afade=t=in:d=0.4,afade=t=out:st={l2 - 0.8:.2f}:d=0.8[p2]")
    parts.append(f"[0:a]{F},asplit=2[s1][s2]")
    parts.append("[s1]atrim=0:17.92,asetpts=N/SR/TB[p1a]")
    parts.append("[s2]atrim=21.4:35.48,asetpts=N/SR/TB[p1b]")
    parts.append(f"[p1a][p1b]acrossfade=d=0.8:c1=tri:c2=tri[p1x]")
    parts.append(f"[p1x]atrim=0:{SILENT_FROM},afade=t=out:st={SILENT_FROM - 0.35:.2f}:d=0.35,apad=whole_dur={P2_START}[p1]")
    parts.append("[p1][p2]concat=n=2:v=0:a=1[o]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P1), "-i", str(P2), "-filter_complex", ";".join(parts),
                    "-map", "[o]", "-t", f"{TOTAL:.3f}", str(FIT)], check=True)

def mix():
    W = json.loads((H.parent / "audio_v4" / "narration_v41.words.json").read_text(encoding="utf-8"))
    him = next(w for w in W if w["w"].lower().startswith("him") and w["start"] > 50); us = W[-1]
    def seg(a, b, db, ramp=0.4):
        return f"({db})*min(1,max(0,min((t-{a:.2f})/{ramp},({b:.2f}-t)/{ramp})))"
    extra = "+".join([seg(11.2, 12.6, -8), seg(13.8, 15.0, -8), seg(27.0, 29.9, -5), seg(31.2, 32.0, -40, 0.15),
                      seg(35.0, 37.9, 3), seg(52.45, 54.35, 2), seg(him["end"] - 0.05, us["end"] + 0.2, -14), seg(us["end"] + 0.1, 62.0, 5)])
    vol = f"volume='pow(10,(-13+{extra})/20)':eval=frame"
    fc = (f"[0:a]{F},asplit=2[v][sc];"
          f"[1:a]{F},apad,{vol}[m];"
          "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
          f"[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(VID), "-i", str(FIT), "-filter_complex", fc,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)

if __name__ == "__main__":
    if "--mix-only" not in sys.argv:
        build(); print(FIT)
    if "--build-only" not in sys.argv:
        mix(); print(OUT)
