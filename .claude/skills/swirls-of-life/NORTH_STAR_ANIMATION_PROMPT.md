# Swirls of Life — North-Star Animation Prompt (v2, consolidated 2026-08-20)

Paired with `NORTH_STAR_PROMPT.md`. This v2 replaces the same-day v1 wholesale:
v1 accumulated a day of corrections (INK_LIFE / FROZEN_v2 tone-breathing-only)
that the same day's real renders then superseded — the validated style turned
out to be the user's own hand-written Kling prompt (short, positive, per-panel
bounded content motion), not the engineered tone-breathing approach. Everything
below is stated once, as the current rule, with the evidence that earned it.
Check **VALIDATED vs OPEN** at the bottom before trusting any rule in a new
situation.

---

## LAW 0 — the still and the animation are ONE design

A shot is designed once, as a pair. The Fable design pass (SKILL.md Step 0)
writes the STILL prompt and the ANIMATION prompt together, before any
rendering. Never still-first-animation-later. The reason is hard evidence, not
tidiness: **most animation failures are still defects.** Shot 7 of John 4
failed 5 times across 2 models and 2 days (3 regens to get a clean base
render, then 2 failed animation attempts under two opposite prompt
philosophies) — and every failure traces to the still's own composition, not
to any animation wording.

Division of labor:

- **The still owns the story.** Geometry (who faces where, what lies on whose
  path, where the destination is), substance separation (ink motif vs real
  water), prop placement and salience, and the composition's honest motion
  headroom. If the story needs a direction — "the life is leaving the well and
  heading for the town" — the still's STATIC geometry states it (e.g. a sky
  band of ink stretching from above the well toward the town). The clip never
  has to create meaning.
- **The clip owns continuation and life.** It may continue a motion the still
  already draws, along the vector the still already draws it, to an endpoint
  visible along that vector — and it may let bounded things cycle and breathe.
  It must never redirect, reverse, or turn a figure, never grow or move the
  ink motif's shape, never enact a story change the still doesn't already
  show in progress. Story change happens BETWEEN pages — exactly how the
  Swirls dose already works (Stage 0→1→2→3 across stills, never within a
  clip).

### The animation-fragility checklist (run at STILL design time)

These are reshape-the-still items, discovered the expensive way. If a
composition trips one, fix the composition — do not plan to fix it later in
the animation prompt (that was tried twice on shot 7; both attempts failed,
the second worse than the first).

1. **Drawn vector must match intended motion.** For every figure who will
   move: is she drawn facing her direction of travel, destination visible in
   frame ahead of her, nothing on the line between? Shot 7 drew the woman
   running TOWARD the camera with the well directly in her path and the town
   behind her — while the beat said "she runs from the well to the town."
   Irrecoverable: mild text → the model followed the drawing (she ran at the
   well, read as about to jump in); forceful text → the model obeyed the text
   by contorting the drawing (she turned around on-screen mid-clip).
2. **Figure moving away from / past a body of water = inherently risky.**
   Recognize it at design time. Either (a) reshape: lateral profile travel,
   water feature small and behind the figure, or (b) if the composition must
   keep water on the figure's line, cut the motion ask to near-zero (hold,
   gaze, garment stir) and let the next page carry the movement. Never combine
   "big locomotion ask" + "water feature on or near the motion line."
3. **Ink motif and real water never share a zone.** If the scene contains a
   well mouth, stream, rain, or jars of water, the dose lives in the SKY/air,
   anchored high, touching nothing on the ground — and the still says the
   ground is dry explicitly. Never draw the motif as ribbons lying along the
   ground: to the model, blue ribbons on the ground ARE a river, whatever the
   prompt calls them (LAW 3).
4. **Figure + vessel + water-source is a loaded invention prior.** veo drew a
   carried pot twice against explicit empty-hands language; Kling tipped the
   pot into the well. Keep the vessel off the figure's motion line, small, or
   panel-only.
5. **Match the ask to the composition's headroom.** Locomotion shots get
   locomotion; close-ups get gaze/blink/breath; a shot that would only ever
   read as a camera push gets no paid animation at all
   (`feedback-spend-only-for-cinematic-value`).
6. **Fragility budget.** A still that itself needed regens to render clean
   gets the SMALLEST animation ask, never a compensating bigger one.

The Step 0 output stays one reviewable table, one row per shot:
**still prompt | animation prompt (model per tiering) | Focal Tour gap-fill
plan | (long-form only) skip motion?** — reviewed by eye before any spend.

---

## LAW 1 — blocking: the clip continues the drawing

Video models obey the pixels first and the text second.

- **Every NAMED figure who moves gets exactly ONE sentence**: continue the
  drawn motion, with an anchor and a stated endpoint or direction that matches
  the drawing. Evidence: shot 8's first attempt failed because the named woman
  had no sentence of her own — she got swept into generic crowd motion and
  walked PAST Jesus. The fix — *"the woman walks forward and arrives at Jesus,
  stopping close beside him and turning to face him"* — worked on the next
  render (user-confirmed). Unnamed crowds may stay generic ("the crowd
  continues walking forward at an even pace").
- **A figure who should not move gets an explicit hold**, one short positive
  clause.
- **If the text contradicts the drawing, both outcomes are failures** — the
  model either ignores the text (shot 7 v3) or warps the drawing to comply
  (shot 7 v4, the turn-around, judged worse). There is no prompt-side fix for
  a blocking contradiction; only the still fixes it (LAW 0.1).

---

## LAW 2 — ink motif motion: anchored cycles and fixed-region drift only

The safe motions have **no destination and no growth axis**. All four forms
below are validated on real renders:

| Form | Validated phrasing |
|---|---|
| Closed orbit around a fixed anchor | "golden halo line swirls rotate around head" (the user's Cross prompt) |
| Drift within a named region that already exists at full size | "background watercolor wind swirls flow smoothly across the sky" (Cross); "drift smoothly ... within their own fixed band" (shot 8) |
| Small-area curl near an anchor | "the soft blue threads near him drift gently within their own small area" (shot 4) |
| In-place property change | tone deepens/pales, gold warms and settles — minimal but always safe |

Banned: any motion defined by a **route or a moving target** — "flows along
the path," "trails after her," "follows the spilled water," "moves from X
toward Y," lengthens / spreads / grows / widens. A trail is by definition a
growing object. **Caps and bans do not fix these** — "never widening into a
broad river" preceded a broad river; naming the catastrophe raises its
salience.

**Verb discipline alone is NOT sufficient.** Shot 7's second attempt used
zero banned verbs (fully in-place tone-breathing) and still failed — because
its real problems were substance (LAW 3) and referent (LAW 4), which carry
equal weight.

**The same rule governs DEAD INK (see `NORTH_STAR_PROMPT.md`'s Stain/Fray
system): dispelling a shadow motif is NEVER a within-clip animation
request.** A "fades/dissolves/shrinks" ask is the mirror of the banned
grow-family verbs — same escalation risk, opposite direction, and this
project's own evidence (the v4 pot pouring ink the moment the prompt drew
attention to it) says naming a loaded thing for removal is exactly how a
model decides to do something dramatic to it instead. The Stain/Fray get
ONE positive stillness clause each, same as any other load-bearing static
element ("the cold stain in the paper lies completely still, exactly as
drawn"), and the dose only drops between pages — a hard cut, exactly like
the Swirl's own 0→3 stages already only change page to page. This is also
truer to the text: Mark 5:29's healing is "straightway" (instant), not a
gradual on-screen dissolve — the cut IS the miracle, not a compromise for it.

---

## LAW 3 — substance separation is a STILL duty

Shot 7's still prompt asked for the dose "like wet ink following spilled
water" along the path — and the render duly drew water-like blue ribbons
winding across the ground next to a drawn stream. From that moment no
animation wording could save the shot: motion language widened the ribbons
into a dark river (v3); fully-static language got a new vertical water line
poured into the well instead (v4). The model treats ink thread and drawn
water as one substance and lets them bleed into each other.

Rule: the dose and any real water are **spatially separated zones in the
still itself** (sky vs ground is the standard split), and where the beat
allows, the still states the ground is dry in so many words. This is why the
checklist item LAW 0.3 exists — the animation prompt inherits a safe page or
an unsafe one; it cannot convert one into the other.

---

## LAW 4 — referent fidelity + negation salience

- **Write the animation prompt against the RENDERED still, and re-verify
  after still QC.** Every noun in the motion prompt must be pointable-to in
  the actual pixels, described as it actually rendered. Shot 7 v4 asserted
  "the thin blue-gold ink thread already trailing from the well" — no such
  single clean thread existed in the render (the dose had come out as ground
  ribbons), so the model MANUFACTURED one: a thick blue line hanging from the
  pot down into the well shaft. An asserted-but-absent referent is an
  invitation to invent.
- **Props: one short positive stillness clause, maximum.** "The waterpot sits
  still on the well's edge." Never a negation pile — "it never moves, tips,
  or falls" is a menu, not a fence (v4's panel pot poured ink after exactly
  that treatment, where v3's mildly-treated pot had stayed put).

---

## THE TEMPLATE (validated on Kling3.0 pro, 2026-08-20)

Directly adopted from the user's own hand-written Cross prompt (worked very
well on watch) and confirmed on shot 8 (user-confirmed after the named-blocking
fix). Short, almost entirely positive, real per-panel bounded content motion.

**Second exemplar, 2026-08-20: Hem F05 v2** (user: "this was a good animation
prompt... much better, lets lock this one in" — full text in the WORKED
EXAMPLE-adjacent VALIDATED entry above). What made it land: every motion was
small, specific, and tied to THIS beat's own emotion — Jesus's one kind nod,
the woman's breath and shoulder-release as fear visibly leaves her, the
crowd leaning in because they just witnessed it — not generic ambient
motion. When designing a new page's animation prompt, ask "what is the ONE
human thing each figure does at exactly this moment in the story" before
reaching for a generic hold/sway/settle.

```
Stationary camera, locked {WIDE|MEDIUM|CLOSE-UP} shot of the 2D storyboard
layout, frame borders and all baked text stay static, with no border, box, or
speech bubble ever appearing around any caption or note. Animate isolated
motion inside each panel: panel 1 {ONE bounded motion, or in-place tone/light
change}; panel 2 {...}; panel 3 {...}. Large bottom panel: {one sentence per
named figure — continue the drawn motion with anchor + endpoint/direction, or
an explicit hold}; {optional: one atmosphere motion inside a named fixed
region}; {ink clause from the stage table below}; {one positive stillness
clause per load-bearing static prop, max}.
```

Rules:

- **~70–130 words total.** The user's 70-word prompt outperformed every long
  engineered one. Short and positive beats long and defensive.
- **No speech bubbles around captions** — added 2026-08-20 after Kling drew
  an unrequested bubble around caption text twice (the Cross INK_LIFE test,
  then Hem F04 v2), both times on a caption that reads as the figure's own
  quoted line with NO_MOUTH already stated. Untested as a fix yet; watch for
  recurrence even with this clause present.
- **Exactly one motion per panel.** Panel CONTENT may genuinely move (Mary
  weeps, soldiers cast dice, clouds drift, crowd streams — all validated);
  borders, title, frame number, and baked text never do.
- **Caution inside panels:** a panel whose subject carries a loaded prior in
  the main scene (the pot), or a small sketched face, gets in-place tone/light
  motion only — v4's pot panel poured ink and its face panel morphed under
  content-motion asks on a shot that was already fighting.
- **NO_MOUTH** whenever a figure has a spoken line in the beat (voice-over
  series, no lip-sync, ever): *"His/Her lips stay closed and completely still
  — he/she is not speaking and his/her mouth does not move at all."*
- **Blink needs its full arc** or it reads as close-and-stay-closed:
  *"closes, then opens again fully, ending wide open, gaze steady on the
  viewer."*

### Ink clause by Swirls stage

| Stage | On the page | Clause |
|---|---|---|
| 0 — absent | none | "No blue or gold ink motif appears anywhere on this page, and none appears at any point in the clip." |
| 1 — first trace | one thread | Hold, stated positively: "the single thin blue ink thread stays exactly as drawn, in place, for the whole clip." (Motion on a lone thread is the worst risk/reward on the page — untested, don't.) |
| 2 — present | few threads + bloom near an anchor | "the soft blue threads near {anchor} drift gently within their own small area." |
| 3 — diffused | woven through scene | "the blue-and-gold ink threads drift smoothly within their own fixed band across {the sky / the air of the scene}." |
| Halo (always-on, separate from the dose) | — | "the golden halo line swirls rotate slowly around his head." |

veo variant: never "glint," "sparkle," or "catch the light" on the gold
(`feedback-veo-no-glitter-glow`) — positive-only "slowly warm and settle."
Kling may use "glint softly and settle."

---

## Model tiering — veo-first default (revised 2026-08-20)

**Default to veo3_1_lite; use Kling3.0 pro first only when the shot needs a
designed/cued gesture that must COMPLETE mid-clip.** veo is roughly half the
cost (4cr/~$0.60 vs Kling pro's 8.75cr/~$1.31, 5s/1080p sound-off) and the
Storm F06 bake-off validated it cleanly on a genuinely hard shot (dramatic
water, a real dose, multiple named figures, all holds) — user's own call on
watch: "veo had a better animation" (better depth/motion quality than Kling
on the same prompt, no real defect once judged on real playback rather than
a compressed contact sheet).

- **veo3_1_lite (default)** — atmospheric holds, multi-figure "hold still"
  crowd/group shots, subtle settle/expression softening, anything drawn
  already-in-progress that the clip just continues (LAW 0/1's whole
  philosophy — most shots under this framework ARE holds).
- **Kling3.0 pro (first choice only for this case)** — a motion that has to
  visibly COMPLETE on camera with a stated start-and-end arc: a blink, a
  turn, a designed gesture. Real evidence, same session: the Cross bake-off
  asked for one full blink (close → open) — Kling executed it cleanly, veo's
  eyes stayed open the whole clip, never attempting the close. Today's Storm
  shot deliberately had NO completing gesture (the raised hand holds, it
  never rises) — which is why veo won there without contradicting the blink
  finding; the two results are consistent, not in tension.
- **If a shot fights its assigned model (artifact or invention), switch
  models before rerolling the same one.** Kling had a real seam artifact on
  3 of 8 John 4 shots; veo invented a carried pot twice on shot 7. Each was
  fixed by the other model, not by more prompt surgery.
- **Judge model quality on real playback, not the contact sheet alone.**
  Today's veo storm clip initially read as a panel-hallucination defect from
  a compressed 4-frame JPEG; on full-resolution real playback it was a
  legitimate, good-looking render. Contact sheets remain mandatory (they
  catch escalation/blocking failures reliably) but a defect call from a
  contact sheet alone should be treated as provisional until confirmed on
  real playback.

---

## Shot 7, and shots like it — the standing decision

**The original shot 7 composition is RETIRED for animation.** ("She runs from
the well": toward-camera run, well + pot in the foreground on her path, dose
drawn as ribbons along the ground, a stream drawn into the background.) Full
record: 3 regens for a clean base render on the original build (Kling and veo
each inventing content), then 2 failed animation attempts on 2026-08-20 under
two opposite prompt philosophies — 5 failures, 2 models, 2 days, each failing
differently. A composition that fails under every prompt philosophy is itself
the defect.

**Standing rule: after TWO failed animation attempts on one still, stop
patching the animation prompt and redesign the still** under the LAW 0
checklist. The shipped John 4 film keeps its shipped clip (the regen that
passed); retirement means no further animation attempts on that still, and
any re-animation of the sequence uses the F07 v2 redesign below.

---

## No python "aliveness" layers (kept — user's standing rule)

Animation life comes from the Kling/veo prompt only. No line_boil /
raking_light / ink_bloom compositing to fake motion the clip lacks — built
once, user rejected it on watch. The lock_panels overlay stays removed (its
static-top-vs-animated-bottom seam side effect). **Focal Tour gap-fill is a
TIMING device, not an aliveness device, and is unaffected:** whatever slot
time is left after the real clip's natural length is covered by
`panel_animator/focal_tour.py` (`dramatic_spotlight`) touring 2–4 of the
still's own named regions in narration order. Decided at design time, in the
Step 0 table. Long-form (or an occasional credit-saving short) may make Focal
Tour a shot's PRIMARY treatment; on a short, every shot gets a real AI clip
by default.

---

## QC — every clip, no exceptions

1. **Referent check BEFORE rendering:** re-read the rendered still next to
   the animation prompt; every noun must exist in the pixels as described
   (LAW 4). Rewrite referents to match the paper, not the design intent.
2. **4-frame contact sheet** — catches invented content, escalation, blocking
   drift (caught the v3 river and the v4 turn-around + blue line).
3. **Real playback, by eye** — the contact sheet under-reports motion-domain
   failures (the v3 "about to jump into the well" read, the Kling seam
   artifact were both playback-only catches). Both checks, always.

---

## WORKED EXAMPLE — F07 v2, still + animation designed together

The canonical demonstration of LAW 0: the retired shot 7 beat ("she leaves
her waterpot and runs to tell the town," John 4:28-29), redesigned so the
animation ask is safe by construction. Every design choice traces to a
diagnosed failure: lateral profile run matching the text's direction (LAW
0.1/LAW 1); well + pot small, behind her, off her line (LAW 0.2/0.4); ground
explicitly dry, no stream (LAW 0.3/LAW 3); dose moved to a sky band whose
static geometry — stretching from above the well toward the town — tells the
story direction so the clip doesn't have to (LAW 0); pot given one positive
stillness clause (LAW 4).

### Still prompt (from NORTH_STAR_PROMPT.md's template; refs: woman only)

```
One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE WELL". Top-right frame number, handwrite: "F07". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "pot left behind") a small sketch of the round clay waterpot sitting abandoned on the stone rim of the well, panel 2 (handwrite: "urgent joy") a study of the woman's face mid-run, alight with urgent joy, panel 3 (handwrite: "town ahead") a small sketch of the town's flat rooftops and gate on the road ahead. Below them, ONE large full-scene illustration filling the lower half of the page — a WIDE PROFILE shot: the Samaritan woman in full figure, seen from the side in profile, running from the left of the frame toward the right in mid-stride, her garments and head covering streaming out behind her; the dry dirt path she runs on leads from the old stone well — small and fully inside the frame at the lower left, behind her, the abandoned clay waterpot fully visible sitting alone on its stone rim — rising gently across open country to the distant town, its flat rooftops and gate small and fully inside the frame on the higher right horizon ahead of her; long afternoon light; the ground, the path, and all the country below the horizon are dry ochre earth and grass, with no stream, no water, and no blue anywhere on the ground. The Samaritan woman (match the attached reference): an ordinary first-century working woman with a strong distinctive face and expressive eyes, dark hair partly under a practical head covering, layered garments in burnt umber wash with muted olive-green and clay-red accents, drawn in dense cross-hatching and short dry-brush strokes, her cross-hatching drawn visibly looser now, almost flying. Stage 3 beginning dosage: the blue ink motif begins to diffuse — one loose open band of blue ink threads with traces of muted gold drifting high in the sky, stretching from above the well at the left across the upper air toward the town at the right, tied to no single figure and touching nothing on the ground, no longer one single thread but not yet filling the scene, behaving like wet ink bled into the paper's sky wash. Small handwritten production notes integrated naturally on the page: a caption beneath the main scene, handwrite: "Come, see a man", and a corner note, handwrite: "NOTE: pot left behind". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash on aged cream paper with visible grain. Not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX — every blue or gold element behaves like literal wet ink bleeding into paper, never a magic-particle glow.
```

Render:

```
hf generate create nano_banana_pro --prompt "<still prompt>" --image F:\slk\PycharmProjects\JesusInTheBible\.claude\skills\swirls-of-life\references\john4_woman_ref.png --aspect_ratio 9:16 --resolution 2k --wait
```

### Animation prompt (from THE TEMPLATE; Kling3.0 pro per tiering — real locomotion)

```
Stationary camera, locked wide shot of the 2D storyboard layout, frame borders and all baked text stay static. Animate isolated motion inside each panel: panel 1 the warm afternoon light on the clay pot deepens very slightly, nothing else changes; panel 2 a few loose strands of the woman's hair stir in the wind of her run; panel 3 a thin banner of dust drifts across the road before the town gate. Large bottom panel: the woman keeps running from left to right along the dirt path toward the distant town gate, one continuous steady stride the whole clip, her robes and head covering streaming behind her; the blue-and-gold ink threads high in the sky drift smoothly within their own fixed band across the sky; the waterpot sits still on the well's edge.
```

Render (after the still passes QC AND the referent check — sky band present,
ground dry, woman in profile facing right, pot on rim at lower left):

```
hf generate create kling3_0 --prompt "<animation prompt>" --start-image <f07_v2_9x16.png> --aspect_ratio 9:16 --mode pro --duration 5 --sound off --wait
```

### Why the pair is safe by construction (the design-together proof)

- Her drawn vector IS the asked vector: profile, facing right, town visible
  ahead of her, nothing on her line — the clip only continues the drawing.
  No contradiction to disobey (v3's failure) or contort around (v4's).
- The story direction lives in the still's static sky-band geometry
  (well-side → town-side), so the animation needs zero travel language for
  the motif — its clause is the validated fixed-band drift, verbatim family.
- No drawn water anywhere on the ground: the substance-confusion channel
  (ribbon → river; thread → pour) is deleted at the source, not fenced with
  words.
- The pot is small, behind her, off her line, with one positive stillness
  clause and a tone-only panel — the invention prior gets nothing to grab.
- Gap-fill (Step 0 table entry): Focal Tour over [pot on well rim] → [her
  profile mid-stride] → [sky band toward town], narration order, for
  whatever slot time remains after the 5s clip.

### 9:16 note

Lateral well-left/town-right geography has less horizontal room in 9:16; the
gentle diagonal (well lower-left, town higher-right horizon) is deliberate —
it stacks travel into depth. The MUST-SHOW "fully inside the frame" language
guards the two anchors; check both at still QC before animating.

---

## VALIDATED vs OPEN

**VALIDATED (real renders, user-confirmed or eyeballed clean):**

- The short/positive/per-panel-bounded template on Kling3.0 pro (the user's
  Cross prompt, user-approved on watch; shot 8 after the named-blocking fix,
  user-confirmed).
- Named-figure blocking with anchor + endpoint (shot 8's fix).
- Fixed-region drift + anchored orbit for the ink motif (Cross halo + sky
  swirls; shot 8's band).
- Panel content motion under static borders/text (Cross panels; shot 8
  panels).
- NO_MOUTH; blink with full arc (2026-08-19 builds).
- Switch models when a shot fights one (shot 7 original build; Kling seam
  shots).
- The shot-7 diagnosis itself — still-level defect, per 5 distinct failures
  across 2 models.

**F07 v2 rendered and PASSED, 2026-08-20 (moved out of OPEN):** still +
animation both rendered clean on the first attempt — the first time this
story beat has worked in 6 tries across 2 models and 2 days. 4-frame contact
sheet confirms: continuous left-to-right run, no reversal, no turn-back
toward the well; waterpot completely static; sky band drifts within its own
region with no runaway growth; panel 1's "light deepens on the pot" tone-only
ask rendered correctly; no hallucinated content, no stray text. This is the
first real, positive proof that LAW 0 (design still + animation together,
run the fragility checklist before the still even renders) produces a
working result where reactive prompt-patching on an already-fixed still
failed twice. Real playback still worth a human eye before fully trusting
it — contact sheets don't catch every failure mode (see QC section) — but
this is the strongest evidence in the doc so far.

**Storm F06 rendered and PASSED on BOTH models, 2026-08-20 (moved out of
OPEN):** the hardest LAW 3 stress test yet — a dramatic storm sea as the
page's actual subject, sharing the page with a real Stage 2 dose — held on
Kling AND on veo3_1_lite. Zero blue in any wave on either render (the single
named hard regen criterion), ink motif stayed bounded near the raised hand
on both, no escalation, no blocking failures. User's verdict on real
playback: veo's motion quality read as better than Kling's here (a
contact-sheet-only read had flagged an apparent panel-3 hallucination on
veo; on full-resolution playback this was a legitimate render, not a
defect — see the model-tiering section's new playback-vs-contact-sheet
note). This is the evidence behind the veo-first default above.

**DEAD INK / "The Hem" — Stain motif rendered and PASSED both pages,
2026-08-20 (moved out of OPEN, with one real failure en route worth keeping
as the record):** F04's still passed full QC immediately (the stain
correctly crossed the drawn frame border into the margin — the system's
signature disambiguating trick — worked on the first still render). Its
FIRST animation attempt (veo3_1_lite, an all-holds prompt with the stain's
only defense a local positive-stillness clause) FAILED: the page's own
warm-brown aging/foxing — not the cold grey stain itself — grew into panel 3
and the sky, a defect the contact sheet caught cleanly. Root cause: the
prompt's only dynamic verb ("deepens," repeated three times with nothing
else given real motion) put the model's whole motion budget onto the one
darkening-capable material on a page whose own baked note reads "stain in
paper," and the stillness clause only fenced the DRAWN stain, not the
page's other stain-capable material (its own aging). Same session, the user
independently flagged the deeper issue: an all-holds prompt produced a
technically-clean-but-lifeless clip — "we should not forget the larger
story." **Both problems shared one fix**, applied together and validated on
retry (Kling3.0 pro, per the standing switch-models rule): (1) real
story-driven motion given to every element — her fingers closing around the
hem into an actual grasp (a validated completing-gesture, matching F04's
panel 2 "reach" study), Jesus's mid-step settling to a stop, his halo
quickening/glinting as power visibly leaves him, the crowd jostling — which
gave the motion budget legitimate targets, and (2) a PAGE-GLOBAL fence
("every mark in the paper is old, dry, long set... no new stain, spot, or
darkening appears anywhere") rather than a stain-local one. Retry passed
clean: stain held stable, real story motion visible, user-confirmed on
watch ("looks good"). F05 (veo, pure holds, the resolution page) passed
technical QC on the first attempt — then FAILED on the user's real-playback
watch ("this was not that good... too static/lifeless"): the same all-holds
disease F04 v1 had, minus the stain escalation, because F05 was never given
the F04 v2 fix. Redesigned same day the identical way, tuned to its own beat
(the blessing landing, not the desperate touch): Jesus's one small kind nod,
the woman's slow deep breath + shoulder-release as the fear leaves her, a
full-arc blink on panel 2's tear-streaked close-up, the crowd leaning gently
in, NO_MOUTH moved to Jesus (the baked caption is HIS line, Mark 5:34),
page-global fence kept verbatim — and moved to Kling3.0 pro per the
completing-gesture tiering rule (the nod and the blink must complete
mid-clip; veo never attempts them). **F05 v2 rendered clean and
user-confirmed ("much better, lets lock this one in"):** no stain regrowth,
no speech bubble, and this time real playback (not just the contact sheet)
carried the story. **"The Hem" is now a fully locked, validated two-page
sequence — both pages passed on real playback, not just technical QC.**
**Standing lesson, the load-bearing one from this whole test: a "hold
everything still" clip is not automatically safe — it can starve every
OTHER element of motion and dump the model's motion budget onto whatever's
left un-fenced. Give the real story real motion, fence what must not move
with a page-global fence (not a local mention of one thing), and — this is
the part that bit F05 specifically — a fix proven on one page does NOT
carry to a sibling page automatically; each page needs its own real-playback
verdict, even in the same sequence, even from the same session.**

**Recurring finding, now confirmed 2x, and the candidate fix held on a
retest — Kling can draw an unrequested speech bubble around caption text.**
Seen on the Cross INK_LIFE test and on Hem F04 v2 (both Kling, both on
captions that are effectively the speaking figure's own quoted line, both
with NO_MOUTH already stated). The fix added to THE TEMPLATE ("with no
border, box, or speech bubble ever appearing around any caption or note")
did NOT recur on F05 v2, also Kling, also a quoted-line caption — one clean
data point in the fix's favor, not yet enough renders to call it fully
proven, but promising enough to keep as the standing template default.

**OPEN (designed or inferred, not yet proven — do not rely on):**

- Close-up micro-motion (shot 4 v3: no defects on the contact sheet but very
  little visible motion — needs a real-playback verdict; may need a slightly
  larger bounded ask).
- Stage 1 single-thread motion (untested; rule says hold it still).
- Whether tone-only panel treatment actually prevents prop invention
  (inferred from one v3-vs-v4 contrast, not A/B'd).
- 16:9 behavior of all of the above (every animation test so far was 9:16).
- The Fray motif (still-only, no animation claim to test — untested at all,
  still or clip).
- The speech-bubble fix above (diagnosed, not yet attempted).
