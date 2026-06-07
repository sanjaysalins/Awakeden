# Independent review — gemini (OK, 33s)

**CRITIQUE & FINDINGS:**

**1. Catastrophic Human Bottleneck in KJV Witnessing (Phase B2)**
*   **Claim:** *"Cross-verify per-verse against ≥2 independent public-domain KJV sources; require agreement... route every disagreement to human adjudication."*
*   **Risk:** This is a massive project-blocker. There are 31,102 verses in the Bible. Different public KJV datasets (even Cambridge 1769 editions) have *thousands* of orthographic and typographic variances (e.g., "Spirit" vs "spirit", "spake" vs "spoke", hyphens vs em-dashes, colons vs semicolons). Routing *every* disagreement to human adjudication is completely unworkable and will stall the project indefinitely.
*   **Fix:** You must select *one* highly vetted structured dataset (e.g., a specific Cambridge 1769 XML/JSON from a reputable scholarly source) as the baseline, programmatically accept it, and perform human spot-checks *only* on a predefined list of known hard cases (like Ps 22:7). 

**2. Hand-Waved "Standing Gate" for Hand-Authored Content (Phase C2 / A4)**
*   **Claim:** *"Identify the single lock chokepoint (or add one) so future locks append reliably... today `_finalize.py` only renders audio and `handoff.py` only covers engine-generated content; hand-authored folders touch neither."*
*   **Risk:** You are building standing gates to prevent human error, but explicitly admitting that the hand-authored files *have no systemic lock step*. You cannot tell a script to "identify or add one" as a passing thought. If it doesn't exist, your standing gates will remain optional CLIs that humans forget to run (which is exactly what caused this defect).
*   **Fix:** The plan must explicitly design the lock mechanism for hand-authored text. (e.g., "Create `cli_lock.py` which runs all C1/A2 gates and outputs a `.locked` token file, and modify the Veed.io rendering scripts to *refuse* to render audio for any text lacking this token").

**3. Silent Duplication and Downstream Breakage (Phase A1)**
*   **Claim:** *"New importable `pipeline/narration_parse.py`... parsing `**[speaker]**`..."*
*   **Risk:** You are creating a new parser to fix the fact that `veed_io/_extract_spoken.py` fails on shorts. However, the plan does not explicitly state that it will refactor `veed_io` to use this new parser. `veed_io` contains `aligner.py`, `caption.py`, and `_extract_spoken.py`. If you build `narration_parse.py` in `pipeline/` but leave `veed_io` alone, the downstream captioning and timing pipeline will still fail silently on shorts. 
*   **Fix:** Phase A1 must explicitly include deprecating/removing `veed_io/_extract_spoken.py` and wiring `veed_io`'s internal tools to depend entirely on the new `pipeline/narration_parse.py`.

**4. Typographical False-Fails in Exact Matching (Phase B4)**
*   **Claim:** *"Interior punctuation must match exactly; boundary ellipsis... is allowed"*
*   **Risk:** Hand-authored markdown files frequently contain smart quotes (`""` vs `“”`), apostrophe variants (`'` vs `’`), em-dashes (`—` vs `--`), and whitespace inconsistencies. KJV datasets typically use strict ASCII. If you enforce "exact" interior matching without aggressive typographical normalization, you will generate endless false-FAILs for perfectly accurate quotes, frustrating the authors.
*   **Fix:** Specify that the B4 check will normalize all smart quotes, dashes, and whitespace variations prior to the contiguous substring check.

**5. Tool Proliferation (Phase A2 vs C1)**
*   **Claim:** *"A2 — Cluster / series review gate (`cluster_review.py`)"* and *"C1 — Standalone verify harness (`verify_narration.py`)"*
*   **Risk:** You are proposing building *two* separate verification CLIs. Splitting the review process into `cluster_review.py` (which checks the ledger/group) and `verify_narration.py` (which checks KJV quotes) guarantees workflow fragmentation.
*   **Fix:** Consolidate. There should be *one* verification CLI (`verify_narration.py`) that accepts either a single artifact or a directory/list of artifacts, applying the KJV rules to all of them, and then applying the cluster/ledger rules to the set.

VERDICT: REVISE
TOP FIXES:
1. Scrap the "human adjudication for every disagreement" requirement in B2; pick one vetted scholarly dataset and spot-check only known edge cases.
2. Explicitly define the mechanical lock chokepoint for hand-authored content (e.g., a `.locked` token system required before audio render), rather than leaving it as "identify or add one".
3. Require deprecation of `veed_io/_extract_spoken.py` and wire all `veed_io` tooling (captions, aligner) to use the new `pipeline/narration_parse.py` so the downstream pipeline doesn't break.
