# DESIGN BRIEF — Episode 5, "The Barrel That Did Not Waste"

1 Kings 17:8-16 (Elijah and the widow of Zarephath) · NT link Luke 4:25-26 ·
Dead ink: **Fray only** (fear/doubt — the text's own verbatim "Fear not", 1 Kings 17:13) ·
Swirl capped Stage 1-2 (OT episode, per the series-plan row) · panel_style **woodcut_hybrid** throughout.

Fable design pass, 2026-08-30. This brief is the single creative source for the
Sonnet implementation pass (episode.py PageSpec/CoverSpec objects). Narration and
voices are LOCKED — nothing here changes a spoken word. Every choice below states
its WHY, in the spirit of Naaman's own episode.py docstring. Open questions are
flagged inline and collected at the end — do not silently resolve them.

---

## 0. The shape of the episode, in one paragraph

The narration opens on the widow (not on Jesus — the opposite of Naaman), so the
covers belong to HER world: front = the widow gathering sticks in the famine (the
hook's own image), back = the open barrel in dawn light (the landing's own image,
"He needs it open"). The Nazareth beat goes to an INTERIOR page (F05), exactly as
Naaman placed its own Nazareth beat at F06 — and deliberately NOT on a cover,
because Naaman's front cover already spent the Nazareth-cliff image and repeating
it would read as a rerun to a series viewer (full reasoning in §4). Six interior
pages + two covers, mirroring Naaman's count because this narration's own beats
divide that way (shown in §1), not because Naaman did it. The Fray peaks on the
widow's death-sentence line ("we may eat it, and die"), clears sharply in the
hard cut that lands on Elijah's "Fear not", and finishes clearing in the next
cut when she obeys — a two-step descent (FR3 → FR1 → FR0) that mirrors Naaman's
Stain turning at F04 and clearing in the F04→F05 cut. The swirl rises against it
(0 → 0 → 1 → 2 → 2 → 2), first trace arriving WITH the word "Fear not", crossing
the falling Fray exactly at the gospel turn.

---

## 1. Narration beat map → units (why six interior pages)

The locked narration divides into 8 natural picture-beats. Word weights are my
own estimates (sum 212, matching my count of the narration); the assembler
treats them as proportions, same as Naaman.

| Unit | Narration beat | Words | Voice(s) |
|---|---|---|---|
| **front** | "A widow was gathering sticks for her own funeral fire." | 10 | narrator |
| **F01** | "A stranger passing through, Elijah, asked her for water. Then bread. She had nothing to spare — nothing, period:" | 22 | narrator |
| **F02** | "I have not a cake, but an handful of meal in a barrel… that we may eat it, and die." | 27 | **widow** |
| **F03** | "Elijah answered:" + "Fear not; go and do as thou hast said: but make me thereof a little cake first…" | 33 | narrator + **elijah** |
| **F04** | "She fed a stranger before she fed her own child. The barrel of meal wasted not. The oil did not fail, for as long as the famine lasted." | 26 | narrator |
| **F05** | "Centuries later, Jesus named her by her own city:" + "Many widows were in Israel… save unto Sarepta, a city of Sidon…" | 38 | narrator + **jesus** |
| **F06** | "Of every hungry house in Israel, God went to the one with nothing left to give — and asked her anyway." | 22 | narrator |
| **back** | "She didn't have enough. She gave first anyway. The barrel that fed a stranger fed her too — it never once ran dry. God doesn't need your barrel full. He needs it open." | 34 | narrator |

**Why not 7 interiors:** the only candidate split is F04 (giving 10w + miracle
16w). A 10-word unit is a ~3.5s slot — below a clip's natural length, pure
churn — and the narration itself compresses giving and miracle into one breath,
so one page compresses them into one scene (§6, F04). **Why not 4 (the Ashes
count):** the two voiced OT dialogue beats (her line, his line) each carry a
Fray state change and cannot share a page with each other or with the meeting —
that alone forces F01/F02/F03; the miracle, the Jesus citation, and the
reflection are three more irreducible pictures.

---

## 2. The motif arcs (the episode's spine)

### Fray (the widow's fear) — descending

| Page | Fray | Rendering |
|---|---|---|
| F01 | **FR1** | Loose, slightly overworked hatching in her figure only; contour intact and single |
| F02 | **FR3** | Peak: her contour visibly broken and doubled, a tremored second line beside the true one, scratchy flying hatching |
| F03 | **FR1** | HARD CUT clear — lands exactly on "Fear not". Hatching still loose, contour whole again |
| F04–F06 | **FR0** | Confident single-struck line, stated explicitly (see the override note below) |

- **The clearing is the cut, never a clip.** FR3→FR1 happens between F02 and
  F03 (the page turn IS "Fear not" landing); FR1→FR0 between F03 and F04 (she
  obeys). Never a within-clip dissolve — same law as Naaman's Stain (F04→F05)
  and the Hem. Every Fray page's animation gets the page-global fence with the
  Thomas-validated wording ("…including the broken, tremored linework of the
  widow's figure").
- **Why F01 is only FR1, not FR2 (a real trap, please keep):** the widow's
  full-figure and face refs are CROPPED FROM F01's approved render. A heavily
  frayed debut would bake tremored linework into her reference and pressure
  every later steady-line page toward fray — the same reason Naaman's ref
  carried his patches and F05 needed an explicit healed-override. So F01 keeps
  the fray subtle (loose hatching only, contour clean), and every FR0 page
  carries an explicit steady-line override clause: *"her contour drawn steady,
  confident, and single-struck, no doubled or tremored line anywhere in her
  figure."* Story-wise the jump FR1→FR3 also reads true: fear crests the
  moment she says the death plan out loud.
- **FR3 is untested** (Thomas only proved FR2). Attempt it on F02 —
  fallback: if "visibly incomplete contour" reads as a render defect or a
  ghost-double at QC, drop to a strong FR2 (broken/tremored, contour complete).
  Pareidolia eye-check applies. **[OPEN — flagged]**
- Elijah's linework is stated *"steady, single-struck, confident"* on every
  shared page (the Thomas contrast pattern) — the Fray is hers alone.

### Swirl (living blue-gold ink) — rising

| Page | Stage | Anchor |
|---|---|---|
| front | none | Deliberate: famine-before-the-word. Naaman's front carried a blue curl because its subject was Jesus; this front is the Stage-0 world |
| F01 | **0** | Canonical absence statement |
| F02 | **0** | Her lowest page stays absolutely stark (and keeps FR3 within high-tide) |
| F03 | **1** | ONE thread rising from the two dry sticks lying on the ground between them — the wood she gathered to die with is the first thing the life touches. First trace arrives WITH "Fear not" |
| F04 | **2** | Few threads + one bloom rising from the meal jar's open mouth |
| F05 | **2** (episode cap, held) | Threads + faintest gold + one bloom rising from the closed scroll on the reading desk — Naaman F06's exact anchor, kept as a deliberate series constant: the life is in the word |
| F06 | **2** (held) | Threads + one bloom hanging high above the ONE lit house, touching nothing |
| back | curl | One small hard-capped closed curl of blue-gold rising from the barrel's open mouth (Naaman-front-cover language family: "no longer than a hand's width… never straightening, never trailing") |

- **Why the cap is Stage 2, not Stage 3, on the Jesus page:** the task framing
  reserves Stage 3 for fulfilment-on-page, but the series-plan row caps this
  episode at Stage 1-2, and Naaman's own precedent held its Jesus page at the
  episode cap (Stage 2). I follow the plan + precedent: Stage 2 held at cap on
  F05/F06. **[OPEN — flagged, trivial to raise to 3 on F05 if the user prefers
  the task-text reading]**
- **Why the sticks anchor on F03, not Elijah:** anchoring the first trace to
  the word-bearer repeats the Doubting-Thomas placement the user flagged as
  "missing what the swirls are meant to be" (meaning that only works when
  explained). The sticks are HERS, in frame between the two figures, and the
  inversion (funeral wood → first life) reads without narration.
- **High-tide check, every page:** F01 1+0 · F02 3+0 · F03 1+1 · F04 0+2 ·
  F05 0+2 · F06 0+2 — all ≤ 4. On F03 (the only page where both motifs
  coexist) the QUAD lock applies: the thread touches only the sticks and the
  air above them, clean paper between it and both figures, form separation
  stated both ways.

---

## 3. Refs — who and what needs pinning

All new refs live in this episode folder's `refs/`. Chain order is hard
(render_still stops on a missing ref).

### Characters

**THE WIDOW** — new to the series. Full design (build text, use verbatim):

> the widow of Zarephath, a Phoenician woman in her middle thirties made older
> by famine, thin and small-framed with a worn upright dignity, hollowed cheeks
> and large deep-set dark eyes, sun-lined olive skin, dark hair bound back
> under a plain widow's head-scarf of undyed grey-brown wool with a narrow band
> of faded clay-red woven at its edge, wearing a patched ankle-length tunic of
> faded ochre-brown under a loose olive-grey shawl knotted at one shoulder,
> bare dusty feet

Why: young enough to have a small son, famine-worn but dignified (the text
shows her courteous and honest even in despair); the clay-red scarf band is her
likeness pin (Naaman's bronze band pattern); **no blue anywhere in her dress**
(chromatic reservation — blue belongs to the motif alone).
Refs: `widow_ref.png` (full figure) + `widow_face_ref.png` (she gets a true
close-up page, F02, and a face-study panel on F06 — full-figure crops are too
small to pin a face). Both cropped from F01 approved.

**ELIJAH** — new to the series. Grounded in the text's own description
(2 Kings 1:8 "an hairy man, girt with a girdle of leather"; the mantle,
1 Kings 19:19). Build text:

> Elijah the Tishbite, a wilderness prophet in his fifties, lean and rawboned,
> weathered hard by sun and travel, a deep-lined dark-bronzed face with fierce
> steady eyes, a great unkempt mane of thick grey-streaked black hair and a
> full wild beard, wearing a rough shaggy mantle of dark camel-hair thrown over
> a coarse knee-length tunic of undyed wool, a wide plain leather girdle bound
> about his loins, worn leather sandals, a tall rough-cut walking staff in one
> hand

Why: maximally distinct silhouette from every existing series man — Jesus
(young, smooth plain robe, no staff), Naaman (armored Syrian), Jacob,
Nathanael. The shaggy mantle + staff read at any distance.
Refs: `elijah_ref.png` + `elijah_face_ref.png` (he gets a close eye-study
panel on F03). Both cropped from F01 approved.

**THE SON** — minor, deliberately ref-free: he appears in a main scene ONCE
(F04, at the table) and on no other still, so the recurring-subject rule never
triggers. Design line (author per-page, no build constant needed): *a thin boy
of seven or eight, large dark eyes in a small famine-thinned face, a plain
patched undyed tunic, bare feet.* Beats that mention him elsewhere are carried
by object surrogates (F02's "two empty bowls" panel; F06's "three full bowls"
panel) — cheaper, and honestly more affecting. If a later revision puts him on
a second still, he must get a ref then.

**JESUS** — SERIES CONSTANT. `refs/jesus_ref.png` copied verbatim from
episode 4's own `refs/jesus_ref.png` (itself from ep1/ep8's approved crop).
JESUS_BUILD text reused verbatim from Naaman's episode.py. No redesign, no
approval cycle.

### Objects / locations

**THE BARREL + CRUSE** — the two objects the miracle turns on; one shared
object ref (`barrel_cruse_ref.png`, cropped from F04 approved — their first
main-scene appearance), chained into the back cover. Build text:

> the meal barrel: a waist-high rounded earthenware storage jar of fired
> ochre-umber clay — one smooth ceramic body, a wide open mouth, two small
> clay lug handles, a flat round lid — never wooden planks, never metal hoops;
> the cruse: a palm-sized round-bellied clay flask of oil, narrow-necked,
> unglazed, with a small plug stopper

**The "barrel" literalism trap (important):** KJV "barrel" = a storage JAR.
An image model's prior for "barrel" is a wooden stave-and-hoop cask — wrong by
~2,700 years. Every prompt that shows it must say "earthenware storage jar"
first and carry the compact never-wooden/never-hoops pair (Naaman's
"never raw, never a wound" register); the back cover appends "wooden staves,
metal hoops, wine cask" to its Avoid list. Captions still say "barrel" —
that's the KJV's word; only the drawing is corrected.

**ZAREPHATH'S CITY GATE** — the location of the whole dialogue (v10: "when he
came to the gate of the city, behold, the widow woman was there gathering of
sticks"). Recurs F01→F03. Build text:

> the gate of Zarephath: two squared weathered drystone posts carrying a rough
> timber lintel, set in a low sun-dried mud-brick town wall, drought-bleached,
> the lane through it leading toward low flat-roofed houses

Ref: `gate_ref.png`, cropped from F01 approved.

**THE SYNAGOGUE (cross-episode, proposed — new practice, needs user OK):**
F05 is the SAME ROOM as Naaman's F06 (same sermon, two verses apart). Propose
cropping `synagogue_ref.png` from episode 4's approved F06 still and chaining
it into F05, so the room genuinely holds across the two episodes — the first
cross-episode location ref in the series. It also pays forward to episode #14
(the full sermon episode, which the build order says ships only after these
two). If declined, F05 simply reuses Naaman F06's room prose verbatim and
accepts render variance. **[OPEN — flagged]**

### Chain order (hard dependencies)

1. **F01** renders with `refs=[]` (widow + Elijah + gate all debut here) →
   approve → crop `widow_ref`, `widow_face_ref`, `elijah_ref`,
   `elijah_face_ref`, `gate_ref`. *Risk, accepted and flagged: two new
   characters debut on one page, so F01 approval must check BOTH likenesses;
   a miss on either means a full-page regen. There is no earlier page to
   split them across — the meeting IS the first beat.*
2. **Front cover** (widow_ref), **F02** (widow refs + gate), **F03** (widow +
   Elijah refs + gate) may then run, any order.
3. **F04** (widow + Elijah refs; barrel + cruse debut) → approve → crop
   `barrel_cruse_ref`.
4. **Back cover** (barrel_cruse_ref + widow_ref) after F04.
5. **F05** needs only jesus_ref (copy immediately) + the proposed synagogue
   crop (available now from ep4) — independent of the widow chain.
6. **F06** needs widow_face_ref → after F01.

---

## 4. Covers

### The Nazareth judgment call (stated, as asked)

Naaman's front cover led with the NT scene because ITS narration opens there
("his own hometown tried to throw him off a cliff" energy from line one). THIS
narration opens on the widow gathering sticks and lands on the open barrel —
so the covers go to those two images, and the Nazareth/Jesus beat lives at
interior F05, precisely as Naaman itself placed its Jesus beat at interior
F06. Three reasons, in strength order: (1) **picture-matches-audio** — the
front cover plays under the hook line, and the hook line is the widow and her
sticks; (2) **series freshness** — Naaman's front already spent the
Nazareth image; a repeat viewer one episode later would read a second Nazareth
cover as a rerun; (3) **the twin-episode rhyme is better served inside** —
F05 is designed as the deliberate sibling of Naaman's F06 (same room, earlier
moment; §6), which rewards the repeat viewer far more than a repeated cover
would, and keeps the covers doing what covers do: selling THIS episode's own
story.

### FRONT COVER

- **Scene:** the widow, small and isolated in the lower third, bent low
  gathering dry sticks from the bare cracked ground before the gate of
  Zarephath — the drystone posts and timber lintel rising behind her in the
  low mud-brick wall — a thin bundle of sticks already in the crook of one
  arm; beyond the wall, the town's low flat rooftops stepping down toward a
  flat grey sea on the far horizon; drought-bleached scrub, dust, a bare dead
  tree. (The sea locates us on the Phoenician coast from the first frame —
  quietly setting up Jesus's own "a city of Sidon" point.)
- **Lighting (law: ≥1 warm + ≥1 cool):** a low smoldering ember-orange sun
  breaking under a heavy slate-grey famine sky, its warm light raking the
  ground and the sticks in her arm; cold blue-teal shadow holding the gate,
  the wall, and the sea. (The warm element is deliberately FIRE-colored — the
  hook line is "her own funeral fire"; the light itself carries the dread.)
- **Motif:** none — deliberate, see §2. The cover's teal shadow is cover-style
  palette, not the motif.
- **Title:** `AN HANDFUL OF MEAL` (top) — verbatim contiguous from her own
  KJV line, per the grounded-title rule. **Subtitle:** `1 KINGS 17`.
- **seq_title for all interior pages = `AN HANDFUL OF MEAL`** (matching
  front title, Naaman's own pattern). **[OPEN — minor: if the user finds it
  long for the handwritten page-top, `THE BARREL` is the short fallback.]**
- **Refs:** widow_ref (hence F01 approval precedes this render).
- **extra_avoid append:** "emaciated horror, skeletal figures, corpses".
- **Animation (strong front lock, per the cover doc):** her skirt hem, shawl,
  and head-scarf stir in a low dry wind; the dead scrub at her feet trembles
  faintly; the ember light stays exactly as warm and low as it already is,
  unchanged; no new figure, mark, or text appears. (Ambient-only living
  detail — covers render on veo, which won't execute cued gestures.)
  `clip_duration=4` (the 10-word slot is ~3.6s; no fill needed).

### BACK COVER

- **Scene:** the dim interior of the widow's small mud-brick house at dawn;
  the meal barrel — the earthenware storage jar, per the build — standing
  open in the lower third, its flat lid leaning against its side, mouth
  toward the door; a shaft of dawn light through the low open doorway falls
  across the jar's open mouth and the pale meal inside it; the little clay
  cruse standing beside the jar, stoppered; in the doorway beyond, the widow
  standing small, half-silhouetted against the light, at rest. One small
  hard-capped closed curl of blue ink with a trace of muted gold rises from
  the jar's open mouth into the light shaft, its whole visible length no
  longer than a hand's width, curled into one small closed loop, never
  straightening, never trailing, behaving like a small dab of living ink,
  never a glow.
- **Why this image:** the landing line is "God doesn't need your barrel full.
  He needs it open." The OPEN jar in the light IS the sentence. It also gives
  the title object the hero frame the interior pages never quite give it
  (F04's hero is her hand and the giving) — the episode is named for this
  image and the episode ends on it.
- **Lighting (law):** warm dawn gold pouring through the doorway and pooling
  in the jar's mouth; cold blue-grey night shadow still holding the room's
  corners and the floor's edges.
- **Title:** `HE NEEDS IT OPEN` (bottom) — the narration's own final sentence
  verbatim, per the back-cover closing-line pattern. **Subtitle:**
  `LUKE 4:26` — the twin of Naaman's back-cover `LUKE 4:27`: adjacent verses
  of the same sermon, back to back on the two episodes' back covers. That
  symmetry is deliberate; please keep it.
- **Refs:** barrel_cruse_ref + widow_ref (hence F04 approval precedes this).
- **extra_avoid append:** "wooden staves, metal hoops, wine cask".
- **Animation (light back lock, per the cover doc):** fine dust motes drift
  slowly through the dawn shaft; the widow's scarf stirs faintly in the
  doorway air; the blue curl stays exactly as drawn; the dawn light stays
  exactly as warm and low as it already is, unchanged. `clip_duration=8`
  (34-word ≈ 12s slot; fill mode in §7).

---

## 5. Page design conventions used below

- Every page: `panel_style="woodcut_hybrid"`, 9:16, include_no_bubble_clause
  True (three pages carry quoted-line captions — the exact bubble-prior case).
- Main-scene prose is written near-final (PageSpec `main_scene_still`
  register, starting mid-sentence after the shot type, dosage line included at
  the end, Naaman-style). Sonnet may tighten wording but must keep every
  MUST-SHOW, dosage, separation, and never-X clause.
- NO_MOUTH goes to whichever figure owns the beat's voiced line (widow F02,
  Elijah F03, Jesus F05) — voice-over series, no lip-sync ever.
- KJV captions are verbatim contiguous fragments, ≤4 words per line; panel
  labels 2-3 authored words.

---

## 6. Page-by-page

### F01 — "A stranger asks" (22w · FR1 · Swirl 0 · kling3_0)

The meeting at the gate, v10. Debut page for the widow, Elijah, and the gate —
renders unpinned, sources five ref crops, so its approval bar is the episode's
highest.

- **Panels**
  1. `"the dry brook"` — the cracked, stone-littered bed of a dried-up brook,
     no water anywhere *(Cherith, v7 — where Elijah has just come from; the
     famine has already taken even the prophet's own supply — supports the
     beat without duplicating the main scene)*
  2. `"two sticks"` — two dry sticks lying crossed on bare cracked earth
     *(v12's own number; plants the object F03's first trace will rise from)*
  3. `"by the sea"` — Zarephath's low flat rooftops stepping down to a flat
     grey sea *(the Phoenician coast — quietly pre-loading Jesus's "a city of
     Sidon" point four pages early)*
- **Main scene** — `MEDIUM TWO-SHOT`:
  > the dusty open ground before the gate of Zarephath — two squared weathered
  > drystone posts carrying a rough timber lintel in a low sun-dried mud-brick
  > town wall, drought-bleached, fully inside the frame. {WIDOW_BUILD}, fully
  > inside the frame, paused half-bent over the bare ground, a thin bundle of
  > dry sticks gathered in the crook of one arm, her face lifted toward the
  > stranger, guarded and hollow-eyed; the hatching of her figure drawn
  > slightly loose and overworked, though her contour stays whole and single.
  > {ELIJAH_BUILD}, fully inside the frame, standing travel-worn before her,
  > his staff in one hand, his other hand half-raised in a quiet ask, his own
  > linework steady, single-struck, confident; cracked dry earth, wisps of
  > drought-killed grass, no water drawn anywhere. Stage 0 dosage: no blue
  > Swirls of Life ink motif anywhere on this page — no blue ink appears
  > anywhere in the scene, the panels, or the margins.
- **material_closer:** "the loosened hatching in the widow's own figure is the
  only unusual ink at work on this page, and no blue appears anywhere."
- **Fence:** `fray` — "the loosened, overworked hatching of the widow's figure"
- **Caption:** `("nothing to spare",)` *(narration verbatim)* ·
  **Corner note:** `NOTE: a stranger asks`
- **Panel motions:** (1) a faint heat-shimmer plays over the dry brook stones;
  (2) the two sticks sit undisturbed, casting fixed shadows; (3) a thin haze
  drifts over the far rooftops and sea.
- **Main animation:** the widow's head completes its lift and her eyes settle
  on Elijah, finishing early and holding still; Elijah stays exactly as drawn,
  one slow breath, his half-raised hand not moving further, his lips staying
  closed and completely still; the dry grass wisps at their feet stir faintly.
- **Why kling:** her look-up is a designed completing gesture (Kling's proven
  lane); it also gives the debut page one legible human event. `refs=[]`.

### F02 — "We may eat it, and die" (27w · **FR3 peak** · Swirl 0 · kling3_0, clip 9s)

Her voiced line — the episode's fear summit and the Fray's whole reason for
being. The starkest page in the episode: no blue, no warmth, the frame close.

- **Panels** *(her spoken inventory, made visible — the mind's eye going home
  before her feet do)*
  1. `"the last handful"` — looking straight down into the open mouth of an
     earthenware meal jar, a thin handful's worth of pale meal dusting its
     bottom *(interior view only — deliberately framed so the jar's exterior
     form debuts at F04, where its ref is cropped)*
  2. `"a little oil"` — a palm-sized clay cruse lying tilted, near empty, one
     soft gleam of oil at its lip
  3. `"two empty bowls"` — a bare low table with two empty clay bowls set out
     *("for me and my son" without drawing the boy — the pair of bowls will be
     answered by F06's three full ones)*
- **Main scene** — `CLOSE-UP`:
  > tight on the widow before the gate's shadowed stones. {WIDOW_BUILD}, her
  > head and shoulders filling the frame, the bundle of dry sticks clutched
  > against her chest with both arms, fully inside the frame; her eyes down,
  > her face emptied of hope, resigned; her figure's linework destabilized to
  > its furthest point — her contour visibly broken and doubled, a faint
  > tremored second line running beside the true line of her shoulder, cheek,
  > and arms, the hatching scratchy, overworked, almost flying — while every
  > stone and stick around her is drawn steady and single-struck. Stage 0
  > dosage: no blue Swirls of Life ink motif anywhere on this page — no blue
  > ink appears anywhere in the scene, the panels, or the margins.
- **material_closer:** "the broken, tremored linework of the widow's own
  figure is the only unusual ink at work on this page, and no blue appears
  anywhere."
- **Fence:** `fray` — "the broken, doubled, tremored linework of the widow's
  figure and its scratchy flying hatching"
- **Caption:** `("we may eat it,", "and die")` *(KJV v12, verbatim
  contiguous, split ≤4 words/line)* · **Corner note:** `NOTE: the funeral fire`
- **Panel motions:** (1) the light inside the jar's mouth deepens very
  slightly, nothing else changes; (2) the gleam of oil at the cruse's lip
  catches the light softly and settles; (3) the two empty bowls sit
  undisturbed on the bare table.
- **Main animation:** the widow takes one slow shallow breath; her eyes lower
  the last small distance and settle, finishing early and holding still; her
  grip on the stick bundle tightens once and stills; her lips stay closed and
  completely still — she is not speaking and her mouth does not move at all.
- **Why the smallest ask on the biggest page:** FR3 is untested and a
  close-up has little honest motion headroom (fragility budget, LAW 0.6);
  the eye-settle + breath is the Hem-validated register, and Kling owns
  completing micro-gestures. Panel 1 and 2 get tone-only motion — a vessel
  with liquid is the loaded invention prior (the v4 pot lesson).
- **Refs:** widow_ref + widow_face_ref + gate_ref.

### F03 — "Fear not" (33w · FR3→**FR1** hard cut · **Swirl 1 first trace** · kling3_0, clip 9s)

The gospel turn's first half: the word lands before any proof does. The page
turn from F02 to this page IS the Fray clearing — the widow's linework arrives
already steadied, and the first blue of the episode arrives with it.

- **Panels**
  1. `"steady eyes"` — a close study of Elijah's weathered face, his eyes
     level and unafraid *(needs elijah_face_ref)*
  2. `"a cake first"` — one small round flat cake resting on an open upturned
     palm *(the scandalous ask made visible)*
  3. `"go and do"` — the narrow lane from the gate running toward low
     flat-roofed houses *(her obedience path; label is KJV v13 verbatim)*
- **Main scene** — `MEDIUM TWO-SHOT`:
  > before the gate of Zarephath, fully inside the frame. {ELIJAH_BUILD},
  > fully inside the frame, facing the widow, his staff grounded, his free
  > hand lifted gently palm-out toward her, already extended, his linework
  > steady, single-struck, confident. {WIDOW_BUILD}, fully inside the frame,
  > facing him, her arms loosened at her sides, her chin just beginning to
  > lift, her contour whole and single again though her hatching stays loose
  > and worked; the small bundle of dry sticks now lying on the bare ground
  > between the two figures, fully inside the frame, with clean open ground
  > around it; cracked dry earth, no water drawn anywhere. Stage 1 dosage:
  > exactly one restrained thread of blue ink rising thin from the two dry
  > sticks lying on the ground between them, touching only the sticks and the
  > air just above them, the only blue on the whole page, behaving like one
  > stroke of wet ink bled into the paper, a clean band of untouched paper
  > between the thread and both figures.
- **material_closer:** "the widow's loosened hatching and the single blue
  thread above the sticks are the only two kinds of unusual ink at work on
  this page, kept apart by clean paper."
- **Fence:** `fray` — "the loosened hatching of the widow's figure and the
  single blue thread above the sticks"
- **Caption:** `("Fear not",)` *(KJV v13 verbatim — two words, the motif's own
  name; the episode's whole hinge deserves the page's shortest caption)* ·
  **Corner note:** `NOTE: before the miracle` *(the word precedes the
  provision — the page's theology in three words)*
- **Panel motions:** (1) Elijah's sketched face holds, the light across it
  warming very slightly; (2) the small cake sits undisturbed on the open
  palm; (3) a thin banner of dust drifts low along the empty lane.
- **Main animation:** the widow's chin completes its lift and her shoulders
  drop and settle, finishing early and holding still; Elijah stays exactly as
  drawn, his lifted palm not moving further, one slow steady breath, his lips
  staying closed and completely still — he is not speaking and his mouth does
  not move at all; the single thin blue ink thread stays exactly as drawn, in
  place, for the whole clip.
- **Why:** the shoulder-release is the Hem-F05-validated "fear visibly leaves
  her" register — the one human thing this exact moment is. Stage 1 thread
  motion is the worst risk/reward on the page (north-star table: hold it).
  The sticks moved from her arms (F02) to the ground — a between-pages state
  change, which is exactly where state changes belong.
- **Refs:** widow_ref + widow_face_ref + elijah_ref + elijah_face_ref +
  gate_ref.

### F04 — "The barrel of meal wasted not" (26w · **FR0** · **Swirl 2** · kling3_0, clip 9s)

Giving and miracle in one scene, compressed exactly as the narration
compresses them. Interior debut of her house and of the barrel + cruse
(ref-crop page for `barrel_cruse_ref`). The completing gesture IS the miracle
on camera: a fresh handful of meal lifting from a jar that should be empty.

- **Panels**
  1. `"a stranger fed"` — Elijah's weathered hands breaking a small flat cake
     over a plain bowl *(hands only — "she fed a stranger before she fed her
     own child")*
  2. `"the cruse"` — the small clay cruse standing upright, stopper set
     beside it, one soft gleam of oil at its lip
  3. `"wasted not"` — looking straight down into the jar's open mouth, a thin
     handful's worth of pale meal dusting its bottom — the same view as
     F02's panel 1, unchanged *(the deliberate panel rhyme: the identical
     interior on both pages, meaning inverted — the level never drops. Label
     is KJV v16 verbatim)*
- **Main scene** — `MEDIUM shot`:
  > the single dim room of the widow's small mud-brick house, morning light
  > through the low doorway. In the foreground, the meal barrel — a waist-high
  > rounded earthenware storage jar of fired ochre-umber clay, one smooth
  > ceramic body with a wide open mouth and two small clay lug handles, its
  > flat round lid set aside, never wooden planks, never metal hoops — fully
  > inside the frame, the small stoppered clay cruse standing beside it.
  > {WIDOW_BUILD}, fully inside the frame, kneeling at the jar, her hand just
  > drawn back from its mouth a hand's-width clear of the rim, a fresh
  > handful of pale dry meal — warm ochre-cream, never blue — lifted in her
  > open fingers, her face turning toward it in the first break of wonder;
  > her contour drawn steady, confident, and single-struck, no doubled or
  > tremored line anywhere in her figure. Behind her at a low table,
  > {ELIJAH_BUILD}, seated, a small flat cake before him, and beside him the
  > widow's son, a thin boy of seven or eight, large dark eyes in a small
  > famine-thinned face, a plain patched undyed tunic, watching the jar
  > wide-eyed, both fully inside the frame. No liquid drawn pouring anywhere
  > on the page. Stage 2 dosage: the blue ink motif is quietly present — a
  > few soft blue threads and one small watercolor bloom rising from the open
  > mouth of the meal jar, touching only the jar's rim and the air above it,
  > touching no person and nothing else on the page, behaving like wet ink
  > bled into the paper.
- **material_closer:** "the soft blue threads at the jar's mouth are the only
  unusual ink at work on this page; every figure's linework is steady and
  single-struck."
- **Fence:** `none` *(FR0 — the Fray is gone; the standard page-global
  stillness fence still guards the paper's own aging)*
- **Caption:** `("the barrel of meal", "wasted not")` *(KJV v16 verbatim
  contiguous, 4+2)* · **Corner note:** `NOTE: she gave first` *(the episode's
  conviction in four words)*
- **Panel motions:** (1) Elijah's hands complete the breaking of the cake and
  hold; (2) the gleam at the cruse's lip warms softly and settles; (3) the
  light inside the jar's mouth deepens very slightly, nothing else changes.
- **Main animation:** the widow's hand completes its small lift and a few
  grains of pale meal sift down from her fingers and fall, then her hand
  holds still; her face stays turned toward her open hand; Elijah and the boy
  stay exactly as drawn, each one slow breath; the soft blue threads near the
  jar's mouth drift gently within their own small area; the cruse sits still
  beside the jar.
- **Why:** the meal-sift is a real completing gesture (Kling lane) and the
  only motion the miracle needs; the meal is named ochre-cream and the hand
  is a stated distance clear of the rim so pale dust and blue thread can
  never read as one substance (LAW 3 applied to a non-water liquid page —
  the cruse additionally stays stoppered and gets a stillness clause plus a
  tone-only panel, since vessel+liquid is the loaded invention prior).
- **Refs:** widow_ref + widow_face_ref + elijah_ref + elijah_face_ref.

### F05 — "Sarepta, a city of Sidon" (38w · no Fray · **Swirl 2, held at cap** · veo3_1_lite, clip 8s)

Jesus's own citation, Luke 4:25-26 — the fulfilment-on-page beat, and the
deliberate sibling of Naaman's F06. Same plain stone synagogue, same
reading-desk-and-scroll swirl anchor — but an EARLIER minute of the same
sermon: Luke seats him ("he sat down… and began to say", 4:20-21), and the
wrath doesn't rise until v28. So where Naaman's page showed the crowd RISEN as
one surging mass, this page shows them still seated and hardening — the
before-frame of a two-frame story told across two episodes. A repeat viewer
gets "we are back in that room, one breath earlier"; a new viewer gets a
complete page. That's the answer to the repetition worry: not avoided, rhymed
with progression.

- **Panels**
  1. `"her city"` — Zarephath's low rooftops by the flat grey sea, small
     *(rhymes F01's panel 3 — the same town, now in Jesus's mouth)*
  2. `"many widows"` — several distant veiled figures standing apart across
     open ground, dignified *(the deliberate twin of Naaman F06's "many
     lepers" panel — sibling panels for sibling verses)*
  3. `"the syrian"` — a far small figure standing waist-deep in a river
     gorge *(Naaman himself, one verse ahead — the previous episode inside
     this one, exactly as both live inside one sermon. See OPEN questions;
     safe fallback: `"his hometown"` — Nazareth's stacked rooftops)*
- **Main scene** — `MEDIUM WIDE shot`:
  > the plain stone synagogue interior. {JESUS_BUILD}, fully inside the
  > frame, seated on the low stone bench at the front, his hands at rest, his
  > gaze steady and level; beside him the simple wooden reading desk with the
  > closed scroll lying on it, fully inside the frame. Around him on low
  > benches, the men of Nazareth still seated, drawn as one dense-hatched
  > mass — townsmen in plain undyed and ochre wool, faces turned toward
  > Jesus, hardening, brows drawn down, a few heads inclined toward one
  > another, no single face individuated or finished anywhere in the mass,
  > their gathering anger carried entirely in posture and stillness, not one
  > man risen, fully inside the frame. Stage 2 dosage, held at this episode's
  > own cap: the blue ink motif quietly present — a few soft blue threads
  > with the faintest trace of muted gold, and one small watercolor bloom,
  > rising from the closed scroll on the reading desk beside him, touching
  > only the scroll and the air above the desk, touching no person on the
  > page.
- **material_closer:** "the blue-and-gold threads on the scroll are the only
  living ink on the page." *(Naaman F06 verbatim — deliberate.)*
- **Fence:** `none`
- **Caption:** `("save unto Sarepta,", "a city of Sidon")` *(KJV Luke 4:26
  verbatim contiguous, 3+4)* · **Corner note:** `NOTE: named centuries later`
- **Panel motions:** (1) a thin haze drifts over the sea beyond the
  rooftops; (2) the far veiled figures stand undisturbed, dignified; (3) the
  river's surface glimmers faintly around the far figure, who holds still.
- **Main animation:** the seated crowd mass stiffens almost imperceptibly as
  one body, a few heads inclining a finger's width further toward one another
  and holding, no man rising at any point; every man keeps his lips exactly
  as drawn, not speaking; Jesus stays exactly as drawn, one slow steady
  breath, his lips staying closed and completely still — he is not speaking
  and his mouth does not move at all; the threads and bloom on the scroll
  drift gently within their own small area, never spreading beyond the
  scroll and the air above it; no new figure, bubble, or mark appears
  anywhere on the page at any point.
- **Why veo:** all holds and drift, no completing gesture — and Naaman F06
  validated exactly this crowd-tension page on veo at clip 8. The
  crowd-must-not-rise clause is load-bearing: rising is the NEXT frame, and
  it belongs to episode 4.
- **Refs:** jesus_ref (+ proposed synagogue_ref crop from ep4 F06).

### F06 — "The one with nothing left" (22w · FR0 · Swirl 2 held · veo3_1_lite, clip 8s)

The reflection beat, made literal: many dark houses, one lit one — and the lit
one is across the border. Doctrine check built into the composition: Jesus's
point is that God went OUTSIDE Israel ("unto none of them… save unto
Sarepta"), so the one lit house stands apart from the hills, at the coast,
by the sea — not among them.

- **Panels**
  1. `"no rain"` — cracked bare earth under an empty rainless sky *(1 Kings
     17:1 — the famine's cause, the shut heavens)*
  2. `"three full bowls"` — the same low table, three plain clay bowls set
     out, filled *(answers F02's "two empty bowls" — two-who-would-die became
     three-who-eat; "she, and he, and her house, did eat many days", v15)*
  3. `"her face, after"` — a close study of the widow's face at rest, her
     linework steady and single, no tremor anywhere *(closes the Fray arc
     explicitly; needs widow_face_ref)*
- **Main scene** — `WIDE shot`:
  > dusk over a wide drought-stricken land: dark hills rolling away under a
  > deepening sky, small flat-roofed houses scattered across them, every one
  > of them dark and unlit; far beyond the hills at the coastline, small with
  > distance and set apart across open ground, one single low house by the
  > flat grey evening sea with a warm lit doorway, a thin line of pale
  > hearth-smoke rising from its roof, fully inside the frame; the ground
  > everywhere dry, no water drawn anywhere but the far sea. Her contour and
  > the whole scene drawn steady, confident, and single-struck. Stage 2
  > dosage, held: a few soft blue threads with traces of muted gold and one
  > small watercolor bloom hanging high in the evening air directly above the
  > one lit house, small with distance, touching nothing below the sky.
- **material_closer:** "the blue-and-gold threads above the one lit house are
  the only unusual ink at work on this page."
- **Fence:** `none`
- **Caption:** `("nothing left to give",)` *(narration verbatim)* ·
  **Corner note:** `NOTE: asked her anyway`
- **Panel motions:** (1) a low banner of dust drifts across the cracked
  earth; (2) a faint curl of steam rises from the bowls and thins; (3) the
  sketched face holds, the light across it warming very slightly *(tone-only
  — small sketched faces morph under content-motion asks)*.
- **Main animation:** the thin line of hearth-smoke rises steadily from the
  one lit roof and drifts, staying its own thin line; the far grey sea
  glimmers faintly along the coast; the warm doorway light stays exactly as
  warm and steady as it already is, unchanged; the blue-and-gold threads
  above the house drift gently within their own small area; every dark house
  on the hills stays exactly as drawn, none of them ever lighting.
- **Why the smoke:** it is the page's one real motion AND the hook inverted —
  the fire she gathered sticks to die by is now a cooking fire that feeds
  three. veo positive-only light language throughout (no "glint"/"sparkle").
- **Refs:** widow_face_ref (panel 3 only).

---

## 7. Assembly suggestions (word-proportional, Fable estimates)

Modes follow the Naaman lesson: boomerang ONLY for genuinely non-directional
ambience; anything with directional motion (smoke rising, a gesture, drift)
gets freeze (+tail_loop where a completing gesture settles near the clip's
end). Final modes are an assembly-QC call on the real renders — real
playback, per the standing rule.

| Unit | Words | Clip | Suggested mode |
|---|---|---|---|
| front | 10 | 4s | freeze (slot shorter than clip — likely trims) |
| f01 | 22 | 5s | freeze + tail_loop ~1.0 (look-up settles) |
| f02 | 27 | 9s | freeze + tail_loop ~1.0 (eye-settle) |
| f03 | 33 | 9s | freeze + tail_loop ~1.5 (shoulder-release settles) |
| f04 | 26 | 9s | freeze (meal-sift is directional — no boomerang) |
| f05 | 38 | 8s | freeze (Naaman F06 precedent — its lean reversed badly under boomerang) |
| f06 | 22 | 8s | freeze (rising smoke would visibly sink under boomerang) |
| back | 34 | 8s | freeze (drifting motes read directional on reversal risk — be safe) |

Sum 212 ≈ the narration's own length; ~76s of narration + landing hold ≥3.0s
(INV-26) — in family with the series' shipped runtimes.

---

## 8. OPEN QUESTIONS (do not silently resolve)

1. **FR3 on F02 is a series first** (Thomas only validated FR2). Attempt as
   designed; if the broken/doubled contour reads as a render defect or a
   ghost-double at QC, fall back to a strong FR2 and note it. Pareidolia
   eye-check on the tremored lines.
2. **Cross-episode synagogue ref** — cropping `synagogue_ref.png` from
   episode 4's approved F06 still into F05 is a NEW practice (first
   cross-episode location ref). I recommend it (same room, same sermon, pays
   forward to episode #14); needs the user's OK.
3. **F05 panel 3 "the syrian"** — the Naaman-in-the-Jordan callback panel is
   a deliberate twin-episode easter egg (the sermon names him one verse
   later). Delightful to a series viewer, opaque-but-harmless to a new one.
   Fallback ready: `"his hometown"` (Nazareth rooftops). User's call.
4. **Swirl cap on the Jesus page** — I hold Stage 2 (series-plan row + Naaman
   precedent) rather than the Stage-3-for-fulfilment reading. One line to
   change on F05 if the user prefers Stage 3.
5. **Title length** — seq/front title `AN HANDFUL OF MEAL` (4 words,
   KJV-verbatim). If it proves long for the handwritten page-top at render,
   `THE BARREL` is the short fallback; the front cover keeps the full phrase
   either way.
6. **Barrel/cruse tiny-panel appearances before their ref exists** (F02
   panels 1-2 precede the F04 ref crop). Mitigated by framing F02's jar panel
   as interior-view-only so the exterior form debuts at F04; the residual
   panel-scale variance is accepted and flagged, same family as Naaman's F01
   helmet panel. If the user wants zero variance, the alternative is a
   standalone object-ref render before F02 — new practice, not recommended.
7. **F01 dual debut** — widow AND Elijah both crop from F01's single
   approval; a likeness miss on either means a full-page regen. Unavoidable
   (the meeting is the first beat); budget one extra regen cycle here.
8. **F02/F04 barrel-interior panel rhyme** — the "same view, unchanged" idea
   can't be pixel-guaranteed across two renders; the shared framing +
   labels ("the last handful" → "wasted not") carry it. Accept approximate.
