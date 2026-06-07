# Independent review — claude (OK, 174s)

I verified the plan's premises against the actual repo. They hold up — this is an honest, well-grounded plan. But I found gaps in the keystone itself.

## What I confirmed (premises are real)

- **Parser empty-on-shorts** — `veed_io/_extract_spoken.py:20-21` only keeps text inside `## MOVEMENT`; short #01 uses `**[narrator]**` blocks with no movement headers → returns empty. ✅ True.
- **Ps 22:7 cache corruption** — cache holds `"...they shake the head saying,"` (missing the comma after *head*). ✅ True.
- **Calibration inert** — `panel_misses` only *read* (`learning.py:56`), never written; `append_record` defined (`learning.py:45`), zero callers in-repo. ✅ True.
- **Single-artifact review** — `independent_review.py:157-158` takes one `artifact`, `--type` ∈ {narration, plan} only. ✅ True.
- **No lock step** — `_finalize.py` just clears stale files and calls `handoff.run_audio_pipeline`; no gate. ✅ True.
- **Engine gates exist** — G3 "pierces" / G8(3) "actually PIERCES" confirmed in `engine.py`. ✅ True.

## NEW problems (cite the real repo)

**1. The keystone's enforcement point is underspecified — and "non-bypassable" is overstated.** The plan says *"`per_turn_synth` / `_finalize.py` ... check for a current `.locked` token and abort."* But `per_turn_synth.py` does **not live in this repo** — it's in `PythonProject1`, which CLAUDE.md marks *reuse-don't-duplicate*. Guarding it means editing a foreign project. The only chokepoint this repo actually owns is `handoff.run_audio_pipeline` (called by `_finalize.py`). A user invoking `per_turn_synth.py` directly — a documented reuse path — **bypasses a guard that lives only in `_finalize`**. The plan must name `handoff.run_audio_pipeline` as the canonical guard and either (a) add a small token-check inside the foreign synth script, or (b) explicitly declare handoff the *sole* sanctioned audio entry and concede the residual bypass. Right now the keystone claim ("non-bypassable") is aspirational.

**2. A3's "hard requirement" is internally inconsistent with the real CTAs.** I pulled the 8 actual closers. **Seven** end with the byte-identical sentence `"Come to Him."` — but **#02** ends `"That's Jesus — come to him."` (lowercase, em-dash, one sentence). So *exact full-sentence match flags 7/8, not 8.* #02 only joins under case-insensitive substring normalization. Yet A3 says *"The exact-CTA catch is the hard requirement"* while elsewhere acknowledging variants (`come to Him and drink`). Pin the deterministic bar precisely: **normalized closer-substring `come to him` = 8/8**, not "exact." Otherwise A3 can pass on 7 identical strings while believing it caught the 8× problem.

**3. `.locked` hash scope is undefined.** *"commit-ish of the narration text" / "matching the narration hash"* — is it the whole `narration.md` (which carries a huge non-spoken `## DEPTH & SOURCING` + `## VOICE PLAN` ledger, so editing a comment needlessly busts the lock) or spoken-only via A1? Stale-detection hinges on this. Define it.

## Minor
- The "proof obligation" (*8 shorts flow through `cli_lock.py` before further code*) is mildly circular — `cli_lock` needs A2/B/C to exist to run a full pass. Sequencing resolves it (skeleton → A → prove → B → C), but the wording oversells "before any code is built on top."
- Cross-catalogue exact match at ~76 shorts + ~21 longs is trivially cheap — no perf concern. Good.
- `bible-api-not-a-fallback-for-lock` (B3) correctly closes the corrupt-cache trust hole. Strong.

## Go/no-go
**GO to implement** — the architecture is sound, the v2 gaps (chokepoint, scoped canon, one CLI, honest inert-calibration) are genuinely closed, and the premises are verified. But the keystone's *enforcement point* and *acceptance bar* are not yet pin-down-tight, and both are checkable against this exact repo. Fold the three fixes before building, not after.

VERDICT: REVISE
TOP FIXES:
1. Name `handoff.run_audio_pipeline` as the canonical fail-closed guard (not the out-of-repo `per_turn_synth.py`); either add a token-check to the foreign synth or explicitly concede + close the direct-synth bypass — otherwise "non-bypassable" is false.
2. Redefine A3's hard requirement as a **normalized closer-substring** catch (`come to him` = 8/8), since 7/8 are exact but #02's lowercase em-dash closer escapes exact-sentence matching.
3. Specify exactly what the `.locked` hash covers (spoken-only via A1, not the whole ledger-bearing `narration.md`) so non-spoken edits don't spuriously stale the lock.
