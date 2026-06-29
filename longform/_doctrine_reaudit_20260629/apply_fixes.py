"""apply_fixes.py — apply the 4 CONFIRMED doctrinal/narrative-fact fixes.

Each fix lists every variant file that carries the line (narration.md = source
of truth, narration-tagged.md = synth input, *.spoken.txt). We assert the OLD
string is present EXACTLY ONCE in each target before replacing (fail-closed:
abort if the text drifted), then record before/after to fixes.json for the
report. We do NOT re-lock — the spoken text changes, so the existing audio/video
go stale and the fail-closed lock correctly blocks re-render until the user
re-voices (a separate, metered step). Each fixed piece = NEEDS-REVOICE.
"""
import json
from pathlib import Path

LF = Path(__file__).resolve().parent.parent          # longform/
WORK = Path(__file__).resolve().parent

FIXES = {
    "EW06_Noah__v1": {
        "severity": "narrative-fact",
        "scripture_ref": "Gen 6:15",
        "note": "300 cubits is the ark's LENGTH (height was 30); 'climbed into the sky' wrongly made it vertical.",
        "old": "Three hundred cubits it climbed into the sky on dry land",
        "new": "Three hundred cubits it stretched across the dry land",
        "files": ["EW06_Noah/v1/narration.md",
                  "EW06_Noah/v1/narration-tagged.md",
                  "EW06_Noah/v1/narration.spoken.txt"],
    },
    "EW03_Joseph__v1": {
        "severity": "narrative-fact",
        "scripture_ref": "Gen 42:3-4; 45:1-4",
        "note": "The 'I am Joseph' reveal (Gen 45) was on the SECOND visit with all eleven brothers present (Benjamin included); 'ten' belongs to the first visit. Dropped the false count.",
        "old": "But on that day, ten travel-worn men came begging me for grain, not knowing the ruler they bowed to. They were my brothers — the very brothers who had sold me, whose faces I had carried in the dark for half my life.",
        "new": "But on that day, my travel-worn brothers came begging me for grain, not knowing the ruler they bowed to — the very brothers who had sold me, whose faces I had carried in the dark for half my life.",
        "files": ["EW03_Joseph/v1/narration.md",
                  "EW03_Joseph/v1/narration-tagged.md",
                  "EW03_Joseph/v1/narration.spoken.txt"],
    },
    "EW01_Two_Goats__v1__short": {
        "severity": "narrative-fact",
        "scripture_ref": "Lev 16:21-22",
        "note": "Lev 16:21 has the scapegoat sent away 'by the hand of a fit man' — the high priest did not personally drive it out. Same Aaron-overclaim family as the prior Lev 10 catch.",
        "old": "confessed every sin of the people over it, and drove it into the desert to be lost.",
        "new": "confessed every sin of the people over it, and sent it away into the desert to be lost.",
        "files": ["EW01_Two_Goats/v1/short/narration.md",
                  "EW01_Two_Goats/v1/short/narration-tagged.md",
                  "EW01_Two_Goats/v1/short/narration.spoken.txt"],
    },
    "02_Psalm_22_Song_From_The_Cross__v1__shorts__03_The_Forsaken_Cry": {
        "severity": "narrative-fact",
        "scripture_ref": "Matt 27:46 (cf. Luke 23:34)",
        "note": "'did not speak His own words first' implies the dereliction cry was Jesus' opening word from the cross; Luke 23:34 ('Father, forgive them') precedes it. Reworded to keep the hook (borrowed words) without the false order. All 4 panel reviewers confirmed.",
        "old": "From the cross, Jesus did not speak His own words first — He cried a psalm David had written a thousand years before.",
        "new": "From the cross, Jesus cried words that were not His own — a psalm David had written a thousand years before.",
        "files": ["02_Psalm_22_Song_From_The_Cross/v1/shorts/03_The_Forsaken_Cry/narration.md",
                  "02_Psalm_22_Song_From_The_Cross/v1/shorts/03_The_Forsaken_Cry/narration-tagged.md"],
    },
}


def main():
    record = {}
    # 1) verify EVERY target has the old string exactly once (fail-closed)
    for pid, fx in FIXES.items():
        for rel in fx["files"]:
            p = LF / rel
            txt = p.read_text(encoding="utf-8")
            n = txt.count(fx["old"])
            assert n == 1, f"ABORT: '{fx['old'][:40]}...' found {n}x in {rel} (expected 1)"
    # 2) apply
    for pid, fx in FIXES.items():
        touched = []
        for rel in fx["files"]:
            p = LF / rel
            txt = p.read_text(encoding="utf-8")
            p.write_text(txt.replace(fx["old"], fx["new"]), encoding="utf-8")
            touched.append(rel)
        record[pid] = {
            "severity": fx["severity"], "scripture_ref": fx["scripture_ref"],
            "note": fx["note"], "before": fx["old"], "after": fx["new"],
            "files": touched, "relock_needed": True, "revoice_needed": True,
        }
        print(f"FIXED {pid}  ({len(touched)} files)")
    (WORK / "fixes.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"\nwrote {WORK / 'fixes.json'}  ({len(record)} fixes)")


if __name__ == "__main__":
    main()
