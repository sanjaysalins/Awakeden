# Fable — enhancement briefs for STORM (living-sketchbook)

**Date:** 2026-07-29 · **Piece:** `STORM_living_sketchbook.mp4`, 13 spreads, 63.0s, 9:16
**Read first:** `.claude/skills/living-sketchbook/SKILL.md`, `panel_animator/README.md`

---

## The creative take

I looked at the real stills at full resolution (s01, s04, s08, s09, s10, s13) and read the
assembler. Here is what I think the piece is, and what it is missing.

Every spread is **two things stacked**: a drawing, and a sheet of paper the drawing sits on.
The sheet is beautifully specified — torn kraft edge, hairline engineering rules, halftone
patches in the corners, a strip of real gold leaf down the right side, a cream inner sheet
lifting off a warmer backing. And it is doing **absolutely nothing**. In all 13 spreads the
paper is wallpaper: the model paints it, the animator ignores it, the camera pushes past it.
Every device this project has built so far — Scribed Ink, Ink Stamp, the torn page, grain-boil,
paperRip — acts on the *picture*. Almost nothing acts on the *paper*.

That is the whole opportunity, and it is not just an aesthetic one. **Anything done to the
paper is $0, deterministic, and structurally incapable of inventing doctrine.** A wash that
creeps, a sheet that buckles, a tide-mark that rises — none of them can put an extra hand on
Jesus, invent a fourth disciple, or grow a modern trouser hem. The failure modes logged in
SKILL.md §8a all live in the *generated* layer. Devices in the paper layer are immune to every
one of them, cost nothing, and are the fastest remaining lever on how expensive and hand-made
this piece feels.

Second observation: this episode's subject is **water**, and its structure is **a turn** —
storm to calm, at exactly 29.79s. That is a gift. Watercolour has real physical behaviours
(bleeding, blooming, backruns, cockling, drying, tide-marks) that *are* water. This is the one
episode in the catalogue where the medium and the subject are the same substance. The medium
can carry the miracle: the sea obeys — so does the wash.

Third: the alignment file is word-perfect (172/172) and every device so far reads it for
*words*. Nothing in this repo reads it for **silence**. The biggest gap in the whole narration
is 1.64s, and it sits immediately after "He is asleep." That silence is the thesis of the
episode and no device is using it.

So: eight devices, all in the paper layer, all $0 deterministic PIL/numpy/cv2/ffmpeg, none of
them duplicating `panel_animator/` or the §5b scorecard.

---

## 1. Tide-Mark — the page keeps the water level

**What it does.** A real damp tide-line across the bottom of the *sheet* (not the drawing): a
wavering, never-straight boundary with a slightly darker, feathered ridge exactly at the edge
and faintly warmer, heavier paper below it — the stain a page gets from sitting in a puddle. It
**rises** as the fear rises, holds, and then **dries back** after the calm, leaving a permanent
faint ghost line — because paper never fully forgets a soaking. Later, on one beat, it returns
to its exact old high-water height.

**Why it fits.** This episode names the water level twice and means something different each
time: *"Water in the boat past your knees"* (3.15s, the storm) and *"when the water reaches
your knees, you don't trust the Christ in the boat"* (43.16s, **you**). That callback is the
narration's whole hinge, and right now nothing visual connects the two. Tide-Mark makes the
page itself the meter: the stain that rose on their boat rises again on yours, to the same
height, twenty seconds after it dried. The theme, the KJV callback, the fear-to-faith arc and
the physical medium all land on one mark.

**Technical approach.** $0 deterministic. Build the boundary once as a 1-D height field
(sum of 3-4 seeded sines + light smoothing — never a straight line, never a gauge). Per frame:
mask below the boundary, multiply the paper by ~0.94-0.97 warm-brown, add a 4-8px feathered
darker ridge at the boundary itself (classic stain physics — darkest where the water stopped),
then multiply that whole mask by the still's own paper-region mask so it never darkens the
drawn illustration. ~40 lines of numpy in `_s4_assemble.py`'s per-frame loop. The height is an
authored keyframe curve driven off the alignment word times.

**Where it goes.** Rises s01→s03 (0.0→6.7s); holds s04-s06; **frozen, untouched under the KJV
verse at s08** (the page does not editorialise under Scripture — that restraint is the device's
best manners); recedes s10→s11 (29.8→40.0s) to a faint permanent line; snaps back to full
height for ~1.2s on the word "knees," at 43.16s in s12; gone by the landing.

**Discipline.** No number, no gauge, no straight edge, never visible on more than 6 of 13
spreads, and never in the bottom 18% UI band's readable area as a hard line.

---

## 2. Wash-Creep — the paint has not dried yet

**What it does.** The dark storm washes stop being frozen. Their edges **creep**: pigment
advances a few pixels outward along the paper fibre with a feathered, slightly fingered front,
the way ink does on damp cold-press paper. Optionally one **backrun** — the pale cauliflower
bloom that forms when wet pigment pushes back into a drying wash. And then, after the rebuke,
the creep runs **backwards**: the storm wash retreats, the edge drying inward, cream paper
reclaiming what the ink had taken.

**Why it fits.** In s01 and s04 the storm is a single enormous charcoal-navy wash across the
top two-thirds of the sheet. It is the most *alive-looking* thing in the piece and it is the
only thing that never moves. Making it creep costs nothing and turns "a painting of a storm"
into "a storm still happening on this page." More importantly, the reverse is the miracle:
*"and there was a great calm"* (30.96s) is currently carried entirely by a hard cut between two
different generated stills. If the wash itself withdraws — visibly, in the medium — then the
sea obeying is something the *paper* does, not something the image model asserted. That is the
single most doctrinally-safe way to animate a miracle I know of.

**Technical approach.** $0. Isolate the storm wash by hue/value (HSV band on the blue-grey
range, morphological close, keep the largest components). `cv2.distanceTransform` outward from
that mask gives a distance field; perturb it with a low-frequency seeded noise field and
threshold at an advancing radius → a creeping, fibrous front. Feather 2-3px, composite the
wash's own sampled colour, respect the illustration's ruled border so it doesn't crawl onto the
kraft backing. Total advance is tiny — 6-15px over 2s. Backrun = the same trick with an
inverted threshold and a lighter tint. Related in family to `ink_transition`'s noise field but
a completely different application: that one wipes *between* two clips, this one deforms a
colour region *inside* one.

**Where it goes.** Advance on s01 (0.0-2.1s) and s04 (6.7-10.8s, the long held asleep beat).
Retreat across s10 (29.8-32.2s) into s11. Never on the verse spread.

---

## 3. Damp Cockle — the sheet will not lie flat

**What it does.** Paper that has been wet **cockles**: it waves and buckles, and under a raking
light the crests catch and the troughs shadow. During the storm the whole sheet has a slow,
heavy cockle rolling through it — the page is damp and unhappy. At the calm it presses flat and
stays flat.

**Why it fits.** Right now every spread is a perfectly flat rectangle, which is the one detail
that says "this is a JPEG" louder than anything else in the frame. This is also a *weather*
device with no weather in it: no invented rain, no added spray, nothing the image model has to
be trusted with — just a sheet of paper reacting to how wet the story is. And it gives the
storm→calm turn a second, tactile register beyond palette: the page relaxes.

**Technical approach.** $0, and distinct from `line_boil` (which is a whole-frame micro
translate/rotate). This is a spatially-varying warp with lighting: build a low-frequency 2-D
displacement field (two summed sines drifting in x and y at ~0.15Hz), `cv2.remap` the frame
through it at ±3-6px, then multiply by a shading term derived from the field's own gradient
(`1 + k·∂d/∂x`) so crests brighten and troughs darken by 2-4%. The lighting term is what makes
it read as paper rather than as a wobbly video. Amplitude is a per-episode curve: full during
s01-s06, tapering across s09→s10, zero from s11 on.

**Where it goes.** s01-s06 at full amplitude; decays through the rebuke; **flat from s10
onward** — the calm is a *flat sheet*, which is also why it must never be used on the landing.

---

## 4. Set-Off — the page remembers the question

**What it does.** Heavy ink pressed against a facing page leaves a **set-off**: a faint,
mirrored, absorbed impression of what was written opposite. At the landing, the Matthew 8:26
line that was scribed at 23.75s reappears on the blank upper half of the final page — mirrored,
pale, brown-ink, sunk into the fibre rather than sitting on top of it. No caption, no card, no
repetition: the words have simply come through from an earlier page.

**Why it fits.** This episode asks the same question twice — *"Why are ye fearful, O ye of
little faith?"* (KJV, 24.45s) and *"why are you afraid?"* (to you, 58.89s) — and the second
asking is the entire CTA. The letterer law rightly forbids type competing with the landing, so
the current cut lets the audio carry it alone. Set-Off threads the needle: it is not type, it
is a **stain**. It is illegible-as-reading and unmistakable-as-recognition. And it is the only
device I can design that makes the landing's blank cream upper half — which in s13 is a huge,
gorgeous, completely empty region above the tear — do work.

**Technical approach.** $0, and it reuses the exact raster `scribed_ink_card()` already
produces, so it is guaranteed to be the same handwriting. Mirror horizontally, desaturate
toward the paper's own brown (roughly `FADED_INK` at 12-18% alpha), blur ~1.2px, then multiply
the alpha by a fibre-noise field so it absorbs unevenly instead of appearing as a clean
watermark. Composite with a 2.5s ease-in over s13's blank upper page, above the tear, clear of
the watermark zone. Because it is a deterministic overlay of an already-rendered raster, it
never touches the never-animate-writing rule.

**Where it goes.** s13, fading in from ~53.5s (just after *"Come to the Christ who slept
unafraid"*), still there under the final question at 58.89s, holding through the ≥3.0s tail.

---

## 5. Still-Water Mirror — the sea gives the reflection back

**What it does.** On the calm spreads, the flat water gains a reflection that was never in the
still: mast, hull, standing figure, mirrored below the waterline in pale, horizontally rippled
ink — and the ripple **decays to nearly nothing** across the spread, so you watch the water go
still while you look at it.

**Why it fits.** *"There was a great calm."* Calm water is not defined by being flat; it is
defined by **reflecting**. A storm sea gives you nothing back; still water gives you the world.
s10 and s11 currently show flat blue washes with no reflection at all, which is exactly why
they read as "less stormy" rather than as "calm." This device makes the calm a positive
statement rather than an absence — and the settling ripple gives the assembler something honest
to do with s11's long 7.8s hold besides a push-in.

**Technical approach.** $0. Mask the water region (hue band + the horizon line, both stable in
these two stills), mirror the region above the waterline, squash vertically ~0.45, tint toward
the water wash, and apply a horizontal sinusoidal `cv2.remap` displacement whose amplitude
decays exponentially over the spread. Alpha ~0.2-0.3, clipped to the water mask, feathered at
the horizon. **Doctrinal check that must be honoured:** the repo already has a hard-won rule
that a reflected cross renders *upright*, not inverted (`feedback-cross-in-water-inverted`) —
so any reflection of a standing Christ figure gets a deliberate look before it ships, not an
automatic mirror.

**Where it goes.** s10 (29.79-32.20s) at high ripple; s11 (32.20-39.97s) settling to near-glass
under *"Exactly."*

---

## 6. Blue-Line — the drawing arrives

**What it does.** The spread begins as **underdrawing**: non-photo-blue construction lines,
loose graphite, wash blocked in pale — a page mid-way through being made. Then the ink arrives,
resolving the drawing along a soft diagonal front, as if a hand moved across the sheet. About
0.9s, once, and then it is a finished drawing like every other spread.

**Why it fits.** The format is called **living sketchbook** and it has never once shown a
drawing being made. The premise is asserted in the style block and nowhere in the footage. The
first second of a 9:16 short is the whole retention battle, and "an unfinished sketch finishing
itself" is a far stronger opening beat than "a nice illustration with a push-in" — it tells the
viewer what kind of thing they are watching before a single word lands. It also earns the aged
sheet, the ruled hairlines and the pencil grid that are already drawn into every still: those
are construction marks, and this is the only device that admits it.

**Technical approach.** $0, two plates from the one still. Underdrawing plate = luminance
lifted and desaturated, ink extracted via `cv2.adaptiveThreshold` / Sobel on the dark channel
and re-tinted toward ink-blue at low opacity, washes knocked back ~70%. Then wipe from
underdrawing to finished through a hand-wobbled diagonal mask (reuse the existing
`transition_mask` polyline generator, rotated) with a 60-90px feathered front. Careful
governor: it must resolve *fast* and never look like a filter — the pleasure is in the arrival,
not the effect.

**Where it goes.** s01 only, 0.0-0.9s (the hook), plus at most **one** other use per episode.
Two is a signature; four is a gimmick. For Storm, the second use — if any — is s08 under the
verse, so the KJV lands on a page finishing itself.

---

## 7. Held Breath — silence drives the page

**What it does.** Not an effect: a **pacing engine**. Every existing device in this project is
word-timed. This one is *gap*-timed. It reads the alignment for real silences ≥0.35s and, for
their exact duration, damps everything the page is doing — camera move eases toward zero, wash
creep pauses, cockle amplitude halves, grain-boil drops to a slow minimum. On the next word,
motion resumes. Silence becomes something you can see.

**Why it fits.** Look at where this narration's silences actually are:

| Gap | Length | Sits after |
|---|---|---|
| 9.21s | **1.64s** | *"And in the stern — He is asleep."* |
| 17.10s | 1.27s | *"...the very thing that is killing them."* |
| 20.72s | 1.23s | *"...that He could possibly sleep through this."* |
| 31.24s | 0.96s | *"...and there was a great calm."* |
| 34.40s | 0.85s | before *"Exactly."* |

The longest silence in the entire piece is the one **immediately after "He is asleep"** — the
episode's thesis, and the writer already left a hole there. Right now the page keeps fidgeting
straight through it. A device that makes the page go quiet exactly where the narrator does
turns those five gaps into five free dramatic beats, at $0, on every future episode
automatically.

**Technical approach.** $0. Parse `_storm_alignment.json` once into a per-frame `energy(t)`
envelope: 1.0 during speech, easing to a floor of ~0.25 across the middle of any gap ≥0.35s,
with 0.15s ramps so nothing snaps. Every other device multiplies its amplitude by `energy(t)`.
**One honest conflict to flag:** the repo's own rule says a fully-still hold must keep
grain-boil or it reads frozen (and the ArkAIology freeze-audit finding backs that up
empirically) — so this is a *decay to a floor*, never a true freeze. The page inhales; it does
not die.

**Where it goes.** Global, all 13 spreads, with the deepest damping allowed at 9.21s (post
"asleep") and 34.40s (before "Exactly.").

---

## 8. Raking Light — the lamp moves, not the camera

**What it does.** The style block already asks for "soft raking museum light." This makes the
light **move**: a broad, slow directional grazing sweep across the sheet that catches the paper
tooth, deepens the shadow inside the torn edge, and — on one beat only — passes across the
gold-leaf strip at the right margin so it **flares**, the way real leaf does when the light
finds it.

**Why it fits.** It is the difference between "an image on screen" and "a physical artefact
being filmed," applied to every spread for free, and it is the one device that gives the show a
camera-less way to move. And the gold flare has a job: palette theology says **gold is His
glory only**, so the strip is allowed to ignite exactly once — as the light crosses the page on
*"and there was a great calm"* (30.96s). The glory beat lights the gold; nothing else does.

**Technical approach.** $0. High-pass the still's own luminance to approximate paper tooth
(no normal map needed), then per frame modulate brightness by `1 + k·highpass·dot(sweep_dir)`
where the sweep is a wide soft gradient translating across the frame over 2-4s. Gold flare =
isolate the leaf strip by hue, add a short specular bump with a slight bloom as the sweep
crosses it. Keep `k` small (2-5%) — overcooked relighting is the one way this reads as CG
rather than as a lamp.

**Where it goes.** A slow sweep on s05 (10.84-18.36s, the long held "nothing to fear" beat that
currently has the least to look at), and **the gold flare on s10** at 30.96s. Nowhere else —
one flare per episode.

---

## Considered, and deliberately cut

- **Tear-Line** (the torn page opening progressively from the rebuke onward, finishing at the
  landing). Genuinely lovely, but the torn page is the show's landing device and its most
  sacred gesture. Spending it early — even gradually — cheapens the one image the format has
  reserved for Christ. Same reasoning the skill uses for Illuminated Rubric: some registers are
  worth more unspent.
- **Line-tremor keyed to fear** (only the ink linework shakes, amplitude decaying to zero at
  the calm). Too close to `line_boil` with a story justification bolted on, and the frightened-
  hand reading is a hair away from cartoon.
- **Struck-page / jolt on the thunder hits.** Camera shake is the definition of the "gimmicky"
  this format's taste explicitly rejects. `impact_burst` already covers real points of contact,
  and this episode has none.

---

## If I could only build three

**1. Tide-Mark.** The only one of the eight that is *about something*. It carries the
narration's actual hinge (their knees → your knees), the fear-to-faith arc, the callback, and
the page-as-object idea in a single mark, and it costs about forty lines of numpy. It is also
the most reusable idea here in disguise: "let the paper keep score of the episode's own stated
stake" generalises to almost every future piece — a scorch line, a fold, a crease that deepens.

**2. Wash-Creep.** The highest ratio of felt-magic to risk in the list. It makes the storm
alive without asking any model to animate water, and its reverse is the safest possible way to
render a miracle — the sea obeys because the *paint* obeys, and no generated frame gets a
chance to invent anything. On a water episode this is the device the medium was waiting for.

**3. Held Breath.** Not the flashiest, and that is the point: it is infrastructure. Build it
once, and every device above — plus every device already in the toolkit — gets dramatic timing
for free, on every episode, forever. Given that the largest silence in this narration sits
directly on the episode's thesis line and is currently being wasted, this is the cheapest real
upgrade available to the *cut* rather than to the *frame*.

Runner-up, if a fourth is cheap: **Set-Off**, because the landing is the one beat that
currently carries no visual idea at all, and it needs about fifteen lines of code on a raster
that already exists.

All eight are $0. None of them touches the generated layer, so none of them can reintroduce any
defect class in SKILL.md §8a. Every one of them should still be looked at on a real frame before
it is called done.
