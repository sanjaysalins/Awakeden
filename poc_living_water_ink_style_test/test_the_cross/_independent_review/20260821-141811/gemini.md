# Independent review — gemini (OK, 122s)

Here is the adversarial review of the plan:

### 1. Reuse & Missing Steps: Pipeline Evasion (Fatal)
- **Cite:** *"swirls_page.py (formalized scripts) exists; full deterministic gates deferred until the format stabilizes further."*
- **Critique:** This is a blatant violation of the repository's core invariant (`CLAUDE.md`: "The standing verify is: 0 FAIL gates"). You are proposing a parallel, un-gated workflow (`swirls_page.py`) that duplicates downstream orchestration instead of reusing `cli_visual.py`. You cannot "defer" deterministic gates (SP-G1..G9) to accommodate a new format; the gates exist exactly to validate and enforce the rules on new formats. 

### 2. Over-engineering & Cost: Premature Scaling (Fatal)
- **Cite:** *"Total season-one estimate: 14 shorts... + 2 longs... ≈ $450-920"* AND *"Zero rendered pixels for any episode in this slate"* AND *"zero ledger evidence for this format's own long-form yet."*
- **Critique:** You are asking to greenlight a ~$920 budget across an unproven slate based on a completely unverified cost model. Planning a full season before proving a single episode end-to-end is textbook premature scaling and an unjustified spend risk. 

### 3. Feasibility: Basic Math & Verification Failures
- **Cite:** *"The slate — 15 episodes"* (header) vs. *"17 candidate passages below"* (intro) vs. tables that list exactly **16** episodes (5 OT + 4 Fear + 5 Shame + 2 Longs). 
- **Critique:** The episode count is contradictory in three different places. If the plan cannot even consistently count the slate, the claim that *"Every one of the 17 candidate passages... was checked... and confirmed clear"* is highly unreliable.

### 4. Hidden Risks: Breaking the Core Format
- **Cite:** *"Simon of Cyrene has no clean Stain/Fray fit"* and is marked *"none (unique)"*
- **Critique:** The entire justification for this series is stated as: *"the motif IS the diagnosis."* By including an episode marked "none," you break the foundational grammar of the series. If an episode does not fit the motif, it does not belong in this specific slate.

### 5. Verification Gaps: Superseding Without Authority
- **Cite:** *"supersedes SWIRLS_OF_LIFE_SERIES_PLAN.md"* (header) vs. *"Governance... needs independent_review.py... In progress."* (footer)
- **Critique:** A plan cannot declare itself the superseding source of truth at the top of the document while simultaneously admitting at the bottom that its mandatory governance review is incomplete.

VERDICT: FAIL
TOP FIXES:
1. Enforce the deterministic gates immediately; integrate `swirls_page.py` into `cli_visual.py` rather than bypassing the project's core visual invariants.
2. Halt the full-season scale-up. Prove the unverified cost model and new pipeline on exactly ONE pilot episode first.
3. Correct the contradictory episode counts (15 vs 16 vs 17) and drop Simon of Cyrene if it cannot organically carry the series' mandatory motif.
