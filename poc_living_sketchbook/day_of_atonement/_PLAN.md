# Day of Atonement LONG — living-sketchbook spread-by-spread plan

**STATUS: PLANNING ONLY. No renders, no spend, no code that calls a paid API.**

Second full-length living-sketchbook film, following the Bronze Serpent LONG
pilot (`C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_living_sketchbook\bronze_serpent_long\_PLAN.md`
is the structural template; the pacing here is reasoned fresh from THIS
story's content, not copied). Source narration: the LOCKED, ALREADY-VOICED
eyewitness long "The Two Goats" (Aaron, Leviticus 16, 7 beats, v1.3
panel-passed) at
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\EW01_Two_Goats\v1\narration.md`,
audio at
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\EW01_Two_Goats\v1\narration.mp3`.

---

## 1. Real turn-by-turn timing — the arithmetic

### 1a. The trap in the handed-down model (found, verified, corrected)

The planning brief said to use the Bronze Serpent pause model: a 0.4s
pre-pause + 0.3s post-pause around every turn
(`cumulative = prior_end + 0.4 + natural_seconds + 0.3`). **That model is
WRONG for this file.** Three independent numbers prove it:

1. `narration.meta.json` states it outright: `pre_quote_pause_seconds: 0.0`,
   `post_quote_pause_seconds: 0.0`, `pause_total_seconds: 0.0`,
   `final_total_seconds: 588.64` = `natural_total_seconds: 588.64`. This
   synth run (2026-06-28, `dialogue_per_turn_with_narrator_atempo`,
   target 900s, no atempo applied anywhere) was made with ZERO inter-turn
   padding.
2. The 31 per-turn `natural_seconds` sum to exactly **588.64s** (verified by
   hand: group sums 215.44 + 200.16 + 173.04 = 588.64), and `ffprobe` on the
   full `narration.mp3` reports exactly **588.640000s**. If the 0.4/0.3
   pauses were present, the file would be 588.64 + 31×0.7 = **610.34s** — it
   is not.
3. The `_silence_pre_400ms.mp3` / `_silence_post_300ms.mp3` files DO sit in
   `_turns\` (ffprobe: 0.400000s / 0.300000s) — they exist as synth-script
   furniture but contributed nothing to this concat, per the meta's own
   pause totals.

**Conclusion: cumulative = plain running sum of `natural_seconds`, no pause
terms.** Same discipline as the Bronze Serpent plan's §1a (which threw out
`final_seconds` there): trust the file, not the brief. One practical
consequence worth carrying into build: with no inter-turn silence, every
spread cut at a turn boundary lands with ZERO audio breathing room —
lettering overlays need their hard exit BEFORE the window ends (letterer
law, the Two Goats short already got burned by a 0.6s overlay bleed), and
the assembler cannot count on a pause to hide a late cut.

### 1b. Verification of the per-turn numbers themselves

Spot-checked the given `natural_seconds` against the actual files in
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\EW01_Two_Goats\v1\_turns\`
with ffprobe: `00_witness.mp3` 87.920000, `01_the_LORD.mp3` 18.320000,
`14_witness.mp3` 106.640000, `30_witness.mp3` 35.440000 — exact match, and
the meta's 31-entry `turns[]` (`final_seconds` == `natural_seconds` on every
row here, `atempo_applied: false` throughout — no shifted-index artifact in
THIS file) matches the directory listing: 31 files, indices 00–30, speaker
sequence witness / the_LORD(01) / witness / scripture alternating exactly as
the narration.md speaker order reads. Turn-to-content mapping was
additionally confirmed by the meta's per-turn `chars` counts against the
narration text (e.g. turn 15 = 136 chars = the TWO stacked Hebrews quotes,
53 + 82 + newline; turn 19 = 53 chars = Isaiah 53:6b; turn 26 = 565 chars =
the Beat 7 opening block). Every mapping below is char-verified, not
eyeballed.

### 1c. Cumulative start/end per turn (no-pause model)

`start(i) = Σ natural_seconds(0..i-1)`, `end(i) = start(i) + natural(i)`.
Final cumulative = **588.64s**, matching the file exactly.

| turn | speaker | natural_s | window (s) | content |
|---|---|---|---|---|
| 0 | witness | 87.92 | 0.00 – 87.92 | **Beat 1 (all)** + **Beat 2 opening** (Nadab/Abihu through "Moses brought me the word:") — straddles the beat seam |
| 1 | **the_LORD** | 18.32 | 87.92 – 106.24 | [the LORD] Lev 16:2 "Speak unto Aaron thy brother, that he come not at all times…" — red-letter, ARRIVES WHOLE (LAW 1) |
| 2 | witness | 27.04 | 106.24 – 133.28 | "That was my charge… I did not bear their guilt… it ran red through everything I did:" |
| 3 | scripture | 3.92 | 133.28 – 137.20 | Lev 17:11 "for it is the blood that maketh an atonement for the soul." |
| 4 | witness | 18.88 | 137.20 – 156.08 | Beat 2 close ("Something innocent had to die…") + **Beat 3 open** ("Let me tell you what I did… cast lots over them:") — straddles |
| 5 | scripture | 7.28 | 156.08 – 163.36 | Lev 16:8 "And Aaron shall cast lots upon the two goats…" |
| 6 | witness | 12.08 | 163.36 – 175.44 | "The first goat I killed… through the veil, into the thick dark… sprinkled it before the mercy seat:" |
| 7 | scripture | 6.72 | 175.44 – 182.16 | Lev 16:15 "…bring his blood within the vail." |
| 8 | witness | 11.76 | 182.16 – 193.92 | "But the second goat I did not kill. I laid both my hands upon its living head…" |
| 9 | scripture | 21.52 | 193.92 – 215.44 | Lev 16:21 (the long confession verse, 291 chars) |
| 10 | witness | 8.24 | 215.44 – 223.68 | "…watched it go, smaller and smaller…" |
| 11 | scripture | 6.24 | 223.68 – 229.92 | Lev 16:22 "…unto a land not inhabited." |
| 12 | witness | 9.28 | 229.92 – 239.20 | **Beat 4 opens exactly here**: "Here is the thing that never let me rest… one sin offering — yet it took two goats." |
| 13 | scripture | 7.04 | 239.20 – 246.24 | Lev 16:5 "…two kids of the goats for a sin offering." |
| 14 | witness | 106.64 | 246.24 – 352.88 | **Beat 4 remainder + ALL of Beat 5 + Beat 6 opening** — the monster turn, straddles two beat seams |
| 15 | scripture | 10.48 | 352.88 – 363.36 | Heb 10:3 + Heb 10:4 — TWO verses in ONE turn ("remembrance again… " / "not possible that the blood of bulls and of goats…") |
| 16 | witness | 18.72 | 363.36 – 382.08 | "It was a shadow… The body came. There came a Man, Jesus… He entered once, and it was finished." |
| 17 | scripture | 10.40 | 382.08 – 392.48 | Heb 9:12 "Neither by the blood of goats and calves, but by his own blood…" — the thesis verse |
| 18 | witness | 19.20 | 392.48 – 411.68 | "By His own blood He paid the price… as I had laid the people's sin on the goat… Isaiah… wrote it:" |
| 19 | scripture | 3.92 | 411.68 – 415.60 | Isa 53:6 "and the LORD hath laid on him the iniquity of us all." |
| 20 | witness | 21.20 | 415.60 – 436.80 | "That is why there were two… both were finished in one Priest. They led Him outside the city… The letter says:" |
| 21 | scripture | 7.68 | 436.80 – 444.48 | Heb 13:12 "…suffered without the gate." |
| 22 | witness | 9.52 | 444.48 – 454.00 | "I always stood at my work; there was no chair behind that veil. But this Priest finished it, and sat down:" |
| 23 | scripture | 7.28 | 454.00 – 461.28 | Heb 10:12 "…sat down on the right hand of God." |
| 24 | witness | 14.56 | 461.28 – 475.84 | "And the veil I trembled before… was torn the very hour He died… Matthew… records it:" |
| 25 | scripture | 6.24 | 475.84 – 482.08 | Matt 27:51 "…the veil of the temple was rent in twain from the top to the bottom." |
| 26 | witness | 44.00 | 482.08 – 526.08 | **Beat 7 opens exactly here**: "So hear me… Do not come to me… Come to Jesus… So David sang in his psalm, long before:" |
| 27 | scripture | 6.24 | 526.08 – 532.32 | Ps 103:12 "As far as the east is from the west…" |
| 28 | witness | 14.88 | 532.32 – 547.20 | "The veil I trembled before is torn… The way in is thrown wide open… That same letter says:" |
| 29 | scripture | 6.00 | 547.20 – 553.20 | Heb 10:19 "…boldness to enter into the holiest by the blood of Jesus." |
| 30 | witness | 35.44 | 553.20 – 588.64 | Beat 7 close — the question, the invitation, "Walk in — the holiest is open, and Jesus is already inside." |

Beat seams that fall MID-turn (three of them: Beat1/2 inside turn 0;
Beat2/3 inside turn 4; Beat4/5 and Beat5/6 both inside turn 14) are
estimated below by **proportional character count at that turn's own
chars-per-second rate** — turn 0 runs at 13.62 c/s, turn 4 at 15.15 c/s,
turn 14 at 13.54 c/s. Resulting beat map:

| Beat | window (s) | dur | note |
|---|---|---|---|
| 1 — I was there | 0.00 – ~46.4 | ~46.4 | seam estimated (Beat 1 ≈ 632 of turn 0's 1197 chars) |
| 2 — The world | ~46.4 – ~141.2 | ~94.8 | seam estimated (61 of turn 4's 286 chars close Beat 2) |
| 3 — The act | ~141.2 – 229.92 | ~88.7 | ends exactly at turn 11/12 boundary |
| 4 — The strange detail | 229.92 – ~269.4 | ~39.5 | seam estimated (313 of turn 14's 1444 chars) |
| 5 — The wrestling | ~269.4 – ~327.0 | ~57.6 | seam estimated (777 of turn 14's chars) |
| 6 — The reveal | ~327.0 – 482.08 | ~155.1 | ends exactly at turn 25/26 boundary |
| 7 — The invitation | 482.08 – 588.64 | 106.56 | exact both ends |

Exactly as the Bronze Serpent plan flagged for itself: **turn-level
timestamps above are hard, ffprobe-verified numbers; sub-turn spread cut
points in §2 are planning estimates that must be corrected against a real
forced-alignment (WhisperX) pass before final build.**

---

## 2. The full spread table — all 588.64s, all 7 beats

**76 spreads.** Type legend: **NS**=narrative single-focus ·
**MV**=multi-vignette · **VC**=verse-card/lettered spread · **LAND**=landing.
Assets: Aaron / Moses / Jesus = existing repo-level sketch cast anchors
(`C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_living_sketchbook\cast\`,
REUSE $0). tabernacle / veil / holyofholies / altar / goat = existing world
anchors (`…\poc_living_sketchbook\world\`, REUSE $0). "crowd" = anonymous
figures, ≤2-3 sharp faces (standing discipline). NEW assets are bolded and
listed in §5. Boundaries inside a turn carry the §1c estimate caveat.

| # | Start–End (s) | Dur | Beat | Type | Shows | Assets | Device |
|---|---|---|---|---|---|---|---|
| 1 | 0.00–3.2 | 3.2 | 1 | NS | Cold open: Aaron's face arrives on the page — "I am Aaron, the first high priest" | Aaron | **blue-line** (page-being-made reveal; the man himself IS the hook) |
| 2 | 3.2–9.3 | 6.1 | 1 | NS | Wide: the tabernacle in its linen courtyard, desert light — "where no other man on earth was permitted to go" | tabernacle | none |
| 3 | 9.3–13.9 | 4.6 | 1 | NS | The garments of gold and glory laid aside — breastplate, blue robe, gold plate set down (their ONLY appearance, per AARON.md's exception note) | Aaron (golden-garment exception) | none |
| 4 | 13.9–22.2 | 8.3 | 1 | NS | Aaron in plain white linen, tying the girdle, bronze laver behind — "like a servant, like a man with nothing to boast of" | Aaron | slow push-in |
| 5 | 22.2–26.8 | 4.6 | 1 | NS | Walking toward the veil, alone in the Holy Place gloom — "my heart in my throat" | Aaron, veil (distant) | none |
| 6 | 26.8–34.5 | 7.7 | 1 | NS | Behind the curtain: the mercy seat, the cloud-glow above it — the room otherwise EMPTY | holyofholies, **LORD-glow** | none (glow breathes via animation discipline, not a device) |
| 7 | 34.5–39.4 | 4.9 | 1 | NS | Wide: the whole nation outside the courtyard, hushed, holding its breath | crowd, tabernacle | none |
| 8 | 39.4–46.4 | 7.0 | 1 | NS | The curtain falls shut behind Aaron; close on his face in the dark — "not certain I would come out alive" | Aaron, veil | none |
| 9 | 46.4–49.6 | 3.2 | 2 | NS | Hard register drop: Aaron's grief, close — "I lost two of my own sons" | Aaron | none |
| 10 | 49.6–54.3 | 4.7 | 2 | NS | Nadab and Abihu with censers, strange fire glowing (event stage 1) | **Nadab+Abihu** | multi-stage hard cut (with 11) |
| 11 | 54.3–58.9 | 4.6 | 2 | NS | Struck down before the LORD — fire/light from above, NO figure, no gore (Lev 10:2; stage 2, the cut tells the event) | Nadab+Abihu, LORD-glow | multi-stage hard cut |
| 12 | 58.9–65.6 | 6.7 | 2 | NS | The cousins carrying the wrapped bodies out of the camp (Lev 10:4-5 — NOT Aaron carrying them, per the narration's own v1.3 fix) | crowd (2 bearers) | none |
| 13 | 65.6–72.3 | 6.7 | 2 | NS | Aaron at the tabernacle DOOR-curtain (the plain needlework one, not the veil), gripping the robe he is forbidden to rend | Aaron, tabernacle (door-curtain) | sl13 charcoal-and-eraser insert page CANDIDATE — see §6, user decision |
| 14 | 72.3–82.0 | 9.7 | 2 | NS | Close: Aaron's hand at the veil's edge, trembling — "I heard it in my bones every time I reached for the veil" | Aaron (hands), veil | none |
| 15 | 82.0–87.92 | 5.9 | 2 | NS | Moses comes to Aaron bearing the word — two old brothers, the charge between them | Moses (~80 register, same anchor per MOSES.md flashback note), Aaron | none |
| 16 | 87.92–106.24 | 18.3 | 2 | VC | [the LORD] Lev 16:2 — Illuminated Rubric, the film's central charge. LAW 1: red-letter ARRIVES WHOLE (~1.5s in), never letter-by-letter. Cloud-glow on the mercy seat behind the lettering. LONGEST single card of the film — the slow push does the work for the remaining ~16s, per the Bronze Serpent "don't chop the card" precedent | holyofholies (bg), LORD-glow | whole-arrival Illuminated Rubric + slow push-in |
| 17 | 106.24–112.3 | 6.1 | 2 | NS | Aaron squared at the veil — "to stand at the veil for the people and not be consumed" | Aaron, veil | none |
| 18 | 112.3–122.3 | 10.0 | 2 | NS | Aaron with the basin, bringing blood FOR HIS OWN SIN first — the mediator who is himself a sinner, never a substitute | Aaron, basin (text-locked prop) | none |
| 19 | 122.3–133.28 | 11.0 | 2 | NS | The bronze altar mid-ministry, blood at its base, smoke rising — "it ran red through everything I did" (restrained, ritual not gore) | altar, Aaron | none |
| 20 | 133.28–137.20 | 3.9 | 2 | VC | Verse card, Scribed Ink: Lev 17:11 "for it is the blood that maketh an atonement for the soul." (58 glyphs in ~3.5s — fast but inside Scribed Ink's proven pace) | altar (bg) | none |
| 21 | 137.20–141.2 | 4.0 | 2 | NS | The goat's innocent face, close — "Something innocent had to die, or none of us could draw near" (first goat appearance, foreshadow) | goat | none |
| 22 | 141.2–148.5 | 7.3 | 3 | NS | Close on Aaron's old hands — "I did it year after year and could have done it in the dark" (ritual muscle-memory; shot-variety close-hands) | Aaron (hands) | none |
| 23 | 148.5–156.08 | 7.6 | 3 | NS | The two goats brought before Aaron — ONE design, both animals, indistinguishable ON PURPOSE (the lot decides, not the look — TABERNACLE_WORLD.md §7) | goat ×2, Aaron, crowd (handlers) | none |
| 24 | 156.08–163.36 | 7.3 | 3 | VC | Verse card, Scribed Ink: Lev 16:8 — the two lots in Aaron's open palm behind the lettering | Aaron (hands), goat ×2 (bg) | none |
| 25 | 163.36–167.4 | 4.0 | 3 | NS | The slaying at the altar — knife and goat at the altar base, staged, wound-FREE (living-light rule: Kling regenerates blood; render none) (event stage 1) | altar, goat, Aaron | multi-stage hard cut (with 26, 27) |
| 26 | 167.4–171.4 | 4.0 | 3 | NS | The basin carried THROUGH the veil into the thick dark — threshold shot, Aaron half-swallowed by the curtain (stage 2) | Aaron, veil, basin | multi-stage hard cut |
| 27 | 171.4–175.44 | 4.0 | 3 | NS | Sprinkling before the mercy seat, alone in the dark chamber, cloud-glow (stage 3) | holyofholies, Aaron, LORD-glow | multi-stage hard cut |
| 28 | 175.44–182.16 | 6.7 | 3 | VC | Verse card, Scribed Ink: Lev 16:15 "…bring his blood within the vail." over the dark interior | holyofholies (bg) | none |
| 29 | 182.16–188.1 | 5.9 | 3 | NS | **ACTING SPREAD 1**: Aaron lays BOTH hands on the live goat's head — the motion completes, then holds (the rite's iconic gesture) | Aaron, goat | designed acting spread (Kling tier) |
| 30 | 188.1–193.92 | 5.8 | 3 | NS | The confession — different framing from 29: Aaron's bowed face, mouth moving, eyes shut, hands still on the head | Aaron, goat | none |
| 31 | 193.92–215.44 | 21.5 | 3 | VC | Verse card, Scribed Ink LIVE-WRITE: Lev 16:21 — the film's longest verse (291 glyphs over 21.5s ≈ 13.5 glyph/s): the scribe's hand writes the whole confession in real time as the voice reads it, hands-on-head image ghosted behind, slow drift. LONGEST spread of the film, deliberately | Aaron+goat (bg art) | full-duration Scribed Ink reveal + slow drift |
| 32 | 215.44–223.68 | 8.2 | 3 | NS | The goat led away by the fit man, smaller and smaller into the wilderness — wide, receding | goat, **fit man** (anonymous, no sheet) | none |
| 33 | 223.68–229.92 | 6.2 | 3 | VC | Lev 16:22 lettered over the SAME wilderness horizon, now EMPTY — the goat gone (continuity pair with 32; composite card, no page-flip) | wilderness wide (bg) | none |
| 34 | 229.92–239.20 | 9.3 | 4 | MV | The riddle recap: two soft memory vignettes — goat at the altar / goat receding — around Aaron's turning face | Aaron, goat ×2 (vignettes) | optional **INK STAMP** "WHY TWO?" (inside the ≤6 budget) |
| 35 | 239.20–246.24 | 7.0 | 4 | VC | Verse card, Scribed Ink: Lev 16:5 "…two kids of the goats for a sin offering." — ONE offering, two creatures | goat ×2 (bg) | none |
| 36 | 246.24–255.4 | 9.2 | 4 | NS | Night, Aaron's tent: the two lots turned over in his lamplit hand — "why two? Why not put both to death?" (object insert) | Aaron (hands), lots | none |
| 37 | 255.4–264.6 | 9.2 | 4 | NS | Split composition: the altar (the price paid) ‖ the empty horizon (the carrying away) — "two things at once that no single creature could hold" | altar, wilderness | none |
| 38 | 264.6–269.4 | 4.8 | 4 | NS | Aaron walking home at dusk, camp behind — "the riddle of it followed me home" (atmosphere beat) | Aaron | none |
| 39 | 269.4–276.9 | 7.5 | 5 | NS | Direct-address close, honesty register: "I will be honest with you… I obeyed, and I believed" | Aaron | none |
| 40 | 276.9–288.0 | 11.1 | 5 | NS | The people going home CLEAN — evening camp, lightened faces, real relief (Lev 16:30 was REAL, not failed — render it warm, per the narration's own v1.3 correction) | crowd | none |
| 41 | 288.0–297.2 | 9.2 | 5 | MV | The repetition: the same rite in three vignettes, distinguished by season/light (dawn/dusk/haze — variety per panel-variety discipline), "every year I came back and did the whole thing again" | Aaron, altar, goat (vignettes) | none |
| 42 | 297.2–307.5 | 10.3 | 5 | NS | Object insert: the basin scrubbed clean and set ready AGAIN, the folded linen waiting — "the need returned with each new year, as faithful as the feast" | basin, linen (props) | none |
| 43 | 307.5–314.0 | 6.5 | 5 | NS | Old Aaron at night, a single lamp, the fear he dared not speak — the film's dread register | Aaron | **candle-only** (the light budget closes down with the fear — this beat is the device's literal design case) |
| 44 | 314.0–323.9 | 9.9 | 5 | NS | The pointing image: altar smoke rising and leaning past the frame's edge, Aaron's eyes following it — "I was only ever pointing… at some greater atonement my own hands could never reach" | altar, Aaron | none |
| 45 | 323.9–327.0 | 3.1 | 5 | NS | Near-silence: Aaron a small silhouette before the veil — "I was a sign. I did not yet know of what." | Aaron, veil | held-breath quiet point (episode envelope, see §4 note) |
| 46 | 327.0–334.5 | 7.5 | 6 | NS | "I did not see the answer in my own day" — Aaron aged, dim, the veil unchanged behind him | Aaron, veil | none |
| 47 | 334.5–342.6 | 8.1 | 6 | NS | The cross-time turn: light arrives from beyond the page's edge, the palette warms — "by the light that came long after I laid down my office" (EW-INV-11 is a NARRATION device; the visual grammar is just this time-shift) | Aaron | halftone dissolve IN (time-shift grammar, SKILL §6) |
| 48 | 342.6–352.88 | 10.3 | 6 | NS | The insufficiency image: the little basin at the foot of the towering veil — "the blood I carried could never finish it" | basin, veil | none |
| 49 | 352.88–363.36 | 10.5 | 6 | VC | DOUBLE card, Scribed Ink: Heb 10:3 then Heb 10:4 letter onto the SAME page in sequence as the voice reaches each — two verses, one spread, attributed ("that later word — the letter to the Hebrews") | veil (bg) | stacked two-verse Scribed Ink |
| 50 | 363.36–368.3 | 4.9 | 6 | NS | THE SHADOW: a long shadow thrown across the sand by something beyond the frame — "a shadow waits for the body that casts it" (no-figure atmosphere) | wilderness | none |
| 51 | 368.3–382.08 | 13.8 | 6 | NS | **JESUS 1 — the pivot**: the true High Priest entering once, gold register arriving — "The body came. There came a Man, Jesus… He entered once, and it was finished." FIRST Jesus render: once approved, it becomes the SECOND reference chained into every later Jesus spread (multi-pose identity lock, SKILL §2). Longest Jesus hold — camera push does the work | Jesus | slow push + gold-leaf arrival |
| 52 | 382.08–392.48 | 10.4 | 6 | VC | Illuminated Rubric (formal peak 2 of 2): Heb 9:12 "Neither by the blood of goats and calves, but by his own blood…" — gold dropped cap, the film's thesis verse, full ceremony | Jesus (bg, entering) | Illuminated Rubric |
| 53 | 392.48–399.0 | 6.5 | 6 | NS | The cross — the price paid, reverent, restrained, no gore — "bearing in His own death the judgment our sin had earned" (Jesus pose 2) | Jesus | none |
| 54 | 399.0–411.68 | 12.7 | 6 | MV | The two layings-on, paired: Aaron's hands on the goat's head ‖ the guilt laid on Christ — a fine GOLD THREAD runs from the OT vignette to the Christ figure; in the last ~2s an OLDER foxed leaf settles onto the page ("Isaiah, the prophet who came after me, wrote it:" — the attribution line IS the leaf's arrival) | Aaron+goat (vignette), Jesus | **Thread Device** (its designed OT→NT purpose) + **Elder Leaf** settle |
| 55 | 411.68–415.60 | 3.9 | 6 | VC | Isa 53:6 letters onto the settled elder leaf, elder register, thread still running to Christ — the episode's ONE Elder Leaf (≤1, never landing ✓). TIMING FLAG: 53 glyphs in ~3.5s is the top of comfortable Scribed Ink pace; the leaf MUST pre-settle during 54 or this card is rushed | elder leaf, Jesus | Elder Leaf + Thread Device carry-through |
| 56 | 415.60–426.3 | 10.7 | 6 | NS | THE ANSWER — the film's thesis image: both goat-memories small and earthbound below; Christ central and radiant holding BOTH halves — "both were finished in one Priest" | Jesus, goat ×2 (small, dull register — gold stays His) | none |
| 57 | 426.3–436.80 | 10.5 | 6 | MV | Without the gate ‖ outside the camp: Christ led out of the city gate / the sin-offering's body carried outside the camp and burned (Lev 16:27 — the SLAIN goat's body, NOT the scapegoat; the narration's own locked distinction) | Jesus, **city-gate plate**, crowd | none |
| 58 | 436.80–444.48 | 7.7 | 6 | VC | Verse card, Scribed Ink: Heb 13:12 "…suffered without the gate." | city gate (bg) | none |
| 59 | 444.48–454.00 | 9.5 | 6 | NS | NO CHAIR: the Holy of Holies bare except the ark (the anchor's emptiness IS this line's payoff — TABERNACLE_WORLD.md §5), Aaron standing at his work, forever standing | holyofholies, Aaron | none |
| 60 | 454.00–461.28 | 7.3 | 6 | VC | COMPOSITE card: Heb 10:12 "…sat down on the right hand of God." lettered over Christ SEATED in glory (Jesus pose 3) — the standing/seated contrast lands visually, no separate card page | Jesus (seated, gold register) | composite verse-over-art |
| 61 | 461.28–468.9 | 7.6 | 6 | NS | The veil WHOLE — the same curtain design as spreads 5/8/14, recall register — "the curtain that shut every man but one out, one day a year" | veil | none |
| 62 | 468.9–475.84 | 6.9 | 6 | NS | THE TEAR — hard cut from 61: the same veil torn from the TOP to the bottom, gold light through the rent, no human hand in frame (the cut tells the event; never a morph) | veil (torn state, chained from same anchor) | multi-stage hard cut (whole→torn) |
| 63 | 475.84–482.08 | 6.2 | 6 | VC | COMPOSITE card: Matt 27:51 lettered over the torn veil itself, light spilling through the rent behind the words | veil (torn, bg) | composite verse-over-art |
| 64 | 482.08–489.5 | 7.4 | 7 | NS | "So hear me — and be still a moment" — Aaron utterly still, direct address, the page quiets | Aaron | held-breath quiet point |
| 65 | 489.5–501.0 | 11.5 | 7 | MV | The old apparatus receding: goat / yearly altar / linen priest as desaturating memory vignettes — "Do not come to me. Do not come to a goat…" | Aaron, goat, altar (vignettes) | none |
| 66 | 501.0–507.6 | 6.6 | 7 | NS | The contrast cut: Christ radiant — "None of it ever stayed done. He can. Come to Jesus — the High Priest who finished it." | Jesus | none |
| 67 | 507.6–516.6 | 9.0 | 7 | NS | The scapegoat echo TRANSFIGURED: sin carried away into gold-lit distance — "not held down for another year — carried away" (distinct staging from 32: light, not desolation) | goat (receding, gold-lit), wilderness | none |
| 68 | 516.6–526.08 | 9.5 | 7 | NS | Vast wide: east horizon / west horizon, dawn at one edge — "as far as the east is from the west… So David sang in his psalm" | wilderness wide | none |
| 69 | 526.08–532.32 | 6.2 | 7 | VC | COMPOSITE card: Ps 103:12 lettered across the same horizon sky | wilderness (bg) | composite verse-over-art |
| 70 | 532.32–538.7 | 6.4 | 7 | NS | The torn veil, held open, gold light steady — "no hand will ever sew it shut again" | veil (torn) | none |
| 71 | 538.7–547.20 | 8.5 | 7 | NS | THE WAY OPEN: through the rent, the mercy seat visible beyond, light pouring OUT toward the viewer — "not for one man one day a year, but for you" | veil (torn), holyofholies | none |
| 72 | 547.20–553.20 | 6.0 | 7 | VC | Verse card, Scribed Ink: Heb 10:19 "…boldness to enter into the holiest by the blood of Jesus." — the invitation verse | veil (torn, bg) | none |
| 73 | 553.20–558.3 | 5.1 | 7 | NS | Aaron steps ASIDE from the torn veil, gesturing the viewer forward — the mediator no longer needed | Aaron, veil (torn) | none |
| 74 | 558.3–571.0 | 12.7 | 7 | NS | The most intimate direct-address hold of the film: Aaron's face, every year's fear gone — "will you come in?" (long held close; camera and the held-breath envelope do the work) | Aaron | slow push-in |
| 75 | 571.0–583.3 | 12.3 | 7 | NS | **ACTING SPREAD 2**: Christ at the open veil, hand extending toward the viewer — the motion completes, then holds — "now, on His. Come." | Jesus, veil (torn) | designed acting spread (Kling tier, fail-closed Jesus QC) |
| 76 | 583.3–588.64 (+ ≥3.0s hold at assembly) | 5.3 + hold | 7 | **LAND** | THE LANDING: "Walk in — the holiest is open, and Jesus is already inside." The page tears open AS the veil — tear_hole, gold light from beneath the paper, Jesus within the opening. Sacred stillness (glow breathes only), INV-26 hold, INV-27 watermark | Jesus, veil (torn) | **tear_hole** (mandatory landing device — and for THIS story the torn page and the torn veil are the SAME image, the toolkit's best possible fit); optional ribbon-marker A/B (ships only if it wins) |

**Sum check (spreads re-partition the 31 verified turns exactly):**
spreads 1–15 = turn 0 (87.92) · 16 = turn 1 (18.32) · 17–19 = turn 2 (27.04)
· 20 = turn 3 (3.92) · 21–23 = turn 4 (18.88) · 24 = turn 5 (7.28) · 25–27 =
turn 6 (12.08) · 28 = turn 7 (6.72) · 29–30 = turn 8 (11.76) · 31 = turn 9
(21.52) · 32 = turn 10 (8.24) · 33 = turn 11 (6.24) · 34 = turn 12 (9.28) ·
35 = turn 13 (7.04) · 36–48 = turn 14 (106.64) · 49 = turn 15 (10.48) ·
50–51 = turn 16 (18.72) · 52 = turn 17 (10.40) · 53–54 = turn 18 (19.20) ·
55 = turn 19 (3.92) · 56–57 = turn 20 (21.20) · 58 = turn 21 (7.68) · 59 =
turn 22 (9.52) · 60 = turn 23 (7.28) · 61–62 = turn 24 (14.56) · 63 = turn
25 (6.24) · 64–68 = turn 26 (44.00) · 69 = turn 27 (6.24) · 70–71 = turn 28
(14.88) · 72 = turn 29 (6.00) · 73–76 = turn 30 (35.44). Every spread
boundary sits inside a turn whose duration is ffprobe-verified, so the
table's total is guaranteed = **588.64s** (+ the assembly-added ≥3.0s
landing hold). 15+1+3+1+3+1+3+1+2+1+1+1+1+1+13+1+2+1+2+1+2+1+1+1+2+1+5+1+2+1+4
= **76**.

---

## 3. Spread count and pacing — why 76, not 68 copied and not ~119 scaled

**76 spreads over 588.64s. Average 7.75s/spread, range 3.1s–21.5s.**
Bronze Serpent landed on 68 at 8.7s average for an almost identical runtime
(590.38s) — this plan does NOT copy that number, and the difference is
driven by measurable properties of THIS narration:

1. **Quote density forces a higher spread floor.** This narration has **15
   quote turns (16 verses — turn 15 carries two Hebrews verses) out of 31
   turns**; Bronze Serpent had 10 quote turns out of 21, and its quotes were
   concentrated in two stretches. A lettered page is its own composition —
   every quote turn hard-forces at least one spread boundary on each side.
   That alone puts ~15 spreads on the board before any narrative choice is
   made, and it is why the average here (7.75s) sits below Bronze Serpent's
   8.7s: the verse-card cadence chops the timeline finer whether or not the
   imagery wants it.
2. **This story is more procedural than psychological.** Beat 1 is a vesting
   RITE (lay aside gold → wash → linen → walk → enter — five distinct
   physical states) and Beat 3 is a liturgy (two goats → lots → slay → carry
   → sprinkle → hands → confess → send — each act named by the text, several
   commanded by the quoted verses themselves). Procedure cuts; each act is
   its own still. Compare Bronze Serpent, whose center of mass was one
   178-second unbroken interior monologue (its turn 12) that EARNED
   25-second held wides. This story's longest unbroken witness turn is
   106.64s and even that one crosses three beats. So: **more, shorter
   spreads in Beats 1–3 (5.8/7.3/7.4s averages — hook and rite), longer
   holds where the reflection actually lives (Beat 5 wrestling 8.2s avg,
   Beat 6 reveal 8.6s avg — and the film's four longest single spreads, 21.5
   / 18.3 / 13.8 / 12.7s, all sit on its four heaviest moments: the Lev
   16:21 confession live-write, the LORD's charge, the Jesus pivot, and the
   final "will you come in?").**
3. **A naive proportional scale-up is rejected for the same three reasons
   Bronze Serpent's plan gave**, which all still hold: QC and cost compound
   per spread, not per second (76 full-res 4-point QC passes is already the
   dominant time cost; ~119 at a short's ~5s pace would be half again more
   money and eye-work for a worse film); a ~10-minute contemplative piece is
   a different viewing contract from a 60s short (held compositions + camera
   motion read as deliberate, not static); and the content is not evenly
   dense (Beat 4's riddle gets 5 spreads at 7.9s while the same 39.5s at
   short-pace would demand 8 — nothing in the text wants those extra cuts).

Beat-by-beat: B1 8 spreads/5.8s avg (hook) · B2 13/7.3s (grief+charge) ·
B3 12/7.4s (the rite) · B4 5/7.9s (riddle) · B5 7/8.2s (wrestling — slowest
narrative section) · B6 18/8.6s (reveal — most spreads AND longest holds;
see §4) · B7 13/8.2s (CTA — accelerating cuts but three long intimate holds
where the ask lands).

---

## 4. Beat 6's quote stack — the flagged pacing risk, and the spacing plan

The brief described Beat 6 as "4 NT/OT quotes." **The verified count is
worse: SEVEN verses in SIX scripture turns inside one ~155s beat** (Hebrews
10:3 + 10:4 stacked in turn 15, then Heb 9:12, Isa 53:6, Heb 13:12, Heb
10:12, Matt 27:51), plus two more in Beat 7 (Ps 103:12, Heb 10:19). Nine
verse reveals in the film's back third is the single biggest monotony risk
in this episode — six near-identical Scribed Ink card pages in a row would
read as a slideshow. The plan absorbs it three ways, all with EXISTING
locked grammar (SKILL §5 — no new device):

1. **Register rotation, never two lettered spreads adjacent.** Beat 6's
   quote spreads run: stacked double card (49) → THREE narrative spreads →
   Illuminated Rubric (52) → two narrative → Elder Leaf (55) → two narrative
   → plain card (58) → one narrative → composite-over-art (60) → two
   narrative → composite-over-art (63). Maximum run of lettered spreads: 1.
   Five distinct treatments across six quote spreads.
2. **The two most ceremonial registers are spent exactly twice each, at the
   two peaks.** Illuminated Rubric: the LORD's charge (16) and the Heb 9:12
   thesis (52) — nothing else gets the gold dropped cap. Elder Leaf: Isa
   53:6 only — the episode's one OT-echo citation, thread-connected to
   Christ, per that device's own ≤1 budget.
3. **The last three quote treatments of the film (60, 63, 69) are
   composites** — the verse letters onto the story image itself (seated
   Christ / torn veil / east-west horizon) instead of turning to a card
   page. The film's climax accelerates visually instead of stacking pages,
   and the torn-veil verse literally shares the frame with the torn veil.

Two timing flags inside this scheme, both for the build stage: **spread 55**
(Isa 53:6, 3.92s) only works if the elder leaf pre-settles during spread
54's tail — the attribution line "Isaiah… wrote it:" is spoken there and IS
the leaf's arrival cue; and **spread 16** (Lev 16:2, 18.32s) is a single
whole-arrival card held ~16s after the text lands — the slow push plus the
breathing cloud-glow must carry it (precedent: Bronze Serpent's 10.9s
single-card hold, same LAW-1 don't-chop rule; this one is longer, worth an
eye-check at assembly). A single episode-level **held-breath** envelope pass
(quiet points at 45 and 64, the two "be still" beats) is the one pacing
infrastructure device proposed.

---

## 5. Assets — existing (reuse, $0) vs. gaps

**Existing, already built this session or earlier — REFERENCE, do not
rebuild** (all under
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_living_sketchbook\`):

- `cast\AARON.md` + `cast\aaron_ref.png` — ONE anchor for the whole ~39-year
  priesthood (83→123, old-man register both ends, per its own KJV age
  verification). On screen in ~45 of 76 spreads. The golden "garments of
  glory" (spread 3 only) are already text-locked in that sheet's exception
  paragraph — no second anchor.
- `cast\MOSES.md` + `cast\moses_ref.png` — one appearance (spread 15), at
  the ~80-year register per that sheet's own golden-calf-flashback note
  (the Day-of-Atonement institution is the SAME early period — Exodus
  40:17, year 2). Same anchor, at most slightly less white.
- `cast\JESUS.md` + `cast\jesus_ref.png` — appears in 4+ distinct poses
  (entering 51, cross 53, seated 60, at the open veil 66/75/76).
  **Multi-pose identity lock applies in force**: spread 51's approved render
  chains as the SECOND reference into every later Jesus spread. Fail-closed
  eye-QC on all of them.
- `world\TABERNACLE_WORLD.md` + `tabernacle_ref.png`, `veil_ref.png`,
  `holyofholies_ref.png`, `altar_ref.png`, `goat_ref.png` — the veil must
  read as the SAME curtain whole (5/8/14/16/26/45/46/48/61) and torn
  (62/63/70/71/73/75/76), chained from the one anchor; the Holy of Holies
  stays EMPTY except the ark (spread 59's payoff); ONE goat design serves
  BOTH goats, distinguished by staging only; the door-curtain (spread 13)
  is the plainer needlework hanging folded into the tabernacle render, NOT
  the veil. Blood basin + Holy Place are text-locked, no renders.

**Gaps — need a decision or a small build BEFORE stills render:**

1. **Nadab + Abihu** (spreads 10–11, plus their wrapped bodies in 12): two
   adult priests, one scene. Scripture gives no ages — render as grown men
   (they served as priests; sons of an 84-year-old father), NOT boys, and
   visually distinct from EACH OTHER (cross-character distinctness rule).
   Minimal text-lock + chain spread 11 to spread 10's approved render — a
   Hezekiah-style one-off, not a full cast sheet.
2. **The LORD's presence / strange-fire treatment** (glow in 6/16/27, fire
   in 11): the locked repo convention exists
   (`ref_library\characters\THE_LORD.json` — radiant light, never a figure),
   and the Bronze Serpent LONG plan called for porting it into the sketch
   register. **Check whether that port was actually built during the Bronze
   Serpent production; reuse it if so, else 1–2 light-study renders.** The
   strange-fire strike (Lev 10:2 "there went out fire from the LORD") uses
   the same no-figure discipline.
3. **The fit man** (spread 32): anonymous background figure, no cast sheet
   (Nicodemus/SEEKER precedent).
4. **City-gate plate** (spreads 57–58): new. Check the Bronze Serpent LONG's
   approved Golgotha/crucifixion stills for reuse FIRST (same style family,
   reuse-first rule) — but topical-fit gate applies: only if no bronze
   serpent/pole appears in frame. Eye-check, don't assume.
5. **Seated Christ at the right hand** (spread 60): new pose; the standing
   `library-lacks-living-christ` gap means no stock exists. Fail-closed QC.
6. **Wilderness wides** (32/33/50/67/68): check the clip/still banks for
   thread-neutral desert plates before rendering new ones.

**Doctrine guards carried into every render** (from the narration's own
locked fixes + world canon): the goats are never visually distinguished; the
slain-goat spreads are wound-free (staging implies, never shows); "outside
the camp" imagery is the SLAIN offering's body (Lev 16:27), never the
scapegoat; the Holy of Holies contains nothing but the ark; gold-leaf stays
the register of His glory — the goats, altar, basin, and linen never borrow
it (the ark/mercy seat are literally gold objects and render as material
gold, not as the sacred-glow register); Lev 16:30's cleansing renders as
REAL relief, not failure; red-letter (turn 1) arrives whole.

**One continuity question for the user** (small, but it touches ~10
spreads): AARON.md's canon puts him in Day-of-Atonement linen "in nearly
every appearance." Spreads 36/38/43 (home at dusk, tent at night, old-age
fear) are outside the rite itself — strict canon linen everywhere is the
default this plan assumes (mitre optional off at night), but if you want
ordinary priestly dress for the domestic beats, that's a canon-sheet
amendment to make BEFORE stills, not during.

---

## 6. Style-variant swaps considered (5 production_approved: sl10/12/13/14/16)

Standing rule: Style 1 is the spine; variants are occasional deliberate
insert pages, never a default. Verdicts for THIS episode:

- **sl13 charcoal-and-eraser — ONE genuine candidate, proposed for user
  decision (spread 13).** Its manifest beat signal is literally "memory,
  erasure, soft-grief," and spread 13 is a father forbidden to mourn — grief
  that must be visibly ERASED is this variant's exact register. Budget fits
  (max 1/episode; nearest other candidate page is 40+ spreads away).
  Caveat before adopting: the bakeoff scored Moses/Jesus only — Aaron was
  never identity-tested in this variant, so it needs one test render against
  `aaron_ref.png` before it's committed. If the test drifts, spread 13 ships
  in spine style and loses nothing structural.
- **sl12 scratchboard inversion (night/threshold-into-dark) — considered
  for spread 26 (through the veil into the thick dark), REJECTED.** The
  dark-interior continuity chain (26→27→28 must read as one descent into
  the same darkness) would be broken by restyling its middle frame, and
  sl12 carries a gold-leaf conflict flag while the chamber's cloud-glow is
  the very next frame's subject.
- **sl16 foreground occlusion (hidden-observer/threshold) — REJECTED on
  meaning.** Its grammar implies someone watching from concealment; this
  story's entire point is that NO ONE could watch — "I went in alone." A
  hidden-observer frame would quietly contradict the text it illustrates.
- **sl10 overhead plan (scale/isolation) — considered for spreads 2/7 (the
  tabernacle in the camp, the nation outside), REJECTED.** Those are Beat 1
  hook spreads; the opening must establish the spine look, not spend a
  variant in the first 40 seconds. The identity trade-off the manifest
  itself records (faces soften at altitude) also lands on the two spreads
  that introduce Aaron's world.
- **sl14 torn-paper depth planes (memory/composite) — considered for the
  memory recaps (34/41/65), REJECTED.** The MV vignette grammar already
  does the memory-composite job on those spreads; stacking a second memory
  grammar on top is device-stacking, and the film's torn-paper vocabulary
  is deliberately reserved for ONE meaning here: the tear that opens on
  Christ (62/76).

Net: zero committed swaps, one candidate (sl13, spread 13) pending an Aaron
identity test + user eye.

---

## 7. Rough cost — order-of-magnitude, for the go/no-go conversation only

No API called, no estimator run. Anchored to the same unit prices as the
Bronze Serpent plan (~$0.30–0.50/still NBP; Seedance ~$0.65 real-bill /
Kling ~$1.20/clip):

- **Stills**: 76 spreads × $0.30–0.50 = $22.80–38.00; new-asset renders
  (Nadab+Abihu lock, LORD light-study if the Bronze Serpent port wasn't
  built, seated Christ, city gate, sl13 test) ~4–6 renders = $1.20–3.00;
  re-roll contingency 20–25% (standing practice, and the veil/goat anchors
  each already needed a corrective roll this session) = +$5–9.
  **Subtotal ~$29–50.**
- **Animation**: the ~10 pure card spreads (16, 20, 24, 28, 31, 35, 49, 52,
  58, 72) can take the $0 path (deterministic lettering + grain-boil /
  pingpong hold over a static ground) — decision per-card at animate stage;
  ~66 spreads paid: ~55 Seedance-tier × ~$0.65 ≈ $36 + ~11 Kling-tier
  (crowd 7/40, strange-fire 10–11, bearers 12, goats+handlers 23, slaying
  25, acting 29, Jesus-entering 51, MV 65, acting 75, and margin) × ~$1.20
  ≈ $13. **Subtotal ~$25–55 (midpoint ~$49).**
- **Total rough range ~$55–105, midpoint ~$80–95** — in the same band as the
  Bronze Serpent plan's estimate (~$75–90 midpoint) for +12% spreads, which
  is the expected direction: cost tracks spread count, not runtime.

---

## 8. Summary for the go/no-go conversation

- **76 spreads, 7.75s average (range 3.1–21.5s)**, content-paced: fast
  procedural rite (Beats 1–3), slow wrestling and reveal (Beats 5–6), the
  four longest holds on the four heaviest moments.
- **Timing model corrected**: this file has NO inter-turn pauses (meta +
  ffprobe + arithmetic all agree, 588.64s = Σ naturals exactly) — the
  briefed 0.4/0.3 Bronze-Serpent pause formula does not apply. Sub-turn cut
  points need a WhisperX pass before build.
- **Beat 6 is denser than briefed**: 7 verses in 6 scripture turns (not 4
  quotes) — absorbed by register rotation (never two lettered spreads
  adjacent; Rubric ×2 at the two peaks; Elder Leaf ×1 on the Isaiah echo;
  the last three quotes are composites over story art).
- **Zero new cast/world anchors needed for the leads** — Aaron, Moses,
  Jesus, and all 5 tabernacle-world anchors exist. Gaps: Nadab+Abihu
  one-off lock, LORD-presence sketch port (verify Bronze Serpent build
  first), fit man (anonymous), city-gate plate (check Bronze Serpent
  Golgotha stills for serpent-free reuse), seated Christ, wilderness-wide
  bank check.
- **Open questions for the user**: (1) sl13 insert page on spread 13 —
  test + eye, or spine style? (2) Aaron's dress on the three domestic
  spreads — strict canon linen, or amend the sheet? (3) the 18.3s
  single-card hold on the LORD's charge (16) — approve the
  whole-arrival + long push treatment, or split the visual behind a
  persistent card? (4) rough spend ~$55–105 — OK to proceed to stills at
  the next session?
