"""Force-align ONE episode's narration.mp3 -> words.json (free, offline WhisperX).

Usage: python sfx_pilots/align_ep.py "<v1 folder>"  [anchor words...]
Writes <here>/work/<safe>.words.json and prints anchor word times.
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


def spoken_text(folder: Path) -> str:
    raw = (folder / "narration.md").read_text(encoding="utf-8")
    body = raw.split("----")[0]
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    return " ".join(lines)


def main():
    folder = Path(sys.argv[1])
    anchors = [a.lower() for a in sys.argv[2:]]
    work = HERE / "work"
    work.mkdir(exist_ok=True)
    safe = folder.parent.name.replace(" ", "_")

    mp3 = folder / "narration.mp3"
    wav = work / f"{safe}.16k.wav"
    if not wav.exists():
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-i", str(mp3), "-ac", "1", "-ar", "16000", str(wav)], check=True)

    script = spoken_text(folder)
    print(f"[align] {len(script.split())} script words")
    words = forced_align_script(str(wav), script)
    out = work / f"{safe}.words.json"
    out.write_text(json.dumps(words, indent=2), encoding="utf-8")
    print(f"[align] wrote {len(words)} timed words -> {out}")

    def find_all(needle):
        hits = []
        for w in words:
            tok = re.sub(r"[^a-z]", "", w["w"].lower())
            if tok == needle:
                hits.append(w)
        return hits

    print("\n=== anchors ===")
    for a in anchors:
        for h in find_all(a):
            print(f"  '{a}' -> '{h['w']}'  {h['start']:.2f}-{h['end']:.2f}s")
    if words:
        print(f"  [last word] '{words[-1]['w']}'  {words[-1]['start']:.2f}-{words[-1]['end']:.2f}s")


if __name__ == "__main__":
    main()
