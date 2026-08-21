# Independent review — codex (OK, 260s)

**Findings**

1. The core audit claim is false. The plan says “Every one of the 17 candidate passages… confirmed clear” and “The slate — 15 episodes, all newly chosen, all verified clear.” But `data/series.json` already contains “Melchizedek” and “Walking on water,” and `_website/manifest.yaml` has `the-empty-tomb`, `public_status: studio_complete`, sourced from `batches/cluster_02_resurrection/empty_tomb_john208`. That directly collides with #16 “The Name She Knew” and weakens #1/#7.

2. The plan cannot count itself. It says “17 candidate passages,” then “15 episodes,” then lists rows #1-#16, then says “Ratio: 14 shorts : 2 longs.” That is not a cosmetic error for a plan whose purpose is collision clearance.

3. The motif accounting is wrong. “Motif balance: 5 Stain · 5 Fray · 3 swirl-only…” does not match the table: Stain appears on #2, #4, #10, #11, #12, #13 = 6; swirl-only appears only on #1 and #3 = 2.

4. The Stain taxonomy is violated by the slate itself. The rules define Stain as “moral sin/guilt” or “ceremonial/Levitical uncleanness-as-barrier,” but #10 uses “Gentile outsider status” and #13 uses “shame at being served.” Those are new categories, not covered by the stated system.

5. “Build order… first build spends nothing beyond one still” is not a valid proof gate. The swirls skill requires designing the whole shot list before rendering, and the validated northstar short uses 8 shots plus assembly. One still proves neither narration, motif readability, ref chaining, animation, captions, nor final cut viability.

6. “No production pipeline for this format… full deterministic gates deferred” is acknowledged, then underweighted. The swirls pipeline doc says a swirls page is not a `cli_visual.py` scene and final assembly still forks `northstar_shortform`. The cost/build order does not budget that per-episode assembly work or the risk of bypassing existing gates.

7. Multi-reference episodes are a hidden pipeline risk. #6 uses “Mark 5:21-24, 35-43,” #15 uses “Luke 4:16-30,” and #16 uses two John passages, but `pipeline/handoff.py` stores only `title` and `primary_ref`, while `visual_runner` reconstructs `refs` as `[primary_ref]`. The plan does not say how those wider passages survive tooling.

8. The cost model is not decision-grade. It admits “zero ledger evidence for this format’s own long-form yet” but still quotes “2 longs (~$100-190)” and a season total of “$450-920” before regen overruns. That is a soft guess dressed as a season budget.

9. Governance is incomplete. “needs `independent_review.py "<plan.md>" --type plan` + a Fable creative-critique pass… In progress” is not enough; the existing v2 review folder has only partial outputs and no `INDEX.md`, while `independent_review.py` requires a 4-voice healthy quorum.

10. There is a textual-care error in #3: “Pays off one chapter later, in Jesus’s own mouth.” Jacob’s ladder is Genesis 28; the cited payoff is John 1:51, not “one chapter later.” Small, but in a biblical slate plan it is evidence the audit pass was not careful enough.

VERDICT: FAIL
TOP FIXES:
1. Redo the catalog collision audit and publish the evidence inline, removing or explicitly justifying every overlap.
2. Replace the “one still” start with one complete pilot gate: shot list, refs, pages, animation, assembly, captions, review, and measured cost.
3. Fix the episode counts, motif taxonomy, motif balance, multi-ref pipeline handling, and long-form cost assumptions before any `series.json` change.
