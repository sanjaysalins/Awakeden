# Independent review — gemini (OK, 77s)

Here is the independent, adversarial review of the plan.

### FINDINGS

**1. Feasibility / False Assumptions: The cross-platform A/B testing fallacy**
> *Line/Phrase:* "Where a hook is contested, cut two hook variants of the same piece and publish the loser lane on TikTok only; compare 3-second retention." (Section 5)
**Problem:** This is mathematically and scientifically invalid. You cannot A/B test a variable (the hook) by splitting it across two completely different platforms. TikTok and YouTube Shorts have wildly different audiences, algorithmic baselines, scroll velocities, and default retention curves. A 60% 3-second retention on TikTok does not equal a 60% retention on YouTube. This is a false assumption that will feed garbage data into your analytics.

**2. Hidden Risks: UI Safe Zones & Clickable Link Restrictions**
> *Line/Phrase:* "TikTok, Instagram Reels, Facebook Reels (same file, native captions already burned in)." (Section 6)
> *Line/Phrase:* "every video description links its Read-page" (Section 6)
**Problem:** 
- **Captions:** Every platform has a different "safe zone" for 9:16 video (TikTok covers the right side and bottom third with UI, IG Reels is slightly different). If you burn captions into the "same file" without a strict, unified safe-zone mask in your PIL rendering step, your captions will be unreadable under the platform UI.
- **Links:** TikTok does not allow clickable URLs in video descriptions for standard/new accounts (you typically need 1,000+ followers or a registered business account to even put a link in the bio, let alone a video description). Relying on descriptions to drive awakeden.com traffic from TikTok will fail on day one.

**3. Missing Steps: The Email Infrastructure Void**
> *Line/Phrase:* "platform-proof home base — awakeden.com + an email list." (Section 1)
> *Line/Phrase:* "email capture (simple provider embed)." (Section 7)
**Problem:** Email signups are listed as a primary "Success metric", yet Phase 0 (Prep) completely omits setting up this infrastructure. A "simple provider embed" implies the provider exists. Who is the provider? Where is the DNS authentication (DMARC/DKIM/SPF) setup so your welcome emails don't go to spam? You cannot launch and measure email signups if the infrastructure isn't explicitly provisioned in Phase 0. 

**4. Feasibility / Over-engineering: Automated Gate Feedback Loop**
> *Line/Phrase:* "append per-piece {...} to data/learning/yt_analytics.jsonl → feeds the C0 gate weights." (Section 5)
**Problem:** Does `narration_gate.py` (your C0 gate) actually have the code to dynamically read `yt_analytics.jsonl` and mathematically alter its LLM gating criteria? "Feeds the C0 gate weights" implies an automated algorithmic loop. If this is currently just a manual review process (as Phase 2 step 11 "tune the C0 gate weights" implies), you are over-claiming the engine's capabilities in Section 5. 

**5. Over-engineering / Scope Creep: CSS Re-implementation**
> *Line/Phrase:* "the web version is a CSS re-implementation, not a copy-paste... Read-page v1 = panels + captions/bars as styled HTML text" (Section 7)
**Problem:** Re-implementing pixel-perfect text placement, bounding boxes, and typography via CSS across infinite mobile and desktop viewport sizes is a massive time sink. If the PIL video rendering already calculates and generates these frames perfectly, attempting to recreate them natively in HTML/CSS for "v1" is textbook over-engineering. Just extract the rendered PIL frames as static images.

VERDICT: REVISE
TOP FIXES:
1. Scrap the cross-platform A/B testing strategy; formulate a valid testing methodology that doesn't compare YouTube metrics directly against TikTok metrics.
2. Account for 9:16 UI safe zones for burned-in captions, and explicitly address how to handle TikTok's ban on clickable description links.
3. Add explicit email provider provisioning and domain DNS setup to the Phase 0 prep steps.
