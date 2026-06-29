# Independent review — cursor (OK, 79s)

## Independent adversarial review — Inked-Style Guardrail Plan

### Feasibility vs. real codebase

**The plan describes integration work as if the guardrails mostly exist; they do not on the inked path.**

- **“Fix: the inked default pipeline RUNS `bible_kb` on every piece (not optional, not bypassable)”** (§2) — `bible_kb.gate()` is only called from `longform/_animate_16x9.py` and `longform/_animate_directional.py`. EW04 POC scripts under `longform/_style_poc/ew04/` never import `bible_kb` or `bib_validate`. Shorts paths (`pipeline/visual_runner.py`, `longform/_hf_animate_short.py`, `pipeline/video_render.py`) have no bible gate. “Not bypassable” also contradicts `bible_kb.gate()` itself, which skips on `BIBLE_GATE=off`, `.bible_gate_exempt`, and any piece with no `_bible_check/` unless `BIBLE_GATE=strict`.

- **“Consolidated pipeline flow”** (flow block) assumes a single inked default pipeline — the repo still ships Baroque/NBP+Kling via `cli_visual.py` / `pipeline/visual_render.py` / `pipeline/video_render.py`. `seedream_v4_5` and `cinematic_studio_video_v2` exist only in `longform/_style_poc/` hand scripts, not in the production providers. Switching default style is not “wire guardrails”; it requires new/changed `ImageProvider` + `VideoProvider`, config, and skills.

- **“audit still BOTH ways: facts (bible_kb Vision) + identity (matches grid)”** (flow block) — the second half is **not implemented anywhere**. `verify_biblical_accuracy()` checks facts vs. image; `verify_image()` checks subject_block vs. image (and hardcodes **Baroque oil** — see `pipeline/visual_render.py` lines 389–415). Nothing compares a rendered still to a `ref_library` anchor/grid.

- **§2 claim that `bible_kb` “PANELs the facts” as enforced truth** — `check_status()` explicitly says the 5-CLI panel verdict is **not** a hard gate; only deterministic checks + recorded `.bib_audit.json` sidecars gate GREEN (`pipeline/bible_kb.py` ~739–741). The plan overstates panel enforcement.

### Hidden risks & false assumptions

**EW04 diagnosis is partly wrong, which weakens the proposed fixes.**

- **“used the reference index (`ref_library`) only loosely”** (Context) — EW04 render scripts *do* pass `ref_library` PNGs as `--image` on every scene (`render_ew04_stills.py`, `render_ew04_stills_b.py`). The caduceus/nail/tattoo failures happened **with anchors attached** and with shape negatives already on `BRONZE_SERPENT_STANDARD.json`. The gap is not “no lookup-before-render”; it is weak prompt wording + Vision audits that miss iconographic failures. A coverage rule alone would not have prevented EW04’s caduceus pass.

- **“Vision audit passed the caduceus, the nails, the roped wrists”** (Learning 3) — true and damning — but the plan’s fix stack (more Vision + human Read + prompt lint) does not explain **why** `bible_kb` would catch these. Calibration (`bible_kb/_calibration/labels.json`) is 8 EW01 goat scenarios; zero labels for caduceus, crucifixion nails, neck-snake, roped wrists. Routing through `bible_kb` without extending calibration/fact templates replays the same blind spot.

- **Guardrail 3 internal contradiction:** §3 says `cinematic_studio_video_v2` “over-animates faces/mouths on dialogue beats (confirmed on EW04)”, but EW04’s own `animate_ew04.py` motion prompts for talking beats already use frozen-tableau language (“sit still… as they speak”), and the POC bake-off (`PASS2_RESULTS.md`) rated the same model as “rock-steady faces” on close-ups. The open question admits SUBTLE is “unproven” — that should block calling Guardrail 3 a fix, not bury it in risks.

**Unify-by-slug is underspecified and likely churn-heavy.**

- Proposed unified card uses slug `MOSES` with `truth.scripture: ["Numbers 21:4-9"]` — but `bible_kb/` today has **no `characters/` entities at all** (only `customs/`). Slug namespaces differ: `ref_library` uses `MOSES` / `JESUS`; `bible_kb` uses kebab-case entity slugs on **facts** (`day-of-atonement`, `aaron-high-priest`). “Migration: merge by slug; nothing regenerated” (Key architectural decision) hand-waves a schema merge (`FactCard[]` truth vs. flat `look`/`truth` blocks) with no migration script, no conflict rules, and no answer to the plan’s own open question about look rerolls touching verified-fact files.

### Over-engineering / build-before-proof

- **Unifying `bible_kb/` + `ref_library/` before either gates production** is premature. `ref_library` has 6 EW04 cards; `bible_kb` character/object/places dirs are nearly empty. You could prove Guardrails 1–2 by wiring existing `ref_library` lookup + `bib_validate.py` into one inked render driver **without** a unified schema. The merge adds migration risk before the simpler path is proven.

- **New “prompt lint”** (Learning 1) duplicates mechanisms already present: object cards carry caduceus bans, `enrich_for_scene()` folds `banned_anachronisms`, and scene prompts already paraphrase physically. EW04 still failed. A lint layer without deterministic iconography checks (caduceus vs. bronze serpent-on-pole) is likely another LLM-ish band-aid.

- **“identity (matches grid)” audit** adds a third Vision pass on top of `verify_image` + `verify_biblical_accuracy` — expensive, correlated failure modes, no calibration plan.

### Missing steps, edge cases, verification gaps

| Plan step | Gap |
|---|---|
| “renderer must QUERY the index first” (§1) | No entity extraction step: who decides which scene-plan nouns require a registered card vs. generic extras? |
| “mint the grid, get human approval, register” (§1) | No workflow, cost estimate, or SLA for first-encounter entities; coverage rule can stall every new witness/episode. |
| “content-hash idempotence” for animation (Learning 2) | Correct problem — EW04 uses `if dest.exists(): skip` (`animate_ew04.py` ~91). But plan doesn’t note `bible_kb` already hash-binds **still audits**, not clips; no sidecar spec for clip/still binding. |
| “assemble to mp3 length; minterpolate long holds” (flow) | `minterpolate` exists only in `assemble_ew04.py`; main assembly (`pipeline/assembly_*.py`) doesn’t inherit this. |
| Learning 4 topical-fit reuse | `pipeline/clip_reuse.py` + `hero_library` topical-fit audits already exist; plan treats reuse as a learning, not a **reuse** of existing tooling. |
| Style rollout | No step to rewrite `verify_image`’s Baroque-specific audit rubric for inked graphic-novel — shipping inked stills through current audit would fail good frames or pass wrong ones. |
| Ship-time enforcement | No bible gate at assembly/publish (`cli_assemble.py`, `cli_publish.py`) — animate-only gate still allows shipping stale/wrong stills if animate is hand-run. |
| Shorts vs eyewitness | EW04 is eyewitness-format; plan doesn’t say how inked defaults interact with `witness-world` skill (still points at `image_library` + NBP/HF Baroque path). |
| Tests / validate | Plan doesn’t require extending `test_bible_kb*.py`, calibration labels, or `/validate` wiring for inked-specific failures before LOCK. |

### Reuse / duplication

The repo already has **four** visual reuse banks with overlapping intent:

- `image_library/`
- `_hero_library/` (`pipeline/hero_library.py`) — wired for shorts reuse, topical-fit LLM audit
- `ref_library/` — EW04 inked anchors (POC-built)
- `bible_kb/` — scriptural truth

`TODO.md` already queues unifying `image_library` vs `_hero_library`. This plan adds a **fifth conceptual layer** (unified slug card) without reconciling `hero_library` or `witness-world`’s “REUSE CHECK FIRST → `image_library`” step. That is duplication, not consolidation.

### Cost / spend justification

- **“Happy-path cost: ~93.5 credits… animation = 88%”** — arithmetic is plausible (11×7.5 + ~11×1), but the plan never maps HF credits to the project’s `$23/episode` model, never compares to current Kling-short economics, and never budgets **grid minting** (§1 wants ¾/profile/expression rows per hero — potentially dozens of seedream jobs before the first scene renders). Guardrail 1 can dominate cost on new series.

- **SUBTLE/DYNAMIC paid test** is correctly flagged as an open question — good — but Guardrail 3 is still listed as a deliverable before that test, which violates the project’s own “test-gate-before-batch” rule.

### Specific line/phrase callouts (skeptical read)

1. **“PROPOSAL, pre-build… guardrails exist”** — partially false: `bible_kb`, `bib_validate`, `bible_gate`, hash-bound still audits, and `enrich_for_scene()` already exist; what’s missing is **inked-path wiring**, audit rubric updates, and calibration for EW04 failure classes.

2. **“Every accuracy defect… caught by a human Reading the frames — NOT by any gate”** — accurate for EW04; underplays that **automated gates also failed** when run (Vision pass on caduceus), so “route through bible_kb” is not sufficient without new fact classes + calibration.

3. **“Cards are written *after* a render (`first_used` is set post-hoc), so the index does not yet *gate* anything”** — true for catalogue metadata, but misleading about EW04 runtime: scripts already require PNG paths; gating is a **policy/engine** change, not greenfield.

4. **“Coverage rule: no named reusable person/object/place is ever drawn without a registered card”** — undefined enforcement; easy to bypass in hand scripts (exactly how EW04 POC works today).

5. **“Reuse is the cost engine… match the *moment*”** — correct insight, but the repo already encodes this in `clip_reuse` scope + topical-fit; plan should say “wire existing `clip_reuse`/hero_library rules into inked animate path”, not rediscover.

6. **Open question: “Does routing every short through bible_kb (built for long-form) fit shorts’ punchier cadence and budget?”** — this is the highest-risk feasibility question and should be **answered before build**, not listed passively. Full derive+panel+audit per 14–20 short scenes is a large Opus/Vision spend vs. one EW04 hand script.

---

VERDICT: REVISE
TOP FIXES:
1. Replace “unify card systems first” with a phased integration spec: inked `ImageProvider`/`VideoProvider` in `visual_render`/`video_render`, wire `bib_validate` + `bible_gate` on the actual shorts/witness animate paths, and update `verify_image` (and calibration labels) for inked failures (caduceus, nails, neck-snake) before any schema merge.
2. Correct the EW04 root-cause analysis: anchors were used; failures were prompt iconography + unc calibrated Vision — specify deterministic checks (or expanded `specified` facts) for known failure motifs, not just “prompt lint” + another Vision pass.
3. Resolve library duplication explicitly: state how `ref_library` relates to `hero_library`/`image_library`, reuse `clip_reuse` topical-fit for Learning 4, and define entity-coverage detection + grid-mint cost/latency before enforcing “no card → no render.”
