# Independent review — gemini (OK, 243s)

I have reviewed the `DESIGN v2` artifact with an adversarial, independent lens focusing on feasibility, risks, reuse, and cost.

**1. Feasibility & False Assumptions (Math Error)**
In **Step 5 — Stills**, the SWS-G10 cover edge scan claims: *"crop the same amount off all four sides (keeps 9:16)"*. This is mathematically false. Subtracting a constant pixel value `C` from both width `W` and height `H` alters the aspect ratio (e.g., `(1080 - 20) / (1920 - 20) = 0.553`, not `0.562`). Forcing this back to 1080x1920 will squash/stretch the image. Crops must be proportional (e.g., 9 pixels horizontally for every 16 vertically) to maintain the true 9:16 ratio.

**2. Hidden Risks & Single Points of Failure (SWS-G0 Spend Guard)**
In **Section 3. The pipeline**, the **SWS-G0** spend guard works out the price as *"clip 35 cr x seconds"* and rigidly enforces: *"Missing, or more than 110% of the worked-out price: ... every later paid command refuses"*. If OpenArt bills Kling 3 Omni in fixed 5-second tiers (e.g., a 7-second clip is billed as 10 seconds), the actual price will be 350 credits instead of the estimated 245 credits (142% of the estimate). This will instantly trip the fail-closed threshold and deadlock the pipeline on the very first clip. The billing increment assumption must be verified before hard-coding a strict 110% ceiling.

**3. Reuse Gaps (Code Duplication)**
In **Step 8** and **Step 9**, the plan explicitly directs: *"Copy ep13's generate_score_piano.py into the episode"* and *"Copy ep13's build_sfx.py"*. This explicitly violates DRY and codebase reuse principles. For a "repeatable pipeline", these scripts must be abstracted into central tools (e.g., in `pipeline/`) that accept the episode directory as an argument, rather than polluting every new episode folder with duplicated boilerplate.

**4. Verification Gaps & Over-engineering**
In **Section 4.1**, the draft film build claims: *"stop after the mux, pad the sound to total"*. Because the draft mux command drops `-shortest` and relies on `-c:v copy -c:a aac`, the audio stream will simply end early unless an explicit `-filter_complex "[1:a]apad=whole_dur=total"` is injected into the draft command. 
Additionally, building a full 12-step pipeline with `swirls_short.py` containing custom SWS-G lints, auto-spend guards, and Vision QC (Section 4) *before* rendering and proving the unproven 45s pilot format manually is premature over-engineering.

VERDICT: REVISE
TOP FIXES:
1. Fix the SWS-G10 math error: cropping the "same amount off all four sides" destroys the 9:16 aspect ratio; the crop must be proportional.
2. Verify OpenArt's exact duration billing increments for Kling before enforcing the strict 110% SWS-G0 spend guard, or fractional duration requests (e.g., 7s) will instantly deadlock the pipeline.
3. Abstract `generate_score_piano.py` and `build_sfx.py` into shared reusable tools instead of explicitly instructing them to be copied into every new episode folder (Steps 8 & 9).
