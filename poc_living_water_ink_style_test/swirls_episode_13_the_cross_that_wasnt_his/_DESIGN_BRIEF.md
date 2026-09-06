# DESIGN BRIEF — Episode 13, "The Cross That Wasn't His"

Mark 15:20-21 + Luke 23:26 (Simon of Cyrene compelled to bear the cross) read through
Hebrews 13:11-13 (the sin offering burned "without the camp" → Jesus "suffered without
the gate" → "let us go forth therefore unto him") · Dead ink: **NONE — no Stain, no
Fray, on any page** (reasoned in §2: nobody in this text is marked unclean, guilty, or
wavering; the sin the offering covers is "the people's," corporate and off-page; a stain
on Simon would say "guilty," which is exactly the doctrine error the narration's fence
exists to prevent, and a fray would say "doubting," which the text never gives him) ·
NT episode, Jesus bodily in frame on the gate pages (F01-F03, F06) and present only as a
small led figure AHEAD on the road pages (F07, F09), absent from F04-F05 and F08 —
this episode's human protagonist is Simon, and Jesus is present mostly by
*direction* (he went out first) · Stage 3 is reached on the last three pages, beginning
exactly where the narration "turns to you" · `panel_style` **woodcut_hybrid**
throughout · Voices: **narrator only** (voices.json — every KJV line is narrator-read;
no NO_MOUTH assignment anywhere, but every figure's lips stay closed on every clip).

Fable design pass, 2026-09-06. This brief is the single creative source for the Sonnet
implementation pass (episode.py PageSpec/CoverSpec objects). Narration and audio are
LOCKED — **227 words** (my own count of `narration.md`; the handover said ~220),
**103.44s natural, `narrator_atempo_factor 1.0`** (no time-stretch), one narrator turn,
no pre-quote pauses (no second voice). Nothing here changes a spoken word. Every choice
states its WHY. Open questions are flagged inline and collected in §8 — do not silently
resolve them.

**Two things changed since ep11's brief and are folded in everywhere below, not
patched on:** (1) the provider is **OpenArt** — every still and every clip renders
through the bridge, there is no veo model, and `model_tier` is *advisory only* (stated
per page as the ideal lane, exactly as ep11 did; everything actually renders on
Kling 3 Omni unless the user explicitly opts a clip back to Higgsfield — not a call this
brief makes). (2) **Still-model tiering is LOCKED**: `still_model="nano-banana-pro"`
(40cr) is the default and MANDATORY for crowd/complex content; `"seedream-4-5"` (15cr)
is a real per-page option for calm, non-crowd content — a single figure or a close
pair. This episode has at most four figures on any page and several single-figure
pages, so the call is made page by page in §6 with its reasoning, the same way
`model_tier` is.

---

## 0. The shape of the episode, in one paragraph

The narration is built on a single road with two directions on it — "Jesus, out of the
city. Simon, in from the country. Same road." — and on one doorway that the whole of
Hebrews 13 turns on: the GATE, the line between *inside* (the sanctuary, the camp, the
city) and *outside* ("without"). So the episode's geometry is fixed on every page: **the
camera stands OUTSIDE the city, the wall and its gate at the frame's LEFT, the road
running away to the RIGHT into open country; IN is left, OUT is right, on every page
and in every panel — including the Old-Testament panels, where the blood is carried
LEFT into the tent and the carcass is carried RIGHT out of the camp.** Jesus is led out
left-to-right; Simon walks in right-to-left; they meet at the threshold; Simon turns
on the page cut (F02→F03, never inside a clip) and from then on everyone on the page
faces right. Nine interior pages: the three prose paragraphs after the hook each split
into three at their own picture-changes (the approach / the seizure / the turn · the
word / the type / the antitype · the address / the carrying / the call), with the hook
on the front cover and the fence on the back. The episode's first hard problem — three
citations from three books stacked so fast a cold ear loses which voice is speaking —
is solved by giving each register its own native layer of the page: **the Old-Testament
type lives ONLY in the carved woodcut panels** (older, harder, block-printed — it never
enters a main scene), **the road and the event live ONLY in the washed main scene**
(the sanctuary, the camp, and Golgotha are never a main scene, ever), **and the address
to the viewer is carried by the camera itself turning to look OUT along the road from
the viewer's own feet on the last three pages** — the "Hebrews turns to you" beat is a
literal camera turn, and the captions turn with it ("Let us go forth" / "You are
asked"). A corner note `NOTE: Hebrews 13` on the sin-offering page does by eye the
attribution the panel said the ear lost. The second hard problem — "outside is
'without'" is a lesson about a WORD — is solved by a page whose three carved panels are
the same doorway seen from inside, at the threshold, and from outside, labeled
*inside / the gate / without*, under a caption that is the narration's own equation.
The third — Simon's carrying must picture REPROACH and never re-enact the atonement — is
a locked drawing rule (§2): one plain rough beam (never a crucifix shape), laid on
Simon by the SOLDIERS' hands and never by Jesus's, no blood or nails or inscription on
the wood ever, no execution place ever in frame, no mark of any kind on Simon, and the
living ink never on the beam or on the man who carries it. The swirl's anchor is **the
gate's threshold stone** — the line Jesus crossed first on F01 (his foot on it, going
out), the line Simon crosses after him on F03 (the first thread rises from the stone his
heel is leaving, its tip leaning outward), the doorway that holds the Stage 2 bloom
while Hebrews explains what crossing it meant (F04-F06), and the place the band leaves
on the camera turn to fill the open air above the road ahead (F07-F09). Covers: front =
Simon large, walking LEFT along the road toward the gate, empty-shouldered, while far
at the left in the gate's cold opening the tiny procession comes out the other way (the
hook's literal picture); back = the same gate at dusk, EMPTY, two lines of footprints
running out from its threshold, one a pace behind the other, and one small hard-capped
curl rising from the threshold stone ("He went out through that gate first"). Swirl
arc 0·0·1·2·2·2·3b·3·3; no dead ink; hero = F06 (Hebrews 13:12 — Christ's own atoning
act named, Jesus a pace ahead of the man who follows him out).

---

## 1. Narration beat map → units (why nine interior pages)

Word counts are a deterministic whitespace count of the locked text (paragraphs
14 / 68 / 70 / 75 = **227**; 103.44s ≈ **2.19 words/sec, 0.456 s/word** — the slowest
delivery in the series, natural speed, reflective register). The assembler treats the
weights as proportions, same as every precedent episode; **real slots come from the
alignment timestamps at the score/assembly stage (the ep11 lesson — see §7), so every
clip below is designed with ≥0.4s of headroom under its estimated slot.** One narrator
turn, 103.43s final, no quote pauses.

| Unit | Narration beat | Words | ≈Slot | Voice |
|---|---|---|---|---|
| **front** | "The man who would carry the cross of Jesus was walking the other way." | 14 | 6.4s | narrator |
| **F01** | "Mark says the soldiers 'led him out to crucify him. And they compel one Simon a Cyrenian, who passed by, coming out of the country.'" | 25 | 11.4s | narrator (KJV) |
| **F02** | "Jesus, out of the city. Simon, in from the country. Same road. They put the cross on Simon's back. Nobody asked him." | 21 | 9.6s | narrator |
| **F03** | "Luke says, 'on him they laid the cross, that he might bear it after Jesus.' Simon turns, and walks out too." | 22 | 10.0s | narrator (KJV) |
| **F04** | "Now he is through the gate. In the King James Bible, outside is 'without.'" | 14 | 6.4s | narrator |
| **F05** | "The sin offering, an animal killed for the people's sin, had its blood carried into the sanctuary, God's holy tent. Its body went out, burned 'without the camp.'" | 28 | 12.8s | narrator (KJV) |
| **F06** | "Then it says of Jesus: 'Wherefore Jesus also, that he might sanctify the people with his own blood, suffered without the gate.' Out there, where Simon is walking." | 28 | 12.8s | narrator (KJV) |
| **F07** | "Hebrews turns to you: 'Let us go forth therefore unto him without the camp, bearing his reproach.'" | 17 | 7.7s | narrator (KJV) |
| **F08** | "Reproach is shame. Bearing it is carrying it, as Simon carried the wood." | 13 | 5.9s | narrator |
| **F09** | "Simon was forced out. You are asked. Turn on your own road, and carry his shame after him, freely this time." | 21 | 9.6s | narrator |
| **back** | "Only the shame. He went out through that gate first, and the atoning, the dying, the finishing, that was his, with his own blood." | 24 | 10.9s | narrator |

Sum 14+25+21+22+14+28+28+17+13+21+24 = **227** = the file's own count.

**Why the paragraphs split 3 / 3 / 3.** Paragraph 2 (68w ≈ 31s) holds three pictures
the text itself separates: the two-direction APPROACH (Mark's verse — "led him out" /
"coming out of the country"), the SEIZURE at the gate ("They put the cross on Simon's
back. Nobody asked him." — the beam on a man still facing the way he was going), and
the TURN ("Simon turns, and walks out too" — the same man now facing the other way).
The seizure and the turn MUST be two pages because in this series a figure never turns
inside a clip (LAW 1): F02 draws him facing LEFT under the beam; F03 draws him facing
RIGHT under it; the page turn IS Simon's turn. Luke's verse rides on F03, not F02,
because "that he might bear it AFTER Jesus" is the turned man's picture, not the seized
man's. Paragraph 3 (70w ≈ 32s) splits at its three registers: the WORD ("outside is
'without'" — a lesson, F04), the TYPE (the sin offering — Old Testament, F05), the
ANTITYPE ("Then it says of Jesus… suffered without the gate" — F06). These are the
three voices the review panel said a cold ear conflates; giving each its own page is
the first half of the fix (the second half is §2's register rule). Paragraph 4 (75w ≈
34s) splits at the ADDRESS ("Hebrews turns to you" — the camera turns, F07), the
CARRYING ("Bearing it is carrying it, as Simon carried the wood" — a close on the
beam, F08), the CALL ("You are asked. Turn on your own road" — F09), and the FENCE
("Only the shame… that was his, with his own blood" — the back cover, the empty gate).
**Why the hook is 14 words on the front:** the Bier's front carried 23, ep11's 8;
14w/6.4s is inside precedent, and the hook's own picture (a man walking the other way)
is a cover picture, not a page. **Why the landing is 24 words on the back:** ep7's back
carried 34; the fence sentence is the episode's own closing caption ("through that gate
first") and belongs over the empty gate. **Why not eight:** the only candidate merge is
F07+F08 (30w, 13.7s) — it would bolt the camera-turn wide onto the close-on-the-wood,
two pictures, AND it is the only place the drawing can insist at close range that the
thing on Simon's shoulders is a plain beam with nothing on it (hard problem #3 needs
that close). It would also push one clip to ~13s on Kling, past the series' proven 10s.
**Why not ten:** F08 (13w/5.9s) and F04 (14w/6.4s) are already at the series' floor
(ep11's F04 at 12w/4.8s); splitting F01 at "crucify him." leaves a 9-word page, and
splitting F05 or F06 re-joins nothing the eye needs separated. The story's beats and
the freeze cap agree on nine.

---

## 2. The three hard problems, the dead-ink decision, then the motif arc

### Hard problem #1 — three books in forty seconds: the REGISTER rule

The final panel round flagged it from three directions (cursor: "rapid typology stack";
grok: "'Then it says of Jesus' — *it* who? … a cold ear hears Leviticus say 'Wherefore
Jesus also'"; codex: the Simon↔Hebrews join is "unmarked"). The narration is locked, so
the EYE has to carry what the ear drops. The page template already has three native
layers with three different visual characters, and the fix is simply to never let a
register leave its layer:

| Register | Layer of the page | Why it fits | Never |
|---|---|---|---|
| **The Old-Testament TYPE** (sin offering, blood carried in, body burned without the camp) | **the three carved woodcut PANELS only** — F05's whole panel row, F06's panel 1 | the hybrid panels are literally an older, harder printing register (block-cut, dense, "cuts"); the type reads as the older pattern set beside the living page | never a main scene; never in the ink-wash register; never on a page after F06 |
| **The EVENT / the antitype** (the road, the gate, Simon, Jesus led out) | **the washed MAIN SCENE only** | the gentle living wash is where the story happens *now* | never the sanctuary, never the camp, never Golgotha or any execution place — the main scene is the road outside the gate on every single page |
| **The address to YOU** ("Hebrews turns to you… Let us go forth… You are asked… Turn on your own road") | **the camera turning** (F07-F09 look OUT along the road from the viewer's own feet) **+ the captions** on those pages | the viewer is put on the road; the handwriting stops quoting and starts inviting | never before F07 — the first six pages are watched from the side |

Two extra eye-cues for the attribution the ear lost: F05's corner note is
**`NOTE: Hebrews 13`** (the sin-offering page names its own source while the narrator
says "The sin offering…"), and F06's panel row is the visual bridge itself — panel 1
the camp's edge with the burning place OUTSIDE it, panel 2 the city's gate with the road
OUTSIDE it, drawn to the same layout (inside left, outside right), panel 3 Jesus's face
("Jesus also"). The eye sees camp = gate = the same outside, which is Hebrews' whole
argument, before the narrator finishes the verse. **Rule for the implementation pass:**
no panel on F01-F04 or F07-F09 may show sanctuary/camp/altar/priest content; the type
appears exactly where it is heard (F05) and where it is joined to Christ (F06 p1), and
nowhere else.

### Hard problem #2 — "outside is 'without'": a page about a WORD

An abstract translation note cannot be staged as action, and this style's own strength
is baked lettering. F04's three panels are one doorway seen three ways — from INSIDE
(the shadowed lane looking out to light), AT the threshold (the worn stone across the
doorway's foot), from OUTSIDE (the gate's outer face, the road beginning) — labeled
`inside` / `the gate` / `without`, and the caption beneath the main scene is the
narration's own equation, `outside is without` (3 words, verbatim; the quote marks are
dropped — punctuation is the known baked-text failure zone, and ep11's F05 caption
dropped its comma the same way). The word appears twice on one page, once as a carved
label over a picture of the outside, once in the running hand — the equation is done by
adjacency, no diagram, no arrow. The main scene is Simon just outside the gate, so the
whole page IS the word.

### Hard problem #3 — Simon's carrying pictures REPROACH, never the atonement (LOCKED drawing rules)

The narration's fence — "Only the shame. He went out through that gate first, and the
atoning, the dying, the finishing, that was his, with his own blood" — has to be as
unmissable in the pictures as in the text, because two reviewers heard the risk in the
words alone (grok: "the script uses that wood as the shame-picture, then yanks the
atonement off it"; codex: "'carry his shame' can imply participation in bearing
Christ's guilt"). These hold on every page that shows the beam (F01-F09, both covers):

1. **The object is a plain BEAM, never a crucifix.** One straight rough-hewn timber
   across the back of the shoulders (the honest historical object, and the narration's
   own word — "as Simon carried the wood"). Never a full cross shape, never a
   crosspiece joined to an upright, never dragged, never an upright post. The KJV
   captions keep the word "cross"; only the drawing is corrected — ep7's bier-not-coffin
   precedent verbatim. (§8: the user may prefer the popular full-cross image; my
   recommendation is the beam.)
2. **Nothing is ever on the wood.** No nails, no rope, no inscription or titulus, no
   blood, no marks. The wood is plain ochre-umber with no blue and no gold on it
   anywhere. "With his own blood" is the narration's word for the atonement and belongs
   to the back cover's lettering, not to any drawn object.
3. **The SOLDIERS lay it on him; Jesus never does.** Luke's own grammar — "on him THEY
   laid the cross." F02's still puts both of one soldier's hands on the beam pressing it
   onto Simon's shoulders; Jesus stands a few steps ahead, unburdened, facing the road,
   touching no one. A render in which Jesus hands, passes, or looks back over the beam
   to Simon is a regen — it would draw Christ delegating his atonement.
4. **No execution place, ever.** No hill, no crosses, no crowd at the road's end, no
   skull-shaped anything (the Gold Exemplar's literalism lesson) — on every page the road
   simply runs out of frame at the right or over a crest. Jesus "suffered without the
   gate" is heard over a picture of the road, with Jesus led AHEAD, never at the site.
5. **No mark of any kind on Simon.** No stain (below), no wound, no blood, no bound
   wrists — he is a countryman with a beam on his back. He is never drawn ON the ground,
   never drawn falling, never drawn in a Via-Dolorosa pose. He carries; that is the whole
   picture.
6. **The living ink is never on the beam or on the man who carries it.** The swirl's
   anchor is the gate's threshold stone (below), then the open air; it never rises from,
   touches, or descends toward the beam, Simon, or Simon's hands. A thread on the wood
   would say "the life is in the carrying" — the works reading the narration fences.
7. **Jesus under the beam (F01 only) keeps the series' restraint:** his own clothes
   (Mark 15:20's own detail — JESUS_BUILD verbatim), head bare, no crown of thorns
   drawn, no wounds or blood, no rope on his wrists, walking upright at an even pace, a
   soldier's hand on his upper arm. (§8: the crown — v17 puts it on, the text never
   says it came off; I choose restraint and the "put his own clothes on him" line.)

### Dead ink — reasoned, not defaulted: NONE

- **Stain on Simon — REJECTED, and it would be a doctrine error.** The Stain is
  sin/guilt/uncleanness IN a figure. Nothing in Mark, Luke, or Hebrews marks Simon as
  sinful, unclean, or guilty; "reproach" (13:13) is Christ's disgrace shared by
  identification, not the bearer's own guilt. A blot under Simon would draw exactly the
  confusion the fence exists to stop ("carry his shame" = carry his guilt).
- **Stain under the sin-offering carcass (F05 panel 2) — REJECTED.** The Stain's whole
  grammar is IN-the-paper, crossing the page's margin, under the main scene's linework;
  it has never been drawn inside a woodcut panel, and a grey blot in a dense-hatched
  block-cut would read as shadow. The type is carried by the carcass carried OUT, not by
  a motif.
- **Stain on Jesus — REJECTED, obviously,** and stated so no "sin-bearer" reading ever
  tempts a render toward it: the paper under Jesus is wholly clean on every page.
- **Fray on Simon — REJECTED.** "They compel" / "Nobody asked him" is compulsion, not
  fear or doubt. A tremored contour on him would say "wavering," which the text never
  gives; he is drawn in the same steady, confident, single-struck line as every figure
  on the page, stated on every Simon page (the standing steady-line override).
- **What carries the tension instead:** DIRECTION (a man facing the wrong way under a
  beam on F02, the right way on F03) and WEIGHT (the beam's size against his shoulders,
  the bent neck, the gripping hands). Both are story geometry, not motif.

Consequence for the code: `fence_kind="none"` on every page; every page's
`main_scene_animation` still ends with the page-global no-new-mark clause ("no new
stain, spot, or darkening appears anywhere on the page at any point"), as ep11's D0
pages did — the Hem lesson that a page's own aging is a stain-capable material with no
drawn stain to fence.

### Swirl (living blue-gold ink) — rising, anchored to the THRESHOLD

| Page | Stage | Anchor |
|---|---|---|
| front | none | Covers carry no interior motif; the lighting law carries the tension |
| F01 | **0** | Absence stated — a Roman execution detail; Jesus's foot on the threshold stone going out, no ink on it yet (the seed, unlit) |
| F02 | **0** | Absence stated — "Nobody asked him"; an imposition, not a gift |
| F03 | **1** | Exactly one thread rising from the worn THRESHOLD STONE of the gate — the stone Simon's rear heel is just leaving as he steps out after Jesus — up into the air of the doorway, its upper end leaning RIGHT toward the road; touching only the stone and the air; never the beam, never any figure |
| F04 | **2** | A few soft threads rising from the threshold stone into the gate's open doorway behind Simon, and one small amorphous watercolor bloom hanging in the air of the doorway, contained within the opening; "without" is where the life is |
| F05 | **2 held** | Same, the gate now small at the far left; the doorway's threads and bloom small with it; NO blue in any of the three type panels |
| F06 | **2 held — the hero** | Same, the gate at the far-left edge; the ink stays in the doorway while Hebrews names what crossing it meant; the road, Jesus, Simon, and the beam free of any ink |
| F07 | **3 beginning** | The camera has turned; the gate is behind the viewer. For the first time one loose open band of blue threads with traces of muted gold drifts high in the air above the road ahead, stretching from above the near road toward the far crest where the road goes out of sight — tied to no figure, touching nothing on the ground, never on the beam |
| F08 | **3 held (crop-limited)** | A close profile with sky above him: a few threads of the same band cross the top of the frame high above the beam and his head, touching nothing |
| F09 | **3** | Diffused: blue-and-gold threads in one loose band through the whole upper air above the road from the near foreground to the far crest, touching no person, never on the beam, never on the ground — the invitation open outward |
| back | curl | One small hard-capped hooked curl rising from the THRESHOLD STONE of the empty gate — from the line he crossed first — never from the footprints, never from the road beyond |

- **Why the threshold, and not his hand (ep7/ep10/ep11's proven root):** Jesus's hands
  are on the beam on F01 and he is ahead, a led figure, from F02 on — a hand anchor has
  no continuous root here. Not the beam (rule 6 above). Not Simon (never a person). The
  text's own hinge noun is the GATE — "suffered without the gate," "went out through
  that gate first" — and Hebrews' whole argument is about which side of a line the
  sin-bearing happened on. The threshold stone is that line, drawn. It is static and
  in-frame on F01-F06 (LAW 2 safe — no moving target), it is never a person or a burden
  (fence-safe), and a doorway with living ink standing in its opening reads on its own
  as "something went through here / this is the way" with no prose to lean on (the
  Thomas F01 lesson). F01 plants it unlit under Jesus's foot; F03 lights it under
  Simon's heel; the back cover's curl rises from the same stone. One root, whole episode.
- **Why the ink leaves the gate on the camera turn (F06→F07) and not before:** Stage 3
  is "the direct address" in the locked arc, and the address IS the camera turn. Two
  meanings on one cut — "Hebrews turns to you" and the life opening outward — read as
  one event. It also keeps the hero (F06) at Stage 2: a Kling page (its gaze-lift must
  complete) carrying a contained doorway dose is the lower-escalation shape (ep10 F08's
  hero was Stage 2 held for the same reason).
- **Why the band stretches toward the crest, static:** LAW 2 bans routes; the still's
  own geometry (band from near-road toward far-crest, where Jesus went) tells the
  direction "unto him" so the clip only ever drifts it in its fixed band. F07-v2's
  sky-band grammar, validated on Kling.
- **Kling-only caution (this episode's real risk from the advisory tier):** F07-F09 are
  three consecutive Stage-3 pages on Kling. ep11 had two. The band clause is verbatim
  the validated fixed-band form on every one, the F09 dose is the only "whole air"
  dose, and the contact sheet on each is checked for growth before the next is spent.

### High-tide check, every page (`stainDose + swirlStage <= 4`)

Trivially satisfied — no stain anywhere — but recorded so the gate has a row per page:

| Page | Stain | Swirl | Sum | Note |
|---|---|---|---|---|
| F01 | 0 | 0 | 0 | ✓ |
| F02 | 0 | 0 | 0 | ✓ |
| F03 | 0 | 1 | 1 | ✓ — the crossing point is the TURN, not a stain clearing: swirl > 0 for the first time as Simon faces out |
| F04 | 0 | 2 | 2 | ✓ |
| F05 | 0 | 2 | 2 | ✓ — three type panels with zero blue |
| F06 | 0 | 2 | 2 | ✓ |
| F07 | 0 | 3b | 3 | ✓ |
| F08 | 0 | 3 | 3 | ✓ — crop-limited |
| F09 | 0 | 3 | 3 | ✓ |

**The gospel turn = F03**, "that he might bear it after Jesus" — the first blue in the
episode rises the moment a man faces the way Christ went. Not when he is loaded (F02,
an imposition — no ink), not when he understands (he never does, on the page — Hebrews
does the understanding for him three pages later).

### The DIRECTION guard — this episode's literalism trap (the Barrel's "barrel," ep11's "ten")

Every page states which way each figure FACES. Jesus faces/moves RIGHT (out) on every
page he is on. Simon faces LEFT (in) on the front cover, F01, and F02; RIGHT (out) on
F03-F09. A render with Simon facing the wrong way on F02 or F03 breaks the turn and is
a regen before anything else is checked; the eye-QC checks direction FIRST on every
page (§5).

---

## 3. Refs — who and what needs pinning

All new refs live in this episode folder's `refs/`
(`F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_13_the_cross_that_wasnt_his\refs\`).
Chain order is hard (render_still stops on a missing ref).

### Characters

**JESUS** — SERIES CONSTANT. **Already in place:**
`F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_13_the_cross_that_wasnt_his\refs\jesus_ref.png`
(the same approved crop ep10/ep11 used). No redesign, no approval cycle. JESUS_BUILD
reused verbatim from ep11's §3 / ep10's episode.py:

> Jesus, a Judean man in his early thirties, medium height and ordinary build,
> sun-browned skin, shoulder-length dark brown hair pushed back from his face, a
> short full dark beard, wearing a simple ankle-length robe of undyed cream-brown
> wool with a plain olive-toned mantle draped over one shoulder, a narrow rope belt,
> and flat worn leather sandals -- no halo, no glow, nothing in his dress
> distinguishing him from the men around him, standing square, still, and
> unhurried, his gaze steady and direct

**Per-page guard, every Jesus page (this episode's "coffin" — the PASSION-PRIOR trap):**
the image model's prior for "Jesus + soldiers + cross + road" is the Via Dolorosa —
crown of thorns, blood, a fall, a full cross dragged, a wailing crowd, Renaissance
staging. None of that is in these two verses or in this narration. State on every Jesus
page: *"his head bare, no crown of thorns, no wounds or blood anywhere, no rope on his
wrists, walking upright at an even pace, his face calm and set toward the road ahead,
in his own clothes; a soldier's hand on his upper arm is the only hand on him; he
touches no one on this page and never looks back."* **Touch geography for THIS story:**
Jesus is touched by the soldier who leads him (the text: "led him out") and by nothing
else; Simon and Jesus never touch, never speak, never meet eyes on any page — the text
gives no exchange between them, and drawing one would invent a relationship moment
(Luke's only words on the road are to the daughters of Jerusalem, 23:28, which this
narration does not use). The beam passes between them only by the soldiers' hands
(§2 rule 3). Second prior, same guard: no glow, no radiance, no light on his face
different from the light on Simon's — the template's "no glowing spiritual VFX" plus
the dose language handle it; eye-check every Jesus page for a glow leaking into the
doorway dose.

**Where Jesus actually appears, and at what size** (the honest read the handover asked
for): F01 (in the doorway, medium, under the beam), F02 (a few steps ahead, medium,
unburdened), F03 (a few paces ahead outside, medium-small), F06 (a pace ahead of Simon,
medium — the hero), F07 and F09 (far ahead on the road, small, his back to the viewer),
front cover (tiny, in the gate's cold opening). NOT on F04, F05, F08, or the back
cover. Four full-figure pages, two small-figure pages — fewer Jesus-figure pages than a
typical episode, and correctly so: the narration's focus is Simon, the gate, and the
typology; Jesus is present by direction ("after Jesus," "unto him," "he went out
through that gate first"), and the drawing keeps him AHEAD, never face-on to the
viewer after F01.

**SIMON OF CYRENE** — new to the series; the human protagonist. The narration calls him
"the man," "Simon," "one Simon a Cyrenian," "coming out of the country." Build text
(use verbatim):

> Simon of Cyrene, a broad-shouldered countryman of about forty, thick-armed and
> strong-backed from field work, deep sun-browned skin, a wide square face with a
> heavy jaw, a broad straight nose, calm dark eyes under level brows, a short dense
> black beard, close-cut black hair under a plain undyed head-cloth tied at the
> nape; wearing a knee-length coarse tunic of undyed oatmeal wool with a rope belt
> and a short mantle of undyed wool with one narrow rust-red stripe along its edge
> worn over his left shoulder, bare dusty legs, flat worn leather sandals; his ONLY
> distinguishing marks are the plain head-cloth and the single rust-red stripe, and
> no other figure on this page, including Jesus and the soldiers, ever wears a
> head-cloth or that rust-red stripe; drawn in the same steady, confident,
> single-struck line, with the same care, the same line weight, and the same dignity
> as every other figure on the page

**Why this build:** "coming out of the country" (Mark's *ap' agrou*, from the field) —
a working man, not a pilgrim in white, not a disciple, not a soldier; strong enough
that a Roman picked him to carry a beam. The head-cloth is a field-worker's sun-cloth
(state "tied at the nape, not a turban, not a hood") and is the one thing on his
head that Jesus (hair pushed back, bare-headed) and the soldiers (helmets) never
share — so at any distance the head tells you which walking man is Simon. The rust-red
stripe is the ep10/ep11 band pattern (a pin, not a costume). **The 2026-09-05
one-figure-only-mark rule is applied twice, verbatim,** because the Seedream bake-off
leaked exactly this kind of mark onto Jesus: the clause "no other figure on this page,
including Jesus and the soldiers, ever wears a head-cloth or that rust-red stripe" is
in the build text itself and travels with it to every page. **Reverence/otherness
guard:** Cyrene is in Libya and the popular image of Simon is "the African who carried
the cross"; the text says nothing of his appearance beyond his city, and this series'
standing rule (ep11's Samaritan) is that no figure is marked as an ethnic TYPE. His
skin is "deep sun-browned" like a man who works outdoors in that country — no darker
than Jesus's by design intent, no costume of otherness — and "Cyrenian" is the KJV's
word in a caption, not a drawing note. Chromatic reservation: no blue on him anywhere;
rust-red is allowed (no stain exists to conflict).

**Refs:** `simon_ref.png` (full figure WITH the beam across his shoulders, facing
right) cropped from **F04 approved** — his first large, calm, single-figure page;
`simon_face_ref.png` (face, three-quarter toward the viewer, eyes open, mouth closed)
cropped from the same F04 render — F04 is a MEDIUM CLOSE precisely so one approval
yields both crops (ep11 needed two pages for its two Samaritan crops; here the debut
page is designed to give both). He has true close framing on F04 and F08, and a
three-quarter face on F02/F03/F06; full-figure crops are too small to pin a face, so
the face ref chains into every page where his face is larger than a thumbnail.

**The unburdened state (front cover, F01):** the ref carries the beam; the two
unburdened pages carry an explicit override — *"his shoulders bare of any beam or
burden, nothing carried, his hands empty and swinging at his sides as he walks"* —
the ep11 "lip-cloth now loosed" pattern (a text-line state change against a ref, which
held). §8 flags the fallback: if the front cover's render keeps a beam on him, crop an
unburdened `simon_unburdened_ref.png` from F01's approved main scene (he is foreground-
sized there by design) and rechain the cover.

**THE TWO SOLDIERS** — a shared GROUP identity, one LOOK ref (ep11's `ten_ref`
pattern), no individual faces. Build text (use verbatim on every soldier page):

> two Roman soldiers — exactly two, count them, no more — in short rust-brown
> tunics under plain leather-and-iron cuirasses, bare-legged, in hobnailed sandals,
> plain iron helmets with no plume and no crest, no cloak, no shield; one carries a
> short spear held upright, the other is empty-handed; drawn as ordinary working men
> doing an ordinary duty, their faces neither cruel nor kind, never caricatured,
> never sneering, in the same steady single-struck line as every figure on the page

Why two: Mark's "the soldiers" is plural; two is the minimum plural, and every extra
figure is a regen risk. Why "neither cruel nor kind": the narration's tone toward them
is matter-of-fact ("They put the cross on Simon's back. Nobody asked him.") — a
leering soldier would editorialize what the text doesn't. Ref: `soldiers_ref.png`
cropped from **F02 approved** (the two of them together, one with both hands on the
beam, one with a hand on Jesus's arm — the crop takes the pair). Chained into F01, F03,
F06, F07, F09, and the front cover as a LOOK ref.

### Objects / locations

**THE BEAM** — the episode's title object, recurring on F01-F09 (and NOT on either
cover: the front is before it, the back is after it). Build text (use verbatim):

> the beam: one single straight rough-hewn timber of pale raw wood, squared with an
> adze, about as long as a man is tall and as thick as a man's forearm, its two ends
> raw and split, carried across the back of the shoulders behind the neck with both
> arms raised and the hands gripping it at either side — one beam only, never a full
> cross shape, never a crosspiece joined to an upright, never dragged along the
> ground, never an upright post; no nails, no rope, no inscription, no blood, no
> marks of any kind on the wood; plain ochre-umber wood with no blue and no gold on
> it anywhere

**Why a beam and why it is stated this hard:** the model's prior for "carry the cross"
is a full Latin cross dragged by its foot — a crucifix icon, which is exactly the
atonement-object the fence forbids Simon from being pictured with (§2 rule 1). A beam
across the shoulders is what a man carries through a gate, what "the wood" means, and
what keeps the caption's KJV "cross" honest without drawing an icon. Both covers'
`extra_avoid` and every page's text carry the never-cross-shape triple. Ref:
`beam_ref.png` cropped tight on the wood from **F04 approved** (a little of Simon's
shoulders will be in the crop — acceptable; the manifest line reads "image N is the
beam — match its rough squared timber, its length, and its raw split ends").

**THE GATE OF THE CITY** — the location of every profile page (F01-F06), both covers,
and the anchor of the whole dose. Deliberately NOT Nain's gate (ep7's `gate_ref` is a
low drystone-and-mud-brick village gate with a timber lintel — a different city, a
different scale; reusing it would say "the same town"). Build text (use verbatim):

> the gate of the city: a tall squared opening in a high wall of great dressed
> pale-gold limestone blocks, the doorway framed by a heavy stone lintel and two
> stone jambs, its timber doors standing open inward, one broad worn threshold
> stone lying across the doorway's foot; through the opening, a narrow shadowed lane
> climbing between tall flat-roofed stone houses; outside the gate, a dry dirt road
> running along the foot of the wall to the right and then away over a low stony
> rise into open country; the ground dry ochre earth and stone, no water, no pool,
> no cistern, no trough anywhere; no hill, no crosses, no crowd, and no place of
> execution visible anywhere

Why the DRY is stated: LAW 3 — the doorway holds the dose on four pages, and a
trough or pool at a city gate is exactly the water feature that turns a thread into a
pour. Why "one broad worn threshold stone": it is the anchor and must exist as a
pointable object in the pixels (LAW 4) on every profile page. Why "no place of
execution visible anywhere" lives in the LOCATION build, not just the rules: it then
travels to every page automatically. Ref: `gate_ref.png` cropped from **F04 approved**
(the doorway + jambs + lintel + threshold + a little wall either side, no figures).

**THE ROAD (from behind)** — the location of the three camera-turned pages (F07-F09):
no gate in frame (it is behind the viewer). Build text (use verbatim):

> the same dry dirt road seen from behind, running straight away from the viewer's
> own feet over open stony country and up a long gentle rise to a far crest where it
> goes out of sight against the sky; dry ochre earth and scattered field-stones,
> thin dry grass, no wall, no building, no tree, no water of any kind; nothing
> visible beyond the crest — no hill, no crosses, no crowd

Ref: `road_ref.png` cropped from **F07 approved** (the road + rise + crest, no
figures). Chained into F08 (its far background) and F09.

**No other objects.** No bundle, staff, or pack on Simon (an invention magnet — ep11's
"no staffs"; "walking the other way" is a direction, not luggage). No rope on Jesus. The
back cover's footprints and the front cover's tiny procession are one-page elements.

### Chain order (hard dependencies)

1. `jesus_ref.png` — already present (immediate, no cycle).
2. **F04** renders with `refs=[]` — Simon, the beam, and the gate all debut, large and
   calm, single figure → approve → crop `simon_ref`, `simon_face_ref`, `beam_ref`,
   `gate_ref`. *A QUADRUPLE debut on one approval — ep7's F01 shape (five crops). It is
   the simplest page in the episode (one figure, one doorway, no dose on the man), which
   is why the debut lives here and not on the busier F02/F03. Budget two regen cycles
   (§8).*
3. **F02** (jesus + simon + face + beam + gate; the soldiers debut text-only) → approve
   → crop `soldiers_ref`.
4. **F01, F03** (jesus + simon + face + beam + gate + soldiers), any order after 3.
5. **F05** (simon + face + beam + gate) after 2.
6. **F06 — hero** (jesus + simon + face + beam + gate + soldiers) after 3.
7. **F07** (simon + beam + jesus + soldiers; the road-from-behind debuts) → approve →
   crop `road_ref`.
8. **F08** (simon + face + beam + road), **F09** (simon + beam + jesus + soldiers +
   road) after 7.
9. **Front cover** (simon + face + gate + jesus + soldiers, with the unburdened
   override) after 3.
10. **Back cover** (gate_ref only) after 2.

---

## 4. Covers

### The cover judgment call (stated, as the format asks)

The hook is a man walking the other way; the landing is "He went out through that gate
first." So the covers are the two ends of one doorway: SIMON walking toward it,
empty-shouldered, while the tiny procession comes out of it the other way (front — the
hook's literal picture, the whole two-direction geometry in one frame), and the same
GATE at dusk, EMPTY, with two lines of footprints running out from its threshold, one a
pace behind the other (back — the landing's own picture, no whole figure). Series
variety: ep4 led with Jesus, ep5 its widow, ep7 the object, ep10 the woman with the
object, ep11 a crowd; ep13 leads with its protagonist walking AWAY from the viewer's
expectation, and lands on a doorway rather than an object — the beam is not left behind
(it went where he went), so the object-landing pattern gives way to the place-landing
pattern (ep11's pressed dust). **Neither cover shows the beam:** front is before it,
back is after it. The title object of the episode is on every interior page and on
neither cover — a deliberate frame.

### FRONT COVER

- **Scene:** Simon (SIMON_BUILD, match the attached references) in full figure, large
  in the lower third at the frame's center-right, walking from right to LEFT along a
  dry dirt road in profile, mid-stride, his shoulders bare of any beam or burden,
  nothing carried, his hands empty and swinging at his sides, his head-cloth tied at
  the nape, his rust-striped mantle over his left shoulder, an ordinary countryman on
  an ordinary morning; the road runs along the foot of a high wall of great dressed
  pale-gold limestone blocks toward the tall squared gate of the city at the far left
  (GATE_BUILD, match the attached reference); IN the gate's opening, small and far, the
  procession coming OUT the other way — Jesus (JESUS_BUILD) under the beam across his
  shoulders, upright, walking right, a soldier's hand on his arm, the two soldiers
  (SOLDIERS_BUILD) with him — tiny against the doorway, no more than a few figures,
  none of them looking at Simon and Simon not looking at them; behind Simon at the
  right the road comes in over a low stony rise from open country.
- **Lighting (law: ≥1 warm + ≥1 cool):** warm early-morning gold from the open country
  at the right, low behind Simon, rim-lighting his shoulders and the dust of the road he
  has walked; cold blue-grey shadow filling the gate's opening and the shadowed face of
  the wall at the left, the procession inside it in that cold. WHY: the warmth is the
  morning he was walking in; the cold is the doorway he is walking toward, and what is
  coming out of it.
- **Motif:** none (covers never carry the interior motifs). No blue in the gate.
- **Title:** `THE CROSS THAT WASN'T HIS` (top) — the locked episode title, ep7's
  paraphrase-title precedent ("THE BIER HE TOUCHED" was not a verbatim line either).
  **The apostrophe is a baked-punctuation risk** (the standing full-zoom check on
  punctuation); fallback in order: `WALKING THE OTHER WAY` (4 words, the hook verbatim
  contiguous, no punctuation), then `THE OTHER WAY` (3) — §8. **Subtitle:** `MARK 15`.
  **seq_title for all interior pages = `WITHOUT THE GATE`** (3 words, Hebrews 13:12
  verbatim, the episode's hinge phrase, no punctuation — the 5-word apostrophe title
  would render nine times as a header; §8 if the user wants the title instead).
- **Refs:** simon_ref + simon_face_ref + gate_ref + jesus_ref + soldiers_ref (hence F02
  approval precedes this render).
- **extra_avoid append:** "a full cross shape, a crucifix, a dragged cross, a crown of
  thorns, blood, wounds, gore, a crowd, a hill with crosses, any bundle or staff or pack
  carried, any figure touching another except a soldier's hand on an arm, modern
  clothing".
- **Animation (strong front lock, per the cover doc):** Simon keeps walking from right
  to left along the road toward the gate, one continuous steady stride the whole clip,
  his empty hands swinging, his mantle's loose edge stirring; the small figures in the
  gate's opening hold exactly as drawn, still; the warm morning light behind him stays
  exactly as warm and low as it already is, unchanged for the whole clip; the cold
  shadow in the gate's opening stays exactly as cold and dim as it already is; the wall
  and the gate stay exactly as drawn; no new figure, mark, or text appears.
  `clip_duration=5` (6.4s slot, ~22% frozen — a deliberate ≥1s headroom under the
  estimated slot after ep11's real-timestamp drift, §7). Freeze (a walk — never
  boomerang: a reversed walk would send him OUT before the story does).

### BACK COVER

- **Scene:** the gate of the city (GATE_BUILD, match the attached reference) seen from
  outside at dusk, filling the left half of the frame and rising past its top — the
  tall squared opening in the high pale-gold wall, its timber doors standing open, the
  doorway EMPTY, the shadowed lane beyond it empty, no figure anywhere on the image;
  the broad worn threshold stone across the doorway's foot, large and low in the frame;
  from that threshold, two lines of bare footprints in the dust of the dry road running
  away to the RIGHT and out over the low stony rise, one line a pace behind the other,
  the second following the first exactly — plain marks in dust, no figure; from the
  threshold stone itself, not from the footprints and not from the road, one small
  hard-capped hooked curl of blue ink with a trace of muted gold rises — its whole
  visible length no longer than a hand's width, curling back toward its own root like
  a comma or a fishhook WITHOUT fully closing into a ring, flat and two-dimensional,
  drawn ON the paper's surface, a single continuous brushstroke, never a ring, never a
  bracelet, never a bangle, never jewelry, never metallic, never reflective, never
  straightening, never trailing, behaving like a small dab of living ink, never a glow;
  the road beyond the rise EMPTY under carved cloud forms in an open dusk sky.
- **Why this image:** "He went out through that gate first" — the doorway he crossed,
  now empty; the first footprints his, the second a pace behind, following ("after
  him"); the only living ink on the cover rises from the line he crossed, never from
  the tracks (the tracks are what a man does; the crossing is what was done for him).
  No whole figure: the viewer's own eye-line is at the threshold, low, and the road out
  is open. It is also the fence drawn: nothing on the picture is a cross, a hill, or a
  burden — what is left at the gate is the crossing itself.
- **Lighting (law):** warm last dusk gold lying low across the road OUTSIDE and along
  the two lines of footprints running out to the right ("without" is where the light
  is); cold blue dusk holding the wall, the doorway, and the empty lane inside it at
  the left.
- **Title:** `THROUGH THAT GATE FIRST` (bottom) — the narration's own clause, verbatim
  contiguous, 4 words, and it names the picture: the priority ("first") IS the fence
  (he went first; what you carry after him is not what he did). Alternative `WITH HIS
  OWN BLOOD` (4, verbatim contiguous and Hebrews 13:12 verbatim — the fence's own last
  words; over an empty doorway it reads as "done") — §8. **Subtitle:** `HEBREWS 13:13`
  — "Let us go forth therefore unto him without the camp, bearing his reproach": the
  verse the whole thread points TO and the open road's own invitation (the cover doc's
  rule: the NT verse the thread points to, not the one it is). Alternative `HEBREWS
  13:12` if the title moves to "WITH HIS OWN BLOOD" (keep verse and phrase from the same
  verse) — §8.
- **Refs:** gate_ref only (no figures; the wall, doorway, threshold must match).
- **extra_avoid append:** "any human figure, a face, a hand, a cross of any shape, a
  beam or timber, a hill, jewelry, bright neon, a drawn border or caption strip".
- **Animation (light back lock, per the cover doc):** fine dust drifts slowly and low
  along the empty road outside the gate in the dusk wind; the small blue-gold curl
  stays exactly as drawn, in place, for the whole clip; the two lines of footprints lie
  still, exactly as drawn; the warm light across the road stays exactly as warm and low
  as it already is, unchanged; the cold dusk in the doorway stays exactly as cold and
  dim as it already is; the gate and wall stay exactly as drawn; no new figure, mark,
  or text appears. `clip_duration=8` (10.9s slot, ~27% frozen — under SW-F1's 35%; 10s
  if the bridge accepts it, ~9%). Freeze (drifting dust — never boomerang).

---

## 5. Page design conventions used below

- Every page: `panel_style="woodcut_hybrid"`, 9:16, `include_no_bubble_clause=True`,
  `fence_kind="none"` (no dead ink — §2), the page-global no-new-mark clause written
  at the end of every `main_scene_animation` by hand.
- **Page geometry law, every interior page:** F01-F06 are PROFILE pages — the camera
  outside the city, the wall and gate at the frame's LEFT, the road running to the
  RIGHT; IN is left, OUT is right; Jesus always faces right; Simon faces left on
  F01-F02 and right from F03. F07-F09 are the CAMERA-TURNED pages — the viewer stands
  on the road just outside the gate looking OUT along it; the gate is behind the camera
  and never in frame; OUT is now INTO the frame's depth, toward the far crest; every
  figure has his back to the viewer. The turn happens exactly once, on the F06→F07 cut,
  and is never undone.
- **DIRECTION check first (this episode's literalism trap):** on every page and every
  panel with a walking figure, the eye-QC reads which way each figure faces BEFORE
  checking anything else (§2). Then the beam: one beam, across the shoulders, nothing
  on it, no cross shape. Then the count: exactly two soldiers where soldiers appear.
- **Passion-prior guard** (§3, Jesus) on every Jesus page: own clothes, bare head, no
  crown, no wounds, no blood, no rope, upright, calm, led by one soldier's hand, never
  looking back, never touching or touched by Simon.
- **Reproach-not-atonement rules** (§2, seven of them) on every beam page: the
  implementation pass copies the beam build verbatim and the "never a cross shape /
  nothing on the wood / never dragged" triple onto every page the beam is on.
- **Standing steady-line override:** every Simon page states *"drawn in the same
  steady, confident, single-struck line, no doubled or tremored contour"* — a man
  seized by soldiers is exactly what a render loosens into fray-hatching, and here that
  would say "afraid" about a man the text only calls compelled.
- **Type panels only on F05 and F06 p1** (§2's register rule); the type panels carry
  NO blue, and their small figures get tone-only panel motion (small sketched figures
  morph under content-motion asks).
- **LAW 3 for this episode:** no water on any page — no pool, cistern, or trough at the
  gate, no stream by the road — stated as "dry" in both location builds; the dose lives
  in the doorway's air (F03-F06) or the open upper air (F07-F09) and touches nothing on
  the ground, ever, and never the beam.
- **Lips closed on every figure on every clip** — narrator-only episode, no lip-sync
  ever; no NO_MOUTH owner, but the clause is still written for any face larger than a
  thumbnail.
- **Captions are ONE line on every page** (≤4 words, one collapsed 5-word line on the
  hero, ep7 F04's / ep11 F09's precedent). Under OpenArt every page renders on Kling,
  so the documented Kling + 2-line-caption bubble risk now applies to every page, not
  just the Kling-tier ones; ep11 did ship five 2-line captions through OpenArt's Kling
  with no bubble defect recorded, so this is an avoidable risk, not a proven one — I
  avoid it anyway, and no page below needs two lines. Captions are verbatim contiguous
  fragments of the locked narration (KJV lines included; trailing/inner punctuation
  dropped per ep11's F05 precedent); panel labels are 1-3 authored words; corner notes
  short.
- **Still-model call per page:** `nano-banana-pro` wherever a page has three or more
  figures, a debut, a hero, a type-panel row, or a first-of-its-kind composition;
  `seedream-4-5` only where the validated case holds (a calm single figure, all refs
  chained, no other figure to leak a mark onto). Stated per page with its why, and
  the seedream candidates that did NOT make the cut are listed in §8 with the condition
  that would promote them.
- Main-scene prose below is design intent at near-final density (PageSpec
  `main_scene_still` register). Sonnet writes the template prompts — keeping every
  MUST-SHOW, direction, count, dosage, separation, never-X, touch, reverence, and
  steady-line clause — and, per LAW 4, the final animation prompt against the RENDERED
  still's actual pixels.
- Model lanes per the north-star tiering, stated per page with its why: Kling3.0 pro
  where a designed gesture must COMPLETE mid-clip; veo3_1_lite for holds and
  locomotion-that-continues. **Under the OpenArt bridge there is no veo model — the
  tier is advisory and every clip renders on Kling 3 Omni; see §7.**

---

## 6. Page-by-page

### F01 — "led him out to crucify him… coming out of the country" (25w · Swirl **0** · veo3_1_lite advisory, clip 10 · nano-banana-pro)

The establishing shot: the whole two-direction geometry in one frame. Jesus stepping OUT
over the threshold stone under the beam (his foot on the stone — the anchor planted,
unlit); Simon foreground-sized at the right walking IN, empty-shouldered; a long stretch
of road between. Renders AFTER F04 (refs) and F02 (soldiers).

- **Panels** *(Mark's three nouns)*
  1. `"the soldiers"` — a plain iron helmet and the head of a short spear against the
     sky, close, no face.
  2. `"led him out"` — a soldier's hand gripping a man's upper arm through the sleeve of
     an undyed cream-brown robe, close, no face *(partial main-scene element; the touch
     the text gives)*.
  3. `"the country"` — open stony fields under morning light, a dry road coming in over
     a rise, no one on it *(where Simon comes from)*.
- **Main scene** — `WIDE shot`:
  > the gate of the city (GATE_BUILD) at the frame's left-center, the high pale-gold
  > wall running across the background, the doorway open; IN the doorway, {JESUS_BUILD}
  > stepping OUT through it from left to right, his right foot planted ON the broad worn
  > threshold stone, the beam (BEAM_BUILD) across the back of his shoulders with both
  > hands gripping it, upright, walking at an even pace, in his own clothes, his head
  > bare, no crown of thorns, no wounds or blood, no rope on his wrists, his face calm
  > and set toward the road ahead, fully inside the frame; {SOLDIERS_BUILD} — one just
  > outside the doorway ahead of him with a hand on his upper arm, leading, the other
  > behind him in the doorway — the only hands on Jesus; at the frame's RIGHT, nearer
  > the viewer and larger, {SIMON_BUILD} walking from right to LEFT along the road
  > toward the gate, mid-stride, his shoulders bare of any beam or burden, nothing
  > carried, his hands empty and swinging at his sides, his eyes on the road, not on
  > the gate, fully inside the frame; a long stretch of EMPTY dry road between him and
  > the gate; the road running along the foot of the wall and then away over the rise
  > at the right; morning light, long shadows; the ground dry, no water anywhere; no
  > hill, no crosses, no crowd anywhere. Stage 0 dosage: no blue Swirls of Life ink
  > motif anywhere on this page — no blue ink appears anywhere in the scene, the
  > panels, or the margins; the threshold stone plain worn stone, unmarked.
- **material_closer:** "no unusual ink of any kind is at work on this page — no blue,
  no gold, no stain — and the paper beneath every figure is wholly clean."
- **Fence:** `none`
- **Caption:** `("led him out",)` *(KJV 15:20 verbatim contiguous, 3)* · **Corner
  note:** `NOTE: passed by` *(KJV 15:21's own phrase)*
- **Panel motions:** (1) the light on the helmet warms very slightly and settles; (2)
  the gripping hand holds, still; (3) a thin banner of dust drifts across the far road.
- **Main animation:** Jesus keeps walking out through the doorway from left to right at
  an unhurried, even pace, the beam steady on his shoulders, the soldier's hand staying
  on his arm, his face toward the road, his lips closed and completely still; the two
  soldiers walk with him at the same pace; Simon keeps walking from right to left along
  the road toward the gate, one continuous unhurried stride the whole clip, his empty
  hands swinging, a long stretch of road staying between him and the gate for the whole
  clip; a low thin haze of dust drifts along the empty road between them; no blue or
  gold ink motif appears anywhere on this page, and none appears at any point in the
  clip; no new stain, spot, or darkening appears anywhere on the page at any point.
- **Why veo (advisory):** two continuing walks, no completing gesture; under Kling-only
  the one thing to watch is that the model does not STAGE the meeting — the still puts
  the full frame width between the two walking men, both are given "unhurried," and
  "a long stretch of road staying between them" is a positive clause (§8: if the
  contact sheet shows Simon reaching the gate, cut to clip 8). **Why NBP:** five
  figures, two of them likeness-critical. **Refs:** jesus + simon + face + beam + gate
  + soldiers.

### F02 — "Same road. They put the cross on Simon's back. Nobody asked him." (21w · Swirl **0** · kling3_0, clip 8 · nano-banana-pro)

The seizure at the gate's mouth. The beam is ALREADY on Simon — laid by the soldier's
hands, still pressing — and Simon still faces LEFT, the way he was going. Jesus a few
steps ahead, unburdened, facing the road, touching no one, not looking back. The
soldiers' DEBUT (renders second, after F04).

- **Panels**
  1. `"same road"` — the dust of the road close and low, two lines of sandal-prints
     crossing each other in opposite directions, no figure *(the crossing, as marks)*.
  2. `"on his back"` — the rough underside of a squared beam pressing down across the
     back of a man's neck and shoulders, seen from behind, the knot of a plain
     head-cloth at the nape, close, no face *(Simon's mark, partial)*.
  3. `"nobody asked"` — a soldier's two hands gripping a beam and pressing it down,
     close, no face.
- **Main scene** — `MEDIUM shot` at the gate's mouth:
  > the gate of the city (GATE_BUILD) at the left, its doorway open and its threshold
  > stone plain and unmarked, fully inside the frame; just outside the threshold at
  > center, {SIMON_BUILD} stopped mid-stride and facing LEFT toward the doorway — the
  > way he was walking — with the beam (BEAM_BUILD) just laid across the back of his
  > shoulders, his back bent under the sudden weight, his own hands coming up to grip
  > it, his face turned toward the doorway, his eyes open, his mouth closed, fully
  > inside the frame, drawn in the same steady, confident, single-struck line as every
  > figure on the page, no doubled or tremored contour; beside him one of
  > {SOLDIERS_BUILD} with BOTH hands on the beam pressing it down onto Simon's
  > shoulders; a few steps to the RIGHT beyond them, outside, {JESUS_BUILD} standing
  > unburdened, facing RIGHT toward the road, the other soldier's hand on his upper
  > arm, his hands empty, touching no one, not looking back, his head bare, no crown,
  > no wounds, no blood, no rope, fully inside the frame — the beam passes from him to
  > Simon only by the soldier's hands, never by his; exactly two soldiers; the road
  > running out to the right; the ground dry, no water anywhere; no hill, no crosses,
  > no crowd. Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page —
  > no blue ink appears anywhere in the scene, the panels, or the margins.
- **material_closer:** "no unusual ink of any kind is at work on this page — no blue,
  no gold, no stain — and the paper beneath every figure is wholly clean."
- **Fence:** `none`
- **Caption:** `("Nobody asked him",)` *(narration verbatim, 3)* · **Corner note:**
  `NOTE: same road` *(narration verbatim)*
- **Panel motions:** (1) a thin haze of dust drifts across the crossing prints; (2) the
  beam's underside holds, the light across the wood warming very slightly; (3) the
  gripping hands hold, still.
- **Main animation:** the soldier's hands press the beam down the last small distance
  onto Simon's shoulders and hold there; Simon's knees bend a little as they take the
  weight and his hands close around the beam and hold it, his face staying turned toward
  the doorway, his lips closed and completely still; Jesus stays exactly as drawn,
  facing the road, the soldier's hand on his arm, one slow breath, never looking back,
  his lips closed; a low thin haze of dust drifts along the road beyond; no blue or gold
  ink motif appears anywhere on this page, and none appears at any point in the clip;
  no new stain, spot, or darkening appears anywhere on the page at any point.
- **Why kling:** the press-and-settle is a completing gesture with a stated end — the
  page's one human event, "Nobody asked him" told by knees and hands. **LAW 0
  discipline:** the beam is drawn ALREADY on Simon; the clip only completes the settle —
  it is never asked to move the beam from one man to another (an object handoff is a
  morph). **Why NBP:** four figures; the soldiers debut here. **Refs:** jesus + simon +
  face + beam + gate → approve → crop `soldiers_ref`.

### F03 — "that he might bear it after Jesus. Simon turns, and walks out too." (22w · **Swirl 1 first trace** · veo3_1_lite advisory, clip 8 · nano-banana-pro) — THE GOSPEL TURN

Same gate, same beam, same man — now facing RIGHT. The turn happened on the page cut
(LAW 1). His rear heel is lifting from the threshold stone; the first blue of the
episode rises from that stone behind him, its tip leaning after Jesus.

- **Panels**
  1. `"they laid"` — a beam lying across a man's shoulders seen from behind, its two raw
     ends jutting out either side, close, no face *(the laid-on object)*.
  2. `"after Jesus"` — Jesus's back, small, walking away to the right along a road, a
     soldier beside him *(jesus_ref; small figures → tone-only motion)*.
  3. `"turns"` — a single pair of sandaled feet on a broad worn threshold stone, toes
     pointing RIGHT, the rear heel lifting, low and close *(the turn as feet — direction
     told statically)*.
- **Main scene** — `MEDIUM WIDE shot` at the gate:
  > the gate of the city (GATE_BUILD) at the left, its doorway open behind him, its
  > broad worn threshold stone fully inside the frame; AT the threshold, {SIMON_BUILD}
  > TURNED — now facing RIGHT toward the open road — the beam (BEAM_BUILD) across the
  > back of his shoulders, both hands gripping it, mid-first-step outward: his front
  > foot on the dry road outside, his rear heel just lifting from the threshold stone,
  > his face toward the road ahead, his eyes open, his mouth closed, fully inside the
  > frame, drawn in the same steady, confident, single-struck line as every figure on
  > the page; beside and a little behind him one of {SOLDIERS_BUILD}, empty-handed
  > now, walking; a few paces ahead outside to the right, {JESUS_BUILD} walking RIGHT
  > at an even pace, the other soldier's hand on his upper arm, unburdened, not
  > looking back, touching no one, head bare, no crown, no wounds, no blood, no rope,
  > fully inside the frame; exactly two soldiers; the road running out to the right
  > over the rise; the ground dry, no water anywhere; no hill, no crosses, no crowd.
  > Stage 1 dosage: exactly one restrained thread of blue ink rising from the worn
  > threshold stone itself — from the stone just behind Simon's lifting heel — up into
  > the air of the doorway behind him, its upper end leaning to the right toward the
  > road, touching only the stone and the air, touching no figure, never touching the
  > beam, the man, or his foot, the only blue on the whole page, behaving like one
  > stroke of wet ink bled into the paper, smooth and open in its curl, never
  > blot-shaped, never a glow.
- **material_closer:** "the single blue thread rising from the threshold stone behind
  him is the only unusual ink at work on this page, and the beam, the man, and the paper
  beneath every figure are free of any ink."
- **Fence:** `none`
- **Caption:** `("after Jesus",)` *(KJV 23:26 verbatim contiguous, 2 — the whole page
  in two words)* · **Corner note:** `NOTE: Simon turns` *(narration verbatim)*
- **Panel motions:** (1) the beam on the shoulders holds, the light across the wood
  warming very slightly; (2) the small far figures hold, tone-only; (3) a little dust
  lifts from under the lifting heel and drifts.
- **Main animation:** Simon keeps walking out from left to right along the road away
  from the gate, one continuous steady stride the whole clip, the beam steady across
  his shoulders, his hands gripping it, his face toward the road ahead, his lips closed
  and completely still; the soldier beside him walks at the same pace; Jesus ahead keeps
  walking right at an even pace, the soldier's hand on his arm, never looking back, his
  lips closed; the single thin blue ink thread at the threshold stone stays exactly as
  drawn, in place, for the whole clip; a low thin haze of dust drifts along the road; no
  new stain, spot, or darkening appears anywhere on the page at any point.
- **Why veo (advisory):** the turn is already made — the drawing faces right and the
  clip only continues it (LAW 1; F02 faces left, F03 faces right, the cut is the turn);
  every motion is a continuing walk; the Stage 1 thread is held still per the table.
  **Fragility note (LAW 0.6):** the thread's root and the lifting heel share the
  threshold stone — the root is stated as "the stone just behind his heel"; if the
  render puts the thread on his foot, his sandal, or the beam, regen the still (never
  adapt the animation clause). **Why NBP:** four figures. **Refs:** jesus + simon +
  face + beam + gate + soldiers.

### F04 — "Now he is through the gate… outside is 'without.'" (14w · **Swirl 2** · veo3_1_lite advisory, clip 5 · nano-banana-pro — THE DEBUT)

The WORD page (hard problem #2) and the episode's debut render (renders FIRST,
`refs=[]`): Simon large, calm, alone, three-quarter to the viewer so one approval
yields his full-figure ref, his face ref, the beam ref, and the gate ref. The three
panels are one doorway from inside, at the threshold, and from outside.

- **Panels** *(one doorway, three ways — the word drawn)*
  1. `"inside"` — the gate seen from INSIDE the lane: shadowed stone jambs and lintel
     framing a bright opening onto the road beyond, no figure.
  2. `"the gate"` — the broad worn threshold stone across the doorway's foot, close and
     low, no figure.
  3. `"without"` — the gate's outer face seen from OUTSIDE on the road, the doorway dark,
     the road beginning at its foot, no figure.
- **Main scene** — `MEDIUM CLOSE shot`:
  > {SIMON_BUILD} a few paces outside the gate, walking RIGHT along the dry road, seen
  > three-quarter from the front-right so that his whole face is fully visible inside
  > the frame — his eyes open, his mouth closed, his brow set, dust on his cheek — the
  > beam (BEAM_BUILD) across the back of his shoulders with both hands gripping it, his
  > head-cloth tied at the nape, his rust-striped mantle over his left shoulder, fully
  > inside the frame from the knees up, drawn in the same steady, confident,
  > single-struck line, no doubled or tremored contour; behind him at the left, the
  > gate of the city (GATE_BUILD) — its open doorway, its threshold stone, and the
  > shadowed lane beyond, fully inside the frame; no other figure anywhere in the frame;
  > the ground dry, no water anywhere; no hill, no crosses, no crowd. Stage 2 dosage:
  > the blue ink motif is quietly present — a few soft blue threads rising from the
  > threshold stone up into the gate's open doorway behind him, and at their top one
  > soft, irregular, hazy patch of the same blue pigment, entirely amorphous, with soft
  > feathered edges and no internal structure of any kind, exactly like a single drop of
  > watercolor spreading into wet paper, hanging in the air of the doorway and contained
  > within the opening, touching only the stone and the air, touching no figure, never
  > on the road, never on the beam, never on the man; every thread behaving like wet ink
  > bled into the paper, smooth and open, never blot-shaped, never a glow.
- **material_closer:** "the soft blue threads and the one small bloom held inside the
  gate's doorway behind him are the only unusual ink on the page, and the beam, the man,
  and the paper beneath him are free of any ink."
- **Fence:** `none`
- **Caption:** `("outside is without",)` *(narration verbatim contiguous, 3 — the
  quote marks dropped, §2)* · **Corner note:** `NOTE: through the gate` *(narration
  verbatim)*
- **Panel motions:** (1) the light in the bright opening warms very slightly; (2) the
  threshold stone lies still, a little dust drifting over it; (3) a thin banner of dust
  drifts across the road at the gate's foot.
- **Main animation:** Simon keeps walking right at a steady pace, the beam steady on his
  shoulders, his eyes on the road ahead, one slow breath, his lips closed and completely
  still; the soft blue threads and the small bloom in the doorway behind him drift
  gently within their own small area inside the doorway, never leaving it, never
  lowering toward the road; a low thin haze of dust drifts along the road; no new
  stain, spot, or darkening appears anywhere on the page at any point.
- **Why veo (advisory):** a walk-and-hold, no completing gesture. **Why 5s on a 6.4s
  slot:** ≥1s headroom for the real-timestamp slot (§7). **Why NBP on a page that is
  otherwise the textbook seedream case:** this is the DEBUT — every likeness in the
  episode is born from this render, and chaining a Seedream-born ref into
  Nano-Banana-Pro pages is untested; the strongest model owns the birth (§8). **Refs:**
  `[]` → approve → crop `simon_ref`, `simon_face_ref`, `beam_ref`, `gate_ref`.

### F05 — "The sin offering… burned 'without the camp.'" (28w · Swirl 2 held · veo3_1_lite advisory, clip 10 · nano-banana-pro) — THE TYPE PAGE

The Old Testament enters the episode — in the carved panels ONLY (the register rule).
The main scene never leaves the road: Simon walking out, the gate small behind him, no
other figure; the narrator explains while Simon walks, exactly as the text does ("Out
there, where Simon is walking" is the very next beat). The three panels are the type
told left-to-right on the episode's own axis: blood carried IN (leftward), body carried
OUT (rightward), burned outside.

- **Panels** *(the type, carved; IN is left, OUT is right; no blue; no gore)*
  1. `"blood carried in"` — a priest's two hands carrying a shallow clay bowl held level,
     its contents dark, LEFTWARD in through the hanging woven curtain of a tent's
     doorway, close, no face *(the sanctuary as a tent door — "God's holy tent," the
     narration's own words — never a stone temple, never a church)*.
  2. `"body went out"` — two men carrying the carcass of a slaughtered animal slung on
     a pole between them, RIGHTWARD past the last goat-hair tents of a camp toward open
     ground, small, seen from the side, plainly and reverently drawn, no wound visible,
     no gore.
  3. `"burned"` — a low fire on open ground outside a camp's edge, thin smoke rising,
     the tents small and far at the left, no figure.
- **Main scene** — `WIDE shot`:
  > the road outside the city: the high wall receding at the left with the gate of the
  > city (GATE_BUILD) small at the far left, its doorway and threshold stone fully
  > inside the frame; {SIMON_BUILD} walking RIGHT along the road at mid-frame, the beam
  > (BEAM_BUILD) across the back of his shoulders, both hands gripping it, his face
  > toward the road ahead, fully inside the frame, drawn in the same steady, confident,
  > single-struck line; no other figure anywhere in the frame; the road running away to
  > the right over the low stony rise into open country; the ground dry, no water
  > anywhere; no hill, no crosses, no crowd, nothing at the road's end. Stage 2 dosage,
  > held: a few soft blue threads rising from the small far threshold stone up into the
  > small doorway at the far left, and one small amorphous watercolor bloom hanging in
  > the doorway's air, small with the distance, contained within the opening, touching
  > only the stone and the air, the only blue on the whole page; no blue of any kind in
  > any of the three top panels; the road, the man, and the beam free of any ink of any
  > kind.
- **material_closer:** "the small blue threads and bloom held inside the far doorway are
  the only unusual ink on the page; the three top panels carry no blue at all, and the
  paper beneath the man is wholly clean."
- **Fence:** `none`
- **Caption:** `("without the camp",)` *(KJV Heb 13:11 verbatim contiguous, 3)* ·
  **Corner note:** `NOTE: Hebrews 13` *(the attribution the ear lost — hard problem #1;
  §8 for the numeral risk and the fallback `NOTE: the sin offering`)*
- **Panel motions:** (1) the bowl and the hands hold, the light across them warming very
  slightly *(small figure — tone-only)*; (2) the two carriers hold, tone-only; (3) the
  flames of the fire flicker in place and the thin smoke drifts upward within its own
  column.
- **Main animation:** Simon keeps walking right along the road at a steady pace, one
  continuous stride the whole clip, the beam steady on his shoulders, his lips closed;
  the small blue threads and bloom inside the far doorway drift gently within their own
  small area, never leaving the doorway; a low thin haze of dust drifts along the road;
  no new stain, spot, or darkening appears anywhere on the page at any point.
- **Why veo (advisory):** a continuing walk and near-static panels. **Why NBP, not
  seedream:** the main scene is a calm single figure (the validated seedream case on its
  face), but the three type panels are the episode's single most content-critical
  diagram — a bowl carried IN, a carcass carried OUT by two men, a fire — count-critical
  small figures and a direction that must read; the bake-off found no cheap model clean
  on complex content, and a garbled panel here breaks hard problem #1. The panels decide
  the model. (§8: the first seedream candidate to promote if F08's seedream render holds
  its panels clean — the user's call, never automatic.) **Refs:** simon + face + beam +
  gate.

### F06 — HERO — "Wherefore Jesus also… suffered without the gate. Out there, where Simon is walking." (28w · Swirl 2 held · kling3_0, clip 10 · nano-banana-pro)

The gospel pivot: Christ's own atoning act named in Hebrews' words, and Jesus bodily
back in frame — "Then it says of Jesus" is the moment he re-enters — a single pace
AHEAD of the man who follows him out. The panel row is the visual bridge (camp's
outside / gate's outside / the Person). Simon's head is drawn lifting toward the man in
front of him; the clip completes the lift.

- **Panels** *(the bridge — two outsides drawn to the same layout, then the Person)*
  1. `"without the camp"` — the edge of a camp: the last goat-hair tents small at the
     LEFT, open ground and a low fire's thin smoke at the RIGHT, no figure *(the type's
     outside; rhymes F05 p3, wider)*.
  2. `"without the gate"` — the gate of the city small at the LEFT, the dry road running
     out to the RIGHT, empty, no figure *(the antitype's outside — drawn to the SAME
     layout as panel 1, so the eye sees camp = gate)*.
  3. `"Jesus also"` — Jesus's face in profile, close, calm, facing right, lips closed,
     head bare *(jesus_ref; small face → tone-only motion)*.
- **Main scene** — `MEDIUM WIDE shot` from beside the road, low:
  > the gate of the city (GATE_BUILD) small at the far-left edge of the frame, its
  > doorway and threshold stone fully inside the frame; at center-right, {JESUS_BUILD}
  > walking RIGHT along the road, a single pace AHEAD of Simon, in his own clothes, his
  > head bare, no crown of thorns, no wounds or blood, no rope, upright, at an even
  > pace, one of {SOLDIERS_BUILD} with a hand on his upper arm, his own hands empty,
  > touching no one, not looking back, fully inside the frame; at center-left, one pace
  > behind him, {SIMON_BUILD} walking RIGHT, the beam (BEAM_BUILD) across the back of
  > his shoulders, both hands gripping it, his head LIFTED and his eyes on the man ahead
  > of him, his mouth closed, fully inside the frame, drawn in the same steady,
  > confident, single-struck line as every figure on the page; the second soldier beside
  > Simon; exactly two soldiers; Simon and Jesus never touching; the road running away
  > to the right over the rise, nothing at its end; the ground dry, no water anywhere;
  > no hill, no crosses, no crowd. Stage 2 dosage, held: a few soft blue threads and one
  > small amorphous watercolor bloom held inside the small far doorway at the left edge,
  > touching only the threshold stone and the air of the doorway; the road, Jesus,
  > Simon, the soldiers, and the beam free of any ink of any kind.
- **material_closer:** "the small blue threads and bloom held inside the far doorway are
  the only unusual ink on the page, and the beam and every figure on the road are free
  of any ink."
- **Fence:** `none`
- **Caption:** `("suffered without the gate",)` *(KJV Heb 13:12 verbatim contiguous, 4
  — the hero's line is Christ's act, not Simon's)* · **Corner note:** `NOTE: out there`
  *(narration verbatim — the return to the road)*
- **Panel motions:** (1) the thin smoke drifts upward within its own column; (2) a thin
  banner of dust drifts across the empty road at the gate's foot; (3) the sketched
  profile holds, tone-only.
- **Main animation (the Hem F05 recipe, tuned to this beat):** Simon's head lifts the
  last small distance and holds, his eyes staying on the man ahead of him, his stride
  continuing at the same steady pace one pace behind Jesus, the beam steady on his
  shoulders, his lips closed and completely still; Jesus keeps walking right at an even
  pace, the soldier's hand on his arm, never looking back, his lips closed and
  completely still; the two soldiers walk at the same pace; the small blue threads and
  bloom inside the far doorway drift gently within their own small area, never leaving
  it; a low thin haze of dust drifts along the road; no new stain, spot, or darkening
  appears anywhere on the page at any point.
- **Why kling:** the head-lift with a stated end (eyes on the man ahead) is a
  completing gesture — the hero's one human event, so it is not a lifeless walk. **Why
  hero:** the gospel-pivot sentence — Hebrews 13:12, "sanctify the people with his own
  blood, suffered without the gate" — Christ's own atoning act named, Jesus bodily in
  frame with the man who bears it AFTER him (Luke's word drawn literally: one pace
  behind); not the emotional climax (the seizure and the turn, F02-F03), exactly as the
  locked rule asks. In this Swirls pipeline the covers bookend the cut; F06 is the hero
  still for any thumbnail / hero-bookend use. Alternate: F03 (the first blue, the turn)
  if the user wants the more graphic page — §8. **Why Stage 2 held and not 3
  beginning:** a Kling page with a completing gesture keeps the contained doorway dose
  (ep10 F08's hero shape); Stage 3 waits for the camera turn (§2). **Why NBP:** four
  figures, the hero. **Refs:** jesus + simon + face + beam + gate + soldiers.

### F07 — "Hebrews turns to you: 'Let us go forth therefore unto him…'" (17w · **Swirl 3 beginning** · veo3_1_lite advisory, clip 6 · nano-banana-pro) — THE CAMERA TURN

"Turns to you" is drawn as the camera turning: for the first time the viewer stands ON
the road, just outside the gate (which is now behind the camera and never in frame),
looking OUT along it. Simon mid-distance walking away with the beam; Jesus and the
soldiers further along, small — "unto him" is a visible destination. The band leaves
the doorway and opens across the air above the road. The road-from-behind DEBUT →
crop `road_ref`.

- **Panels**
  1. `"turns to you"` — the dust of a road close at the viewer's own feet, one line of
     sandal-prints leading away from the panel's bottom edge into the distance, no
     figure *(the viewer's own road)*.
  2. `"unto him"` — Jesus's back, small and far, walking away up a road, a soldier
     beside him *(jesus_ref; small figures → tone-only motion)*.
  3. `"his reproach"` — the back of a man's neck and shoulders under a beam, from
     behind, close, the knot of a plain head-cloth at the nape, no face *(Simon's mark,
     partial)*.
- **Main scene** — `WIDE shot` from behind, low:
  > the road (ROAD_BUILD) running straight away from the viewer's own feet over open
  > stony country and up the long gentle rise to the far crest, fully inside the frame;
  > no gate, no wall, and no building anywhere in the frame; at mid-distance,
  > {SIMON_BUILD} walking AWAY from the viewer along the road, his back to the viewer,
  > the beam (BEAM_BUILD) across the back of his shoulders with its two raw ends jutting
  > out either side, both hands gripping it, the knot of his head-cloth at his nape and
  > his rust-striped mantle over his left shoulder, fully inside the frame, drawn in
  > the same steady, confident, single-struck line; further along and smaller,
  > {JESUS_BUILD} walking away up the road, his back to the viewer, upright, one of
  > {SOLDIERS_BUILD} with a hand on his upper arm and the other soldier beside him,
  > exactly two soldiers, none of them turning; nothing visible beyond the crest — no
  > hill, no crosses, no crowd; the ground dry, no water anywhere. Stage 3 beginning
  > dosage: the blue ink motif begins to diffuse — one loose open band of blue ink
  > threads with traces of muted gold drifting high in the air above the road,
  > stretching from above the near road toward the far crest where the road goes out
  > of sight, tied to no single figure, touching nothing on the ground, never on the
  > beam, never on any figure, no longer held in any doorway but not yet filling the
  > scene, behaving like wet ink bled into the paper's sky wash, never a glow.
- **material_closer:** "the loose blue-and-gold band beginning high in the air above
  the road is the only unusual ink on the page, and the beam and every figure on the
  road are free of any ink."
- **Fence:** `none`
- **Caption:** `("Let us go forth",)` *(KJV Heb 13:13 verbatim contiguous, 4)* ·
  **Corner note:** `NOTE: unto him` *(KJV — the destination three reviewers said the
  landing lacked; the picture's own far figure)*
- **Panel motions:** (1) a thin haze of dust drifts across the near prints; (2) the
  small far figures hold, tone-only; (3) the beam on the shoulders holds, the light
  across the wood warming very slightly.
- **Main animation:** Simon keeps walking away from the viewer along the road toward
  the far crest, one continuous steady stride the whole clip, his back to the viewer,
  the beam steady across his shoulders, never turning; Jesus and the two soldiers
  further along keep walking away at the same pace, never turning; the blue-and-gold
  ink threads high in the air drift smoothly within their own fixed band across the sky
  above the road; a low thin haze of dust drifts along the road; no new stain, spot, or
  darkening appears anywhere on the page at any point.
- **Why veo (advisory):** away-from-camera locomotion that only continues the drawing
  (no toward-camera motion, nothing on the line, no water — LAW 0's safe shape) plus
  fixed-band drift. **Why the turn lives in the still, not the clip:** LAW 0 — the
  still's own geometry does "turns to you"; no clip ever turns a camera or a figure.
  **Why NBP:** four figures AND a first-of-its-kind composition for the series (the
  from-behind road, the first free band) — never stack a cheaper model on a new
  composition. **Kling-only caution:** the first free-band page; contact-sheet it for
  growth before F08/F09 are spent. **Refs:** simon + beam + jesus + soldiers → approve
  → crop `road_ref`.

### F08 — "Reproach is shame. Bearing it is carrying it, as Simon carried the wood." (13w · Swirl 3 held, crop-limited · kling3_0, clip 5 · **seedream-4-5**) — THE FENCE PAGE

The close on the carrying — the one page where the drawing can insist at close range
that the thing on his shoulders is a plain beam with nothing on it. The three panels are
the narration's own verbs made physical. The horizon is drawn LOW so there is sky
above him for the dose to live in (LAW 4: the dose anchors to what the crop contains).

- **Panels** *(the narration's verbs — the wood / bearing / carrying)*
  1. `"the wood"` — the rough adzed grain and split raw end of a timber beam, close, no
     hands, nothing on the wood.
  2. `"bearing it"` — two hands gripping the underside of a beam from below, knuckles
     tight, close, no face.
  3. `"carrying it"` — two sandaled feet in dust under a load, the prints pressed deep,
     low and close.
- **Main scene** — `CLOSE-UP profile shot`:
  > {SIMON_BUILD} in profile facing RIGHT, from the waist up, the beam (BEAM_BUILD)
  > across the back of his shoulders behind his neck, both hands gripping it, his head
  > bowed a little under the weight, his neck and shoulders taut, sweat at his temple,
  > dust on his cheek and on the wood, his whole face fully visible in profile inside
  > the frame — his eyes open on the road ahead, his mouth closed — drawn in the same
  > steady, confident, single-struck line, no doubled or tremored contour; nothing on
  > the wood — no nails, no rope, no inscription, no blood, no marks of any kind, plain
  > raw timber; the horizon LOW, so that open sky fills the upper third of the frame
  > above his head and the beam; the road (ROAD_BUILD) small and soft in the far
  > background; no other figure anywhere in the frame; the ground dry, no water
  > anywhere; no hill, no crosses, no crowd. Stage 3 dosage, held: a few threads of the
  > loose blue-and-gold band cross the very top of the frame high in the sky, well
  > above the beam and his head, tied to nothing, touching nothing, never lowering
  > toward the beam or the man; the beam and the man free of any ink of any kind.
- **material_closer:** "the few blue-and-gold threads crossing the top of the sky are
  the only unusual ink on the page, and the beam and the man are free of any ink of
  any kind."
- **Fence:** `none`
- **Caption:** `("as Simon carried the wood",)` *(narration verbatim contiguous, 5 —
  one collapsed line, the hero-length precedent (ep7 F04 / ep11 F09), used here
  because it IS the fence's own phrase; fallback `("carried the wood",)` (3) if it
  crowds — §8)* · **Corner note:** `NOTE: reproach is shame` *(narration verbatim)*
- **Panel motions:** (1) the light across the grain warms very slightly; (2) the
  gripping hands tighten a little and hold; (3) dust drifts from around the pressed
  feet.
- **Main animation:** Simon's grip tightens on the beam and holds, his shoulders
  settling a little lower under the weight and holding there, one slow heavy breath,
  his head staying bowed, his eyes open on the road ahead, his lips closed and
  completely still; the few blue-and-gold threads high in the sky drift smoothly within
  their own fixed band at the top of the frame, never lowering; no new stain, spot, or
  darkening appears anywhere on the page at any point.
- **Why kling:** the grip-and-settle is a small completing gesture with a stated end,
  and close-up micro-motion is veo's OPEN item ("very little visible motion"). **Why
  seedream-4-5 — the one page where the locked tiering's validated case holds
  exactly:** a calm single figure, close, every ref already chained, NO other figure in
  frame for a mark to leak onto (the bake-off's one Seedream defect), and a DESIGNED
  POSE (bowed, gripping, taut) — the case the bake-off found Seedream got right where
  Nano Banana Pro didn't. 15cr vs 40cr. **Fallback:** if the seedream render garbles
  the caption or a panel label, draws a cross shape, or puts anything on the wood,
  regen ONCE on nano-banana-pro — never a second seedream attempt. **Refs:** simon +
  face + beam + road.

### F09 — "Simon was forced out. You are asked. Turn on your own road…" (21w · **Swirl 3** · veo3_1_lite advisory, clip 8 · nano-banana-pro)

The call, drawn as the viewer's own road: the near dust large at the bottom edge (the
viewer's feet just out of frame), Simon further along and smaller, Jesus and the
soldiers tiny at the crest about to go over — "after him." The whole upper air is
Stage 3, open outward. The caption is the grace line.

- **Panels**
  1. `"forced out"` — a soldier's hand gripping a man's upper arm through an oatmeal
     wool sleeve, close, no face *(rhymes F01 p2 — the same grip, the other man)*.
  2. `"asked"` — a single open hand, palm up, empty, offered toward the viewer against
     plain paper, no figure, no ink on or near it *(the invitation as a hand; NOT the
     anchor — stated no-blue; §8 for the fallback panel)*.
  3. `"after him"` — two lines of sandal-prints in dust running away from the viewer,
     one line a pace behind the other, no figure *(the back cover's motif, previewed)*.
- **Main scene** — `WIDE shot` from behind, very low:
  > the road (ROAD_BUILD) seen from the viewer's own standing place: the near dust of
  > the road large in the foreground at the bottom edge of the frame, the road running
  > straight away up the long gentle rise to the far crest, fully inside the frame; no
  > gate, no wall, no building anywhere in the frame; at mid-distance, further along
  > than before and smaller, {SIMON_BUILD} walking AWAY from the viewer along the road,
  > his back to the viewer, the beam (BEAM_BUILD) across the back of his shoulders,
  > both hands gripping it, the knot of his head-cloth at his nape, his rust-striped
  > mantle over his left shoulder, fully inside the frame, drawn in the same steady,
  > confident, single-struck line; at the far crest, tiny, {JESUS_BUILD} and
  > {SOLDIERS_BUILD} — exactly two soldiers — walking away, their backs to the viewer,
  > about to go over the crest but not yet gone; nothing visible beyond the crest — no
  > hill, no crosses, no crowd; the ground dry, no water anywhere. Stage 3 dosage: the
  > blue ink motif, with traces of muted gold, is woven through the whole upper air
  > above the road from the near foreground to the far crest — threads drifting in one
  > loose open band across the sky, tied to no single figure, touching no person, never
  > on the beam, never on the ground, behaving like wet ink bled through the page's own
  > sky wash, never a glow.
- **material_closer:** "the blue-and-gold band woven through the whole sky above the
  road is the only unusual ink on the page, and the beam, the road, and every figure are
  free of any ink."
- **Fence:** `none`
- **Caption:** `("You are asked",)` *(narration verbatim, 3 — the grace line, the one
  reviewers called "the only grace note," made the page's whole handwriting)* ·
  **Corner note:** `NOTE: freely this time` *(narration verbatim)*
- **Panel motions:** (1) the gripping hand holds, still; (2) the open hand holds, the
  light across it warming very slightly; (3) a thin haze of dust drifts across the
  prints.
- **Main animation:** Simon keeps walking away from the viewer along the road toward
  the crest, one continuous steady stride the whole clip, his back to the viewer, the
  beam steady across his shoulders, never turning; the tiny figures at the crest keep
  walking away at the same pace, never turning, not yet going over the crest; the
  blue-and-gold ink threads drift smoothly within their own fixed band across the whole
  sky above the road; a low thin haze of dust drifts along the road; no new stain, spot,
  or darkening appears anywhere on the page at any point.
- **Why veo (advisory):** away-locomotion plus a whole-sky fixed-band drift — veo's
  exact Stage 3 lane (ep7 F06, ep10 F09, ep11 F10 were all veo bands). Under Kling-only
  this is THE page to contact-sheet for band growth — the widest dose in the episode,
  with positive-only light wording throughout (no glint, no sparkle). **Why NBP:** four
  figures and the widest dose; a cheaper model has not been tested with a Stage 3 band.
  **Why the near dust is large:** "Turn on your own road" — the still puts the viewer's
  own road under the caption without any drawn viewer; the invitation is the ground you
  are standing on. **Refs:** simon + beam + jesus + soldiers + road.

---

## 7. Assembly suggestions (word-proportional, Fable estimates)

227 words over 103.44s ≈ 2.19 words/sec (one narrator turn, natural speed, no quote
pauses — proportions are approximate as always). **Boomerang nowhere in this episode**:
every unit walks in one direction, settles a completing gesture, drifts a band, or
drifts dust — all of which read backwards under reversal, and here the worst case is
the worst in the series (a reversed walk sends Jesus back IN through the gate). **Every
clip is designed ≥0.9s shorter than its estimated slot** — not just shorter: ep11's
real alignment timestamps tightened three slots below their word-proportional
estimates, freeze can pad but never trim, and the hero drifted 1.35s off its chord as
the accepted result. So: **compute the real slots from `narration.alignment.json`
(forced-align the locked audio first — the score-design-early rule) BEFORE setting any
`clip_duration`,** and only then confirm the numbers below. Every frozen tail is under
SW-F1's 35% (`MAX_FREEZE_STATIC_RATIO`). Final modes are an assembly-QC call on the real
renders — real playback, per the standing rule.

| Unit | Words | ≈Slot | Clip | Lane (advisory) | Frozen | Suggested mode |
|---|---|---|---|---|---|---|
| front | 14 | 6.4s | 5s | veo | 22% | freeze (a walk — never boomerang) |
| f01 | 25 | 11.4s | 10s | veo | 12% | freeze (two walks — never boomerang) |
| f02 | 21 | 9.6s | 8s | kling | 16% | freeze + tail_loop ~1.0 (knees and hands settle) |
| f03 | 22 | 10.0s | 8s | veo | 20% | freeze (a walk — never boomerang) |
| f04 | 14 | 6.4s | 5s | veo | 22% | freeze |
| f05 | 28 | 12.8s | 10s | veo | 22% | freeze |
| f06 | 28 | 12.8s | 10s | kling | 22% | freeze + tail_loop ~1.0 (head settles lifted) |
| f07 | 17 | 7.7s | 6s | veo | 23% | freeze |
| f08 | 13 | 5.9s | 5s | kling | 16% | freeze + tail_loop ~1.0 (grip settles) |
| f09 | 21 | 9.6s | 8s | veo | 16% | freeze |
| back | 24 | 10.9s | 8s | veo | 27% | freeze (drifting dust — be safe; 10s if the bridge accepts it) |

Sum 227 = the narration's own count; 103.44s locked audio + landing hold ≥3.0s
(INV-26). Lane split: 3 kling (the completing-gesture pages F02, F06, F08) / 6 veo
pages + 2 veo covers — veo-first where the shot allows it, including every walking
page (continuation, not completion). **The OpenArt bridge has no veo model —
`model_tier` is advisory there and everything renders via Kling 3 Omni unless the user
explicitly sets `SWIRLS_GEN_PROVIDER=hf` for a specific clip (ep7 F04's documented
one-off exception, never a policy change).** Under Kling-only, the places the advisory
tier actually changes the risk are: the three consecutive Stage-3 band pages (F07, F08,
F09 — contact-sheet each for band growth before the next is spent), and F01's two
converging walks over a 10s clip (watch for a staged meeting). 10s clips are ep10's
OpenArt precedent; 4-8s are ep11's; nothing here exceeds 10. Still credits (estimate
only): 8 pages × 40cr + 1 page × 15cr + 2 covers × 40cr = 415cr; the ledger (`/cost`,
`/spend`) is the only truth.

**Render/spend order** (refs gate everything — §3): F04 → crops (simon, face, beam,
gate) → F02 → crop soldiers → F01, F03, F05, F06 (any order) → F07 → crop road → F08,
F09 → front cover → back cover. Animate nothing until every still has passed the eye-QC
(direction first, then the beam's shape and its bare surface, then the soldier count,
then baked text, likeness, layout, dose, no un-requested text, every MUST-SHOW in
frame) and the LAW 4 referent check against the rendered pixels.

**Score note for the next stage (not designed here):** this is the most somber
narration in the series — a man walking under a beam toward an execution, Hebrews'
quiet typology, a landing on "his own blood" — with a delivery-tag arc of quiet →
matter-of-fact → deliberate → emphasized. The bank's locked default (B, a driving
135-bpm dream-trance) would fight it; the sparse felt-piano direction the user loved on
ep8 and evolved on ep4/ep10 is the register to check first, and the D/E "built around
its breakdowns" idea fits the hush at "Now he is through the gate." Design it from the
real alignment timestamps, early, per the standing rule.

---

## 8. OPEN QUESTIONS (do not silently resolve)

1. **Front-cover title** — `THE CROSS THAT WASN'T HIS` (the locked episode title; ep7's
   paraphrase-title precedent; **carries an apostrophe, the known baked-punctuation
   failure zone**) vs `WALKING THE OTHER WAY` (4, the hook verbatim contiguous, no
   punctuation) vs `THE OTHER WAY` (3). I recommend the episode title with a mandatory
   2×-zoom check on the apostrophe; fall back in that order if it renders as a pasted
   glyph.
2. **seq_title** — `WITHOUT THE GATE` (recommended: 3 words, Hebrews 13:12 verbatim, the
   hinge phrase, no punctuation) vs the episode title (5 words + apostrophe, rendered
   nine times as a running header) vs `SIMON` (1, the Thomas pattern). User's call.
3. **Back-cover title + subtitle** — `THROUGH THAT GATE FIRST` / `HEBREWS 13:13`
   (recommended: the picture's own line, the priority that IS the fence, and the
   go-forth-unto-him verse the thread points to) vs `WITH HIS OWN BLOOD` / `HEBREWS
   13:12` (the fence's own last words over an empty doorway — reads as "done"). Both are
   verbatim narration; keep the verse and the phrase from the same verse whichever way.
4. **Beam vs full cross.** The popular image is a full cross; the honest object and the
   narration's own word ("the wood") is a beam, and the fence (§2 rule 1) is far safer
   with a beam than with a crucifix icon on Simon's back. Recommended: the beam, ep7's
   bier-not-coffin precedent. If the user wants the full cross, rules 2-6 still hold
   and the risk of the Via-Dolorosa prior on F01 rises sharply.
5. **The crown of thorns on F01.** Mark 15:17 puts it on; the text never says it came
   off; v20 says "put his own clothes on him, and led him out." I chose restraint (bare
   head, no crown, no blood) on the series' own no-gore rule and the Gold Exemplar's
   restraint lesson. If the user wants the crown, it is one text line on F01 and the
   front cover's tiny figure — and a regen magnet for blood.
6. **Jesus carrying the beam on F01 at all.** Mark says "led him out"; John 19:17 says
   he went out bearing his cross. I put the beam on Jesus on F01 so "the cross of Jesus"
   / "the cross that wasn't his" has a visible referent before it moves to Simon; the
   alternative (a soldier carries it in, Jesus walks unburdened) is textually equally
   defensible from Mark alone and removes the Passion-prior risk. User's call; my
   recommendation stands.
7. **Debut on F04 (a quadruple crop — simon, face, beam, gate — from one single-figure
   approval)** vs debut on F03 (the turn page, four figures, where every recurring
   subject is at cropable size). F04 is the simplest page in the episode; budget two
   regen cycles for the debut either way.
8. **Seedream — F08 only, by design.** Candidates that did NOT make the cut and the
   condition that would promote them: **F05** (calm single figure, but its three type
   panels are the episode's most content-critical diagram; promote only if F08's
   seedream render holds its own panels and captions clean, and only at the user's
   call); **F04** (never — it is the debut); **F09** (no — four figures and the widest
   Stage 3 dose, untested on any cheap model); **F07** (no — a first-of-its-kind
   composition). If the user wants more savings, F05 is the one to try.
9. **`NOTE: Hebrews 13` on F05** — a numeral in handwriting is the same baked-glyph risk
   as punctuation (frame numbers render clean every page, so the risk is low, not
   zero). It does real work (the attribution the ear lost). Fallback `NOTE: the sin
   offering` (narration verbatim).
10. **F08's caption** — `as Simon carried the wood` (5 words, the fence's own phrase,
    the hero-length precedent) vs `carried the wood` (3). Recommend the five; fall back
    if it crowds or wraps.
11. **F01's converging walks over a 10s clip.** Two figures walking toward each other
    is a "meeting" prior; the still puts the full frame width between them and the
    clause says a long stretch of road stays between them. If the contact sheet shows
    Simon reaching the gate, cut `clip_duration` to 8 (30% frozen — still under the cap)
    rather than reroll.
12. **10s clips on the OpenArt bridge** (F01, F05, F06) — ep10's precedent; ep11 used
    4-8. Confirm the bridge accepts 10 before the first 10s spend; 9 is untested on
    OpenArt — avoid it unless confirmed.
13. **The unburdened override (front cover, F01)** — `simon_ref` carries the beam; the
    two unburdened pages override it by text (the ep11 loosed-cloth pattern). If the
    front cover keeps rendering a beam on him, crop `simon_unburdened_ref.png` from
    F01's approved main scene (he is foreground-sized there for this reason) and
    rechain the cover.
14. **Hero nomination = F06** (the Hebrews 13:12 page, Christ's act named, Jesus a pace
    ahead) — for the main engine's hero-bookend rule and any thumbnail; the Swirls
    assembly bookends with the covers. Alternate **F03** (the turn, the first blue at
    the threshold) if the user wants the more graphic single image.
15. **The camera turn (F07-F09 from behind)** is a first for the series and is the
    whole visual answer to "Hebrews turns to you." Risk: the from-behind pages read as
    a different place. Mitigation: `road_ref` chained into F08/F09, the same dry ochre
    country, the same figures at the same relative distances. If F07's first render
    reads as a location change on watch, fallback: keep the profile axis on F07-F09 with
    the gate beyond the LEFT edge (ep11's F04 pattern) and the band entering from the
    left — one line to change per page, the meaning survives, the "turn" is lost.
16. **Soldiers' kit.** The prior is the Hollywood legionary (red cape, plume, drawn
    sword). The build bans all three; accept variance in the cuirass type; regen only on
    a cape, a plume, a drawn weapon, or a sneer.
17. **The back cover's two footprint lines** — a one-page element the model may render
    as a single path or a cart-rut. Regen criterion: two distinct lines readable as
    prints, one a pace behind the other.
18. **Simon's appearance.** Cyrene is in Libya; the traditional image of Simon is "the
    African who carried the cross." The text gives only his city. The build says "deep
    sun-browned," no costume of otherness (the ep11 Samaritan guard). If the user
    prefers the traditional depiction, it is a build-text change and the same
    one-figure-only-mark clauses still apply; if a render caricatures him either way,
    regen.
19. **F09 panel 2 (`"asked"` — an open offered hand).** Risk: reads as Jesus's hand or
    grows a glow. It is stated no-ink, no figure. Fallback panel: `"your own road"` — a
    fork in a dry road, no figure.
20. **Nothing on any page shows the crucifixion, Golgotha, the crowd of Luke 23:27, the
    daughters of Jerusalem, the second thief, or the titulus** — deliberate, all of it.
    The narration never goes there and the fence forbids the site. Listed so the
    implementation pass never adds any of them "for context."
21. **No bundle, pack, or staff on Simon anywhere** — deliberate (an invention magnet).
    If the user wants "coming out of the country" carried by an object, the safest is
    a short-handled mattock over the shoulder on the front cover and F01 ONLY, dropped
    on the F01→F02 cut, never seen again; not recommended.
22. **Score direction** (flag only, §7): the narration's register breaks from the
    bank's groove default; the next stage should check the felt-piano direction before
    generating.
