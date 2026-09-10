# Assembly Plan — "My Lord and My God"

Built from the REAL synthesized narration (`narration.mp3`, 61.30s, natural pace — no time-stretch),
not word-count estimates. Now on its second revision: the original 6-shot list left two shots (F01
and Back Cover) carrying a heavy freeze-hold burden (+6.9s and +5.3s respectively) because each was
covering two distinct narration beats in one clip. Split each into two shots — 8 total now — so
almost every shot needs only a light trim or a small 1-2s hold. Fix real shot targets against this
file, not the brief's original beat-math table.

## Real per-turn durations (measured, `per_turn_synth.py` probe)

| Turn | Speaker | Text | Duration |
|---|---|---|---|
| 00 | narrator | "Ten men said the same thing: 'We have seen the Lord.'" + lead-in to Thomas | 6.80s |
| — | *pause* | | 0.30s |
| 01 | thomas | "Except I shall see in his hands the print of the nails..." | 11.44s |
| 02 | narrator | "Eight days he stayed with them anyway..." + "Then came Jesus, the doors being shut, and stood in the midst, and said," | 11.12s |
| — | *pause* | | 0.30s |
| 03 | jesus | "Peace be unto you." | 1.36s |
| 04 | narrator | "He turned straight to Thomas:" | 1.60s |
| — | *pause* | | 0.30s |
| 05 | jesus | "Reach hither thy finger, and behold my hands..." | 10.88s |
| 06 | narrator | "Thomas didn't touch a thing. He only said," | 2.96s |
| — | *pause* | | 0.30s |
| 07 | thomas | "My Lord and my God." | 1.60s |
| 08 | narrator | "And Jesus answered him — answered you too:" | 3.76s |
| — | *pause* | | 0.30s |
| 09 | jesus | "Because thou hast seen me, thou hast believed..." | 8.32s |

**Total: 61.30s.**

(Turn 02's ~11.12s is estimated to split ~49%/51% between its two sentences by character count, not
separately measured — close enough for shot-timing purposes, not exact to the frame.)

## Shot-to-timeline mapping and REAL target durations (8 shots)

| Shot | Name | Timerange | Real duration needed | Native clip | Freeze/trim needed |
|---|---|---|---|---|---|
| 1 | Front Cover | 0.00 – 7.10s | **~7.1s** | 8-10s | trim, none |
| 2 | F01 "I will not believe" | 7.10 – 18.54s | **~11.4s** | 8-10s | light, ~1-2s |
| 3 | F02 "Eight Days" *(NEW)* | 18.54 – 24.0s | **~5.5s** | 8-10s | trim, none |
| 4 | F03 "Peace be unto you" | 24.0 – 31.32s | **~7.3s** | 8-10s | trim, none |
| 5 | F04 "Reach hither" | 31.32 – 44.10s | **~12.8s** | 8-10s | real, ~3-4s — the one shot still needing a genuine extension |
| 6 | F05 "My Lord and my God" | 44.10 – 48.96s | **~4.9s** | 8-10s | trim, none |
| 7 | F06 "Answered You Too" *(NEW)* | 48.96 – 52.72s | **~3.8s** | 8-10s | trim heavily, none |
| 8 | Back Cover | 52.72 – 61.30s + landing hold | **~11.6s** (8.32s narration + ≥3.0s hold) | 8-10s | light, ~1-2s |

**Total raw need: 64.3s** (61.3s narration + 3.0s mandatory landing hold), matching the final cut
length exactly. Only Shot 5 (F04, the invitation) still needs a real freeze-hold extension — every
other shot either trims down or needs only a light 1-2s hold. This is the fix for the two shots
that used to need heavy stretching.

## What used to be the problem, and why splitting fixed it

- **Old Shot 2 (F01)** covered BOTH Thomas's declaration (11.44s) AND the "eight days" bridge
  (~5.46s) in one clip — 16.9s total from an 8-10s native clip, a ~7s stretch. Split: F01 now covers
  only the declaration (~11.4s, close to native); the new "Eight Days" shot covers the bridge
  (~5.5s, well under native — trims down instead of stretching).
- **Old Shot 6 (Back Cover)** covered BOTH the narrator's pivot line ("And Jesus answered him —
  answered you too") AND Jesus's closing quote AND the landing hold — 15.3s total from an 8-10s
  native clip, a ~5-7s stretch, on top of being the one shot where a heavy stretch was hardest to
  hide (continuously walking figures, no completing gesture — boomerang looks broken on this kind
  of motion, confirmed elsewhere in this project). Split: the new "Answered You Too" shot covers the
  narrator pivot (~3.8s, trims heavily); Back Cover now only covers the closing quote + landing hold
  (~11.6s, close to native).

**Shot 5 (F04, "Reach hither") is the one remaining real extension** — Jesus's invitation quote runs
10.88s on its own, plus narrator lead-in, totaling ~12.8s against an 8-10s native clip. This wasn't
split because it's a single continuous beat (Jesus speaking one uninterrupted invitation) — there's
no natural internal cut point the way there was in the other two. A ~3-4s freeze-hold here is
reasonable and matches the shot's own "invitation held open, unmoving" design.

## Landing hold requirement (INV-26, this project's own binding rule)

After the last spoken word (narration ends at 61.30s), the finished video AND audio must both keep
running for a minimum ≥3.0s hold before the file ends — never a silent early cutoff. That means:

- **Final cut minimum length: ~64.3s**, not 61.3s.
- Shot 8 (Back Cover) carries this entire hold — its clip needs to still be visibly alive (walking
  figures continuing, sky traces drifting) through the full ≥3.0s past the last word, not frozen
  dead the instant narration stops.
- `check_landing_hold.py` (this project's own $0 gate) should confirm this once the cut is built —
  run it before calling this episode done, same as every other episode.

## Hero-bookend structure — confirmed intact

Front Cover opens the piece (0.00s), Back Cover closes it (52.72s through the landing hold) — this
matches this project's standing convention (hero bookend open/close) without needing any redesign.

## What this changes in the brief

`GOOGLE_FLOW_BRIEF.md` now has 8 story shots (was 6, was 4 originally), each with its per-shot
"Target" line citing these real numbers. Generate to the real target where practical; Shot 5 (F04)
is the only one that still needs a genuine freeze-hold extension at assembly time.
