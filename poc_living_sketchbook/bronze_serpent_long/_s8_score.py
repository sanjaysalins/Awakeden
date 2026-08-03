"""Bronze Serpent LONG -- step 8: SCORE. Adapts the SAME Suno recipe already
proven+shipped for this exact story's OTHER visual treatment
(longform/04_The_Bronze_Serpent/_add_score_inked.py, itself a verbatim copy
of longform/_add_score_lf.py's EPISODES["04_The_Bronze_Serpent"]) onto this
sketchbook pilot's own base cut -- same segments/xfade/gain, just a new
src/out/total. Reusing a proven arc for the SAME narration beats "simple
first" over authoring a bespoke one for this first-of-its-kind long pilot;
a richer beat-tracking arc (e.g. a dip back to `lonely` under beat 5's dread
flashback) is a fair polish-pass-2 candidate later, not needed to ship this.

$0 -- Suno library, no API spend. Engine: pipeline/score_mix.py (INV-26
narration-pad + duck + mix tail), same one every other long-form scorer uses.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s8_score.py --yes
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline import score_mix  # noqa: E402

HERE = Path(__file__).resolve().parent
MUSIC_LIB = ROOT / "music_library" / "clips"
SRC = HERE / "BRONZESERPENT_LONG_living_sketchbook.mp4"
OUT = HERE / "BRONZESERPENT_LONG_living_sketchbook_scored.mp4"

RECIPE = {
    "segments": ["lonely_searching_a", "glory_holy_stillness_a", "sacred_grace_rise_b"],
    "xfade_s": 6.0,
    "gain_db": -11.0,
    "outro_s": 2.5,
}


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True,
    ).stdout.strip()
    return float(out)


def run(yes: bool, regen: bool) -> None:
    if not SRC.exists():
        sys.exit(f"missing base cut: {SRC} -- run _s7_assemble.py first")
    if OUT.exists() and not regen:
        print(f"[score] already exists -- skip (--regen to redo): {OUT}")
        return

    V = dur(SRC)
    outro = RECIPE["outro_s"]
    total = V + outro
    gain = RECIPE["gain_db"]
    xfade_s = RECIPE["xfade_s"]
    segments = [MUSIC_LIB / (s + ".mp3") for s in RECIPE["segments"]]
    for seg in segments:
        if not seg.exists():
            sys.exit(f"Missing music segment: {seg}")

    seg_durations = [dur(s) for s in segments]
    chained_dur = sum(seg_durations) - xfade_s * (len(segments) - 1)
    print(f"[score] source  : {SRC.name} ({V:.1f}s)")
    print(f"[score] segments: {[s.name for s in segments]}")
    print(f"[score] arc     : {' -> '.join(f'{d:.0f}s' for d in seg_durations)} "
          f"(xfade {xfade_s}s) = {chained_dur:.1f}s")
    print(f"[score] target  : {total:.1f}s  gain={gain}dB  outro={outro}s")
    print(f"[score] output  : {OUT}")

    if not yes:
        print("\n  $0 (Suno library, no API spend). Re-run with --yes to mix.\n")
        return

    fmt = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
    n = len(segments)
    if n == 1:
        chain = f"[0:a]{fmt}[mc]"
    else:
        parts = [f"[{i}:a]{fmt}[s{i}]" for i in range(n)]
        prev = "s0"
        for i in range(1, n):
            parts.append(f"[{prev}][s{i}]acrossfade=d={xfade_s:.1f}:c1=exp:c2=exp[x{i}]")
            prev = f"x{i}"
        parts.append(f"[{prev}]anull[mc]")
        chain = "; ".join(parts)
    trimmed = OUT.with_name("_score_music_trimmed.wav")
    trim_fc = (f"{chain}; [mc]silenceremove=stop_periods=-1:stop_threshold=-50dB:"
               f"stop_duration=0.25,asetpts=PTS-STARTPTS[m]")
    seg_inputs = [x for seg in segments for x in ["-i", str(seg)]]
    pp = subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *seg_inputs,
         "-filter_complex", trim_fc, "-map", "[m]", str(trimmed)],
        capture_output=True, text=True,
    )
    if pp.returncode != 0:
        print(f"[score] music pre-pass FAILED:\n{pp.stderr[-1500:]}")
        sys.exit(1)
    music_real = dur(trimmed)
    atempo = max(0.92, min(1.0, music_real / total))
    print(f"[score] music (de-tailed) {music_real:.1f}s -> atempo {atempo:.4f} to fill {total:.1f}s")

    fade_dur = 1.5
    fade_out_start = max(0.0, total - fade_dur)
    fc = (
        f"[1:a]{fmt},atempo={atempo:.4f},asetpts=PTS-STARTPTS,"
        f"atrim=0:{total + 0.2:.3f},"
        f"afade=t=in:st=0:d=2,"
        f"afade=t=out:st={fade_out_start:.2f}:d={fade_dur},"
        f"volume={gain}dB[mus];"
        + score_mix.mix_tail(total, outro, fmt_narration=True)
    )
    inputs = ["-i", str(SRC), "-i", str(trimmed)]
    cmd = (
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
        + inputs
        + ["-filter_complex", fc]
        + score_mix.output_args(OUT, preset="veryfast", total=total)
    )
    print("[score] mixing (may take a while under the CPU throttle)...", flush=True)
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print(f"[score] ffmpeg FAILED:\n{p.stderr[-2000:]}")
        sys.exit(1)
    final_dur = dur(OUT)
    print(f"[score] done  -> {OUT}  ({final_dur:.1f}s)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yes", action="store_true")
    ap.add_argument("--regen", action="store_true")
    a = ap.parse_args()
    run(a.yes, a.regen)


if __name__ == "__main__":
    main()
