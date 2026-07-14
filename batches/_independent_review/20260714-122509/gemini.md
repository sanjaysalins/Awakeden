# Independent review — gemini (OK, 439s)

I have reviewed the CORPUS ROLLOUT PLAN v5 against the codebase, applying the adversarial lens specified.

**Finding 1: Single point of failure in automation (Incomplete Codex Fix)**
You claim: *"all gate/stop-loss refusals now propagate to the shell exit code (round-4 codex: main() was swallowing them — automation saw success on refused runs)."*
**Reality:** The fix is only partially implemented. While `run_piece.py` returns `4` on a stop-loss breach, if an individual clip render fails (e.g. an NSFW block returning `False` from `hf_animate`), the script merely prints `"FAILED {slug}"`, continues the loop, and ultimately returns `0` (lines 403-409). Automation will receive a success code and blindly proceed as if the missing clip was successfully rendered.

**Finding 2: The 3-attempt cap is a false assumption of control**
You claim: *"Per-slug roll cap: 3 attempts, then stop and report (pilot precedent) — one stubborn CU cannot eat a wave's budget."*
**Reality:** There is zero code enforcing this cap. Furthermore, you state that *"failed-but-BILLED rolls (502s, NSFW blocks) leave neither row nor mp4"*. Because these failures generate no artifacts or ledger rows, `run_piece.py` has no state to track how many attempts have occurred. This rule relies entirely on an operator keeping a mental tally of invisible failures, meaning a stubborn CU absolutely *can* eat the budget.

**Finding 3: Fragile cross-piece dependency bypasses existing reuse tooling**
You claim: *"Wave E must never move/delete assets other pieces reference (`it_is_finished` refs `../father_forgive_them/visual/_byteplus/face_on_cross_fix2.png`)"*
**Reality:** You are establishing a hardcoded, relative-path dependency on a piece that is simultaneously slated for a *"greenfield mocomic→livingpage migration"* in Wave E. This is a massive hidden risk. The codebase has an `image_library/` directory and `asset_index.py`. Instead of relying on human discipline to not break Wave A when Wave E is refactored, you should properly promote this shared asset to the library.

**Finding 4: Unsafe default execution paths**
You claim: *"A(b) invocations MUST use `--only <ll_slugs>` — a bare `--stage animate` re-renders every hash-stale clip and burns the envelope..."*
**Reality:** If the operator simply forgets the `--only` flag, the CLI defaults to the dangerous path and silently burns the budget on non-living-light work. This critical constraint is left to human discipline instead of being fail-closed in code.

VERDICT: REVISE
TOP FIXES:
1. Fix the single point of failure in `run_piece.py`: ensure an `hf_animate` failure (like an NSFW block) propagates a non-zero exit code so automation does not proceed on missing clips.
2. The 3-attempt cap is unenforceable because failed-but-billed rolls leave no state; track failed attempts in code (e.g., in a sidecar file) to actively enforce the cap instead of relying on a mental tally.
3. Promote `face_on_cross_fix2.png` to the `image_library` using existing reuse tooling instead of hardcoding a fragile `../father_forgive_them/` relative path that will break during Wave E's migration.
