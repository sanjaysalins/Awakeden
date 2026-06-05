# Isaiah 53 stills re-do — PLAN v2 (post red-team + ai-panel, user decisions locked)

Supersedes v1. Panel (gemini FAIL, claude REVISE, codex REVISE) + my full-res re-audit
forced three corrections: (a) my v1 audit was thumbnail-based and MISSED real defects;
(b) several "extend the existing path" claims were net-new code; (c) cost/spend math was soft.

## User decisions (locked)
- **Scope: redo ALL defective stills** (the true hero-still standard).
- **Show the cross:** render an actual ROBED crucifixion at the atonement beats.
- **Gaza road:** regenerate S13 + S14 + S15 as one consistent set (S14 is NOT a good anchor —
  its ornate gilded carriage reads more 18th-c European than 1st-c chariot).
- Opening concept: **"Prophet on the high place"**, but with **NO cross foreshadow** (RT1 +
  panel G5: a literal/implied cross in Isaiah's wilderness is anachronistic and bleeds the
  model toward drawing crosses — drop the distant hill/crosses; carry it on scale + light).

## Corrected full-res audit (every still viewed at full size)
REDO (defects): S1 (weak/off-style open), S3 (triptych frame + putti), S6 (no cross — must
show robed crucifixion), S7 (literal gilt picture-frame triptych), S10 (17th-c Dutch hats),
S12 (Christian cross headstones + European cemetery — anachronistic + premature), S13/S14/S15
(Gaza continuity + S14 non-1st-c chariot), S16 (no cross — robed crucifixion under dark sky).
MINOR: S2 (scroll script), S11 (a few European garments). RE-VERIFY: S19.
KEEP (confirmed full-res): S4, S5, S8, S9, S17, S18, S20, S21.

## The production loop (binding per scene)
NARRATION → MOTION → FIRST FRAME → ELEMENTS (must already be in the still) → animate ONLY
pre-placed elements, lock the rest → **QC the WHOLE clip** (≥6 evenly-spaced frames), not
just the last frame. Hero-still bar: one focal subject readable <1s, strong chiaroscuro,
scale cue, tells more than it shows.

## Panel fixes folded in (each maps to a finding)
1. **Idempotence (claude C1 / codex 1 — BLOCKER):** `_render_images_16x9.py:80` skips existing
   PNGs and `_animate_*` skip existing MP4s. → NEW step: move the stale PNGs + the base MP4s
   for every redo scene + S13's `_cont*` clips into `_redo_backup/` BEFORE re-render. Nothing
   renders otherwise.
2. **No multi-ref hallucination (gemini G2 / claude C3 / codex 2):** NBPProvider attaches only
   the Jesus ref, and multi-image role-conditioning on gemini-3-pro-image is unreliable. →
   do NOT build a style+character ref attach. Christ consistency stays on the existing Jesus
   ref. **Ethiopian + chariot consistency = identical, detailed TEXT description reused across
   S13/S14/S15** (same skin tone, same robe, same turban, same authentic chariot), rendered as
   a batch, and I QC the three together for match.
3. **Audit is mine, fail-closed (claude C2 / codex 5 / gemini G4-rebuttal):** the long-form path
   has no audit/retry and the generic SDK audit fails OPEN on a usage cap. → I do QC by VIEWING
   each render with the Read tool (this harness can; I've done it all session). Accept/adjust/
   re-roll. **Hard cap 3 image attempts/scene**, then stop + report.
4. **Animation is the real uncapped risk (claude C4/C5):** S3/S15 "a figure rises" = veo's known
   invent-motion failure. → figure scenes get **camera-only motion** (push-in / tilt / light
   brightening), no subject locomotion. **Cap animation attempts** (≤2 per scene/continuation).
   Cross scenes (S6/S16) robed → veo first, **Kling fallback on NSFW** (already wired).
5. **No legible scripture (codex 8):** style tail is "no text". → scrolls show faint,
   non-legible ancient script (no attempt at legible Hebrew/Greek that fights the style).
6. **Re-bank decision (claude C6):** redo renders will NOT auto-bank (skip `bank()`), so the
   original `image_library` plates are not silently overwritten; re-bank the improved neutral
   plates deliberately only after the film is locked.
7. **Assembler reality (claude C7 / codex 7):** `_assemble_16x9.py` is a full re-run, not a
   segment swap. → keep `Isaiah53_16x9.frozen.bak.mp4` + a pre-redo copy; compare before/after.
8. **Cost honesty + pre-spend gate (codex 6):** real numbers below; **I do NOT spend until the
   user says go.**

## Per-scene redo specs (loop-applied, brief)
- **S1 Prophet/high place:** monumental prophet on a storm-dawn clifftop, huge Hebrew scroll
  snapping in wind, sky split by one shaft of light, vast depth. Motion: wind in scroll+robe,
  clouds, light widens (camera push-in). Elements: prophet, scroll, cloth, dust, light. NO cross.
- **S3 Behold/exalted:** ONE unified radiant exalted figure in breaking glory; face luminous/
  abstracted (don't pre-reveal the Servant before S4). No panels/triptych/cherubs. Motion:
  glory brightens (camera slow rise) — NOT a rising figure.
- **S6 Wounded/cross:** robed crucified Servant, pierced hands shown, head bowed, dark sky,
  reverent/restrained. Motion: cloth/sky stir, slow push-in to the pierced hand.
- **S7 Chastisement/substitution:** single unified tableau — the Servant bowed under a great
  weight, freed figures upright in soft light behind. NO frame/panels. Motion: light shift,
  lateral drift.
- **S10 Silent trial:** bound Servant before accusers in **1st-c Judean dress** (priestly robes,
  head cloths/turbans), chiaroscuro hall. Motion: flame/shadow, slow push-in.
- **S12 Rich man's tomb:** 1st-c **rock-hewn tombs** in a dusk hillside, one set-apart sealed
  tomb, single light. **No cross headstones, no European sarcophagi.** Motion: dusk haze, approach.
- **S13/S14/S15 Gaza trio (one canon):** dark-skinned Ethiopian official, consistent rich robe +
  turban, ONE authentic 1st-c chariot (light two-wheeled, not a gilded carriage), two horses.
  S13 = riding/reading (directional). S14 = Philip meets the halted chariot. S15 = Philip points
  him to the luminous canon Christ over the open scroll (Baroque, not smooth-devotional).
- **S16 It pleased the LORD:** robed crucified Servant on the hill under a black thunderous sky,
  one shaft of heaven's light. Motion: clouds churn, light steady, slow push-in.
- **S2 (minor):** scroll w/ faint non-legible script. **S11 (minor):** swap European garments
  for Near-Eastern robes.

## QC (whole-clip, mine)
Per redone clip: extract ~6 even frames → montage → I check: (1) era-correct dress/artifacts,
(2) no frame/panel/triptych, (3) no morph / no invented elements across the clip, (4) style
matches kept neighbors, (5) Christ=canon / Ethiopian=consistent, (6) S1 hero/epic test.

## Cost & pre-spend gate
- ~12 stills × ~1.5 avg attempts ≈ **~$9 images** (hard cap 3/scene ≈ $18 worst case).
- ~17 veo clips (incl. Gaza chains) ≈ **~$11** (+ Kling fallback on the 2 cross scenes if NSFW).
- Re-assembly $0.  **Estimated $20–28; hard not-to-exceed ~$35.**
- **GATE: render nothing until the user approves the spend.** Stop at any per-scene 3-attempt
  cap and report rather than burn budget.
