# Swirls of Life — North-Star Prompt (production-locked)

Fable-authored, 2026-08-19. This is the one canonical, reusable prompt template
for every future Swirls of Life shot — HF CLI only (`hf generate create
nano_banana_pro`), reference images chained on every shot, validated across
both 9:16 and 16:9 on a real 8-shot John 4 sequence (see
`poc_living_water_ink_style_test/northstar_shortform/`).

## Template

```
One single storyboard page of hand-drawn animation development art, delicate ink
linework and watercolor on aged cream paper, laid out like a real found piece of
production art. Top-left title, handwrite: "SEQ: {SEQUENCE_NAME}". Top-right
frame number, handwrite: "F{NN}". Across the top, a row of exactly three small
storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1
(handwrite: "{PANEL_1_LABEL}") {PANEL_1_SUPPORT_SKETCH}, panel 2 (handwrite:
"{PANEL_2_LABEL}") {PANEL_2_SUPPORT_SKETCH}, panel 3 (handwrite: "{PANEL_3_LABEL}")
{PANEL_3_SUPPORT_SKETCH}. Below them, ONE large full-scene illustration filling
the lower half of the page — a {CAMERA_DISTANCE} shot: {MAIN_SCENE: subjects,
action, setting, lighting, mood, and every MUST-SHOW element named explicitly as
fully inside the frame}. {CHARACTER_CONTINUITY_LINES}. {SWIRL_DOSAGE_LINE}. Small
handwritten production notes integrated naturally on the page: {NOTES_AND_CAPTIONS,
each as its own handwrite: "..."}. No other text, letters, numbers, or words
appear anywhere on the page beyond the exact handwrite strings given above — no
invented captions, signs, inscriptions, or titulus. Palette: black ink, ochre,
muted brown, olive green, clay-red, touches of soft gold wash on aged cream paper
with visible grain. Not photorealistic, not anime, not Disney, no polished
graphic design, no clean comic-book inking, no Renaissance religious staging, no
glowing spiritual VFX — every blue or gold element behaves like literal wet ink
bleeding into paper, never a magic-particle glow.
```

## Slot rules (fill without re-deriving)

- `{SEQUENCE_NAME}` — a short title phrase, held CONSTANT across every page of one episode.
- `{NN}` — two-digit frame number, increments per shot (`F01`, `F02`, ...).
- `{PANEL_*_LABEL}` — **added 2026-08-20, Fable design-critique finding.** 2-3 words, always author it yourself — never leave the panel unlabeled and never let the model invent its own caption. The old template said "labeled" without giving the model a label to use; it improvised one (correct spelling, but unauthored, and inconsistently — see the Gold Exemplar note below). A model may still add small in-genre furniture the prompt doesn't explicitly forbid; the global "no other text" sentence in the template closes that off entirely.
- `{PANEL_*_SUPPORT_SKETCH}` — each panel is a small SUPPORTING sketch for this beat (a detail, a reaction, a prop, an establishing element) — never a duplicate of the main scene, and the main scene's own subject may appear in a panel only partially/incidentally, never as that panel's own focus.
- `{CAMERA_DISTANCE}` — WIDE / MEDIUM TWO-SHOT / CLOSE-UP / HELD SINGLE etc., stated explicitly.
- **MUST-SHOW elements** — added 2026-08-20. If a detail is load-bearing for the beat (a wound mark, a held object, a specific gesture), name it explicitly as "fully inside the frame" in the `{MAIN_SCENE}` text itself — a HELD SINGLE / CLOSE-UP crop can and will silently crop a requested detail out of frame otherwise (the Gold Exemplar's 9:16 dropped the nail marks this way; nobody caught it until an independent review looked for it, not just at it).
- **Similes in scene/panel text render literally, at maximum literalism** — added 2026-08-20. "A skull-shaped hill" was read as a giant, anatomically literal skull. When a detail should only be SUGGESTED, hedge it explicitly: "crags and hollow shadows that faintly suggest a skull, not a literal face."
- `{CHARACTER_CONTINUITY_LINES}` — the locked build text for each recurring character IN this shot, verbatim from the established builds. Continuity backup only — the chained `--image` reference files do the real likeness work. Never invent new face description. **If a character's continuity includes a halo (or any other ink element that is ALWAYS present, not tied to the episode's Swirls stage), say explicitly that it is separate from the `{SWIRL_DOSAGE_LINE}` and does not grow, spread, or merge with it** — added 2026-08-20 after the Gold Exemplar's own halo and Stage-3 dose merged into one object on the render, the opposite of the "not tied to any single figure" the dose asked for.
- `{SWIRL_DOSAGE_LINE}` — MANDATORY on every page, even Stage 0. **Only anchor the dose to elements that are actually visible inside THIS shot's own framing** (added 2026-08-20 — "along the base of the cross" was unrenderable on a HELD SINGLE crop that ends at the waist; anchor to the sky, the ground at the frame's own edges, or whatever the crop genuinely contains):
  - **Stage 0 (ABSENT):** *"Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page..."*
  - **Stage 1 (FIRST TRACE):** *"Stage 1 dosage: exactly one restrained thread of blue ink {rising from / curling out of ELEMENT}..."*
  - **Stage 2 (PRESENT):** *"Stage 2 dosage: the blue ink motif is quietly present — a few soft blue threads and one small watercolor bloom..."*
  - **Stage 3 (DIFFUSED):** *"Stage 3 dosage: the blue ink motif, with traces of muted gold, is woven through the whole scene..."*
  - Transitional beats (1→2, 2→3) state the exact intermediate dose in the same wet-ink language.
- `{NOTES_AND_CAPTIONS}` — each its own `handwrite: "..."`, 2-4 words, NEVER a sentence. KJV captions must be VERBATIM CONTIGUOUS fragments; a verse longer than 4 words splits across two stacked `handwrite:` lines, never elided mid-line.

## Render call

```
hf generate create nano_banana_pro --prompt "<filled template>" ^
  --image <path>\references\jesus_ref.png ^
  --image <path>\references\john4_woman_ref.png ^
  --aspect_ratio 9:16 --resolution 2k --wait
```

A shot with a recurring subject and no chained ref is a hard stop. **A second aspect ratio of the SAME shot counts as a recurring shot for this rule too (added 2026-08-20, "The Hem" 16:9 finding)** — a brand-new character rendered without a ref in 9:16, then rendered again text-only for 16:9, is two independent generations and will drift exactly like two different shots would; chain her crop into the 16:9 render even though it's "the same page." Eyeball every PNG at 1:1 — baked spelling, ref likeness, layout held, dose matches stage, **AND (added 2026-08-20, Fable design-critique finding) no un-requested text anywhere on the page, and every MUST-SHOW element actually visible in frame** — both failures on the Gold Exemplar passed the original 4-point checklist; an independent review looking specifically for missing/extra elements is what caught them. A Higgsfield 503 is transient — retry, don't rewrite. **AND (added 2026-09-05, Seedream 4.5 bake-off finding, episode 11's F08) no distinguishing mark authored for ONE named figure (e.g. the Samaritan's clay-red hem-trim) appears on any OTHER figure on the page, including Jesus** — a page's own prose usually only states "his ONLY distinguishing mark is X... not repeated anywhere else on HIS clothing," which a cheaper/less careful model can satisfy while still painting X onto a different figure; when authoring this kind of one-figure-only mark, add an explicit second clause naming who else must NEVER show it (e.g. "and no other figure on this page, including Jesus, ever wears this mark").

## Validation run — LOCKED 2026-08-19

8-shot John 4 short-form sequence (`poc_living_water_ink_style_test/northstar_shortform/`), shot list + KJV lines locked from `poc_living_sketchbook/_well_scene_coverage/_JACOBS_WELL_STRUCTURE.html`'s 60s short-form structure. All 16 stills (8 shots x 9:16 + 16:9) rendered clean on the first pass (1 transient Higgsfield 503, plain retry succeeded) — held under the hardest test yet: a true extreme close-up (shot 4) with zero drift from the wide establishing shot, AND two single-ref shots (shot 6 Jesus-only, shot 7 woman-only) that still matched their multi-ref siblings. Full filled prompts for all 8 shots are in `_prompts.json`; the render script is `render_northstar.py` (HF CLI only, both ratios).

Carried all the way to a finished 68.86s film in both formats — `THE_WELL_9x16.mp4` / `THE_WELL_16x9.mp4` — narration + multi-voice dialogue (4 voices) + a fresh water-themed score, landing-hold GREEN (INV-26). See `poc_living_water_ink_style_test/northstar_shortform/_REPORT.html` for the full build log, findings, and both finished cuts.

## 🥇 Gold exemplar — "The Cross" (2026-08-20, v1 — superseded by v2 below)

`examples/gold_exemplar_the_cross_9x16.png` / `examples/gold_exemplar_the_cross_16x9.png` —
imitate the composition discipline (a HELD SINGLE main illustration + 3
genuinely supporting, non-duplicate panels) and the restraint on a
sacred/heavy subject (a plain loincloth, faint ink wound marks, no gore).
**Do NOT imitate everything on this pair uncritically** — an independent
Fable design-critique (2026-08-20, full report in `poc_living_water_ink_style_test/
test_the_cross/DESIGN.md`) found real defects the original QC pass missed:
the 9:16's swirl merged with Jesus's halo instead of reading as diffused
Stage 3 (the 16:9 is closer, but still halo-adjacent, not the fix); the
9:16 cropped the nail marks out of frame entirely; Golgotha rendered as a
literal giant skull rather than a hill that merely suggests one; and the
16:9's panel captions were an UNAUTHORED model improvisation, not a
deliberate design choice (root cause: the template said "labeled" without
giving a label, and `jesus_ref.png` itself has a baked circled panel number
that reinforced the model's own genre habit). All fixed in the template
above (MUST-SHOW, panel labels, halo/dose separation, literalism warning,
global text lock) — see v2 below for the re-render.

## Hybrid panel variant (validated 2026-08-22, F01–F08; wired into `swirls_page.py` 2026-08-23)

The 3 top panels render in denser, more intense Durer-woodcut linework — the
same woodcut style covers use (see `NORTH_STAR_COVER_PROMPT.md`) — while the
main scene stays in the page's own gentle ink-and-watercolor wash. The
contrast between the two is the point: the panels read as sharper, more
cinematic "cuts," the main scene stays the soft found-page style. Validated
clean on Jacob's Ladder F08 (`swirls_pilot_01_jacobs_ladder\_style_test_
durer_woodcut\render_hybrid_panels.py`) — this was a disconnected style test
never wired into any real production script until now; episode 2 (Ashes)
shipped with the plain template instead purely because nothing pointed a new
episode at this validated recipe. **This is now the standard interior-page
treatment** (the user's own call, after watching episode 2): default new
episodes to `PageSpec(panel_style="woodcut_hybrid", ...)`; the plain
all-ink-wash treatment (`panel_style="ink_wash"`, still the field's default)
remains available by explicit choice, not the norm going forward.

```
... Across the top, a row of exactly three small storyboard panels, each with
a circled number 1, 2, 3 as its ONLY label — these three panels ONLY are
rendered in a deliberately different, more intense style from the rest of the
page: 16th-century Albrecht Durer woodcut linework blended with contemporary
cinematic landscape photography — dense parallel hatching, hard black
contours, ink-on-block texture, dramatic volumetric light rays, deep teal
shadows, golden-hour glow, photographic tonality. panel 1 (handwrite: "...")
{content}, drawn in that woodcut-cinematic style; panel 2 ... ; panel 3 ... .
Below them, ONE large full-scene illustration filling the lower half of the
page — returning fully to the page's OWN gentle hand-drawn style, delicate
ink linework and soft watercolor on aged cream paper, NOT the panels' denser
woodcut-cinematic treatment — a {CAMERA_DISTANCE}: {MAIN_SCENE}. ...
Palette for the MAIN SCENE ONLY: black ink, ochre, muted brown, olive green,
clay-red, touches of soft gold wash on aged cream paper with visible grain,
not photorealistic, not anime, no polished graphic design, no clean
comic-book inking, no glowing spiritual VFX. {MATERIAL_CLOSER} The three top
panels keep their own separate deep teal and gold cinematic woodcut palette,
described above, distinct from the main scene's palette.
```

Implemented as `swirls_page.py`'s `panel_style="woodcut_hybrid"` branch of
`assemble_still_prompt()` — the constants above (`WOODCUT_STYLE`,
`STYLE_OPEN_HYBRID`, `HYBRID_MAIN_BRIDGE`, `TEXT_LOCK_HYBRID`,
`HYBRID_PALETTE_PREFIX`/`HYBRID_PALETTE_CLOSER`) are sliced verbatim from the
validated test. Does NOT affect `assemble_animation_prompt()` — neither
variant's animation prompt describes rendering style, only motion.
`_validate_swirls_page_hybrid.py` proves byte-identical reproduction (plus
the module's own standard refs-manifest clause, which the one-off test
predates and never called — a disclosed, deliberate addition, not a
deviation from validated content).

## Animation prompt — see NORTH_STAR_ANIMATION_PROMPT.md (2026-08-20)

The clean, reusable animation-prompt template + the locked "the ink motif is
never an AI motion request" rule + the MOTION/FREEZE lane decision now live in
their own file, `NORTH_STAR_ANIMATION_PROMPT.md`, next to this one — written
directly from the user's own review of this session ("keep it simple, use
Focal Tour for freeze moments, lock a north star for the animation prompt
too"). The raw lessons below are kept as history/evidence for *why* that file
looks the way it does — read it first; come back here only for the specific
model-artifact findings (Kling seam, veo pot-hallucination) it references.

## Animation-tier lessons (rev 2, 2026-08-19 — superseded by NORTH_STAR_ANIMATION_PROMPT.md above for anything about swirl motion or fill-device choice; kept for the model-specific bugs found)

- **Never trust the video model's "stay frozen" compliance on the panel row — enforce it deterministically.** Round 1 asked for the title/3-panel row to stay frozen via prompt language alone; a contact-sheet review (sample 4 frames evenly across the clip, tile into one image, read once) caught a hallucinated word appearing mid-clip in a panel that was told to stay static, plus the swirl bleeding into an adjacent panel. Prompting alone is not enough. `lock_panels.py` is the fix: composite the SOURCE STILL's own top region back onto every frame of the rendered clip (measured freeze boundary: 9:16 top 43%, 16:9 top 40%, from the panel row's own bottom border) — pixel-guaranteed static regardless of what the model did there. Run this on every clip, every episode, no exceptions.
- **Never write "speaks the line" / "mouth completes a motion of speech" into a motion prompt.** This is a voice-over-narrated series (no lip-sync, ever, per the project's own locked rule) — any mouth-movement language WILL produce a talking-looking clip that can't match the actual audio. State pure expression/gaze instead: "lips stay closed and completely still, not speaking."
- **A "blink" prompt needs an explicit end-state.** "One deliberate blink, gaze settles on the viewer" was read by the model as close-and-stay-closed. State the full arc: closes, then opens again fully, ending wide open.
- **Cap swirl growth explicitly and expect to still see some overshoot.** "The current flows outward" reliably over-escalates on Kling into a wide river; adding an explicit end-size cap ("stays a thin calligraphic line, barely larger than the very first frame") reins it in substantially but not completely. Treat prompt-only swirl control as a partial mitigation, not a real fix — the real fix is pulling the swirl motif out of the AI generation and animating it as its own deterministic compositing layer (this project's existing ink-motion device toolkit — blue-line, wash-creep, tide-mark — is the right pattern to extend), not yet built.
- **Fill-strategy history, SUPERSEDED (rev 6, 2026-08-19) — see below for the current answer.** Three earlier attempts in the same session: (1) hard tpad freeze — flagged as dead/boring; (2) a whole-frame Ken-Burns zoom — still read as padding; (3) a hard-cut gallery tour through the page's own 3 panels — technically worked but the user judged it broken/corrupted on watch (the real cause turned out to be the panel-lock overlay's side effect, see the entry below, not the cuts themselves) and asked to revert to plain freeze. That plain freeze shipped as a stable baseline, but the underlying complaint (dead hold time) was never actually solved — it was deferred, not fixed. Once the user asked to properly solve it, a Fable-authored plan (grounded by reading this project's own `panel_animator/` device toolkit) replaced plain freeze with a per-shot DEVISED fill: **Lamplight** (`line_boil` + `raking_light`, shots 1/5/7 — the calm/atmospheric or fragile-clip shots), **Live Ink Hold** (a new small module, `ink_bloom.py` — a soft radial deepen-toward-ink-blue at a MANUALLY-VERIFIED point inside the swirl, shots 2/3/6), and **Halo Tour** (`focal_tour.render_clip` on the fill segment, using the already-measured `PANEL_BOXES`, shot 4). All modulated by `held_breath.energy_envelope` computed from REAL forced-aligned word timing (`narration.alignment.json`, generated via `veed_io/aligner.py`'s `forced_align_script` — this narration had no alignment file before). `build_fills.py` is the orchestrator; `assemble.py` now just concats its `{stem}__filled.mp4` output. Entirely $0 — no new AI generation for the fills themselves.
  - **wash_creep's own HSV color-isolation approach was tried first for Live Ink Hold and rejected** — sampled directly against this style's real renders (not assumed), the swirl's blue and Jesus's own indigo robe overlap heavily in hue; a full-frame mask lit up the robe, not the swirl. Manual per-shot points (eyeballed, then verified with a quick single-frame multi-candidate test BEFORE the expensive full frame-by-frame render) is the safe substitute — 4-5 minutes of calibration per shot, cheap insurance against a real visible defect.
  - **Shot 7 stays on Lamplight, not Live Ink Hold, deliberately** — its clip was fragile (3 regens needed just to get a clean base render, see the Kling/veo entries below), so the fill was kept as low-risk as possible rather than adding another processing layer on top.

## DEAD INK — companion motif system for sin/fear/doubt (Fable, 2026-08-20)

The Swirls of Life motif (blue-gold, "living ink") represents God's word / the
Holy Spirit / the gospel truth entering a scene. **DEAD INK** is its designed
counterpart — "dead" (Eph 2:1 "dead in trespasses and sins" → 2:5
"quickened") because in this grammar **evil is damage, not a rival power**:
it never gets a beautiful living form, never moves, never fights. Two motifs,
not one — Scripture treats sin and fear differently (cleansing vs.
strengthening), so one visual for both would muddy it. Two is also the
ceiling — no motif-per-emotion sprawl.

- **The Stain** (sin, guilt, uncleanness) — a cold grey-umber damp-stain
  soaked INTO THE PAPER ITSELF, not the scene: formless, matte, feathered
  damp edges, lying beneath the linework so every drawn line passes over it
  unbroken. At dose D2+ it crosses the drawn frame border into the page's
  own margin — scene shadow can never do that, which is the one detail that
  keeps it from ever reading as ordinary night/storm darkness. Grounded in
  Isa 1:18 ("scarlet... white as snow"), Ps 51:7 ("wash me... whiter than
  snow"), Jer 2:22.
- **The Fray** (fear, doubt, wavering) — the afflicted figure's OWN
  linework destabilized: broken/doubled/tremored contours, scratchy
  overworked hatching. Already half-precedented — F07 v2's "her
  cross-hatching drawn visibly looser now, almost flying" is an early form
  of this. Grounded in Jas 1:6 ("wavereth... like a wave of the sea"), Matt
  14:31. Still-only, forever — dispelling it means the line steadies, and
  that only ever changes between pages (a generative "line steadies" ask is
  a face-morph risk).
- **Rejected:** cords/tangles (too close to creature/horror territory, and
  collides with scenes that have LITERAL chains in the text, e.g. Mark 5:4);
  a grey flood/wash (indistinguishable from ordinary scene darkness in a
  render).

**Dosage (descending — the new axis the original 0→3 system doesn't have):**
Stain D3 (saturated, bounded to ≤⅓ page, never over a face) → D2 (one
defined stain; *turning* variant has its gospel-side edge already dried to a
pale ring — static geometry telling the story's direction, per LAW 0) → D1
(only the dried pale ring remains; paper INSIDE it is the cleanest cream on
the page — "made new," not just "back to normal") → D0 (canonical absence,
like Swirl Stage 0). Fray: FR3 (contour visibly incomplete) → FR2 (broken,
tremored) → FR1 (loose hatching, the validated F07 register) → FR0
(confident line). Crossing arcs: swirl rising, stain/fray falling, across an
episode's pages — the crossing point (swirl ≥ stain) IS the gospel turn.

**Coexistence on one page — the QUAD lock** (extends the Storm F06 triple
lock, which held on the hardest LAW 3 test yet):
1. Chromatic reservation — blue+gold belongs ONLY to the life motif/halo;
   the Stain is explicitly "no blue, no gold, no red."
2. Zone separation — a stated band of clean paper between them; **they never
   touch** (contact is exactly the bleed channel LAW 3 already found).
3. Form separation — smooth open calligraphic curl vs. formless feathered
   blot; "never swirl-shaped" / "never blot-shaped," stated both ways.
4. Substrate separation (the Stain's own contribution) — the swirl is drawn
   ON the page; the stain is damage IN the page, under the linework.
   Different diegetic layers, can't bleed into each other the way two
   on-page substances can.

**High-tide exclusion (deterministic, gate-able):** both motifs wet-and-big
never share a page — roughly `stainDose + swirlStage <= 4`.

**QC additions this system brings:** the stain must read cold/matte/under-
the-linework and cross the border (in-page, not in-scene); zero blue/gold/
red inside it; a clean-paper band between stain and swirl everywhere; and a
**pareidolia check** — no face/figure/creature accidentally readable in the
blot (the Gold Exemplar's literal-skull lesson: models over-literalize, and
a blot invites faces — a human eye must clear every one).

**Animation rule — see `NORTH_STAR_ANIMATION_PROMPT.md`: the dispelling
happens BETWEEN pages, never within one clip.** Full worked example ("The
Hem," Mark 5:25-34, both pages' still + animation prompts, discretion locks,
render script) in `poc_living_water_ink_style_test/test_the_cross/
render_the_hem.py`. **Status: VALIDATED, 2026-08-20** — both pages rendered
and passed (stills + animation), one real failure en route (a first
animation attempt let the page's own aging bleed instead of the drawn
stain — fixed by a page-global stillness fence + giving the rest of the
scene real story motion; see `NORTH_STAR_ANIMATION_PROMPT.md`'s VALIDATED
ledger for the full record). The Fray motif is still undemonstrated (no
still or clip test yet).
- **The panel-lock overlay (deterministic top-region freeze) was REMOVED from the pipeline, 2026-08-19 — do not re-add without the user asking.** It correctly fixed the hallucinated-text/swirl-bleed bug, but had a real side effect nobody anticipated: it made the top panel row 100% static against a 100% animated big scene, and the storyboard page's own hand-drawn border line between them (present in every still, never a problem before) started reading as a hard technical seam — "like two clips stitched together" — right from frame 0 of every shot. Traced by: user watched the raw HF-hosted clip directly (clean) and confirmed the raw downloaded file decodes with zero errors (`ffmpeg -v error -i x -f null -`), which isolated the cause to this project's own compositing, not the source render. Current pipeline (`assemble.py`) uses the raw animated clips directly, no overlay. If the hallucination/bleed bug resurfaces, the fix is in the PROMPT (reinforced FROZEN language in `animate_northstar.py`), which already resolved it once on its own before panel-lock was ever added — reach for that first, not the overlay.
- **Kling3.0 produced a visible line/seam artifact on this style, confirmed in the raw render itself (not this project's compositing).** User caught it watching the raw per-shot clips directly, before any assembly/panel-lock/concat touched them — isolated to the 3 shots rendered on Kling (4, 6, 7), never appeared on the 5 veo3_1_lite shots. Not reproduced as a static-frame artifact (checked full-res frame grabs from all 3 Kling clips, found nothing) — likely only visible in motion/playback. Fix applied: switched all 3 shots to veo3_1_lite instead of troubleshooting/rerolling Kling further. Contrary to this project's older documented veo weakness ("does not reliably execute a designed/cued gesture"), veo3_1_lite handled shot 7's real running locomotion well here — re-check that old finding before assuming veo can't do action for THIS style.
- **veo3_1_lite can invent a held object tied to a composition, resistant to positive-prompt correction.** Shot 7 (she runs, near a well with a waterpot visibly left behind) generated with a pot in her hands on 2 separate veo3_1_lite attempts — including a rewrite that explicitly added "her arms and hands are empty and swing freely... she carries nothing in either hand" (positive framing, per this project's own "Gemini/veo honors positives, drops negatives" finding) — no change. This reads as a strong compositional prior (running figure + nearby vessel = carrying it) that prompt language alone did not override twice. Third attempt on Kling3.0 rendered it correctly (empty hands, pot stays on the well) with no line-artifact recurrence for THIS composition specifically — the Kling line-artifact finding above is real but evidently not universal across every shot; when a specific composition is fighting one model, trying the other is a reasonable next step before more rerolls on the same model.
- **If a panel-cut or zoom fill IS revisited later:** the resolution-source bug is worth remembering even though the feature itself was reverted — crop any panel-region punch-in from the SOURCE STILL (2k), never from a rendered clip's last frame (veo3_1_lite renders as low as 720px tall, Kling ~1080px, both well under the still's 1536-2752px) — cropping a small region out of the low-res frame and blowing it up 5-6x is very visibly soft. Panel boxes are template-fixed per ratio and can be measured once via ink-density scan of the border lines (kept in git history in `assemble.py` if needed again).

## Recurring-prop identity check — POSITIVE, not just negative (user catch, 2026-09-06)

A prop build that describes itself only by what it must NOT look like can pass every
negative test while losing its actual identity entirely. Found on ep13's beam: `BEAM_BUILD`
was written purely as "single plank... no cross shape... no second timber" (fighting a real,
recurring hallucination — the model kept drawing a full crucifix). Every render that passed
that negative test did it by becoming smooth, pale, generic carpentry lumber — visually
disconnected from what the text actually names it (Mark 15:21/Luke 23:26: Simon bore "his
cross," Gk *stauros*, not "a beam"). Eleven renders shipped to GATE 2 before the user asked
the plain question: **"was he carrying a log or a cross?"**

**The fix pattern, not just this one prop:** any recurring object/costume/mark built mainly
from negative constraints ("no X, never Y, not Z-shaped") needs an equally explicit POSITIVE
identity clause stating what it concretely IS, era-and-location-grounded, so a render can't
satisfy the negative rule by drifting into generic/anonymous territory. For ep13's beam that
meant: named as a Roman *patibulum* (execution crossbeam) specifically, not just "a beam";
rough-hewn/adze-scarred/weathered-dark (era-accurate — 1st-century Roman military-grade
timber, reused, NOT fresh pale lumber); and one empty mortise notch cut into the wood (the
single detail that reads as "this attaches to a cross" without ever drawing the forbidden
second timber). Verified this doesn't reopen the original hallucination — the notch is
explicitly carved INTO the one timber, never a separate piece, and the "trace one straight
line end to end" test explicitly ignores it.

**Standing QC addition (every episode, every recurring prop/artifact, not just ep13):**
alongside whatever negative shape/count/mark rules a prop needs, ask **"does this read as
era-compliant, location-compliant, and biblically/historically identifiable as the actual
named object — or has it drifted into something generic?"** A prop that only ever gets
checked against what it must avoid will silently drift toward the least distinctive thing
that satisfies the avoidance rule.
