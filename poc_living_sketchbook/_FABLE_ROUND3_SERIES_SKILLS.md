# Fable — round 3: series skills for living-sketchbook

**Date:** 2026-07-30 · **Reacting to:** `STORM_living_sketchbook.mp4` v5 (63.0s, 13 spreads,
8 paper-layer devices live) · **Source mine:** the FULL ArkAIology skill roster, this time the
ten skills rounds 1–2 never touched — red-team, retention-review, shorts-factory, sound-design,
thumbnail-forge, higgsfield-video-explainer, mixed-media-explainer, vox-3d, vox-blend, vox-flat —
plus a fresh-eyes pass over vox-motion and threads now that a finished film exists to react to.

**Read first:** `_FABLE_ENHANCEMENT_BRIEFS.md` (round 2, the format this follows),
`_SKILL_ADAPTATIONS_REVIEW.html` (round 1 scorecard), `_STORM_REVIEW.html` (the v5 section
especially), `.claude/skills/living-sketchbook/SKILL.md` §5b/§8a.

---

## The creative take

Rounds 1 and 2 answered two different questions. Round 1: *what should the page be allowed to
say?* (lettering voices, map moves, the thread, the ledger). Round 2: *what should the page be
allowed to do?* (eight physical behaviours of paper and wash). Both were answered from inside
the frame.

Watching the finished v5 straight through — with the sound up, at full resolution, knowing what
it cost — the remaining gaps are all *outside* the frame:

**1. Nothing guards the film.** The s09 signature is the most instructive defect this project
has produced: a cursive mark Kling hallucinated into the wave-spray corner, present since v4,
**missed by four review rounds**, caught only by a full-context eye-check on the fifth. Every
gate this project owns audits a *still* or a *script*. Nothing mechanically audits **time** —
the one dimension where the animator invents. The paper-layer devices won their safety argument
by being structurally unable to touch the generated layer; the mirror-image argument says the
generated layer needs a structural *detector*, because eyes demonstrably saturate after two
passes over the same footage.

**2. The page is seen being made and never heard being made.** Scribed Ink writes a verse
letter by letter; blue-line resolves a drawing in 0.9s; the stamp slams down; the wash creeps
— and all of it happens in acoustic vacuum, over a score bed. The show's whole premise is
*hand-made artefact*, and hands make noise: nib scratch, brush drag, the tap of a stamp. Every
one of those cues can be timed deterministically because **our own devices already know their
exact schedules** — no ASR, no guessing, the cue list falls out of the assembler for free.

**3. The series' thesis has no tooling.** "The whole Bible, through Jesus" is a locked
non-negotiable, and the thread-finding that serves it currently lives in Opus's memory at
Stage 0. ArkAIology solved the identical problem *deterministically* — an exhaustive
verbatim-phrase concordance over all 31k KJV verses that rediscovered every hand-placed thread
and surfaced two nobody had asked for. Storm shipped without its own OT echo (Psalm 107:29 —
"He maketh the storm a calm, so that the waves thereof are still" — is the classic anchor for
this exact pericope, and it is nowhere in the episode). That miss was findable by grep.

**4. The show meets its audience wearing someone else's clothes.** The thumbnail stage
(`pipeline/thumbnails.py`) is Georgia-Bold-caps over a gradient — a perfectly good *brand*
treatment that is, structurally, the caption-box lesson at packshot scale: typeset UI laid
over hand-made art. The first pixel a viewer ever sees of a living-sketchbook episode is the
one place the hand-made argument currently surrenders.

Seven proposals below, ranked by my own confidence. Three are process/tooling adaptations
(where the ArkAIology idea is a workflow, I ported the workflow, not a look); four are visual
or audio devices that had to pass the same test as round 2: *does this look — or sound — like
it was made by the same hand as everything else on the page?* Three candidates failed that
test or duplicated existing kit, and are named as skips at the end, same as round 2's split-flap.

---

## 1. Margin Sentinel — the blank paper is a tripwire · **CONFIDENCE: HIGH**

**Inspired by:** `/red-team` — not its five voices, but its two structural laws: *every finding
must be verified against primary evidence, never the artifact's own claims*, and *the designer
never grades their own work*. The Sentinel is those laws compiled into numpy: a reviewer that
is not me, cannot get tired, and looks only at pixels.

**The pitch.** In this style, every clip carries regions that are *contractually inert*: the
kraft border, the cream margins, the torn-edge surround — paper the animator was told to leave
alone ("the blank paper margin in every corner stays perfectly empty" is literally the wording
that fixed s09). The Sentinel makes that contract enforceable at $0: for every raw clip, build
a quiet-mask from frame 0 (pixels matching the paper palette, low ink density, outside the
drawing's ruled border), then scan every subsequent frame for *structured* difference inside
the mask — thresholded, morphologically opened so grain and compression noise vanish, kept only
if a connected component persists or grows across ≥0.5s. Any hit exports a cropped filmstrip of
the offending region at its first-appearance timestamp for a human eye-check. It is a detector
with no drawing hand at all: it can flag a hallucination, it cannot create one.

**The translation.** There is no visual component to translate — the adaptation is that the
adversarial-review discipline becomes *pre-attentive*. The eye-check stays (this is a lead
generator, not a verdict machine, exactly like retention-review's "hypotheses, not verdicts"),
but the eye now gets handed a crop instead of 63 seconds of footage to re-watch cold.

**Cost:** $0 deterministic (numpy/cv2 over frames ffmpeg already extracts). Runs on RAW clips
before any paper-device compositing — ordering matters, since tide-mark and wash-creep *legally*
alter the paper and would false-positive; the living-sketchbook camera lock (§4: "the camera
does not move") is what makes frame-0 registration valid.

**The Storm moment.** s09_rebuke, v4: the signature grew out of the wave-foam into the corner
from ~1s in. The corner margin is exactly quiet-mask territory. Four human rounds missed it;
a persistence-filtered component appearing at t≈1.0s in a region that was blank paper at t=0
is about the easiest positive this detector could be handed. (Honest limit: a hallucination
fully inside busy drawing motion — a fourth face in the wave chop — stays the eye's job. The
Sentinel shrinks the unaudited area; it doesn't eliminate it. Kling signature-hallucination is
a known class — artists sign the corners of its training data — so the corners it watches are
precisely the corners at risk.)

**Structurally safe because:** it generates nothing, composites nothing, and fails toward a
human eye-check with evidence attached — the same fail-closed posture as `still_water_mirror`'s
figure guardrail, which proved its worth in v5 by firing nine times and being *investigated*
rather than trusted.

---

## 2. Scriptorium Foley — the page is heard being made · **CONFIDENCE: HIGH**

**Inspired by:** `/sound-design` — structural ideas, plural: (a) *cues map to CONTENT beats,
never just mood* ("state the motif once per day, five statements, each fuller"); (b) a series
needs a recognizable sonic identity, not per-episode ad-hoc scoring; (c) the level-matched
A/B/C/D method from the skills-day POC (same picture, isolate WHICH change did it) — reviewed
that day, never adopted into the 11. My judgment on why it went unclaimed: its *devices* (motif
theme, reader voice) were already owned here — §7's cold-to-warm arc and the repo's standing
Scripture-voice rule cover them. What was genuinely unclaimed is the *content-mapped-cue* idea
pointed at a target ArkAIology doesn't have: **a page that physically does things on schedule.**

**The pitch.** Every lettering and paper device in this show already knows, to the frame, when
it acts: Scribed Ink knows each glyph's reveal time (it reads the word alignment), Ink Stamp
knows its 0.18s pop, blue-line knows its 0.9s front, paperRip knows its tear, wash-creep knows
its advance window. Scriptorium Foley has each device emit its schedule into one cue-list JSON
at assembly time, then lays matched, quiet, *diegetic* sounds from the existing `sound_library`
under those exact windows: nib scratch under handwriting, a single wet brush-drag under an ink
arrival, paper tear under the rip (if not already), a felt press-tap under the stamp, a faint
water-wash under wash-creep. Levels stay ambience-class (−14dB or lower, sidechain-ducked, per
the repo's own audio-layer-stack constants). The result is the difference between watching a
sketchbook and *sitting at the desk it's being drawn in.*

**The translation.** ArkAIology's sound identity is a composed musical motif — a broadcast
convention. Ours must be the sound of the *medium*: no whooshes, no risers, no UI ticks, only
sounds a scribe's desk could produce. The series "ident" this creates is not a chime — it's
blue-line's cold-open ink arrival always carrying the same single brush-stroke sound, episode
after episode. A sonic logo that is literally a pen.

**One honest conflict to flag (do not resolve it silently):** §7 mandates near-silence + one
low tone under quoted Scripture, and Scribed Ink's flagship use IS the KJV verse. A nib scratch
under the verse is diegetic and arguably *is* the reverence — the Word being written — but it
is still a change to a locked sound rule, so it ships only at a whisper level under the low
tone, A/B'd level-matched (the skills-day method, reused verbatim as process), and the user
decides by ear. If it loses, the Foley still covers every non-KJV device untouched by §7.

**Cost:** $0 — cue timing is deterministic, sounds come from the existing library; any missing
one-shot (a good nib scratch) is a one-time ElevenLabs SFX generation on quota, then banked.

**The Storm moment.** s08 (23.75s): Matthew 8:26 writes itself in silence today — the scratch
would put a hand on the pen. s11: the "EXACTLY." stamp gets its press-tap. The cold open gets
the series' first-ever ident stroke. And held-breath already multiplies every device by the
narration's silence envelope — the Foley inherits that for free, so the desk goes quiet exactly
where the narrator does.

**Structurally safe because:** audio cannot add a disciple, a limb, or a doctrine; every cue is
bound to a device window that already passed its own gates; and it's additive under the locked
mix constants, never a re-mix.

---

## 3. Concordance Loom — the thesis gets tooling · **CONFIDENCE: HIGH**

**Inspired by:** `/threads` — but where round 1 adopted the *visual* thread (gold thread, two
verses, chosen and shipped), this adopts the half round 1 left on the table: the
**thread-director pipeline**. ArkAIology's `plan_threads.py` runs an exhaustive cross-book
verbatim-phrase concordance over all 31k KJV verses, then routes candidates through judgment →
validate → fail-closed verify. Proven the day it was built: it rediscovered all three
hand-placed thread beats and surfaced Gen 2:2→Heb 4:4 and Ex 20:11→Acts 4:24 *unprompted*.

**The pitch.** This series' first locked non-negotiable is "the whole Bible, through Jesus" —
and the mechanism serving it (Stage 0 discover_thread, the OT-echo scene requirement) runs on
model memory and model judgment alone. The Loom is the deterministic understudy: a local
full-KJV index (the repo already caches KJV; the full text is a solved download) that, given an
episode's locked passage, emits every cross-book verbatim-phrase match and every classic
echo-candidate above a length threshold, as a *candidate sheet* for Stage 0 and for the Thread
Device — each candidate carrying its refs and verbatim quotes, pre-verified by string equality
rather than model confidence. Judgment stays exactly where it is (the four-part thread
qualification test, the panel, the user); the *finding* stops depending on what Opus happened
to remember that day.

**The translation.** Process-only — no visual to reskin, which per the brief's own rules means
the WORKFLOW is what ports: scaffold (exhaustive, deterministic, cheap) → judgment (in-session,
against the real narration) → validate (fail-closed against the existing verify chain). It
slots upstream of the already-adopted Thread Device v2 the same way ArkAIology's director slots
upstream of ThreadCard.

**Cost:** $0 — pure text scan, stdlib Python, no model calls for the scaffold pass.

**The Storm moment — the one that stings.** Storm shipped with no OT echo at all. Psalm 107:
23–30 is the Old Testament's storm-stilling passage — *"He maketh the storm a calm, so that
the waves thereof are still"* (107:29), sailors at their wits' end crying to the LORD — and the
Gospel scene is its enactment in a boat. A phrase-level scan on "storm"/"calm"/"waves" surfaces
Psalm 107 instantly. Whether it becomes a gold-thread beat or an OT-echo spread is a judgment
call the qualification test exists for (the verbatim overlap is modest — this is an echo, not a
shared-phrase thread, and the candidate sheet must say so honestly); that the episode never got
to *make* that call is the gap. Future episodes: bronze serpent→John 3:14, manna→John 6 — the
whole series is made of exactly these seams.

**Structurally safe because:** it can only surface strings that exist verbatim in the KJV, with
refs attached; it proposes, never asserts; and everything it proposes still walks through the
locked doctrine gates (self AND panel) like any other claim.

---

## 4. Scribe's Tally — the count the Flap died for · **CONFIDENCE: HIGH**

**Inspired by:** `/vox-motion` — the countable-refrain components (PictogramGrid's units
popping in one by one with a live counter; CountUpNumeral's arrival at one big number). And by
this project's own confirmed SKIP: round 1's split-flap day-counter, which proved — twice —
that *the grid-of-cells shape is the anachronism, not the material*, and whose review ended
with an explicit unbuilt suggestion: "redesign from zero... with no frame at all."

**The pitch.** This is that redesign. When a narration counts — laps, dips, days, denials —
short hand-wobbled ink strokes accumulate in the page's open margin, one per counted beat,
timed to the alignment words, grouped in gates of five (four strokes and the fifth struck
diagonally through — a counting idiom older than Rome, and exactly what a scribe tracking a
count on paper would actually do). The final, completing stroke lands in rubric-red — or gold,
if and only if the completed count IS the glory beat. No frame, no cells, no card, no numeral
font: strokes on paper, drawn with the same seeded wobble as MarkerCircle and the map arc's
chevrons, in the same iron-gall ink as everything else the cartographer-hand draws.

**The translation.** PictogramGrid's structural idea is *watch the count happen, unit by unit,
so the number is earned rather than asserted*. Everything else about it — icon units, the ×k
chip, the grid — is the UI idiom, discarded whole. What survives is accumulation-on-the-beat,
re-expressed in the one mark-making vocabulary that is genuinely period, genuinely hand-made,
and already native to this show's margins.

**Discipline (load-bearing, from payoff-ledger's honesty rule):** the count must be verified
against the text before authoring — Jericho's 13 circuits (once daily six days, seven times the
seventh, Joshua 6) is derivable and was verified in round 1; Naaman's seven dips is stated
verbatim (2 Kings 5:14). A count the text doesn't state doesn't get a tally. And ≤1 tally
sequence per episode — it's a device, not a metronome.

**Cost:** $0 deterministic PIL, word-timed off the alignment like every lettering device.

**The moment.** Storm has no countable refrain — honestly, this device sits out this episode.
The worked moment is Jericho (the exact beat the Flap failed on): thirteen strokes accumulating
beside the siege-map arc across the episode, the thirteenth landing in red as the walls fall.
Future: Naaman's seven dips (the seventh in gold — the healing), Peter's three denials (three
strokes, then the cock-crow beat), forty days of rain arriving as eight gates of five.

**Structurally safe because:** deterministic overlay on the paper layer; can't touch the
generated drawing; the only "content" it carries is an integer, and the rule above makes that
integer Scripture-verified or absent.

---

## 5. Frontispiece — the packshot drawn by the same hand · **CONFIDENCE: MEDIUM-HIGH**

**Inspired by:** `/thumbnail-forge` — nearly all of it, structurally: compose over
already-paid-for hero art, never generate; ALL text deterministic, never AI; a mandatory
168px-downscale legibility gate that isn't satisfied by an exit code (you READ the tiny image);
hard safe-margin constants for the platform's own UI (YouTube's duration badge eats the
bottom-right ~220×80). Every one of those is aesthetic-free discipline and ports verbatim.

**The pitch.** What must NOT port is ThumbCard itself — Bangers, scrims, accent chips: the
exact UI-chip idiom this series rebuilt its lettering to escape. A living-sketchbook episode's
thumbnail should be its **frontispiece** — the engraved title plate of an old book: the
episode's own hero spread (Storm: s13's torn page, or s01's storm full-bleed), the title in the
show's own lettering voices (Ink Stamp for the hook line, Illuminated Rubric's gold capital if
the episode earns ceremony, Scribed Ink never — script dies at 168px, and the gate will prove
it), the torn-edge and gold-leaf strip doing the framing work a brand bar does elsewhere. Built
from the SAME raster renderers the episodes already use, so the packshot is provably the same
hand — the click and the content stop being two different shows.

**The translation.** Keep thumbnail-forge's entire *process spine* (candidates → 168px gate →
HITL pick, never a self-graded publish); replace 100% of its visual system with the lettering
grammar §5 already locked. One deliberate echo: thumbnail-forge's "art must be the episode's
single most dramatic frame, and if it doesn't have one, that's a gap to flag" — that rule is
better than what `pipeline/thumbnails.py` does today (default t=40% frame grab) and should port
as a picking discipline.

**The honest flag (why not full confidence):** `pipeline/thumbnails.py` is the *brand-wide*
Awakeden stage, and a catalogue has real value in looking uniform. Whether living-sketchbook
episodes get a style-family variant or conform to the house packshot is a **user decision about
the channel, not a device decision I can make** — this proposal is the variant, ready if wanted,
plus the two portable disciplines (168px gate, hero-frame rule) that improve the existing stage
either way.

**Cost:** $0 — PIL composition over existing art with existing renderers.

**Structurally safe because:** composes only approved art + deterministic type; nothing
generated, nothing invented; and it inherits thumbnail-forge's own honesty rule that the art
frame must be text-free before type goes on.

---

## 6. Light Table — the episode's pulse, on one sheet · **CONFIDENCE: MEDIUM-HIGH**

**Inspired by:** `/retention-review` — its structural idea has nothing to do with YouTube:
*map a per-second signal onto the shot timeline, attribute every anomaly to the exact shot on
screen, and hand a human ranked hypotheses — never verdicts, never auto-edits.* Also its
humility rules: proxies are labelled as proxies; a dip is "go look here," not proof.

**The pitch.** Pre-publish, we have no audience curve — but we have honest per-second signals
the finished cut already contains: mean-absolute-frame-difference (how much the page is
actually moving), the narration's word-density and silence gaps (already parsed by
held-breath), and the device schedule (every overlay/paper event, from the same cue list Foley
uses). The Light Table renders one diagnostic sheet per finished cut — the animator's light
table where you see the bones: the MAFD curve with spread boundaries ticked, silence bands
shaded, device beats pinned, and three deterministic flags: **dead page** (sustained
near-floor visual change while the narrator is mid-flow — the freeze-audit's blind spot,
since grain-boil keeps frames technically non-identical), **flat-line** (a spread whose
motion never varies — pacing monotony held-breath should have shaped but didn't reach), and
**pile-up** (3+ device beats inside ~2s — the overlay governor's temporal cousin). When real
YouTube Studio retention exists for published Awakeden pieces, the same sheet gains the real
curve as a second row and becomes the full retention-review port, spread-attributed — the CSV
mapper is a solved problem in ArkAIology's script and adapts to the spread list directly.

**The translation.** Process tool, no aesthetic surface — the sheet is for the editor, not the
viewer. The one idiom choice: it renders as a filmstrip-with-annotations, because that's how
this project already reviews clips (filmstrip QC), not as a dashboard.

**Cost:** $0 — ffmpeg frame deltas + the alignment JSON + the device cue list; stdlib plot.

**The Storm moment.** s05 (10.84–18.36s) is the longest, least-eventful hold in the piece —
round 2 flagged it by *watching* ("currently has the least to look at") and spent raking-light
on it. The Light Table finds that stretch numerically in every future episode before anyone
watches it tired, and would show at a glance whether the fix actually changed the pulse.

**Structurally safe because:** read-only over finished artifacts; produces a report a human
judges; touches no media, ever — retention-review's own "no auto-edits" covenant, kept.

---

## 7. The Unmade Page — finish as a register · **CONFIDENCE: MEDIUM (honest stretch)**

**Inspired by:** `/vox-blend` — the one structural idea in the three vox style pipelines that
survives translation: *one visual chassis, two named registers, and a deliberate, single
mid-episode register shift as a storytelling beat* (vox-blend lets a chapter switch
Diorama↔Collage on purpose, never by accident; vox-3d reserves ALERT WASH for one shot per
episode — a register spent like currency).

**The pitch.** Blue-line already builds, deterministically, a second version of any spread:
the underdrawing plate (non-photo-blue construction lines, washes knocked back). Today that
plate exists for 0.9 seconds, once, as a reveal. The Unmade Page promotes the pair to a
*register system*: the finished plate is the show's default voice; the underdrawing plate is a
second register — the page **less finished** — deployable as a held state, and, used in
reverse, as the one genuinely new dramatic move this unlocks: a spread that *un-finishes*,
wash and ink draining back to construction lines, the drawing being unmade. Lettering already
has exactly this duality (Scribed Ink the scribe, Typeset the compositor — round 1's "two
legitimate lettering voices"); this gives the drawing hand the same two voices.

**The translation.** Vox-blend's registers are two art styles from two prompt blocks — paid,
generated, and alien here. Ours are two *states of completion of the same drawing*, derived at
$0 from stills already QC'd, which is both the aesthetic translation (unfinishedness is native
to a sketchbook the way a style-swap never could be) and the safety argument.

**Governor (why the confidence is only medium):** this is one wrong use away from gimmick.
Hard caps: at most ONE register event per episode beyond blue-line's cold open; never on the
landing spread (the landing is the torn page's register, always finished); never under the KJV
verse. And it must survive a real A/B against the same beat played straight — if the un-making
reads as an effect rather than a feeling, it dies the split-flap's death and I'll say so.

**Cost:** $0 — blue-line's existing plate extraction + a reversed, slower front.

**The Storm moment.** s12, 43.16s: *"when the water reaches your own knees, you don't trust
the Christ in the boat either."* The episode turns its question on the viewer — and the page,
which has been finished art for forty seconds, quietly starts coming apart toward pencil under
them: your composure was the drawing; the storm is the underdrawing. Tide-mark already snaps
to full height on that exact word — the two devices firing together is either the strongest
non-landing beat in the piece or one device too many, and the A/B exists to find out.

**Structurally safe because:** both plates derive deterministically from one approved still —
no generation, no new content; the register can only reveal construction marks that were, in
the fiction of the medium, always under the ink.

---

## Considered, and deliberately skipped

- **shorts-factory.** Its one rule — a short is a fresh mini-episode from ONE nugget, never a
  crop — is already this repo's law twice over (`feedback-shorts-first-class`,
  `shorts-longform-funnel`), and living-sketchbook episodes ARE native 9:16 mini-episodes.
  Porting it would be re-labeling standing doctrine, which is how a skill roster gets fat.
  The one transplantable organ — the written *rejection log* for nugget selection ("2 rejected
  alternatives minimum, each naming the rule it failed") — is a sentence of process hygiene the
  runbook can absorb without a skill attached.
- **higgsfield-video-explainer + mixed-media-explainer.** The generic pipeline scaffolding
  (audio-barrier-then-clips, one style key everywhere, two-identical-failures-means-change-
  approach) is either already in the runbook/§4 or was mined in round 0 (multi-stage hard cuts
  came from mixed-media). Their remaining content is CLI mechanics for another repo's stack.
  Nothing left to translate — skipping is the honest verdict, not an oversight.
- **The Plate Loupe** (vox-motion's ZoomInset reinvented as an engraver's "detail enlarged"
  inset — a pinned scrap showing a magnified crop of the same still, leader-lined). I sketched
  it and killed it: §6's hunt_and_lock camera already owns "look closer" natively, in motion,
  with no second frame-within-frame — and a bordered inset window over art is picture-in-
  picture, a broadcast structure. Texture wouldn't have saved the flap; it won't save this.
  Same lesson, applied to my own idea before it cost anyone a review round.
- **The motif score + reader voice** (sound-design's two headline devices, reviewed on
  skills-day and never adopted into the 11). My read after forming my own judgment: correctly
  left unclaimed as *devices* — §7's cold-to-warm arc + near-silence-under-Scripture and the
  repo's standing Scripture-voice rule already occupy both sockets. What was genuinely
  unclaimed was the content-mapped-cue discipline and the level-matched A/B method, and both
  are alive inside proposal 2 rather than standing as a redundant skill.

---

## If I could only build three

**1. Margin Sentinel.** The s09 signature survived four review rounds *this week* — the defect
class is proven, current, and lives exactly where no existing gate looks. Every other proposal
makes episodes better; this one makes the thing that already almost shipped wrong detectable
at $0, forever, with the eye-check kept where it belongs.

**2. Scriptorium Foley.** The single biggest felt-quality gap between v5 and the show this is
trying to be. The cue timing is already computed by our own devices — the marginal cost is
wiring and taste — and it gives the series its sonic signature as a side effect: the same pen,
heard on every cold open, forever. (Its one rule-conflict, the scratch under the KJV, goes to
the user by A/B, not resolved silently.)

**3. Concordance Loom.** Infrastructure, like held-breath was: build once, every episode's
Stage 0 gets deterministic candidate threads forever, in direct service of the series' first
non-negotiable. Storm missing Psalm 107:29 is the concrete, slightly embarrassing proof it's
needed — the seam the whole series is about, findable by string search, unfound.

Runner-up: **Scribe's Tally** — the cheapest to build (it's MarkerCircle's wobble math drawing
shorter lines) and the redemption of round 1's only confirmed skip, but it waits for an
episode that counts, and Storm doesn't.

All seven are $0. Four never touch the generated layer at all (Sentinel, Foley, Loom, Light
Table are read-only or audio-only); Tally and Frontispiece are deterministic paper-layer
overlays under the same governors as round 2; the Unmade Page derives both of its plates from
already-approved stills. Nothing here can grow a fourth disciple — and proposal 1 exists
specifically to catch the layer that can.
