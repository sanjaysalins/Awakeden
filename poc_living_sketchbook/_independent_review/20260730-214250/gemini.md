# Independent review — gemini (OK, 78s)

Here is the adversarial review of the plan:

### 1. LLM Spatial Hallucination on Coordinates (Feasibility / False Assumption)
*Cite: "candle anchors are authored per-spread coordinates from the still-QC pass (the POC's LAMP = (0.295W, 0.495H) pattern), never auto-detected"*
The still-QC pass (`verify_image`) runs on Claude Vision. Foundational LLM vision models are notoriously incapable of outputting reliable, exact X/Y pixel coordinates. Relying on Claude Vision to pinpoint the exact center of a candle will result in radial grades floating in the wrong place. Expecting a (0.295, 0.495) level of precision from the LLM is a fatal assumption. This requires either a manual human click-to-pin tool during the image gate or a dedicated bounding-box/object-detection model. 

### 2. Unspecified Synchronization Mechanism for `t` (Verification Gap)
*Cite: "API: KeeperEntry... interrupt_at=t (the Word-Whole behaviour)" AND "enforcement lives in the verse-compositing path"*
You have split the "Word-Whole" effect across two entirely separate tools (the `keeper_hand` engine stops at `t`, while the verse-compositor flashes the Word on). There is no mechanism described for how `t` is synchronized between them. How does the verse-compositor know the exact frame `t` that the Keeper's hand was interrupted? Without a shared timeline data structure or a sidecar handoff file, these two paths will drift and break the effect.

### 3. Orphaned "Filmstrip Check" Responsibility (Hidden Risk)
*Cite: "Governor: lanes planned against the CLIP's motion (a face may MOVE into a lane — check the filmstrip, not just frame 0)."*
Who or what performs this filmstrip check? The new `keeper_lint.py` is explicitly described as a "$0 deterministic script" that only "checks lanes against logo/UI zones" (which are static). A $0 script cannot see faces moving in an MP4. If this is a manual check, you haven't formally wired it into the human Assembly gates (AS-G1..G7). If it's meant to be automated, you are hiding a massive Vision/processing cost to analyze video frames.

### 4. Brittle Keyword Doctrine Guard (Over-engineering / False Assumption)
*Cite: "keeper_lint.py... flags any keeper text containing doctrine-adjacent phrasing (keyword list) for the panel"*
Using a deterministic keyword list to identify "doctrine-adjacent phrasing" is a terrible engineering trap. The vocabulary of a personal journal entry and a doctrinal claim overlap entirely (e.g., "Lord", "Word", "truth", "save"). A keyword list will either generate overwhelming false positives (creating alert fatigue for the panel) or completely miss subtle doctrinal claims. Let the LLM panel semantically review for doctrine; don't build a brittle regex pre-filter.

VERDICT: REVISE
TOP FIXES:
1. Replace the assumption that the Claude Vision still-QC pass can output exact X,Y coordinates for the candle anchor; define a manual human-pinning step or a viable detection alternative.
2. Define the explicit data handoff (sidecar file or shared timeline structure) that synchronizes the exact frame `t` between the `keeper_hand` engine and the verse-compositing path.
3. Explicitly assign the "filmstrip check" for moving clips to the human Assembly gate, as the $0 `keeper_lint.py` cannot analyze motion in video files.
