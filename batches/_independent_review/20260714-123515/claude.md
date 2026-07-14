# Independent review — claude (OK, 302s)

I verified this plan hands-on against the code, tests, ledger, and the checked-in baseline dump — most of its claims are true. Here is what I confirmed and what's still broken.

## Verified TRUE (I checked, not trusted)

- `pipeline/rollout_gate.py` implements every listed check: temp-grade arc (7000K/5500K poles), `motion:"smooth"`, `cut_ticks`, ≥3 templates, ≤60% full-bleed, adjacency rule, living_light ≥2 + played-not-dyncam'd, landing lit, double-lighting, dash/mojibake captions, and the `duration != 5` meter pin (`pipeline/rollout_gate.py:85-88`).
- `run_piece.py:343-425`: gate → exit 3, stop-loss → exit 4, bulk guard >2 pending → exit 5, **per-clip mid-batch re-check** before each `hf_animate`, and `main()` now returns `rc` with `sys.exit(main())` — the round-4 codex fix is real.
- `pipeline/rollout_spend.py`: projected check (`credits + 7.5 > 485`, line 89), recursive disk count incl. `_rejected/`/`_stale_from_bad_stills/`, `(size, mtime)` de-dup, charged at `max(ledger, disk)`.
- Live run: **5 clips = 37.5cr, headroom 447.5cr, exit 0** — exactly the plan's "ONE TRUTH" number. Ledger independently re-tallied: 5 hf clip rows since 2026-07-14, women only.
- Re-roll mechanic: `_clip_state` returns `"missing"` for a parked reject (`run_piece.py:326-329`) — real in code.
- `cli_livingpage._sfx_builder()` (line 47) and `pipeline.clip_anim_qc.build_filmstrip()` (line 69) exist as claimed.
- Baseline dump covers all 12 pieces; Wave D re-derivation checks out — `risen_christ_wounds ×5` is the only stills>2× entry; the other empty_tomb doubles are non-adjacent full-bleed repeats, i.e. $0 grid conversions. The 15–30cr number is now genuinely derived.
- Gate tests: **22 passed** (plan says 21 — immaterial off-by-one).

## Findings

**F1 (real spend-control hole): the 485cr stop-loss, gate, AND bulk guard are all keyed on `livingpage_short.spec.json` presence, not `ROLLOUT_EPISODES` membership.** All three sit inside `if (piece_dir / "visual" / "livingpage_short.spec.json").is_file():` (`run_piece.py:352`, `:381`, `:414`). The plan's headline claim — "Stop-loss is fail-closed AT THE CHOKEPOINT" — is only true while that file exists. Wave A(a) is a **full spec rewrite ×3**, and the user co-edits live (memory: `feedback-user-coedits-live`): a spec temporarily renamed/moved mid-rewrite makes `--stage animate` run with NO gate, NO 485cr stop-loss, NO bulk guard — only the $25/episode ceiling. This is exactly the mid-migration bypass class round 2 fixed for the gate condition. The fix is one line: key the stop-loss (at minimum) on `episode ∈ rollout_spend.ROLLOUT_EPISODES`, which already exists as a set. "Caveat now stated" (the cursor answer) states it; it doesn't close it.

**F2 (residual human-discipline control): the banned render paths have no mechanical teeth.** `_hf_animate_short.hf_animate` carries only `cost.check_budget` ($25/episode) and explicitly **"proceeds unmetered"** when the ledger import errors (`_hf_animate_short.py:135-136`). `_animate_rerolls.py` still sits in `batches/cluster_01_cross/` where an agent following older cluster docs will find it. After four rounds of converting SOP into fail-closed code, the last spend chokepoint is again SOP ("never the CLI"). One-line hardening: `rollout_spend.check()` inside `hf_animate` when the episode is in `ROLLOUT_EPISODES` — then F1 and F2 both close at the true bottom of the funnel, the only function that actually bills.

**F3 (minor, conservative direction): timezone mismatch in the two cutoffs.** Ledger filter is a UTC string compare (`ts < "2026-07-14"`); `disk_clip_count` uses `fromisoformat("2026-07-14").timestamp()` = local midnight (`rollout_spend.py:59`), ~5.5h earlier on this machine. Disk can therefore count late-July-13 mp4s the ledger excludes → overcounts → trips early, never leaks. Acceptable, but worth a comment so nobody "fixes" it the wrong way later.

**F4 (budget honesty, no action beyond what's written): worst case already breaches.** 24 clips × 2.3× ≈ 414cr + Wave D 35–69cr = 449–483cr vs 447.5cr remaining. The plan says "right at the wall," but strictly it's *over* the wall at the pilot rate — meaning the Wave B re-quote + scope cuts aren't a contingency, they're the expected path unless Wave A lands ≤~1.5×. The forecast rule covers this; just don't let anyone read the 180cr base as the plan of record.

**F5 (nit):** the 7.5cr pin is enforced via `duration != 5` only; `--mode pro` / aspect changes could also move the meter and aren't gate-checked. Low risk since `hf_animate` hardcodes the call, but the pin's stated coverage is narrower than "the meter is pinned."

## Verdict block

The plan is the strongest revision yet — every round-4 fix is verifiably in code, the numbers reconcile live, and the Wave D estimate is now actually derived. But F1 contradicts the plan's own central claim (fail-closed at the chokepoint) during exactly the window Wave A(a) creates, and F2 is the same class one layer down. Both are one-line closes; A(a) $0 authoring is safe to start regardless.

VERDICT: REVISE
TOP FIXES:
1. Key the 485cr stop-loss (and ideally gate + bulk guard) on `episode ∈ rollout_spend.ROLLOUT_EPISODES`, not on `livingpage_short.spec.json` existing — a spec mid-rewrite must not strip all spend control (run_piece.py:352/381/414).
2. Put `rollout_spend.check()` inside `_hf_animate_short.hf_animate` for rollout episodes so the banned CLI/`_animate_rerolls.py` paths are mechanically capped, not SOP-capped — especially since it "proceeds unmetered" on ledger errors.
3. State in the budget section that at the pilot 2.3× rate the plan is already over the remaining envelope (449–483 vs 447.5), so the Wave B re-quote + scope cut is the expected path, not a contingency; and align the disk-count cutoff to UTC (or comment the deliberate conservative skew) in rollout_spend.py:59.
