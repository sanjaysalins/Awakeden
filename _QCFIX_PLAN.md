# Clip-QC fix batch — state file (2026-07-19)

User mandate: nothing uploaded yet; fix all 52 FAIL clips, production-worthy, no AI slop.
Approved: test-gate (~$6 spent, done) then full batch (quoted $46-60 total).

## PROVEN RECIPES (test-gate rounds 1-2, all eye-verified)
1. BLOOD class -> Gemini-edit still to remove painted hanging drips (KEEP-LIST per
   still: nails/nail heads, faces, composition; Gemini REPAINTS — eye-check every
   edit; the test edit lost the nail heads and must be REDONE with the keep-list),
   then seedance1_5 4s frozen-tableau positive-only roll. Proven: 31_dryroll clean.
2. SNOW class (EW01) -> seedance1_5 instead of veo3_1_lite (veo re-grows particles
   even with clean prompts). Proven: 07_seedance clean + oil look held.
3. INVENTION class -> push-in ONLY (never pull back past the painting edge),
   frozen-tableau phrasing. Proven: slice_13 veo3 push-in clean.
4. WRITING class -> "fixed exactly as painted" phrasing, camera led away from text.
   Proven: david_psalmist clean scroll.
Standard prompt block: "The entire painting holds perfectly still like a printed
page — every figure, face, and mark stays fixed exactly as painted. Only the camera
moves." Model choice: seedance1_5 for ALL re-rolls (EW01 included — veo3 is the
particle source; Seedance held Baroque at near-static motion).

## PROMOTABLE TEST CLIPS (QC with the batch, then replace originals)
- longform/EW01_Two_Goats/v1/visual_16x9/_qcfix_test/slice_13.mp4
- longform/EW01_Two_Goats/v1/visual_16x9/_qcfix_test/07_they_brought_me_two_goats_and_i_cast_lot.mp4
- longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked/clips/_qcfix_test/david_psalmist.mp4
NOT promotable: 31_dryroll (source still lost the nails — redo edit + re-roll).

## WORKLIST (unique fix jobs; qc_verdicts.json in scratchpad has full defect notes)
STILL EDITS FIRST (Gemini, keep-list, eye check) then re-roll from edited still:
- bronze 12, 16, 18, 25, 31, two_thieves_foreground (native 16:9 stills, hanging drips out)
- isaiah nail_through_hand, willing_offering
- bronze reuse_face_on_cross (9:16 shorts still — find source in shorts pool; roll at 9:16)
ROLL-ONLY (frozen-tableau/push-in/writing recipes):
- isaiah: crowd_mocking, hands_of_light_open, isaiah_writing_lamplight, mourners_only_son,
  nations_streaming_wide*, poured_out_bones*, three_days_dark_tomb, tomb_stone_sealed
  (*shared byte-identical with psalm22 — one roll, copy to both lanes)
- psalm22: lots_dice_closeup, mockers_below_cross_low, thirst_dust (watch lip mark — if
  blood leaks, escalate to still edit), worm_lowest
- bronze: 03, 07, 10, 15_hezekiah, 19, 20, 22, reuse_ninth_hour_darkness (9:16, INRI —
  writing recipe from shorts still)
- EW01 (all seedance): 04, 05, 08 (watch blood bowl), 09, 10, 11, 14, 16, 17, 21, 22, 25,
  slice_01, slice_03, slice_07, slice_08, slice_21, slice_22, slice_24
Durations: 4s seedance (16:9) except 9:16 reuse rolls (aspect 9:16).

## PIPELINE AFTER ROLLS
1. QC every output: extract_frames + vision review (same LF_CRITERIA) + my eye on fails.
2. Promote passes: archive old clip to <clips_dir>/_qcfix_replaced/, move new into place,
   record_verdict PASS sidecar. One retry per still-leaking clip, then stop and report.
3. Rebuild all 4 films ($0): Bronze + Psalm22 + Isaiah livingpage lanes, EW01 window lane
   (_assemble_16x9). Then score + sfx (pipeline/score_mix + pipeline/sfx_bed wrappers),
   check_landing_hold.py, panel_variety, animated-pct gate, suite.
4. Refresh _CLIPQC_REVIEW.html galleries + final report with full file:/// links.

## LEDGER
Test spend so far ~$6 (4 rolls r1 + 1 edit + 2 rolls r2, all in spend ledger).
Remaining budget ~ $40-50: ~9 Gemini edits ($0.50 ea) + ~46 seedance rolls ($0.72 ea)
+ retry headroom.
