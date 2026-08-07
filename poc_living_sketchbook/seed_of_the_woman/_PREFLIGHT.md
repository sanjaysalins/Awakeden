# POC30 Seed — pre-flight (process-validation test, not a real episode)

**Purpose:** validate the Day of Atonement retrospective's fixes (memory
`day-of-atonement-retro-learnings`) on a throwaway ~33s excerpt BEFORE
committing to the real next episode (Passover Lamb or Seed of the Woman in
full). Content: Genesis 3:8-10, the opening of the already-locked
`longform/05_The_Seed_Of_The_Woman/v1/` narration, turns 0-3 (narrator ->
scripture quote -> narrator -> the LORD). Real audio, real forced-aligned
timing (`_alignment.json`, 92 words, ffprobe-confirmed against the real
narration.mp3 -- not estimated).

Per fix #7 (stills discipline from prompt 1, not learned mid-build via
re-rolls): every item below is filled in BEFORE the first render, not
discovered after.

## Repeated-element census (incl. SETTINGS, per feedback-repeated-element-census)
| Element | Appears in | Anchor needed? |
|---|---|---|
| Adam | s01, s02 | YES -- new cast anchor (no cross-style reuse; the existing Seed of the Woman oil-painting refs are a different visual style per the locked provider-split rule) |
| Eve | s01, s02 | YES -- new cast anchor |
| Eden garden (SETTING) | s01, s02, s03, s04, s05 (every spread) | YES -- world anchor (trees, dappled light, unspoiled-but-shadowed mood) |
| the LORD (presence) | s04, s05 | NO image anchor -- per this project's own locked convention (Day of Atonement's own "LORD-glow, no figure" device), rendered as light/cloud-presence via prompt language only, never a figure. Consistent across s04/s05 by re-using the same prompt block, not a reference image. |

## KJV-number check (fix #7's discipline)
No load-bearing counts/ages/measurements in this excerpt (Gen 3:8-10 names
no numbers) -- explicitly checked, nothing to verify. Recorded per the
standing rule even when the answer is "none."

## Camera-angle / shot-type plan (per SKILL.md sec.3, filled at plan time)
| # | Name | Shot | Angle | Notes |
|---|---|---|---|---|
| 1 | s01_something_wrong | wide, high angle | looking down into the garden | isolation -- the two figures small against a garden that now feels wrong (color draining at the edges, long shadow) |
| 2 | s02_the_hiding | medium, eye-level, from among the trees | -- | multi-figure (2), genuinely different composition from s01 (close/hidden vs. wide/isolated) so the two don't repeat |
| 3 | s03_verse_card | -- (device-only card) | -- | Scribed Ink over the same garden background, KJV Gen 3:8 verbatim |
| 4 | s04_god_walking | wide, low angle looking up through the trees | -- | light/presence moving through the canopy, no figure |
| 5 | s05_where_art_thou | held close on the light between the trees | -- | the landing -- Fable-designed bespoke composition, no camera move, the question hangs |

## Anchors (built + full-res eye-checked BEFORE any spread render, fix #7)
- `cast/ADAM.md` + `adam_ref.png`
- `cast/EVE.md` + `eve_ref.png`
- `world/eden_ref.png` (+ a short text-canon paragraph, matching the
  "object/world anchors need inline text canon too" lesson from Day of
  Atonement's veil defect)

## Device/bbox plan (filled at plan time, per fix #8 -- Fable pre-designs
the hard beats; bboxes picked via `panel_animator/bbox_sheet.py` once
stills exist, not guessed)
| # | Type | Device | Deliverable |
|---|---|---|---|
| 1 | NS | dramatic_spotlight (still) | full-scope hold, bbox on the two hiding figures |
| 2 | NS | real clip -- Kling (multi-figure) | the hiding, animated |
| 3 | VC | Grand-Text combo (Scribed Ink), lettering built WITH this spread | Gen 3:8 KJV verbatim |
| 4 | NS | real clip -- Seedance (calm, single light-presence) | God walking, no figure |
| 5 | NS | device-only, Fable-designed bespoke hold | "Where art thou?" landing, no camera move |

No mid-build design-rescue calls permitted (fix #8) -- s03 and s05's
compositions are decided here, not during rendering.
