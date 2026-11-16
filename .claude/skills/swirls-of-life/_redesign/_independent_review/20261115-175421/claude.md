# Independent review — claude (OK, 204s)

I've finished checking the plan against the code. Here is the review.

## Checked against the code

**1. The voice step uses tools that don't exist (Step 2). Most serious.**
- `per_turn_synth.py` is at `F:\slk\PycharmProjects\PythonProject1\jesus\narration\per_turn_synth.py`. The plan's path is wrong.
- `--target` is a required flag there. The plan's command leaves it out, so the command as written fails.
- There is one global `--stability` flag. It sends every line to `eleven_v3`. There is no per-line stability (0.65 narrator, 0.3 characters) and no "2 takes each".
- It writes no `narration.alignment.json`. Step 3 timing, the score, the SFX and the SRT all need that file. So the plan needs a real step that makes it (ElevenLabs timestamps, as `build_srt.py` does). Name the tool.

**2. "The three existing `_validate_swirls_*.py` scripts" (4.1, 4.4) is wrong.** There are five:
- `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\_validate_swirls_assemble.py`
- `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\_validate_swirls_cover.py`
- `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\test_the_cross\_validate_swirls_page.py`
- `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\test_the_cross\_validate_swirls_page_hem.py`
- `F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\test_the_cross\_validate_swirls_page_hybrid.py`

The plan changes `swirls_page.py`, and the three `_validate_swirls_page*.py` files test it. They are left out of the "must still pass" list.

**3. The clip-QC calibration set is partly made up (Step 6).**
- Real: `back_cover.mp4.SUPERSEDED_title_lettering_vanished` and `front_cover.mp4.SUPERSEDED_simon_walked_off_right_edge` (ep13).
- Not found anywhere: `*.mp4.SUPERSEDED_cast_vanished`.
- Most other SUPERSEDED clips (ep7, ep10, ep11) are bad for other reasons: NSFW reading, cloth glitch, "rising defect".
- That leaves about 3 bad clips on text and figures, and none on motif growth or speech bubbles. That is too few to set SWS-G12 thresholds. The plan should admit this, or treat G12 as warn-only until the pilot.

**4. `swirls_episode.py` is a small runner.** Today it has 5 commands: plan, still, animate, verify, assemble. The plan adds about 11 commands and about 8 new modules (state, clipqc, score, sfx, pages, timing, scaffold, validator) before one pilot proves the format. Build order step 5 (state, pages, scaffold) and step 6 (shared score and SFX) can wait until after the pilot. For one episode, copying ep13's `generate_score_piano.py` and `build_sfx.py` works today.

## Design risks

**5. Two rules fight each other (1.4 rule 5 vs 1.2).**
- The voice starts at 0.0 s, so almost every page has someone speaking.
- "A figure whose line is being spoken does not move" plus "hero always has real motion" plus "at most one panel moves" leaves many single-figure pages with only air and light moving. That is the Ken Burns look the owner hates.
- The plan flags this only as a bend. It needs a planning-time count: how many pages end up "speaker holds, nothing else to move".

**6. 5-6 s per page is a big untested change.** Old pages ran 10-13 s, and each page has 3 labels, a caption and a title to read. Section 7 says so, but no step tests it for $0 before spending. A draft from existing stills (say ep10's, timed at about 6 s per page) would show whether it can be read.

**7. Cover border auto-crop (SWS-G10).** Cropping the outer 6% of a 2K 9:16 still leaves less than 1920 px of height. That conflicts with SWS-G11's "height >= 1,900 px", and the clip is made from the cropped still. Do the size maths, or crop after animation.

**8. Spend guard.** "The runner adds up credits from bridge responses." `swirls_page.py` prints `resp.get('credits_spent', '?')`, so credits can be missing. The guard must fail closed when they are missing, not count them as 0. The account is also shared with other sessions, so the cap must use credits per job, never the balance going down.

**9. Cost check.** 35 cr/s × 53 s gives the stated 1,855 cr. But the buffer assumes 25% clip redos, while old episodes took 3-6 fix rounds. With a "~$9 cap", one bad reroll cycle on a 60 s film goes over. Quote the cap from the worst case (2 rerolls on 30% of clips), not the clean run.

## Fine as is

Reusing `swirls_assemble.py` with a new `trim` mode is right: today it has only `Literal["freeze","boomerang"]`. Keeping `fill_policy` opt-in (`legacy` default) is right. Kling 3 Omni through the OpenArt bridge already exists in `swirls_page.py`. The pilot-before-lock idea is good.

VERDICT: REVISE
TOP FIXES:
1. Fix Step 2 to match the real `per_turn_synth.py`: correct path, the required `--target`, no per-line stability or takes, and no alignment output. Name the tool that makes `narration.alignment.json`, since timing, score, SFX and SRT all depend on it.
2. Cut the build before the pilot to trim mode, timing, lints and a warn-only clip QC. Put the regression list at all 5 validators. Replace the made-up calibration file with the real labelled clips, and admit the set is too small to calibrate on.
3. Before any spend, add a $0 check of the 5-6 s page pace (re-time old stills) and of how many pages end up "speaker holds". Settle the 6% cover crop against the 1,900 px rule. Make the spend guard fail closed when credits are missing, and set the cap from the worst case.
