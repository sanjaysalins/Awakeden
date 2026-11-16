# Swirls uplift rollout - executor brief (one film per executor)

OWNER APPROVAL: the owner said "go ahead and spend the money for swirls fix". Total cap for all Swirls uplift is $35; the ep08 pilot used $3.90. YOUR film has its OWN hard cap (in your prompt). Do not exceed it.

## Follow
- Design: `_quality_uplift_20261116\design_swirls\SWIRLS_UPLIFT_SPEC.md` - your film's section 4.x (shot table, doodles, costs) plus the kit (section 2-3) and gates.
- Proven recipe = the finished pilot. COPY and adapt its scripts (do not edit them in place): `poc_living_water_ink_style_test\swirls_episode_08_can_any_good_thing\uplift\` -> `cut_uplift.py`, `marks_overlay.py`, `check_uplift.py`, `make_review.py`, `uplift_pages.py`, `prompts.json` (prompt style that worked). Read its `_PILOT_REVIEW.html` and `gate_report.json`.
- House rules: `CLAUDE.md` + memory index `C:\Users\sanjay\.claude\projects\F--slk-PycharmProjects-JesusInTheBible\memory\MEMORY.md`.

## Lessons from the pilot (apply them)
- Do NOT put "no bubble / no box / no speech bubble" style negative clauses in clip prompts - they CAUSED speech bubbles. Plain positive motion wording only.
- Do not leave palette/ink instructions in a way that can be drawn as text on the still; scan every prompt for instruction words that could be rendered.
- About 1 clip in 3 needed a redo. Budget for it; keep a still that fails a check from ever being animated.
- Real price: Kling 3 Omni pro, sound off = 35 credits/second; Nano Banana Pro still = 40 credits. $0.002/credit.
- OpenArt tool results echo the whole prompt (~4k tokens): batch where possible, poll each job ONCE when likely done, keep prompts short. If you run low on context, stop cleanly and report exactly what is done and spent.

## Spend control (mandatory)
- OpenArt MCP only (load via ToolSearch). Stills `nano-banana-pro`; clips `kling-3-omni` pro, sound off. Never PixVerse, Higgsfield, ElevenLabs.
- Before EVERY job: openart_model_cost quote; check (your spend so far + job) <= your cap; else STOP. Keep a running total from the quotes (the account balance is shared with other executors - do not use balance deltas).
- Log every job to `data\spend_ledger.jsonl` per `.claude\skills\cost\SKILL.md`.

## Build rules
- Ink motif never animated. No freeze/boomerang/zoom/reverse fill: every clip >= slot + 0.05 s, trimmed from frame 0 at 1.0x, hard cuts. No burned captions. Era-check and count people in every still; same face as references for recurring people.
- Audio bit-identical to the shipped final (stream copy). Same frame count as the shipped film.
- Write ONLY in your film's `uplift\` folder (for Jacob's Ladder: `poc_living_sketchbook\_rewrite_v4\panel_jl\uplift\`) plus ledger rows. Never touch the shipped final, FINAL_VIDEO.txt, publish\, other films, comic_kit or Root.tsx. No git commits. Never auto-open files.
- Skip any shot the spec ties to a pending new-narration line (spec section 7); list it.

## Finish
1. Run your copied gate script: all gates PASS/FAIL with evidence; look at frames yourself (Read tool) at every changed beat and first/last frame of every new clip.
2. `uplift\_REVIEW.html`: old vs new side-by-side players, before/after stills, new stills, gate table, $ spent. Short plain words, click-to-zoom.
3. Reply: $ spent (from your quotes), jobs incl. rejected redos, gates, skipped items, file:/// links to new mp4 + review page, deviations.
