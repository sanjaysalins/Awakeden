# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
All 20 clips, full-coverage timeline (board now reaches 74s). Proof: man(#01), sheep(#08), scourged(#03), close wound(#05), poured-out(#17), hung(#16), ninth-hour(#15), crushed-substitution(#23), cry(#18), apostle(#07), bare-our-sins(#09). Pivot face(#11). Landing spread evenly to the end: reach-of-cross(#22), man-at-peace(#14), it-is-finished(#20), finished-at-cross(#12), come-to-him(#19), room-to-turn(#21), open-hands CTA(#13) on the final 'Come to Him, and receive it'. Hero pierced-Christ(#06) closes.

## Slots
- ` 0` **body/hook** — #01 The Wound That Won't Close · 0.00-2.98s (2.98s) · 1.69x · speed  
  _unhealed man — hook_
- ` 1` **body/hook** — #08 All We Like Sheep · 2.98-9.90s (6.92s) · 0.73x · speed  
  _sheep OT echo_
- ` 2` **body/hook** — #03 Wounded For Our Transgressions · 9.90-12.94s (3.04s) · 1.66x · speed  
  _scourged Christ_
- ` 3` **body/isaiah** — #05 Wounded For Us · 12.94-16.98s (4.04s) · 1.25x · speed  
  _close wound_
- ` 4` **body/isaiah** — #17 Poured Out Like Water · 16.98-19.24s (2.26s) · 2.23x · speed  
  _poured-out_
- ` 5` **body/isaiah** — #16 Hung By The Arms · 19.24-22.90s (3.66s) · 2.74x · speed  
  _hung by the arms — with his stripes_
- ` 6` **body/bridge** — #15 The Ninth Hour · 22.90-24.10s (1.20s) · 3.00x · speed+trim  
  _ninth-hour_
- ` 7` **body/bridge** — #23 Crushed In Your Place · 24.10-25.96s (1.86s) · 2.71x · speed  
  _crushed-in-your-place substitution_
- ` 8` **body/bridge** — #18 The Cry Of The Cross · 25.96-30.24s (4.28s) · 1.18x · speed  
  _the cry_
- ` 9` **body/bridge** — #07 The Apostle Lays It On Christ · 30.24-33.56s (3.32s) · 1.52x · speed  
  _apostle — Peter took up Isaiah's words_
- `10` **body/peter** — #09 He Bare Our Sins · 33.56-39.30s (5.74s) · 0.88x · speed  
  _bare our sins in his own body_
- `11` **body/peter** — #11 Aimed At You · 39.30-43.30s (4.00s) · 1.26x · speed  
  _face to viewer — ye were healed_
- `12` **body/landing** — #22 The Reach Of The Cross · 43.30-48.70s (5.40s) · 0.93x · speed  
  _radiant crucified Christ_
- `13` **body/landing** — #14 The Wound He Closed · 48.70-54.58s (5.88s) · 0.86x · speed  
  _man at peace_
- `14` **body/landing** — #20 It Is Finished · 54.58-59.48s (4.90s) · 1.03x · speed  
  _it is finished, dawn_
- `15` **body/landing** — #12 Finished At The Cross · 59.48-63.30s (3.82s) · 1.32x · speed  
  _finished at the cross_
- `16` **body/landing** — #19 Come To Him · 63.30-67.36s (4.06s) · 1.24x · speed  
  _come-to-him cross_
- `17` **body/landing** — #21 Room To Turn · 67.36-69.18s (1.82s) · 2.77x · speed  
  _dawn cross + path_
- `18` **body/landing** — #13 Come And Receive · 69.18-72.02s (2.84s) · 1.77x · speed  
  _open hands — Come to Him, and receive it_
- `19` **hero-tail/hero** — #06 Whom They Pierced · 72.02-74.02s (2.00s) · 2.52x · speed  
  _Hero close — the whole hero clip sped to fit, landing on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — Tight throughout, longest hold 6.9s; alignment fixed so CTA lands on the real final words.
- **Beat-Sync** — `STRONG` — Clips match their words; CTA on the closing line.
- **No-Reuse** — `STRONG` — 19 distinct; hero once at close.
- **Pacing** — `STRONG` — Sacred near full speed; narrator gently 1.08x; lively.
- **Hero-Continuity** — `STRONG` — Hook-open -> pierced-Christ gospel-pivot close.
- **Jaded Viewer** — `STRONG` — Fast, varied, lands on Christ.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 20 slots tile 0->74.02s contiguously.
- **AS-G2 No Reuse** — `PASS` — 19 distinct body clips; hero #06 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.62x, max 3.00x, 1 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['bridge', 'hook', 'isaiah', 'landing', 'peter'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #06 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — thread carried; clips fit words.
- **AS-G9 Beat Density** — `PASS` — 19 moments · avg slot 3.8s (target 4s) — lively.
