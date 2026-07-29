# Independent review — gemini (OK, 59s)

Here is the adversarial review of the proposed plan. 

### FINDINGS

**1. False claim masking ignored tests (Inherited Flaw)**
*   **Citation:** §14: *"Comic-strip-native has never been tried against a locked EXTERNAL reference image — only page-to-page self-chaining within one piece."*
*   **Critique:** This is factually false and ignores project history. External Christ-reference chaining *was* tested in `poc_thief_e2e/_comic_strip_native.py` on 2026-07-24 and silently dropped. The plan builds its "single most important open item" and "concrete next experiment" on a lie, proposing to re-test something that already failed or was discarded without analyzing *why* it was discarded.

**2. Physically impossible Stage 3 choreography (Feasibility/Over-engineering)**
*   **Citation:** §7: *"treat each comic-strip-native PAGE the way the living-page engine treats one beat's panel grid — a grid_choreography pass... sweeps attention across the page's live panels"*
*   **Critique:** Fatal technical assumption. `grid_choreography.py` works on the living-page lane because the code *composites* the grid and knows the exact mathematical coordinates of every panel. A comic-strip-native page is a single, flat, AI-generated PNG. There is no coordinate data, no bounding boxes, and no DOM. You cannot run a "virtual page camera" over a flat image without a panel-detection/bounding-box extraction step, which is entirely missing from this plan.

**3. Doctrinal hallucination accepted as a "cost" (Hidden Risk)**
*   **Citation:** §6e: *"accept some invention as a real, named cost... If invention becomes unacceptable for a specific real piece (e.g. a sacred beat where an invented gesture on Christ is a doctrine problem...)"*
*   **Critique:** You cannot accept "some invention" on Christ's actions during a passion panel. The plan admits Kling 3.0 invents motion, accepts it as a baseline, and offers only an *untested* fallback ("crop-and-recomposite... never actually run") for sacred beats. Proposing a pipeline that has no proven defense against doctrinal hallucination in motion violates the project's core invariants.

**4. Doubling down on broken negative prompts (Inherited Flaw)**
*   **Citation:** §6d: *"CSN-G3 Christ body gate | no heroic/athletic musculature, no ab-definition, no blood... recurs even with 'fixed' wording"*
*   **Critique:** The plan complains that the body-gate fails repeatedly, but continues to use strictly negated prompt phrasing ("no heroic... no ab-definition"). It completely ignores the locked rule in `v2/AWAKEDEN_COMIC_DNA.md` Section 5a which explicitly warns against negated prompt phrasing (since image models notoriously draw the exact things you tell them "no" to). 

**5. Blindly inheriting wrong costs (Cost/Spend)**
*   **Citation:** §6d: *"Cost: ~$0.40/page at 2k, 9:16 (today's actual rate, COMIC_STRIP_NATIVE_SPEC.md §8)."* and §16: *"Comic pages, 3 pages @ $0.40 | ~$1.20"*
*   **Critique:** The parent spec (`COMIC_STRIP_NATIVE_SPEC.md`) failed independent review specifically because this per-page cost was wrong. This plan blindly copies the false rate and uses it to justify the production budget in §16.

**6. Manual cropping assumed but not specified (Missing Steps)**
*   **Citation:** §12: *"cut-outs: make_cutouts.py needs a clean single-figure Christ painting... will likely need a CROPPED panel, not the whole page, as its source image"*
*   **Critique:** Similar to the Stage 3 failure, how is this panel cropped? Without panel boundary data, this implies a human must manually slice the PNG in Photoshop before Stage 7 can run. This breaks the automated pipeline promise.

VERDICT: FAIL
TOP FIXES:
1. Acknowledge and analyze the 2026-07-24 `poc_thief_e2e` external reference test instead of falsely claiming it never happened.
2. Design a real panel-coordinate extraction step for Stage 3, because `grid_choreography` cannot sweep across a flat, unmapped PNG.
3. Fix the CSN-G3 Christ body-gate by removing negated prompt phrasing per the `AWAKEDEN_COMIC_DNA.md` standard, rather than accepting failures as inevitable.
