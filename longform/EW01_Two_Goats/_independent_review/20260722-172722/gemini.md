# Independent review — gemini (OK, 53s)

Here is the independent, adversarial review of the proposal.

### Findings

**1. Style Corruption via Contradictory Prompts (Feasibility/Risks)**
*Claim/Step:* "Shallow depth of field — one plane sharp, others soft."
*Critique:* You correctly identified the risk: "real comics build depth with linework/overlap, not blur." Injecting 3D/photographic lens terminology into an explicitly 2D `VISUAL_STYLE_BASE_GN` prompt is a direct vector for style degradation. The model will resolve this contradiction by generating a 3D/photoreal image and slapping a cheap comic filter on it, destroying the "INK purity" you are trying to protect. Depth in ink is achieved via line weight, shading, and overlap—not Gaussian blur.

**2. Direct Threat to the "Frozen-Tableau" Invariant (Hidden Risks)**
*Claim/Step:* "A foreground element crossing close to the lens (silhouettes, hands, an object)."
*Critique:* This is a massive animation-safety regression. By explicitly forcing objects "close to the lens" into the foreground, you are providing prime bait for the i2v models (Seedance/Kling). Foreground hands and silhouettes are the first things these models hallucinate motion for. This directly undermines the locked pipeline discipline of maintaining a "frozen tableau."

**3. Visual Exhaustion and Tonal Mismatch (Over-engineering)**
*Claim/Step:* "One committed camera angle (low three-quarter, macro, crane)... to every inked still prompt"
*Critique:* Forcing extreme angles on *every single still* replaces flat monotony with chaotic exhaustion. Applying a "low three-quarter" or "crane" shot to a quiet, reverent teaching moment or the CTA landing will absolutely "cheapen the holy, still moments." This rule lacks pacing awareness and assumes all narrative beats require dynamic action framing.

**4. False Cost Assumptions and Insufficient Evidence (Cost/Verification)**
*Claim/Step:* "Evidence so far... n=2... one of the two grew an anachronistic cross finial (a 50% period-slip)" AND "zero marginal cost" AND "retrofitting EW01's 25 existing stills (~$7.50 + re-animation)"
*Critique:* Proposing a systemic, cross-pipeline standard based on n=2 where 50% failed is reckless. Complex spatial prompts inherently raise the defect rate because the model has to render more interacting elements. The "zero marginal cost" claim is false: a 50% defect rate means doubling your image spend (HF/NBP) and blowing up your Claude Vision audit retries. Furthermore, the ~$7.50 retrofit estimate ignores the cost of re-animating 25 clips in Kling/Seedance, re-running assembly audits, and human QA time. 

VERDICT: REVISE
TOP FIXES:
1. Replace photographic "Shallow depth of field" with 2D-native depth terms (e.g., overlapping layers, heavy foreground line-weight, atmospheric fade) to protect ink style purity.
2. Make extreme angles and foreground elements strictly conditional (e.g., for establishing shots or action beats), explicitly exempting reverent, sacred, or landing beats to protect tone and prevent i2v motion hallucination.
3. Halt the EW01 retrofit. Run a statistically significant n=10 bake-off across varied scene types (action, teaching, sacred) to measure the *actual* defect rate, Vision audit failure rate, and downstream Kling animation stability before rolling this out.
