r"""Empty Tomb endfix1 AUDIO. Re-runs the film's own audio chain (score stage + sfx stage, copied filter-for-filter from
run_piece.score_cmd and sfx_pilots/build_empty_tomb_sfx_v6.py) over a NEW voice track, then splices that mix onto the
old final's audio at CUT (30 ms crossfade) so everything before the cut is the old final's audio untouched.
  voice  = old narration.mp3 up to VCUT (silent gap after 'believed.') + new line (take a, atempo 1.1809) at 54.2 + silence
  total  = 61.4 s  (voice ends ~58.12, landing hold ~3.28 s)
  score  = piece.json score settings, total=61.4, 2.5 s fade at the end, cta_dip (music x0.5) from the landing beat 55.7
  sfx    = the v6 layers; only 'dawn2' length changes (ends with the film)
Modes: `old` rebuilds the OLD audio the same way (fidelity check vs the old final), `new` builds the new one.
Needs a video file for [0:v] only so the stock filter text is reused unchanged; we use it audio-side only.
  .venv\Scripts\python.exe audio\_endfix1\build_audio_endfix1.py new <picture_video.mp4>"""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
PIECE = HERE.parents[1]
ROOT = PIECE.parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "sfx_pilots"))
from pipeline import score_mix
import sfxlib

mode = sys.argv[1]
PIC = Path(sys.argv[2])                      # video whose picture is irrelevant here
OLD_FINAL = PIECE / "visual" / "empty_tomb_john208_sfx_v6trim.mp4"
VCUT, NEW_AT, T_END, CUT = 54.05, 54.2, 61.4, 54.05
BEAT_B = 55.7
sc = json.load(open(PIECE / "piece.json", encoding="utf-8"))["score"]
total = 64.82 if mode == "old" else T_END
cta_start = "58.05" if mode == "old" else f"{BEAT_B}"
W = HERE / f"_work_{mode}"; W.mkdir(exist_ok=True)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-1500:])

# 1. voice track
nar = W / "narration.wav"
if mode == "old":
    run(["ffmpeg", "-y", "-v", "error", "-i", str(PIECE / "audio" / "narration.mp3"), "-ar", "44100", "-ac", "2", str(nar)])
else:
    fmt = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
    ms = int(NEW_AT * 1000)
    fc = (f"[0:a]{fmt},atrim=0:{VCUT},asetpts=PTS-STARTPTS,afade=t=out:st={VCUT-0.03}:d=0.03[h];"
          f"[1:a]{fmt},adelay={ms}|{ms}[n];[h][n]amix=inputs=2:normalize=0:duration=longest,apad=whole_dur={T_END},atrim=0:{T_END}[o]")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(PIECE / "audio" / "narration.mp3"), "-i", str(HERE / "28_narrator_a__atempo.mp3"),
         "-filter_complex", fc, "-map", "[o]", "-c:a", "pcm_s16le", str(nar)])
# 2. mux voice onto the picture -> src for the score stage
src = W / "src_voice.mp4"
run(["ffmpeg", "-y", "-v", "error", "-i", str(PIC), "-i", str(nar), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(src)])
# 3. score stage (verbatim from run_piece.score_cmd)
mus = ROOT / "music_library" / "clips"
fc = (f"[1:a]atrim=0:{sc['dark_trim_end']},{score_mix.AFMT}[d];"
      f"[2:a]atrim={sc['grace_trim'][0]}:{sc['grace_trim'][1]},{score_mix.AFMT}[g];"
      f"[d][g]acrossfade=d={sc['crossfade']}:c1=exp:c2=exp[mch];"
      f"[mch]atrim=0:{total},afade=t=in:st=0:d=1.5,"
      f"afade=t=out:st={total - 2.5:.2f}:d=2.5,volume=-13dB,"
      f"volume=volume={sc['cta_dip'][1]}:enable='between(t,{cta_start},{total})'[mus];"
      + score_mix.mix_tail(total, sc["tpad"]))
scored = W / "scored.mp4"
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-i", str(mus / sc["dark"]), "-i", str(mus / sc["grace"]),
     "-filter_complex", fc, *score_mix.output_args(scored, preset="veryfast")])
# 4. sfx stage (v6 layers; dawn2 ends with the film)
L = sfxlib.layer
d2 = round(total - 48.11, 2)
layers = [L("wind", "wind_desert_bleak", "loop", 0.00, 13.49, -40.0, fin=1.5, fout=1.5),
          L("maryrun", "footsteps_dirt_approach", "oneshot", 6.79, 1.80, -34.0, fin=0.0, fout=0.6),
          L("theyran", "footsteps_stone", "oneshot", 13.49, 2.40, -33.0, fin=0.0, fout=0.8),
          L("hollow1", "air_hollow_desolate", "loop", 15.99, 12.20, -38.0, filt="lowpass=f=3000", fin=1.2, fout=1.0),
          L("johnin", "footsteps_stone", "oneshot", 28.19, 1.60, -38.0, fin=0.0, fout=0.6),
          L("dawn1", "dawn_morning_warm", "loop", 32.70, 7.21, -38.0, filt="lowpass=f=3400", fin=2.5, fout=2.0),
          L("lamp", "fire_crackling", "loop", 39.91, 8.20, -42.0, filt="lowpass=f=2800", fin=1.5, fout=1.5),
          L("dawn2", "dawn_morning_warm", "loop", 48.11, d2, -36.0, filt="lowpass=f=3400", fin=3.0, fout=1.5)]
sfxout = W / "sfx.mp4"
sfxlib.build(scored, sfxout, layers)
run(["ffmpeg", "-y", "-v", "error", "-i", str(sfxout), "-vn", "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", str(W / "mix_full.wav")])
print("ok", W / "mix_full.wav")
if mode == "new":
    # 5. splice: old final audio [0..CUT] crossfaded into the new mix
    X = 0.03
    fmt = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
    fc = (f"[0:a]{fmt},atrim=0:{CUT+X},asetpts=PTS-STARTPTS[a];[1:a]{fmt},atrim={CUT}:{T_END},asetpts=PTS-STARTPTS[b];"
          f"[a][b]acrossfade=d={X}:c1=tri:c2=tri,apad=whole_dur={T_END},atrim=0:{T_END},asetpts=PTS-STARTPTS[o]")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(OLD_FINAL), "-i", str(W / "mix_full.wav"), "-filter_complex", fc,
         "-map", "[o]", "-c:a", "pcm_s16le", str(HERE / "narration_endfix1_mix.wav")])
    print("ok", HERE / "narration_endfix1_mix.wav")
