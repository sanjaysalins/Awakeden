# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Opens on the weathered man with the wound that won't close (#01) under the hook. The wandering sheep + bowed figure (#08) on 'Isaiah wrote the healing would come through someone else'. The scourged back (#03) on 'wounded for our transgressions'. The apostle laying Isaiah's words on Christ (#07) on 'Peter took up Isaiah's words'; Christ bearing our sins (#09) on 'bare our sins in his own body'. The open welcoming hands (#13) on 'points the promise straight at you'. The dawn cross of completion (#12) on 'it was finished at the cross'; the same man now healed, scar closed (#14) on 'He has already closed'. Hero #06 — Christ in his own body on the tree — holds the close. Spread every ~4 beats so no slot drags.

## Slots
- ` 0` **body/hook** — #01 The Wound That Won't Close · 0.00-2.88s (2.88s) · 1.75x · speed  
  _man with a hand pressed over an unhealed wound = the hook 'a wound nothing can close'_
- ` 1` **body/hook** — #08 All We Like Sheep · 2.88-12.36s (9.48s) · 0.53x · speed  
  _scattered sheep + a figure bowed under weight = 'healing through someone else' (Isaiah)_
- ` 2` **body/hook** — #03 Wounded For Our Transgressions · 12.36-16.84s (4.48s) · 1.13x · speed  
  _the scourged, welted back = 'wounded for our transgressions'_
- ` 3` **body/hook** — #07 The Apostle Lays It On Christ · 16.84-32.74s (15.90s) · 0.32x · speed  
  _the apostle turning Isaiah's words toward the cross = 'Peter took up Isaiah's words'_
- ` 4` **body/hook** — #09 He Bare Our Sins · 32.74-37.84s (5.10s) · 0.99x · speed  
  _Christ bearing the burdens laid on him = 'bare our sins in his own body'_
- ` 5` **body/hook** — #13 Come And Receive · 37.84-52.68s (14.84s) · 0.34x · speed  
  _open welcoming hands with healed marks = 'points the promise straight at you'_
- ` 6` **body/hook** — #12 Finished At The Cross · 52.68-60.66s (7.98s) · 0.63x · speed  
  _the dawn cross of completion = 'it was finished at the cross'_
- ` 7` **body/hook** — #14 The Wound He Closed · 60.66-68.00s (7.34s) · 0.69x · speed  
  _the same man, scar now closed and at peace = 'He has already closed'_
- ` 8` **hero-tail/hero** — #06 In His Own Body, On The Tree · 68.00-70.00s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Beat-Sync** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **No-Reuse** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Pacing** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Hero-Continuity** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Jaded Viewer** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 9 slots tile 0->70.00s contiguously.
- **AS-G2 No Reuse** — `PASS` — 8 distinct body clips; hero #06 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 0.80x, max 1.75x, 0 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #06 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G9 Beat Density** — `CONDITIONAL` — 8 moments · avg slot 8.5s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 18 (pool has 9).
- **AS-G8 Beat Continuity** — `PASS` — thread carried open->climax->close; jigsaw pinned each clip to its phrase by meaning; cut lands on the gospel-pivot.
