# Independent review — codex (OK, 176s)

**Findings**

1. **Governance command is wrong as written.** The plan says run `independent_review.py --type plan`, but the actual tool requires a positional artifact path: `independent_review.py "<plan.md>" --type plan`. As written, this gate fails before reviewing anything.

2. **“/narrate → /voice → pages → cut” and `/narrate-long` are not evidenced as executable workflows.** The repo has `cli.py`, `cli_pipeline.py`, `pipeline/orchestrator.py`, and long-form scripts, but not the slash commands the plan names. The claim “run the whole pipeline: /narrate → /voice → pages → cut → landing-hold → captions” is producer prose, not an executable build path.

3. **“Paste-ready series.json entry” is misleading.** `data/series.json` is a top-level object with a `"series"` array; the shown JSON object is only an array element. The plan’s phrase “so it drops in clean” omits the actual insertion point, comma discipline, and validation step.

4. **The Stage-cap lint is invented or at least not wired.** The plan claims “a $0 lint can check every OT page’s dosage line before a credit is spent,” but I found general `render_lint` checks, not a Stage-cap/OT-type dosage validator. This is a false safety claim until a concrete lint rule, input format, and CI/command are specified.

5. **The “4 of 15 already carry validated work” claim overstates readiness.** “My Lord and My God” has “F01 validated, F02 pending”; “Peace Be Still” has one validated storm page; “The Hem” has two validated pages, not a full episode. That is component validation, not episode validation. The plan should not treat eps 1-4 as comparable “tested ground.”

6. **Long-form cost is under-justified.** The plan estimates “~$22-30/episode” for 20-26 spreads while also admitting long-form is “entirely untested,” uses 16:9 at scale, needs references, regens, panel review, hero clips, audio, assembly, and QC. The repo’s budget ceiling is real, but this range is not backed by a per-operation quote.

7. **It duplicates catalog concepts without specifying release-state semantics.** The “Dual-home policy” says overlap is fine and “theme string names the source series,” but the loader treats `theme` as plain text. There is no structural link, no duplicate prevention, no source-series relation, and no rule for website/release state treating style variants as distinct products.

8. **The plan builds a season-level theology payoff before proving viewer comprehension.** Claims like “Every ring in the season was an IOU” and “A viewer who has learned the language sees that Stage 3 never came” assume the audience understands the grammar. The only stated verification is muted-watch motif placement, not viewer comprehension across episodes.

9. **The riskiest doctrinal visual is deferred but not operationalized.** “full independent panel sign-off required” for Stain touching Christ is not defined: who signs, what artifact they review, what failure blocks, and whether this is separate from `independent_review.py`. This is the highest-risk page and has the loosest process.

10. **Reuse is discussed as theme overlap, not asset/pipeline reuse.** The plan does not say how it reuses existing long-form/short-form assets, references, clip libraries, scene plans, or existing long-form infrastructure. It risks rebuilding a parallel POC production lane under `poc_living_water_ink_style_test` instead of integrating with `cli_pipeline.py`/orchestrator and existing gates.

VERDICT: REVISE
TOP FIXES:
1. Replace prose/slash-command workflow claims with exact repo commands, paths, required artifact inputs, and validation commands.
2. Add real gates for Stage-cap/dosage, duplicate/source-series handling, and the Stain-touches-Christ sign-off.
3. Rework cost/readiness claims from per-operation quotes and clearly separate component tests from full-episode validation.
