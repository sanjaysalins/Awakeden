# DESIGN BRIEF — Episode 7, "The Bier He Touched"

Luke 7:11-17 (the widow of Nain) · OT rhyme-partner: Numbers 19 (episode 2, "The Ashes
That Made Clean" — the season's second old-to-new rhyme, per the v4 series plan) ·
Dead ink: **Stain (ceremonial uncleanness) only — NO Fray anywhere** (the retag is
binding: the text has zero fear/doubt vocabulary; her arc is grief met with compassion,
and grief is not Fray) · NT episode — the OT Stage 1-2 swirl cap does NOT apply;
Stage 3 is reached (once, earned — see §2) · panel_style **woodcut_hybrid** throughout ·
Voices: narrator + jesus ONLY (voices.json) — Jesus's two lines ("Weep not." /
"Young man, I say unto thee, Arise.") are the episode's only non-narrator audio.

Fable design pass, 2026-08-31. This brief is the single creative source for the
Sonnet implementation pass (episode.py PageSpec/CoverSpec objects). Narration and
audio are LOCKED (69.0s final) — nothing here changes a spoken word. Every choice
states its WHY. Open questions are flagged inline and collected in §8 — do not
silently resolve them.

---

## 0. The shape of the episode, in one paragraph

The narration opens on the funeral procession and closes on "he touched a funeral,
and it became a homecoming" — so the covers belong to the BIER, the episode's own
title object: front = the procession carrying it OUT through the gate of Nain
(the hook's literal image), back = the same bier EMPTY at dawn, leaning against
the gate wall with the graveclothes folded on its boards (the funeral canceled —
the object-landing pattern of Naaman's abandoned armor and the Barrel's open jar).
Six interior pages + two covers, one unit per narration paragraph — the eight
paragraphs divide themselves (shown in §1). The hard first-of-its-kind problem —
where the Stain lives when the uncleanness is a CORPSE, not a diagnosed living
person — is solved by attaching the Stain to the bier-and-its-burden as one
object, never to any living figure, and telling the narration's reversal
("Death didn't spread from the boy to Jesus. Life spread from Jesus to the boy")
through the stain's own GEOMETRY: from the moment of contact (F03) the stain
dries from the edge nearest Jesus's hand outward — it dies of the touch instead
of spreading by it — until only the dried pale ring remains under the boy who
sits up inside the cleanest cream paper on the page (F05). The swirl rises
against it (0 → 1 → 1 → 2 → 2 → 3), anchored to the hand that does the touching,
crossing the falling Stain exactly at "Arise" (F04) — the crossing point IS the
gospel turn, per the system's own law. Because this is an NT episode with the
fulfilment bodily on-page, the swirl is allowed past the OT cap: it reaches
Stage 3 exactly once, on F06, the homecoming-through-the-gate page (full
reasoning in §2).

---

## 1. Narration beat map → units (why six interior pages)

The locked narration divides into 8 natural picture-beats — one per paragraph,
no forcing needed. Word counts are my own count of the locked text (sum 186;
the synthesized audio is 69.0s, ≈2.70 words/sec). The assembler treats the
weights as proportions, same as Naaman and the Barrel.

| Unit | Narration beat | Words | Voice(s) |
|---|---|---|---|
| **front** | "A widow was walking behind her only son's body, carried out on a bier to be buried. He was all she had left." | 23 | narrator |
| **F01** | "The law was simple: touch a dead man, and you were unclean. Everyone kept their distance. That was survival, not cruelty." | 21 | narrator |
| **F02** | "Jesus walked toward her instead of away. And when the Lord saw her, he had compassion on her, and said unto her, 'Weep not.'" | 24 | narrator + **jesus** |
| **F03** | "Then he touched what no one else would touch: and he came and touched the bier, and they that bare him stood still." | 23 | narrator |
| **F04** | "Under that same law, the touch should have made him unclean. It didn't work that way with him. And he said, 'Young man, I say unto thee, Arise.'" | 28 | narrator + **jesus** |
| **F05** | "And he that was dead sat up, and began to speak. And he delivered him to his mother." | 18 | narrator |
| **F06** | "Death didn't spread from the boy to Jesus. Life spread from Jesus to the boy." | 15 | narrator |
| **back** | "That is still the only direction he touches anything dead in you. Not to catch what's wrong with you — to give you what's his instead. He touched a funeral, and it became a homecoming." | 34 | narrator |

**Why not 5 interiors:** the only candidate merge is F05+F06 (18w + 15w). It
would bolt the raising (a crowded, figure-heavy scene) onto the thesis line
(a direction statement) — two different pictures, and F06 is the episode's one
Stage 3 page, which must not share a frame with the D1 ring (the raising page
still carries it). **Why not 7:** no beat splits without dropping below ~10
words (a ~3.5s slot, below a clip's natural length — the Barrel's own churn
threshold). F06's 15 words (~5.6s) is the shortest unit and it comfortably fits
a 5s clip. The paragraph structure IS the page structure; leave it alone.

---

## 2. The Stain decision (the hard problem), then the motif arcs

### Where the Stain lives — reasoned, not defaulted

Candidates weighed:

- **(a) On the widow** — REJECTED. Her arc is grief, and grief is neither
  Stain sub-case (moral guilt / ceremonial barrier *diagnosed on her*).
  Yes, as chief mourner she would technically contract corpse-uncleanness
  under Numbers 19:11 — but the narration never goes there, staining her
  would read as a judgment on the grieving mother, and it would add a second
  clearing arc the narration resolves in no sentence. Same *kind* of error
  as v3's Fray tag, one motif over. Her linework stays steady and
  single-struck on every page (see the standing override in §5 — a weeping
  figure is exactly what a model will spontaneously loosen into fray-like
  hatching, so every page states the override explicitly).
- **(b) On the boy as a separate subject** — REJECTED as stated, ABSORBED in
  practice. Until F05 the boy has no independent visual existence: he is a
  shrouded form ON the bier, face bound in the napkin (John 11:44's own
  grave-dress). Visually the bier-and-burden are one object from F01 to F04.
- **(c) On the bier-and-its-burden as ONE object** — CHOSEN. The Stain is
  corpse-defilement-as-barrier (the series' own second sub-case, "never
  framed as guilt"), and Numbers 19 attaches it to contact with the dead —
  so the motif soaks the paper beneath the one dead thing on the page. The
  crowd's kept distance (F01) becomes the stain's reach made legible: the
  villagers stand just beyond where the paper is damaged. This is the first
  object-attached Stain in the series, and it is exactly what the text
  gives.
- **(d) "Clears the instant he touches it," on-page** — REJECTED as an
  event, KEPT as geometry. State changes happen BETWEEN pages, never within
  a clip (locked law), and an instant-vanish would say his touch is a
  detergent. The narration says something stronger: contact happened and the
  FLOW REVERSED. So the design is: **the Stain never touches Jesus at any
  dose on any page** (his figure, hand, sleeve, and the paper beneath him
  stay the cleanest paper in the frame, stated every time), and from F03
  onward the stain's drying begins at the exact edge nearest his touching
  hand and proceeds outward, page by page — static geometry telling the
  direction (the system's own D2-"turning" grammar, aimed for the first time
  at a corpse instead of a penitent). The stain does not transfer to him and
  does not merely vanish: it dies of the touch, from the touch-point out.

Two-layer mapping (Naaman's own pattern, kept deliberate): the LITERAL layer
is the shrouded corpse itself — the fact the text names — which changes state
once, between F04 and F05 (dead → risen; never on camera, the cut is the
miracle, the series' tagline at its most literal). The PAPER layer is the
Stain proper, with its own descending dose track below. Numbers 19's remedy
(the water of separation) appears in the PANELS, not the stain — the old
provision standing ready and unused (F01/F04 panel rhyme, §6).

### Stain (corpse-defilement) — descending

| Page | Dose | Rendering |
|---|---|---|
| F01 | **D3 peak** | Saturated cold grey-umber in the paper beneath the bier and the bare ground around it, bounded ≤⅓ page, never over any face, crossing the drawn frame border into the lower margin below the bier; its edge stops a stated band of clean paper short of every living figure — the crowd's gap and the stain's reach coincide |
| F02 | **D3 held** | Unchanged — nothing has acted on it yet (a dose change with no story cause would break the surface grammar the plan's #11 note guards) |
| F03 | **D2-turning** | One defined stain, still crossing the border on the corpse's side — but its whole edge nearest Jesus's touching hand already dried to a pale ring; the wet remainder lies only away from him |
| F04 | **D2-turning, late** | The greater part of its former extent dried to the pale ring; one narrow wet remainder in the paper directly beneath the bier's head end; the border-crossing itself now dried pale. (Counted conservatively as D2 for high-tide — see the flag in §8) |
| F05 | **D1** | Only the dried pale ring remains, lying where the wet stain used to sit beneath the bier; the paper INSIDE the ring is the cleanest cream on the page — the boy sits up inside "made new," not "back to normal" |
| F06 | **D0** | Canonical absence, stated: no stain, ring, or grey blot anywhere in the paper |

- **The clearing is the cut, never a clip.** D3→D2t lands on the page turn
  into F03 (the touch); D2t→D1 on the turn into F05 (the raising); D1→D0 on
  the turn into F06. Every stain page's animation carries the page-global
  fence (Hem-validated wording) plus "never deepening, never spreading,
  never fading."
- **The stain never lies under any living figure, ever** — stated on every
  page. On F03/F04 the substrate law does the elegant work: Jesus's drawn
  hand rests ON the bier while the stain lies IN the paper beneath it —
  different diegetic layers, so even at the moment of contact the motifs
  never touch. His hand, in plain ink, is the fulcrum between them.
- **Pareidolia eye-check** on every blot render, standing rule.

### Swirl (living blue-gold ink) — rising

| Page | Stage | Anchor |
|---|---|---|
| front | none | Covers never carry the paper-Stain OR the interior dose — the stain's signature move (crossing the drawn border into the margin) is impossible on a borderless edge-to-edge cover, and no prior episode's cover carried interior motifs. Dread is carried by the lighting law instead |
| F01 | **0** | Canonical absence statement — the law's world, no life in it yet |
| F02 | **1** | Exactly one restrained thread curling from the back of Jesus's half-lifted right hand, touching only his hand and the air just above it — planting the hand F03 pays off |
| F03 | **1 held** | The same single thread, now rising from the back of that hand where it rests on the bier rail, straight up, touching only the hand and the air. The touch page keeps the HUMBLEST swirl — the story is carried by the stain's dried edge, and "they that bare him stood still" is an awe-quiet beat, not a fireworks beat |
| F04 | **2** | A few soft blue threads and one small watercolor bloom rising from the back of his hand on the rail into the air above it — the dose answers the command being given |
| F05 | **2 held** | Same anchor, same dose — the raising page stays calm on the swirl side; the D1 ring and the risen boy carry it |
| F06 | **3** | Diffused: blue-and-gold threads woven in one loose open band through the air of the road and the gate, above every head, touching no person, tied to no single figure — the homecoming crowd page, the exact community image Stage 3 was designed for |
| back | curl | One small hard-capped closed curl of blue-gold rising from the folded napkin on the empty bier's boards (Naaman-cover language family: "no longer than a hand's width… never straightening, never trailing") |

- **Why the swirl anchors to Jesus's own hand (F02–F05):** the series has
  precedent hesitancy about anchoring to his figure (the Doubting-Thomas
  placement the user flagged; #11's "his word, not his figure" note). But
  those cases were INDIRECT — meaning that needed prose to explain. Here the
  narration's thesis names his person as the source in so many words: "Life
  spread FROM JESUS to the boy," and the title act is a touch. The hand that
  touches is the least indirect anchor this series will ever get; it reads
  in pixels with no narration to lean on, and it gives F02→F03→F04 one
  continuous anchor through the whole turn. Flagged in §8 for confirmation,
  not silently assumed.
- **Why Stage 3 IS reached, and why on F06 rather than F05** (the open item
  the task says to reason explicitly, not default): (1) this is an NT
  episode with fulfilment bodily on-page — Jesus raising the dead is the
  precise thing Numbers 19 could only quarantine against — so the OT cap's
  own carve-out applies; capping at 2 out of OT habit would mute the
  season's second old-to-new rhyme exactly where it lands. (2) F06's own
  narration line is the thesis — "Life spread from Jesus to the boy" — the
  one sentence in the episode that SAYS diffusion; Stage 3 lands with the
  words that earn it. (3) Not on F05, deliberately: F05 still carries the
  D1 ring (Stage 3 there would put the page at the high-tide cap on the
  episode's most render-fragile scene — a just-raised corpse, a crowd, a
  mid-reach mother), and its narration is still fact-reporting ("sat up…
  delivered"), not yet the direction statement. Holding F05 at Stage 2 keeps
  the miracle page quiet and spends the episode's one Stage 3 where the
  composition (crowd streaming home through the gate) can actually carry
  "woven through the whole scene."

### High-tide check, every page (`stainDose + swirlStage <= 4`)

| Page | Stain | Swirl | Sum | Note |
|---|---|---|---|---|
| F01 | 3 | 0 | 3 | ✓ |
| F02 | 3 | 1 | **4** | AT CAP — one big + one small, the safest at-cap shape (ep12's own 2+2 precedent for deliberate cap pages); full QUAD lock stated |
| F03 | 2 | 1 | 3 | ✓ — the touch page deliberately relieved |
| F04 | 2 | 2 | **4** | AT CAP — QUAD lock stated; conservative count (see §8) |
| F05 | 1 | 2 | 3 | ✓ |
| F06 | 0 | 3 | 3 | ✓ |

**Crossing point (swirl ≥ stain) = the gospel turn:** first equality lands on
F04 — "Under that same law… It didn't work that way with him… Arise" — the
episode's doctrinal pivot sentence; strictly greater from F05. The two at-cap
pages each get the QUAD lock in full (chromatic reservation / zone separation
with a stated clean-paper band / form separation stated both ways / substrate
separation), and both are flagged as the episode's two highest-risk renders.

---

## 3. Refs — who and what needs pinning

All new refs live in this episode folder's `refs/`
(`F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_07_the_bier_he_touched\refs\`).
Chain order is hard (render_still stops on a missing ref).

### Characters

**JESUS** — SERIES CONSTANT. `refs/jesus_ref.png` copied verbatim from episode
4's own `refs/jesus_ref.png` (itself from ep1/ep8's approved crop). JESUS_BUILD
reused verbatim from Naaman's episode.py:

> Jesus, a Judean man in his early thirties, medium height and ordinary build,
> sun-browned skin, shoulder-length dark brown hair pushed back from his face,
> a short full dark beard, wearing a simple ankle-length robe of undyed
> cream-brown wool with a plain olive-toned mantle draped over one shoulder, a
> narrow rope belt, and flat worn leather sandals -- no halo, no glow, nothing
> in his dress distinguishing him from the men around him, standing square,
> still, and unhurried, his gaze steady and direct

No redesign, no approval cycle.

**THE WIDOW OF NAIN** — new to the series. Build text (use verbatim):

> the widow of Nain, a Galilean village woman in her late forties, worn thin
> by loss, a lined olive-skinned face with deep-set dark eyes red-rimmed from
> weeping, strands of grey in the dark hair bound back beneath a plain
> mourning veil of coarse dark charcoal-grey wool drawn low over her brow,
> wearing an ankle-length tunic of faded umber-brown beneath a loose mourning
> mantle of the same dark grey wool, its edge visibly rent in one torn place
> at the breast, bare dusty feet

Why: her son is a "young man" (νεανίσκος — grown), so she is a generation
older than the Barrel's Zarephath widow (30s, grey-brown scarf with clay-red
band) — deliberately distinct in age, silhouette, and palette. The RENT
MANTLE (keriah, the torn mourning garment — Job 1:20's own gesture) is her
likeness pin AND a period-true grief mark that carries her state without any
motif: **she gets NO Stain and NO Fray — grief is carried entirely by
content** (veil, tear-lines, posture, the torn edge). No blue anywhere in
her dress (chromatic reservation). No red family either — the dark-grey
mourning dress keeps her visually apart from the stain's grey-umber (form
and placement separate them: her grey is woven cloth in the scene; the
stain is formless damage in the paper).
Refs: `widow_ref.png` (full figure) + `widow_face_ref.png` (she gets a
tear-lined face study on F02 and close framing through the middle pages;
full-figure crops are too small to pin a face). Both cropped from F01
approved — which is why F01's camera is a MEDIUM shot with her prominent
(stated in §6), not a wide.

**THE SON** — new, TWO STATES like Naaman's skin, and the state change is the
episode. State A, F01–F04 (no ref needed — no face exists to pin):

> the dead son: a still human form lying full-length on the open bier,
> wrapped from chest to feet in plain linen grave-bands, a folded linen
> napkin bound over the face so that no feature of the face is visible, the
> wrapped form slight and young in build

Period basis: John 11:44 — bound in graveclothes, "his face was bound about
with a napkin." Keeping the face covered until F05 is period-true, reverent
(no dead face ever rendered), AND it makes the ref problem solvable: the boy
has no likeness until he is alive. State B, F05 onward (build text, use
verbatim):

> the widow's son, a young man of about eighteen, lean and slight, an
> olive-skinned unlined face with large dark eyes and tousled black hair,
> bare-shouldered above the loosened linen grave-bands still wrapped about
> his waist and legs, the unbound napkin fallen in his lap

Ref: `son_ref.png` (face + shoulders), cropped from F05 approved, chained
into F06.

**THE BEARERS + CROWDS** — deliberately ref-free. The four bearers carry the
bier on F01–F05 but are designed semi-generic on purpose: plain undyed and
ochre wool tunics, heads bowed or faces turned toward the bier/Jesus,
never individuated or finished — the dense-hatched-mass treatment Naaman F06
validated, applied at four-figure scale. Two crowds exist in the text (Luke
7:11-12: Jesus's "much people" meeting the city's "much people… with her") —
both render as unindividuated hatched masses. Accepted variance across
pages, flagged in §8.

### Objects / locations

**THE BIER** — the title object; the episode fails if this renders wrong.
Build text (use verbatim):

> the bier: an open flat wooden hand-bier — a plain rectangular pallet of
> weathered olive-brown wood boards with two long carrying poles running its
> full length, borne shoulder-high on the shoulders of four bearers, its top
> entirely open to the sky — never a coffin, never a casket, never a box,
> never any lid

**The "bier" literalism trap (the Barrel's "barrel" lesson, same family):**
an image model's prior for "bier"/"funeral procession" is a Western coffin
or a draped casket — wrong by geography and centuries, and it would
physically hide the shrouded form whose visibility the whole episode turns
on ("touched the bier" only reads as touching-death-adjacent if the body is
openly THERE). Every prompt that shows it says "open flat wooden hand-bier"
first and carries the never-coffin/never-box/never-lid triple verbatim;
both covers append "coffin, casket, closed box, lid" to their Avoid lists.
Captions and title still say "bier" — that is the KJV's word; only the
drawing is corrected.
Ref: `bier_ref.png` cropped from F01 approved — deliberately cropped WITH
the shrouded form on it, because bier-and-burden travel as one object
through F01–F05. The EMPTY bier (F06 midground, back cover hero) is a
different state needing an explicit override ("the bier now empty, no
body on it, the linen lying folded on its bare boards") — and see §8 for
the proposed panel-crop ref that would pin the empty state properly.

**THE GATE OF NAIN** — the location that makes the geometry work (Luke 7:12:
"when he came nigh to the gate of the city, behold, there was a dead man
carried out"). Build text:

> the gate of Nain: a low squared opening in a rough drystone-and-mud-brick
> village wall, a heavy timber lintel, the lane through it climbing between
> small flat-roofed houses stacked on the green-brown slope of the hill
> behind; outside the gate, a dusty road running down the open slope, and
> scattered dark rock-cut tomb openings in the hillside further down

Why the tombs: burial was outside the walls, and the rock-cut tombs on the
slope below Nain are attested — they give the procession a visible
DESTINATION (front cover, F01) and, inverted, a visible "road not taken"
(F06 panel). The gate itself is the episode's hinge geometry: death carried
OUT through it (front, F01), life walking back IN through it (F06) — the
narration's direction-reversal drawn as one doorway used both ways.
Ref: `gate_ref.png`, cropped from F01 approved.

### Chain order (hard dependencies)

1. Copy `jesus_ref.png` from episode 4 (immediate, no cycle).
2. **F01** renders with `refs=[]` — widow, bier (with form), and gate ALL
   debut here → approve → crop `widow_ref`, `widow_face_ref`, `bier_ref`,
   `gate_ref`. *Risk, accepted and flagged (§8): a TRIPLE debut on one
   approval — a miss on any of the three means a full-page regen. There is
   no earlier page to split them across: the procession is the first beat,
   and the procession IS widow + bier + gate. Budget one extra regen cycle,
   same as the Barrel's dual debut.*
3. **Front cover** (widow_ref + bier_ref + gate_ref) after F01.
4. **F02** (jesus_ref + widow refs + bier_ref + gate_ref), **F03** (jesus_ref
   + bier_ref + widow refs + gate_ref), **F04** (jesus_ref + bier_ref +
   widow refs) may then run, any order.
5. **F05** (jesus_ref + bier_ref + widow refs) → approve → crop `son_ref`.
6. **F06** (jesus_ref + widow refs + son_ref + gate_ref + bier_ref) after F05.
7. **Back cover** (bier_ref + gate_ref, no figures) after F01 (or after the
   §8 empty-bier panel-crop decision).

---

## 4. Covers

### The cover judgment call (stated, as the format asks)

Naaman's front went to its NT scene because ITS narration opens there; the
Barrel's went to the widow because ITS hook is hers. THIS narration opens on
the procession and lands on "he touched a funeral, and it became a
homecoming" — and both of those sentences are pictures of the BIER: full and
walking out, empty and left behind. So the covers are the title object in
its two states, and the bookend pair IS the episode's argument: same object,
same gate, death outbound on the front, death unemployed on the back. Jesus
appears on neither cover — deliberate: the narration's hook doesn't name him
yet (he enters at F02), the back cover's empty bier says what he did more
loudly than his figure would, and it keeps the series' covers varied (ep4
led with Jesus; ep5 led with its widow; ep7 leads with the object).

### FRONT COVER

- **Scene:** the funeral procession emerging through the gate of Nain,
  small and isolated in the lower third: four bearers carrying the open
  hand-bier shoulder-high, the shrouded form lying on its open top (never a
  coffin, never a box, never a lid — the form openly visible), the widow
  walking close behind it, veiled, her rent mourning mantle drawn about
  her; behind her, the village crowd following out of the gate; the low
  drystone-and-mud-brick wall and timber-lintel gate rising behind them,
  the small flat-roofed houses of Nain stacked on the hill's slope above;
  the dusty road running down the open slope ahead of the procession toward
  scattered dark rock-cut tomb openings in the hillside — the destination
  visible, the walk already begun.
- **Lighting (law: ≥1 warm + ≥1 cool):** low hard morning light breaking
  warm ochre-gold across the hillside, the village rooftops, and the dusty
  road, against cold slate blue-grey shadow holding the gate's opening, the
  wall, and the dark-clothed procession itself. WHY this split: the world is
  warm and alive; the procession is the one cold thing moving through it —
  death walking through an ordinary bright morning, which is exactly the
  hook's register ("that was survival, not cruelty" — nobody in this frame
  is a villain, the day is simply going on).
- **Motif:** none (covers never carry the interior motifs — see §2's table
  note; the cold/warm split does the work).
- **Title:** `THE BIER HE TOUCHED` (top) — the locked episode title, naming
  the act per the series-plan retitle. **Subtitle:** `LUKE 7`.
- **seq_title for all interior pages = `THE BIER HE TOUCHED`** (matching
  front title, the Naaman/Barrel pattern). Fallback if it proves long for
  the handwritten page-top: `THE BIER` (§8).
- **Refs:** widow_ref + bier_ref + gate_ref (hence F01 approval precedes
  this render).
- **extra_avoid append:** "coffin, casket, closed box, lid, visible dead
  face, gore, skeletal figures, modern funeral clothing".
- **Animation (strong front lock, per the cover doc):** the procession
  continues its slow, even funeral pace forward along the road — one
  continuous unhurried walk, no figure turning or stopping (the living
  detail; an unnamed crowd may take generic motion per LAW 1); the widow's
  veil and mantle stir faintly as she walks; the morning light stays
  exactly as warm and low as it already is, unchanged; the gate, wall, and
  tombs stay exactly as drawn. `clip_duration=8` (23-word ≈ 8.5s slot).
  Assembly mode freeze — a walking procession is directional motion,
  NEVER boomerang (it would visibly walk backwards, the exact ep4 defect).

### BACK COVER

- **Scene:** dawn, outside the gate of Nain; the open hand-bier EMPTY,
  leaning upright at a slight angle against the drystone wall beside the
  gate opening, its two carrying poles bare; lying folded in a neat small
  pile on its bare boards, the linen grave-bands and, set on top of them,
  the linen napkin folded together by itself; the road down toward the
  rock-cut tombs empty and untraveled; through the gate's opening, the lane
  into the village just catching light. One small hard-capped closed curl
  of blue ink with a trace of muted gold rises from the folded napkin on
  the boards, its whole visible length no longer than a hand's width,
  curled into one small closed loop, never straightening, never trailing,
  behaving like a small dab of living ink, never a glow.
- **Why this image:** the landing is "he touched a funeral, and it became a
  homecoming" — the canceled funeral IS the empty bier with its unused
  graveclothes, exactly the object-landing grammar of Naaman's abandoned
  armor. And the folded napkin set by itself is a deliberate, quiet echo of
  John 20:7 ("the napkin, that was about his head… wrapped together in a
  place by itself") — this raising is the season's foretaste of THE
  resurrection, and the back cover whispers it to anyone who knows the
  verse without costing a new viewer anything. The living curl rises from
  the napkin — the life-mark sitting on death's unemployed equipment.
- **Lighting (law):** warm dawn gold pouring OUT through the gate's opening
  from the village side, falling across the bier's boards and the folded
  linen; cold blue-grey night shadow still holding the downhill road and
  the tomb-pocked slope. WHY: the geography of the light is the sermon —
  warmth comes from the homecoming side of the wall, the cold lingers
  toward the graves, and the bier leans exactly on the boundary, retired.
- **Title:** `IT BECAME A HOMECOMING` (bottom) — the narration's own final
  clause, verbatim contiguous. **Subtitle:** `NUMBERS 19:11` — completing
  the season's designed #2→#7 rhyme on the covers themselves: episode 2's
  FRONT said "NUMBERS 19" (the law of corpse-defilement); episode 7's BACK
  answers it from the other side of the fulfilment, mirroring how ep1's
  back (`JOHN 1:51`) pointed at its own rhyme-partner #8. Flagged in §8
  with `JOHN 11:25` as the alternative if the user prefers a forward NT
  landing over the backward rhyme.
- **Refs:** bier_ref + gate_ref (empty-state override stated; see §8 for
  the proposed empty-bier panel-crop ref).
- **extra_avoid append:** "coffin, casket, closed box, lid, skeleton,
  bones, any human figure".
- **Animation (light back lock, per the cover doc):** fine dust motes
  drift slowly through the shaft of dawn light in the gate's opening; one
  loose edge of the folded linen stirs faintly and settles; the blue-gold
  curl stays exactly as drawn, in place, for the whole clip; the dawn
  light stays exactly as warm and low as it already is, unchanged.
  `clip_duration=8` (34-word ≈ 12.6s slot; freeze fill — drifting motes
  are directional-on-reversal risk, the Barrel's own call).

---

## 5. Page design conventions used below

- Every page: `panel_style="woodcut_hybrid"`, 9:16,
  include_no_bubble_clause True (two pages carry Jesus's own quoted-line
  captions — the exact speech-bubble-prior case).
- Main-scene prose below is written near-final (PageSpec `main_scene_still`
  register, starting mid-sentence after the shot type, dosage line at the
  end, Naaman-style). Sonnet may tighten wording but must keep every
  MUST-SHOW, dosage, separation, never-X, and steady-line clause. Animation
  prose is design intent — per LAW 4, Sonnet writes the final animation
  prompt against the RENDERED still's actual pixels.
- **NO_MOUTH** goes to Jesus on F02 and F04 (his two voiced lines) — and,
  belt-and-braces, to the BOY on F05: the narration says "began to speak,"
  which is the strongest lip-sync temptation in the series so far; his lips
  stay closed like every other figure's (voice-over series, no lip-sync,
  ever).
- **Standing steady-line override (the no-Fray guard):** every page the
  widow appears on states *"her contour drawn steady and single-struck, no
  doubled or tremored line anywhere in her figure"* — a weeping figure is
  exactly what a render will spontaneously loosen into fray-like hatching,
  and this episode's retag makes accidental Fray a canon error, not a
  style wobble. Same clause for the bearers and the boy where they carry
  emotional weight.
- **Corpse discipline:** the shrouded form's face is NEVER visible
  (napkin bound over it, F01–F04); no dead face is ever rendered in this
  episode. On every F01–F04 animation the form gets an absolute stillness
  clause including "no rise or fall of breath" — a corpse does not
  breathe, and any stir would pre-empt the miracle that belongs to the
  F04→F05 cut. F05 then grants the breath explicitly — the two clips'
  opposite breath clauses ARE the resurrection, told in animation grammar.
- KJV captions are verbatim contiguous fragments, ≤4 words per line;
  panel labels 2-3 authored words; corner notes short.
- Model lanes per the north-star tiering: Kling3.0 pro where a designed
  gesture must COMPLETE mid-clip; veo3_1_lite for holds/ambient/locomotion
  pages. Stated per page with its why.

---

## 6. Page-by-page

### F01 — "Everyone kept their distance" (21w · Stain **D3 peak** · Swirl 0 · veo3_1_lite, clip 5)

The law page — the Stain's own establishing shot. Triple-debut page (widow,
bier, gate → all five ref crops), so its approval bar is the episode's
highest, and its camera is deliberately a MEDIUM shot (not wide) so the
widow's face crops clean for `widow_face_ref`.

- **Panels**
  1. `"kept their distance"` — a doorway in a village wall, a householder
     drawn back deep into its shadow, watching the road pass *(the law as
     lived behavior — a different household, not the road crowd, so it
     supports without duplicating the main scene)*
  2. `"water of separation"` — a plain clay vessel of water with a sprig of
     hyssop laid across its mouth *(Numbers 19:9's own remedy for exactly
     this defilement — episode 2's purification kit, standing ready. Plants
     the F04 panel rhyme, and stitches the season's #2→#7 rhyme into the
     page furniture)*
  3. `"outside the walls"` — dark rock-cut tomb openings in a bare
     hillside, small and unadorned *(where this road ends; the
     destination the touch will cancel)*
- **Main scene** — `MEDIUM shot`:
  > the dusty road just outside the gate of Nain — the low
  > drystone-and-mud-brick wall and timber-lintel gate rising at the frame's
  > edge, fully inside the frame. The open flat wooden hand-bier — a plain
  > rectangular pallet of weathered olive-brown wood boards with two long
  > carrying poles running its full length, its top entirely open to the
  > sky, never a coffin, never a casket, never any lid — borne shoulder-high
  > past the viewer by four bearers in plain undyed and ochre wool, their
  > heads bowed, their faces turned down toward the poles, none of them
  > individuated or finished; lying full-length on the bier's open top, the
  > dead son: a still human form wrapped from chest to feet in plain linen
  > grave-bands, a folded linen napkin bound over the face so that no
  > feature of the face is visible, the wrapped form slight and young,
  > fully inside the frame. Close behind the bier, {WIDOW_BUILD}, fully
  > inside the frame, walking with her eyes down, one hand holding her rent
  > mantle closed at the breast, her face lined with weeping; her contour
  > drawn steady and single-struck, no doubled or tremored line anywhere in
  > her figure. At the road's edges, villagers drawn back off the road —
  > figures pressed to the walls and standing in halted clusters, a wide
  > band of bare empty ground between every one of them and the bier, no
  > one within arm's reach of it but the bearers and the widow. A cold
  > grey-umber stain lies in the paper itself beneath the bier and the
  > bare ground around it, formless and matte, its feathered damp edge
  > crossing the drawn frame border into the page's own lower margin
  > directly below the bier, never over any face, bounded to less than a
  > third of the page; its edge stops short of every living figure, a band
  > of clean paper between the stain and the widow, the bearers' feet, and
  > every villager. Stage 0 dosage: no blue Swirls of Life ink motif
  > anywhere on this page — no blue ink appears anywhere in the scene, the
  > panels, or the margins.
- **material_closer:** "the cold stain lying in the paper beneath the bier
  is the only unusual ink at work on this page, and no blue appears
  anywhere."
- **Fence:** `stain` — "the cold grey-umber stain in the paper beneath the
  bier"
- **Caption:** `("and you were unclean",)` *(narration verbatim, 4 words —
  the law in its own voice)* · **Corner note:** `NOTE: survival, not cruelty`
  *(the narration's own mercy toward the crowd — this page must not read as
  villainizing them)*
- **Panel motions:** (1) the shadow inside the doorway deepens very
  slightly, nothing else changes; (2) the light across the clay vessel
  warms softly and settles *(vessel + liquid = the loaded invention prior —
  tone-only, always)*; (3) a thin haze drifts across the hillside before
  the tomb openings.
- **Main animation:** the bearers and the bier continue their slow, even
  funeral pace along the road, one continuous unhurried walk; the widow
  walks with them at the same pace, her eyes staying down, her mantle
  stirring faintly; the shrouded form lies completely still on the bier,
  exactly as drawn, no rise or fall of breath, for the whole clip; every
  villager at the road's edges stays exactly as drawn, held in their
  drawn-back stillness; the cold stain in the paper stays exactly as
  drawn, never deepening, never spreading, never fading.
- **Why veo:** continuation-of-drawn-locomotion plus holds, no completing
  gesture — veo's proven lane (it handled real walking cleanly on John 4's
  F07 v2 era findings), at the cheaper credit tier on the page most likely
  to need likeness regens. `refs=[]`.

### F02 — "Weep not" (24w · Stain D3 held + **Swirl 1 first trace** = 4, AT CAP · kling3_0, clip 5)

Jesus enters the episode — and the first blue of the episode enters with
him, one thread from the hand that will do the touching. The first of the
two at-cap pages: full QUAD lock.

- **Panels**
  1. `"he saw her"` — a close study of the widow's tear-lined eyes beneath
     the dark veil *(needs widow_face_ref; the compassion clause made
     visible — he SAW her before he did anything)*
  2. `"toward, not away"` — worn sandaled feet mid-stride on a dusty road,
     the hem of a plain cream-brown robe above them *(the narration's own
     inversion, drawn at ground level — everyone else's feet step back;
     these step forward)*
  3. `"two crowds met"` — two streams of small figures converging on one
     road outside a gate, seen far off *(Luke's own staging: his "much
     people" meeting her "much people" — the collision of processions this
     whole episode is)*
- **Main scene** — `MEDIUM TWO-SHOT`:
  > the road before the gate of Nain. {JESUS_BUILD}, fully inside the
  > frame, standing in the procession's path facing the widow, his gaze on
  > her, his right hand half-lifted toward her, palm gently open, already
  > raised, not touching anything; {WIDOW_BUILD}, fully inside the frame,
  > stopped before him, her tear-lined face lifting toward his, one hand
  > still holding her rent mantle closed; her contour drawn steady and
  > single-struck, no doubled or tremored line anywhere in her figure.
  > Behind and beside them, the open wooden hand-bier held steady on the
  > four bearers' shoulders, the shrouded form with its napkin-bound face
  > lying on its open top, never a coffin, never any lid, fully inside the
  > frame; the halted crowds drawn as unindividuated hatched masses beyond.
  > The cold grey-umber stain lies in the paper beneath the bier, unchanged
  > from before, still crossing the drawn frame border into the lower
  > margin, never over any face, a band of clean paper between the stain
  > and every living figure, the stain nowhere near Jesus and never beneath
  > his figure or his feet. Stage 1 dosage: exactly one restrained thread
  > of blue ink curling up from the back of Jesus's half-lifted right hand,
  > touching only his hand and the air just above it, the only blue on the
  > whole page, behaving like one stroke of wet ink bled into the paper,
  > smooth and open in its curl, never blot-shaped; the stain formless and
  > matte, never swirl-shaped; a wide band of untouched clean paper between
  > the thread and the stain at every point, the thread drawn ON the page's
  > surface, the stain lying IN the paper beneath the linework.
- **material_closer:** "the cold stain in the paper and the single blue
  thread at his hand are the only two kinds of unusual ink at work on this
  page, kept apart by clean paper."
- **Fence:** `stain` — "the cold grey-umber stain in the paper beneath the
  bier and the single blue thread at his lifted hand"
- **Caption:** `("Weep not",)` *(KJV Luke 7:13 verbatim — two words, the
  jesus-voice line; the episode's shortest caption on its tenderest beat,
  the Barrel's own "Fear not" pattern)* · **Corner note:**
  `NOTE: toward, not away`
- **Panel motions:** (1) the sketched eyes hold, the light across the
  study warming very slightly *(tone-only — small sketched faces morph
  under content-motion asks)*; (2) a thin banner of dust drifts low across
  the road behind the sandaled feet; (3) the two far crowd-streams hold,
  a faint heat-shimmer over the road between them.
- **Main animation:** the widow's tear-lined face completes its lift and
  her eyes settle on Jesus, finishing early and holding still; Jesus stays
  exactly as drawn, his half-lifted hand not rising further and not
  reaching toward anything, one slow steady breath, his lips staying
  closed and completely still — he is not speaking and his mouth does not
  move at all; the bearers hold the bier perfectly steady; the shrouded
  form lies completely still, exactly as drawn, no rise or fall of breath;
  the single thin blue ink thread at his hand stays exactly as drawn, in
  place, for the whole clip; the cold stain in the paper stays exactly as
  drawn, never deepening, never spreading, never fading.
- **Why kling, and why the gesture is HERS:** her face-lift is the page's
  one human event (the Hem-F05 "what is the one human thing" register) and
  a completing gesture — Kling's lane. Jesus's hand deliberately does NOT
  move: a hand completing a lift toward the bier would tempt the model to
  render the touch, and the touch belongs to F03's page turn. Stage 1
  thread motion is the worst risk/reward on the page — held still, per the
  north-star table.
- **Refs:** jesus_ref + widow_ref + widow_face_ref + bier_ref + gate_ref.

### F03 — "And touched the bier" (23w · Stain **D2-turning** · Swirl 1 held · kling3_0, clip 5)

The title act. Contact is drawn as ALREADY MADE — his hand rests on the
bier's rail; no clip ever shows the hand arriving. The page's whole story is
the stain's dried edge: the damage in the paper has begun dying at exactly
the point where he touched it, and the direction of the dying points away
from him. Deliberately the quietest swirl of the middle pages — "and they
that bare him stood still" is an awe-halt, not a crescendo.

- **Panels**
  1. `"stood still"` — four pairs of sandaled feet halted mid-stride on the
     dusty road, close, low dust settling around them *(KJV's own clause
     made visible at ground level)*
  2. `"the open bier"` — a small object study of the hand-bier empty: bare
     boards, two poles, no lid, drawn plain *(the object the episode is
     named for, studied on its own — and the deliberate seed of the back
     cover's empty-bier image and the §8 panel-crop ref)*
  3. `"unclean until even"` — a lone small figure seated apart from a
     village wall under a low sun *(KJV Numbers 19:22 verbatim contiguous —
     what the law says should now happen to the man who touched it: the
     exile he should have contracted, drawn one panel before the page that
     says it didn't work that way)*
- **Main scene** — `MEDIUM shot`:
  > the road before the gate. {JESUS_BUILD}, fully inside the frame,
  > standing at the side of the halted bier, his right hand laid flat and
  > full on the bier's wooden side rail, palm down, in complete unbroken
  > contact with the wood, fully inside the frame — the hand and the rail
  > touching with no gap between them; the four bearers frozen mid-step
  > under the poles, their heads turned toward him, their postures caught
  > between motion and stillness, none of their faces individuated or
  > finished; the shrouded form with its napkin-bound face lying
  > full-length on the bier's open top, never a coffin, never any lid,
  > fully inside the frame; {WIDOW_BUILD} a step behind, her hands risen
  > toward her mouth, her contour drawn steady and single-struck, no
  > doubled or tremored line anywhere in her figure. The cold grey-umber
  > stain lies in the paper beneath the bier, still crossing the drawn
  > frame border into the lower margin on the side away from Jesus, never
  > over any face — but its whole edge nearest his touching hand has dried
  > to a pale ring, the wet remainder lying only toward the bier's far
  > end, away from him; no stain of any kind on Jesus's figure, hand,
  > sleeve, or the paper beneath him — his side of the page the cleanest
  > paper on it. Stage 1 dosage, held: the same single restrained thread
  > of blue ink, now rising thin from the back of his right hand where it
  > rests on the rail, straight up, touching only his hand and the air
  > above it, the only blue on the whole page, behaving like one stroke of
  > wet ink bled into the paper, a wide band of untouched clean paper
  > between the thread and the stain's wet remainder at every point.
- **material_closer:** "the stain dying back from his hand and the single
  blue thread rising from it are the only two kinds of unusual ink at work
  on this page, kept apart by clean paper."
- **Fence:** `stain` — "the cold grey-umber stain in the paper beneath the
  bier, its dried pale edge, and the single blue thread at his hand"
- **Caption:** `("and touched the bier",)` *(KJV Luke 7:14 verbatim
  contiguous, 4 words — the title act in the text's own words)* ·
  **Corner note:** `NOTE: the flow reverses` *(the stain geometry's
  caption — three words naming what the page is doing)*
- **Panel motions:** (1) the settling dust around the halted feet thins
  and stills; (2) the empty bier study holds, the light across its boards
  warming very slightly; (3) the lone figure holds, seated apart,
  unmoving.
- **Main animation:** Jesus's head bows slightly toward the shrouded form
  and stills, finishing early and holding — his hand staying laid flat on
  the rail exactly as drawn, pressing without moving, never lifting, never
  sliding; the bearers hold their frozen mid-step postures, knuckles tight
  on the poles, each one slow breath; the shrouded form lies completely
  still, exactly as drawn, no rise or fall of breath; the widow's raised
  hands tremble faintly and still; the single thin blue ink thread at his
  hand stays exactly as drawn, in place, for the whole clip; the stain and
  its dried pale edge stay exactly as drawn, never deepening, never
  spreading, never fading.
- **Why kling:** the head-bow is a designed completing gesture, and this
  is the title page — it earns the gesture lane. The touch itself is
  never animated: contact is a drawn fact, not a motion ask (LAW 0 — the
  still owns the story; the clip only continues it).
- **Refs:** jesus_ref + bier_ref + widow_ref + widow_face_ref + gate_ref.

### F04 — "Arise" (28w · Stain **D2-turning, late** + **Swirl 2** = 4, AT CAP · kling3_0, clip 9)

The doctrinal pivot ("Under that same law… It didn't work that way with
him") and the crossing point — swirl equals stain for the first time,
landing exactly on the command. The held-breath page: one second before the
miracle, everything fenced, one small human motion.

- **Panels**
  1. `"the old remedy"` — the same plain clay vessel of water with its
     hyssop sprig, unused, exactly as F01's panel drew it *(the deliberate
     panel rhyme, the Barrel's F02/F04 pattern: the Numbers 19 kit stands
     ready for the man who touched a bier — and stands unused, because the
     defilement never arrived. The rhyme carries the narration's "should
     have made him unclean… it didn't work that way" without a word)*
  2. `"the bound napkin"` — a close study of the folded linen napkin bound
     over the face, its knot and folds *(the last barrier between death
     and daylight — about to come off BETWEEN pages, never on camera)*
  3. `"her clasped hands"` — the widow's hands clasped tight at her lips,
     close *(hope she dares not say aloud; her face not in frame — the
     hands carry it)*
- **Main scene** — `MEDIUM shot`:
  > close along the side of the halted bier. {JESUS_BUILD}, fully inside
  > the frame, standing at the bier's head end, his right hand resting on
  > the wooden rail, his face turned down toward the shrouded form, calm,
  > unhurried, his gaze steady on the napkin-bound face; the shrouded form
  > lying full-length on the open boards, wrapped chest to feet in linen
  > grave-bands, the folded napkin bound over the face, no feature
  > visible, never a coffin, never any lid, fully inside the frame; two of
  > the bearers visible at the poles, heads turned, unfinished faces;
  > {WIDOW_BUILD} beyond the bier, gripping the rent edge of her mantle,
  > watching, her contour drawn steady and single-struck, no doubled or
  > tremored line anywhere in her figure. Of the cold grey-umber stain in
  > the paper, only a narrow wet remainder is left, lying directly beneath
  > the bier's head end; all the rest of its former reach — including where
  > it once crossed the drawn frame border into the margin — has dried to
  > a pale ring; never over any face, no stain anywhere on Jesus or the
  > paper beneath him. Stage 2 dosage: the blue ink motif quietly present —
  > a few soft blue threads and one small watercolor bloom rising from the
  > back of his hand on the rail into the air above it, touching only his
  > hand and the air, touching no other person and nothing else on the
  > page, every thread behaving like wet ink bled into the paper, smooth
  > and open, never blot-shaped; the stain remainder formless and matte,
  > never swirl-shaped; a wide band of untouched clean paper between the
  > threads and the stain remainder at every point, the threads drawn ON
  > the page, the stain lying IN the paper beneath the linework.
- **material_closer:** "the last narrow remainder of the stain and the
  soft blue threads at his hand are the only two kinds of unusual ink at
  work on this page, kept apart by clean paper."
- **Fence:** `stain` — "the narrow wet remainder of the stain beneath the
  bier's head, its dried pale ring, and the blue threads at his hand"
- **Caption:** `("I say unto thee,", "Arise")` *(KJV Luke 7:14 verbatim
  contiguous, 4+1 — the jesus-voice line)* · **Corner note:**
  `NOTE: no stain on him` *(the page's doctrine in four words — the law
  ran backward)*
- **Panel motions:** (1) the light across the clay vessel warms softly
  and settles *(tone-only, loaded prior)*; (2) the napkin study holds,
  its folds exactly as drawn, nothing stirring; (3) her clasped hands
  press once slightly tighter and still.
- **Main animation:** Jesus stays exactly as drawn, his hand resting on
  the rail without moving, one slow steady breath, his lips staying
  closed and completely still — he is not speaking and his mouth does not
  move at all; the shrouded form lies completely still, exactly as drawn,
  no rise or fall of breath, no stir anywhere in the linen, for the whole
  clip; the widow's grip on her mantle's edge tightens once and stills;
  the bearers hold, exactly as drawn; the soft blue threads at his hand
  drift gently within their own small area, never spreading beyond his
  hand and the air above it; the stain remainder and its dried ring stay
  exactly as drawn, never deepening, never spreading, never fading.
- **Why kling, and why the biggest slot gets the smallest asks:** 28 words
  ≈ 10.4s — the longest interior slot — on the page where the ONLY correct
  motion is almost none: any stir in the shroud destroys the F04→F05 cut.
  The widow's two micro-gestures (panel hands-press, main grip-tighten)
  are the completing gestures that keep the clip alive (the Hem's
  all-holds-is-lifeless lesson) while the motion budget is given
  legitimate small targets so it never lands on the linen (the F04-Hem
  aging-creep lesson — page-global fence plus real motion elsewhere).
  Kling for the completing micro-gestures; clip 9 (the Naaman F03/F04
  precedent duration), freeze + tail_loop to fill the slot.
- **Refs:** jesus_ref + bier_ref + widow_ref + widow_face_ref.

### F05 — "He that was dead sat up" (18w · Stain **D1** · Swirl 2 held · kling3_0, clip 5)

The miracle page — and the miracle itself happened between the pages: F04's
shrouded form IS F05's upright boy, and no clip ever shows the change. The
cut is the miracle, at its most literal in the whole season. The boy sits
inside the dried ring's cleanest cream — death's footprint made the newest
paper on the page.

- **Panels**
  1. `"the bands loosed"` — the linen grave-bands lying slack and unwound
     across the bier's boards *(what was bound, undone — object evidence,
     no figure)*
  2. `"his eyes open"` — a close study of the boy's living eyes, open,
     unlined, light in them *(needs the F05 main render itself for its
     crop — this panel is authored from the same build text; the face
     study that seeds son_ref's own likeness)*
  3. `"to his mother"` — two pairs of hands meeting: an older woman's
     hands clasping a young man's hand between them *(KJV 7:15's closing
     clause — the delivery, studied at hand scale; the embrace itself is
     saved for F06's world)*
- **Main scene** — `MEDIUM WIDE shot`:
  > the road before the gate, the bier still borne on the four bearers'
  > shoulders. The widow's son — a young man of about eighteen, lean and
  > slight, an olive-skinned unlined face with large dark eyes and tousled
  > black hair, alive, his eyes open — SITTING FULLY UPRIGHT on the open
  > bier's boards, already risen to a seated position, bare-shouldered
  > above the loosened linen grave-bands still wrapped about his waist and
  > legs, the unbound napkin fallen in his lap, his face turned toward his
  > mother, his lips closed; fully inside the frame. {JESUS_BUILD}, fully
  > inside the frame, standing at the bier's side, his right hand now
  > lifted open toward the widow in a small presenting gesture — giving
  > him back; {WIDOW_BUILD}, fully inside the frame, her arms opening
  > toward her son, not yet reaching him, her tear-lined face breaking
  > from grief into astonishment; her contour drawn steady and
  > single-struck, no doubled or tremored line anywhere in her figure.
  > The bearers still under the poles, faces turned up toward the risen
  > boy, awe in their unfinished faces; the halted crowds beyond, drawn
  > as hatched masses. Of the stain, nothing wet remains anywhere: only
  > the dried pale ring lies in the paper where the stain once sat
  > beneath the bier, and the paper inside that ring is the cleanest
  > cream on the whole page; no border crossing remains but a pale dried
  > trace. Stage 2 dosage, held: a few soft blue threads and one small
  > watercolor bloom rising from the back of Jesus's lifted hand into the
  > air above it, touching only his hand and the air, touching no other
  > person, every thread behaving like wet ink bled into the paper, a
  > band of clean paper between the threads and the dried ring.
- **material_closer:** "the dried pale ring in the paper and the soft
  blue threads at his lifted hand are the only two kinds of unusual mark
  on this page, and the paper inside the ring is the cleanest on it."
- **Fence:** `stain` — "the dried pale ring in the paper beneath the bier"
- **Caption:** `("he that was dead", "sat up")` *(KJV Luke 7:15 verbatim
  contiguous, 4+2)* · **Corner note:** `NOTE: given back` *(the delivery
  in two words)*
- **Panel motions:** (1) the slack grave-bands lie undisturbed, exactly
  as drawn; (2) the sketched living eyes blink once fully — closing,
  then opening again fully, ending wide open *(the full-arc blink rule;
  the one panel in the episode that earns a real content motion, because
  aliveness IS this panel's subject)*; (3) the clasped hands hold,
  the light across them warming very slightly.
- **Main animation:** the boy's chest rises and falls in slow visible
  breathing — the first breath on any bier page — his head turning the
  last small distance toward his mother and settling, his lips staying
  closed and completely still, not speaking, his mouth never moving; the
  widow's opening arms complete the last small part of their opening and
  hold, not yet reaching him; Jesus stays exactly as drawn, his lifted
  hand not moving further, one slow steady breath, lips closed and
  completely still; the bearers hold the bier perfectly steady; the soft
  blue threads at his hand drift gently within their own small area; the
  dried pale ring stays exactly as drawn, and no new stain, spot, or
  darkening appears anywhere on the page at any point.
- **Why kling, and the breath-inversion:** two completing gestures (the
  boy's head-turn, her arms' last opening) — Kling's lane. The load-bearing
  design detail: F04's animation DENIED breath to the form ("no rise or
  fall of breath"); F05's GRANTS it in so many words — the resurrection is
  told by the only clause that changed. "Began to speak" stays narrated:
  his lips are closed like every figure in this series, and the caption
  carries "sat up," not the speaking.
- **Refs:** jesus_ref + bier_ref + widow_ref + widow_face_ref. → approve →
  crop `son_ref` (face + shoulders).

### F06 — "Life spread from Jesus to the boy" (15w · Stain **D0** · **Swirl 3** · veo3_1_lite, clip 5)

The thesis page, drawn as the homecoming: the same gate that death was
carried OUT of, now walked back IN through — the narration's
direction-reversal as pure geometry. The episode's one Stage 3 page, earned
here and nowhere else (§2), on the community image Stage 3 was designed
for. The empty bier leans retired against the wall, planting the back cover.

- **Panels**
  1. `"a great prophet"` — a cluster of small figures with arms lifted in
     praise, seen from behind *(KJV Luke 7:16 verbatim contiguous — the
     crowd's own confession; posture, not faces)*
  2. `"the tombs behind"` — the rock-cut tomb openings on the hillside,
     the road past them empty and untraveled *(F01's panel 3 inverted:
     death's address, no delivery today)*
  3. `"home again"` — a warm-lit open doorway inside the village, a low
     table laid, no figures *(where this procession is going now; the
     funeral's destination replaced)*
- **Main scene** — `WIDE shot`:
  > the gate of Nain from outside, the low drystone-and-mud-brick wall and
  > timber lintel fully inside the frame, the lane through it climbing
  > between the small flat-roofed houses on the slope. The crowd streaming
  > IN through the gate toward home, drawn as one glad unindividuated
  > hatched mass; at its heart, fully inside the frame, the widow and her
  > son walking side by side, her arm wrapped through his, his loosened
  > grave-bands traded for a plain borrowed mantle about his shoulders,
  > both their contours drawn steady and single-struck; {JESUS_BUILD},
  > fully inside the frame, walking among them at the same unhurried pace,
  > unremarkable in the crowd; leaning upright against the wall's outer
  > face beside the gate, small in the midground, the open hand-bier now
  > empty, no body on it, its bare boards and two poles plain, the linen
  > lying folded on its boards, never a coffin, never any lid, fully
  > inside the frame. No stain, ring, or grey blot anywhere in the paper —
  > the paper wholly clean. Stage 3 dosage: the blue ink motif, with
  > traces of muted gold, is woven through the whole scene — threads
  > drifting in one loose open band through the air of the road and the
  > gate's opening, above every head, touching no person, tied to no
  > single figure, behaving like wet ink bled through the page's own sky
  > wash, never a glow.
- **material_closer:** "the blue-and-gold band woven through the air is
  the only unusual ink on the page, and the paper beneath it is wholly
  clean."
- **Fence:** `none`
- **Caption:** `("God hath visited", "his people")` *(KJV Luke 7:16
  verbatim contiguous, 3+2 — the crowd's verdict as the page's text)* ·
  **Corner note:** `NOTE: the other direction`
- **Panel motions:** (1) the lifted arms hold their praise, unmoving, the
  light across them warming; (2) a thin haze drifts across the hillside
  before the tombs; (3) the doorway's warm light stays exactly as warm
  and steady as it already is, unchanged *(veo positive-only light
  language)*.
- **Main animation:** the crowd continues its slow glad walk in through
  the gate at an even pace; the widow and her son walk with them, her arm
  keeping its hold through his, neither turning; Jesus walks among them
  at the same even pace; the blue-and-gold ink threads drift smoothly
  within their own fixed band across the air above the road, never
  lowering onto any figure; the empty bier leans motionless against the
  wall, exactly as drawn.
- **Why veo:** continuation-of-drawn-locomotion for an unindividuated
  crowd plus fixed-band drift — veo's exact lane, no completing gesture
  anywhere, and the cheaper tier on a page whose Stage 3 band may need a
  dosage regen. Positive-only light wording throughout (no
  glint/sparkle).
- **Refs:** jesus_ref + widow_ref + widow_face_ref + son_ref + gate_ref +
  bier_ref.

---

## 7. Assembly suggestions (word-proportional, Fable estimates)

186 words over 69.0s of locked audio ≈ 2.70 words/sec. Modes follow the
standing lessons: **boomerang nowhere in this episode** — every unit either
walks (directional locomotion: front, F01, F06), settles a completing
gesture (F02, F03, F04, F05), or drifts motes (back — directional-on-
reversal risk, the Barrel's own call). Freeze everywhere, tail_loop where a
gesture settles near the clip's end. Every clip is designed shorter than
its slot (freeze pads, never trims — the standing swirls-freeze lesson).
Final modes are an assembly-QC call on the real renders — real playback,
per the standing rule.

| Unit | Words | ≈Slot | Clip | Model | Suggested mode |
|---|---|---|---|---|---|
| front | 23 | 8.5s | 8s | veo | freeze (walking — never boomerang) |
| f01 | 21 | 7.8s | 5s | veo | freeze (walking) |
| f02 | 24 | 8.9s | 5s | kling | freeze + tail_loop ~1.0 (face-lift settles) |
| f03 | 23 | 8.5s | 5s | kling | freeze + tail_loop ~1.0 (head-bow settles) |
| f04 | 28 | 10.4s | 9s | kling | freeze + tail_loop ~1.0 (grip-tighten stills) |
| f05 | 18 | 6.7s | 5s | kling | freeze + tail_loop ~1.0 (head-turn/arms settle) |
| f06 | 15 | 5.6s | 5s | veo | freeze (walking) |
| back | 34 | 12.6s | 8s | veo | freeze (drifting motes — be safe) |

Sum 186 = the narration's own count; 69.0s locked audio + landing hold
≥3.0s (INV-26) — in family with the series' shipped runtimes. Lane split:
4 kling (the completing-gesture pages) + 4 veo (locomotion/ambient) — the
same 50/50 shape as Naaman, on the cheaper-first tiering. Credits, not
dollars, are estimated here; the ledger (`/cost`, `/spend`) is the only
truth, and the render provider is the locked series default (OpenArt
bridge; HF fallback only by the user's explicit `SWIRLS_GEN_PROVIDER=hf`).

---

## 8. OPEN QUESTIONS (do not silently resolve)

1. **Back-cover subtitle: `NUMBERS 19:11` vs `JOHN 11:25`.** I recommend
   NUMBERS 19:11 — it completes the season's designed #2→#7 rhyme on the
   covers themselves (ep2's front said "NUMBERS 19"; ep1's back likewise
   pointed at its rhyme-partner's text with JOHN 1:51). The alternative,
   JOHN 11:25 ("I am the resurrection, and the life"), is the doctrinal
   apex verse if the user prefers a forward NT landing over the backward
   rhyme. One line to change.
2. **The swirl anchored to Jesus's own hand (F02–F05).** The series has
   two prior notes of hesitancy about figure-anchoring (the Doubting-
   Thomas placement the user flagged as "not reading"; #11's "his word,
   not his figure"). My reasoning for overriding here is in §2 — the
   narration names his person as the source ("Life spread FROM JESUS"),
   and the touching hand is the least indirect anchor available. Needs
   the user's eye at F02's first render: if the thread-at-hand reads as
   decoration rather than source, the fallback anchor is the air directly
   above the bier rail at the touch point (same zone logic, one line per
   page).
3. **Stage 3 on F06.** My call is YES (NT fulfilment on-page — the rule's
   own carve-out; full reasoning §2), held to exactly one page. If the
   user prefers the conservative Stage 2 cap anyway, F06's dosage line
   drops to the Stage 2 register and the episode still works — but the
   season's second old-to-new rhyme loses its visual payoff, so I
   recommend keeping 3.
4. **F04 sits AT the high-tide cap (D2-late + Stage 2 = 4), the second
   cap page after F02.** Counted conservatively (the stain is nearly
   spent — arguably closer to D1). If the user wants slack on the
   episode's most fence-critical page, the relief valve is dropping F04's
   swirl to Stage 1 held (thread only, no bloom) → sum 3; the cost is
   losing the "dose answers the command" beat. I recommend keeping 2+2
   with the full QUAD lock — it is ep12's own proven numeric shape.
5. **seq/front title length.** `THE BIER HE TOUCHED` (4 words) matches
   the Barrel's 4-word precedent, which shipped clean. If it proves long
   for the handwritten page-top at render, `THE BIER` is the fallback;
   the front cover keeps the full phrase either way.
6. **Empty-bier ref via panel crop (new practice).** The back cover and
   F06 need the bier EMPTY, but `bier_ref.png` is deliberately cropped
   WITH the shrouded form (they are one object F01–F05). Proposal: crop
   an `empty_bier_ref.png` from F03's approved panel 2 ("the open bier" —
   an empty object study, rendered in the same woodcut register the
   covers use). Cropping a REF from a woodcut PANEL is a first for the
   series; if declined, the back cover chains bier_ref with an explicit
   "now empty, no body" override and accepts the residual variance.
7. **F01 triple debut** — widow, bier, AND gate all crop from F01's
   single approval; a likeness/form miss on any means a full-page regen.
   Unavoidable (the procession is the first beat and the procession is
   all three). Budget one extra regen cycle, per the Barrel's dual-debut
   precedent.
8. **Un-ref'd recurring extras** — the four bearers (F01–F05) and the
   shrouded form (F01–F04) carry no refs by design: bearers stay
   unindividuated hatched figures with turned/bowed faces; the form is a
   wrapped shape with no face to pin. Accepted panel-scale variance,
   flagged; if any render individuates a bearer enough to be
   recognizable, regen rather than ref him.
9. **The widow carries NO motif at all** — no Stain (grief is not
   uncleanness; the diagnosis belongs to the bier), no Fray (the retag is
   binding). Stated here as a decision with its reasoning (§2, §3), not
   an open item — listed only so the implementation pass never "helpfully"
   adds either. The steady-line override clause on every page is the
   enforcement.
