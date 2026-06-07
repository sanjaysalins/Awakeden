# Independent review — codex (OK, 181s)

**Findings**

1. `pipeline/kjv_strict.py:89,114-118` strips `.!?` from both ends of every fragment before matching. That means a real terminal-punctuation error can pass. The test at `pipeline/test_kjv_strict.py:51` even blesses `John 19:30` as `"It is finished."`, although KJV continues with a colon. This conflicts with the project rule in `pipeline/engine.py:672` requiring exact terminal punctuation.

2. `pipeline/kjv_strict.py:114-118` checks ellipsis fragments independently with `f not in text`; it does not enforce order or increasing offsets. A reversed quote like final clause first, opening clause second can still pass if both fragments occur in the verse/range. The claim at lines `16-18` that fragments are verified against their tagged verse is weaker than it sounds.

3. Phase B is not wired into the production gate. `pipeline/engine.py:703` still calls `kjv_check.verbatim_mismatches`, fed by cache-backed `pipeline/scripture.py:46-48` via `pipeline/runner.py:52-53`. `kjv_strict.py` only appears in its own file and tests. So the claim that this “closes” the corrupt-cache root cause is false unless the audit is manually run.

4. Marker handling is one-sided. `_strip_markers()` is applied to corpus text at `pipeline/kjv_strict.py:108,154`, but quoted spans only get `_canon()` at line `115`. A correct quote copied with supplied-word braces like `{saying}` or a source note marker can false-block despite the claim at lines `19-20`.

5. The import is a single-machine dependency. `pipeline/kjv_strict.py:35-57` hardcodes `C:\Users\sanjay\...PythonProject1...short_gate\kjv.py` and imports it at module import time. A fresh checkout or CI box fails before producing an audit finding. `corpus_provenance()` at lines `60-67` records paths, but not a corpus hash/version, so drift is not controlled.

6. Malformed refs can crash instead of returning `UNRESOLVED`. `_verse_text()` calls `_SG.verses_for(...)` at `pipeline/kjv_strict.py:105` without catching `ValueError`; the reused `short_gate` parser converts range endpoints with `int()` at `short_gate/kjv.py:97-101`. A bad range like `Psalm 22:7-` can abort the audit, contradicting the fail-closed claim at `pipeline/kjv_strict.py:22-23`.

7. Inline resolution can hide a bad intended echo. `resolve_inline()` searches whole cited chapters and returns `OK` on any substring match at `pipeline/kjv_strict.py:157-170`, with no verse identity, ambiguity check, or minimum distinctiveness. A misquote intended from one verse can be marked OK by matching a different verse in the same chapter.

8. The reference grammar is inherited but narrowed in practice. `short_gate/kjv.py:35` does not parse full multi-word book names like `Song of Solomon 2:1`, and the new `_verse_text()` at `pipeline/kjv_strict.py:95-99` does not preserve short_gate’s `last_book` fallback from `short_gate/kjv.py:113`. Valid human refs can false-block.

VERDICT: REVISE
TOP FIXES:
1. Replace `_fragments_in` with an ordered, boundary-aware matcher that preserves terminal punctuation unless an explicit, tested truncation rule applies.
2. Wire `kjv_strict` into the actual deterministic gate, or stop claiming the corrupt-cache root cause is closed.
3. Remove the hardcoded cross-repo import/corpus dependency by pinning a local corpus or packaged dependency with provenance hash and graceful audit errors.
