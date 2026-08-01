# Independent review — gemini (OK, 58s)

Here is the adversarial review of the proposed plan.

### 1. Feasibility & Hidden Risks: Generative spatial tracking is assumed but not solved
**Citation:** *"Anchor MUST be a drawn light source in the approved art"* (Engine 5) and *"lanes planned against the CLIP's motion (a face may MOVE into a lane)"* (Engine 1).
**Finding:** The plan assumes the text/compositing engine magically knows the (x,y) coordinates of a "drawn light source" in a generative still, and the bounding-box motion of a face in a generative Kling video. There is no automated spatial tracking for Kling outputs in this codebase. Unless you are introducing a manual human-in-the-loop coordinate tagging step (which is missing from the plan) or a Vision LLM pass (which violates your "$0 per episode-use" claim), these features will blindly composite over faces and the wrong parts of the image. 

### 2. False Assumption: Audio silence equals handwriting panic
**Citation:** *"Production energy source: the held-breath envelope sampled over the entry's window — the narration's own fear drives the hand."*
**Finding:** You are conflating two entirely different data structures. The existing `held-breath` skill detects discrete audio silences/pauses. Assuming a pause array maps cleanly to a continuous `0.0 ... 1.0` "panic/energy" envelope that dictates physical handwriting jitter is a massive, unproven leap. Silence often means reverence or calm, not just "fear." This mapping will produce erratic, nonsensical handwriting behavior if wired up blindly.

### 3. Missing Steps: Asset extraction is hand-waved
**Citation:** *"Studies derive ONLY from the spread's own approved art"* (Engine 2).
**Finding:** How exactly does `margin_study.py` "derive" a graphite sketch from a Baroque oil painting? Are you running an edge-detection OpenCV filter? Are you prompting a new image generation? The technical implementation of extracting a doodle from the approved art is completely missing. If it requires generation, your $0 cost claim is false again.

### 4. Verification Gap: Process violation on locked rules
**Citation:** *"DELIBERATELY revises §5's universal letter-by-letter reveal, pending panel"* vs. Build Order Step 5 (*"§5 letter-reveal rule amended"*) and Step 6 (*"External 5-CLI panel review"*).
**Finding:** You cannot amend a locked doctrine rule (Step 5) *before* the independent panel actually reviews and approves it (Step 6). If the panel rejects the revision to Law 1, your engine is already built and the documentation is already mutated. The panel must gate the rule change, not rubber-stamp it after the fact.

VERDICT: REVISE
TOP FIXES:
1. Define the exact technical mechanism for extracting spatial coordinates (light sources) and avoiding moving subjects in generative clips without breaking the $0 cost model.
2. Define the exact image-processing method `margin_study.py` will use to turn oil paintings into graphite sketches.
3. Reorder the build steps so the 5-CLI panel approves the doctrinal §5 rule change *before* it is written into the SKILL.md system.
