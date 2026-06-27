# Independent review — codex (OK, 81s)

**Findings**

1. **The plan is stale against repo state.** It says, “The current Awakeden eyewitness short = slideshow / boomerang stills” and “calm/intimate.” But [STATE.md](</C:/Users/sanjay/PycharmProjects/JesusInTheBible/STATE.md:44>) says the user already rejected the 2-minute calm shorts and all 9 were “rewritten punchy” and re-voiced at “1:01-1:15.” The A/B/C framing is built around an old baseline.

2. **The Veo assumption is likely infeasible for shorts.** Option B says “paid veo clips per scene,” and C says spend paid faithful cinematic moves on hook and landing. But [CLAUDE.md](</C:/Users/sanjay/PycharmProjects/JesusInTheBible/CLAUDE.md:315>) locks shorts to HF Kling pro / direct-Kling fallback and explicitly says “veo CANNOT execute the shorts’ viral cut-plan” and “Kling is the permanent shorts animation model; veo is long-form only.” This plan asks for a provider path the tooling has already ruled out.

3. **It skips the existing reusable short pipeline.** The plan talks in generic “boomerang,” “paid faithful cinematic moves,” and “A/B” terms, but does not anchor to `/witness-world`, `/witness-cut`, `_hf_animate_short.py`, the shorts assembler, clip QC, or the cost ledger. That violates the repo’s reuse direction in [v2/EYEWITNESS_SPEC.md](</C:/Users/sanjay/PycharmProjects/JesusInTheBible/v2/EYEWITNESS_SPEC.md:175>): “Reused engine ... never reimplement.”

4. **The recommended test is under-specified.** “C ... measured against A on a real A/B” has no metric definition, sample size, platform, upload schedule, thumbnail/first-frame control, caption control, or decision threshold. Retention, reverence, CTA click-through, and “not-AI-slop” can conflict; the plan never says which one wins.

5. **It omits the most relevant comparator.** The artifact admits, “We are NOT confident this beats a genuinely punchy fast-cut treatment on raw retention,” but then only proposes measuring C against A. If punchy fast-cut is the serious threat, it needs to be Option D or the control.

6. **The cost claim is hand-wavy.** “Cheapest ‘premium’ option” and “Boomerang/hold ... ($0)” ignore render retries, failed clips, QC replacement, face/Christ failure, NSFW fallback, and existing budget tooling. [PSALM22_SHORTS_BUDGET.md](</C:/Users/sanjay/PycharmProjects/JesusInTheBible/PSALM22_SHORTS_BUDGET.md:1>) already has provider costs and tracking; the plan should quote a per-pilot cost ceiling before recommending paid motion.

7. **Long-form validation is overgeneralized.** “What we just validated on the LONG form” does not prove “painterly-oil + faithful-motion look transfers to shorts.” Faster 9:16 crops, larger faces, captions, first-frame readability, and phone-feed compression are separate constraints. The plan lists this as a question but still recommends C as if transfer is likely.

8. **The “hook + landing” spend logic is too simplistic.** “the two moments that carry retention and the CTA” ignores that retention also depends on the first frame, spoken hook, caption motion, visual density, mid-video pattern breaks, and scroll-back clarity. Spending on the landing is wasted if the middle loses viewers.

VERDICT: FAIL
TOP FIXES:
1. Replace the stale calm-boomerang baseline with the current punchy 1:01-1:15 eyewitness-short baseline.
2. Rebuild the options around the actual short tooling: HF Kling pro / direct-Kling fallback, `/witness-world`, `/witness-cut`, QC, captions, and spend ledger.
3. Define a real test matrix that includes the punchy fast-cut comparator, success metrics, cost ceiling, and controlled upload variables.
