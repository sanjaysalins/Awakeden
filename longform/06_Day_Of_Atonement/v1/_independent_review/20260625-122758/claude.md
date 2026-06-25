# Independent review — claude (OK, 125s)

I read all 25 scenes against the codebase rules, the veo/long-form constraints, and the doctrinal memory. The spine is sound and the binding mix is satisfied — but the plan makes one false safety claim, carries real duplication, and skips the test-gate. Specifics:

## Feasibility / tool reality

**1. "all crosses robed → veo NSFW-safe" is FALSE (header claim vs S12/S14/S19).** The header asserts crosses are robed and therefore safe. But S12, S14, and S19 all specify *"a cloth wound about the waist and hips"* with the torso bare — that is a **bare-torso crucifixion**, exactly the thing memory `feedback-hf-video-blocks-cross` says veo3/HF video **refuses as NSFW** (video falls back to direct-Kling for the cross). A loincloth is not "robed." So three of your four Christ scenes — including the EPIC centerpiece S19 — will likely NSFW-block on veo and silently drop to the Kling fallback. The plan should (a) stop claiming they're safe, and (b) state which provider renders them. This is the single biggest unstated risk.

**2. No test-gate, and the hero is a single point of failure.** The whole film closes on S25 — a risen Christ with *"a CLEAR dark nail-wound scar piercing the centre of the open palm"* and *"five fingers."* Pierced-palm + correct hand anatomy is the hardest thing for the image model to land, and there is **no backup hero**. Memory `feedback-test-gate-before-batch` is explicit: lock the look on 1–2 paid stills before the 25-scene batch. The plan jumps straight to a full batch. Render S25 **and one cross** as test-gate stills first.

**3. No spend estimate.** 25 NBP/HF stills + 25 veo clips is a metered batch and the plan quotes nothing. `feedback-ask-before-spending` requires a pre-flight number before the run.

## Repetition / weak beats

**4. S11 and S22 are near-verbatim duplicates.** Both are *"a single live goat led away alone toward the vast empty wilderness, small against the desert distance, still and plain, NOT writhing NOT struggling."* The mood tails differ (S11 desolate / S22 dawn-bright east-west horizon), but the core image is copy-pasted. Over an 8-min film a viewer will read it as the same shot twice. Differentiate the composition, not just the lighting.

**5. The white-linen priest carries 9 scenes (S1, S3, S5, S6, S7, S9, S10, S16, S18) and the bronze altar 4 (S5, S8, S16, S18).** Plus an "altar/figure + warm shaft of light toward a far hill" motif recurs in S5, S13, S17. He's the narrative through-line, so some repetition is right — but this density risks monotony. S16, S17, S18 in particular (all sombre priest-at-altar / altar-light) are three slow beats in a row in M5–M6.

**6. Seven windows exceed the ~22s boomerang guideline.** S15–S21 all run 23.0–23.6s. Memory `longform-animation-aware-still-design` says keep windows ≤~22s and split the longest. Boomerang tolerates length better than directional, so this is minor — but it's a documented threshold crossed seven times.

## veo-morph hazards

**7. S4 crowd faces.** *"Several small grouped vignettes of bowed families"* = many faces in one frame. veo is a generative animator that morphs/invents subjects; boomerang locks the camera but does not guarantee frozen faces. Same lower-grade risk on the single faces in S15 and the welcoming face/hand of S25.

## Verification gaps (cannot confirm from the artifact)

- **Cohesion is asserted, not shown.** The header claims *"every quote's visual matches its narration cue"* and that t[] tile the turn timeline, but the **narration text was not provided to this review** — I can confirm the windows tile 0→532.6s contiguously and that the KJV cues (Lev 16:2, Lev 17:11, Isa 53:6, Heb 9:12 / 10:10 / 13:12 / 10:19, Ps 103:12) map to real verses, but not that each line lands in its window. Per `alignment-cache-staleness` / `assembly-stale-turn-overshoot`, confirm t[] came from the real `_turns` atempo audio, not scrambled meta.
- **Doctrine note (not an error):** making *both* goats types of Christ is a legitimate evangelical reading, but the strongest scholarly objection — scapegoat-as-Azazel/removal rather than Christ — is the one a panel will raise, and your M5 "honest objection" answers a *different* objection (the rite never finishes). Consider whether the spine should pre-empt it. The wrist-nailed crosses vs palm-wound hero (S25) is internally inconsistent but scripturally defensible (KJV "hands"); leave it.

**What's right (so you don't undo it):** white-linen-not-gold (Lev 16:4) is precise; God shown only as cloud+light is doctrinally safe; OT-echoes (S13/S22) + Jesus frames + multi-vignette + hero singles satisfy the binding mix; goats kept still for veo; curtain text suppressed (S3/S20). The plan is fundamentally sound — it needs cleanup, not a rebuild.

VERDICT: REVISE
TOP FIXES:
1. Drop the false "all crosses robed → NSFW-safe" claim — S12/S14/S19 are bare-torso; name the real provider (direct-Kling fallback) and test-gate one cross before the batch.
2. Test-gate the S25 resurrection hero (pierced palm + 5 fingers) as a paid still BEFORE the 25-scene run — it's the close and has no backup.
3. De-duplicate S11≈S22 (recompose, don't just relight) and break up the priest/altar repetition density in S16–S18.
