# Independent review — codex (OK, 380s)

**Findings**

1. **The build chain is not feasible past spread 5.** The step “THEN batches of ~10 spreads, `motion_lint.py` + `_layer_check.py` run after every batch” assumes the seed episode scripts can build 71 spreads. They cannot. [\_s2_stills.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/poc_living_sketchbook/seed_of_the_woman/_s2_stills.py:136) only defines stills for s01/s02/s04/s05, [\_s4_animate.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/poc_living_sketchbook/seed_of_the_woman/_s4_animate.py:7) says “Only 2 clips for this tiny excerpt,” and [\_s6_assemble.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/poc_living_sketchbook/seed_of_the_woman/_s6_assemble.py:201) only has segment builders for s01-s05 while [\_spread_table.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/poc_living_sketchbook/seed_of_the_woman/_spread_table.py:16) now lists 71. As written, assembly would hit s06 and fail.

2. **The staged build order falsely exempts s51 from alignment correction.** The claim “does not block s06/s16/s51 below, which sit on already-real turn boundaries” is wrong for s51. `_turn_boundaries.json` has turn 34 at 353.657-371.210, while s51 is 359.50-365.50, an internal split. Since s51 is the Jesus anchor for later spreads, rendering it before the per-word pass risks locking the wrong visual beat.

3. **Timing artifacts are stale.** The plan says “Spread 5’s end therefore extends 33.03 → 33.80” and “total is guaranteed = 500.45s,” but [\_spread_windows.json](C:/Users/sanjay/PycharmProjects/JesusInTheBible/poc_living_sketchbook/seed_of_the_woman/_spread_windows.json:1) still contains only five windows and still ends s05 at 33.03. The seed workspace MP3/MP4 are also ~33.03s; the real 500.53s narration is in `longform/05_The_Seed_Of_The_Woman/v1/narration.mp3`, while the seed assembler hardcodes the 33s local MP3.

4. **`_PREFLIGHT.md` is not actually “matching.”** The phrase “the matching pre-designs are in `_PREFLIGHT.md`” is false. The plan rejects `bronze_serpent_long\stills\s44_shadow_cross.png`, but `_PREFLIGHT.md` still lists it as a reuse candidate. `_PREFLIGHT.md` also still contains stale “stamp + pressed lines” and “wash CONVERGES onto the cross” language that conflicts with the revised Scribed Ink and wash-retreat plan.

5. **The s71 landing device exists, but is not wired into this episode.** The plan says “`torn_out_page` transition (real, built - `panel_animator/page_transitions.py`).” The module exists, but seed [\_devices.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/poc_living_sketchbook/seed_of_the_woman/_devices.py:37) has `TRANSITION_OVERRIDES = {}`, no `DEFAULT_TRANSITION`, and no `render_transition`; seed [\_s6_assemble.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/poc_living_sketchbook/seed_of_the_woman/_s6_assemble.py:241) has no transition insertion path. This is not production-ready reuse yet.

6. **s51’s Kling assignment contradicts the project’s own cross-risk precedent.** The table says “s51 ... real clip - Kling,” while the doctrine guard says “Kling regenerates blood.” Day of Atonement’s animator explicitly says “Seedance ALWAYS for Christ/crucifixion iconography” because Kling regenerated wounds, and later replaced a cross attempt with deterministic orbit after visual drift. This plan treats the highest-risk Christ/cross anchor as an ordinary Kling spend with post-QC.

7. **Cost approval is not clean.** Section 6 says “Total rough range ~$53-80,” but Open Question 5 still says “rough ~$50-75.” The plan also says “No API called, no estimator run,” yet asks for a spend decision on a range that excludes script work, alignment-driven redraws, stale preflight cleanup, and s51 fallback risk. The repo cost module’s default long ceiling is `$40` unless overridden, so this needs an explicit estimator run and ceiling approval.

8. **The validation claim is overstated.** “Validated the Day of Atonement retrospective’s fixes on this exact content” is not supported by the local report: [\_motion_lint_report.md](C:/Users/sanjay/PycharmProjects/JesusInTheBible/poc_living_sketchbook/seed_of_the_woman/_motion_lint_report.md:1) shows “6 FAIL, 2 WARN” on the five-spread slice. If those failures are POC-size artifacts, the plan should say so and require a full-window rerun after the 71-spread implementation exists.

VERDICT: REVISE
TOP FIXES:
1. Implement and verify the actual 71-spread seed build scripts, device table, windows, full-audio wiring, and transition wiring before any spend.
2. Run the real per-word alignment pass first, including s51, then update the table/windows/preflight from that single source of truth.
3. Replace or separately gate the s51 Kling plan, synchronize `_PREFLIGHT.md`, and get a real estimator-backed spend approval.
