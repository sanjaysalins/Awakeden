# The Serpent-Crusher Promised — Seed of the Woman short #4 (Romans 16:20)

Manifest slug: `seed-of-woman-04-serpent-crusher-promised`. Source narration
(LOCKED): `PythonProject1/jesus/narration/46_Old_Story._Unfinished/v1/` —
narration.md + narration.mp3 (58.863s last word end). Real word-level
timing: `_alignment.json` (this folder), via `_s0_align.py`, 134/134 words
matched.

**2026-08-15 UPDATE — two voices, not one.** Originally single-voice
throughout (narrator only). The narration predates G9 Multi-voice (locked
2026-08-14) so it was never actually gate-checked — running G9's real logic
against this text confirms CONDITIONAL, not FAIL (the "Paul writes..."
attribution doesn't match the spoken-verb regex), meaning narrator-only was
a legitimate, gate-allowed choice, matching the documented Pauline/epistle
exemption (same precedent as Her Seed's own Galatians 4:4 quote). But per
the standing `feedback-maximize-multivoice` rule and for consistency with
Her Seed (which DID voice its own analogous Paul quote), the user asked for
a dedicated Scripture voice on the Romans 16:20 quote too. Added
`<speaker name="scripture">` (voice_id `puDRtQWF8NtQiPMJygTb`, the
project-standard Scripture voice) around the KJV quote in
`narration-tagged.md`, re-synthesized via `per_turn_synth.py` (same original
params: target=59, pre-quote-pause=0.5, stability=0.65), which shifted
`narration.mp3` from 57.153s to 58.863s last-word-end. Re-ran `_s0_align.py`
and rebuilt every downstream timing (spread windows, title/quote cards,
score/sfx cues) from the fresh alignment — see each script's own file for
the current numbers, this table below is now STALE for exact timestamps
(structure/order unchanged, only the numbers shifted).

This is the 4th and last of the 4 declared Seed of the Woman shorts. Its own
thread is distinct from its 3 siblings: short #1 (First Gospel in the Curse)
and short #3 (Heel vs Head) both stay inside Genesis 3:15 itself; **this
piece is the ONLY one that crosses into the NT fulfillment text** (Romans
16:20, Paul writing to Rome) and carries its own real doctrinal tension the
narration resolves explicitly — Christ's blow at the cross is already struck,
but Romans 16:20 still phrases it "shall bruise... shortly." The narration
(panel-LOCKED already) answers this itself: the fight isn't still in doubt,
the crushing is being applied, not still being decided.

## Cast / object census

- **The SERPENT** — no repo cast anchor exists (same as every prior piece in
  this cluster); chains as a DESIGN reference from this cluster's own prior
  approved serpent art for visual consistency: `poc_living_sketchbook/
  first_gospel_in_the_curse/stills/s03_turns_to_serpent.png` /
  `s04_serpent_in_light.png` (judged-serpent-under-unseen-light staging) and
  `poc_living_sketchbook/heel_vs_head/stills/s03_serpent_judged.png` /
  `s05_heel_and_head_insert.png` (the already-crushed head design this piece
  needs for s01/s06/s09).
- **God's presence** — never a human figure (locked convention across this
  whole cluster): unseen radiant light only.
- **CHRIST** — reuse repo cast `poc_living_sketchbook/cast/jesus_ref.png` for
  the landing (s09).
- **PAUL** (s04 only) — no repo cast anchor, not a recurring character in this
  cluster; rendered fresh as hands + quill + parchment, face obscured/turned
  away (same "unnamed figure, no identity-consistency need" convention as
  heel_vs_head's own s06 human figure) — avoids inventing a Paul likeness the
  project has no doctrinal or repo basis for.
- **An ordinary human figure, unnamed** — s07's "your willpower, your
  vigilance" / "not yours to crush" split, and s09's landing ("where His
  grace has set your feet") — the viewer's own stand-in, not a named
  character, face obscured or distant, same convention as heel_vs_head s06.

## Spread table (9 spreads, 57.153s last word + 3.847s landing hold)

Real word-timed windows, midpoint of each inter-beat silence gap in
`_alignment.json` (not eyeballed).

| # | window (s) | shot | content | words |
|---|---|---|---|---|
| s01 | 0.00–5.614 | wide, recap/aged | The familiar Genesis 3:15 scene, deliberately staged with a worn/faded, "already-told" quality (this is the story the viewer already knows) — the serpent already judged, an unseen heel-shape pressed over its head, garden setting, no Adam/Eve (design-reference from `first_gospel_in_the_curse/s03_turns_to_serpent.png` + `heel_vs_head/s03_serpent_judged.png`) | "You've heard this before - a curse in a garden, a serpent's head crushed under a heel." |
| s02 | 5.614–7.994 | device insert | An unfinished-page device — an open sketchbook spread where the crushed-serpent drawing stops mid-stroke, the rest of the page still bare paper/blank space (the book-itself conceit, per this cluster's Round 5 devices) — visually withholding completion rather than showing it | "It isn't finished yet." |
| s03 | 7.994–15.427 | point, absence-contrast | A soldier's armor and sword laid down, set aside, untouched — no warrior present — with calm unseen radiant light falling across the empty armor (God's presence convention: light only, never a figure) — the crushing was never handed to force | "That crushing was never handed to a warrior. Scripture calls Him the God of peace, not force." |
| s04 | 15.427–19.83 | wide, hands-only | Hands, quill, and parchment on a plain Roman writing surface — an unfinished letter mid-line, face turned away/obscured (no identity claim on Paul's likeness) — ordinary, unadorned setting matching "ordinary believers in Rome" | "Paul writes this to ordinary believers in Rome, echoing Eden's promise:" |
| s05 | 19.83–29.008 | HERO, KJV quote | The verse's own imagery: unseen radiant presence (God of peace) resting over ordinary bare feet already standing on a crushed, unmoving serpent head — grace-light, not conquest-light; no visible human upper body, no triumphant pose, just feet already given the standing the verse names | KJV: "And the God of peace shall bruise Satan under your feet shortly. The grace of our Lord Jesus Christ be with you. Amen." |
| s06 | 29.008–38.016 | proof resolution | An empty cross, shadow falling long across the ground where the crushed serpent already lies still — past-tense, already-fallen staging (distinct from a crucifixion moment) — the blow already struck, nothing still in motion | "If Christ won at the cross, why still future? Because the blow already fell - the fight isn't still in doubt." |
| s07 | 38.016–48.049 | conviction, split-contrast device | A single split composition: one side a human figure straining/keeping vigil alone, fists clenched, exhausted (design-reference from `heel_vs_head/s06_own_blow_straining.png` for cluster consistency) — the other side the same crushed serpent head from s01/s06, completely undisturbed, no hand near it at all | "You want to be the one who crushes what's crushing you - your willpower, your vigilance. But that head was never yours to crush." |
| s08 | 48.049–54.281 | landing bridge | The s01 garden scene revisited, but the worn/faded quality now breaking into vivid gold-threaded light reaching toward it (the "whole Bible, through Jesus" visual grammar, design-reference from `first_gospel_in_the_curse/s07_gold_thread_in_curse.png`) — old promise, present fulfillment, in one frame | "The garden's promise isn't old history - it's Christ, finishing what He won." |
| s09 | 54.281–57.153 (+3.847s hold) | LANDING, sacred stillness | Christ (repo cast `jesus_ref.png`), reverent distance, and beside Him an ordinary unnamed figure's bare feet standing firm — both sets of feet grounded together over the same crushed serpent head — this is deliberately NOT a crucifixion image (both sibling shorts already landed there) — it is a STANDING image, the verse's own "under your feet" made literal as shared ground, not watching Him die again | "Stand where His grace has set your feet." |

Shot-variety floor: wide/recap (s01) / device insert (s02) / point
absence-contrast (s03) / wide hands-only (s04) / HERO quote (s05) / proof
resolution — empty cross (s06) / conviction split-device (s07) / landing
bridge (s08) / LANDING standing (s09) — satisfied, no repeated shot type
back-to-back. s01/s06/s07/s09 all involve the crushed serpent but at four
genuinely different framings (wide recap / cross-shadow / split-device inset
/ landing feet-only) — same discipline as Heel vs Head's own s03/s04 lesson,
carried forward.

Doctrine note (already resolved by the LOCKED narration text, carried into
staging): s05's "under your feet" and s09's landing both show ORDINARY human
feet already standing on the crushed serpent — never the human figure doing
the crushing (that would contradict s07's own explicit "never yours to
crush"). The crushing is God's/Christ's finished act; the standing is what
grace gives.

TOTAL = 61.0s (LAST_WORD_END 57.153 + HOLD 3.847, comfortably above INV-26's
3.0s minimum, clean at 30fps = 1830 frames).

## Animation tiering (judged per-shot, to be finalized at animate time)

Per this cluster's own locked lessons (CLAUDE.md):
- s02 (unfinished-page device) is a strong $0-device candidate — a drawn
  reveal stopping mid-stroke is closer to a bespoke creative device than
  anything a paid animator would add value to.
- s01/s08 (garden recap / gold-thread bridge) are atmospheric light-only
  shots — veo3_1_lite tier, matching this cluster's own precedent for
  similar shots in the first two siblings.
- s03/s04/s06 (absence-contrast, hands-only, empty cross+shadow) — no cued
  body gesture needed, likely veo3_1_lite or a $0 device depending on how
  much genuine motion headroom each still has once rendered; judge before
  spending, per the standing rule.
- s05 (HERO KJV quote) — reverent hold, positive-only glow phrasing,
  veo3_1_lite tier (matches s07_landing_christ precedent from this cluster).
- s07 (conviction split-device) — likely a $0-device candidate matching
  Heel vs Head's own s02 split-contrast treatment, unless the straining-figure
  half needs a real cued gesture, in which case that half alone goes Kling
  tier.
- s09 (LANDING) — veo3_1_lite, reverent hold, matches every prior landing in
  this cluster.

## Cost estimate (real per-unit prices from this cluster's own ledger)

Stills: 6–7× kling_omni_image ($0.075) + 2–3× seedream_v4_5 ($0.15, the
hero/landing/Christ shots) ≈ **$0.75–1.05**. Animation: to be quoted once
stills are locked and the $0-vs-paid tier is finalized per shot (per the
standing ask-before-spending rule) — rough estimate **$3.00–4.50** based on
this cluster's own realized costs for similarly-sized 9-spread pieces.
