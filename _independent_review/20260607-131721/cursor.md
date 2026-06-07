# Independent review — cursor (OK, 85s)

## Independent adversarial review — PLAN v4 (REUSE-FIRST)

v4 is a real improvement over v1–v3: the reuse discovery is accurate, the two root causes are correctly named, and several prior panel gaps are explicitly closed. It is **not** safe to build as written. The architecture points the right way; execution still has bypass holes, ambiguous cluster semantics, and new fork-drift risk from the port.

---

### What the plan gets right (verified against repo)

**Root cause #1 is real.** `gate_g7_freshness` in sibling `short_gate/gates.py` fingerprints the whole landing beat (`landing_fingerprint` = last 8 words), landing matches are `blocking=False` (`conditional`), and it keys on `thread_slug` not hook opener. The Psalm 22 cluster was never gated: `per_turn_synth.py` skips gate when `episode.manifest.json` is absent (lines 191–203), which these hand-authored folders lack.

**Root cause #2 is real.** `data/kjv_cache.json` has Ps 22:7 without the comma; `short_gate/kjv.py` `norm()` strips all punctuation (line 74: `re.sub(r"[^A-Za-z0-9'\s]", " ", text)`), so even the HF-POC corpus would not catch the comma miss. Short #02’s narration actually has the comma — authors trusted the corrupt cache in DEPTH notes, not the spoken text.

**A1 problem is verified.** `veed_io/_extract_spoken.py` is MOVEMENT-only (lines 20–24); shorts use `**[narrator]**` blocks with no `## MOVEMENT` → empty spoken text. `veed_io/caption.py` `load_script_text()` does a separate coarse strip (lines 42–52), not A1.

**v4 closes some v3 gaps honestly.** Naming `handoff.run_audio_pipeline` as canonical guard (not foreign `per_turn_synth`), hashing A1-parsed spoken text (not raw md), stating calibration is inert, and scoping KJV witness are all correct moves.

---

### Critical findings

#### 1. “Non-bypassable lock chokepoint” is still overstated

The plan claims enforcement at `handoff.run_audio_pipeline` plus veed_io, with foreign-script bypass “documented, discouraged.”

```37:37:PIPELINE_HARDENING_PLAN.md
- **Enforcement inventory (every audio/caption entrypoint must check `.locked`):** `handoff.run_audio_pipeline` ...
```

**Problem:** `handoff.run_audio_pipeline` today has **zero** `.locked` check — it runs verify→tag→audit→synth unconditionally (`pipeline/handoff.py` lines 251–269). And `per_turn_synth.py` only enforces `validate_gate_stamp` when `episode.manifest.json` exists; otherwise it prints `[gate] skip` and proceeds. Psalm 22 shorts have no manifest → **current audio already bypasses all gates**.

Residual bypasses the plan does not close:
- Direct `per_turn_synth.py --no-gate` (explicit flag exists)
- `narration_pipeline.py --no-gate`
- `pipeline/runner.py` line 143 and `_fix26_audio.py` call `handoff` but nothing stops a user from invoking synth directly afterward
- **`cli_visual.py` / `visual_runner` / assembly** — no `.locked` requirement anywhere; you can spend on images/Kling/assembly on unverified text

“Declared sole sanctioned entry” is policy, not enforcement. The keystone does not yet exist in code, and the inventory is incomplete.

#### 2. Registry rebuild vs cluster detection — ambiguous, can false-pass

A2 says two things that conflict unless wired explicitly:

```54:56:PIPELINE_HARDENING_PLAN.md
- Port ... **Single source of truth:** rebuild the registry from on-disk `.locked` folders at check time
- **Scope:** within-series AND across-catalogue, via a manifest auto-built by globbing **both** `longform/**/v1/**/narration.md` ... and `NARRATION_TREE_DIR`
```

The ported `gate_g7_freshness` only compares against **registry entries**, not a live manifest scan. Rebuild-from-`.locked` is good for phantom-entry hygiene, but:

- **Unlocked siblings with identical CTAs are invisible** until the first one locks. Locking short #03 before #01 passes with an empty registry even though #01 sits on disk with the same CTA.
- **A3 acceptance** (“must flag 8/8 `come to him` on the real shorts”) requires **cluster/set mode** that reads all peers from the manifest, not registry-only.
- The plan never states that `cli_lock.py`’s per-artifact freshness check **must also scan unlocked manifest peers in the same series/cluster**, not only `.locked` registry rows.

Sequential backfill after rewrite partially mitigates this, but it does not close the org failure (“nobody checked the SET before lock”) for folders that coexist unlocked.

#### 3. CTA blocking design may fight locked doctrine and over-block

```56:57:PIPELINE_HARDENING_PLAN.md
- add `cta_fingerprint` (last sentence/clause, **normalized substring** — so `come to him` matches across ...)
- **CTA/opener repetition is BLOCKING**
```

And C3:

```91:91:PIPELINE_HARDENING_PLAN.md
A synthetic 9th short ending "Come to Him" **MUST FAIL** `cli_lock.py` within-series AND cross-series.
```

This is internally consistent but operationally harsh. CTA-to-Jesus is **locked project doctrine** (CLAUDE.md). A normalized substring match with **no whitelist** and **cross-catalogue scope** means the second short in the entire catalogue whose CTA contains “come to him” fails — even with different surrounding landing work.

That catches Psalm 22 8/8 templating (verified: all 8 shorts end with “Come to Him” / “come to him”). It also guarantees perpetual paraphrase churn for orthodox invitations. The plan does not define:
- `freshness_window` (ported G7 defaults to last N episodes — unspecified in v4)
- Whether blocking is **within-series only** vs catalogue-wide for per-artifact lock
- How `#02`’s “That’s Jesus — come to him.” interacts with mid-body “all who come to Him” in #04 (substring collision outside CTA clause)

A3 proves the catch; it does not prove the gate is **safe for normal production volume** (~76 shorts + long-forms).

#### 4. Opener detection: honest acceptance, undefined blocking rule

A3 honestly says “thousand years” is not 6/8 (#04/#06 don’t open with it). Good.

But A2 also says `opener_family` repetition is **BLOCKING** with no threshold: 2-of-8? 3-of-8? within-series only? “anywhere in the opening block” is vague for shorts where the hook spans multiple `**[narrator]**` blocks. Five shorts open with “a thousand years” variants; the plan never says whether that blocks lock or only flags cluster review.

#### 5. Templating detector is narrower than the actual cluster failure

The cluster shipped with more than CTA + opener repetition:
- **“bring you home”** bridge in #03, #05, #07 (verified in repo)
- **“That’s Jesus”** tag in #03, #02
- Shared conviction-bridge patterns

A2/A3 target only `come to him` + `thousand years`. Fixing those two does not prove the SET is de-templated — only that two fingerprints were caught. Root cause #1 (“collectively templated”) is only **partially** addressed.

#### 6. Root cause #2 fixed at lock time only — upstream authoring still corrupt

B2–B3 fix verification at `cli_lock.py`. **`pipeline/scripture.py` `fetch_kjv()` still reads/writes `kjv_cache.json` via bible-api.com** (lines 36–69). Authors continue to “self-verify” against the corrupt cache during writing (short #01 DEPTH: “self-verified via `pipeline/scripture.fetch_kjv`”). Lock-time strict check does not stop wrong cache from misleading authors **before** lock. The plan does not say to redirect `fetch_kjv` / retire `kjv_cache.json` for authoring lookups.

#### 7. Port ≠ no duplication — it creates a fork with drift risk

“Do NOT edit sibling-repo `short_gate` … Port the proven logic into `pipeline/`” avoids sibling-repo edits but **creates a second copy** of `kjv.py`, `gates.py` registry logic, ref parsing, etc. `short_gate` already has `test_gates.py`; v4 does not require port parity tests against the sibling originals.

Worse: two stamp systems will coexist:
- Sibling: `narration.gate.json` + `validate_gate_stamp` (hashes raw narration via `resolve_narration_sources`)
- v4: `.locked` hashing A1 spoken text

Engine-generated episodes using `short_gate` stamps won’t interoperate with JesusInTheBible `.locked` without a migration story. “Reuse-first” is correct tactically; “avoids duplication” is false.

**Alternative not considered:** import `short_gate` as a library + thin adapter for manifest-less hand-authored folders (auto-build manifest from glob), extending in one place. v4 chose port for control, but should own the fork-maintenance cost explicitly.

#### 8. `.locked` hash vs what downstream actually consumes

Plan: hash is **A1-parsed spoken text from `narration.md`**.

Downstream reality:
- `per_turn_synth.py` reads **`narration-tagged.md`** exclusively (line 184)
- `assembly_timing.py` / `assembly_align.py` require `narration-tagged.md`
- `veed_io/caption.py` reads script path via `load_script_text()` — third parser

`_finalize.py` deletes stale `narration-tagged.md` before re-synth (good), but the plan does not require lock to verify **tag-stage output matches A1 spoken hash**. A hand-edit to `narration-tagged.md` after lock bypasses the hash while synth/captions/assembly follow the tagged file.

#### 9. veed_io rewire is underspecified

```50:50:PIPELINE_HARDENING_PLAN.md
- **veed_io decoupling (gemini):** do NOT import `pipeline` into `veed_io`. `pipeline` parses and passes **plain spoken strings** down to `veed_io`
```

Good direction, but no caller inventory:
- `python -m veed_io.caption --script <path>` CLI still calls `load_script_text(path)` directly
- `music_library/placer.py` imports `veed_io.aligner` with audio paths, not pre-parsed strings
- Long-form timing workflows in `veed_io/RESUME_veed_io.md` reference `_extract_spoken.py` CLI

“Retire `_extract_spoken.py`” alone does not unify spoken-text sources. Three parsers can still diverge: A1, `caption.load_script_text`, tagged-md turn parser.

#### 10. Sequencing contradiction — chokepoint before KJV strict exists

```119:119:PIPELINE_HARDENING_PLAN.md
Chokepoint skeleton + **A** ... → prove A3 on the real 8 → **B** ... → **C**
```

But `cli_lock.py` is defined from the start as running “KJV strict, Rule-8, anchor-verse” (line 36), and B3 (punctuation-strict ref-mapped check) is Phase B. A “chokepoint skeleton” that can write `.locked` before B exists is a **false lock** risk — exactly the failure mode this plan is trying to eliminate.

Rule-8 and anchor-verse are still `status: "none"` in `defect_classes.json`; C1 treats them as done.

#### 11. `independent_review.py --type cluster` — unspecified contract

Line 26: add `--type cluster` + `LENS_CLUSTER`. Today only `narration` and `plan` exist (`independent_review.py` line 158). Missing from v4:
- Input format (folder list? manifest JSON?)
- How concatenated spoken-only text is built (must use A1, not raw md)
- Exit-code mapping into `cli_lock.py` blocking behavior
- Whether cluster LLM review is required per lock or only batch QA

Using LLM as backstop for a deterministic miss is fine; making it blocking without a spec is a single point of flaky failure.

#### 12. `cli_witness_verse.py` cold-start friction

B2 spot-checks “used + known-hard verses”; B3 blocks unwitnessed refs. No witness registry format, no bootstrap for the HF-POC corpus copy (thousands of verses), no definition of what “witnessed” means in machine-readable form. First quote of an unspot-checked verse blocks lock until manual CLI run — workable but unbudgeted.

#### 13. Cost honesty is good; scope of re-verification is still underestimated

Re-verification (Phase D) requires rewriting 8 LOCKED shorts + **re-panel each** + audio re-render. Plan states this honestly. It understates **visual/assembly rework** if text changes post-image-plan: scene plans, PNGs, Kling clips, edit plans may stale. No mention of invalidating downstream visual artifacts when narration text changes.

---

### Does porting avoid duplication concerns?

**Partially.** It avoids editing `PythonProject1` and reuses proven algorithms. It does **not** avoid duplication — it **forks** them. Without parity tests and a sync policy, you trade sibling-repo edit risk for silent drift between two gate implementations (`narration.gate.json` vs `.locked`).

---

### Does punctuation-strict + blocking-CTA + rebuild-from-disk close the two root causes?

| Root cause | Closed? | Gap |
|---|---|---|
| #1 No set-level check before lock | **Partially** | A3/cluster mode catches Psalm 22; per-artifact `cli_lock` registry-only can miss unlocked peers; opener/bridge templating incomplete; bypass paths remain |
| #2 Scripture from corrupt cache | **Partially** | B3 at lock with HF-POC corpus + punctuation-strict fixes forward verification; `fetch_kjv`/`kjv_cache.json` authoring path untouched |

---

### New risks introduced by the port

1. **Dual gate ecosystems** — `short_gate` stamps vs `.locked` stamps; engine shorts vs hand-authored longform shorts behave differently.
2. **Fork drift** — bugfixes in sibling `short_gate` won’t flow to `pipeline/freshness.py` / ported `kjv` logic.
3. **CTA substring brittleness** — false blocks on legitimate repeated gospel invitations; false passes if author paraphrases CTA (“turn to Him”, “come to Christ”) while keeping identical hook/bridge templates.
4. **False-lock window** — chokepoint skeleton writable before B3/KJV strict is real.
5. **Parser trifurcation** — A1 + caption + tagged-md paths unless veed_io rewire is fully inventoried.

---

### Go / no-go

**NO-GO for implementation as written.** **GO for direction** — reuse-first, A1 fail-closed, HF-POC corpus, punctuation-strict mode, cluster acceptance on real Psalm 22 set, honest about inert calibration.

Implement after REVISE on: enforcement inventory (real bypass closure), cluster-vs-registry comparison semantics, hash/tag round-trip, upstream `fetch_kjv` redirect, opener/CTA threshold rules, and phased lock capability (no `.locked` until B3 is live).

---

VERDICT: REVISE
TOP FIXES:
1. **Define and enforce cluster comparison semantics:** `cli_lock.py` must scan manifest peers (same series + catalogue, including unlocked folders) for CTA/opener blocking — not registry-only; specify exact match thresholds for `opener_family`; add “bring you home” / conviction-bridge fingerprints or accept partial templating coverage.
2. **Close real bypass holes with an enumerated enforcement inventory:** implement `.locked` + hash check in `handoff.run_audio_pipeline` first; list and guard every audio/caption/align entry (`runner.py`, `_finalize.py`, `_fix26_audio.py`, `veed_io.caption` CLI, `music_library/placer.py`, assembly align/timing); state what happens to existing MP3s without `.locked`; defer “non-bypassable” claim until `per_turn_synth --no-gate` path is addressed or explicitly accepted.
3. **Bind lock hash to synth/caption reality and fix upstream cache:** verify `narration-tagged.md` spoken content matches A1 hash at lock (or hash post-tag output); retire or redirect `pipeline/scripture.fetch_kjv` away from `kjv_cache.json`; forbid writing `.locked` until B3 punctuation-strict is live (no chokepoint skeleton that false-locks).
