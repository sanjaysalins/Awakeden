# Fable — round 5: the book itself

**Date:** 2026-07-30 · **Reacting to:** `STORM_living_sketchbook.mp4` v5, watched fresh this
session (frames pulled at 7s intervals and eyeballed at full context — the collage edges, the
gold strip, the Scribed Ink verse card at 23.75s, the set-off ghost on the landing, the torn
page with Christ in gold light). · **The mine status, verified:** ArkAIology's skills folder
contains exactly 17 skills — cast-bible, higgsfield-video-explainer, mixed-media-explainer,
payoff-ledger, produce-episode, red-team, retention-review, shorts-factory, sound-design,
threads, thumbnail-forge, vox-3d, vox-blend, vox-flat, vox-map, vox-motion, vox-type — and
every one is accounted for across rounds 1–4 (adopted, translated, or skipped with reasons).
**The mine is empty.** This round therefore does what a round has never had to do: design from
the film and the fiction alone, held to the same laws the mined rounds obeyed.

> **BUILD STATUS (same day):** all five built and machine-tested. Engines:
> `panel_animator/{elder_leaf,papermakers_mark,ribbon_marker,frottage}.py` (+ the Second
> Sitting prototype `poc_living_sketchbook/storm/_second_sitting_ab.py`); skills registered
> under `.claude/skills/{elder-leaf,papermakers-mark,ribbon-marker,frottage}/`. Demos +
> honest flags: `poc_living_sketchbook/storm/_round5_demos/_ROUND5_REVIEW.html`. Pending the
> USER's eye: all five demos, the ribbon-vs-stillness A/B, the Second Sitting A/B, and the
> ichthys-vs-cross symbol decision. One build finding worth recording: a 550px-FWHM sweep
> band's Gaussian tail never fully leaves a 1080px frame — `apply_papermakers_mark` now
> truncates the envelope to EXACT zero below 10% band value so "invisible at rest" is
> mathematically true at any placement (the self-test probes at ±3.2σ in projection space,
> not at hardcoded sweep endpoints).

**Read first:** `_FABLE_ROUND3_SERIES_SKILLS.md` and `_FABLE_ROUND4_REMOTION_SKILLS.md` (the
format and the standing skips), `_STORM_REVIEW.html` (v5 section), `.claude/skills/living-sketchbook/SKILL.md`
§1/§3/§7, and one built device for house engine format: `.claude/skills/tide-mark/SKILL.md` +
`panel_animator/tide_mark.py`.

**Queue honesty, stated up front:** rounds 3–4 designed ten skills; three are built
(margin-sentinel, scriptorium-foley, concordance-loom) and seven are designed-but-unbuilt
(Scribe's Tally, Frontispiece, Light Table, Unmade Page, Voyage Camera, Annotator's Circle,
Measuring Reed). A new round must not be a backlog inflator. My own ranking across BOTH piles
is at the end — some of this round outranks some of that queue, and some of it doesn't, and
I say which.

---

## The creative take

Rounds 1–4 each answered one question. Round 1: what may the page *say* (the lettering
voices). Round 2: what may the page *do* (eight physical behaviours of paper and wash).
Round 3: what *guards* the film and *serves the thesis* (the Sentinel, the Foley, the Loom).
Round 4: what *instruments* does the hand hold (the map camera, the circle, the reed).

Watch v5 knowing all of that, and the remaining absence is structural, not decorative:

**every device so far treats the page as if it were the only page in the world.**

But the fiction — the one this show is named for — is a *sketchbook*. A book. And a book is
three things no round has touched:

1. **A substrate with a maker.** The paper existed before the first ink touched it. Real
   cold-press sheets carry the papermaker's watermark — a wire device pressed into the pulp,
   invisible until light finds it. Our page has no mark in it. Nothing under the ink.
2. **Other leaves.** A sketchbook has pages before this one — older material, pasted-in
   documents, the antiquarian's habit of tipping an ancestor's leaf into his own book. Our
   series' first non-negotiable is "the whole Bible, through Jesus," round 3 built the Loom
   to *find* the Old Testament echoes deterministically — and the page still has no way to
   *show* one as what it is: an older witness, physically present.
3. **A reader who returns.** Every episode ends with a CTA to Jesus, spoken. The book's own
   language for "come back to this" has existed for a thousand years: a ribbon laid in the
   page. We close every episode without marking the place.

Five proposals below, ranked by confidence. All five are about the book as an object — the
substrate, the elder leaves, the ribbon, the world pressed into the pages, the book in time.
All five are $0 per run (two need a one-time banked texture, quoted). All five live on the
deterministic paper layer under round 2's standing governors — none can touch the generated
drawing, none can grow a fourth disciple. Each carries a **build card** so a Sonnet session
can implement the engine and the SKILL.md without me; the built engine goes through the same
chain as round 2's: self-test → demo clip → user eye → only then a `.claude/skills/` entry.

---

## 1. The Papermaker's Mark — Christ in the substrate · **CONFIDENCE: HIGH**

**The pitch.** A watermark IN the paper — a wire-form line device (my proposal: the ichthys,
the earliest Christian mark, a two-stroke fish any wire could bend; the plain cross is the
alternative) — that is **invisible at rest** and appears ONLY while raking-light's sweep
crosses it: the paper thins where the wire pressed, the lamp finds it, the strokes glow
faintly lighter for a moment, and the sweep moves on. The theology is the whole device: *the
mark was in the paper before anything was drawn on it.* Every story this series will ever
tell is drawn on a sheet that already carried His sign — which is precisely what "the whole
Bible, through Jesus" claims about the text itself. The torn-page landing says "Christ
beneath the page" at full volume; the watermark says it in a whisper, forty seconds earlier,
to the viewers who are looking closely. It is the quietest device this show will own, and
the one most likely to be discovered on a second watch — a gift to the rewatcher, which is
also, not incidentally, a retention mechanic.

**The fiction check (same-hand test).** Papermakers' watermarks are real, period-plausible
for the sketchbook object (chain-lines-and-device marks are as old as European paper), and
*already implied* by the cold-press fiction the style block asserts. This isn't adding a
prop; it's admitting the paper was made by someone.

**Why it composes instead of adding a slot.** It has no reveal mechanism of its own and
never will — the raking-light sweep (round 2, built, shipped in v5) is its ONLY trigger.
No sweep, no mark. It upgrades an existing device's payload rather than competing for a new
overlay beat, so the overlay governor budget is untouched.

**Governors (load-bearing):**
- ≤1 reveal per episode. The mark's position sits in blank margin (quiet-mask territory),
  never over drawing, never over lettering.
- Never during the KJV verse hold — the verse owns its moment (§7's law extends here).
- The symbol is **series-constant and a user decision, not mine** — ichthys vs cross is a
  reverence call. Decided once, then it is the same wire in every sheet, forever: the series'
  second ident (blue-line's stroke opens the show; the Mark hides inside it).
- Strength cap ~0.12 lighten at sweep peak; at rest, mathematically zero.

**Cost:** $0 — a 1-bit line-art PNG (drawn deterministically or once by hand) + per-frame
masked lighten in the existing raking-light pass.

**The Storm moment.** s05 — *"he was asleep."* The longest, quietest hold in the piece,
the spread round 2 chose for raking-light precisely because it had the least to look at.
The lamp sweeps the sleeping Christ's spread, and for two seconds the paper itself confesses
the fish. Power present, hidden, in the boat; the mark present, hidden, in the sheet. The
device and the doctrine are the same sentence.

**Structurally safe because:** deterministic luminance modulation inside an existing pass;
composited after the Margin Sentinel's raw-clip scan by the standing order-of-operations
(Sentinel scans RAW clips; paper devices composite later), so the tripwire never fires on it;
and it can only lighten pixels along a fixed, user-approved line form — it cannot depict,
assert, or add.

**Build card (Sonnet):**
- Engine: `panel_animator/papermakers_mark.py`.
- `apply_papermakers_mark(frame_bgr, sweep_center_frac, mark_mask, mark_center_frac,
  strength=0.10, band_frac=0.22)` — called per-frame inside the raking-light pass, sharing
  its `sweep_center_frac`. Visibility envelope = the sweep band's own falloff evaluated at
  the mark's position (so the mark fades in/out exactly as the light crosses — never its own
  animation curve).
- `mark_mask`: line-art PNG → Gaussian-soften ~2px → normalized float mask. Provide
  `make_ichthys_mask(w, h, seed)` drawing the two-arc fish with the house seeded wobble
  (MarkerCircle's math) so even the wire is hand-bent.
- Self-test: render 3 frames (sweep far / sweep on-mark / sweep past) from one Storm still;
  assert mark-region mean-delta ≈ 0 in frames 1 and 3, > threshold in frame 2. Then a demo
  clip for the eye.
- QC by eye at full res: visible when you know where to look, missable when you don't.
  If it pops as an "effect," halve the strength before touching anything else.

---

## 2. The Elder Leaf — the Old Testament, physically present · **CONFIDENCE: HIGH**

**The pitch.** When an episode cites its Old Testament echo, the citation arrives as an
**older leaf tipped into the sketchbook**: a smaller sheet of visibly older stock — darker,
foxed, deckle-edged — laid onto the spread with linen-tape corners, settling with a soft
lay-down, carrying the OT verse in an elder register of the existing lettering (faded
iron-gall brown, the same scribe's hand aged), reference stamped in the same rubric red.
The gold thread — round 1's thread device — runs from the elder leaf to the Christ-element
on the present page. The series' thesis finally has a *visual grammar*: New Testament events
are drawn on the book's own cream; the Old Testament witnesses to them as an older document,
physically present, connected by gold. Tipping ancestral leaves into one's own book is
exactly what a real antiquarian's sketchbook does — the fiction was already waiting for this.

**The pairing that makes it infrastructure.** Round 3's Concordance Loom (built) *finds*
echo candidates deterministically; the qualification test and the panel *judge* them; the
Elder Leaf is *how the page cites the ones that pass*. Finder → judge → citation. Storm
shipped without Psalm 107:29 because the finding failed; from now on, when the finding
succeeds, the showing is a solved problem too.

**The reverence question, flagged, not resolved silently:** older paper must never read as
*lesser* paper — OT-as-obsolete would be a doctrinal error rendered in texture. The
mitigations are in the governors: the elder leaf is aged but IMMACULATE — never torn, never
stained, never damaged beyond its years; it is taped in with visible care (a treasured
ancestor, not a scrap); and the gold thread always runs FROM it — the elder leaf is the
root, not the relic. If the first render reads as "old junk pasted on," the stock gets
rebanked before the device ships. User judges by eye.

**Governors:**
- Only verses that came through the Loom + qualification test (or a hand-verified classic
  echo); KJV verbatim + reference, always; the standing letterer laws apply on the leaf.
- ≤1 elder leaf per episode. It lands on the spread the echo serves, never on the landing
  spread (the torn page's register stays uncontested).
- The leaf never covers a face or the spread's subject; placement planned against the real
  still like every overlay.

**Cost:** $0 per use. One-time: 2–3 banked elder-stock textures with deckled-edge alpha
(`poc_living_sketchbook/world/elder_stock_*.png`) — one seedream texture render (~2cr) or a
scan, then banked forever. Linen-tape corners drawn deterministically (PIL: warm translucent
strip + edge noise).

**The Storm moment — the sting, redeemed.** Round 3's most embarrassing finding was that
Storm shipped with no OT echo while Psalm 107:29 — *"He maketh the storm a calm, so that
the waves thereof are still"* — sat unfound. The Elder Leaf is that verse arriving on the
great-calm spread (the s10–s11 stretch, where the sea has just gone glass): an older sheet
settling beside the stilled water, the psalmist's line in faded brown, the gold thread
running from "maketh the storm a calm" down to the Christ who just did. The episode's one
missing beat, in the device built to carry every such beat from now on.

**Structurally safe because:** every pixel is deterministic composition of approved
material — banked stock, existing lettering renderers with a color/fade parameter, the
existing thread device; the only content it can carry is a verbatim KJV verse that already
passed the doctrine chain.

**Build card (Sonnet):**
- Engine: `panel_animator/elder_leaf.py`.
- `compose_elder_leaf(verse_text, ref, stock_png, angle_deg=-2.5, age=0.7) -> leaf_rgba` —
  renders the verse via the EXISTING Scribed Ink / Typeset renderers (copy the
  `render_scribed_ink()` pattern from `_lettering_compare/_render_candidates.py`, including
  the punctuation-scaling gotcha) with an `ink_rgb` + `fade` parameter. Do NOT build a new
  letterer.
- `settle_frames(leaf_rgba, t, t0, dur=0.5)` — lay-down: scale 1.035→1.0 smootherstep,
  contact shadow blur 18px→6px and offset shrinking, then perfectly still. Export the
  settle window to the Foley cue list (`paper_lay` cue) — scriptorium_foley picks it up
  for free.
- Gold thread: call the existing thread renderer, endpoint on the leaf's emphasis phrase,
  endpoint on the present-page Christ element.
- Self-test: compose one leaf over a Storm still, render a 3s demo, check by eye at full
  res: stock reads OLD not DIRTY; verse legible at video size; tape reads as tape.

---

## 3. The Ribbon Marker — the CTA in the book's own language · **CONFIDENCE: MEDIUM-HIGH**

**The pitch.** At the landing, after the last spoken word, a narrow woven ribbon — rubric
red, slightly frayed at the tip — slips down from the top edge and settles across the
margin of the landing spread, the way a reader marks the page they intend to return to.
One soft cloth-settle, one contact shadow, then absolute stillness through the ≥3.0s hold.
The spoken CTA says *come to Jesus*; the book's own gesture says *this is the page you will
want again.* Blue-line's ink-arrival opens every episode as the series' ident; the ribbon
closes it — the show gains matching bookends, the pen and the ribbon, episode after episode,
forever. And a marked page is a quiet promise of seriality: this book has more pages, and
we will be back in it.

**The honest conflict (goes to the user, by A/B, not resolved by me):** §3's landing law is
sacred stillness — "glow breathes only." A ribbon settling *during* the hold is motion where
the law says none. My proposed timing keeps the letter of it: the settle completes within
~0.6s of the last word, BEFORE the 3.0s stillness clock starts (INV-26 measures hold after
final audio; the settle rides the word's own tail), then contributes zero motion. But
whether even that reads as an intrusion on the torn page's moment is exactly the kind of
call the A/B exists for: landing with ribbon vs landing straight, judged by eye. If it
loses, it dies — or retreats to the very last second before the endcard, as the book's
goodbye rather than the landing's punctuation.

**Governors:**
- Landing spread only; by definition once per episode.
- Rubric red ONLY — gold is His glory, and the ribbon is the *reader's* object; a gold
  ribbon would claim the wrong thing.
- The ribbon occupies a fixed margin lane (series-constant x, ident behavior) and never
  crosses the torn hole, the Christ figure, or any lettering. It marks the page, not the
  picture.
- One settle, one micro-bounce (the closed-form spring from round 4's polish notes — an
  object with mass, not a tween), then nothing.

**Cost:** $0 per use. One-time: a single banked ribbon texture
(`poc_living_sketchbook/world/ribbon_red.png`, woven texture + frayed tip, alpha) — one
texture render (~2cr) or even a photographed real ribbon, then banked forever.

**The Storm moment.** The torn page stands open — Christ in gold light, the boat at rest
below, the set-off ghost of Matthew 8:26 above. *"…and there was a great calm"* finishes,
and in the right margin, past the torn edge, the red ribbon slips down and lies still.
The episode doesn't end so much as get *kept*.

**Structurally safe because:** a deterministic composite of one banked texture on a fixed
lane; it can carry no words, no image, no claim — the only thing it can possibly say is
"return," which is the CTA's own word.

**Build card (Sonnet):**
- Engine: `panel_animator/ribbon_marker.py`.
- `apply_ribbon(frame, t, t0, ribbon_png, x_frac=0.80, seed=3)` — drop-in from top edge
  over ~0.5s: vertical position spring-settled (closed-form damped oscillator, ~15 lines of
  numpy, overshoot ≤6px), lateral S-curve relaxing (2 control points, seeded), contact
  shadow fading in; after t0+0.6s the function returns a byte-identical composite every
  frame (assert this in the self-test — stillness is the law).
- Export the settle window to the Foley cue list (`fabric_slip` — one soft one-shot,
  generated once on ElevenLabs quota if the sound library lacks it, then banked).
- Self-test: demo on the Storm landing still; assert post-settle frames identical; eye-check
  that the ribbon reads as silk lying ON the page (shadow contact), not a red bar drawn
  over it.

---

## 4. The Rubbing — evidence taken by hand · **CONFIDENCE: MEDIUM-HIGH**

**The pitch.** When an episode turns on an *object* — a coin, a seal, an inscription, a
nail — the sketchbook does what antiquarians have always done with objects they cannot keep:
**takes a rubbing.** The spread's object-insert arrives as graphite frottage: diagonal
graphite strokes accumulate in hand-order (band by band, the way a wrist actually works),
and the image emerges *under* them — graphite-gray on paper-white, edges strong where the
relief is, grain showing through every stroke. It is a reveal that IS a documentary claim:
this was pressed against the real thing. ArkAIology's whole DNA is evidence handled
honestly; this is that DNA in the one idiom a sketchbook owns natively. And it gives the
Foley its most tactile cue yet — two seconds of soft graphite scratch under the strokes,
timed for free because the stroke schedule is ours.

**Where it must never go (governor before pitch, deliberately):** objects and inscriptions
ONLY. Never a figure, never a face, and absolutely never the Face — a rubbing of Christ's
countenance is Veronica-relic territory, an icon claim this series has no business making.
The device documents *things*; persons stay drawn.

**Governors:**
- ≤1 rubbing per episode; only for an object the text itself makes load-bearing.
- The object still passes the standing period gates (a denarius looks like a denarius);
  the rubbing plate derives from an approved still, never from a fresh unaudited render.
- Stroke reveal duration 1.8–2.5s; strokes never fully opaque — paper always breathes
  through.

**Cost:** $0 — the rubbing plate is a deterministic tone-map of an existing approved still
(desaturate → graphite curve → edge-boost), the strokes are seeded PIL bands.

**The honest Storm answer:** Storm has no artifact beat — this device sits the episode out,
exactly as Scribe's Tally and the Measuring Reed did in their rounds, and saying so is the
health check. The worked moments are queued elsewhere: *"Shew me a penny"* / render-unto-
Caesar (the denarius rubbing IS the hook frame), the nails of the crucifixion cluster, the
Ark episodes' pitch-seams, Pilate's titulus (a rubbing of INRI — lettering as OBJECT, which
the never-animate-writing law permits because the letters are a deterministic plate, not
generative).

**Structurally safe because:** reveal-only over an already-gated still; the graphite plate
cannot add content, only re-tone it; the stroke mask is seeded and reproducible.

**Build card (Sonnet):**
- Engine: `panel_animator/frottage.py`.
- `make_rubbing_plate(still_bgr)` — desaturate; tone-curve to graphite-on-paper (paper
  white ≈ the stock's own cream, never pure white); Sobel edge-boost blended ~0.35 so
  relief edges catch as real rubbings do.
- `apply_frottage(frame, plate, t, t0, duration=2.2, angle_deg=38, seed)` — precompute
  N≈40 stroke bands (seeded jitter on angle ±4°, width, length, band order top-to-bottom
  with local left-to-right), accumulate soft-edged stroke masks; per frame, composite
  plate-through-mask over the blank paper region.
- Export the stroke window to the Foley cue list (`graphite_scratch`, looped one-shot).
- Self-test: run on any approved object still; check by eye that mid-reveal frames read as
  a HAND'S PROGRESS (banded, directional) and not a wipe transition — if it reads as a
  wipe, the band ordering is too regular; increase seed jitter, not stroke count.

---

## 5. The Second Sitting — the book in time · **CONFIDENCE: MEDIUM (honest stretch)**

**The pitch.** Sketchbooks are not storyboards; their pages get *returned to*. The Second
Sitting lets an episode revisit one earlier spread late in the cut — the same plate, now
carrying new ink: the answer scribed into the margin of the page that asked the question, a
tally completed, a thread finally tied. Not a flashback (the footage doesn't replay); a
*revisit* — the page aged by the story that happened since. Storm's shape is literally
this: the terror spread asks "carest thou not that we perish?", and the episode's end knows
the answer. A cut back to that spread with one new line of faded ink in its margin — the
question annotated by its own answer — is a move no other device can make, because every
other device lives inside one spread's lifetime.

**Why only medium:** it spends the episode's scarcest resource — seconds — on footage the
viewer has already seen, in a 60s format whose pacing law is forward motion. It works only
when the narration itself verbally returns (the script must earn the cut back; the
payoff-ledger can verify the loop is genuinely paid), and it must survive an A/B against
the same beat cut straight. If the revisit reads as padding rather than payoff, it dies
the split-flap's death and the doc says so.

**Governors:**
- ≤1 per episode, only when the narration audibly returns to the earlier beat.
- The addition is deterministic overlay ink ONLY (Scribed Ink margin line, a thread, a
  Tally completion) — the generated drawing is never re-rendered, so the plate cannot
  drift. ($0 always; the chained-re-render variant is explicitly out of scope — that's
  a different, spend-bearing device and it isn't needed.)
- The revisit is ≤2.5s. It answers; it does not dwell.
- Payoff-ledger check: the revisited question must be a REGISTERED loop and the addition
  must close it.

**Cost:** $0 — the plate exists, the additions are the existing lettering/thread renderers.

**The Storm moment.** ~52s, as the narrator turns the knife — *"when the water reaches
your own knees"* — cut back to s03's terrified-disciples spread for two seconds: the same
plate, unchanged but for one new margin line in elder-faded ink, *"…and there was a great
calm,"* then cut forward to the landing. The page that panicked, annotated by the calm it
couldn't see coming. That is the episode's argument, made by the book instead of the
narrator.

**Structurally safe because:** the plate is byte-identical approved art; the only new
pixels are deterministic lettering that passes the standing letterer laws and the doctrine
chain like any overlay.

**Build card (Sonnet):**
- No new engine — an assembler pattern + ~40 lines: `second_sitting(plate_png, additions,
  t0, dur)` where `additions` reuses existing renderers. The work is in the cut plan, not
  the code. Prototype directly in `_s4_assemble.py`'s idiom on the Storm plates for the
  A/B, before any generalization.

---

## Polish notes (not skills — folded into existing kit, like round 4's spring)

- **Wet ink.** Scribed Ink glyphs should be born glossy and dry matte: a faint specular
  lighten on each glyph for ~2s after its reveal, decaying to nothing. Per-glyph age is
  already known (the alignment drives the reveal). One parameter inside the existing
  letterer; A/B at full res — if it's invisible at video size, drop it without mourning.
- **Selah.** A grammar rule for the assembler, not a device: when held-breath finds a
  ≥1.2s narration silence immediately before the landing, the cut may hold one beat of
  almost-blank paper — grain breathing, nothing else — before the torn page. The visual
  rest the psalmists notated. Costs nothing; needs no code beyond a spread entry.
- **The Gutter (future, long-form only).** When living-sketchbook goes 16:9, the two-page
  spread's gutter becomes the thesis line: OT material on the left leaf, NT on the right,
  the gold thread crossing the binding. The Elder Leaf is this device's younger sibling;
  noted now so the 16:9 design starts there instead of discovering it.

## Considered, and deliberately skipped

- **The Boards** (a cold open on the closed book, opening). The first frame of a Short is
  the hook, and a closed cover is a weak one — the format law kills it before the fiction
  gets a vote. Blue-line already owns the "beginning" ident, in-page, at full hook value.
- **Page-curl turns.** A cv2 3D curl between spreads reads as CG the instant it moves —
  the same-hand test failing at the technology layer, round 4's flyover lesson exactly.
  paperRip / inkSwipe / halftone already own act changes, in-idiom.
- **The visible hand.** The show's hand is implied by its works — stamps, strokes, rubbings
  — and must never be seen: a rendered hand re-introduces the generative layer onto the
  paper layer, breaks the reader-as-hand ambiguity, and adds an anatomy-QC surface for zero
  narrative gain.
- **Dust motes in the lamplight.** Adjacent to the no-glitter law; raking-light's whole
  character is that it stays clean. The paper's texture is the payload, not the air.
- **Correction strike-throughs** (a scribe's crossed-out word). The scribe never errs on
  the Word — a "correction" on or near KJV text is a doctrine hazard rendered as charm.
  No version of this survives the reverence bar.

---

## If I could only build three — ranked against BOTH queues

**1. The Elder Leaf.** It serves the first non-negotiable directly, it is the missing
third stage of a chain two-thirds built (Loom finds → panel judges → *nothing yet cites*),
and it retro-redeems Storm's one acknowledged content gap with Psalm 107:29. Against the
round 3/4 leftovers: I rank it above everything except Annotator's Circle's ready-tonight
Storm moment — and the Leaf has one of those too.

**2. The Papermaker's Mark.** The highest beauty-per-line-of-code this series has left:
one masked lighten inside an already-built pass, carrying the series' entire thesis as a
secret. Zero new overlay slots, zero new governors beyond a strength cap, and it makes the
existing raking-light better rather than crowding it.

**3. The Ribbon Marker.** The series has an opening ident and no closing one; the CTA is
the show's reason to exist and currently ends as audio only. One banked texture, one
spring, and every episode forever after ends *kept* instead of merely finished. Its
sacred-stillness A/B is a genuine open question — which is exactly why it should be built
and judged rather than debated.

The Rubbing waits, without complaint, for the denarius. The Second Sitting waits for its
A/B on the Storm plates — cheapest possible experiment, one evening, no new engine.

And from the standing queue: **Annotator's Circle** (round 4) still has a Storm moment
ready tonight and should ride along with whichever of these builds first; **Voyage Camera**
(round 4) remains the unlock for the journey-episode class and outranks everything here
the day an Exodus or Acts 27 episode is greenlit.

All five proposals are $0 per run. Two need a one-time banked texture (~2cr each, quoted
before generating, per the standing spend rule). All five are deterministic paper-layer
work under round 2's governors: they compose approved material, they cannot generate, and
the one layer that CAN hallucinate is already being watched by the round-3 device built
for exactly that.
