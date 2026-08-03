# Bronze Serpent LONG — living-sketchbook full-length pilot plan

**Status: PLANNING ONLY. No renders, no spend, no code that calls a paid API.**
This is the first attempt to build a full-length (6-8+ min) film in the
living-sketchbook style. Source narration: the LOCKED, ALREADY-VOICED
long-form "Types & Shadows" deep-dive at
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\EW04_Bronze_Serpent\v1\narration.md`
(7 beats) — **not** the short Eyewitness script that
`poc_living_sketchbook\bronze_serpent\` already shipped (that POC is a
DIFFERENT, shorter (69.31s) narration; it is the pacing/register reference
only, not the source text).

---

## 1. Real turn-by-turn timing — the arithmetic

### 1a. Source data and the trap in it

`longform\EW04_Bronze_Serpent\v1\narration.meta.json` has a `turns[]` array
with 21 turns, each carrying `natural_seconds` and `final_seconds`. The
task's own warning ("the field's exact meaning needs verifying... don't
guess") was correct to raise — **`final_seconds` is not usable as a
per-turn duration.** Proof:

- `sum(natural_seconds)` across all 21 turns = **575.68s**, which equals the
  file's own `natural_total_seconds` field exactly. This field is internally
  consistent.
- `sum(final_seconds)` across all 21 turns = **137.86s** — matches neither
  `pause_total_seconds` (14.7s) nor `natural_total_seconds` (575.68s) nor
  anything else in the file. It is not a real total of anything. The values
  in that column are almost certainly a bookkeeping artifact from the synth
  script (looks like a shifted-index bug: turn *i*'s `final_seconds` is
  turn *i-1* or *i-3*'s `natural_seconds`, or a bare pause value 0.3/0.4).
  **Conclusion: ignore `final_seconds` entirely.**

### 1b. What the real numbers are (ffprobe-verified, not just JSON-trusted)

Spot-checked `natural_seconds` against the actual per-turn files in
`longform\EW04_Bronze_Serpent\v1\_turns\` with `ffprobe`:

| turn file | `natural_seconds` (JSON) | ffprobe duration |
|---|---|---|
| 00_witness.mp3 | 61.12 | 61.120000 |
| 01_scripture.mp3 | 5.28 | 5.280000 |
| 09_the_LORD.mp3 | 12.64 | 12.640000 |
| 12_witness.mp3 | 178.16 | 178.160000 |
| 13_jesus.mp3 | 13.6 | 13.600000 |
| 20_witness.mp3 | 72.0 | 72.000000 |
| `_silence_pre_400ms.mp3` | (pre-pause) | 0.400000 |
| `_silence_post_300ms.mp3` | (post-pause) | 0.300000 |

Exact match on all six spot-checked turns. **`natural_seconds` is the real,
correct per-turn spoken duration.** The pause files confirm the model:
`per_turn_synth.py`'s `dialogue_per_turn_with_narrator_atempo` mode
concatenates, for every one of the 21 turns in order:

```
[0.4s pre-pause] + [turn audio, natural_seconds long] + [0.3s post-pause]
```

21 turns x 0.7s pause each = **14.7s**, exactly matching
`pause_total_seconds`. `575.68 + 14.7 = 590.38` exactly matches
`final_total_seconds`. `ffprobe` on the full `narration.mp3` confirms
**590.380000s** file duration. Three independent numbers agree — the model
is right.

### 1c. Cumulative start/end per turn

Running the formula above turn-by-turn (`speak_start = cumulative + 0.4`,
`speak_end = speak_start + natural_seconds`, `cumulative = speak_end + 0.3`)
gives the exact speech window for every turn. Final cumulative = **590.38s**,
matching the file exactly — the whole chain is internally consistent, not
just the endpoints.

| turn | speaker | natural_s | speak window (s) | content |
|---|---|---|---|---|
| 0 | witness | 61.12 | 0.40 – 61.52 | Beat1 (all) + Beat2 opening |
| 1 | scripture | 5.28 | 62.22 – 67.50 | "the soul of the people was much discouraged..." |
| 2 | witness | 7.84 | 68.20 – 76.04 | "Discouraged turned to anger..." |
| 3 | scripture | 10.88 | 76.74 – 87.62 | [the people] "Wherefore have ye brought us up..." |
| 4 | witness | 15.84 | 88.32 – 104.16 | "I had heard that voice before..." |
| 5 | scripture | 7.2 | 104.86 – 112.06 | "And the LORD sent fiery serpents..." |
| 6 | witness | 24.8 | 112.76 – 137.56 | Beat2 close ("Fiery, we named them...") + Beat3 open ("Then the people came to me...") — **straddles the beat boundary** |
| 7 | scripture | 9.12 | 138.26 – 147.38 | [the people] "We have sinned..." |
| 8 | witness | 15.76 | 148.08 – 163.84 | "So I did the one thing a mediator can do..." |
| 9 | **the_LORD** | 12.64 | 164.54 – 177.18 | [the LORD] "Make thee a fiery serpent..." |
| 10 | witness | 18.4 | 177.88 – 196.28 | "He did not promise to take the serpents away..." |
| 11 | scripture | 12.0 | 196.98 – 208.98 | "And Moses made a serpent of brass..." |
| 12 | witness | 178.16 | 209.68 – 387.84 | Beat3 close + **all of Beat4 + all of Beat5** — one huge continuous turn, no quote breaks |
| 13 | **jesus** | 13.6 | 388.54 – 402.14 | [Jesus] John 3:14-15 combined (red-letter) |
| 14 | witness | 30.64 | 402.84 – 433.48 | "There it was. My serpent was never the point of it..." |
| 15 | scripture | 7.36 | 434.18 – 441.54 | "being made a curse for us..." (Gal 3:13) |
| 16 | witness | 14.24 | 442.24 – 456.48 | "He bore, upon that pole..." |
| 17 | **jesus** | 6.88 | 457.18 – 464.06 | [Jesus] "And I, if I be lifted up..." |
| 18 | witness | 42.88 | 464.76 – 507.64 | "...the riddle of the look..." through the Nehushtan/Hezekiah detail |
| 19 | scripture | 9.04 | 508.34 – 517.38 | John 3:16 |
| 20 | witness | 72.0 | 518.08 – 590.08 | Beat7 (all) — the CTA |

Beat boundaries do **not** line up cleanly with turn boundaries in three
places (turn 6 straddles Beat2/Beat3; turn 12 straddles Beat3/Beat4/Beat5).
Where that happens, the sub-turn split points below are estimated by
**proportional character count** within the turn (the turn's own text
divided at the beat seam, converted to seconds at that turn's own
chars-per-second rate) — this is an estimate, not a measurement. Exactly
like `poc_living_sketchbook\bronze_serpent\_TIMING.md` did for the short (it
flagged its own metadata as stale and needed a real WhisperX pass to get
word-exact cuts), **this plan's turn-level timestamps are hard, ffprobe-
verified numbers; the sub-turn spread cut points below are planning
estimates that should be corrected against a real forced-alignment pass
before final build**, the same discipline this project already used once.

---

## 2. The full spread table — all 590.38s, all 7 beats

**68 spreads.** Columns: # / start–end (s) / dur / Beat / Type / What it
shows / Assets needed / Device.

Type legend: **NS**=narrative single-figure · **MV**=multi-vignette ·
**IP**=insert-page · **VC**=verse-card · **LAND**=landing.
Assets: "Moses"/"Jesus" = existing sketch-style cast anchors (REUSE, $0).
"LORD-presence" = new unseen-presence treatment (see §4). "Hezekiah" /
"calf" = new (see §4). "crowd" = anonymous background figures, discipline
carried from the short's s04 face-count fix, no new cast sheet.

| # | Start–End (s) | Dur | Beat | Type | Shows | Assets | Device |
|---|---|---|---|---|---|---|---|
| 1 | 0.40–7.50 | 7.1 | 1 | NS | Wide establishing: aged Moses, wilderness camp behind | Moses | none |
| 2 | 7.50–17.00 | 9.5 | 1 | MV | Triptych memory-vignette: rod-to-serpent / Red Sea split / water from the rock | Moses | none |
| 3 | 17.00–21.50 | 4.5 | 1 | NS | Close on Moses's eyes, haunted, "follows me still" | Moses | none |
| 4 | 21.50–27.50 | 6.0 | 1 | NS | THE ICON: pole in the sand, bronze serpent revealed | Moses, bronze-serpent (reuse short's design) | **blue-line** (cold-open page-being-made reveal) |
| 5 | 27.50–32.50 | 5.0 | 1 | NS | Graves being dug, the dying, grief — wide | crowd | none |
| 6 | 32.50–37.10 | 4.6 | 1 | NS | Close: a dying man's empty/reaching hand, then an eye — the "look not climb" theme image | crowd (1 figure) | none |
| 7 | 37.10–43.00 | 5.9 | 2 | NS | Wide: the freed-but-ungrateful camp (CORRECTED 2026-08-01: dropped "the mixed multitude" — that term is Exodus 12:38/Numbers 11:4's label for the generation that left Egypt at year 0-2, and per Numbers 14:29-35 that whole 20-and-over generation had already died in the wilderness by Numbers 21/year 40 — not sourced from the narration either) | crowd | none |
| 8 | 43.00–53.00 | 10.0 | 2 | NS | Wide: the wandering column, going round Edom, barren road, no end in sight | crowd | none |
| 9 | 53.00–61.52 | 8.5 | 2 | NS | Manna falling, faithfully, being turned from/scorned | crowd | none |
| 10 | 62.22–67.50 | 5.3 | 2 | VC | Verse card (Scribed Ink): "the soul of the people was much discouraged because of the way" | crowd (bg art) | none |
| 11 | 68.20–76.04 | 7.8 | 2 | NS | Crowd turns angry, toward Moses and toward heaven | crowd, Moses | none |
| 12 | 76.74–87.62 | 10.9 | 2 | VC | Verse card: [the people] "Wherefore have ye brought us up..." — single unbroken quote | crowd | slow push-in camera (insert_page_camera-style pan; the quote arrives and stays whole per LAW 1, don't chop it into two cards) |
| 13 | 88.32–98.00 | 9.7 | 2 | MV | Memory-vignette: the sea / the rock / the golden calf under the cloud at Sinai | Moses, **calf** (new, dull/tarnished — never sacred-gold) | none |
| 14 | 98.00–104.16 | 6.2 | 2 | NS | Something slides in the dust between the tents — first hint of the serpents | none new | none |
| 15 | 104.86–112.06 | 7.2 | 2 | VC | Verse card: "And the LORD sent fiery serpents among the people..." + serpents among the camp | crowd | none |
| 16 | 112.76–117.00 | 4.2 | 2 | NS | Close: the bite, "burned like a coal" — heat/glow, not graphic wound | crowd (1 figure) | none |
| 17 | 117.00–125.00 | 8.0 | 2 | MV | Vignette: a strong man collapsed + a mother cradling a child — restrained, no gore | crowd (2 figures max, per short's s04 face-count fix) | none |
| 18 | 125.00–131.61 | 6.6 | 2 | NS | Moses alone, hands empty, no remedy — atmosphere beat | Moses | none |
| 19 | 131.61–137.56 | 6.0 | 3 | NS | The people kneel before Moses, posture shifts from anger to contrition | crowd, Moses | none |
| 20 | 138.26–147.38 | 9.1 | 3 | VC | Verse card: [the people] "We have sinned, for we have spoken against the LORD..." | crowd | none |
| 21 | 148.08–154.00 | 5.9 | 3 | NS | Moses interceding, kneeling, arms raised in prayer | Moses | none |
| 22 | 154.00–163.84 | 9.8 | 3 | NS | Moses's face — surprise the LORD did not simply remove the serpents; listening | Moses | none |
| 23 | 164.54–169.00 | 4.5 | 3 | NS | **The LORD's presence appears** — Moses shields his eyes/kneels before an overwhelming radiant light, NO figure, NO face | Moses, **LORD-presence** (new) | **candle-only** (radial light budget on the drawn light source; this is the beat the device description literally names — "fear closes it down, the turn opens it") |
| 24 | 169.00–177.18 | 8.2 | 3 | VC | Illuminated Rubric verse card (gold dropped-cap, formal register — this is the film's central command): [the LORD] "Make thee a fiery serpent, and set it upon a pole..." | LORD-presence (bg glow) | none |
| 25 | 177.88–184.00 | 6.1 | 3 | NS | Moses processing — no medicine offered, negation imagery (empty hands, no jar) | Moses | none |
| 26 | 184.00–192.00 | 8.0 | 3 | NS | Moses looking at a live serpent on the ground — resolve forming | Moses | none |
| 27 | 192.00–196.28 | 4.3 | 3 | NS | Close-up hands, beginning the forge (shot-variety floor: close hands) | Moses (hands) | none |
| 28 | 196.98–204.00 | 7.0 | 3 | NS | **Acting spread**: Moses hammering the bronze serpent into shape, extreme close, motion completes then holds | Moses (hands), bronze-serpent | optional **raking-light** (light catching the hammered bronze) |
| 29 | 204.00–208.98 | 5.0 | 3 | NS | The pole now stands; the first bitten look up, first healing | crowd, bronze-serpent | none |
| 30 | 209.68–228.25 | 18.6 | 3 | MV | Payoff: a man's fever breaks as he looks up at the pole — "no payment, no climbing" | crowd, bronze-serpent | none |
| 31 | 228.25–233.41 | 5.2 | 4 | NS | Close on Moses's face turning the question over: "Why a serpent?" | Moses | optional ink-stamp display text ("WHY A SERPENT?") — governed under the episode's <=6 display-stamp budget |
| 32 | 233.41–259.03 | 25.6 | 4 | NS | Wide/mid: the serpent on its pole, silhouetted against the camp at dusk — "the very shape of what was striking them down" | bronze-serpent | slow drift/push camera (long single-hold shot — let the camera do the work, per this plan's own pacing rule) |
| 33 | 259.03–272.61 | 13.6 | 4 | MV | Vignette: strong man / child / dying elder, all lifting their eyes the same way — universality of the cure | crowd (3 vignette figures) | none |
| 34 | 272.61–284.83 | 12.2 | 4 | NS | Moses walking alone at dusk, the riddle "walking home with him every evening" | Moses | none, no-figure-adjacent atmosphere beat |
| 35 | 284.83–293.25 | 8.4 | 5 | NS | Close on elderly Moses's face, direct-address register begins: "I will be honest with you" | Moses | none |
| 36 | 293.25–314.62 | 21.4 | 5 | NS | Mid: a proud man turning away from the pole in the background while others look — "a cure so simple is its own stumbling-block" | crowd | none |
| 37 | 314.62–325.48 | 10.9 | 5 | NS | FLASHBACK, soft-focus/silhouette: grinding the golden calf to powder. **CORRECTED 2026-08-01** (was going to build a "younger Moses" for this — wrong, see §4 item 4): Moses was ~80 (Exodus 7:7) at the golden calf, only ~40 years younger than his ~120-year-old Numbers-21 self — SAME elder cast anchor for both, not a distinct younger face. Calf must read as a large public cult object (see §4 item 3), not a small figurine. | Moses (silhouette, existing elder anchor), **calf** (dull, non-sacred gold, LARGE scale) | none |
| 38 | 325.48–344.31 | 18.8 | 5 | NS | THE DREAD IMAGE: Moses holding the bronze serpent, staring at it — the tablets of the law referenced small in-frame | Moses, bronze-serpent | none |
| 39 | 344.31–350.29 | 6.0 | 5 | NS | Close, night: Moses sleepless, "had God bidden the very sin I had just broken?" | Moses | **candle-only** (single lamp, dread register — distinct tonal use from spread 23's glory-light) |
| 40 | 350.29–364.51 | 14.2 | 5 | NS | Moses's resolve returning, hand on the bronze but eyes lifted — "the look that took Him at His word" | Moses, bronze-serpent | none |
| 41 | 364.51–382.80 | 18.3 | 5 | NS | Wide: Moses at the camp's edge, looking down a long empty road into darkness — "a signpost... pointing past itself" | Moses | slow push-out (suggest depth/time) |
| 42 | 382.80–387.84 | 5.0 | 5 | NS | Close on hands finishing the forge, quiet — bookends spread 28 | Moses (hands), bronze-serpent | none |
| 43 | 388.54–402.14 | 13.6 | 6 | **IP** | INSERT PAGE 1: Scholar's-Margin two-panel typology diagram (Numbers 21 / John 3), red-letter John 3:14-15 lettered whole (LAW 1) — reuses the short's proven s08 device exactly | Jesus (small, teaching-by-night register), Nicodemus (anonymous seeker, no cast sheet needed) | **lift_away** transitioning IN (mirrors short's s07->s08 exactly); **insert_page_camera** reading-order pan; $0 — no paid animation on this spread |
| 44 | 402.84–410.00 | 7.2 | 6 | NS | Moses's realization: the bronze serpent's shadow, symbolically cross-shaped on the ground — restrained, not garish | Moses, bronze-serpent | none |
| 45 | 410.00–420.00 | 10.0 | 6 | NS | Golgotha: Christ lifted on the cross, wide, reverent, restrained, no gore (echoes short's s10) | Jesus | none |
| 46 | 420.00–425.00 | 5.0 | 6 | NS | Paired composition: bronze serpent + the cross together in one frame — the film's thesis image | bronze-serpent, Jesus | none |
| 47 | 425.00–433.48 | 8.5 | 6 | NS | Christ on the cross, reverent, leading into the Gal 3:13 quote | Jesus | none |
| 48 | 434.18–441.54 | 7.4 | 6 | VC | Verse card: "being made a curse for us: for it is written, Cursed is every one that hangeth on a tree" | Jesus (bg) | none |
| 49 | 442.24–451.00 | 8.8 | 6 | NS | Christ lifted, radiant register beginning — "bore the judgment... taken in our place" | Jesus | none |
| 50 | 451.00–456.48 | 5.5 | 6 | NS | Close, leading into Jesus's own words | Jesus | none |
| 51 | 457.18–464.06 | 6.9 | 6 | NS | Red-letter, arrives whole: [Jesus] "And I, if I be lifted up from the earth, will draw all men unto me" — Christ radiant, light drawing figures toward Him, restrained/symbolic | Jesus, crowd (distant, drawn toward light) | none |
| 52 | 464.76–475.54 | 10.8 | 6 | NS | Moses reflecting, resolved: "it was never the bronze; it was the looking that God honoured" | Moses | none |
| 53 | 475.54–478.92 | 3.4 | 6 | NS | Brief, close on Moses: "I know that now better than I once wished to" | Moses | none |
| 54 | 478.92–486.11 | 7.2 | 6 | NS | TIME SHIFT (generations later): people burning incense before the enshrined serpent — idolatry creeping in | crowd, bronze-serpent (now enshrined/venerated — visually distinct staging from its earlier plain forge/pole treatment) | soft dissolve transition IN (time-shift grammar per SKILL §6 — not a hard cut) |
| 55 | 486.11–493.51 | 7.4 | 6 | NS | **Hezekiah** — a YOUNG king, mid-to-late 20s (2 Kings 18:2, corrected 2026-08-01, was unspecified) — breaks the bronze serpent to pieces — decisive, corrective, NOT shameful | **Hezekiah** (new) | **impact-burst** (ink impact-star + speed lines on the strike, synced to a real SFX hit) |
| 56 | 493.51–498.18 | 4.7 | 6 | NS | Moses's voice affirms: "he was right to break it. The power was never in my handiwork" | Moses | none |
| 57 | 498.18–507.64 | 9.5 | 6 | NS | Transition back to Christ/gold register: "the power was in the God who said look and live" | Jesus, Moses | none |
| 58 | 508.34–517.38 | 9.0 | 6 | VC | Illuminated Rubric verse card (most famous verse — full ceremony): John 3:16 | Jesus (bg, radiant) | none |
| 59 | 518.08–524.00 | 5.9 | 7 | NS | Moses direct-address: "So hear me — be still. Do not rush past this as my people rushed past the manna" | Moses | none |
| 60 | 524.00–532.00 | 8.0 | 7 | MV | Vignette: strong men trying to walk the fire off, each failing in his own way — "none was healed by his own hands" | crowd (2-3 vignette figures) | none |
| 61 | 532.00–539.00 | 7.0 | 7 | NS | Intimate close on Moses: "That is you. That is me" | Moses | none |
| 62 | 539.00–544.50 | 5.5 | 7 | NS | Close, resolute: "you were never asked to" | Moses | none |
| 63 | 544.50–553.00 | 8.5 | 7 | MV | Christ radiant lifted; three small figures below — the least, the last, a child turning his head — looking up | Jesus, crowd (3 vignette figures, distinct staging from spread 33's echo of the same "least/child/elder" idea) | none |
| 64 | 553.00–559.00 | 6.0 | 7 | NS | Pause beat, near-silence: "Sit with that" | Moses | optional **held-breath** energy-envelope pass (quiets the page here, if the assembler wants a true silence beat) |
| 65 | 559.00–565.00 | 6.0 | 7 | NS | Christ, plain and open: "costs you nothing but a look" | Jesus | none |
| 66 | 565.00–576.00 | 11.0 | 7 | NS | Moses turning the question directly to the viewer — most intimate direct-address of the film | Moses | none |
| 67 | 576.00–585.00 | 9.0 | 7 | **IP** | INSERT PAGE 2 (Gilded Proclamation echo, reuses short's s12 device): "Not to the bronze, nor to me — but to Jesus" — ONE unified gold-ground composition, dull bronze serpent small/earthbound foreground, Christ radiant in gold leaf above/behind, no labels | bronze-serpent, Jesus | **lift_away** transitioning in; $0 camera pan only, no paid animation |
| 68 | 585.00–590.08 (+ >=3.0s hold, added at assembly) | 5.1 + hold | 7 | **LAND** | THE LANDING: "Look to Him, and live." Torn-page device (tear_hole), gold light from beneath the tear, Christ's silhouette distant | Jesus (silhouette) | **tear_hole** (the landing's own device, mandatory); sacred stillness hold; optional ribbon-marker A/B (ships only if it wins) |

**Sum check:** spreads 1-9 = 61.12s, 10 = 5.28s, 11 = 7.84s, 12 = 10.88s,
13-14 = 15.84s, 15 = 7.2s, 16-18 = 18.85s, 19 = 5.95s, 20 = 9.12s, 21-22 =
15.76s, 23-24 = 12.64s, 25-27 = 18.4s, 28-29 = 12.0s, 30-42 = 178.16s, 43 =
13.6s, 44-47 = 30.64s, 48 = 7.36s, 49-50 = 14.24s, 51 = 6.88s, 52-57 =
42.88s, 58 = 9.04s, 59-68 = 72.0s. These are exactly the 21 real turn
durations from §1c, re-partitioned into 68 spreads — the table's total
speech time is guaranteed to equal 575.68s (+ 14.7s of built-in inter-turn
pause + the assembly-added >=3.0s landing hold) because every spread
boundary sits inside a turn whose real duration is already
ffprobe-verified.

---

## 3. Spread count and pacing — why 68, not ~119 and not 14

**Total: 68 spreads over 590.38s. Average 8.7s/spread**, ranging from
3.4s (a one-line beat) to 25.6s (a single held wide shot with camera
drift). This is **not** a proportional scale-up of the short. A naive
scale-up (14 spreads x 590.38/69.31 = ~119 spreads at the short's own
~5s/spread pace) is explicitly rejected, for three reasons:

1. **Cost and QC load compound linearly with spread count, not with
   runtime.** 119 spreads means 119 full-res 4-point still-QC passes (the
   short's own `_STILLS_REVIEW.html` shows this is where real defects hide
   — the s04 crowd-face-count bug and the s12 wound-streak bug were both
   caught only at full resolution, not on a contact sheet) and up to 119
   paid animation jobs. That is roughly 8.5x the short's real ~$16 spend for
   a film that is meaningfully more expensive to make right, not just
   longer.
2. **A ~5s average is a SHORT's rhythm — hook-paced, built to be watched
   once at speed.** A 9:50 contemplative deep-dive is a different viewing
   contract: the viewer has settled in. Holding a well-composed spread
   longer and lettering the camera move do the work (slow push, drift,
   raking light, candle-only) reads as *deliberate*, not static, in a
   documentary-sketch register — the same instinct behind this project's
   own `longform-camera-variety-moves` practice elsewhere in the pipeline.
3. **The content itself is not evenly dense.** Turn 12 alone (Beat4 + Beat5,
   178.16s, no quote breaks) is the psychological and doctrinal core of the
   piece — Moses's dread over the second-commandment echo. That earns
   slower, held spreads (this plan's Beat4/5 section averages ~13.7s/spread
   across 13 spreads) so the wrestling can actually breathe. The Beat1 hook
   (9 spreads over 61.12s, ~6.8s avg) and the Beat7 CTA build (10 spreads
   over 72.0s, ~7.2s avg) are deliberately faster and more direct, because
   those sections are doing hook/persuasion work, not reflection work. The
   two insert pages (43, 67) each hold a single locked composition for
   9-13.6s with $0 camera-pan motion only, no re-cut — consistent with
   LAW 1 (the Word/a locked composition arrives and stays whole).

So the pacing is **content-driven and variable (3.4s-25.6s), averaging
8.7s** — roughly 1.7x the short's own per-spread hold time, while the total
spread count grew only ~4.9x (68/14) against an 8.5x runtime growth. The
difference between those two ratios (4.9x vs 8.5x) is exactly the
"hold longer, use camera movement" adjustment the task asked for, applied
for a stated content reason at every section rather than as a flat rule.

---

## 4. New production variables vs. the short (asset list)

The short's own asset list (Moses, the bronze serpent, a generic crowd) does
**not** cover this narration. New for this pilot:

1. **THE LORD, unseen presence (spreads 23-24).** No sketch-style
   precedent exists — the short's own script has no direct-speech LORD
   quote at all (confirmed: grepped `short/narration.md`, it has none). This
   project DOES already have a locked doctrinal convention elsewhere
   (`ref_library/characters/THE_LORD.json`, used 21x in the inked style):
   *"the unseen presence of the LORD shown only as overwhelming radiant
   golden light... a towering pillar of glory and shadow... never a human
   face or body."* Recommend porting that same convention into the sketch
   register rather than inventing a new one — no risk of an anthropomorphic
   depiction, consistent with the red-letter-speaker rule (first-person
   divine speech = THE LORD, never visualized as a human figure here).
   Needs: a locked treatment paragraph + 1-2 reference light-study renders
   (no fixed "face" to anchor, so cheaper than a character cast sheet).
2. **Hezekiah / "a good king of Judah" (spread 55).** Entirely new
   character, unnamed in the script, one appearance only (the Nehushtan
   detail — 2 Kings 18:4 — is in the long-form's Beat 6 and was NOT in the
   short at all). Needs a minimal canon description (8th-century-BC king of
   Judah, humble/righteous register, breaking the serpent — not a full
   recurring cast sheet since he appears once).
   **AGE, added 2026-08-01 (fact-check pass):** 2 Kings 18:2 states
   Hezekiah was 25 ("twenty and five years old") when he began to reign;
   the Nehushtan-breaking (18:4) sits in the same undated reform block as
   his other opening acts, before the chapter's first dated regnal year
   (18:9), and 2 Chronicles 29:3 dates the parallel reform cluster to "the
   first year of his reign." **Hezekiah must render as a young king in his
   mid-to-late 20s, vigorous — NOT an elderly greybeard "wise king"
   stereotype.** Same category of risk as the Moses catch — locking this
   before any render, not after. Memory: [[feedback-verify-character-age-scale-before-render]].
3. **The golden calf (spreads 13, 37).** New OBJECT asset, appears twice.
   **Doctrine-load-bearing rendering rule, ported from the short's own
   playbook** (`_STILLS_REVIEW.html`'s s08/s12 notes: "gold = His glory
   only... gilding the [wrong object] would visually claim it was holy"):
   the calf must render dull/tarnished bronze-and-base-metal, NEVER in the
   sacred gold-leaf register reserved for Christ/the LORD's presence. This
   is the same discipline the short already proved out for the bronze
   serpent itself; it now needs to extend to a second idol object.
   **SCALE, added 2026-08-01 (user catch):** Scripture states no exact
   size, but the gold came from the whole camp's jewelry (Exodus 32:2-3,
   a nation numbering 600,000+ men) and the whole camp gathered to worship
   it (Exodus 32:6) — this reads as a substantial public cult object, not
   a hand-sized figurine. Render LARGE.
4. **RESOLVED 2026-08-01 (was an open question) — no second Moses anchor.**
   Verified against KJV: Exodus 7:7 states Moses was 80 ("fourscore") at
   the Exodus; Deuteronomy 34:7 states he was 120 when he died; Numbers
   33:38 pins the Bronze Serpent to "the fortieth year" after the Exodus.
   So Moses was ~120 at the Bronze Serpent and ~80 (not "middle-aged") at
   the golden calf, which happens **roughly 3-4 months after the Exodus**
   (Exodus 19:1 places Sinai arrival in "the third month"; Exodus 24:18
   gives Moses' forty-day mountain stay before the calf incident —
   corrected 2026-08-01 fact-check pass, was previously the looser "within
   about a year"; doesn't change any age math) — only ~40 years before the
   Bronze Serpent, BOTH elderly. A distinct "younger Moses" anchor was
   built on 2026-08-01 on the wrong assumption and is superseded (see
   `cast/MOSES_YOUNGER.md`, kept for the record only). Spread 37 reuses the
   SAME elder `cast/MOSES.md` / `moses_ref.png` anchor as every other
   spread — see that file's own "Golden-calf flashback" section for the
   corrected canon note. Memory: [[feedback-verify-character-age-scale-before-render]].
5. **Reuse confirmed, no new work needed:** Moses (cast/MOSES.md +
   moses_ref.png) and **Jesus** (cast/JESUS.md + jesus_ref.png already
   exist at the repo-level `poc_living_sketchbook/cast/` — built for
   another episode, directly reusable here with zero new cast cost). The
   crowd-face-count discipline (<=2-3 sharp faces, rest turned
   away/shadow/downcast) the short had to learn the hard way on s04 carries
   forward as a standing rule, not a new asset.
6. **Nicodemus / the night seeker (spread 43)** — minor, background-only,
   no dedicated cast sheet recommended; treat as an anonymous
   shadowed secondary figure, same convention this project already uses
   for minor secondary figures elsewhere (e.g. the eyewitness-format
   SEEKER precedent).

---

## 5. Rough cost/time estimate — ROUGH, for a go/no-go conversation only

**This is order-of-magnitude, not a quote.** No API has been called; no
credits estimator has been run against real prompts.

**Stills** (68 spreads, nano_banana_pro register per this project's
`stills`/long-form-Christ-face convention, ~$0.30-0.50/still per CLAUDE.md):
- 66 standard single-composition stills: 66 x $0.30-0.50 = **$19.80-$33.00**
- 2 insert-page compositions (historically 2-3 render attempts each on the
  short's own s08/s12 — budget ~3x a single still): **$1.80-$3.00**
- New assets (THE LORD light-study, Hezekiah, golden calf, ~3 renders):
  **$0.90-$1.50**
- Re-roll contingency (~20-25%, this project's own standing practice, and
  the short genuinely needed it — s04's crowd-face fix, s12's 3 attempts):
  **+$4.50-$7.50**
- **Stills subtotal: ~$27-$45**

**Animation** (66 of 68 spreads need paid animation — the 2 insert pages
use the $0 deterministic `insert_page_camera` pan instead, per the
already-proven short pattern):
- ~56 calm/single-figure spreads -> Seedance tier (~$0.15-0.75/clip per
  CLAUDE.md's locked comic-grid-tiering price range, real bills tending
  toward the low half of quote): **~$8-$42**
- ~10 multi-figure/action/crowd spreads (serpent attack, the forge acting
  spread, Hezekiah breaking the idol, multi-vignette compositions) -> Kling
  tier (~$0.75-1.50/clip): **~$7.50-$15.00**
- **Animation subtotal: ~$16-$57** (midpoint using this project's own
  measured "~half of Seedance quote bills for real" pattern from the
  living-sketchbook cost model: ~56 x $0.65 + ~10 x $1.20 = **~$48**)

**Total rough range: ~$45-$102, midpoint ~$75-$90.** Compare to the short's
own *measured* (not estimated) actual cost of ~$16 for 12 spreads + 2
anchors — this pilot's spread count grew ~4.9x (68/14) and its measured
cost should grow roughly in step with that (not with the 8.5x runtime
growth), which is consistent with the ~5x range landed on here.

**Time:** no hard data exists to estimate this precisely (the short's own
build history spans several dated planning rounds, not a single sitting).
Qualitatively: full-res 4-point still QC (§8a of the living-sketchbook
skill) on 68 stills plus the new-asset cast work is realistically the
dominant time cost, not raw render time — expect several distinct
production sessions, not one continuous build, mirroring how the short
itself was actually built in rounds.

---

## 6. Summary for the go/no-go conversation

- **68 spreads**, 8.7s average (range 3.4-25.6s), content-paced not
  duration-scaled.
- **New assets needed:** THE LORD unseen-presence treatment, Hezekiah
  (one-off), golden calf (dull, non-sacred-gold, doctrine-load-bearing),
  plus one open question (does the golden-calf flashback need a second
  Moses age-lock, or does silhouette suffice). Moses and Jesus are both
  already-built reusable cast anchors — zero new cost there.
- **Rough spend: ~$45-$102 (midpoint ~$75-$90)**, roughly 5x the short's
  own measured ~$16, tracking the ~4.9x spread-count growth rather than the
  8.5x runtime growth.
- Doctrine carried forward unchanged from the short: bronze serpent and
  golden calf both stay OFF the sacred-gold register (gold = Christ's glory
  only); the LORD is never shown as a human figure; red-letter Jesus
  quotes arrive whole, never letter-by-letter; the Nehushtan/Hezekiah beat
  is staged as vindication ("he was right to break it"), not shame.
