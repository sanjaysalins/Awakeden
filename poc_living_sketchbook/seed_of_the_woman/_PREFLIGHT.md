# Seed of the Woman LONG — pre-flight (spreads 1-5 + FULL-EPISODE extension below)

**Origin:** these 5 spreads were originally built to validate the Day of
Atonement retrospective's fixes (memory `day-of-atonement-retro-learnings`)
on a throwaway ~33s excerpt. The validation passed and the user chose to
continue this exact episode rather than discard it (2026-08-07) — so this
pre-flight now covers the REAL episode's opening. Content: Genesis 3:8-10,
the opening of the already-locked `longform/05_The_Seed_Of_The_Woman/v1/`
narration, turns 0-3 (narrator -> scripture quote -> narrator -> the LORD).
Real audio, real forced-aligned
timing (`_alignment.json`, 92 words, ffprobe-confirmed against the real
narration.mp3 -- not estimated).

Per fix #7 (stills discipline from prompt 1, not learned mid-build via
re-rolls): every item below is filled in BEFORE the first render, not
discovered after.

## Repeated-element census (incl. SETTINGS, per feedback-repeated-element-census)
| Element | Appears in | Anchor needed? |
|---|---|---|
| Adam | s01, s02 | YES -- new cast anchor (no cross-style reuse; the existing Seed of the Woman oil-painting refs are a different visual style per the locked provider-split rule) |
| Eve | s01, s02 | YES -- new cast anchor |
| Eden garden (SETTING) | s01, s02, s03, s04, s05 (every spread) | YES -- world anchor (trees, dappled light, unspoiled-but-shadowed mood) |
| the LORD (presence) | s04, s05 | NO image anchor -- per this project's own locked convention (Day of Atonement's own "LORD-glow, no figure" device), rendered as light/cloud-presence via prompt language only, never a figure. Consistent across s04/s05 by re-using the same prompt block, not a reference image. |

## KJV-number check (fix #7's discipline)
No load-bearing counts/ages/measurements in this excerpt (Gen 3:8-10 names
no numbers) -- explicitly checked, nothing to verify. Recorded per the
standing rule even when the answer is "none."

## Camera-angle / shot-type plan (per SKILL.md sec.3, filled at plan time)
| # | Name | Shot | Angle | Notes |
|---|---|---|---|---|
| 1 | s01_something_wrong | wide, high angle | looking down into the garden | isolation -- the two figures small against a garden that now feels wrong (color draining at the edges, long shadow) |
| 2 | s02_the_hiding | medium, eye-level, from among the trees | -- | multi-figure (2), genuinely different composition from s01 (close/hidden vs. wide/isolated) so the two don't repeat |
| 3 | s03_verse_card | -- (device-only card) | -- | Scribed Ink over the same garden background, KJV Gen 3:8 verbatim |
| 4 | s04_god_walking | wide, low angle looking up through the trees | -- | light/presence moving through the canopy, no figure |
| 5 | s05_where_art_thou | held close on the light between the trees | -- | the landing -- Fable-designed bespoke composition, no camera move, the question hangs |

## Anchors (built + full-res eye-checked BEFORE any spread render, fix #7)
- `cast/ADAM.md` + `adam_ref.png`
- `cast/EVE.md` + `eve_ref.png`
- `world/eden_ref.png` (+ a short text-canon paragraph, matching the
  "object/world anchors need inline text canon too" lesson from Day of
  Atonement's veil defect)

## Device/bbox plan (filled at plan time, per fix #8 -- Fable pre-designs
the hard beats; bboxes picked via `panel_animator/bbox_sheet.py` once
stills exist, not guessed)
| # | Type | Device | Deliverable |
|---|---|---|---|
| 1 | NS | dramatic_spotlight (still) | full-scope hold, bbox on the two hiding figures |
| 2 | NS | real clip -- Kling (multi-figure) | the hiding, animated |
| 3 | VC | Grand-Text combo (Scribed Ink), lettering built WITH this spread | Gen 3:8 KJV verbatim |
| 4 | NS | real clip -- Seedance (calm, single light-presence) | God walking, no figure |
| 5 | NS | device-only, Fable-designed bespoke hold | "Where art thou?" landing, no camera move |

No mid-build design-rescue calls permitted (fix #8) -- s03 and s05's
compositions are decided here, not during rendering.

---

# EXTENSION — spreads 6-71 (the full episode, pre-flight authored 2026-08-07)

Companion to `_PLAN.md`'s full table. Everything below is decided BEFORE
the first new render (SKILL.md sec.8b point 1): census incl. settings,
camera/shot per spread, KJV-number check, device/bbox plan, and the
Fable pre-designs for every verse card, the landing, and every run of 3+
introspective spreads. A Sonnet execution pass builds from this without
making composition decisions.

## E1. Repeated-element census — extension (3 buckets, incl. SETTINGS)

**Characters**
| Element | Appears in | Anchor needed? |
|---|---|---|
| Adam | s01,02,06,08,11,15,17,24,62 | existing `cast/adam_ref.png` — REUSE |
| Eve | s01,02,06,07,08,11,12,15,17,24,28(small),62 | existing `cast/eve_ref.png` — REUSE |
| Jesus | s42(vig),43(feet),45(silhouette),50(distant),51,53(bg),54(distant),56,64(vig),66(vig),71(risen) | existing repo `cast/JESUS.md` + `jesus_ref.png` — REUSE. Multi-pose lock: s51's approved render chains as 2nd ref into every later Jesus spread. Fail-closed QC on all |
| Mary | s30, 31(bg), 42(vignette) | **NO anchor — deliberate** (bowed, veiled, face averted in every frame; angel = light-presence only; see _PLAN §5.5) |
| the LORD (presence) | s04,05,11,16,17,18,65,70,71 | NO — light only, spreads 4-5's exact prompt block reused verbatim |
| anonymous figures | s27 (father-chain sketches), s43 (crowd feet), s44 (small figures), s48-49 (heel figure), s69 (hands) | NO sheets — anonymity discipline, ≤2-3 sharp faces, mostly no faces at all |

**Portable objects / props**
| Element | Appears in | Anchor needed? |
|---|---|---|
| **the serpent** | s06,07(shadow),12,16,18,19,20,25,42(vig),44(subdued),48,49,54(shadow),55,58(shed skin),62,65(shadow-shape),67(skin) — ~18 appearances | **YES — NEW `world/SERPENT.md` + `serpent_ref.png`**, the episode's one big new anchor. Treatment locked in E2 |
| the fruit | s13 only | NO — text-locked inline (one bite gone, fallen in dust) |
| the study copy (the promise in the Keeper's hand) | s26,40,46,47,60,66 | NO image anchor — consistency via ONE base-page still + IDENTICAL overlay params/seed each appearance (a letterform anchor, $0). Drift here = the same defect class as a face drift |
| the naming page | s34,35,36 | ONE paper-prop still shared by all three beats |
| the gold thread | s21,22,24,25,28,37,45,62,63,64,66 | NO — one shared $0 overlay implementation (draw-on + gleam-pass), identical stroke/color params every use |

**Settings / architecture** (the bucket most likely to get skipped — walked explicitly)
| Element | Appears in | Anchor needed? |
|---|---|---|
| Eden garden | s01-06,08,09,10,11,12,15(far),62,65,68(far),70,71(light) | existing `world/eden_ref.png` — REUSE. One garden, one WORLD |
| the study desk | s26,32,38,39,40,46,60,66 | **YES (cheap)** — ONE desk base still (aged wood, oil lamp, page field), re-dressed per spread. A recurring setting exactly like Day of Atonement's rooms |
| Golgotha | s45(silhouette),50,51,52,53,54,55,56 | **Reuse-check FIRST**: `day_of_atonement/stills/s53_the_cross.png`, `s54_guilt_laid_on_christ.png`, `bronze_serpent_long/stills/s44_shadow_cross.png` (topical-fit gate — eye-check for tabernacle/serpent-pole). Expect 1 new wide (s50) minimum; whatever is approved first chains into the rest of the darkness run |
| the empty tomb | s57, 64(vignette) | **YES — NEW plate** (banks lack tomb plates, known gap); s64's vignette derives from s57's approved render |
| annunciation interior | s30, 31(bg) | NO — single scene, minimal set (dark room, one light-presence, bowed figure) |
| the breach / drawn chasm | s15, 68 | motif, not a render anchor — s68 re-frames s15's approved still (chained) |
| horizon / dawn wilderness | s58,59,67 | check clip/still banks for thread-neutral desert-dawn plates before rendering new |

## E2. The serpent — treatment locked at plan time (the reasoning)

The project's own doctrine: never render Satan sympathetically or
cartoonishly, and Genesis 3's serpent is a real creature under judgment
(Gen 3:14 "upon thy belly shalt thou go"). Locked rules, applied to every
serpent frame:

1. **A real creature, plainly drawn** — no dragon fantasy, no wings, no
   expressive face, no anthropomorphic posture. Loose graphite-and-ink,
   like every other living thing in this style.
2. **The camera looks DOWN on it in every serpent-focus frame** — the
   deliberate inverse of the Bowed Camera. The lens kneels at glory
   (s22, s50); it never kneels to the enemy. (s48's ground-level strike
   frame is heel-focused, not serpent-focused — the one framing
   exception, and the serpent is mid-judgment even there.)
3. **Ink-blue judgment register always; NEVER gold, never warm palette.**
4. **Posture tracks the curse**: among branches only in pre-curse frames
   (s06-s16); from s18 onward belly-to-ground, low in the frame, every
   time.
5. **No charm shots**: never a full-frame face close-up, never eye
   contact with the viewer.
6. **The beaten enemy = the SHED SKIN** (s58, s67): an empty cast skin,
   hollow, in the dust — victory shown without gore and without staging
   the enemy as a fought equal. The head-crush itself is never an impact
   frame: s49 freezes the instant BEFORE; s55 lands the cross-beam's
   SHADOW across the head. The narration's own theology (the cross IS
   the crushing blow) does the visual work.
7. **Serpent = Satan is stated where the canon states it** — on the
   naming page (s34, Rev 12:9), never painted back into the Eden frames
   (the narration's own panel-locked constraint 6).

## E3. KJV-number check (fix #7's discipline — full episode)

No load-bearing counts, ages, or measurements anywhere in Gen 3:8-19 or
the quoted NT verses — explicitly checked, nothing to verify with
`/measuring-reed` (n/a this episode). Staging counts only: TWO people
(one man, one woman), ONE serpent, TWO wounds (head/heel — never
equal-sized in composition, per the narration), ONE pair of hands in s69
(stated in the prompt — anatomy QC). "The empty tomb three days later" is
narration phrasing of the third day; nothing numeric renders. Recorded
per the standing rule even where the answer is "none."

## E4. Camera-angle / shot-type plan (spreads 6-71)

Standing principles for this episode: low angle = glory/reverence only
(the camera kneels at s22's card push and s50's Calvary); high angle
looking down = the serpent under judgment, isolation, or the desk;
eye-level = witness beats, chosen on purpose. Never two near-identical
compositions back to back — the desk spreads alternate framing
(overhead / lateral / pulled-wide) and the serpent spreads alternate
scale (wide-high vs tight-high).

| # | Name | Shot | Angle | Notes |
|---|---|---|---|---|
| 6 | s06_blame_circle | medium-wide, 3 subjects | eye-level | circular staging: the pointing arm leads the eye Adam→Eve→serpent-low; foreground branch occlusion for depth |
| 7 | s07_beguiled_card | close (card over art) | eye-level | Eve's turned profile re-framed from s06; serpent shadow along the bottom edge; letters in the calm upper field |
| 8 | s08_coming_apart | wide | slightly high | the two figures separated by dead center negative space; leaves falling between them; color drains at page edges |
| 9 | s09_unexpected_place | extreme low crop of GROUND | high, looking down at dust | the page darkens; one gold fleck at the lowest margin — nothing else |
| 10 | s10_judgment_falls | very wide | high overhead | Eden as a shape; ONE long shadow lengthening across it |
| 11 | s11_afraid_of_presence | medium two-shot | eye-level, from among trunks | trees bracket the crouched pair (occlusion); the light beyond, faces averted from it |
| 12 | s12_creatures_word | close profile | eye-level | flashback register, desaturated; Eve's ear inclined toward the serpent-shape in branches |
| 13 | s13_the_fruit | object insert, macro | near-ground | fruit large and sharp, one bite gone; garden soft behind (shallow depth) |
| 14 | s14_death_enters | page-scale flat | — (the page IS the subject) | the wash advances from the edges; no figures |
| 15 | s15_the_breach | wide | slightly low from the near rim | the chasm runs diagonal; far garden HIGH and lit; couple small on the near side |
| 16 | s16_watch_closely | wide → locked detail | starts eye-level, locks LOW | hunt_and_lock: hunts the tableau, locks on the dust where the serpent lies |
| 17 | s17_not_adam_not_eve | medium two-shot | eye-level | the two braced; the light enters from a frame edge NOT facing them |
| 18 | s18_turns_to_serpent | wide | HIGH, looking down | the accused: light pivots down onto the serpent low in the dust (camera-looks-down rule begins) |
| 19 | s19_curse_card | card over art | high (inherits s18 register) | Scribed Ink live-write center; serpent-in-dust art beneath |
| 20 | s20_pure_curse | tight | HIGH, closer than s18 | differs from 18 by SCALE (wide-high vs tight-high); belly to the ground |
| 21 | s21_gold_woven_in | page-scale close | — | the curse-lines fill the frame; the gold thread draws through them on a diagonal |
| 22 | s22_promise_card | formal card, frontal | centered, slow push | the film's most formal frame; whole-arrival then ~9s push |
| 23 | s23_let_that_land | same card HELD | no reframe | stillness is the point; grain + faint thread gleam only |
| 24 | s24_before_their_sentences | medium two-shot | eye-level | couple in shadow; the thread's glow a thin line between them; presence-light soft in one corner |
| 25 | s25_promise_in_curse | wide | low horizon | serpent low in a dark band; the thread rises past the TOP edge |
| 26 | s26_her_seed_study | desk overhead | high (the Keeper's view) | lamp pool right; the study copy fills the frame; circle lands on "her seed" |
| 27 | s27_line_of_fathers | page-scale lateral | — | descent-line runs left→right through small father-figures; no lettering anywhere |
| 28 | s28_clue_lights_up | wide page-scale | — | Eve's small figure low-left; thread runs to a far-right warm glow; hard diagonal |
| 29 | s29_fulness_card | formal card, frontal | centered | warm register arrives; per-line reveal |
| 30 | s30_annunciation | medium | slightly LOW toward the light | the light-presence holds the upper field; Mary's bowed, veiled silhouette beneath; face fully averted |
| 31 | s31_holy_thing_card | card over s30's art, tighter | as s30 | letters live in the calm dark left field (never over the light — no verse over busy gold) |
| 32 | s32_honest_match | desk overhead, two pages | high, symmetric | the GAP between the two pages is dead center — the composition's subject |
| 33 | s33_trajectory | very wide lateral | — | the fanned canon-shelf rises on a slight diagonal toward one gold point far right |
| 34 | s34_naming_serpent | desk overhead, page TOP third | high | one continuous page for 34-36; stamp + pressed lines accumulate |
| 35 | s35_naming_mission | same page, MIDDLE third | high | camera drifts down the page — in-page beat, not a page turn |
| 36 | s36_naming_crushing | same page, LOWER third | high | third drift; the page now carries all three testimonies |
| 37 | s37_promise_planted | macro at the book's fore-edge | low | drawn soil at the bottom page; the thread-sprout rises vertically |
| 38 | s38_skeptic_quiet | desk pulled back WIDE | eye-level | the whole desk small and cool; lamp small; gold dimmed |
| 39 | s39_snake_story | close on the margin | high | the writing hand enters from a frame edge; entry ≥54px, stroke-bold (LAW 2) |
| 40 | s40_partly_fair | desk close, two elements | high | study copy left / graphite descent-sketches right; even weight — the concession is honest |
| 41 | s41_shape_of_canon | the whole book | HIGH overhead | the movement's hero wide: pages fanned in one long arc, thread through every page |
| 42 | s42_from_within | page-scale triptych | — | three soft vignettes; the thread emerges FROM the paper fibers; focal-tour visits each |
| 43 | s43_under_your_feet | extreme ground-level crop | eye at floor height | many bare feet on stone + ONE Man's feet; no faces |
| 44 | s44_stands_on_one | wide | LOW, up at the high ground | low = the victory is His; serpent-coil shadow subdued at the base |
| 45 | s45_eden_to_cross | very wide lateral | flat horizon | Eden trees left edge, cross silhouette right edge, thread full width |
| 46 | s46_look_again | desk medium | eye-level across the desk | lamp flame in frame left, page right, hand resting — differs from every overhead desk frame |
| 47 | s47_two_wounds_card | page fills frame | high | swashes arrive under the two phrases as each is spoken |
| 48 | s48_heel_strike | tight, ground-level | low along the ground | the strike at the heel, diagonal; ink-red accent, sparing (the one non-down serpent frame — heel-focused) |
| 49 | s49_head_crush | along the dust | ground-level, heel silhouette ABOVE | frozen instant before the crush; spotlight bbox on heel + head |
| 50 | s50_that_is_the_cross | very wide | LOW (the camera kneels) | Calvary; unnatural midday darkness — ink-wash sky, NEVER storm clouds or lightning |
| 51 | s51_bearing_wages | closer | low | head bowed, wound-free; thin gold-leaf edge present; fail-closed Jesus QC |
| 52 | s52_judgment_on_him | page-scale wide | — | the wash CONVERGES onto the cross — the page is the subject again (mirror of s14) |
| 53 | s53_through_death_card | card over s51 re-framed | low | letters in the dark sky field over a subtle band |
| 54 | s54_seeming_win | deep-staged | eye-level | the LIE of the frame: coil-shadow LARGE in foreground, cross small and far — enemy near, Christ far |
| 55 | s55_the_inversion | SAME framing as s54, held | eye-level | the re-read IS the device: identical composition; the beam's shadow travels onto the serpent's head |
| 56 | s56_triumph_card | the same scene turned | LOW | cross now gold-edged; letters in the lower-third band |
| 57 | s57_empty_tomb | at the tomb mouth | eye-level, off-axis | never centered; gold light from WITHIN; folded linen visible; dawn palette; NO figure |
| 58 | s58_beaten_enemy | at the shed skin | HIGH, looking down | judgment-view consistent; the skin hollow in the dust |
| 59 | s59_end_certain | extreme wide | flat horizon | dawn at one edge; a FAR brighter waiting light beyond the opposite horizon |
| 60 | s60_still_open | desk overhead | high | the open book centered, warm; held |
| 61 | s61_not_altar_not_mountain | page-scale, two vignettes | — | altar / mountain in non-photo-blue underdrawing, never inked; diagonal placement |
| 62 | s62_into_a_curse | wide tableau | eye-level | recall of s24's staging, WIDER (recall register); thread glowing between the figures |
| 63 | s63_before_temple | page-scale MV | — | three pencil ghosts arranged around the solid inked thread's diagonal |
| 64 | s64_named_future | close, lower-right | — | the thread enters from left and completes INTO the cross+tomb vignette |
| 65 | s65_oldest_lie | POV from within the trees | eye-level | heavy foreground occlusion (branches frame ~40% of edges); light center-far; coil-shape in the shadows |
| 66 | s66_promise_kept | desk, two elements | high | s32's framing RETURNED — and now the thread connects the pages (the designed mirror) |
| 67 | s67_matter_of_time | wide | flat horizon | the skin tiny at the horizon band; mostly dawn sky |
| 68 | s68_no_climbing_back | from the chasm floor | LOW, walls looming | unclimbability: garden light far above; s15 re-framed, chained |
| 69 | s69_empty_hands | close-up | slightly high, into the hands | ONE pair of open empty hands; nothing else in frame |
| 70 | s70_step_out | POV, same axis as s65 | eye-level | the light in the clearing WIDENS toward the viewer; camera locked — the light moves |
| 71 | s71_found_by_him | frontal page-scale → through the tear | eye-level on Christ within | the tear is frontal; inside it Christ mid-distance in the s04 garden light; sacred stillness |

## E5. Device/bbox plan (spreads 6-71)

Bounding boxes are picked with `panel_animator/bbox_sheet.py` once stills
exist (sec.8b point 2), never eyeballed; "bbox:" below names the intended
subject so the picker session is mechanical. Device-quota guard (the Day
of Atonement 28%-raking-light lesson): no named $0 device exceeds 6 of 66
new spreads — tally in E7.

| # | Type | Device | Deliverable |
|---|---|---|---|
| 6 | NS | real clip — Kling (ACTING 1) | blame gesture completes, holds; 3 subjects |
| 7 | VC | Scribed Ink composite ($0) | Gen 3:13b over the profile art; 13.0 g/s |
| 8 | NS | real clip — Seedance | leaves drift; color drains (sl13 candidate) |
| 9 | NS | $0 bespoke: gold-fleck breathe | pre-designed E6-A |
| 10 | NS | real clip — Seedance | shadow lengthens, state-only |
| 11 | NS | real clip — Kling | two crouched figures, light beyond |
| 12 | NS | real clip — Seedance | branch sway ONLY; serpent still |
| 13 | NS | dramatic_spotlight ($0) | bbox: the fruit |
| 14 | NS | wash-creep ADVANCE ($0) | edges → center; pays off at s52 |
| 15 | NS | parallax-panel ($0) | near-rim layer vs far-garden layer |
| 16 | NS | hunt_and_lock ($0) | hunt the tableau, lock LOW on the serpent |
| 17 | NS | real clip — Kling | braced faces, subtle |
| 18 | NS | real clip — Seedance | light pivots down; serpent still |
| 19 | VC | Scribed Ink live-write ($0) | Gen 3:14, 14.0 g/s; card holds through the pause |
| 20 | NS | real clip — Seedance | dust settles, state-only |
| 21 | NS | Thread draw-on ($0) | the thread's FIRST appearance; through the curse-lines |
| 22 | VC | Illuminated Rubric, WHOLE arrival ($0) | LAW 1; gold dropped cap; slow push — pre-designed E6-B |
| 23 | NS | $0 hold: grain-boil + held-breath QP1 | s22's card held; nothing else moves |
| 24 | NS | real clip — Kling | two waiting faces; thread-glow line |
| 25 | NS | Thread gleam-pass ($0) | bottom-dark band → top edge |
| 26 | VC | annotators-circle ($0, 1/1) | on "her seed"; study copy pre-written — pre-designed E6-C |
| 27 | NS | $0 drawn-line reveal | descent line draws father→father (thread-code family) |
| 28 | NS | real clip — Seedance | far glow warms; thread pre-drawn in the still |
| 29 | VC | Illuminated Rubric, per-line ($0) | Gal 4:4 — pre-designed E6-D |
| 30 | NS | real clip — Kling (ACTING 2) | bow completes, holds; face averted by design |
| 31 | VC | Scribed Ink composite ($0) | Luke 1:35b, 13.6 g/s — pre-designed E6-E |
| 32 | NS | focal-tour ($0) | halo: promise page → Gospel page → the GAP |
| 33 | NS | real clip — Seedance | ember-glow breathes at the far point |
| 34 | VC | Scribed Ink ($0, proven — REVISED, "Ink Stamp"/"Typeset" don't exist as built tools) | naming page top third — pre-designed E6-F |
| 35 | VC | Scribed Ink ($0, proven) | middle third |
| 36 | VC | Scribed Ink ($0, proven) | lower third |
| 37 | NS | Thread draw-on upward ($0) | seed → sprout → up the page-edges |
| 38 | NS | raking-light ($0 — its ONE use) + held-breath QP2 | the lamp sweeps the cooled desk |
| 39 | NS | keeper-hand entry ($0, 1 entry) | "Just a snake story?", energy ~0.35; LAW 2 sizes |
| 40 | NS | $0 hold + spotlight shift | bbox pair: study copy / descent sketches |
| 41 | NS | real clip — Seedance | pages stir faintly; thread gleams along the arc |
| 42 | MV | focal-tour ($0) | three vignettes in narration order — run pre-design E6-H |
| 43 | NS | real clip — Kling | many feet + One's feet; no card for the 0.6s fragment (deliberate) |
| 44 | NS | real clip — Seedance | dust + light, state-only |
| 45 | NS | Thread gleam-pass ($0) | left (Eden) → right (cross silhouette) |
| 46 | NS | real clip — Seedance | flame breathes ONLY; page region static (text overlay) |
| 47 | VC | Scribed Ink + 2 timed swashes ($0) | Gen 3:15b, 11.8 g/s — pre-designed E6-G |
| 48 | NS | real clip — Kling (action) | the strike; ink-red sparing |
| 49 | NS | dramatic_spotlight ($0) | bbox: raised heel + serpent head; frozen instant |
| 50 | NS | real clip — Seedance | darkness thickens; never storm |
| 51 | NS | real clip — Kling | fail-closed Jesus QC; HF-NSFW → direct-Kling fallback |
| 52 | NS | wash-creep RETREAT ($0, proven real mode — REVISED, "CONVERGE" isn't implemented) | the s14 payoff; "falls on Him" staged in the still's own composition, not new motion geometry |
| 53 | VC | Scribed Ink composite ($0) | Heb 2:14b over the cross art, 13.8 g/s |
| 54 | NS | real clip — Seedance | shadow deepens; coil pre-risen in the still |
| 55 | NS | $0 bespoke: shadow-sweep | pre-designed E6-I; beam shadow travels onto the head, holds |
| 56 | VC | Scribed Ink composite ($0) | Col 2:15 — TIMING FLAG (mid-turn; alignment pass) |
| 57 | NS | real clip — Seedance | inner light breathes; dust motes; NO figure |
| 58 | NS | real clip — Seedance | dawn wind stirs dust; the skin itself still |
| 59 | NS | $0 bespoke: dual-glow breathe | two horizon lights, opposite edges, slow alternate breathing |
| 60 | NS | $0 warm-glow breathe + grain-boil | text on page — no base motion |
| 61 | MV | focal-tour ($0) | altar → mountain; both STAY pale underdrawing |
| 62 | NS | real clip — Seedance | figures still; thread gleams |
| 63 | MV | $0: thread gleam-pass | ghosts pre-drawn; only the thread is solid |
| 64 | NS | real clip — Seedance | warm light rises on the vignette |
| 65 | NS | real clip — Seedance | leaves stir; light steady; camera locked (sl16 candidate) |
| 66 | NS | focal-tour ($0) | copy → thread → vignette; the s32 mirror |
| 67 | NS | real clip — Seedance | wind, dust, calm |
| 68 | NS | parallax-panel ($0) | chasm-wall layer vs far-garden layer; s15 chained |
| 69 | NS | real clip — Kling | ONE pair of hands; tremble → still; anatomy QC |
| 70 | NS | real clip — Seedance | the light WIDENS; named motion only |
| 71 | LAND | `torn_out_page` transition (real, built) into a plain static/breathing hold, same as s05 ($0, proven — REVISED, "tear_hole" isn't built; see DoA's own s76_landing.py precedent) | pre-designed E6-J; INV-26 ≥3.0s; INV-27 watermark |

## E6. Fable pre-designs (sec.8b point 1 — decided HERE, not mid-build)

### E6-A · s09 gold-fleck breathe (bespoke $0)
Base still: the s01 garden register darkened ~55% with the ink-blue night
ramp, horizon line kept low. ONE gold-leaf fleck, 14-18px at 1080-width,
sits in the dust band at ~x 62% / y 91% (inside the lower-third but above
the 18% UI band — check against the caption zone at build). Behaviour:
opacity 0.55→0.9→0.55 on an ~3.4s ease-in-out cycle, plus grain-boil over
the whole frame. Nothing else moves. The fleck is the FIRST gold on any
page since the style's edge-strip — the promise pre-echoed, one spark in
the dust where the serpent will be cursed.

### E6-B · s22 — Gen 3:15, Illuminated Rubric, formal peak 1 (THE verse)
Ground: the s21 curse-page art (dark ink-lines, the gold thread already
run through them) dimmed 30% behind a warm parchment scrim band occupying
the center ~55% of frame height, edges torn-soft. LAW 1: god voice — the
whole card ARRIVES COMPLETE between two frames at ~1.2s in (one soft
paper-settle thump in the SFX pass), never letter-by-letter. Layout: gold
dropped cap "A" (OLDENGL.TTF, gold fill + thin ink stroke, cap height
~3.2 body lines), body in printed-Bible serif italic between two thin
hairline rules — 4 lines, ragged right: "And I will put enmity between
thee and the woman, / and between thy seed and her seed; / it shall
bruise thy head, / and thou shalt bruise his heel." Reference "GENESIS
3 : 15" stamps last in rubric-red serif caps, small, below the lower
rule, at the verse's audio END (~142.5s). The slow push (scale 1.00→1.06
across the full 11.0s) carries the hold; the thread behind the scrim
keeps its faint gleam. Hard exit margin: card persists into s23 (same
frame held) — NO exit before the cut, by design; s23 is its stillness.

### E6-C · s26 — the study copy + the episode's ONE annotator's circle
Base: the desk anchor still, overhead, lamp pool warm-right. The study
copy is PRE-WRITTEN (it arrives already complete — the Keeper copied it
out between scenes; no letter reveal): Scribed Ink (KUNSTLER.TTF, seeded
jitter, seed FIXED = 315 for every study-copy appearance), 5 lines,
≥54px equivalent (LAW 2), the full Gen 3:15 text. This is Keeper-register
study ink, NOT the Word's own formal card — which is why a human
annotation may touch it (the /bleeding-word ban protects the Word's
Scribed Ink; the circle is allowed on a study copy). At the narrator's
"her seed" (~163.4s, refine at alignment pass) the annotator's circle
draws itself around the words "her seed" in line 2: full sweep ~0.55s,
then the lighter offset second pass ~0.4s, ink-red, hand-wobbled ellipse.
Circle inks fully at least 0.8s before the spread ends (hard exit
margin). Budget: 1/1 — no other circle anywhere in the episode.

### E6-D · s29 — Gal 4:4, Illuminated Rubric, formal peak 2 (the pair)
Deliberately the SAME structure as E6-B — dropped cap "B", same serif
body, same hairline rules — so the two Rubrics read as a matched pair:
the promise SPOKEN (dark page, whole arrival) / the promise KEPT (warm
page, revealed). Ground: plain warm parchment, the first fully warm page
of the film; a faint gold thread enters from the LEFT edge and passes
under the lower rule (continuity from s28's glow). Scripture voice, so
per-LINE arrival is allowed: 3 body lines, each fading in 0.25s as the
voice reaches it ("But when the fulness of the time was come," / "God
sent forth his Son, made of a woman," / "made under the law."). Reference
"GALATIANS 4 : 4" rubric-red at the end. No push — this card sits still
and warm (contrast with E6-B's push is the pair's designed asymmetry).

### E6-E · s31 — Luke 1:35b, composite over the annunciation art
No card page: the verse letters directly onto s30's art, in the calm dark
LEFT field (the light-presence owns the right — verse never over busy
gold). Scribed Ink, 3 lines, 13.6 g/s, letter reveal timed to the voice;
underline swash arrives under "shall be called the Son of God" on those
words (~206-208.6s). Reference "LUKE 1 : 35" small, rubric-red, below.
Mary's silhouette is NEVER overlapped by type (letterer law: type never
covers a face — her averted head counts). Hard exit: all ink complete by
208.0s, 0.6s before the cut.

### E6-F · s34-36 — THE NAMING PAGE (one page, three beats) — REVISED 2026-08-07
ONE paper-prop still: an open inquest page, NOT a grid of cells (the Flap
lesson — a grid reads as a scoreboard regardless of texture). Three
stations arranged top / middle / lower third. **Revised after the
independent-review panel found "Ink Stamp" and "Typeset pressed lines"
don't exist as built tools** (only an unpromoted, never-validated
prototype under different naming) — each station now uses the SAME proven
Scribed Ink technique as the composite quotes (s7/s31/s53/s56): a short
hand-lettered question line, then the verse line, both in the established
ink-hand style. The original worry ("Rev 12:9's 46 glyphs land in 2.56s,
too fast for Scribed Ink") doesn't actually apply once the constraint is
named correctly: the LETTERING doesn't have to match the spoken pace
word-for-word inside the 2.56s vocal utterance — it has the whole 11.4s/
8.1s/8.6s spread duration to letter in at a comfortable ≤15 g/s ceiling
(46 glyphs over even 4-5s of held spread time ≈ 9-11 g/s, well inside the
proven range), same logic already used for s19's live-write pacing.
Camera: overhead, drifting DOWN the page ~12% per beat (in-page beats, no
page turns). Station text: "THE SERPENT?" → "that old serpent, called the
Devil, and Satan." (REVELATION 12 : 9) · "THE MISSION?" → "For this
purpose the Son of God was manifested, that he might destroy the works of
the devil." (1 JOHN 3 : 8) · "THE CRUSHING?" → "And the God of peace shall
bruise Satan under your feet shortly." (ROMANS 16 : 20). References
rubric-red, small, right-aligned per station. Grain-boil throughout; each
station complete ≥0.5s before its beat ends.

### E6-G · s47 — Gen 3:15b re-study, the two-wounds card
The SAME study copy asset as E6-C (fixed seed 315, same base still, lamp
unchanged — the letterform anchor) but framed page-full. The clause
"it shall bruise thy head, and thou shalt bruise his heel." re-inks
darker over its own line (a re-inking pass, 11.8 g/s, following the
voice), then TWO underline swashes: under "bruise thy head" as it is
spoken (~338.5s) and under "bruise his heel" (~340.8s). KJV-strict: "it
shall bruise" — never "he" — on every lettered appearance. Complete by
341.4s (0.55s exit margin).

### E6-H · introspective run 2 — M5, the skeptic's desk (s38-45)
The danger zone: eight spreads of argument. The run's visual spine is a
DESK STORY with two escapes into grandeur — monotony is broken by
framing rotation and by the run's own designed energy curve:
- s38 pulled-back wide, gold DIMMED, raking-light's one sweep (the
  argument cools the room) — held-breath quiet point 2 sits here.
- s39 close margin + the Keeper's hand writing the objection (the only
  keeper-hand entry of the film — the skeptic's voice in OUR handwriting,
  which is the point: the objection is taken seriously, owned).
- s40 two-element close: the concession given EQUAL visual weight
  (copy left, ordinary-descent graphite right) — honesty is symmetric.
- s41 ESCAPE 1: the hero overhead — the whole book fanned, the thread
  through every page. The answer is not a clever phrase; it is the shape
  of the entire canon, seen at once.
- s42 the three-witness MV (serpent named / works destroyed / woman's
  child), focal-tour in narration order; the thread visibly emerges from
  INSIDE the paper fibers — "followed out from within" made literal.
- s43 ground-level feet (the second objection gets a concrete image, not
  a diagram; the 0.6s quote fragment deliberately unlettered).
- s44 ESCAPE 2: low-angle gold — the shared victory STANDS ON the Victor;
  serpent-coil shadow subdued under the ground-line.
- s45 the resolution wide: Eden→cross, thread full-width — the movement
  exits pointing at M6.
Energy: cool (38) → tense (39) → level (40) → lift (41) → warm (42) →
grounded (43) → lift (44) → resolve (45). No two adjacent desk frames
share a framing (wide / margin-close / two-element / overhead).

### E6-I · s54-55 — the inversion pair (bespoke shadow-sweep)
One composition, two spreads — the film's thesis image. s54: deep-staged
still, the serpent's risen coil as a LARGE foreground shadow-mass, the
cross small and distant beyond — the frame itself tells the lie ("the
serpent is winning"). Seedance: shadow deepens only, state-language.
s55: the IDENTICAL framing (same still, re-used — the re-read is the
device), with the $0 bespoke sweep: the cross-beam's shadow-edge travels
diagonally (~2.8s, ease-out) across the ground until it lies exactly
across the serpent's head, then HOLDS for the spread's remainder,
grain-boil only. Mask edge feathered ~30px; travel path and final
head-bbox picked with bbox_sheet.py on the real still. No impact, no
gore: the shadow of the cross IS the crushing — the narration says it,
the page shows it.

### E6-J · s71 — THE LANDING (pre-designed complete) — REVISED 2026-08-07
**Revised after the independent-review panel found "tear_hole" isn't a
built device anywhere in the repo** (DoA's own `_s76_landing.py` states
this outright and used a real $0 held frame instead: "tear_hole... isn't
built... a reverent held/pushed frame now, real, finished, $0"). Same call
here, with the ALREADY-BUILT `torn_out_page` (panel_animator/
page_transitions.py) doing the "arrival" work instead of an invented
in-frame tear effect: at ~490.4s ("the One whose heel was struck...") the
`torn_out_page` TRANSITION runs (real, tested primitive — deckled fiber
edges, an existing page torn away) carrying INTO s71's own still, rather
than the still itself animating a tear. Within: the risen Christ,
mid-distance, standing among the trees in the SAME warm seeking-light
built for s04 (the hook→landing mirror: the God who came looking is the
rescue) — NEW still, jesus_ref + s51-approval chained, fail-closed QC, no
wounds emphasized, arms open but NOT mid-motion (lock arms explicitly —
the known arm-raise pressure failure). "Come out, and be found by Him."
lands at ~498.6-500.45s over sacred stillness: the same proven bespoke
static/breathing hold as s05 — nothing moves but the gold glow breathing
(period ~4s, amplitude subtle) and grain-boil. INV-26: audio and video
both run ≥3.0s past the last word. INV-27 watermark. Optional /ribbon-marker
A/B AFTER the last word (settles ~0.6s post-voice, margin lane) — ships
only if it beats the straight landing in the user's A/B.

### Other pre-designed runs (composition logic, so Sonnet decides nothing)
- **Run 1 — M2's descent (s12-15):** flashback-desaturated close (12) →
  macro object (13) → the page itself dying (14, wash) → the drawn
  chasm thesis (15). Four DIFFERENT grammars in a row by design
  (figure / object / medium / diagram) — the descent accelerates by
  changing language every cut, and s14's wash is the seed of the film's
  s52 payoff.
- **Run 3 — t36's climax (s54-59):** lie (54) → inversion (55) → triumph
  card (56) → tomb (57) → shed skin (58) → two horizons (59). The pair
  54/55 shares ONE composition (designed); 56 letters over its turned
  version; 57-59 then WIDEN step by step (mouth-of-tomb → ground → full
  horizon) so the movement exhales after the inversion instead of
  stacking more argument.
- **Run 4 — M7's meditation (s60-64):** open book (60) → pale
  underdrawing MV (61) → sentencing recall (62) → pencil-ghost MV (63) →
  the completed vignette (64). Alternation page/scene/page/scene by
  design; the two MV spreads are visually opposite (blue underdrawing
  that STAYS pale vs graphite ghosts around a SOLID gold thread) so the
  run never reads as two of the same trick.

## E7. Device-budget tally (the 28%-lesson guard, checked at plan time)
**Recounted 2026-08-07 after the independent-review panel's device fixes**
(hunt_and_lock now real+tested; Ink Stamp/Typeset -> Scribed Ink;
wash-creep converge -> retreat; tear_hole -> torn_out_page+static hold):

66 new spreads: **Kling 10 (15%)** · **Seedance 20 (30%)** · $0 cards 12
(18%) · $0 devices 24 (36%). Named-device counts: thread-grammar 6
(all `thread_opacity`/`thread_swell`, proven functions only) · focal-tour
4 (s32/42/61/66) · parallax 2 · wash-creep 2 (advance + retreat, a
designed pair, both proven real modes) · dramatic_spotlight 2 · bespoke
holds 4 (s9/55/59/60) · hunt_and_lock 1 (`panel_animator/hunt_and_lock.py`
— promoted from Jericho's one-off code and tested 2026-08-07 against an
existing still, no new spend) · raking-light 1 (capped deliberately — it
ate 28% of Day of Atonement by being frictionless) · keeper-hand 1 ·
annotators-circle 1 · Scribed Ink (naming page) 3 · Illuminated Rubric 2 ·
`torn_out_page` transition 1 (landing only, real built primitive) + static
hold (shares the s05-proven device, not counted separately). Kling sits
exactly at 15%, the lint WARN threshold, not FAIL — worth a human glance
once real segments exist, not a blocker. Card spreads never adjacent
except the designed s34-36 continuous page (user sign-off pending, _PLAN
§7.2).

## E8. Alignment caveat + build-order notes

- Turn boundaries from `_turn_boundaries.json` are ground truth ±1-2s;
  every sub-turn seam inside long narrator turns (s8/9, s10/11, s12-15,
  s17/18, s20/21, s23-25, s26-28, s32-34, s39-42, s44/45, s48/49,
  s50-52, s54-59, s61-64, s65-67, s68-71) is a word-proportional ESTIMATE
  — run the standard alignment-correction pass and re-cut seams before
  build; per-card ink timings (E6) refine then too.
- s05's end extends 33.03 → 33.80 at that pass (excerpt vs full-file
  timing; its designed hold just breathes longer).
- `motion_lint.py --episode-dir` after every ~10-spread batch (sec.8b
  point 3); `_layer_check.py` before any card spread is called done
  (point 4); finishing via `_finish_long.py` + this folder's existing
  `finish_config.py` (point 5); `finish_check.py` before "finished" is
  ever said (point 6); `_s6_assemble.py` freshness stamps already proven
  on this episode (point 7).
- No mid-build design-rescue calls (fix #8): every hard beat above is
  designed HERE. If a render fights one of these designs twice, the
  design comes back to Fable — it does not get improvised at build.
