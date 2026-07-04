# THE LIVING PAGE — the default motion-comic standard (LOCKED 2026-07-02)

> The user locked this after the Psalm 22 M1 v3 test: every motion-comic finishing layer is
> DIRECTED like an animator, never assembled like a template. This document is the ratchet:
> the bar only moves UP. When this and a per-episode spec disagree, this wins.

## 1. The language (the five moves)

| Move | Rule | Cost |
|---|---|---|
| **SLAM** | Panels arrive ON the narration's exact words (alignment.json): ~4-frame slide + 60%-alpha impact flash + decaying page shake + a low boom (sound_library, ≥ -8dB under narration; nail_strike for nails, thunder for storms) | $0 |
| **TAKEOVER** | A beat may end with the camera diving INTO a chosen panel (zoompan to its centre) so the cut lands inside the art | $0 |
| **SACRED STILLNESS** | Red-letter Scripture beats NEVER slam, punch or shake. The contrast is the reverence. ≤2 held beats, none >8s | $0 |
| **CRAFT** | Hand-wobbled ink borders, soft panel drop-shadows, halftone paper. Red appears ONLY as Scripture, keywords, and blood | $0 |
| **ALIVE** | Every panel moves (Kling hero or dynamic_cam). Frame 1 is never empty paper — the thumbnail is a held wide, then the first slam | Kling ~$0.65/clip |
| **RAMP** | Viral speed ramp (`"ramp": true`): the beat's art plays ~2.5x for its first ~0.8s then settles — fast-in, settle, cut. Hook + CTA beats. NEVER on beats with mid-beat slams/border-break (word-timed events would desync; the engine guards it) | $0 |
| **WHIP** | Whip-cut (`"whip": true`): a horizontal motion-blur streak on the first ~3 frames + a synth whoosh — the cut reads as camera energy, not a splice | $0 |
| **INSERT** | Flash-frame insert (`"inserts":[{at,slug,frames}]`): a full-bleed still stabbed in for ~4 frames (comic panel-burst recall — the nail under "raised his spear"). Exempt from reuse counters BY DESIGN; ~2-3 per short | $0 |
| **TICK** | Cut ticks (`"cut_ticks": true`): a -19dB synth snap on every ordinary cut, so slams keep their rank while every cut has texture. Skips beat 1, red-letter beats and the border-break | $0 |

Added after the Pierced pilot punch-pass (2026-07-03, "punchier + viral edits"). All four are
measured in the DoD json (`ramps` / `whips` / `flash_inserts` / `cut_ticks`).

## 2. The engine

- Compositor: `longform/02_Psalm_22_Song_From_The_Cross/build_livingpage_16x9.py`
  (graduate to a shared `longform/_livingpage/` engine at first reuse in another episode).
- Spec pattern: `livingpage_m1.spec.json` — per-clip `at` (absolute word time), `slide`, `flash`,
  `sfx`; per-beat `takeover{panel,start,zoom}`, `punch`, `sfx[[name,t,gain]]`, fracture `panel_at`.
- Carries ALL red-teamed v2 machinery: frame-exact segments (zero cut drift), the 3-tier
  motion-inflated caption solver (`caption_layout.py` + `caption_render16.py`), panel_fit crops,
  reuse rule (≥8 beats AND different crop), KJV verbatim + both-ways doctrine checks.

## 3. Definition of Done (adds to the episode spec's DoD)

1. Every slam lands within ±0.05s of its word (frame-snapped windows).
2. Slam audio is AUDIBLE: boom peaks within ~3dB of narration peaks at the slam.
3. Sacred beats measurably still (no slam/punch/shake events inside them).
4. Frame 1 holds real art. No empty-paper open.
5. **The ratchet test:** side-by-side with the LAST LOCKED piece, the new cut reads the same
   family or better — never worse. A regression blocks LOCK.

## 3b. Scale rules for LONGS (locked after the Psalm 22 full-film critique, 2026-07-02)

The user caught the failure mode: at 99 beats, the reuse rule + dyncam fallback rebuilt the
slideshow at a faster cut rate (44 stills / 118 slots, top images 5-6x, 45 drift-only beats,
dash-grammar captions). These rules prevent it:

1. **Distinct still per beat is the default.** A still may appear at most TWICE in a film,
   never twice as a full-bleed single — the second use must be a grid panel or macro crop.
   Stills are the cheap ingredient (~$0.05); NEVER save money on stills.
2. **Generative floor:** ≥80% of beats carry true generative motion (Kling) in the finished
   film. dynamic_cam is for grid panels, writing stills and tiny inserts ONLY — a drifting
   full-bleed still is ken-burns and reads as slideshow.
3. **Mix the page:** full-bleed singles ≤50% of beats; the rest grids/fractures/slams.
   Key hero beats may use the timecoded multi-shot gallery-tour Kling prompt (hard cuts
   INSIDE the clip) for cinematic richness.
4. **Caption grammar — no AI slop on screen:** kinetic captions are short punchy phrases
   with NO dashes, no ellipses, no quotes; break thoughts into separate captions or lines.
   Scripture partial verses are marked by the TAG (v.14a, v.24b), never by "..." in the text.
5. **Sound is story-keyed:** beyond slam booms — ≥1 placed narrative sound per movement
   (crowd, dice, wind, dawn, congregation) + score automation dips at the sacred stops.
6. **Budget honestly:** a long at this standard costs ~$25-30 (≈ one standard episode).
   Do not silently trade the standard down to fit an old cap; pre-flight the real number.

## 4. The ratchet (how it always gets better)

Every session that invents a new move that survives the user's eye:
1. Codify it here (one row in §1, one DoD line in §3).
2. Make it a reusable spec flag in the engine (never a one-off hack).
3. `/learn` entry + memory update so the next session starts from it.
Nothing is removed from this doc without the user; techniques only accumulate.

## 6. THE PROTOCOL — creation + verification, stage by stage (LOCKED 2026-07-03)

Run via the `/livingpage` skill. Every stage ends in a GATE; no spend crosses a failed gate.
The user approved the Psalm 22 v3 film as THE calibration reference — when in doubt, open it
and match it: `longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9/LivingPage_Psalm22_16x9_scored.mp4`
(spec: `v1/visual_16x9_inked/livingpage_full.spec.json`).

**C0. The narration itself is gated FIRST — earned hook + earned landing.** Before any
choreography: `narration_gate.py "<narration.md>"` ($0, deterministic). FAILs a stock closer
("come to Jesus / turn to Him / look to Jesus") unless the piece's own quoted KJV uses that
verb; FAILs a landing that shares no significant word with the piece's Scripture/hook; FAILs
template hooks ("Did you know / Imagine"); WARNs corpus-stale closer verbs. The 5-CLI panel
now also scores HOOK 1-10 and LANDING 1-10 explicitly (<8 = REVISE). The gate makes lazy
impossible; the tournament + panel make it great.
**C1. Choreograph on the words ($0).** Word-level alignment.json → beats at clause level
(~4-5s median). Per beat: narration line, image CONCEPT justified from that line/verse, tpl,
slams on percussive words, punch on hooks, sacred bars still, takeover/border-break where the
text turns. GATE: `--lint` = 0 reuse violations, 0 standard_3b violations, median ≤6s.
**C2. Ground the stills ($0 then ~$0.05/still).** Every image = a spec in still_specs.json
(verse + distinct shot + signature + distinct_from). GATE: still_validate.py GREEN. Render via
BytePlus direct. GATE: eye-audit EVERY still (contact sheets fine) — anachronism, anatomy,
style-consistency (no uncolored strays), doctrine-weighted images (e.g. a body-shaped shroud
in an EMPTY tomb = fail). Re-roll fails. Write anchors.
**C3. Animate (~$0.65/clip).** INK camera-only prompts; HF Kling pro 16:9 (or 9:16), retry
502s, direct-Kling second, dyncam only as last resort AND only for grids/writing/inserts.
GATE: ≥80% of beats carry Kling/slam/punch (the lint measures it).
**C4. Build.** The living-page engine (slams/shake/takeover/border-break/heartbeat, frame-exact
segments, caption tier solver). GATE: DoD json — every number in §3 + standard_3b clean.
**C5. Sound.** Slam booms baked; ≥1 story-keyed sound per movement; score chain with dips at
the sacred stops. GATE: measure the mix (slam peaks within ~3dB of narration; dip window level
drops ≥4dB) — never trust it by construction.
**C6. Doctrine BOTH WAYS.** (a) script-check every red bar byte-vs-kjv_cache AND
text-vs-narration AND tag-vs-text (the Ps22:22/Heb2:12 class of error!); (b) the 5-CLI panel
on the clean caption artifact. Fix confirmed findings; disputed narration-level notes go TO THE
USER, never silently. GATE: 0 confirmed doctrinal/citation errors.
**C7. Eye + ear + ratchet.** Frames from every movement Read and judged; side-by-side with the
LAST LOCKED piece (same family or better — regression blocks LOCK); the review HTML with
measured DoD; the user's eye/ear is the final gate.

## 7. SHORTS — the same treatment at 9:16

The locked short (father_forgive_them) predates the living page; the next short pilots this:
- Same engine language: word-timed SLAMS, takeover dive, sacred stillness, craft borders,
  slam SFX, score dips. `comic_engine.set_page(1080,1920)` retargets; the livingpage builder's
  PAGE constant is parameterized at first 9:16 use.
- Same richness rules: ~13-16 beats need 13-16 DISTINCT images (a short never reuses a still);
  every beat Kling or slam; caption grammar identical (no dashes/ellipses ever).
- Same protocol C1-C7 (shorts panel-review the caption layer with the narration lock).
- Shorts keep their own pacing (median ~3.5-4s, punchier) and the hero bookend rule.
- 9:16 calibrations (from the Pierced pilot): stills + clips are PORTRAIT natives (solver aspect
  follows --page); side-by-side `two_v` columns are wrong at 9:16 — pair with `stack_h` rows;
  caption Tier-3 flags are ADVISORY on shorts — the fallback lower-third box IS the locked
  short look; full-bleed-beat share may run ~60-70% (the 50% cap is a long-form rule).

## 8. MODEL-INDEPENDENCE — how the standard survives a weaker builder

The user asked: "how can I be sure, when I am not able to use Fable, we still get this richness?"
Three layers, strongest first:
1. **Machine gates (cannot be sweet-talked):** still_validate, the build lint (reuse gap+crop,
   max-2-uses, never-2x-full-bleed, ≥80% motion floor, caption slop scan, frame-exact cuts,
   DoD numbers). A weaker model literally cannot ship the slideshow or slop text — the gates
   print the violation list until the plan is fixed.
2. **The calibration reference + this protocol:** the next builder IMITATES a concrete approved
   film and follows C1-C7 step-by-step instead of inventing. Imitation + checklists degrade
   far more gracefully than open-ended judgment.
3. **Independent review of JUDGMENT calls:** the paper beat-plan ($0) and the caption layer go
   to the 5-CLI panel BEFORE/AFTER spend; the panel catches concept-pairing and doctrine slips
   a weaker builder makes (it caught a real citation error even on Fable's work).
What genuinely degrades without a top model: the poetic pairings (lion-shadow beside the ink,
the king's resting hands under "he hath done this"). Mitigation: per-beat concepts must cite
their narration line (C1), and the paper plan panel-reviews BEFORE render — weak pairings get
caught at $0, not after the spend.

## 5. Queued next moves (approved direction, build when an episode calls for them)

Match-cut graphic rhymes across beats · panel-border BREAK on resurrection beats (the risen
panel bleeds past its ink frame) · light/blood spilling across gutters · camera whip-pans
THROUGH the gutter instead of hard cuts · heartbeat SFX that stops at "It is finished" ·
kinetic type as performance ("forsaken" cracks; "finished" settles like stone) · the mosaic
ending (the page fills with nation-panels that form a cross, then pulls back).
