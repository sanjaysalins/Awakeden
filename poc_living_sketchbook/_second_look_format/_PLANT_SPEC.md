# The Second Look — Plant Spec (pilot: Look and Live / Numbers 21:8 → John 3:14)

**Status:** design spec only, nothing rendered under this spec yet. Step 1 of the 6-step
production plan in the format recommendation (`_SECOND_LOOK_RECOMMENDATION.md` — Fable's
synthesized verdict from 4 independent format deep-dives, approved by the user 2026-08-18).

**Scope note:** this is a NEW, separate format experiment. It is unrelated to and must not
touch `longform/EW04_Bronze_Serpent/v1/` (a different, already-LOCKED eyewitness/living-sketchbook
piece — do not open, do not edit). This spec's pilot material is the session's own Jesus-POV
`Look and Live` work (`poc_living_sketchbook/look_and_live/_jesus_pov_poc/`, "Noon Frieze" visual
style, already validated across 32 test renders / 8 rounds).

**Structural exception, explicitly authorized:** this format holds Jesus's name and voice out of
the first 45 seconds, which cuts against the project's locked Gospel Five-Beat structure and
early-thread discipline. The user reviewed this exact tension (flagged in the recommendation doc)
and said "go" — treated here as sign-off for this format as a deliberate structural variant, not
a quiet swap of the locked default. If this pilot ships, it should be logged as such, not folded
into the default structure silently.

---

## 1. The mechanic, restated

Act 1 (0:00–0:45) tells Numbers 21:8 straight — a complete, gripping story on its own, zero
mention of Jesus. Four shots are quietly double-designed: each has an honest first-watch reading
and a true second-watch reading, achieved through composition alone (angle, shadow, silhouette
shape, pose) — nothing added to any shot that isn't already, honestly, there. At 0:45, Christ's
own voice speaks John 3:14–15 KJV while the four shots replay fast and complete (The Vantage's
word-locked snap, not a soft dissolve). The final frame matches the opening frame exactly, so
Shorts' auto-loop plays Act 1 again — now read completely differently.

## 2. The four plants

Each entry: the honest first-watch reading, the honest second-watch reading, and the concrete
composition note that makes the second reading true without touching the first.

### Plant 1 — Moses raises the pole
- **First watch:** Moses plants a tall wooden pole upright in the sand, straining with the effort.
- **Second watch:** Shot from a low frontal angle with two smaller support stakes or tent-poles
  placed in the background left and right of the main pole (already a natural feature of a
  wilderness camp — nothing invented), the three uprights read as a Golgotha silhouette.
- **Composition note:** camera height at Moses's knee level, main pole dead center, the two
  secondary uprights placed at roughly 30° either side, far enough back to read as camp structure
  on first watch, close enough in the frame's geometry to complete the three-crosses read on
  second watch.

### Plant 2 — The bronze serpent effigy
- **First watch:** A coiled bronze serpent fixed at the top of the pole, catching the sun.
- **Second watch:** The coil's silhouette, held at this exact angle, reads as a figure's slumped
  head and shoulders against a crossbar.
- **Composition note:** this is the highest-risk plant — the coil shape must be genuinely
  ambiguous, not forced. Render 2–3 coil-angle variants and blind-test each (see §4) before
  locking one.

### Plant 3 — The pole's shadow
- **First watch:** The pole casts a long shadow across the sand near a suffering figure.
- **Second watch:** The shadow's shape, given the sun angle, falls as a cross directly over him.
- **Composition note:** low sun (already established in the Noon Frieze default palette — this
  plant needs no new lighting setup), shadow length calculated so the crossbar shadow lands across
  the figure's chest, not just near him.

### Plant 4 — Moses's lifting pose
- **First watch:** Moses's arms spread as he raises the pole into position.
- **Second watch:** Held for one beat at the top of the motion, his own pose is cruciform.
- **Composition note:** this is a pose-timing plant, not a composition plant — whichever animation
  provider renders this beat needs a one-frame hold at full arm extension, not a continuous motion
  blur through it.

## 3. The Turn (0:45–0:52)

Christ's voice (the established `jesus` ElevenLabs voice) speaks John 3:14–15 KJV. Under it, the
four plants replay in order at ~0.7s each, each one completing:
- Plant 1's three uprights → held on the Golgotha angle, no further reveal needed, it's already read.
- Plant 2's coil → match-cut or match-dissolve to the same silhouette shape rendered as Christ's
  head and shoulders on the cross (same coil angle, same frame position — this is the one plant
  that needs an actual second rendered asset, built to match the first's silhouette exactly).
- Plant 3's shadow → the shadow's cross shape holds, camera pulls back to reveal it now falls
  across the base of an actual cross, not just the pole.
- Plant 4's pose → freeze-match to Christ's own cruciform pose on the cross, same arm angle.

Word-lock: the snap on Plant 2 (the highest-impact one) fires on the word "**lifted**" in
"...even so must the Son of man be lifted up," using the caption stage's existing word-alignment
JSON — deterministic ffmpeg cut, not an AI-generated transition.

## 4. Blind-read test (before any animation spend)

Render only the 4 Act-1 stills through the existing image gate (Noon Frieze style, already proven
consistent — see `_ALL_STYLES_REVIEW.html`). Show them cold, no context, to fresh reviewers with
one question: "describe what you see."

- Anyone naming Jesus, a cross, or crucifixion unprompted on FIRST exposure → that plant is too
  loud, reframe the composition note above.
- Show the same 4 stills again, this time primed ("these are from a story about Jesus — look
  again") → if nobody senses anything different on the second look, the plant is too quiet.
- Target: the plant is invisible unprimed, legible primed. That gap is the whole format.

## 5. Doctrinal grounding (for the panel)

- **Luke 24:27, 24:32** — the Emmaus road: Christ opens the same Scriptures the disciples already
  knew, and *they see him in them* — "did not our heart burn within us." The format's whole
  mechanic — same material, second pass, Christ suddenly visible — is this text, not a metaphor
  borrowed from it.
- **Hebrews 10:1** — the law "having a shadow of good things to come, and not the very image" —
  grounds why Act 1's plants are honestly readable as ordinary story details on first watch: a
  shadow is real and true on its own terms, it just isn't the whole picture yet.
- **2 Corinthians 3:18** — "beholding... changed into the same image" — grounds the loop mechanic
  itself: the second watch is not new information, it's the same material seen with opened eyes.
- **Guardrail:** every plant must survive being described honestly and neutrally (§4's blind test)
  as an ordinary detail of the Numbers 21 story. If a plant only "works" because it quietly implies
  something false about the Old Testament scene itself (e.g., inventing three poles that wouldn't
  plausibly be there), it fails and must be reframed or cut — the typology must ride on real
  compositional ambiguity, never on a fabricated detail.

## 6. Open questions for the panel

1. Does holding Jesus's name/voice out of the first 45 seconds read as evasive or as a genuine
   dramatic structure, given the project's own doctrine that "the whole Bible, through Jesus" is
   never optional? (This is the structural-exception risk from §0, put to the panel directly.)
2. Is Plant 2 (the serpent-coil-as-slumped-figure) doctrinally sound as a compositional device, or
   does it risk reading as making light of the crucifixion by "hiding" it in a puzzle?
3. Are any of the four plants a stretch that a hostile reader would flag as invented meaning rather
   than discovered pattern?

---

**Next step (§2 of the 6-step plan):** render the 4 Act-1 stills only (no animation spend) and run
the blind-read test in §4, in parallel with this panel review.
