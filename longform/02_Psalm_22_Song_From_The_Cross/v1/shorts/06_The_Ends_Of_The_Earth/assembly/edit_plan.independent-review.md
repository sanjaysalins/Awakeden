# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Opens on #01 (one forsaken man alone) under the hook. #03 (cross with the world horizon opening on every side) sits on 'the song throws its arms open to every nation'; #09 (far peoples turning toward the dawn light) under 'all the ends of the world shall remember and turn unto the LORD'; #08 (gathered nations worshipping) exactly on 'all the kindreds of the nations shall worship'. #05 (three crosses dwarfed in the Roman landscape) on 'a man dying in one corner of the Roman Empire'; #07 (patriarch under countless stars) on 'his song says the ends of the earth will turn to God'. #10 (the empty tomb) on 'and the empty tomb'; #11 (procession of many lands) on 'nation after nation have turned'; #14 (cross cresting the whole-earth horizon, light sweeping out) on 'the reach of the cross'. #12 (lone traveller toward the light) on 'wherever you are'; #13 (open road to the cross) on 'room for you to turn'. Hero #04 (the cross lifted, light spreading) closes.

## Slots
- ` 0` **body/hook** — #01 One Man, Alone · 0.00-3.82s (3.82s) · 1.30x · speed+trim  
  _hook-open: the single forsaken man on the lone cross under 'one forsaken man dying alone'._
- ` 1` **body/hook** — #03 All the Ends of the World · 3.82-11.20s (7.38s) · 0.68x · speed  
  _cross with the world horizon opening on every side = 'the song throws its arms open to every nation'._
- ` 2` **body/hook** — #09 A Light to the Gentiles · 11.20-13.82s (2.62s) · 1.30x · speed+trim  
  _far gentiles turning toward the single dawn light = 'all the ends of the world shall remember and turn unto the LORD'._
- ` 3` **body/hook** — #08 Kindreds of the Nations · 13.82-18.60s (4.78s) · 1.05x · speed  
  _a gathered company of many nations lifting their faces in worship = 'all the kindreds of the nations shall worship before thee'._
- ` 4` **body/hook** — #05 One Corner of the Empire · 18.60-21.88s (3.28s) · 1.54x · speed  
  _three crosses dwarfed by an immense Roman-era landscape = 'a man dying in one corner of the Roman Empire'._
- ` 5` **body/hook** — #07 In Thee All Nations Blessed · 21.88-24.38s (2.50s) · 1.30x · speed+trim  
  _the patriarch under numberless stars (the all-nations promise) = 'his song says the ends of the earth will turn to God'._
- ` 6` **body/hook** — #10 The Empty Tomb · 24.38-30.48s (6.10s) · 0.83x · speed  
  _the open rock-hewn tomb, stone rolled aside = 'and the empty tomb'._
- ` 7` **body/hook** — #11 Nation After Nation · 30.48-35.78s (5.30s) · 0.95x · speed  
  _a long procession of pilgrims of many lands toward the light = 'people in nation after nation have turned'._
- ` 8` **body/hook** — #14 The Whole Earth at Dawn · 35.78-41.92s (6.14s) · 0.82x · speed  
  _the cross cresting a vast world horizon, light sweeping across far lands = 'that is the reach of the cross'._
- ` 9` **body/hook** — #12 Wherever You Are · 41.92-50.86s (8.94s) · 0.56x · speed  
  _a lone traveller on a far road turned toward the distant light = '"the ends of the world" includes wherever you are'._
- `10` **body/hook** — #13 Room to Turn · 50.86-59.82s (8.96s) · 0.56x · speed  
  _a worn open road leading to the cross, the way left open = 'still has room for you to turn to Him'._
- `11` **hero-tail/hero** — #04 The Reach of the Cross · 59.82-61.82s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `CAUTION` — Clean arc; 11 clips for 61.8s runs ~5.4s/slot — slower than ideal, but HF clips carry internal viral motion so it does not read static.
- **Beat-Sync** — `STRONG` — Strong word-image pinning throughout: kindreds->worship, empire->three crosses, tomb->empty tomb, wherever-you-are->lone traveller, room-to-turn->open road.
- **No-Reuse** — `STRONG` — Every clip once; hero #04 only at close.
- **Pacing** — `STRONG` — Sacred frames near full speed; max 1.54x only on a landscape beat.
- **Hero-Continuity** — `STRONG` — Opens on the lone-cross hook, lands on the cross hero #04 — gospel frame intact.
- **Jaded Viewer** — `CAUTION` — Cross/horizon motif repeats; acceptable for the 'reach to the nations' theme and the viral motion holds attention.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 12 slots tile 0->61.82s contiguously.
- **AS-G2 No Reuse** — `PASS` — 11 distinct body clips; hero #04 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 0.99x, max 1.54x, 3 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #04 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — thread carried open->climax->close; no clip contradicts its words.
- **AS-G9 Beat Density** — `CONDITIONAL` — 11 moments · avg slot 5.4s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 15 (pool has 12).
