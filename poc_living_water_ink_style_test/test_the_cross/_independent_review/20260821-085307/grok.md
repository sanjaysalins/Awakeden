# Independent review — grok (OK, 123s)

I'll verify the plan's claims against the real codebase — series schema, existing skills/pipelines, and what's actually validated — before writing an adversarial review.Found prior panel notes on this same plan — now checking the concrete gaps they flagged against the live code and artifacts.## Adversarial review — Swirls of Life series plan

Default stance: treat every “validated / drops in clean / proves X / ~$Y” claim as guilty until the repo proves it. Several do not.

---

### 1. Feasibility — pipeline gap the plan papers over

**Claim (build 2):** *“run the whole pipeline: /narrate → /voice → pages → cut → landing-hold → captions.”*

**Reality:** Every asset this plan leans on lives as one-off scripts under  
`F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\test_the_cross\`  
(`render_the_hem.py`, `render_the_thomas.py`, `render_the_storm_f06.py`). There is **no** `swirls` / storyboard-page entry in `config.py`’s `STYLE_REGISTRY`. `cli_visual.py` / SP-G* / AS-G* operate on scene stills, not baked-title / 3-panel / big-illustration pages.

So “full series episode through the production pipeline” is not a production step — it is an **unscoped engineering project**. Section 6’s risk table never names that. Same-day `RESUME.md` already flags it as the biggest finding; this artifact still hands the producer a spend path as if the path exists.

Slash commands (`/narrate`, `/voice`, `/narrate-long`) are operator shorthand, not the documented executables (`cli.py`, `cli_visual.py`, `cli_assemble.py`, `cli_livingpage.py`). For a “hand to producer” doc, that is a real failure mode.

---

### 2. “Strict schema… drops in clean” — syntactically true, operationally false

**Phrase:** *“Strict schema — `pipeline/series.py` reads only these keys, so it drops in clean.”*

`pipeline/series.py` only loads string fields. It does **not** store motif, dose, form (SHORT/LONG), status, source-series id, or Stage-cap. Those are stuffed into free-text `theme` strings.

Then section 3 claims: *“a $0 lint can check every OT page’s dosage line before a credit is spent.”*  
There is no dosage field and no linter. You cannot gate what you never modeled. Committing this JSON now does not enforce Stage-cap; it only narrates it.

Side effect not named: `render_series_library()` injects **every** series into the cached narration system prompt. Pasting this entry grows every future `/narrate` call project-wide and busts the prompt cache. Not inert.

---

### 3. “Validated” collapses three different readiness states

| Plan label | What actually exists |
|---|---|
| Ep 01 “shipped… finished 69s… proof it works end-to-end” | John 4 northstar cut; same-day notes call it a **proof cut**, not LOCKED — no standing SFX/captions/panel lock, AS-G6/G7 not enforced |
| Ep 02 “2 pages validated” | Hem F04/F05 pages only — not a narration, not a full short |
| Ep 03 “F01 validated” | User already rejected F01 swirl legibility on watch; section 6 admits it, table still says “validated” |
| Ep 04 “F06 validated” | Storm/water page only; **Fray on disciples is explicitly still open** (build 3) |

A producer scanning the slate table will over-read readiness. Split the column or stop using one word.

---

### 4. Look and Live is not “new content”

**Phrase:** *“the swirls short is new content, not a remake”* / table Status **“new”** for ep 11.

`F:\slk\PycharmProjects\JesusInTheBible\poc_living_sketchbook\look_and_live\` already has a finished short (`LOOKANDLIVE_living_sketchbook_cc_scored_sfx.mp4` and full assemble/caption/score chain). Dual-home does not answer remake/reuse. Without an explicit “archive sketchbook / remake in swirls / or leave Look and Live alone” rule, build 5 risks paying twice for the same Numbers 21 beat under a different brand.

Long-form “entirely untested in this style” is also slippery: Passover / Bronze Serpent / Isaiah longs already exist in other inked/sketchbook registers. Say **swirls storyboard-page format**, not “long-form.”

---

### 5. Cost model is not credible — and same-day spend already undercuts it

**Claims:** shorts *“~$12–18”*, longs *“~$22–30”*, build 2 *“~$10–14”*, build 6 *“~$22–30”*.

Against ledger / handover reality:
- Comparable longs landed far higher (Passover ~$45, Bronze Serpent ~$90 in prior review notes).
- John 4 POC alone logged ~$33 in one day.
- Same-day HF reconciliation: **~$95 unexplained / under-attributed** Kling volume (`RESUME.md`). Every per-render quote that assumes “one bill per render” is suspect until that is diagnosed.

Handing a producer optimistic ranges **before** fixing unexplained spend is how you double-burn the budget on builds 2–6.

Also: shorts say “every shot gets a real AI clip”; long section then pivots to “Focal Tour as primary… real clips on hero spreads only (~1/3).” That undercuts the north-star default and needs an explicit policy + gate, not a quiet cost patch.

---

### 6. “Each build adds exactly one new risk” is false

**Phrase (section 5):** *“Sequenced so each build adds exactly one new risk.”*

- **Build 5:** two episodes + first OT + first crowd-scale Stain + shared composition rhyme + first Stage-cap watch-test.
- **Build 6:** first long + 16:9 at scale + per-movement dose + Focal-Tour economy + DEAD INK at length.

That is bundled risk, not one-at-a-time. Call it what it is, or split the builds.

---

### 7. Motif / doctrine — the Stain’s “home story” fights the plan’s own guardrail

**Guardrail:** *“Never assign a motif to suffering or illness the text does not call sin (John 9:3)”*  
**Ep 02:** Stain on the hemorrhaging woman (Mark 5:25–34) as *“12 years unclean.”*

Mark 5 never calls her condition sin. Ritual uncleanness ≠ moral guilt. The plan expands Stain to “sin/guilt/uncleanness” via Isaiah 1:18 / Psalm 51:7 (moral-sin metaphors) and then makes Mark 5 the **flagship** Stain story. That is the single most load-bearing motif assignment in the slate, and it is the weakest textual fit under the plan’s own John 9:3 discipline.

Other “each one cites its verse” overclaims:
- Nicodemus questions → FR1 (interpretive)
- Prodigal “home-side edge already dried… great way off” (geometric invention)
- “STAIN on EVERY doorstep, Israelite and Egyptian alike” (Exodus does not say that)

Defensible as art direction after panel review — not as currently claimed “textually grounded / never decoration.”

Isaiah 53 “Stain touches Christ” exception is correctly flagged as heavy — but it is already written into the paste-ready `guardrails` string **before** any dried-ring inventory exists. Do not hard-code the exception into catalog text until the season actually has rings to transfer.

---

### 8. Missing steps / single points of failure

1. **No decision gate before spend:** prove page-format through real gates **or** explicitly budget hand-rolled production + the engineering to wire it — then spend.
2. **Talitha Cumi** is sold as free Hem continuity (*“shared street, crowd, refs”*) but is **absent from the next six builds**. Expanding Hem now without a shared-ref / continuity contract burns the “for free” claim.
3. **Multi-`refs` loss:** `pipeline/handoff.py` writes only `title` + `primary_ref` into `narration.creation.json`. Talitha (two Mark chunks), Exodus 3–4, Passover, serpent pair can silently drop supporting passages in later visual planning.
4. **Dual-home “never two styles at once”** has no enforcement (board check, slug lock, release_state field). Policy-only.
5. **Season dried-rings → Isaiah payoff** needs eps 2,7,8,9,10,11 shipped; the six-build plan only partially advances that chain. Fine if stated as multi-season architecture — not if “season finale” language implies this slate closes soon.
6. **Commit-15-episodes-now** is premature catalogization before one full swirls episode clears narration + voice + pages + cut + landing-hold + captions under standing gates.

---

### 9. Reuse vs duplication

The plan correctly reuses series.json shape and existing catalog titles. It does **not** reuse:
- living-sketchbook Look and Live assets (remake ambiguity)
- production runners (`cli_visual` / assemble gates)
- any existing Stage/dose linter pattern (bible-check / panel_variety_lint style) — it only promises one

Hand-rolled `test_the_cross` scripts will keep spawning per episode unless wiring is scheduled. That is duplication by inertia.

---

### 10. What is actually solid (brief, not praise)

Own-series framing for grammar teaching is coherent. OT→NT Stage-cap *idea* matches the project spine. Sequencing Thomas → Hem before water/Fray escalation is sensible. Risks section is more honest than the episode table — the table and cost claims undo that honesty.

---

VERDICT: REVISE  
TOP FIXES:  
1. Add an explicit pipeline-integration decision **before** any build-2+ spend: wire swirls pages into real gates, or formally scope builds as hand-rolled + cost the engineering separately; name real CLI commands.  
2. Replace optimistic $ ranges with ledger-backed estimates **after** diagnosing the unexplained HF spend; stop treating John 4 / Hem pages / F01 / F06 as interchangeable “validated.”  
3. Fix catalog truth before paste: Look and Live remake/reuse policy; structured motif/dose fields + real Stage-cap lint (or drop the lint claim); resolve Mark 5 Stain vs John 9:3 guardrail; do not commit the Isaiah-53 Christ-Stain exception into series.json until the season has rings.
