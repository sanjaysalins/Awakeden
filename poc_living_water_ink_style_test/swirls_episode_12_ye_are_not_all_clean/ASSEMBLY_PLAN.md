# Assembly Plan — "Ye Are Not All Clean"

Built from REAL forced-alignment on the locked, GATE-1-approved `narration.mp3` (74.55s total file,
74.32s of speech, natural pace — no time-stretch), not word-count estimates. Alignment run via
`pipeline/assembly_align.py` (local whisper backend, $0), cached at `narration.alignment.json`.
`_DESIGN_BRIEF.md` §1's own word-proportional table (167 words → per-beat estimates) is superseded
by this file for shot-timing purposes — use these real numbers.

## Real per-beat durations (measured, whisper forced-alignment probe)

| Unit | Start | End | Duration | Gap before | Content |
|---|---|---|---|---|---|
| Front cover | 0.00s | 3.74s | 3.74s | — | "Judas walked out into the night on feet Jesus had washed." |
| F01 | 5.14s | 13.36s | 8.22s | 1.40s | "John says the devil had already 'put into the heart of Judas Iscariot, Simon's son, to betray him.' Jesus knew." |
| F02 | 14.58s | 19.52s | 4.94s | 1.22s | "He knew as He poured the water. He knew as He dried their feet with the towel." |
| F03 | 20.82s | 34.38s | 13.56s | 1.30s | "Then He told them, 'ye are clean, but not all.' And He quoted the old word for betrayal, from Scripture: 'He that eateth bread with me hath lifted up his heel against me.'" |
| F04 | 35.84s | 46.46s | 10.62s | 1.46s | "He handed Judas the sop — a piece of dipped bread. 'That thou doest, do quickly.' Some at the table thought he had gone to buy food." |
| F05 | 46.46s | 50.34s | 3.88s | **0.00s** | "Judas 'went immediately out: and it was night.'" |
| F06 (hero) | 51.92s | 63.34s | 11.42s | 1.58s | "Jesus did not wash those feet because Judas earned it. He washed them knowing Judas would betray Him anyway. That is what His love does when it already knows the worst." |
| Back cover | 64.78s | 74.32s | 9.54s | 1.44s | "He knows your heart, every corner of it, like that. He has not put the towel down — bring Him your worst." |

**Total: 74.32s narration + ≥3.0s mandatory landing hold (INV-26) = ~77.3s minimum final cut.**

## The F04→F05 hard-cut finding — real, not assumed

**The gap between F04 and F05 is 0.00s.** The narration runs "...thought he had gone to buy food.
Judas 'went immediately out: and it was night'" as one continuous breath — no pause at all between
"food." and "Judas." `_DESIGN_BRIEF.md` §1 designed F04/F05 as two separate pages for a real visual
reason (the lit table scene vs. the dark doorway are two different pictures, and "and it was night"
earns its own held silence for the eye), but the ear gets no natural pause to cut on at that exact
boundary. **The visual cut at 46.46s must be built as a deliberate hard cut in the edit — it cannot
ride a breath or a soft dissolve.** Whoever assembles the final video should treat this as a known,
intentional edit point, not a bug to smooth over.

## Native clip length vs. real target — per shot

Flow's native clip length is 8-10s (longer available on some models via "longest available").
Real targets below; `LONG` = ask for the model's longest available single-generation length.

| Shot | Real target | Native fit | Ask for |
|---|---|---|---|
| Front cover | 3.74s | well under native | default length, heavy trim/freeze at assembly |
| F01 | 8.22s | close fit | default length |
| F02 | 4.94s | well under native | default length, trim at assembly |
| F03 | 13.56s | **over native** | **LONG — longest available** (still likely needs ~3-5s freeze-hold at assembly; this is the episode's single densest page — two KJV quotes in one breath) |
| F04 | 10.62s | at/near native ceiling | LONG if available, else default |
| F05 | 3.88s | well under native | default length, trim/freeze at assembly |
| F06 (hero) | 11.42s | **over native** | **LONG — longest available** (likely needs ~1-3s freeze-hold at assembly) |
| Back cover | 9.54s + ≥3.0s landing hold ≈ 12.5-13s | **over native, and must stay visibly alive through the hold** | **LONG — longest available**; back cover's clip must not read as frozen dead the instant narration stops — the blue-gold drift (per `_DESIGN_BRIEF.md` §4) needs to still be moving through the full hold |

Only F03, F06, and the back cover need genuine extension beyond a native clip; everything else
trims down or needs a light 1-2s hold. F03 and F06 both carry real content weight (F03 = the two
densest KJV quotes in the piece; F06 = the rhetorical peak) so their extra length is earned, not a
design accident.

## Landing hold requirement (INV-26, this project's own binding rule)

After the last spoken word (74.32s), video AND audio must both keep running for a minimum ≥3.0s
hold before the file ends — never a silent early cutoff. Final cut minimum length: **~77.3s**.
Back cover's clip carries this entire hold and must stay visibly alive through it (the blue-gold
band still drifting, per `_DESIGN_BRIEF.md` §4's own animation direction — "never lowering toward
the basin, never leaving the upper part of the frame," which already describes a slow, ongoing
drift well suited to holding through the landing). `check_landing_hold.py` (this project's own $0
gate) should confirm this once the cut is built, same as every other episode.

## Hero-bookend structure — confirmed intact

Front cover opens the piece (0.00s), back cover closes it (64.78s through the landing hold) —
matches this project's standing hero-bookend convention. Note this episode's covers are
deliberately asymmetric (per `_DESIGN_BRIEF.md` §4's own stated judgment call): front carries
Judas mid-exit (the hook's own picture), back carries no human figure at all (the basin/towel
alone, echoing F06) — not a mirrored pair like some prior episodes, a deliberate choice tied to
this episode's landing addressing the viewer past Judas's own unresolved story.

## What this feeds

`FLOW_RUN_SHEET.md` (same folder) uses these exact real numbers in its Global Settings per-clip
length table — do not re-derive from word counts there.
