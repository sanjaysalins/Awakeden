# Independent review — codex (OK, 213s)

**Findings**

1. **The XML parser does not bind what synth actually renders.** Artifact claim: “`narration_parse now parses BOTH ... <speaker> XML`” and “hash of the SPOKEN text actually rendered.” In live code, `pipeline/narration_parse.py:96-101` only hashes `m.group(2)` inside `<speaker>...</speaker>`. But sibling `per_turn_synth.py:65-78` renders narrator text before/after speaker tags as separate narrator turns, and `pipeline/assembly_timing.py:55-75` does the same. Any mixed tagged file like `Narrator prose <speaker name="jesus">quote</speaker> more prose` is not locked against the actual rendered text.

2. **Parity is not fail-closed when only `narration.md` exists.** Artifact claim: “PARITY guard requires narration.md spoken text == narration-tagged.md spoken text.” Code returns `None` if either file is absent (`pipeline/lock.py:72-74`). `run_lock()` can lock only `narration.md`; `handoff.run_audio_pipeline()` checks once before `verify/tag/audit/synth` (`pipeline/handoff.py:239-242`, then synth at `272-281`). A generated or changed `narration-tagged.md` is not rechecked before render. That leaves an audio-render split-brain window.

3. **The engine exemption is a real bypass, not just a documented follow-up.** Artifact phrase: “Engine generate path is EXEMPT ... documented follow-up, NOT a silent bypass.” But `cli.py`’s default path runs audio (`cli.py:88-90`), `orchestrator.start()` runs `create_narration(..., run_audio=True)` (`pipeline/orchestrator.py:276-279`), and `runner.py` explicitly calls `handoff.run_audio_pipeline(folder, enforce_lock=False)` (`pipeline/runner.py:143-145`). That is the normal production path rendering audio without Phase C.

4. **The claimed “siblings + catalogue” check is not implemented.** Artifact docstring says “folder’s siblings + the catalogue.” `run_lock()` only gathers sibling folders (`pipeline/lock.py:171-186`). The registry is written (`pipeline/lock.py:207-215`) but never read during lock. `cluster_gate` even documents cross-catalogue as advisory only (`pipeline/cluster_gate.py:120-121`). This closes the Psalm 22 sibling case, not catalogue freshness.

5. **`--no-cluster` creates a full-looking lock.** Artifact exposes `cli_lock.py "<folder>" --no-cluster`; code passes `check_cluster=False` (`cli_lock.py:27`, `cli_lock.py:41`). The `.locked` file stores only `version` and `spoken_sha256` (`pipeline/lock.py:199-203`), so a lock created without the root-cause cluster gate is indistinguishable from a full lock and `require_lock()` accepts it.

6. **Caption and alignment surfaces remain outside the lock.** Artifact says “v2 fixes ALL” and frames multi-door coverage as `run_audio_pipeline` + `run_assembly`. But `veed_io.caption` can produce captioned publishable video from `--video` and optional `--script` with no lock check (`veed_io/caption.py:171-263`, CLI args at `269-276`). `assembly_align.align()` can cache `narration.alignment.json` from `narration.mp3` with no lock check if called directly (`pipeline/assembly_align.py:239-273`).

7. **The tests mutate production registry state.** The artifact’s “13/13 tests pass” is not clean evidence: tests call `L.run_lock(d...)` on temp folders (`pipeline/test_lock.py:40-51`, `102-128`, `163-168`), and `run_lock()` calls `register()` on pass (`pipeline/lock.py:191-194`). `register()` writes the real `data/learning/freshness_registry.json` (`pipeline/lock.py:214-215`). The live registry currently contains a temp-folder entry, proving pollution.

The v1 crash/punctuation/sibling-read issues are materially improved for the all-wrapped Psalm 22 short fixtures. But the plan still has false-pass and bypass paths that contradict the stated chokepoint goal.

VERDICT: FAIL
TOP FIXES:
1. Make the lock hash/parity parser use the same turn extraction semantics as `per_turn_synth` and re-check after `tag` before synth.
2. Remove or provenance-mark bypass locks: `enforce_lock=False`, `--no-cluster`, and missing-tagged parity must not produce an indistinguishable `.locked`.
3. Implement real catalogue/registry checking and isolate tests from `data/learning/freshness_registry.json`.
