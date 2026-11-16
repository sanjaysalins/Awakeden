**A. My own bake-off (5 lines)**
1. Pick 3 stories, not 1. Same-story pairs, two formats only: Control vs "Hook-first + short + loop".
2. Build the new format as a real new build, not a re-cut of old assets.
3. Show 60+ strangers per pair on phones, muted-first. Primary metric: swipe point and completion.
4. Write one primary metric and one threshold before looking. Everything else is a diagnostic.
5. Test format changes one at a time only if the first test shows a gap. Otherwise ship the bundle.

**B. Grade the draft**
- Arm A (control): KEEP. It must stay the exact shipped file, with no re-encode.
- Arm B (hook-first): CHANGE. It bundles title length, spoken hook, and page count. If it wins, you can't say why.
- Arm C (rhythm): CHANGE. It is B plus cuts, so C vs B isolates the cuts. But the panels are low-res crops, so a loss may only be a quality loss.
- Arm D (big-picture): CHANGE. It changes page chrome, loop ending, and framing all at once. It is built on a different base than C, so C vs D is not clean.
- Layer 1 numbers: KEEP, but relabel. These are manipulation checks. They prove you built the arm you meant to build. They say nothing about which arm is better.
- Layer 2 blind panel: CHANGE. AI seats are not viewers. "Would I swipe at 3 s" is a guess. Use it as a bug-finder, not as a vote.
- Layer 3 real viewers: CHANGE. 20-30 people can't detect a small effect. The bigger problem is who they are (see C).
- Win rule: CHANGE. See F.
- Bake-off 2: KEEP, with changes. 5 stills per arm is too few. A stochastic defect needs about 15-20 per arm. It is also a different question, so don't let it share the "win" language.

**C. Biggest flaw**
The test runs on one story that was picked because it is the cleanest: 64 s, 0 rejects, no bug. Four arms are compared on that single story. Whatever wins is a statement about Ep 8 only. Ep 8 is also the best case for Control, so an A win says little about the weaker episodes. The arms are also re-cuts of assets made for the control format, which favors A. And people who know the owner, or who watched the arms back to back, will judge by taste. The result can look decisive and still not carry over to the next story.

**D. Wrong or unsupported claims**
- "A win needs 2 of 3 layers" implies the layers are independent. They aren't. The panel and the numbers both reflect the owner's own rules, so they agree by construction.
- The pack presents the panel's earlier finding ("first 2 s, pacing, legibility, loop ending") as evidence for the rules. It was the same kind of AI seat, with no viewer data. These rules are hypotheses.
- "Target 45-60 s" is a guess. The measured facts show runtimes, not performance. No retention data exists.
- The loop ending is assumed to help. Nothing here supports that.
- "Ties go to the cheaper arm" and "the owner's hours count" are unmeasured.
- The Layer 1 "time to first picture change" has no stated threshold or link to outcomes.
- The pack says 12 films were audited as "no file is broken", but only the 4 near-60 s films fit the proposed length rule. The other 8 are not comparable on length.
- The 48 h post is described as optional. At zero followers it is an n=1 comparison with noise from the algorithm, time of day, and audience seeding.

**E. What to add or change (ranked)**
1. Run at least 3 stories, including 1 weak one and 1 long one (the 106 s). Report per-story results, not a pooled number.
2. Fix one primary metric and a numeric threshold before looking (e.g. "completion of first 10 s, B beats A by 15 points"). Without it, "2 of 3" lets the owner pick a win after the fact.
3. Make the real-viewer layer non-friends. Use a paid panel or cold strangers. Don't let the owner or people who know the series be the sample. Randomize order, and counterbalance muted/sound. Each person sees one arm only for a retention measure.
4. Separate the bundle: B alone, then B+loop. Or admit that you're testing a package. Don't call it "which element works."
5. Add one new build at the end of the test, built from scratch in the winning format. A re-cut can't show whether the format works when it is made that way from the start.

**F. Is the win rule sound?**
No. "2 of 3 layers" lets two weak layers outvote one real one. The panel and the numbers are cheap and correlated. Layer 3 is the only one that measures viewers.

Better rule: Layer 3 decides. An arm wins only if it beats Control on the pre-set primary metric in the strangers' test, in at least 2 of 3 stories. The panel has a veto only: if any seat can't say who/what/why, fix it first. The numbers confirm the build. If the effect is under the noise level, declare "no detectable difference", pick the cheaper arm, and move on.

**G. Confidence: 5/10** that this design would pick the better format.
It would go up with: 3 stories, a stranger sample of at least 60, a numeric primary metric, and a from-scratch build.
It would go down if real viewers are friends, or if Ep 8 is the only story.
