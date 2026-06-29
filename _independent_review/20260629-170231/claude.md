# Independent review — claude (OK, 107s)

I verified the plan's central claims against the actual code and data. Findings below cite exact files.

## Findings

**1. The headline architectural decision rests on a factually wrong premise.**
The plan's "Key architectural decision (user-approved): UNIFY THE TWO CARD SYSTEMS BY SLUG" claims both systems are *"already keyed by entity slug (`MOSES`, `BRONZE_SERPENT_STANDARD`)."* That is not true of either system as built:
- `ref_library` cards key by a **`name`** field, uppercase (`"name": "MOSES"` in `ref_library/characters/MOSES.json`). There is **no `slug` field**.
- `bible_kb` has **zero** character/object/place entities. `bible_kb/characters/`, `objects/`, `places/`, `eras/` don't even exist on disk — only `customs/` and `_calibration/` do. Its one populated entity (`bible_kb/customs/day-of-atonement.json`) keys by **`"slug": "day-of-atonement"`** — lowercase kebab, not `MOSES`.

So the two stores use **different field names AND different casing conventions**, and the truth side has nothing to key for the very entities (MOSES, the serpent standard) the plan names. "Both already keyed by entity slug" is the load-bearing claim under a user-approved decision, and it's wrong.

**2. The migration ("nothing is regenerated") is not feasible as written.**
The plan says: *"merge the existing `ref_library` cards with `bible_kb` entities by slug; preserve both PNGs and citations; nothing is regenerated."* There are **no `bible_kb` entity records to merge** for characters/objects/places — they'd have to be **authored from scratch** (era, scripture, customs, visual_directive, banned_anachronisms per slug). "Nothing is regenerated" hides a from-scratch authoring cost for every entity.

**3. Deeper mismatch: bible_kb is SCENE-scoped and per-episode, not a persistent per-entity store.**
`enrich_for_scene(v1, scene_id, ...)` (bible_kb.py:491) reads `<v1>/_bible_check/scene_facts.json` — facts are **derived per scene per episode** via `derive_scene_facts` / `build_episode_facts` (bible_kb.py:289, 318), producing `EpisodeFacts`. `ref_library` look-cards are **persistent, entity-scoped, cross-episode**. These are two different addressing schemes (scene-id vs entity-slug). Folding an episode-derived scene directive into a persistent entity card (the proposed unified `truth.visual_directive`) fights bible_kb's actual data model. The plan's own open question — *"does coupling truth and look create churn"* — understates it: it's not just churn, it's a unit-of-work mismatch.

**4. Guardrail 2 is oversold against the plan's own evidence.**
The plan positions routing through `bible_kb` as closing "the gap that this plan closes." But learning #3 states the Vision audit **passed** the caduceus, the nails, and the roped wrists — i.e. the automated half of bible_kb (`bib_validate`/`bible_gate`) is exactly what *failed* to catch these defect classes. By the plan's own data, what caught them was the human Read. So "route every piece through bible_kb" does **not** close the accuracy gap for these failure modes; the **human checklist (learning #3)** does. Honest framing: bible_kb catches fact-card violations at scale; the eyeball gate remains the authority on these subtle morphs. Don't sell guardrail 2 as the fix it isn't.

**5. The prompt-lint rule "ban the trigger noun" conflicts with existing cards.**
`BRONZE_SERPENT_STANDARD.canonical` legitimately contains "serpent" and "snake" (in shape-negatives: "a snake-wrapped staff"). A blanket "ban the trigger noun, describe the result" rule is underspecified — it would collide with cards that need the noun in their negatives. The rule needs to be "ban the *bare* trigger noun in the positive subject, keep it only in negatives," or similar.

**What's sound (reuse + low risk):** guardrail 1's lookup-before-render and coverage rule are a real fix for the generic-bearded-man bleed and reuse existing `ref_library` PNGs as `--image`. Guardrail 3's SUBTLE/DYNAMIC presets and learning #2's content-hash idempotence are sensible, reuse the frozen-tableau discipline, and carry little risk. The plan correctly flags its own n=1 (single EW04 POC) and asks for a paid test beat before rollout (consistent with `test-gate-before-batch`).

**Cost note:** minting grids (¾ + profile + expression row + costume variants) per entity multiplies the cheap-1-credit stills, but the bigger cost is the from-scratch truth-card authoring hidden by "nothing is regenerated" (finding 2) and the first-use approval latency the plan already flags.

VERDICT: REVISE
TOP FIXES:
1. Fix the false premise under the user-approved unify-by-slug decision: ref_library keys by uppercase `name`, bible_kb's only entities key by kebab `slug` and there are **no** character/object/place entities to merge — so "both already keyed by slug / nothing is regenerated" is wrong. Either choose the cross-referenced-by-slug alternative (your own open question), or scope the real work: a slug-normalization map + from-scratch authoring of every truth half. Don't build on the merge-by-slug claim as stated.
2. Reconcile the scene-scoped/per-episode reality of bible_kb (`enrich_for_scene` reads `<v1>/_bible_check/scene_facts.json`) with the persistent per-entity look cards before unifying — they are different units of work; a single-file unified card will fight `build_episode_facts`.
3. Re-frame guardrail 2 honestly: by learning #3 the bible_kb Vision audit *passed* the caduceus/nails/wrists, so it does not close that gap — make the human Read + known-failure checklist the named authority for these morph defects, and don't claim routing through bible_kb fixes EW04's eyeball-only accuracy.
