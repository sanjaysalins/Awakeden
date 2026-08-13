# Her Seed — Seed of the Woman short #2 (Galatians 4:4)

Manifest slug: `seed-of-woman-02-her-seed`. Source narration (LOCKED, already
voiced, reused verbatim, $0): `PythonProject1/jesus/narration/45_Not_Plan_B/v1/`
— narration.md + narration.mp3 (58.82s). Real word-level timing:
`_alignment.json` (this folder), via `_s0_align.py`, 166/166 words matched.
Single voice throughout (narrator only, `voices.json` — no first-person
divine speech in this piece, so no multi-voice split needed).

## Cast / object census

- **ADAM / EVE** — reuse repo cast `poc_living_sketchbook/cast/ADAM.md` +
  `adam_ref.png`, `EVE.md` + `eve_ref.png` (s01 only).
- **MARY** — NO fixed cast anchor, by design. The LOCKED long's own §5
  decision was "Mary with no anchor — face always averted, angel as
  light" (`seed_of_the_woman/_PLAN.md` row 30, `s30_annunciation.png`
  reference) — same convention carried here, so no `mary_ref.png` gets
  created. s04 and s06 both show her; s06 self-chains from s04's own
  rendered output (pass it as an image ref) to keep the two shots
  feeling like the same figure across this short WITHOUT a permanent
  named cast asset — consistent with why the long never locked one.
- **CHRIST** — reuse repo cast `poc_living_sketchbook/cast/jesus_ref.png`
  for the landing (s08).
- **No serpent this short** — Her Seed never depicts the curse scene
  itself, a deliberate visual break from short #1's serpent-heavy
  content (real variety across the cluster, not an oversight).

**On reuse from the LOCKED long**: checked `seed_of_the_woman/stills/` for
direct pixel reuse (s26_her_seed_study.png for the "already written"
beat, s27_line_of_fathers.png for the genealogy-line beat, s30_annunciation.png
for Mary). All three are 2752×1536 (16:9, the long's own format) — none
crop cleanly to this short's 9:16 vertical without destroying the
composition (s27 is a full-width horizontal line of 7 figures; a
portrait crop would show 1-2 figures and lose the "lineage" point
entirely; s26 is a wide desk collage with corner vignette panels around
a narrow center column that doesn't reach the frame edges cleanly).
So: **design-reference reuse, not pixel reuse** — same pattern short #1
used for its serpent chain (image passed as a style/composition anchor
to the still-generation call, new vertical render). Genuine $0 pixel
reuse is limited to the repo cast anchors (Adam/Eve/Christ).

## Spread table (8 spreads, ~58.8s + 3.0s landing hold)

| # | window (s) | shot | content | words |
|---|---|---|---|---|
| s01 | 0.00–8.29 | wide (shot-variety floor) | Eden coming apart — Adam and Eve small, leaves falling, color draining, but ONE faint warm thread of light already present unlit at the frame's edge (a visual seed for the "that's not the oldest promise" subversion two lines later) | "You've heard it as Plan B — Eden fell apart, so God improvised a rescue and sent His Son. That is not what the oldest promise says." |
| s02 | 8.29–13.25 | wide, no-figure-on-her-alone (shot-variety floor) | Eve standing alone in the garden, unseen radiant light falling on her — the promise being spoken, not the curse (a calmer echo of short #1's "sentence spoken to serpent" convention, this time light ON a person, not the snake) | "Genesis already named this seed — a promise spoken over a woman in the garden." |
| s03 | 13.25–20.39 | object insert, close (shot-variety floor) | an old open page, already inked long ago, warm oil-lamp light — design-reference from `s26_her_seed_study.png`'s "already written under lamplight" idea, built fresh in vertical, no writing hand needed (it's ALREADY written, that's the point) | "Jesus wasn't a rescue invented in the fulness of time. He was the plan, named first." |
| s04 | 20.39–27.88 | ACTING spread, HERO (shot-variety floor) | Mary, veiled, face averted, hands gathering at her heart, unseen radiant light above (no angel figure) — design-reference from `s30_annunciation.png`, built fresh vertical, this is the anchor image of the whole piece | KJV: "Paul writes: 'But when the fulness of the time was come, God sent forth his Son, made of a woman, made under the law.'" |
| s05 | 27.88–34.66 | device spread, no-figure (shot-variety floor) | a vertical descent-line: small anonymous silhouetted figures linked father-to-father, drawn top to bottom down the page (portrait adaptation of `s27_line_of_fathers.png`'s device, NOT a crop — the line runs DOWN not across) | "Paul could have written son of David, son of Abraham — a line that runs through the man, like every title before it." |
| s06 | 34.66–41.21 | close portrait, match-cut to s04 | Mary again, close on her veiled face, still averted — self-chained from s04's own output for visual consistency, no new identity | "Here, he doesn't. He writes: made of a woman, the woman promised in the garden." |
| s07 | 41.21–51.26 | conviction, close hands | two human hands reaching out, straining toward something just out of frame, tense — by the end of the clip's motion they stop reaching and go still, unclenched (mirrors short #1's s01→s08b tension/release arc, compressed into one shot's motion arc here) | "You still reach for your own rescue plans — the fix, the resolution, the version of you that finally gets it right. But the plan was never yours to write." |
| s08 | 51.26–58.82 (+3.0s hold) | LANDING, sacred stillness | Christ in radiant warm gold light, reverent distance, closing on Him per the locked AS-G7 rule | "This was never Plan B. It was the plan, kept word for word — and He has already arrived for you." |

Shot-variety floor: wide (s01/s02) / object insert (s03) / acting/hero
(s04) / device no-figure (s05) / close portrait (s06) / close hands (s07)
/ landing (s08) — satisfied, no repeated shot type back-to-back.

## Animation tiering (judged per-shot, not mechanically applied)

- **Seedance**: s01 (leaves drift, calm — matches the long's own "leaves
  drift, calm" treatment for a coming-apart Eden), s06 (Mary's close
  portrait, a single blink + soft settling — face-fidelity matters here).
- **Kling**: s04 (the one designed/cued acting spread — hands gathering
  at the heart, light brightening, then holds — veo does not reliably
  execute cued gestures per this project's own bake-off), s07 (reach,
  then release — also a real cued gesture, two-stage).
- **veo3_1_lite**: s08 (reverent radiant hold, veo's clearest proven win
  per short #1). Positive-only glow phrasing on the light (the known
  glitter gotcha).
- **$0, by device, not by default**: s02 (camera push is enough — light
  arriving on a still figure needs no invented motion) and s03/s05
  (BOTH already-proven $0 devices from the long's own toolkit —
  annotators-circle and drawn-line-reveal — reused as techniques, not
  paid-then-reverted fallbacks). This is the discipline the round-2
  first_gospel_in_the_curse rebuild established: $0 only where a device
  or the shot's own content genuinely doesn't need generated motion,
  decided BEFORE rendering, not as a retreat after a paid attempt fails.

## Cost estimate (real per-unit prices from this cluster's own ledger)

Stills: 5× kling_omni_image ($0.075 — s01/s02/s03/s05/s07) + 3×
seedream_v4_5 ($0.15 — s04/s06/s08, the hero/consistency/landing shots)
= **$0.825**.
Animation: 2× Seedance ($0.72 — s01/s06 = $1.44) + 2× Kling ($1.312 —
s04/s07 = $2.624) + 1× veo ($0.60 — s08) + 2× $0 device (s02/s03... wait,
s02 is camera-push $0, s03/s05 are device $0) = **$4.664**.
**Total estimate ≈ $5.49**, plus a retry buffer for 1-2 shots (this
cluster's own realized-vs-estimated pattern has run close to or under
estimate) — call it **$5.50-7.50** to be safe. Cheaper than short #1
($8.35 actual) mostly because only 3 shots need the expensive
Kling/seedream tier (vs 5) and 2 of the 3 $0 slots are proven devices,
not paid-then-reverted retries.
