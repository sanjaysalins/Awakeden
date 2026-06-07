# Independent review — gemini (OK, 176s)

The v2 revisions address the immediate v1 crashes, but the implementation introduces critical new bypasses and a fatal pipeline crash. The lock logic fundamentally fails to bind the speaker identity, fails-open when the source is deleted, and the engine exemption is incomplete.

Here are the concrete findings:

**1. Engine Exemption Causes a Fatal Assembly Crash**
The plan states the engine generate path is exempt, which is implemented in `runner.py` via `handoff.run_audio_pipeline(folder, enforce_lock=False)`. However, `assembly_runner.run_assembly` unconditionally calls `_lock.require_lock(v1_folder)` without any `enforce_lock` override parameter. Because engine-generated narration is "plain prose" and will always fail to lock (raising `EmptyNarrationError`), the orchestrator will hit an uncatchable `PermissionError` in `run_assembly` and crash the entire engine pipeline. 

**2. Voice-Swap Bypass (Speaker Identity Ignored in Hash/Parity)**
The `_canon_spoken` function normalizes the text by joining `b.text`, but it entirely discards the speaker identity (`name="..."` in XML, `**[speaker]**` in Markdown). This means a user or buggy script can alter `narration-tagged.md` to change `<speaker name="narrator">` to `<speaker name="satan">`. Because the spoken text is identical, both `spoken_hash` and `parity_mismatch` will falsely pass. The lock verifies the text but fails to bind the voice, allowing the pipeline to synthesize unverified speaker assignments.

**3. Parity Check Fails-Open on Missing Source (Split-Brain Hole)**
In `parity_mismatch`, the check bails out early: `if not (src.is_file() and tagged.is_file()): return None`. If `narration.md` is deleted *after* the folder is successfully locked, this parity check silently returns `None` (pass). `is_locked` will then succeed using only `narration-tagged.md`. This allows a folder to remain "locked" even after its authoritative, KJV-referenced source file is destroyed. Consequently, `rebuild_registry` will silently skip this folder in future runs, dropping it from sibling cluster checks.

VERDICT: FAIL
TOP FIXES:
1. Engine Exemption Breaks Assembly: Propagate the `enforce_lock=False` exemption parameter to `assembly_runner.run_assembly` so the orchestrator doesn't hard-crash on engine-generated plain prose.
2. Voice-Swap Bypass: Update `_canon_spoken` to include the speaker identity in the canonical string (e.g., `f"{b.speaker}: {b.text}"`) so the hash and parity checks strictly bind both the voice and the text.
3. Parity Fails-Open: Refactor `parity_mismatch` to explicitly fail closed if `narration.md` is missing but `.locked` or `narration-tagged.md` is present.
