# Independent review — claude (OK, 115s)

Read the artifact and grounded its claims against the repo (`_test_camera_palette.py`, `EYEWITNESS_SPEC.md`, `witness-cut/SKILL.md`, `video_render.py`). Findings below.

## What holds up
- The "current short = slideshow/boomerang stills, $0 fill" claim is accurate — `EYEWITNESS_SPEC.md:17` and `witness-cut/SKILL.md:8,14` confirm it, and boomerang is ffmpeg-loop, genuinely $0.
- It's appropriately cautious as a *decision* doc: it asks the panel and proposes an A/B rather than building Option B/C blind. No premature engineering there.

## Real problems

**1. The whole GREEN/RED camera palette was validated at 16:9 only — Options B and C assume it transfers to 9:16, untested.** `_test_camera_palette.py:17` hard-codes `config.VIDEO_HF_ASPECT = "16:9"` and every variant is a landscape composition ("vast wilderness," "the immense cracked valley"). The morph behavior that produced the rule ("rotate → AI invents geometry") has zero vertical evidence. Vertical reframing changes what's in-frame and what the model has to invent. The plan presents the palette as a portable asset ("Bring the long form's GREEN-palette... to the short's painterly stills, 9:16") — that's the single biggest hidden assumption and it's unverified.

**2. It silently crosses a LOCKED architectural line and ignores the already-built shorts animator.** CLAUDE.md's locked decisions: shorts animate on **HF Kling pro** (`_hf_animate_short.py`), and "veo is long-form only ... Kling is the permanent shorts animation model." Options B/C propose **veo** for shorts without naming Kling once. Either the lock is being overturned (then say so and justify it) or the plan picked the wrong tool. The engine already has a premium generative shorts-motion path (`_hf_animate_short.py`, gallery-tour Kling) — the plan treats "premium motion on shorts" as a net-new thing to buy via veo, which is a reuse miss.

**3. No cost math — and Option B may cost more than a whole long-form.** `_test_camera_palette.py:3` puts veo at ~$1–1.5/clip. Option B = "paid veo clips per scene." An eyewitness short has ~8–15 beats → ~$12–22/short. A *long-form* is ~$15–20 total (`EYEWITNESS_SPEC.md:207`). So Option B potentially spends long-form money on a snackable short, and the plan never surfaces this. Option C's "hook + landing only" is ~2 clips ≈ $2–3 — fine, but unquantified.

**4. The recommended A/B is hand-waved and likely infeasible.** "Measured against A on a real A/B" — no sample size, duration, metric definition, or acknowledgement that a new Awakeden channel has little/no traffic. You cannot get statistically meaningful retention deltas without an audience; the recommendation's entire validation hinges on a measurement that probably can't run for months.

**5. A fourth option is missing — and it may be the best one: punchy boomerang.** The plan frames a false dichotomy: A = calm/$0 vs B/C = paid motion = punchy. But "punchy" is an *editing-rhythm* lever (fast cuts, more stills), not a render-model lever — the `always-punchier` doctrine is "pack in more clips + speed them up," achievable with $0 boomerang stills cut tight. "Cut A fast" — premium-looking, $0, high-retention — isn't on the table at all. That omission undercuts the whole comparison.

**6. Missing the standing test-gate-before-batch step.** Doctrine (`feedback-test-gate-before-batch`) says lock the look on 1–2 paid test clips before any batch. The plan jumps to "A/B the pilot" with no cheap 9:16 camera-palette re-validation first — which is exactly the missing step that would de-risk problem #1 for ~$3.

**7. Minor: "no premium face-consistency model needed" was a 16:9 finding too** — reasonable to carry over, but it's asserted as settled for shorts when it was only proven on the long.

VERDICT: REVISE
TOP FIXES:
1. Re-validate the GREEN/RED camera palette at 9:16 on 1–2 paid test clips (a ~$3 test-gate) BEFORE proposing veo-on-shorts — the rule is only proven at 16:9, and Option B/C ride on it.
2. Add the missing fourth option — "Option A cut punchy" (fast-cut boomerang stills, $0) — and reconcile the proposal with the LOCKED decision that shorts = HF Kling pro / veo = long-form only; if you're overturning that lock, justify why veo over the already-built Kling shorts animator.
3. Put real numbers on it: per-option cost (Option B ≈ $12–22/short, near/above a long-form) and a concrete A/B method that accounts for a channel with little traffic — otherwise "measure it later" is a non-decision.
