# POC30 Seed — spread plan (process-validation test, ~33s, 5 spreads)

**STATUS: internal process test, not a real episode.** Validates the Day of
Atonement retrospective's fixes (memory `day-of-atonement-retro-learnings`)
before committing to a full new living-sketchbook LONG episode. Content:
Genesis 3:8-10, reusing `longform/05_The_Seed_Of_The_Woman/v1/narration.mp3`
turns 0-3 verbatim (already-locked text, already-voiced audio, real
forced-aligned timing in `_alignment.json`). See `_PREFLIGHT.md` for the
census, camera-angle plan, and device/bbox assignments filled in at plan
time (fix #7/#8), before any render.

## The spread table (real alignment timing, not estimated)

| # | Start–End (s) | Dur | Beat | Type | Shows | Assets | Device |
|---|---|---|---|---|---|---|---|
| 1 | 0.0–5.8 | 5.8 | 1 | NS | Wide, high angle: Adam and Eve small in the garden, something visibly wrong — "Something has just gone terribly wrong in the garden... have believed a lie," | Adam, Eve, eden (bg) | dramatic_spotlight (still, bbox on the two figures) |
| 2 | 5.8–11.9 | 6.1 | 1 | NS | Medium, eye-level, among the trees: the two of them hiding — "eaten what He forbade... they are hiding from Him." | Adam, Eve, eden (bg) | real clip — Kling (multi-figure) |
| 3 | 11.9–24.0 | 12.1 | 1 | VC | Verse card, Scribed Ink: Gen 3:8 KJV verbatim, over the eden background | eden (bg) | Grand-Text combo, lettering built with this spread |
| 4 | 24.0–30.7 | 6.7 | 1 | NS | Wide, low angle through the canopy: light/presence moving, no figure — "And God comes looking... with a question." | eden (bg), LORD-presence (light only) | real clip — Seedance (calm, single light-presence) |
| 5 | 30.7–33.0 | 2.3 | 1 | NS | Held close on the light between the trees — "Where art thou?" (the landing) | eden (bg), LORD-presence (light only) | device-only, Fable-designed bespoke hold, no camera move |

## Why this excerpt (not a random 30s)

Chosen specifically because it contains a real scripture turn (spread 3,
Gen 3:8) inside the first 33 seconds — without a verse-card spread, the
lettering-built-with-the-spread fix (retrospective fix #4) couldn't be
tested at all. It's also the true opening of one of the two real candidate
next episodes (Seed of the Woman), so the Adam/Eve cast anchors and the
Eden world anchor built here carry forward into the real build rather than
being thrown away.

## Reuse posture

Narration text and audio: reused verbatim, $0, already locked+voiced+
5-CLI-panel-reviewed as part of `longform/05_The_Seed_Of_The_Woman/v1/`.
Visuals: entirely new (living-sketchbook has never rendered this passage) —
this is what the stills-discipline fix (#7) is actually testing.
