# Independent review — gemini (OK, 40s)

Here is the adversarial review of PLAN v3.

**Feasibility against the real codebase / Architecture Leakage**
*Claim:* "Retire `veed_io/_extract_spoken.py`: delete it and rewire all `veed_io` callers (caption/aligner/timing) to import `narration_parse`" (A1)
*Critique:* This introduces a severe architectural boundary violation. Looking at the workspace, `veed_io/` is structured as a standalone, reusable package (it has its own `requirements.txt`, `.gitignore`, `tests/`, and `examples/`). If `veed_io/aligner.py` or `caption.py` imports `pipeline/narration_parse.py`, you are creating an upward, circular dependency that injects domain-specific markdown rules into what should be an isolated API client. `veed_io` tools should be stripped of markdown parsing entirely and refactored to accept pure strings or structured data from the `pipeline` orchestrators.

**Hidden Risks & State Duplication (The Ledger vs. Reality)**
*Claim:* "catalogue manifest (`data/catalogue_index.json`, auto-built by globbing narration folders)" (A2) **vs.** "Dynamic phrase ledger (`data/learning/phrase_ledger.jsonl`), appended by `cli_lock.py`... Used for post-generation flagging in A2/C1" (C2).
*Critique:* You are creating two competing sources of truth for historical phrases. If `cli_lock.py` uses an append-only `.jsonl` ledger, what happens when a narration is updated, rewritten, or deleted? The append-only ledger will contain "phantom" phrases from deleted folders, permanently blocking new content with false positives. You MUST choose one source of truth: either dynamically parse the locked folders on disk at verification time, OR ensure the ledger is fully synchronized/rebuilt from disk states, not just naively appended to.

**False Assumptions / Automation Blockers (B2)**
*Claim:* "spot-check it against a second independent source and a trusted printed reference... New verses entering a narration are witnessed on demand by the same step" (B2)
*Critique:* You cannot put a manual "trusted printed reference" human-research step inside `cli_lock.py` if `cli_lock.py` is meant to be the automated chokepoint for the pipeline. If a batch runner hits a new verse, does it hang indefinitely waiting for human input? The lock step must be purely deterministic. Unverified verses must instantly *fail* the lock, prompting the author to run a separate, dedicated manual witnessing tool (e.g., `cli_witness_verse.py`) to update `kjv_verified.json`.

**Edge Cases in the Lock Token**
*Claim:* "writes a `<folder>/.locked` token (with the commit-ish of the narration text)... downstream refuses without a current `.locked` matching the narration hash"
*Critique:* What exactly constitutes "the narration text"? If the hash is generated from the raw `.md` file, then fixing a typo in a private author note (e.g., inside `## VOICE PLAN` or `## DEPTH & SOURCING`) will invalidate the `.locked` token, forcing a full re-verification of content that didn't actually change. The token must hash the *normalized, parsed spoken text outputted by A1*, not the raw file.

VERDICT: REVISE
TOP FIXES:
1. Resolve the A2 vs C2 state duplication: drop the append-only ledger or rebuild it entirely from current locked folders to prevent phantom blocks.
2. Decouple `veed_io`: do not import `pipeline` into `veed_io`; parse in `pipeline` and pass raw strings down to `veed_io` tools.
3. Remove manual witnessing from the automated `cli_lock.py` chokepoint; unverified verses must instantly fail the lock, requiring a separate human workflow to update the verified store.
