"""Noah / The Builder -- burn ink captions onto the finished cut, same recipe
already used on the other 4 sketchbook shorts (memory
`sketchbook-shorts-finishing-gap`), but using _finish_long.py's 16:9 (1920x1080)
caption functions, NOT _short_captions.py's 9:16 (1080x1920) ones -- this piece
(poc_castbible_look/_04_assemble.py) is landscape, unlike the other 4 pieces
which are true vertical shorts. (First attempt used the 9:16 burner: the
caption canvas was taller than the video itself, so every caption composited
below the visible 1080px frame and rendered invisible -- caught by an eye-check
of extracted frames, not by the ffmpeg exit code, before shipping.) Post-process
only -- overlays onto the already-watermarked NOAH_THE_DOOR_castbible_poc.mp4,
does not touch _04_assemble.

No word-level timing exists for this piece (audio/timing.json is LINE-level
only, no per-word "words" array, unlike the other 4 pieces' narration
pipeline output). Forced-aligns each line's own mp3 (l1..l5) against its own
known exact text (veed_io.aligner.forced_align_script), then shifts each
line's word times by its real timing.json start offset -- ffprobe-measured
ground truth from _02_audio.py's own concat, not guessed -- so the 0.35s
inter-line gaps stay exact.

Skips every on-screen type_img() overlay window from _04_assemble.py's
OVERLAYS list (title card, verse cards, type-stamps) so a caption never
doubles text already on screen.

  .venv\\Scripts\\python.exe poc_castbible_look/_captions.py
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.resolve().parents[0]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "poc_living_sketchbook"))
from _polite import be_polite  # noqa: E402
from veed_io.aligner import forced_align_script  # noqa: E402
from _finish_long import chunk_words, build_caption_segment  # noqa: E402

AUD = HERE / "audio"
SRC = HERE / "NOAH_THE_DOOR_castbible_poc.mp4"
OUT = HERE / "NOAH_THE_DOOR_castbible_poc_cc.mp4"

# mirrors _04_assemble.py's OVERLAYS windows (title / verse cards / type-stamps)
SKIPS = [
    (1.2, 5.5),
    (11.0, 13.95),
    (11.5, 13.95),
    (14.15, 16.45),
    (17.0, 22.95),
    (17.5, 22.95),
    (26.3, 30.4),
]


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    be_polite()
    timing = json.loads((AUD / "timing.json").read_text(encoding="utf-8"))
    words = []
    for line in timing["lines"]:
        mp3 = AUD / f"{line['name']}.mp3"
        print(f"[align] {line['name']} ({mp3.name}) ...")
        aligned = forced_align_script(str(mp3), line["text"])
        for w in aligned:
            words.append({"w": w["w"], "start": w["start"] + line["start"],
                          "end": w["end"] + line["start"]})
        print(f"  -> {len(aligned)} words, shifted +{line['start']:.3f}s")

    total = dur(SRC)
    chunks = chunk_words(words, SKIPS)
    print(f"[chunks] {len(chunks)} caption chunks across {total:.1f}s")

    work_dir = HERE / "_caption_frames"
    work_dir.mkdir(exist_ok=True)
    seg = build_caption_segment(SRC, HERE, work_dir, 0, 0.0, total, chunks, rebuild=True)
    seg.replace(OUT)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
