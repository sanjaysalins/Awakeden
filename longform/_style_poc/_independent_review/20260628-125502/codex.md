# Independent review — codex (OK, 197s)

**Best recommendation:** use **MI mature brush-ink manga / seinen ink**, not PG, as the primary comic lane. It is the only candidate that is unmistakably comic while matching the prior finding that ink/charcoal survives Kling. Best hf-CLI model to try first: **`seedream_v4_5`**, because local HF-POC notes rate it as the illustration winner and say it supports multi-ref image anchoring. Keep **`nano_banana_2`** as the fallback if Christ-face reverence or face lock fails.

**Findings**

- The execution step assumes a script that does not exist: `Execute: 1. render_comic.py Round 1`. I found no `render_comic.py` in this repo. There is `pipeline.visual_render.HFProvider`, HF-POC `run_batch.sh`, and gallery builders, but this plan does not say how to adapt them.

- `Round 2 ... extend FACES.html` appears to reference a nonexistent gallery. I found `_STYLE_COMPARE.html`, `_COMPARE.html`, sweep galleries, and `visual/nbp/index.html`, but no `FACES.html`. This is a concrete feasibility miss.

- The model list is not grounded in the local hf tooling. `recraft_v4_1` is in the plan, but HF-POC `run_batch.sh` lists 19 models and does not include it; it does include `grok_image`, `seedream_v5_lite`, `marketing_studio_image`, etc. The plan’s “MODEL candidates (5)” is therefore not the local “best available” set.

- The style/model methodology is biased by `Round 1 — Fix ONE style = PG painted graphic-novel`. That will select the best painted-realism renderer, not the best comic renderer. Then `Round 2 — Use the Round-1 winning model` can unfairly bury MI/NR, which need ink/graphic-specialist models.

- The plan contradicts local character-lock evidence. It says `Only nano_banana_2 (refs) and ... text2image_soul_v2 ... give true cross-scene face-lock`, but HF-POC `CLAUDE.md` says `seedream_v4_5` has `input_images` and that the old single-ref rule was stale. That matters because `seedream_v4_5` is probably the right first model for MI.

- The cost math is wrong enough to affect decisions. `~5 × ~7cr ≈ ~35cr` treats all image models as GPT-image-priced. Local HF-POC costs list `seedream_v4_5:1`, `flux_2:1`, `nano_banana_2:2`, `gpt_image_2:7`, and Soul models at `0.12`. The plan says to confirm cost only before Round 2, but the Round 1 design itself depends on cost.

- Existing pipeline defaults fight the comic experiment. `config.py` hard-locks `VISUAL_STYLE_BASE` to Flemish Baroque and bans `comic panel`, `cartoon`, and `anime`; `_hf_animate_short.py` animation prompts repeatedly say “Baroque oil painting.” `Round 3 — Animate the winning style+subject in Kling pro 5s` is not valid unless the animation prompt is rewritten for comic stills.

- `PG painted graphic-novel realism ... reverent by default` is an unsupported assumption. It is also the closest to the current Baroque lane, so it is weakest for the stated reach-broadening goal. It may select “nice serious painting” rather than “comic teens/adults read.”

- `NR ... Sin City / Blacksad ... betrayal/pit/cross` is risky for reverence. Noir visual grammar can make sacred scenes feel crime-thriller, cynical, or sensational. It may be useful for betrayal inserts, not as the house style for Christ-facing episodes.

- `Christ-face` as the only Round 1 subject is too narrow. A model can pass a sacred portrait and fail multi-figure period scenes, hands, crucifixion anatomy, resurrection light, or first-person witness continuity. At minimum test one Christ close-up, one full-body/sacred scene, and one witness action frame.

- `review full-res myself → pick top 2` creates a single reviewer failure point. This repo already has independent review/audit habits; the plan should define a rubric and use an independent visual/reverence pass before spending on motion.

- The plan says the channel includes shorts plus long-form, but the bake-off only proves 9:16 Kling shorts. A comic look can fail 16:9 composition, long-form pacing, or caption-safe negative space even if the vertical splash works.

VERDICT: REVISE
TOP FIXES:
1. Replace PG-first with a fair MI-first bake-off: test MI + `seedream_v4_5` against PG + `nano_banana_2`, both with reference anchoring and Christ-face gates.
2. Ground execution in existing tools: create/adapt the actual render script/gallery path, rewrite Baroque-only style and Kling prompts, and verify model availability/cost with `hf generate cost`.
3. Add real verification: independent reverence review, character-lock proof across 3 scenes, and motion tests for both Christ-face and a high-emotion witness scene.
