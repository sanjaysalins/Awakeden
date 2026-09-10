# My Lord and My God — Master Prompt for Google Flow (Clean Rebuild v2)

John 20:24–29 (Doubting Thomas). "Swirls of Life" house style. All 8 generations — 2 character
references + 8 story shots, still + motion prompts — in one document. Companion file: `narration.md`
in this same folder (already written, KJV-verbatim, not part of this brief).

**Why a rebuild:** v1 sent the prompts one giant paragraph per shot with the house style
re-described every time, no dedicated reference-creation step (it pointed at old low-res crops
instead), and no explicit shot count up front. Result: the cover came out wrong, the operator
wasn't sure what to generate in what order, and the animation quality was inconsistent. This v2
copies the working mechanism of a proven brief from a sister project
(`MeekAndMighty/08_rhoda/creative/RHODA_FLOW_MASTER_PROMPT.md`): one HOUSE STYLE block stated once,
a dedicated reference-generation step before any story shot, compact per-shot entries, and a
"known traps" section instead of pretending nothing can go wrong.

**This series runs TWO deliberately different visual styles, not one — this was the actual source
of the last mismatch, not the Flow mechanism itself.** Interior pages (Shots 2 & 3) are the soft
hand-drawn ink-and-watercolor "found storyboard" look. Covers (Shots 1 & 4) are a separate,
harder-edged 16th-century woodcut-cinematic look, pulled directly from this project's own real
cover-generation code (`swirls_cover.py`) — small figures against a wide landscape, engraved
wood-block title lettering, not the ink-wash treatment. Both are correct; they're just not the same
style as each other, on purpose, and the House Style section below is split accordingly (A =
interior, A2 = covers).

**Assumption this document makes — flag if wrong:** the two existing character images in this
project (`the_thomas_ref.png`-family crops, `jesus_ref.png`) are used ONLY as likeness/style
Ingredients to generate brand-new, clean, high-resolution reference sheets THROUGH Flow itself
(Step 1 below) — not uploaded directly as the final references for the 8 story shots. This fixes
last time's low-resolution problem at the source instead of patching around it.

---

## ⚠ Read this before pasting anything into Flow

**The real bug, found by red-teaming this document, not guessed:** earlier versions of every
shot's "Still image prompt" code block were INCOMPLETE on their own — they started directly with
"Main scene..." and relied on the reader to separately notice and manually combine three other
things written elsewhere in the document: the base style paragraph (House Style A/A2), the page
layout structure (SEQ:/frame-number/3-panel grid, House Style B), and — for the interior pages —
the actual content of the three panels, which lived in a "Panel captions" note ABOVE the code block,
not inside it. Copying just the labeled code block (the natural, reasonable thing to do) would hand
Flow a prompt with no idea there should be three panels or what belongs in them. **That's a strong,
concrete explanation for the blank panels seen on the real test** — better founded than an earlier
draft of this note, which guessed the cause was Flow's own Gemini layer paraphrasing shorthand
references. That mechanism is real (Google's own description: "Gemini provides the intelligence
layer for understanding prompts," a real interpreting step OpenArt's direct API doesn't have) and is
still worth guarding against below — but it was not fully verified as THE cause, and shouldn't have
been stated that strongly. The incomplete-prompt-block bug is the better-evidenced fix.

**Fixed now: every "Still image prompt" code block below is completely self-contained** — the full
style paragraph, the panel structure, and every panel's content are all inline, in that one block,
every time. Copy exactly that block and nothing else; you do not need to also paste the HOUSE STYLE
section separately anymore (that section below is now reference documentation for how these prompts
were built, not something to paste each time).

**Still worth doing, since the interpreting-layer fact is real even if unverified as the specific
cause here:** when you paste a still prompt, say something like *"Use this prompt exactly as
written — do not summarize, shorten, or rewrite it before generating."* If Flow's interface has any
"enhance my prompt" or "auto-improve" toggle, turn it off before generating anything in this brief.

---

## How to use this in Flow

1. **Generate the 2 character reference images first** (Step 1 below) — Thomas, then Jesus. Do not
   start any story shot until both are approved.
2. **Generate the 8 story stills next, in order** (Shot 1 → 2 → ... → 8) — each shot's "Still
   image prompt" code block is complete on its own now; copy exactly that block, nothing more, no
   need to also find and paste the HOUSE STYLE section separately. Attach the approved character
   reference(s) as Ingredients per shot (table under each shot says which). **Ingredients are only
   needed at this still-generation step** — once a still is approved, the character's likeness is
   already locked into that image, so the animation step (next) does NOT need Ingredients
   re-attached.
3. **Animate each approved still** with its own MOTION prompt, 8–10s, 9:16 — animating FROM the
   still image itself, no reference images needed at this step.
4. **Send the Motion prompt and the Audio direction together, as ONE message, every time.** Never
   send Motion alone — that's the easiest way for Flow to default back to inventing dialogue, since
   nothing in the Motion text itself says "silent."
5. Zip everything and send back — see "What to send back" at the bottom.

**Total generations: 10.** 2 reference images (stills only, not animated) + 8 story shots (each a
still AND a clip). That's 10 stills, 8 clips. **Expanded twice now** — first from 4 to 6 shots to
close the raw-footage-vs-narration gap, then from 6 to 8 to fix the two shots that were still
carrying a real freeze-hold burden (F01 and Back Cover each needed 5-7 extra seconds of stretch
beyond their native clip length). Splitting each of those into two shots means almost every clip now
needs only a light trim or a small 1-2s hold, not a heavy stretch — see the real per-shot durations
under each shot below, all measured against the real synthesized narration
(`ASSEMBLY_PLAN.md`).

| # | Name | Type | Animated? | Covers | Real duration |
|---|---|---|---|---|---|
| Step 1a | Thomas reference | reference image | no | — | — |
| Step 1b | Jesus reference | reference image | no | — | — |
| Shot 1 | Front Cover | story shot | yes | "We have seen the Lord" | ~7.1s |
| Shot 2 | F01 — "I will not believe" | story shot | yes | Thomas's refusal (just his declaration now) | ~11.4s |
| Shot 3 | F02 — "Eight Days" *(NEW, split off Shot 2)* | story shot | yes | the time-passage bridge | ~5.5s |
| Shot 4 | F03 — "Peace be unto you" | story shot | yes | Jesus's arrival, doors shut | ~7.3s |
| Shot 5 | F04 — "Reach hither" | story shot | yes | the invitation | ~12.8s |
| Shot 6 | F05 — "My Lord and my God" close-up | story shot | yes | the confession itself | ~4.9s |
| Shot 7 | F06 — "Answered You Too" *(NEW, split off Back Cover)* | story shot | yes | the pull-back before the landing | ~3.8s |
| Shot 8 | Back Cover | story shot | yes | "Blessed are they that have not seen" | ~11.6s |

---

## HOUSE STYLE — paste into every story-shot prompt (Shots 1–4, not the reference sheets)

**A · MASTER STYLE (verbatim, every interior page — Shots 2 & 3):**
One single storyboard page of hand-drawn animation development art, delicate ink linework and
watercolor on aged cream paper with visible grain, laid out like a real found piece of production
art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book
inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element
behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black
ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame.

**A2 · MASTER STYLE, covers only (Shots 1 & 4) — a DIFFERENT, deliberately distinct look from the
interior pages, this project's own real cover convention, not the ink-wash style above:**
16th-century Albrecht Dürer woodcut linework blended with contemporary cinematic landscape
photography — dense parallel hatching, hard black contours, ink-on-block texture, dramatic
volumetric light rays, photographic tonality. Figure(s) held small, in the lower third of the
frame, against a vast wind-scoured wilderness — rugged rocky hill country, sweeping stony valleys,
carved structural cloud forms in an open sweeping sky. Stationary camera, wide static shot,
ultra-crisp. No storyboard panel grid, no "SEQ:"/frame-number labels on covers. Vertical 9:16.

**A2a · LIGHTING CONTRAST (both covers, non-negotiable):** the lighting sentence must name at least
one WARM element (ochre / gold / golden / amber / warm / dawn / dusk-sun / ember) AND at least one
COOL element (teal / blue / cool / grey / cold) in the same scene. A cover with only one temperature
has shipped as a real defect before on this series (an earlier episode's front cover lost all color
contrast) — this is a known trap, not a hypothetical.

**A2b · TITLE LETTERING (both covers):** bold engraved wood-block title lettering, carved in the
same dense woodcut style as the rest of the image — thick confident carved strokes, NOT a modern
font, not a decorative flourish font, no drop shadow, no glow, no banner or box behind it, sitting
naturally within the composition. Smaller matching lettering beneath it for the subtitle/reference.
No other text, letters, numbers, or words appear anywhere on the image beyond these two lines.

**A2c · EDGE-TO-EDGE (both covers):** the artwork fills the entire image edge to edge — never a
drawn border, picture frame, caption strip, or margin band around the scene. At the edge OPPOSITE
the title (bottom for the front cover, top for the back cover), the scene's own artwork runs all
the way to the canvas edge, fully painted, no blank paper showing. A blank margin band at that
opposite edge has shipped as a real defect before on this series — also a known trap, not
hypothetical.

**A2d · COVER NEGATIVE (replaces House Style E for Shots 1 & 4 only — interior-page E does not
apply to covers):** modern clothing, busy foreground, bright neon colors, deformed anatomy, blurry
rendering, smooth photorealism without linework.

**P · PERIOD (every shot, stills and motion, no exceptions):** 1st-century Roman Judea, Jerusalem —
an upper room in a modest stone house. Plain plastered stone walls, a shuttered wood-lattice window
with no glass, a heavy wooden door on a simple wood or iron bar, worn stone or packed-earth floor, a
small clay oil lamp with a pinched wick and no visible chimney or glass. Simple ankle-length tunics
in undyed cream or muted natural-dye colors, a looser mantle draped over one shoulder, a woven or
roped belt, plain leather sandals — no visible buttons, zippers, buckles, or metal fasteners of any
kind beyond simple cloth ties. No eyeglasses, no wristwatches, no modern haircut shapes, no bright
synthetic-looking dye colors. No electric light anywhere — only the oil lamp's glow and daylight
through the shutter. Architecture stays plain: no carved relief work, no stained glass, no arches
beyond a simple doorway.

**B · PAGE LAYOUT CONVENTION (interior pages only — Shots 2–7):** Top-left title, handwrite:
"SEQ: THOMAS". Top-right frame number, handwrite: the shot's own frame code ("F01" through "F06").
Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3
as its ONLY label. Below them, ONE large full-scene illustration filling the lower half of the page.
Small handwritten production notes: a caption beneath the main scene, and a corner note. No other
text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings
given in each shot below — no invented captions, signs, inscriptions, or titulus.

**C · DEAD-INK / MOTIF RULES (every shot with Thomas or Jesus in it):**
- **Halo:** Jesus only, a faint incomplete calligraphic halo of muted gold-and-blue curls, never a
  solid disc. It is SEPARATE from and unrelated to the blue-ink motif elsewhere on the page — does
  not grow, spread, or merge with it. No halo ever appears on Thomas or any other figure.
- **Fray (doubt) progression, Thomas only — this episode uses all three stages, in order across the
  6 interior shots, never skipping or reversing:**
  - **FR2, Shots 2 & 3 (full doubt):** his outline broken in short stretches and struck again, a
    second faint tremored line running close beside his true contour, cross-hatching scratchy and
    overworked — while every OTHER figure on the page stays a steady, single-struck confident line.
    The contrast must be unmistakable. Shot 3 ("Eight Days") and Shot 4 (Jesus's arrival) both keep
    this SAME FR2 state unchanged — nothing has happened yet to ease it.
  - **FR1, Shot 5 (loosening, not resolved):** loose, easing hatching — no longer sharply broken,
    but not yet a fully confident single line either. Doubt easing, not gone. Do not let this shot
    drift all the way to a fully steady line; that belongs to Shot 6 only.
  - **FR0, Shots 6 & 7 (fully resolved):** his contour is now one single, unbroken, confidently
    struck line, matching every other figure. No broken/doubled/tremored line remains anywhere on
    him. Shot 7 ("Answered You Too") keeps this SAME FR0 state — the resolution already happened,
    this shot holds it.
  This lives in the character of the ink line only — Thomas himself stays one solid, still figure
  in every shot, never blurred, never a double image.
- **Chromatic reservation:** blue and gold belong ONLY to the life motif and Jesus's halo — Thomas
  wears and carries no blue, no gold, anywhere, ever.
- **The gap rule (any shot where the motif or Jesus's hand reaches toward Thomas — Shots 2, 5 & 6,
  non-negotiable, holds even at the confession itself):** wherever the blue-ink motif or Jesus's
  offered hand reaches toward Thomas, it stops with a clear, visible, deliberate GAP before touching
  him — it never closes the gap, never touches his hand or figure. This is a hard rule, not a
  suggestion, and it does NOT relax as the story resolves — John's own text records an ANSWER
  (v.28), never a description of touch.
- **No graphic wounds:** any nail-mark on Jesus's hands is a small, faint, DRY ink mark only — never
  blood, never torn flesh, no red on or near his hands, no side wound depicted.

**D · AUDIO RULE (every story shot, state explicitly, separate from the visual prompt):** Ambient
sound only — no dialogue, no character speech of any kind, no narrator voice, no music. Lips stay
closed and do not move on every figure in every clip; nobody in this episode speaks on camera — all
spoken lines are added afterward as separate narration audio.

**E · NEGATIVE (paste as one line, every prompt, stills and motion both):**
photorealistic, anime, Disney, polished graphic design, clean comic-book inking, Renaissance
religious staging, glowing spiritual VFX, magic-particle glow, 3D render, CGI sheen, airbrushed
skin, glossy surfaces, blood, gore, torn flesh, open wounds, modern clothing, modern objects,
speech bubble, thought bubble, text box, caption box or banner around any handwritten note, any
invented text beyond the exact handwrite strings given, a second/duplicate figure, blurred figure,
transparent figure, extra limbs, malformed hands, changing facial identity between shots, camera
pan/zoom/orbit/dolly/handheld on any story shot (locked static camera only).

**F0 · MOTION PROMPTS SPECIFICALLY — CONFIRMED, not hypothetical (see Known Traps below): the
first delivered test batch came back with literally zero motion in all 4 clips** (frame-diffed
pixel-by-pixel — the tiny differences present were compression noise, not real movement). The
likely cause: those motion prompts opened with 2-3 sentences of "locked camera, everything stays
exactly as drawn, never redraws" BEFORE ever describing the one thing that should move — the
stillness language dominated and the model rendered exactly that, a still. **Fix, applied to every
Motion prompt below and required on any new one:** state the actual motion FIRST, in a full
sentence, using continuous/visible language ("flickers continuously and visibly," "a real readable
push," "walk continuously onward") — never bury it after the lock/stillness rules. Put "camera:
locked, static" and the "stays exactly as drawn" preservation clauses AFTER the motion description,
as a closer, not an opener.

**F · PRECISION — how every prompt here is worded, and how to write any new one:** a model told only
"no X" can still invent X — negation alone is unreliable. Confirmed the hard way elsewhere in this
project: stacking stronger "never do X" wording on a defect sometimes made it worse; what actually
worked was removing the thing from the prompt's attention entirely. So every rule in this brief
states the POSITIVE fact first (what IS there, what DOES happen), with the negative as
reinforcement, never as the only instruction — check any new prompt against that order before
sending it. Use an exact count wherever a number matters ("exactly three disciples," "exactly three
panels") — an uncounted crowd invites drift; leave a count OPEN only where the scene is deliberately
an indefinite multitude (Shot 8's road). Avoid a mood word with no concrete fact under it — not
"dramatic lighting" alone, but the actual light source, direction, and color named. Every constraint
should be checkable by looking at the result — if a rule can't be verified by eye, it isn't specific
enough yet.

---

## Known traps — worth knowing before you generate, not after

- **CONFIRMED, not hypothetical — zero-motion clips.** The first test batch through this brief came
  back with all 4 clips showing no perceptible motion at all — checked by pixel-diffing actual
  frames, not just eyeballing (the tiny differences present were compression noise, evenly spread
  across the whole frame, not concentrated where the intended flame/hand/figures were meant to
  move). Root cause and fix: see House Style F0 above — every Motion prompt in this document has
  been rewritten to lead with the actual motion instead of the stillness rules. If a regenerated
  clip STILL shows no motion after this fix, that's a genuinely new problem worth flagging back
  immediately, not something to accept.

- **A halo hallucinating onto Thomas.** A prior animation attempt on this exact character (not
  through Flow — a different generator) produced a halo on Thomas even though the prompt explicitly
  said only Jesus gets one. If it happens here too, that's a known model tendency, not a sign the
  prompt is wrong — reject and retry that one generation rather than rewriting the rule.
- **A "floating" thread/gesture that doesn't read as connected to the actual action.** An earlier
  version of Shot 2's design had the blue thread rising straight up out of the disciple's hands with
  no clear destination — on review it read as decorative background squiggle, not "life reaching
  toward Thomas." Fixed in Shot 2's prompt below (the thread arcs low, directly toward Thomas's
  raised palm) — if Flow's output drifts back toward a vertical/undirected thread, that's the same
  failure recurring, worth a regenerate rather than accepting it.
- **Clip length may not land exactly on the requested duration.** Flow/Veo has been observed
  elsewhere returning clips at a near-fixed length regardless of the requested duration. If a shot
  comes back shorter than ~8s, that's expected, not a mistake — flag it back and it'll be extended
  in final assembly (a last-frame hold, never a re-request loop).
- **A close two-figure shot (Shots 5 & 6, Jesus + Thomas — Shot 6 especially, the tightest framing
  in the episode) may resist keeping the hand-gap clean on the FIRST attempt.** Check this
  specifically before approving — it's the one rule in this whole brief that must never fail
  silently.
- **CONFIRMED — an animation inventing motion the still explicitly forbids.** A real test render of
  the Front Cover animated the door swinging open with a hand reaching through and light spilling
  out, directly contradicting both the Motion prompt ("the door... never moves, opens, or changes")
  and the still's own baked corner note. If any door/barrier this episode establishes as shut starts
  to open, close, or change during a clip, reject it — that rule has zero tolerance, not "mostly
  holds."
- **CONFIRMED — a two-line caption truncating to one line.** A real test render of Shot 6 (the
  confession close-up) baked only "My Lord and" into the still, silently dropping "my God" — present
  in every frame of the resulting clip, not a one-off glitch. Always check multi-line captions
  render BOTH lines before approving a still, especially on close/tight framings.
- **A cover losing its warm/cool color contrast.** A real defect on a prior episode's front cover —
  it rendered with no vivid color anywhere, just one flat temperature. Check both covers (Shots 1 &
  8) specifically for a genuine warm note AND a genuine cool note before approving (A2a).
- **A blank paper margin band opposite the title.** Also a real, repeated defect on a prior
  episode's covers (3 for 3 on one episode) — a strip of unpainted paper at the edge away from the
  title text, even on an otherwise-approved render. Check the edge opposite wherever the title sits
  (A2c) — the artwork should run fully to that edge too.
- **A stretched-out clip can go dead in the back half.** These beats were originally designed for
  5-second clips, where "the gesture completes, then holds for a second" reads as a natural pause.
  Stretched to 8-10s, that same hold could run 4-5 seconds of near-total stillness — this project's
  own standard explicitly rejects "technically clean but static" clips as a fail, same as it would
  reject invented extra motion. Watch full playback, not just the first couple of seconds, before
  approving any clip.

---

## Character references — generate these FIRST

One clean reference IMAGE per character (not a multi-pose composite sheet — kept simple to match
the proven mechanism, and a split side-by-side layout doesn't sit well in a 9:16 vertical frame
anyway). Standing three-quarter view, close enough to read the face clearly, wide enough to read
the robe and build.

### Step 1a — Thomas reference

**Still image prompt:**
```
A single clean reference image, plain neutral background, hand-inked linework and watercolor wash matching the attached reference images exactly — same face, same likeness, same build. A sturdy middle-aged Galilean man with a squarish weathered face, heavy dark brows, deep-set questioning eyes, dark hair and a short thick dark beard flecked with grey, a plain robe of muted clay-red wash over an undyed cream tunic, a rough olive-brown mantle across one shoulder, drawn in dense workmanlike cross-hatching; he wears no blue and no gold anywhere. Standing three-quarter view, calm neutral expression, arms visible at his sides, steady confident single-struck ink line (no Fray/doubt marking on this reference — that gets applied per-shot later). High resolution, sharp linework, no blur, no text, no caption, no background scene — just the figure on a plain aged-cream paper ground.
```
**Ingredients to attach:** `thomas_ref_hd_face.png` + `thomas_ref_hd_full.png` (likeness/style guides — both already in this folder).

### Step 1b — Jesus reference

**Still image prompt:**
```
A single clean reference image, plain neutral background, hand-inked linework and watercolor wash matching the attached reference image exactly — same face, same likeness, same hair, same beard, same robe colors and style. A first-century Jewish man in his early thirties, lean from travel, weathered calm face, dark textured shoulder-length hair, short natural beard, drawn in broad confident economical ink strokes, loose layered robes of deep indigo and charcoal watercolor that pool and bloom and leave paper exposed, a faint incomplete calligraphic halo of muted gold-and-blue curls close around his head, never a solid disc. Standing three-quarter view, both hands open at chest height with palms visible (this episode needs his open palms clearly), calm neutral expression. High resolution, sharp linework, no blur, no text, no caption, no background scene — just the figure on a plain aged-cream paper ground.
```
**Ingredients to attach:** `jesus_ref_upscaled3x.png` (likeness/style guide — already in this folder).

**Once both are approved, use THEM (not the old files) as the Ingredients for every shot below.**

---

## THE 8 STORY SHOTS, IN ORDER

### Shot 1 — Front Cover

Composition note: this episode is set entirely indoors, but this series' covers are built around a
small figure held against a wide exterior world — confirmed by checking how another indoor-story
episode ("She Loved Much") solved the same problem: framed at a threshold, not deep inside the
room. Same move here, and it happens to be the text's own detail — "the doors being shut" (John
20:19, 26) IS the image.

**Still image prompt (complete — everything needed is in this one block, nothing lives outside it):**
```
16th-century Albrecht Dürer woodcut linework blended with contemporary cinematic landscape photography — dense parallel hatching, hard black contours, ink-on-block texture, dramatic volumetric light rays, photographic tonality. Stationary camera, wide static shot, ultra-crisp. Vertical 9:16 frame. No storyboard panel grid, no "SEQ:"/frame-number labels — this is cover art, not a story page. The exterior of a plain stone house on a narrow street at dusk, seen from the street itself. A heavy wooden door fills the center-right of the frame, shut and barred, its old grain and iron fittings catching the last low light, held small in the lower third against the house's stone wall rising above it. Beside the door's edge, a narrow gap lets one thin bar of warm lamplight escape from within — and in that sliver of light, Thomas is glimpsed small and shadowed just inside, his raised palm-out hand catching the light's edge, his face turned from it in refusal. Above the doorway and the house's stone shoulder, a strip of open dusk sky and the dark rooftops of the narrow street recede into shadow. Warm amber lamplight spills in that single thin bar beside the door — the only warm note in the whole frame; cold blue-grey dusk fills the street, the stone, and the sky above, deep teal shadow pooling at the door's foot. No other figure anywhere in this frame. No halo, no glow, no spiritual VFX. Stage 0 dosage: no blue or gold Swirls-of-Life ink motif anywhere on this page. Near the top of the frame, bold engraved wood-block title lettering, carved in the same dense woodcut style as the rest of the image — thick confident carved strokes, NOT a modern font, not a decorative flourish font, no drop shadow, no glow, no banner or box behind it, sitting naturally within the composition, reading: "MY LORD AND MY GOD" — write this exact phrase once, as one continuous title, do not repeat any word in it. Smaller matching carved lettering beneath it reading: "JOHN 20". No other text, letters, numbers, or words appear anywhere on the image beyond these two lines. The artwork fills the entire image edge to edge — never a drawn border, picture frame, caption strip, or margin band around the scene; at the bottom edge of the frame (opposite the title), the scene's own artwork runs all the way to the canvas edge, fully painted, no blank paper showing. Avoid: modern clothing, busy foreground, bright neon colors, deformed anatomy, blurry rendering, smooth photorealism without linework.
```
**Ingredients:** Thomas reference only. **Target: ~7s** (measured against the real synthesized
narration — see `ASSEMBLY_PLAN.md` — this shot covers 0.00–7.10s of the actual audio; generate at
Flow's normal ~8s and it'll trim down cleanly, no extension needed).

**Motion (per FRONT_ANIM_LOCK convention — motion leads, stillness rules trail):**
```
The thin bar of lamplight beside the door flickers continuously and visibly for the entire clip — small warm pulses of brightness rising and falling, never settling into a flat glow. This flicker is the clip's main visible motion, present from the very first frame to the very last. Thomas's raised hand, glimpsed in that light, presses further outward across roughly the first half of the clip, then holds firm for the remainder. Camera: stationary, locked wide shot, no pan, no zoom. The baked title lettering at the top stays pixel-for-pixel identical throughout — same opacity, no fade, no drift, no duplication. The door, stone, street, and sky stay as drawn. No new figure, mark, or text appears at any point.
```
**Audio:** faint lamp flicker, distant muffled street/night ambience from outside the door. (Rule D applies.)

---

### Shot 2 — F01 "I will not believe"

**Still image prompt (complete — everything needed is in this one block, nothing lives outside it):**
```
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain, laid out like a real found piece of production art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F01". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "not with them") a small sketch of a shut wooden door with its heavy bar in place; panel 2 (handwrite: "the proof") a small plain study of a single iron nail lying on its side, drawn as a quiet dry object; panel 3 (handwrite: "eight days") a small sketch of a low-burned oil lamp beside a shuttered window, its oil nearly spent. Below them, ONE large full-scene illustration filling the lower half of the page — a MEDIUM WIDE shot: a plain lamplit room at evening, a shuttered window on the back wall. Three of the other disciples stand together at the left, faces alight with joy, the foremost mid-gesture of telling, his open hands lifted toward Thomas, fully inside the frame. Thomas stands apart at the right, turned half away, his near arm raised with his palm out toward the group in refusal, that hand fully inside the frame and unobstructed, jaw set, mouth closed, eyes averted. Empty lamplit floor between them. Jesus is not in this scene and does not appear anywhere on the page. The three disciples: steady, confident, single-struck ink lines and even hatching. Thomas alone is drawn with an unsteady, doubting line — his outline broken in short stretches and struck again, a second faint tremored line running close beside his true contour, cross-hatching scratchy and overworked — while every OTHER figure on this page (the three disciples) stays a steady, single-struck confident line; the contrast between Thomas's broken line and their steady lines must be unmistakable. Thomas himself stays one solid, still figure, never blurred, never a double image. One restrained thread of blue ink, with the faintest trace of muted gold, rises from the foremost disciple's open lifted hands and arcs LOW across the open floor directly toward Thomas's raised palm, reaching nearly to the level of his hand — a clear, deliberate, visible GAP remains between the thread's end and his palm; the thread stops there and does NOT touch his hand or his figure — this gap is a hard rule, not a suggestion. The thread touches nothing and no one else, one smooth unbroken confident calligraphic line, sharing nothing of Thomas's broken tremored line character. Small handwritten production notes: a caption beneath the main scene, handwrite: "I will not believe", and a corner note, handwrite: "NOTE: line unsteady". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus.
```
**Ingredients:** Thomas reference sheet only (Jesus not in this shot). **Target: ~11.4s real
requirement** (measured against the real narration — see `ASSEMBLY_PLAN.md` — this is just Thomas's
declaration now, 7.10–18.54s; the "eight days" bridge that used to share this shot has its own
dedicated shot next. Generate at Flow's normal 8-10s and extend by only ~1-2s via freeze-hold —
a light hold, not a heavy stretch.)

**Motion (motion leads, stillness rules trail):**
```
The foremost disciple leans in toward Thomas continuously across the first third of the clip, his open hands visibly rising further in appeal — real, clearly readable movement, not a subtle shift — then holds his new position for the remainder. The lamp flame in panel 3 sways continuously and visibly the entire clip, never going still. Thomas's raised palm presses further outward across that same first third, a real visible push, then holds firm. His chest visibly rises and falls once with a slow, tense breath partway through the hold. The other two disciples stir gently throughout, small continuous shifts of weight. Camera: locked static. All lips stay closed, nobody speaks. The blue thread's tip stays fixed in its gap short of Thomas's hand — it does not move, that gap is the one thing that must never change. Thomas's broken/tremored linework keeps its exact drawn character throughout.
```
**Audio:** faint room tone, soft rustle of robes as the disciples lean in, barest floorboard creak. (Rule D applies — disciples and Thomas do NOT speak aloud in this clip.)

**Checklist before moving on:** Jesus absent, no halo anywhere · Thomas's line visibly broken vs. the 3 steady disciples · thread stops with a clear visible gap, never touches · baked text exact, nothing extra.

---

### Shot 3 — F02 "Eight Days" (NEW — split off Shot 2 to fix a real freeze-hold problem)

Covers the time-passage bridge — "Eight days he stayed with them anyway" — that used to share Shot
2's clip and forced a heavy ~7s freeze-hold there. Giving it its own shot fixes that AND gives this
real beat (he doubted, but he didn't leave) its own moment instead of being an afterthought.

**Still image prompt (complete — everything needed is in this one block, nothing lives outside it):**
```
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain, laid out like a real found piece of production art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F02". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "the door") the same shut barred door, unchanged; panel 2 (handwrite: "the lamp burns low") a small study of the same oil lamp beside the shuttered window, its flame smaller now, its oil visibly lower than before; panel 3 (handwrite: "yet he stayed") a small sketch of a pair of sandaled feet, planted still on the floor, not turned toward any door or exit. Below them, ONE large full-scene illustration filling the lower half of the page — a MEDIUM WIDE shot, quieter than the page before: the same plain room, later in the evening, the lamp burning lower now. Thomas stands alone at the right of the frame, apart from the others but still fully inside the same room — he has not left, fully inside the frame, arms now at his sides, no longer raised in active refusal, but his face still set and unconvinced, eyes lowered rather than meeting anyone's gaze. The three disciples are visible in the middle distance at the left, seated or settled for the evening, quiet, steady confident single-struck ink lines and even hatching, paying Thomas no particular attention — this is a quiet in-between moment, not a confrontation. Thomas alone keeps his outline broken in short stretches and struck again, a second faint tremored line running close beside his true contour, cross-hatching scratchy and overworked, exactly as unsteady as before — nothing has changed in his doubt, only time has passed. No blue ink motif appears anywhere near Thomas in this shot. Jesus is not in this scene and does not appear anywhere on the page. Small handwritten production notes: a caption beneath the main scene, handwrite: "yet he stayed", and a corner note, handwrite: "NOTE: line still unsteady". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus.
```
**Ingredients:** Thomas reference sheet only. **Target: ~5.5s real requirement** (measured — covers
18.54–24.0s of the real narration. Well under Flow's normal 8-10s native length, generate normally
and trim down — no extension needed at all.)

**Motion (motion leads, stillness rules trail):**
```
The lamp flame in panel 2 burns low and continuously flickers, visibly smaller and dimmer than an ordinary flame, for the entire clip — the clip's main visible motion, marking time passing. Thomas's chest rises and falls once with a slow, quiet breath, midway through the clip — a small, real, readable motion, not a static pose. The seated disciples in the middle distance shift very slightly, a small settling motion, once. Camera: locked static. Thomas's lips stay closed, not speaking; the seated disciples' lips stay closed too. Thomas's broken/tremored linework keeps its exact drawn character throughout — unchanged, since his doubt has not moved. No line anywhere redraws, no new figure, mark, or text appears at any point.
```
**Audio:** very quiet room tone, the faint low crackle of the dimming lamp, near-silence otherwise.
(Rule D applies — nobody speaks aloud in this clip; "Eight days he stayed with them anyway — the
men he wouldn't believe" is added later as narration.)

**Checklist before moving on:** Thomas has NOT left the room — still fully present · his Fray is
UNCHANGED, still broken (matches Shot 2, does not ease here) · the lamp reads visibly lower/dimmer
than Shot 2's · baked text exact.

---

### Shot 4 — F03 "Peace be unto you" (renamed from Shot 3)

Covers the beat that had NO visual before either of the last two rebuilds: Jesus's actual arrival —
"the doors being shut, and stood in the midst, and said, Peace be unto you" (John 20:26). This
happens a beat BEFORE he turns specifically to Thomas (that's Shot 5) — here the focus is the
miracle of the appearance itself, Thomas present but not yet singled out.

**Still image prompt (complete — everything needed is in this one block, nothing lives outside it):**
```
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain, laid out like a real found piece of production art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F03". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "doors being shut") the same shut door, still barred; panel 2 (handwrite: "peace be unto you") a small sketch of one open hand raised in blessing; panel 3 (handwrite: "stood in the midst") a small sketch of an empty patch of floor, nothing marking how he came to be there. Below them, ONE large full-scene illustration filling the lower half of the page — a MEDIUM WIDE shot: the same plain room, now filled with morning light through the shuttered window. The heavy door in the background is fully shut and barred, exactly as drawn before — no gap, no opening. Jesus stands at the center of the room, having simply appeared there, one hand raised open at chest height in a plain gesture of blessing, his face calm and glad, turned generally toward the group rather than at any one person yet. The other disciples stand in a loose cluster to one side, caught mid-reaction — surprise easing into joy, a few hands half-raised. Thomas stands among them, not singled out, not yet approached, his outline still broken in short stretches and struck again, a second faint tremored line running close beside his true contour, cross-hatching scratchy and overworked — unchanged from the earlier page, since nothing has happened yet to resolve his doubt; every OTHER figure in this scene, including Jesus and the other disciples, stays a steady, single-struck confident line, so Thomas's broken line reads as a clear, unmistakable contrast. Jesus has a faint incomplete calligraphic halo of muted gold-and-blue curls around his head, never a solid disc. No blue ink motif elements point toward or touch Thomas in this shot — if any thread is shown at all, it stays close around Jesus's own figure only, touching no one, not reaching toward anyone yet. Small handwritten production notes: a caption beneath the main scene, handwrite: "Peace be unto you", and a corner note, handwrite: "NOTE: no door opened". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus.
```
**Ingredients:** Thomas reference + Jesus reference (both — Jesus's first appearance in the
episode). **Target: ~7.3s real requirement** (measured — covers 24.0–31.3s of the real narration.
Close to Flow's normal range, generate at 8s and trim, no extension needed).

**Motion (motion leads, stillness rules trail):**
```
Jesus's raised hand settles slowly downward across roughly the first third of the clip — a real, visible, deliberate lowering motion, not a static pose — then holds at rest for the remainder. The disciples visibly react across that same opening stretch: shoulders easing, a couple of heads turning toward Jesus, real readable motion, then settling into stillness. Morning light shifts visibly across the door and the raised-open-palm study in panels 1 and 2 throughout the clip. Camera: locked static. Jesus's lips stay closed and completely still — not speaking. Thomas's broken/tremored linework keeps its exact drawn character, unchanged from before — it does not begin resolving in this clip. No line anywhere redraws, no new figure, mark, or door opening appears.
```
**Audio:** soft morning room tone, a collective intake of breath from the group, faint rustle of
robes. (Rule D applies — nobody, including Jesus, speaks aloud in this clip; "Peace be unto you" is
added later as narration.)

**Checklist before moving on:** the door stays completely shut throughout, no visible mechanism for
Jesus's arrival · Thomas's Fray is UNCHANGED here, still broken (it resolves in Shot 5, not this
one) · halo on Jesus only · baked text exact.

---

### Shot 5 — F04 "Reach hither" (renamed from Shot 4)

Covers Jesus's spoken invitation itself (beat 5, John 20:27) — this is BEFORE the confession, not
the confession. Thomas's doubt is loosening here, not yet gone; the actual resolution is reserved
for Shot 6's close-up, so don't let this shot's Fray or pose get ahead of itself.

**Still image prompt (complete — everything needed is in this one block, nothing lives outside it):**
```
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain, laid out like a real found piece of production art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F04". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "the wounds") a close study of Jesus's one open palm, a single faint dry nail-mark; panel 2 (handwrite: "reach hither") a small sketch of Thomas's own hand, half-raised, uncertain; panel 3 (handwrite: "be not faithless") a small sketch of the bare gap of air between two reaching hands, nothing touching. Below them, ONE large full-scene illustration filling the lower half of the page — a MEDIUM TWO-SHOT: the same room, morning light through the shuttered window, the other disciples drawn back into a loose still ring behind. Jesus stands at the left, now turned fully and specifically toward Thomas — singled out from the group, unlike the previous page — both open hands held out toward Thomas at chest height, palms toward him, a single small faint dry ink nail-mark in each palm — the mark is a small quiet ink mark only, never blood, never torn flesh, no red anywhere on or near his hands — both palms fully in frame. Thomas stands at the right, still on his feet, not yet kneeling, his near hand half-raised toward Jesus's offered hands, uncertain, not yet committed — a clear, deliberate, visible GAP remains between his fingertips and Jesus's hands; they do not touch, this gap is a hard rule that holds at every stage of this story, including the eventual confession in a later page. Thomas's linework is loose and easing — no longer sharply broken like the earlier pages, but not yet one fully confident single line either; doubt loosening, not gone. Jesus has a faint incomplete calligraphic halo of muted gold-and-blue curls around his head, never a solid disc. The blue ink motif: a few soft threads beginning to curl in the air between the two figures, still well short of either hand, touching neither — the life reaching further than it has before, still not arriving. Small handwritten production notes: a caption beneath the main scene, handwrite: "reach hither thy hand", and a corner note, handwrite: "NOTE: line loosening". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus.
```
**Ingredients:** Thomas reference + Jesus reference (both). **Target: ~12.8s real requirement**
(measured — covers 31.3–44.1s of the real narration, since Jesus's spoken invitation runs 10.88s on
its own. Generate at Flow's normal 8-10s, extend a couple seconds via freeze-hold in assembly — this
is the one shot in the episode that still needs a real, if modest, freeze extension.)

**Motion (motion leads, stillness rules trail):**
```
Thomas's half-raised hand trembles visibly and inches closer within its own drawn range across the whole clip — a real, continuous, readable tremor and slow approach, not a static pose — before settling, still short of the gap, in the final moment. His breathing visibly changes partway through — shoulders lowering out of refusal but not yet at rest, a clear physical shift. The soft blue threads between the two figures drift continuously and visibly the entire clip, curling and shifting in the air, never locking into a static shape. Camera: locked static. Jesus's offered hands stay steady and open throughout, unmoving, the invitation held out; his lips stay closed, not speaking. Thomas's lips stay closed too. The hand-gap itself does NOT close, does not touch — that one thing stays fixed even while everything around it moves. Thomas's FR1 linework keeps its own drawn character; it does not resolve further in this clip. No new mark appears.
```
**Audio:** soft morning room tone, a held, uncertain quiet, faint rustle of cloth. (Rule D applies
— neither Jesus nor Thomas speaks aloud in this clip; "Reach hither..." is added later as
narration.)

**Checklist before moving on:** the gap between the two hands is clearly visible and does NOT close
· Thomas is NOT yet kneeling, NOT yet fully resolved (that's Shot 6) · one small dry nail-mark per
palm, no blood/red · halo on Jesus only · baked text exact.

---

### Shot 6 — F05 "My Lord and my God" close-up (renamed from Shot 5)

The actual confession, given its own dedicated shot instead of sharing a wide two-shot — this is
the episode's emotional peak and now gets a real close-up. The hand-gap rule still holds here even
at the climax (matching this story's own original design: John records an ANSWER in v.28, not a
description of touch) — Thomas's confession is spoken, not physical contact.

**Still image prompt (complete — everything needed is in this one block, nothing lives outside it):**
```
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain, laid out like a real found piece of production art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F05". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "he answered") a small sketch of Thomas's open hand, no longer raised in refusal, now simply open and relaxed at his side; panel 2 (handwrite: "and said unto him") a small sketch of the same gap of air from the previous page, now with the faintest single thread of blue reaching into it, still not touching; panel 3 (handwrite: "not faithless") a small sketch of morning light broadening across the floor. Below them, ONE large full-scene illustration filling the lower half of the page — a CLOSE TWO-SHOT (tighter framing than the previous page — this is the close-up the confession earns): Thomas, now kneeling, risen upright on his knees, face lifted fully to Jesus, filling the lower-right of the frame; Jesus's presence at the frame's left edge, his open offered hand still visible at the frame's edge with its single faint nail-mark, not his whole figure — the camera has moved in close on Thomas's face and posture, not on Jesus. Thomas's one hand still half-lifted toward the edge of frame where Jesus's hand is, stopped just short of touching — a clear, deliberate, visible GAP remains, closer than ever but still not touching; this gap is a hard rule and holds even at this climax. Thomas's contour is now one single, unbroken, confidently struck line — fully resolved, no broken or tremored line remains anywhere on him — his face lifted in open, unguarded worship, eyes wide, jaw loose, nothing held back. A few soft threads of blue ink, with the faintest gold trace, curl in the narrow gap between his reaching hand and the edge of frame where Jesus's hand is, closer than any prior page, still not touching either. Small handwritten production notes: a caption beneath the main scene, handwritten on exactly two stacked lines, both lines fully present and fully legible — the first line reads "My Lord and", the second line directly beneath it reads "my God" — this caption is not complete without both lines, check that "my God" is actually visible before accepting this page. Below the caption, a corner note, handwrite: "NOTE: line steady". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus.
```
**KNOWN RISK on this exact shot — check before accepting:** a prior real render of this page baked
only the first caption line ("My Lord and") and silently dropped the second line ("my God"),
present in every frame including the still itself. This is the confession line — the page is
incomplete without it. If it happens again, regenerate; do not accept a still with only one caption
line here.

**Ingredients:** Thomas reference + Jesus reference (both). **Target: ~4.9s real requirement**
(measured — covers 44.1–49.0s of the real narration. Shortest shot in the episode, matches Flow's
range naturally, no extension needed.)

**Motion (motion leads, stillness rules trail):**
```
One slow, visible breath loosens Thomas's shoulders fully across the length of the clip — a real, continuous, readable release of tension, shoulders and chest visibly settling from tight to open. His lifted face holds in open worship throughout, eyes wide and warm. The soft blue threads in the gap between his hand and Jesus's drift continuously and visibly, curling gently, never frozen into one shape. Camera: locked, close framing held throughout — no push, no zoom, the closeness is baked into the still. Thomas's lips stay closed and completely still — not speaking; the baked caption "My Lord and / my God" carries the words, not his mouth. His half-lifted hand stays exactly where drawn, in its own fixed gap, the whole clip — it never closes the gap, never touches. Jesus's visible hand at the frame's edge stays steady. Thomas's steady FR0 linework stays exactly as drawn, stroke for stroke.
```
**Audio:** a single soft settling breath, the faintest rustle as Thomas's weight shifts on his
knees, otherwise near-silence. (Rule D applies — Thomas's lips stay closed throughout, per the
Motion prompt above; "My Lord and my God" is added afterward as narration audio only.)

**Checklist before moving on — the one rule that must never fail silently, closest quarters yet:**
the hand-gap is CLEARLY visible and does not close, even in this tight framing · Fray fully
resolved, one single confident line · this is Thomas's shot — Jesus should read as present at the
frame's edge, not competing for the frame's center · baked text exact.

---

### Shot 7 — F06 "Answered You Too" (NEW — split off Back Cover to fix a real freeze-hold problem)

Covers the narrator's pivot line — "And Jesus answered him — answered you too:" — that used to
share Back Cover's clip and forced a heavy ~5s freeze-hold there. This beat is the turn from the
intimate Thomas scene toward the viewer; giving it a real image instead of stretching the road shot
to cover it makes that turn land as its own moment.

**Still image prompt (complete — everything needed is in this one block, nothing lives outside it):**
```
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper with visible grain, laid out like a real found piece of production art — not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX. Every blue or gold ink element behaves like literal wet ink bleeding into the paper, never a magic-particle glow. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash. Vertical 9:16 frame. Top-left title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F06". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "his own hands") a small close study of Jesus's two open hands, held together at rest, their faint nail-marks visible, no longer reaching, simply resting; panel 2 (handwrite: "the room at peace") a small loose sketch of the gathered disciples, calm, close together; panel 3 (handwrite: "the road ahead") a small sketch of an open doorway with a bright, plain, empty stretch of daylight beyond it, nothing else in the frame. Below them, ONE large full-scene illustration filling the lower half of the page — a WIDE shot, pulled back further than the previous page: the same room, full morning light, all the disciples now gathered loosely around Jesus and Thomas together in one settled group, no one apart from the others anymore. Thomas is still on his knees in the middle of the group, his face calm now, contour one single steady confident line, fully resolved, matching every other figure on the page — no broken or tremored line remains anywhere on him. Jesus stands at the center, his face turned slightly outward from the group, calm and open, his faint incomplete calligraphic halo of muted gold-and-blue curls around his head, never a solid disc. Soft threads of blue ink, with muted gold traces, now drift more freely through the open air of the room, above the whole gathered group rather than confined to one small area — quiet and restrained still, behaving like wet ink bled into the paper's morning light, never a magic-particle glow. Small handwritten production notes: a caption beneath the main scene, handwrite: "he answered him", and a corner note, handwrite: "NOTE: line steady, room at rest". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus.
```
**Ingredients:** Thomas reference + Jesus reference (both). **Target: ~3.8s real requirement**
(measured — covers 48.96–52.72s of the real narration. This is the shortest shot in the episode by
a wide margin; generate at Flow's normal 8-10s and trim down heavily — no extension needed at all.)

**Motion (motion leads, stillness rules trail):**
```
The soft blue threads above the gathered group drift continuously and visibly, curling slowly through the room's morning light, for the entire clip — the clip's main visible motion. Jesus's halo curls rotate slowly and continuously around his head. The gathered disciples shift very slightly, small settled movements of a group at rest, once early in the clip, then hold. Camera: locked static. All lips stay closed, nobody speaks, including Jesus and Thomas. Thomas's steady, fully resolved linework stays exactly as drawn, stroke for stroke, the entire clip — it does not change further, the resolution already happened on an earlier page. No new mark, figure, or text appears at any point.
```
**Audio:** soft morning room tone, the faint settled murmur of a group at rest, near-silence
otherwise. (Rule D applies — nobody speaks aloud in this clip; "And Jesus answered him — answered
you too" is added later as narration.)

**Checklist before moving on:** Thomas's Fray stays FR0, fully resolved, unchanged from the previous
page · halo on Jesus only · the group reads as gathered/settled, not posed or staged · baked text
exact.

---

### Shot 8 — Back Cover (renamed from Shot 6)

This one was already the right shape (a small-figures-against-open-landscape composition matches
the wilderness convention natively) — just needed the woodcut style, an explicit cool element for
lighting contrast, and the real title/edge/animation conventions.

**Still image prompt (complete — everything needed is in this one block, nothing lives outside it):**
```
16th-century Albrecht Dürer woodcut linework blended with contemporary cinematic landscape photography — dense parallel hatching, hard black contours, ink-on-block texture, dramatic volumetric light rays, photographic tonality. Stationary camera, wide static shot, ultra-crisp. Vertical 9:16 frame. No storyboard panel grid, no "SEQ:"/frame-number labels — this is cover art, not a story page. An open road climbing over a low, wind-scoured hillside at morning, seen from a clear middle distance, held small in the lower third of the frame against a sweeping open sky with carved structural cloud forms. Many ordinary figures, varied in age, dress, and stature, walk or stand on the road in loose small clusters, faces lifted toward the sky ahead, none looking back — ordinary anonymous people, none of them the disciples or Thomas from earlier in the story. No named figure, no halo, no glowing presence — Jesus does NOT appear anywhere in this frame. Warm morning gold light spills across the road and the near hillside from the upper right; cold blue-grey shadow still pools in the low ground and valley folds beyond the road, not yet reached by the light. Very faint traces of the blue-and-gold motif drift high in the open sky above the road — small, restrained, distant, more suggestion than presence, touching no figure. Near the bottom of the frame, bold engraved wood-block title lettering, carved in the same dense woodcut style as the rest of the image — thick confident carved strokes, NOT a modern font, not a decorative flourish font, no drop shadow, no glow, no banner or box behind it, sitting naturally within the composition, reading: "BLESSED ARE THEY THAT HAVE NOT SEEN" — write this exact phrase once, do not repeat any word in it. Smaller matching carved lettering beneath it reading: "JOHN 20:29". No other text, letters, numbers, or words appear anywhere on the image beyond these two lines. The artwork fills the entire image edge to edge — never a drawn border, picture frame, caption strip, or margin band around the scene; at the top edge of the frame (opposite the title), the scene's own artwork runs all the way to the canvas edge, fully painted, no blank paper showing. Avoid: modern clothing, busy foreground, bright neon colors, deformed anatomy, blurry rendering, smooth photorealism without linework.
```
**Ingredients:** none required — no named character appears in this shot. **Target: ~11.6s real
requirement** (measured — covers 53.0s through the end of the real narration at 61.3s, PLUS the
mandatory ≥3.0s silent landing hold after the last word (this project's own binding rule — see
`ASSEMBLY_PLAN.md`), so it needs to read as visibly alive through ~11.6s total. Much closer to
Flow's normal 8-10s native length now that the narrator bridge has its own shot — a light freeze-
hold (~1-2s) covers the rest. **Do NOT extend with a boomerang** — the figures are continuously
walking with no completing gesture, and a reversed mid-stride walk reads as broken (a real,
already-learned lesson in this project). Freeze the LAST frame instead, once the walk cycle looks
natural to stop on.

**Motion (per BACK_ANIM_LOCK convention — motion leads, stillness rules trail):**
```
The figures on the road walk continuously and visibly onward at an unhurried pace for the entire clip — real, readable footfalls and forward progress, not a subtle drift — exactly as many figures as drawn, none appearing or disappearing. The faint blue-and-gold sky traces drift continuously and visibly, curling slowly, staying small and distant but clearly in motion throughout, never locking into one static shape. Camera: stationary, locked wide shot, no pan, no zoom. The baked closing lettering at the bottom stays perfectly static the whole clip. None of the figures turn to face camera, gesture, or speak. Morning light and the cold valley shadow stay as drawn. No new figure, mark, or text appears.
```
**Audio:** soft open-air morning ambience — light wind, distant birdsong, faint footsteps on the road. (Rule D applies.)

---

## What to send back

One zip with, for each of the 8 story shots, the final still AND the final clip (keep the ambient
audio track — assembly will decide whether to keep or replace it). Also include the 2 approved
character reference images. Name files to match the shot list:

`ref_thomas.png`, `ref_jesus.png`,
`01_front_cover.png` / `.mp4`,
`02_f01_doubt.png` / `.mp4`,
`03_f02_eight_days.png` / `.mp4`,
`04_f03_arrival.png` / `.mp4`,
`05_f04_invitation.png` / `.mp4`,
`06_f05_confession.png` / `.mp4`,
`07_f06_answered_you_too.png` / `.mp4`,
`08_back_cover.png` / `.mp4`.

Final approved version only — no need to send rejected attempts.

## What happens after the zip comes back

Narration (already written, `narration.md` in this folder) and a score get muxed against these 8
clips using the same assembly process every other episode goes through — trimming/timing each clip
to its slot, checking the landing hold, laying SFX if the ambient audio needs backup — producing a
finished cut to review before anything posts. This episode counts toward the 30-episode target
either way.
