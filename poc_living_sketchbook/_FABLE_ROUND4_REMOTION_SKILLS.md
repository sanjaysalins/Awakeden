# Fable — round 4: what Remotion actually has left to teach this series

**Date:** 2026-07-30 · **The question:** which great Remotion animation skills from ArkAIology
could this series adapt? · **Sources verified by reading the real files:** `remotion-overlays/src/components/*.tsx`
(20 components), `KineticWord.tsx` all six voices, `TransitionReveal.tsx`, `BarChartCard.tsx`,
`LineChartCard.tsx`, `vox-map/src/broadcast/` (camera.ts, VoxMapBroadcast.tsx, Beats.tsx),
`vox-map/_legacy_flyover/README.md`, vox-motion's SKILL.md `deterministic_clip` section, this
repo's `_remotion/src/Trailer.tsx`, `storm/_s4_assemble.py` (TRANSITIONS + transition_mask +
grain), `panel_animator/parallax_25d.py`, and `.claude/skills/map/SKILL.md`.

**Read first:** `_FABLE_ROUND3_SERIES_SKILLS.md` (round 3, the format this follows),
`_SKILL_ADAPTATIONS_REVIEW.html` (round 1 scorecard — 11 items already mined).

---

## The finding that reframes the whole question

Only three ArkAIology skills are genuinely Remotion — vox-motion, vox-type, vox-map. I went
looking for the thing among them that PIL/cv2/ffmpeg structurally cannot do, because that is
the only honest justification for path (b) and a second render engine. Here is what I found,
in the source, not in anyone's summary:

**The one true path-(b) candidate is already dead — killed by its own project.** vox-map's
package.json carries `three@0.169` + `@react-three/fiber` + `@remotion/three`, and the research
framing called it "a REAL 3D engine." But the live compositions (`VoxMapBroadcast.tsx`,
`VoxMapExile.tsx`, all of `src/broadcast/`) contain **zero three.js** — they are d3-geo
projections onto a flat SVG plate, moved by a keyframed 2D pan/zoom camera. The actual 3D
terrain flyover lives in `_legacy_flyover/`, whose README opens: *"DEPRECATED — v1 terrain
flyover (do not use). Archived 2026-07-25 by user decision... It worked... but it is the
fragile path: WebGL determinism gotchas... slower renders, and every new region needs a new AI
plate + heightmap (credits)... keeping two engines live meant the wrong one would eventually
get used by mistake."*

Sit with the date. **2026-07-25 is the same day this repo killed `_remotion/`.** Two sibling
projects, independently, on the same day, paid the two-engines tax and retreated from it. And
ArkAIology's retreat was *within* Remotion — even they concluded the 2D plate camera delivers
the felt experience of the flyover without the fragile half of the stack.

**Does true 3D matter for a living-sketchbook map anyway?** The brief asked me to judge this
honestly, so: the difference is real and *felt* — an orbiting, tilting camera over displaced
terrain is something a flat pan genuinely is not. But for this show it points the **wrong
way**. Our map is ink on cold-press paper on a desk. The native motion of that object is a
reader's eye traveling over it — which is exactly what a 2D glide-and-zoom looks like. A
terrain orbit would read as CGI erupting out of a drawing: the same-hand test failed at the
technology layer instead of the texture layer. The flap lesson again, one level down. And if a
map hero still ever genuinely wants depth, `panel_animator/parallax_25d.py` (rembg layer-drift
over the base plate) already approximates it at $0, in-idiom.

**What survives in ArkAIology's Remotion stack today is deterministic 2D math over layers** —
springs (a closed-form damped oscillator), dash-offset draw-ons, seeded-noise masks, keyframed
affine cameras. That is precisely the category `panel_animator/` reimplements at $0. So every
proposal below routes (a), there are **zero (b) routes**, and I do not recommend reviving
`_remotion/` — grounded in reading `Trailer.tsx` itself, not just the fact of its death. It is
real, competent work (38 seconds, a 34-cell clip score, spring slams with red keyword bleeds,
and one genuinely elegant trick: a global noir-to-color bloom crossfaded frame-accurately
across every simultaneously-playing cell at the veil-tear frame). But that one trick is
per-frame blending between two graded frame sets — the Storm assembler already does per-frame
composites over extracted frames as its ordinary mode of existence. Nothing in that file needs
React. The style it served is dead by lock, and the pipeline can stay dead with it.

Two smaller verifications the brief asked for, answered plainly:

- **Ghost and lowerThird are explicitly claimed.** Round 1's review headers literally read
  "ADOPT — Ghost" ("word pressed into wet paper") and "ADOPT — lowerThird" (chapter/act title
  card). Five of KineticWord's six voices are accounted for. **`circled` is the only unclaimed
  vox-type voice** — it becomes proposal 2.
- **The liveness trick is redundant.** vox-motion's `deterministic_clip` rule re-seats a noise
  texture per frame at opacity 0.12, NORMAL blend, calibrated to ~0.008 MAFD against
  `freezedetect n=0.0015` (their SKILL.md even warns soft-light damps the delta 16×). Our
  `_s4_assemble.py` cycles 8 seeded noise layers every frame, lightening speckle where noise
  exceeds threshold — same defense, already shipped. The one transplantable organ is the
  *calibration habit*: measure the MAFD your liveness layer actually produces against the named
  detector. That's one line folded into round 3's Light Table spec, not a skill.

Three proposals below, ranked by confidence. All path (a). All $0.

---

## 1. Voyage Camera — the map learns to travel · **CONFIDENCE: HIGH**

**Inspired by:** `vox-map/src/broadcast/camera.ts` — the `cameraAt()` keyframe system — and
`VoxMapBroadcast.tsx`'s camera score. Three specific techniques, each named in the source:
**log-space zoom interpolation** (`Math.exp(Math.log(a.k) + (Math.log(b.k) - Math.log(a.k)) * p)`
— equal-*feeling* zoom speed at every scale, the difference between broadcast and slideshow),
**smootherstep-eased keyframes** (wide → push to a place → hold → glide to the next → wide
outro), and the score discipline in the file's own comment: *"every move leads its beat by
~10f"* — the camera arrives just before the content does, so the viewer's eye is already
parked where the payoff lands.

**The pitch.** This series already owns its answer to "a Bible map that moves" — `/map`'s
mapengine: inked seedream base, progressively-drawn route, walking caravan, label pop-ins,
Red Sea parting. What it does not own is a camera. `config.camera_zoom` is a single 0.05
push-in; the viewer watches the whole journey from the ceiling. The Voyage Camera gives
route.json a `camera` block — a keyframe list of (time, center-on-waypoint, zoom) — rendered
as a per-frame affine crop over the composed map. Wide establishes the world; the camera
glides down to Rameses as the caravan sets out; travels *with* the route head across the
wilderness; pulls wide for the sea; arrives at Canaan ten frames before the label pops. The
same $0 clip stops being a diagram and becomes a journey.

**The translation.** Nothing to re-skin — the fiction improves on its own: a keyframed 2D
glide over paper IS what looking at a real map does, which is exactly why the deprecated 3D
flyover would have broken it. Port the three techniques whole: log-space zoom (numpy one-liner),
smootherstep easing (mapengine already eases), move-leads-beat-by-10-frames as a scheduling
rule tied to the route-draw head and label times mapengine already computes. vox-map's
constant micro-drift (`7·sin(f/53), 5·cos(f/71)`) ports at reduced amplitude as the reader's
hand holding the page — though grain-boil already guards the freeze-audit side.

**One real implementation note (still $0, just CPU):** a zooming camera needs headroom —
compose the map layers at ~2.2× supersample once, then crop per camera pose, or zoomed-in
frames go soft. That is the entire technical risk of this proposal.

**Cost:** $0 beyond the base map's existing ~$0.30 seedream render. Pure PIL/cv2 crops.

**The moment.** Storm is itself a crossing — "let us pass over unto the other side" — and a
four-second Voyage beat (Capernaum, the glide across Galilee, the far country) is the map beat
that episode never had. But the real test targets are the journey episodes the brief names:
**Exodus** (Rameses → Red Sea → Sinai, the parting beat finally seen close instead of from
orbit) and **Acts 27, Paul's voyage to Rome** — a journey episode that is *also* a storm
episode, where this camera and the entire round-2 paper-layer storm kit (tide-mark, damp-cockle,
wash-creep) would fire on the same spreads for the first time.

**Structurally safe because:** the render is fully deterministic — no generative layer exists
anywhere in mapengine, so there is nothing to hallucinate; waypoints and labels stay
human-authored through /map's existing Read-the-image QC loop; the camera can only frame what
the approved map already contains.

---

## 2. Annotator's Circle — the hand that marks the Word · **CONFIDENCE: MEDIUM-HIGH**

**Inspired by:** `KineticWord.tsx`'s `Circled` treatment — the one vox-type voice round 1
never touched. Two techniques worth naming precisely: the **two-pass dash-offset draw-on**
(`draw1` sweeps an ellipse over ~22 frames, then `draw2` traces a second, lighter,
slightly-offset pass overlapping the first — because a real hand circling something important
goes around twice), and the discipline that the circled word sits **full-ink bold amid faded
body text** — emphasis carried by ink weight and gesture, never by a UI highlight.

**The pitch.** When the narration lands on one word inside a verse already on the page — and
the alignment JSON knows the instant that word is spoken — a rubric-red ellipse hand-draws
itself around that word on the existing Scribed Ink card, wobbled by the same seeded math as
MarkerCircle's absorbed technique and the map arc's chevrons, in two passes, the second
lighter. Gold instead of rubric if and only if the circled word IS the glory beat (Scribe's
Tally's color law, reused verbatim). This is marginalia — the single oldest annotation gesture
in the history of reading, found in real hands in real centuries-old Bibles — and it is the
one "look here" the series does not yet own: §6's hunt_and_lock camera looks closer at the
*drawing*; nothing yet lets the reader's hand respond to the *text*.

**Why this isn't the Plate Loupe dying twice, and isn't Scribe's Tally either.** The Loupe
died because a bordered inset is picture-in-picture — a borrowed broadcast structure. A circle
drawn on the page has no frame, no window, no second surface: it is a mark, in the page's own
ink family. And Tally *counts* (accumulation of strokes); the Circle *points* (a single
gesture of emphasis). Shared wobble math is not redundancy — it is the same-hand argument
working as designed.

**Governors (load-bearing):** at most ONE circle per episode. Only on a word inside verbatim
KJV (or a map label) already approved on the page — the device cannot add text, only mark it.
Never on the landing spread's set-off (that register is quiet by law). And one reverence
question goes to the user, not resolved silently: red ink on the Word may read as the reader's
hand honoring it (the marginalia tradition) or as defacing it — if it fails by eye, the
fallback placement is circling a word in the narrator's own lettering instead, and the KJV
stays unmarked.

**Cost:** $0 — progressive PIL ellipse, word-timed off the alignment like every lettering
device.

**The Storm moment.** The Matthew 8:26 card holds the screen 23.75–27.10s: *"Why are ye
fearful, O ye of little faith?"* The whole episode is fear against faith. As the narrator
speaks "faith," the circle draws around it — first pass, then the confirming second — and the
episode's question is suddenly in the reader's handwriting, not just the scribe's.

**Structurally safe because:** it is a deterministic overlay that can only point at words
already gated onto the page; it cannot assert, quote, or add; and the choice of *which* word
follows the narration's own emphasis, reviewed like any overlay in the same doctrine passes.

---

## 3. Measuring Reed — the magnitude that earns itself · **CONFIDENCE: MEDIUM**

**Inspired by:** `BarChartCard.tsx` and `LineChartCard.tsx` — but by their one structural
idea, not their bodies. BarChartCard grows each bar from the baseline with a staggered spring
(`local - 10 - i * BAR_STAGGER_FRAMES`) so the quantity is *watched into existence*;
LineChartCard draws its path by SVG dash-offset with each dot popping the instant the
draw-front reaches it. The shared organ: **a value the viewer watches being earned, never a
number asserted by a caption.** (CountUpNumeral's arrival was already absorbed into round 3's
Scribe's Tally; this is the draw-on's turn.)

**The pitch.** The charts themselves die on sight — axes, bars, value chips, and a card are
the flap lesson at dashboard scale, and the diagram/stat sockets are already owned by
infographic-panel and typography-panel besides. What survives is this: when Scripture states
a *magnitude*, a hand-ruled measured span extends across the open paper — the line drawing
itself to length (the dash-offset, in wobbled iron-gall ink), cubit tick strokes arriving one
by one as the front passes them (the stagger, in Tally's own stroke vocabulary), and the
numeral + unit arriving in Scribed Ink only when the span completes. The Bible even names the
instrument: *"a measuring reed of six cubits"* (Ezekiel 40:5) — the device is period because
it is scriptural.

**Discipline (the payoff-ledger honesty rule, extended):** only magnitudes the text states
verbatim get a reed — the ark's three hundred cubits (Gen 6:15), Goliath's six cubits and a
span (1 Sam 17:4), Ezekiel's reed itself, the city measured in Revelation 21:16. A
side-by-side comparison of two spans (drawn to the same scale — the honest version of
BarChartCard's whole reason to exist) is allowed only when BOTH magnitudes are stated: the
ark's length against its breadth against its height, all from one verse. A magnitude the text
doesn't state doesn't get drawn. And ≤1 reed sequence per episode.

**Cost:** $0 — deterministic PIL, the same progressive-draw machinery as Tally and the map
route.

**The moment.** Storm states no magnitude — this device sits the episode out, exactly as
Scribe's Tally did, and saying so is the honest answer. The worked moment is the **Noah
material already in this repo's orbit** (the cast-bible taste piece is Noah): three hundred
cubits ruling itself across a full spread beneath the hull, tick by tick, the number arriving
last — the size of the thing felt before it is stated. Future: Goliath's span drawn beside a
sling left unmeasured; Revelation's city, measured with a golden reed by the text's own angel.

**Structurally safe because:** the only content it carries is an integer and a unit, and the
rule above makes both Scripture-verbatim or absent; deterministic paper-layer overlay under
round 2's governors; it cannot depict, only measure.

---

## Considered, and deliberately skipped

- **Any path (b) — reviving `_remotion/` or building fresh compositions in it.** The full
  argument is the opening section. Shortest form: the one capability that would have justified
  React (true 3D flyover) was deprecated by its own project for the exact second-engine
  reasons this repo named on the same calendar day; everything Remotion still does in
  ArkAIology is deterministic 2D math this stack already speaks natively; and `Trailer.tsx`'s
  single elegant trick (the frame-accurate global bloom) is ordinary per-frame blending here.
  Zero proposals route (b). The `_remotion/out/` MP4s stay what they are — a well-made grave.
- **TransitionReveal (paperRip / halftone / inkSwipe).** Verified against the real assembler:
  `_s4_assemble.py` already owns a seeded jagged-polygon paperRip (`TRANSITIONS` +
  `transition_mask()`), and the `/ink-transition` skill already owns the organic ink-wipe.
  Halftone-dissolve is a printing-press idiom that belongs to `/print-grade`'s finishing pass,
  not to a hand-inked page's scene changes. One free polish note, not a proposal:
  TransitionReveal leads its tear with a deckled white fringe (a second clip-path offset
  ~16px ahead of the reveal edge) — a five-line addition to `transition_mask()` if the
  existing rip ever reads too clean. Noted for whoever next touches the assembler.
- **The `deterministic_clip` liveness noise.** Functionally redundant with grain-boil —
  verified in both sources, details in the opening section. The calibration habit (measure
  your MAFD against the named detector) folds into Light Table's spec as one line.
- **Ghost and lowerThird.** Explicitly claimed in round 1 under their own names. Checked so
  nobody re-proposes them under new branding — the exact failure this round was briefed to
  avoid.
- **BarChartCard / LineChartCard as charts.** Axes-and-bars is the grid-of-cells anachronism
  at full-frame scale; infographic-panel and typography-panel already own the
  diagram-that-looks-like-our-art socket. The one surviving organ became the Measuring Reed.
- **PING / SPOTLIGHT / BARS-3D as standalone beats** (`Beats.tsx`). PING's expanding rings
  are radar HUD — a borrowed structure no wobble will save. Its narrative job (a place
  announces itself) is already mapengine's label pop-in, completed by the Voyage Camera's
  arrive-and-hold; SPOTLIGHT's static re-skin was round 1's ANCIENT REGION, and its motion
  version is just a Voyage Camera framing move; BARS-3D is charts standing on a map — skip
  per the entry above.
- **Remotion's `spring()` itself.** A closed-form damped oscillator, ~15 lines of numpy. Not
  a skill — a shared easing upgrade *inside* existing devices, worth adopting the next time
  the Ink Stamp or typography-panel pop should overshoot like a real object instead of easing
  like a tween. Polish note, same bin as the deckled fringe.

---

## If I could only build one

**Voyage Camera.** The other two decorate episodes; this one unlocks an episode *class*. The
journey stories — Exodus, Abraham's call, the wilderness, Paul to Rome — are structurally
underserved by a locked-camera sketchbook, and this proposal upgrades an already-locked, $0,
zero-hallucination asset (/map) rather than adding a new device that needs a governor. It is
also the cleanest possible answer to this round's actual question: the best thing Remotion
had to teach was never React — it was a camera score. Keyframes, log zoom, and arriving ten
frames early are ideas, and ideas port for free.

If two: add **Annotator's Circle** — the last unclaimed vox-type voice, the cheapest build
(Tally's wobble drawing a closed curve), and the only proposal with a Storm moment ready
tonight. The Measuring Reed waits, without complaint, for Noah.

All three are $0, deterministic, and never touch the generated layer — the Voyage Camera has
no generated layer to touch, and the Circle and the Reed live on the paper layer under round
2's standing governors. Nothing here can grow a fourth disciple, and nothing here needs
node_modules to move a page.
