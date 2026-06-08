"""Force-align all 8 finished shorts in one process (WhisperX model loaded once).
Writes sfx_pilots/work/<safe>.words.json each + prints anchor word times.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from veed_io.aligner import forced_align_script  # noqa: E402

NARR = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration")
WORK = HERE / "work"

EPS = {
    "12 The Kiss That Cut Off the Bargain": ["rehearsed", "road", "ran", "neck", "kissed", "great", "compassion", "home"],
    "16 The Fire Jesus Built":              ["charcoal", "fire", "smoke", "shore", "morning", "lovest", "feed"],
    "18 He Never Said Yes":                 ["bethesda", "water", "pool", "whole", "walks", "troubled", "up"],
    "32_The_Door_Was_a_Body":               ["door", "pasture", "saved", "opened", "come"],
    "33_The_Shepherd_In_The_Gap":           ["gap", "door", "wolf", "shepherd", "laid", "pasture"],
    "34_The_Hunger_Bread_Cant_Fill":        ["empty", "hungry", "bread", "reaching", "come"],
    "35_Manna_Fulfilled":                   ["desert", "morning", "died", "bread", "flesh", "ever", "grave"],
    "36_In_No_Wise_Cast_Out":               ["door", "cast", "locked", "come", "rehearsing"],
}


def spoken_text(folder: Path) -> str:
    raw = (folder / "narration.md").read_text(encoding="utf-8")
    body = raw.split("----")[0]
    return " ".join(ln.strip() for ln in body.splitlines() if ln.strip())


def main():
    WORK.mkdir(exist_ok=True)
    for name, anchors in EPS.items():
        folder = NARR / name / "v1"
        if not (folder / "v1").exists() and not (folder / "narration.mp3").exists():
            # name/v1 layout
            pass
        safe = name.replace(" ", "_")
        mp3 = folder / "narration.mp3"
        wav = WORK / f"{safe}.16k.wav"
        if not mp3.exists():
            print(f"!! {name}: no narration.mp3 at {mp3}")
            continue
        if not wav.exists():
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                            "-i", str(mp3), "-ac", "1", "-ar", "16000", str(wav)], check=True)
        script = spoken_text(folder)
        words = forced_align_script(str(wav), script)
        (WORK / f"{safe}.words.json").write_text(json.dumps(words, indent=2), encoding="utf-8")
        print(f"\n=== {name}  ({len(words)} words) ===")

        def find_all(needle):
            return [w for w in words if re.sub(r"[^a-z]", "", w["w"].lower()) == needle]

        for a in anchors:
            for h in find_all(a):
                print(f"  {a:<11} '{h['w']}'  {h['start']:.2f}-{h['end']:.2f}s")
        if words:
            print(f"  [last]      '{words[-1]['w']}'  {words[-1]['start']:.2f}-{words[-1]['end']:.2f}s")


if __name__ == "__main__":
    main()
