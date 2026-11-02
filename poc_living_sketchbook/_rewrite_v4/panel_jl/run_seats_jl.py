import sys
from pathlib import Path
sys.path.insert(0, r"F:\slk\PycharmProjects\JesusInTheBible")
import independent_review as IR
BASE = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_living_sketchbook\_rewrite_v4\panel_jl")
# distinct lens per seat, appended to the same pack (no seat sees another's work)
LENS = {
 "claude": "Your lens: the NEWCOMER. Check every line as someone with no Bible knowledge hearing it once.",
 "codex": "Your lens: the BIBLE READER. Check every claim against the source text and plain doctrine.",
 "grok": "Your lens: the HOOK and the LANDING. The first 2 seconds and the last line must be unforgettable and specific to this story.",
 "cursor": "Your lens: ECONOMY. Say it in the fewest plain words that still land.",
}
pieces = sys.argv[1].split(",") if len(sys.argv) > 1 else ["jacobs_ladder"]
for piece in pieces:
    d = BASE / piece
    base = (d/"header.txt").read_text(encoding="utf-8") + "\n\n" + (d/"pack.md").read_text(encoding="utf-8") + "\n\n" + (d/"format.txt").read_text(encoding="utf-8")
    for seat, lens in LENS.items():
        out = d / f"draft_{seat}.md"
        if out.exists() and "## MY NARRATION" in out.read_text(encoding="utf-8", errors="ignore"):
            continue
        name, ok, text, dur = IR.run_one(seat, base + "\n\n" + lens, d)
        out.write_text(text, encoding="utf-8")
        print(piece, seat, "ok" if ok else "FAIL", round(dur), flush=True)
print("ALL DONE", flush=True)
