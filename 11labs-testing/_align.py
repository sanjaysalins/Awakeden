"""Force-align the spoken narration to the extracted audio -> work/words.json.
Free / offline (WhisperX phoneme align). Reuses veed_io.aligner.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from veed_io.aligner import forced_align_script  # noqa: E402

NARR_MD = Path(r"G:\My Drive\0 Personal\0Company\jobs\0salinss\saltandlightkingdom"
               r"\0 Christianity\0 People Who Encountered Jesus"
               r"\08 The Well That Never Runs Dry\narration.md")


def spoken_text() -> str:
    raw = NARR_MD.read_text(encoding="utf-8")
    body = raw.split("----")[0]                       # drop the SEO ledger
    # join non-empty lines into one spoken block
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    return " ".join(lines)


def main():
    wav = str(HERE / "work" / "narration16k.wav")
    script = spoken_text()
    print(f"[align] {len(script.split())} script words")
    words = forced_align_script(wav, script)
    out = HERE / "work" / "words.json"
    out.write_text(json.dumps(words, indent=2), encoding="utf-8")
    print(f"[align] wrote {len(words)} timed words -> {out}")

    # quick anchor report for the SFX we care about
    def find(*needles):
        for i, w in enumerate(words):
            tok = re.sub(r"[^a-z]", "", w["w"].lower())
            if tok in needles:
                return w
        return None

    for label, needles in [
        ("waterpot", ("waterpot",)),
        ("ran", ("ran",)),
        ("noon(first)", ("noon",)),
        ("everlasting", ("everlasting",)),
        ("still-offers", ("still",)),
        ("last-word", (re.sub(r"[^a-z]", "", words[-1]["w"].lower()),)),
    ]:
        hit = find(*needles)
        if hit:
            print(f"  anchor {label:<16} '{hit['w']}'  {hit['start']:.2f}-{hit['end']:.2f}s")


if __name__ == "__main__":
    main()
