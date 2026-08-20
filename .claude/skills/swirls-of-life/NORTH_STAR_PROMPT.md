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
labeled storyboard panels numbered 1, 2, 3: panel 1 {PANEL_1_SUPPORT_SKETCH},
panel 2 {PANEL_2_SUPPORT_SKETCH}, panel 3 {PANEL_3_SUPPORT_SKETCH}. Below them,
ONE large full-scene illustration filling the lower half of the page — a
{CAMERA_DISTANCE} shot: {MAIN_SCENE: subjects, action, setting, lighting, mood}.
{CHARACTER_CONTINUITY_LINES}. {SWIRL_DOSAGE_LINE}. Small handwritten production
notes integrated naturally on the page: {NOTES_AND_CAPTIONS, each as its own
handwrite: "..."}. Palette: black ink, ochre, muted brown, olive green,
clay-red, touches of soft gold wash on aged cream paper with visible grain. Not
photorealistic, not anime, not Disney, no polished graphic design, no clean
comic-book inking, no Renaissance religious staging, no glowing spiritual VFX —
every blue or gold element behaves like literal wet ink bleeding into paper,
never a magic-particle glow.
```

## Slot rules (fill without re-deriving)

- `{SEQUENCE_NAME}` — a short title phrase, held CONSTANT across every page of one episode.
- `{NN}` — two-digit frame number, increments per shot (`F01`, `F02`, ...).
- `{PANEL_*_SUPPORT_SKETCH}` — each panel is a small SUPPORTING sketch for this beat (a detail, a reaction, a prop, an establishing element) — never a duplicate of the main scene.
- `{CAMERA_DISTANCE}` — WIDE / MEDIUM TWO-SHOT / CLOSE-UP / HELD SINGLE etc., stated explicitly.
- `{CHARACTER_CONTINUITY_LINES}` — the locked build text for each recurring character IN this shot, verbatim from the established builds. Continuity backup only — the chained `--image` reference files do the real likeness work. Never invent new face description.
- `{SWIRL_DOSAGE_LINE}` — MANDATORY on every page, even Stage 0:
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

A shot with a recurring subject and no chained ref is a hard stop. Eyeball every PNG at 1:1 (baked spelling, ref likeness, layout held, dose matches stage). A Higgsfield 503 is transient — retry, don't rewrite.

## Validation run — LOCKED 2026-08-19

8-shot John 4 short-form sequence (`poc_living_water_ink_style_test/northstar_shortform/`), shot list + KJV lines locked from `poc_living_sketchbook/_well_scene_coverage/_JACOBS_WELL_STRUCTURE.html`'s 60s short-form structure. All 16 stills (8 shots x 9:16 + 16:9) rendered clean on the first pass (1 transient Higgsfield 503, plain retry succeeded) — held under the hardest test yet: a true extreme close-up (shot 4) with zero drift from the wide establishing shot, AND two single-ref shots (shot 6 Jesus-only, shot 7 woman-only) that still matched their multi-ref siblings. Full filled prompts for all 8 shots are in `_prompts.json`; the render script is `render_northstar.py` (HF CLI only, both ratios).

Carried all the way to a finished 68.86s film in both formats — `THE_WELL_9x16.mp4` / `THE_WELL_16x9.mp4` — narration + multi-voice dialogue (4 voices) + a fresh water-themed score, landing-hold GREEN (INV-26). See `poc_living_water_ink_style_test/northstar_shortform/_REPORT.html` for the full build log, findings, and both finished cuts.

## Animation-tier lessons (rev 2, 2026-08-19 — locked, apply to every future episode)

- **Never trust the video model's "stay frozen" compliance on the panel row — enforce it deterministically.** Round 1 asked for the title/3-panel row to stay frozen via prompt language alone; a contact-sheet review (sample 4 frames evenly across the clip, tile into one image, read once) caught a hallucinated word appearing mid-clip in a panel that was told to stay static, plus the swirl bleeding into an adjacent panel. Prompting alone is not enough. `lock_panels.py` is the fix: composite the SOURCE STILL's own top region back onto every frame of the rendered clip (measured freeze boundary: 9:16 top 43%, 16:9 top 40%, from the panel row's own bottom border) — pixel-guaranteed static regardless of what the model did there. Run this on every clip, every episode, no exceptions.
- **Never write "speaks the line" / "mouth completes a motion of speech" into a motion prompt.** This is a voice-over-narrated series (no lip-sync, ever, per the project's own locked rule) — any mouth-movement language WILL produce a talking-looking clip that can't match the actual audio. State pure expression/gaze instead: "lips stay closed and completely still, not speaking."
- **A "blink" prompt needs an explicit end-state.** "One deliberate blink, gaze settles on the viewer" was read by the model as close-and-stay-closed. State the full arc: closes, then opens again fully, ending wide open.
- **Cap swirl growth explicitly and expect to still see some overshoot.** "The current flows outward" reliably over-escalates on Kling into a wide river; adding an explicit end-size cap ("stays a thin calligraphic line, barely larger than the very first frame") reins it in substantially but not completely. Treat prompt-only swirl control as a partial mitigation, not a real fix — the real fix is pulling the swirl motif out of the AI generation and animating it as its own deterministic compositing layer (this project's existing ink-motion device toolkit — blue-line, wash-creep, tide-mark — is the right pattern to extend), not yet built.
- **Fill-strategy history, SUPERSEDED (rev 6, 2026-08-19) — see below for the current answer.** Three earlier attempts in the same session: (1) hard tpad freeze — flagged as dead/boring; (2) a whole-frame Ken-Burns zoom — still read as padding; (3) a hard-cut gallery tour through the page's own 3 panels — technically worked but the user judged it broken/corrupted on watch (the real cause turned out to be the panel-lock overlay's side effect, see the entry below, not the cuts themselves) and asked to revert to plain freeze. That plain freeze shipped as a stable baseline, but the underlying complaint (dead hold time) was never actually solved — it was deferred, not fixed. Once the user asked to properly solve it, a Fable-authored plan (grounded by reading this project's own `panel_animator/` device toolkit) replaced plain freeze with a per-shot DEVISED fill: **Lamplight** (`line_boil` + `raking_light`, shots 1/5/7 — the calm/atmospheric or fragile-clip shots), **Live Ink Hold** (a new small module, `ink_bloom.py` — a soft radial deepen-toward-ink-blue at a MANUALLY-VERIFIED point inside the swirl, shots 2/3/6), and **Halo Tour** (`focal_tour.render_clip` on the fill segment, using the already-measured `PANEL_BOXES`, shot 4). All modulated by `held_breath.energy_envelope` computed from REAL forced-aligned word timing (`narration.alignment.json`, generated via `veed_io/aligner.py`'s `forced_align_script` — this narration had no alignment file before). `build_fills.py` is the orchestrator; `assemble.py` now just concats its `{stem}__filled.mp4` output. Entirely $0 — no new AI generation for the fills themselves.
  - **wash_creep's own HSV color-isolation approach was tried first for Live Ink Hold and rejected** — sampled directly against this style's real renders (not assumed), the swirl's blue and Jesus's own indigo robe overlap heavily in hue; a full-frame mask lit up the robe, not the swirl. Manual per-shot points (eyeballed, then verified with a quick single-frame multi-candidate test BEFORE the expensive full frame-by-frame render) is the safe substitute — 4-5 minutes of calibration per shot, cheap insurance against a real visible defect.
  - **Shot 7 stays on Lamplight, not Live Ink Hold, deliberately** — its clip was fragile (3 regens needed just to get a clean base render, see the Kling/veo entries below), so the fill was kept as low-risk as possible rather than adding another processing layer on top.
- **The panel-lock overlay (deterministic top-region freeze) was REMOVED from the pipeline, 2026-08-19 — do not re-add without the user asking.** It correctly fixed the hallucinated-text/swirl-bleed bug, but had a real side effect nobody anticipated: it made the top panel row 100% static against a 100% animated big scene, and the storyboard page's own hand-drawn border line between them (present in every still, never a problem before) started reading as a hard technical seam — "like two clips stitched together" — right from frame 0 of every shot. Traced by: user watched the raw HF-hosted clip directly (clean) and confirmed the raw downloaded file decodes with zero errors (`ffmpeg -v error -i x -f null -`), which isolated the cause to this project's own compositing, not the source render. Current pipeline (`assemble.py`) uses the raw animated clips directly, no overlay. If the hallucination/bleed bug resurfaces, the fix is in the PROMPT (reinforced FROZEN language in `animate_northstar.py`), which already resolved it once on its own before panel-lock was ever added — reach for that first, not the overlay.
- **Kling3.0 produced a visible line/seam artifact on this style, confirmed in the raw render itself (not this project's compositing).** User caught it watching the raw per-shot clips directly, before any assembly/panel-lock/concat touched them — isolated to the 3 shots rendered on Kling (4, 6, 7), never appeared on the 5 veo3_1_lite shots. Not reproduced as a static-frame artifact (checked full-res frame grabs from all 3 Kling clips, found nothing) — likely only visible in motion/playback. Fix applied: switched all 3 shots to veo3_1_lite instead of troubleshooting/rerolling Kling further. Contrary to this project's older documented veo weakness ("does not reliably execute a designed/cued gesture"), veo3_1_lite handled shot 7's real running locomotion well here — re-check that old finding before assuming veo can't do action for THIS style.
- **veo3_1_lite can invent a held object tied to a composition, resistant to positive-prompt correction.** Shot 7 (she runs, near a well with a waterpot visibly left behind) generated with a pot in her hands on 2 separate veo3_1_lite attempts — including a rewrite that explicitly added "her arms and hands are empty and swing freely... she carries nothing in either hand" (positive framing, per this project's own "Gemini/veo honors positives, drops negatives" finding) — no change. This reads as a strong compositional prior (running figure + nearby vessel = carrying it) that prompt language alone did not override twice. Third attempt on Kling3.0 rendered it correctly (empty hands, pot stays on the well) with no line-artifact recurrence for THIS composition specifically — the Kling line-artifact finding above is real but evidently not universal across every shot; when a specific composition is fighting one model, trying the other is a reasonable next step before more rerolls on the same model.
- **If a panel-cut or zoom fill IS revisited later:** the resolution-source bug is worth remembering even though the feature itself was reverted — crop any panel-region punch-in from the SOURCE STILL (2k), never from a rendered clip's last frame (veo3_1_lite renders as low as 720px tall, Kling ~1080px, both well under the still's 1536-2752px) — cropping a small region out of the low-res frame and blowing it up 5-6x is very visibly soft. Panel boxes are template-fixed per ratio and can be measured once via ink-density scan of the border lines (kept in git history in `assemble.py` if needed again).
