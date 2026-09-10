# FLOW_RUN_SHEET.md — "My Lord and My God" — hand this whole file to Flow's agent, once

**v2 — rebuilt after a real run.** A first version of this document was actually run through Google
Flow (see `_flow_delivery_v6/_REVIEW.html` in this folder for the full visual review of what came
back). Two real, independent findings drove this rebuild: Flow's own agent, unprompted, sent back
two messages recommending the exact restructuring below (phases instead of one interleaved pass,
explicit ACTION tags, a compact SUCCESS line per step) — and a side-by-side look at the actual
delivered images found 4 specific, real content defects, now fixed inline where they happened. See
the "What changed in v2" note at the very end of this file for the full list.

This is a single, fully self-contained execution document. Paste it into a FRESH Google Flow
project as one message (or, if it's too long to paste at once, split it at any `## Step` or
`## PHASE` heading — never mid-step). The agent then runs the whole thing itself, start to finish,
with no human re-pasting anything in between.

**Before you paste anything, read Section 0.5 (Flow settings and cost) below** — Flow's Agent asks
permission before spending credits by default, which would silently stall an "unattended" run.

**Companion, human-facing document** (the rationale, the "why," the design history, and the
episode's assembly-timing plan): `GOOGLE_FLOW_BRIEF.md` in this same folder. This file supersedes
that one on reference generation, deliberately: Thomas (Step R1) is generated from text alone —
he's unique to this one episode, nothing to stay consistent with. Jesus (Step R2) is the one
deliberate exception — he recurs across every episode in this whole series, so R2 attaches this
project's existing series-wide Jesus reference as an Ingredient to keep his face consistent with
every other episode, not generated from text alone. That one file is the only upload anywhere in
this run; everything else — Thomas, all 8 stills, all 8 clips — is fully Flow-generated with
nothing else provided. Everything else in the brief still holds. If anything else looks
inconsistent between the two files, this one wins for generation purposes.

---

## Section 0 — Message to the Flow agent

**Read this entire message before generating anything. Then execute every phase in order, on your
own, start to finish.**

You are producing the complete visual footage for one 60-second episode, "My Lord and My God"
(John 20:24–29): first 2 character reference images, then 8 storyboard stills, then 8 video clips —
each clip animated from its matching still. That is 10 stills and 8 clips — 18 generations, run in
four phases (Section headed "PHASE 1" through "PHASE 4" below). You do all 18 in this one
conversation, in the order written, without pausing for approval and without asking me anything. I
am not watching between steps. You send me exactly two messages: one line now — "Read. 18
generations, 4 phases. Starting Phase 1." — and the FINAL REPORT (Phase 4) when everything is done.

These rules apply to every step. None of them relax at any point.

1. **Prompts are verbatim.** Every generation has its prompt between a line reading `PROMPT STARTS`
   and a line reading `PROMPT ENDS`. Send that text to the image or video model exactly as written —
   do not summarize, shorten, reorder, translate, "improve," merge, or add to it. If Flow offers any
   prompt-enhancement, auto-improve, or rewrite option, turn it off for this whole session.
2. **Each step stands alone.** Everything a step needs is inside that step. Carry nothing forward
   from an earlier step except the images the step names by label.
3. **Nobody speaks. Ever.** No dialogue, no character speech, no narrator, no music, in any clip.
   Lips stay closed on every figure in every clip. All spoken lines are added later, outside Flow.
4. **Images carry forward by label, tracked in a running log — not by Flow's own filenames.** Flow's
   own auto-generated names will NOT match REF_THOMAS / STILL_0N / CLIP_0N — expect completely
   different, content-descriptive names (a real run came back with names like
   `Storyboard_page_of_animation_art...jpeg`). After EVERY single generation, immediately add one
   line to a running log you keep for this whole session: `[our label] = [Flow's own filename or a
   one-line description of exactly what it shows]`. This log is the real mechanism for matching
   outputs to labels — never rely on a title/name field actually holding our label text; it won't.
   You will generate REF_THOMAS and REF_JESUS in Phase 1. Phase 2 and Phase 3 steps tell you which
   of those two to attach as Ingredients — attach exactly the ones named, those images from this
   conversation, never a file, never a substitute, never a re-made version. Every clip is animated
   from the still labeled in its own step, as the starting frame.
5. **Check every result yourself before moving on.** Each step lists a compact SUCCESS line plus a
   full checklist below it. If any line fails, regenerate that one generation once, unchanged. If it
   fails again, keep the better of the two, write the failure under Flags in the FINAL REPORT, and
   continue. If Flow refuses to generate something, write that under Flags and continue. Never fix a
   defect by editing a prompt. Never stop the run.
6. **One output per generation.** If Flow gives you more than one candidate, judge them against the
   step's checks, keep exactly one, log only that one, and never use the others for anything. A real
   run once delivered an extra, unrequested image — watch for this and don't log a second output
   under any label.
7. **Do not skip, reorder, repeat, or add steps.** Follow the four phases in order: PHASE 1 (R1,
   R2) → PHASE 2 (STILL_01 through STILL_08) → PHASE 3 (CLIP_01 through CLIP_08) → PHASE 4 (FINAL
   REPORT). Within a phase, follow its steps in the order written. Generate nothing not on this
   sheet.
8. **Aspect ratio is vertical 9:16 for every generation.** Clip length varies by shot — the table in
   Global Settings below gives each clip's real target. When a target exceeds one generation's
   normal length, ask for the model's longest available single-clip length for that generation, and
   report the actual length delivered either way.

---

## Section 0.5 — Before you paste this: Flow settings and cost

Do this in Flow itself, before pasting Section 0 onward, or the "unattended, never stop" behavior
in Section 0 rule 5 will silently stall waiting for clicks:

1. **Turn off generation confirmation.** In Flow's settings, set "Confirm before generating" (or
   whatever your account calls the credit-spend confirmation prompt) to Off / Never. Telling the
   agent not to pause does not change this setting on its own — it's a separate Flow-side toggle.
2. **Set output count to 1 per generation**, if Flow offers a "number of candidates" setting. Flow
   bills per generated output, not per request — leaving this above 1 pays for images/clips this
   plan then discards anyway.
3. **Know your cost ceiling before you start.** This plan is 18 generations (10 stills, 8 clips),
   plus up to 2 extra retries on CRITICAL checks (Section 3) — so the real range is 18-36 generation
   attempts. Video credit cost per clip varies a lot by model on Flow. Check your own plan's current
   per-generation credit cost for whichever still and video models you're using, multiply by up to
   36, and confirm that's a spend you're happy with before pasting Section 0. This document doesn't
   know your Flow tier or model choice, so it can't total this for you — do that check once, here,
   not partway through the run.
4. **Upload the one reference file this run uses, before pasting Section 0.** File:
   `jesus_ref_upscaled3x.png`, in this episode's own folder
   (`F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_pilot_02_my_lord_and_my_god\jesus_ref_upscaled3x.png`)
   — the same Jesus likeness used across every other Swirls-of-Life episode, upscaled for a cleaner
   Ingredient attachment. Add it to this Flow project so it's ready to attach when the agent reaches
   Step R2. This is the only file provided anywhere in this run — Thomas, every still, and every
   clip are otherwise generated by Flow itself from text alone.
5. **Count outputs against the target when the zip comes back.** A real run of an earlier version of
   this document delivered 11 images against a 10-still target (2 refs + 8 stills) — Flow can
   occasionally emit an extra or duplicate output. Count files against 10 stills + 8 clips = 18, and
   use the running label-mapping log (Section 0 rule 4) to spot any extra or orphaned file before
   assembly.

---

## Global settings

| Setting | Value |
|---|---|
| Aspect ratio | 9:16, always |
| Image model | whatever this Flow project's image model is currently set to |
| Video model | whatever this Flow project's video model is currently set to |
| Retry budget, ordinary checks | 1 extra attempt (2 attempts total) |
| Retry budget, CRITICAL checks (marked per step) | 2 extra attempts (3 attempts total) before falling back |
| Prompt enhancement / auto-improve | OFF for the whole session |
| Total generations | 10 stills + 8 clips = 18 (up to 36 attempts with retries) |
| Labels | REF_THOMAS, REF_JESUS, STILL_01–STILL_08, CLIP_01–CLIP_08 |

**Per-clip length target**, from this episode's real `ASSEMBLY_PLAN.md` timing. Ask for the
model's longest available single-clip length on the three marked LONG; the rest are fine at the
model's normal default (typically 8-10s):

| Clip | Real target | Ask for |
|---|---|---|
| CLIP_01 Front Cover | ~7.1s | default length |
| CLIP_02 F01 | ~11.4s | **LONG — longest available** |
| CLIP_03 F02 | ~5.5s | default length |
| CLIP_04 F03 | ~7.3s | default length |
| CLIP_05 F04 | ~12.8s | **LONG — longest available** (still needs a freeze-hold added afterward in assembly — see the note at the end of Step S5 in Phase 2) |
| CLIP_06 F05 | ~4.9s | default length |
| CLIP_07 F06 | ~3.8s | default length |
| CLIP_08 Back Cover | ~11.6s (incl. landing hold) | **LONG — longest available** |

Report whatever length Flow actually delivers in the FINAL REPORT — assembly trims or holds
against the real footage, not the target.

Which references each still attaches (restated inside each step too):

| Step | Attach |
|---|---|
| S1 Front Cover | REF_THOMAS (likeness only — this still's own style is the woodcut style in its own prompt, same as S8) |
| S2 F01 | REF_THOMAS |
| S3 F02 | REF_THOMAS |
| S4 F03 | REF_THOMAS + REF_JESUS |
| S5 F04 | REF_THOMAS + REF_JESUS |
| S6 F05 | REF_THOMAS + REF_JESUS |
| S7 F06 | REF_THOMAS + REF_JESUS |
| S8 Back Cover | none |

---

## Section 3 — The check-and-retry loop (applied after every generation)

After every generation and before the next step: for a still, look at the whole image; for a clip,
watch it end to end AND listen to its audio track — not just the opening seconds, not video only.
Check the compact SUCCESS line first, then go through the full checklist below it line by line. Each
step's full checklist is grouped "Must not fail" and "Also check" — some "Must not fail" lines are
additionally marked **CRITICAL**.

- All pass → log it (Section 0 rule 4) → next.
- An ordinary line fails → regenerate that one generation once, same prompt, same attached images,
  nothing changed. Still failing → keep the attempt that passes more lines, log it, write the failed
  line under Flags in the FINAL REPORT, continue.
- **A CRITICAL line fails → regenerate up to twice more** (three attempts total), same prompt and
  Ingredients each time, nothing changed. Still failing on the third attempt → keep the best of the
  three, log it as normal so the run can continue, but write it under a separate **CRITICAL — review
  before assembly** heading at the top of Flags in the FINAL REPORT, not mixed in with ordinary
  flags. This never stops the run — Flow can't ask me anything mid-session — but it makes sure a
  genuinely broken shot doesn't disappear quietly into a list of 17 other notes.

For every clip, two comparisons: the element the prompt names as moving must be visibly different
between the first frame and the last frame; every element the prompt says stays as drawn must be
unchanged in content and position between the first frame and the last frame (allow for the normal
frame-to-frame redraw of a generative video model — "unchanged" here means nothing new appears,
nothing drawn disappears, nothing shifts position; it does not mean literal pixel equality, which no
eye or agent can actually certify from playback). A clip whose first and last frames show no real
change in the element that was supposed to move fails — that has happened on an entire batch before,
on this exact episode.

---
---

# PHASE 1: CHARACTER REFERENCE GENERATION

## Step R1 [REF_THOMAS]

- **ACTION:** `generate_image` | **Inputs:** Text only, no Ingredients
- **SUCCESS:** 1 figure? Yes. Squarish weathered face, dark hair/beard? Yes. Clay-red robe over
  cream tunic? Yes. No blue/gold, no halo? Yes. Outline one steady unbroken line? Yes. Plain paper
  ground, no text? Yes.

```
PROMPT STARTS
A single clean character reference image of one figure on a plain aged-cream paper ground, no background scene: hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. A sturdy middle-aged Galilean man with a squarish weathered face, heavy dark brows, deep-set questioning eyes, dark hair and a short thick dark beard flecked with grey, a plain robe of muted clay-red wash over an undyed cream tunic, a rough olive-brown mantle across one shoulder, drawn in dense workmanlike cross-hatching; he wears no blue and no gold anywhere. Standing three-quarter view, close enough to read the face clearly, wide enough to read the robe and build, calm neutral expression, arms visible at his sides, steady confident single-struck ink line. Period, 1st-century Roman Judea — simple ankle-length tunics in undyed cream or muted natural-dye colors, a looser mantle draped over one shoulder, a woven or roped belt, plain leather sandals — no visible buttons, zippers, buckles, or metal fasteners of any kind beyond simple cloth ties. No eyeglasses, no wristwatches, no modern haircut shapes, no bright synthetic-looking dye colors. High resolution, sharp linework, no blur, no text, no caption, no background scene — just the figure on a plain aged-cream paper ground.
PROMPT ENDS
```

Full checklist:

Must not fail — **CRITICAL, all lines** (six downstream shots, S2-S7, depend on this reference):
- Exactly one figure, face clearly readable, robe and build readable, arms at his sides.
- Squarish weathered face, heavy dark brows, dark hair, short thick dark beard flecked with grey.
- Clay-red robe over an undyed cream tunic, olive-brown mantle over one shoulder.
- No blue and no gold anywhere on him. No halo.
- His outline is one single confident unbroken line — no broken, doubled, or tremored line.
- No text, letters, numbers, caption, or scene — plain aged-cream paper ground only.

Also check:
- Ink linework and watercolor on grained paper — not photoreal, anime, 3D, or glossy.
- Hands correct, no extra limbs, no duplicate or transparent figure.
- No buttons, zippers, buckles, eyeglasses, wristwatch, or modern haircut.

All lines pass → log this image as REF_THOMAS. Go to Step R2.
Any line fails → regenerate up to twice more (three attempts total, the CRITICAL rule in Section 3),
same prompt, nothing changed. Still failing on the third attempt → keep the best attempt, log it as
REF_THOMAS anyway (the run can't stop to ask), but write it under **CRITICAL — review before
assembly** at the top of Flags in your FINAL REPORT, since a wrong-looking Thomas here carries into
S2 through S7. Go to Step R2. Do not ask. Do not edit the prompt. REF_THOMAS is never regenerated
after this step.

---

## Step R2 [REF_JESUS]

- **ACTION:** `generate_image` | **Inputs:** REF: `jesus_ref_upscaled3x.png` (uploaded, per Section
  0.5). Do not attach REF_THOMAS.
- **SUCCESS:** Face/hair/beard match the uploaded reference's identity? Yes. Indigo/charcoal robes?
  Yes. Faint incomplete halo, not a solid disc? Yes. Both palms open, no blood/wounds? Yes. Plain
  paper ground, no text? Yes.

```
PROMPT STARTS
Using the attached reference image as the exact likeness guide for this figure's face, hair, beard, and build — keep his identity consistent with that reference image, redrawn fresh in the house style described below, not copied or traced. A single clean character reference image of one figure on a plain aged-cream paper ground, no background scene: hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. A first-century Jewish man in his early thirties, lean from travel, weathered calm face, dark textured shoulder-length hair, short natural beard, drawn in broad confident economical ink strokes, loose layered robes of deep indigo and charcoal watercolor that pool and bloom and leave paper exposed, a faint incomplete calligraphic halo of muted gold-and-blue curls close around his head, never a solid disc. Standing three-quarter view, close enough to read the face clearly, wide enough to read the robe and build, both hands open at chest height with palms visible, calm neutral expression. Period, 1st-century Roman Judea — simple ankle-length tunics in undyed cream or muted natural-dye colors, a looser mantle draped over one shoulder, a woven or roped belt, plain leather sandals — no visible buttons, zippers, buckles, or metal fasteners of any kind beyond simple cloth ties. No eyeglasses, no wristwatches, no modern haircut shapes, no bright synthetic-looking dye colors. High resolution, sharp linework, no blur, no text, no caption, no background scene — just the figure on a plain aged-cream paper ground.
PROMPT ENDS
```

Full checklist:

Must not fail — **CRITICAL, all lines** (four downstream shots, S4-S7, depend on this reference):
- Face, hair, and beard genuinely match the attached reference image's identity — the specific
  person shown in the uploaded file, not just a generic plausible first-century man.
- Exactly one figure, face clearly readable, robe and build readable.
- Both hands open at chest height, both palms fully visible. No blood, no red, no wound on either palm.
- Halo: a faint, incomplete ring of gold-and-blue calligraphic curls close around the head — not a solid disc, not a glow, not sparkle.
- Dark textured shoulder-length hair, short natural beard, early thirties, lean.
- Robes of deep indigo and charcoal watercolor.
- No text, letters, numbers, caption, or scene — plain aged-cream paper ground only.

Also check:
- Ink linework and watercolor on grained paper — not photoreal, anime, 3D, or glossy; no Renaissance staging.
- Hands correct, five fingers each, no extra limbs, no duplicate or transparent figure.
- No buttons, zippers, buckles, eyeglasses, wristwatch, or modern haircut.

All lines pass → log this image as REF_JESUS. Go to Phase 2, Step S1.
Any line fails → regenerate up to twice more (three attempts total, the CRITICAL rule in Section 3),
same prompt and the same uploaded reference file, nothing changed. Still failing on the third
attempt → keep the best attempt, log it as REF_JESUS anyway (the run can't stop to ask), but write
it under **CRITICAL — review before assembly** at the top of Flags in your FINAL REPORT, since a
wrong-looking Jesus here carries into S4 through S7. Go to Phase 2. Do not ask. Do not edit the
prompt. REF_JESUS is never regenerated after this step.

---
---

# PHASE 2: STORYBOARD STILL GENERATION

Generate all 8 stills in this phase before generating any clip. Do not animate a still the moment
you make it — that happens later, in Phase 3.

## Step S1 [STILL_01] — Front Cover

- **ACTION:** `generate_image` | **Inputs:** REF: `REF_THOMAS` (likeness only)
- **Continuity anchor:** same woodcut rendering technique as Step S8 (Back Cover) — both are cover
  art, one shared style.
- **SUCCESS:** Same woodcut engraving style as Back Cover, not a modern comic/poster style? Yes.
  Door reads shut with only a narrow gap, Thomas small and partial, not standing in an open doorway?
  Yes. Title exactly "MY LORD AND MY GOD" once + "JOHN 20"? Yes. Warm+cool contrast present? Yes.
  Art runs edge to edge, no margin band? Yes.

```
PROMPT STARTS
16th-century Albrecht Dürer woodcut linework blended with contemporary cinematic landscape photography — dense parallel hatching, hard black contours, ink-on-block texture, dramatic volumetric light rays, photographic tonality. This is the exact same rendering technique as this episode's Back Cover shot — the same dense woodcut hatching, the same carved wood-block lettering, the same cinematic-landscape treatment — not a modern comic-book or movie-poster illustration style, not clean cel-shaded color, not a bold sans-serif or slab title font. Stationary camera, wide static shot, ultra-crisp. Vertical 9:16 frame. No storyboard panel grid, no "SEQ:"/frame-number labels — this is cover art, not a story page. The exterior of a plain stone house on a narrow street at dusk, seen from the street itself. A heavy wooden door fills the center-right of the frame, almost entirely CLOSED — shut and barred, its old grain and iron fittings catching the last low light, held small in the lower third against the house's stone wall rising above it — this door is NOT open, does not swing wide, and Thomas does NOT stand in an open doorway. Only a narrow vertical gap, no wider than a hand's breadth, remains where the door has not fully met the frame, and one thin bar of warm lamplight escapes through that gap alone — the street beyond the door stays hidden, not visible through any open doorway. In that narrow sliver of light, Thomas is glimpsed small, partial, and shadowed — most of his body hidden behind the door's own edge, only a fraction of him visible, his raised palm-out hand catching the light's edge, his face turned from it in refusal. He is a small detail in this composition, never the main, fully-visible subject. Above the doorway and the house's stone shoulder, a strip of open dusk sky and the dark rooftops of the narrow street recede into shadow. Warm amber lamplight spills in that single thin bar beside the door — the only warm note in the whole frame; cold blue-grey dusk fills the street, the stone, and the sky above, deep teal shadow pooling at the door's foot. No other figure anywhere in this frame. No halo, no glow, no spiritual VFX. Stage 0 dosage: no blue or gold Swirls-of-Life ink motif anywhere on this page. Near the top of the frame, bold engraved wood-block title lettering, carved in the same dense woodcut style as the rest of the image — thick confident carved strokes, NOT a modern font, not a decorative flourish font, no drop shadow, no glow, no banner or box behind it, sitting naturally within the composition, reading: "MY LORD AND MY GOD" — write this exact phrase once, as one continuous title, do not repeat any word in it. Smaller matching carved lettering beneath it reading: "JOHN 20". No other text, letters, numbers, or words appear anywhere on the image beyond these two lines. The artwork fills the entire image edge to edge — never a drawn border, picture frame, caption strip, or margin band around the scene; at the bottom edge of the frame (opposite the title), the scene's own artwork runs all the way to the canvas edge, fully painted, no blank paper showing. Period costume: Thomas wears a simple ankle-length tunic in undyed cream, a looser clay-red-and-olive mantle draped over one shoulder, a woven or roped belt, plain leather sandals — no visible buttons, zippers, buckles, or metal fasteners of any kind beyond simple cloth ties, no eyeglasses, no wristwatch, no modern haircut shapes. Avoid: modern clothing, busy foreground, bright neon colors, deformed anatomy, blurry rendering, smooth photorealism without linework.
PROMPT ENDS
```

Full checklist:

Must not fail:
- **CRITICAL** — the door reads as shut, not open: only a narrow gap of light, Thomas only
  partially visible through it, not standing fully in an open doorway with the whole street behind
  him. This exact defect (door wide open, Thomas fully visible, whole street visible) has happened
  on a real render of this shot.
- **CRITICAL** — rendered in the same woodcut-engraving technique as Step S8's Back Cover — dense
  hatching, hard black contours, carved-looking title lettering — not a modern comic-book or
  movie-poster illustration style. This exact defect (a bold cel-shaded style with a generic title
  font) has happened on a real render of this shot.
- Title reads exactly "MY LORD AND MY GOD", written once, no repeated word. Subtitle reads exactly "JOHN 20". No other text anywhere on the image.
- At least one genuinely warm note (the lamplight in the door gap) AND at least one genuinely cool note (the dusk street/sky) both clearly present in the same image — not one flat temperature.
- The artwork runs fully to the edge of the frame on all sides — no blank paper margin band anywhere, especially the edge opposite the title (the bottom).
- No storyboard panel grid, no "SEQ:" or frame-number label anywhere — this is a cover, not a story page.
- Thomas matches REF_THOMAS: squarish weathered face, heavy dark brows, dark hair, short thick dark beard flecked with grey — glimpsed small in the door gap, not the main subject of the frame.
- No halo on Thomas or anyone. No blue or gold ink motif anywhere on the page.

Also check:
- No modern clothing, no modern objects, no deformed anatomy, no blurry rendering.

All lines pass → log this image as STILL_01. Go to Step S2.
An ordinary line fails → regenerate once: same prompt, same Ingredient, nothing changed; still
failing, keep the better attempt, log it as STILL_01, write it under Flags, go to Step S2. A
CRITICAL line fails → regenerate up to twice more (three attempts total); still failing, keep the
best attempt, log it as STILL_01, write it under **CRITICAL — review before assembly** at the top
of Flags, go to Step S2. Do not stop. Do not ask. Do not edit the prompt. Do not regenerate
REF_THOMAS.

---

## Step S2 [STILL_02] — F01 "I will not believe"

- **ACTION:** `generate_image` | **Inputs:** REF: `REF_THOMAS`
- **Continuity anchor:** the room's own recurring details (plastered stone walls, shuttered
  lattice window, heavy wooden door, small clay oil lamp) carry forward unchanged across S2-S7 —
  this is the same room throughout, just at different times of day.
- **SUCCESS:** Jesus absent? Yes. Thomas's line visibly shaky/broken vs. the disciples' steady
  line — an obvious, unmistakable contrast? Yes. Blue thread arcs low with a clear gap to his palm,
  never touching? Yes. SEQ/F01 header + 3 panels + caption exact, nothing extra? Yes.

```
PROMPT STARTS
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain, laid out like a real found piece of production art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F01". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "not with them") a small sketch of a shut wooden door with its heavy bar in place; panel 2 (handwrite: "the proof") a small plain study of a single iron nail lying on its side, drawn as a quiet dry object; panel 3 (handwrite: "eight days") a small sketch of a low-burned oil lamp beside a shuttered window, its oil nearly spent. Below them, ONE large full-scene illustration filling the lower half of the page — a MEDIUM WIDE shot: a plain lamplit room at evening, a shuttered window on the back wall. Three of the other disciples stand together at the left, faces alight with joy, the foremost mid-gesture of telling, his open hands lifted toward Thomas, fully inside the frame. Thomas stands apart at the right, turned half away, his near arm raised with his palm out toward the group in refusal, that hand fully inside the frame and unobstructed, jaw set, mouth closed, eyes averted. Empty lamplit floor between them. Jesus is not in this scene and does not appear anywhere on the page. The three disciples: steady, confident, single-struck ink lines and even hatching. Thomas alone is drawn as if the artist's hand was visibly trembling while inking him — his outline actually shaky and uneven, broken into short interrupted strokes that don't quite meet, redrawn two or three times so a second and third faint ghost-line runs close beside his true contour, his cross-hatching scratchy, nervous, and overworked compared to the calm even hatching on every other figure — this must be immediately, unmistakably obvious at a glance, not a subtle texture difference; every OTHER figure on this page (the three disciples) stays a steady, single-struck confident line, so the contrast between Thomas's shaky line and their calm lines reads instantly. Thomas himself stays one solid, still figure, never blurred, never a double image. One restrained thread of blue ink, with the faintest trace of muted gold, rises from the foremost disciple's open lifted hands and arcs LOW across the open floor directly toward Thomas's raised palm, reaching nearly to the level of his hand — a clear, deliberate, visible GAP remains between the thread's end and his palm; the thread stops there and does NOT touch his hand or his figure — this gap is a hard rule, not a suggestion. The thread touches nothing and no one else, one smooth unbroken confident calligraphic line, sharing nothing of Thomas's shaky tremored line character. Small handwritten production notes: a caption beneath the main scene, handwrite: "I will not believe", and a corner note, handwrite: "NOTE: line unsteady". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus — this includes not adding any shot-type or camera-framing label anywhere on the page itself (for example, never write words like "CLOSE TWO-SHOT", "WIDE SHOT", "MEDIUM SHOT", or any other scene-description text as if it were part of the artwork), and not extending, completing, or adding to any caption beyond the exact words quoted above. Period: 1st-century Roman Judea, Jerusalem — an upper room in a modest stone house. Plain plastered stone walls, a shuttered wood-lattice window with no glass, a heavy wooden door on a simple wood or iron bar, worn stone or packed-earth floor, a small clay oil lamp with a pinched wick and no visible chimney or glass. Simple ankle-length tunics in undyed cream or muted natural-dye colors, a looser mantle draped over one shoulder, a woven or roped belt, plain leather sandals — no visible buttons, zippers, buckles, or metal fasteners of any kind beyond simple cloth ties. No eyeglasses, no wristwatches, no modern haircut shapes, no bright synthetic-looking dye colors. No electric light anywhere — only the oil lamp's glow and daylight through the shutter. Architecture stays plain: no carved relief work, no stained glass, no arches beyond a simple doorway.
PROMPT ENDS
```

Full checklist:

Must not fail:
- Jesus is absent, does not appear anywhere on the page.
- **CRITICAL** — Thomas's outline reads as visibly shaky, broken, and doubled — an obvious,
  unmistakable contrast against the three disciples' steady single-struck lines, not a subtle
  texture difference. A real render of this shot has come back with Thomas's line reading just as
  calm and steady as everyone else's — that is a fail.
- The blue thread arcs LOW from the disciple's hands toward Thomas's palm and stops with a clear visible gap — it does not touch him, and it does not rise straight up as an undirected vertical squiggle (a real defect on an earlier version of this exact shot).
- No halo on anyone.
- Top-left reads "SEQ: THOMAS", top-right reads "F01", corner note reads "NOTE: line unsteady". Exactly three small panels, labeled only with a circled 1/2/3, their handwritten captions reading "not with them", "the proof", "eight days". Main caption reads "I will not believe". No other letters, numbers, or words anywhere — no invented shot-type labels, no extended captions.
- Thomas matches REF_THOMAS: squarish weathered face, heavy dark brows, dark hair, short thick dark beard flecked with grey, clay-red robe over cream tunic.

Also check:
- Thomas wears and carries no blue and no gold anywhere.
- Ink-and-watercolor on grained cream paper — not photoreal, anime, 3D, or glossy. No speech bubble, thought bubble, text box, or banner around any note.
- No extra limbs, no malformed hands, no duplicate, blurred, or transparent figure.
- Era: no buttons, zippers, buckles, eyeglasses, wristwatches, modern haircuts, or electric light; tunic, mantle, sandals only.

All lines pass → log this image as STILL_02. Go to Step S3.
An ordinary line fails → regenerate once: same prompt, same Ingredient, nothing changed; still
failing, keep the better attempt, log it as STILL_02, write it under Flags, go to Step S3. A
CRITICAL line fails → regenerate up to twice more (three attempts total); still failing, keep the
best attempt, log it as STILL_02, write it under **CRITICAL — review before assembly** at the top
of Flags, go to Step S3. Do not stop. Do not ask. Do not edit the prompt. Do not regenerate
REF_THOMAS.

---

## Step S3 [STILL_03] — F02 "Eight Days"

- **ACTION:** `generate_image` | **Inputs:** REF: `REF_THOMAS`
- **Continuity anchor:** same room as S2 — plastered stone walls, shuttered lattice window, heavy
  wooden door, the same clay oil lamp, now later in the evening and burning lower.
- **SUCCESS:** Thomas still fully in the room, no door/exit shown? Yes. His line still visibly
  shaky/broken, unchanged from S2? Yes. Lamp reads low and dim? Yes. Jesus absent? Yes. SEQ/F02
  header + 3 panels + caption exact, nothing extra? Yes.

```
PROMPT STARTS
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain, laid out like a real found piece of production art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F02". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "the door") the same shut barred door, unchanged; panel 2 (handwrite: "the lamp burns low") a small study of the same oil lamp beside the shuttered window, its flame smaller now, its oil visibly lower than before; panel 3 (handwrite: "yet he stayed") a small sketch of a pair of sandaled feet, planted still on the floor, not turned toward any door or exit. Below them, ONE large full-scene illustration filling the lower half of the page — a MEDIUM WIDE shot, quieter than the page before: the same plain room, later in the evening, the lamp burning lower now. Thomas stands alone at the right of the frame, apart from the others but still fully inside the same room — he has not left, fully inside the frame, arms now at his sides, no longer raised in active refusal, but his face still set and unconvinced, eyes lowered rather than meeting anyone's gaze. The three disciples are visible in the middle distance at the left, seated or settled for the evening, quiet, steady confident single-struck ink lines and even hatching, paying Thomas no particular attention — this is a quiet in-between moment, not a confrontation. Thomas alone is still drawn as if the artist's hand was visibly trembling while inking him — his outline actually shaky and uneven, broken into short interrupted strokes that don't quite meet, redrawn two or three times so a second and third faint ghost-line runs close beside his true contour, cross-hatching scratchy, nervous, and overworked — exactly as unsteady as on the page before, immediately and unmistakably obvious at a glance, not a subtle texture difference — nothing has changed in his doubt, only time has passed. No blue ink motif appears anywhere near Thomas in this shot. Jesus is not in this scene and does not appear anywhere on the page. Small handwritten production notes: a caption beneath the main scene, handwrite: "yet he stayed", and a corner note, handwrite: "NOTE: line still unsteady". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus — this includes not adding any shot-type or camera-framing label anywhere on the page itself (for example, never write words like "CLOSE TWO-SHOT", "WIDE SHOT", "MEDIUM SHOT", or any other scene-description text as if it were part of the artwork), and not extending, completing, or adding to any caption beyond the exact words quoted above. Period: 1st-century Roman Judea, Jerusalem — an upper room in a modest stone house. Plain plastered stone walls, a shuttered wood-lattice window with no glass, a heavy wooden door on a simple wood or iron bar, worn stone or packed-earth floor, a small clay oil lamp with a pinched wick and no visible chimney or glass. Simple ankle-length tunics in undyed cream or muted natural-dye colors, a looser mantle draped over one shoulder, a woven or roped belt, plain leather sandals — no visible buttons, zippers, buckles, or metal fasteners of any kind beyond simple cloth ties. No eyeglasses, no wristwatches, no modern haircut shapes, no bright synthetic-looking dye colors. No electric light anywhere — only the oil lamp's glow and daylight through the shutter. Architecture stays plain: no carved relief work, no stained glass, no arches beyond a simple doorway.
PROMPT ENDS
```

Full checklist:

Must not fail:
- Thomas is still fully inside the room — he has not left, not shown near or through any door/exit.
- **CRITICAL** — Thomas's outline reads as visibly shaky, broken, and doubled — the same
  unmistakable, obvious-at-a-glance character as S2, not smoothed toward one clean confident line.
  A real render of this shot has come back with Thomas's line reading calm and steady — that is a
  fail.
- The oil lamp in panel 2 and in the main scene reads as burning low: a small flame, oil visibly reduced, dimmer than a fresh-lit lamp would read.
- Jesus is absent, does not appear anywhere on the page. No blue ink motif appears near Thomas.
- Top-left reads "SEQ: THOMAS", top-right reads "F02", corner note reads "NOTE: line still unsteady". Exactly three panels labeled "the door", "the lamp burns low", "yet he stayed". Main caption reads "yet he stayed". No other letters, numbers, or words anywhere — no invented shot-type labels, no extended captions.
- Thomas matches REF_THOMAS: squarish weathered face, heavy dark brows, dark hair, short thick dark beard flecked with grey, clay-red robe over cream tunic.

Also check:
- Thomas wears and carries no blue and no gold anywhere. No halo on anyone.
- Ink-and-watercolor on grained cream paper — not photoreal, anime, 3D, or glossy.
- No extra limbs, no malformed hands, no duplicate, blurred, or transparent figure.
- Era: no buttons, zippers, buckles, eyeglasses, wristwatches, modern haircuts, or electric light.

All lines pass → log this image as STILL_03. Go to Step S4.
An ordinary line fails → regenerate once: same prompt, same Ingredient, nothing changed; still
failing, keep the better attempt, log it as STILL_03, write it under Flags, go to Step S4. A
CRITICAL line fails → regenerate up to twice more (three attempts total); still failing, keep the
best attempt, log it as STILL_03, write it under **CRITICAL — review before assembly** at the top
of Flags, go to Step S4. Do not stop. Do not ask. Do not edit the prompt. Do not regenerate
REF_THOMAS.

---

## Step S4 [STILL_04] — F03 "Peace be unto you"

- **ACTION:** `generate_image` | **Inputs:** REF: `REF_THOMAS` + REF: `REF_JESUS` (Jesus's first
  appearance in this episode)
- **Continuity anchor:** same room as S2/S3, now filled with morning light; the same heavy wooden
  door, still shut and barred.
- **SUCCESS:** Door fully shut, no gap, no opening? Yes. Thomas's line still visibly shaky/broken
  (unresolved)? Yes. Halo only on Jesus, faint and incomplete? Yes. No thread touching Thomas?
  Yes. SEQ/F03 header + 3 panels + caption exact, nothing extra? Yes.

```
PROMPT STARTS
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain, laid out like a real found piece of production art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F03". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "doors being shut") the same shut door, still barred; panel 2 (handwrite: "peace be unto you") a small sketch of one open hand raised in blessing; panel 3 (handwrite: "stood in the midst") a small sketch of an empty patch of floor, nothing marking how he came to be there. Below them, ONE large full-scene illustration filling the lower half of the page — a MEDIUM WIDE shot: the same plain room, now filled with morning light through the shuttered window. The heavy door in the background is fully shut and barred, exactly as drawn before — no gap, no opening. Jesus stands at the center of the room, having simply appeared there, one hand raised open at chest height in a plain gesture of blessing, his face calm and glad, turned generally toward the group rather than at any one person yet. The other disciples stand in a loose cluster to one side, caught mid-reaction — surprise easing into joy, a few hands half-raised. Thomas stands among them, not singled out, not yet approached, his outline still drawn as if the artist's hand was visibly trembling while inking him — shaky and uneven, broken into short interrupted strokes that don't quite meet, a second and third faint ghost-line running close beside his true contour, cross-hatching scratchy and nervous — unchanged from the earlier pages, immediately and unmistakably obvious at a glance, since nothing has happened yet to resolve his doubt; every OTHER figure in this scene, including Jesus and the other disciples, stays a steady, single-struck confident line, so Thomas's shaky line reads as a clear, unmistakable contrast. Jesus has a faint incomplete calligraphic halo of muted gold-and-blue curls around his head, never a solid disc. No blue ink motif elements point toward or touch Thomas in this shot — if any thread is shown at all, it stays close around Jesus's own figure only, touching no one, not reaching toward anyone yet. Small handwritten production notes: a caption beneath the main scene, handwrite: "Peace be unto you", and a corner note, handwrite: "NOTE: no door opened". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus — this includes not adding any shot-type or camera-framing label anywhere on the page itself (for example, never write words like "CLOSE TWO-SHOT", "WIDE SHOT", "MEDIUM SHOT", or any other scene-description text as if it were part of the artwork), and not extending, completing, or adding to any caption beyond the exact words quoted above — panel 3's caption reads exactly "stood in the midst" and nothing more. Period: 1st-century Roman Judea, Jerusalem — an upper room in a modest stone house. Plain plastered stone walls, a shuttered wood-lattice window with no glass, a heavy wooden door on a simple wood or iron bar, worn stone or packed-earth floor, a small clay oil lamp with a pinched wick and no visible chimney or glass. Simple ankle-length tunics in undyed cream or muted natural-dye colors, a looser mantle draped over one shoulder, a woven or roped belt, plain leather sandals — no visible buttons, zippers, buckles, or metal fasteners of any kind beyond simple cloth ties. No eyeglasses, no wristwatches, no modern haircut shapes, no bright synthetic-looking dye colors. No electric light anywhere — only the oil lamp's glow and daylight through the shutter. Architecture stays plain: no carved relief work, no stained glass, no arches beyond a simple doorway.
PROMPT ENDS
```

Full checklist:

Must not fail:
- **CRITICAL** — the door in the background is fully shut and barred — no gap, no opening, no visible mechanism for how Jesus arrived. This exact family of defect (a door opening when it must not) has happened on a real render in this episode already.
- **CRITICAL** — Thomas's outline reads as visibly shaky, broken, and doubled — the same
  unmistakable, obvious-at-a-glance character as S2/S3. It does NOT read as one clean, steady,
  fully confident line here — his doubt has not resolved yet at this point in the story.
- Halo on Jesus only — a faint incomplete ring of curls, never a solid disc. No halo on Thomas or anyone else.
- No blue-ink thread touches or points toward Thomas.
- Top-left reads "SEQ: THOMAS", top-right reads "F03", corner note reads "NOTE: no door opened". Exactly three panels labeled "doors being shut", "peace be unto you", "stood in the midst" — panel 3's caption is exactly those three words, nothing added. Main caption reads "Peace be unto you". No other letters, numbers, or words anywhere — no invented shot-type labels, no extended captions.
- Thomas matches REF_THOMAS; Jesus matches REF_JESUS (deep indigo and charcoal robes, dark shoulder-length hair, short beard).

Also check:
- Thomas wears and carries no blue and no gold anywhere.
- Jesus's face reads calm and glad, turned generally toward the group, not singling out Thomas yet.
- Ink-and-watercolor on grained cream paper — not photoreal, anime, 3D, or glossy.
- No extra limbs, no malformed hands, no duplicate, blurred, or transparent figure.
- Era: no buttons, zippers, buckles, eyeglasses, wristwatches, modern haircuts, or electric light.

All lines pass → log this image as STILL_04. Go to Step S5.
An ordinary line fails → regenerate once: same prompt, same two Ingredients, nothing changed; still
failing, keep the better attempt, log it as STILL_04, write it under Flags, go to Step S5. A
CRITICAL line fails → regenerate up to twice more (three attempts total); still failing, keep the
best attempt, log it as STILL_04, write it under **CRITICAL — review before assembly** at the top
of Flags, go to Step S5. Do not stop. Do not ask. Do not edit the prompt. Do not regenerate
REF_THOMAS or REF_JESUS.

---

## Step S5 [STILL_05] — F04 "Reach hither"

- **ACTION:** `generate_image` | **Inputs:** REF: `REF_THOMAS` + REF: `REF_JESUS`
- **Continuity anchor:** same room, morning light, disciples drawn back into a loose ring behind.
- **SUCCESS:** Rendered in real ink-and-watercolor with visible color washes, NOT a graphite pencil
  sketch? Yes. Clear gap between the two hands, not touching? Yes. Thomas standing, not kneeling?
  Yes. Nail-marks small and dry, no blood? Yes. SEQ/F04 header + 3 panels + caption exact, nothing
  extra? Yes.

```
PROMPT STARTS
One single storyboard page of hand-drawn animation development art, delicate ink linework and rich watercolor color washes on aged cream paper with visible grain, laid out like a real found piece of production art. This page MUST be fully colored ink-and-watercolor, with the same black, ochre, muted-brown, olive-green, clay-red, and soft-gold palette as every other page in this set, real visible color washes throughout — it must NOT be a graphite pencil sketch, must NOT be monochrome or uncolored line art, must NOT look like an unfinished grey under-drawing. Not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F04". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "the wounds") a close study of Jesus's one open palm, a single faint dry nail-mark; panel 2 (handwrite: "reach hither") a small sketch of Thomas's own hand, half-raised, uncertain; panel 3 (handwrite: "be not faithless") a small sketch of the bare gap of air between two reaching hands, nothing touching. Below them, ONE large full-scene illustration filling the lower half of the page — a MEDIUM TWO-SHOT: the same room, morning light through the shuttered window, the other disciples drawn back into a loose still ring behind. Jesus stands at the left, now turned fully and specifically toward Thomas — singled out from the group, unlike the previous page — both open hands held out toward Thomas at chest height, palms toward him, a single small faint dry ink nail-mark in each palm — the mark is a small quiet ink mark only, never blood, never torn flesh, no red anywhere on or near his hands — both palms fully in frame. Thomas stands at the right, still on his feet, not yet kneeling, his near hand half-raised toward Jesus's offered hands, uncertain, not yet committed — a clear, deliberate, visible GAP remains between his fingertips and Jesus's hands; they do not touch, this gap is a hard rule that holds at every stage of this story, including the eventual confession in a later page. Thomas's linework is loose and easing — no longer sharply broken like the earlier pages, but not yet one fully confident single line either; doubt loosening, not gone. Jesus has a faint incomplete calligraphic halo of muted gold-and-blue curls around his head, never a solid disc. The blue ink motif: a few soft threads beginning to curl in the air between the two figures, still well short of either hand, touching neither — the life reaching further than it has before, still not arriving. Small handwritten production notes: a caption beneath the main scene, handwrite: "reach hither thy hand", and a corner note, handwrite: "NOTE: line loosening". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus — this includes not adding any shot-type or camera-framing label anywhere on the page itself (for example, never write words like "CLOSE TWO-SHOT", "WIDE SHOT", "MEDIUM SHOT", or any other scene-description text as if it were part of the artwork), and not extending, completing, or adding to any caption beyond the exact words quoted above. Period: 1st-century Roman Judea, Jerusalem — an upper room in a modest stone house. Plain plastered stone walls, a shuttered wood-lattice window with no glass, a heavy wooden door on a simple wood or iron bar, worn stone or packed-earth floor, a small clay oil lamp with a pinched wick and no visible chimney or glass. Simple ankle-length tunics in undyed cream or muted natural-dye colors, a looser mantle draped over one shoulder, a woven or roped belt, plain leather sandals — no visible buttons, zippers, buckles, or metal fasteners of any kind beyond simple cloth ties. No eyeglasses, no wristwatches, no modern haircut shapes, no bright synthetic-looking dye colors. No electric light anywhere — only the oil lamp's glow and daylight through the shutter. Architecture stays plain: no carved relief work, no stained glass, no arches beyond a simple doorway.
PROMPT ENDS
```

Full checklist:

Must not fail:
- **CRITICAL** — rendered in real ink-and-watercolor with visible color washes matching every
  other page — NOT a graphite pencil sketch, NOT monochrome, NOT uncolored line art. This exact
  defect (a full pencil-sketch page) has happened on a real render of this shot.
- A clear, visible gap of air between Thomas's fingertips and Jesus's offered hands — they do not touch.
- Thomas is NOT kneeling here — still on his feet, uncertain, not yet fully resolved.
- Thomas's linework is loose and easing — no longer as sharply broken as STILL_02–04, but not yet one fully confident single line.
- Jesus's two open palms each show one small faint dry ink mark only — no blood, no red, no torn flesh, both palms fully in frame.
- Halo on Jesus only. Top-left reads "SEQ: THOMAS", top-right reads "F04", corner note reads "NOTE: line loosening". Exactly three panels labeled "the wounds", "reach hither", "be not faithless". Main caption reads "reach hither thy hand". No other letters, numbers, or words anywhere — no invented shot-type labels, no extended captions.
- Thomas matches REF_THOMAS; Jesus matches REF_JESUS.

Also check:
- Thomas wears and carries no blue and no gold anywhere.
- The blue threads between the two figures stay well short of both hands, touching neither.
- No extra limbs, no malformed hands, no duplicate, blurred, or transparent figure.
- Era: no buttons, zippers, buckles, eyeglasses, wristwatches, modern haircuts, or electric light.

All lines pass → log this image as STILL_05. Go to Step S6.
An ordinary line fails → regenerate once: same prompt, same two Ingredients, nothing changed; still
failing, keep the better attempt, log it as STILL_05, write it under Flags, go to Step S6. A
CRITICAL line fails → regenerate up to twice more (three attempts total); still failing, keep the
best attempt, log it as STILL_05, write it under **CRITICAL — review before assembly** at the top
of Flags, go to Step S6. Do not stop. Do not ask. Do not edit the prompt. Do not regenerate
REF_THOMAS or REF_JESUS.

**Assembly note (not a Flow instruction):** CLIP_05 is the one shot in this whole episode that
still needs a genuine ~3-4s freeze-hold extension in final assembly, per `ASSEMBLY_PLAN.md` — its
real narration coverage runs longer than one native clip length.

---

## Step S6 [STILL_06] — F05 "My Lord and my God" close-up

- **ACTION:** `generate_image` | **Inputs:** REF: `REF_THOMAS` + REF: `REF_JESUS`
- **Continuity anchor:** same room, tighter framing than every prior page — the confession earns
  the close-up.
- **SUCCESS:** Both caption lines "My Lord and" / "my God" visible and legible? Yes. Clear gap
  between the two hands, not touching? Yes. Thomas's line fully steady and resolved, no break
  anywhere? Yes. Thomas kneeling, filling the lower-right; Jesus a partial presence at the frame
  edge, not competing for center? Yes.

```
PROMPT STARTS
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain, laid out like a real found piece of production art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F05". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "he answered") a small sketch of Thomas's open hand, no longer raised in refusal, now simply open and relaxed at his side; panel 2 (handwrite: "and said unto him") a small sketch of the same gap of air from the previous page, now with the faintest single thread of blue reaching into it, still not touching; panel 3 (handwrite: "not faithless") a small sketch of morning light broadening across the floor. Below them, ONE large full-scene illustration filling the lower half of the page — framed tighter than the previous page — this is the close-up the confession earns: Thomas, now kneeling, risen upright on his knees, face lifted fully to Jesus, filling the lower-right of the frame; Jesus's presence at the frame's left edge, his open offered hand still visible at the frame's edge with its single faint nail-mark, not his whole figure — the camera has moved in close on Thomas's face and posture, not on Jesus. Thomas's one hand still half-lifted toward the edge of frame where Jesus's hand is, stopped just short of touching — a clear, deliberate, visible GAP remains, closer than ever but still not touching; this gap is a hard rule and holds even at this climax. Thomas's contour is now one single, unbroken, confidently struck line — fully resolved, no broken or tremored line remains anywhere on him — his face lifted in open, unguarded worship, eyes wide, jaw loose, nothing held back. A few soft threads of blue ink, with the faintest gold trace, curl in the narrow gap between his reaching hand and the edge of frame where Jesus's hand is, closer than any prior page, still not touching either. Small handwritten production notes: a caption beneath the main scene, handwritten on exactly two stacked lines, both lines fully present and fully legible — the first line reads "My Lord and", the second line directly beneath it reads "my God", and no other words, sentences, or instructions of any kind appear near this caption or anywhere else on the page. Below the caption, a corner note, handwrite: "NOTE: line steady". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus — this includes not adding any shot-type or camera-framing label anywhere on the page itself (for example, never write words like "CLOSE TWO-SHOT", "ONE:", "ONLY", or any other scene-description or editorial label as if it were part of the artwork — the framing description in this prompt is an instruction to you, not text to render), and not extending, completing, or adding to any caption beyond the exact words quoted above. Period: 1st-century Roman Judea, Jerusalem — an upper room in a modest stone house. Plain plastered stone walls, a shuttered wood-lattice window with no glass, a heavy wooden door on a simple wood or iron bar, worn stone or packed-earth floor, a small clay oil lamp with a pinched wick and no visible chimney or glass. Simple ankle-length tunics in undyed cream or muted natural-dye colors, a looser mantle draped over one shoulder, a woven or roped belt, plain leather sandals — no visible buttons, zippers, buckles, or metal fasteners of any kind beyond simple cloth ties. No eyeglasses, no wristwatches, no modern haircut shapes, no bright synthetic-looking dye colors. No electric light anywhere — only the oil lamp's glow and daylight through the shutter. Architecture stays plain: no carved relief work, no stained glass, no arches beyond a simple doorway.
PROMPT ENDS
```

Full checklist:

Must not fail:
- **CRITICAL** — the caption beneath the main scene has TWO stacked lines: "My Lord and" on the first line and "my God" directly beneath it, both actually visible and legible. A page showing only "My Lord and" fails — this exact defect has happened on this page before.
- **CRITICAL** — no invented text of any kind appears on the page beyond the exact handwrite strings quoted — specifically, do not render editorial/framing words like "ONLY" or "ONE: CLOSE TWO-SHOT" anywhere on the page. This exact defect has happened on a real render of this shot.
- A clear, visible gap of air between Thomas's half-lifted hand and Jesus's hand at the left frame edge. They do not touch. This is the tightest framing in the episode and the one rule that must never fail silently.
- Thomas's outline is ONE single unbroken confident line everywhere on him — no broken, doubled, or tremored line anywhere.
- Top-left reads "SEQ: THOMAS", top-right reads "F05", corner note reads "NOTE: line steady". Exactly three small panels across the top, each labeled only with a circled 1, 2, 3, their handwritten labels reading "he answered", "and said unto him", "not faithless". No other letters, numbers, or words anywhere on the page.
- Thomas is kneeling, upright on his knees, face lifted, filling the lower-right. Jesus reads as a presence at the left edge with his open hand visible — not his whole figure, not competing for the center. This is Thomas's shot.
- Jesus's visible palm shows one small faint dry ink mark only — no blood, no red, no torn flesh.
- Thomas matches REF_THOMAS: squarish weathered face, heavy dark brows, short thick dark beard flecked with grey, clay-red robe over cream tunic. Jesus's visible hand and robe edge match REF_JESUS: deep indigo and charcoal robe.

Also check:
- Thomas wears and carries no blue and no gold anywhere.
- The blue-and-gold threads in the gap are wet-ink lines, not glow, sparkle, or particles, and touch neither hand.
- Halo on no one in this frame but Jesus (if his head is visible); never on Thomas.
- Ink-and-watercolor on grained cream paper — not photoreal, anime, 3D, or glossy. No speech bubble, thought bubble, text box, or banner around any note.
- No extra limbs, malformed hands, or duplicate/blurred/transparent figure.
- Era: no buttons, zippers, buckles, eyeglasses, wristwatches, modern haircuts, or electric light.

All lines pass → log this image as STILL_06. Go to Step S7.
An ordinary line fails → regenerate once: same prompt, same two Ingredients, nothing changed; still
failing, keep the better attempt, log it as STILL_06, write it under Flags, go to Step S7. A
CRITICAL line fails → regenerate up to twice more (three attempts total); still failing, keep the
best attempt, log it as STILL_06, write it under **CRITICAL — review before assembly** at the top
of Flags, go to Step S7. Do not stop. Do not ask. Do not edit the prompt. Do not regenerate
REF_THOMAS or REF_JESUS.

---

## Step S7 [STILL_07] — F06 "Answered You Too"

- **ACTION:** `generate_image` | **Inputs:** REF: `REF_THOMAS` + REF: `REF_JESUS`
- **Continuity anchor:** same room, pulled back wider than S6 — the whole group gathered and settled.
- **SUCCESS:** Thomas's line fully resolved and steady, matching S6? Yes. Halo only on Jesus? Yes.
  Group reads gathered and settled, not staged in a line? Yes. SEQ/F06 header + 3 panels + caption
  exact, nothing extra? Yes.

```
PROMPT STARTS
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain, laid out like a real found piece of production art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F06". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "his own hands") a small close study of Jesus's two open hands, held together at rest, their faint nail-marks visible, no longer reaching, simply resting; panel 2 (handwrite: "the room at peace") a small loose sketch of the gathered disciples, calm, close together; panel 3 (handwrite: "the road ahead") a small sketch of an open doorway with a bright, plain, empty stretch of daylight beyond it, nothing else in the frame. Below them, ONE large full-scene illustration filling the lower half of the page — a WIDE shot, pulled back further than the previous page: the same room, full morning light, all the disciples now gathered loosely around Jesus and Thomas together in one settled group, no one apart from the others anymore. Thomas is still on his knees in the middle of the group, his face calm now, contour one single steady confident line, fully resolved, matching every other figure on the page — no broken or tremored line remains anywhere on him. Jesus stands at the center, his face turned slightly outward from the group, calm and open, his faint incomplete calligraphic halo of muted gold-and-blue curls around his head, never a solid disc. Soft threads of blue ink, with muted gold traces, now drift more freely through the open air of the room, above the whole gathered group rather than confined to one small area — quiet and restrained still, behaving like wet ink bled into the paper's morning light, never a magic-particle glow. Small handwritten production notes: a caption beneath the main scene, handwrite: "he answered him", and a corner note, handwrite: "NOTE: line steady, room at rest". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus — this includes not adding any shot-type or camera-framing label anywhere on the page itself (for example, never write words like "WIDE SHOT" or any other scene-description text as if it were part of the artwork), and not extending, completing, or adding to any caption beyond the exact words quoted above. Period: 1st-century Roman Judea, Jerusalem — an upper room in a modest stone house. Plain plastered stone walls, a shuttered wood-lattice window with no glass, a heavy wooden door on a simple wood or iron bar, worn stone or packed-earth floor, a small clay oil lamp with a pinched wick and no visible chimney or glass. Simple ankle-length tunics in undyed cream or muted natural-dye colors, a looser mantle draped over one shoulder, a woven or roped belt, plain leather sandals — no visible buttons, zippers, buckles, or metal fasteners of any kind beyond simple cloth ties. No eyeglasses, no wristwatches, no modern haircut shapes, no bright synthetic-looking dye colors. No electric light anywhere — only the oil lamp's glow and daylight through the shutter. Architecture stays plain: no carved relief work, no stained glass, no arches beyond a simple doorway.
PROMPT ENDS
```

Full checklist:

Must not fail:
- Thomas's Fray is fully resolved, matching STILL_06 — one single steady confident line, unchanged, no broken or tremored line anywhere on him.
- Halo on Jesus only, never on Thomas or anyone else.
- The disciples read as a single gathered, settled group around Jesus and Thomas — not posed in a line, not staged.
- Top-left reads "SEQ: THOMAS", top-right reads "F06", corner note reads "NOTE: line steady, room at rest". Exactly three panels labeled "his own hands", "the room at peace", "the road ahead". Main caption reads "he answered him". No other letters, numbers, or words anywhere — no invented shot-type labels, no extended captions.
- Thomas matches REF_THOMAS; Jesus matches REF_JESUS.

Also check:
- Thomas wears and carries no blue and no gold anywhere.
- The blue-and-gold threads drift freely above the group, quiet and restrained, wet-ink in character, never glow or sparkle.
- Ink-and-watercolor on grained cream paper — not photoreal, anime, 3D, or glossy.
- No extra limbs, malformed hands, or duplicate/blurred/transparent figure.
- Era: no buttons, zippers, buckles, eyeglasses, wristwatches, modern haircuts, or electric light.

All lines pass → log this image as STILL_07. Go to Step S8.
An ordinary line fails → regenerate once: same prompt, same two Ingredients, nothing changed; still
failing, keep the better attempt, log it as STILL_07, write it under Flags, go to Step S8. A
CRITICAL line fails → regenerate up to twice more (three attempts total); still failing, keep the
best attempt, log it as STILL_07, write it under **CRITICAL — review before assembly** at the top
of Flags, go to Step S8. Do not stop. Do not ask. Do not edit the prompt. Do not regenerate
REF_THOMAS or REF_JESUS.

---

## Step S8 [STILL_08] — Back Cover

- **ACTION:** `generate_image` | **Inputs:** none — no named character appears in this shot
- **Continuity anchor:** same woodcut rendering technique as Step S1 (Front Cover) — the two covers
  share one style, bookending the interior storyboard pages.
- **SUCCESS:** Same woodcut engraving style, warm+cool contrast? Yes. Jesus absent, no halo
  anywhere? Yes. Title exactly "BLESSED ARE THEY THAT HAVE NOT SEEN" once + "JOHN 20:29"? Yes.
  Art runs edge to edge, no margin band? Yes. Crowd anonymous, no figure singled out? Yes.

```
PROMPT STARTS
16th-century Albrecht Dürer woodcut linework blended with contemporary cinematic landscape photography — dense parallel hatching, hard black contours, ink-on-block texture, dramatic volumetric light rays, photographic tonality. This is the exact same rendering technique as this episode's Front Cover shot — the same dense woodcut hatching, the same carved wood-block lettering, the same cinematic-landscape treatment. Stationary camera, wide static shot, ultra-crisp. Vertical 9:16 frame. No storyboard panel grid, no "SEQ:"/frame-number labels — this is cover art, not a story page. An open road climbing over a low, wind-scoured hillside at morning, seen from a clear middle distance, held small in the lower third of the frame against a sweeping open sky with carved structural cloud forms. Many ordinary figures, varied in age, dress, and stature, walk or stand on the road in loose small clusters, faces lifted toward the sky ahead, none looking back — ordinary anonymous people, none of them the disciples or Thomas from earlier in the story. No named figure, no halo, no glowing presence — Jesus does NOT appear anywhere in this frame. Warm morning gold light spills across the road and the near hillside from the upper right; cold blue-grey shadow still pools in the low ground and valley folds beyond the road, not yet reached by the light. Very faint traces of the blue-and-gold motif drift high in the open sky above the road — small, restrained, distant, more suggestion than presence, touching no figure. Near the bottom of the frame, bold engraved wood-block title lettering, carved in the same dense woodcut style as the rest of the image — thick confident carved strokes, NOT a modern font, not a decorative flourish font, no drop shadow, no glow, no banner or box behind it, sitting naturally within the composition, reading: "BLESSED ARE THEY THAT HAVE NOT SEEN" — write this exact phrase once, do not repeat any word in it. Smaller matching carved lettering beneath it reading: "JOHN 20:29". No other text, letters, numbers, or words appear anywhere on the image beyond these two lines. The artwork fills the entire image edge to edge — never a drawn border, picture frame, caption strip, or margin band around the scene; at the top edge of the frame (opposite the title), the scene's own artwork runs all the way to the canvas edge, fully painted, no blank paper showing. Period costume, the road's ordinary figures: simple ankle-length tunics in undyed cream or muted natural-dye colors, plain mantles, woven or roped belts, plain leather sandals — no visible buttons, zippers, buckles, or metal fasteners of any kind beyond simple cloth ties, no eyeglasses, no wristwatches, no modern haircut shapes. Avoid: modern clothing, busy foreground, bright neon colors, deformed anatomy, blurry rendering, smooth photorealism without linework.
PROMPT ENDS
```

Full checklist:

Must not fail:
- Title reads exactly "BLESSED ARE THEY THAT HAVE NOT SEEN", written once, no repeated word. Subtitle reads exactly "JOHN 20:29". No other text anywhere on the image.
- At least one genuinely warm note (the morning gold light) AND at least one genuinely cool note (the blue-grey valley shadow) both clearly present in the same image — not one flat temperature.
- The artwork runs fully to the edge of the frame on all sides — no blank paper margin band anywhere, especially the edge opposite the title (the top).
- No storyboard panel grid, no "SEQ:" or frame-number label anywhere.
- Jesus does NOT appear anywhere in this frame. No halo, no glowing presence anywhere.
- No single figure among the road's crowd is named, singled out, or more prominent than the rest — an anonymous multitude.

Also check:
- Dense woodcut hatching and hard black contours, cinematic dramatic light — not the soft ink-wash storyboard-page look, and matching the same technique as Step S1's Front Cover.
- The blue-and-gold sky traces stay small, restrained, and distant — touching no figure.
- No modern clothing, no modern objects, no deformed anatomy, no blurry rendering.

All lines pass → log this image as STILL_08. Phase 2 is complete — go to Phase 3, Step V1.
An ordinary line fails → regenerate once: same prompt, nothing changed; still failing, keep the
better attempt, log it as STILL_08, write it under Flags, go to Phase 3. Do not stop. Do not ask.
Do not edit the prompt.

---
---

# PHASE 3: ANIMATION (I2V)

Generate all 8 clips in this phase, each animated from its matching still already generated and
logged in Phase 2. Do not generate a new still here — attach the exact logged still as the starting
frame for each clip below.

## Step V1 [CLIP_01] — animates STILL_01 (Front Cover)

- **ACTION:** `generate_video_with_first_frame` | **Inputs:** START: `STILL_01` | **Duration:**
  default length (see Global Settings table)
- **SUCCESS:** Lamplight visibly flickers, first frame to last? Yes. Door stays completely still,
  zero movement? Yes. Title text unchanged first-to-last? Yes. Nobody speaks, no lips move? Yes.

```
PROMPT STARTS
The thin bar of lamplight beside the door flickers continuously and visibly for the entire clip — small warm pulses of brightness rising and falling, never settling into a flat glow. This flicker is the clip's main visible motion, present from the very first frame to the very last. Thomas's raised hand, glimpsed in that light, presses further outward across roughly the first half of the clip, then holds firm for the remainder. Camera: stationary, locked wide shot, no pan, no zoom. The baked title lettering at the top stays pixel-for-pixel identical throughout — same opacity, no fade, no drift, no duplication. The door, stone, street, and sky stay as drawn. No new figure, mark, or text appears at any point.
Audio: faint lamp flicker, distant muffled street/night ambience from outside the door. Ambient sound only — no dialogue, no character speech of any kind, no narrator voice, no music. Lips stay closed and do not move on every figure in this clip; nobody speaks on camera — all spoken lines are added afterward as separate narration audio.
PROMPT ENDS
```

Full checklist:

Must not fail:
- Motion exists: the lamplight in the door gap is visibly flickering, first frame to last — brightness pulses up and down, never a flat unchanging glow.
- **CRITICAL** — the door does not open, swing, crack, shift, or change at any point, first frame to last. No hand reaches through it beyond the wrist already established in the still. No light spills through it beyond the one thin bar already drawn. This exact defect has happened on a real render of this shot — any door movement triggers the CRITICAL retry rule in Section 3, never a silent pass.
- The baked title text does not visibly change, fade, drift, or duplicate between the first frame and the last frame.
- Nobody's lips move. No speech, no words, no narrator, no music on the audio track — ambient only.

Also check:
- The street, stone, and sky stay exactly as drawn throughout.
- Camera does not pan, zoom, orbit, dolly, or shake.
- Note the clip's actual length for the FINAL REPORT.

All lines pass → log this video as CLIP_01. Go to Step V2.
An ordinary line fails → regenerate once: same prompt, same starting frame STILL_01, nothing
changed; still failing, keep the better attempt, log it as CLIP_01, write it under Flags, go to
Step V2. The CRITICAL door-movement line fails → regenerate up to twice more (three attempts
total); still failing, keep the best attempt, log it as CLIP_01, write it under **CRITICAL —
review before assembly** at the top of Flags, go to Step V2. Do not stop. Do not ask. Do not edit
the prompt. Do not regenerate STILL_01 to fix a clip.

---

## Step V2 [CLIP_02] — animates STILL_02 (F01)

- **ACTION:** `generate_video_with_first_frame` | **Inputs:** START: `STILL_02` | **Duration:**
  **LONG — longest available**
- **SUCCESS:** Disciple's hands and the lamp flame visibly move, motion still visible near the end?
  Yes. Blue thread's gap stays fixed, never touches? Yes. Thomas's shaky line unchanged throughout?
  Yes. Nobody speaks? Yes.

```
PROMPT STARTS
The foremost disciple leans in toward Thomas continuously across the first third of the clip, his open hands visibly rising further in appeal — real, clearly readable movement, not a subtle shift — then holds his new position for the remainder. The lamp flame in panel 3 sways continuously and visibly the entire clip, never going still. Thomas's raised palm presses further outward across that same first third, a real visible push, then holds firm. His chest visibly rises and falls once with a slow, tense breath partway through the hold. The other two disciples stir gently throughout, small continuous shifts of weight. Camera: locked static. All lips stay closed, nobody speaks. The blue thread's tip stays fixed in its gap short of Thomas's hand — it does not move, that gap is the one thing that must never change. Thomas's shaky, tremored linework keeps its exact drawn character throughout.
Audio: faint room tone, soft rustle of robes as the disciples lean in, barest floorboard creak. Ambient sound only — no dialogue, no character speech of any kind, no narrator voice, no music. Lips stay closed and do not move on every figure in this clip; nobody speaks on camera — all spoken lines are added afterward as separate narration audio.
PROMPT ENDS
```

Full checklist:

Must not fail:
- Motion exists: the foremost disciple's hands and the lamp flame are both visibly different between the first frame and the last frame. A clip whose first and last frames are effectively identical fails.
- Motion lasts: the lamp flame is still visibly swaying in the final third of the clip — the clip does not go dead in its back half.
- The blue thread's tip stays in the exact same fixed gap, first frame to last — it never moves closer, never touches Thomas.
- Nobody's lips move. No speech, no words, no narrator, no music — ambient only.
- Thomas's shaky, tremored line keeps its exact drawn character, first frame to last — it does not smooth out or steady.

Also check:
- Camera does not pan, zoom, orbit, dolly, or shake.
- No new figure, mark, or text appears at any point.
- Note the clip's actual length for the FINAL REPORT.

All lines pass → log this video as CLIP_02. Go to Step V3.
An ordinary line fails → regenerate once: same prompt, same starting frame STILL_02, nothing
changed; still failing, keep the better attempt, log it as CLIP_02, write it under Flags, go to
Step V3. Do not stop. Do not ask. Do not edit the prompt. Do not regenerate STILL_02 to fix a clip.

---

## Step V3 [CLIP_03] — animates STILL_03 (F02)

- **ACTION:** `generate_video_with_first_frame` | **Inputs:** START: `STILL_03` | **Duration:**
  default length
- **SUCCESS:** Lamp flame's flicker visibly different first-to-last? Yes. Thomas stays in the room
  throughout? Yes. His shaky line unchanged? Yes. Nobody speaks? Yes.

```
PROMPT STARTS
The lamp flame in panel 2 burns low and continuously flickers, visibly smaller and dimmer than an ordinary flame, for the entire clip — the clip's main visible motion, marking time passing. Thomas's chest rises and falls once with a slow, quiet breath, midway through the clip — a small, real, readable motion, not a static pose. The seated disciples in the middle distance shift very slightly, a small settling motion, once. Camera: locked static. Thomas's lips stay closed, not speaking; the seated disciples' lips stay closed too. Thomas's shaky, tremored linework keeps its exact drawn character throughout — unchanged, since his doubt has not moved. No line anywhere redraws, no new figure, mark, or text appears at any point.
Audio: very quiet room tone, the faint low crackle of the dimming lamp, near-silence otherwise. Ambient sound only — no dialogue, no character speech of any kind, no narrator voice, no music. Lips stay closed and do not move on every figure in this clip; nobody speaks on camera — all spoken lines are added afterward as separate narration audio.
PROMPT ENDS
```

Full checklist:

Must not fail:
- Motion exists: the lamp flame's flicker is visibly different between the first frame and the last frame.
- Thomas has not left the room at any point — still fully present, first frame to last.
- Thomas's shaky, tremored line keeps its exact drawn character throughout — unchanged.
- Nobody's lips move. No speech, no words, no narrator, no music — ambient only.

Also check:
- Camera does not pan, zoom, orbit, dolly, or shake.
- No new figure, mark, or text appears at any point.
- Note the clip's actual length for the FINAL REPORT.

All lines pass → log this video as CLIP_03. Go to Step V4.
An ordinary line fails → regenerate once: same prompt, same starting frame STILL_03, nothing
changed; still failing, keep the better attempt, log it as CLIP_03, write it under Flags, go to
Step V4. Do not stop. Do not ask. Do not edit the prompt. Do not regenerate STILL_03 to fix a clip.

---

## Step V4 [CLIP_04] — animates STILL_04 (F03)

- **ACTION:** `generate_video_with_first_frame` | **Inputs:** START: `STILL_04` | **Duration:**
  default length
- **SUCCESS:** Jesus's hand visibly lowers, disciples visibly react? Yes. Door stays completely
  still, zero movement? Yes. Thomas's shaky line unchanged? Yes. Nobody speaks? Yes.

```
PROMPT STARTS
Jesus's raised hand settles slowly downward across roughly the first third of the clip — a real, visible, deliberate lowering motion, not a static pose — then holds at rest for the remainder. The disciples visibly react across that same opening stretch: shoulders easing, a couple of heads turning toward Jesus, real readable motion, then settling into stillness. Morning light shifts visibly across the door and the raised-open-palm study in panels 1 and 2 throughout the clip. Camera: locked static. Jesus's lips stay closed and completely still — not speaking. Thomas's shaky, tremored linework keeps its exact drawn character, unchanged from before — it does not begin resolving in this clip. No line anywhere redraws, no new figure, mark, or door opening appears.
Audio: soft morning room tone, a collective intake of breath from the group, faint rustle of robes. Ambient sound only — no dialogue, no character speech of any kind, no narrator voice, no music. Lips stay closed and do not move on every figure in this clip; nobody speaks on camera — all spoken lines are added afterward as separate narration audio.
PROMPT ENDS
```

Full checklist:

Must not fail:
- Motion exists: Jesus's hand is visibly lower in the last frame than the first, and the disciples' postures are visibly different first-to-last.
- **CRITICAL** — the door does not open, swing, crack, shift, or change at any point, first frame to last. This exact defect has happened on a real render of a different shot in this episode — any door movement triggers the CRITICAL retry rule in Section 3, never a silent pass.
- Thomas's shaky, tremored line keeps its exact drawn character throughout — it does not begin steadying in this clip.
- Nobody's lips move. No speech, no words, no narrator, no music — ambient only.

Also check:
- Camera does not pan, zoom, orbit, dolly, or shake.
- No new figure, mark, or text appears at any point.
- Note the clip's actual length for the FINAL REPORT.

All lines pass → log this video as CLIP_04. Go to Step V5.
An ordinary line fails → regenerate once: same prompt, same starting frame STILL_04, nothing
changed; still failing, keep the better attempt, log it as CLIP_04, write it under Flags, go to
Step V5. The CRITICAL door-movement line fails → regenerate up to twice more (three attempts
total); still failing, keep the best attempt, log it as CLIP_04, write it under **CRITICAL —
review before assembly** at the top of Flags, go to Step V5. Do not stop. Do not ask. Do not edit
the prompt. Do not regenerate STILL_04 to fix a clip.

---

## Step V5 [CLIP_05] — animates STILL_05 (F04)

- **ACTION:** `generate_video_with_first_frame` | **Inputs:** START: `STILL_05` | **Duration:**
  **LONG — longest available**
- **SUCCESS:** Thomas's hand visibly moves closer but never touches, even in the last frame? Yes.
  Threads still visibly moving near the end? Yes. Thomas stays standing, never kneels? Yes. Nobody
  speaks? Yes.

```
PROMPT STARTS
Thomas's half-raised hand trembles visibly and inches closer within its own drawn range across the whole clip — a real, continuous, readable tremor and slow approach, not a static pose — before settling, still short of the gap, in the final moment. His breathing visibly changes partway through — shoulders lowering out of refusal but not yet at rest, a clear physical shift. The soft blue threads between the two figures drift continuously and visibly the entire clip, curling and shifting in the air, never locking into a static shape. Camera: locked static. Jesus's offered hands stay steady and open throughout, unmoving, the invitation held out; his lips stay closed, not speaking. Thomas's lips stay closed too. The gap between Thomas's fingertips and Jesus's hand may narrow as his hand inches closer, but never fully closes and never touches — a visible sliver of air always remains, at every point in the clip including the very last frame. Thomas's linework keeps its own drawn character; it does not resolve further in this clip. No new mark appears.
Audio: soft morning room tone, a held, uncertain quiet, faint rustle of cloth. Ambient sound only — no dialogue, no character speech of any kind, no narrator voice, no music. Lips stay closed and do not move on every figure in this clip; nobody speaks on camera — all spoken lines are added afterward as separate narration audio.
PROMPT ENDS
```

Full checklist:

Must not fail:
- Motion exists: Thomas's hand is visibly closer (though still short of touching) in the last frame than the first, and the blue threads' shapes differ first-to-last.
- Motion lasts: the threads are still visibly moving in the final third of the clip.
- **CRITICAL** — the hand-gap never fully closes and the two hands never touch, at any point in the clip including the very last frame. A visible sliver of air always remains.
- Nobody's lips move. No speech, no words, no narrator, no music — ambient only.
- Thomas is NOT kneeling anywhere in this clip.

Also check:
- Jesus's offered hands stay steady, unmoving.
- Camera does not pan, zoom, orbit, dolly, or shake.
- Note the clip's actual length for the FINAL REPORT.

All lines pass → log this video as CLIP_05. Go to Step V6.
An ordinary line fails → regenerate once: same prompt, same starting frame STILL_05, nothing
changed; still failing, keep the better attempt, log it as CLIP_05, write it under Flags, go to
Step V6. The CRITICAL hand-gap line fails → regenerate up to twice more (three attempts total);
still failing, keep the best attempt, log it as CLIP_05, write it under **CRITICAL — review before
assembly** at the top of Flags, go to Step V6. Do not stop. Do not ask. Do not edit the prompt. Do
not regenerate STILL_05 to fix a clip.

---

## Step V6 [CLIP_06] — animates STILL_06 (F05)

- **ACTION:** `generate_video_with_first_frame` | **Inputs:** START: `STILL_06` | **Duration:**
  default length
- **SUCCESS:** Thomas's shoulders/chest visibly settle, threads still visibly moving near the end?
  Yes. Both caption lines unchanged first-to-last? Yes. Hand-gap never closes? Yes. Nobody speaks?
  Yes.

```
PROMPT STARTS
One slow, visible breath loosens Thomas's shoulders fully across the length of the clip — a real, continuous, readable release of tension, shoulders and chest visibly settling from tight to open. His lifted face holds in open worship throughout, eyes wide and warm. The soft blue threads in the gap between his hand and Jesus's drift continuously and visibly, curling gently, never frozen into one shape. Camera: locked, close framing held throughout — no push, no zoom, the closeness is baked into the still. Thomas's lips stay closed and completely still — not speaking; the baked caption "My Lord and / my God" carries the words, not his mouth. His half-lifted hand stays exactly where drawn, in its own fixed gap, the whole clip — it never closes the gap, never touches. Jesus's visible hand at the frame's edge stays steady. Thomas's steady linework stays exactly as drawn, stroke for stroke.
Audio: a single soft settling breath, the faintest rustle as Thomas's weight shifts on his knees, otherwise near-silence. Ambient sound only — no dialogue, no character speech of any kind, no narrator voice, no music. Lips stay closed and do not move on every figure in this clip; nobody speaks on camera — all spoken lines are added afterward as separate narration audio.
PROMPT ENDS
```

Full checklist:

Must not fail:
- Motion exists: Thomas's shoulders and chest are visibly different between the first frame and the last frame — settled and opened, not the same pose. The blue threads' shapes differ between first and last frames. A clip whose first and last frames are effectively identical fails.
- Motion lasts: the threads are still visibly moving in the final third of the clip. The clip does not go dead in its back half.
- The hand-gap is identical first frame to last: Thomas's hand never moves toward Jesus's, never touches.
- **CRITICAL** — both caption lines "My Lord and" / "my God" are present and unchanged in the first frame AND the last frame. All page text is unchanged throughout. This exact defect (the second line dropping) has happened on this page before.
- Thomas's lips never move. No speech, no words, no narrator, no music on the audio track — ambient breath and rustle only.

Also check:
- Jesus's hand stays steady. No new figure, mark, hand, or text appears at any point.
- Thomas's single steady line stays as drawn — it does not flicker into a broken or doubled line.
- Camera does not push, zoom, pan, orbit, dolly, or shake.
- Note the clip's actual length for the FINAL REPORT.

All lines pass → log this video as CLIP_06. Go to Step V7.
An ordinary line fails → regenerate once: same prompt, same starting frame STILL_06, nothing
changed; still failing, keep the better attempt, log it as CLIP_06, write it under Flags, go to
Step V7. The CRITICAL caption line fails → regenerate up to twice more (three attempts total);
still failing, keep the best attempt, log it as CLIP_06, write it under **CRITICAL — review before
assembly** at the top of Flags, go to Step V7. Do not stop. Do not ask. Do not edit the prompt. Do
not regenerate STILL_06 to fix a clip.

---

## Step V7 [CLIP_07] — animates STILL_07 (F06)

- **ACTION:** `generate_video_with_first_frame` | **Inputs:** START: `STILL_07` | **Duration:**
  default length
- **SUCCESS:** Blue threads and Jesus's halo curls visibly move? Yes. Thomas's resolved line
  unchanged? Yes. Nobody speaks? Yes.

```
PROMPT STARTS
The soft blue threads above the gathered group drift continuously and visibly, curling slowly through the room's morning light, for the entire clip — the clip's main visible motion. Jesus's halo curls rotate slowly and continuously around his head. The gathered disciples shift very slightly, small settled movements of a group at rest, once early in the clip, then hold. Camera: locked static. All lips stay closed, nobody speaks, including Jesus and Thomas. Thomas's steady, fully resolved linework stays exactly as drawn, stroke for stroke, the entire clip — it does not change further, the resolution already happened on an earlier page. No new mark, figure, or text appears at any point.
Audio: soft morning room tone, the faint settled murmur of a group at rest, near-silence otherwise. Ambient sound only — no dialogue, no character speech of any kind, no narrator voice, no music. Lips stay closed and do not move on every figure in this clip; nobody speaks on camera — all spoken lines are added afterward as separate narration audio.
PROMPT ENDS
```

Full checklist:

Must not fail:
- Motion exists: the blue threads' shapes and Jesus's halo curls are both visibly different between the first frame and the last frame.
- Thomas's Fray stays fully resolved throughout — one steady line, unchanged, first frame to last.
- Nobody's lips move. No speech, no words, no narrator, no music — ambient only.

Also check:
- The gathered group's small settling motion happens once early, then holds — no repeated or looping shift.
- Camera does not pan, zoom, orbit, dolly, or shake.
- Note the clip's actual length for the FINAL REPORT.

All lines pass → log this video as CLIP_07. Go to Step V8.
An ordinary line fails → regenerate once: same prompt, same starting frame STILL_07, nothing
changed; still failing, keep the better attempt, log it as CLIP_07, write it under Flags, go to
Step V8. Do not stop. Do not ask. Do not edit the prompt. Do not regenerate STILL_07 to fix a clip.

---

## Step V8 [CLIP_08] — animates STILL_08 (Back Cover)

- **ACTION:** `generate_video_with_first_frame` | **Inputs:** START: `STILL_08` | **Duration:**
  **LONG — longest available**
- **SUCCESS:** Figures visibly walk forward, motion still visible near the end? Yes. Same number of
  figures throughout? Yes. Title text unchanged? Yes. Nobody speaks or faces camera? Yes.

```
PROMPT STARTS
The figures on the road walk continuously and visibly onward at an unhurried pace for the entire clip — real, readable footfalls and forward progress, not a subtle drift — exactly as many figures as drawn, none appearing or disappearing. The faint blue-and-gold sky traces drift continuously and visibly, curling slowly, staying small and distant but clearly in motion throughout, never locking into one static shape. Camera: stationary, locked wide shot, no pan, no zoom. The baked closing lettering at the bottom stays perfectly static the whole clip. None of the figures turn to face camera, gesture, or speak. Morning light and the cold valley shadow stay as drawn. No new figure, mark, or text appears.
Audio: soft open-air morning ambience — light wind, distant birdsong, faint footsteps on the road. Ambient sound only — no dialogue, no character speech of any kind, no narrator voice, no music. Lips stay closed and do not move on every figure in this clip; nobody speaks on camera — all spoken lines are added afterward as separate narration audio.
PROMPT ENDS
```

**Do NOT use a boomerang/reverse loop to extend this clip if Flow offers that option.** The figures
are continuously walking with no completing gesture, and a reversed mid-stride walk reads as broken
(a real, already-learned lesson in this project). If the clip needs to be longer, that is handled
outside Flow, in final assembly — generate this clip once, straightforwardly, and log it.

Full checklist:

Must not fail:
- Motion exists: the walking figures are visibly further along the road in the last frame than the first. The sky traces' shapes differ first-to-last.
- Motion lasts: the figures are still visibly walking in the final third of the clip.
- Exactly as many figures as the still shows — none appear or disappear during the clip.
- Nobody's lips move, nobody turns to face camera, nobody gestures. No speech, no words, no narrator, no music — ambient only.
- The baked title/subtitle text stays unchanged first frame to last.

Also check:
- Camera does not pan, zoom, orbit, dolly, or shake.
- No new figure, mark, or text appears at any point.
- Note the clip's actual length for the FINAL REPORT.

All lines pass → log this video as CLIP_08. Phase 3 is complete — go to Phase 4, the FINAL REPORT.
An ordinary line fails → regenerate once: same prompt, same starting frame STILL_08, nothing
changed; still failing, keep the better attempt, log it as CLIP_08, write it under Flags, go to
Phase 4. Do not stop. Do not ask. Do not edit the prompt. Do not regenerate STILL_08 to fix a clip.

---
---

# PHASE 4: FINAL REPORTING

You are finished when all 18 labels below exist and this FINAL REPORT is posted as your last
message. After posting it, generate nothing further. I will download the assets from Flow myself.

The **Ingredient/label record** below IS the running log you kept per Section 0 rule 4 — reproduce
it in full, one line per generation, in the exact order you made them. This is the real mechanism
for matching Flow's own filenames back to our labels; do not rely on a title/name field alone.

```
FINAL REPORT — My Lord and My God — 18 generations

| Label | Flow's own filename or content description | Attempts (1-3) | All checks passed? (yes/no) | Actual length (clips only) | Position in session |
|---|---|---|---|---|---|
| REF_THOMAS | | | | — | |
| REF_JESUS | | | | — | |
| STILL_01 | | | | — | |
| STILL_02 | | | | — | |
| STILL_03 | | | | — | |
| STILL_04 | | | | — | |
| STILL_05 | | | | — | |
| STILL_06 | | | | — | |
| STILL_07 | | | | — | |
| STILL_08 | | | | — | |
| CLIP_01 | | | | | |
| CLIP_02 | | | | | |
| CLIP_03 | | | | | |
| CLIP_04 | | | | | |
| CLIP_05 | | | | | |
| CLIP_06 | | | | | |
| CLIP_07 | | | | | |
| CLIP_08 | | | | | |

Totals: __ of 10 stills, __ of 8 clips. Total images generated this session (should be 10 —
flag if more, per Section 0.5 item 5): __
Not generated (list, or "none"):
CRITICAL — review before assembly (every line that failed a CRITICAL check even after 3 attempts,
by label, in the words of the check):
Flags — every other failed check line, by label, in the words of the check:
```

Suggested download filenames, matching this episode's assembly step — rename to these when you save
the zip locally (Flow itself will not produce these names):

| Label | Suggested filename |
|---|---|
| REF_THOMAS | ref_thomas.png |
| REF_JESUS | ref_jesus.png |
| STILL_01 / CLIP_01 | 01_front_cover.png / 01_front_cover.mp4 |
| STILL_02 / CLIP_02 | 02_f01_doubt.png / 02_f01_doubt.mp4 |
| STILL_03 / CLIP_03 | 03_f02_eight_days.png / 03_f02_eight_days.mp4 |
| STILL_04 / CLIP_04 | 04_f03_arrival.png / 04_f03_arrival.mp4 |
| STILL_05 / CLIP_05 | 05_f04_invitation.png / 05_f04_invitation.mp4 |
| STILL_06 / CLIP_06 | 06_f05_confession.png / 06_f05_confession.mp4 |
| STILL_07 / CLIP_07 | 07_f06_answered_you_too.png / 07_f06_answered_you_too.mp4 |
| STILL_08 / CLIP_08 | 08_back_cover.png / 08_back_cover.mp4 |

---

## After the zip comes back (not part of the Flow run — for whoever assembles this next)

1. Read the FINAL REPORT first. Anything under **CRITICAL — review before assembly** needs a human
   eyeball on that specific still/clip before it's trusted — don't feed a flagged asset straight
   into assembly unreviewed.
2. Use the Ingredient/label record to match Flow's real filenames to our labels, then rename to the
   suggested filenames above before assembly.
3. Assembly follows `ASSEMBLY_PLAN.md` in this same folder — real per-shot targets, and the note
   that CLIP_05 (F04) is the one shot still needing a genuine ~3-4s freeze-hold extension.
4. The existing `_assembly_v2/build_cut.py` in this folder was built for the OLD 6-shot delivery
   and does not yet know about the 8-shot filenames this run produces — it needs updating before it
   can build this cut, not a drop-in rerun.
5. Run `check_landing_hold.py` on the finished cut before calling the episode done — same gate
   every other episode in this project goes through (INV-26, ≥3.0s hold after the last word).

---

## What changed in v2 (for reference — not part of the Flow instructions)

A first version of this document was run through Google Flow for real (delivery in
`_flow_delivery_v6/`, full visual review in `_flow_delivery_v6/_REVIEW.html`). Two things drove
this rebuild:

1. **Structural fix, matching Flow's own unprompted advice.** The old document interleaved
   still-then-clip per shot in one long pass. Flow's own agent, in two separate messages, recommended
   splitting into phases (all refs, then all stills, then all clips) with explicit ACTION tags and a
   compact SUCCESS line per step — exactly what this v2 document now does.
2. **Four real content defects, found by looking at the actual delivered pixels, each fixed at its
   source:**
   - Front Cover (S1) rendered with the door wide open and in the wrong art style — fixed with an
     explicit same-style-as-Back-Cover anchor and much more forceful door-composition wording.
   - F04 (S5) rendered as a graphite pencil sketch — fixed with an explicit
     ink-and-watercolor-not-pencil reinforcement.
   - F01 and F02 (S2, S3) didn't show Thomas's "doubt" line as visibly different from the other
     disciples — fixed with more vivid, concrete "trembling hand" wording.
   - Invented text appeared beyond what was asked on 2 stills (F05, F03) — fixed with an explicit
     negative example added to every interior still's "no other text" rule.

Also fixed: Flow's own filenames don't preserve our label scheme at all (confirmed on a real run,
where the actual generated Jesus reference was named after a different file entirely) — the "use
Flow's title field" instruction is replaced with a running plain-text log, now the FINAL REPORT's
real mechanism for matching assets to labels.
