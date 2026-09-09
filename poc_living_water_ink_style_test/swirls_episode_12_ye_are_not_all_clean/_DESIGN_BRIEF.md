# DESIGN BRIEF — Episode 12, "Ye Are Not All Clean"

John 13:1-30 (Jesus washes the disciples' feet at the Last Supper, knowing Judas will
betray him; "ye are clean, but not all"; the sop; Judas exits into the night) · Dead
ink: **NONE — no Stain, no Fray, on any page.** Reasoned, not defaulted (§2): the
narration's own point is that Judas's exclusion was a matter of a heart Jesus already
knew, not a visible defect — a Stain on him would draw exactly the thing nine rounds of
narration review fought to avoid (treating cleanness as a mark you can see rather than a
heart Jesus reads). No figure wavers or doubts on-page either (Judas's betrayal is
already decided before the episode opens — "the devil had already put into the heart of
Judas" — so a Fray, which reads as doubt-in-progress, would misdate the moment). NT
episode, Jesus present and active on every page except the two Judas-alone pages (F04,
F05) — Stage 3 is reached only on the back cover, the direct address to the viewer ·
`panel_style` **woodcut_hybrid** throughout · Voices: **narrator only** (confirmed at the
audio-tag stage — no speaker roster beyond narrator; lips stay closed on every figure on
every clip).

Sonnet design pass, 2026-09-09 (routine per-episode design inside an already-established
house style — not a major creative pivot, so this does not go to Fable per the standing
"Fable for major pivots only" rule). This brief is the single creative source for the
implementation pass (episode.py PageSpec/CoverSpec objects). Narration and audio are
LOCKED — **167 words** (my own count of `narration.md`), **74.55s natural,
`narrator_atempo_factor 1.0`** (no time-stretch), one narrator turn, no quote pauses (no
second voice). Nothing here changes a spoken word. Every choice states its WHY. Open
questions are flagged inline and collected in §8 — do not silently resolve them.

---

## 0. The shape of the episode, in one paragraph

The narration is built on one collective act (the washing) and one solitary exit (the
night), and the whole design turns on keeping those two physically apart on the page —
the plan-only pass that cleared this episode before the narration was even finalized
found that John 13:1-11's washing is dramatized as a group action with only Peter's own
exchange individually staged, and Judas's distinct beat lands later, at the sop and the
door, never at the basin. So the episode's geometry is a **room split into two zones that
never touch inside one panel**: the LOW table where Jesus kneels and washes — collective,
warm-lit, where the Swirls-of-Life ink motif is allowed to live — and the DOOR at the
room's edge, unlit, motif-free, where Judas's own moment happens. No page shows Judas's
own feet at the basin in contact with any blue ink; no page shows the door with any blue
ink in frame. The first hard problem — staging "Jesus did not wash those feet because
Judas earned it" as a picture, not an argument — is solved by anchoring the whole
episode's motif to the ACT of washing itself, not to any one recipient: the ink rises
from the water in the basin, never from a foot, never from a face, so it reads as
something Jesus is doing, not something anyone is receiving on merit. The second hard
problem — Judas must look like nothing, not like a villain — is solved by giving him no
mark of any kind (§3): same build register as the ten other disciples, an ordinary
place at the table, no darker palette, no shifty features, no visible stain. He is
indistinguishable until the text itself distinguishes him. The third hard problem — the
final beat turns to the VIEWER, not to Judas's own redemption, and the piece must not
show Judas reconciled — is solved by keeping Judas OFF the hero page and off the back
cover entirely: his last appearance is F05, walking out; the hero (F06) and the landing
(back cover) both return to Jesus and the basin, never back to Judas. Swirl arc
0·0·1·1·0·0·2·3 (front · F01 · F02 · F03 · F04 · F05 · F06 · back); no Stain, no Fray
anywhere. Hero = F06.

---

## 1. Narration beat map → units (why six interior pages)

Word counts are my own count of the locked text (11 + 37 + 33 + 34 + 31 + 21 = **167**;
74.55s ≈ 2.24 words/sec, 0.446 s/word — close to episode 13's 0.456, a plain, direct
delivery). One narrator turn, no quote pauses (no second voice), landing hold ≥3.0s
(INV-26) still applies at assembly. **Real slots come from `narration.alignment.json`
(forced-align the locked audio first) before any `clip_duration` is fixed** — every clip
below is designed with ≥0.9s headroom under its word-proportional estimate, same
discipline as ep11/ep13.

| Unit | Narration beat | Words | ≈Slot | Voice |
|---|---|---|---|---|
| **front** | "Judas walked out into the night on feet Jesus had washed." | 11 | 4.9s | narrator |
| **F01** | "John says the devil had already 'put into the heart of Judas Iscariot, Simon's son, to betray him.' Jesus knew." | 20 | 8.9s | narrator (KJV) |
| **F02** | "He knew as He poured the water. He knew as He dried their feet with the towel." | 17 | 7.6s | narrator |
| **F03** | "Then He told them, 'ye are clean, but not all.' And He quoted the old word for betrayal, from Scripture: 'He that eateth bread with me hath lifted up his heel against me.'" | 33 | 14.7s | narrator (KJV) |
| **F04** | "He handed Judas the sop — a piece of dipped bread. 'That thou doest, do quickly.' Some at the table thought he had gone to buy food." | 25 | 11.2s | narrator (KJV) |
| **F05** | "Judas 'went immediately out: and it was night.'" | 9 | 4.0s | narrator (KJV) |
| **F06 — HERO** | "Jesus did not wash those feet because Judas earned it. He washed them knowing Judas would betray Him anyway. That is what His love does when it already knows the worst." | 31 | 13.8s | narrator |
| **back** | "He knows your heart, every corner of it, like that. He has not put the towel down — bring Him your worst." | 21 | 9.4s | narrator |

Sum 11+20+17+33+25+9+31+21 = **167** = the file's own count.

**Why the second paragraph (37w) splits into F01+F02.** F01 is entirely interior — "the
devil had already put... Jesus knew" — a fact about what Jesus already knows, not yet an
action; it wants a contemplative page, Jesus's own face, before anything visible starts.
F02 is entirely action — pouring, drying — the concrete washing the motif needs to live
in. Splitting them lets the motif dose apply cleanly to F02 (the washing) without
crowding F01 (the knowing), and gives the "he knew" beat, which sound-doctrine review
flagged repeatedly across nine narration rounds as the piece's real hinge, its own
uncrowded page.

**Why the fourth paragraph (34w) splits into F04+F05.** The sop/dismissal/misunderstanding
(25w) and the exit itself (9w — "and it was night") are two different pictures: a lit
table scene and a dark doorway. Nine rounds of narration review kept circling back to
"and it was night" as the piece's single darkest, most load-bearing line; giving it a
whole page (even a small one, 9w/4.0s, at the series' floor alongside ep11's F04 12w/4.8s
and ep13's F08 13w/5.9s) lets the eye hold the silence the ear gets from the narration
gate's own pause discipline. Splitting also enforces the zone-separation rule
structurally: F04 is the last page with the table/basin in frame; F05 is Judas alone at
the door, and no page after F03 shows the basin again until F06 returns to it by
implication (in narration only — see §2).

**Why not merge F02+F03, or F03+F04.** F02 (the washing, no words yet from Jesus) and F03
(Jesus SPEAKING, "ye are clean, but not all" + the Scripture quote, 33w — this episode's
single densest page) are different registers: action, then the spoken reveal. F03 is long
for one page (14.7s, above ep13's F05/F06 at 12.8s) because it carries the episode's own
title line AND the betrayal prophecy in one breath — the plan-only pass already confirmed
these two quotes belong at the same table beat, before Judas's own distinct moment at the
sop; splitting them would separate two things the text keeps together and buy nothing.
F03+F04 stays split because F03 is still at the table (the room, Jesus speaking to the
group) while F04 begins Judas's own zone (the sop specifically given to him) — the exact
line the zone-separation rule draws.

**Why not eight, or five.** Eight would need another split; the only candidate is F03
(33w) at its internal comma ("ye are clean, but not all" / the Scripture quote), but both
halves are short (roughly 10w/16w) and neither carries a picture-change strong enough to
justify a ninth page on a 74.55s piece — ep13's own floor pages (13-14w) are already
close to what half of F03 would be. Five would require merging F01+F02 (losing the
knowing/washing register split, §1 above) or F04+F05 (losing the table/door split, the
episode's own hinge). Six interior pages for 167 words (74.55s) sits proportionally
between ep11 (202w/80.61s, 10 pages) and ep7/ep8-scale shorter pieces — this episode
reads faster and simpler than either, and six pages is what its own beats actually give.

---

## 2. The hard problems, the dead-ink decision, then the motif arc

### Hard problem #1 — grace as a picture, not an argument: anchor the motif to the ACT

"Jesus did not wash those feet because Judas earned it... that is what His love does when
it already knows the worst" is the piece's rhetorical peak (F06) — and it is a claim about
MOTIVE, which cannot be drawn directly. The fix: the Swirls-of-Life ink motif is anchored
to **the water in the basin itself**, never to a foot, a face, or a hand receiving
anything — so its presence reads as "something Jesus is doing" (an act, freely given),
never as "something someone has earned or been given more/less of." This also protects
the zone-separation rule mechanically: an anchor tied to the basin cannot accidentally
drift onto Judas at the door, because the basin and the door are never in the same frame
after F03.

### Hard problem #2 — Judas must look like nothing

Nine rounds of narration review circled the same danger from every direction: any visual
choice that marks Judas as different-looking risks implying his exclusion was visible,
knowable, deserved — exactly the doctrine the narration fought to avoid ("ye are clean,
but not all" names a heart Jesus already knew, not a defect anyone else could have seen).
So Judas's build (§3) is deliberately unremarkable: same era, same class of dress, same
steady single-struck line as every other disciple, no darker palette, no shadowed face,
no shifty eyes, nothing "villain-coded." He is one of the twelve until the text itself
names him.

### Hard problem #3 — the ending turns to the viewer, not to Judas's redemption

The narration's landing ("He knows your heart... bring Him your worst") is addressed past
Judas, to the listener — the piece does not resolve Judas's own story, and the design must
not either. Judas's last appearance is F05 (walking out into night); he does not reappear
on F06 (the hero, which returns to JESUS's motive, not to Judas) or on the back cover
(which addresses the viewer directly, with no human figure at all — see §4). No page
implies Judas turned back, was forgiven on-page, or is shown at peace.

### Dead ink — reasoned, not defaulted: NONE

- **Stain on Judas — REJECTED, and it would be a doctrine error** (hard problem #2,
  above). The Stain's own grammar in this series is a visible mark of uncleanness IN a
  figure; putting one on Judas would assert exactly what nine narration rounds fought to
  avoid saying — that his exclusion was a visible defect rather than a heart Jesus already
  knew. The whole point of "ye are clean, but not all" is that nothing on the outside told
  the difference.
- **Stain on the OTHER disciples — REJECTED, obviously.** They are the ones Jesus calls
  clean; the paper under every disciple but Judas on F02-F03 is exactly as clean as the
  paper under Jesus.
- **Fray on Judas — REJECTED.** Fray reads as doubt-in-progress, a wavering line. Judas's
  betrayal is not wavering — "the devil had already put into the heart of Judas... to
  betray him" (F01) states it as already decided before the episode even opens. A frayed
  line on him would misdate the moment, drawing hesitation the text never gives him. He is
  drawn in the same steady, confident, single-struck line as every other figure, on every
  page, including F04 and F05 — the steady-line override is stated explicitly on both.
- **What carries the tension instead:** ZONE (the basin's warm light vs. the door's dark;
  motif present vs. motif absent) and the KNOWLEDGE ASYMMETRY (Jesus's calm, direct gaze
  on every page he shares with Judas — he knows, and nothing on his face changes toward
  him). Both are story geometry and expression, not motif.

Consequence for the code: `fence_kind="none"` on every page; every page's
`main_scene_animation` still ends with the page-global no-new-mark clause ("no new stain,
spot, or darkening appears anywhere on the page at any point").

### Swirl (living blue-and-muted-gold ink) — anchored to the WATER, never the man

| Page | Stage | Anchor |
|---|---|---|
| front | none | Covers carry no interior motif; the lighting law carries the tension |
| F01 | **0** | Absence stated — this page is entirely interior/contemplative (Jesus's own knowledge, before any washing begins); no blue ink anywhere |
| F02 | **1** | Exactly one restrained thread of blue ink rising from the surface of the water in the basin itself as Jesus pours/dries — touching only the water and the air just above it, never a foot, never a hand, never Jesus's own hands, never any disciple's face; the only blue on the page |
| F03 | **1 held** | Same single thread, same basin, now small and a little apart as the frame widens to include the room and Jesus speaking; NO blue anywhere near Judas even though he is present in this wider room shot (he sits at a distance from the basin — the zone-separation geometry, stated explicitly in the still prompt, §6) |
| F04 | **0** | Absence stated — Judas's own zone begins here; no blue ink anywhere on the page, even though the same room and (unlit, out of frame or backgrounded) basin exist in the world of the scene |
| F05 | **0** | Absence stated — the door, the night, Judas alone; no blue ink, no warm light at all; this is the episode's darkest page by design |
| F06 — hero | **2** | The blue ink motif returns, now quietly present rather than a single restrained thread — a few soft threads and one small amorphous watercolor bloom hanging in the air just above an empty basin (Jesus is remembered/implied by the water and the towel laid across the basin's rim, not necessarily by his own figure — see §6 open question) — present but not spectacular, echoing F02 without repeating it |
| back | **3** | Diffused — a loose, open band of blue-and-muted-gold threads drifts across the whole width of the frame, tied to no object and no figure at all — the first page in the episode where the ink is not anchored to the basin, because this is the moment the invitation moves off the page and toward the viewer |

- **Why the basin, not a hand (departs from ep7/ep10/ep11's proven hand-anchor):** every
  prior episode's motif rose from a person's hand or a threshold a person crossed. This
  episode's whole design problem is keeping the motif OFF the person receiving it (to avoid
  implying earned/unearned visibility) — so the anchor has to be the ACT's own instrument,
  the water, not anyone's body. This is a genuine departure from precedent and is flagged
  in §8 for confirmation before the first render.
- **Why F03 holds at Stage 1 instead of advancing to Stage 2.** F03 is still the same table
  beat as F02 (the group has not yet moved, Jesus is still speaking to the room), and it is
  also the page where Judas is first shown seated among the others (at a distance from the
  basin) — advancing the dose here would put a growing motif in the same frame as Judas's
  own first appearance, which is exactly the contact the zone rule forbids. Holding flat
  keeps the frame's growing tension (the room now knows something is wrong) from reading as
  a growing motif near Judas.
- **Why F04 and F05 drop to 0 rather than holding at 1.** The zone-separation rule is not
  "the motif doesn't touch Judas" alone — it is "Judas's own zone carries none of it," a
  clean-paper band. Holding a distant, contained thread somewhere off-frame would be a
  half-measure; dropping to true absence is the stronger, clearer version of the same rule,
  and it gives F05 ("and it was night") real visual silence to match the narration's own
  starkness.
- **Why F06 returns to Stage 2, not Stage 1 or Stage 3.** F06 is a reflective/summary page,
  not a continuation of the literal washing scene (Judas has already left; this is Jesus's
  motive stated as a principle). Stage 2 (present, not yet diffused) matches the register of
  a page that is stating a truth rather than depicting the peak of an unfolding scene — ep13
  used the identical logic to hold its own hero at Stage 2, reserving Stage 3 for the true
  final-address pages.
- **Why the back cover alone reaches Stage 3.** The direct-address landing ("He knows your
  heart... bring Him your worst") is the only beat in the piece addressed to the viewer,
  not to anyone inside the story — diffusing the motif off any anchor at all, for the first
  and only time, matches that shift from "watching a scene" to "being spoken to."

### High-tide check, every page (`stainDose + swirlStage <= 4`)

Trivially satisfied — no Stain anywhere — but recorded so the gate has a row per page:

| Page | Stain | Swirl | Sum | Note |
|---|---|---|---|---|
| F01 | 0 | 0 | 0 | ✓ |
| F02 | 0 | 1 | 1 | ✓ — the gospel turn: grace visible the moment the washing starts |
| F03 | 0 | 1 | 1 | ✓ — held flat, kept away from Judas's first appearance |
| F04 | 0 | 0 | 0 | ✓ — Judas's own zone, clean paper |
| F05 | 0 | 0 | 0 | ✓ — the darkest page, by design |
| F06 | 0 | 2 | 2 | ✓ |
| back | 0 | 3 | 3 | ✓ |

**The gospel turn = F02**, the moment Jesus begins washing — not F01 (knowledge alone, no
act yet), not F06 (the act is already over; F06 only names why it happened).

### The ZONE guard — this episode's literalism trap

Every page states, explicitly, whether the basin is in frame, whether it carries any
ink, and where Judas is relative to it. F02-F03: basin in frame, ink present, Judas absent
(F02) or seated at a stated distance from it (F03). F04-F05: basin absent from frame
entirely (F04 may background it, unlit; F05 has no basin at all — a doorway/night
exterior). A render that puts any blue ink in the same frame as Judas, at any dose, on any
page, is a regen before anything else is checked — the eye-QC checks this FIRST on every
page Judas appears on (§5).

---

## 3. Refs — who and what needs pinning

All new refs live in this episode folder's `refs/`
(`F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_12_ye_are_not_all_clean\refs\`).
Chain order is hard (render_still stops on a missing ref).

### Characters

**JESUS** — SERIES CONSTANT. Already in place:
`.claude/skills/swirls-of-life/references/jesus_ref.png` (the same approved crop every
prior episode used). No redesign, no approval cycle. JESUS_BUILD reused verbatim from
ep11/ep13:

> Jesus, a Judean man in his early thirties, medium height and ordinary build,
> sun-browned skin, shoulder-length dark brown hair pushed back from his face, a
> short full dark beard, wearing a simple ankle-length robe of undyed cream-brown
> wool with a plain olive-toned mantle draped over one shoulder, a narrow rope belt,
> and flat worn leather sandals -- no halo, no glow, nothing in his dress
> distinguishing him from the men around him, standing square, still, and
> unhurried, his gaze steady and direct

**Per-page guard, every page with Jesus at the basin (F02-F03):** he kneels or crouches at
the basin, sleeves/hem gathered practically, a plain linen towel girded at his waist
(John 13:4's own detail) — state on both pages: *"his face calm, unhurried, his expression
unchanged toward the man he already knows will betray him — no sorrow, no anger, no
distress visible on his face."* This last clause is the episode's real fragility point:
the natural render instinct on "Jesus knows Judas will betray him" is to draw grief or
tension in Jesus's face, which would visually pre-empt F06's own claim that his motive was
love, not resignation. **Where Jesus appears:** F02 (kneeling at the basin, medium),
F03 (a little further back, still near the basin, speaking to the room, medium), F06
(optional — see §8 open question on whether F06 shows him at all or only the basin/towel).
NOT on F04, F05, front cover, or back cover.

**JUDAS ISCARIOT** — new to the series, and the episode's central design problem (§2, hard
problem #2). Build text (use verbatim):

> Judas Iscariot, a Judean man in his thirties, ordinary build and height, sun-browned
> skin no different in tone from any other disciple in the room, dark hair cut and
> combed the same plain way as the other disciples, a short trimmed dark beard,
> an ordinary calm face with no scowl, no narrowed eyes, no shadow cast across it
> that is not cast the same way on every other face in the room; wearing a simple
> knee-to-ankle-length robe of undyed grey-brown wool, a plain rope belt, a small
> worn leather coin-purse at his belt (the one small, honest, textual detail — he
> "had the bag," John 13:29 — and the ONLY thing that distinguishes him from the
> other eleven at a glance); no dark palette, no isolated seating, no visual cue of
> any kind beyond the purse; drawn in the same steady, confident, single-struck
> line, with the same care, the same line weight, and the same dignity as every
> other figure in the room

**Why this build.** The whole design problem is that Judas must NOT look different — the
narration's own point is that nothing visible marked him. The coin-purse is the one
concession: it is textually attested (13:29, "some of them thought... that Jesus had said
unto him, Buy those things that we have need of"), it is small and easy to miss on a first
look (exactly right — nobody at the table noticed anything either), and it gives the
implementation pass one stable, non-symbolic detail to track him by across pages without
resorting to a dark robe or a marked face. **The one-figure-only-mark rule applies:** no
other disciple carries a coin-purse or bag on any page.

**THE OTHER DISCIPLES** — a shared GROUP identity (the ep11 `ten_ref` pattern), no
individual faces beyond Jesus and Judas. Build text (use verbatim on every table page):

> a group of Judean men in their twenties to forties, ordinary builds, sun-browned
> skin, plain undyed robes in earth tones (cream, grey-brown, olive), simple rope
> belts, seated or reclining around a low table, drawn as ordinary men at an ordinary
> meal, their faces calm or attentive, never caricatured; drawn in the same steady,
> single-struck line as every figure in the room

Why a group, not named individuals: only Peter's exchange is individually dramatized in
John 13:1-11, and this narration doesn't quote it — the room can stay a general company.
Ref: `disciples_ref.png` cropped from **F03 approved** (the widest room shot, several
figures together).

### Objects / locations

**THE BASIN AND TOWEL** — the episode's title objects, in frame on F02-F03 (and echoed,
empty, on F06 — see §8). Build text (use verbatim):

> a wide shallow basin of plain hammered bronze, its water within it, resting on the
> floor beside a low table; a plain undyed linen towel, long enough to gird about the
> waist, its cloth simple and unmarked; no ornament, no color, no pattern on either
> object

**Why plain bronze and plain linen:** John 13:4-5 names both objects without ornament; the
render risk is a model defaulting to something more elaborate (silver, patterned cloth) —
stated plainly to keep the objects from drifting into something ceremonial-looking rather
than ordinary household ware. Ref: `basin_towel_ref.png` cropped from **F02 approved**
(the basin, the water, and the towel together, no figure needed in the crop itself if
avoidable).

**THE SUPPER ROOM** — the location of F01-F04 and F06 (implied). Build text (use
verbatim):

> the interior of a plain upper room by lamplight: a low rectangular table surrounded
> by simple cushions and low couches, a few clay oil lamps burning on stands or ledges
> giving warm low light, plain plastered walls, no windows showing night sky directly
> in frame, simple clay dishes and bread on the table, no luxury, no ornament

Ref: `supper_room_ref.png` cropped from **F01 approved** (the room's walls, lamps, and
table, minimal figures in the crop).

**THE DOORWAY AT NIGHT** — the location of F05 only. Build text (use verbatim):

> a plain doorway at the edge of the same upper room, its wooden door standing open
> onto a dark stone stairway or passage beyond, lit only by the faint warm spill of
> lamplight from the room behind, spilling no more than a step or two past the
> threshold; beyond the doorway, near-total darkness; no stars, no moon, no other
> light source of any kind visible

**Why the near-total dark:** "and it was night" is the narration's own last word on Judas;
the page should be the visual opposite of every other page's warm lamplight, with no
competing light source to soften it. Ref: `doorway_ref.png` cropped from **F04 approved**
(if the doorway is visible in F04's background) or rendered fresh on F05 if not — flagged
in §8.

**No other objects.** No bread basket, no wine cup singled out, no ornamented dish — the
sop itself (F04) is a small detail within the table scene, not a separate object needing
its own ref (it is a piece of the bread already on the table, dipped, per John 13:26).

### Chain order (hard dependencies)

1. `jesus_ref.png` — already present (immediate, no cycle).
2. **F01** renders with `refs=[jesus]` — the supper room and the disciples debut, wide,
   calm → approve → crop `supper_room_ref`.
3. **F02** (jesus + supper_room; Judas debuts here, seated, but the frame is on the
   basin) → approve → crop `basin_towel_ref`, `judas_ref` (if his face is large enough at
   this distance — otherwise defer the Judas face crop to F03), `judas_face_ref`.
4. **F03** (jesus + supper_room + basin_towel + judas + judas_face; the wider group
   debuts) after 3 → approve → crop `disciples_ref`.
5. **F04** (judas + judas_face + supper_room; the doorway may debut in background) after
   4.
6. **F05** (judas + judas_face + doorway) after 5 (or fresh, if the doorway wasn't
   visible in F04 — §8).
7. **F06 — hero** (jesus + basin_towel; Judas absent) after 3.
8. **Front cover** (judas + judas_face; supper_room in background, small) after 4.
9. **Back cover** (no figure refs needed — see §4) after none (can render early).

---

## 4. Covers

### The cover judgment call (stated, as the format asks)

The hook is Judas walking out on feet Jesus had washed; the landing turns past Judas to
the viewer. So the covers do NOT mirror each other the way ep13's did (a road with two
ends) — they are asymmetric on purpose: the front carries the episode's one human figure
in motion (Judas, mid-exit, small and dark against a lit doorway behind him — the hook's
own picture), and the back carries NO human figure at all (the basin and towel alone,
echoing F06, under the landing's own words) — the object-landing pattern (ep7's bier,
ep11's pressed dust), chosen because this episode's landing is addressed to the viewer,
not to any character's fate, and putting a face on the back cover (Jesus's, or worse,
Judas's) would risk exactly the "whose story is this ending on" confusion §2's third hard
problem exists to prevent.

### FRONT COVER

- **Scene:** {JUDAS_BUILD} in silhouette-leaning low light, mid-stride, walking away from
  the viewer through a plain doorway into darkness beyond it, his back and side visible,
  his face turned slightly away (not fully hidden — enough that `judas_face_ref` still
  reads, but not a front-on portrait); behind him, filling most of the frame, the warm
  lamplit edge of the room he is leaving — a corner of the low table, a hint of the other
  disciples as soft, smaller, out-of-focus shapes, no blue ink anywhere; ahead of him
  through the doorway, near-total darkness, no stars, no other light.
- **Lighting (law: ≥1 warm + ≥1 cool):** warm low lamplight filling the room behind him,
  catching the edge of his robe and shoulder as he moves away from it; cold near-black
  darkness ahead of him through the doorway. WHY: the warmth is everything he is walking
  away from; the cold is where he is going.
- **Motif:** none (covers never carry the interior motifs).
- **Title:** `YE ARE NOT ALL CLEAN` (top) — the locked episode title, John 13:10 verbatim
  contiguous, no punctuation, 5 words. **Subtitle:** `JOHN 13`. **seq_title for all
  interior pages = `THE BASIN AND THE DOOR`** (5 words, authored — names the episode's own
  zone geometry; alternative `NOT ALL CLEAN` (3, near-verbatim) if the longer phrase
  crowds a running header — §8, user's call).
- **Refs:** judas + judas_face + supper_room.
- **extra_avoid append:** "a stain, mark, or shadow on Judas's face or robe beyond the
  ordinary; a crowd of more than a few soft background figures; any blue or gold ink
  anywhere; modern clothing; any other figure looking directly at Judas."
- **Animation:** Judas keeps walking away from the viewer at a steady, unhurried pace,
  one continuous motion the whole clip, his robe swaying naturally; the warm light in the
  room behind him stays exactly as warm and steady as it already is, unchanged for the
  whole clip; the darkness ahead of him stays exactly as dark as it already is; no new
  figure, mark, or text appears; nothing brightens or dims. `clip_duration=5` (4.9s slot,
  ~2% frozen — freeze a settled final frame, not boomerang: a reversed walk would send him
  back INTO the light before the story does).

### BACK COVER

- **Scene:** the basin and towel (BASIN_TOWEL_BUILD, match the attached reference) alone
  on the floor beside the low table, no figure anywhere in the frame, the room around it
  empty and still, warm lamplight low and steady; a loose, open band of blue-and-muted-gold
  ink threads drifts across the upper part of the frame, well above the basin, tied to no
  object, touching nothing — the only page in the episode where the ink is not anchored to
  the basin's water itself, drifting free instead.
- **Why this image:** the landing addresses the viewer directly, past every character in
  the story — an empty room with the basin still there says "this is still happening,"
  without resolving Judas's own fate or putting words in Jesus's mouth after the fact. The
  free-floating band (not anchored to the water, for the only time in the episode) marks
  the shift from "a scene you watched" to "an invitation you're being given."
- **Lighting (law):** warm steady lamplight throughout, low and even, no doorway, no
  darkness in frame at all — the opposite lighting logic of the front cover, on purpose.
- **Title:** `BRING HIM YOUR WORST` (bottom) — the narration's own closing clause, verbatim
  contiguous, 4 words. **Subtitle:** `JOHN 13:35` (alternative `1 JOHN 1:9`, the "if we
  confess our sins" verse the ending gestures toward without quoting — §8, user's call
  between the in-passage verse and the thematically-pointed one, same as ep13's own
  cover-verse convention).
- **Refs:** basin_towel only (no figures).
- **extra_avoid append:** "any human figure, a face, a hand, a door, darkness, a stain or
  mark of any kind, jewelry, bright neon, a drawn border or caption strip."
- **Animation:** the loose band of blue-and-gold threads drifts slowly within its own
  region high in the frame, never lowering toward the basin, never leaving the upper part
  of the frame; the warm lamplight stays exactly as warm and steady as it already is,
  unchanged for the whole clip; the basin and towel lie exactly as drawn, undisturbed; no
  new figure, mark, or text appears. `clip_duration=8` (9.4s slot, ~15% frozen — freeze a
  settled frame, never boomerang).

---

## 5. Page design conventions used below

- Every page: `panel_style="woodcut_hybrid"`, 9:16, `include_no_bubble_clause=True`,
  `fence_kind="none"` (no dead ink — §2), the page-global no-new-mark clause written at
  the end of every `main_scene_animation` by hand.
- **ZONE check first (this episode's literalism trap, §2):** on every page with Judas in
  frame, the eye-QC checks whether any blue ink appears anywhere in the same frame BEFORE
  checking anything else. Then Jesus's face on F02-F03 (calm, unchanged, no grief or
  distress — the fragility point, §3). Then the basin/towel's plainness (no ornament).
- **Standing steady-line override:** every page states *"drawn in the same steady,
  confident, single-struck line, no doubled or tremored contour"* on every figure,
  including Judas — a man about to betray is exactly what a render loosens into
  fray-hatching, and here that would say "wavering," which the text explicitly denies
  ("the devil had ALREADY put... to betray him" — already decided, not in progress).
- **Lips closed on every figure on every clip** — narrator-only episode, no lip-sync ever.
- **Captions are ONE line on every page** (≤5 words), verbatim contiguous fragments of the
  locked narration; panel labels 1-3 authored words; corner notes short.
- **Still-model call per page:** `nano-banana-pro` wherever a page has three or more
  figures, a debut, a hero, or a first-of-its-kind composition; `seedream-4-5` only for a
  calm single-figure page with no other figure to leak a mark onto — F05 (Judas alone at
  the door) is the one clean candidate and is called out per-page below.
- Main-scene prose below is design intent at near-final density; the implementation pass
  keeps every MUST-SHOW, direction, dosage, zone-separation, never-X, and steady-line
  clause, and writes the final animation prompt against the RENDERED still's actual pixels
  (LAW 4).
- Model lanes per the north-star tiering, stated per page with its why. Under the OpenArt
  bridge there is no veo model — the tier is advisory and every clip renders on Kling 3
  Omni unless the user explicitly opts a clip back to Higgsfield.

---

## 6. Page-by-page

### F01 — "the devil had already put... to betray him. Jesus knew." (20w · Swirl **0** · veo3_1_lite advisory, clip 6 · nano-banana-pro)

The interior/contemplative beat: nothing visible has happened yet. Jesus's own face,
knowing, before the washing begins. Renders after F01... (self: renders first among
interior pages, `refs=[jesus]`.)

- **Panels**
  1. `"the heart"` — a closed hand resting on a knee, close, no face *(a small human
     detail, not Judas specifically — deliberately ambiguous whose hand)*.
  2. `"Judas"` — an empty place at the low table, a plain clay cup, no figure *(the name
     without the face yet — he has not been shown)*.
  3. `"Jesus knew"` — Jesus's own eyes, close, calm, direct *(jesus_ref)*.
- **Main scene** — `MEDIUM shot`:
  > the interior of the supper room (SUPPER_ROOM_BUILD), warm low lamplight; {JESUS_BUILD}
  > seated at the low table among a soft, general group of disciples (DISCIPLES_BUILD,
  > unindividuated, smaller and a little out of focus), his face turned slightly toward
  > the viewer, his gaze calm, steady, and direct, his expression unchanged — no sorrow,
  > no distress, no anger visible on his face, fully inside the frame; no other figure
  > singled out or named by the composition; the room warm and ordinary. Stage 0 dosage:
  > no blue Swirls of Life ink motif anywhere on this page — no blue or gold ink appears
  > anywhere in the scene, the panels, or the margins.
- **material_closer:** "nothing on this page carries any unusual ink; the room, the table,
  and every face are free of any mark."
- **Fence:** `none`
- **Caption:** `("Jesus knew",)` *(narration verbatim, 2 words)* · **Corner note:**
  `NOTE: already decided` *(authored, short — names that this is settled, not unfolding)*.
- **Panel motions:** (1) the hand rests still, a lamp's light flickering faintly on it;
  (2) the cup sits still, steam or nothing rising, tone-only; (3) a slow, single blink.
- **Main animation:** Jesus's gaze holds steady on the viewer/room, unmoving, his
  expression completely unchanged for the whole clip, his lips closed and still; the
  soft background figures hold, tone-only; the lamplight flickers gently and warmly
  throughout, unchanged in color or intensity; no new stain, spot, or darkening appears
  anywhere on the page at any point.
- **Why veo (advisory):** a held gaze, no completing gesture — the whole point is
  stillness. **Why NBP:** a debut composition (the room, the group) even though the focal
  figure is one face. **Refs:** jesus.

### F02 — "He knew as He poured the water... dried their feet with the towel." (17w · **Swirl 1 first trace** · kling3_0, clip 6 · nano-banana-pro — THE GOSPEL TURN)

The washing itself begins. Judas debuts here, seated among the others, but the frame's
subject is the basin and Jesus's hands — the first blue rises from the water, not from
any foot.

- **Panels**
  1. `"poured"` — water pouring from a plain vessel into the basin, close, no face.
  2. `"the water"` — the basin's still surface, close, no figure.
  3. `"the towel"` — a plain linen towel gathered at a waist, close, no face.
- **Main scene** — `MEDIUM WIDE shot`:
  > {JESUS_BUILD} kneeling beside the wide bronze basin (BASIN_TOWEL_BUILD), a plain linen
  > towel girded at his waist, his hands at the water's surface mid-motion, washing a
  > disciple's feet, his face calm and unhurried, his expression unchanged, no sorrow or
  > distress visible, fully inside the frame; nearby at the low table, {JUDAS_BUILD} seated
  > among the other disciples (DISCIPLES_BUILD), an ordinary man among ordinary men, his
  > own feet not yet the ones being washed, no mark or shadow distinguishing him from
  > anyone else at the table, seated at least an arm's length from the basin itself; the
  > room warm, lamplit, ordinary. Stage 1 dosage: exactly one restrained thread of blue ink
  > rising from the surface of the water in the basin itself — touching only the water and
  > the air just above it, never a foot, never a hand, never Jesus's own hands, never any
  > disciple's face, never anywhere near Judas — the only blue on the whole page, behaving
  > like one stroke of wet ink bled into the paper, smooth and open in its curl, never
  > blot-shaped, never a glow.
- **material_closer:** "the single blue thread rising from the basin's water is the only
  unusual ink at work on this page, and every hand, every foot, and the paper beneath
  every figure — including Judas — are free of any ink."
- **Fence:** `none`
- **Caption:** `("dried their feet",)` *(narration verbatim contiguous, 3 words)* ·
  **Corner note:** `NOTE: all of them` *(authored, short)*.
- **Panel motions:** (1) water pours in a steady stream, tone-only; (2) the water's
  surface settles, calm; (3) the towel's cloth shifts slightly.
- **Main animation:** Jesus's hands continue their washing motion at the basin, steady and
  unhurried, his face calm and unchanged, his lips closed and still; the seated disciples,
  including Judas, hold quietly at the table, tone-only, no one moving toward or away from
  the basin; the single thin blue ink thread at the basin's water stays exactly as drawn,
  in place, for the whole clip; no new stain, spot, or darkening appears anywhere on the
  page at any point, and no blue ink drifts, grows, or moves toward Judas or any figure at
  any point in the clip.
- **Why kling (a completing gesture — the washing motion itself must read as continuing
  cleanly, not inventing a new action):** **Why NBP:** Judas's debut, plus the group, plus
  the zone-separation geometry — too much riding on this page for the cheaper model.
  **Fragility note:** if the render puts any hint of blue near Judas or near any foot
  other than the one being washed, regen the still — never adapt the animation clause.
  **Refs:** jesus + supper_room.

### F03 — "'ye are clean, but not all.' ... 'lifted up his heel against me.'" (33w · Swirl **1 held** · veo3_1_lite advisory, clip 12 · nano-banana-pro)

The reveal, spoken to the room. The frame widens; the basin's thread holds small and
distant; Judas is now clearly visible among the group, still with no ink anywhere near
him.

- **Panels**
  1. `"clean"` — a single washed foot, dry, resting on the floor mat, close, no face.
  2. `"not all"` — the room's faces in a soft row, unindividuated, no one singled out.
  3. `"the old word"` — an open scroll or a hand gesturing as if quoting, close, no face
     *(the Scripture citation, drawn as an act of speech, not a literal scroll if that
     reads as anachronistic — implementation's call, §8)*.
- **Main scene** — `WIDE shot`:
  > the interior of the supper room (SUPPER_ROOM_BUILD), the low table and the seated
  > company of disciples (DISCIPLES_BUILD) now fully in frame; {JESUS_BUILD} standing or
  > kneeling near the basin (BASIN_TOWEL_BUILD), speaking, his hand open in a plain
  > gesture toward the room, his face calm and direct; among the seated disciples,
  > {JUDAS_BUILD} at his own place at the table, an arm's length or more from the basin,
  > his face as calm and ordinary as every other face in the room, no mark, no shadow, no
  > isolation in the seating; the basin's water small and a little apart in the
  > composition, near Jesus, not near Judas. Stage 1 dosage, held flat: the same single
  > restrained thread of blue ink from F02, now small in the wider frame, rising from the
  > basin's water only, touching nothing else, especially not any figure near it or
  > across the room, including Judas — the only blue on the whole page.
- **material_closer:** "the same single thread at the basin, now small in this wider room,
  is the only unusual ink on the page; every face at the table, including Judas's, and the
  paper beneath every figure are free of any mark."
- **Fence:** `none`
- **Caption:** `("ye are clean but not all",)` *(narration verbatim contiguous, quote
  marks dropped, 6 words — episode title line; §8 if this crowds, fall back to
  `"not all"`, 2 words)* · **Corner note:** `NOTE: he knew` *(authored, short)*.
- **Panel motions:** (1) the dried foot rests still; (2) the row of faces holds, a slow
  blink or two, tone-only; (3) the gesturing hand completes its motion and settles.
- **Main animation:** Jesus continues speaking, his gesture completing and settling, his
  face calm throughout, his lips closed and still (narrator-voiced, per the series' own
  no-lip-sync rule); the seated company, including Judas, holds attentively, no one
  reacting visibly, tone-only; the small blue thread at the basin stays exactly as drawn,
  in place, for the whole clip; no new stain, spot, or darkening appears anywhere on the
  page at any point, and no blue ink drifts toward Judas or any other figure at any point.
- **Why veo (advisory):** a held speaking pose, no completing gesture beyond the hand's
  own settle. **Why NBP:** the widest, most crowded composition in the episode (full
  table, full company, Judas clearly placed). **Refs:** jesus + supper_room + basin_towel
  + judas + judas_face + disciples.

### F04 — "He handed Judas the sop... 'do quickly.' Some... thought he had gone to buy food." (25w · Swirl **0** · kling3_0, clip 9 · nano-banana-pro)

Judas's own zone begins. The basin is gone from frame (backgrounded, unlit, or entirely
out of shot); no blue ink anywhere.

- **Panels**
  1. `"the sop"` — a piece of bread held between two fingers, close, no face.
  2. `"do quickly"` — Jesus's mouth and jaw, close, calm, speaking, no other feature.
  3. `"buy food"` — a small leather coin-purse at a belt, close, no face *(Judas's one
     distinguishing detail, isolated in a panel — a visual echo of the "buy those things"
     misunderstanding)*.
- **Main scene** — `MEDIUM shot`:
  > the interior of the supper room (SUPPER_ROOM_BUILD), lamplight now a little lower and
  > warmer, the low table nearby; {JESUS_BUILD} handing a small piece of dipped bread to
  > {JUDAS_BUILD}, both men's faces calm — Jesus's unchanged, direct; Judas's ordinary, no
  > mark, no shadow, no expression of guilt or fear, exactly as calm as any other disciple
  > at the table would look; the basin and its water NOT visible anywhere in this frame,
  > entirely absent from the composition; a few of the other disciples nearby, unremarkable,
  > glancing without alarm. Stage 0 dosage: no blue Swirls of Life ink motif anywhere on
  > this page — no blue or gold ink appears anywhere in the scene, the panels, or the
  > margins, even though the basin exists elsewhere in this room's world.
- **material_closer:** "nothing on this page carries any unusual ink; the room, the bread,
  and every face, including Judas's, are free of any mark."
- **Fence:** `none`
- **Caption:** `("that thou doest do quickly",)` *(narration verbatim contiguous, quote
  marks dropped, 5 words)* · **Corner note:** `NOTE: no man knew` *(narration verbatim,
  short)*.
- **Panel motions:** (1) the bread passes from one hand to another, completing; (2) the
  mouth completes one spoken phrase and settles closed; (3) the purse hangs still, a
  little sway.
- **Main animation:** the bread finishes passing from Jesus's hand to Judas's, both men's
  faces calm and unchanged, lips closed and still; the nearby disciples hold, unremarkable,
  tone-only; no blue or gold ink appears anywhere in the clip at any point; no new stain,
  spot, or darkening appears anywhere on the page at any point.
- **Why kling (a completing gesture — the hand-off of the bread must complete cleanly):**
  **Why NBP:** three figures plus the coin-purse detail, and the absence-of-basin
  constraint is easiest to verify on the stronger model's first pass. **Refs:** judas +
  judas_face + supper_room.

### F05 — "Judas 'went immediately out: and it was night.'" (9w · Swirl **0** · veo3_1_lite advisory, clip 4 · seedream-4-5 — THE DARK PAGE)

The episode's single darkest page, and its smallest. Judas alone, at the doorway, no
warmth, no ink, no one else in frame.

- **Panels**
  1. `"immediately"` — a hand pushing a door further open, close, no face.
  2. `"out"` — a foot crossing a threshold stone, close, no face.
  3. `"night"` — near-total darkness with the faintest warm sliver of lamplight at one
     edge, no figure.
- **Main scene** — `MEDIUM WIDE shot`:
  > {JUDAS_BUILD} alone, walking through the plain doorway (DOORWAY_BUILD) away from the
  > viewer, his back mostly to the frame, the warm lamplight of the room behind him
  > spilling only a short way past the threshold and no further; ahead of him, near-total
  > darkness, no stars, no moon, no other light source of any kind; no other figure
  > anywhere in the frame; the ground at the threshold dry stone, plain, unmarked. Stage 0
  > dosage: no blue Swirls of Life ink motif anywhere on this page — no blue or gold ink
  > appears anywhere in the scene, the panels, or the margins; this is the darkest page in
  > the episode by design, and it stays entirely free of any ink or unusual light.
- **material_closer:** "nothing on this page carries any unusual ink or light; the
  darkness beyond the doorway is plain darkness, and the threshold stone is unmarked."
- **Fence:** `none`
- **Caption:** `("and it was night",)` *(narration verbatim contiguous, quote marks
  dropped, 4 words)* · **Corner note:** none *(the page's own silence is the note — §8 if
  the format requires one, fallback `NOTE: alone`)*.
- **Panel motions:** (1) the hand completes pushing the door, settles; (2) the foot
  completes crossing the threshold, settles; (3) the sliver of light holds steady, no
  flicker.
- **Main animation:** Judas continues walking away from the viewer into the darkness at a
  steady, unhurried pace, one continuous motion the whole clip; the warm light behind him
  stays exactly as warm and contained as it already is, spilling no further past the
  threshold than it already does; the darkness ahead of him stays exactly as dark as it
  already is, with no new light, star, or glow appearing anywhere; no new stain, spot, or
  darkening appears anywhere on the page at any point (this page has no motif to protect,
  but the clause is written for consistency).
- **Why veo (advisory):** a continuing walk into darkness, no completing gesture. **Why
  seedream-4-5 (the one calm-single-figure candidate in the episode):** exactly one figure,
  no other figure to leak a mark onto, no crowd, no complex geometry, all refs already
  chained and approved by this point — the validated seedream case. **Refs:** judas +
  judas_face + doorway.

### F06 — HERO — "Jesus did not wash those feet because Judas earned it... already knows the worst." (31w · **Swirl 2** · kling3_0, clip 11 · nano-banana-pro)

The thesis, stated as an image: the basin, remembered, still and warm, Judas already
gone. This is the piece's rhetorical peak and the point the motif returns after its total
absence on F04-F05.

- **Panels**
  1. `"did not earn"` — an open, empty hand, palm up, close, no face.
  2. `"knowing"` — Jesus's own eyes again, close, calm, unchanged *(a deliberate echo of
     F01's panel 3)*.
  3. `"anyway"` — the basin's water, still, close, no figure.
- **Main scene** — `MEDIUM WIDE shot`:
  > the interior of the supper room (SUPPER_ROOM_BUILD), quieter now, the table a little
  > disturbed where one place has been left; {JESUS_BUILD} kneeling still beside the
  > basin (BASIN_TOWEL_BUILD), the towel still girded at his waist, his hands resting
  > lightly at the basin's rim, his face calm, steady, unchanged — the same expression as
  > every prior page, no grief, no anger, no triumph; the room around him warm and
  > ordinary, no other figure emphasized (§8: whether to include the remaining disciples
  > softly in frame or leave Jesus alone with the basin — I recommend alone, for the
  > thesis's own weight). Stage 2 dosage: the blue ink motif returns, now quietly present —
  > a few soft blue threads and one small amorphous watercolor bloom, entirely amorphous,
  > soft feathered edges, hanging in the air just above the basin's water, present but not
  > spectacular, echoing F02's single thread without repeating it exactly; touching only
  > the water and the air, never Jesus's hands, never anywhere else on the page.
- **material_closer:** "the soft threads and the one small bloom above the basin's water
  are the only unusual ink on the page, and Jesus's hands, the towel, and the paper
  beneath everything else are free of any ink."
- **Fence:** `none`
- **Caption:** `("knowing he wouldn't",)` *(authored, near-paraphrase kept short — §8: the
  exact locked line is long; consider `"knew the worst"`, narration-adjacent, 3 words, as
  the safer verbatim-leaning alternative)* · **Corner note:** `NOTE: that is love`
  *(authored, short)*.
- **Panel motions:** (1) the open hand holds still, unclenching further if anything; (2)
  a slow, steady blink; (3) the water's surface settles, calm.
- **Main animation:** Jesus's hands rest lightly at the basin's rim, unmoving, his face
  calm and completely unchanged for the whole clip, his lips closed and still; the soft
  blue threads and the small bloom above the water drift very gently within their own
  small area, never leaving it, never lowering toward Jesus's hands; the room holds quiet
  and warm around him; no new stain, spot, or darkening appears anywhere on the page at
  any point.
- **Why kling (the hero deserves the more deliberate lane, matching ep13's own hero
  treatment):** **Why NBP:** the hero page, and the motif's return after its absence needs
  the stronger model's control. **Refs:** jesus + basin_towel.

---

## 7. Assembly suggestions (word-proportional, Fable-style estimates)

167 words over 74.55s ≈ 2.24 words/sec (one narrator turn, natural speed, no quote
pauses). **Boomerang nowhere in this episode:** every unit walks, washes, speaks, or
drifts a band — all of which read backwards under reversal, and the worst case here is
F05 (a reversed walk would send Judas back INTO the light before the story does). **Every
clip is designed with real headroom under its word-proportional estimate** — compute the
real slots from `narration.alignment.json` (forced-align the locked audio first) before
setting any final `clip_duration`.

| Unit | Words | ≈Slot | Clip | Lane (advisory) | Frozen | Suggested mode |
|---|---|---|---|---|---|---|
| front | 11 | 4.9s | 5s | veo | ~2% | freeze (a walk — never boomerang) |
| f01 | 20 | 8.9s | 6s | veo | 0% (full clip) | freeze (a held gaze) |
| f02 | 17 | 7.6s | 6s | kling | ~21% | freeze + tail_loop (hands settle) |
| f03 | 33 | 14.7s | 12s | veo | ~18% | freeze (a held speaking pose) |
| f04 | 25 | 11.2s | 9s | kling | ~20% | freeze + tail_loop (hand-off settles) |
| f05 | 9 | 4.0s | 4s | veo | 0% (full clip) | freeze (a walk — never boomerang) |
| f06 | 31 | 13.8s | 11s | kling | ~20% | freeze + tail_loop (hands settle) |
| back | 21 | 9.4s | 8s | veo | ~15% | freeze (drifting band — never boomerang) |

Sum 167 = the narration's own count; 74.55s locked audio + landing hold ≥3.0s (INV-26).
Lane split: 3 kling (the completing-gesture pages F02, F04, F06) / 4 veo pages + 2 veo
covers. **The OpenArt bridge has no veo model — `model_tier` is advisory there and
everything renders via Kling 3 Omni unless the user explicitly sets
`SWIRLS_GEN_PROVIDER=hf` for a specific clip.** Still credits (estimate only): 6 pages ×
40cr (5 NBP pages) + 1 page × 15cr (F05 seedream) + 2 covers × 40cr = 335cr; the ledger
(`/cost`, `/spend`) is the only truth.

**Render/spend order** (refs gate everything — §3): F01 → crop supper_room → F02 → crop
basin_towel, judas, judas_face → F03 → crop disciples → F04 (+ doorway if visible) → F05
→ F06 → front cover → back cover. Animate nothing until every still has passed eye-QC
(zone check first — no ink near Judas — then Jesus's unchanged expression, then the
basin/towel's plainness, then baked text, likeness, layout, dose) and the LAW 4 referent
check against the rendered pixels.

**Score note for the next stage (not designed here):** this narration's own register is
quiet throughout — no dramatic peaks, a steady reflective-to-serious delivery with one
brief emphasized beat (F06's thesis) — closer to ep8/ep10/ep11's sparse felt-piano
direction than the bank's driving-groove default. Design it from the real alignment
timestamps, early, per the standing rule; the felt-piano direction should be checked
first, same recommendation as ep13's own brief.

---

## 8. OPEN QUESTIONS (do not silently resolve)

1. **The basin-as-anchor departure from precedent (§2).** Every prior episode anchored its
   swirl to a person's hand or a threshold a person crossed; this episode anchors it to
   the water itself, to keep the motif off the man receiving the washing. This is a
   genuine first for the series. Recommended: proceed as designed — the zone-separation
   requirement leaves no better option — but flag it for the user's explicit sign-off
   before the first F02 render, since it departs from a locked pattern.
2. **Whether F06 shows Jesus's figure at all, or only the basin/towel with him implied.**
   I recommend showing him (the thesis is HIS motive; a page about his love with no trace
   of him risks reading as generic). Alternative: an even quieter page with only the
   basin, the towel, and the water — no figure at all, mirroring the back cover's
   figure-free treatment one page early. User's call.
3. **F03's caption length.** `"ye are clean but not all"` (6 words, the episode's own
   title line, verbatim) may be long for one baked line at this style's tested legibility
   ceiling (2-4 words recommended by SKILL.md, "never a sentence"). Recommended fallback:
   `"not all"` (2 words) with the fuller line reserved for the front cover's title instead.
   Mandatory 2×-zoom legibility check either way.
4. **F06's caption.** The locked narration line is long (31 words for the whole beat); no
   short fragment of it is as strong as F03's or F04's captions. I've proposed an authored
   near-paraphrase (`"knowing he wouldn't"`) rather than a verbatim fragment, which is a
   real departure from this episode's otherwise-all-verbatim caption convention (every
   other page's caption is a narration-verbatim fragment). Recommended alternative if the
   user wants strict verbatim: cut to the shortest true fragment, `"he wouldn't"` (2 words,
   contiguous, but loses clarity out of context) or skip a caption on this page entirely
   (the corner note carries the beat instead). User's call.
5. **The Scripture-quote panel on F03 (panel 3, `"the old word"`).** Drawing "an open
   scroll" risks a small anachronism (scrolls existed, but a hand-gesture-as-speech panel
   is safer and matches how the rest of the episode avoids literalizing quotation). I lean
   toward the gesture; either is defensible. User's call, or leave to the implementation
   pass's judgment.
6. **The doorway ref's origin (F04 background vs. a fresh F05 render).** If F04's
   composition doesn't naturally include a visible doorway, `doorway_ref.png` needs to be
   approved fresh on F05 itself rather than cropped forward from F04 — meaning F05 may need
   `refs=[judas, judas_face]` only on its first pass, with a second crop cycle after
   approval. Flagged so the implementation pass doesn't assume the crop exists before
   checking.
7. **Back cover subtitle — `JOHN 13:35` vs `1 JOHN 1:9`.** John 13:35 ("by this shall all
   men know that ye are my disciples") is in-passage but thematically about love displayed,
   not about being made clean; 1 John 1:9 ("if we confess our sins, he is faithful and just
   to forgive us... and to cleanse us") is the verse the landing's own "bring Him your
   worst" most directly echoes, but it's outside John's Gospel and outside this episode's
   own citation set. I lean toward 1 John 1:9 for thematic accuracy over in-book
   convenience; flagged since every other episode's cover subtitle stayed within its own
   passage. User's call.
8. **seq_title — `THE BASIN AND THE DOOR` vs `NOT ALL CLEAN`.** The longer phrase names the
   episode's own zone geometry (useful for anyone reading the running header cold); the
   shorter is closer to verbatim and matches the front-cover title's own words. Recommend
   the longer, authored phrase for clarity; either fits the baked-text length limits.
9. **F02's model lane (kling vs. veo).** I called it kling for the washing motion's own
   completing gesture, but a case exists for veo if the render reads more as a continuing
   hold than a discrete completing action once the still is in hand — a judgment call to
   make against the actual rendered pixels, per LAW 0/4, not on paper.
10. **Whether F03 needs the wider "several disciples visible" composition at all**, or
    whether a tighter frame (Jesus, the basin, and Judas alone, with the rest of the room
    only implied) would make the zone-separation geometry easier to verify by eye. I
    designed wide because the reveal is spoken "to the room" in the text; a tighter
    alternative is available if the wide version proves hard to keep clean of stray ink
    near background figures.

**RESOLVED 2026-09-09 (user: "lock it").** User approved the recommended option on all 10 —
proceeding as designed: basin-anchored motif (Q1), Jesus's figure shown on F06 (Q2), F03 caption
"not all" (Q3), F06 caption "knowing he wouldn't" (Q4), gesture-as-speech on F03 (Q5), fresh
doorway-ref approval on F05 if needed (Q6), 1 John 1:9 on the back cover (Q7), seq_title "THE
BASIN AND THE DOOR" (Q8), F02 model lane left as a render-time judgment call (Q9), F03 composition
wide (Q10). This design brief is now LOCKED — next step is implementing `episode.py` from it.
