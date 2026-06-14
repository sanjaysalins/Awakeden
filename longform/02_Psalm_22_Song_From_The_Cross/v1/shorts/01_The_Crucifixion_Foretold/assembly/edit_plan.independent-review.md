# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Pinned by meaning in time order, matching the prior locked cut: #01 'Ten centuries before the cross' (hook); #02 'a song recorded how a dying man's clothes'; #04 'Psalm twenty-two'; #03 'David himself was never executed'; #11 'describing someone else'; #08 'stripped, surrounded, poured out'; #09 'his killers would divide his clothes'; #12 'cast lots upon my vesture'; #06 'soldiers dividing Jesus' clothes'; #05 'casting lots for the seamless coat'; #10 'the cross was no accident' (re-rendered, no inscription board); #13 'the suffering man has a name'; #14 'rolled dice for the clothes'. Hero #07 the cross closes.

## Slots
- ` 0` **body/hook** — #01 The Dice in the Dust · 0.00-2.04s (2.04s) · 2.20x · speed+trim  
  _'Ten centuries before the cross' — dice/garments hook._
- ` 1` **body/hook** — #02 David at the Lamp · 2.04-5.34s (3.30s) · 1.30x · speed+trim  
  _'a song recorded how a dying man's clothes would be divided'._
- ` 2` **body/hook** — #04 The Line, Centuries Early · 5.34-8.42s (3.08s) · 1.30x · speed+trim  
  _'Psalm twenty-two' — David at the lamp._
- ` 3` **body/hook** — #03 A Death Not His Own · 8.42-12.46s (4.04s) · 2.20x · speed+trim  
  _'David himself was never executed'._
- ` 4` **body/hook** — #11 A Thousand Years Apart · 12.46-16.30s (3.84s) · 1.30x · speed+trim  
  _'He was describing someone else'._
- ` 5` **body/hook** — #08 The Whole Execution, Written Early · 16.30-20.54s (4.24s) · 1.30x · speed+trim  
  _'stripped, surrounded, his life poured out'._
- ` 6` **body/hook** — #09 A Life Down to a Pile of Cloth · 20.54-25.02s (4.48s) · 2.20x · speed+trim  
  _'his killers would divide his clothes'._
- ` 7` **body/hook** — #12 Chance Rolls Out a Certainty · 25.02-32.04s (7.02s) · 1.43x · speed  
  _'cast lots upon my vesture'._
- ` 8` **body/hook** — #06 Cast Lots at the Cross · 32.04-37.76s (5.72s) · 1.30x · speed+trim  
  _'soldiers dividing Jesus' clothes'._
- ` 9` **body/hook** — #05 The Coat They Would Not Tear · 37.76-40.40s (2.64s) · 2.20x · speed+trim  
  _'casting lots for the seamless coat'._
- `10` **body/hook** — #10 No Accident - the Plan · 40.40-50.32s (9.92s) · 1.01x · speed  
  _'the cross was no accident' (re-rendered, no inscription board)._
- `11` **body/hook** — #13 His Name Is Jesus · 50.32-55.50s (5.18s) · 1.30x · speed+trim  
  _'the suffering man of Psalm 22 has a name'._
- `12` **body/hook** — #14 Laying Down His Life · 55.50-62.14s (6.64s) · 1.30x · speed+trim  
  _'they rolled dice for the clothes off His back'._
- `13` **hero-tail/hero** — #07 The Cross, Foretold · 62.14-64.14s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — Dense 13-clip gated crop-cut body; hero #07 cross held close.
- **Beat-Sync** — `STRONG` — Exact-phrase pins throughout the garments thread.
- **No-Reuse** — `STRONG` — 13 distinct; hero #07 only at close.
- **Pacing** — `STRONG` — Sacred close near full speed.
- **Hero-Continuity** — `STRONG` — Dice hook-open + hero #07 cross close.
- **Jaded Viewer** — `STRONG` — Coherent, tight.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->64.14s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #07 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `CONDITIONAL` — avg speed 1.56x, max 2.20x, 11/13 trimmed — brisk; verify it does not strobe.  
  _fix:_ Reduce clip count (lower --clips) so slots breathe.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #07 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — Garments thread carried; close on the cross.
- **AS-G9 Beat Density** — `CONDITIONAL` — 13 moments · avg slot 4.8s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 16 (pool has 14).
