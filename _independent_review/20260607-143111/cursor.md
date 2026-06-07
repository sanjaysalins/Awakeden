# Independent review — cursor (OK, 76s)

## Adversarial review — Phase C v2

### v1 FAIL findings: status

| v1 defect | Closed? | Evidence |
|-----------|---------|----------|
| Crash on real XML `narration-tagged.md` | **Yes** | `narration_parse.py` lines 108–112 route `<speaker>` XML; real Psalm 22 tagged files are single-block XML; `test_real_xml_tagged_file_locks_and_hashes` passes. |
| Split-brain (verify `.md`, hash `-tagged.md`) | **Partially** | Parity at `run_lock` + `is_locked` when **both** files exist (`lock.py` 68–81, 164–167). **Fail-open** when tagged is absent (see below). |
| Punctuation-blind hash | **Yes** | `_canon_spoken` uses `kjv_strict._canon` (preserves punctuation); `test_punctuation_edit_busts_lock` passes. |
| Single-door guard | **Partially** | `assembly_runner.run_assembly` + `cli_assemble` + `handoff.run_audio_pipeline(enforce_lock=True)` guarded. Several doors still open (see below). |

The four v1 *mechanisms* are fixed in code. The stated *goal* (“fail-closed chokepoint every narration must pass”) is not met.

---

### Critical findings (new / residual bypasses)

**1. Primary production path bypasses the lock entirely**

The artifact says engine generate is “EXEMPT … documented follow-up, NOT a silent bypass.” In code it is a hard bypass:

```143:145:pipeline/runner.py
        # engine path is exempt from the lock guard pending narration-format
        # reconciliation; hand-authored long/short content is enforced via cli_lock.
        code = handoff.run_audio_pipeline(folder, enforce_lock=False)
```

`cli_pipeline.py` → `orchestrator.start()` → `runner.create_narration(run_audio=True)` never calls `cli_lock`. Engine `narration.md` is plain prose (`handoff.py` line 105), so `run_lock` would fail `EmptyNarrationError` anyway. The Psalm 22 cluster failure mode (templated engine output → audio → cut) is **still reachable** on the default `cli_pipeline` path. Calling this “not a silent bypass” contradicts `lock.py` lines 4–6 (“every narration … must pass before … audio is rendered”).

**2. Parity is fail-open when only `narration.md` exists — plus tag-stage TOCTOU**

```72:74:pipeline/lock.py
    src, tagged = folder / "narration.md", folder / "narration-tagged.md"
    if not (src.is_file() and tagged.is_file()):
        return None
```

If tagged is missing at lock time, parity is skipped and `.locked` hashes `narration.md` (`_spoken_source` falls through). Then `handoff.run_audio_pipeline` checks lock **once at the top** (lines 239–245), **before** `verify → tag → audit → synth` (lines 263–281). Tag creates/rewrites `narration-tagged.md`; synth renders that file. No post-tag re-check.

This is the normal `_finalize.py` workflow: it deletes stale tagged/mp3 (`_finalize.py` lines 26–29), expects a prior `cli_lock`, then runs audio. Lock passes on md-only; rendered audio may diverge from what was certified. **No test covers this.**

**3. `_finalize.py` can deadlock against a tagged-based lock**

If a user locks while `narration-tagged.md` exists, `.locked` binds the **tagged** hash (`_spoken_source` prefers tagged). `_finalize` deletes tagged, then `require_lock` hashes **md only** → stale mismatch → audio refused. The plan does not document lock-then-finalize ordering. Operators will hit this.

**4. Enforcement inventory is still incomplete**

| Door | Guarded? |
|------|------------|
| `handoff.run_audio_pipeline` (default) | Yes |
| `handoff.run_audio_pipeline(enforce_lock=False)` | **No** — engine path |
| `runner.py` / `orchestrator.start` | **No** |
| `visual_runner.create_visuals` | **No** — spends on unlocked narration |
| `veed_io/caption.py` | **No** — final publish step unguarded |
| `assembly_align.align` | **No** — reuses stale `narration.mp3` |
| Direct sibling `per_turn_synth.py --no-gate` | **No** — documented residual, still operational |
| `JITB_REQUIRE_LOCK=0` | Disables **all** guards globally |
| `cli_lock.py --no-cluster` | Skips cluster check entirely |

The artifact claims “require_lock now guards run_audio_pipeline AND run_assembly” — true for those two wrappers, but false for the headline “every narration … must pass.”

**5. Docstring / plan overclaims vs implementation**

- `lock.py` line 10: “siblings **+ the catalogue**” — `run_lock` only scans `folder.parent.iterdir()` siblings (lines 141–146). `freshness_registry.json` is written, never read during `cluster_check`. Cross-series duplication (Psalm 22 vs Isaiah 53) is not caught.
- `lock.py` lines 8–9 / `_anchor_findings`: “anchor-verse” — function is `return []` (lines 135–138). Aspirational, not enforced.
- “fail-closed” — undermined by `JITB_REQUIRE_LOCK=0`, `--no-cluster`, engine exemption, and foreign synth bypass.

**6. XML parser: fixed for happy path, brittle at edges**

- Trigger is substring `if "<speaker" in md.lower()` (`narration_parse.py` line 108), not structural detection. Any `narration.md` containing that substring misroutes to XML parsing.
- Regex requires `name="..."` **double quotes** only (`line 92`). Single-quoted attributes won’t match.
- `re.DOTALL` + non-greedy `.*?` can mis-parse nested/malformed `</speaker>` — no test for adversarial XML.
- Text **outside** `<speaker>` tags is silently dropped from spoken extraction. If synth ever consumed it, parity wouldn’t see it. (Current real files are single-tag; risk is latent.)

**7. Cluster gate weakened by sibling skip**

```180:181:pipeline/lock.py
                except (OSError, NP.EmptyNarrationError):
                    cluster_skipped.append(s.name)  # one bad sibling must not crash the lock
```

A clean short can lock **without** cross-artifact scrutiny if siblings are unparseable. Only a warning in `cluster_skipped` — not blocking. Opposite of fail-closed for cluster detection.

**8. Registry can serve stale metadata**

`rebuild_registry()` (lines 218–231) indexes any on-disk `.locked` without re-running `is_locked()` hash/parity checks. Edited `narration.md` after lock can leave stale hook/cta in `freshness_registry.json`.

**9. Tests prove unit behaviors, not operational fail-closed**

13/13 passes regress v1 bugs (XML, parity mismatch, punctuation, assembly guard, templated cluster block). Missing:

- Engine `enforce_lock=False` / `cli_pipeline` start path  
- Md-only lock → tag → synth without re-verify  
- `_finalize` lock/hash ordering conflict  
- `JITB_REQUIRE_LOCK=0`, `--no-cluster`  
- Parity when tagged deleted between lock and `require_lock`  
- Visual/caption doors  
- Cross-catalogue duplication  

`test_assembly_allows_locked` catches any `BaseException` after the guard — weak signal that assembly actually proceeded.

---

### Feasibility / reuse / cost

- **Feasible** against the real codebase: modules exist, tests run, real XML shorts parse.
- **Reuse** is good: `narration_parse`, `kjv_strict`, `cluster_gate` — no duplication.
- **Cost justified** for cluster/KJV regression on hand-authored shorts. **Not justified** as “Phase C complete” while the default `cli_pipeline` engine path and several spend doors remain unguarded.

---

### Go / no-go on committing Phase C

**No-go** if the commit message or merge intent claims Phase C is complete or “fail-closed.”

**Conditional go** only as an honest incremental checkpoint: “v2 fixes v1 crash/split-brain/punctuation/assembly-door; enforcement inventory and engine path remain open.”

The v1 panel findings are genuinely closed **at the mechanism level**. The organizational failure mode (templated cluster → audio → cut on the default pipeline) is **not** closed because the highest-volume producer is exempt and never passes `run_lock`.

---

VERDICT: REVISE
TOP FIXES:
1. Guard the engine/`cli_pipeline` start path: either remove `enforce_lock=False` and normalize engine plain-prose `narration.md` into parseable speaker blocks before lock, or block audio until `cli_lock` passes — the exemption is a real bypass of the stated goal, not a footnote.
2. Close the tag-stage TOCTOU: re-run `is_locked()` (hash + parity) **after** the tag stage in `run_audio_pipeline`, and make parity blocking at lock time (refuse md-only lock when shorts mode will generate tagged).
3. Finish the enforcement inventory with tests: treat `JITB_REQUIRE_LOCK=0` and `--no-cluster` as dev-only (warn loudly / CI fail), add cross-catalogue cluster check, and either guard or explicitly accept visual/caption/direct-synth doors with regression tests for each.
