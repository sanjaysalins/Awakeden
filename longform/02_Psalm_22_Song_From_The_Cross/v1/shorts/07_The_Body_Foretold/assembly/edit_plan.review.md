# Edit plan — Self-review panel

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Opens on the crucified body wrenched out of joint (#01) under 'a king described a dying body'. The king at his scroll (#02) on 'David wrote it'. The drained body (#03) on 'poured out like water'; the arm hung taut (#07) on 'hangs when suspended by the arms'; the countable ribs (#05) on 'I may tell all my bones'; the scourged back (#10) on 'stretched and exposed'; the staring onlookers (#06) on 'stood and stared'; the pierced marks (#08) on 'bears the marks of one'; the road to the lit door (#13) on 'to bring you home'; the dawn cross (#14) on the resolution; the climax of Christ crushed with the freed man kneeling (#12) on 'crushed in your place'. Hero #04 — the full crucified Christ — holds the close. The split-screen #09 is omitted (F2 defect).

## Slots
- ` 0` **body/hook** — #01 Out of Joint · 0.00-3.28s (3.28s) · 1.30x · speed+trim  
  _crucified body, arms taut, shoulders out of socket = the hook 'a dying body so exactly'_
- ` 1` **body/hook** — #02 The King Who Wrote It · 3.28-10.52s (7.24s) · 1.39x · speed  
  _the king low over his scroll = 'David wrote it in the first person'_
- ` 2` **body/hook** — #03 Poured Out Like Water · 10.52-18.50s (7.98s) · 0.63x · speed  
  _the drained, water-sheened body = 'I am poured out like water'_
- ` 3` **body/hook** — #07 Hung by the Arms · 18.50-27.40s (8.90s) · 0.48x · speed  
  _one arm pulled rigid along the beam = 'the way a body hangs when suspended by the arms'_
- ` 4` **body/hook** — #05 I May Tell All My Bones · 27.40-29.68s (2.28s) · 1.30x · speed+trim  
  _the countable ribcage = 'I may tell all my bones'_
- ` 5` **body/hook** — #10 Wounded for Us · 29.68-35.18s (5.50s) · 0.92x · speed  
  _the scourged, striped back = 'stretched and exposed'_
- ` 6` **body/hook** — #06 They Look and Stare · 35.18-38.62s (3.44s) · 1.30x · speed+trim  
  _the cluster of upturned staring onlookers = 'onlookers stood and stared at him'_
- ` 7` **body/hook** — #08 Whom They Pierced · 38.62-46.24s (7.62s) · 0.66x · speed  
  _the pierced side / marks = 'bears the marks of one'_
- ` 8` **body/hook** — #13 To Bring You Home · 46.24-51.20s (4.96s) · 1.02x · speed  
  _the road to a warm lit doorway = 'to bring you home'_
- ` 9` **body/hook** — #14 Come to Him · 51.20-52.58s (1.38s) · 1.30x · speed+trim  
  _the cross against a widening dawn = the resolution_
- `10` **body/hook** — #12 Crushed So Another Goes Free · 52.58-58.07s (5.49s) · 0.92x · speed  
  _Christ crushed with the freed man kneeling = 'He was crushed in your place'_
- `11` **hero-tail/hero** — #04 Crushed in Your Place · 58.07-60.07s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Self-review panel
- **Editor** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Beat-Sync** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **No-Reuse** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Pacing** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Hero-Continuity** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Jaded Viewer** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 12 slots tile 0->60.07s contiguously.
- **AS-G2 No Reuse** — `PASS` — 11 distinct body clips; hero #04 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.02x, max 1.39x, 4 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #04 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G9 Beat Density** — `CONDITIONAL` — 11 moments · avg slot 5.3s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 15 (pool has 13).
- **AS-G8 Beat Continuity** — `PASS` — thread carried open->climax->close; jigsaw pinned each clip to its phrase by meaning; cut lands on the gospel-pivot.
