"""Ingest Suno downloads from _inbox/ into the music library.

Scans _inbox for <base_slug>_a.mp3 / <base_slug>_b.mp3 (any file whose name starts
with a known catalogue base slug), measures real loudness, and registers each take as
its own entry (slug keeps the _a/_b suffix so both takes coexist and stay selectable).
Idempotent: re-running re-measures + re-registers. Free / offline (ffmpeg only).

  python ingest.py            # ingest everything in _inbox
  python ingest.py --move     # also move ingested files out of _inbox into clips/
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from music_library import MusicLibrary, MusicEntry          # noqa: E402
from _specs import SPECS                                     # noqa: E402

TODAY = "2026-06-06"


def measure(path: Path) -> tuple[float, float, float, float | None]:
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path),
                          "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    mean = mx = -60.0
    for line in out.splitlines():
        if "mean_volume:" in line:
            mean = float(line.split("mean_volume:")[1].split("dB")[0])
        elif "max_volume:" in line:
            mx = float(line.split("max_volume:")[1].split("dB")[0])
    # integrated loudness (EBU R128 LUFS) — the right metric for narration-safe gain
    lufs = None
    lo = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path),
                         "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    import json as _json
    try:
        blob = lo[lo.rindex("{"):lo.rindex("}") + 1]
        lufs = float(_json.loads(blob).get("input_i"))
    except (ValueError, KeyError, TypeError):
        pass
    dur = 0.0
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True)
    try:
        dur = float(p.stdout.strip())
    except ValueError:
        pass
    return mean, mx, dur, lufs


def base_of(stem: str) -> str | None:
    """sacred_grace_rise_a -> sacred_grace_rise (longest matching catalogue slug)."""
    for b in sorted(SPECS, key=len, reverse=True):
        if stem == b or stem.startswith(b + "_"):
            return b
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--move", action="store_true", help="move files out of _inbox after ingest")
    ap.add_argument("--all", action="store_true",
                    help="ingest the whole catalogue (default: PILOT_SLUGS only, test-gate)")
    args = ap.parse_args()

    from _specs import PILOT_SLUGS
    lib = MusicLibrary()
    inbox = HERE / "_inbox"
    mp3s = sorted(p for p in inbox.glob("*.mp3"))
    if not mp3s:
        print(f"[ingest] no .mp3 in {inbox} — drop your Suno downloads there "
              f"(named <slug>_a.mp3 / <slug>_b.mp3)")
        return

    done = unknown = 0
    for src in mp3s:
        stem = src.stem
        base = base_of(stem)
        if not base:
            print(f"[skip ] {src.name} — name doesn't match any catalogue slug")
            unknown += 1
            continue
        if not args.all and base not in PILOT_SLUGS:
            print(f"[gate ] {src.name} — not a PILOT bed; prove the loop first or pass --all")
            unknown += 1
            continue
        spec = SPECS[base]
        mean, mx, dur, lufs = measure(src)
        lib.import_file(src, slug=stem, mood=spec["mood"], energy=spec["energy"],
                        tags=spec["tags"], prompt=spec["prompt"], duration_s=round(dur, 1),
                        tempo_bpm=spec["tempo_bpm"], instrumentation=spec["instrumentation"],
                        has_vocals=False, use_cases=spec["use_cases"],
                        raw_mean_db=round(mean, 1), raw_max_db=round(mx, 1),
                        lufs_i=(round(lufs, 1) if lufs is not None else None),
                        status="pending",   # NOT selectable until human audition approves
                        source="suno", license="suno-paid-commercial",
                        reuse_scope="neutral", created=TODAY, used_in=[])
        lu = f"{lufs:.1f} LUFS" if lufs is not None else "LUFS n/a"
        print(f"[ok   ] {stem:<30} {spec['mood']:<10} {dur:>5.0f}s  {lu}  (status: pending)")
        done += 1
        if args.move:
            src.unlink()   # import_file already copied it into clips/

    print(f"\n[ingest] registered {done} take(s){' (unknown: %d)' % unknown if unknown else ''} "
          f"· library now {len(lib.entries)} tracks")
    print("  ALL tracks are status=pending and NOT selectable yet. Audition each, then:")
    print("    python approve.py <slug> [--url <suno_url>]      # mark a good take selectable")
    print("    python approve.py <slug> --reject --notes '...'  # drop a vocal/drum/muddy take")


if __name__ == "__main__":
    main()
