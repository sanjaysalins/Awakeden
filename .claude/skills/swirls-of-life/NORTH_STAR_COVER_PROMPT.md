# Swirls of Life — North-Star Cover Prompt (production-locked)

Extracted verbatim 2026-08-23 from episode 1's proven cover script
(`poc_living_water_ink_style_test/swirls_pilot_01_jacobs_ladder/_style_test_durer_woodcut/render_covers.py`
+ `animate_covers.py`) — no creative rewrite, just promoting proven content
out of a one-off test script into a canonical doc, the same way
`NORTH_STAR_PROMPT.md` did for interior pages. Until this doc existed, covers
had **no** single source of truth: episode 2 was built by hand-editing
episode 1's script and silently dropped the warm/cool lighting contrast, and
its back cover grew an unrequested border/caption strip that nothing in
either prompt ever asked for. This doc + `swirls_cover.py`'s `CoverSpec`
close that gap the same way `swirls_page.py` already closed it for interior
pages.

Covers are their own storyboard-page STYLE variant — full-bleed 16th-century
Durer woodcut linework blended with cinematic landscape photography, no
panels, no captions beyond a baked title/subtitle. They bookend an episode's
locked interior pages (plain ink-wash or the hybrid woodcut-panel variant —
see `NORTH_STAR_PROMPT.md`'s "Hybrid panel variant" section); the covers'
own woodcut look is deliberately more intense than the interior's gentle ink
wash — that contrast is part of why a book's cover reads as a cover.

## Template (still)

```
{FIGURE_DESCRIPTION: character(s), pose, scale-in-frame, what they carry}.
Vast wind-scoured wilderness, rugged rocky {hill country | terrain}, sweeping
{stony | desert} valleys, carved structural cloud forms in an open sweeping
sky. {LIGHTING_SLOT — MUST name at least one warm element and one cool
element, see the Lighting-contrast law below}, cinematic atmospheric haze,
photographic tonality. {OPTIONAL_BACKGROUND_DETAIL, e.g. "Far behind him,
small and fading into the haze, the low goat-hair tents of the home he has
fled."} 16th-century Albrecht Durer woodcut linework blended with
contemporary cinematic landscape photography, dense parallel hatching, hard
black contours, ink-on-block texture, vertical 9:16 aspect ratio, figure
isolated in the lower third, stationary camera, wide static shot,
ultra-crisp. Near the {top | bottom} of the frame, bold engraved wood-block
title lettering, carved in the same dense woodcut style as the rest of the
image — thick confident carved strokes, not a modern font, not a decorative
flourish font, no drop shadow, no glow, no banner or box behind it, sitting
naturally within the composition, reading: "{TITLE}", with smaller matching
lettering beneath it reading: "{SUBTITLE}". The artwork fills the entire
image edge to edge — never a drawn border, picture frame, caption strip, or
margin band around the scene. No other text, letters, numbers, or words
appear anywhere on the image beyond these two lines — no watermark, no
invented captions. Avoid: modern clothing, busy foreground, bright neon
colors, deformed anatomy, blurry rendering, smooth photorealism without
linework{EXTRA_AVOID}.
```

## LOCKED constants (do not edit per episode)

- The woodcut/cinematic style sentence ("16th-century Albrecht Durer woodcut
  linework blended with contemporary cinematic landscape photography...
  ultra-crisp") — verbatim, identical front and back.
- The title-lettering style clause ("bold engraved wood-block title
  lettering... sitting naturally within the composition") — verbatim.
- The text lock ("No other text, letters, numbers, or words appear anywhere
  on the image beyond these two lines — no watermark, no invented
  captions.") — verbatim.
- The base Avoid list ("modern clothing, busy foreground, bright neon
  colors, deformed anatomy, blurry rendering, smooth photorealism without
  linework") — episodes may APPEND to this (e.g. "visible wounds, blood,
  gore"), never remove from it.

## SLOT: lighting-contrast law (defect #1's fix)

A cover's lighting slot must name **at least one warm element and at least
one cool element** — cinematic warm/cool contrast is part of the cover
style's own identity, not a decoration. An episode chooses WHICH contrast
(dusk ochre sky vs. deep teal shadow; grey storm breaking into gold; dawn
gold vs. lingering blue night) — it may never delete the contrast entirely.

**Counter-example, what NOT to do:** episode 2's front cover asked for
"under a flat grey sky, low scrub and stone, no vivid color anywhere" and
"deep grey and ash-toned shadow, a single shaft of pale, cold light" — zero
warm tokens anywhere in the lighting slot. This is exactly what killed the
warm-vs-cool contrast that made episode 1's covers read as a movie poster
instead of a monochrome photo. `swirls_verify.py`'s SW-L1 lint checks for
this automatically (≥1 warm-family token + ≥1 cool-family token) before any
render spend.

## SLOT: edge-to-edge law (defect #2's fix — prevention only)

The template above already states "the artwork fills the entire image edge
to edge — never a drawn border, picture frame, caption strip, or margin
band around the scene." Neither episode's original prompt ever asked for a
border — episode 2's back cover grew one anyway, a pure model hallucination.
This clause is prevention, not detection: the actual catch is
`swirls_verify.py`'s V2 image audit, which bans a drawn border/frame/
caption-strip/margin band in its rubric (the same banned-token category the
main engine's own `pipeline/visual_render.py` already checks for — simply
never pointed at a swirls-of-life cover until now).

## Other slot rules

- `{FIGURE_DESCRIPTION}` — authored per cover, grounded in the episode's own
  narration; chain a face + full-figure ref for the recurring character.
- `{TITLE}` — grounded, not invented: drawn from the narration's own line
  (episode 1: "THE LADDER HE SAW" from "Jacob saw a ladder to heaven in a
  dream"). Front cover only.
- `{SUBTITLE}` — a real scripture reference (episode 1 front: "GENESIS 28").
- Back cover: closing text is the episode's own already-locked closing
  caption verbatim (episode 1: "HE IS THAT LADDER", F08's own caption), and
  its subtitle is the real NT verse the episode's thread points to (episode
  1: "JOHN 1:51"). Title position: **front = top of frame, back = bottom of
  frame** — validated pattern, keep it.
- Aspect ratio: `9:16` (matches the interior pages' short-form format).
- Model: `nano_banana_pro`, `--resolution 2k`, refs chained (face + staff/
  object/location refs as relevant — same ref-chaining rule as interior
  pages, `render_cover_still` hard-stops on a missing ref).

## Template (animation)

**Correction, 2026-08-23 (red-team catch):** front and back genuinely need
DIFFERENT text-lock strength — they are not one template with a `{title |
closing}` swap. Episode 1's front-cover animation failed twice (text
duplicated, then faded) before the strong "pixel-for-pixel identical...
never duplicating or doubling" wording fixed it on attempt 3. Episode 1's
back-cover animation never had that problem — it rendered clean on the
FIRST attempt with a much lighter "stays perfectly static and unchanged"
lock. Presenting these as one merged template (as an earlier draft of this
doc did) silently applied the strong front wording to back too, which is
not what shipped and not what was validated for back specifically.

**Front-cover template** (the strong lock — proven necessary here):

```
Stationary camera, locked wide static shot, no pan, no zoom. The baked title
lettering at the top of the frame — both the large title and the smaller
line beneath it — stays pixel-for-pixel identical for every single frame of
the clip: same exact opacity from first frame to last, never fading in or
out, never dissolving, never duplicating or doubling, never drifting
position. {LIVING_DETAIL_PROSE — the ONE thing that moves: a stride, a
mantle stirring, a robe hem in the wind}; {LIGHTING_INVARIANCE — name the
light's own quality, e.g. "the dusk light stays exactly as warm and dim as
it already is, unchanged for the whole clip"}; {STATIC_BACKGROUND_ELEMENTS,
if any — e.g. "the distant tents stay exactly as drawn"}; no new figure,
mark, or text appears anywhere on the frame at any point.
```

**Back-cover template** (the lighter lock — validated clean on first
attempt; use this by default, escalate to the front-cover's strong wording
only if a back-cover render actually shows text drift):

```
Stationary camera, locked wide static shot, no pan, no zoom. The baked
closing lettering at the bottom of the frame stays perfectly static and
unchanged for the whole clip. {LIVING_DETAIL_PROSE}; {LIGHTING_INVARIANCE};
no new figure, mark, or text appears anywhere on the frame at any point.
```

Model: `veo3_1_lite`, native `--duration 4` by default (raise via
`CoverSpec.clip_duration` if the freeze-hold gate in `swirls_verify.py`
demands a longer clip for the page this cover's slot borders).

## Render calls

```
hf generate create nano_banana_pro --prompt "<filled still template>" ^
  --image <face_ref.png> --image <other refs...> ^
  --aspect_ratio 9:16 --resolution 2k --wait

hf generate create veo3_1_lite --prompt "<filled animation template>" ^
  --start-image <cover_still.png> --aspect_ratio 9:16 --duration 4 --wait
```

## Validation

Episode 1's two covers (`front_cover_woodcut.png`, `back_cover_woodcut.png`)
are the reference renders this doc was extracted from — both clean on first
still render, front-cover animation clean on attempt 3 (strong text-lock
wording above), back-cover animation clean on first attempt (light text-lock
wording above). `_validate_swirls_cover.py` byte-diffs `CoverSpec` still-prompt
assembly against these exact prompts (modulo the one new documented
edge-to-edge clause), and separately byte-diffs the front and back
ANIMATION prompts each against their own real source template (front
against the strong lock, back against the light lock — not against each
other) to prove the module reproduces both correctly. Episode 2's covers are
the DEFECTIVE example this doc exists to prevent recurring — not a
reference.
