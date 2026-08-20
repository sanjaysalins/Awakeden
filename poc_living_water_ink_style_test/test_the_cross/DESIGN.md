# Design-machine test — "The Cross" (single still, 2026-08-20)

Smoke test of `SKILL.md` Step 0 (the Fable design pass) + both north-star
templates, on ONE new shot outside the John 4 sequence — user's own scoping:
"Jesus on the cross, panels: (1) his mother, (2) the Roman soldiers, (3) the
location." Grounded in John 19:17,23-27 and Matthew 27:33,45-46 (Golgotha,
the soldiers casting lots, Mary at the foot of the cross, the midday
darkness). Stills only today — no animation spend.

## Lane decision (Step 0's other output, for the record)

**Corrected 2026-08-20** (see `NORTH_STAR_ANIMATION_PROMPT.md`'s "THE
DEFAULT" — this shot's original call, "FREEZE lane," was written before that
correction and was wrong): on a short, this still gets REAL motion by
default, same as every other shot — a steady, unwavering gaze and a single
slow blink (NO_MOUTH, per the locked vocabulary), Kling or veo3_1_lite per
the tiering rule. Focal Tour (Jesus's face -> the crown of thorns -> the
darkened sky, `dramatic_spotlight`) is only the GAP-FILL for whatever time
is left after that real clip's natural length, not a substitute for
animating the shot. Not run today — still-only test.

## Still prompt (filled from NORTH_STAR_PROMPT.md's template)

Sequence: `THE CROSS`, frame `F01`. Refs chained: `jesus_ref.png` only (Mary
and the soldiers are panel-only supporting sketches, not recurring subjects
needing a locked ref for a one-shot test).

```
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE CROSS". Top-right frame number, handwrite: "F01". Across the top, a row of exactly three small labeled storyboard panels numbered 1, 2, 3: panel 1 a small sketch of his mother Mary standing at the foot of the cross, one hand pressed to her mouth, grief held with quiet dignity, panel 2 a small sketch of Roman soldiers below the cross, one crouched casting lots on the ground for his garment, spear and helmet loosely inked, panel 3 a small establishing sketch of Golgotha, the bare skull-shaped hill outside the city wall, three crosses in silhouette against a darkening sky. Below them, ONE large full-scene illustration filling the lower half of the page — a HELD SINGLE, close on Jesus alone: Jesus alone on the cross at Golgotha, his upper body filling the frame, arms outstretched along the crossbeam, head bowed slightly; the sky behind him gone dark though it is midday, the bare hill falling away soft and unfinished at the page edges beneath him; stillness and complete surrender. Jesus (match the attached reference for his face, hair, and build): a first-century Jewish man in his early thirties, weathered calm face, dark textured shoulder-length hair, short natural beard, drawn in broad confident economical ink strokes; here on the cross, stripped for the crucifixion but modestly wrapped in a plain loincloth, a crown of twisted thorns pressed into his brow, faint ink marks of the nails at his hands, a faint incomplete calligraphic halo of muted gold-and-blue curls, never a solid disc. Stage 3 dosage: the blue-and-gold ink motif is fully diffused but subdued — quiet threads of blue with the barest trace of gold woven faintly through the darkened sky and along the base of the cross, not tied to any single figure, behaving like wet ink bled deep into the paper, grave and quiet, never bright, never celebratory. Small handwritten production notes integrated naturally on the page: a caption beneath the main scene, handwrite: "Father, forgive them", and a corner note, handwrite: "NOTE: darkness at noon". Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash on aged cream paper with visible grain. Not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX — every blue or gold element behaves like literal wet ink bleeding into paper, never a magic-particle glow.
```

## Known risk

Higgsfield content moderation has previously refused bare-torso-cross images
(the project's own documented NSFW-cross issue, elsewhere handled by a
direct-Kling animation fallback — not applicable here, this is a stills-only
test). If `nano_banana_pro` refuses this prompt, that is new information for
this style specifically, worth reporting back rather than quietly rewording.

## Result — rendered clean, 2026-08-20 (2 credits x2 = ~$0.60)

Both `the_cross_9x16.png` and `the_cross_16x9.png` rendered on the first
attempt, no NSFW refusal (the bare-torso-cross moderation risk noted above
did NOT trigger on this ink/watercolor style, unlike the Baroque-oil pipeline
elsewhere in the project). Eyeball-QC:

- Layout held in both ratios: title / F01 / 3 panels / one big scene / notes.
- Jesus face/hair/build consistent with the chained `jesus_ref.png`.
- Swirl dose read correctly restrained — Stage 3 "subdued, grave, never
  celebratory" landed as intended: two faint blue-gold curls flanking the
  halo, nothing showy. The still-rendering half of this style was never the
  broken part (only the AI *motion* on it was) — this test reconfirms that.
- Crucifixion handled with real restraint: a plain loincloth, faint ink
  marks at the wrists and a few small red marks from the thorns, no gore.
  Golgotha rendered as the traditional "skull-shaped hill" visual (a known
  artistic convention tied to the name's meaning, Matthew 27:33 / John
  19:17 — not an invented doctrinal claim).
- Both captions baked correctly: "Father, forgive them" (verbatim KJV
  fragment, Luke 23:34) and "NOTE: darkness at noon".

**One real finding:** the 16:9 render baked an extra label under each of the
3 panels ("Mary's Grief" / "Soldiers Cast Lots" / "Golgotha - Darkening Sky")
that was NEVER requested in the prompt — the identical prompt text produced
this in 16:9 but not in 9:16. Not a legibility or spelling failure (the
labels are correct and match their panels), but it's invented content the
template didn't ask for, and it means the two ratios are not byte-identical
in what they bake — worth watching for on future multi-ratio renders, not
yet worth a template change off a single occurrence.

## v1 -> Fable design-critique -> v2 (2026-08-20)

An independent Fable-model design review (unbiased, fresh eyes, full
transcript in the session) found real defects in v1 beyond the label bug:
the halo and the Stage 3 swirl dose had merged into one object (the prompt
itself was self-contradictory — a figure-anchored halo vs. a dose explicitly
"not tied to any single figure"); the 9:16 crop dropped the requested nail
marks out of frame entirely; Golgotha rendered as a literal giant skull
("fantasy album art" next to a devotional image); and the panel labels were
an unauthored model improvisation, not a deliberate choice. All four fixes
went into `NORTH_STAR_PROMPT.md` (dated 2026-08-20 edits) and into
`render_test_v2.py`'s prompt: halo explicitly separated from the dose,
both hands + nail marks stated as MUST-SHOW, Golgotha hedged to "suggests a
skull," panel labels authored + a global "no other text" lock added.

**v2 result:** `the_cross_v2_9x16.png` / `the_cross_v2_16x9.png`.
- **Fixed, both ratios:** panel labels now identical and consistent
  ("Mary's Grief" / "Soldiers Cast Lots" / "Golgotha"), no stray unrequested
  text anywhere; cross now reads as a real Latin cross, not scaffolding;
  halo and swirl dose read as visually separate elements, not merged.
- **Fixed, 9:16 only:** both nail marks now visible in frame; Golgotha
  hedged successfully — a rocky hill, not a literal skull.
- **Still open, 16:9 only:** Golgotha panel is STILL a literal giant skull —
  the same hedge language that worked on 9:16 did not take on 16:9 (the
  aspect-ratio-dependent-interpretation pattern from the label bug, now seen
  on a second, unrelated prompt clause). And the wrists in the 16:9 main
  illustration read as bound with **rope**, not nailed — the requested "ink
  marks of the nails" did not clearly render; what's visible looks like
  coiled cord with a frayed hanging end. Both are 16:9-specific misses on an
  otherwise-fixed prompt — worth one more targeted 16:9-only regen before
  calling this template locked, rather than a further template rewrite (the
  fixes that DID work, worked on both ratios where applied; these two look
  like generation variance on this specific pass, not a template gap).

