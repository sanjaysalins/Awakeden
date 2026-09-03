# DESIGN BRIEF — Episode 10, "She Loved Much"

Luke 7:36-50 (the woman in Simon the Pharisee's house) · Dead ink: **Stain (moral
sin/guilt) — attached to the WOMAN, the series' first Stain that the text itself puts
on a living person it names "a sinner" (v37, v39)** · NO Fray anywhere (zero fear/doubt
vocabulary; her weeping is contrition/love, not fear — and a weeping figure is exactly
what a render loosens into fray-hatching, so the steady-line override is stated on every
page she is on) · NT episode, Jesus bodily present and DECLARING forgiveness — the OT
Stage 1-2 cap does NOT apply; Stage 3 is reached once (§2) · `panel_style`
**woodcut_hybrid** throughout · Voices: narrator + **jesus** + **simon** (voices.json).

Fable design pass, 2026-09-03. This brief is the single creative source for the Sonnet
implementation pass (episode.py PageSpec/CoverSpec objects). Narration and audio are
LOCKED — 240 words, 103.29s final, `narrator_atempo_factor 1.0` (no time-stretch),
seven voiced quotes each with a 0.4s pre-quote pause. Nothing here changes a spoken
word. Every choice states its WHY. Open questions are flagged inline and collected in
§8 — do not silently resolve them.

---

## 0. The shape of the episode, in one paragraph

The narration is built on a three-beat spine — **"No water for his feet. No kiss. No
oil."** — and everything in the story happens at Jesus's FEET, at the foot-end of a
reclining couch, behind his back. So the episode's geometry is fixed on every page:
table at the left, Simon on the far couch, Jesus on the near couch propped on his left
elbow with his bare feet extended away from the table, the doorway and the woman at the
LOWER RIGHT. The covers belong to the **alabaster box** in its two states: front = she
stands at Simon's lit threshold carrying it in (the hook's own picture — Simon's table
beyond her, the dry foot-basin by the door); back = the flask left standing open on the
floor at the couch-foot, the room empty, no stain anywhere ("she left carrying his
peace" — the object-landing grammar of Naaman's armor, the Barrel's open jar, the Bier's
folded linen). Nine interior pages, not six: the narration runs 1.5× the series' usual
length and its beats split nine ways under the freeze-budget cap (§1). The hard
problem — the Stain on a living person whose LOVE must not be what clears it — is
solved with two rules stated on every page: (1) the stain lives IN THE PAPER beneath
and around HER position (Hem/Naaman geometry), crossing the lower-right border, and it
travels with her across the room ("whoever still carries what Simon called her");
(2) her tears and ointment are REAL LIQUID IN THE SCENE, on HIS feet, on a different
diegetic layer and in a different zone, separated by a stated band of clean paper —
the stain stays at full D3, visibly unchanged, through both tear pages, and its drying
begins only at the first SPOKEN forgiveness (F05, "he frankly forgave them both"), from
Jesus's side outward, until only the dried ring remains under her at the declaration
(F08, "Her sins… are forgiven") and nothing at all at "go in peace" (F09). The swirl
rises against it — 0·0·0·1·1·1·2·2·3 — anchored to the hand Jesus speaks with (the
ep7 hand-anchor precedent, user-accepted on watch), deliberately ABSENT on the three
tear/ointment pages ("Not thy tears. Not thy ointment." — and LAW 3: those pages carry
real water). Crossing point: equality at F07 ("Seest thou this woman?" — the moment he
SEES her), strictly greater at F08 (the declaration). Stage 3 lands on F09, the sending
page. Hero = F08.

---

## 1. Narration beat map → units (why nine interior pages)

Word counts are my own count of the locked text (sum 240, matching narration.md;
103.29s locked audio ≈ 2.32 words/sec — slower than ep7's 2.70 because the seven
voiced quotes are read at natural speed with pauses). The assembler treats the weights
as proportions, same as every precedent episode.

| Unit | Narration beat | Words | ≈Slot | Voice(s) |
|---|---|---|---|---|
| **front** | "No water for his feet. No kiss. No oil." | 9 | 3.9s | narrator |
| **F01** | "That's what Simon the Pharisee never gave Jesus at his own table. A woman he hadn't invited walked in anyway, and gave him all three." | 25 | 10.8s | narrator |
| **F02** | "A woman in the city, which was a sinner... brought an alabaster box of ointment, and stood at his feet behind him weeping," | 23 | 9.9s | narrator (KJV) |
| **F03** | "and began to wash his feet with tears... and kissed his feet, and anointed them with the ointment." | 18 | 7.8s | narrator (KJV) |
| **F04** | "Simon thought it, not out loud: 'This man, if he were a prophet, would have known... for she is a sinner.' Jesus answered anyway." | 24 | 10.3s | narrator + **simon** |
| **F05** | "A creditor had two debtors — one owed five hundred pence, one fifty. 'When they had nothing to pay, he frankly forgave them both' — frankly, that's freely." | 26 | 11.2s | narrator + **jesus** |
| **F06** | "'Which of them will love him most?' Simon hedged: 'I suppose that he, to whom he forgave most.'" | 18 | 7.8s | **jesus** + narrator + **simon** |
| **F07** | "Jesus turned to her, and asked Simon: 'Seest thou this woman?' Simon had seen the sin. Never the woman." | 19 | 8.2s | narrator + **jesus** |
| **F08** | "'Her sins, which are many, are forgiven; for she loved much: but to whom little is forgiven, the same loveth little.' Forgiven first — love was the receipt, not the price." | 30 | 12.9s | **jesus** + narrator |
| **F09** | "He turned from the parable to her: 'Thy faith hath saved thee; go in peace.' Not thy tears. Not thy ointment. Thy faith." | 23 | 9.9s | narrator + **jesus** |
| **back** | "That answer holds for whoever still carries what Simon called her — a sinner. She came in carrying an alabaster box. She left carrying his peace." | 25 | 10.8s | narrator |

**Why the paragraphs don't map 1:1 (unlike ep7):** three of the five paragraphs are
too long for one page under SW-F1's ~35% frozen-tail cap with a 10s Kling / 8s veo
ceiling — the KJV paragraph (41w ≈ 17.7s), the parable paragraph (68w ≈ 29s), and the
"Seest thou / Her sins" paragraph (40w ≈ 17.2s). Each splits at its own natural
picture-change: standing-behind-weeping → kneeling-kiss-anoint; Simon's thought → the
parable → Simon's hedge; he turns to her → he declares. **Why "Forgiven first — love
was the receipt, not the price" moves onto F08 rather than F09:** it is the narrator's
gloss on F08's own verse (v47) and belongs under that picture; it also brings F09 down
to 23w (a veo 8s clip clears the cap) and F08 up to 30w (Kling 10s, 22% frozen) on the
page that deserves the longest look. **Why the hook splits 9/25 rather than 21/13:**
the front cover's slot under nine words (3.9s) is the Barrel's own 10-word/3.6s
precedent, and F01 — the room's establishing shot and a quadruple debut — needs its
10.8s. **Why not ten:** no remaining beat splits without dropping under ~10 words (a
~4s slot, below any clip's natural length — the Barrel's churn threshold). **Why not
eight:** every candidate merge re-creates one of the over-cap pages above. The story's
beats and the freeze cap agree on nine.

---

## 2. The Stain decision (the hard problem), then the motif arcs

### Where the Stain lives — reasoned, not defaulted

- **On the woman — CHOSEN, and it is exactly what the text gives.** Luke's own
  narrator calls her "a sinner" (v37) and Simon repeats it (v39); the narration's
  landing names it as something CARRIED ("whoever still carries what Simon called
  her — a sinner"). Series sub-case: moral sin/guilt (Isa 1:18, Ps 51:7). Geometry
  follows the two person-attached precedents: the Hem ("around and beneath the
  kneeling woman in the lower-right… reaching across the drawn frame border into the
  bottom-right margin") and Naaman (in the paper beneath the linework on his side,
  crossing the border on that side). It is never on her skin, face, or garments — it
  lies IN the paper under her, so every drawn line passes over it unbroken; it is the
  paper she brought in with her.
- **It travels with her.** Unlike ep7's stain (fixed to an object) this stain moves
  as she moves: at the threshold (F01), standing at the couch-foot (F02), beneath her
  knees (F03–F08). Always the LOWER-RIGHT of the page, always crossing the lower-right
  margin (her side, the door side). Its anchor is her position, which is why she is in
  frame on every interior page — the text never sends her out until v50.
- **On the alabaster box — REJECTED.** Doctrine trap: the narration explicitly
  negates her offering as the cause ("Not thy ointment"). The stain lies beneath HER;
  the flask, when set down (F03 onward), sits on clean paper just outside the stain's
  edge — she is what is stained, not what she brought. The same reasoning bans the
  SWIRL from the box (see the swirl table).
- **Cleared by her tears/kiss/ointment — REJECTED as an event, and actively
  contradicted in the drawing.** This is the exact backwards causality the narration
  was revised four times to avoid. So on F02 and F03 the stain is at full D3 and every
  page states: *the tears and the ointment are in the scene, on his feet; the stain is
  in the paper, beneath her; a band of clean paper stands between them at every point;
  the stain's edge nearest his feet is exactly as saturated as everywhere else —
  neither dried nor spread.* Real water and the paper-stain are different substrates
  AND different zones (LAW 3 applied to sin vs tears). The viewer sees: she wept, she
  poured, nothing about the stain changed.
- **Cleared by his WORD — CHOSEN, in the series' own between-pages grammar.** The
  drying begins on the page turn into F05, the first time forgiveness is SPOKEN ("he
  frankly forgave them both — frankly, that's freely"), and its geometry points the
  cause: the edge nearest Jesus's couch dries first, the wet remainder retreats toward
  the door/margin — it dies from his side outward (ep7's grammar, aimed at a penitent
  instead of a corpse). D2 holds through Simon's hedge (F06) and through "Seest thou"
  (F07), collapses to the dried ring on the turn into F08 (the declaration), and to
  nothing on the turn into F09. The cut is the miracle; no clip ever shows it.
- **"Forgiven first" — how the doctrine survives without deleting the arc.** The
  narration says her love was the receipt, not the price — the forgiveness preceded
  the act. The pictures cannot literally show forgiveness before her tears without
  erasing the stain's arc, so the design encodes the CAUSE correctly instead: the
  stain ignores her tears and ointment entirely (F02/F03 held, stated), and turns only
  at his spoken word. The one further encoding I considered — drawing F01's stain
  already dried on the side facing Jesus ("she came in already turned toward him") —
  I rejected: it costs the D3 peak on the establishing page for a nuance no viewer
  reads without prose. Listed in §8 for the record.
- **The literal layer (Naaman's two-layer pattern):** there is no physical mark on
  her (unlike leprosy). The literal "fact the text names" is SOCIAL — Simon's gaze,
  the guests' hard turned faces, and her posture: on every page she is behind, below,
  at the feet, never once at the table's own level. Simon's own portrait carries the
  blind spot, not malice ("Simon had seen the sin. Never the woman." — his face is
  composed and courteous on every page, never a sneer).

### Stain (sin/guilt, on the woman) — descending

| Page | Dose | Rendering |
|---|---|---|
| F01 | **D3 peak** | Saturated cold grey-umber in the paper beneath and around her where she stands just inside the doorway (lower right), bounded ≤⅓ page, never over any face, crossing the drawn frame border into the lower-right margin; a stated band of clean paper between it and the dry basin, the couch-foot, Jesus's feet, and every other figure |
| F02 | **D3 held** | Same dose, now beneath her standing feet at the couch-foot; unchanged — the tears (in the scene, on his feet) do nothing to it |
| F03 | **D3 held** | Beneath her knees; unchanged in every way; the flask set down on clean paper outside its edge; the edge nearest his feet exactly as wet as the rest |
| F04 | **D3 held** | Beneath her bowed figure at the lower-right corner; unchanged — this is Simon's page: the stain is what he sees |
| F05 | **D2-turning** | Still crossing the lower-right margin, but its whole edge nearest Jesus's couch and feet dried to a pale ring; the wet remainder lies only toward the door — the drying began where the word was spoken |
| F06 | **D2 held** | Unchanged from F05 — Simon's hedge advances nothing |
| F07 | **D2 held** | Unchanged — the equality page (see the crossing note) |
| F08 | **D1** | Only the thin pale dried ring lies in the paper around where she kneels; the paper INSIDE it is the cleanest, brightest cream on the page — she kneels inside "made new"; no border crossing remains but a pale dried trace |
| F09 | **D0** | Canonical absence, stated: no stain, ring, or grey blot anywhere in the paper |

- **The clearing is the cut.** D3→D2t on the turn into F05; D2→D1 into F08; D1→D0
  into F09. Every stain page's animation carries the Hem-validated page-global fence
  ("every stain and mark in the paper is old, dry, and long set… no new stain, spot,
  or darkening appears anywhere") plus "never deepening, never spreading, never
  fading."
- **The stain never lies under Jesus, his couch, his feet, the table, or the
  flask** — stated on every page. **Pareidolia eye-check** on every blot render,
  standing rule.

### Swirl (living blue-gold ink) — rising

| Page | Stage | Anchor |
|---|---|---|
| front | none | Covers carry neither motif (no border for the stain to cross; no prior cover carried the interior dose). The lighting law carries the tension |
| F01 | **0** | Absence stated — Simon's table: no water, no kiss, no oil; nothing living given |
| F02 | **0** | Absence stated — and this page carries REAL WATER (her tears): LAW 3 wants zero blue here |
| F03 | **0** | Absence stated — tears + ointment on the page; "Not thy tears. Not thy ointment." drawn as literal absence of the life-ink on the love-climax page |
| F04 | **1** | Exactly one thread rising from the back of Jesus's right hand, lifted a little from the cushion, palm open toward Simon — "Jesus answered anyway": the life enters with his answer |
| F05 | **1 held** | Same hand, now open in the teller's gesture; same single thread |
| F06 | **1 held** | Same; Simon's page stays quiet on the swirl side |
| F07 | **2** | Jesus turned toward her, his hand extended low and open toward her (clear of his own feet, clear of her): a few threads and one bloom rising UPWARD ONLY from the back of that hand — the dose rises the moment he looks at her |
| F08 | **2 held** | Same anchor — the declaration page stays calm on the swirl side; the D1 ring and her released posture carry it |
| F09 | **3** | Diffused: blue-and-gold threads in one loose open band through the lamplit air of the room above every head, tied to no figure, touching no person, touching neither the flask on the floor nor his anointed feet |
| back | curl | One small hard-capped hooked curl (ep7's "comma/fishhook, never a ring, never a bracelet" wording) rising from the floor stones at the couch-foot WHERE SHE KNELT — beside the flask, never from it |

- **Why the hand, again:** ep7 established (and the user accepted on watch) the
  speaking/touching hand as the least indirect anchor this series has. Here the
  text's own source of the life is his WORD, and the feet — the story's literal site
  — are ruled out for the whole episode: from F03 on they carry ointment sheen and
  tears (real liquid; LAW 3), and a swirl at his mouth is a speech-bubble magnet. The
  hand that answers, tells, asks, and turns to her is the honest anchor and gives
  F04→F08 one continuous root. Fallback if it reads as decoration at F04's first
  render: the air directly above his couch cushion (same zone logic, one line per
  page).
- **Why three Stage-0 pages open the episode** (flagged in §8): the narration
  withholds the life from her act in so many words, and both tear pages carry drawn
  water. The pages are not motif-empty — they carry the Stain at D3. The safe
  fallback, if the user wants blue earlier (the ep2 "swirls missing in the middle"
  instinct), is a Stage 1 thread from Jesus's RESTING hand on the cushion on F02/F03 —
  never from the box, never from the tears — with the hand/feet zones separated by a
  stated band.
- **Why Stage 3 IS reached, and on F09 not F08:** NT fulfilment bodily on-page —
  Jesus forgiving sin in his own voice is the carve-out. F08 carries the D1 ring on
  the most fence-critical render (Stage 3 there = at cap on the hero page); its
  narration is the declaration, still addressed to Simon. F09 is the SENDING — "go in
  peace" — the one line that says the peace is now in the room and leaving with her;
  the wide shot of the whole room is the community image Stage 3 was designed for.
  Stage 3 exactly once.

### High-tide check, every page (`stainDose + swirlStage <= 4`)

| Page | Stain | Swirl | Sum | Note |
|---|---|---|---|---|
| F01 | 3 | 0 | 3 | ✓ |
| F02 | 3 | 0 | 3 | ✓ |
| F03 | 3 | 0 | 3 | ✓ |
| F04 | 3 | 1 | **4** | AT CAP — ep7 F02's proven 3+1 shape; full QUAD lock; the two motifs sit at opposite corners of the frame |
| F05 | 2 | 1 | 3 | ✓ |
| F06 | 2 | 1 | 3 | ✓ |
| F07 | 2 | 2 | **4** | AT CAP — ep7 F04's proven 2+2 shape; full QUAD lock |
| F08 | 1 | 2 | 3 | ✓ |
| F09 | 0 | 3 | 3 | ✓ |

**Crossing point (swirl ≥ stain) = the gospel turn:** equality on F07 — "Seest thou
this woman?" — the first time in the story anyone looks at HER; strictly greater on
F08 — "Her sins… are forgiven." The turn spans the seeing and the declaring, which is
exactly the narration's own argument ("Simon had seen the sin. Never the woman.").
Two at-cap pages, same count as ep7, both flagged as the highest-risk renders.

---

## 3. Refs — who and what needs pinning

All new refs live in this episode folder's `refs/`
(`F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_10_she_loved_much\refs\`).
Chain order is hard (render_still stops on a missing ref).

### Characters

**JESUS** — SERIES CONSTANT. `refs/jesus_ref.png` copied verbatim from episode 7's own
`refs/jesus_ref.png` (itself from ep4/ep1/ep8's approved crop). JESUS_BUILD reused
verbatim from ep7's episode.py:

> Jesus, a Judean man in his early thirties, medium height and ordinary build,
> sun-browned skin, shoulder-length dark brown hair pushed back from his face, a
> short full dark beard, wearing a simple ankle-length robe of undyed cream-brown
> wool with a plain olive-toned mantle draped over one shoulder, a narrow rope belt,
> and flat worn leather sandals -- no halo, no glow, nothing in his dress
> distinguishing him from the men around him, standing square, still, and
> unhurried, his gaze steady and direct

No redesign, no approval cycle. **New per-page guard, every table page (the
"reclining" literalism trap — this episode's "coffin"):** *"reclining on the near
couch on his left side, propped on his left elbow, facing the low table, his sandals
set on the floor, his bare feet extended away from the table past the couch's
foot-end — never seated upright on a chair, never at a high table."* An image model's
prior for "Jesus at a dinner" is a Last-Supper bench-and-table; the whole story
depends on his feet being BEHIND him, reachable from the floor.

**THE WOMAN** — new to the series. Unnamed in the text; the narration calls her only
"a woman… a sinner." Build text (use verbatim):

> the woman of the city, about thirty, olive-skinned, a narrow oval face with high
> cheekbones, large dark heavy-lidded eyes, strong dark brows, a straight nose and a
> full mouth, thick black hair bound back beneath a plain cream head-cloth; wearing
> an ankle-length tunic of faded ochre-cream linen under a deep madder-red woolen
> mantle drawn close about her shoulders and body, full and modest, no jewelry of
> any kind, bare dusty feet

Why: distinct from every series woman so far (the Bier widow — late 40s, grey
mourning veil, rent mantle; the Barrel widow — 30s, famine-thin, grey-brown scarf
with a clay-red band; the Hem woman — gaunt, olive/grey-brown; the John 4 woman —
burnt umber, olive/clay-red). She could afford alabaster ointment, so her cloth is
finer in weave than the village women's but plain in cut. The **madder-red mantle**
is her likeness pin AND the one saturated color in a room of undyed and ochre men —
she is the outsider at a glance — with Isaiah 1:18's "scarlet" sitting quietly
underneath (the Stain's own founding verse). Chromatic reservation: no blue on her;
red is allowed (Naaman's clay-red tunic coexisted with a Stain — the QUAD lock
forbids red only INSIDE the stain; form and substrate keep woven cloth in the scene
apart from formless damage in the paper). **Reverence guards, stated on every page:**
full modest dress, shoulders and back covered, no jewelry, "never a sensual pose" —
the "scarlet woman" cliché is a real render risk and this brief refuses it (§8).
**Hair states (between-pages changes):** bound under the cloth on F01–F02 and again
on F09 (matches the ref); unbound and fallen forward on F03–F08 (v38 "the hairs of
her head", v44 — period-true, and the ref pins the FACE, so the override is a text
line: *"her hair now unbound, fallen forward"*). Refs: `woman_ref.png` (full figure)
+ `woman_face_ref.png` (she has true close framing on F03, F07, F08 and face-study
panels on F08/F09 — full-figure crops are too small to pin a face). Both cropped
from F01 approved, which is why F01 is a MEDIUM shot with her prominent.

**SIMON THE PHARISEE** — new; a different Simon from any Peter elsewhere in this
project. Build text (use verbatim):

> Simon the Pharisee, a man of about fifty-five, thickset and well-fed, an
> olive-skinned broad face with heavy lids, a long straight nose, and a full
> square-trimmed beard streaked iron-grey, dark hair beneath a fine cream linen
> head-cloth; wearing a long wide-sleeved robe of fine undyed white-cream linen, a
> broad cream-and-umber striped woolen mantle with long knotted fringes at its
> corners -- the fringes undyed cream, never blue -- and a wide embroidered sash;
> composed, upright even while reclining, his hands folded, his face courteous and
> closed

Why: maximally distinct from Jesus (young, plain, rope belt, no fringe) and from
every series man (Elijah's shag and staff, Naaman's bronze, Jacob, Nathanael). The
square-trimmed grey beard + the fringed mantle (Matt 23:5's "borders of their
garments") read at any distance and are period-true. The tekhelet BLUE thread a
Pharisee's fringe would carry (Num 15:38) is sacrificed to the motif's chromatic
reservation — stated "never blue" on every page (§8). Not a villain: courteous,
closed, a blind spot — the narration's own register ("Simon had seen the sin. Never
the woman."). Refs: `simon_ref.png` (full figure, reclining) from F01;
`simon_face_ref.png` from F04 — his own close page, shot over Jesus's shoulder so his
face is large (on F01 he is across the table, too small to pin a face).

**THE GUESTS / THE PARABLE FIGURES** — deliberately ref-free. Guests on the far
couches render as unindividuated hatched masses (ep7's bearers/crowd treatment),
faces turned, unfinished. The parable's creditor and two debtors appear ONLY as
hand-studies in F05's panels — no faces, no recurrence, no ref.

### Objects / locations

**THE ALABASTER BOX** — the title object; bookends the episode. Build text (use
verbatim):

> the alabaster box: a small palm-sized flask of pale translucent white-veined
> alabaster stone, a rounded body narrowing to a short neck closed with a small
> stone stopper -- never a square box, never a hinged casket, never a wooden chest,
> never any lid

**The "box" literalism trap (the Barrel's "barrel", the Bier's "bier" — same
family):** KJV "alabaster box" = an alabastron, a stone perfume flask; a model's
prior for "box" is a hinged jewelry casket. Every prompt says "small alabaster flask"
first and carries the never-box/never-casket/never-chest triple verbatim; both covers
append "hinged box, jewelry casket, wooden chest" to their Avoid lists. Captions and
the narration still say "alabaster box" — that is the KJV's word; only the drawing is
corrected. **Two states, between pages:** sealed in her hands (F01, F02, front); open
— its stopper lying beside it — on the floor beside her (F03–F09, back). Luke 7 does
NOT say she broke it (that is Mark 14:3, Bethany — a different event; do not import
"brake the box"). Ref: `alabaster_ref.png` cropped from F01 approved (in her hands,
sealed); the open state is a one-line text override on every later page.

**SIMON'S DINING ROOM** — the location of every interior page. Build text (use
verbatim):

> the dining room of Simon the Pharisee's house: a lamplit room of plastered walls
> washed warm by oil-lamp light, low wooden dining couches with cushions set around
> a low table on three sides, the fourth side open, a tall bronze lamp-stand carrying
> several small burning clay lamps, a doorway open to a dim courtyard; a plain clay
> foot-basin with a folded towel standing DRY beside the doorway, unused

Why: first-century reclining-dinner architecture, plausible for a wealthy Judean
host, and the DRY BASIN is the hook's first sentence made into furniture — it stands
unused by the door on F01, F09, and the back cover (Simon never did give the water).
Ref: `room_ref.png` cropped from F01 approved (couches + table + lamp-stand +
doorway).

### Chain order (hard dependencies)

1. Copy `jesus_ref.png` from episode 7 (immediate, no cycle).
2. **F01** renders with `refs=[R_JESUS]` — woman, Simon, flask, AND room all debut →
   approve → crop `woman_ref`, `woman_face_ref`, `simon_ref`, `alabaster_ref`,
   `room_ref`. *A QUADRUPLE debut on one approval — one more than ep7's triple.
   Unavoidable: the hook IS Simon's table + the uninvited woman + her box. Budget TWO
   regen cycles (§8).*
3. **Front cover** (woman_ref + woman_face_ref + alabaster_ref + room_ref) after F01.
4. **F02, F03** (jesus + woman refs + alabaster + room) any order after F01.
5. **F04** (jesus + simon_ref + woman refs + alabaster + room) → approve → crop
   `simon_face_ref`.
6. **F05–F09** after F04 (all chain simon_face_ref).
7. **Back cover** (alabaster_ref + room_ref, no figures) after F01.

---

## 4. Covers

### The cover judgment call (stated, as the format asks)

The hook's three absences are Simon's table; the landing is the box she left behind.
So the covers are the alabaster box in its two states, at the two ends of the same
room: carried IN across a lit threshold (front), left standing on the floor in an
empty room (back). Jesus appears on neither cover — the front's picture is the
outsider at the door (the room beyond her is warm and blurred with distance), and the
back's empty room says what happened more loudly than his figure would. Series
variety: ep4 led with Jesus, ep5 with its widow, ep7 with the object; ep10 leads with
the woman-carrying-the-object, and lands on the object alone.

### FRONT COVER

- **Scene:** the woman, small and isolated in the lower third, standing on the
  threshold stones of Simon's open doorway seen from behind and a little to one side,
  the sealed alabaster flask held in both hands against her breast, her madder-red
  mantle drawn about her, her head covered, bare feet on the stone; beyond and above
  her through the doorway, the lamplit dining room — the low table, the reclining
  figures on their couches small and unindividuated, the near couch's foot-end
  nearest the door with a pair of bare feet extended toward it, the tall lamp-stand;
  the plain clay foot-basin and folded towel standing dry beside the door-jamb;
  behind her, the dim courtyard and a narrow dusk street between close walls.
- **Lighting (law: ≥1 warm + ≥1 cool):** warm amber lamplight pouring OUT through the
  doorway across the threshold stones and her shoulders; cold blue-grey dusk holding
  the street, the courtyard, and the stone jambs of the door. WHY: the warmth is
  inside a house that has withheld every warm thing; she stands on the exact line
  between cold and warm, about to cross it uninvited.
- **Motif:** none (covers never carry the interior motifs).
- **Title:** `SHE LOVED MUCH` (top) — the locked episode title, KJV 7:47 verbatim
  contiguous. **Subtitle:** `LUKE 7`. **seq_title for all interior pages = `SHE LOVED
  MUCH`** (3 words — shorter than the Bier's 4, no length fallback needed).
- **Refs:** woman_ref + woman_face_ref + alabaster_ref + room_ref (hence F01 approval
  precedes this render).
- **extra_avoid append:** "jewelry, bared shoulders, revealing dress, sensual pose,
  hinged box, jewelry casket, wooden chest, modern clothing".
- **Animation (strong front lock, per the cover doc):** the hem of her mantle stirs
  faintly in the doorway's air; the lamplight inside stays exactly as warm and steady
  as it already is, unchanged; the dusk outside stays exactly as cold and dim as it
  already is; the reclining figures, the basin, and the lamp-stand stay exactly as
  drawn; no new figure, mark, or text appears. `clip_duration=4` (3.9s slot). Freeze
  (slot shorter than clip — the Barrel's own front-cover case).

### BACK COVER

- **Scene:** the same dining room at dawn, empty of every person: the couches bare,
  their cushions pressed, the low table cleared; on the worn floor stones at the
  foot-end of the near couch, the alabaster flask standing open, its small stopper
  lying beside it, a matte trace of spent ointment at its lip, alone; the dry
  foot-basin and folded towel still standing unused beside the doorway; the lamps on
  the stand burned low; the doorway open to a courtyard just catching light. The floor
  where she knelt is bare clean stone. One small hard-capped hooked curl of blue ink
  with a trace of muted gold rises from the floor stones beside the flask — from the
  place where she knelt, not from the flask — its whole visible length no longer than
  a hand's width, curling back toward its own root like a comma or a fishhook WITHOUT
  fully closing into a ring, flat and two-dimensional, drawn ON the paper's surface,
  a single continuous brushstroke, never a ring, never a bracelet, never a bangle,
  never jewelry, never metallic, never reflective, never straightening, never
  trailing, behaving like a small dab of living ink, never a glow.
- **Why this image:** "She came in carrying an alabaster box. She left carrying his
  peace." The thing she carried in is the thing left on the floor; the thing she
  carried out has no picture — so the cover shows the box left behind and the title
  names what she took instead. The curl rises from WHERE SHE KNELT, deliberately
  beside the flask and never from it: the life was in the place of forgiveness, not
  in the ointment ("Not thy ointment"). The dry basin in the doorway light closes the
  hook's own bracket — the water was never given, and it did not matter.
- **Lighting (law):** warm dawn gold low through the doorway across the floor stones,
  the flask, and the couch-foot; cold blue-grey holding the room's far corners, the
  bare far couches, and the burned-low lamp-stand.
- **Title:** `SHE LEFT CARRYING HIS PEACE` (bottom) — the narration's final sentence
  verbatim. Length fallback `CARRYING HIS PEACE` (§8). **Subtitle:** `1 JOHN 4:19` —
  "We love him, because he first loved us": the exact verse of the narration's thesis
  ("Forgiven first — love was the receipt, not the price"), and the NT landing this
  episode's thread points to. Alternative `ISAIAH 1:18` (the Stain's own founding
  verse) in §8.
- **Refs:** alabaster_ref + room_ref.
- **extra_avoid append:** "any human figure, hinged box, jewelry casket, wooden chest,
  jewelry, bright neon".
- **Animation (light back lock, per the cover doc):** fine dust motes drift slowly
  through the dawn shaft in the doorway; the last low lamp flame on the stand wavers
  softly and settles; the blue-gold curl stays exactly as drawn, in place, for the
  whole clip; the dawn light stays exactly as warm and low as it already is,
  unchanged; no new figure, mark, or text appears. `clip_duration=8` (10.8s slot, 26%
  frozen). Freeze (drifting motes — never boomerang).

---

## 5. Page design conventions used below

- Every page: `panel_style="woodcut_hybrid"`, 9:16, `include_no_bubble_clause=True`
  (seven quoted-line captions — the bubble-prior case at its densest).
- **Page geometry law, every interior page:** table at the frame's left; Simon on the
  far couch (upper left / center); Jesus on the near couch, head toward the table,
  bare feet extended toward the LOWER RIGHT; the doorway at the right; THE WOMAN
  ALWAYS AT THE LOWER RIGHT; the stain always crossing the LOWER-RIGHT margin. F03
  closes in on that corner; F04 reverses over Jesus's shoulder but keeps her in the
  lower-right corner. Consistent geography is what lets a nine-page room read as one
  room.
- **Reclining guard** (§3, Jesus) on every table page, plus the same for Simon
  ("reclining on the far couch, propped on his elbow").
- **Standing steady-line override (the no-Fray guard):** every page states *"her
  contour drawn steady and single-struck, no doubled or tremored line anywhere in her
  figure"* — she weeps on three pages; accidental fray here is a canon error, not a
  style wobble.
- **Reverence guards** on every page she is on (§3) — and the kiss (F03 main, F07
  panel 2) is drawn as ALREADY MADE, her face hidden by her fallen hair, her lips at
  his instep; never animated, never sensual.
- **Liquid discipline (LAW 3 for tears and ointment):** the tears are drawn as wet
  tracks on her cheeks and a few fallen drops on his feet; the ointment as a matte
  sheen on his feet — both IN THE SCENE, on HIS side; the stain IN THE PAPER on HER
  side; a stated clean-paper band between; no blue on F01–F03 at all; from F04 the
  swirl anchors to his HAND, upward only, never toward the feet.
- **NO_MOUTH** to the owner of each page's voiced line: Simon on F04 ("not out loud"
  — the text hands us the clause); Jesus on F05, F07, F08, F09; BOTH on F06.
- **Kling + 2-line captions = the documented OpenArt failure combo** (ep7 F04: 3/3
  speech-bubble tails; swirls_page.py warns on it). Every Kling page below carries a
  ONE-line caption; only veo pages (F02, F09) stack two lines.
- Captions are verbatim contiguous fragments of the locked narration (KJV lines
  included), ≤4 words per line except one collapsed 5-word line where noted (ep7
  F04's own precedent); panel labels are 2–3 authored words; corner notes short.
- Main-scene prose below is design intent at near-final density (PageSpec
  `main_scene_still` register). Sonnet writes the template prompts — keeping every
  MUST-SHOW, dosage, separation, never-X, reclining, reverence, and steady-line
  clause — and, per LAW 4, the final animation prompt against the RENDERED still's
  actual pixels.
- Model lanes per the north-star tiering: Kling3.0 pro where a designed gesture must
  COMPLETE mid-clip; veo3_1_lite for holds/ambient pages. Stated per page with its
  why. Under the OpenArt bridge (no veo model) the tier is advisory — see §7.

---

## 6. Page-by-page

### F01 — "at his own table" (25w · Stain **D3 peak** · Swirl 0 · veo3_1_lite, clip 8)

The room's establishing shot and the Stain's debut — the three absences as furniture,
and the uninvited woman just inside the door. Quadruple-debut page (woman, Simon,
flask, room → five crops); MEDIUM shot with her prominent so her face crops clean.

- **Panels** *(the three absences, rhymed by F07's three gifts)*
  1. `"no water"` — the plain clay foot-basin and folded towel standing dry beside a
     doorway, unused *(the hook's first sentence as an object)*.
  2. `"no kiss"` — the open doorway of a house from inside, its threshold stones
     empty, no host standing in it to greet anyone *(the greeting never given)*.
  3. `"no oil"` — a small stoppered oil flask on a high wall-shelf, out of reach,
     dusty *(the anointing never offered)*.
- **Main scene** — `MEDIUM shot`:
  > the lamplit dining room (ROOM_BUILD), the low table at the frame's left, fully
  > inside the frame. {JESUS_BUILD}, reclining on the near couch on his left side,
  > propped on his left elbow, facing the low table, his sandals set on the floor,
  > his bare feet dusty and unwashed, extended away from the table past the couch's
  > foot-end toward the lower right — never seated upright on a chair, never at a
  > high table — fully inside the frame; {SIMON_BUILD}, reclining on the far couch
  > across the table, propped on his elbow, his head turned toward the doorway,
  > composed; two or three other guests on the far couches as unindividuated hatched
  > figures in undyed and ochre wool, faces turned toward the door, none finished.
  > At the right, just inside the doorway, stopped: {WOMAN_BUILD}, her hair bound
  > under the cloth, the sealed alabaster flask (ALABASTER_BUILD) held in both hands
  > against her breast, fully inside the frame, her eyes on Jesus's feet, her dress
  > full and modest, never a sensual pose; her contour drawn steady and
  > single-struck, no doubled or tremored line anywhere in her figure; the dry
  > foot-basin and folded towel by the door-jamb between her and the couch-foot,
  > fully inside the frame. A cold grey-umber stain lies in the paper itself beneath
  > and around where she stands, formless and matte, lying beneath the linework so
  > every drawn line passes over it unbroken, its feathered damp edge crossing the
  > drawn frame border into the page's own lower-right margin directly below her,
  > never over any face, bounded to less than a third of the page; a band of clean
  > paper between the stain and the basin, the couch-foot, Jesus's feet, and every
  > other figure; the stain nowhere near Jesus and never beneath his couch. Stage 0
  > dosage: no blue Swirls of Life ink motif anywhere on this page — no blue ink
  > appears anywhere in the scene, the panels, or the margins.
- **material_closer:** "the cold stain lying in the paper beneath the woman at the
  door is the only unusual ink at work on this page, and no blue appears anywhere."
- **Fence:** `stain` — "the cold grey-umber stain in the paper beneath the woman at
  the door"
- **Caption:** `("at his own table",)` *(narration verbatim, 4 words)* · **Corner
  note:** `NOTE: not invited`
- **Panel motions:** (1) the light across the dry basin warms very slightly and
  settles *(vessel — tone-only, the loaded prior)*; (2) a thin haze of lamp-smoke
  drifts across the empty doorway; (3) the shelf flask sits undisturbed, exactly as
  drawn.
- **Main animation:** the woman stands still just inside the door, one slow breath,
  her mantle settling from her walk and stilling; Simon's turned head stays turned,
  still; Jesus stays exactly as drawn, one slow breath, his face toward the table,
  his feet completely still; the guests hold; the lamp flames on the stand waver
  softly; the cold stain in the paper stays exactly as drawn, never deepening, never
  spreading, never fading.
- **Why veo:** all holds plus ambient, no completing gesture — the cheapest tier on
  the page most likely to need likeness regens (five crops ride on it).
  `refs=[R_JESUS]`.

### F02 — "stood at his feet behind him weeping" (23w · Stain D3 held · Swirl 0 · veo3_1_lite, clip 8)

She has crossed the room and stands where no guest stands — at the foot of his couch,
behind his back. The tears begin; the stain does not move.

- **Panels**
  1. `"in the city"` — a narrow dusk street between close house walls, empty *(the
     text's own phrase — where she came from; no figure)*.
  2. `"alabaster"` — a close object study of the sealed flask, pale veined stone, its
     small stopper.
  3. `"behind him"` — the back of Jesus's head and one shoulder as he reclines, seen
     from behind, close *(her view of him — he has not turned)*.
- **Main scene** — `MEDIUM shot` from the couch-foot side:
  > {WOMAN_BUILD}, standing at the foot-end of Jesus's couch, behind him, fully
  > inside the frame, her head bowed, wet tear-tracks on her cheeks, the sealed
  > alabaster flask held low in both hands, her hair still bound under the cloth,
  > her dress full and modest; her contour drawn steady and single-struck, no
  > doubled or tremored line anywhere in her figure. {JESUS_BUILD}, reclining on the
  > near couch on his left side, propped on his left elbow, his head and torso
  > toward the table, his face NOT turned toward her; his bare feet extended toward
  > her on the couch-end, fully inside the frame, a few fallen tear-drops on them.
  > Beyond, the low table, {SIMON_BUILD} watching from the far couch, the guests as
  > hatched masses. The same cold grey-umber stain lies in the paper beneath her
  > standing feet, still crossing the drawn frame border into the lower-right
  > margin, unchanged in every way from before; the tears are in the scene, on his
  > feet; the stain is in the paper, beneath her; a band of clean paper between them
  > at every point; the stain nowhere near his feet or his couch, never over any
  > face. Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page —
  > the only water on this page is her tears, drawn plainly in the scene, and no
  > blue ink appears anywhere in the scene, the panels, or the margins.
- **material_closer:** "the cold stain in the paper beneath her is the only unusual
  ink at work on this page; her tears are plain drawn water, and no blue appears
  anywhere."
- **Fence:** `stain` — "the cold grey-umber stain in the paper beneath the woman's
  feet"
- **Caption:** `("stood at his feet", "behind him weeping")` *(KJV 7:38 verbatim
  contiguous, 4+3; veo page — two lines OK)* · **Corner note:** `NOTE: behind him`
- **Panel motions:** (1) a thin haze drifts along the empty dusk street; (2) the
  flask study holds, the light across it warming very slightly; (3) the sketched
  shoulder holds, still.
- **Main animation:** the woman's shoulders tremble with weeping and settle, her head
  staying bowed, her lips closed; the wet tracks on her cheeks stay as they are;
  Jesus stays exactly as drawn, his face toward the table, one slow breath, his feet
  completely still; Simon and the guests hold; the lamp flames waver; the cold stain
  in the paper stays exactly as drawn, never deepening, never spreading, never
  fading.
- **Why veo:** a tremble-and-hold, no cued gesture; Stage 0 means the water on the
  page has no ink to be confused with. **Refs:** jesus + woman_ref + woman_face_ref +
  alabaster_ref + room_ref.

### F03 — "and kissed his feet" (18w · Stain **D3 held — the load-bearing hold** · Swirl 0 · kling3_0, clip 7)

The climax of her love — and the page that proves the doctrine by NOT changing the
stain. The most render-fragile composition in the episode (hair on feet; reverence),
so the animation ask is the smallest (LAW 0.6).

- **Panels**
  1. `"with tears"` — close on a bare foot's instep with a few fallen drops on it.
  2. `"her hair loosed"` — her plain head-cloth lying discarded on the floor stones
     *(the unbinding, told by the object)*.
  3. `"the ointment"` — the flask now open on the floor stones, its stopper lying
     beside it.
- **Main scene** — `CLOSE MEDIUM shot`, low, at the couch-foot:
  > {WOMAN_BUILD}, kneeling on the floor at his feet, fully inside the frame, her
  > hair now unbound and fallen forward, its ends drawn across his wet feet, her
  > head bowed low over them so that her face is turned down and mostly hidden by
  > her hair, her lips at his instep — the kiss already made, reverent; her red
  > mantle covering her shoulders and back, her dress full and modest, never a
  > sensual pose; her contour drawn steady and single-struck, no doubled or tremored
  > line anywhere in her figure; the open alabaster flask in one hand, tilted, its
  > stopper lying on the floor stones, a matte sheen of ointment on his feet. His
  > bare feet fully inside the frame on the couch-end, the lower hem of his plain
  > cream robe and the wooden foot of the couch visible, his face out of frame. The
  > cold grey-umber stain lies in the paper beneath her knees and the floor around
  > them, crossing the drawn frame border into the lower-right margin, EXACTLY as
  > before — its edge nearest his feet as saturated as everywhere else, neither
  > dried nor spread; the tears and the ointment are in the scene, on his feet; the
  > stain is in the paper, beneath her; a band of clean paper between them at every
  > point; the open flask and its stopper standing on clean paper outside the
  > stain's edge; never over any face. Stage 0 dosage: no blue Swirls of Life ink
  > motif anywhere on this page — no blue ink appears anywhere in the scene, the
  > panels, or the margins.
- **material_closer:** "the unchanged cold stain in the paper beneath her knees is
  the only unusual ink at work on this page; the tears and ointment are plain drawn
  liquid on his feet, and no blue appears anywhere."
- **Fence:** `stain` — "the cold grey-umber stain in the paper beneath the woman's
  knees"
- **Caption:** `("and kissed his feet",)` *(KJV 7:38 verbatim contiguous, 4 — one
  line, Kling page)* · **Corner note:** `NOTE: stain unchanged` *(the page's whole
  design in two words — the Hem's own "stain in paper" register)*
- **Panel motions:** (1) the drops on the instep hold, the light across them warming
  very slightly; (2) the fallen head-cloth lies undisturbed; (3) the open flask sits
  still, exactly as drawn.
- **Main animation:** her shoulders shake once with a sob and still; her hands hold
  the tilted flask exactly as drawn, not moving; her hair lies still across his
  feet; his feet stay completely still; her lips stay closed against his instep, her
  mouth not moving; the cold stain in the paper stays exactly as drawn, never
  deepening, never spreading, never fading.
- **Why kling, and why the smallest ask:** the sob is the one completing gesture
  (Kling's lane); everything else is fenced — a fragile composition gets the smallest
  ask, never a compensating bigger one. **Refs:** jesus + woman_ref + woman_face_ref
  + alabaster_ref + room_ref.

### F04 — "she is a sinner" (24w · Stain D3 held + **Swirl 1 first trace** = 4, AT CAP · veo3_1_lite, clip 8)

Simon's page — the thought he never spoke — and the first blue of the episode,
entering with "Jesus answered anyway." Camera reversed over Jesus's shoulder so
Simon's face is large: the crop source for `simon_face_ref`. First of the two at-cap
pages: full QUAD lock.

- **Panels**
  1. `"a prophet"` — a small robed figure far off on a bare hill, staff in hand *(the
     prophet Simon has decided Jesus is not)*.
  2. `"the guests"` — two or three guests' faces on a far couch turned toward the
     lower corner, hard, unfinished *(the room's verdict)*.
  3. `"answered anyway"` — Jesus's right hand lifted a little from a cushion, palm
     open, close *(the hand the thread rises from — partial main-scene element)*.
- **Main scene** — `MEDIUM TWO-SHOT` over Jesus's near shoulder across the table:
  > {SIMON_BUILD}, reclining on the far couch propped on his elbow, largest in the
  > frame, fully inside the frame, his face turned toward the lower right, his brow
  > drawn down, his mouth SHUT, composed and cold, courteous and closed, never a
  > sneer; {JESUS_BUILD} in the near foreground, reclining on the near couch on his
  > left side, his shoulder and the side of his face visible, his gaze on Simon,
  > calm, his right hand lifted a little from the cushion, palm open toward Simon,
  > already raised, not touching anything, fully inside the frame; at the lower-right
  > corner of the frame, {WOMAN_BUILD}'s bowed figure — her hair unbound and fallen
  > forward, her red mantle, the open alabaster flask on the floor beside her on
  > clean paper — her contour drawn steady and single-struck, no doubled or tremored
  > line anywhere in her figure. The cold grey-umber stain lies in the paper beneath
  > her at the lower-right corner, crossing the drawn frame border into the
  > lower-right margin, unchanged, never over any face, nowhere near Jesus or Simon
  > and never beneath either couch. Stage 1 dosage: exactly one restrained thread of
  > blue ink curling up from the back of Jesus's lifted right hand, touching only his
  > hand and the air just above it, the only blue on the whole page, behaving like
  > one stroke of wet ink bled into the paper, smooth and open in its curl, never
  > blot-shaped; the stain formless and matte, never swirl-shaped; a wide band of
  > untouched clean paper between the thread and the stain at every point (they sit
  > at opposite corners of the frame); the thread drawn ON the page's surface, the
  > stain lying IN the paper beneath the linework.
- **material_closer:** "the cold stain in the paper beneath the woman and the single
  blue thread at his hand are the only two kinds of unusual ink at work on this page,
  kept apart by clean paper."
- **Fence:** `stain` — "the cold grey-umber stain in the paper beneath the woman and
  the single blue thread at his lifted hand"
- **Caption:** `("she is a sinner",)` *(KJV 7:39 verbatim contiguous, Simon's voiced
  line, 4)* · **Corner note:** `NOTE: not out loud`
- **Panel motions:** (1) a faint heat-shimmer plays over the far hill; (2) the
  sketched faces hold, the light across them warming very slightly *(tone-only —
  small sketched faces morph under content asks)*; (3) the lifted hand holds, still.
- **Main animation:** Simon's jaw sets and his eyes narrow a fraction and hold, his
  lips staying closed and completely still — he is not speaking and his mouth does
  not move at all; Jesus stays exactly as drawn, his lifted hand not rising further
  and not reaching toward anything, one slow breath; the woman's bowed head stays
  bowed; the single thin blue ink thread at his hand stays exactly as drawn, in
  place, for the whole clip; the cold stain in the paper stays exactly as drawn,
  never deepening, never spreading, never fading.
- **Why veo:** near-holds and one expression tightening (veo's softening lane — ep5
  F05's crowd-hardening precedent); the Stage 1 thread is held still per the
  north-star table; the cheaper tier on an at-cap page that may need a QUAD-lock
  regen. **Refs:** jesus + simon_ref + woman_ref + woman_face_ref + alabaster_ref +
  room_ref → approve → crop `simon_face_ref`.

### F05 — "he frankly forgave them both" (26w · Stain **D2-turning** · Swirl 1 held · kling3_0, clip 10)

The parable page. The parable itself lives in the three woodcut panels — the
"sharper cinematic cuts" the hybrid style is for — as three hand-studies, no faces,
no refs; the main scene stays at the table so she is on-page to hear it. The stain
turns HERE: the first spoken forgiveness.

- **Panels** *(the parable triptych)*
  1. `"five hundred pence"` — a ringed, well-kept hand holding a large empty purse
     upside-down over a table, nothing falling from it.
  2. `"fifty"` — a rough, work-worn hand holding a small empty purse likewise turned
     out, nothing falling.
  3. `"forgave them both"` — a creditor's two open hands, palms up and empty, over
     the same table — releasing *(no coins anywhere on any of the three panels:
     "they had nothing to pay")*.
- **Main scene** — `MEDIUM shot` at the table:
  > {JESUS_BUILD}, reclining on the near couch on his left side, propped on his left
  > elbow, his face toward Simon, calm, his right hand now open in a teller's
  > gesture — already lifted, not touching anything — fully inside the frame;
  > {SIMON_BUILD}, reclining on the far couch across the table, listening, composed
  > and guarded, his hands folded, fully inside the frame; at the lower right,
  > {WOMAN_BUILD}, her hair unbound and fallen forward, kneeling at his feet, her
  > head bowed but lifted a little — listening — her dress full and modest, her
  > contour drawn steady and single-struck, no doubled or tremored line anywhere in
  > her figure; the open alabaster flask on the floor beside her on clean paper; his
  > bare feet on the couch-end with the matte ointment sheen, fully inside the frame.
  > The cold grey-umber stain in the paper beneath her knees still crosses the drawn
  > frame border into the lower-right margin on the door side, never over any face —
  > but its whole edge nearest Jesus's couch and feet has dried to a pale ring, the
  > wet remainder lying only toward the door and the margin, away from him; no stain
  > anywhere near Jesus, his couch, or his feet. Stage 1 dosage, held: the same
  > single restrained thread of blue ink rising from the back of his open right hand,
  > touching only his hand and the air above it, the only blue on the whole page,
  > behaving like one stroke of wet ink bled into the paper, smooth and open, never
  > blot-shaped; the stain formless and matte, never swirl-shaped; a wide band of
  > untouched clean paper between the thread and the stain's wet remainder at every
  > point; the thread drawn ON the page, the stain lying IN the paper beneath the
  > linework.
- **material_closer:** "the stain drying back from his side and the single blue
  thread at his hand are the only two kinds of unusual ink at work on this page,
  kept apart by clean paper."
- **Fence:** `stain` — "the cold grey-umber stain beneath the woman, its dried pale
  edge, and the single blue thread at his hand"
- **Caption:** `("forgave them both",)` *(KJV 7:42 verbatim contiguous, 3 — one
  line, Kling page; the full "he frankly forgave" is the beat text)* · **Corner
  note:** `NOTE: that's freely` *(narration verbatim)*
- **Panel motions:** (1) the upturned purse holds, nothing falling; (2) the small
  purse holds, nothing falling; (3) the open hands hold, the light across them
  warming very slightly.
- **Main animation:** the woman's bowed head lifts a fraction as she listens and
  holds, her eyes staying down; Jesus stays exactly as drawn, his open hand not
  moving further, one slow breath, his lips staying closed and completely still — he
  is not speaking and his mouth does not move at all; Simon holds, one breath; the
  lamp flames waver; the single thin blue ink thread at his hand stays exactly as
  drawn, in place, for the whole clip; the stain and its dried pale edge stay
  exactly as drawn, never deepening, never spreading, never fading.
- **Why kling:** her head-lift is the page's one human event — she hears "forgave" —
  a completing gesture; and the 11.2s slot wants the 10s clip (11% frozen) rather
  than veo's 8s (29%). **Refs:** jesus + simon_ref + simon_face_ref + woman_ref +
  woman_face_ref + alabaster_ref + room_ref.

### F06 — "Which of them will love him most?" (18w · Stain D2 held · Swirl 1 held · kling3_0, clip 7)

Simon's hedge. Deliberately the stillest middle page — nothing advances on either
motif; the one human thing is a grudging half-nod.

- **Panels**
  1. `"two debtors"` — two small figures walking away from a counting-house door
     side by side, one in fine dress, one in rags, seen from behind.
  2. `"I suppose"` — Simon's hand, palm half-turned outward in a reluctant
     concession, close *(hand only — no face ref needed for the panel)*.
  3. `"the most"` — the woman's hand laid flat on Jesus's bare foot, close, the
     matte sheen on it *(the living answer to the question — partial main-scene
     element)*.
- **Main scene** — `MEDIUM TWO-SHOT` across the table:
  > {SIMON_BUILD}, reclining on the far couch propped on his elbow, his face
  > half-turned away, eyes down, his chin just beginning to dip, fully inside the
  > frame; {JESUS_BUILD}, reclining on the near couch on his left side, his face on
  > Simon, patient, his open right hand exactly as before, already lifted, fully
  > inside the frame; at the lower right, {WOMAN_BUILD}, her hair unbound, bowed at
  > his feet, her dress full and modest, her contour drawn steady and
  > single-struck, no doubled or tremored line anywhere in her figure; the open
  > flask on clean paper beside her; his feet on the couch-end, fully inside the
  > frame. The cold grey-umber stain in the paper beneath her knees exactly as
  > before — its edge nearest Jesus's couch dried to a pale ring, the wet remainder
  > lying only toward the door and still crossing the lower-right margin, never
  > over any face, nowhere near either couch. Stage 1 dosage, held: the same single
  > thread of blue ink from the back of his open hand, touching only his hand and
  > the air above it, the only blue on the page; QUAD lock as F05; a wide band of
  > clean paper between thread and stain at every point.
- **material_closer:** as F05.
- **Fence:** `stain` — as F05.
- **Caption:** `("will love him most",)` *(KJV 7:42 verbatim contiguous, Jesus's
  voiced line, 4 — one line, Kling page)* · **Corner note:** `NOTE: he hedged`
- **Panel motions:** (1) the two far figures hold their walk, unmoving; (2) the
  half-turned hand holds; (3) the hand on the foot holds, the light across it
  warming very slightly.
- **Main animation:** Simon's grudging half-nod completes — his chin dips once and
  holds, his eyes never meeting Jesus's, his lips staying closed and completely
  still, not speaking; Jesus stays exactly as drawn, one slow breath, his lips also
  closed and completely still — not speaking; the woman holds exactly as drawn; the
  single thin blue ink thread stays exactly as drawn, in place; the stain and its
  dried edge stay exactly as drawn, never deepening, never spreading, never fading.
- **Why kling:** the nod must complete mid-clip. **Refs:** as F05.

### F07 — "Seest thou this woman?" (19w · Stain D2 held + **Swirl 2** = 4, AT CAP · kling3_0, clip 7)

The crossing point. Jesus has TURNED (v44 — drawn as already turned) and looks at
her; she is seen for the first time in the episode. Panels rhyme F01's absences with
her three gifts. Second at-cap page: full QUAD lock.

- **Panels** *(the three gifts)*
  1. `"the water"` — tear-drops on a bare instep, close *(rhymes F01's dry basin)*.
  2. `"the kiss"` — her bowed profile at his instep, her face hidden by her fallen
     hair, close *(reverent; tiny face → tone-only motion; rhymes F01's empty
     threshold)*.
  3. `"the oil"` — the open flask on the floor stones, stopper beside it *(rhymes
     F01's shelf flask)*.
- **Main scene** — `MEDIUM shot`:
  > {JESUS_BUILD}, reclining on the near couch on his left side but turned back
  > toward the couch-foot, his torso and face toward the woman, his right hand
  > extended low and open toward her over the couch's side at couch height — a
  > hand's width clear of his own feet and clear of her, touching nothing — fully
  > inside the frame; {WOMAN_BUILD}, kneeling at his feet, her hair unbound and
  > fallen forward, her face lifted to his, wet, her eyes meeting his, her dress
  > full and modest, her contour drawn steady and single-struck, no doubled or
  > tremored line anywhere in her figure, fully inside the frame; {SIMON_BUILD}
  > beyond on the far couch, his gaze on JESUS, not on her; his bare feet on the
  > couch-end with the matte ointment sheen, fully inside the frame; the open flask
  > on clean paper beside her. The cold grey-umber stain in the paper beneath her
  > knees exactly as before — its edge nearest Jesus dried to a pale ring, the wet
  > remainder toward the door and the lower-right margin, never over any face,
  > nowhere near Jesus. Stage 2 dosage: the blue ink motif quietly present — a few
  > soft blue threads rising UPWARD ONLY from the back of his extended hand into the
  > air above it, every thread's root touching his hand directly and going up from
  > there, none descending toward his feet, the floor, or her, none dripping, none
  > pooling; at the top of the threads, one soft, irregular, hazy patch of the same
  > blue pigment, entirely amorphous, with soft feathered edges and no internal
  > structure of any kind, exactly like a single drop of watercolor spreading into
  > wet paper, completely without symmetry or distinct segments, touching only his
  > hand and the air above it, touching no other person and nothing else on the
  > page; the floor and his feet free of any ink of any kind; every thread behaving
  > like wet ink bled into the paper, smooth and open, never blot-shaped; the stain
  > formless and matte, never swirl-shaped; a wide band of untouched clean paper
  > between the threads and the stain at every point; the threads drawn ON the
  > page, the stain lying IN the paper beneath the linework.
- **material_closer:** "the stain drying back from his side and the soft blue
  threads at his extended hand are the only two kinds of unusual ink at work on
  this page, kept apart by clean paper."
- **Fence:** `stain` — "the cold grey-umber stain beneath the woman, its dried pale
  edge, and the blue threads at his extended hand"
- **Caption:** `("Seest thou this woman?",)` *(KJV 7:44 verbatim, 4 — one line)* ·
  **Corner note:** `NOTE: he saw her`
- **Panel motions:** (1) the drops hold, the light warming very slightly; (2) the
  sketched profile holds, tone-only; (3) the flask sits still.
- **Main animation:** the woman's eyes lift the last small distance to his and one
  full blink — closes, then opens again fully, ending wide open on him; Jesus stays
  exactly as drawn, his extended hand not moving further, one slow breath, his lips
  closed and completely still — he is not speaking and his mouth does not move at
  all; Simon's gaze stays on Jesus, never turning to her; the soft blue threads at
  his hand drift gently within their own small area, never lowering toward the
  floor or his feet; the stain and its dried edge stay exactly as drawn, never
  deepening, never spreading, never fading.
- **Why kling:** the full-arc blink (veo never attempts the close). **Refs:** as F05.

### F08 — HERO — "Her sins, which are many, are forgiven" (30w · Stain **D1** · Swirl 2 held · kling3_0, clip 10)

The declaration and the episode's gospel pivot. The stain is gone between F07 and
F08 — at his word — leaving only the ring; she kneels inside the cleanest paper on
the page. Longest interior slot (12.9s).

- **Panels**
  1. `"the receipt"` — a small wax tablet, its surface scraped smooth and BLANK,
     lying on a table *(the narration's own metaphor; blank so no text is invented)*.
  2. `"her face"` — a close study of her tear-streaked face, lifted, at rest, eyes
     open, contour steady *(woman_face_ref)*.
  3. `"loveth little"` — a stiff figure reclining alone at a table's far end, small,
     an untouched cup before him *(KJV 7:47's own last clause, drawn as a type — not
     Simon's likeness)*.
- **Main scene** — `MEDIUM shot`:
  > {JESUS_BUILD}, reclining on the near couch, turned fully toward her, his face on
  > her, calm and kind, his right hand open toward her as before, fully inside the
  > frame; {WOMAN_BUILD}, risen tall on her knees at his feet, her face lifted to
  > his, her hands open at her sides, her hair unbound, her dress full and modest,
  > her contour drawn steady and single-struck, no doubled or tremored line anywhere
  > in her figure, fully inside the frame; the open alabaster flask on the floor
  > beside her, outside the ring; {SIMON_BUILD} beyond on the far couch, his face at
  > last turned toward HER, unreadable; the guests as hatched masses; his bare feet
  > on the couch-end, fully inside the frame. Of the cold stain, nothing wet remains
  > anywhere: only a thin, faint, pale dried watermark ring lies in the paper around
  > where she kneels — the dried edge of the old stain, the stain itself gone — and
  > the paper inside that ring is the cleanest, brightest cream on the whole page;
  > no border crossing remains but a pale dried trace; the ring contains no blue, no
  > gold, and no red, and touches no figure's drawn line. Stage 2 dosage, held: a
  > few soft blue threads rising UPWARD ONLY from the back of his open hand into the
  > air above it, their roots touching his hand and nowhere else, one soft amorphous
  > watercolor patch at their top (as F07), touching only his hand and the air; a
  > band of clean paper between the threads and the dried ring.
- **material_closer:** "the dried pale ring in the paper and the soft blue threads
  at his hand are the only two kinds of unusual mark on this page, and the paper
  inside the ring is the cleanest on it."
- **Fence:** `stain` — "the dried pale ring in the paper around where the woman
  kneels"
- **Caption:** `("which are many, are forgiven",)` *(KJV 7:47 verbatim contiguous,
  5 — one collapsed line, Kling page, ep7 F04's "I say unto thee, Arise" length
  precedent. NOT "for she loved much": that caption over a just-cleared stain would
  read as the backwards causality this whole design exists to avoid)* · **Corner
  note:** `NOTE: forgiven first` *(narration verbatim — the doctrine in two words)*
- **Panel motions:** (1) the blank tablet lies undisturbed; (2) the sketched face
  blinks once fully — closes, then opens again, ending wide open; (3) the stiff
  figure holds.
- **Main animation (the Hem F05 recipe, tuned to this beat):** Jesus's one small
  kind nod completes and holds, his lips staying closed and completely still — he
  is not speaking and his mouth does not move at all; the woman takes one slow deep
  breath and her shoulders drop and release as the weight visibly leaves her, then
  hold; Simon's turned face stays turned toward her, still; the lamp flames waver;
  the soft blue threads at his hand drift gently within their own small area, never
  lowering; the dried pale ring stays exactly as drawn, and no new stain, spot, or
  darkening appears anywhere on the page at any point.
- **Why kling:** two completing gestures (the nod, the shoulder-release); the 10s
  clip fills the 12.9s slot at 22% frozen. **Why hero:** the gospel-pivot sentence,
  Christ bodily declaring forgiveness, all three principals in one frame with the
  stain cleared AT HIS WORD — not the emotional climax (F03), exactly as the locked
  rule asks. In this Swirls pipeline the covers bookend the cut; F08 is the hero
  still for any thumbnail / hero-bookend use. Alternate: F07. **Refs:** as F05.

### F09 — "Thy faith hath saved thee" (23w · Stain **D0** · **Swirl 3** · veo3_1_lite, clip 8)

The sending. She has risen; the flask is left on the floor; the peace is in the
room's air. The episode's one Stage 3 page.

- **Panels**
  1. `"not thy tears"` — a close study of her face, tears dried, at peace
     *(woman_face_ref; label echoes the narration)*.
  2. `"not thy ointment"` — the open flask standing alone on the floor stones.
  3. `"go in peace"` — the open doorway from inside, its threshold clear, a
     dawn-grey courtyard beyond *(KJV 7:50 — her way out)*.
- **Main scene** — `WIDE shot`, the whole room:
  > the lamplit dining room (ROOM_BUILD) fully inside the frame. {WOMAN_BUILD},
  > standing risen at the couch-foot, facing the doorway at the right, at rest, her
  > hair bound back beneath her re-settled head-cloth, her mantle drawn about her,
  > her hands empty and open at her sides, her dress full and modest, her contour
  > drawn steady and single-struck, no doubled or tremored line anywhere in her
  > figure, fully inside the frame; {JESUS_BUILD}, half-risen on his left elbow on
  > the near couch, his right hand open toward her in sending, his face on her,
  > fully inside the frame; {SIMON_BUILD} on the far couch, the guests as hatched
  > masses; the open alabaster flask left on the floor at the couch-foot behind her,
  > fully inside the frame; the dry foot-basin and folded towel still standing
  > unused by the door. No stain, ring, or grey blot anywhere in the paper — the
  > paper wholly clean. Stage 3 dosage: the blue ink motif, with traces of muted
  > gold, is woven through the whole scene — threads drifting in one loose open
  > band through the lamplit air of the room above every head, tied to no single
  > figure, touching no person, touching neither the flask on the floor nor his
  > feet, behaving like wet ink bled through the page's own wash, never a glow.
- **material_closer:** "the blue-and-gold band woven through the air of the room is
  the only unusual ink on the page, and the paper beneath it is wholly clean."
- **Fence:** `none` *(D0 — the page-global no-new-stain clause is still stated)*
- **Caption:** `("Thy faith hath", "saved thee")` *(KJV 7:50 verbatim contiguous,
  3+2; veo page — two lines OK; "go in peace" is carried by panel 3's label)* ·
  **Corner note:** `NOTE: she left it` *(the flask — plants the back cover)*
- **Panel motions:** (1) the sketched face holds, the light warming very slightly;
  (2) the flask sits still; (3) a thin haze drifts across the courtyard beyond the
  door.
- **Main animation:** the woman's empty hands open a little further at her sides and
  settle; her chest rises once in a slow breath, her face toward the door; Jesus
  stays exactly as drawn, his open hand not moving, one slow breath, his lips closed
  and completely still — not speaking; Simon and the guests hold; the flask sits
  still on the floor; the blue-and-gold ink threads drift smoothly within their own
  fixed band across the air above every head, never lowering onto any figure; the
  lamp flames waver; no new stain, spot, or darkening appears anywhere on the page
  at any point.
- **Why veo (and why she HOLDS rather than walks):** all holds plus fixed-band drift
  is veo's exact lane (ep7 F06's Stage 3 band was veo); a walk to the door under an
  8s clip would either reverse under any fill or need Kling, where a Stage 3 band
  over-escalates. "Go in peace" is received here; the going belongs to the page
  turn. Positive-only light wording throughout (no glint/sparkle). **Refs:** jesus +
  simon_ref + simon_face_ref + woman_ref + woman_face_ref + alabaster_ref + room_ref.

---

## 7. Assembly suggestions (word-proportional, Fable estimates)

240 words over 103.29s ≈ 2.32 words/sec (the voiced quotes run slower with pauses —
proportions are approximate as always). **Boomerang nowhere in this episode**: every
unit either settles a completing gesture, drifts a band/motes, or wavers lamp flames
— all of which read backwards under reversal. Every clip is designed shorter than its
slot (freeze pads, never trims — the standing swirls-freeze lesson); every frozen
tail is under SW-F1's 35%. Final modes are an assembly-QC call on the real renders —
real playback, per the standing rule.

| Unit | Words | ≈Slot | Clip | Model | Frozen | Suggested mode |
|---|---|---|---|---|---|---|
| front | 9 | 3.9s | 4s | veo | — | freeze (slot shorter than clip — trims) |
| f01 | 25 | 10.8s | 8s | veo | 26% | freeze |
| f02 | 23 | 9.9s | 8s | veo | 19% | freeze |
| f03 | 18 | 7.8s | 7s | kling | 10% | freeze + tail_loop ~1.0 (sob settles) |
| f04 | 24 | 10.3s | 8s | veo | 22% | freeze |
| f05 | 26 | 11.2s | 10s | kling | 11% | freeze + tail_loop ~1.0 (head-lift settles) |
| f06 | 18 | 7.8s | 7s | kling | 10% | freeze + tail_loop ~1.0 (nod settles) |
| f07 | 19 | 8.2s | 7s | kling | 15% | freeze + tail_loop ~1.0 (blink ends open) |
| f08 | 30 | 12.9s | 10s | kling | 22% | freeze + tail_loop ~1.0 (shoulder-release settles) |
| f09 | 23 | 9.9s | 8s | veo | 19% | freeze |
| back | 25 | 10.8s | 8s | veo | 26% | freeze (drifting motes — be safe) |

Sum 240 = the narration's own count; 103.29s locked audio + landing hold ≥3.0s
(INV-26). Lane split: 5 kling (the completing-gesture pages) / 4 veo pages + 2 veo
covers — veo-first where the shot allows it. The OpenArt bridge has no veo model —
`model_tier` is advisory there and everything renders via Kling unless the user
explicitly sets `SWIRLS_GEN_PROVIDER=hf` for a specific clip (ep7 F04's documented
one-off exception, never a policy change). Credits, not dollars, are estimated here;
the ledger (`/cost`, `/spend`) is the only truth.

---

## 8. OPEN QUESTIONS (do not silently resolve)

1. **Back-cover title length** — `SHE LEFT CARRYING HIS PEACE` (5 words, the
   narration's final sentence verbatim) vs the fallback `CARRYING HIS PEACE` (3,
   verbatim contiguous). I recommend the full sentence; one line to change if the
   woodcut lettering crowds.
2. **Back-cover subtitle** — `1 JOHN 4:19` (recommended: the narration's own thesis
   verse, "we love him, because he first loved us") vs `ISAIAH 1:18` (the Stain's
   founding verse, "though your sins be as scarlet"). Both are real; the first is
   forward/doctrinal, the second is the motif's own root.
3. **Three Stage-0 pages open the episode (F01–F03).** Deliberate — the narration
   negates her act as the source ("Not thy tears. Not thy ointment."), and both tear
   pages carry real drawn water (LAW 3). Against it: the user's ep2 note that middle
   pages felt swirl-less. Fallback if wanted: a Stage 1 thread from Jesus's RESTING
   hand on the cushion on F02 and F03 (zone-separated from the feet/tears by a stated
   band) — never from the box, never from the tears; the rest of the arc shifts up
   one page (F04 → 1 held, F07 → 2, unchanged high-tide sums).
4. **The stain turns at F05 (the parable's spoken "forgave"), not at F07 or F08.** My
   reasoning: the first spoken forgiveness is the honest trigger, and it keeps F07 at
   a proven 2+2 cap shape. Alternative: hold D3 through F06 and turn at F07 (D2t +
   Stage 2 = 4, same cap; then only ONE page shows the turning geometry before the
   ring). One line per page to change.
5. **The woman's madder-red mantle** — the only saturated color in the room, her
   likeness pin, and Isaiah 1:18 underneath. Risk: the "scarlet woman" cliché pulling
   a render toward a sensual figure. Reverence guards are on every page; if F01's
   first render still reads that way, the fallback is a deep olive-umber mantle with
   a narrow madder band at its edge (the Barrel-widow band pattern).
6. **Simon's fringe is "undyed cream, never blue."** The tekhelet blue thread is
   period-true (Num 15:38) and is sacrificed to the motif's chromatic reservation —
   the same trade ep2 and ep7 made between period detail and the motif. Confirm.
7. **F01 quadruple debut** — woman, Simon, flask, AND room all crop from one
   approval (five refs). One more debut than ep7's triple; a miss on any is a
   full-page regen. Budget two regen cycles. Alternative (new practice, not
   recommended): a standalone room/flask object render before F01.
8. **The swirl anchored to Jesus's speaking hand (F04–F08)** — ep7's user-accepted
   precedent, reasoned in §2. Needs the user's eye at F04's first render; the
   fallback anchor is the air directly above his couch cushion.
9. **Unbound hair on F03–F08 and the kiss drawn as already made.** Period-true (v38,
   v44) and reverent as designed (face hidden by hair, lips at the instep, fully
   clothed). If any render sexualizes it, fallback: her forehead bowed to his instep
   instead of her lips, hair falling behind her shoulders with only its ends drawn
   forward.
10. **F08's caption** — `which are many, are forgiven` (5 words, one line, Kling
    page) vs the two-line `Her sins, which are many, / are forgiven` on veo (which
    loses the nod). I recommend the one-line Kling version; the kind nod is the hero
    page's one human event.
11. **"Forgiven first" as an already-dried edge on F01** — considered and REJECTED
    (keeps the D3 peak; the cause is carried by WHEN the turn happens, not by the
    debut's geometry). Listed for the record so the implementation pass never adds
    it.
12. **Un-ref'd guests and parable figures** — accepted variance, same as ep7's
    bearers; if a render individuates a guest enough to recur, regen rather than ref
    him.
13. **Hero nomination = F08** — for the main engine's hero-bookend rule and any
    thumbnail; the Swirls assembly itself bookends with the covers. Alternate F07 if
    the user prefers the "seeing" over the "declaring."
