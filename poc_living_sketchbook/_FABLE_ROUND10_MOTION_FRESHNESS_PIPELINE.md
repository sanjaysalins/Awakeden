# Fable — ROUND 10: MOTION FRESHNESS + THE FINISHING-PASS PIPELINE

**Date:** 2026-08-06 · **Brief:** the user, after watching the full 591s Day of Atonement cut:
*"this is really good, but I am finding several places we just a frozen still, it looks very
abrupt, it looks very ameriuish [amateurish], how can we tweak those frozen stills or animation,
can we bring is some grand text or redemption animation to make it feel fresh and dynamic. Can we
get fable to think of a repeatable pipeline we can apply to these long episodes"*

**What this round answers, specifically:** three things, in order of permanence — (1) a
per-spread disposition for every frozen spot the motion diagnostic found in THIS film, using only
the project's own device vocabulary; (2) the "grand text" and "redemption animation" the user is
asking for, designed as three concrete concepts on named spreads; (3) the REPEATABLE
finishing-pass pipeline — taxonomy, quota law, cliff rule, and a $0 deterministic motion-lint gate
— so no future long-form episode can ship with this failure mode again. A Sonnet agent builds all
of it; every spec below is written to be executed without a creative judgment call.

**Everything in this round is $0 deterministic** — PIL/numpy/ffmpeg over already-approved stills
and clips, no generative spend, no re-render of any approved art. CPU time only (`_polite`).

Rules carried (non-negotiable, same as every round): doctrine sound + proven both ways; KJV
verbatim via deterministic overlay only, never generated lettering; LAW 1 (red-letter arrives
WHOLE); LAW 2 (big/bold — the Word is never timid on the page); gold = His glory only; sacred
stillness on the landing (s76 untouched, by definition); the three mandatory hard-cut pairs
(10/11, 25/26/27, 61/62) stay pure hard cuts; Elder Leaf budget ≤1 (SPENT on s55 — no extension);
never animate generated writing; dense-frame eye-check before calling any rebuilt spread done.

---

## 0. The honest diagnosis (mine to own)

The prior session — me, in the rollout round — assigned **Raking Light to 21 of 76 spreads
(28%)**. The motion diagnostic confirms what the user felt: raking light at FULL-spread scope
scores 0.37–0.46 (vs 0.02 for the deliberately-static landing — i.e. it is visually
indistinguishable from a frozen still with lamp flicker), and 9 of the bottom 13 lowest-motion
spreads are raking-light spreads.

**Root cause, named precisely: assignment friction, not device quality.** Raking light is the
only hold device in the roster that needs NO per-still bbox/region pick. Every spotlight-family
device costs 30–60 seconds of eyeballing a bbox; raking costs zero. Over 50+ assignment
decisions, the zero-friction option won by default — a selection bias, not a design choice. The
same bias explains the second-tier problem: **the six "specially-named" verse cards (s16, s31,
s49, s52, s60, s63) shipped on their raking "placeholder"** because a placeholder, once written
into the table, is indistinguishable from a decision. Three of those six are in the bottom-13.

Two compounding factors the fix must also address:

1. **Contrast at the cut.** 61 of 75 seams use Unseen Hand (deliberately near-invisible, 0.7s).
   Cutting from a genuinely-moving Kling clip straight into a light-flicker spread with an
   invisible transition makes the freeze land INSTANTLY — the near-invisible transition is the
   right default for like-into-like cuts and exactly wrong at a motion cliff.
2. **No gate existed.** The failure was only discoverable by the user watching 10 minutes of
   film. The diagnostic that found the 25 worst spreads took minutes to run and should have run
   BEFORE the rollout was called done. That gate is deliverable 3d.

---

## PART 1 — THE DISPOSITION TABLE (fix the frozen spots)

### 1a. The 21 raking-light spreads — full disposition

Verdict key: **SWITCH** (different device, from the real vocabulary) · **KEEP+PAIR** (raking
stays but may never again be pure-static — see the Pairing Law, §3b) · **REBUILD** (the spread is
one of the six deferred special cards; its real register gets built in Part 2).

**Full-scope raking (the 5 worst offenders + 1 errored):**

| spread | dur | content (per `_PLAN.md`) | verdict → device | params / notes |
|---|---|---|---|---|
| s25_slaying_stage1 | 4.0s | the slaying at the altar base, knife + goat, wound-free | **SWITCH → dramatic_spotlight** | bbox on goat+knife+Aaron's arm (eye-pick against the still). Caravaggist slaughter lighting is the right register; stays inside the 25/26/27 hard-cut triple untouched |
| s27_sprinkling | 4.0s | sprinkling before the mercy seat, alone in the dark, cloud-glow | **SWITCH → breath_synced_halo** | bbox on the CLOUD-GLOW above the mercy seat, not on Aaron — the Presence breathes in the dark (the plan's own "glow breathes" language for spread 6, finally honored here) |
| s50_the_shadow | 4.9s | a long shadow across sand cast by something beyond the frame | **SWITCH → wash_creep (re-anchored)** | the shadow IS an advancing dark front — `isolate_storm_wash`'s HSV band re-tuned to the shadow's tone (eye-check the mask), advance a few px toward the viewer across the spread. "A shadow waits for the body that casts it" — the shadow moves because the body is coming. Honest flag: wash_creep was built for storm washes; this is a re-anchoring of the same mechanism, not new code — but the mask isolation MUST be eye-checked on this exact still before trusting it |
| s60_seated_glory | 7.3s | COMPOSITE card: Heb 10:12 over Christ seated in glory | **REBUILD → Concept A3** ("Sat Down") | Part 2 |
| s63_torn_veil_card | 6.2s | COMPOSITE card: Matt 27:51 over the torn veil | **REBUILD → Concept A1** ("From the Top to the Bottom") | Part 2 |
| s52_jesus_entering_formal | 10.4s | Illuminated Rubric #2: Heb 9:12, the thesis verse | **REBUILD → Concept B** (Rubric grammar) | Part 2. Was one of the 2 frame-extraction errors — treat as confirmed-frozen |

**Tail-scope raking on the special cards (placeholders that shipped):**

| spread | dur | register owed | verdict |
|---|---|---|---|
| s16_lords_charge_card | 18.3s | Illuminated Rubric #1 (the LORD's charge, LAW 1) | **REBUILD → Concept B** |
| s31_confession_card | 21.5s | Scribed-Ink LIVE-WRITE (the film's longest spread) | **REBUILD → Concept B** |
| s49_veil_detail_card | 10.5s | stacked double-verse (Heb 10:3 → 10:4) | **REBUILD → Concept B** |

**Tail-scope raking, ordinary spreads (12):**

| spread | content | verdict → device | params / notes |
|---|---|---|---|
| s03_golden_garments | the garments of gold laid aside | **KEEP raking + enable the gold FLARE** | the subject IS gold — this is the device's designed beat, and it spends the episode's ONE flare budget here (nowhere else flares) |
| s08_curtain_shut | curtain falls shut, Aaron's face in the dark | **SWITCH → caravaggio_pulse** | bbox Aaron's face |
| s11_struck_down | (raking assigned but never fires — real clip fills the window) | **DELETE the dead entry** | table hygiene: dead entries poison the device-share stats the new quota gate counts. Document in the commit message |
| s13_door_curtain_sl13 | Aaron gripping the robe he is forbidden to rend | **SWITCH → dramatic_spotlight** | bbox the gripping HAND at the robe — the grief lives in the grip. (If the pending sl13 charcoal-insert decision lands later, this assignment moves with the spread) |
| s19_altar_ministry | altar mid-ministry, smoke rising | **SWITCH → chiaroscuro_reveal** | regions in narration order: altar base → smoke column → Aaron. FINAL region = the smoke top at ~(0.30, 0.10) — the exact center where the existing through_object_cut into s20 opens. The tour hands the eye to the transition |
| s21_goat_innocent | the goat's innocent face, close | **SWITCH → line_boil** | the held gaze gets hand-inked LIFE, not a lamp — first use of line_boil in this film, subtle amplitude |
| s36_two_shadows_one_flame | night tent, the two lots in Aaron's lamplit hand | **SWITCH → caravaggio_pulse** | bbox lamp flame + hand — the flame's pulse is diegetic |
| s42_basin_linen_ready | basin scrubbed and set ready again | **KEEP raking + held_breath pairing** | the proven test spread, and a legitimate raking subject (museum-lit object). Pairing Law applies: raking amplitude `k` is multiplied by the episode `energy_envelope` so the light visibly quiets with the narrator |
| s44_pointing_smoke | smoke leaning past the frame edge, Aaron's eyes following | **SWITCH → focal_tour (dramatic_spotlight), 2 regions** | Aaron's eyes → the smoke tip at (0.55, 0.15) — which is BYTE-IDENTICALLY the center where the existing through_object_cut into s45 opens. The halo lands on the spot, then the cut opens through it. This is the transitions-carry-motion principle (§3c) made literal |
| s46_aged_unchanged_veil | Aaron aged, dim, the veil unchanged | **SWITCH → desat_focus** | region = Aaron's aged face; the colour drains from his day while his face holds it — "I did not see the answer in my own day." Was the other frame-extraction error — confirmed-frozen, fixed here |
| s59_no_chair | Holy of Holies bare except the ark, Aaron forever standing | **SWITCH → chiaroscuro_reveal** | 3 regions: the ark → the EMPTY floor beside it → Aaron standing. Lighting an empty patch of floor is the beat — there was no chair. Eye-pick the empty-floor bbox deliberately |
| s61_veil_recall | the veil WHOLE, recall register, the last frame before THE TEAR | **KEEP raking + HUSH DECAY** | raking amplitude × `energy_envelope`, AND a forced decay-to-zero over the final ~1.2s: the page goes DEAD STILL just before the mandatory hard cut to s62. Stillness that ARRIVES reads as intent; stillness that just sits reads as a freeze. This is the film's held breath before the tear |

**Also in the bottom-25, not raking — dispositions:**

| spread | score | current | fix |
|---|---|---|---|
| s34_riddle_recap / s57_without_the_gate | 3.78 / 3.92 | ink_up_build (full) | the build finishes early and the rest of the window is static. Fix: stretch the region schedule so vignette arrivals are staggered across the FULL window (last region completes at ~85% of duration), then held_breath-modulated halo drift on the final composition for the remainder. Parameter/glue change, no new device |
| s53_the_cross | 2.29 | locked_plate_parallax (full) | keep parallax; ADD a slow edge-darkening ramp (Passion-Vigil register): edge brightness eases 1.00 → 0.72 across the spread while the figure stays lit — the world darkens around Him. Restrained, no pulse, reverence cap. ~15 lines of glue on the existing halo_brightness primitive |
| s51_jesus_pivot | 5.30 | locked_plate_parallax (full) | the plan's own device column says "slow push + gold-leaf arrival" — the gold arrival was never built. Fix: fg_amp 6→9, plus a warm gold-register palette ramp over the first ~3s (palette_pivot's ramp math at low amplitude, warm direction only). The gold register ARRIVING with Him is the beat |
| s28 / s58 (combo C cards) | 2.19 / 2.04 | letterpress-beat verse combo | combo C's darkening pulse barely registers on screen. Fixed by the Grand-Text baseline (§2, Concept A0): word-timed presses + display-scale key word raise the card's real motion events; also deepen `DARKEN_K` ~1.5× on C cards specifically |
| s72 / s35 / s24 / s20 / s69 / s33 (combo A/B cards) | 5.4–9.4 | verse combos | Grand-Text baseline upgrade (A0); s69 additionally gets the bespoke A2 layout |
| s05_walking_to_veil | 11.53 | parallax (full) | above the frozen band — leave; the lint will re-measure after calibration |
| s68_east_west_horizon | 11.30 | palette_pivot (tail) | above the frozen band — leave |
| s43_shadow_on_tent_wall | (not bottom-25) | dramatic_spotlight *placeholder* | **UPGRADE → real candle_only** — the plan calls this beat "the device's literal design case" and `panel_animator/candle_only.py` now exists. Authored anchor ≈ the lamp at frac (0.50, 0.87) (from the placeholder bbox [42,78,16,18]) — eye-check against the still. R(t) closes down with the fear per the device's own grammar. Kills the last registered placeholder outside the six cards |

**Quota trims (not frozen-driven — required by the new quota law, §3b, because
locked_plate_parallax sits at 13/76 = 17%):** three tail-scope parallax entries move to
under-used signatures, each a better content fit anyway: **s10_strange_fire → caravaggio_pulse**
(bbox the censers' glow — fire that pulses), **s12_bodies_carried_out → desat_focus** (region the
two bearers — the colour of the day drains as the dead leave the camp), **s15_moses_charge →
line_boil** (two old brothers holding still; hand-inked life, no lamp).

### 1b. Resulting device distribution (proof the plan obeys its own law)

Hold devices, all scopes, 76 spreads — after every disposition above:

| signature | spreads | share |
|---|---|---|
| locked_plate_parallax | s05 s17 s26 s32 s48 s51 s53 s62 s70 s73 | 10 = 13.2% (WARN band, accepted — 6 of 10 are tail-scope behind real clips; recorded here as the documented exception the lint expects) |
| palette_pivot | s02 s06 s07 s38 s40 s67 s68 s71 | 8 = 10.5% |
| ink_up_build | s14 s22 s23 s34 s37 s41 s57 | 7 = 9.2% |
| breath_synced_halo | s04 s27 s30 s45 s64 s74 | 6 = 7.9% |
| caravaggio_pulse | s08 s10 s18 s36 s66 | 5 = 6.6% |
| dramatic_spotlight | s09 s13 s25 s44 | 4 = 5.3% |
| chiaroscuro_reveal | s19 s56 s59 s65 | 4 = 5.3% |
| raking_light | s03(+flare) s42(+pair) s61(+hush) | **3 = 3.9% (was 21 = 28%)** |
| desat_focus | s12 s46 | 2 |
| line_boil | s15 s21 | 2 |
| plain_static | s39 s76(landing) | 2 |
| one-offs | s43 candle_only · s47 registration_snap · s50 wash_creep | 3 |
| verse cards | 8 combo (A/B/C rotated) + 6 special registers (Part 2) | 14 |
| already-locked, untouched | s01 blue_line · s29+s75 Kling acting · s54/s55 thread+elder leaf · hard-cut stages | — |

No signature above 15%; raking demoted from dominant to rare; every raking survivor paired.

---

## PART 2 — GRAND TEXT + REDEMPTION ANIMATION (three concepts)

All three are built from the project's own proven letterpress-verse primitives
(`make_line_mask` / `compose_pressed_tile` / `paste_tile` / `make_ref_tile` from
`day_of_atonement/_s3_thread_leaf_54_55.py` — approved on spreads 54–55) plus `_alignment.json`
word timings. The per-run size support in `LINES` (`[(text, size), ...]`) already exists — the
display-scale words below are DATA, not new rendering code.

### Concept A — "Scripture enacted in the letterpress" (the grand text)

The user's instinct is right: on a card, more camera motion hurts legibility — the boldness must
live in the TEXT ARRIVAL. The principle: **the layout choreography enacts the verse's own
claim.** Never decorative; the motion IS the exegesis.

**A0 — baseline upgrade, all 8 combo cards ($0, mostly data):**

1. **Word-timed presses.** Each card line presses at the moment the scripture voice actually
   speaks its first word: match the line's leading token sequence inside the card's alignment
   window; on a match, press at that word's `start`; on no match, fall back to the current
   spacing and print a WARN. (letterpress_beat already reads `_alignment.json`; this extends the
   same lookup to combos A and B — the standing 🔴 rule "motion design serves the real text"
   finally applied to every card, not just combo C.)
2. **One display-scale key word per card (LAW 2).** The operative word renders at ~2.2× body
   size within its line (mixed run sizes already supported): s20 "**blood**" · s24 "**LORD**" /
   "**scapegoat**" (the two destinies, one scale each) · s28 "**vail**" · s33 "**not
   inhabited**" · s35 "**two kids**" · s58 "**without the gate**" · s72 "**boldness**". Note the
   deliberate echoes: s20's "blood" and s72's "boldness" are the SAME words the existing
   verse_mask_reveal transitions open through into the next spread — the card shouts the word,
   the cut then walks through it. `_draw_backing`'s plate must size from the realized line
   tiles, not the line count (display words widen lines).
3. **Combo C amplitude:** `DARKEN_K` ×1.5 on C cards only, so the ink-pulse actually reads.

**A1 — "FROM THE TOP TO THE BOTTOM" (s63_torn_veil_card, 6.2s, Matt 27:51).** Replaces the
raking placeholder. The composite card over the torn-veil art, frame-by-frame:

- t=0: the torn-veil still; the rent's light breathes gently (radial warm gain 1.00→1.06 cycle,
  `candle_only.apply_candle` math anchored on the RENT, R fixed, gain oscillating — the light is
  already drawn; we only let it breathe).
- Presses descend the page beside the rent, each timed to the spoken words (window
  475.84–482.08): "…the veil of the temple" at y≈0.10 → "was **rent in twain**" at y≈0.38
  (display scale on "rent in twain") → "from the top" at y≈0.55 → "to the bottom." at y≈0.80 —
  **the last clause physically lands lowest as the voice says "bottom."** The text performs the
  verse's own doctrinal detail: torn from the TOP — God's act, not man's.
- At the "rent in twain" press: one 0.4s light-bloom swell on the rent (same radial-gain
  wrapper, gain spike 1.15). Not a gold flare — the flare budget is spent on s03.
- "MATTHEW 27:51" stamps bottom-right via `make_ref_tile` (gold stitch + letterspaced ref).
- New code: the y-descent layout table + the rent-anchored gain wrapper (~60 lines total).

**A2 — "EAST FROM WEST" (s69_east_west_card, 6.2s, Ps 103:12).** Upgrades its combo-A
assignment to a bespoke layout on the horizon art: "As far as the east" presses at the far LEFT
edge (x≈0.04, mid-height); "is from the west…" presses at the far RIGHT edge (x≈0.72) as the
voice reaches it — **the whole horizon lies between the two clauses.** The span IS the
statement; nothing else moves. Each clause gets its own small backing plate. New code: a
two-anchor layout entry (~20 lines).

**A3 — "SAT DOWN" (s60_seated_glory, 7.3s, Heb 10:12).** Replaces the raking placeholder.
Composite over the seated-Christ art: the verse presses word-timed into the upper margin; the
operative clause "**sat down**" (display scale) arrives with a SETTLE, not a pop — the pressed
tile descends ~12px into its baseline over 0.35s ease-out, with one letterpress-beat paper thump
on the landing frame. Text that sits down. Then "on the right hand of God." at body size.
Behind, a slow_breath-amplitude halo on the seated figure. New code: the settle easing variant
(~15 lines).

### Concept B — completing the two ceremonies (the deferred special cards, now un-deferrable)

These four were always designed registers (`_PLAN.md` §4's own monotony-defense depends on
them); they shipped as raking placeholders. Building them IS the grand-text answer for the
film's formal peaks. All letterpress-primitive work; no camera on any of them.

- **s16_lords_charge_card (18.32s, Lev 16:2 — Illuminated Rubric #1, red-letter).** 0–1.5s: the
  cloud-glow art alone, glow breathing (breath_synced_halo bbox on the glow). At ~1.5s the
  ENTIRE rubric arrives WHOLE in one block press — **LAW 1: red-letter is the LORD speaking;
  never letter-by-letter, never word-by-word.** Large dropped capital "S" ("Speak unto
  Aaron…") with a gold-leaf ground behind the CAP ONLY (gold = His glory; the ground of the
  Speaker's initial qualifies; body text plain rubric red). Arrival = one whole-block
  `compose_pressed_tile` press + a 0.6s radial light swell centered on the cap. The remaining
  ~16s: the glow keeps breathing, and ONE slow flare-free raking pass (k=0.02) crosses at ~9s so
  the longest card of the film is never inert. Precedent: Bronze Serpent's 10.9s whole-arrival
  hold; this is the same law at 18s, which is why it needs the breathing layers.
- **s52_jesus_entering_formal (10.4s, Heb 9:12 — Illuminated Rubric #2).** Same grammar: gold
  dropped cap "N" ("Neither by the blood of goats…"), whole-block arrival at ~1.2s over the
  Jesus-entering art, glow-breath + one k=0.02 raking pass at ~6s. The two Rubrics are the
  film's ONLY two (the locked ≤2-at-the-peaks budget) and they now visually rhyme.
- **s31_confession_card (21.5s, Lev 16:21 — Scribed-Ink live-write).** The film's longest
  spread: the confession appears word-by-word IN SYNC with the scripture voice (291 glyphs /
  21.5s ≈ 13.5 glyph/s, the plan's own pace check). Implementation: per-WORD ink arrival timed
  from `_alignment.json` (per-glyph is fake precision), each word appearing wet-dark and drying
  to final ink over 0.5s (the existing INK_DARK→INK_FINAL ease) — written, not stamped: no
  press-pop, a 0.06s soft fade-in per word. **NO hand is rendered** — keeper_hand is forbidden
  on the Word's own lettering (its own doc says so); the ink simply arrives as-written.
  Doctrinal note for the builder: LAW 1 (whole arrival) binds RED-LETTER divine speech (s16's
  turn 1). Lev 16:21 here is the scripture voice narrating — progressive reveal is the plan's
  own locked call for this card ("LIVE-WRITE… as the voice reads it"). Do not "fix" it to whole
  arrival; do not extend live-write to s16. Hands-on-head art stays ghosted behind per the plan.
- **s49_veil_detail_card (10.48s, Heb 10:3 + 10:4 — the stacked double).** Verse 1 presses
  word-timed (~352.9s onward); holds; a thin scribe's rule line draws itself between the verses
  (0.3s) at the turn; verse 2 presses BELOW as the voice reaches it (~358s onward). Two verses,
  one page, sequenced by the audio. Rule-line draw is trivial new code (~10 lines).

### Concept C — "The thread holds both goats" (the redemption animation)

The gold thread (spreads 54–55) is this project's established OT→NT redemption grammar — the
user's "redemption animation" already has a native visual language, so we extend ITS presence
rather than inventing a parallel motif, and we extend it by exactly ONE spread:

- **s56_the_answer (10.7s)** — the film's thesis image: both goat-memories small and earthbound,
  Christ central holding both halves. It already runs chiaroscuro_reveal with 3 regions. Add:
  as the tour's halo leaves goat-memory 1, gold thread 1 fades in from that vignette to Christ;
  as it leaves goat-memory 2, thread 2 fades in likewise; when the tour lands on Christ, BOTH
  threads swell once (the existing `thread_swell` luminance bump) timed to the spoken words
  "one Priest" (alignment lookup inside window 415.60–436.80). Two deaths of meaning, one
  Person — the film's riddle answered in its own established vocabulary.
- **Continuity dividend:** s54 → s55 → s56 are consecutive. The thread now lives for one
  unbroken three-spread arc at the heart of the reveal — laid on the goat, cited by Isaiah,
  resolved in the one Priest — then never appears again. Scarcity preserved; presence deepened.
- **Build note:** promote `make_thread_layer` / `thread_opacity` / `thread_swell` out of
  `_s3_thread_leaf_54_55.py` into **`panel_animator/thread_device.py`** (a PROMOTION of proven
  code to the shared toolkit — s54/55's script then imports from there too; byte-identical
  output required on re-render of 54/55 as the regression check).
- **Explicitly NOT done:** no third thread anywhere else (s67's gold-lit scapegoat carries the
  meaning in paint already), and NO second Elder Leaf — that budget is locked at ≤1 and spent.

---

## PART 3 — THE REPEATABLE FINISHING-PASS PIPELINE

This section is the standing procedure for EVERY future long-form episode's finishing pass. It
exists because the Day of Atonement rollout proved that per-spread taste, unguarded, drifts to
whatever is cheapest to assign. Four components: a taxonomy that makes the right choice the easy
choice, a quota law that makes drift impossible, a cliff rule for transitions, and a $0 lint
gate that measures the film before the user ever has to.

### 3a. The hold-device taxonomy (assign by content class, rotate within the class)

At rollout-planning time, every spread gets a CLASS column written into its table (the class is
readable straight off the plan's "Shows" column). Each class has a pool; assignment ROTATES
within the pool — never the same signature twice in any 3 consecutive spreads, never >2 of one
family in any 5.

| class | pool (rotate) | notes |
|---|---|---|
| PORTRAIT (face, direct address, contemplation) | dramatic_spotlight · caravaggio_pulse · breath_synced_halo · plain_static (occasionally — not every face gets a lamp) | bbox on the face/hands, eye-picked |
| OBJECT / PROP (basin, lots, garments, close hands) | raking_light (paired, §3b) · ink_up_build (2+ sub-elements) · locked_plate_parallax (clean depth split) · line_boil (calm held) · frottage (≤1/ep, text-load-bearing artifact ONLY) | raking is legitimate HERE and only here as a primary |
| LANDSCAPE / WIDE (horizon, camp, courtyard) | palette_pivot · desat_focus · wash_creep (only if the still contains a real advancing-front element: shadow, smoke, water) · still_water_mirror (calm water only, fail-closed) | |
| MULTI-VIGNETTE (memory composites) | ink_up_build (schedule stretched to full window) · chiaroscuro_reveal · + thread_device when the vignettes are an OT→NT pairing | |
| VERSE-CARD | text-combo A/B/C rotation + the special registers (Rubric ≤2 at the two peaks · Elder Leaf ≤1 · live-write for a voice-paced long verse · composite-over-art for climax cards) | **text arrival IS the motion**; camera never; every card word-timed + one display-scale key word (LAW 2) |
| ACT / EVENT (procedural stages, motion moments) | real generative clip first; hold tail = locked_plate_parallax or spotlight-on-the-act; multi-stage hard-cut sequences keep ONE visual language across their stages | |
| DARK / LIGHT-SOURCE (lamp, glow, fire beats) | candle_only (≤1/ep, authored anchor) · breath_synced_halo on the glow · caravaggio_pulse on the flame | |
| LANDING | plain_static, sacred stillness, INV-26 | locked; whitelisted in the lint |

### 3b. The three laws (what makes the taxonomy enforceable)

1. **QUOTA LAW.** No single device signature may exceed **10% of spreads (WARN) / 15% (FAIL)**,
   counted from the episode's device table by the lint. Full-scope entries (device carries the
   whole spread, no real clip) are additionally capped at **8% per signature**. Any accepted
   WARN must be written into the episode's device file as a comment naming the reason (this
   episode: parallax at 13.2%, mostly tails — accepted, documented in §1b).
2. **PAIRING LAW.** Any pure-relight or pure-static device (raking_light, plain_static outside
   the landing, letterpress pulse) carrying a spread ≥5s at full scope, or a tail ≥4s, MUST be
   paired with an energy layer (held_breath-modulated amplitude) or possess an arrival event in
   its first 1.5s. Pure lamp-flicker over a frozen frame for 5+ seconds is now illegal — that
   is the exact signature the user called amateurish.
3. **PLACEHOLDER LAW.** A placeholder assignment must be registered as
   `"placeholder": True` in the device table. The lint FAILS any film that ships with a
   placeholder entry still live. Placeholders may exist during the build; they may never
   survive it silently — the six special cards shipped frozen because a placeholder, once
   written down, looked like a decision.

### 3c. The cliff rule (transitions carry motion at the seams that need it)

**Definition:** a MOTION CLIFF is a seam where the outgoing segment's final ~1.0s measures
high motion and the incoming segment's first ~1.5s measures low motion (thresholds from the
lint's calibration, §3d — both are measured, not judged).

**Rule:** Unseen Hand (near-invisible) remains the default for like-into-like cuts. At a
motion cliff, the seam must satisfy ONE of:

1. the incoming spread's device has an **arrival event** inside its first 1.5s (a press, an
   ink-up, a snap, a settling plate — devices that ARRIVE rather than just ARE), or
2. the transition escalates to a **visible device** that carries the motion across the seam —
   tipped_in_plate / leaf_flick / ink_transition blot / through_object_cut / verse_mask_reveal,
   chosen by content fit exactly as Round 9 rotated them, or
3. the seam is one of the episode's **protected hard cuts** ("the cut tells the event") —
   always exempt, the plan's own rule wins.

In THIS film, most cliffs die with Part 1/2 (rebuilt cards all have arrival events; s61's hush
makes the 61/62 hard cut a designed contrast, not an accident). The lint still audits every
seam and lists surviving cliffs for a human pick from option 2's rotation.

### 3d. `motion_lint.py` — the standing $0 QC gate (NEW build, ~180 lines)

**Location:** `panel_animator/motion_lint.py` (shared toolkit, episode-agnostic). Inputs: a
segments directory (`_segments/*.mp4`), the episode's `_spread_windows.json`, and its device
table (import the episode's `_devices.py` equivalents). No LLM, no spend.

**Metric (better than my crude start/mid/end diff, which under-measured event-based devices):**
sample each segment at 3fps via ffmpeg; compute mean absolute luminance difference per pixel
between consecutive samples; report per segment **`mean`** and **`p95`** of that series. A
verse card whose only motion is three big presses scores near-zero on start/mid/end sampling
but its p95 catches the press events — p95 is the freshness signal, mean is the energy signal.

**Calibration, not guessed thresholds:** first run executes in `--calibrate` mode against the
current segments and prints the score distribution with device labels. Sonnet sets `T_frozen`
just above the known-frozen cluster (this film: raking-full ≈ 0.4, landing 0.02 on the old
metric) and below the known-alive cluster, then commits the thresholds INTO the report header
so every future run states its own calibration lineage. Per-class thresholds: narrative
spreads and verse cards get separate `T_frozen` values (cards are legitimately quieter between
presses).

**Checks (FAIL exits 1):**

| check | condition | severity |
|---|---|---|
| FROZEN-SPREAD | p95 < T_frozen(class) AND dur ≥ 5.0s AND not whitelisted | FAIL |
| FROZEN-SHORT | same, dur < 5.0s | WARN |
| STATIC-RUN | 2+ consecutive spreads at/below WARN level | FAIL |
| DEVICE-QUOTA | signature share >10% / >15% (from the device table; full-scope >8%) | WARN / FAIL |
| PLACEHOLDER | any `placeholder: True` entry live | FAIL |
| MOTION-CLIFF | A-tail high, B-head low, transition == unseen_hand | WARN (lists the seam) |
| EXTRACT-ERROR | any segment fails frame extraction | **FAIL, fail-closed** — this round's two extraction errors (s46, s52) were both confirmed-frozen spreads; an unreadable segment is a suspect segment, never a skip |

**Whitelist:** the landing + any explicitly-authored stillness spread, declared in the device
table (`"stillness_authored": True`), never inferred.

**Output:** `_motion_lint_report.md` in the episode folder + console summary.

**Standing position in the finishing checklist** (the repeatable order for every long episode):

```
animate → margin_sentinel → rollout planning (taxonomy CLASS column + assignments
  under the three laws) → segment build → motion_lint (fix FAILs, re-run to zero)
  → concat + transitions (cliff audit from the lint's WARN list) → motion_lint
  again on the final film (windowed by spread times) → check_landing_hold →
  full-film human watch → ship
```

The human watch stays — the lint is the floor, not the ceiling (the panel-variety precedent:
deterministic checks caught 6 of 9; eyes caught the rest). But the user should never again be
the first detector of a 21-spread systematic freeze.

**Optional helper (recommended, ~40 lines):** `panel_animator/bbox_sheet.py` — renders any
still with a 10×10 percent-grid overlay to a contact sheet, so eye-picking a bbox takes
seconds. This attacks the ROOT CAUSE directly: raking light won by being the only zero-bbox
device; make bboxes nearly free and the friction bias dies.

---

## BUILD ORDER FOR SONNET (with eye-gates)

Everything below is $0. Work in `poc_living_sketchbook/day_of_atonement/` + `panel_animator/`.

1. **`motion_lint.py` first** (+ calibrate on the current segments, commit the report) — so
   every subsequent fix is measured, before/after. Then `bbox_sheet.py` (optional but cheap).
2. **Table edits + simple switches** (§1a SWITCH rows + the 3 quota trims + s43 candle_only +
   delete the s11 dead entry) in `_devices.py`; eye-pick all new bboxes against the real
   stills (bbox_sheet helps). Re-render only the affected segments (`_s6_assemble.py --only`).
3. **Pairing glue:** raking × held_breath amplitude (s42), the s61 hush decay, ink_up schedule
   stretch (s34/s57), s53 edge-darkening ramp, s51 fg_amp+warm-in. Small functions in
   `_devices.py`, patterned on `_breath_synced_halo`'s existing envelope usage.
4. **Grand-Text baseline (A0)** on the 8 combo cards: word-timed presses + display-scale key
   words + backing-plate sizing + C-card DARKEN_K. Extends `_poc_motion_text_combo.py`'s
   combo functions + the per-card `VERSE_CARDS` table (add `key_words` + timing lookup).
5. **Special-card rebuilds (Concept B)** one at a time, **s16 first** (it sets the Rubric
   grammar s52 reuses), each behind a dense-frame eye-check before the next starts.
6. **Bespoke layouts (A1 s63, A2 s69, A3 s60)** — new layout tables on the proven press
   primitives + the rent-anchored gain wrapper.
7. **Thread promotion + s56 reprise (Concept C)** — `panel_animator/thread_device.py`;
   regression: re-render spread54/55 clips and require byte-identical frames.
8. **Transition cliff audit** from the lint's WARN list; escalate surviving cliffs per §3c
   option 2's rotation. Protected hard cuts untouched.
9. **Full re-assemble → motion_lint to zero FAIL → check_landing_hold → hand the film to the
   user** with the before/after lint report.

**Do-not-touch list (verify before every step):** s76 landing (plain static is the ANSWER, not
a placeholder) · s01 blue_line · s29/s75 Kling acting spreads · s54/s55 thread+elder-leaf clips
(except the import-path change in step 7, byte-identical output required) · the three mandatory
hard-cut pairs 10/11, 25/26/27, 61/62 (device changes on those spreads are fine; the SEAMS stay
naked hard cuts) · every approved still and generative clip (nothing is regenerated anywhere in
this round).

## What is genuinely NEW vs recombined (honesty ledger)

- **NEW code, small:** `motion_lint.py` (~180 lines) · `bbox_sheet.py` (~40, optional) ·
  descent/edge-span/settle layout logic on existing press primitives (~100 lines across
  A1/A2/A3) · scribe rule-line draw (~10) · rent-anchored radial-gain wrapper reusing
  `candle_only.apply_candle` math (~25) · hush-decay + pairing glue (~40) · per-word live-write
  scheduler for s31 (~60, all on existing tile primitives).
- **PROMOTION, not new:** thread primitives → `panel_animator/thread_device.py`.
- **RE-ANCHORING, flagged:** wash_creep's mask tuned to a shadow instead of a storm wash (s50)
  — same mechanism, must be eye-checked on the real still.
- **Everything else** is recombination of the 27 kept devices plus data-table edits. No new
  visual grammar is invented anywhere; the "grand text" is the project's own letterpress voice
  finally given LAW-2 scale and real word-timing, and the "redemption animation" is the
  project's own gold thread finishing the argument it started on spread 54.

*— Fable*
