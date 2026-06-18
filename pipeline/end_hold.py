"""LAST-WORD LINGER — hold the final frame ~1.5-2s so the last word rings out, never hard-cut.

Standing rule [[feedback-last-word-linger]]: every finished cut must let the final word linger.
This appends a held-last-frame tail (freeze the last video frame + carry audio then held silence)
to a finished captioned cut, so the closing Christ frame + the last word breathe before the end.

Idempotent-ish: writes a one-time `<stem>_pre_linger.mp4` backup, then replaces the file in place
so the canonical final filename is unchanged (downstream upload/refs keep working). A marker
sidecar `<mp4>.linger.json` records it so we don't double-apply.

Run: .venv\\Scripts\\python.exe -m pipeline.end_hold "<final captioned mp4>" [--hold 1.8]
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_HOLD = 1.8


def _marker(mp4: Path) -> Path:
    return Path(mp4).with_suffix(Path(mp4).suffix + ".linger.json")


def already_held(mp4: Path) -> bool:
    return _marker(mp4).exists()


def add_end_hold(mp4: Path, hold: float = DEFAULT_HOLD, log=print) -> bool:
    """Freeze the last frame + pad audio by `hold` seconds, in place (with a write-once backup)."""
    mp4 = Path(mp4)
    if not mp4.exists():
        log(f"  !! no file {mp4}")
        return False
    if already_held(mp4):
        log(f"  (already lingered: {mp4.name})")
        return True
    bak = mp4.with_name(mp4.stem + "_pre_linger.mp4")
    if not bak.exists():
        import shutil
        shutil.copy2(mp4, bak)
    tmp = mp4.with_suffix(".linger.tmp.mp4")
    # tpad clones the last video frame for `hold`s; apad adds matching audio silence so the
    # last word's natural decay rings into a held, reverent beat rather than a hard cut.
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4),
           "-vf", f"tpad=stop_mode=clone:stop_duration={hold}",
           "-af", f"apad=pad_dur={hold}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", str(tmp)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not tmp.exists():
        log(f"  !! ffmpeg failed: {(r.stderr or '')[-200:]}")
        tmp.unlink(missing_ok=True)
        return False
    tmp.replace(mp4)
    _marker(mp4).write_text(json.dumps({"held_s": hold, "backup": bak.name}), encoding="utf-8")
    log(f"  lingered +{hold}s -> {mp4.name}")
    return True


def _dur(mp4: Path) -> float:
    try:
        return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "default=nw=1:nk=1", str(mp4)],
                                    capture_output=True, text=True).stdout.strip())
    except (ValueError, OSError):
        return 0.0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    hold = float(sys.argv[sys.argv.index("--hold") + 1]) if "--hold" in sys.argv else DEFAULT_HOLD
    if not args:
        print("usage: python -m pipeline.end_hold <final mp4> [--hold 1.8]")
        raise SystemExit(2)
    p = Path(args[0])
    before = _dur(p)
    ok = add_end_hold(p, hold)
    print(f"  {before:.2f}s -> {_dur(p):.2f}s" if ok else "  FAILED")
    raise SystemExit(0 if ok else 1)
