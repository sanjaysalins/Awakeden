# Round 9 — BRONZE SERPENT END-TO-END PLAN (design round, not a build)

**Date:** 2026-07-31 · **Handoff note:** rounds 1-8 of this style/insert-page work were built by
Fable, who hit its usage limit partway through this round. The user asked to continue on Sonnet
instead, matching the same discipline: honest self-review, eye-verify at full resolution before
anything counts as a pass, name every defect even on a PASS, never claim more than was actually
tested. Everything below is written to that standard — first-person voice kept consistent with
rounds 1-8 since this is one continuous body of work, not a fresh start.

**What this round is:** the user flagged three real gaps before any of rounds 1-8's work is
production-ready — (1) nothing has been animated, only static proof stills; (2) nothing has been
tested inside a real assembled episode with the actual paper-layer devices, transitions, and
Keeper identity; (3) they want to know what skills are still missing before a real end-to-end test.
This round answers (3) and lays the groundwork for (2): a full spread-by-spread plan for one real
episode — **Bronze Serpent** (`longform/EW04_Bronze_Serpent/v1/short/`, "Look and Live," Numbers
21:4-9 → John 3:14-16, LOCKED narration, do not touch) — plus specs for the skills the plan
actually needs. **This is a planning round.** No episode stills get built except one optional proof
render (section D). The real 3 skills and the real episode assembly are later rounds, after the
user reviews this plan.

**Read first (the sources this plan is built from):**
`longform/EW04_Bronze_Serpent/v1/short/narration.md` + `passage.txt` + `narration.meta.json` +
`_synth.log` (the locked script + its real turn/voice timing) · `poc_living_sketchbook/storm/
_STORM_V6_REVIEW.html` + `_s4_assemble.py` (how a living-sketchbook episode is actually built) ·
`poc_living_sketchbook/_FABLE_ROUND7_STORM_COMPLEMENTS.md` + `_style_bakeoff/
combo_style3_jonah_echo.png` (the proven insert-page precedent) · `poc_living_sketchbook/
_FABLE_ROUND8_INSERT_PAGES.md` (12 insert grammars + THE LAW on counted things) ·
`mapengine/README.md` + `route.example.json` · `panel_animator/page_transitions.py` +
`poc_living_sketchbook/_FABLE_ROUND6_THE_KEEPER.md` (the transition family + its open lanes) ·
`panel_animator/measuring_reed.py` (the magnitude-drawing cousin of the device this round specs) ·
`.claude/skills/living-sketchbook/SKILL.md` in full, especially §0 (LAW 1/LAW 2), §2, §8a.

Rules carried unconditionally (unchanged from every prior round): doctrine sound + proven both
ways; whole Bible through Jesus; KJV verbatim only via deterministic overlay; period lock, zero
modern anything, checked at full resolution; no named artist/book in prompts; positive-only
wording; gold = His glory only; crowds ≤3 distinct faces.

---

## A. The Bronze Serpent beat plan

### A0. Timing methodology (read before trusting any number below)

The locked narration has **no forced-alignment file yet** (Storm's `_storm_alignment.json`
equivalent doesn't exist for this episode). `narration.meta.json` + `_synth.log` DO give exact
per-TURN boundaries (three turns: witness / jesus / witness, each with a real `natural_seconds`
duration and the pre/post-quote pause structure), and I confirmed by character-count that every
line of the locked narration maps cleanly onto exactly one turn:

| turn | speaker | text | window (s) | duration |
|---|---|---|---|---|
| 0 | witness | Beat 1 + Beat 2 + "I speak now from the far side of my life..." | 0.30 – 40.62 | 40.32s |
| 1 | jesus | the John 3:14 quote (red-letter) | 40.87 – 48.23 | 7.36s |
| 2 | witness | "My bronze was only a shadow..." + Beat 4 | 48.53 – 76.85 | 28.32s |

Total narration.mp3 = **77.65s** (confirmed against `_synth.log`'s concat math to the millisecond).
That is longer than the "~60-75s" figure in the brief — the real locked audio runs a little past
75s; the plan below is built on the REAL 77.65s, not the estimate.

Within each turn I do NOT have real word timestamps, so the sub-turn spread boundaries below are
**character-count-proportional estimates** (each line's share of its turn's `natural_seconds`,
by character count — verified arithmetically against the real 543/95/323-char turn splits, which
match the locked narration.md text exactly). This is good enough to plan spread COUNT, ORDER, and
approximate pacing, and it is explicitly **not** good enough to cut frames against. **Before any
real assembly, run the same WhisperX/forced-alignment step Storm used and rebind every spread
window (and the insert-page's entrance) to real word onsets** — the same standing rule
(`scene-window-staleness` memory) that governs every other episode in this project.

### A1. The spread table (14 spreads, ~80s finished cut)

`Beat` = the narration.md beat the spread's text comes from. `Est. window` = the A0 estimate.
`Device` = what beyond plain Style-1 narrative art this spread carries — most carry nothing extra,
by design (see the budget rule in section C: this episode earns exactly one insert page and one
new transition, nothing else stacked on top).

| # | Beat | Est. window | Text | Shot | Device |
|---|---|---|---|---|---|
| s01 | 1 | 0.30–4.2s | "I am Moses. My people were dying of snakebite..." (opening clause) | Wide establishing: the camp of tents at the wilderness's edge, Moses in the foreground, a stricken family in the middle distance (distress read through posture/gesture, never wounds — no gore) | **Field Header** overlay ("WILDERNESS. FORTIETH YEAR.") writes ~1.0–3.2s, energy 0.15 — the episode's one header, composited on s01's own art per the Storm precedent, not a separate spread |
| s02 | 1 | 4.2–8.69s | "...and God told me to forge a snake of bronze and lift it on a pole." | Close/mid: Moses's face, grief and urgency, kneeling by a stricken figure | face close-up (shot-variety floor) |
| s03 | 2 | 8.69–13.5s | "The serpents were no accident — we had spoken against God..." | Wide: a knot of the people, gesturing in complaint/discouragement, Moses standing apart (≤3 distinct faces, rest shadowed/turned away) | — |
| s04 | 2 | 13.5–18.0s | "...and the LORD sent fiery serpents..." (judgment) | Serpents among the rocks and tent-lines, people recoiling — tension via composition/shadow, never a wound shown | — |
| s05 | 2 | 18.0–23.5s | "I begged Him to take the snakes away. He would not." | Moses alone, kneeling in intercession against open sky — isolation, no crowd | no-figure-adjacent atmosphere beat (shot-variety floor) |
| s06 | 2 | 23.5–30.0s | "Instead He told me to forge the image... The bitten had only to look — and live." | Close on Moses's hands at the forge, hammering the bronze serpent into shape, sparks, ochre/copper glow (never gold — gold is reserved for the Christ element, see A2) | close-up hands (shot-variety floor) |
| s07 | 3 | 30.0–40.62s | "I speak now from the far side of my life, by the light that came after — a night I never saw, when one they called Teacher answered a seeker:" | Moses's face turned toward the horizon/light, older register than s01-s06 — the narration itself steps outside ordinary time here (Moses narrating something he never witnessed), and the art should feel the same shift | **lift_away** transition (section B1) begins in this spread's last ~0.4s and finishes crossing into s08 |
| **s08** | **3** | **40.87–48.23s** | **"And as Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up:"** (red-letter, John 3:14) | **THE ONE INSERT PAGE** — Scholar's-Margin typology sheet, Numbers 21 beside John 3 (see A2/A3) | insert page + controlled reading-order pan (section B3) + THE WORD ARRIVES WHOLE (LAW 1) for the verse card overlaid on the same page |
| s09 | 3 | 48.53–54.0s | "My bronze was only a shadow." | Moses's face, humble, the bronze serpent visually smaller/plainer than the gold page just shown — hard cut back from s08 (no second transition; see governor in B1) | — |
| s10 | 3 | 54.0–58.96s | "They lifted Jesus on a Roman pole, made a curse for us, bearing our judgment in our place." | Christ lifted up, a reverent Golgotha beat — sacred, restrained, no gore (per `crucifixion-still-facts` memory: no nail close-ups, darkness rendered as darkness not storm) | sacred/reverence beat |
| s11 | 4 | 58.96–64.0s | "So hear me, you who are bitten — that is every one of us." | Moses turns to address the reader directly — the CTA's own opening line, direct-address framing | — |
| s12 | 4 | 64.0–69.0s | "The cure was never in you; it hangs in plain sight, and costs you nothing but a look." | Echo composition: the bronze serpent and the cross both visible/implied, "hangs in plain sight" made literal | — |
| s13 | 4 | 69.0–73.5s | "Lift your eyes to Jesus, lifted up for you." | Christ lifted, radiant, the landing's approach | — |
| **s14** | **4** | **73.5–76.85s + ≥3.0s hold** | **"Look, and live."** | **THE LANDING** — torn-page device (per SKILL.md §3: landing = torn page + sacred stillness, always a Christ-beat), gold light from beneath the tear | torn-page (mandatory), sacred stillness hold ≥3.0s (INV-26) |

Finished-cut target: **~80s** (77.65s narration + the ≥3.0s INV-26 hold past "live.," so the last
spoken word cannot land before ~76.85s and the file cannot end before ~79.85s). Real number depends
on the real forced-alignment end-timestamp for "live," not the A0 estimate.

14 spreads for 77.65s (~5.5s average) sits inside SKILL.md §3's "10-14 spreads per ~60s" band once
scaled for this episode's real length (77.65s / 63s Storm-length ≈ 1.23×, so 12-14 spreads scaled
up would land around 15-17 — 14 is on the disciplined/lean side of that range, which is the right
call for a piece this direct: it is a single confession-and-mercy arc with one pivot, not a
multi-scene epic, and the user's own worry was "keep the story moving," not "fill the runway.")

### A2. Why the insert page goes exactly at the Jesus quote (s08) — confirming the prior

Yes — and stronger than a generic "good spot" case:

1. **The words themselves ARE the typology.** John 3:14 is Jesus's own cross-reference back to
   Numbers 21 ("as Moses lifted up... even so must..."). No other beat in the narration states the
   comparison explicitly; every other line is either the Numbers 21 half or the CTA. This is the
   ONLY moment where showing both halves side by side is illustrating what the narration is
   LITERALLY saying, not adding a new idea next to it.
2. **The turn boundary is already there in the audio.** Turn 1 (the Jesus quote) is a genuinely
   separate ElevenLabs render, a different voice, bounded by real pre/post-quote pauses on both
   sides (40.62→40.87 and 48.23→48.53). A register change that lands exactly on an EXISTING voice
   change costs less momentum than one dropped into the middle of a continuous read — the audio
   itself already marks this as a seam.
3. **LAW 1 and the insert page reinforce each other instead of competing.** The Word Arrives Whole
   (the John 3:14 card must appear complete, never letter-by-letter) and the insert page's own
   register change are two different signals for the same instant: "this line is different in
   kind from the lines around it." Landing them together is one strong beat, not two competing
   ones.
4. **It is the shortest turn (7.36s).** An insert page is the single most expensive momentum cost
   in the whole toolkit (a full register switch, not a device layered on Style 1 — see section C).
   Spending it on the shortest, most self-contained turn in the episode is the cheapest place to
   spend it.

### A3. What the insert page actually shows

Scholar's-Margin (Style 3), byte-identical style block to the already-adopted precedent
(`combo_style3_jonah_echo.png`). LEFT panel: Moses (elderly, per Numbers 21 — this is 40 years
after the Exodus, not young Moses) lifting the bronze serpent on its pole before the camp, labeled
"NUMBERS 21," bronze/ochre only, no gold. RIGHT panel: Christ lifted up, labeled "JOHN 3," gold ONLY
on Christ's figure and the light around him — the serpent never gets gold, ever (palette theology:
gold = His glory only; conflating the two would visually claim the bronze object itself is the
holy thing, which is exactly the error 2 Kings 18:4 records Israel later making with this same
object — Hezekiah broke it in pieces and called it Nehushtan precisely because it had stopped
pointing past itself). A single comparison arrow, open chevron, Numbers 21 → John 3. The John 3:14
verse card (Scribed Ink, arrives whole, LAW 1) sits on this same page. Section D renders this for
real — see the eye-verify writeup there.

### A4. Second insert page / map — deliberately NOT built

Numbers 21:4 does mention a journey clause in the wider passage.txt context ("they journeyed from
mount Hor by the way of the Red sea, to compass the land of Edom"), and `mapengine/` already has a
route engine proven on this exact region/period. I checked the locked narration.md against that
temptation directly: **the journey clause is not in the narration.** Moses's first-person script
starts at "I am Moses. My people were dying of snakebite" — the whole piece is a STATIONARY
judgment-and-mercy scene inside an already-established camp, never a journey-so-far beat. A map
insert here would have nothing in the narration to anchor to; it would be decorative geography
bolted onto a piece that isn't about geography, exactly the "keep the story moving, don't over-stuff
it" failure mode the user named. **Verdict: one insert page, not two.** The `mapengine`/Style 13
Mariner's Chart pairing remains a strong candidate for a FUTURE episode where the journey itself is
load-bearing (Kadesh-Barnea, the wilderness wanderings overview, Paul's voyages) — not this one.

---

## B. Three skill specs

### B1. `lift_away` — the calm page-turn transition

**The gap:** `page_transitions.py` ships exactly one device, `torn_out_page` — grab → lift →
accelerating rip-away, deckle flash, a `paper_tear` foley cue at release. That is built for a
panic/rejection act-turn (the Keeper discards a page). Round 6's own doc names two open
candidates for the OTHER end of this family — a calm turn, not a violent one — but ships neither:
`slide_under` and `lift_away`, "named CANDIDATES that get their own $0 POC round and the user's
taste gate before any production code." This spec is that gate's paperwork for one of the two.

**Which one, and why:** I'm speccing **`lift_away`**, not `slide_under`. Two reasons. First, the
physical action: "the Keeper turns to a page they already prepared" is a real page-turn — you grab
a corner, lift it, and set it down turned — not a horizontal slide-under-the-stack motion, which
reads more like filing/archiving than advancing the story. Second, `lift_away` is the closer
SIBLING to `torn_out_page` (same grab→lift opening act, different resolution — settle instead of
rip), which is exactly the "family" relationship the round-6 doc wants and lets the implementation
reuse `TornOutPage`'s scaffolding (the smootherstep easing, the above/below frame-pair API, the
byte-stable-after-transition governor) rather than inventing an unrelated geometry. `slide_under`
stays open as a genuinely different future candidate for a different feeling (tucking a page away,
not advancing to a new one) — not built here, not needed for this episode.

**API (mirrors `TornOutPage`'s shape on purpose):**

```python
from lift_away import LiftAwayPage

tr = LiftAwayPage(above=s07_reflective_moses, below=s08_typology_page,
                   grab_t=0.9, lift_t=1.5, settle_t=2.3, seed=13)
frame = tr.compose(t)      # t = seconds since the transition's own t=0
cues = tr.foley_cues()
```

**Motion (deliberately the opposite curve from `torn_out_page`, not just a slower version of it):**
- `t < grab_t`: `above` fills the frame, untouched — same as `TornOutPage`.
- `grab_t ≤ t < lift_t`: the near corner (LEFT edge — opposite side from `torn_out_page`'s
  rip-to-the-right, so the two devices are visually distinguishable at a glance even from a single
  frame) lifts slightly off the page beneath it (a small, growing soft contact shadow signals the
  lift — no deckle flash, ever: nothing tears, this is a whole page, never cut). Eased with the
  same `_smootherstep` `torn_out_page` already uses.
- `lift_t ≤ t < settle_t`: the page arcs — rotates gently around a spine-side hinge (max ~35°,
  against `torn_out_page`'s rip which keeps accelerating past that), translates left and slightly
  up-then-down like a real page turning, at **constant eased velocity** (no `** 1.8` acceleration
  curve — that curve IS what makes `torn_out_page` read as violent; its absence is what makes this
  read as deliberate). `below` is revealed progressively underneath.
- `t ≥ settle_t`: `below` fills the frame, byte-stable for any later `t` (same governor,
  same self-test shape as `TornOutPage`'s tests 1-2).
- Default timing: `grab_t=0.9, lift_t=1.5, settle_t=2.3` — a 1.4s active turn, LONGER than
  `torn_out_page`'s 1.05s (0.9→1.95) active rip. Slower here reads as unhurried, not sluggish,
  because the motion itself never accelerates.

**Foley:** a single `page_turn` cue at `lift_t` (the instant the page is fully lifted and begins
its arc) — never `paper_tear` (nothing tears; reusing that cue would lie about the action).
**Open item, honestly flagged:** I checked `sound_library/clips/` and there is no clean page-turn/
paper-rustle one-shot in the bank (closest neighbors — `door_gate_creak`, `bread_tearing`,
`veil_tearing` — are all wrong-object). This needs either a quoted ElevenLabs one-shot (same
ask-first pattern round 6 used for the pencil-scratch/dip-drop gaps) or a sourced library asset,
banked before this device ships — not invented in this planning round.

**Governors (carried + new):**
- Never on a page carrying the Word mid-reveal (LAW 1 — same rule as `torn_out_page`).
- Reserved for CALM/REFLECTIVE turns, never a panic/rejection beat — the two transition devices are
  chosen by EMOTIONAL REGISTER, not just "which one is due." Using `lift_away` on a fear beat or
  `torn_out_page` on a calm one is a content error, not a style choice.
- ≤1 per episode by default (same conservative starting budget as every other round-6-family
  device — bleeding-word, candle-only are ≤1/episode too; a device this new does not get a higher
  starting allowance than the proven ones).
- The 10-second rule is a COMBINED budget across the whole transition family: never two
  page-transition devices of ANY kind (`torn_out_page` + `lift_away` together) within 10s of each
  other in the same episode.
- Never the landing spread (the torn-page device owns the landing, per SKILL.md §3).
- Size mismatch raises `ValueError` (same defensive check as `TornOutPage`).

**Self-tests to write (mirrors `TornOutPage`'s 5, same fixture style):** before `grab_t`, frame ==
pure `above`; at/after `settle_t`, frame == pure `below`, byte-stable for any later t; mid-arc frame
differs from both pure frames; `foley_cues()` returns exactly one `page_turn` cue at `lift_t`
(never `paper_tear`); size mismatch raises.

**Naming check (grok's rule from round 6, still binding):** `torn_out_page` (violent transition),
`tear_hole` (the landing's own device), `lift_away` (this new calm transition) — three distinct
terms, no reuse of tear/rip/torn language anywhere in this device's naming or cues.

**Used in this plan:** s07→s08, once, per A1/A2 above.

### B2. `Tally` — the exact-count device

**The gap this closes:** round 8 proved, three separate times (14 tally strokes rendered as
~15-16; 30 coins rendered as 50 until reframed as "three rows of ten"; 7 seals rendered as 5, twice,
honest fail both times) that a generative image model cannot be trusted to render a
Scripture-stated DISCRETE count. `measuring_reed.py` already enforces this same doctrine for
CONTINUOUS magnitudes (a span, a height) — draw the line and ticks deterministically, let the model
draw only the page around it. This device is that same doctrine for COUNTED OBJECTS. Note on the
name: `measuring_reed.py`'s own docstring already refers to "the same progressive-draw machinery as
**Tally** and the map route" — `Tally` is the pre-existing forward-reference name for exactly this
device; I'm using it rather than inventing a new one.

**Not needed for Bronze Serpent.** Numbers 21:4-9 / John 3:14-16 contain no scripture-stated count
(no number of serpents, no number of days, nothing to get wrong). Spec'd here because round 8
proved the gap is real and it will be needed the next time a counted episode comes up — Passover's
firstborn, the 12 tribes, the 5 loaves and 2 fishes, 30 pieces of silver, 7 seals, 14 generations,
"above five hundred brethren at once" (1 Cor 15:6).

**API (modeled on `apply_measuring_reed`'s signature and discipline, adapted for discrete objects):**

```python
from tally import apply_tally

frame = apply_tally(frame, region=(x0, y0, x1, y1), n=30, progress=0.7,
                     mark_kind="coin", layout="rows", seed=17,
                     label_text="thirty pieces of silver", ref_text="ZECHARIAH 11:12")
```

- `region`: the blank-paper reservation the STILL was prompted to leave open (round 8's own
  mechanism find: "the psalm leaf proves models CAN leave ruled space empty" — the generative
  model draws the page WITH a reserved lane; this module never draws over existing linework, same
  discipline as `measuring_reed`'s "never smeared across the drawn illustration itself" rule).
- `n`: the verbatim Scripture-stated count. Like `measuring_reed`, **this module does not know or
  check Scripture** — the caller is responsible for only ever passing a verse-stated `n`.
- `mark_kind`: the glyph drawn per instance — `"tally"` (hand-tally strokes, bundled in 5s with a
  diagonal strike — the real hand-counting convention, not a generic dot), `"coin"`, `"dot"`,
  `"head_mark"` (a tiny ink head-silhouette, for a people-count), or a caller-supplied custom icon
  function.
- `layout`: **`"individual"`** (n ≤ ~7 — loose natural scatter, seeded jitter on position/rotation/
  size so it never reads as a mechanical grid — round 8's own finding that small counts survive
  ONLY when grouped applies in reverse here: below ~7, individual marks are fine); **`"rows"`**
  (~8 ≤ n ≤ ~60 — grouped into rows/bundles, e.g. 3 rows of 10 — this is the ONLY framing round 8
  found actually works above a handful, verified twice); **`"representative"`** (n > ~60 — draws a
  believable partial field (a few legible rows) plus an explicit hand-drawn "…and more" trailing
  mark, and REFUSES to literally emit n discrete marks past that ceiling — this is not a
  workaround, it is the correct reading: round 8's own Witness Roll page found that "too many to
  name" reading the count as overwhelming IS 1 Cor 15:6's own rhetorical point, not a limitation to
  apologize for).
- Progressive draw-on: marks appear along a seeded natural order (never raster left-right/top-
  bottom) as `progress` 0→1 advances, same staggered-front doctrine as `measuring_reed`'s ticks —
  each mark's appearance is a pure function of its own position in the seeded order, so an
  already-drawn mark never moves or re-jitters between frames.
- `label_text`/`ref_text`: reuses `measuring_reed`'s own `_scribed_ink_label` verbatim (ported the
  same way `measuring_reed` ported it from `_s4_assemble.py` — copy the working function, don't
  reinvent the punctuation-glyph fix or the sentence-case rule).

**Governor (hard, not a suggestion):** `layout="individual"` for `n > 7` is a caller error the
module should refuse (raise), not silently render — round 8's evidence is that ungrouped counts
above single digits are simply not reliable, full stop, regardless of prompt wording.

**Self-tests to write:** count of drawn marks at `progress=1.0` exactly equals `n` for
`"individual"`/`"rows"` layouts (a real assertable invariant `measuring_reed` doesn't have, because
a continuous line has no "count" to check — this is the one place `Tally` is strictly stronger than
its cousin); draw-front never regresses (a mark visible at progress `p` stays visible at any
`p' > p`); same seed -> byte-identical marks; `layout="individual"` with `n=8` raises;
`layout="rows"` picks a sane row/column split for a handful of representative `n` values (10 → 3
rows incl. a partial, per round 8's "three rows of ten" precedent for exactly 30).

### B3. Generalized insert-page camera treatment

**What exists today:** `_style_bakeoff/_controlled_pan_test.py` proves the RIGHT motion language
for any insert page (a deterministic $0 camera move — reading-order pan, controlled push/pull —
never generative motion, which would garble the page's own baked lettering), but it is hardcoded to
one specific file (`style3_margin_typology.png`) and one specific keyframe list. Its log-space zoom
interpolation is explicitly borrowed from `mapengine`'s Voyage Camera (`camera.keyframes[].hold_s`
pattern) — the spec below keeps that lineage explicit rather than re-deriving the math.

**Generalize into `panel_animator/insert_page_camera.py`:**

```python
from insert_page_camera import InsertPageCamera

cam = InsertPageCamera(still_path, keyframes=[
    {"t": 0.00, "cx": 0.20, "cy": 0.42, "zoom": 1.85, "hold_s": 1.3},   # close on Numbers 21 panel
    {"t": 0.55, "cx": 0.62, "cy": 0.35, "zoom": 1.85, "hold_s": 0.0},   # glide right, across the arrow
    {"t": 1.00, "cx": 0.50, "cy": 0.50, "zoom": 1.00, "hold_s": 1.8},   # pull back, wide, both labels legible
], apply_raking_light=True, raking_light_at=0.55, apply_grid_choreography=False)
frame = cam.frame_at(t_frac)
```

**What varies per insert page (the parameters this generalization actually needs to expose):**

1. **Which regions to rack focus across** — the caller-supplied ordered `keyframes` list, exactly
   `_controlled_pan_test.py`'s `(t, cx_frac, cy_frac, zoom)` tuple shape, now a parameter instead of
   a hardcoded constant. The Numbers-21→John-3 page's reading order is a simple 2-panel L→R glide;
   a DIFFERENT insert (the Wilderness Road strip-itinerary, say) would instead want a vertical
   bottom-to-top crawl station by station — same engine, different keyframe list.
2. **Hold times** — each keyframe carries its own `hold_s`, reusing `mapengine`'s own
   `camera.keyframes[].hold_s` field NAME and semantics on purpose, so an author who already knows
   the Voyage Camera's field reference doesn't have to learn a second vocabulary for the same idea.
3. **Whether raking-light or grid-choreography apply** — both OFF by default, opt-in flags layered
   on top of the base pan, never baked into the pan itself: `apply_raking_light` (a `raking_light.
   apply_raking_light()` sweep timed to cross the page's one gold element during a hold — this
   episode's page wants exactly one flare arriving as the camera settles on Christ, so
   `raking_light_at` should line up with whichever keyframe holds on the John 3 panel);
   `apply_grid_choreography` (only relevant if the insert page is ITSELF laid out as a multi-panel
   comic grid rather than a single diagram sheet — most inserts, including this one, are single
   diagrams, so this stays off by default; only a literal panel-grid insert would ever need it).
4. **Never generative motion** — reaffirmed, not new: baked lettering pages never go to a
   generative animator (`feedback-never-animate-writing`); this engine is deterministic PIL/ffmpeg
   crop+resize, same as the proven test, forever.
5. Internal, not caller-exposed: the 2× supersample-before-crop step `_controlled_pan_test.py`
   already uses for zoom headroom stays a fixed implementation default (it's plumbing, not a
   creative choice per insert page).

**Concrete keyframes for THIS episode's s08 (needed for the real build, not hypothetical):** open
close on the Numbers 21 panel (Moses + serpent + pole) → hold → glide right across the comparison
arrow to the John 3 panel → hold, with the raking-light gold flare arriving exactly as the camera
settles there → pull back wide to the full two-panel comparison, holding on both labels legible
for the John 3:14 verse card overlay to arrive on top of. Total window ≈ 7.36s (matches s08's real
turn duration, not the 5.5s the original proof test used — the keyframe `t` fractions above are
already expressed as 0..1 so they retime automatically to whatever the real forced-alignment window
for turn 1 turns out to be).

---

## C. Insert-page budget rule

**Rule:** at most **1 insert page per episode of ≤90s** runtime, scaling by **+1 insert per full
additional ~90s** beyond that (so a 3-minute piece could justify 2, a 7-movement 6-8 minute
long-form deep-dive could justify 3-4, spread across separate movements) — and regardless of the
runtime-derived ceiling, **never two insert pages back-to-back**: at least 2 normal Style-1 spreads
must separate any two inserts, so the return to the spine register is felt as a homecoming, not a
second departure.

**Reason, stated plainly:** an insert page is not another item in the paper-layer device list next
to candle-only or bleeding-word. Every one of THOSE devices modifies the SAME page the reader is
already on — the reader never loses their place. An insert page relocates the reader to a
DIFFERENT KIND OF PAGE entirely. That is a strictly more expensive move, and round 6's own verdict
record makes the comparison concrete: 13 of 22 candidate devices were killed specifically for
costing subtlety/momentum at a MUCH cheaper price than a full register switch (a breathing page, a
dog-ear, a wax seal) — if those didn't survive the taste gate, a whole different pictorial mode
must be governed at least as strictly, not more loosely just because it is visually spectacular.
For Bronze Serpent specifically (77.65s, under the 90s line): **the ceiling is exactly 1**, which
is what section A already used — not a coincidence, the rule was derived FROM this episode's own
math, then checked against the general case.

---

## D. Proof render — rendered, PASS at full resolution

**What was rendered:** the Numbers 21 / John 3 typology page (spread s08), Scholar's-Margin style,
byte-identical style block to `combo_style3_jonah_echo.png`. Script:
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_living_sketchbook\_style_bakeoff\
_render_r5_bronzeserpent_typology.py`. Output:
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_living_sketchbook\_style_bakeoff\
bronzeserpent_typology_numbers21_john3.png`

Cost: pre-flight quoted at `python -m pipeline.cost estimate nano_banana_pro` = 2.0 credits
(~$0.30); one job ran, no re-rolls needed (first-pass PASS). Ledgered under `LS_StyleBakeoff`,
note `[bakeoff-r5-bronzeserpent-plan] bronzeserpent_typology_numbers21_john3`, in
`data/spend_ledger.jsonl`. Running total for `LS_StyleBakeoff`: **109.15 of 200cr** (was 107.15
before this round; ~91cr remaining).

**Eye-verify at full resolution against SKILL.md §8a (not a thumbnail):**

1. **Anatomy** — PASS. Moses: one head, staff-holding hand correctly rendered, robed other arm,
   two legs, sandals visible, no duplicate/malformed hands. Christ: arms extended along the
   crossbeam, both hands present (small/stylized at this diagram scale, not distorted), legs
   crossed at a single foot-support with no graphic nail/wound close-up (as the prompt asked).
2. **Period costume, at full res** — PASS. Moses: undyed woolen robe, fur-trimmed mantle, cord
   belt, plain leather sandals, no headwear/ornament — reads authentically ancient Near Eastern,
   nothing modern at the hems/cuffs/footwear. Christ: a plain loincloth wrap, nothing else — the
   standard reverent-crucifixion convention, no anachronism.
3. **Scale/proportion vs. shot type** — PASS. This is a diagram/study sheet by design (same idiom
   as the proven `combo_style3_jonah_echo.png` precedent), not a naturalistic scene — both figures
   are consistently diagram-scaled, proportion reads as intentional, not distorted.
4. **Cross-character distinctness** — trivially PASS. An elderly gray/white-bearded robed prophet
   and a young Christ on a cross are unmistakably different figures; no confusion risk.
5. **Doctrine/palette check (the load-bearing one for this page specifically)** — PASS. The
   serpent-on-pole stays plain bronze/copper throughout, untouched by gold, exactly as specified —
   this matters doctrinally, not just aesthetically: gilding the serpent itself would visually
   claim the OBJECT was holy, the precise error 2 Kings 18:4/Nehushtan records Israel later making.
   Gold appears ONLY as Christ's halo and radiating light ("his lifted figure and the light around
   him") — legible as glory, not costume. Labels "NUMBERS 21" and "JOHN 3" both letter-perfect, no
   stray pseudo-text anywhere else on the page. The crucifixion is reverent — bowed head, no
   visible wounds, no blood, no nail close-up — consistent with this project's standing
   `crucifixion-still-facts` discipline.

**Honest flags (a PASS still gets these, per every prior round's own discipline):**
1. **Photographed-codex framing.** Same known limitation as Round 3's two combo stills and Round
   4's witness-roll/trial-docket pieces: this rendered as a bound book photographed on a neutral
   grey studio ground (visible spine at left, drop shadow), not a true edge-to-edge parchment
   spread. A $0 crop (crop to just the parchment leaf) or a future re-prompt with explicit
   "no book, no table, collage on solid cream" wording fixes this before real assembly — not a new
   problem, the same one every Style-3-family render has carried so far.
2. **No locked Moses cast anchor.** This project has no `cast/MOSES.md` + committed anchor
   portrait anywhere yet (checked). Fine at THIS diagram-panel scale, same as Round 3's own
   precedent on the boat-panel Jesus figure ("diagram idiom absorbs it, §8a.3 would not forgive it
   in a narrative spread") — but s01/s02/s05/s06/s07/s09 in section A's plan all show Moses at
   narrative scale across SEVEN spreads. A real production build of this episode needs a proper
   Moses cast file + committed anchor chained across every appearance BEFORE any of those narrative
   spreads render, or Moses will drift face-to-face across the episode the way Storm's own cast
   discipline exists to prevent. This is real, necessary follow-up work this planning round did
   not (and was not asked to) do.
3. **The serpent-on-staff reads close to the classical medical caduceus/Asclepius emblem.** Not a
   defect — it is the textually correct image (Numbers 21:9 itself: "a serpent of brass... upon a
   pole") — but worth naming: if production wants to push the association away, describe a cruder,
   more primitive ancient-Near-Eastern casting rather than the smoother spiral this render chose.
4. **Christ's hands at the crossbeam ends are small/stylized at full res.** Not distorted, passes
   §8a.1, but noted for honesty the way Round 3 flagged a "rubbery wrist" on an otherwise-passing
   render — a closer crop is worth a second look before this exact file is used past the planning
   stage.

**Verdict: PASS.** This is real evidence the s08 design in section A works as described, not just a
plausible-sounding plan.

---

## What I did NOT build this round, deliberately

- **The 3 skills themselves (`lift_away.py`, `tally.py`, `insert_page_camera.py`).** Specced in
  full above; zero production code written. That is next round's work, after the user reviews this
  plan — matches the brief exactly ("real implementation... happen in later rounds").
- **Any animation.** Out of scope per the brief; every motion claim above (the lift_away arc, the
  insert-page camera pan, the torn-page landing) is a design spec, not a rendered test.
- **A second insert page or a map spread.** Considered honestly in A4 and rejected — the locked
  narration gives it nothing to anchor to.
- **A Moses cast file.** Named as necessary follow-up (honest flag 2 above), not built here — a
  single diagram-panel figure doesn't need it; seven narrative-scale appearances do.
- **Any touch of `longform/EW04_Bronze_Serpent/`.** Read-only all round, per the brief — the locked
  narration is reused, never edited. Everything built lives in `poc_living_sketchbook/
  _style_bakeoff/`.
- **candle-only / bleeding-word for this episode.** Considered and set aside: candle-only requires
  a drawn light source already in the art (a lamp/fire/torch) and this narration is set in open
  wilderness daylight throughout — no natural anchor exists. bleeding-word requires an existing
  Keeper-hand journal entry to bleed (the device bleeds the KEEPER's word, never the Word) — this
  plan doesn't commit to a specific Keeper-hand entry text/placement (a real content call better
  made at build time against the finished art, not speculatively here), so there is nothing yet
  for it to attach to. Both remain open, not rejected outright, for the real build round.

## Spend (honest, vs the 200cr LS_StyleBakeoff ceiling)

| batch | jobs | credits |
|---|---|---|
| rounds 1-4 (prior, Fable) | 45 | 107.15 |
| round 9 (this round, section D) | 1 × nano_banana_pro | 2.0 |
| **running total** | **46 jobs** | **109.15 of 200** |

Every row in `data/spend_ledger.jsonl` under `LS_StyleBakeoff`, note `[bakeoff-r5-bronzeserpent-plan]`.

## Summary for the user

- **A:** 14-spread beat plan for the real 77.65s locked narration, one insert page at s08 (the
  John 3:14 quote, where the typology IS the text), no second insert/map — the content doesn't ask
  for one.
- **B:** 3 real specs — `lift_away` (calm sibling to `torn_out_page`, used once at s07→s08),
  `Tally` (exact-count doctrine, not needed by this episode but real infrastructure for the next
  counted one), `insert_page_camera` (generalizes the already-proven Style 3 pan, with concrete
  numbers for this episode's actual insert page).
- **C:** insert-page budget = 1 per ≤90s, +1 per additional ~90s, never back-to-back — derived from
  this episode's own math, not asserted.
- **D:** rendered the one proof still, PASS at full resolution, 4 honest flags (none blocking), 2cr
  spent, 91cr remaining in the pool.
- **Real follow-up this round surfaced, not yet done:** a Moses cast file + anchor (needed before
  any narrative-scale spread renders), the forced-alignment pass (needed before any spread window
  is treated as real), and the 3 skills' actual code.

Full path to this document:
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_living_sketchbook\_FABLE_ROUND9_BRONZESERPENT_E2E_PLAN.md`
