# Independent review — codex (OK, 190s)

**Findings**

1. **FALSE PASS: this is not a chokepoint.** The claim “audio cannot render for unlocked/stale text” is false. `runner.py:143-145` explicitly calls `handoff.run_audio_pipeline(folder, enforce_lock=False)`, and the real synth still allows direct bypass: sibling `per_turn_synth.py:170-205` has `--no-gate` and skips gating when `episode.manifest.json` is absent. No-go against the stated “fail-closed” goal.

2. **Existing media reuse bypasses the lock.** `cli_assemble.py:63-64` only checks that `narration.mp3` exists. `orchestrator.py:116-131` advances pipeline state from existing `narration.mp3`, clips, and `viral_cut.mp4`. `assembly_runner.py:120-123` and `:241-246` render from existing audio without calling `require_lock()`. A stale MP3/alignment/cut can ship after narration text changes.

3. **The hash does not bind what was validated.** `run_lock()` validates `narration.md` only (`pipeline/lock.py:123-141`), but `write_lock()` hashes `narration-tagged.md` when present (`:42-56`, `:154-157`). If `narration.md` passes KJV/cluster but `narration-tagged.md` differs, the unchecked tagged text can be locked and rendered. Also, `handoff.py:239-264` checks the lock before the tag stage, so tag output can change after the guard.

4. **Current real tagged files likely crash lock hashing.** `spoken_hash()` parses `narration-tagged.md` with `pipeline.narration_parse` (`lock.py:54`), but that parser only recognizes `**[speaker]**` block headers (`narration_parse.py:28-30`) and fails closed on no such blocks (`:120-124`). Real `narration-tagged.md` uses `<speaker name="narrator">...`, so clean real folders with tagged files are not covered by the “clean folder LOCKS” test.

5. **Registry/cross-catalogue claims are not implemented.** The doc claims “siblings + the catalogue,” but `run_lock()` only loads sibling `narration.md` files (`lock.py:113-141`). `rebuild_registry()` only globs `longform/**/.locked` (`:176`) and never calls `is_locked()` before registering current `narration.md` (`:181-185`), so stale locks can feed the registry. Writes to `.locked` and registry are non-atomic (`:155`, `:170`).

6. **False-lock escape hatches are indistinguishable.** `cli_lock.py` exposes `--no-cluster` (`cli_lock.py:11`, `:27`), but `.locked` stores only `version` and `spoken_sha256` (`lock.py:155-157`). A lock created without the root-cause cluster check looks identical to a full lock.

7. **Caption paths are outside enforcement.** `veed_io.caption` captions any video from `--video` (`veed_io/caption.py:269-276`) and optionally aligns to an arbitrary script via its own parser (`:42-52`, `:208-239`). No `.locked` check exists, so unlocked/stale cuts can still become captioned publishable artifacts.

8. **The tests prove too little.** `test_clean_folder_locks_and_registers` uses a temp folder with only `narration.md` (`pipeline/test_lock.py:16-23`, `:35-41`), not a real folder with `narration-tagged.md`. There is no test for md/tagged divergence, assembly/caption bypass, engine `enforce_lock=False`, stale registry entries, or `--no-cluster`.

VERDICT: FAIL
TOP FIXES:
1. Enforce one lock contract across audio, assembly, alignment, captioning, and existing-media reuse before any render/reuse step.
2. Validate and hash the same rendered text: parse `<speaker>` tagged files, require md/tagged parity, and re-check after tag before synth.
3. Remove or explicitly mark bypass locks (`enforce_lock=False`, `--no-cluster`, env override), and make `.locked` record source, checks run, form, and full provenance.
