# Independent review — cursor (OK, 72s)

# Adversarial review — Phase C fail-closed LOCK chokepoint

Skeptical read against the real repo. The artifact overstates what is enforced and understates bypasses. Several claims are **false on disk today**.

---

## 1. FALSE-PASS / bypass holes (highest priority)

### 1a. `narration-tagged.md` hash binding is broken on real folders

**Claim (artifact lines 20–21, `lock.py` lines 20–21, 42–46):**  
> "The `.locked` hash binds `narration-tagged.md` when present (what synth actually consumes)"

**Reality:** All 8 Psalm 22 shorts already have `narration-tagged.md` in XML form (`<speaker name="narrator">…</speaker>`). `spoken_hash()` feeds that file to `NP.parse()`, which **only** parses `**[speaker]**` blocks (`narration_parse.py` lines 28–29, 104–124). XML tagged files yield `EmptyNarrationError`.

So on any folder with existing tagged audio artifacts:

- `write_lock()` → `spoken_hash()` → **crash** on successful `run_lock` (uncaught in `run_lock` ok-branch, lines 147–149)
- `is_locked()` → catches exception → returns `(False, "cannot hash spoken text: …")` (lines 67–70) → audio **blocked even after a valid lock attempt**

The repo already has a working tagged-md parser in `assembly_timing._parse_tagged_chunks` (XML regex, line 24). Phase C does not use it. **7/7 tests pass only because `_mk()` creates `narration.md` only — never the production XML tagged file.**

This is not a theoretical edge case; it is the current state of the hand-authored content this phase was built to protect.

### 1b. Split-brain: certify `narration.md`, bind/hash tagged (when it worked)

Even if tagged parsing were fixed, `run_lock()` runs KJV, Rule-8, and cluster on **`narration.md` only** (lines 123–126, 140), while `spoken_hash()` prefers **`narration-tagged.md`** (lines 42–46).

Attack / drift path:

1. `narration.md` passes KJV + cluster (panel-approved text).
2. Stale `narration-tagged.md` still carries old templated spoken text (Psalm 22 shorts already do).
3. Lock certifies md; hash binds tagged → **templated audio can render while md looks clean**, or lock/hash disagree.

`test_stale_lock_detected_on_edit` only mutates `narration.md` in an md-only temp dir (test lines 44–50). **No test** for md/tagged divergence or post-tag staleness.

### 1c. `_finalize.py` vs lock ordering is contradictory

`_finalize.py` (lines 26–29) **deletes** `narration-tagged.md` before `handoff.run_audio_pipeline()`.

If lock was taken while tagged existed (intended design), hash = tagged. After finalize deletes tagged, `require_lock()` hashes `narration.md` instead → **stale mismatch → audio refused**.

If lock was taken with tagged absent, finalize works once; tag stage then creates tagged; **any later `require_lock()` call breaks** (§1a).

The artifact never defines the required order: lock before tag? after tag? delete tagged before lock? It says both "binds tagged" and `_finalize` clears tagged.

### 1d. Enforcement inventory is one function wide — not fail-closed

**Claim (artifact line 7):**  
> "require_lock() is the guard wired into handoff.run_audio_pipeline so audio cannot render"

**Only caller:** `pipeline/handoff.py` lines 239–245. Nothing else in the repo calls `require_lock`.

**Un guarded entry points (confirmed in codebase):**

| Entry | Bypass |
|-------|--------|
| `pipeline/runner.py` line 145 | `enforce_lock=False` — engine + `orchestrator.start()` (`run_audio=True`, orchestrator line 278) |
| `runner.py` lines 149–157 | Logs **direct** `per_turn_synth.py` / `narration_pipeline.py` commands when audio skipped |
| `RESUME.md` / `longform/SOUNDSTAGE_SPEC.md` | Documented `--no-gate` on sibling `per_turn_synth` |
| Sibling synth (not edited) | Manifest-absent gate skip + `--no-gate` per prior panel reviews |
| `JITB_REQUIRE_LOCK=0` | `require_lock_enabled()` returns immediately (lock.py lines 37–38, 78–79) |
| `pipeline/orchestrator.py` `detect_position()` line 116 | Proceeds on `narration.mp3` existence — **no lock/hash check** |
| `cli_assemble.py` / `assembly_runner.py` line 120 | Consumes existing `narration.mp3` + `narration-tagged.md` — **no lock check** |
| `pipeline/assembly_align.py` | Aligns mp3 to tagged transcript — **no lock check** |
| `veed_io/caption.py` | Burns captions from video audio + optional script — **no lock check** |
| `music_library/placer.py` | Imports `veed_io.aligner` — **no lock check** |

Stale-mp3 survival: edit `narration.md` → lock goes stale (maybe) → `orchestrator --continue` / `cli_assemble` still assemble from old mp3. **Text gate does not gate the cut.**

The artifact does not mention this inventory. `PIPELINE_HARDENING_PLAN.md` required it; Phase C delivered only the handoff hook.

### 1e. `enforce_lock=False` is a real bypass, not a footnote

**Claim (artifact lines 8–9):** engine path exempted "pending narration-format reconciliation."

**Code:** `runner.py` line 145. `orchestrator.start()` always uses that path (line 278).

**Contradiction:** `lock.py` module docstring lines 5–6 says **"every narration — engine-generated or hand-authored"** must pass. Engine-generated shorts via `cli_pipeline.py` never hit `cli_lock` and never hit `require_lock`. For the org failure (templated cluster shipped), engine output is equally capable of clustering. This is not scoped honestly in the artifact.

### 1f. `--no-cluster` is an intentional cluster bypass

`cli_lock.py` line 28: `--no-cluster`. A templated Psalm 22 short that fails cluster with default flags could be locked by skipping cluster, if hash write succeeded. **No test** asserts `--no-cluster` cannot certify templated CTAs.

---

## 2. False assumptions / doc vs code

### 2a. "vs siblings + the catalogue" — catalogue not implemented

**Claim:** `lock.py` docstring line 10: cluster check vs "siblings + the catalogue."

**Code:** `run_lock()` lines 137–144 only gather `_sibling_folders()` (same parent dir). `register()` / `freshness_registry.json` is written but **never read** during `cluster_check()`. `cluster_gate.cluster_check(..., within_cluster=False)` exists for advisory cross-catalogue (cluster_gate.py lines 120–121) but is **never called** from lock.

A short duplicating a hook/CTA in another series under a different parent passes.

### 2b. `_anchor_findings` is a no-op

`lock.py` lines 107–110: `return []` always. Claim of "anchor-verse" check in `run_lock` docstring (lines 8–9) is **aspirational**, not enforced.

### 2c. "Non-bypassable" / "fail-closed" — not supportable

Residual bypasses are the default operational paths (`--no-gate`, direct synth, stale mp3 assembly, env override). Calling this fail-closed overclaims.

---

## 3. Registry rebuild — race and batch gaps

### 3a. Non-atomic registry write

`register()` (lines 165–170): `rebuild_registry()` → mutate → single `write_text`. Concurrent `cli_lock` on two folders: last writer wins; no file lock, no atomic rename. Low probability for one user, but not safe for batch locking.

### 3b. In-flight batch cluster — partial rewrite hole

Cluster compares **on-disk sibling `narration.md` files** (lines 138–140), not lock state. That correctly blocks the current templated Psalm 22 cluster (test passes).

**Gap:** Rewriting shorts 1–7 to unique CTAs, leaving 5–8 with old template — locking 5–8 still blocked. Good. But locking short 8 **after** 1–7 are unique and 8 alone still matches no sibling (min_share=2) → **short 8 can lock with a template CTA** if it no longer shares an n-gram with any *current* sibling text, even though the series still has a template pattern historically. Cluster is snapshot-only, not registry-backed.

### 3c. Registry scope

`rebuild_registry()` globs `longform/**/.locked` only (line 176). Engine output under `PythonProject1/jesus/narration/` never registers. Inconsistent with "every narration" rhetoric.

---

## 4. Verification gaps in tests

Tests (`test_lock.py`) cover: cluster block on real templated short, md-only clean lock, md-only stale, require_lock refuse, KJV misquote, Rule-8 short/long.

**Missing (any one would have caught §1a):**

- Lock/hash with existing XML `narration-tagged.md` (production shape)
- `narration.md` passes / `narration-tagged.md` diverges
- `_finalize` clear-tagged → `require_lock` integration
- `--no-cluster` cannot certify known templated fixture
- Downstream stale-mp3 refusal (assembly/orchestrator)
- Catalogue cross-series duplicate

**"7/7 + A/B green"** validates md-only happy paths, not the hand-authored Psalm 22 folders this phase targets.

---

## 5. Reuse / duplication

Porting cluster/KJV into `pipeline/` is consistent with the hardening plan. **Bug is the opposite of duplication:** `assembly_timing` already parses tagged-md for synth/assembly; `lock.spoken_hash` reimplements binding via the wrong parser instead of reusing `_parse_tagged_chunks`.

---

## 6. Cost / spend

Phase C itself is cheap (deterministic checks). **Cost of a false PASS is high** — unchanged ability to ship templated cluster audio via direct synth, stale mp3 assembly, or engine path. Spend justification holds only if the chokepoint actually binds what renders; today it does not on existing tagged folders.

---

## Go / no-go

**NO-GO** for production enforcement on hand-authored Psalm 22 shorts (and any folder with XML `narration-tagged.md`).

The cluster block on templated md is real and valuable, but the enforcement chain (hash → guard → render) is **not coherent** with how synth actually consumes files, and the guard is trivially bypassed outside `handoff.run_audio_pipeline(enforce_lock=True)`.

Acceptable as **Phase C skeleton** only after: unified transcript source, tagged-md parser reuse, enforcement inventory, and honest scoping of engine/direct-synth bypasses.

---

VERDICT: FAIL
TOP FIXES:
1. **Unify certify + hash + synth on one transcript path** — reuse `assembly_timing._parse_tagged_chunks` for tagged-md (or always hash post-tag canonical text); run KJV/cluster on that same spoken string; add integration test with real XML `narration-tagged.md` and md/tagged divergence.
2. **Complete the enforcement inventory** — at minimum: `orchestrator`/`cli_assemble`/`assembly_align` must refuse stale mp3 when `.locked` missing or hash mismatches; document and gate `JITB_REQUIRE_LOCK=0`, direct `per_turn_synth --no-gate`, and remove or justify `enforce_lock=False` on the default `cli_pipeline` start path.
3. **Fix workflow + catalogue honesty** — define lock-after-tag (or delete-tagged-before-lock) to match `_finalize`; implement catalogue cluster via `freshness_registry` or drop the claim; add `--no-cluster` to blocking findings for templated fixtures or remove the flag.
