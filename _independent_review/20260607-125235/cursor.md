# Independent review — cursor (OK, 54s)

## v1 convergent findings — resolution check

| v1 finding | Resolved in v2? | Evidence |
|---|---|---|
| Extractor fail-closed | **Mostly yes** | A1 (`pipeline/narration_parse.py`, zero blocks → raise) directly fixes the verified bug in `veed_io/_extract_spoken.py` (MOVEMENT-only, CLI-only). |
| Witnessed KJV, no bible-api fallback | **Partially** | B2/B3 intent is right, but B2 has no named dataset/sources, and B3 never says to stop `scripture.fetch_kjv` from continuing to write unverified API text into `data/kjv_cache.json` (current behavior at `pipeline/scripture.py:36-69`). |
| No five-beat coercion | **Yes** | C1 line 98: “Do NOT run `engine.review`'s structure gates on hand-authored content.” |
| Rule-8 short-only | **Yes** | C1 line 97 + verification line 137. Matches `defect_classes.json` rationale. |
| Cluster sim exact+semantic, sentence level | **Partially / oversold** | Changelog line 5 claims “exact + semantic”; A2 lines 48–49 are exact + normalized + stem, with **LLM** semantic in line 52 — not deterministic sentence-level semantic. |
| Phrase ledger post-gen only | **Yes** | C2 lines 103–106 explicitly reverses v1’s generation banned-wall. |
| Fix 5 (conviction) deferred | **Yes** | Phase D lines 117–118; G3/G8 exist in `engine.py:674,679`. |
| Standing gates + ledger backfill | **Weak** | Backfill is in C2 line 107; “standing gate” is A4 line 62 = RESUME.md note only — no hard fail point. |
| Regression test | **Yes** | A3 + C3 lines 58–59, 110–111. |

---

## Critical new / remaining problems

### 1. Internal contradiction: whitelist vs acceptance test (A2 line 50 vs A3 line 59)

A3 requires flagging **8× "Come to Him"** (including variants). A2 line 50 whitelists **"Come to Him" *as a concept*** in gospel vocabulary.

Those cannot both be true in one deterministic gate. An implementer following the whitelist will pass the exact defect the plan was written to catch. The whitelist must exclude closers/CTAs/hooks, or A3 is false on arrival.

### 2. A3 acceptance criteria do not match real artifacts (A3 line 59, Context line 11)

Context claims **“6/8 open ‘A thousand years before the cross…’”**. Actual first spoken sentences:

- **Match (~4):** #01, #02, #08 (variants); #03 has “thousand years” but not in the first ~6 tokens.
- **Miss on opener n-gram:** #04 (“Psalm twenty-two is…”), #05, #06 (“The psalm Jesus cried…”), #07 (“A king once wrote…”).

A2 line 47 defines hook as **first spoken sentence** and opener as **first ~6 tokens**. That will **not** reliably flag “6/8 thousand years hooks.” A3 as written is a **false gate** — Phase A could “pass” while missing half the stated hook repetition. Either widen hook detection (e.g. first 2 sentences, stemmed n-grams, “thousand years” anywhere in opening block) or downgrade A3’s hook claim to what the deterministic layer actually catches.

**8× "Come to Him"** is real and should pass exact/normalized CTA match — that half of A3 is sound.

### 3. A4 “standing gate” repeats the org failure (A4 lines 61–62)

Root cause line 15–16: checks never ran because nothing **required** them. A4 only says wire into workflow and note in `RESUME.md`. Today:

- `_finalize.py` runs audio only — no verification.
- `handoff.py` covers engine-generated paths, not hand-authored longform/shorts (C2 line 107 admits this).
- `independent_review.py` accepts **one file** (`artifact` positional arg, line 157) — no `--type cluster`, no multi-artifact input.

Without a **named, fail-closed chokepoint** (e.g. `verify_narration.py --lock` must exit non-zero before `_finalize.py` / LOCK status), A4 is documentation, not enforcement — same failure mode as v1.

### 4. `LENS_CLUSTER` / `--type cluster` is unspecified (A2 line 52)

`independent_review.py` only supports `--type narration|plan` (line 158). Plan adds cluster mode but does not specify:

- CLI contract (folder? glob? manifest?)
- How 8× spoken-only texts fit CLI context limits
- Whether cluster review is blocking or advisory
- Grok failure mode (v1 header: grok errored; no mitigation)

Reusing the panel is fine; the **interface and enforcement** are not designed.

### 5. Phase B is correct in principle, under-specified in execution (B2 lines 74–77, B4 lines 85–88)

**B2:** “Download a known-good structured dataset” + “cross-verify ≥2 independent sources” + “human adjudication” — but **no named sources** (Crosswire? BibleGateway scrape? DBP?). Feasibility and timeline are unknown; this can block B indefinitely while A is cheap.

**B4:** Ref-mapped contiguous substring is the right fix for Acts-8:35-style elision and NT-vs-OT (panel points). Gaps:

- Long-form already uses boundary ellipsis in quotes (e.g. Ps 22:6–7 in `longform/02_.../v1/narration.md:40`) — interior vs boundary rules need worked examples.
- KJV **italics** (B2 line 76 spot-check) are not in automated B4 rules — edition mismatch will false-fail or false-pass.
- B4 line 88 threads canon through `engine.review`/`independent_review` but C1’s hand-authored path **bypasses** `engine.review` — canon must go through `verify_narration.py` explicitly.

**Ps 22:7 comma** claim is verified against live cache: `"…they shake the head saying,"` (missing comma before “saying”).

### 6. C2 gaps left as footnotes, not deliverables (C2 lines 107–108)

- **Lock chokepoint:** “Identify the single lock chokepoint (or add one)” — required for ledger backfill and A4, but not assigned to a phase step with acceptance criteria.
- **`panel_misses` writer:** “Confirm the `panel_misses` writer exists” — it **does not** as an automated path. `learning.append_record` exists (`pipeline/learning.py:45`) but only manual RESUME.md workflow appends to `calibration.jsonl`. Plan flags inert learning loop but does not schedule building the writer.

### 7. Cluster scope for longform + shorts undefined (A2 line 54, Re-verification line 125)

8 shorts live under `longform/02_.../v1/shorts/`. Plan says within-series **and** cross-catalogue but never defines whether parent long-form + 8 shorts are **one cluster** or two. Re-verification step 2 (“de-template hooks + CTAs so **no two land the same**”) is a **content rewrite** across 8 LOCKED artifacts + panel cycles — cost/time beyond “~$0–$3 ElevenLabs per short” (Re-verification line 128).

### 8. Duplication / drift risk (A1 vs existing tool)

New `pipeline/narration_parse.py` is correct; plan does not say to **replace** `veed_io/_extract_spoken.py` with it. Two parsers will diverge (caption/timing vs verification).

### 9. “Semantic at sentence level” in changelog (line 5) misstates A2

Panel asked for sentence-level similarity without heavy Jaccard. v2 dropped Jaccard (good) but “semantic” is delegated to LLM backstop (A2 line 52), not deterministic. Changelog overclaims relative to implementation.

### 10. C1 deterministic `lecture-phrasing` underspecified (C1 line 97)

`lecture-phrasing` is `deterministic: true` in `defect_classes.json:14` (“G8(2) + banned phrase list”) but plan does not point to an existing phrase list module for the harness — risk of re-inventing or LLM-only check while labeled deterministic.

---

## Feasibility summary

**Phase A (A1–A3):** Worth building first; extractor fix is real and verified. Fix A2 whitelist + A3 hook criteria before calling A3 the “gate for the whole effort.”

**Phase B:** Necessary for Scripture integrity; needs named sources and a scoped MVP (audit script B1 before full canon B2).

**Phase C:** Sound direction; depends on B for KJV checks and on a real lock chokepoint for ledger/gates.

**Cost:** Deterministic tier honestly $0. Re-verification (lines 122–128) understates panel/time cost for de-templating 8 shorts + re-panel.

---

## Safe to implement?

**Phase A only:** yes, after fixing the whitelist/A3 contradiction.

**Full A–C as written:** not yet — A4 enforcement, cluster CLI contract, and B2 source pinning are blocking design holes, not nits.

---

VERDICT: REVISE

TOP FIXES:
1. **Delete or sharply narrow A2 line 50 whitelist** — never exempt CTA/hook/closer strings (“Come to Him”); whitelist only shared doctrinal *mid-body* phrases, or A3’s primary acceptance test is self-nullifying.
2. **Rewrite A3 hook acceptance** to match real Psalm 22 openers (or change A2 detection to multi-sentence / “thousand years” family matching); current “first ~6 tokens” will not flag the claimed 6/8 hooks.
3. **Specify enforceable lock integration in A4/C2** — one fail-closed pre-lock command, `cluster_review` + `independent_review --type cluster` CLI contract (inputs, exit codes, blocking vs advisory), and retire/replace `veed_io/_extract_spoken.py` via `narration_parse.py`.
