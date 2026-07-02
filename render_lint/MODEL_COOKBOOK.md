# MODEL COOKBOOK — seedream_v4_5 (HF, inked graphic-novel)

Empirical "what works" for THIS model, learned from controlled probes (hold everything constant,
vary one clause, render a matrix, look). Each entry = a proven recipe that feeds `rules.json`.
Run a probe with `render_lint/probe.py`; distil the winner here + into a rule.

The goal: before rendering 1000+ stills, know the model's behaviour so we don't pay for redos.

---

## 1. Pierced hand / crucifixion nail  ·  PROBE #1 (2026-07-01, 10 variants)
`batches/cluster_01_cross/father_forgive_them/visual/_probe/nail/compare.html`

**Finding:** On a palm-forward hand, the **word "nail"/"spike" always renders a proud vertical nail
standing OUT of the palm** (like a nail hammered into a board). Head-shape wording only changes the
top of that proud nail:
- `round head` / `flat head` / `disc` / `flush` → proud nail, different heads — all read wrong.
- `spike` → proud **arrowhead/harpoon**.
- `square head` → proud **floating cube**.
- even `"nail sunk so deep no metal stands out"` → still drew a small proud nail (the word summons it).

**What works — drop the word "nail" entirely, describe only the WOUND:**
- ✅ PASSION: *"a dark ragged pierced hole in the centre of the palm, dark red blood running down
  toward the wrist"* → clean pierced hole, no metal. (variant 09 — cleanest/most reverent)
- ✅ (gorier) *"a deep round puncture wound, rimmed with torn skin and dark clotted blood"* (variant 10)
- ✅ RISEN: *"one single round healed scar at the centre of the palm, smooth closed pale skin, flat
  and level"* — never say "nail" (draws a nail-in-scar), never "puckered" (draws X-stitches), pin to
  ONE centre-palm scar (two lifted hands can render an asymmetric white blob — prefer one dominant hand).

**Rule:** `nail-renders-as-stud`.
**If a nail object is truly needed** (e.g. a soldier holding one): show it lying flat / from the back
of the hand — not driven into a palm-forward hand.

---

## 2. Framing / zoom SWEET SPOT  ·  PROBE #2 (2026-07-01, 6 framings)
`batches/cluster_01_cross/father_forgive_them/visual/_probe/framing/compare.html`

Same subject + style, varied only the framing:

| framing | verdict |
|---|---|
| extreme macro (tiny detail) | ⚠️ RISKY — crams the subject in, floated a stray mini-FACE into the palm |
| close (subject + context) | ✅ EXCELLENT — the wound recipe reads perfectly here |
| medium (waist-up, one subject) | ✅ EXCELLENT |
| wide (full figure + environment) | ✅ EXCELLENT |
| epic vista (silhouettes, scale) | ✅ EXCELLENT |
| busy / "packed with detail / many elements" | ❌ BREAKS — fragments into a multi-panel COMIC PAGE (even with the ONE clause) |

**Design rule for the whole corpus:** compose **CLOSE → EPIC WIDE with ONE dominant subject**
(face / figure / cross / vista) — that is the model's dependable zone. AVOID:
- extreme macro of tiny detail (nails, coins, text) — it floats stray composites; shoot CLOSE not MACRO.
- "busy / packed / dense / many elements" — it splits into comic panels. For crowded moments use one
  dominant subject + a SHADOW/SILHOUETTE crowd + 2-3 props, never a fully packed frame.
**Rule:** `framing-sweet-spot`.

---

## 3. Character-face CONSISTENCY  ·  PROBE #3 (2026-07-01, 6 scenes)
`batches/cluster_01_cross/father_forgive_them/visual/_probe/face/compare.html`

seedream `--input_images` ref-lock is BROKEN, so we render no-ref with a shared text descriptor.
Same descriptor across 6 scenes/moods → **strong FAMILY resemblance** (same type: centre-parted dark
hair, full beard, olive skin, brown eyes, early 30s — a viewer accepts them as the same person across
a story) **but NOT an identity lock** — face width, beard shape and apparent age drift between renders.

**Biggest drift driver:** mood / glory adjectives ("glorified and radiant", "joyful", "sorrowful")
reshape the face (the glory render came out younger and prettier). Framing changes it too.

**Recipe for max consistency (given no working ref-lock):**
- use the EXACT SAME descriptor string every time (don't paraphrase it per scene);
- keep the FACE description NEUTRAL even in emotional scenes — put the emotion in posture, hands, light and context, NOT in face-reshaping adjectives;
- add specific STRUCTURAL marks (see probe #4);
- accept family-resemblance as the ceiling; don't expect frame-to-frame identity.
**Rule:** `character-face-consistency`.

---

## 4. Unique marks — STRUCTURE works, spot-marks DON'T  ·  PROBE #4 (2026-07-01, 6 scenes)
`batches/cluster_01_cross/father_forgive_them/visual/_probe/face_marks/compare.html`

Same 6 scene contexts as probe #3, but the descriptor added (a) **structural** marks — *lean face,
high cheekbones, slightly aquiline nose* — and (b) a **spot** mark — *a small dark mole on the LEFT
cheek below the eye*. Kept the face neutral, mood in posture/light.

**Finding — split result:**
- ✅ **Structural marks tightened the lock.** The face is noticeably more repeatable scene-to-scene
  than probe #3's generic descriptor — giving the model a specific skull geometry (lean / high
  cheekbones / aquiline nose) is the real consistency gain. Keep these.
- ⚠️ **The spot mole is unreliable — DROP it.** It persisted in all 6 (so it *is* a strong anchor
  signal) but it drifts: rendered as a **detached dot floating in the air** beside the cheek (night
  scene), **jumped to the forehead** (glory scene), wandered position on the rest. On a close/macro
  frame that stray dot is a defect. The cost outweighs the marginal anchor gain.
- ✅ Confirmed probe #3: neutral face + mood-in-posture/light held the same face across sorrow, glory, profile.

**Recipe:** bake the **structural** descriptors into the canonical string (lean face, high cheekbones,
aquiline nose, + the existing hair/beard/skin/eyes). Do **not** add a mole or other single spot-mark.
**Rule:** `character-face-consistency` (updated).

---

## 5. Animating an INKED panel (Kling 3.0 pro)  ·  TEST GATE (2026-07-01, 2 panels)
`batches/cluster_01_cross/father_forgive_them/visual/nbp/{02_jesus_prays,05_pierced_hand}.mp4`

The root shorts animator's motion prompt opens *"A still finished Baroque oil painting on flat
canvas…"* — feeding that over an **inked graphic-novel** panel makes Kling **repaint the ink into
oil**. Fix: declare the real medium.

**Recipe (validated on the two riskiest panels — a face push-in + the pierced-hand wound):**
- Open the motion prompt with *"A finished inked graphic-novel comic panel — flat printed art with
  bold black ink outlines, cel-flat color and cross-hatching."* → ink stays **flat, un-repainted**.
- Keep the proven cut-discipline verbatim: *"The drawing never moves/redraws/repaints… only the
  camera moves… INVENT NOTHING: show ONLY what is already inked; do not add any hand, nail, wound,
  limb, face…"* → the pierced-hand **wound held as a clean hole, no nail grew** (the 7×-fought panel).
- For a **motion comic** use ONE gentle per-panel move (push-in / pull-back / hold / dolly), not the
  5-hard-cut gallery tour — it leaves the frame readable under the PIL furniture composited on top.
- Faces stayed consistent through the push-in; no morphing.
**Driver:** `animate_stills.py` (piece-local; reuses `hf_animate`, slug-keyed to dodge the `01b/06c`
numeric-index collision). **Rule:** feeds the existing `never-animate-writing` / particle rules at stage=animation.

---

## Recurring model quirks already proven (see rules.json for the full set)
- **No negative channel:** naming a thing to forbid it DRAWS it ("no text/speech bubbles" → gibberish;
  "no cross" → cross). Describe the positive end-state; use the TEXT-FREE style for speaking panels.
- **Particle words** (dust/motes/sparkles) bloom into AI-glitter (veo/kling) — use steady-light wording.
- **Conflicting poses** (arms "nailed to the beam" AND "reaching to viewer") grow extra limbs — state ONE pose + an explicit limb count.
- **Large objects** (cross/throne) float unless explicitly planted/grounded.
- **Idols** default to Buddha unless the culture is named (Greco-Roman / Pan …).

## How to add an entry
1. Write `probe_<primitive>.py` (see `probe_nail.py`) — constant base, vary only the tested clause, 6-10 variants incl. controls.
2. Run it → `_probe/<primitive>/compare.html`; look at every variant.
3. Record the finding + the winning phrasing here; add/refine a rule in `rules.json` with the probe as provenance.
