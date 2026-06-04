"""One-off: align the Isaiah 53 narration + print absolute timestamps for the
pilot soundstage cue phrases. Free (local whisper). Read-only."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.assembly_align import align  # noqa: E402

V1 = ROOT / "longform" / "01_Isaiah_53_Suffering_Servant" / "v1"

# cue phrases to locate (normalized token match against the aligned word stream)
CUES = {
    "M1 OPEN (wilderness wind)":                    "Seven hundred years before a Roman nail",
    "M2 BEHOLD start (God - SACRED CLEAN)":        "Behold my servant shall deal prudently",
    "M2 picture breaks (visage marred)":           "his visage was so marred more than any man",
    "M2 despised + rejected (crowd murmur)":       "He is despised and rejected of men",
    "M3 EXCHANGE start (low drone in)":            "Surely he hath borne our griefs",
    "M3 NAIL (single strike)":                      "he was wounded for our transgressions",
    "M4 LAMB to slaughter":                         "he is brought as a lamb to the slaughter",
    "M4 sheep before shearers":                     "as a sheep before her shearers is dumb",
    "M4 honest objection (bed thins)":             "For centuries many thoughtful Jewish readers",
    "M5 GAZA road (chariot in)":                   "riding home in his chariot reading this very chapter",
    "M5 Philip approaches (footsteps)":            "comes alongside the chariot",
    "M5 preached unto him Jesus":                   "began at the same scripture and preached unto him Jesus",
    "M6 THUNDER (it pleased the LORD)":            "Yet it pleased the LORD to bruise him",
    "M7 DAWN (resurrection turn)":                  "he shall see his seed he shall prolong his days",
    "M7 arm of the LORD (swell)":                  "The arm of the LORD the saving strength of God",
    "CLOSE (His name is Jesus)":                    "His name is Jesus",
}


def norm(t: str) -> str:
    return re.sub(r"[^a-z0-9']", "", t.lower())


def find(words, phrase):
    toks = [norm(x) for x in phrase.split()]
    nwords = [norm(w.text) for w in words]
    n = len(toks)
    for i in range(len(nwords) - n + 1):
        if nwords[i:i + n] == toks:
            return words[i].start, words[i + n - 1].end
    # loose: match first 3 + last token
    for i in range(len(nwords) - n + 1):
        if nwords[i] == toks[0] and nwords[i + 1] == toks[1] and nwords[i + n - 1] == toks[-1]:
            return words[i].start, words[i + n - 1].end
    return None


def fmt(s):
    return f"{int(s // 60)}:{s % 60:05.2f}"


words = align(V1)
total = words[-1].end if words else 0.0
print(f"\n=== {len(words)} words, ends at {fmt(total)} ({total:.1f}s) ===\n")
for label, phrase in CUES.items():
    hit = find(words, phrase)
    if hit:
        s, e = hit
        print(f"{label:<42} {fmt(s)} -> {fmt(e)}   [{s:.2f}-{e:.2f}s]")
    else:
        print(f"{label:<42} NOT FOUND  ('{phrase[:40]}...')")
