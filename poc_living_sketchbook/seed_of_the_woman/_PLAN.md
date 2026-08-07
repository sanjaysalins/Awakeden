# Seed of the Woman LONG — spread plan (FULL: 71 spreads, all 7 movements)

**STATUS: real episode, promoted from the POC30 process-validation test**
(2026-08-07, memory `day-of-atonement-retro-learnings` — validated the Day
of Atonement retrospective's fixes on this exact content first, then
promoted rather than discarding it). Content: Genesis 3:8-10 so far,
reusing `longform/05_The_Seed_Of_The_Woman/v1/narration.mp3` turns 0-3
verbatim (already-locked text, already-voiced audio, real forced-aligned
timing in `_alignment.json`). See `_PREFLIGHT.md` for the census,
camera-angle plan, and device/bbox assignments for spreads 1-5.

**FULL PLAN AUTHORED 2026-08-07** (spreads 6-71 below, per SKILL.md sec.8b
point 1: Fable pre-designed the whole table — camera angles, device/bbox
assignments, every verse card, the landing, and the introspective runs —
BEFORE any further rendering; the matching pre-designs are in
`_PREFLIGHT.md`). Timing basis for spreads 6+: `_turn_boundaries.json`
(real forced-alignment-derived turn windows, accurate to ~1-2s; sub-turn
seams inside long narrator turns are word-proportional ESTIMATES flagged
for the standard alignment-correction pass before build — same two-pass
model as always). Get a fresh cost quote before the full stills+animate
pass — this 5-spread slice cost ~$4; the full-episode rough range is in
§6 below and needs an explicit OK first, per ask-before-spending.

**Timing seam note:** spreads 1-5 were timed against the 33s excerpt's own
`_alignment.json`; the full-file `_turn_boundaries.json` puts turn 3's end
at 33.76s (vs the excerpt's 33.03). Spread 5's end therefore extends
33.03 → 33.80 at the alignment-correction pass (its designed hold simply
breathes ~0.8s longer; no rework). Spread 6 starts at 33.80.

## The spread table

**Timing honesty (corrected 2026-08-07):** turn-level boundaries (33 of
41 turns) are real forced-alignment timing from `_turn_boundaries.json`.
Sub-turn seams — where ONE turn is split across multiple spreads — were
word-count-proportional ESTIMATES in the first draft; the independent-
review panel correctly called the original header's "real alignment
timing, not estimated" claim false. A real per-word spot-check on turn 27
(the s39-42 block, one of the panel's named highest-risk spans) CONFIRMS
the word-count-proportional splits are meaningfully off, not just
technically-unverified: the real pause structure gives four natural
clauses at roughly 6.0s / 6.3s / 11.3s / 13.3s, vs. the plan's assumed
7.7s / 8.0s / 9.5s / 11.8s — different enough that s40/s41's actual visual
beats may need re-drawing against where the words really fall, not just a
timestamp nudge. That is a real content-design task (the same one
`_s5_align.py` + `_s5b_spread_windows.py` do carefully for every other
living-sketchbook episode), not something to rush through inside a plan
revision — **so it is now scheduled as an explicit pre-batch step (see the
staged build order after §6), not marked done here.** s34-36 and s56 are
lower-risk than first flagged: their actual quote content sits on already-
real SCRIPTURE-turn boundaries (`_turn_boundaries.json` turns 20/22/24),
so only the narrator lead-in portions need the same careful pass. The
remaining ~15 other multi-spread turns are unexamined and still word-count
estimates.

| # | Start–End (s) | Dur | Beat | Type | Shows | Assets | Device |
|---|---|---|---|---|---|---|---|
| 1 | 0.0–5.8 | 5.8 | 1 | NS | Wide, high angle: Adam and Eve small in the garden, something visibly wrong — "Something has just gone terribly wrong in the garden... have believed a lie," | Adam, Eve, eden (bg) | dramatic_spotlight (still, bbox on the two figures) |
| 2 | 5.8–11.9 | 6.1 | 1 | NS | Medium, eye-level, among the trees: the two of them hiding — "eaten what He forbade... they are hiding from Him." | Adam, Eve, eden (bg) | real clip — Kling (multi-figure) |
| 3 | 11.9–24.0 | 12.1 | 1 | VC | Verse card, Scribed Ink: Gen 3:8 KJV verbatim, over the eden background | eden (bg) | Grand-Text combo, lettering built with this spread |
| 4 | 24.0–30.7 | 6.7 | 1 | NS | Wide, low angle through the canopy: light/presence moving, no figure — "And God comes looking... with a question." | eden (bg), LORD-presence (light only) | real clip — Seedance (calm, single light-presence) |
| 5 | 30.7–33.0 | 2.3 | 1 | NS | Held close on the light between the trees — "Where art thou?" (the landing) | eden (bg), LORD-presence (light only) | device-only, Fable-designed bespoke hold, no camera move |
| 6 | 33.80–40.67 | 6.9 | 1 | NS | ACTING 1: the blame circle — Adam's arm extends toward Eve (motion completes, holds), Eve turning toward the serpent low in the leaves — "The man blames the woman, and the woman blames the serpent:" | Adam, Eve, **serpent** (first appearance), eden (bg) | real clip — Kling (designed acting spread, multi-figure) |
| 7 | 40.67–43.75 | 3.1 | 1 | VC | Composite verse-over-art, Scribed Ink fast (39 glyphs / 3.0s voiced = 13.0 g/s): Gen 3:13b "The serpent beguiled me, and I did eat." over Eve's turned profile, serpent shadow at the low frame edge | Eve, serpent (shadow) | Scribed Ink composite, $0 |
| 8 | 43.75–49.30 | 5.6 | 1 | NS | "Everything good is coming apart in real time" — the two figures small and separate, leaves falling, color draining at the page edges | Adam, Eve, eden (bg) | real clip — Seedance (leaves drift, calm) — sl13 variant CANDIDATE, see §5b |
| 9 | 49.30–54.33 | 5.0 | 1 | NS | "God's answer begins in the most unexpected place" — the page darkens; ONE gold fleck breathes at the lowest margin, in the dust | eden (bg, darkened) | device-only, Fable-designed bespoke hold (gold-fleck breathe; pre-designed in _PREFLIGHT) |
| 10 | 54.33–61.50 | 7.2 | 2 | NS | "And judgment has to fall" — high overhead: Eden wide, one long shadow lengthening across it | eden (bg) | real clip — Seedance (shadow lengthens; state-only) |
| 11 | 61.50–68.81 | 7.3 | 2 | NS | The couple crouched among the trees, afraid of the presence they were made for — light beyond the trunks, faces averted | Adam, Eve, eden (bg), LORD-presence (light) | real clip — Kling (two figures, faces under weight) |
| 12 | 68.81–76.50 | 7.7 | 2 | NS | Flashback register, desaturated: Eve's ear inclined toward the serpent-shape in the branches — "taken the creature's word against the Creator's" | Eve, serpent, eden (bg) | real clip — Seedance (branch sway only; serpent STILL) |
| 13 | 76.50–83.50 | 7.0 | 2 | NS | Object insert: the fruit fallen in the dust, one bite gone — "You cannot un-eat the fruit" | fruit (text-locked prop), eden (bg) | dramatic_spotlight (still, bbox on the fruit) |
| 14 | 83.50–89.50 | 6.0 | 2 | NS | "or stop the death that has now entered the world" — the ink-blue wash creeps over the garden page from the edges: death enters as the medium itself | eden (bg) | wash-creep ADVANCE ($0 — pays off at s52) |
| 15 | 89.50–96.16 | 6.7 | 2 | NS | THE BREACH: a DRAWN chasm splits the spread — garden light on the far side, the couple small on the near side, no bridge — "it has to come from God's side of the breach" (drawn, never torn paper: the tear stays reserved for the landing) | Adam, Eve, eden (far side) | parallax-panel ($0 — near rim drifts against the far garden) |
| 16 | 96.16–100.64 | 4.5 | 3 | NS | "Now watch closely" — the camera hunts the sentencing tableau and locks LOW, on the dust where the serpent lies | Adam, Eve, serpent, LORD-presence | hunt_and_lock ($0 — the device's literal design case) |
| 17 | 100.64–105.30 | 4.7 | 3 | NS | "He does not turn to Adam first. He does not turn to Eve first." — the two braced for sentence, the light NOT facing them | Adam, Eve, LORD-presence | real clip — Kling (braced faces, subtle) |
| 18 | 105.30–110.31 | 5.0 | 3 | NS | "He turns to the serpent." — the light pivots DOWNWARD to the serpent low in the dust; high angle on the accused | serpent, LORD-presence | real clip — Seedance (light pivots; serpent still) |
| 19 | 110.31–121.36 | 11.1 | 3 | VC | Verse card, Scribed Ink live-write: Gen 3:14 (~138 glyphs / 9.87s voiced = 14.0 g/s, inside proven ≤15 pace; card holds through the 1.2s post-verse pause) over the serpent-in-dust art | serpent (bg art) | Grand-Text combo, Scribed Ink live-write, $0 |
| 20 | 121.36–126.50 | 5.1 | 3 | NS | "That much is pure curse." — the serpent flattened, belly to the ground, tight-high crop, ink-blue judgment register | serpent | real clip — Seedance (dust settles; state-only) |
| 21 | 126.50–132.20 | 5.7 | 3 | NS | "listen to what God weaves into it" — a fine GOLD THREAD (already placed in the still) fades and swells into visibility THROUGH the dark curse-lines of the page | serpent (dark ground), gold thread | Thread Device: stroke placed in the still + `thread_opacity` fade-in + `thread_swell` pulse ($0, proven functions only — the episode's signature image is seeded here) |
| 22 | 132.20–143.15 | 11.0 | 3 | VC | THE VERSE — Gen 3:15, god voice, red-letter: Illuminated Rubric (formal peak 1 of 2), ARRIVES WHOLE ~1.2s in (LAW 1), gold dropped cap "A"; the curse-dark page with the gold thread behind; slow push carries the ~9s hold | gold thread (bg) | Illuminated Rubric, whole arrival + slow push, $0 |
| 23 | 143.15–149.50 | 6.4 | 3 | NS | "Let that land." — sacred stillness on the promise card; nothing moves but the grain and the thread's faint gleam | (s22's card, held) | $0 hold: grain-boil + held-breath quiet point 1 |
| 24 | 149.50–156.00 | 6.5 | 3 | NS | "Before God says a word to Eve about sorrow, before a word to Adam about thorns and dust" — the couple still waiting in shadow, sentences unspoken, the gold thread already glowing between them | Adam, Eve, gold thread | real clip — Kling (two waiting faces) |
| 25 | 156.00–162.01 | 6.0 | 3 | NS | Thesis wide: "the first promise of rescue... spoken into the enemy's own curse" — serpent low under the curse-dark band; the thread (drawn full-length in the still) gleams via `thread_swell` toward the future | serpent, gold thread | Thread Device: `thread_swell` gleam ($0, proven) |
| 26 | 162.01–168.50 | 6.5 | 4 | VC | THE STUDY COPY: the promise re-copied in the Keeper's own hand under lamplight, already written; the ANNOTATOR'S CIRCLE draws around "her seed" the instant the narrator says it (the episode's ONE circle) | study-copy (overlay prop), desk | annotators-circle ($0, 1/1 budget) |
| 27 | 168.50–176.50 | 8.0 | 4 | NS | "a line is most often traced through fathers" — small chained figure-sketches, father to son to son, a drawn descent-line linking them (figures only, NO lettering) | (anonymous sketch figures) | $0 drawn-line reveal (descent line draws itself, father to father) |
| 28 | 176.50–186.90 | 10.4 | 4 | NS | "Here the hope hangs on the woman's seed... a clue that lights up" — from Eve's small figure ONE luminous thread runs forward off-page; at its far end a first warm glow brightens | Eve (small), gold thread | real clip — Seedance (far glow warms; thread pre-drawn) |
| 29 | 186.90–194.76 | 7.9 | 4 | VC | Illuminated Rubric (formal peak 2 of 2 — the promise KEPT): Gal 4:4, gold dropped cap "B", per-line arrival timed to the voice, first fully WARM palette page | — | Illuminated Rubric, per-line arrival, $0 |
| 30 | 194.76–201.98 | 7.2 | 4 | NS | ACTING 2 — the annunciation: a bowed young woman, veiled, face averted, hands gathering at her heart (motion completes, holds); the angel rendered as LIGHT only | **Mary** (no-anchor treatment, see §5), light-presence | real clip — Kling (designed acting spread; face averted by design) |
| 31 | 201.98–208.63 | 6.7 | 4 | VC | Composite verse-over-art: Luke 1:35b (90 glyphs / 6.6s = 13.6 g/s) letters over the annunciation art's calm dark field — underline swash on "shall be called the Son of God" | Mary (bg art) | Scribed Ink composite, $0 |
| 32 | 208.63–216.50 | 7.9 | 4 | NS | Honesty register: the promise page and the Gospel page side by side on the desk, and NO drawn line between them — the gap where the reader expects a thread ("No New Testament writer ever stops, quotes Genesis 3:15 word for word...") | study-copy, second page, desk | focal-tour ($0 — halo visits promise page → Gospel page → the empty gap) |
| 33 | 216.50–225.50 | 9.0 | 4 | NS | THE TRAJECTORY: the whole canon as one long fanned shelf of pages across the spread, bending like a drawn curve toward a single gold point at the far edge | (canon pages) | real clip — Seedance (ember-glow breathes at the far point) |
| 34 | 225.50–236.91 | 11.4 | 4 | VC | THE NAMING PAGE 1/3 (ONE continuous page across 34-36, in-page arrivals, no page turns — see §3 note): a short hand-lettered question "THE SERPENT?" then Rev 12:9 "that old serpent, called the Devil, and Satan." | naming page (prop) | Scribed Ink (question line + verse line, same proven technique as s7/s31/s53/s56 — NOT Ink Stamp/Typeset, which don't exist as built tools), $0 |
| 35 | 236.91–244.96 | 8.1 | 4 | VC | THE NAMING PAGE 2/3: "THE MISSION?" + 1 John 3:8 "For this purpose the Son of God was manifested, that he might destroy the works of the devil." | naming page | Scribed Ink (question + verse, same technique, accumulating on the same page), $0 |
| 36 | 244.96–253.59 | 8.6 | 4 | VC | THE NAMING PAGE 3/3: "THE CRUSHING?" + Rom 16:20 "And the God of peace shall bruise Satan under your feet shortly." | naming page | Scribed Ink (question + verse, same technique, page now full), $0 |
| 37 | 253.59–259.55 | 6.0 | 4 | NS | "The opening pages of Scripture planted a promise" — a seed in drawn soil at the book's first pages; a gold thread-sprout (drawn in the still, rising from the seed through the stacked page-edges) fades and swells into visibility — the title image | gold thread, (the book) | Thread Device: `thread_opacity` fade-in + `thread_swell` ($0, proven) |
| 38 | 259.55–267.82 | 8.3 | 5 | NS | Register drop: "a fair-minded skeptic has real objections" — the desk pulled back wide, gold dimmed deliberately, cool light | desk | raking-light ($0, its ONE use — the lamp sweeps the cooled desk) + held-breath quiet point 2 |
| 39 | 267.82–275.50 | 7.7 | 5 | NS | The objection in the Keeper's OWN hand: the margin entry "Just a snake story?" writes itself (energy ~0.35 — honest, not panicked) | desk | keeper-hand entry ($0, 1 entry) |
| 40 | 275.50–283.50 | 8.0 | 5 | NS | The fair concession: the "her seed" study copy beside quick graphite sketches of ORDINARY descent — children, generations — the ordinary reading given real weight | study-copy, desk | $0 hold: grain-boil + spotlight shift copy → sketches |
| 41 | 283.50–293.00 | 9.5 | 5 | NS | THE SHAPE OF THE CANON: pull way back — the whole sketchbook from above, pages fanned in one long arc, the gold thread visible running through every page toward the last | (the book itself) | real clip — Seedance (pages stir faintly; thread gleams along the arc) |
| 42 | 293.00–304.77 | 11.8 | 5 | MV | "followed out from within": three soft vignettes — the serpent named / the Son destroying the enemy's works / the woman's child — with the thread emerging FROM the Genesis page's own paper fibers, not laid on top | serpent, Jesus (vignette), Mary (vignette) | focal-tour ($0 — visits the three vignettes in narration order) |
| 43 | 304.77–311.19 | 6.4 | 5 | NS | "crushed under your feet — the church's feet?" — many bare feet standing on stone beside ONE Man's feet; the 0.6s "under your feet" fragment gets NO card (deliberate — it lives in the composition) | crowd feet (anonymous), Jesus (feet) | real clip — Kling (multi-figure) |
| 44 | 311.19–318.50 | 7.3 | 5 | NS | "the church... stands on the One who won it first" — small figures atop high ground lit gold; beneath the ground-line's shadow the serpent's coil lies subdued (Rom 16:20's own image, restrained) | crowd (small), serpent (subdued) | real clip — Seedance (dust, light; state-only) |
| 45 | 318.50–327.03 | 8.5 | 5 | NS | THE LINE: very wide — Eden's trees at the left edge, the cross a far silhouette at the right (its FIRST appearance), the gold thread (drawn full-width in the still) gleams via `thread_swell` — "follow the line that runs from Eden to the cross" | eden (edge), **Golgotha silhouette**, gold thread | Thread Device: `thread_swell` gleam ($0, proven) |
| 46 | 327.03–337.03 | 10.0 | 6 | NS | "Look again at how the deliverer wins" — the study copy under the lamp once more, the hand resting beside it, flame breathing (recall register) | study-copy, desk | real clip — Seedance (flame breathes ONLY; page region static — text overlay lives there) |
| 47 | 337.03–341.96 | 4.9 | 6 | VC | The study copy re-inked: Gen 3:15b "it shall bruise thy head, and thou shalt bruise his heel." (58 glyphs / 4.9s = 11.8 g/s) — underline swashes arrive under "bruise thy head" and "bruise his heel" as each is spoken | study-copy | Scribed Ink + two timed underline swashes, $0 |
| 48 | 341.96–348.00 | 6.0 | 6 | NS | The heel-strike: the serpent's strike at a human heel — fangs at the heel, ink-red accent (sparing) — "real, agonizing, the kind of strike that can kill" | serpent, heel (anonymous figure) | real clip — Kling (action tier) |
| 49 | 348.00–353.66 | 5.7 | 6 | NS | The head-crush, FROZEN: the descending heel above the serpent's head, held at the instant before — "final." No gore; the stillness carries it | serpent, heel | dramatic_spotlight (still, bbox on heel + head) |
| 50 | 353.66–359.50 | 5.8 | 6 | NS | HARD CUT — "That is the cross." Golgotha wide, LOW angle (the camera kneels), the cross against an UNNATURAL midday darkness — ink-wash swallowing the sky, never storm clouds, never lightning | **Golgotha plate** (reuse-check §5), Jesus (distant) | real clip — Seedance (darkness thickens; state-only) |
| 51 | 359.50–365.50 | 6.0 | 6 | NS | Closer: the Son bearing what we had earned — reverent, wound-free staging, head bowed; the thin gold-leaf edge stays present (glory never fully absent) | Jesus (cross pose) | real clip — **Seedance, NOT Kling** (FIXED 2026-08-07, real doctrinal bug the panel caught: this project's OWN locked rule is "Seedance ALWAYS for Christ/crucifixion iconography regardless of complexity" — Kling regenerates wounds/blood even on a retouched-clean still, `living-light-no-fresh-blood`; the original Kling assignment directly violated a rule already locked in this repo's own CLAUDE.md) |
| 52 | 365.50–371.21 | 5.7 | 6 | NS | THE EXCHANGE: the ink-blue judgment wash that entered the world at s14 now RETREATS and withdraws from the world's edges, cream paper reclaiming what it had taken — the still's OWN composition (not the motion) already shows its last dark trace resting over Him, carried from s51's framing | Jesus (cross) | wash-creep RETREAT ($0, proven real mode — `wash_creep.py` only advances/retreats along an edge, no converge-to-figure geometry exists; the "falls on Him" idea is staged in the STILL, not invented in new motion code) |
| 53 | 371.21–377.70 | 6.5 | 6 | VC | Composite verse-over-art: Heb 2:14b (89 glyphs / 6.4s = 13.8 g/s) over the cross art — "that through death he might destroy him that had the power of death, that is, the devil." | Jesus (bg art, re-framed s51) | Scribed Ink composite, $0 |
| 54 | 377.70–384.50 | 6.8 | 6 | NS | "The blow that looked like the serpent winning" — the cross distant and small; the serpent's coil risen LARGE in the foreground shadow, rendered as darkness only (the LIE of the frame — never triumph, never charm) | serpent (shadow), Jesus (cross, distant) | real clip — Seedance (shadow deepens; coil pre-risen in the still, state-only) |
| 55 | 384.50–391.50 | 7.0 | 6 | NS | THE INVERSION — the SAME framing held and re-read: the cross-beam's shadow travels until it falls across the serpent's head, and holds — the cross itself is the crushing blow | serpent, cross shadow | $0 bespoke shadow-sweep (Fable pre-designed, _PREFLIGHT) |
| 56 | 391.50–399.50 | 8.0 | 6 | VC | Composite: Col 2:15 "And having spoiled principalities and powers, he made a shew of them openly, triumphing over them in it." over the now gold-edged cross, dark powers broken beneath — quote sits INSIDE narrator turn 36: needs the alignment pass, TIMING FLAG | Jesus (cross, gold edge) | Scribed Ink composite, $0 |
| 57 | 399.50–407.50 | 8.0 | 6 | NS | The EMPTY TOMB at dawn: stone rolled, gold light from WITHIN the opening, folded linen — no figure (the emptiness filled with light and linen, per the empty-place rule) | **tomb plate** (NEW) | real clip — Seedance (inner light breathes, dust motes) |
| 58 | 407.50–413.00 | 5.5 | 6 | NS | "a beaten enemy already" — the SHED SKIN: the old serpent's empty cast skin in the dust at dawn, hollow, the power gone (the beaten-enemy symbol — see §5; never gore) | serpent (shed skin) | real clip — Seedance (dawn wind stirs dust; skin still) |
| 59 | 413.00–419.44 | 6.4 | 6 | NS | Already / not-yet: horizon wide — dawn fully arrived at one edge, a FAR brighter light waiting beyond the opposite horizon — "defeated at the cross, finished forever at the King's return" (holds through the 1.15s pre-M7 pause) | horizon plate | $0 bespoke dual-glow breathe (pre-designed) |
| 60 | 419.44–424.59 | 5.2 | 7 | NS | "the oldest promise in the world, and it is still open" — the study copy lying OPEN in warm light, the book literally open, held | study-copy, desk | $0 warm-glow breathe + grain-boil (text on page — no base motion) |
| 61 | 424.59–431.00 | 6.4 | 7 | MV | "Not over an altar, not from a mountain" — two pale vignettes (an altar / a mountain) left as NON-PHOTO-BLUE UNDERDRAWING, never inked — the promise came before them | (underdrawn vignettes) | focal-tour ($0 — visits altar → mountain; both stay pale) |
| 62 | 431.00–438.00 | 7.0 | 7 | NS | "into a curse, in the hearing of the enemy, while two guilty people stood waiting" — the whole sentencing tableau recalled in one wide: couple waiting, serpent low, the gold thread glowing in the dark between | Adam, Eve, serpent, gold thread | real clip — Seedance (figures still; thread gleams) |
| 63 | 438.00–444.50 | 6.5 | 7 | MV | "Before there was a temple, a prophet, or a single drop of sacrificial blood" — temple / prophet / altar-blood as unfinished PENCIL GHOSTS on the page; only the gold thread is inked solid, already old | (pencil ghosts), gold thread | $0: ghosts pre-drawn, thread gleam-pass |
| 64 | 444.50–450.54 | 6.0 | 7 | NS | "God had already named the future" — the thread completes INTO a small finished vignette: the cross and the open tomb, warm | gold thread, cross+tomb vignette | real clip — Seedance (warm light rises on the vignette) |
| 65 | 450.54–457.50 | 7.0 | 7 | NS | POV — the viewer hides: from WITHIN the trees looking out toward the light in the clearing; the shadows between trunks carry the serpent's old coil-shape — "your safest move is to stay hidden in the trees" | eden (bg), serpent (shadow-shape), LORD-presence (light) | real clip — Seedance (leaves stir, light steady; camera locked) — sl16 variant CANDIDATE, see §5b |
| 66 | 457.50–463.50 | 6.0 | 7 | NS | "But that promise has been kept." — s32's two-page framing RETURNS, and now the thread DOES connect them: the study copy and the cross-vignette bridged on one desk (the answer to s32's gap) | study-copy, cross vignette, desk | focal-tour ($0 — copy → thread → vignette; no base motion) |
| 67 | 463.50–469.75 | 6.3 | 7 | NS | "whose end is now only a matter of time" — the shed skin again, smaller, far off at the dawn horizon's edge | serpent (shed skin), horizon | real clip — Seedance (wind, dust; calm) |
| 68 | 469.75–474.30 | 4.6 | 7 | NS | "you do not have to climb your own way back into the garden" — the breach recalled (s15's drawn chasm, re-framed LOW from the chasm floor): the garden higher and farther, no ladder, no bridge from the near side | eden (far), chasm (chained from s15) | parallax-panel ($0 — same grammar as s15, new framing) |
| 69 | 474.30–483.40 | 9.1 | 7 | NS | "the dying do not heal themselves, and they were never asked to" — close on ONE pair of open, empty hands, held out, nothing in them (anatomy QC: exactly two hands, one pair, stated in prompt) | hands (anonymous) | real clip — Kling (hands tier; tremble, then still) |
| 70 | 483.40–490.40 | 7.0 | 7 | NS | "So step out from behind the trees" — s65's POV reversed in meaning: the light in the clearing WIDENS and brightens toward the viewer; the way stands open (camera locked; the LIGHT moves, not the camera) | eden (bg), LORD-presence (light) | real clip — Seedance (light widens; named motion only) |
| 71 | 490.40–500.45 (+ ≥3.0s hold) | 10.1 + hold | 7 | LAND | THE LANDING: `torn_out_page` (real, built) transitions INTO this spread as "the One whose heel was struck" begins — the risen Christ stands in the same garden light that came looking in s04 — the God who came seeking IS the rescue (hook→landing mirror). "Come out, and be found by Him." lands over sacred stillness; glow breathes only (same proven bespoke hold as s05); INV-26 hold; INV-27 watermark | Jesus (risen, garden light — NEW render, fail-closed), eden light | `torn_out_page` transition (real, built — panel_animator/page_transitions.py) arriving into a plain static/breathing hold (same proven device as s05, NOT the unbuilt "tear_hole" — see DoA's own s76_landing.py precedent: "tear_hole... isn't built... a reverent held/pushed frame now, real, finished, $0"); optional ribbon-marker A/B (ships only if it wins) |

**Sum check (spreads re-partition the 41 turns exactly):** t4=s6 · t5=s7 ·
t6=s8-9 · t7=s10-11 · t8=s12-15 · t9=s16 · t10=s17-18 · t11=s19 ·
t12=s20-21 · t13=s22 · t14=s23-25 · t15=s26-28 · t16=s29 · t17=s30 ·
t18=s31 · t19=s32-34a · t20 inside s34 · t21+t22=s35 · t23+t24=s36 ·
t25=s37 · t26=s38 · t27=s39-42 · t28+t29=s43 · t30=s44-45 · t31=s46 ·
t32=s47 · t33=s48-49 · t34=s50-52 · t35=s53 · t36=s54-59 · t37=s60 ·
t38=s61-64 · t39=s65-67 · t40=s68-71. The chain is CONTINUOUS (each
spread's start = the previous end; inter-turn pauses are absorbed into the
preceding spread's hold, e.g. s19 and s59), so the table's total is
guaranteed = 500.45s (+ the assembly-added ≥3.0s landing hold).
5 existing + 66 new = **71**.

## Why this excerpt (not a random 30s)

Chosen specifically because it contains a real scripture turn (spread 3,
Gen 3:8) inside the first 33 seconds — without a verse-card spread, the
lettering-built-with-the-spread fix (retrospective fix #4) couldn't be
tested at all. It's also the true opening of one of the two real candidate
next episodes (Seed of the Woman), so the Adam/Eve cast anchors and the
Eden world anchor built here carry forward into the real build rather than
being thrown away.

## Reuse posture

Narration text and audio: reused verbatim, $0, already locked+voiced+
5-CLI-panel-reviewed as part of `longform/05_The_Seed_Of_The_Woman/v1/`.
Visuals: entirely new (living-sketchbook has never rendered this passage) —
this is what the stills-discipline fix (#7) is actually testing.

---

## 3. Why 71 spreads — not 76 copied, not ~65 scaled

**71 spreads over 500.45s. Average 7.05s/spread, range 2.3s (s05) – 12.1s
(s03).** Day of Atonement landed on 76 at 7.75s avg for 588.64s; Bronze
Serpent on 68 at 8.7s for 590s. This plan does not copy either number —
the pacing is driven by measurable properties of THIS narration:

1. **Same quote density, choppier quote SHAPE.** 13 scripture/god turns in
   500s (1 per ~38.5s — almost exactly Day of Atonement's 1 per 39s), but
   three of them are FRAGMENTS under 3.1s (Gen 3:13b at 3.0s, Rev 12:9 at
   2.6s, "under your feet" at 0.6s) and one sits mid-sentence inside a
   narrator turn (Col 2:15). Fragments force fine chops (s7) or deliberate
   refusals (t29 gets NO card; t20-24 get the Typeset pressed-line register
   precisely because Scribed Ink cannot letter 46 glyphs in 2.6s). The
   naming run (s34-36) is designed as ONE continuous page with in-page
   arrivals — a deliberate, user-flagged exception to the never-two-
   lettered-adjacent rule, because three page-turn cards in 28s WOULD be a
   slideshow while one accumulating inquest page is a rhythm.
2. **This story argues; Day of Atonement performed.** That narration's
   center was a physical RITE (vest → slay → carry → sprinkle → send), and
   procedure cuts fast. This one's center (M4-M5, ~165s) is an ARGUMENT —
   trajectory, objection, concession, answer — which lives on the Keeper's
   desk and earns FEWER, LONGER spreads (M4 8.1s / M5 8.4s averages, the
   slowest of the film) built on study-page grammar, while the hook keeps
   spreads 1-5's established fast pace (M1 6.0s avg) and the climax
   accelerates (M6 6.6s avg, 14 spreads — most in the film, matching Day
   of Atonement's "reveal gets the most spreads" shape). The four longest
   holds sit on the four heaviest moments: the naming page's Rev 12:9 turn
   (11.4s), "followed out from within" (11.8s), the Gen 3:14 curse card
   (11.1s), and the Gen 3:15 Rubric (11.0s) — plus the 10.1s landing.
3. **A proportional scale-down of Day of Atonement (~65) is rejected for
   the same reasons its own plan rejected scaling up**: QC and cost
   compound per spread, not per second — but M6 here genuinely needs 14
   spreads (two-wounds dissection → Calvary 3-stage → inversion pair →
   tomb → shed skin → horizon is 6 distinct image IDEAS the text names one
   after another), and starving it to hit a copied average would blur the
   film's actual climax. Movement-by-movement: M1 9/6.0s · M2 6/7.0s ·
   M3 10/6.6s · M4 12/8.1s · M5 8/8.4s · M6 14/6.6s · M7 12/6.8s.

**Hook→landing mirror (the structural spine):** the film opens with God
walking in the garden, seeking ("Where art thou?", s04-05) and lands on
the risen Christ standing in that same seeking light as the page tears
open ("Come out, and be found by Him", s71). s65/s70 are a designed POV
pair (hiding in the trees / the light widening), and s32/s66 are a
designed desk pair (the gap where no thread runs / the thread connecting
promise to keeping).

## 4. Verse-card register map (12 new lettered spreads + s03)

Never two lettered spreads adjacent (the one designed exception: the
s34-36 continuous naming page). Five registers, spent deliberately:

- **Illuminated Rubric ×2, the matched pair:** Gen 3:15 (s22, promise
  SPOKEN, god voice, LAW-1 whole arrival) and Gal 4:4 (s29, promise KEPT,
  per-line arrival). Nothing else gets the gold dropped cap.
- **Scribed Ink cards ×2:** Gen 3:14 live-write (s19, 14.0 g/s — fastest,
  inside the proven ≤15 ceiling) and Gen 3:15b re-study (s47, 11.8 g/s,
  two timed underline swashes).
- **Scribed Ink composites over story art ×4:** Gen 3:13b (s7), Luke
  1:35b (s31), Heb 2:14b (s53), Col 2:15 (s56 — TIMING FLAG: mid-turn,
  needs the alignment pass). Climax quotes letter onto the art itself,
  per the Day of Atonement precedent (accelerate visually, don't stack
  card pages).
- **Scribed Ink, question+verse pairs ×3 (the naming page, s34-36):**
  REVISED 2026-08-07 after the independent-review panel found "Ink Stamp"/
  "Typeset pressed lines" don't exist as built tools (only an unpromoted,
  never-validated prototype under different naming) — uses the SAME proven
  Scribed Ink technique as the composite quotes (s7/s31/s53/s56) instead,
  a short question line + the verse line, accumulating on one page across
  the three spreads. Solves the same 2.6s-fragment pacing problem (each
  beat gets its own short line, not one long card) without inventing new
  lettering mechanics right before a full spend decision.
- **The study copy (s26/40/47/60/66):** the Keeper's own hand-copy of the
  promise — a recurring PROP, not a new card each time (same base still +
  same overlay params/seed every appearance). Carries the episode's ONE
  annotators-circle ("her seed", s26).
- **Refused on purpose:** t29's 0.6s "under your feet" fragment gets no
  lettering — it lives in s43's composition.

## 5. Assets — existing (reuse, $0) vs. gaps

**Existing — REFERENCE, do not rebuild** (all under
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_living_sketchbook\`):

- `cast\adam_ref.png` + `cast\eve_ref.png` — this episode's own approved
  anchors (spreads 1-5). Adam in 9 spreads, Eve in 12.
- `world\eden_ref.png` — every Eden-set spread (s01-s12, s15, s62, s65,
  s68, s70, s71's light). One garden, one WORLD.
- `cast\JESUS.md` + `cast\jesus_ref.png` — repo-level sketch anchor.
  Appears ~8 spreads across 4+ poses (cross s50-56, vignettes s42/64/66,
  feet s43, risen s71). **Multi-pose identity lock applies in force — with
  an explicit RENDER-ORDER fix** (the independent-review panel caught that
  s42/s43 sit EARLIER than s51 in spread-number order, so building strictly
  in table order would lock those two in BEFORE the s51 anchor exists,
  exactly the drift risk the lock is meant to prevent): **render s51 first
  among all Jesus spreads, out of table sequence**, get it approved, THEN
  render s42/s43/s50/s53-56/s64/s66/s71 chaining s51 as the second
  reference. Table position stays for assembly/timing; build ORDER does
  not follow table order for Jesus spreads. Fail-closed eye-QC on all.
- LORD-presence — light only, never a figure: re-use spreads 4-5's exact
  prompt block (s11, s16-18, s65, s70, s71's garden light).

**Gaps — need a decision or a small build BEFORE stills render:**

1. **The serpent (NEW world anchor** — `world\SERPENT.md` +
   `serpent_ref.png`): ~18 appearances, by far the most-recurring new
   element. Locked treatment (reasoning in `_PREFLIGHT.md`): a REAL
   creature of judgment, never cartoonish, never sympathetic, never
   charming — no dragon fantasy, no facial expression, no upright coil
   after Gen 3:14; ink-blue judgment register always, NEVER gold; the
   camera looks DOWN on it in every serpent-focus frame (the deliberate
   inverse of the Bowed Camera — the lens kneels only at glory). Before
   the curse verse (s6-16) it may be among branches; from s18 onward
   belly-to-ground, per the verse itself. The "beaten enemy" beats
   (s58/s67) use the SHED SKIN — an empty cast skin, hollow, the power
   gone — so victory is shown without gore and without ever staging the
   enemy as a fought equal. The head-crush is never rendered as impact:
   s49 freezes the instant BEFORE, and s55 lands the cross-beam's shadow
   across the head — the narration's own theology (the cross IS the
   crushing blow) doing the visual work.
2. **Golgotha / cross plate:** reuse-check FIRST: `day_of_atonement\stills\
   s53_the_cross.png`, `day_of_atonement\stills\s54_guilt_laid_on_christ.png`
   (s54 is a multi-vignette Aaron+goat-memory composite, not a clean cross
   plate on its own — reuse only its cross ELEMENT if isolatable, don't
   assume the whole frame transfers). **`bronze_serpent_long\stills\
   s44_shadow_cross.png` is explicitly REJECTED, not a candidate** — that
   episode's own `_build_clips_review.md` already flags it "doctrinally too
   risky"; listing it here was a bad reuse suggestion the independent-review
   panel caught. Topical-fit gate applies to whatever IS reused (no
   tabernacle, no serpent-pole in frame; eye-check, don't assume). Expect at
   least 1 new wide (s50's kneeling-camera darkness) even if closer frames
   reuse.
3. **Empty tomb plate** (s57 + s64's vignette): new; check the banks for
   a thread-neutral tomb first (none expected — the
   `library-lacks-living-christ` gap extends to tomb plates).
4. **Risen Christ in garden light** (s71): NEW render, the known library
   gap; fail-closed QC, chained to jesus_ref + the s51 approval.
5. **Mary — deliberately NO anchor:** 2 spreads + 1 vignette. Rendered as
   a bowed, veiled young woman, face averted or downcast in every frame,
   the angel as light-presence only. Reasoning: a full cast sheet +
   distinctness check for a figure with ~14s of screen time invites drift
   risk for no gain, and the averted-face treatment keeps the beat's
   focus where the narration puts it — on the WORD spoken over her
   ("that holy thing... shall be called the Son of God"), not on a face.
   A deliberate reverence choice, not an omission.
6. **The fruit** (s13 only): text-locked inline prompt (one bite gone,
   fallen in dust), ≤2 appearances, no anchor.
7. **The study desk** (s26/32/38/39/40/46/60/66 — a recurring SETTING per
   the census discipline): ONE desk base still (aged wood, lamp, page
   field), re-dressed per spread. Build once, chain everywhere.
8. **The naming page** (s34-36): one paper prop still. NOT a grid of
   cells (the Flap lesson: grid-of-cells reads as a scoreboard on sight)
   — an open inquest page where stamps and pressed lines accumulate
   vertically.
9. **Horizon/dawn plates** (s59/s67): check the wilderness banks for
   thread-neutral plates before rendering new.
10. **The gold thread**: ONE shared $0 overlay implementation (draw-on /
    gleam-pass), reused across s21/22/25/28/37/45/62/63/64/66 — an
    implementation asset, not an image.

**Doctrine guards carried into every render** (narration's own locked
constraints + repo conventions): KJV-strict **"it shall bruise thy head"**
(never "he") on every lettered appearance; serpent-as-Satan is stated by
the NAMING PAGE quoting Rev 12:9 — the Eden-scene serpent is drawn as the
Genesis creature, and the identification happens exactly where the canon
makes it (M4), never painted back into the garden frames; darkness at the
cross is unnatural darkness, NOT storm weather; cross staging wound-free
(living-light rule — Kling regenerates blood), no titulus text ever
rendered (never animate writing / no generated lettering); the empty tomb
holds light and folded linen, no figure, no invented visitors
(empty-place rule); Gal 4:4/Luke 1:35 render the annunciation reverently
with no halo iconography beyond the established light-presence register;
gold leaf stays His glory only — the serpent, the curse, the desk never
borrow it; red-letter (s22) ARRIVES WHOLE per LAW 1.

## 5b. Style-variant swaps considered (production_approved: sl10/12/13/14/16)

Standing rule: Style 1 is the spine; variants are occasional deliberate
insert pages. Verdicts for THIS episode:

- **sl13 charcoal-and-eraser — CANDIDATE, s08** ("everything good is
  coming apart"): its beat signal is memory/erasure/soft-grief, and s08
  is goodness being visibly UN-made — erasure is the register. Caveat:
  Adam/Eve were never identity-tested in this variant (the bake-off
  scored Moses/Jesus only) — needs one test render against
  `adam_ref.png`/`eve_ref.png` before committing; ships in spine style
  if it drifts.
- **sl16 foreground occlusion (hidden-observer) — CANDIDATE, s65**: Day
  of Atonement rejected sl16 because its story forbade watchers; THIS
  story's spine IS hiding — the hidden-observer grammar would make the
  viewer the hider at exactly the beat that says "your safest move is to
  stay hidden in the trees." Same identity-test caveat (no figures in
  frame helps — likely safe). User eye decides.
- **sl14 torn-paper depth planes — REJECTED**: the torn-paper vocabulary
  is reserved for ONE meaning in this film — the landing tear (s71).
- **sl12 scratchboard inversion — REJECTED**: the s50-56 darkness chain
  must read as one continuous world; restyling a middle frame breaks it,
  and sl12's gold-leaf conflict flag lands exactly where the gold edge
  is doctrinally load-bearing (s51/s56).
- **sl10 overhead plan — REJECTED**: s10/s41 already get plain overhead
  staging in spine style; spending a variant there buys nothing the
  camera plan doesn't already do.

Net: zero committed, two candidates (s08 sl13, s65 sl16) pending identity
test + user eye.

## 6. Rough cost — order-of-magnitude, for the go/no-go conversation only

No API called, no estimator run. Same unit prices as the Day of Atonement
plan (~$0.30-0.50/still NBP; Seedance ~$0.65 real-bill / Kling ~$1.20):

- **Stills:** ~60-64 new renders (66 spreads minus shared art: s23 holds
  s22's card, s31 letters over s30, s34-36 share one page, s53 re-frames
  s51, s47/60/66 re-dress the study-copy/desk bases, s68 re-frames s15)
  × $0.30-0.50 ≈ $18-32; gap/anchor renders (serpent anchor, tomb,
  Golgotha wide, risen Christ, desk base, naming page, 2 variant tests)
  ~7-9 ≈ $2-4.5; re-roll contingency 20-25% ≈ +$5-8.
  **Subtotal ~$25-45.**
- **Animation:** RECOUNTED 2026-08-07 directly from the table (the
  independent-review panel caught the prior tally undercounting both) —
  **10 Kling** (s2,6,11,17,24,30,43,48,51,69) × ~$1.20 ≈ $12 + **20
  Seedance** (s4,8,10,12,18,20,28,33,41,44,46,50,54,57,58,62,64,65,67,70)
  × ~$0.65 ≈ $13; the 12 card spreads and 26 $0-device spreads take the
  deterministic path. **Subtotal ~$25-30.** No NSFW/fallback contingency
  line yet (s51's cross render has a real fail-closed risk per the
  living-light rule) — add ~$3-5 headroom.
- **Total rough range ~$53-80, midpoint ~$65** — still below Day of
  Atonement's ~$80-95 midpoint, though the panel's math corrections push
  this slightly above the original $50-75 estimate. NOT a quote — run the
  real estimator and get an explicit OK before any stills batch, per
  ask-before-spending.

**Staged build order (added 2026-08-07, per the panel's "no risk-tier test
gate" finding and this episode's own retrospective fix #7):** do not batch
all 66 spreads at once, even after spend approval.
0. **Real alignment-correction pass** on the sub-turn seams — a proper
   `_s5_align.py`/`_s5b_spread_windows.py`-equivalent for this episode
   (doesn't exist yet; DoA's own versions are the pattern to follow),
   using `_alignment.json`'s real per-word timestamps, not word-count
   proportions. Priority order: turn 27 (s39-42, spot-checked above,
   confirmed meaningfully off), turn 34 (s50-52, contains s51 — CORRECTED
   2026-08-07: the panel caught s51 is a sub-split of turn 34's
   353.657-371.210 span, NOT already-real as first claimed; it needs this
   pass BEFORE it renders since it becomes the Jesus anchor for later
   spreads), and turn 36 (s54-59), then the narrator lead-ins inside
   s32-34a, then the remaining ~14 turns before THEIR spreads are batched.
   Only s06 and s16 sit on genuinely already-real single-turn boundaries
   (turns 4 and 9, no sub-split) — s51 does NOT.
1. Serpent anchor (`world/serpent_ref.png`) — approve before anything
   using it.
2. s06 (the hardest identity+motion still: Adam+Eve+serpent, multi-figure
   Kling acting spread) — full QC before the serpent's other ~17
   appearances build on top of it.
3. s16 — `hunt_and_lock` is now a real, promoted, tested device
   (`panel_animator/hunt_and_lock.py`, verified 2026-08-07 against an
   existing still with no new spend) — still worth a first real-content
   render as the standard device confirmation, cheap.
4. s51 (Jesus, out of table order — see §5's render-order fix) — approve
   before s42/s43/s50/s53-56/s64/s66/s71.
5. THEN batches of ~10 spreads, `motion_lint.py` + `_layer_check.py` run
   after every batch per SKILL.md sec.8b, not saved up for the end.

## 7. Open questions for the user (before rendering starts)

1. **Serpent treatment** (§5.1): real creature, judgment framing,
   camera-looks-down rule, shed-skin as the beaten-enemy symbol — OK?
2. **The naming page** (s34-36): three lettered beats back-to-back as ONE
   continuous accumulating page — a designed exception to
   never-two-lettered-adjacent. OK, or split with narrative spreads?
3. **Mary with no anchor** (face always averted, angel as light) — OK?
4. **Variant candidates** (s08 sl13, s65 sl16) — spend 2 test renders, or
   ship both in spine style?
5. **Spend**: rough ~$53-80, midpoint ~$65 (synced to §6 2026-08-07 — this
   was previously inconsistent between sections, the panel's own catch);
   real quote to follow at stills time.
6. (Mechanical) s05's end extends 33.03 → 33.80 at the alignment-
   correction pass — no rework, its hold just breathes longer.

This is a SIGNIFICANT plan — per the standing enforced-independent-review
rule it should go to the external panel (`independent_review.py --type
plan`) before the build session starts.
