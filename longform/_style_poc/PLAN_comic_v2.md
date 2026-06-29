# Plan v2 — "Comic teens & adults read" + best-model bake-off (REVISED after adversarial + 4-CLI panel)

Supersedes PLAN_comic.md. Folds in: 1 hostile adversarial agent + the live panel (codex REVISE,
claude REVISE; gemini/grok errored). Every load-bearing number now verified against the live `hf`
CLI + the repo, not assumed.

## Verified facts (were assumptions in v1)
- **All model IDs are real** (live `hf model list` + `hf generate cost` preflight, $0/no job).
- **Real per-still credit cost** (preflighted): seedream_v4_5 **1** · seedream_v5_lite 1 · flux_2 **1** ·
  grok_image 1 · z_image **0.15** · text2image_soul_v2 **0.12** · recraft_v4_1 **1.25** ·
  nano_banana_flash 1.5 · nano_banana_2 (Pro) **2** · cinematic_studio_2_5 2 · gpt_image_2 **7**.
  → v1's flat "~7cr/still / ~104cr total" was wrong; gpt_image is the 7× outlier. Comic stills ≈1cr.
- **Face-lock models** (cross-scene same face): `nano_banana_2` (ref images) AND `seedream_v4_5`
  (`input_images`, per repo A/B note) AND `text2image_soul_v2` (trained Soul, 0.12cr).
- **Repo gate conflict (real):** `config.py` hard-locks Baroque + bans `comic/cartoon/anime`
  tokens, and `verify_image` check #6 fail-closes anything not Old-Master period. **This POC runs in
  the scratchpad with its OWN standalone render + my own full-res review** — it does NOT touch the
  engine config or its period gate. (Productionizing a comic look later = a separate config change.)

## What the reviewers converged on (the revisions)
1. **Kill the PG-first confound** (all 3 reviewers). Don't pick the model on one style then force it
   on the rest — model quality is style-dependent. → one sparse style×model grid instead of 2 rounds.
2. **PG painted-realism is the wrong seed** — closest to current Baroque, least "comic," highest
   melt-to-photoreal risk. Demote to control. (hostile + codex + claude)
3. **Add the actual teen-read format: flat webtoon/manhwa** — seinen brush-ink is what adults read;
   webtoon is what teens read. (hostile agent)
4. **Noir = crime-thriller reverence risk on Christ** (codex + claude). Keep it for betrayal/pit
   INSERTS or with a warm accent; do NOT make it the Christ-facing house style.
5. **Reverence guard must block "cool/edgy/antihero," not just "juvenile."** (hostile)
6. **Test character-lock on the production path BEFORE motion** — render the SAME witness face across
   3 scenes; a no-ref still-winner that can't hold a face is unshippable. (all 3)
7. **Broaden the model probe beyond Christ-face** — also a witness action frame + a multi-figure
   scene (hands, crowd, anatomy). (codex)
8. **n=1 per cell picks on noise** — reseed the 2-3 finalists 2-3× (trivial at ~1cr). (claude)
9. **Both gates, not just self-review** — my full-res look AND a re-panel on finalists before motion.
10. **Color vs B&W + native 9:16** are explicit tested variables, not smuggled inside style. (hostile)

## STYLE shortlist (4, revised) — descriptive strings, no IP tokens
| Key | Lane (reference) | Role |
|-----|------------------|------|
| **MI** mature seinen brush-ink + screentone | "Vagabond" | **primary reverent comic** (ink already survives Kling) |
| **WT** flat webtoon/manhwa, clean cel-shade, bold flat color, limited palette | modern digital comic | **teen-reach challenger** |
| **NR** noir high-contrast ink, black spot-blacks + ONE warm accent | "Blacksad"/tenebrism | **drama/insert** look (warm accent on Christ; not house style) |
| **PG** painted graphic-novel realism | "Kingdom Come" | **control** (likely melts; benchmark only) |

Format: full-bleed single splash frames, native **9:16**, NO panels/gutters/lettering (Kling garbles
them; captions added deterministically later). Comic-ness = linework/halftone/flat-color register.

Reverence + anti-slop tail (every prompt):
"mature reverent dignified gravitas, period-accurate ancient Near East / Egypt, no modern objects;
NOT childish, NOT a cape/superhero comic, NOT a cute mascot, NOT cool/edgy/antihero/crime-thriller;
emotionally truthful face; the face of Christ is holy, never a dramatic 'beat'."

## The bake-off (one grid + 2 confirm phases) — real costs

### Phase A — style × model grid (find look + renderer together)
3 cheap stylization specialists (all ≈1cr) cover the grid; PG control adds nano_banana_2.
- Models: `seedream_v4_5`, `flux_2`, `recraft_v4_1` (+ `nano_banana_2` for the PG control & face-lock).
- Subjects (3, broadened): `christ_face` (reverence gate) · `joseph_pit` (emotion/morph) ·
  `joseph_action` (a witness hauled/thrown — hands + body + multi-figure stress).
- Grid: 4 styles × 3 models × 3 subjects = **36 stills ≈ ~40cr** (recraft 1.25 nudges it slightly).
  *(Lean option: drop joseph_action → 24 stills ≈ ~27cr.)*

### Phase B — finalist reseed + character-lock probe (before any motion)
- Reseed the top 2 style×model cells 2× each (kill noise) ≈ 4 stills ≈ ~5cr.
- **Character-lock**: take the winning witness face → render SAME face in 3 different scenes via
  `nano_banana_2` (ref) and/or `seedream_v4_5` (input_images). ≈ 6 stills ≈ ~10cr.
- Re-panel the finalists (free, local CLIs) for the comic-adapted reverence verdict.

### Phase C — motion confirm (only the winner, production-realistic)
- Animate Christ-face + a high-emotion witness frame, Kling pro 5s, ref-locked config.
- 2 clips × 12.5cr ≈ **~25cr** (Kling is now the dominant cost).
- Review start/end frames for: photoreal-melt, face morph, halftone/screentone crawl.

**Total ≈ 40 + 15 + 25 ≈ ~80cr** (lean ≈ ~67cr). Budget remaining ≈143cr → comfortable reserve.

## Decision the USER still owns (not mine to make)
This is the *popular-reach* bet vs the *premium charcoal/Baroque* lane that already passed reverence +
motion and differentiates Awakeden in apologetics. The bake-off produces evidence; the user picks the
lane (or runs comic as a parallel sub-playlist, the reviewers' suggested hedge). A comic look must
clearly BEAT charcoal to justify switching — "also nice" isn't enough.

## Execute (after go) — scratchpad only, idempotent, full-res self-review, spend logged
1. `render_comic_grid.py` — Phase A grid (thin standalone over the same hf-subprocess pattern as
   render_faces.py; writes `comic/` + extends a COMIC.html gallery).
2. Full-res review (me) → pick top 2 cells → Phase B reseed + character-lock → re-panel.
3. Phase C motion on the single winner → frame review → verdict + clickable links.
