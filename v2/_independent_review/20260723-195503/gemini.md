# Independent review — gemini (OK, 68s)

This plan contains critical contradictions, feasibility blockers, and fundamental misunderstandings of both generative AI and platform algorithms. 

Here are the specific findings:

**1. Contradiction on Negative Prompts (§1)**
- **Claim:** "The render prompt (both providers, genuinely...) AND it MUST carry the no-baked-text negatives (`no text, no lettering...`)"
- **Contradiction:** Just three sentences later, the plan admits: "seedream has no true negative-prompt channel and can DRAW the forbidden object; describe the desired end-state positively instead". 
- **Problem:** You cannot strictly mandate a list of negative prompts for a provider you acknowledge ignores them. The strategy for keeping text out of Seedream renders is fundamentally unresolved.

**2. Destructive AI Video Artifacts (§1 & §6)**
- **Claim:** To solve dot-crawl on animation, the plan suggests to "Bake dots into the plate (move *with* the art)".
- **Problem:** This demonstrates a complete misunderstanding of how Kling and Seedance work. If you bake a Ben-Day halftone grid into a still image and feed it to a generative video model, the AI will not treat it as an optical screen layer. It will warp, melt, and stretch the dots as the subjects or camera move, resulting in severe visual hallucinations and destroying the print illusion.

**3. False Assumptions about YouTube Algorithms (§9)**
- **Claim:** "Cold-audience A/B on real traffic — the same piece cut two ways: retro-comic vs. plain cinematic-inked — measured on thumbnail click-through..."
- **Problem:** You cannot upload the exact same audio/narrative cut two different ways to a single YouTube channel without triggering duplicate content flags, which will cannibalize reach or penalize the channel. Furthermore, for Shorts (9:16), "thumbnail click-through" is a fundamentally flawed metric because the vast majority of traffic comes from the swipe feed where thumbnails are never seen.

**4. Missing Programmatic Triggers (§5a)**
- **Claim:** "Body gate: every passion Christ frame is checked (Vision) to FAIL idealized musculature..."
- **Problem:** The plan creates rules for "GLORY beats" vs "PASSION beats" but outlines no technical mechanism for the pipeline to know which beat is which. Without modifying `scene_plan.json` to explicitly tag `passion_beat: true` so the Claude Vision script knows when to apply this specific exclusion list, this gate cannot be reliably automated.

VERDICT: REVISE
TOP FIXES:
1. Reconcile the Seedream text-avoidance strategy in §1; define positive-only text-avoidance prompts rather than mandating a negative list the model ignores.
2. Abandon the "Bake dots into the plate" strategy in §1; relying on Kling/Seedance to animate a halftone grid will result in warped textures. You must solve this in post-compositing (Remotion).
3. Redesign the A/B testing protocol in §9 to avoid YouTube duplicate content penalties, and drop the reliance on Shorts thumbnail metrics.
