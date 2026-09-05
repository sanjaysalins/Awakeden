# DESIGN BRIEF — Episode 11, "Where Are the Nine"

Luke 17:11-19 (ten lepers cleansed on the road; one, a Samaritan, returns) · Dead ink:
**Stain (uncleanness) — ONE corporate stain under a company of TEN men, the series'
first Stain carried by a group, and the first whose clearing happens with Jesus OUT OF
FRAME** (the series-plan v4 continuity fix, honored here as execution detail only) · NO
Fray anywhere (the ten cry out in need, not in doubt; the nine who walk on are OBEDIENT,
not wavering — a frayed line on any of them would be a doctrine error, so the steady-line
override is stated on every group page) · NT episode, Jesus bodily present and speaking on
the bookend pages, absent on the two road pages — Stage 3 is reached on the last interior
page, beginning on the hero · `panel_style` **woodcut_hybrid** throughout · Voices:
narrator + **jesus** (voices.json — the lepers' cry stays in the narrator's voice).

Fable design pass, 2026-09-04. This brief is the single creative source for the Sonnet
implementation pass (episode.py PageSpec/CoverSpec objects). Narration and audio are
LOCKED — 202 words, 80.61s final, `narrator_atempo_factor 1.0` (natural speed, no
time-stretch), three voiced Jesus quotes each with a 0.4s pre-quote pause. Nothing here
changes a spoken word. Every choice states its WHY. Open questions are flagged inline and
collected in §8 — do not silently resolve them.

---

## 0. The shape of the episode, in one paragraph

The narration is built on a distance and a direction — ten men who stood "afar off,"
were sent while still sick, were cleansed "as they went," and then split: **nine kept
going, one turned back**. So the episode's geometry is fixed on every page: **the
village edge and Jesus at the LEFT, the road running away to the RIGHT.** Every walk
away from Jesus goes right; the one return comes back from the right. The covers belong
to the two ends of that road: front = the ten themselves, standing afar off in a ragged
line with their mouths bound (the hook's own picture, Jesus absent); back = Jesus's feet
on the road at the village edge, the pressed place in the dust where one man lay, the
road running away empty behind ("at his feet, not on the road"). Ten interior pages: the
narration's six paragraphs split at their own picture-changes, and two beats the text
itself separates — *obeyed before any difference* / *cleansed as they went* — MUST be
two pages, because in this series a stain never clears inside a clip (LAW 2): the page
turn IS the miracle. The first hard problem — the cleansing with Jesus out of frame — is
solved by making the swirl's Stage 1 thread the WORD, not the man: it rises from his
sending hand on F03 with its tip already leaning toward the road, enters F04 from the
frame's left edge (his side) as the same single thread running high above the walking
group, and the stain beneath them is simply DRIED on that page — same men, same road,
same paper region, the wet blot replaced by its pale ring. The second hard problem — the
two-tier ending — is solved by splitting the two motifs' jobs: the STAIN's clearing is
the GIFT and it is identical for all ten (F04 shows the whole company cleansed as one
group before anyone responds; F05 puts nine and one on the same clean paper under the
same single thread, differing only in direction); the SWIRL is the GIVER and it is
anchored to Jesus's hand only — it never touches the Samaritan, never rises from him, is
never "his." He does not receive more ink; he goes to where the ink is. The nine are
drawn upright, clean, unhurried, obedient — absent from F07's empty road, never
diminished. The Samaritan is a man among men: no ethnic costume, no darker skin, no
turban-as-otherness; distinct only by his own face (refs) and a narrow clay-red band on
an olive-grey mantle; "stranger" is Jesus's word, not the drawing's. Swirl arc
0·0·1·1·1·2·2·2·3b·3; stain arc 3·3·3·1·0·0·0·0·0·0; crossing at F04 (equality, the road)
and F05 (strictly greater, the fork). Hero = F09.

---

## 1. Narration beat map → units (why ten interior pages)

Word counts are my own count of the locked text (sum 202, matching narration.md;
80.61s locked audio ≈ 2.51 words/sec at natural speed). The assembler treats the weights
as proportions, same as every precedent episode. Turn map from `narration.meta.json`:
narrator (20.08s) → jesus 17:14 (2.08s) → narrator (23.60s) → jesus 17:17-18 (8.64s) →
narrator (2.24s) → jesus 17:19 (4.08s) → narrator (18.72s); 0.4s before each quote.

| Unit | Narration beat | Words | ≈Slot | Voice(s) |
|---|---|---|---|---|
| **front** | "Jesus told ten men with leprosy to go —" | 8 | 3.2s | narrator |
| **F01** | "before a single one of them was healed. They were cleansed on the road. Only one of them came back." | 20 | 8.0s | narrator |
| **F02** | "They'd stood at a distance, as their disease required, and cried out, 'Jesus, Master, have mercy on us.'" | 18 | 7.2s | narrator (the cry is narrator-voiced) |
| **F03** | "He told them, 'Go shew yourselves unto the priests.' They obeyed before they could see any difference." | 17 | 7.2s | narrator + **jesus** |
| **F04** | "'And it came to pass, that, as they went, they were cleansed.'" | 12 | 4.8s | narrator (KJV) |
| **F05** | "Nine kept going. One turned back, 'and with a loud voice glorified God,'" | 13 | 5.2s | narrator (KJV) |
| **F06** | "'and fell down on his face at his feet, giving him thanks: and he was a Samaritan.'" | 17 | 6.8s | narrator (KJV) |
| **F07** | "Jesus asked it out loud, naming exactly what nine men had skipped: 'Were there not ten cleansed? but where are the nine?'" | 22 | 9.2s | narrator + **jesus** |
| **F08** | "'There are not found that returned to give glory to God, save this stranger.'" | 14 | 5.6s | **jesus** |
| **F09** | "To the one still on his face, he said, 'Arise, go thy way: thy faith hath made thee whole.'" | 19 | 8.0s | narrator + **jesus** |
| **F10** | "Nine had exactly what they'd asked for, and kept walking. One turned back to him. Luke calls it thanks. Jesus calls it faith." | 23 | 9.2s | narrator |
| **back** | "That question didn't end with the nine. Go back and find him — at his feet, not on the road." | 19 | 7.6s | narrator |

**Why the paragraphs don't map 1:1:** paragraph 2 (47w ≈ 18.7s) holds three pictures —
the cry at a distance, the command and the obedient turn, the road — and the last two
are separated by the text's own "before they could see any difference" / "as they went,
they were cleansed": a before and an after that this series only ever shows as a hard
cut between pages, never inside one clip. Paragraph 3 (30w) splits at the fork
(nine on / one turned, on the road) and the fall (at Jesus's feet) — two locations.
Paragraph 4 (36w ≈ 14.7s) splits at the question aimed at the road ("where are the
nine?") and the word aimed at the man ("save this stranger") — absence, then presence.
**Why the hook splits 8/20:** the front cover's slot under eight words (3.2s) is the
Barrel's 10-word/3.6s and ep10's 9-word/3.9s precedent; F01 — the establishing shot,
the stain's D3 debut — needs its 8.0s. **Why the landing splits 23/19:** the narrator's
summary ("Luke calls it thanks. Jesus calls it faith.") is the encounter's own picture
and belongs on an interior page; the CTA ("Go back and find him — at his feet") is the
back cover's job, exactly as ep10's back carried its final sentence. **Why not nine:**
every candidate merge (F04+F05, F07+F08) re-joins two pictures the text itself
separates — the gift-before-any-response and the fork; the absence and the presence.
**Why not eleven:** no remaining beat splits without dropping under ~10 words (the
Barrel's churn threshold — F04 at 12w/4.8s and F05 at 13w/5.2s are already the floor).
The story's beats and the freeze cap agree on ten.

---

## 2. The Stain decision (the hard problem), then the motif arcs

### Where the Stain lives — reasoned, not defaulted

- **Under the TEN, as one corporate stain — CHOSEN, and it is exactly what the text
  gives.** Luke's "as their disease required" (the narration's gloss on "stood afar
  off," v12, Lev 13:45-46) makes the uncleanness a shared condition of a company: they
  stand together, cry together, are sent together, are cleansed together. Series
  sub-case: uncleanness (the plan's tag; Naaman's leprosy-stain precedent, ep4). ONE
  formless blot lies IN THE PAPER beneath and around the whole huddle — never ten little
  blots (ten blots invite pattern and pareidolia, and would individuate what the text
  keeps corporate). Geometry follows the person-attached precedents (Hem, Naaman, ep10):
  in the paper under their feet, under the linework so every drawn line passes over it
  unbroken, bounded ≤⅓ page, never over any face, crossing the drawn frame border into
  the page's own margin on THEIR side — the RIGHT margin, the road side, on every stain
  page.
- **It travels with them.** At a distance on the road (F01, F02), and walking away
  under their feet (F03). Always the RIGHT side of the page, always crossing the right
  margin. Its anchor is the group's position.
- **On the Samaritan alone — REJECTED.** He is one of the ten; nothing in the text or the
  narration puts anything on him that the other nine did not carry. A stain singled to
  him would pre-load the "outsider" reading the reverence guard forbids (§3).
- **Cleared by their obedience / their walking — REJECTED as a cause, and actively
  contradicted in the drawing.** On F03 they have turned and are walking, obeying, and
  the stain is at full D3 under their walking feet, stated: *their obedience is already
  in the picture and nothing about the stain has changed.* The text's causality is his
  word ("as they went" is the WHEN, not the WHY) — so the swirl's Stage 1 thread enters
  with his word on F03 and is the only new thing on the page.
- **Cleared by his WORD, off-page — CHOSEN, in the series' own between-pages grammar,
  with Jesus not in frame.** This is the locked continuity note, executed: the stain's
  entire drop lands on the cut F03→F04. F03 is D3 with NO turning geometry (no
  gospel-side dried edge) because the text says "before they could see any difference"
  — the stain must be fully wet as they leave. F04 is D1: the same paper region under the
  same men now holds only the dried pale ring, the paper inside it the cleanest cream on
  the page, the border-crossing now a pale dried trace on the right margin. The single
  thread above them (§2, swirl) is the WORD that went with them. The clearing is credited
  to the thread by adjacency and sequence — never by contact (sky/ground split, a stated
  band of clean paper, LAW 3). No clip ever shows it.
- **D1 → D0 on the cut into F05.** By the fork, no one carries a trace. Nine and one
  stand on the same wholly clean paper. This is deliberate and load-bearing: the ring is
  gone BEFORE anyone responds, so no reader can attach "still marked" to the nine.
- **The literal layer (Naaman's two-layer pattern):** leprosy has a physical fact and
  the Law has visible signs. Drawn reverently: *faint pale mottled patches in a few light
  dry-brush strokes on the backs of the hands and forearms and along bare shins —
  subtle, never sores, never gore, never grotesque*; plus Lev 13:45's own markers,
  which read at any distance and carry the diagnosis without any wound: **rent tunics,
  bare heads, and a strip of cloth bound over the upper lip and mouth**, standing afar
  off. **The cleansing has a literal sign too:** on F04 the lip-cloths are LOOSED,
  hanging at their throats, the skin clear, the men standing taller — a between-pages
  change told by an object, no dissolve. *(Implementation: check ep4 Naaman's episode.py
  for its validated leprosy-skin wording and reuse it verbatim if it exists; the wording
  above is my design intent, not a validated string.)*

### Stain (uncleanness, under the ten) — descending

| Page | Dose | Rendering |
|---|---|---|
| F01 | **D3 peak** | Saturated cold grey-umber in the paper beneath and around the huddle of ten standing afar off at the right, bounded ≤⅓ page, never over any face, crossing the drawn frame border into the RIGHT margin below them; a wide band of clean paper between it and the empty road, the village, and Jesus at the left |
| F02 | **D3 held** | Same dose, beneath the group where they stand crying out; unchanged |
| F03 | **D3 held — the load-bearing hold** | Beneath their walking feet as they go, still crossing the right margin, NO dried edge anywhere — "before they could see any difference" |
| F04 | **D1** | Only the thin pale dried ring lies in the paper around the stretch of road the ten walk on; the paper INSIDE it is the cleanest, brightest cream on the page; the border crossing now a pale dried trace; the ring contains no blue, no gold, no red, and touches no figure's drawn line |
| F05–F10 | **D0** | Canonical absence, stated on every page: no stain, ring, or grey blot anywhere in the paper |

- **The clearing is the cut.** D3→D1 into F04; D1→D0 into F05. Every stain page's
  animation carries the Hem-validated page-global fence ("every stain and mark in the
  paper is old, dry, and long set… no new stain, spot, or darkening appears anywhere")
  plus "never deepening, never spreading, never fading."
- **The stain never lies under Jesus, the village, or the road between him and them** —
  stated on every stain page. **Pareidolia eye-check** on every blot render, standing
  rule — and with TEN faces in the drawn scene above it, the blot must be checked for an
  accidental eleventh.

### Swirl (living blue-gold ink) — rising

| Page | Stage | Anchor |
|---|---|---|
| front | none | Covers carry neither interior motif; the lighting law carries the tension |
| F01 | **0** | Absence stated — ten unhealed men at a distance; nothing earned, nothing yet spoken |
| F02 | **0** | Absence stated — their cry is need, not the life; the life enters with HIS word, not their ask (ep10's "Jesus answered anyway" logic) |
| F03 | **1** | Exactly one thread rising from the back of Jesus's raised right hand — "Go shew yourselves" — its upper end leaning to the RIGHT, toward the road the ten are walking down; static geometry telling the direction (F07 v2's sky-band grammar), so no clip ever has to move it |
| F04 | **1 held — the locked-note beat** | Jesus beyond the left frame edge. The SAME single thread enters the frame at the upper-left edge, high in the sky, and runs above the road over the walking group, its far end a little ahead of them; thin as a hair, touching no man and nothing on the ground; "his word, not his figure" |
| F05 | **1 held** | The same single thread across the sky above ALL TEN — nine walking on, one turned — identical over every man; the swirl does not take sides at the fork |
| F06 | **2** | Jesus in frame again. A few threads and one bloom rising UPWARD ONLY from the back of his lowered right hand, open toward the man on his face — every root on his hand, none descending toward the man, the ground, or the feet |
| F07 | **2 held** | Same hand, now lifted a little toward the empty road — "where are the nine?" |
| F08 | **2 held** | Same hand, lowered again toward the man — "save this stranger" |
| F09 | **3 beginning** | His hand extended palm-up in raising: threads rise from it AND for the first time one loose open band drifts free across the upper air above both figures, tied to no figure, touching neither, not yet filling the scene (the F07-v2 "Stage 3 beginning" register, validated on Kling) |
| F10 | **3** | Diffused: blue-and-gold threads in one loose band through the whole air above the road and the village edge, over both heads, touching no person |
| back | curl | One small hard-capped hooked curl rising from the pressed place in the dust WHERE HE LAY, before Jesus's feet — never from the feet, never from the road beyond |

- **Why the hand, again:** ep7 established (user-accepted on watch) and ep10 reused the
  speaking hand as this series' least indirect anchor. Here the text's source of the
  life is his WORD three times over (v14, v17-18, v19), and a swirl at his mouth is a
  speech-bubble magnet. F03's sending hand → F06-F08's lowered/lifted hand → F09's
  palm-up raising hand gives the whole episode one continuous root. Fallback if it reads
  as decoration at F03's first render: the air directly above his head-height at the
  village edge (same zone logic, one line per page).
- **Why the road-page thread runs from the frame edge, not from a man:** the locked
  note says the thread travels WITH them — but LAW 2 bans any ink motion with a route or
  a moving target, and a thread anchored to a walking figure IS a moving target. So the
  still carries the travel: on F03 the thread's tip leans toward the road; on F04/F05 it
  enters from the left (Jesus's side, off-frame) and already spans the sky above and a
  little ahead of the group. In the clip the men walk and the thread holds exactly as
  drawn (the Stage 1 hold rule); because the thread already spans their whole visible
  path, walking under it reads as "it is with them" without a single moving ink pixel.
- **Why the swirl never touches the Samaritan, on any page — the gift/Giver
  argument in ink:** the STAIN's absence (clean paper, D0) is the gift, and it is the
  same under all ten from F05 on. The SWIRL is the Giver's own presence, anchored to
  Jesus's hand, touching no person. The one who returns "gets" no ink pictured on him;
  he is drawn at the place where the ink is. The nine walked away from that place with
  the whole gift intact. That is the narration's exact sentence — "Go back and find him —
  at his feet, not on the road" — drawn as geometry. Stated on every Jesus page: *the
  threads touch only his hand and the air above it, and never touch, descend toward, or
  rise from the man at his feet.*
- **Why Stage 3 lands on F10 and only begins on F09:** F09 is the hero and a Kling page
  (the face-lift must complete) — a full Stage 3 band over-escalates on Kling (ep10 F09's
  reasoning), so the hero carries the "beginning" register that F07 v2 validated on
  Kling; F10 is veo (holds + fixed-band drift, veo's proven lane) and is the encounter
  complete — the man risen, whole, face to face — the community-less but whole image
  Stage 3 was designed for.

### High-tide check, every page (`stainDose + swirlStage <= 4`)

| Page | Stain | Swirl | Sum | Note |
|---|---|---|---|---|
| F01 | 3 | 0 | 3 | ✓ |
| F02 | 3 | 0 | 3 | ✓ |
| F03 | 3 | 1 | **4** | AT CAP — ep7 F02's / ep10 F04's proven 3+1 shape; full QUAD lock; the two motifs sit at opposite sides of the frame (his hand at the left, the stain crossing the right margin) |
| F04 | 1 | 1 | 2 | ✓ — the equality page |
| F05 | 0 | 1 | 1 | ✓ |
| F06 | 0 | 2 | 2 | ✓ |
| F07 | 0 | 2 | 2 | ✓ |
| F08 | 0 | 2 | 2 | ✓ |
| F09 | 0 | 3b | 3 | ✓ |
| F10 | 0 | 3 | 3 | ✓ |

**Crossing point (swirl ≥ stain) = the gospel turn:** equality on F04 — "as they went,
they were cleansed" — the word taking effect with the speaker out of frame; strictly
greater on F05 — the fork. The crossing is the CLEANSING, which is the gift for all ten;
the swirl then keeps rising only where Jesus is (F06→F10). Two axes, two truths: one
at-cap page (F03), flagged as the highest-risk render.

### The two-tier ending — the visual rules, collected (hard problem #2)

1. **F04 shows the whole company cleansed as ONE group before anyone responds** — ten
   men, one huddle-in-motion, every lip-cloth loosed, every arm clear, D1 ring around
   all of them together. The gift precedes every response.
2. **F05 puts nine and one on the SAME wholly clean paper (D0) under the SAME single
   thread.** The only difference is direction: nine walking right, one turned left. The
   nine are drawn *upright, unhurried, clean, their cloths loosed, in the same clean
   confident line as the one, on the same clean paper, none shadowed, none hunched, none
   looking back in shame* — they are OBEYING the command they were given.
3. **The swirl is never on, from, or toward the Samaritan** (§2, swirl). His nearness
   to it is his position, not his possession.
4. **F07's road is EMPTY, not populated by diminished men.** The nine's absence is the
   question, not a punishment picture. No panel anywhere shows the nine dark, small-and-
   sad, or turned away in shame.
5. **F10's panels "kept walking" / "turned back" are the same size, the same line
   weight, the same light** — two tracks in the dust, not a good man and nine bad ones.
6. **Captions never rank "cleansed" against "whole."** F09's caption keeps faith and
   wholeness in ONE line ("thy faith hath made thee whole"), never "made thee whole"
   alone over a picture that could read as a prize; F10's caption is the narration's own
   pair, "Luke calls it thanks." / "Jesus calls it faith." — the same act, two names.

---

## 3. Refs — who and what needs pinning

All new refs live in this episode folder's `refs/`
(`F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_11_where_are_the_nine\refs\`).
Chain order is hard (render_still stops on a missing ref).

### Characters

**JESUS** — SERIES CONSTANT. **Reuse
`F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_10_she_loved_much\refs\jesus_ref.png`
unchanged** — copy it verbatim to this episode's `refs/jesus_ref.png` (itself from
ep7/ep4/ep1/ep8's approved crop). No redesign, no approval cycle. JESUS_BUILD reused
verbatim from ep10's episode.py:

> Jesus, a Judean man in his early thirties, medium height and ordinary build,
> sun-browned skin, shoulder-length dark brown hair pushed back from his face, a
> short full dark beard, wearing a simple ankle-length robe of undyed cream-brown
> wool with a plain olive-toned mantle draped over one shoulder, a narrow rope belt,
> and flat worn leather sandals -- no halo, no glow, nothing in his dress
> distinguishing him from the men around him, standing square, still, and
> unhurried, his gaze steady and direct

**New per-page guard, every Jesus page (this episode's "coffin" — the TOUCH trap):**
*"standing on foot on the dry road, his hands empty, touching no one on this page; the
open distance between him and the men stays open."* An image model's prior for "Jesus +
lepers" is Luke 5:13 / Matt 8:3 — his hand laid on a leper. In THIS story he never
touches anyone: the ten are at a distance (v12), he sends them with a word (v14), and the
Samaritan lies a hand's width before his sandals (v16). A rendered touch is a canon
error, not a style wobble. Second prior, the same guard: no healing light, no radiance
from his hand — the template's "no glowing spiritual VFX" plus the dose language handle
it, but eye-check every Jesus page for a glow leaking into the dose.

**THE SAMARITAN** — new to the series. Unnamed; the narration calls him "one," "a
Samaritan," and (in Jesus's mouth) "this stranger." Build text (use verbatim):

> the Samaritan, a man of about forty, lean and weathered, olive-brown skin like the
> men around him, a long face with a broad brow, deep-set dark eyes with heavy
> brows, a strong straight nose, and a close-cropped black beard flecked with grey;
> dark hair cut short, his head bare; wearing a coarse ankle-length tunic of undyed
> grey-cream wool torn open at the breast (rent, as the Law required) under a
> mantle of faded olive-grey wool with a narrow clay-red selvedge band along its
> edge, worn over one shoulder; bare dusty feet; drawn with the same care, the same
> line weight, and the same dignity as every other man on the page

**Reverence guard (hard problem #3), reasoned:** Luke's point is that the outsider had
the right response — the point is lost, not made, if the drawing marks him as an
outsider TYPE. So: **no ethnic costume, no darker skin than the nine, no turban or
foreign head-dress, no "Samaritan" iconography of any kind** — he is a man among ten
men, indistinguishable in kind from the others on F02-F04, and on those pages he is
findable only by his mantle's clay-red band (the Barrel-widow band pattern) and his own
face. The reveal "and he was a Samaritan" lands on F06 as a corner note over a man lying
on his face — the picture shows a MAN, the note supplies the word. "Stranger" is Jesus's
word (v18, *allogenes*) and in the narration's own reading it is a title of honor
("save this stranger") — the drawing never sneers it. Chromatic reservation: no blue on
him anywhere; clay-red is allowed (Naaman's tunic precedent; the QUAD lock forbids red
only INSIDE a stain). Stated on every page he is on: *drawn with the same care, the same
line weight, and the same dignity as every other man on the page; never a caricature.*

**Lip-cloth states (between-pages changes):** bound over his upper lip and mouth on
F02, F03 (matches the full-figure ref); loosed and hanging at his throat from F04 on
(the ref pins the face; the override is a text line: *"his lip-cloth now loosed,
hanging at his throat"*). Refs: `samaritan_ref.png` (full figure, cloth up) cropped from
F02 approved — the one man in the huddle wearing the olive-grey mantle with the clay-red
band; `samaritan_face_ref.png` (face, eyes open, cloth down) cropped from F05 approved,
his first individuated page (a MEDIUM with his face lifted and his eyes OPEN — the
reason F05's "loud voice" is told by posture, not a thrown-back head with shut eyes:
a face ref needs open eyes). He has true close framing on F05, F09, F10 and a face-study
panel on F09 — full-figure crops are too small to pin a face.

**THE TEN (as a group) / THE NINE** — a shared GROUP identity, no individual refs.
Build text for the group (use verbatim on every group page):

> exactly ten men — count them — no more, no fewer: gaunt, sun-worn men of the
> region in coarse rent tunics of undyed grey-cream and ochre wool torn open at the
> breast, their heads bare, each with a strip of cloth bound over his upper lip and
> mouth, faint pale mottled patches drawn in a few light dry-brush strokes on the
> backs of their hands and forearms and along their bare shins — subtle, never
> sores, never gore, never grotesque — their hands empty; nine of them
> unindividuated, faces half-hidden by their cloths, drawn as different men in the
> same steady, confident, single-struck line, no doubled or tremored contour on any
> of them; no bells, no rattles, no begging bowls, no bandages, no hoods

Why a group ref and not nine refs: the nine never individuate — the text never gives
them a face, and individuating them would invite the "nine bad men" reading (§2). But
the GROUP'S LOOK recurs on five pages plus the front cover (the cloths, the rent tunics,
the bare heads), and a look drifts exactly like a face does (Jacob's Ladder: the mantle
became a cape). So `ten_ref.png` — a crop of the whole huddle from F02 approved — is
chained into F01, F03, F04, F05 and the front cover as a LOOK ref, with the prompt's
manifest line reading "image N is the company of ten lepers — match their rent
garments, bare heads, and the cloth bound over each mouth." **The NUMBER is this
episode's literalism trap** (the Barrel's "barrel," the Bier's "bier," ep10's "box"):
the title is a number, and a render with eight or eleven men breaks the episode. Every
group page states "exactly ten — count them"; F05 states "nine walking on and one
turned — ten in all"; and the eye-QC checklist for this episode adds a COUNT on every
group page and every group panel before anything else is checked (§5).

### Objects / locations

**THE VILLAGE EDGE** — the location of every Jesus page (F01-F03, F06-F10, back).
Build text (use verbatim):

> the edge of a small Galilean-border village: a few low flat-roofed houses of
> pale field-stone with a low dry-stone wall running out from them, a bare terebinth
> tree, and a dry dirt road beginning at the wall's end and running away over open
> stony hill country; no well, no spring, no stream, no water anywhere — the ground
> dry ochre earth and stone

Why the DRY is stated: LAW 3 — the swirl's threads live in the sky on every page, and a
road-side well is exactly the water feature that turns a thread into a pour. Ref:
`village_edge_ref.png` cropped from F02 approved (the houses + wall + tree + the road's
start, small at the left).

**THE ROAD** — the location of the two Jesus-absent pages (F04, F05) and the far
distance of every other page. Build text (use verbatim):

> the same dry dirt road further along, running from left to right over a low rise
> of open stony hill country, dry ochre earth, scattered field-stones, thin dry
> grass, no wall, no building, no tree, and no water of any kind

Ref: `road_ref.png` cropped from F05 approved (the road + rise + hills, no figures).

**No object refs.** The lip-cloths are part of the group build (and the Samaritan's).
No staffs (a prop that morphs — Jacob's staff grew a crook — and an invention prior
for "travelers" that we don't need), no bowls, no vessels: every man's hands are empty
on every page, stated. The back cover's "pressed place in the dust" is a one-page
element, not a recurring object.

### Chain order (hard dependencies)

1. Copy `jesus_ref.png` from episode 10 (immediate, no cycle).
2. **F02** renders with `refs=[R_JESUS]` — the ten, the Samaritan (as one of them), and
   the village edge all debut → approve → crop `ten_ref`, `samaritan_ref` (the
   band-mantled man, cloth up), `village_edge_ref`. *A TRIPLE debut on one approval,
   ep7's shape — and the first page where the count matters. Budget two regen cycles
   (§8).*
3. **F05** (jesus NOT in frame; refs: ten_ref + samaritan_ref) → approve → crop
   `samaritan_face_ref` (eyes open, cloth down) + `road_ref`.
4. **F01, F03** (jesus + ten_ref + samaritan_ref + village_edge_ref) any order after 3.
5. **F04** (ten_ref + samaritan_ref + samaritan_face_ref + road_ref) after 3.
6. **F06–F10** (jesus + samaritan_ref + samaritan_face_ref + village_edge_ref) after 3.
7. **Front cover** (ten_ref + samaritan_ref + village_edge_ref) after 2.
8. **Back cover** (jesus_ref + village_edge_ref, no full figure) after 2.

---

## 4. Covers

### The cover judgment call (stated, as the format asks)

The hook is ten men told to go before one was healed; the landing is "at his feet, not
on the road." So the covers are the two ends of the road: the TEN standing afar off
with their mouths bound (front — the hook's own picture, Jesus absent, the viewer on his
side of the distance), and Jesus's FEET on the road at the village edge with the pressed
place in the dust before them and the road running away empty behind (back — the
landing's own picture, no whole figure). Series variety: ep4 led with Jesus, ep5 with
its widow, ep7 with the object, ep10 with the woman carrying the object; ep11 leads with
a CROWD for the first time, and lands on a place rather than an object — the story has
no object, it has a distance and a direction.

### FRONT COVER

- **Scene:** ten men standing together in a ragged line across the lower third of the
  frame, small against the landscape, seen from the road in front of them at a distance
  — gaunt, sun-worn, in coarse rent tunics torn open at the breast, heads bare, each
  with a strip of cloth bound over his upper lip and mouth, their hands empty at their
  sides, none stepping forward — exactly ten, count them; behind and above them a dry
  dirt road climbing away over open stony hill country under carved structural cloud
  forms; at the far left edge, small, the low flat-roofed houses and dry-stone wall of
  a village, no one standing there.
- **Lighting (law: ≥1 warm + ≥1 cool):** warm low late-afternoon sun from behind the
  hills, rim-lighting the men's ragged shoulders and the dust in gold-ochre; cold
  blue-grey shadow filling the near foreground of the road between the viewer and the
  men, and the shadowed face of the village wall. WHY: the warmth is behind them and
  beyond them, on the road they will be sent down; the cold is the distance the viewer
  stands on — the disease's own required gap.
- **Motif:** none (covers never carry the interior motifs).
- **Title:** `WHERE ARE THE NINE` (top) — the locked episode title, KJV 17:17 verbatim
  contiguous ("but where are the nine?"). **Subtitle:** `LUKE 17`. **seq_title for all
  interior pages = `WHERE ARE THE NINE`** (4 words — the Bier's own 4-word length; if
  the woodcut lettering crowds, fallback `THE NINE`, §8).
- **Refs:** ten_ref + samaritan_ref + village_edge_ref (hence F02 approval precedes this
  render).
- **extra_avoid append:** "bells, rattles, begging bowls, bandaged faces, medieval
  hoods, sores, blood, gore, grotesque deformity, any figure touching another, modern
  clothing".
- **Animation (strong front lock, per the cover doc):** the loose ends of the men's rent
  garments and lip-cloths stir faintly in the road's wind; the low sun behind the hills
  stays exactly as warm and low as it already is, unchanged for the whole clip; the cold
  shadow across the foreground road stays exactly as cold and dim as it already is; the
  ten men stand exactly as drawn, none stepping forward, none raising a hand; the
  village houses stay exactly as drawn; no new figure, mark, or text appears.
  `clip_duration=4` (3.2s slot). Freeze (slot shorter than clip — ep10's and the
  Barrel's front-cover case; see §8 on the trim-vs-boomerang note).

### BACK COVER

- **Scene:** a low angle from the dust of the road at the village edge at dawn: in the
  lower third, large, Jesus's two bare feet in flat worn leather sandals and the hem of
  his undyed cream-brown robe, standing square and still on the dry ochre road, seen
  from the front and a little below — nothing of him above the knee in frame; a hand's
  width before his sandals, the pressed place in the dust where a man lay on his face —
  the shallow prints of a forehead, two spread hands, and two forearms, drawn plainly as
  marks in dust; from that pressed place, not from the feet, one small hard-capped
  hooked curl of blue ink with a trace of muted gold rises — its whole visible length no
  longer than a hand's width, curling back toward its own root like a comma or a
  fishhook WITHOUT fully closing into a ring, flat and two-dimensional, drawn ON the
  paper's surface, a single continuous brushstroke, never a ring, never a bracelet,
  never a bangle, never jewelry, never metallic, never reflective, never straightening,
  never trailing, behaving like a small dab of living ink, never a glow; beyond and
  above, the dry road running away over the rise into open hill country, EMPTY — no
  figure anywhere on it — under carved cloud forms; at the left edge, the corner of the
  village's dry-stone wall and the bare terebinth.
- **Why this image:** "Go back and find him — at his feet, not on the road." The road is
  where the nine went (empty now, cold); the feet are where the one lay (warm, and the
  only living ink on the cover rises from that pressed place — from WHERE HE LAY, never
  from the feet themselves and never from the road: the life was found at the place of
  return, and the cover invites the viewer to the same spot). No whole figure: the
  invitation is a place, and the viewer's own eye-line is already there, low in the
  dust.
- **Lighting (law):** warm dawn gold from the village side at the left, low across the
  feet, the sandals, the hem, and the pressed dust; cold blue-grey night still holding
  the far road, the rise, and the hills where it disappears.
- **Title:** `AT HIS FEET, NOT ON THE ROAD` (bottom) — the narration's final clause
  verbatim. Length fallbacks, in order: `GO BACK AND FIND HIM` (5, verbatim contiguous,
  the CTA itself), then `AT HIS FEET` (3) — §8. **Subtitle:** `EPHESIANS 2:8` — "For by
  grace are ye saved through faith; and that not of yourselves: it is the gift of God":
  the exact verse of the narration's thesis ("Luke calls it thanks. Jesus calls it
  faith." — wholeness by faith, as gift, not earned by the act of returning: the
  doctrinal line the narration was revised six panel-rounds to hold). Alternative `JOHN
  6:37` ("him that cometh to me I will in no wise cast out" — the stranger received)
  in §8.
- **Refs:** jesus_ref (for the sandals, robe hem, and skin — the ref's likeness work is
  moot with no face in frame, but the build must match) + village_edge_ref.
- **extra_avoid append:** "any whole human figure, a face, a hand reaching down, any
  figure on the road, jewelry, bright neon".
- **Animation (light back lock, per the cover doc):** fine dust drifts slowly and low
  along the empty road in the dawn wind; the small blue-gold curl stays exactly as
  drawn, in place, for the whole clip; the warm light across his feet and the pressed
  dust stays exactly as warm and low as it already is, unchanged; the far road stays
  exactly as cold and dim as it already is; his feet stay exactly as drawn; no new
  figure, mark, or text appears. `clip_duration=6` (7.6s slot, 21% frozen). Freeze
  (drifting dust — never boomerang).

---

## 5. Page design conventions used below

- Every page: `panel_style="woodcut_hybrid"`, 9:16, `include_no_bubble_clause=True`
  (five quoted-line captions — the bubble-prior case again).
- **Page geometry law, every interior page:** the village edge and Jesus at the frame's
  LEFT; the road running away to the RIGHT; the ten (and the stain, while it lasts)
  toward the RIGHT; every departure walks right; the one return comes from the right and
  lies at his feet at lower center-right. F04/F05 (Jesus out of frame) keep the same
  axis: he is beyond the LEFT edge, the road runs right, the thread enters from the
  left. Consistent geography is what lets a ten-page road read as one road.
- **COUNT check first (this episode's literalism trap):** on every page and panel that
  shows the group, the eye-QC counts the men BEFORE checking anything else — ten on
  F01-F04 and the front cover; nine + one on F05; ten small figures in F07's panel 1.
  A wrong count is a regen, full stop.
- **Touch guard** (§3, Jesus) on every Jesus page: hands empty, touching no one, the
  distance stays open; on F06-F09 "a hand's width before his sandals, not touching."
- **Standing steady-line override (the no-Fray guard):** every group page states *"drawn
  as different men in the same steady, confident, single-struck line, no doubled or
  tremored contour on any of them"* — ten desperate men are exactly what a render
  loosens into fray-hatching, and here that would say "doubt" about men the text calls
  obedient.
- **Reverence guards** on every Samaritan page (§3) — and the prostration (F06-F09) is
  drawn as ALREADY MADE, face to the dust, arms forward, fully clothed, never animated as
  a fall.
- **Leprosy discipline:** faint dry-brush patches on hands/forearms/shins + the three
  Levitical markers (rent tunic, bare head, bound lip-cloth); never sores, gore, or
  grotesque deformity, stated on every marked page; from F04 the skin is stated clear
  and the cloths loosed.
- **LAW 3 for this episode:** there is NO water on any page — no well, no stream, no
  basin — stated as "dry" in every location build; the threads live in the sky/air on
  every page and touch nothing on the ground.
- **NO_MOUTH** to the owner of each page's voiced line: Jesus on F03, F07, F08, F09.
  The lepers' cry (F02) is narrator-voiced and their mouths are covered anyway; the
  Samaritan's "loud voice" (F05) is narrator-voiced KJV and told by posture, his mouth
  closed — never drawn open and never animated.
- **Kling + 2-line captions = the documented OpenArt failure combo** (ep7 F04: 3/3
  speech-bubble tails; swirls_page.py warns on it). Every Kling page below carries a
  ONE-line caption; only veo pages (F01, F02, F03, F04, F10) stack two lines.
- Captions are verbatim contiguous fragments of the locked narration (KJV lines
  included), ≤4 words per line except one collapsed 5-word line on the hero (ep7 F04's
  and ep10 F08's own precedent); panel labels are 1–3 authored words; corner notes
  short.
- Main-scene prose below is design intent at near-final density (PageSpec
  `main_scene_still` register). Sonnet writes the template prompts — keeping every
  MUST-SHOW, count, dosage, separation, never-X, touch, reverence, and steady-line
  clause — and, per LAW 4, the final animation prompt against the RENDERED still's
  actual pixels.
- Model lanes per the north-star tiering: Kling3.0 pro where a designed gesture must
  COMPLETE mid-clip; veo3_1_lite for holds/locomotion-continues/ambient pages (veo
  handled real running on John 4 shot 7 — walking is a continuation, not a completion).
  Stated per page with its why. Under the OpenArt bridge (no veo model) the tier is
  advisory — see §7.

---

## 6. Page-by-page

### F01 — "before a single one of them was healed" (20w · Stain **D3 peak** · Swirl 0 · veo3_1_lite, clip 6)

The establishing shot and the Stain's debut — the distance as the subject. Renders
AFTER F02 (which debuts the ten and the village at a size that crops), so every ref is
already chained here. WIDE, the whole geography in one frame: village and Jesus left,
the ten far right, the empty road between.

- **Panels** *(the hook's three nouns)*
  1. `"leprosy"` — a bare forearm and the back of a hand, close, with a few faint pale
     mottled dry-brush patches, no sore, no wound *(the disease, reverently)*.
  2. `"the road"` — the dry dirt road leaving a village between a low stone wall and
     open ground, no one on it.
  3. `"came back"` — one small figure alone far down a road, facing the viewer, walking
     this way *(the hook's flash-forward; static, a figure at a distance)*.
- **Main scene** — `WIDE shot`:
  > the edge of the village (VILLAGE_EDGE_BUILD) at the frame's left, fully inside the
  > frame; {JESUS_BUILD}, standing on foot on the dry road at the wall's end, facing
  > right toward the road, still, his hands empty, touching no one on this page, fully
  > inside the frame; the road running away to the right, EMPTY between him and them
  > for a long stretch; far along it at the frame's right, at a clear distance from
  > him, {TEN_BUILD} standing together in a huddle, stopped, looking toward him — one
  > of them the man in the olive-grey mantle with the narrow clay-red band
  > (SAMARITAN_BUILD, match the attached reference), among the others and in no way
  > set apart from them; late-afternoon light, long shadows; the whole ground dry
  > ochre earth and stone, no water anywhere. A cold grey-umber stain lies in the paper
  > itself beneath and around the huddle of ten, formless and matte, lying beneath the
  > linework so every drawn line passes over it unbroken, its feathered damp edge
  > crossing the drawn frame border into the page's own right margin directly below
  > them, never over any face, bounded to less than a third of the page; a wide band of
  > clean paper between the stain and the empty road, the village, and Jesus; the
  > stain nowhere near Jesus. Stage 0 dosage: no blue Swirls of Life ink motif
  > anywhere on this page — no blue ink appears anywhere in the scene, the panels, or
  > the margins.
- **material_closer:** "the cold stain lying in the paper beneath the ten men at the
  right is the only unusual ink at work on this page, and no blue appears anywhere."
- **Fence:** `stain` — "the cold grey-umber stain in the paper beneath the ten men at
  the right"
- **Caption:** `("Only one of them", "came back")` *(narration verbatim contiguous,
  4+2; veo page — two lines OK; the hook's sting under a picture of ten)* · **Corner
  note:** `NOTE: afar off` *(KJV 17:12's own phrase)*
- **Panel motions:** (1) the light across the forearm warms very slightly and settles
  *(tone-only — the marked skin is the loaded element)*; (2) a thin banner of dust
  drifts across the empty road; (3) the far figure holds, still.
- **Main animation:** Jesus stays exactly as drawn, one slow breath, his face toward the
  far men, his hands still and empty; the ten men stand still in their huddle, the loose
  ends of their rent garments and lip-cloths stirring faintly in the wind, none of them
  stepping forward; a low thin haze of dust drifts along the empty road between; the
  cold stain in the paper stays exactly as drawn, never deepening, never spreading,
  never fading.
- **Why veo:** all holds plus ambient, no completing gesture, eleven figures — veo's
  multi-figure "hold still" lane at the cheaper tier. **Refs:** jesus + ten_ref +
  samaritan_ref + village_edge_ref.

### F02 — "Jesus, Master, have mercy on us" (18w · Stain D3 held · Swirl 0 · veo3_1_lite, clip 6)

The cry — and the DEBUT page (renders first): the ten large enough to crop the group
ref and the Samaritan's full-figure ref, the village small beyond them. The three
Levitical marks fill the panels so the main scene can be the cry itself.

- **Panels** *(Lev 13:45 — the three signs)*
  1. `"covered lip"` — a strip of cloth bound over a man's upper lip and mouth, close,
     his eyes above it.
  2. `"rent garment"` — the torn-open breast of a coarse tunic, close, the tear's frayed
     edge.
  3. `"have mercy"` — one raised open hand against the sky, a faint pale mark on its
     back *(the cry as a hand, not a mouth)*.
- **Main scene** — `MEDIUM shot` from the road, the ten filling the right two-thirds:
  > {TEN_BUILD}, standing together at the right, crying out — heads lifted, arms
  > raised, hands open and empty, their mouths covered by their bound cloths — fully
  > inside the frame; one of them the man in the olive-grey mantle with the narrow
  > clay-red band (SAMARITAN_BUILD), fully inside the frame among the others, in no
  > way set apart from them; far beyond them at the frame's left, small, the edge of
  > the village (VILLAGE_EDGE_BUILD) and {JESUS_BUILD} standing on foot at the wall's
  > end, facing them across a long stretch of empty road, his hands empty, touching no
  > one on this page; the whole ground dry, no water anywhere. The same cold
  > grey-umber stain lies in the paper beneath the group where they stand, formless
  > and matte, beneath the linework, crossing the drawn frame border into the
  > right margin, unchanged, never over any face, bounded to less than a third of the
  > page; a wide band of clean paper between it and the road, the village, and Jesus.
  > Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page — no blue
  > ink appears anywhere in the scene, the panels, or the margins.
- **material_closer:** "the cold stain in the paper beneath the ten men is the only
  unusual ink at work on this page, and no blue appears anywhere."
- **Fence:** `stain` — "the cold grey-umber stain in the paper beneath the ten men"
- **Caption:** `("Jesus, Master,", "have mercy on us")` *(KJV 17:13 verbatim
  contiguous, 2+4; veo page — two lines OK; narrator-voiced, mouths covered)* ·
  **Corner note:** `NOTE: as required`
- **Panel motions:** (1) the eyes above the cloth blink once fully — close, then open
  again, ending wide open; (2) the frayed tear-edge stirs faintly; (3) the raised hand
  holds, the light across it warming very slightly.
- **Main animation:** the ten men hold their raised arms up, their chests lifting once
  together with the breath of the cry and settling, their heads staying lifted, their
  cloths staying bound over their mouths, none stepping forward; the far figure of Jesus
  stays exactly as drawn, still; the loose ends of their garments stir in the wind; the
  cold stain in the paper stays exactly as drawn, never deepening, never spreading,
  never fading.
- **Why veo:** ten figures in a hold-with-breath, no completing gesture; the cheapest
  tier on the page most likely to need likeness/count regens (three crops ride on it).
  `refs=[R_JESUS]` → approve → crop `ten_ref`, `samaritan_ref`, `village_edge_ref`.

### F03 — "Go shew yourselves unto the priests" (17w · Stain **D3 held — the load-bearing hold** + **Swirl 1 first trace** = 4, AT CAP · veo3_1_lite, clip 6)

His word, and their obedience before any difference. The ten have ALREADY turned and
are walking away, still fully marked, the stain wet under their feet; the first blue of
the episode rises from his sending hand with its tip leaning after them. The only
at-cap page: full QUAD lock.

- **Panels**
  1. `"the priests"` — a far walled town on a hill under evening light, small, no
     figures *(where they are sent)*.
  2. `"they obeyed"` — the backs of two men walking away, their bare heads and the
     knots of their lip-cloths at the napes, close *(partial main-scene element)*.
  3. `"his word"` — Jesus's right hand raised, open, palm forward, close — NO blue in
     this panel *(the anchor; the Stage 1 thread exists only once, in the main scene)*.
- **Main scene** — `WIDE shot`:
  > the village edge (VILLAGE_EDGE_BUILD) at the left; {JESUS_BUILD}, standing on foot
  > at the wall's end facing right, his right hand raised in sending — already raised,
  > open, palm toward the road, touching nothing — fully inside the frame, his hands
  > otherwise empty, touching no one on this page; at the right, {TEN_BUILD}, all ten
  > turned away from him and walking to the right along the road in the same direction,
  > their backs to him, mid-stride, their cloths still bound over their mouths, the
  > faint pale patches still on their hands and forearms, their heads bare, in no way
  > changed — one of them the man in the olive-grey mantle with the clay-red band
  > (SAMARITAN_BUILD), among the others; the stretch of empty road between him and them
  > fully inside the frame; the ground dry, no water anywhere. The cold grey-umber
  > stain lies in the paper beneath their walking feet, formless and matte, beneath the
  > linework, EXACTLY as before — its edge nearest Jesus as saturated as everywhere
  > else, neither dried nor spread — crossing the drawn frame border into the right
  > margin, never over any face; their obedience is already in the picture and nothing
  > about the stain has changed; a wide band of clean paper between the stain and the
  > road behind them, the village, and Jesus; the stain nowhere near Jesus. Stage 1
  > dosage: exactly one restrained thread of blue ink rising from the back of Jesus's
  > raised right hand into the air above it, its upper end leaning to the right toward
  > the road the men are walking down, touching only his hand and the air, touching no
  > man and nothing on the ground, the only blue on the whole page, behaving like one
  > stroke of wet ink bled into the paper, smooth and open in its curl, never
  > blot-shaped; the stain formless and matte, never swirl-shaped; a wide band of
  > untouched clean paper between the thread and the stain at every point (they sit at
  > opposite sides of the frame); the thread drawn ON the page's surface, the stain
  > lying IN the paper beneath the linework.
- **material_closer:** "the cold stain in the paper beneath the walking men and the
  single blue thread at his raised hand are the only two kinds of unusual ink at work
  on this page, kept apart by clean paper."
- **Fence:** `stain` — "the cold grey-umber stain in the paper beneath the ten walking
  men and the single blue thread at Jesus's raised hand"
- **Caption:** `("Go shew yourselves", "unto the priests")` *(KJV 17:14 verbatim
  contiguous, 3+3; veo page — two lines OK; Jesus's voiced line)* · **Corner note:**
  `NOTE: no difference yet` *(the page's whole design in three words)*
- **Panel motions:** (1) a faint haze drifts over the far hill town; (2) the two backs
  hold their step, unmoving; (3) the raised hand holds, still.
- **Main animation:** the ten men keep walking away from left to right along the road at
  an even pace, their backs to him, one continuous steady stride the whole clip, none
  turning; Jesus stays exactly as drawn, his raised hand held and not rising further,
  one slow breath, his lips staying closed and completely still — he is not speaking and
  his mouth does not move at all; the single thin blue ink thread at his hand stays
  exactly as drawn, in place, for the whole clip; the cold stain in the paper beneath
  the walking men stays exactly as drawn, never deepening, never spreading, never
  fading.
- **Why veo, on an at-cap page:** the walk is a continuation of the drawing (LAW 1),
  not a completing gesture; the Stage 1 thread is held still per the north-star table;
  veo is the cheaper tier on the page most likely to need a QUAD-lock regen. **Fragility
  note (LAW 0.6):** if F03's still needs more than one regen to render the stain and the
  thread apart, cut the walk to "stand turned away, one step begun" and let F04 carry
  all the locomotion. **Refs:** jesus + ten_ref + samaritan_ref + village_edge_ref.

### F04 — "as they went, they were cleansed" (12w · Stain **D1** · Swirl 1 held · veo3_1_lite, clip 4) — THE LOCKED-NOTE BEAT

The road, Jesus out of frame, the cut that is the miracle. Same men, same direction,
same paper region — the wet blot replaced by its dried ring; the same single thread now
entering from his side of the frame and running above them. The literal sign of the
cleansing is an object change (the cloths loosed), and the before/after that this series
never animates is shown instead as a STATIC pair in panels 2 and 3.

- **Panels** *(before / after, between panels — never inside a clip)*
  1. `"as they went"` — bare walking feet on dry dust mid-stride, low, dust lifting.
  2. `"before"` — a bare forearm with the faint pale mottled patches, close.
  3. `"cleansed"` — the same bare forearm, clean and unmarked, close, the same angle
     *(the cut made visible as two still drawings)*.
- **Main scene** — `MEDIUM WIDE PROFILE shot`, the road further along:
  > the road (ROAD_BUILD) running from left to right over a low rise, no village, no
  > figure of Jesus anywhere in the frame; {TEN_BUILD} walking together along it from
  > left to right in profile, mid-stride, still one group — exactly ten, count them —
  > and CLEANSED: every man's lip-cloth loosed and hanging at his throat, their mouths
  > and faces bare, the skin of their hands, forearms, and shins clear and unmarked,
  > standing taller, two of them looking down at their own bared forearms as they walk,
  > one with an open hand lifted to his own uncovered mouth, their tunics still rent;
  > one of them the man in the olive-grey mantle with the clay-red band
  > (SAMARITAN_BUILD, his lip-cloth now loosed, hanging at his throat), among the
  > others; the ground dry ochre earth and stone, no water anywhere. Of the cold
  > stain, nothing wet remains anywhere: only a thin, faint, pale dried watermark ring
  > lies in the paper around the stretch of road the ten walk on — the dried edge of
  > the old stain, the stain itself gone — and the paper inside that ring is the
  > cleanest, brightest cream on the whole page; where the ring meets the drawn frame
  > border at the right, only a pale dried trace remains on the margin; the ring
  > contains no blue, no gold, and no red, and touches no figure's drawn line. Stage 1
  > dosage, held: exactly one restrained thread of blue ink high in the sky, entering
  > the frame at its upper-left edge and running across the upper air above the
  > walking men to a point a little ahead of them at the right, thin as a hair, tied
  > to no figure, touching no man and nothing on the ground, the only blue on the
  > whole page, behaving like one stroke of wet ink bled into the paper's sky wash,
  > smooth and open, never blot-shaped; a wide band of clean paper between the thread
  > in the sky and the dried ring on the ground at every point.
- **material_closer:** "the dried pale ring in the paper around the road and the single
  blue thread high in the sky are the only two kinds of unusual mark on this page, and
  the paper inside the ring is the cleanest on it."
- **Fence:** `stain` — "the dried pale ring in the paper around the stretch of road the
  ten men walk on"
- **Caption:** `("as they went,", "they were cleansed")` *(KJV 17:14 verbatim
  contiguous, 3+3; veo page — two lines OK)* · **Corner note:** `NOTE: not in frame`
  *(the locked note itself, as the page's own production note — flagged in §8 as
  optional; fallback `NOTE: on the road`)*
- **Panel motions:** (1) dust lifts and drifts from the walking feet; (2) the marked
  forearm lies still, the light across it unchanged; (3) the clean forearm holds, the
  light across it warming very slightly.
- **Main animation:** the ten men keep walking from left to right along the road at an
  even pace, one continuous steady stride the whole clip, the two looking at their
  forearms keeping their heads bowed to them, the one with his hand at his mouth holding
  it there, none turning; the loosed cloths at their throats stir with their steps; the
  single thin blue ink thread high in the sky stays exactly as drawn, in place, for the
  whole clip; the dried pale ring in the paper stays exactly as drawn, and no new stain,
  spot, or darkening appears anywhere on the page at any point.
- **Why veo (and why 4s):** real locomotion that only continues the drawing (veo
  handled John 4's shot 7 run); a 4.8s slot — the shortest interior page — takes veo's
  4s (17% frozen). **Why the thread spans the path instead of riding with a man:** LAW 2
  — a thread anchored to a walker is a moving target; a thread already spanning the sky
  above their whole visible path lets them walk "under his word" with zero ink motion
  (§2). **Referent check at QC (LAW 4):** the thread must have rendered as ONE thin
  sky-line entering at the left; if it came out as a ground ribbon or a second thread,
  regen the still — do not adapt the animation clause. **Refs:** ten_ref + samaritan_ref
  + samaritan_face_ref + road_ref.

### F05 — "One turned back" (13w · Stain **D0** · Swirl 1 held · kling3_0, clip 4) — THE FORK

Two responses to one gift, on one page. Nine walk on to the right, obedient and clean;
one has turned to face the left — toward the village and the Jesus who is beyond the
frame's edge — his face lifted, his open hands raised. Same clean paper under all ten;
the same single thread over all ten. Renders SECOND (after F02): the Samaritan's first
individuated page, the crop source for `samaritan_face_ref` (eyes OPEN) and `road_ref`.

- **Panels**
  1. `"kept going"` — a single pair of bare feet mid-stride on dry dust, toes pointing
     to the RIGHT, low *(the nine, as a direction)*.
  2. `"loud voice"` — two raised open hands against the sky, clean and unmarked, no
     face *(the glorifying, as hands)*.
  3. `"the village"` — the far edge of the village small on its rise, the dry-stone
     wall and the bare tree, no figure *(what he has turned toward)*.
- **Main scene** — `MEDIUM shot`, the Samaritan large:
  > the road (ROAD_BUILD) running from left to right, the village (VILLAGE_EDGE_BUILD)
  > tiny on the far-left horizon, no figure of Jesus anywhere in the frame; in the
  > foreground at center-left, {SAMARITAN_BUILD}, stopped and TURNED to face LEFT,
  > back toward the village, his lip-cloth loosed and hanging at his throat, his face
  > bare and lifted a little toward the sky over the village, his eyes OPEN, his mouth
  > closed, both arms lifted from his sides with open, empty, clean hands turned palm
  > up, his skin clear and unmarked, his rent tunic and olive-grey mantle with its
  > clay-red band as before, fully inside the frame, drawn with the same care, the same
  > line weight, and the same dignity as every other man on the page; beyond him to
  > the right and smaller, NINE men — nine, count them, nine and this one make ten —
  > walking on away from him to the right along the road, their backs to the viewer,
  > upright and unhurried, their cloths loosed, their skin clear, in the same clean
  > confident line as the one, none shadowed, none hunched, none looking back; the
  > ground dry, no water anywhere. No stain, ring, or grey blot anywhere in the paper —
  > the paper wholly clean beneath the nine and beneath the one alike. Stage 1 dosage,
  > held: exactly one restrained thread of blue ink high in the sky, entering the
  > frame at its upper-left edge and running across the upper air above ALL ten men —
  > over the nine walking away and over the one turned back alike — thin as a hair,
  > tied to no figure, touching no man and nothing on the ground, the only blue on the
  > whole page, behaving like one stroke of wet ink bled into the sky wash, smooth and
  > open, never blot-shaped.
- **material_closer:** "the single blue thread high in the sky is the only unusual ink
  on the page, and the paper beneath every man is wholly clean."
- **Fence:** `none` *(D0 — the page-global no-new-stain clause is still stated)*
- **Caption:** `("One turned back",)` *(narration verbatim, 3 — one line, Kling page)* ·
  **Corner note:** `NOTE: nine kept going` *(narration verbatim — both responses named
  on the page, neither judged)*
- **Panel motions:** (1) dust lifts from the striding feet and drifts; (2) the raised
  hands hold, the light across them warming very slightly; (3) a thin haze drifts over
  the far village.
- **Main animation:** the Samaritan's raised open hands lift the last small distance
  higher and hold there, his face lifting with them and holding, his eyes open, his lips
  staying closed and completely still — he is not speaking and his mouth does not move
  at all; the nine men beyond him keep walking away to the right at an even pace, one
  continuous stride, none turning; the loosed cloth at his throat stirs; the single thin
  blue ink thread high in the sky stays exactly as drawn, in place, for the whole clip;
  no new stain, spot, or darkening appears anywhere on the page at any point.
- **Why kling:** the hands-and-face lift is a completing gesture with a stated end
  (Kling's lane; veo would hold them where drawn); the 5.2s slot takes a 4s clip (23%).
  **Why his mouth is closed on a "loud voice" page:** NO_MOUTH (no lip-sync, ever) and
  the face-ref crop needs an open-eyed, closed-mouth face — the loud voice is carried by
  the raised hands, the lifted face, the panel, and the KJV caption (§8). **Refs:**
  ten_ref + samaritan_ref → approve → crop `samaritan_face_ref`, `road_ref`.

### F06 — "and fell down on his face at his feet" (17w · Stain D0 · **Swirl 2** · kling3_0, clip 6)

The emotional climax — NOT the hero. Jesus bodily in frame again; the man already on
his face a hand's width before the sandals; the swirl rises to Stage 2 at Jesus's
lowered hand and never descends toward the man. The reveal "and he was a Samaritan" is
the corner note over a picture of a man.

- **Panels**
  1. `"turned back"` — a single pair of bare feet on dry dust, toes pointing to the
     LEFT, low *(rhymes F05's panel 1 — the same feet, the other way)*.
  2. `"on his face"` — dry dust and a field-stone, close, the edge of a spread hand
     pressed into the dust *(the ground he fell on)*.
  3. `"a Samaritan"` — the man's bowed profile, close, eyes closed, calm, drawn with
     care *(the reveal as a face, not a costume; small face → tone-only motion)*.
- **Main scene** — `MEDIUM shot`, low, at the village edge:
  > the village edge (VILLAGE_EDGE_BUILD) at the left; {JESUS_BUILD}, standing on foot
  > at the wall's end facing right, looking down, his right hand lowered and open, palm
  > toward the man below him, not touching him, his hands otherwise empty, touching no
  > one on this page, fully inside the frame; on the dry road at his feet,
  > {SAMARITAN_BUILD}, fallen prostrate — lying on his face, his forehead to the dust
  > a hand's width before Jesus's sandals, not touching them, his arms stretched
  > forward on the ground, his open empty hands spread on the dust, his lip-cloth
  > loosed at his throat, his skin clear, his olive-grey mantle with its clay-red band
  > fallen about his shoulders, fully clothed, fully inside the frame, drawn with the
  > same care, the same line weight, and the same dignity as any figure on the page;
  > the road beyond them to the right running away EMPTY over the rise, no other
  > figure on it; the ground dry, no water anywhere. No stain, ring, or grey blot
  > anywhere in the paper. Stage 2 dosage: the blue ink motif quietly present — a few
  > soft blue threads rising UPWARD ONLY from the back of Jesus's lowered hand into
  > the air above it, every thread's root touching his hand directly and going up from
  > there, none descending toward the man, the ground, or his feet, none dripping,
  > none pooling; at the top of the threads, one soft, irregular, hazy patch of the
  > same blue pigment, entirely amorphous, with soft feathered edges and no internal
  > structure of any kind, exactly like a single drop of watercolor spreading into wet
  > paper, touching only his hand and the air above it, touching no other person and
  > nothing else on the page; the ground, the man, and his feet free of any ink of any
  > kind; every thread behaving like wet ink bled into the paper, smooth and open,
  > never blot-shaped.
- **material_closer:** "the soft blue threads at Jesus's lowered hand are the only
  unusual ink on the page, and the paper beneath the man is wholly clean."
- **Fence:** `none`
- **Caption:** `("giving him thanks",)` *(KJV 17:16 verbatim contiguous, 3 — one line,
  Kling page)* · **Corner note:** `NOTE: a Samaritan` *(the reveal — KJV 17:16's own
  last words)*
- **Panel motions:** (1) dust drifts from the turned feet; (2) the pressed dust lies
  still, the light across it warming very slightly; (3) the bowed profile holds,
  tone-only.
- **Main animation:** the Samaritan's shoulders heave once with the breath of his thanks
  and settle, his forehead staying to the dust, his spread fingers pressing into the
  dust and holding; Jesus stays exactly as drawn, his lowered open hand not moving
  further and not reaching down, his face on the man, one slow breath; the soft blue
  threads at his hand drift gently within their own small area, never lowering toward
  the man or the ground; a low thin haze of dust drifts along the empty road beyond;
  no new stain, spot, or darkening appears anywhere on the page at any point.
- **Why kling:** the heave-and-settle and the fingers pressing are completing gestures
  — the page's one human event, so the climax isn't a lifeless hold (the Hem F04-v2
  lesson); the fall itself is NEVER animated (drawn already made). **Refs:** jesus +
  samaritan_ref + samaritan_face_ref + village_edge_ref.

### F07 — "but where are the nine?" (22w · Stain D0 · Swirl 2 held · kling3_0, clip 8)

The question aimed at the road. Jesus already facing the empty road, his hand lifted a
little toward it; the man still on his face at lower center. The nine are ABSENT, not
diminished — the road is simply empty, in the same clean light as before.

- **Panels**
  1. `"ten cleansed"` — ten small clean figures standing in a line, cloths loosed,
     small, far — TEN, count them *(KJV 17:17's own count)*.
  2. `"the empty road"` — a bend of the dry road over a rise with no one on it, a
     little dust hanging where men have gone.
  3. `"out loud"` — Jesus's face in profile, close, lips closed, brow lifted in the
     question *(jesus_ref; small face → tone-only motion)*.
- **Main scene** — `MEDIUM WIDE shot` from beside Jesus, the road filling the right:
  > the village edge (VILLAGE_EDGE_BUILD) at the left; {JESUS_BUILD}, standing on foot
  > at the wall's end, his body and face turned to the RIGHT toward the road, his
  > right hand lifted a little from his side toward it, open, palm up in the question
  > — already lifted, touching nothing — his hands otherwise empty, touching no one on
  > this page, fully inside the frame; at his feet at lower center, {SAMARITAN_BUILD}
  > still prostrate on the dust, his forehead to the ground a hand's width before the
  > sandals, not touching them, his arms forward, his mantle with its clay-red band
  > about him, fully inside the frame, drawn with the same dignity as any figure; the
  > road running away to the right over the rise and out of sight, EMPTY — no figure
  > anywhere on it — fully inside the frame, in the same clear late light as the
  > village; the ground dry, no water anywhere. No stain, ring, or grey blot anywhere
  > in the paper. Stage 2 dosage, held: a few soft blue threads rising UPWARD ONLY from
  > the back of Jesus's lifted right hand into the air above it, their roots touching
  > his hand and nowhere else, one soft amorphous watercolor patch at their top (as
  > before), touching only his hand and the air, never descending toward the man, the
  > ground, or the road, never reaching out along the road; the road and the man free
  > of any ink of any kind.
- **material_closer:** "the soft blue threads at his lifted hand are the only unusual
  ink on the page; the road beyond is empty and the paper wholly clean."
- **Fence:** `none`
- **Caption:** `("where are the nine?",)` *(KJV 17:17 verbatim contiguous, 4 — one line,
  Kling page; Jesus's voiced line)* · **Corner note:** `NOTE: out loud`
- **Panel motions:** (1) the ten small figures hold, the light across them warming very
  slightly *(count risk — tone-only)*; (2) the hanging dust on the road bend drifts and
  thins; (3) the sketched profile holds, tone-only.
- **Main animation:** Jesus's lifted hand rises the last small distance and opens a
  little wider toward the empty road, then holds, his face staying toward the road, his
  lips staying closed and completely still — he is not speaking and his mouth does not
  move at all; the Samaritan holds exactly as drawn, his forehead to the dust, one slow
  breath through his back; the soft blue threads at Jesus's hand drift gently within
  their own small area, never lowering and never reaching out along the road; a low
  thin haze of dust drifts along the empty road; no new stain, spot, or darkening
  appears anywhere on the page at any point.
- **Why kling:** the hand's rise-and-open is a completing gesture with a stated end
  (the question, asked with the hand); the 9.2s slot takes Kling's 8s (13% frozen)
  where veo's 8s would hold the hand where drawn. **Why he is drawn already facing the
  road:** LAW 1 — never turn a figure in a clip; F06 had him looking down, F07 has him
  turned; the turn happens on the page cut. **Refs:** jesus + samaritan_ref +
  samaritan_face_ref + village_edge_ref.

### F08 — "save this stranger" (14w · Stain D0 · Swirl 2 held · kling3_0, clip 5)

The word aimed at the man — presence after absence. Camera drops to the dust: a CLOSE
MEDIUM of Jesus's lowered hand, his face turned down to the man, the man's bowed back.
"Stranger" is Jesus's word of honor in the narration's reading; the drawing shows a
man being looked at, not a foreigner being pointed out.

- **Panels**
  1. `"not found"` — a far dust cloud hanging over an empty road, no figures *(varies
     F07's road-bend)*.
  2. `"give glory"` — a man's two raised open hands against the sky, clean, no face
     *(rhymes F05's panel 2 — what the one did)*.
  3. `"this stranger"` — the man's hand spread open on the dust, weathered, clean,
     unmarked, close *(a hand like any man's — no face-morph risk)*.
- **Main scene** — `CLOSE MEDIUM shot`, low, at the feet:
  > {JESUS_BUILD}, standing on foot on the dry road at the left, his face turned DOWN
  > toward the man at his feet, calm, his right hand lowered and open, palm toward the
  > man, not touching him — already lowered — his hands otherwise empty, touching no
  > one on this page, his face and lowered hand and sandaled feet fully inside the
  > frame; at his feet, {SAMARITAN_BUILD} prostrate, his bowed head and shoulders and
  > his spread hands on the dust large in the frame at the right, his forehead to the
  > ground a hand's width before the sandals, not touching them, his loosed lip-cloth
  > at his throat, his olive-grey mantle with its clay-red band across his back, fully
  > inside the frame, drawn with the same care and dignity as any figure; the ground
  > dry, no water anywhere; no road, no village, and no other figure needed in this
  > tight frame. No stain, ring, or grey blot anywhere in the paper. Stage 2 dosage,
  > held: a few soft blue threads rising UPWARD ONLY from the back of Jesus's lowered
  > hand into the air above it, their roots touching his hand and nowhere else, one
  > soft amorphous watercolor patch at their top (as before), touching only his hand
  > and the air, never descending toward the man's back, head, or hands, never
  > touching him; the man and the dust free of any ink of any kind.
- **material_closer:** "the soft blue threads at his lowered hand are the only unusual
  ink on the page, and the paper beneath the man is wholly clean."
- **Fence:** `none`
- **Caption:** `("save this stranger",)` *(KJV 17:18 verbatim contiguous, 3 — one line,
  Kling page; Jesus's voiced line)* · **Corner note:** `NOTE: he looked at him`
  *(§8 — or `NOTE: returned`)*
- **Panel motions:** (1) the hanging dust drifts and thins; (2) the raised hands hold,
  the light warming very slightly; (3) the spread hand lies still on the dust.
- **Main animation:** Jesus's eyes lower the last small distance to the man and hold
  there, his lowered open hand staying exactly as drawn and not reaching down, one slow
  breath, his lips staying closed and completely still — he is not speaking and his
  mouth does not move at all; the man's back rises and falls with one slow breath, his
  forehead staying to the dust, his spread hands still; the soft blue threads at
  Jesus's hand drift gently within their own small area, never lowering toward the
  man; no new stain, spot, or darkening appears anywhere on the page at any point.
- **Why kling, not veo, on a hold page:** close-up micro-motion is veo's OPEN item
  ("very little visible motion"); the gaze-drop is a small completing gesture Kling
  executes; and the 5.6s slot takes Kling's 5s (11%) where veo's 4s would leave 29%
  frozen. **Refs:** jesus + samaritan_ref + samaritan_face_ref + village_edge_ref.

### F09 — HERO — "thy faith hath made thee whole" (19w · Stain D0 · **Swirl 3 beginning** · kling3_0, clip 7)

The gospel pivot: Christ's own personal word — "Arise… thy faith hath made thee whole"
— the first time in the episode anyone's eyes meet. The man's face is drawn already
LIFTING from the dust; the clip completes the lift. The swirl begins to leave his hand
for the air above both of them. Faith and wholeness stay in ONE caption line.

- **Panels**
  1. `"Arise"` — Jesus's right hand extended low, open, palm UP, close, empty *(the
     raising as a hand; the anchor)*.
  2. `"go thy way"` — the dry road ahead, open and bright in morning light, no one on
     it *(his sending — the same road the nine took, now his)*.
  3. `"thy faith"` — a close study of the man's face, lifted, dust on his brow, eyes
     open on someone above him, contour steady *(samaritan_face_ref)*.
- **Main scene** — `MEDIUM shot`, low angle at the village edge:
  > the village edge (VILLAGE_EDGE_BUILD) at the left; {JESUS_BUILD}, standing on foot
  > at the wall's end, bent a little toward the man below him, his right hand extended
  > low and open, palm UP, in the gesture of raising — already extended, touching
  > nothing — his hands otherwise empty, touching no one on this page, his face on the
  > man, calm and kind, fully inside the frame; at his feet, {SAMARITAN_BUILD} rising
  > from his face — his forehead just lifted from the dust, his head coming up, his
  > eyes open and meeting Jesus's for the first time, his hands still spread on the
  > ground, his knees under him, his loosed lip-cloth at his throat, dust on his brow,
  > his olive-grey mantle with its clay-red band about him, fully clothed, fully inside
  > the frame, drawn with the same care, the same line weight, and the same dignity as
  > any figure on the page; the road beyond to the right running away empty into
  > morning light; the ground dry, no water anywhere. No stain, ring, or grey blot
  > anywhere in the paper. Stage 3 beginning dosage: the blue ink motif begins to
  > diffuse — a few soft blue threads rising UPWARD from the back of Jesus's extended
  > palm-up hand into the air above it, and for the first time one loose open band of
  > blue ink threads with traces of muted gold drifting high in the air above BOTH
  > figures, tied to no single figure, touching neither of them and nothing on the
  > ground, no longer one single thread but not yet filling the scene, behaving like
  > wet ink bled into the paper's sky wash, never a glow; the man, the dust, and the
  > road free of any ink of any kind; the threads never descending toward the man and
  > never rising from him.
- **material_closer:** "the blue threads at his extended hand and the loose band
  beginning in the air above both figures are the only unusual ink on the page, and
  the paper beneath the man is wholly clean."
- **Fence:** `none`
- **Caption:** `("thy faith hath made thee whole",)` *(KJV 17:19 verbatim contiguous,
  5 — one collapsed line, Kling page, ep7 F04's / ep10 F08's length precedent. NOT
  "made thee whole" alone: over a picture of the one man at Jesus's feet, a
  wholeness-only caption is the two-ranked-prizes reading this whole design exists to
  avoid — faith and whole stay in one breath, as Jesus said them)* · **Corner note:**
  `NOTE: Arise` *(KJV 17:19's first word)*
- **Panel motions:** (1) the palm-up hand holds, the light across it warming very
  slightly; (2) a thin banner of dust drifts across the bright road; (3) the sketched
  face blinks once fully — closes, then opens again fully, ending wide open.
- **Main animation (the Hem F05 recipe, tuned to this beat):** the Samaritan's head
  lifts the last small distance and holds, his eyes staying on Jesus's, his hands
  staying spread on the ground, his lips closed; Jesus's one small kind nod completes
  and holds, his extended palm-up hand staying exactly as drawn and not reaching
  further, his lips staying closed and completely still — he is not speaking and his
  mouth does not move at all; the soft blue threads at his hand drift gently within
  their own small area, and the loose band high in the air above both figures drifts
  smoothly within its own fixed band, never lowering onto either of them; no new
  stain, spot, or darkening appears anywhere on the page at any point.
- **Why kling:** two completing gestures (the head-lift ending eyes-on-Jesus, the kind
  nod); the 8.0s slot takes a 7s clip (13% frozen). **Why hero:** the gospel-pivot
  sentence, Christ personally naming faith and pronouncing wholeness, the two figures'
  eyes meeting for the first time, the swirl beginning to diffuse AT HIS WORD — not the
  emotional climax (F06, the fall and the loud voice), exactly as the locked rule asks.
  In this Swirls pipeline the covers bookend the cut; F09 is the hero still for any
  thumbnail / hero-bookend use. Alternate: F10. **Why "beginning" and not full Stage 3
  here:** a Kling page (the lift must complete) — a full Stage 3 band over-escalates on
  Kling; the "beginning" register was validated on Kling (F07 v2). **Refs:** jesus +
  samaritan_ref + samaritan_face_ref + village_edge_ref.

### F10 — "Luke calls it thanks. Jesus calls it faith." (23w · Stain D0 · **Swirl 3** · veo3_1_lite, clip 8)

The encounter complete: the man RISEN, standing whole, face to face with Jesus — the
only man in the story who sees his face up close. The narrator's summary over the
picture of what the return was for. The episode's Stage 3 page.

- **Panels** *(two responses, equal size, equal line, equal light)*
  1. `"kept walking"` — a single track of bare footprints in dry dust running straight
     away from the viewer over a rise, no figure *(the nine, as a track — no count)*.
  2. `"turned back"` — a single track of bare footprints in dry dust that doubles back
     on itself, the returning prints laid over the departing ones, no figure *(the one,
     as a track — the turn told statically)*.
  3. `"faith"` — Jesus's face, close, calm, his eyes on someone before him *(jesus_ref;
     small face → tone-only motion)*.
- **Main scene** — `MEDIUM TWO-SHOT`, the village edge:
  > the village edge (VILLAGE_EDGE_BUILD) at the left, the dry road running away to
  > the right; {JESUS_BUILD}, standing on foot at the wall's end facing right, square
  > and still, his right hand still open toward the man from the raising, low, not
  > touching him, his hands otherwise empty, touching no one on this page, fully
  > inside the frame; before him, {SAMARITAN_BUILD}, RISEN — standing upright on the
  > road facing LEFT toward Jesus, close, whole, his face bare and level with Jesus's,
  > his eyes on Jesus's eyes, his loosed lip-cloth hanging at his throat, his hands
  > open and empty at his sides, his skin clear, his rent tunic and olive-grey mantle
  > with its clay-red band as before, fully clothed, fully inside the frame, drawn
  > with the same care, the same line weight, and the same dignity as any figure on
  > the page; the road beyond him to the right empty in morning light; the ground dry,
  > no water anywhere. No stain, ring, or grey blot anywhere in the paper — the paper
  > wholly clean. Stage 3 dosage: the blue ink motif, with traces of muted gold, is
  > woven through the whole scene — threads drifting in one loose open band through
  > the air above the road and the village edge, over both heads, tied to no single
  > figure, touching no person, touching nothing on the ground, behaving like wet ink
  > bled through the page's own sky wash, never a glow.
- **material_closer:** "the blue-and-gold band woven through the air above both men is
  the only unusual ink on the page, and the paper beneath them is wholly clean."
- **Fence:** `none` *(D0 — the page-global no-new-stain clause is still stated)*
- **Caption:** `("Luke calls it thanks.", "Jesus calls it faith.")` *(narration verbatim,
  4+4; veo page — two lines OK; the same act under two names, neither ranked)* ·
  **Corner note:** `NOTE: face to face`
- **Panel motions:** (1) a thin banner of dust drifts across the straight track; (2) the
  doubled-back track lies still, the light across it warming very slightly; (3) the
  sketched face holds, tone-only.
- **Main animation:** the Samaritan's chest rises once in a slow breath and his open
  hands settle at his sides, his eyes staying on Jesus's, his lips closed; Jesus stays
  exactly as drawn, his open hand not moving, one slow breath, his lips closed and
  completely still — not speaking; the loosed cloth at the man's throat stirs faintly;
  the blue-and-gold ink threads drift smoothly within their own fixed band across the
  air above both heads, never lowering onto either figure; a low thin haze of dust
  drifts along the empty road beyond; no new stain, spot, or darkening appears anywhere
  on the page at any point.
- **Why veo (and why he STANDS rather than goes):** all holds plus fixed-band drift is
  veo's exact lane (ep7 F06's and ep10 F09's Stage 3 bands were veo); "go thy way" was
  received on F09 and the going belongs to the page turn — this page is the
  face-to-face, the thing the nine walked past. Positive-only light wording throughout
  (no glint/sparkle). **Refs:** jesus + samaritan_ref + samaritan_face_ref +
  village_edge_ref.

---

## 7. Assembly suggestions (word-proportional, Fable estimates)

202 words over 80.61s ≈ 2.51 words/sec (the three voiced quotes run at natural speed
with 0.4s pre-pauses — proportions are approximate as always). **Boomerang nowhere in
this episode**: every unit either walks in one direction, settles a completing gesture,
drifts a band, or drifts dust — all of which read backwards under reversal (a walk
reversing is the worst case of all — the nine would visibly "come back"). Every clip is
designed shorter than its slot (freeze pads, never trims — the standing swirls-freeze
lesson) except the front cover (§8); every frozen tail is under SW-F1's 35%. Final
modes are an assembly-QC call on the real renders — real playback, per the standing
rule.

| Unit | Words | ≈Slot | Clip | Model | Frozen | Suggested mode |
|---|---|---|---|---|---|---|
| front | 8 | 3.2s | 4s | veo | — | freeze (slot shorter than clip — ep10/Barrel precedent; §8) |
| f01 | 20 | 8.0s | 6s | veo | 25% | freeze |
| f02 | 18 | 7.2s | 6s | veo | 17% | freeze |
| f03 | 17 | 7.2s | 6s | veo | 17% | freeze (a walk — never boomerang) |
| f04 | 12 | 4.8s | 4s | veo | 17% | freeze (a walk — never boomerang) |
| f05 | 13 | 5.2s | 4s | kling | 23% | freeze + tail_loop ~1.0 (hands settle high) |
| f06 | 17 | 6.8s | 6s | kling | 12% | freeze + tail_loop ~1.0 (shoulders settle) |
| f07 | 22 | 9.2s | 8s | kling | 13% | freeze + tail_loop ~1.0 (hand settles open) |
| f08 | 14 | 5.6s | 5s | kling | 11% | freeze + tail_loop ~1.0 (breath settles) |
| f09 | 19 | 8.0s | 7s | kling | 13% | freeze + tail_loop ~1.0 (lift ends eyes-on-Jesus) |
| f10 | 23 | 9.2s | 8s | veo | 13% | freeze |
| back | 19 | 7.6s | 6s | veo | 21% | freeze (drifting dust — be safe) |

Sum 202 = the narration's own count; 80.61s locked audio + landing hold ≥3.0s
(INV-26). Lane split: 5 kling (the completing-gesture pages F05–F09) / 5 veo pages +
2 veo covers — veo-first where the shot allows it, including both walking pages
(continuation, not completion). The OpenArt bridge has no veo model — `model_tier` is
advisory there and everything renders via Kling unless the user explicitly sets
`SWIRLS_GEN_PROVIDER=hf` for a specific clip (ep7 F04's documented one-off exception,
never a policy change). Under Kling-only, re-check the two Stage-3 pages (F09, F10)
for band over-escalation on the contact sheet — that is the one place the advisory
tier actually changes the risk. Credits, not dollars, are estimated here; the ledger
(`/cost`, `/spend`) is the only truth.

**Render/spend order** (refs gate everything — §3): F02 → crops → F05 → crops → F01,
F03, F04, F06–F10, covers. Animate nothing until every still has passed the eye-QC
(count first, then baked text, likeness, layout, dose, no un-requested text, every
MUST-SHOW in frame) and the LAW 4 referent check against the rendered pixels.

---

## 8. OPEN QUESTIONS (do not silently resolve)

1. **Back-cover title length** — `AT HIS FEET, NOT ON THE ROAD` (7 words, the
   narration's final clause verbatim, and it reads directly on the feet-and-road
   picture) vs `GO BACK AND FIND HIM` (5, the CTA itself, verbatim contiguous) vs `AT
   HIS FEET` (3). Seven is the longest back-cover line the series has tried (ep1: 4,
   ep10: 5). I recommend the seven-word line; fall back in that order if the woodcut
   lettering crowds or misspells.
2. **Back-cover subtitle** — `EPHESIANS 2:8` (recommended: the doctrine the narration
   fought six panel-rounds to hold — saved through faith, as gift, not of works) vs
   `JOHN 6:37` (the welcome — "him that cometh to me I will in no wise cast out," the
   stranger received) vs `LUKE 17:19` (the episode's own verse — but the cover doc asks
   for the verse the thread points TO, not the one it is). All three are real; the first
   is the thesis, the second is the CTA's promise.
3. **Front-cover slot shorter than its clip (3.2s vs 4s).** ep10 and the Barrel shipped
   this exact case as "freeze (trims)"; the memory note says freeze pads and never trims
   and to use boomerang instead. The two precedents disagree on paper. Recommend: keep
   freeze and let the assembler's real behavior decide at assembly QC — a 0.8s trim on a
   cover hold is harmless either way; a boomerang on stirring cloth is not. If the
   assembler genuinely cannot trim, move to the 16-word front (`Jesus told ten men with
   leprosy to go — before a single one of them was healed`, 6.4s, veo 6) and F01 drops
   to 12w/4.8s (veo 4) — one line to change each.
4. **seq_title `WHERE ARE THE NINE` (4 words).** The Bier ran 4 words; if the top-left
   lettering crowds on 9:16, fallback `THE NINE`.
5. **The count trap.** Ten figures on four pages and a cover, nine + one on F05, ten
   tiny figures in F07's panel 1. Image models miscount groups above ~5 routinely. Every
   group page states "exactly ten — count them"; the eye-QC counts first. Budget regens
   for it (I expect F02/F01 to need at least one). Fallback if a page will not hold ten:
   make the group a tighter huddle where some men are partly hidden behind others (the
   count reads as "a company," not as a row of ten to be tallied) — but F05's nine + one
   and F07's panel 1 must stay countable, because those numbers ARE the episode.
6. **Chaining `samaritan_ref` into the group pages (F01, F03, F04).** Intended so the
   band-mantled man is findable in the huddle. Risk: the model pastes his face onto
   several of the ten. Each group page states "exactly one of the ten… matches the
   attached reference; the other nine are different men." If a render duplicates him,
   drop his ref from the group pages (he stays findable by the mantle band alone) and
   accept that his face is un-pinned until F05.
7. **`ten_ref` as a LOOK ref for an unindividuated group** is new practice (ep10's room
   ref pinned a location; this pins a costume-and-condition on nine faceless men). If it
   fights the count or individuates faces on chaining, drop it and rely on the verbatim
   TEN_BUILD text — the group's look is more text-pinnable than a face is.
8. **Three Stage-1 pages in the middle (F03–F05) and one thread that changes anchor**
   (his hand → the sky from the left edge → the sky over ten). The anchor change is the
   locked note's mechanism, reasoned in §2; it needs the user's eye at F04's first
   render: does a single sky-line entering from the left READ as "his word with them,"
   or does it read as a stray decorative line (the Thomas F01 open question — a
   placement that only makes sense in prose)? Fallback if it reads as decoration: on F04
   and F05 anchor the thread to the far-LEFT horizon where the village is (rising from
   the point on the horizon where he stands off-frame), still one thread, still
   touching nothing — a visible root instead of a frame edge.
9. **F05's "loud voice" with a closed mouth.** Designed for NO_MOUTH and the face-ref
   crop (open eyes, closed lips). If on watch the page reads as too quiet for "with a
   loud voice glorified God," the fallback is a head-back, eyes-shut, open-mouthed
   shout on a REGEN of the still after the face ref has been cropped from the first
   approved render — never animate the mouth either way.
10. **The nine's costume after cleansing** — rent tunics stay rent (can't un-rend), lip
    cloths loosed at the throat, bare heads. A model may "heal" the garments too (whole
    tunics) on F04/F05. Acceptable variance if it does; regen only if the cloths come
    back UP over any mouth (that reverses the literal cleansing sign).
11. **F04's corner note `NOTE: not in frame`** is the locked note in the page's own
    production voice — witty on a found storyboard page, but a repeat viewer might read
    it as an error confession. Fallback `NOTE: on the road` (KJV-adjacent, narration
    verbatim from the hook). User's call.
12. **F08's corner note** — `NOTE: he looked at him` (4 words after NOTE — the longest
    note in the episode) vs `NOTE: returned`. Recommend the shorter if the first
    misrenders.
13. **The Samaritan's mantle band is clay-red.** Chromatic reservation is clean (no
    blue; red is allowed outside a stain, and from F05 there is no stain). ep10's
    madder-red mantle risked the "scarlet woman" cliché; here a narrow band on a
    forty-year-old man carries no such prior. If a render inflates it to a whole red
    cloak, regen — the band is a pin, not a costume.
14. **F02 triple debut** — the ten, the Samaritan-among-them, AND the village edge all
    crop from one approval (three refs). Budget two regen cycles. Alternative (new
    practice, not recommended): a standalone group render before F02.
15. **Hero nomination = F09** — for the main engine's hero-bookend rule and any
    thumbnail; the Swirls assembly itself bookends with the covers. Alternate F10 if the
    user prefers the face-to-face over the word.
16. **Nothing on any page shows the priests, the temple, or Gerizim** — deliberate. The
    Samaritan/Jew question at the priests is a commentary rabbit-hole the narration
    never enters; the "priests" panel (F03) is a neutral far walled town. Listed so the
    implementation pass never adds a shrine.
17. **Leprosy skin wording** — my design intent is stated in §2 (faint dry-brush
    patches, never sores/gore/grotesque). ep4 Naaman's episode.py is the series' only
    prior leprosy render; if it carries a validated skin-wording string, use it verbatim
    over mine.

