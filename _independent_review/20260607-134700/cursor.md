# Independent review — cursor (OK, 75s)

## Adversarial review — Phase B (`pipeline/kjv_strict.py`)

The Ps 22:7 comma regression is real and the reuse of `short_gate/kjv.py` for ref parsing is the right call. That does **not** make this lock-ready. Several concrete false-PASS paths remain, the inline path is deliberately weak, and the artifact overstates what is proven.

---

### Feasibility vs codebase / plan

**What exists and works**
- `pipeline/narration_parse.py` is present; `quoted_spans_with_refs` supplies the tagged/inline/rhetoric split Phase B expects.
- Sibling `short_gate/kjv.py` exists at the hardcoded path; `REF_RX`, `verses_for`, `resolve_book`, and `{note}` / `{italic}` handling are real.
- The flagship comma case is correctly exercised in tests.

**What the artifact assumes but is not in repo**
- B1 cites an audit on 10 narrations, but there is no `pipeline/_audit_kjv.py` (or other committed audit runner). The 54 OK / 1 WARN claim is not reproducible from this tree.
- `PIPELINE_HARDENING_PLAN.md` B2 (`data/kjv_corpus.json` pin + witness) is **not implemented**. Verification still follows `short_gate.resolve_kjv_path()` → live HF-POC file via `JESUS_KJV_CORPUS`. Same drift risk the plan explicitly warned about.
- Nothing wires `kjv_strict` into `cli_lock.py`, `handoff`, or `pipeline/kjv_check.py`. Drafting still hits `data/kjv_cache.json` via `pipeline/kjv_check.py` (punctuation-blind `_norm`). Phase B is an orphan module, not a gate.
- Implementation Contract §1 (“equivalence fixture vs source `check_quote`”) — **missing**. No test proves import-path reuse stays aligned with `short_gate`.

**Import fragility (line 57)**
```python
_SG, _SG_PATH = _load_sg_kjv()
```
- Eager import: `import pipeline.kjv_strict` fails at import time if the sibling path is absent — bad for CI/other machines.
- Line 37 hardcodes `C:\Users\sanjay\...` in source.
- If `kjv.py` loads but corpus is missing, `_SG.load_kjv_by_name()` **raises** (`kjv.py:62-65`) — not mapped to `UNRESOLVED` / `blocking`. `verify_narration` crashes instead of fail-closed reporting.

---

### FALSE-PASS holes (misquote slips through)

**1. Ellipsis fragments: no order constraint (`_fragments_in`, lines 111–118)**

Docstring says each fragment must be a contiguous substring; it does **not** require order or adjacency.

```python
for frag in re.split(r"…|\.\.\.", span):
    f = _canon(frag).strip(_TERMINAL)
    if f and f not in text:
        return False
```

Example against Ps 22:1:
- Quote: `"forsaken me … My God, my God"` → both fragments exist in the verse → **OK**, even though order is reversed and the middle is elided incorrectly.
- Same class of bug for range refs (`Psalm 22:6-7`): a scrambled multi-verse ellipsis can pass if each piece appears *somewhere* in the joined text.

This is exactly the `_fragments_in matching out of order` hole from the brief. Not tested.

**2. Prefix truncation hides dropped supplied-word italics (lines 71–76 vs 111–118)**

Corpus side strips `{saying}` → `saying`. Quote side is **never** passed through `_strip_markers`.

For Ps 22:7, canonical verse ends with `..., they shake the head, saying`.
- `"they shake the head, saying"` → OK (tested)
- `"they shake the head saying"` → MISQUOTE (tested — comma catch works)
- `"they shake the head,"` → **OK** — valid prefix substring; supplied word `saying` silently omitted
- `"they shake the head"` → **OK** — same, plus interior comma before `{saying}` dropped

Substring matching was chosen to allow honest truncation (`test_boundary_truncation_allowed`), but there is no distinction between “intentional clip” and “dropped supplied italic / interior comma before italic.” That undercuts the stated goal of keeping `{saying}` material for the comma case.

**3. `_TERMINAL` strip is boundary-only but enables junk first fragments (line 89, 115)**

`_TERMINAL = ' .!?"\'’"'` — comma and colon are **not** stripped (good for Ps 22:7). But leading strip on ellipsis fragments allows:
- Fragment `", saying"` → `"saying"` → passes if `saying` appears anywhere in verse.

That is acceptable for deliberate head/tail clips; combined with no order check, it widens the ellipsis hole.

**4. Inline resolution: wrong verse, same chapter (`resolve_inline`, lines 157–173)**

`resolve_inline` searches **whole concatenated chapters** from tagged refs, not verse-level attribution:

```python
text = _chapter_text(ref)
if text and _fragments_in(span, text):
    return ("OK", f"inline quote located verbatim in {ref.split(':')[0]} (cited chapter)")
```

A mis-attributed but verbatim phrase elsewhere in Ps 22 (or Heb 2) passes as OK. Example shape: inline echo matches v8 language while the narrator meant v22; chapter search does not care.

This is the “match a DIFFERENT verse in a cited chapter” hole from the brief — **by design advisory for WARN-only**, but when it returns OK it is a false attestation of “located verbatim in cited chapter,” not “correct verse.”

**5. Inline with empty `candidate_refs` (lines 188–197)**

If a narration has `inline_kjv` quotes but zero `tagged_kjv` blocks, `candidate_refs` is `[]`, every inline gets WARN, never MISQUOTE. Misquotes in untagged-only scripts are never blocking — plan allows this, but it is a verification blind spot not disclosed in the artifact header.

**6. Quote/corpus marker asymmetry (lines 71–76 vs 78–86)**

`_strip_markers` runs on corpus only. A span copied from a marked source containing `{saying}` or `{was}` will not match stripped corpus text → false MISQUOTE on tagged blocks (less common, but real).

---

### FALSE-BLOCK holes (correct KJV flagged)

**Mostly handled:** `_canon` folds smart quotes and em/en dashes (lines 81–82); case and whitespace are normalized; boundary `.`/`!`/`?` stripping matches narration practice (`test_boundary_truncation_allowed`).

**Remaining false-block risks (untested):**
- Colon vs comma at phrase end on **tagged full-verse** blocks: Ps 22:22 `my brethren:` vs author `my brethren,` → correctly MISQUOTE on tagged path (B1 WARN on long-form inline confirms detection works when punctuation differs). Good for strictness; ensure authors know tagged blocks are unforgiving.
- `"It is finished".` with terminal punctuation **outside** quotes (short #05) parses as span without period — passes against `It is finished:` in corpus. OK.
- Hyphenation differences not covered by dash fold (rare in KJV narrations).

No false-block regressions in the 10 tests, but coverage is thin on colon/semicolon boundary cases and marked-corpus copy-paste.

---

### Missing steps / verification gaps

| Claim in artifact | Gap |
|---|---|
| “Fail-closed” (lines 22–23, 38–39) | Corpus missing → exception, not structured block |
| B1 audit 54/0/1 | No committed audit script; count not reproducible |
| “REUSES … real import” | No parity fixture vs `check_quote`; strict mode is a forked comparison path |
| 10/10 tests | Zero tests for `resolve_inline`, `verify_narration`, rhetoric skip, tagged-block-without-quotes, ellipsis order, italics omission, import failure |
| Plan B2 corpus pin | Not done — still environment-dependent HF-POC path |
| Plan “fix input not just lock” | `pipeline/kjv_check.py` still uses corrupt cache for drafting |

**`narration_parse` coupling:** `_QUOTE = re.compile(r"[\"“”]([^\"“”]+)[\"“”]")` — single-quoted KJV spans are invisible. Not Phase B’s bug, but end-to-end KJV coverage is incomplete.

**Range ref test is weak:** `test_range_ref_resolves` only checks an opening phrase from v6, not a string crossing the v6/v7 boundary where join artifacts could hide errors.

---

### Reuse / duplication

Dynamic import of `short_gate/kjv.py` avoids a literal copy — good per user direction.

Still duplicated:
- `_canon` / `_strip_markers` partially reimplement `norm()` with different rules.
- No `strict=True` parameter on upstream `check_quote` — future fixes to alias parsing or `verses_for` in sibling repo apply; strict comparison logic does not.

This is acceptable tactically but fails the plan’s “provenance + equivalence fixture” contract.

---

### Cost / spend

Module itself: **$0** (offline). Justified as a backstop **if** wired into lock.

Current state: $0 spent, **$0 enforcement** — corrupt cache still feeds drafting; this code does not run in any mandatory path. Committing the file alone does not justify closing the scripture-integrity root cause from the plan.

---

### Is it sound to commit?

**Commit the module as in-progress library code?** Acceptable — the comma regression and tagged-path strictness are directionally correct.

**Commit as “Phase B done / lock-ready”?** **No.** The ellipsis order hole, italics/prefix omission hole, inline chapter-level false OK, unpinned corpus, missing audit tooling, and zero integration with the chokepoint mean a real misquote can still slip through on paths the B1 sample may not have exercised (multi-fragment ellipsis edits, partial quotes on `{saying}` verses, inline cross-verse echoes within a chapter).

The B1 WARN on `my brethren,` vs `my brethren:` shows the punctuation comparator works when it fires; it does not prove the other holes are absent.

---

VERDICT: REVISE
TOP FIXES:
1. Require ellipsis fragments to match **in order** (and ideally as non-crossing spans in the joined verse text); add regression tests for reversed fragments and cross-verse ranges.
2. Pin and witness the corpus per plan B2 (`data/kjv_corpus.json` + `JESUS_KJV_CORPUS`), catch `load_kjv_by_name` failures as blocking `UNRESOLVED`, and remove the hardcoded user path from `_KNOWN`.
3. Tighten inline verification: resolve at **verse** granularity (reuse `find_ref_for_quote` or require tagged ref proximity), and wire into `cli_lock` / redirect `fetch_kjv` off the corrupt cache before calling Phase B complete.
