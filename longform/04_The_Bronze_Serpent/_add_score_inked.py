"""Add the SAME Bronze Serpent Suno score recipe as longform/_add_score_lf.py
(segments/gain/xfade/outro identical -- copied verbatim from its EPISODES dict)
to the graphic-novel rebuild film in v1/visual_16x9_inked/ (the shared script is
hardcoded to v1/visual_16x9/, so this is a path-only fork, not a design change).
$0 -- Suno library, no API spend.

Usage: .venv\\Scripts\\python.exe longform/04_The_Bronze_Serpent/_add_score_inked.py --yes
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MUSIC_LIB = ROOT / "music_library" / "clips"
VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked"

# verbatim copy of EPISODES["04_The_Bronze_Serpent"] from longform/_add_score_lf.py
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
    candidates = [
        c for c in sorted(VIS.glob("*_16x9.mp4"))
        if "_scored" not in c.name and "_captioned" not in c.name
    ]
    if not candidates:
        sys.exit(f"No *_16x9.mp4 found in {VIS}")
    src = candidates[0]
    out = src.with_name(src.stem + "_scored.mp4")
    if out.exists() and not regen:
        print(f"[score] already exists — skip (--regen to redo): {out}")
        return

    V = dur(src)
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
    print(f"[score] source  : {src.name} ({V:.1f}s)")
    print(f"[score] segments: {[s.name for s in segments]}")
    print(f"[score] arc     : {' -> '.join(f'{d:.0f}s' for d in seg_durations)} "
          f"(xfade {xfade_s}s) = {chained_dur:.1f}s")
    print(f"[score] target  : {total:.1f}s  gain={gain}dB  outro={outro}s")
    print(f"[score] output  : {out}")

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
    trimmed = out.with_name("_score_music_trimmed.wav")
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
        f"atrim=0:{total+0.2:.3f},"
        f"afade=t=in:st=0:d=2,"
        f"afade=t=out:st={fade_out_start:.2f}:d={fade_dur},"
        f"volume={gain}dB[mus]; "
        f"[0:v]tpad=stop_mode=clone:stop_duration={outro}[vout]; "
        # apad=pad_dur=X pads X seconds onto the audio's OWN raw length -- if the
        # source narration audio is already shorter than its video track (a real,
        # ~1s gap found in Bronze Serpent's build), that pre-existing shortfall
        # survives instead of being corrected. whole_dur pads to an ABSOLUTE
        # target (matching [vout]'s true length: V + outro = total) regardless
        # of how long the raw audio actually was going in. INV-26.
        f"[0:a]{fmt},apad=whole_dur={total},asplit=2[main][key]; "
        f"[mus][key]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[musd]; "
        f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
    )
    inputs = ["-i", str(src), "-i", str(trimmed)]
    cmd = (
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
        + inputs
        + ["-filter_complex", fc,
           "-map", "[vout]", "-map", "[mix]",
           "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "192k",
           "-t", f"{total:.3f}",
           str(out)]
    )
    print("[score] mixing (may take ~30s)...", flush=True)
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print(f"[score] ffmpeg FAILED:\n{p.stderr[-2000:]}")
        sys.exit(1)
    final_dur = dur(out)
    print(f"[score] done  -> {out}  ({final_dur:.1f}s)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yes", action="store_true")
    ap.add_argument("--regen", action="store_true")
    a = ap.parse_args()
    run(a.yes, a.regen)


if __name__ == "__main__":
    main()
