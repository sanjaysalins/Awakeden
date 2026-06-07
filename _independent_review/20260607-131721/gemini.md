# Independent review — gemini (OK, 32s)

Here is the adversarial critique of PLAN v4:

**1. The "Porting vs. Duplication" Paradox (Creates a Forked Source of Truth)**
*   **Claim:** *"build the gate in THIS repo, reusing `short_gate`'s proven pieces... Do NOT edit the sibling-repo `short_gate`... Port the proven logic into this repo's `pipeline/` and wrap it."*
*   **Critique:** Copy-pasting `short_gate/kjv.py` and `gates.py` into this repo's `pipeline/` is the exact definition of code duplication, masked under the word "porting". You are creating a parallel, disconnected fork of the core verification logic and the KJV corpus. If a bug is fixed or a new book alias is added to `short_gate` tomorrow, this repo will not get it. True reuse means importing the sibling library directly or abstracting it into a shared dependency, not copy-pasting its files. 

**2. The Registry Rebuild Flaw (Destroys Cross-Repo History)**
*   **Claim:** *"Single source of truth: rebuild the registry from on-disk `.locked` folders at check time... Scope: within-series AND across-catalogue, via a manifest auto-built by globbing... NARRATION_TREE_DIR"*
*   **Critique:** The plan explicitly states that the sibling repo uses `short_gate` which has its own registry (`_registry/freshness.json`). If you rebuild the registry purely by scanning for `.locked` files across both repos, you are making a fatal assumption that the sibling repo also generates `.locked` files in the exact same format. If it doesn't, your globbing will silently ignore the entire sibling repo's history, completely breaking the "cross-episode freshness" requirement.

**3. Punctuation-Strict Substring Match (Guaranteed High False-Positive Rate)**
*   **Claim:** *"add a punctuation-strict mode: ... compare the quote as a contiguous substring of its own tagged verse with interior punctuation preserved"*
*   **Critique:** The KJV is littered with archaic punctuation (colons and semicolons in the middle of sentences). When narrators adapt this for spoken scripts, they routinely change terminal punctuation (e.g., turning a semicolon into a period) for pacing or grammar. A strict contiguous substring match will cause massive false failures for legitimate, faithful quotes. You are solving the Ps 22:7 comma issue by introducing a sledgehammer that will break dozens of previously valid scripts.

**4. Global BLOCK on Openers (Paralyzes Future Content)**
*   **Claim:** *"add cta_fingerprint... and opener_family ('thousand years' + similar stems). CTA/opener repetition is BLOCKING"*
*   **Critique:** Making "thousand years" a *blocking* offense across the *entire* catalogue (cross-series) means no script can ever use that phrasing again, even years from now. The problem in Psalm 22 was that 5 out of 8 shorts in the *same cluster* used it. Elevating this to a global, catalogue-wide block rather than a cluster-density check is severe over-engineering that will trap future writers.

**5. `veed_io` Decoupling Breaks Standalone Utility**
*   **Claim:** *"retire `_extract_spoken.py` and route `caption.load_script_text`'s short path through the string it's handed."*
*   **Critique:** `veed_io` appears to be a standalone integration module (with its own `cli.py` and `tests/`). If you remove its ability to extract spoken text and force the higher-level `pipeline` to pass plain strings down, you risk breaking `veed_io/cli.py` and any external scripts relying on it to process files natively.

VERDICT: REVISE
TOP FIXES:
1. Re-evaluate "Porting": Do not copy-paste code. Either dynamically import `short_gate` from the sibling repo's path via `sys.path` or extract it to a shared Python package to prevent diverging forks of the verification logic.
2. Fix the Registry Source of Truth: Rebuilding from `.locked` files will miss sibling-repo history unless you explicitly map and ingest `short_gate`'s existing `freshness.json` during the rebuild step.
3. Relax Punctuation Strictness: Modify the verbatim check to enforce interior commas/words but allow flexibility for boundary/terminal punctuation (periods, semicolons, question marks) to accommodate spoken script pacing.
