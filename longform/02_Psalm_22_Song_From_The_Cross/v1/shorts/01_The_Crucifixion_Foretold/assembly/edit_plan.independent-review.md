# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Opens on the arresting dice-in-the-dust (#01) under 'Ten centuries before the cross'. Aged David (#03) lands on 'David himself was never executed; he died an old man'. The heap of stripped garments (#09) sits under 'divide his clothes'; the dice macro (#12) under 'cast lots upon my vesture'. The seamless coat between the soldiers (#05) plays under 'casting lots for the seamless coat'. The cut turns to Christ for the landing: His face (#13) on 'has a name: Jesus', and the crucified Christ at middle distance (#14) on 'laying down His life to win you back'. The hero cross (#07) holds as the closing still.

## Slots
- ` 0` **body/hook** — #01 The Dice in the Dust · 0.00-2.04s (2.04s) · 2.20x · speed+trim  
  _dice mid-tumble at the foot of the cross = the most arresting hook-open, under 'Ten centuries before the cross'_
- ` 1` **body/hook** — #03 A Death Not His Own · 2.04-12.46s (10.42s) · 0.48x · speed  
  _aged David at peace in old age = 'David himself was never executed; he died an old man'_
- ` 2` **body/hook** — #09 A Life Down to a Pile of Cloth · 12.46-25.02s (12.56s) · 0.40x · speed  
  _heap of stripped garments = 'divide his clothes'_
- ` 3` **body/hook** — #12 Chance Rolls Out a Certainty · 25.02-32.04s (7.02s) · 0.72x · speed  
  _extreme dice macro = 'and cast lots upon my vesture'_
- ` 4` **body/hook** — #05 The Coat They Would Not Tear · 32.04-40.40s (8.36s) · 0.60x · speed  
  _the seamless tunic held taut between soldiers = 'casting lots for the seamless coat'_
- ` 5` **body/hook** — #13 His Name Is Jesus · 40.40-55.50s (15.10s) · 0.33x · speed  
  _the reverent face of the crucified Christ = 'has a name: Jesus'_
- ` 6` **body/hook** — #14 Laying Down His Life · 55.50-62.14s (6.64s) · 0.76x · speed  
  _the crucified Christ at middle distance = 'laying down His life to win you back'_
- ` 7` **hero-tail/hero** — #07 The Cross, Foretold · 62.14-64.14s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `CAUTION` — clean and lands well, but with 8 clips over 64s the avg slot ~8.9s reads slow for a viral Short.
- **Beat-Sync** — `STRONG` — every clip sits under the phrase it depicts; no clip fights its words.
- **No-Reuse** — `STRONG` — 7 body clips once each; hero #07 close-only.
- **Pacing** — `CAUTION` — avg 0.79x means body clips are slowed below natural — a thin pool, not a strobe; sacred clips fine.
- **Hero-Continuity** — `STRONG` — hook-open on the dice, closes on the crucified Christ — lands on the gospel-pivot.
- **Jaded Viewer** — `CAUTION` — would not feel a seam, but the slow pace risks a mid-scroll drop; punchier with more clips.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 8 slots tile 0->64.14s contiguously.
- **AS-G2 No Reuse** — `PASS` — 7 distinct body clips; hero #07 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 0.79x, max 2.20x, 1 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #07 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — garments/lots thread carried open->close; no clip contradicts its words
- **AS-G9 Beat Density** — `CONDITIONAL` — 7 moments · avg slot 8.9s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 16 (pool has 8).

## Priority fixes
1. Pool is thin (8 clips after exclusions) -> cut paces slow (0.79x); optional: add a clean action clip (e.g. 06 soldiers-cast-lots) or rebuild to punch it up.
