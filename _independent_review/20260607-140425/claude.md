# Independent review — claude (OK, 129s)

Verified against the live repo. Findings below cite exact lines.

## Critical — FALSE-PASS (split-brain confirmed LIVE, not theoretical)

**1. The lock checks `narration.md` but binds + renders `narration-tagged.md`.**
- `run_lock` reads `narration.md` for *every* check — KJV, Rule-8, cluster (`lock.py:123-126`, `130`, `133`, `140`).
- `spoken_hash` / `write_lock` prefer `narration-tagged.md` (`lock.py:43`, `54-56`, `154-156`), and synth consumes `narration-tagged.md`.
- I confirmed **every real folder already has both files** (`narration-tagged.md` exists in all 8 Psalm 22 shorts + both long-forms). So in production the gate validates one file and certifies/renders a *different* file. The two are produced by separate steps with **zero consistency guarantee**. A clean `narration.md` + a templated/misquoted `narration-tagged.md` → **LOCKS and renders the bad text.** The docstring's central claim — "*hash of the SPOKEN text actually rendered*" (`lock.py:11`, `20-21`) — is false whenever tagged ≠ source, which is the normal case.
- **The 7/7 tests never exercise this.** `_mk` writes only `narration.md` (no tagged file), so the live condition is untested — "7/7 green" is false confidence.

## Critical — bypasses (the chokepoint isn't a chokepoint)

**2. The guard sits on one Python wrapper, not on the synth.** `require_lock` is only called inside `handoff.run_audio_pipeline` (`handoff.py` excerpt). The actual renderer `per_turn_synth.py` is unguarded — and CLAUDE.md *documents* running it directly (`per_turn_synth.py --target 59 ...`). Any direct/subprocess synth call, or `veed_io/caption.py` (renders Scripture onto the final clip — **no `require_lock` anywhere in it**, confirmed), ships final content with no lock. The longform soundstage consumes a pre-existing `narration.mp3` (`_soundstage_cinematic.py:164`) — once audio exists, nothing re-gates it. The already-rendered templated Psalm 22 mp3s (commit 104bd0b) sail straight through.

**3. The engine path — the highest-volume producer — is exempt.** `runner.py` passes `enforce_lock=False`. The docstring says "*every narration — engine-generated or hand-authored ... must pass*" (`lock.py:4-6`); the code exempts exactly the engine. This is a direct contradiction of the stated goal, self-labeled a "documented follow-up." Plus `JITB_REQUIRE_LOCK=0` disables it globally (`lock.py:37-38`). Enforcement is soft on every axis.

## Overclaims (docstring promises code doesn't keep)

**4. "anchor-verse" check is a no-op.** `_anchor_findings` returns `[]` unconditionally (`lock.py:107-110`). Docstring line 8-9 claims it. A short that never quotes its primary verse locks clean.

**5. "the catalogue" comparison doesn't exist.** Docstring line 10 says siblings *+ the catalogue*. `run_lock` compares only `folder.parent.iterdir()` siblings (`lock.py:113-118`). A hook/CTA duplicated across *different* clusters (Psalm 22 vs Isaiah 53) is never caught — the exact cross-artifact failure this is supposed to prevent.

## Registry / race

**6. Cluster check is point-in-time, not transactive.** Locking short A compares A against siblings' *current* `narration.md` (`lock.py:140`). If B is later edited to share a phrase and re-locked, A is never re-evaluated (A's text unchanged → not stale → stays locked). Two shorts can both end up locked sharing a phrase. `rebuild_registry` only globs `longform/**/.locked` (`lock.py:176`) — anything outside `longform/` is invisible.

**7. `.locked` is forgeable** — plain JSON written by the same process, hash self-computed (`lock.py:154-158`). Any script can write a valid token. It's an advisory marker, not a binding certificate.

## What does hold
- `_fix26_audio.py` calls `run_audio_pipeline(folder)` with the default `enforce_lock=True` → genuinely enforced (one real win).
- `is_locked` fail-closes on hash/parse errors (`lock.py:69-72`), and `run_lock` doesn't write `.locked` on failure. No false-*block* found; staleness-on-edit works for the source file.

The core defect is structural: **what is checked ≠ what is bound ≠ what is rendered**, the guard is on a bypassable wrapper, and the primary producer is exempted. The motivating failure (templated cluster) can still ship through at least four paths.

VERDICT: FAIL
TOP FIXES:
1. Close the split-brain: run KJV/Rule-8/cluster against the SAME file you hash and synth (`narration-tagged.md` when present), or fail-closed if tagged ≠ source. Add a test with both files present and differing.
2. Move enforcement to the real chokepoint — gate inside the synth path (and `veed_io/caption.py`), not just `run_audio_pipeline` — and remove the `enforce_lock=False` engine exemption (or reconcile the format now, since the engine is the main producer).
3. Make the docstring match the code: implement the anchor-verse check and catalogue-wide (not sibling-only) cluster comparison, or delete those claims; make cluster locking re-validate prior locks when a sibling changes.
