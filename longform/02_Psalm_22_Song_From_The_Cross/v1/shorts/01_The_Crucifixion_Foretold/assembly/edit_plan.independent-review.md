# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Punchy pin-by-meaning across 14 clips + hero. Hook opens on the casting-lots dice (#01), then David describing someone else (#03), a tender suffering face (#04) on 'describing someone else', the full crucified body (#08) on 'his life poured out', the garments heap (#09) on 'divide his clothes', and the KJV quote lands on the soldiers casting lots (#06) + the dice macro (#12). The fulfilment: a thousand years apart (#11), the cross foretold (#07) on 'John watched it at the cross', the seamless coat (#05) on 'dividing Jesus' clothes'. The landing: 'It is finished' (#02) on 'that the scripture might be fulfilled', sovereign stillness (#10) on 'the cross was no accident', His name is Jesus (#13) on 'has a name: Jesus', the substitution (#15) on 'never seeing what He was doing', and the hero #14 (laying down His life) closes on 'to win you back'.

## Slots
- ` 0` **body/hook** — #01 The Dice in the Dust · 0.00-2.04s (2.04s) · 2.47x · speed  
  _hook-open: soldiers' hands + tumbling dice, under 'ten centuries before the cross'_
- ` 1` **body/hook** — #03 A Death Not His Own · 2.04-10.28s (8.24s) · 0.61x · speed  
  _aged David describing a death not his own, under 'David wrote it in the first person'_
- ` 2` **body/hook** — #04 Looking Down In Love · 10.28-16.30s (6.02s) · 0.84x · speed  
  _the tender crucified face looking down, under 'He was describing someone else'_
- ` 3` **body/hook** — #08 Hung By The Arms · 16.30-20.54s (4.24s) · 2.37x · speed  
  _the full crucified Christ, under 'stripped, surrounded, his life poured out'_
- ` 4` **body/hook** — #09 A Life Down to a Pile of Cloth · 20.54-25.02s (4.48s) · 1.13x · speed  
  _the heap of stripped garments, under 'divide his clothes'_
- ` 5` **body/hook** — #06 Cast Lots at the Cross · 25.02-28.98s (3.96s) · 2.54x · speed  
  _soldiers casting lots at the cross, under 'They part my garments among them'_
- ` 6` **body/hook** — #12 Chance Rolls Out a Certainty · 28.98-32.04s (3.06s) · 1.65x · speed  
  _the dice mid-tumble, under 'cast lots upon my vesture'_
- ` 7` **body/david** — #11 A Thousand Years Apart · 32.04-33.44s (1.40s) · 3.00x · speed+trim  
  _David at his lamp + the distant cross, under 'a thousand years later'_
- ` 8` **body/david** — #07 The Cross, Foretold · 33.44-35.52s (2.08s) · 2.42x · speed  
  _the crucified Christ with soldiers below, under 'John watched it at the cross'_
- ` 9` **body/david** — #05 The Coat They Would Not Tear · 35.52-37.76s (2.24s) · 2.25x · speed  
  _the seamless coat held between soldiers, under 'soldiers dividing Jesus' clothes'_
- `10` **body/landing** — #02 It Is Finished · 37.76-43.18s (5.42s) · 0.93x · speed  
  _the crucified Christ, the dying word finished, under 'that the scripture might be fulfilled'_
- `11` **body/landing** — #10 No Accident - the Plan · 43.18-50.32s (7.14s) · 0.71x · speed  
  _the crucified Christ in sovereign stillness, under 'the cross was no accident. It was the plan'_
- `12` **body/landing** — #13 His Name Is Jesus · 50.32-55.50s (5.18s) · 0.97x · speed  
  _the close reverent face, under 'has a name: Jesus'_
- `13` **body/landing** — #15 Crushed In Your Place · 55.50-70.54s (15.04s) · 0.34x · speed  
  _the substitution, crushed in your place, under 'never seeing what He was really doing'_
- `14` **hero-tail/hero** — #14 Laying Down His Life · 70.54-72.54s (2.00s) · 2.52x · speed  
  _Hero close — the whole hero clip sped to fit, landing on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — 14 distinct moments, ~5s/slot — punchy, clean open->climax->close.
- **Beat-Sync** — `STRONG` — garments/dice/coat/no-accident/His-name all land under their words.
- **No-Reuse** — `STRONG` — 14 distinct; hero only at close.
- **Pacing** — `STRONG` — sacred clips near full speed; one short symbolic plate at 3.0x; reverent.
- **Hero-Continuity** — `STRONG` — casting-lots hook open; lands on the crucified Christ.
- **Jaded Viewer** — `STRONG` — would stop; pace now punchy.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 15 slots tile 0->72.54s contiguously.
- **AS-G2 No Reuse** — `PASS` — 14 distinct body clips; hero #14 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.59x, max 3.00x, 1 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['david', 'hook', 'landing'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #14 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — garments-prophecy thread carried open->climax->close; close on gospel-pivot.
- **AS-G9 Beat Density** — `CONDITIONAL` — 14 moments · avg slot 5.0s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 18 (pool has 15).
