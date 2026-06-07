# Independent review — cursor (OK, 95s)

## Adversarial code review — Phase A (`narration_parse.py` + `cluster_gate.py`)

The Psalm 22 regression is real and the fail-closed direction is right. The code is **not** a safe foundation to build Phase B/C on without fixes. It catches one specific shipped defect (byte-identical trailing tag + shared opener n-grams) but has material false-PASS holes, parser brittleness, and acceptance gaps relative to the stated problem and the v5 plan.

---

### Feasibility / integration

| Claim | Reality |
|---|---|
| Replaces `veed_io/_extract_spoken.py` | Parser logic is correct for shorts, but **nothing in the pipeline imports these modules yet** (`runner.py`, `handoff.py`, `cli_lock.py` do not call them). `_extract_spoken.py` still exists; `veed_io/caption.py` still has its own strip path. Phase A is an island. |
| Handles shorts **and** long-form | Works on current long-form files because every spoken line sits under `**[speaker]**`. That is **format discipline**, not parser enforcement. Any continuation line without a re-stated header is **silently dropped** (`parse_blocks` lines 105–106 only append when `cur is not None`). |
| `quoted_spans_with_refs` ready for Phase B | Shipped untested. Classification heuristics (`< 4 words` → `rhetoric`, line 147) will mis-route short verbatim spans unless the block header carries `ref`. |

---

### `narration_parse.py` — parser bugs and brittleness

**1. Header ref parsing is Unicode–em-dash-only (real variance risk)**

```34:34:pipeline/narration_parse.py
_REF_IN_HEADER = re.compile(r"—\s*KJV\s*,\s*(.+?)\s*$", re.IGNORECASE)
```

```75:75:pipeline/narration_parse.py
    speaker = re.split(r"—", inner, 1)[0].strip().lower()
```

Both patterns require U+2014 `—`. ASCII `- KJV` or en-dash `–` (common when copying from Word/Google Docs) yields `ref=None` and a polluted `speaker` string like `"narrator - kjv, psalm 22:18"`. Blocks still parse, but Phase B tagged-KJV verification silently degrades to untagged/heuristic mode.

**2. `hook` / `cta` contract is narrower than the plan and fragile**

```57:66:pipeline/narration_parse.py
    def hook(self) -> str:
        """First spoken sentence (the scroll-stopper)."""
        s = sentences(self.spoken_text)
        return s[0] if s else ""

    @property
    def cta(self) -> str:
        """Last spoken sentence/clause (the close)."""
        s = sentences(self.spoken_text)
        return s[-1] if s else ""
```

- Plan A1 says hook = **first 1–2 sentences**; code uses **first 1 only**. A templated second hook sentence is invisible to the opener gate.
- `cta` = **last sentence of entire narration**, not “last clause / landing beat.” A writer can evade the gate by reordering: e.g. `"Come to Him. That's Jesus."` → CTA becomes `"That's Jesus."`, suffix `"that's jesus"`, **no** `"come to him"` flag. This is a direct false-PASS against the stated goal.
- `sentences()` (lines 167–174) splits only on `(?<=[.!?])\s+`. Semicolons, many KJV-internal `?`, abbreviations, and ellipses are not handled. Short #02’s real close is one compound sentence (`That's Jesus — come to Him.`); you only catch it because substring containment rescues the trailing 3-gram — not because CTA extraction is semantically correct.

**3. `normalize()` does not strip terminal punctuation before fingerprinting**

```155:164:pipeline/narration_parse.py
def normalize(s: str) -> str:
    ...
    s = s.lower()
    s = re.sub(r"\s+", " ", s)
    return s.strip()
```

`_cta_suffix` tokenizes on whitespace, so `"him."` and `"him"` are different tokens. Variants like `"Come to Him!"` / `"Come to Him."` / `"Come to Him"` form separate exact-suffix buckets; you rely on the substring pass (lines 111–114) to merge them. That pass is not a substitute for proper tokenization and will miss variants like `"Will you come to Him today?"` (suffix `"to him today"` — **`"come to him"` is not a substring**).

**4. `quoted_spans_with_refs` — false routing for Phase B**

```147:148:pipeline/narration_parse.py
            elif low in _RHETORIC or len(low.split()) < 4:
                out.append({"text": span, "ref": None, "klass": "rhetoric"})
```

`"I thirst."` (John 19:28 in short #08) becomes `rhetoric`, not a KJV claim — fine only if Phase B always uses block-level `ref`. Untagged inline quotes ≥4 words become `inline_kjv` with `ref=None`; no resolver is implemented here. Building B3 on this without tests is risky.

**5. No markdown emphasis stripping**

Unlike `veed_io/_extract_spoken.py` line 29, spoken text retains `*I*`, `*me*`, etc. (Isaiah long-form Movement 2). Fingerprints and future KJV compare can drift on formatting alone.

---

### `cluster_gate.py` — false-PASS and false-BLOCK holes

**6. CTA detection is too narrow for the actual Psalm 22 defect family**

```100:122:pipeline/cluster_gate.py
    cta_by_id = {aid: nar.cta for aid, nar in parsed}
    ...
        suf = _cta_suffix(cta, 3)
    ...
            if aid not in members and suf and suf in NP.normalize(cta)
```

This catches **trailing 3-word shape of the final sentence** plus substring containment **within that same final sentence**. It does **not** catch:

| Missed pattern | Evidence in real cluster |
|---|---|
| **Bridge / conviction repetition** | `"bring you home"` in shorts #03, #05, #07 — a named defect in the plan/context, **zero implementation** (`bridge_repetition` appears in `Finding.kind` docstring line 38 but is never emitted). |
| **Synonym gospel closes** | `"Come unto Christ"`, `"Turn to the Saviour"`, `"Kneel before the risen Lord"` — your own negative test (lines 81–87) only checks two *orthographically distinct* invites; semantically identical templating passes. |
| **Suffix-appended tags** | `"Come to Him today"` / `"Come to Him now"` — different trailing 3-grams, substring miss. |
| **CTA moved off the final sentence** | Reordering landing sentences bypasses the gate entirely. |
| **Shared conviction scaffolding** | `"a thousand years"` appears in **body** blocks across nearly all 8 shorts, but only **hook first sentence** is scanned (lines 127–128). Body templating is invisible. |

The gate proves the **retroactive** `"Come to Him"` tag; it does **not** prove the general “de-template cluster wording” strategy the plan claims.

**7. Substring containment can false-merge unrelated CTAs**

Line 113: `suf in NP.normalize(cta)` with no word-boundary check. A long CTA containing `"come to him"` as an incidental phrase (e.g. `"not asking you to come to him for gain, but to trust him"`) gets lumped into the `"come to him"` family. Low probability in this corpus, but the logic is sloppy.

**8. Opener gate: legitimate false-BLOCK risk + alert noise**

```133:141:pipeline/cluster_gate.py
    opener_floor = max(min_share, 3)
    for g, c in opener_counts.items():
        if c >= opener_floor:
            report.findings.append(Finding(
                kind="opener_repetition", ...
```

- Any shared 2–3 gram in **first sentence only** with count ≥3 is **BLOCKING**. A Psalm 22 series that legitimately opens `"Psalm twenty-two…"` three times will block — may be intended, but there is no doctrinal whitelist / series-scaffold exemption (plan A2 mentions one for mid-body truth phrases; not implemented).
- `_dedupe_openers` (lines 148–157) dedupes only `opener_repetition`, not `cta_repetition` — overlapping CTA findings can spam the report.

**9. `within_cluster=False` advisory mode is untested**

Lines 89–90 document cross-catalogue advisory behavior; no test verifies findings are non-blocking. Phase C registry design depends on this.

---

### Tests — false confidence

```21:24:pipeline/test_cluster_gate.py
def _real_shorts() -> list[tuple[str, str]]:
    paths = sorted(_SHORTS.glob("0*/narration.md"))
    assert len(paths) == 8, f"expected 8 Psalm 22 shorts, found {len(paths)}"
```

**10. Acceptance suite is regression-theater for the general strategy**

- **No long-form tests** despite plan A1 requiring 8 shorts + 2 longs parse non-empty.
- **No `quoted_spans_with_refs` tests** despite being part of the A1 deliverable.
- **No parser variance fixtures** (ASCII dash headers, smart quotes in headers, multi-line blocks, range refs `Psalm 22:6-7`).
- `test_opener_family_flagged` only asserts `>= 4` members (line 55), not the documented 6/8 — weaker than the artifact claims.
- **No false-PASS regression** for synonym CTAs, bridge phrases, or CTA-not-last-sentence.
- **No test** that `within_cluster=False` downgrades blocking.
- Positive tests grep for fixture phrases (`"come to him" in f.phrase`, `"thousand years" in f.phrase`) — they validate the Psalm 22 snapshot, not the detection algorithm.

7/7 passing means **the fixture cluster is caught**, not that **the gate is sound**.

---

### Reuse / over-engineering

- **Good:** Fail-closed `EmptyNarrationError`, speaker-block model matches real shorts, cluster gate correctly reuses `narration_parse` for extraction.
- **Bad:** `quoted_spans_with_refs` + rhetoric table shipped in Phase A without tests or callers — premature surface for B. Plan’s `short_gate`/`freshness.py` port and `independent_review --type cluster` are not started; this is half of A2, not A2.
- **Duplication risk remains:** Three spoken-text sources can still diverge until `handoff`/`caption` are rewired.

---

### Cost justification

Phase A code is ~$0 and correctly sequenced before content rewrites. **But** building Phase B (KJV corpus pin, `cli_lock.py`, re-panel 8 shorts) on this gate would spend real authoring/review dollars while **bridge repetition** and **synonym CTAs** still sail through — repeating the original failure mode with different words.

---

### Bottom line

**Commit as-is?** Only as an **experimental Phase A3 fixture prover**, not as hardened infrastructure.

**Build Phase B/C on it?** **No** — fix CTA/landing fingerprint scope, punctuation-normalization, header encoding, bridge detection (or explicitly scope it out with a tested deferral), and expand acceptance tests to long-form + false-PASS cases first.

---

VERDICT: REVISE
TOP FIXES:
1. Harden CTA fingerprinting: strip punctuation in `normalize()` before tokenization; fingerprint the **last spoken block** (or last N words), not only the final sentence’s trailing 3-gram; add **bridge/landing-beat repetition** (or formally defer with a failing test documenting the `"bring you home"` gap).
2. Expand acceptance tests: parse **both long-forms** non-empty; add parser fixtures for ASCII/en-dash headers, smart quotes, and multi-sentence landing blocks; add false-PASS regressions for synonym gospel CTAs and CTA-not-last-sentence reordering.
3. Fix header parsing to accept `-`/`–`/`—` interchangeably in `_REF_IN_HEADER` and `_parse_header`, and align `hook` extraction with the plan (first 1–2 sentences) or update the contract and tests explicitly.
