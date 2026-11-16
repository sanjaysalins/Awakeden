# Independent review — cursor (OK, 62s)

## Findings (adversarial, plan-as-artifact)

### Scope mismatch — owner asks 3–4 vs what the plan actually assigns

The header block lists five owner requests verbatim (lines 3–8), including **publication AI removal** (#3) and **complete Awakeden removal** (#4). The assignment then narrows to: *“Find REAL defects in the tracker page and the code that builds it and logs links”* (line 13) and a six-file reading list (lines 15–19).

That is a real defect in the **plan**, not just an omission. Locked-episode **publication** lives under `batches/**/publish/`, is already guarded in `pipeline/publish_check.py` (NO-AI-WORDING, NO OLD BRAND), and is **not** on the file list. A reviewer who only follows this pack can **PASS the tracker** while shipping packs still contain TikTok/Facebook/Instagram sections and Awakeden/AI copy on disk (thousands of `PUBLISH_INDEX.html` files still expose those platforms in the repo). Owner ask #4 explicitly allows **already-posted YouTube** to stay; the plan never says to **exclude** live YT descriptions from “Awakeden purge” scope, so reviewers will disagree on what “completely” means.

### Ambiguous acceptance criteria — “AI wording” will produce false positives

The job bundles *“leftover … AI wording”* with tracker defects (line 13). In the actual builder, the page **intentionally** surfaces YouTube Studio disclosure in `CANON`:

```44:50:F:/slk/PycharmProjects/JesusInTheBible/build_upload_tracker.py
CANON = [
    ("Audience", "NOT made for kids"),
    ("Altered content / AI disclosure", "YES (synthetic/altered imagery)"),
    ...
]
```

That is upload-runbook text, not “publication of a locked episode.” The plan never separates **studio checkbox guidance** (owner may still need this) from **publish-pack / upload-kit copy** (owner ask #3). Without that line, a diligent reviewer is incentivized to file a bogus defect on `build_upload_tracker.py:46` or `_UPLOAD_TRACKER.html` canon rows — or to “fix” the wrong layer.

### Verification gap — stale built HTML

The plan tells the reviewer to read **`_UPLOAD_TRACKER.html (the built page)`** (line 17) but does **not** require regenerating via `build_upload_tracker.py` first or reconciling header counts (`Next up to post ({n_queue})`, `Posted ({n_posted})`) against `release_state.gather()` + `to_post()`. The built file is generated output; git can ship **stale HTML** while Python/ledger logic is already fixed. Wrong counts and wrong sections are exactly what the job cares about (line 13); this is a single point of failure for the whole red-team.

### Feasibility — “ready / to-post / posted” logic is wider than the file list

Queue membership is computed in `pipeline/release_state.py` (`to_post`, `_SHIPPED`, `TRACKED_PLATFORMS`) plus Swirls-specific branching in `build_upload_tracker.py` (`SWIRLS_HOLD`, `SWIRLS_BLOCKED`, `finished_inventory`, hardcoded `POST_ORDER`). The plan only names `release_state.py` and two JSON ledgers (lines 18–19). It does **not** mention:

- `finished_inventory()` (“Other finished videos, not ready”) — where a **ready-on-disk** piece can be **absent from “Next up”** if manifest status ≠ `studio_complete` / `live`.
- Hardcoded `POST_ORDER` / spare-bank labels — calendar order on the page is **not** purely manifest-driven.
- Swirls **ready** for owner ask #5 — no definition (publish pack present? `FINAL_VIDEO.txt` pin via `upload_engine.harvest_facts`? only `discover()`?). Reviewers cannot consistently judge *“a not-ready item shown as ready”* (line 13).

Meanwhile `STATE.md` still describes a **“30-episode rule”** hold section; code has `SWIRLS_HOLD = False` with comment that the hold was lifted (`build_upload_tracker.py` ~377–379). The plan cites the owner lifting the rule (#5) but gives reviewers **no rule for trusting docs vs code**, so expect false “missing section” reports.

### Reuse — duplicates existing $0 gates instead of chaining them

`v2/SPEC.md` already binds publish/release to `publish_check.py` + `release_check.py`. This plan instructs manual grep for Awakeden/AI/TikTok (line 13) while **not** requiring:

- `release_check.py` after `upload_tracker.py --set` (the write path itself prints that reminder).
- `publish_check` on locked `publish/` trees for asks #3–#4.

That is **duplicate, weaker verification** — high reviewer time, easy false GREEN. Prior red-team notes in `_redteam_brand_tracker_20261116/_independent_review/` already argued that weakening G5 + one-off strip scripts ≠ owner asks 3–4; this “final” pack does not incorporate that lesson.

### Hidden risks the job lists but the plan doesn’t operationalize

- **Two write paths / two ledgers** (`data/release_ledger.json` vs `_swirls_release_ledger.json`, lines 18–19): Swirls ledger values are `[url, date]` tuples vs dict entries on the main side — easy to assume parity checks that don’t exist. `swirls_upload_tracker.py` still builds a **separate** `_SWIRLS_UPLOAD_TRACKER.html` board; the plan doesn’t ask whether that second page contradicts the unified owner UX (“one tracker to look at” in code comments).
- **`upload_tracker.py` docstring** still shows a **TikTok @awakeden** example (lines 14–15 in the live file) while runtime rejects non-YouTube — exactly *“commands that would write bad data”* / confusing copy (job line 13), but only if the reviewer reads the module header, which the plan barely surfaces beyond “logging commands.”
- **Dyslexia requirement** (line 10) is not turned into checks: Posted section still uses **episode blocks**, progress bars, and strings like *“1/8 shorts fully posted (1/8 posted somewhere)”* — cognitively heavy compared to flat “Next up.” The job mentions *“confusing wording”* (line 13) but sets no pass/fail bar.

### Cost / spend

The plan itself is $0, but it **does not justify** a human full-repo manual read (line 15 path + open-ended defect hunt) when deterministic gates already exist and the scoped file list undercovers the largest surface (publish packs). That’s poor ROI for owner asks 3–4.

### Over-engineering?

Not in code — but the plan **overloads one adversarial pass** with five owner mandates while **under-specifying** verification (no rebuild step, no `release_check`/`publish_check`, no publication tree). That’s premature “final” labeling for a tracker-only slice.

---

VERDICT: REVISE  
TOP FIXES:  
1. Split scope explicitly: **Tracker slice** (items 1–2, 5, hide/unhide, counts/sections) vs **Publication/brand slice** (items 3–4) with file list adding `pipeline/publish_check.py`, `release_check.py`, and `**/publish/` for locked episodes — and define “AI” as **public-facing copy only**, not YouTube Studio canon on the tracker.  
2. Add mandatory verification steps: run `build_upload_tracker.py`, then reconcile `n_queue` / `n_posted` / section membership against `release_state.gather()` + Swirls `discover()` + ledgers; run `release_check.py` and targeted `publish_check` — don’t treat grep alone as done.  
3. Define **Swirls “ready”** and **blocked vs Next up** in one sentence each (manifest/finality/pack/blocklist), and tell reviewers to ignore stale `STATE.md` 30-episode language when `SWIRLS_HOLD` is false.
