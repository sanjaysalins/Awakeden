# AWAKEDEN COMIC DNA — the series visual identity (v0.3 — CORRECTED post external panel)

> **Status: DRAFT, REVISED after a 4-lens red-team (2026-07-23), CORRECTED after 2 rounds of the**
> **external panel (2026-07-23, see §10 review log — round 3 still REVISE, real code-level gaps**
> **remain, being worked through the punch list).** NOT yet binding. Next gates: close the round-3
> punch list → **ONE named pilot piece (EW01, not a batch — corrected round 2)** → the confirmed
> real-audience read (§9.2) → your sign-off → wire into `config.py` / skills / gates + `v2/SPEC.md`.
>
> **What this reconciles:** the **inked comic art** you chose + the **retro-comic grammar** from the
> DNA study, into ONE identity. Grounded in a 3-agent study (`_retro_dna/_RETRO_DNA_STUDY.html`).

### Red-team outcome (4 hostile lenses, all findings verified by looking)

Verdict = **REVISE, do not lock.** The look is worth keeping; the *commitment language* + *recipe*
were the problem. Two red blockers were **PROVEN FIXABLE** in a bake-off (`_retro_dna/_prove_it/`):

- ✅ **Character drift FIXED (on Christ; Aaron unchain-tested — see §1)** — render Christ + recurring
  cast on **`nano_banana_pro` + a chained `--image` reference** (the `_painted_comic_bright.py` path).
  Proven to hold the same man across 3 scenes for Christ. `seedream_v4_5` = **neutral plates only**.
  **Correction (round-3 panel, grok): this badge cited `[[locked-stills-provider-split]]` for the
  `nano_banana_pro` path — that memory actually locks the DIFFERENT direct-Google-NBP path. §1
  already flags this citation as wrong; the badge just hadn't caught up. Fixed here too, so a reader
  skimming only the checkmarks doesn't inherit the same false attribution the panel caught in §1.**
- ✅ **Isaiah-53 cross FIXED** — a marred/robed, sorrowful, non-heroic crucifixion (no bodybuilder
  torso, no bright decorative blood). Body gate below (§5).

Open items still to resolve before lock (tracked in §8/§9/§10): reframe the over-commitment (done,
§0/§9); one canonical print recipe (§1); restore no-text negatives in the render prompt (done in the
proven recipe); honest owned-vs-build (§8); dots-crawl-on-animation test; pin the numbers; the
kitsch/audience question → the pilot A/B decides it.

---

## 0. Prime stance — "cinematic inked comic with a retro print finish" (REVISED)

We adopt the retro comic's **grammar** (bold ink, tier grids, caption boxes, Ben-Day print texture,
page-turns) as a **system with range** — NOT a single frozen filter cranked to maximum. The red-team
was right: our best renders *pulled back* (dots in skies/shadows, clean sacred faces), and that
restraint is the look, not a compromise of it. So:

- **A system, not a dial-to-11.** One ink+print family; controlled variety in palette-key, dot
  visibility, and panel density per beat. The loud comic vocabulary (heavy dots on a face, comic-yellow
  boxes, SFX) is used **selectively for punch**, never as the blanket default. (This replaces the
  earlier "full retro, no dial" — that language pushed toward kitsch our own renders reject.)
- **Reverence is protected by BOTH content and a graduated style — never by style alone.** Style *is*
  content; we don't pretend otherwise. Dots are masked off sacred faces, SFX are suppressed on the
  atonement/resurrection, expression on Christ is never exaggerated. That graduation *is* the reverence
  mechanism (the dot-mask is a stated rule, §1, not a smuggled exception).
- **Content rules that hold regardless of style:** Christ always dignified + marred-not-heroic on the
  cross (§5); Scripture its own treatment; real sounds never BIFF/POW; primaries land on biblical
  subjects, not costumes.

Inherited non-negotiables still rule and sit ABOVE this (doctrine both ways, whole-Bible-through-Jesus,
KJV verbatim, hero-bookend on Christ, Remotion draws all text, INV-26 hold, INV-27 watermark).

---

## 1. The look — the recipe (PILOT RECIPE, corrected 2026-07-23 post-panel)

> **Correction (2026-07-23, round 1):** the previous revision of this section claimed "Seedream 4.5
> held the SAME man across scenes" and locked it as the model for everything. That was **false** —
> verified against `_prove_it.py` (`MODEL = "nano_banana_pro"`, line 19) and the spend ledger. All 3
> reviewers that answered round 1 (cursor/claude/grok) caught this independently.
>
> **Correction (2026-07-23, round 2 — user decision, explicit):** the round-1 fix cited
> `[[locked-stills-provider-split]]` for the HF `nano_banana_pro` path, but that memory actually locks
> a *different* path (direct Google `genai` NBP, $0.50/still). Citing it was itself wrong — flagged
> independently by claude and grok in the round-2 panel as silently overturning a locked decision
> without the user's sign-off. **The user was asked directly and chose HF `nano_banana_pro` ($0.30,
> proven in-style this session) over reverting to NBP direct.** This is now the binding call,
> superseding `[[locked-stills-provider-split]]` for this DNA's character path — that memory has been
> updated to point here. NBP direct remains the still-locked path for the older baroque/painted-comic
> styles, unchanged.

**Two models, split by role — not one model for everything:**

- **Christ + any recurring character → `nano_banana_pro`** (via HF `hf generate create`,
  ~$0.30/still, 2 credits) **with a chained `--image` reference.** This is the only model+ref
  combination actually proven to hold one face across scenes (`_retro_dna/_prove_it/`, 3 scenes).
  NOTE: this is the HF-billed `nano_banana_pro` — a **different code path** from the existing
  production `NBPProvider` (direct Google `genai` `gemini-3-pro-image-preview`, $0.50/still,
  [[locked-stills-provider-split]]). The two are not yet reconciled; treat them as separate until one
  is chosen for production.
- **Neutral plates / backgrounds / crowds with no recurring named character → `seedream_v4_5`**
  (no ref needed, ~$0.15/still), chosen after a 14-model bake-off for its crowd/depth composition.
  (Runners-up: seedream v5-lite = richer portraits, same cost; `openai_hazel` = best pulp look but
  3:2-only, ruled out for video; `soul_cast` = photoreal casting tool, not the art model.)

**Real cost per still is ~$0.15-0.30, not a flat $0.15** — budget the pilot on the mix (§9), not the
floor.

**Character lock (MANDATORY, but NOT YET production-wired):** chain the character's `--image`
reference into every frame they appear in. Proven on Christ only (3 scenes, `nano_banana_pro`).
**Gap (found by the panel, verified in code):** `pipeline/visual_render.py`'s real `render_scene()`
never passes `HFProvider.extra_ref_paths` — every ref-chained render so far has been an ad-hoc
`subprocess` script (`_prove_it.py` / `_seedream_ref.py`), NOT the production pipeline.
**FIXED 2026-07-23 (updated after round-3 panel):** `render_scene()` now accepts + passes through
`extra_ref_paths`; proved end to end via a real call through the production function
(`_retro_dna/_smoke_render_scene.py`, `_smoke_render_scene/01_smoke_teaching_v2.png`, audit PASS).
**Correction (round-3 panel, verified in code):** that proof was the ONLY place refs actually flow —
the real long-form production script, `longform/EW01_Two_Goats/_render_inked_stills.py`, called
`prov.generate(scene)` directly with no refs at all (now fixed — see §8). The shorts orchestrator
`pipeline/visual_runner.py` still doesn't resolve refs; not fixed this pass, lower priority since
EW01 is long-form. Still open: nothing auto-resolves refs from a scene's style yet (no `retro`
`STYLE_REGISTRY` key — see §8). **Aaron now HAS a locked ref** (`_retro_dna/aaron_retro_ref.png`,
rendered 2026-07-23, correct wilderness setting — not the old `aaron_pc_ref.png`'s anachronistic
Greek columns) — but it is chain-tested on ZERO scenes so far, unlike Christ's 3-scene `_prove_it/`
proof. A real pilot render needs that Aaron multi-scene proof before trusting his identity holds
for him too.

**The render prompt** (both providers, genuinely — the recipe is two models again): strong retro —
bold black ink holding lines, flat limited 4-colour (no gradients), visible coarse Ben-Day dots in
skies/shadows, warm cream colour palette, slight CMYK misregistration — **AND it MUST carry the
no-baked-text negatives** (`no text, no lettering, no captions, no speech balloons, no title box, no
watermark`) so Remotion owns all text (the earlier `_true_retro_test.py` dropped these — fixed in
`_prove_it.py`). **Also watch concrete-noun negatives** — the character-model has no true
negative-prompt channel and can DRAW the forbidden object; describe the desired end-state positively
instead ([[seedream-no-negative-channel]]). Two confirmed cases this session: (1) a `two_goats_splash`
render with "no blood" in the prompt drew blood on the altar cloth — fixed by positive-only phrasing.
(2) **"printed on aged cream newsprint" + "no panel borders" made the model draw an actual bordered
PAGE** (black rule + cream margin) instead of just applying the style — reproduced on 2 separate
renders (`two_goats_splash` + the `render_scene()` smoke test). Tried the same fix as (1): drop the
physical-print-object framing, describe the end-state ("full-bleed... edge-to-edge") instead of
negating "panel borders." **Correction — this REDUCES but does NOT eliminate it:** a same-recipe
Aaron reference render (`_aaron_ref.py`, no "newsprint"/"no borders" wording at all) still came back
bordered on its first roll. Looks stochastic, not purely wording-caused — some renders in this
"vintage 1960s comic" style default to a printed-page composition regardless. **Practical mitigation (2 layers, honesty-corrected round-3):** (a) `config.VISUAL_BANNED_TOKENS`
includes `border`/`frame`/`canvas edge`, so `render_scene()`'s retry-on-audit-fail loop CAN catch and
re-roll this in the real pipeline — **but this is unproven, not confirmed**: the smoke test that
proved the ref-chaining plumbing ran with `max_retries=0`, so the retry path itself was never
actually exercised on a bordered render. Treat "the pipeline auto-retries this" as a claim to verify,
not a fact. (b) **The proven mitigation is manual: crop it off.** When a render comes back bordered,
the interior content already extends nearly to the border — a flat ~4.5% inset crop removes the
cream margin + black rule cleanly with no paid re-render (`aaron_retro_ref.png` was rescued this way
after 2 bordered rolls in a row). This is validated on ONE image so far, not a battle-tested
pipeline step — no automated crop exists inside `render_scene()` itself. Budget the occasional extra
retry/crop in the pilot cost (§9) regardless. Both recipe scripts (`_hook_splash.py`,
`_seedream_ref.py`) updated with the better-odds phrasing anyway — it doesn't hurt, just isn't a
full fix on its own.

**Print-finish (`_retro_dna/_print_finish.py`) — honest caveat:** it adds cream paper + a *subtle*
shadow-masked dot reinforcement + a misregistration fringe. **Most of the retro dots come from the
RENDER, not this pass** — so treat the finish as a light *unifier*, not the consistency engine. Dots
are masked below ~50% luminance so **faces/light solids stay clean** — but that luminance-only mask
is naive (floods an all-dark night frame, does nothing on an all-bright frame); a subject/face
exclusion mask (rembg) is the real fix. **OPEN: this finish is a still-image pass; it is NOT yet
proven on animation** — a fixed screen-space dot grid over moving art will *crawl/moiré*. Bake dots
into the plate (move *with* the art) OR solve per-frame before any animated episode. Reconcile the
three current print scripts (`_print_finish.py` masked-still / `panel_animator/print_grade.py`
unmasked-clip / `_retro_grade_demo.py`) into ONE canonical pass before lock.

---

## 2. Palette — the 4-colour print system, used with range (ONE canonical list)

The retro **print system** — 4 inks (CMYK), flat solids + Ben-Day dots — but applied with the §0
range, not cranked to max on every frame. **This table is the single source of truth; the reference
card must match it exactly** (they diverged before — fixed).

| role | hex | note |
|---|---|---|
| Newsprint (ground) | `#E8D9B5` | never pure white |
| Warm black (ink) | `#231F20` | never pure black |
| Process cyan | `#00AEEF` | print ink |
| Process magenta | `#EC008C` | print ink (the "red plate") |
| Process yellow | `#FFF200` | print ink |
| Comic red (2-ink) | `#ED1C24` | blood / heat, sparing |
| Hero blue (2-ink) | `#2E3192` | rare |
| Storm (judgment) | `#2E3A52` | law / dread beats |
| Gold (glory) | `#E9C877` | Christ / glory light |
| Desert / robe | `#8A7039` | earthy base |
| Caption yellow | `#FFE100` | the narrator caption box only (§3) — NOT `#FFF200` |

Primaries are real but land on **biblical** subjects (glory, storm, blood, robes, desert), never
superhero-costume colour. Arc: **Christ / glory = gold**; **law / judgment = storm blue-black**.

---

## 3. Lettering — the Awakeden hand

- **ALL CAPS.** Emphasis = **bold-italic**. Crossbar-"I" only for the pronoun *I*.
- **Caption box = the narrator voice.** Top-left, italic caps. Colour: **comic-yellow `#FFE100`**
  (one default — resolves the earlier parchment-vs-yellow contradiction). Reverence is carried by the
  *Scripture* treatment below, not by dulling the narrator box.
- **Scripture gets its own treatment** — distinct from dialogue. **LOCKED for the pilot:** the
  `PocKineticType` gold treatment (gold-on-dark, gold border, kinetic reveal) in **PermanentMarker**
  (it's the built, proven one — resolves the "OPEN serif"). Scripture must **never** look like ordinary
  speech, and red-letter Christ speech ALWAYS uses this, never a balloon.
- **Balloons** (shape = meaning) used **only when a scene has speakers** — ties to our
  multi-voice rule.
- Fonts: **Kalam** (dialogue/caption, ✓ `Kalam-Bold.ttf`/`Kalam-Regular.ttf` in `_remotion/public/`),
  **Bangers** (SFX/title, ✓ in repo), **PermanentMarker** (Scripture, ✓ in repo). All three loaded and
  proven in `DnaSplashHook.tsx`.
- **Text is NEVER baked into the AI art — Remotion draws all of it.** (Existing hard rule.)

---

## 4. SFX — restrained, reverent

- The **sound of Scripture**, not POW camp. Allowed: the veil **K–KRAAK**, thunder, a seal
  breaking, wind, a stone rolling. **Banned:** violence camp (BIFF / POW), anything that
  undercuts reverence.
- Retro styling (big / outlined / angled) but **spread THIN** — one SFX per *key* beat, not
  every panel. (Ties to `panel-animator-intentional-use`.)

---

## 5. Panels & tiers — comic grammar mapped to the gospel beat

- Tier-first grid (**6 or 9**), broken **once** per page for the money beat. Gutters 2–4%,
  black borders 4–8px @1080w, cliffhanger bottom-right.
- **Beat map** (comic shot → our function):
  - establishing wide → **OT echo / setting**
  - action panel → **the event**
  - reaction close-up → **conviction**
  - **the Christ pivot** (renamed from "hero pose" — see the split below) → the reveal
  - cliffhanger last panel → **the CTA-to-Jesus**
- **Hero-bookend:** open AND close on Christ (our existing AS-G6/G7 for shorts; the long-form
  Remotion path needs its own bookend check — coverage gap to close). The splash + final panel are Christ.

### 5a. The Christ-figure split (doctrine gate — REQUIRED)

The comic genre's default body is the idealized superhero — which walked straight onto our first
crucifixion render (a bodybuilder torso) and **failed Isaiah 53** ("no form nor comeliness... no
beauty that we should desire him"). So the Christ figure has **two grammars, gated by beat:**

- **GLORY beats** (resurrection / ascension / welcome / the gospel pivot): triumphant is permitted —
  radiant, upright, arms open, the light behind Him.
- **PASSION beats** (the cross, the suffering): **servant register only — marred, gaunt, sorrowful,
  head bowed, NO heroic/athletic musculature, NO defined abs, NO bright decorative blood.** Robed or
  loincloth (robed reads more reverent; a marred loincloth is more literal — a per-piece call, blood
  always faint/matted).
- **Body gate:** every passion Christ frame is checked (Vision) to FAIL idealized musculature + bright
  droplet blood; ban `muscular / heroic / athletic / six-pack / V-taper` tokens on any cross still.
  Proven achievable in `_retro_dna/_prove_it/christ_cross_marred.png`. **Scene-plan authors: describe
  the desired END-STATE only** ("gaunt, sorrowful, marred, no defined form") — do NOT write a negated
  banned word directly into a scene's `subject_block` (e.g. "no heroic muscle"). Two independent
  reasons converge here: (1) [[seedream-no-negative-channel]] — naming a concrete noun even to forbid
  it can draw it in the render; (2) SP-G5 (`pipeline/visual_engine.py _check_sp_g5`) is a plain
  substring match with no negation-awareness, so that exact phrase would FAIL the gate too. Both are
  pushing the author toward the same fix — positive-only phrasing — so this is working as intended,
  not a gate bug to route around (caught by the round-3 external panel; verified, not just asserted).
- **SFX + balloons carve-out:** NO SFX graphic on the crucifixion / veil-tear / resurrection
  (stillness only). Red-letter Christ speech NEVER goes in an ordinary balloon — always the distinct
  Scripture treatment (§3).

---

## 6. Motion — retro comic, alive (Remotion)

**ENGINE DECISION (user, 2026-07-23, resolves the round-2 panel's flagged conflict):** the retro DNA
does NOT extend the existing `build_livingpage_16x9.py` Python/ffmpeg engine (`v2/LIVINGPAGE_STANDARD.md`
— word-timed slams, takeover camera, sacred stillness, craft borders; mature, DoD-gated, already
covers both longs and shorts per its §7). **Remotion stays its own, separate engine** for retro-comic
work going forward. This is a real, acknowledged cost: livingpage's word-timing (`alignment.json` →
frame-snapped slams within ±0.05s), its DoD gates (§3), and its reuse/richness rules (§3b) all need
their OWN Remotion-side equivalents — none of that is inherited for free. Print-comic-specific needs
(gutter panels, misregistration, the gold Scripture reveal) are the stated reason: they fit Remotion's
declarative component model more naturally than livingpage's ffmpeg compositing. **BUILD, not ported:**
word-exact slam timing (current `EW01Slices.tsx`/`DnaSplashHook.tsx` motion is spring-animated on
fixed frame offsets, not driven by forced alignment), a DoD-equivalent gate set, the reuse/richness
counters from §3b.

- **kinetic Scripture type** (built/proven) + **tier reveals**, **page-turn** transitions. Living
  plates (generative clips) inside panels; print-finish over the top (§1 caveat: prove no dot-crawl).
- **Word-timed panel slams are a TARGET, not yet built** — the current `EW01Slices.tsx` uses an
  *approximate* 40%-into-window timing ("no forced alignment"); `DnaSplashHook.tsx`'s slams are
  spring-animated on hand-picked frame offsets, same gap. Given the engine decision above, this needs
  a NEW Remotion-side forced-alignment consumer (reading the same `alignment.json` shape livingpage
  already produces), not a port of livingpage's own compositor.
- **Restraint = reverence:** sacred stillness on Christ frames; energy reserved for
  judgment/action. (Living-page standard — the PRINCIPLE carries over even though the engine doesn't.)

---

## 7. Brand

- **Awakeden masthead** in a retro logo treatment (Bangers / custom deco).
- INV-27 watermark + INV-26 landing hold unchanged.

---

## 8. INCORPORATION MAP — where each piece actually lives (refreshed 2026-07-23 post-panel)

| DNA element | Stage / file that owns it | State |
|---|---|---|
| Art base (ink + colour) | `config.py` `STYLE_REGISTRY` still prompts | exists (extend) — no `retro`/`awakeden_comic` key yet; `graphic_novel` is a DIFFERENT cinematic-manga look |
| Print treatment (dots / paper / misreg) | reconcile `_print_finish.py` / `panel_animator/print_grade.py` / `_retro_grade_demo.py` | **BUILD** — 3 scripts conflict; `DnaSplashHook.tsx`'s `Grain`+`Misregister` prove a $0 Remotion-side version, but not proven on a real animated multi-panel grid |
| Kinetic Scripture type | `PocKineticType.tsx`, ported into `DnaPocFilm.tsx` + `DnaSplashHook.tsx` (`GoldScripture`) | **BUILT + reused twice** |
| Narrator caption box | `DnaPocFilm.tsx` `Caption` + `DnaSplashHook.tsx` `CaptionBox` | **BUILT** (comic-yellow `#FFE100`, Kalam, top-left, italic caps) — was wrongly marked CSS-mockup-only |
| Balloons (attach to moving speaker) | Remotion component | **BUILD** — still not built |
| SFX overlays | `DnaPocFilm.tsx` `Sfx` + `DnaSplashHook.tsx` `ImpactBurst`; reuses `panel_animator/impact_burst.py`'s visual language | **BUILT** (2 variants) — must respect §5a's stillness carve-out (a first draft put a burst + SFX word ON a crucifixion/veil-tear beat; caught + fixed 2026-07-23) |
| Tiers / grids | `DnaSplashHook.tsx` split-panel `Panel` + torn-ink `Gutter` | **BUILT** (2-up split, hard-bordered panels, slam-in) — still no 6/9-tier grid, no page-turn transition |
| Fonts | Bangers ✓, PermanentMarker ✓, Kalam-Bold ✓, Kalam-Regular ✓ | **all in repo** — "Kalam.ttf NOT in repo" was stale, corrected |
| Beat map | scene-plan gates (SP-G*, AS-G6/G7) | exists — add DNA checks; long-form Remotion bookend (open/close-on-Christ) still unenforced |
| Ref-chaining plumbing (character lock) | `pipeline/visual_render.py render_scene(..., extra_ref_paths=)` | **FIXED 2026-07-23** — proved end-to-end through the real function, not an ad-hoc script (`_smoke_render_scene.py`, audit PASS). Still no auto-resolution from a scene/style (caller must supply the path explicitly; no `retro` `STYLE_REGISTRY` key yet) |
| Cast reference bank | `christ_pc_ref.png` + `_retro_dna/aaron_retro_ref.png` (new, 2026-07-23) | Christ proven multi-scene; Aaron rendered clean but NOT yet chain-tested across scenes — any other recurring character still needs a ref |
| Thumbnails | `pipeline/thumbnails.py` | **BUILD** retro skin + a high-contrast non-halftone thumb pass |
| Website | `_website` | **BUILD** retro skin |
| Brand / watermark / hold | `add_watermark.py`, `check_landing_hold.py` | exists (INV-26/27) |

**Honest takeaway (re-corrected 2026-07-23):** more is built than the last pass credited — caption,
SFX/impact-burst, kinetic Scripture, and a 2-up tier/gutter system are now real, working Remotion
pieces (proven in `dna_splash_hook_v6.mp4` + `dna_poc_v1.mp4`, and in their concatenated 36s combo).
Still genuinely open: production ref-chain wiring, a cast-ref bank beyond Christ, balloons, a 6/9-tier
grid + page-turns, ONE canonical print-finish pass proven on animation, and both skins
(thumbnail/website). Closer to **~55% owned, ~45% to build** — better than the prior 40/60, nowhere
near "just codify."

---

## 9. Commitment — a system with range, proven on a PILOT before 76

**We do NOT lock 76 episodes yet.** The retro direction was chosen the same day as the bake-off with
zero audience data; the red-team's strongest point is that this is a strategy decision the *scroller*
should settle, not internal consistency alone. So:

1. **Build ONE named pilot piece first, not a batch (corrected 2026-07-23 per the round-2 panel:**
   "you cannot pilot the DNA without first proving one piece end-to-end" — a 3-piece commitment before
   any single piece is proven end-to-end is the over-spend risk, not the caution). **Pilot piece =
   EW01 Two Goats**, rebuilt in the retro DNA — it already has the deepest DNA proofing (Christ +
   Aaron refs, the hook proof, the body POC) of anything in the slate.
   **Real cost table (grounded in EW01's actual scene_plan.json + its own prior animator-tiering
   decision, not a guess):**

   | item | count | unit cost | subtotal |
   |---|---|---|---|
   | Character stills (Christ/Aaron, `nano_banana_pro` + ref) | 17 of 25 scenes | $0.30 | $5.10 |
   | Plate stills (`seedream_v4_5`, no ref) | 8 of 25 scenes | $0.15 | $1.20 |
   | Retry/re-roll buffer (~20% — the border defect + normal QC re-rolls; most border fixes are a $0 crop, not a re-render) | — | — | ~$1.25 |
   | **Stills subtotal** | 25 | | **≈$7.55** |
   | Animation, Kling (multi-figure/crowd — same 8-scene split EW01's own prior migration used) | 8 clips | ~$1.13 | $9.00 |
   | Animation, Seedance (calm scenes — same 17-scene split) | 17 clips | ~$0.72 | $12.25 |
   | **Animation subtotal** | 25 | | **≈$21.25** |
   | Opus planning (scene-plan + reviews) | — | agent-mode $0, or ~$3-5 metered fallback | $0-5 |
   | **EW01 pilot total** | | | **≈$29-34** |

   (Sanity check: EW01's actual prior oil→ink migration spent ~$35.80 end to end — this estimate
   lands slightly under that, consistent since the character/plate split here is cheaper per-still
   than that migration's all-`nano_banana_pro` approach.) **This is still an estimate, not a quote —
   run a real `/cost` pre-flight and get explicit OK per [[feedback-ask-before-spending]] before any
   render moves.** Only after EW01 reads well end-to-end does a 2nd/3rd pilot piece get named.
2. **Real audience read — corrected 2026-07-23 (the round-2 panel caught the original protocol was
   mechanically broken, not just underspecified):** "cut the same piece two ways" risks a YouTube
   duplicate-content flag on the SAME channel; and 9:16 Shorts traffic comes overwhelmingly from the
   swipe feed, which never shows a thumbnail at all, so "thumbnail CTR" isn't a real Shorts metric.
   **Corrected protocol, CONFIRMED by the user (2026-07-23):**
   - **The free kitsch test runs FIRST, always** (`_KITSCH_TEST.html`, still unsent) — a genuine kill
     gate at $0 before any paid audience read.
   - **EW01 is long-form (16:9)**, where thumbnails DO matter and duplicate-content risk is avoidable:
     compare it **between-subjects**, not within — its real performance (average view duration,
     retention curve, like ratio, comment tone) against the last 2-3 comparable already-shipped
     inked/painted longs, NOT the same content re-cut. YouTube Studio's native thumbnail
     Test-and-Compare feature is usable on EW01 alone if a second thumbnail variant is wanted later,
     without a duplicate video.
   - **Kill criteria (proposed):** average view duration meaningfully below the recent baseline, OR
     comment tone repeatedly reads "cringe / AI filter / looks like a tract" → fall back to the
     inked/painted style for the next piece, don't force a 2nd retro pilot. Comparable-or-better on
     both → proceed to naming pilot pieces 2/3.
   - Shorts get their own, separate read later (once a retro short exists) — swipe-feed retention +
     comment tone, not thumbnail CTR.
3. **Format-split the grammar (corrected 2026-07-23 — matches livingpage's real numbers, not a
   blanket "no grids on shorts"):** the prior wording overstated the split. `/livingpage` §7 already
   runs the SAME move language on shorts and longs (slams/takeover/sacred-stillness/craft), just at a
   different mix — full-bleed beats run ~60-70% on shorts vs a ≤50% cap on long-form (§3b.3). Retro
   DNA follows that same ratio, not "shorts never grid." Tier grids + page-turns stay MORE common on
   16:9 long-form. A high-contrast, saturated, **non-halftone** thumbnail pass is mandatory (halftone
   + cream paper die at 168px / under VP9 compression).
4. **Only after the pilot wins** do we wire into `config.py` + skills + gates + `v2/SPEC.md` and talk
   about the wider slate.

Consistency comes from the **system** (§0) — one ink+print family with controlled variety — not from a
frozen filter across 76 episodes.

---

## 10. Lock process + gate honesty + versioning

**Where we are:** draft → my red-team ✅ → revised ✅ → re-red-team ✅ → $0 cleanup ✅ → **external
5-CLI panel (2026-07-23, DEGRADED — 3/5 quorum: cursor/claude/grok all verdict REVISE, gemini timed
out at 37s with an EPERM error, codex timed out at 300s) → findings verified in code + this doc
corrected (current step)** → free audience kitsch-test → full-quorum panel re-run (recommended — this
run never reached quorum) → pilot + A/B → sign-off → wire-in.

**Review log round 1:** `v2/_independent_review/20260723-193115/`. Top convergent finding (all 3
respondents): §1's "Seedream 4.5 proven for identity" claim was false — fixed. Also fixed: stale §8
map, missing pilot cost estimate, the "Kalam.ttf missing" false claim.

**Review log round 2 (full 5/5 quorum):** `v2/_independent_review/20260723-195503/`. All 5 still
REVISE — caught that round 1's fix itself mis-cited `[[locked-stills-provider-split]]` (resolved by
explicit user decision, see §1), plus new findings. **Punch-list progress against round 2 (session of
2026-07-23, same day):**
1. ✅ Ref-chaining plumbing wired + proven through `render_scene()` (§1/§8).
2. ✅ Aaron's locked reference rendered (§1/§8) — not yet chain-tested multi-scene.
3. ✅ Passion-Christ body tokens (`muscular`/`heroic`/`athletic`/`six-pack`/`v-taper`/`bodybuilder`)
   added to `config.VISUAL_BANNED_TOKENS` — closes the "Vision-only, no deterministic teeth" gap.
4. ✅ Format-split vs `/livingpage` resolved — user decision: **Remotion stays a separate engine**
   (§6), not a livingpage extension; the format-split ratio corrected to match livingpage's real
   60-70%/≤50% numbers instead of an invented "no grids on shorts" rule (§9.3).
5. ✅ Real named pilot plan + cost table (§9) — ONE piece (EW01) not three, grounded in its actual
   scene_plan.json + its own prior animator-tiering decision (≈$29-34, not a placeholder range).
6. ✅ A/B protocol corrected + user-confirmed (§9) — the original "same piece cut two ways" was
   mechanically broken (YouTube duplicate-content risk; Shorts swipe-feed never shows a thumbnail).
   Replaced with a between-subjects baseline comparison against the last 2-3 shipped longs.
7. Still open (lower-severity, deferred to before the pilot renders, not before this doc correction):
   3-script print-finish reconciliation, dot-crawl proven only on a slow push (not dynamic Kling
   motion), word-exact slam timing for Remotion (now explicitly BUILD, not port — §6).

These remaining items are real but lower-severity than the model contradiction — revisit before the
pilot, not before this correction pass.

**`/dna-check` — honest scope (it is NOT a $0 deterministic guarantee):**
- **Deterministic ($0):** watermark present (INV-27), landing hold (INV-26), active `VISUAL_STYLE`
  == the retro record, a print-finish provenance sidecar was written, Remotion used fonts from the
  locked manifest. (Mostly *provenance stamping*, not look-verification.)
- **Vision-audited (paid, not deterministic):** "dots visible but faces flat", "Christ dignified +
  marred-not-heroic on the cross", "Scripture has its distinct treatment", "SFX reverent not camp",
  "opens/closes on Christ". This is the *substance* of the DNA — it needs a paid Vision pass, not a
  free gate. Don't oversell dna-check as $0-deterministic.

**Versioning + migration (was missing):**
- This doc carries a **DNA version** (header). The reference card must **never out-number** it.
- **Migration policy for already-shipped non-retro episodes** (baroque / graphic_novel / painted):
  they are **grandfathered** — stamped with their own `VISUAL_STYLE`, NOT re-rendered. The retro DNA
  applies to **new** pieces from the pilot forward. If the DNA changes after N episodes, earlier
  retro episodes are grandfathered too unless a batch re-render is explicitly funded.

**Correction:** this line previously claimed "nothing costs render money until the pilot" — false;
R&D spend already happened this session (bake-offs, `_prove_it/`, `_seedream_ref/`, the DNA POC
animate pass, the hook iterations), tracked in `data/spend_ledger.jsonl`, not zero. What's actually
true: **no PILOT-BATCH render money moves until it's explicitly quoted (§9) and approved** — and the
pilot only after the free audience test + a pinned dial.
