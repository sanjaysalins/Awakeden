# Independent review — cursor (OK, 115s)

## Findings on the red-team plan

### Feasibility / wrong pointers

- **Line 7 — “`_independent_review/` (latest stamp)`” is wrong in this repo.** The newest folder is `20261116-124529/`, and it only contains another copy of this red-team `prompt.txt`, not the 10-insight panel output. The actual insight reviews live in `20261116-123445/` (`cursor.md`, `gemini.md`, `claude.md`, plus `INDEX.md`). A reviewer who follows “latest stamp” will review the wrong artifact or find nothing useful.

- **Line 7 names `SUMMARY_TEXT.md` but not `_SUMMARY.html`.** The dyslexic-friendly owner page is likely the HTML (`_quality_uplift_20261116/_SUMMARY.html`). Text and HTML track today, but the plan never requires checking both stay in sync.

- **Line 9 — “videos: pull frames with ffmpeg into %TEMP%” without `EPISODES.txt`.** `BRIEF.md` (same pack) already defines the canonical final-mp4 paths in `EPISODES.txt`. This plan omits that file, so reviewers will waste time hunting paths or hit the wrong assets (e.g. Jacob’s Ladder under `poc_living_sketchbook/...` vs a Swirls folder).

- **Line 9 — ffmpeg frames alone won’t reliably prove freeze/boomerang.** `swirls_report.md` §0.1 grounds the rule break in **unit/storyboard metadata** (“every page is `"freeze"`…”). Static frames every few seconds can miss boomerang/tail-loop behavior. The plan never says to read assembly/unit JSON (or the reports’ explicit episode lists) alongside video sampling.

### Hidden risks / false assumptions

- **Line 5 — owner expectation “validated by other AI panels too” vs panel health.** `INDEX.md` for `20261116-123445` records **3/5 healthy voices**, **quorum 4 failed**, and **“DEGRADED PANEL — do not lock on this run”**; codex and grok timed out. All three completed reviewers ended **VERDICT: REVISE** on `INSIGHTS_PANEL.md`. The plan never requires checking quorum or whether the owner summary still over-claims (“Every verse was checked word for word” in `SUMMARY_TEXT.md` line 7) relative to a degraded, REVISE-only panel.

- **Line 9 — truncated house rules vs what motion work actually needs.** The plan cites a short CLAUDE.md bullet list but omits Swirls-specific constraints from `BRIEF.md` §Task A (no burned captions, ink motif static, Remotion on top only, dubbing-friendly meaning). A reviewer could PASS “My pick” motion advice that violates those rules while technically satisfying “no freeze/boomerang.”

- **Spend path not grounded.** Summary figures (~$25 Swirls re-cut, ~$3.50 heroes) trace to Fable estimates in `swirls_report.md`, but the plan doesn’t require checking them against **OpenArt bridge / no unattended Swirls gen** (per `CLAUDE.md`). Treating “~$25” as a simple quote hides that much of this work is **not** a one-command spend.

### Missing steps / verification gaps

- **No explicit condensation checklist against `comic_report.md` / `swirls_report.md` top-5 sections.** Example already visible: comic report **ranked win #5** (“Side-by-side for every `as... so` line” / `infographic-panel` diptychs) is **absent** from `SUMMARY_TEXT.md` §2 and `_SUMMARY.html` §2. The plan says “something important… left out” but doesn’t name “compare top-5 ranked wins line by line,” so omission is easy to miss.

- **No requirement to reconcile per-insight buckets with each reviewer file.** Healthy panel cursor.md labels **#4 TEXT FAIL**, buckets **#1, #2, #7, #8** as USE WITH CARE, and **#6** “trim folded.” The owner page merges two insights into one “Drop” card and promotes several “USE” / “USE – careful” tags. The plan asks for bucket checks but doesn’t require a **per-insight matrix** (insight # → claude/gemini/cursor → owner tag), so systematic mis-bucketing slips through.

- **Swirls freeze count sanity check missing.** Report §0.1 says **every storyboard-page episode** breaks the rule (lists Ep 02, 07, 08, 10, 11, 13, Jacob’s Ladder). Summary says **“6 of the Swirls films”** (`SUMMARY_TEXT.md` line 79). The plan doesn’t flag reconciling **6 vs 7+** before trusting “~ $25 total.”

- **“My pick” / Step 2 doctrine gate underspecified.** Line 9 mentions “doctrine checked both ways” but not **engine + external panel** on any new narration (`narration_gate.py`, `independent_review.py` on locked script) before the owner treats Bier/Forsaken as green-lit rewrites.

### Reuse

- **Duplicates the repo’s `independent_review.py` pattern** without requiring the reviewer to use existing artifacts: `INSIGHTS_PANEL.md` as source, `INDEX.md` for quorum, or the parent `BRIEF.md` methodology (2–3 s frame cadence, skill names). That’s reinvented ad-hoc procedure inside `_quality_uplift_20261116/` instead of pointing at established gates.

- **Does not reference `$0` validators** already in the engine (`check_landing_hold.py`, `.claude/skills/bible-check`, `.claude/skills/cost`) for the mistakes/cost lines the summary asserts.

### Over-engineering

- Not over-built; if anything it’s **under-specified** for the risk: one paragraph of examples (line 9) with no output path, no merge step for degraded panel, and a broken “latest stamp” rule. The nested stamp folder `124529` re-embedding the same prompt suggests **procedural recursion** without a clear “authoritative artifact” list.

### Cost / spend

- The plan asks reviewers to challenge wrong costs but gives **no method** (re-derive from `swirls_report.md` per-film bands, OpenArt credits, or “words-before-money” for re-voice). Comic report win #2 itself admits **“about $3-6, not spent”** for optional new endings while the summary flattens to **“$0 (own clips)”** — a condensation the plan should force reviewers to flag; it doesn’t.

---

VERDICT: REVISE  
TOP FIXES:  
1. Replace line 7’s “latest stamp” with fixed paths: panel artifact `INSIGHTS_PANEL.md`, reviews `/_independent_review/20261116-123445/`, and mandatory read of `INDEX.md` (quorum + DEGRADED status) before judging owner claims about “AI panels validated.”  
2. Add a mandatory verification chain: `EPISODES.txt` → final mp4 + **unit/storyboard JSON** for Swirls freeze/boomerang (not ffmpeg-only), and **both** `SUMMARY_TEXT.md` and `_SUMMARY.html`.  
3. Require line-by-line reconciliation: comic/swirls **top-5 ranked wins** and **top-3 fresh insights** vs owner §1–§3, plus per-insight USE/REJECT matrix against all healthy panel files, and explicit flag if Step 2 rewrites skip narration gate + full doctrine/panel lock.
