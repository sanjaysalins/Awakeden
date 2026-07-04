# Independent review — gemini (OK, 181s)

Here is the adversarial review of the AWAKEDEN RELEASE PLAN:

**1. Fatal Cost Assumption (Cost / Spend)**
*Citation:* `"Cost: ~$4–5 (falls with reuse)"` (Section 3)
*Finding:* This is a massive, fatal contradiction of the engine's actual cost model. `CLAUDE.md` explicitly states the cost is `"~$23/episode, ±30%"` (Kling clips ~$11, images ~$5, Opus ~$5-6). You are underestimating your production burn rate by 400-500%. This completely invalidates your financial assumptions and runway feasibility.

**2. Contradictory Runway Math (Hidden Risks / False Assumptions)**
*Citation:* `"never publish the last piece — keep ≥3 weeks of runway banked."` (Section 1) vs. `"Cluster 1 gives ~3 weeks of runway on day one"` (Section 5).
*Finding:* Cluster 1 consists of exactly 8 shorts. At your stated cadence of 3 shorts/week, 8 shorts provides exactly 2.66 weeks of runway. You are violating your own hard runway floor on Day 1 before you even press publish. You cannot launch a 3/wk cadence with only 8 videos if your absolute floor is 3 weeks (9 videos). 

**3. Hallucinated Pipeline Artifacts (Feasibility against codebase)**
*Citation:* `"...every piece is already a comic. livingpage_short.spec.json holds the beats, captions, and red-letter bars..."` (Section 7)
*Finding:* `livingpage_short.spec.json` does not exist in your pipeline architecture. According to the `CLAUDE.md` file map, the actual artifacts produced are `narration.md`, `scene_plan.json`, and `edit_plan.json`. Designing a custom site generator (`build_readpage.py`) to parse a hallucinated file format means Phase 1 will immediately fail upon implementation.

**4. Premature Engineering of the Website (Over-engineering)**
*Citation:* `"extend _website/build_catalog.py with a build_readpage.py... The Plan page (public tracker): auto-built from batches/batch_manifest.json..."` (Section 7)
*Finding:* You are prioritizing the development of an auto-generated static comic reader and a multi-file public production tracker in "Phase 1 — launch" before a single viewer has watched a short. This is textbook premature building. You are assuming viewers want to read 60s shorts as comics before validating the core YouTube loop.

**5. Unrealistic Platform Mechanics (False Assumptions)**
*Citation:* `"A/B discipline: two title/thumbnail variants per piece where the platform allows"` (Section 5)
*Finding:* YouTube Shorts do not natively support custom uploaded thumbnails in the feed (they force you to select a frame during upload on mobile), and native A/B testing for Shorts titles/thumbnails is not currently supported the way it is for long-form VODs. This "discipline" assumes platform features that do not exist for your primary format.

VERDICT: REVISE
TOP FIXES:
1. Correct the fatal ~$4-5 cost assumption to the actual ~$23/episode and recalculate your production burn.
2. Fix the runway math by either dropping the cadence to 2/wk or waiting to launch until Cluster 2 is partially banked to meet the ≥3 week floor.
3. Rewrite the Website v2 architecture to parse actual existing artifacts (`edit_plan.json` / `scene_plan.json`) instead of hallucinated spec files, or cut the comic-generator entirely until YouTube viewership is proven.
