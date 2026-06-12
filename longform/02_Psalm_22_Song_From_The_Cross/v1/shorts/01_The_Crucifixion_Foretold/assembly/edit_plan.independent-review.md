# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Pinned by meaning in time order. Open on #01 dice (hook) at 'Ten centuries before the cross'; #02 David-at-lamp on 'a song recorded'; #04 the Hebrew line on 'Psalm twenty-two'; #03 David dying in old age on 'never executed... died an old man'; #11 the two-sided David/cross on 'describing someone else'; #08 the scroll+surrounding-beasts vision on 'stripped, surrounded'; #09 the heap of stripped clothes on 'divide his clothes'; #12 the dice macro on 'cast lots upon my vesture'; #06 soldiers at the cross on 'soldiers dividing Jesus' clothes'; #05 the seamless coat on 'the seamless coat'; #10 the sovereign cross on 'the cross was no accident. It was the plan'; #13 Christ's face on 'has a name: Jesus'; #14 the crucifixion on 'laying down His life'. Hero #07 (the cross) closes as the held gospel landing.

## Slots
- ` 0` **body/hook** — #01 The Dice in the Dust · 0.00-2.04s (2.04s) · 2.20x · speed+trim  
  _Dice in the dust — the arresting scroll-stopper under the opening line about the cross._
- ` 1` **body/hook** — #02 David at the Lamp · 2.04-5.34s (3.30s) · 1.30x · speed+trim  
  _David at the lamp recording the song — 'a song recorded'._
- ` 2` **body/hook** — #04 The Line, Centuries Early · 5.34-8.42s (3.08s) · 1.30x · speed+trim  
  _Fingertip on the Hebrew line — 'Psalm twenty-two', the written text._
- ` 3` **body/hook** — #03 A Death Not His Own · 8.42-12.46s (4.04s) · 2.20x · speed+trim  
  _Aged David dying in peace — 'David himself was never executed; he died an old man'._
- ` 4` **body/hook** — #11 A Thousand Years Apart · 12.46-16.30s (3.84s) · 1.30x · speed+trim  
  _Two-sided David-and-distant-cross — 'He was describing someone else'._
- ` 5` **body/hook** — #08 The Whole Execution, Written Early · 16.30-20.54s (4.24s) · 1.30x · speed+trim  
  _The Psalm scroll with the surrounding beasts vision — 'stripped, surrounded, his life poured out'._
- ` 6` **body/hook** — #09 A Life Down to a Pile of Cloth · 20.54-25.02s (4.48s) · 2.20x · speed+trim  
  _Heap of stripped garments — 'the dying man's killers would divide his clothes'._
- ` 7` **body/hook** — #12 Chance Rolls Out a Certainty · 25.02-32.04s (7.02s) · 1.43x · speed  
  _Dice caught mid-tumble — 'cast lots upon my vesture'._
- ` 8` **body/hook** — #06 Cast Lots at the Cross · 32.04-37.76s (5.72s) · 1.30x · speed+trim  
  _Soldiers casting lots at the foot of the cross — 'soldiers dividing Jesus' clothes'._
- ` 9` **body/hook** — #05 The Coat They Would Not Tear · 37.76-40.40s (2.64s) · 2.20x · speed+trim  
  _The seamless tunic held between soldiers — 'casting lots for the seamless coat'._
- `10` **body/hook** — #10 No Accident - the Plan · 40.40-50.32s (9.92s) · 1.01x · speed  
  _The sovereign crucified Christ — 'the cross was no accident. It was the plan'._
- `11` **body/hook** — #13 His Name Is Jesus · 50.32-55.50s (5.18s) · 1.30x · speed+trim  
  _Christ's reverent face — 'has a name: Jesus'._
- `12` **body/hook** — #14 Laying Down His Life · 55.50-62.14s (6.64s) · 1.30x · speed+trim  
  _The crucifixion at middle distance — 'laying down His life to win you back'._
- `13` **hero-tail/hero** — #07 The Cross, Foretold · 62.14-64.14s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — Fast, dense, coherent — the fix to the prior slow cut. 13 distinct moments in time order.
- **Beat-Sync** — `STRONG` — Clip-to-phrase pins hold up under scrutiny; no clip fights its words.
- **No-Reuse** — `STRONG` — 13 distinct; hero once at close.
- **Pacing** — `CAUTION` — Max 2.2x is at the cap; acceptable for a viral short but watch the fastest cuts for strobe on the heaviest Baroque frames.
- **Hero-Continuity** — `STRONG` — Hook open, cross close — lands on the gospel pivot.
- **Jaded Viewer** — `STRONG` — Holds attention; the ending crescendo of three Christ frames is earned.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->64.14s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #07 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `CONDITIONAL` — avg speed 1.56x, max 2.20x, 11/13 trimmed — brisk; verify it does not strobe.  
  _fix:_ Reduce clip count (lower --clips) so slots breathe.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #07 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — thread holds open->climax->close; clips match beats.
- **AS-G9 Beat Density** — `CONDITIONAL` — 13 moments · avg slot 4.8s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 16 (pool has 14).
