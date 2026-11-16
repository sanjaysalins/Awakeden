# Independent review — claude (OK, 148s)

I checked the main code claims. Most are right: `-shortest` is at `swirls_assemble.py:339`, `tpad` clone is in `score_mix.mix_tail`, `output_args(total=)` cuts at `-t total`, `--natural` exists, `align()` exists, `fence_kind="none"` exists, and `sw_f1` skips modes other than freeze. The hold-fix logic works on paper. My findings are below.

**1. SWS-G15's freeze check will reject good calm clips (high risk).** Step 7 makes it a FAIL when "`freezedetect` finds no freeze of 0.5 s or more in the last 3.5 s". This series asks for "light only" motion and a hero action "done in the first half". Kling clips settle into near-still endings. Your own memory note (`feedback_animation_motion_check_by_pixel_diff`) says that kind of subtle motion gives very small pixel diffs. `freezedetect` uses a default noise level of -60 dB, so a calm, living back cover can read as frozen. Section 4.7 says there are "no thresholds to tune", but this is one: the noise setting and the 0.5 s length. Fix: before making it a FAIL, tune both on the real ep10 and ep13 back-cover clips and on a clone-padded build. Until then, make it a WARN. Same goes for SWS-G12-lite at 1.0 s.

**2. The pace test can't answer its own question.** The question is "can a viewer read a page in about 6 s?". But the blind seats get still 390 px JPGs with no time limit. A vision model reading a downscaled JPG is not a person glancing at a phone. So the "2 of 3 seats read all three labels" rule is really a resolution test, not a speed test. The owner's view is the only speed test, and the owner page shows the film "390 px wide" on a desktop. Fix: the owner watches the mp4 on a real phone. Treat seat scores as a legibility floor only. Also, the audio cuts ep13/ep10 lines that were written for longer slots, so the owner hears broken sentences. Say so on the page, or the "too fast" answer gets muddied.

**3. The cost numbers aren't verified, and the clip total looks low.**
- "35 cr per second" and "40 cr" stills aren't backed by any invoice or `openart_model_cost` call in the plan. CLAUDE.md says: always re-derive from real billing. Run the cost check ($0) before quoting any price.
- Using its own formula `max(3, ceil(slot+0.5))`: front about 3-4 s, six pages about 7 s each, back about 10 s. That's about 55-56 clip-seconds. Minus the 7 s test clip, about 48-49 s are left (about 1,690-1,715 cr), not "46 s / 1,610 cr". Small, but the quote and the cap should come from the real `unit_timing.json`, never from a table.
- Kling 3 Omni at 3 s (the front cover) is assumed to be a legal length. Check it.

**4. Leftover veo duration rules may hit the cover path.** The comment at `swirls_cover.py:123` says "legal values 4, 6, 8 only", and `swirls_verify.py:162` keeps `_VEO_DURATIONS`. The plan calls this "stale but harmless". It is only harmless if no gate path for covers goes through the veo tier. SWS-G3 should state the legal Kling lengths and FAIL on anything else. Otherwise a 3 s or 10 s cover could be rejected, or silently rounded.

**5. The plan depends on a panel that keeps timing out.** codex and grok timed out twice, and the plan still needs a "full quorum" at build-order step 2, step 1, step 3 and step 10. It doesn't say what counts as a quorum, or what happens on a third timeout. Fix: define it (for example, Fable plus 3 of 5 CLIs, with a longer timeout), or the build stalls at step 2.

**6. Frame drift at unit cuts.** `make_trim` uses `-t slot` at 30 fps. Each unit can round by up to about 33 ms. Over 7 units, cuts can drift about 0.1-0.2 s from the words. Only the back unit absorbs the total. Fix: round each cut to a frame from the start of the film, not one unit at a time.

**7. A typed number protects the spend guard.** `--balance` is a number the session types in, so it is only as good as that one typing step. It's acceptable, but add a check: refuse if the balance date is older than about 15 minutes. A stale balance could approve a cap that other sessions have already spent from.

**8. Smaller points:**
- SWS-G13 checks head count across 5 frames from the used part of the clip only. A figure that appears in the cut-off tail does no harm, and that's fine. But a figure that comes in early, while the hold is still on screen, needs a check on the true last used frame. G12-lite covers that, but only as a WARN.
- The plan says there are 5 old validators and the build adds one. All 5 exist on disk, so the "six validators" claim checks out.

**Overall:** the scope is now right-sized and it reuses existing tools well. But the one new FAIL gate that guards the main fix (the freeze check) is untested against real calm clips, and the cost table isn't sourced. Both need fixing before the build.

VERDICT: REVISE
TOP FIXES:
1. Tune `freezedetect` (noise level and length) on the real ep10/ep13 back-cover clips and a clone-padded build. Until then, make SWS-G15's freeze rule a WARN, and stop saying there are "no thresholds to tune".
2. Get real per-second and per-still prices from the OpenArt cost check before any quote. Work out clip seconds from `unit_timing.json` (about 48 s left after the test clip, not 46). Make SWS-G3 check the legal Kling lengths so the leftover veo 4/6/8 rule can't reach covers.
3. Fix the pace test: the owner watches the films on a real phone, and seat scores count as a legibility floor only. Also define the panel quorum and what to do on a timeout, since codex and grok failed twice.
