# AI pre-check — Bronze Serpent LONG, 65 clips (2026-08-03)

**This is a pre-check only, not a substitute for the user's own eye-check gate.**
Nothing here is a LOCK/approve decision. Purpose: speed up the real eye-check
by pointing at the handful of clips worth a closer look, out of 65.

## Method

- Extracted 3 frames per clip (first `_a`, middle `_b`, last `_c`) via ffmpeg,
  sequential/single-process (CPU-polite), saved to a scratch folder.
- Verified the extraction itself was sound (one reviewer worried frames looked
  "too identical" on a batch of very-static clips — checked by MD5 hash, all
  three frames per clip are genuinely distinct captures, not a duplicate-frame
  bug; those clips are just genuinely held-camera shots).
- 8 read-only review agents (~8 clips each) compared frame `_a` vs `_c` against
  this project's own "frozen tableau" rule (only the CAMERA may move between
  frames — crop/pan/zoom; the drawn subject itself should not move/morph) and
  its documented past failure modes (anatomy errors, uncoiling serpents,
  continued hammer-swings, robe-sway, identity drift, blood growth, crowd faces
  over-detailed, anachronism, garbled text, margin bleed).
- I then personally opened the actual frames (not just the agents' text
  verdicts) for every clip flagged SUSPECT, per this project's own
  "verify by looking, not running" rule.

## Result: 59 of 65 clean, 6 flagged

**59 clips: no reviewer found anything worth a second look.** Full per-batch
detail is in the 8 result files this session wrote to scratch (not copied
into the repo — see the session transcript if the raw per-clip notes are
ever needed).

### Flagged — I looked myself and agree something real is there (5)

1. **s19_people_kneel** — the two kneeling groups have ~8-9 individually
   rendered, sharp faces, not the ~2-3-sharp/rest-shadow mix this project's
   own crowd rule calls for. Confirmed by eye: this really does read as
   "everyone in the crowd is a portrait," not shadow figures around 2-3 named
   people.
2. **s39_moses_sleepless_candle** — Moses's near hand is genuinely posed
   differently between frame `_a` (flatter, fingers apart, resting near the
   ledge) and frame `_c` (drawn in, fingers curled/clasped near his lap).
   Background (lamp, smoke, wall shadow) is identical in both — so this reads
   as the hand itself moving, not a camera change.
3. **s47_golgotha_midshot** — confirmed and the clearest one: a pale/white
   vertical drip appears below Christ's fisted hand in the MIDDLE frame only
   (`_b`) and is absent in both the first and last frames. Not blood-colored,
   but a real appear-then-vanish element within a single locked-camera shot —
   this is the kind of thing that should not happen in a frozen tableau.
4. **s62_moses_neverasked** — a dark shadow shape appears behind Moses's
   head/shoulder in frames `_b`/`_c` that is not present in `_a`, and the crop
   between `_a` and `_c` looks similar enough that this isn't just zoom
   revealing pre-existing shading — reads as invented background content.
5. **s64_moses_sit_with_that** — a large orange-brown storm/dust cloud fills
   the sky in frames `_b`/`_c` that is completely absent (plain clear sky) in
   frame `_a`. Moses's own pose/hands/staff is identical throughout — only
   the background sky content grows in.

### Flagged — lower confidence, could be a camera-crop artifact (1)

6. **s42_hands_finish_forge** — the reviewer flagged the hammer head looking
   closer to (possibly touching) the serpent coil in the middle frame than in
   the first/last frames. I looked myself: the apparent gap does shrink
   somewhat in the middle frame, but the crop also changes across the three
   frames, and a changing crop can make a static gap look tighter without any
   real motion. I couldn't rule it in or out from 3 still frames — this one
   genuinely needs the real clip played back, not just frame comparison.

## Not flagged but worth knowing

- s28_forge_acting (the scene with history of a hammer completing its swing
  on 3 different providers before) checked CLEAN this time — hammer stays
  raised in the same position across all 3 frames.
- s51, s54, s55, s65 — all scenes with a specific documented past reject
  (robe-sway, uncoiling serpent, completed hammer-strike) were checked with
  extra scrutiny and came back clean.

## Caveat

Only 3 static frames per clip were sampled — a real defect that appears only
between sample points (e.g. a mid-clip flicker) would not be caught by this
method. This narrows the human eye-check, it doesn't replace playing the
clips.

## Where the raw frames are, if useful

`C:\Users\sanjay\AppData\Local\Temp\claude\C--Users-sanjay-PycharmProjects-JesusInTheBible\b6179872-b52b-47f8-a727-3d2790e6a05c\scratchpad\bsl_frames\`
(session-scoped scratch space — may not persist long-term; re-extractable any
time from `clips/*.mp4` if needed later).
