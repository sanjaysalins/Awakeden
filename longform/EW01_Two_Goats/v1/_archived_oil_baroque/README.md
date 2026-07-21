# Archived — EW01 Two Goats, Baroque oil-painting production (2026-07-20)

This folder holds the COMPLETE original visual production of EW01 Two Goats,
built in the legacy Baroque oil-painting style, before the project's move to
the inked graphic-novel style (already done for Isaiah 53, Psalm 22, and
Bronze Serpent — memory `graphic-novel-style-migration`). EW01 was the last
finished long-form piece still on the old style. User call (2026-07-20):
archive it all, keep only the narration, and re-animate everything in the new
comic style.

## What's here (all superseded — reference only, do not reuse the imagery)
- `visual_16x9/` — the long-form film: every still (.png), every animated clip
  (.mp4), clip-QC sidecars (.clipqc.json), Bible-fact audits (.bib_audit.json),
  signature-crop markers (.sigcrop), and `scene_plan.json` (+ two backup
  variants + `scene_plan.md`) — the shot list/story structure for the film.
- `visual_16x9_test/` — throwaway camera-move POC renders, never part of the
  shipped film.
- `publish_thumbs/` — thumbnails cut from the oil-style stills (moved from
  `v1/publish/thumbs/`).
- `short_gallery_clips/` + `short_visual_9x16_test/` — the SEPARATE 9:16
  short's oil-style visual production (moved from `v1/short/gallery_clips/`
  and `v1/short/visual_9x16_test/`).

## What's REUSABLE from this archive
- **`visual_16x9/scene_plan.json`** — the scene-by-scene shot list (subjects,
  camera, timing, captions) is real authored work, independent of art style.
  Follow the Bronze Serpent precedent: `longform/04_The_Bronze_Serpent/
  _build_inked_scene_plan.py` restyled that episode's legacy oil scene_plan
  into an inked one by swapping ONLY the `subject_block` style-prefix text
  (Baroque-oil phrasing -> inked-graphic-novel phrasing) while keeping every
  scene's content/camera/timing/captions untouched. Write an equivalent
  `_build_inked_scene_plan.py` for EW01 pointed at this archived scene_plan.json.
- The clip-QC fix-batch lessons from the 2026-07-19/20 repair session (see
  `_qcfix_state/` at the repo root) still apply to the NEW ink stills/clips:
  frozen-tableau prompt phrasing, Kling-for-action-panels vs Seedance-for-calm
  split, drip-removal-at-the-still technique for blood-invention issues.

## What was NOT touched (still live at their normal paths, reuse as-is)
- `v1/narration.md`, `narration-tagged.md`, `narration.mp3`, `narration.meta.json`,
  `narration.spoken.txt`, `narration.panel_clean.md`, `voices.json`,
  `passage.txt`, `_turns/`, `_independent_review/`, `_bible_check/`,
  `_panel_clean.md`, `_panel_run.log`, `_synth.log`, `.locked`.
- `v1/short/` — its own narration set (`narration.md`, `narration.calm.md`,
  `narration.mp3`, `voices.json`, `passage.txt`, etc.), `_visual_strategy/`
  (planning doc, not rendered assets), `_punchy/` (an alternate narration cut
  with its own `narration_punchy.mp3`), `_turns/`, `_independent_review/`,
  `.locked` — all untouched.

Nothing here was deleted. If any of it is needed for comparison or recovery,
it's all still playable/viewable from this folder.
