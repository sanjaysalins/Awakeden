# Independent review — cursor (OK, 119s)

## Independent review: red-team films pack (plan artifact)

### Feasibility vs codebase

1. **Film paths mostly exist**, but the plan does not anchor the “old” baseline to repo truth. For ep08, `FINAL_VIDEO.txt` already pins `uplift/ep08_uplift_final.mp4` (not `CAN_ANY_GOOD_THING_final_sfx.mp4`). The plan’s ep08 old path matches `check_uplift.py`’s `SHIPPED`, but a reviewer who reads `FINAL_VIDEO.txt` first can mis-identify the baseline. The plan never says: read `FINAL_VIDEO.txt.prev_pre_uplift` or each uplift folder’s `check_uplift.py` `SHIPPED` constant.

2. **“Narration text: narration.md in each film's folder”** is wrong for Jacob’s Ladder as stated. The plan itself admits two narration sources (`swirls_pilot_01_jacobs_ladder` + `poc_living_sketchbook\_rewrite_v4\`) but does not say which drives mark timing. JL `check_uplift.py` uses `SPEC["words"]` from `uplift.json`, not “pick a narration.md.”

3. **Film #7 (Woman, Behold Thy Son)** — the plan points only at `woman_behold_john1926_uplift_v1.mp4` vs `woman_behold_john1926_sfx_v5hook.mp4`. The actual build lives under `visual/uplift_v1/` (`livingpage_short` spec, concat segs, `_PILOT_REVIEW.html`). `COMIC_UPLIFT_SPEC.md` explicitly references `livingpage_short.spec.json` and the livingpage engine. Reviewing two flat MP4s without the spec/seg list makes “wrong picture on key lines” (the spec’s own finding) **unan auditable**.

4. **“How” — ffmpeg 1 fps + extra around every cut** is under-specified. Cuts are not discoverable reliably at 1 Hz. Six of seven Swirls/JL uplift folders already have `uplift.json` (shot `f0`/`f1`) and per-episode `make_review.py` with **curated** compare times (ep08’s `make_review.py` lists narrative beats, not uniform 1 s spacing). The plan asks reviewers to reinvent cut lists by hand.

5. **Audio check** — the plan’s `ffmpeg -i f -map 0:a -c copy -f md5 -` is weaker than what the repo already does: every Swirls/JL `check_uplift.py` uses `-map 0:a:0`, compares uplift vs `SHIPPED`, and gates duration/frame count. The plan omits **video duration parity** and **frame count** entirely.

### Hidden risks / false assumptions

6. **“LOCKED already” (items 1–2)** vs verdict taxonomy **LOCK / REJECT / NEEDS PAID FIX** — no rule for whether red-team can overturn owner lock or only document regressions. Without that, two films are a political landmine, not a technical review.

7. **1 frame/second + Vision** will **miss** defects the builder already automated: frozen/Ken-Burns stand-ins (`clip_motion_audit.py` ECC metrics), blue-motif drift (`G-MOTION` blue pixel counts in `check_uplift.py`), mark word-alignment ±3 frames (`G-MARKS` + `word_timings/*.txt`), keep-out zones on Jesus’ face. The owner rules list these; the methodology largely cannot enforce them.

8. **Biblical accuracy / headcount / face consistency** — the plan treats them as first-class rules but gives no alignment json, scene plan, or character refs. Ep08 alone has multiple shipped variants (`CAN_ANY_GOOD_THING_final_epic_sfx.mp4`, etc.). **1 fps frame grabs cannot CONFIRM headcount or identity**; findings will be mostly SUSPECTED, yet the output schema pushes CONFIRMED with frame paths.

9. **“CONFIRMED … give the frame path”** with **“into %TEMP%”** — evidence is **not reproducible** across reviewers or a second pass. The repo already commits compare stills in places (e.g. ep08 `uplift/review_frames/`, `_quality_uplift_20261116/design_swirls/audit/sheet_*.jpg`). The plan chooses ephemeral temp paths instead.

10. **Comic uplift has no `check_uplift.py`**. `build5.log` in `visual/uplift_v1/` says stills/panel gates were **grandfathered / skipped**. The plan applies the same Swirls-heavy rule set (e.g. “Swirls: blue/gold ink motif must NEVER be animated”) to a **livingpage comic grid** without a comic-specific gate checklist from `COMIC_UPLIFT_SPEC.md` (grid reuse, `hero_frac3`, slow-mo in `build_livingpage`, panel-variety).

### Over-engineering / cost

11. **Duplication of $0 tooling already paid for**: per-episode `uplift/check_uplift.py` + `gate_report.json`, `make_review.py` → `_REVIEW.html` / `_PILOT_REVIEW.html`, `_quality_uplift_20261116/design_swirls/tools/clip_motion_audit.py`, pre-built audit contact sheets (`audit/sheet_e08.jpg`, etc.). The plan’s “Pull frames … 1 frame/second” for **14 full runs** (~100 min of video) is **high agent token cost** for **lower coverage** than running existing gates first.

12. **Missing repo-wide verify steps** the owner already treats as binding: `check_landing_hold.py` (INV-26, 3.0 s hold), and for comic `#7` optionally `panel_variety_lint.py` / `visual_tags.json` (per `CLAUDE.md`). None appear in **Owner rules** or **How**.

### Missing steps / verification gaps

13. No **mandatory first step**: `.venv\Scripts\python.exe uplift\check_uplift.py` (Swirls/JL) and record FAILs before subjective comparison.

14. No instruction to read existing **`gate_report.json`** or owner **`_REVIEW.html`** side-by-sides — yet the plan says **“Do not trust any builder note”**, which encourages ignoring the very artifacts built for adversarial review (`make_review.py` embeds gate table + old/new still pairs).

15. **“Marks tied to the spoken word”** — plan cites `narration.md` but not `narration.alignment.json`, `word_timings/ep*_words.txt`, or `held-breath`-style silence logic. Visual-only 1 s sampling cannot verify timing.

16. **“No stretched clips”** — reviewer eyeball at 1 fps is unreliable; the deterministic check is `G-SLOT` + grep of `cut_uplift.py` for `tpad|reverse|zoompan|setpts` (already in `check_uplift.py`). Plan never mentions source-level verification.

17. **Output “NEEDS PAID FIX” with “rough $”** — no pointer to `spend_summary.json` in uplift folders or the project `cost` skill / spend ledger discipline. Estimates will be invented.

18. **Scope drift in the intro**: “every piece lands on Jesus” is not in the **Owner rules** block; this pack is visual QC only — no `narration_gate.py`, no `bible-check`, no `independent_review.py` on narration. Doctrinal regressions in **unchanged audio** are out of scope but not stated.

### Reuse verdict

The plan **reimplements** frame extraction and partial audio check instead of **layering**: (1) run `check_uplift.py`, (2) read `gate_report.json`, (3) use `make_review.py` anchor times + `uplift.json` shots, (4) use existing audit sheets for regression, (5) Vision only on FAIL slots and doctrine/headcount claims. As written it is **worse coverage, more work**.

---

VERDICT: REVISE  
TOP FIXES:  
1. Add a mandatory Step 0: run each folder’s `check_uplift.py` (where it exists), ingest `gate_report.json`, and treat deterministic FAILs as blocking before any 1 fps Vision pass.  
2. Replace hand-wavy “extra around every cut” with shot boundaries from `uplift.json` / `make_review.py` curated times, and require CONFIRMED evidence under the episode’s `uplift/review_frames/` (or equivalent), not only `%TEMP%`.  
3. Split film #7: comic-specific procedure (`visual/uplift_v1/`, `livingpage_short` spec, `COMIC_UPLIFT_SPEC.md`, `check_landing_hold.py`, panel/grid rules) and clarify LOCKED ep08/ep13 as advisory-only vs overridable.
