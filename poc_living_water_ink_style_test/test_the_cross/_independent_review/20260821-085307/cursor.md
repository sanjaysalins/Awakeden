# Independent review — cursor (OK, 83s)

## Independent adversarial review — Swirls of Life series plan

I checked this against `pipeline/series.py`, `pipeline/handoff.py`, `pipeline/visual_runner.py`, `data/series.json`, `data/spend_ledger.jsonl`, the swirls POC tree, `cli_livingpage.py`, and existing long-form / living-sketchbook artifacts.

---

### Critical — feasibility / false assumptions

**1. Build 2–6 assume a production pipeline that does not exist (Section 5, line 160; Section 4, line 137).**

Build step 2 says: *"run the whole pipeline: /narrate → /voice → pages → cut → landing-hold → captions."* In the repo, validated swirls work lives entirely in `poc_living_water_ink_style_test/` as one-off scripts (`render_the_hem.py`, `render_the_thomas.py`, `render_the_storm_f06.py`, `northstar_shortform/assemble.py`). None of it goes through `cli_visual.py` / `cli_assemble.py`, `STYLE_REGISTRY`, SP-G1–G9, or AS-G6/G7. A swirls **page** (baked title, F##, three sketch panels, one hero illustration) is structurally different from a Baroque **scene** in `scene_plan.json`.

`RESUME.md` explicitly notes this format is *"not wired into the production pipeline."* Section 6’s risk table never names this gap, yet it gates roughly **$80–100** of planned spend. That is the plan’s largest unaddressed failure mode.

**2. The Stage-cap law claims deterministic enforcement that does not exist (Section 3, line 155).**

*"It's also deterministic — a $0 lint can check every OT page's dosage line before a credit is spent."* There is no dosage field in `series.json`, no page-level metadata schema, and no linter in the repo. Motif, dose, source-series, and status are all crammed into free-text `theme` strings (lines 45–76). `pipeline/series.py` loads those strings but enforces nothing about Stain/Fray/Stage caps.

**3. Multi-ref episodes will silently lose supporting passages downstream (JSON block lines 45–76; `visual_runner.py` lines 91–98).**

Episodes like Talitha Cumi (`refs`: Mark 5:21-24 + 35-43), Exodus 3–4, and the serpent pair depend on wide refs. But `pipeline/handoff.py` writes only `title` + `primary_ref` into `narration.creation.json`, and `visual_runner._episode_from_creation()` reconstructs `refs` as `[primary_ref]` only — with an inline comment that the episode block is *"mainly cosmetic."* The plan’s sandwich/interleaving logic (line 105, Talitha + Hem) will not survive into scene planning unless handoff is fixed or every piece gets a custom `creation.json`.

**4. "Strict schema — drops in clean" (line 21) is JSON-parse true, operationally false.**

Committing the entry injects the full concept/guardrails block into **every** future `/narrate` call via `render_series_library()` — a cross-project prompt-cache side effect the plan never mentions.

---

### High — "validated" / "shipped" overstated

**5. Ep 01 "The Well" — "shipped" (table line 96) is POC-only, not catalog production.**

The finished film is `poc_living_water_ink_style_test/northstar_shortform/` (report: **68.86s**, not ~59s). It is not in `data/series.json`, not in `PythonProject1/jesus/narration/`, and not wired to release/manifest tooling. Calling it the series pilot overstates production readiness.

**6. The Status column collapses three different axes (Section 2 table, lines 96–99).**

- **Thomas (ep 03):** "F01 validated" — but Section 6 admits swirl placement *"doesn't read on watch"* and build 1 is explicitly to fix it.
- **Peace Be Still (ep 04):** "F06 validated" — only storm/water rendering; build 3 still opens *"Fray on multiple figures"* as untested.
- **Look and Live (ep 11):** table says **"new"** (line 104) while `poc_living_sketchbook/look_and_live/` already has a LOCKED-narration, voiced, assembled Bronze Serpent short — different visual style, same text family. That directly conflicts with dual-home line 17: *"never produce the same episode in two styles at the same time."*

**7. Long-form "entirely untested in this style" (Section 4, line 146) misclassifies existing evidence.**

`longform/03_The_Passover_Lamb` and `longform/04_The_Bronze_Serpent` exist; ledger history shows Passover long ≈ **$45+** and Bronze Serpent ≈ **$90+** — not the plan’s **$22–30/episode** (line 151). The plan needs a precise style boundary: living-page/inked long-form ≠ storyboard-page swirls long-form. Without that, build 6’s "first long-form test" claim is wrong and the cost model is fantasy.

---

### Medium — hidden risks / missing steps

**8. Season-level "dried rings" arc (Section 3, lines 157–158) has no implementation path.**

Episodes 2, 7, 8, 9, 10, 11 each end with a dried ring; ep 15 pays them off on Christ. That requires cross-episode visual asset continuity, a ring registry, and finale compositing rules. None of that appears in the six-build sequence or any data model — only narrative intent.

**9. Mark 5 sandwich continuity (line 105) is promised without a ref/asset plan.**

*"shared street, crowd, and refs"* / *"cross-episode continuity for free"* assumes matching environments across Hem and Talitha. The swirls skill mandates per-episode ref chaining; shared street/crowd is not free — it is expensive identity-lock work the plan never budgets or sequences.

**10. John 8 episode (lines 57–59, table line 102) ignores a known project guardrail.**

`PRODUCTION_PLAN.md` already flags the pericope adulterae textual-variant issue. The series `guardrails` string (line 54) does not add episode-specific handling. For a KJV-strict, fail-closed engine, greenlighting ep 09 without an explicit textual policy is a doctrine/review landmine.

**11. Motif-to-verse grounding is overstated (line 110).**

Several assignments are interpretive, not textual:
- Nicodemus *"careful night-questions = FR1"* (line 105) — wonder/confusion, not clearly James-1:6 doubt.
- Prodigal *"D2 turning variant"* (line 103) — geometry trick, not a verse-cited Stain placement.
- Passover *"STAIN on EVERY doorstep"* (line 107) — theological illustration, not something Exodus states as guilt-stain on Israelite doors.

Defensible maybe; not as claimed.

**12. Long-form motion policy conflicts with shorts default (Section 4, lines 147 vs 151).**

Shorts: *"every shot gets a real AI clip by default."* Longs: *"Real clips on hero spreads only (~1/3); Focal Tour as a primary treatment."* The swirls skill (`SKILL.md` step 0) says real motion is the shorts default and Focal Tour is gap-fill. If this is a policy change for swirls long-form, it needs explicit approval and a test gate — not a buried ratio in section 4.

**13. "Each build adds exactly one new risk" (line 157) is false.**

- Build 5: two episodes, first OT entry, crowd-scale Stain, shared compositions, Stage-cap test.
- Build 6: first long-form, 16:9, Focal Tour economy, DEAD INK at length, new cost assumptions.

---

### Medium — reuse / duplication

**14. Plan duplicates ad-hoc POC scripts instead of naming a reuse path.**

`cli_livingpage.py` + `livingpage_short.spec.json` already orchestrate a related (though not identical) page-based format for living-sketchbook pieces. `northstar_shortform/assemble.py` is the only end-to-end swirls assembly proof. Build 2 should explicitly fork one of these as the template — not imply `/scene-plan` → `/stills` → `/assemble` work out of the box.

**15. Slash commands are not executable repo entry points (Section 5, line 164; build steps).**

`/narrate`, `/voice`, `/narrate-long` are skill shorthand. Actual commands are `cli.py`, `cli_lock.py`, `per_turn_synth.py`, `python -m pipeline.cost`, etc. A producer handoff that omits real commands will misfire.

**16. Governance invocation is wrong (line 86).**

*"run `independent_review.py --type plan`"* omits the required artifact path. Actual shape: `independent_review.py "<plan.md>" --type plan`.

---

### Cost / spend

**17. Per-episode estimates are optimistic and incomplete (Section 4, lines 141–142, 151; Section 5 dollar ranges).**

- Shorts **$12–18** ignore regen loops visible in ledger (e.g. `LS_Storm` living-sketchbook short with 13 stills + 13 clips + retries ≈ **$46** class spend).
- Longs **$22–30** contradict ledger-backed Passover/Bronze Serpent totals (~2–4× higher).
- Build estimates cover art/audio only — no Opus narration tournament + 6-panel + red-team + 5-CLI panel (~**$5–6/episode** elsewhere in the cost model).
- Stills math assumes **8 × ~$0.30** but swirls skill locks **`nano_banana_pro`**, and ref-chained regens are common in POC scripts.

**18. Fifteen-episode slate before one full swirls episode ships through any stable runner is premature scope.**

Section 5 wisely sequences six builds — but Section 1 already commits a full `series.json` entry with 15 episodes, season arcs, and finale doctrine (Isaiah 53 Stain-on-Christ, line 75) before build 2 proves a single complete short.

---

### What the plan gets right (for balance)

- `series.json` key set matches `pipeline/series.py` dataclasses.
- Cross-series overlap citations (Encounters, Miracles-as-Signs, etc.) check out against `data/series.json`.
- Sequencing Isaiah 53 **after** Passover long and dried-ring accumulation is sound editorial logic.
- Section 6 honestly names swirl legibility, Fray escalation, and 16:9 risks — though it misses the pipeline-integration gap.

---

VERDICT: REVISE
TOP FIXES:
1. Add an explicit pipeline-integration decision before build 2 spend: either wire swirls pages into a real runner (fork `northstar_shortform/` or extend `cli_livingpage.py`) or scope builds 2–6 as continued POC scripts with that engineering costed separately — and put this in Section 6’s risk table.
2. Reconcile the slate against existing artifacts (Look and Live short, Passover/Bronze Serpent/Isaiah 53 longs): define reuse vs remake policy, fix the ep 11 "new" label, and replace $22–30 long-form estimates with ledger-backed ranges including narration Opus spend.
3. Stop claiming Stage-cap enforcement until structured dose/motif/status fields and a real linter exist; fix `handoff.py`/`visual_runner.py` ref loss before committing multi-ref episodes like Talitha, Exodus 3–4, and the serpent pair.
