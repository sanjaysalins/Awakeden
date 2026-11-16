"""Talitha Cumi - FINAL (owner locked the Remotion v1 cut, 2026-11-10).

1. Landing hold: narration ends 50.843 s; pad video (clone last, already teal) and
   audio to 53.90 s so the hold is >= 3.0 s (INV-26).
2. Sparse $0 SFX bed from sound_library via sfx_pilots/sfxlib (reuse only):
   street murmur under the plea + news, footsteps on the walk, NOTHING in the
   room (held breath for the miracle), soft morning air under the landing.
Low priority, 3 threads (gentle mode).
"""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
ROOT = EP.parents[1]
sys.path.insert(0, str(ROOT / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

SRC = HERE / "TALITHA_REMOTION_v1.mp4"
HOLD = HERE / "_build_v2" / "remotion_v1_hold.mp4"
OUT = EP / "swirls_episode_06_talitha_cumi_final_sfx.mp4"
TOTAL = 53.90
LOW = 0x00004000 if sys.platform == "win32" else 0

LAYERS = [
    layer("street_murmur", "crowd_murmur_distant", "loop", 0.0, 13.8, -50.0, filt="lowpass=f=2200", fin=1.5, fout=2.0),
    layer("walk_steps", "footsteps_dirt_approach", "loop", 13.4, 7.0, -50.0, fin=1.0, fout=1.5),
    layer("morning_air", "dawn_morning_warm", "loop", 43.0, TOTAL - 43.0, -48.0, fin=2.5, fout=3.0),
]

if __name__ == "__main__":
    HOLD.parent.mkdir(exist_ok=True)
    r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-threads", "3",
                        "-i", str(SRC), "-filter_complex",
                        f"[0:v]tpad=stop_mode=clone:stop_duration=0.2,trim=0:{TOTAL}[v];"
                        f"[0:a]apad=whole_dur={TOTAL}[a]",
                        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                        "-threads", "3", "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL}", str(HOLD)],
                       capture_output=True, text=True, creationflags=LOW)
    if r.returncode:
        sys.exit(r.stderr[-1500:])
    sfxlib.show_plan("Ep 6 -- Talitha Cumi", LAYERS)
    sfxlib.build(HOLD, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, regions=[("street", 0, 13.6), ("walk", 13.6, 20.2), ("room", 20.2, 37.6),
                                 ("family", 37.6, 43.1), ("landing+hold", 43.1, TOTAL)])
