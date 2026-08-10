"""At the Door -- step 5: hand-written ink captions over the finished cut,
applying the same recipe used on Bronze Serpent (memory
`sketchbook-shorts-finishing-gap`). Post-process only -- overlays onto the
already-watermarked AT_THE_DOOR_sketch_poc.mp4, does not touch _e4/watermark.

Word timing comes from the standard narration pipeline's own
narration.alignment.json (whisper-based, keys text/start/end -- confirmed by
_e4_assemble.py that narration is NOT delayed in the final mix, so its times
map straight onto the video timeline).

Skips every on-screen type_img() overlay window from _e4_assemble.py's OVERLAYS
list (title card, JOHN 6:37 verse, and the three type-stamp beats) so a caption
never doubles text already on screen.

  .venv\\Scripts\\python.exe poc_castbible_look/episode_door/_e5_captions.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.resolve().parents[1]
sys.path.insert(0, str(ROOT / "poc_living_sketchbook"))
from _short_captions import burn  # noqa: E402

ALIGN_PATH = (ROOT.parent / "PythonProject1" / "jesus" / "narration" /
              "36_In_No_Wise_Cast_Out" / "v1" / "narration.alignment.json")
SRC = HERE / "AT_THE_DOOR_sketch_poc.mp4"
OUT = HERE / "AT_THE_DOOR_sketch_poc_cc.mp4"

# mirrors _e4_assemble.py's OVERLAYS windows (title / verse / type-stamps)
SKIPS = [
    (3.0, 5.1),
    (21.6, 25.5),
    (34.0, 36.6),
    (37.8, 40.4),
    (53.2, 57.9),
]


def main():
    raw = json.loads(ALIGN_PATH.read_text(encoding="utf-8"))
    words = [{"w": w["text"], "start": w["start"], "end": w["end"]} for w in raw["words"]]
    burn(SRC, OUT, words, SKIPS, HERE / "_caption_frames")


if __name__ == "__main__":
    main()
