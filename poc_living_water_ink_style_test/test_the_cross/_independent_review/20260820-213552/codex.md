# Independent review — codex (OK, 243s)

**Findings**

1. **Line 21, “Strict schema… drops in clean” is only syntactically true.** `pipeline/series.py` loads strings; it does not enforce motif rules, source-series provenance, status, style, or dosage. The plan then claims line 131’s “$0 lint can check every OT page’s dosage line,” but no such dosage field or linter exists.

2. **Lines 137, 146, 177: “Long-form… untested” is contradicted by the repo.** Existing long-form artifacts include `longform/01_Isaiah_53_Suffering_Servant`, `longform/03_The_Passover_Lamb`, and `longform/04_The_Bronze_Serpent`; line 17 itself says Bronze Serpent long already shipped in inked style. The plan needs a precise style boundary or it is misclassifying known evidence.

3. **Line 151, “~$22-30/episode” for long-form is not credible against ledger history.** Ledger totals I found: Passover long ≈ `$45.10`, Bronze Serpent ≈ `$90.01`. Even shorts range widely: Look and Live ≈ `$17.72`, Storm ≈ `$46.46`. The cost model needs real estimator rows and regen scenarios, not a flat optimistic range.

4. **Line 17, “the swirls short is new content, not a remake,” conflicts with existing Look and Live production.** `poc_living_sketchbook/look_and_live` already contains a Bronze Serpent short with final/captioned/scored outputs. Line 104 also labels Look and Live “new.” This needs an explicit reuse/remake policy, not just “dual-home.”

5. **Line 86/178 gives the wrong review invocation.** `independent_review.py --type plan` omits the required artifact argument. Actual shape is `independent_review.py "<plan.md>" --type plan`. For a producer handoff, this matters.

6. **Lines 160 and 164 use slash-command workflow as if it were repo tooling.** `/narrate`, `/voice`, and `/narrate-long` are not the executable commands documented in the repo; the repo points to `cli.py`, `cli_visual.py`, `cli_assemble.py`, `cli_livingpage.py`, and `python -m pipeline.cost`. The plan should name real commands or clearly mark slash commands as operator shorthand.

7. **Multi-reference episodes will not automatically survive into visual planning.** Lines 45-76 rely on `refs` arrays, but `pipeline/handoff.py` writes only `episode.title` and `primary_ref` into `narration.creation.json`, and `visual_runner` reconstructs `refs` from the primary ref only. Talitha, Exodus 3-4, Passover, and OT→NT pair planning can silently lose supporting passages.

8. **Line 110, “No motif is ever decoration — each one cites its verse,” overstates the grounding.** Examples: line 105 “Nicodemus’s careful night-questions = FR1,” line 103 the prodigal “D2 turning” geometry, and line 107 “STAIN on EVERY doorstep” are interpretive motif placements, not direct textual statements. They may be defensible, but not as currently claimed.

9. **Line 157, “each build adds exactly one new risk,” is false.** Build 5 bundles two episodes, first OT entry, first crowd-scale Stain, shared composition, and first Stage-cap test. Build 6 bundles first long-form claim, 16:9 risk, Focal Tour economy, DEAD INK at length, and new cost assumptions.

10. **Lines 147/151 conflict with existing motion discipline.** “Focal Tour as a primary treatment” and “Real clips on hero spreads only” undercut the project’s current default that real motion is expected, with Focal Tour as gap-fill in the same POC notes. If this is a policy change, it needs explicit approval and a test gate.

VERDICT: REVISE
TOP FIXES:
1. Add real structured motif/dose/source/status fields plus a deterministic linter before claiming Stage-cap enforcement.
2. Reconcile the plan against existing Look and Live, Passover, Bronze Serpent, and Isaiah 53 artifacts, including reuse/remake policy.
3. Replace optimistic spend ranges and shorthand commands with ledger-backed estimates and exact executable repo commands.
