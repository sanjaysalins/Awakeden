# Independent review — claude (OK, 315s)

Every file the brief names exists. Old and new films have the same length and byte-identical audio, so the audio check in the brief will pass for all 7.

**The main problem: that md5 check proves the wrong thing.**
- The uplift copies the whole old mix (voice + score + SFX) unchanged (`COMIC_UPLIFT_SPEC.md:28`, `:56`, `:62`).
- But `SWIRLS_UPLIFT_SPEC.md:14` says ep08's pictures were about 5 s out of sync and were re-timed. Pages were also swapped and new shots were bought for every Swirls film.
- So the old SFX hits were laid against the OLD picture timing. They can now land on the wrong shot. In ep08 that could be up to about 5 s off.
- The brief only checks "narration unchanged", so it will say green and hide this. It needs a separate check: does each SFX hit still match the picture?

**Other findings**
1. **1 frame per second can't catch the main rules.** Freeze, boomerang, slow zoom and "motif never animated" are all about motion. Still frames can't show them, and the memory files say so (`feedback_animation_motion_check_by_pixel_diff`, `feedback_animation_full_clip_check_not_sample`). The brief should ask for a pixel-diff plus first-vs-last-frame check on every unit. It should also reuse the builder's own tools as a cross-check, not a source of truth:
   - `_quality_uplift_20261116\design_swirls\tools\clip_motion_audit.py`
   - `poc_living_sketchbook\_rewrite_v4\panel_jl\uplift\check_uplift.py` + `gate_report.json`
2. **Too big for one reviewer.** At 1 fps, 7 films old + new is about 1,100 frames, before the extra frames at cuts. No one can look at all of them, so the reviewer will quietly skim. The brief should name a plan: frames only at cuts, hero moments and mark times. Or one film per reviewer.
3. **ep08 and ep13 are already locked.** Their `FINAL_VIDEO.txt` already points to the uplift. The brief doesn't say what happens if this review finds a defect: unlock, or log only? Review them first, or say they are done.
4. **The Woman Behold word timings are stale.** `COMIC_UPLIFT_SPEC.md:48` says its alignment covers only 13 s. The rule "marks tied to the spoken word" can't be checked from that file. The reviewer needs real timings or must check by ear.
5. **The Jacob's Ladder words may be the wrong version.** The brief points to the pilot `narration.md`. But the film was built from `poc_living_sketchbook\_rewrite_v4\panel_jl\LOCKED_WORDS_JL_2026-11-02.md`. Name that file instead.
6. **Some owner rules are missing.** The list leaves out the ≥3.0 s landing hold, the ~2.5 s score end fade, and cloned-person counts (all locked rules). Hold and fade carry over with the copied audio, but a re-cut picture could still end early. Add a `check_landing_hold.py` run on the new files.
7. **Doesn't meet the house rule.** It is a single reviewer, not a blind Fable seat plus the AI panel. It also hands the reviewer the old film as a reference point, and "is the new one clearly better" leans toward a yes. For the "global audience" rule, a blind film-only seat is also needed.
8. **Scope doesn't match the spec.** The spec covers 8 Swirls films. The brief reviews 6 Swirls films plus the comic one and gives no reason for the gap. Say which film was left out and why.
9. **Cost:** none. It is read-only and $0, which is fine.

VERDICT: REVISE
TOP FIXES:
1. Add an SFX-to-picture sync check (especially ep08, which was re-timed by ~5 s). Byte-identical audio only proves the voice is unchanged. It does not prove the copied SFX still fit the re-cut pictures.
2. Replace the 1 fps look with a pixel-diff + first/last-frame motion check per unit for freeze, zoom, reverse and motif movement. Cross-check against the builder's `clip_motion_audit.py` / `check_uplift.py`, and cut the frame count to cuts, heroes and marks.
3. Fix the inputs and scope:
   - Jacob's Ladder → `LOCKED_WORDS_JL_2026-11-02.md`.
   - Woman Behold needs fresh word timings.
   - Add `check_landing_hold.py`.
   - Say what a defect in already-locked ep08/ep13 triggers.
   - Run it as blind seats (Fable + panel), not one anchored reviewer.
