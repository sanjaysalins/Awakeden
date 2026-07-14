# Independent review — claude (OK, 293s)

I verified this plan claim-by-claim against the repo. Most of it checks out; two real defects remain, both in the spend control the plan leans hardest on.

## Verified TRUE (no action)

- `pipeline/rollout_gate.py` + `pipeline/rollout_spend.py` exist; **21 gate tests pass** (ran them). Stop-loss is wired at `run_piece.py:362-366` with exit 4, and `JITB_SKIP_ROLLOUT_GATE=1` bypasses only the gate, **not** the stop-loss — as claimed.
- The "no silent fallback" claim is accurate: `ffmpeg_fallback` lives only in `_hf_animate_short.main()` (line 206); the `hf_animate()` function `run_piece` imports returns `False` and `run_piece.py:397` prints `FAILED`, substituting nothing.
- `run_piece.py:34` ARK endpoint, `reuse_check` (run_piece.py:103), `cli_livingpage._sfx_builder` (line 47), `sfx_pilots/build_cluster1_sfx.py` PIECES dict — all real. The gold-master script to generalize exists: `C:\Users\sanjay\PycharmProjects\JesusInTheBible\batches\cluster_02_resurrection\women_first_witnesses_luke245\promote_living_light.py`.
- All 12 rollout pieces + gold master already carry `visual/livingpage_short.spec.json`, so the spec-presence condition guarding gate+stop-loss is closed in practice. All `piece.json` animate durations are 5s, so the flat 7.5cr/clip constant holds.
- Ran `python -m pipeline.rollout_spend`: 6 clips / 45.0cr / 440.0cr headroom — matches the plan's numbers exactly. `it_is_finished_john1930/piece.json:60` does reference `../father_forgive_them/...face_on_cross_fix2.png`, so the Wave E don't-move-assets constraint is justified.

## Finding 1 (major): the disk cross-check goes blind on exactly the spend it exists to catch

`disk_clip_count()` (`pipeline/rollout_spend.py:58-64`) counts `*.mp4` **non-recursively** in only `visual/clips/` and `visual/_fx_pilot/`. But the plan's own workflow moves paid mp4s out of that set: checklist step 5 parks QC rejects in `visual/clips/_rejected/`, and `run_piece.py:385-390` moves stale clips to `clips/_stale_from_bad_stills/`. At the pilot-observed 2.3×/keeper rate, **more than half of all paid rolls end up as rejects** — invisible to the disk count — and the ledger is the only record left, which is precisely the writer the plan admits is best-effort (already observed under-counting: 5 ledger rows vs 6 disk files today). "Charged at the HIGHER number" is only as strong as the larger of two under-counts. One-line fix: `rglob` under `visual/clips/` (or add the park dirs explicitly). Related mechanics gap worth one sentence in the plan: `run_piece --stage animate` skips hash-current clips and has no `--force`, so the *only* re-roll path for a QC-rejected clip is moving the mp4 out — i.e., the re-roll workflow itself is what starves the disk counter.

## Finding 2 (major): the budget forecast ignores its own zero point

The plan says pilot spend counts INSIDE the 485 envelope and states 45cr already charged. But the forecast lines compare `base × rate` against **485**, not against the 440 remaining: worst case is 45 + 569 ≈ **614cr (deficit ~129cr, not 84)**; the hoped 1.5× case is 45 + 371 ≈ **416cr, leaving only ~69cr of headroom, not 114**. The scope-cut trigger ("if the forecast breaches 485") is therefore keyed to the wrong threshold — it should be `45 + base × rate > 485` (equivalently, forecast vs 440). The stop-loss code gets this right; the plan's re-quote arithmetic doesn't.

## Minor notes

- The disk counter over-counts in the other direction too: a $0 mp4 landing in a counted dir (an old CLI ffmpeg-fallback output, a copied/rebuilt file with a fresh mtime — see memory `dyncam-stale-cache-guard`) is charged as 7.5cr. Fail-safe direction, but near the cap in Wave C/D it could falsely trip the stop-loss; worth knowing before debugging a phantom breach.
- Stop-loss coverage is conditional on `livingpage_short.spec.json` existing. All in-scope pieces have one today, so this is theoretical — but the plan's flat claim "fires on EVERY `run_piece --stage animate`" should carry the same "where a spec exists" caveat the gate sentence has.

Structure, wave ordering, re-quote gate, scope-cut menu, and the reuse discipline are all grounded and proportionate — no over-engineering found, no duplicated tooling (A(a) generalizes an existing script rather than rewriting).

VERDICT: REVISE
TOP FIXES:
1. Make `disk_clip_count` recursive over `visual/clips/**` (including `_rejected/` and `_stale_from_bad_stills/`) so re-rolled/rejected paid clips — the dominant spend class at 2.3× — stay in the max(ledger, disk) charge.
2. Re-base the forecast on the 440cr remaining (45 + base×rate vs 485): worst case is ~614 not 569, hoped case leaves ~69cr headroom not ~114 — and key the scope-cut trigger to that corrected number.
3. Document the re-roll mechanic in the plan (reject → park mp4 → re-run `--only <slug>`; no `--force` on animate) and add the "where a livingpage spec exists" caveat to the stop-loss claim.
