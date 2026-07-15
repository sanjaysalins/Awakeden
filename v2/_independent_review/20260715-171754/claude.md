# Independent review — claude (OK, 229s)

Verified against the codebase — this is a "DESIGN + BUILD" doc for code that has already landed (`pipeline/finality.py`, `pipeline/release_state.py`, `release_check.py`, `upload_tracker.py`, `production_board.py` all exist and wire together as described). Feasibility is real; the reuse story is good ($0, deterministic, no new external tools). But the built artifact has holes the plan glosses over.

## Findings

**1. Zero test coverage for the new chokepoint — violates the project's own standing verify.**
The repo's contract is "0 FAIL gates + the full test suite green" and nearly every other gate has a `pipeline/test_*.py` (test_publish, test_upload_lint, test_rollout_gate…). There is no `test_finality.py` and no `test_release_state.py`. The plan never mentions tests at all. The ONE rule everything now trusts (`final_video` precedence, `.bak` skipping, sha-cache invalidation, all seven SYNC gates) is unverified. The `ew-jonah` false-FINAL happened precisely because a matcher had no test pinning the failure case.

**2. Gate holes: G6 and G7 are silently skipped when a piece has no video.**
`pipeline/release_state.py:186-187` — `if not s.video: continue` sits *above* the G6 published-coherence and G7 parent-linkage checks. Concretely: an item with `youtube_id` set but `public_status: in_production` and no final video yet gets **no** G6 "youtube_id set but not live" FAIL; a short whose `parent:` points at a nonexistent slug fires nothing until a video appears. The plan's gate table states no video precondition for G6/G7 — the doc and the code disagree, and the code is the weaker one.

**3. `upload_tracker.py` rewrites THE REGISTRY non-atomically and wholesale.**
`upload_tracker.py:82-83` — `yaml.safe_dump(m, MANIFEST.open("w", ...))`: if dump throws mid-write, `manifest.yaml` — the single registry the whole design hangs on — is left truncated. No temp+rename, no backup. It also re-serializes all 80 items to set one field, reflowing every block string (git-diff churn), and the user co-edits this repo live (memory `feedback-user-coedits-live`) — a whole-file rewrite is the worst-case collision shape. The plan calls this "THE ONE WRITE PATH" without addressing write safety.

**4. The "standing rule" is unenforced — a new convention seam in a plan about killing convention seams.**
"`release_check.py` joins `validate` in the pre-ship set" — but grep shows `ship_gate.py` and `pipeline/validators.py` reference it nowhere. Publish packs went stale before *because* refresh was a convention. Wire it into an existing chokepoint (ship_gate / batch_advance / the validate skill) or it will be forgotten the same way.

**5. The read-video rule is now duplicated — drift seam #6.**
`release_state._read_video` (release_state.py:104-111) re-implements the rule in `_website/build_readpage.py:191-201` (`read_video` override, else `visual/*_scored.mp4`, skip `.bak`). The plan's entire thesis is "one rule, one computation," yet the freshness checker and the frame extractor each carry their own copy. Same for the hardcoded `https://awakeden.com/read/...` URL at release_state.py:212. When build_readpage's rule changes, G5 checks the wrong video with no error.

**6. Long-form read pages get no G5 freshness check at all.**
`_read_video` only globs `visual/` — long pieces (`visual_16x9_inked/`) return None unless the manifest carries an explicit `read_video:` (exactly 1 of 80 items has one). The G5 sha check is then silently skipped (`if s.read_video and not s.read_fresh`). The plan's G5 row claims frame-sha coverage for "promoted items" without this caveat.

**7. Smaller items.**
- `data/.sha_cache.json` is **not gitignored** (verified with `git check-ignore`) and contains machine-absolute Windows paths — it will churn in every commit.
- Doc drift: plan says `final_video(dir, kind)`; the real signature is `final_video(piece_dir)` — layout is detected, not declared.
- Orphan detection only scans `batches/*/*/piece.json` (release_state.py:159); a new `longform/` piece missing from the catalogue is never flagged, so G1's "every item joins" is one-directional for longs.
- G6 plan text says "dated ledger entry" is required, but a missing `posted` date is only a WARN (release_state.py:238-239).
- "written ONLY by upload_tracker.py --set" is aspiration, not enforcement — nothing stops another script writing the ledger.

Cost is justified (all $0, real incidents behind each seam) and this is not over-engineered — the core design is sound. The problems are hardening and honesty gaps between the doc and the shipped code.

VERDICT: REVISE
TOP FIXES:
1. Add `pipeline/test_finality.py` + `pipeline/test_release_state.py` covering finality precedence, `.bak` exclusion, sha-cache invalidation, and each SYNC gate's FAIL/WARN/skip paths — the project's own standing verify demands the suite be green, and this chokepoint has zero tests.
2. Move the G6/G7 checks above the `if not s.video: continue` in `run_gates` (release_state.py:186) so published-coherence and parent-linkage fire even when the final video is missing.
3. Make `upload_tracker.py`'s manifest write atomic (write temp, `os.replace`) and minimal-churn, and wire `release_check.py` into an existing enforced chokepoint (ship_gate/validate) instead of leaving it a standing-rule convention.
