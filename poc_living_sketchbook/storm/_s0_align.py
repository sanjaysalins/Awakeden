"""Storm episode — step 0: force-align the existing LOCKED narration.mp3.

Stage 0 is a REUSE (per RUNBOOK.md, same pattern as episode_door) — no new
text/audio authored. This just gets exact word timings for spread cut points
and the Scribed Ink word-timed verse reveal (SKILL.md build order step 1).

  .venv\\Scripts\\python.exe poc_living_sketchbook/storm/_s0_align.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from veed_io.aligner import forced_align_script

SRC = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\20 He Was Asleep in the Storm\v1")
OUT_DIR = Path(__file__).resolve().parent

SPOKEN = (
    "Waves breaking over the rail. Water in the boat past your knees. "
    "Men screaming for their lives. And in the stern — He is asleep. "
    "He is not asleep because He doesn't care. He is asleep because He has "
    "nothing to fear from the very thing that is killing them. "
    "They shake Him awake, raging that He could possibly sleep through this. "
    "He opens His eyes: Why are ye fearful, O ye of little faith? "
    "Then he arose, and rebuked the winds and the sea; and there was a great "
    "calm. You'll say — easy for Him, He's God. Exactly. The One who could "
    "sleep through it is the One who silenced it with a word. "
    "You have admired this scene your whole life. But when the water reaches "
    "your knees, you don't trust the Christ in the boat. You wake Him, "
    "furious, certain He doesn't care. "
    "He doesn't despise little faith. He grows it by showing you Himself. "
    "Come to the Christ who slept unafraid. He is asking you — why are you afraid?"
)


def main():
    (OUT_DIR / "_storm_spoken.txt").write_text(SPOKEN, encoding="utf-8")
    words = forced_align_script(str(SRC / "narration.mp3"), SPOKEN)
    (OUT_DIR / "_storm_alignment.json").write_text(
        json.dumps(words, indent=1), encoding="utf-8")
    print(f"wrote {len(words)} words -> _storm_alignment.json")


if __name__ == "__main__":
    main()
