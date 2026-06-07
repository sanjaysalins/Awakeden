# Independent review — cursor (OK, 74s)

## Independent adversarial review — PLAN v3

v3 genuinely closes most v2 *architecture* gaps (lock chokepoint concept, scoped canon, whitelist rule, honest A3, inert calibration). It is **not** yet safe to implement as written. Several execution specs would stall the build, false-pass on real content, or leave bypass holes the plan claims to eliminate.

---

### v2 gap closure — lock chokepoint

**Partially closed, not proven closed.**

The keystone design ("`cli_lock.py` → `.locked` token → downstream abort") at lines 38–48 is the right fix for the org failure at line 26 ("no lock step forces hand-authored content through any check"). But enforcement is underspecified and incomplete against the real repo:

1. **Bypass paths not enumerated.** The plan names `per_turn_synth` / `_finalize.py` (line 47). It does **not** name:
   - `pipeline/runner.py` lines 136–143, which call `handoff.run_audio_pipeline(folder)` directly when `run_audio=True` — the engine-generated path never touches `_finalize.py`.
   - `_fix26_audio.py`, which also calls `handoff.run_audio_pipeline` directly.
   - Direct invocation of `PER_TURN_SYNTH_SCRIPT` (documented in `runner.py` lines 147–155 when audio is skipped).

   Without a single inventory of **every** audio entrypoint, "non-bypassable" is aspirational.

2. **Cross-repo dependency hidden.** `PER_TURN_SYNTH_SCRIPT` resolves to `PythonProject1/jesus/narration/per_turn_synth.py` (`config.py` lines 141–147). The plan modifies that external script but "Deliberately NOT doing" (line 155) only lists not *duplicating* it. No mention of coordinating changes across repos, versioning, or what happens if someone runs an unpatched `per_turn_synth.py`.

3. **Phased rollout contradicts the chokepoint spec.** Sequencing (line 148): "A3 must pass before B/C." But `cli_lock.py` step 1 (line 43) already runs "KJV ref-mapped span check" — that is Phase B4. Either the skeleton lock runs without KJV (not stated), or you build B before the sequencing says you should. Pick one; the plan has both.

4. **`.locked` stale semantics undefined.** Line 45 says "commit-ish of the narration text" but does not define: hash of `narration.md` only vs including `narration-tagged.md`, whether re-tag invalidates lock, or whether existing LOCKED folders with pre-built MP3s get grandfathered.

5. **Proof obligation is right but downstream of a chicken-and-egg.** Line 48: prove 8 shorts + 2 long-forms flow through `cli_lock.py`. Those 8 shorts **cannot** pass cluster lock today (8× "Come to Him"). Re-verification section (lines 129–134) acknowledges de-templating first — but C2 line 114 says "**Backfill** the 8 shorts + 2 long-forms via the chokepoint **now**," which contradicts backfill-before-rewrite unless "now" means after re-verification step 2. Sloppy sequencing language will cause someone to try backfill on templated content and hit a wall.

**Verdict on lock chokepoint:** Design closes the v2 *conceptual* gap. Enforcement contract does not yet close the v2 *execution* gap.

---

### v2 gap closure — scoped canon (B2–B4)

**Substantially closed.** Moving from full-Bible witnessing (v1) to "ONLY the refs actually quoted" (lines 90–95) is the correct scope cut and matches repo scale (~76 shorts). B3 fail-closed "bible-api is not a fallback for lock" (line 98) directly fixes the Ps 22:7 self-validation loop described at line 27.

**Remaining holes:**

1. **B2 names no dataset.** Line 94: "one named, vetted public-domain Cambridge-1769 structured dataset" — which file? Which URL/commit? Without a pin, B2 is not implementable; someone will grab bible-api again or a mismatched 1769 edition.

2. **`_audit_kjv_cache.py` does not exist** (line 88). Fine as new code, but B1 is listed as step 1 of re-verification (line 130) before the tool is built — ordering assumes the script exists.

3. **B4 vs current LOCKED content — acceptance test may false-fail or false-pass.** A1 line 66: "every KJV quote … successfully ref-mapped (unmapped span = test failure)." Real files violate a naive reading:
   - `#01` line 42: inline `"that the scripture might be fulfilled"` in an untagged `**[narrator]**` block — no ref tag.
   - `#02` line 55: inline `"Let him deliver him,"` in untagged narrator prose — partial echo, not block-mapped.

   Either the acceptance test must define **only KJV-tagged-block quotes** as in-scope, or the 8 shorts fail A1 on day one. The plan does not specify this boundary. That is a verification gap, not a minor wording issue.

4. **Interior punctuation vs author override.** `#02` DEPTH section (lines 64–68) documents intentional comma against corrupt cache. B4 line 103: "Interior punctuation must match." Good — but the plan does not say whether witnessed store follows **authoritative 1769** or **cache repair list from B1**. Those can diverge on edge cases beyond Ps 22:7.

5. **Italics / LXX.** B4 line 103 handles italics as "documented" — still a hand-wave. Hebrews 2:11 / Ps 22:22 divergence is why `#04` avoids re-quoting Heb 2:12; range-ref join across `Psalm 22:7-8` (`#02` line 42) is specified but not test-fixtured.

**Verdict on scoped canon:** Architecture closes v2. Implementation contract still missing dataset pin + quote-scope definition.

---

### A1 / parser / veed_io (v2 fix #6)

v3 adds "Retire `veed_io/_extract_spoken.py`" (line 65) — good, v2 gap closed **on paper**.

**New/adversarial findings:**

1. **`_extract_spoken.py` is not what captioning uses today.** Grep shows zero Python imports of `_extract_spoken`. The live caption path is `veed_io/caption.py` `load_script_text()` (lines 42–52), which:
   - Does not strip content after `---` / `## DEPTH & SOURCING` — only removes `#` heading *lines*, not section bodies.
   - Would feed ledger prose into alignment for shorts.

   Deleting `_extract_spoken.py` alone does not unify spoken-text sources. Line 65 must explicitly replace `caption.load_script_text` (and any aligner callers), not just the dead CLI script.

2. **Fail-closed on zero blocks (line 64)** is correct for verification. Caption pipeline currently has no equivalent guard — plan mentions caption revalidation (line 134) but not wiring caption to the same fail-closed parser before that step.

---

### A2 cluster gate (v2 fixes #4, #5, #8)

**CTA/hook whitelist rule (lines 73–74)** correctly closes the v2 self-nullification risk. Honest A3 wording (lines 80–81) matches files: all 8 end with "Come to Him" family; "thousand years" appears in `#01/#02/#03/#05/#08` opening hooks, `#07` has "a thousand years before Rome," while `#04/#06` do not — plan no longer overclaims 6/8. Good.

**Still broken or underspecified:**

1. **`--type cluster` does not exist.** `independent_review.py` line 158: `choices=["narration", "plan"]` only. Line 76's "blocking" cluster verdict has no merge logic, exit codes, or spec for how `cli_lock.py` invokes it and parses `INDEX.md`. v2 gap #8 is **not** closed in the artifact — it is a to-do dressed as done.

2. **`independent_review.py` always exits 0** (line 207) even when reviewers fail. "Per-provider failure … tolerated as long as ≥3 reviewers return" (line 76) needs explicit: minimum PASS count, what happens on 2× REVISE + 3× PASS, whether grok FAIL counts as "returned."

3. **Catalogue discovery scope.** Line 74: `data/catalogue_index.json`, auto-built by globbing narration folders. Psalm 22 shorts live under `longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/`, **not** `NARRATION_TREE_DIR` (`config.py` → PythonProject1 tree). If the glob only hits engine output folders, cluster checks never see the actual failure case.

4. **Bridge templating un gated.** Line 71 extracts "bridges" but A3 hard-requires only CTA + thousand-years family. `#03` line 46: "bring you home"; `#07` line 49: same bridge. A2 may catch via near-duplicate layer, but A3 does not require it — secondary templating can ship after CTA de-templating.

5. **CTA normalization not specified.** `#02` line 58: `"That's Jesus — come to Him."` (em dash, lowercase "come"). `#03` line 46: `"That's Jesus. Come to Him."` Exact match without normalization rules will miss variants or over-flag. Line 72 says "exact + normalized" but does not define normalization (case? strip tag prefix? treat "Come to Him and drink" in `#08` body as CTA-adjacent?).

---

### C1 verify CLI / Rule-8 / lecture-phrasing

**One verify CLI (line 110)** closes v2 duplication concern.

**Gaps:**

1. **`lecture-phrasing` has no importable banned list.** `defect_classes.json` line 14 says "G8(2) + banned phrase list" but phrases live only in `engine.py` prompt strings (lines 266, 491, 679). C1 line 111 "reuse the existing … list — do not re-invent" points to nothing extractable. High risk of either re-invention or mislabeling an LLM check as deterministic.

2. **Rule-8 and anchor-verse are still `status: none`** in `defect_classes.json` (lines 8–9). C1 claims they run deterministically. Correct direction, but the plan treats unbuilt checks as done.

3. **`anchor-verse-quoted` from "narration's own header tag"** (line 111). Short `#01` has no clean `primary_ref` field in front matter — spine is in prose bullets, not a parseable header tag. Resolution rules for hand-authored metadata are missing.

---

### C2 ledger / calibration (v2 fix #7)

**Honestly stating inert loop (lines 116–117)** closes v2 — verified: `append_record` has zero callers; `panel_misses` is read-only in `learning.py` line 56.

**Ledger append at lock (line 114)** closes the "where does append happen" gap — good.

---

### Reuse / over-engineering / cost

**Reuse:** Correctly consolidates into `verify_narration.py` + extends `kjv_check` (line 111). Does not duplicate audio/Kling pipelines (line 155). Good.

**Over-engineering:** Still building a multi-phase platform (parser, lock CLI, verify CLI, witnessed store, ledger, cluster LLM mode, regression tests) before A3 proves the cheap deterministic catch — but sequencing line 148 does put A3 first, which mitigates if actually followed. Risk is building the chokepoint skeleton with B4 wired in before A3 passes.

**Cost:** Lines 129–134 and 144–145 honestly state rewrite + re-panel cost. Credible.

---

### Go / no-go

**No-go on implement-as-is → REVISE once more, then build.**

Architecture is converged; execution contract is not. The two root causes (lines 30–32) are addressed in design but would still leak through bypass paths, catalogue blind spots, A1 acceptance ambiguity, and unbuilt cluster CLI blocking.

If forced to prioritize: fix lock enforcement inventory + catalogue glob scope + A1 quote-scope definition + cluster CLI contract before writing code.

---

VERDICT: REVISE
TOP FIXES:
1. **Lock enforcement inventory:** Enumerate every audio/lock entrypoint (`runner.py`, `_finalize.py`, `_fix26_audio.py`, direct `per_turn_synth`, cross-repo script) and specify exact `.locked` check + hash contract; resolve chokepoint step 1 vs "A3 before B/C" phasing so skeleton lock does not require B4 prematurely.
2. **Catalogue + A1 acceptance boundaries:** Define `catalogue_index.json` glob to include `longform/**/narration.md` (not just `NARRATION_TREE_DIR`); define whether A1 ref-mapping applies only to `**[speaker — KJV, ref]**` block quotes vs all double-quoted spans — current 8 LOCKED shorts fail a naive "every span" rule (`#01` inline John phrase, `#02` partial taunt).
3. **`--type cluster` blocking contract:** Add `LENS_CLUSTER`, manifest input, merged verdict exit codes, and how `cli_lock.py` invokes/parses it; explicitly rewire `veed_io/caption.py` (not just delete unused `_extract_spoken.py`) to `narration_parse`; pin the B2 Cambridge-1769 dataset source in the plan text.
