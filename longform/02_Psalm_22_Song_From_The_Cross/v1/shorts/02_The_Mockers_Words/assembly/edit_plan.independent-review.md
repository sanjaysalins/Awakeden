# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Pinned by meaning in time order. Open on #01 the shaking heads at 'they shook their heads and sneered the very taunt'; #02 David records on 'Psalm twenty-two'; #03 the written Hebrew line on 'even writes his tormentors' words'; #06 the shot-out lip on the KJV shaking-the-head taunt; #12 the David-to-cross diptych on 'A thousand years later'; #04 the crowd at the cross on 'Matthew records both'; #13 the wagging crowd on 'passers-by wagging their heads'; #05 the leaders jeering on 'the religious leaders jeering'; #07 the jabbing hands on 'let him deliver him now'; #14 the nailed hand on 'not because Jesus lacked the power to come down'; #08 on 'He had every power'; #09 the restrained legions on 'staying was the only way to deliver you'; #10 the face of love on 'It was love'. Hero #11 (the cross, 'He chose to stay, with you in view') closes the cut.

## Slots
- ` 0` **body/hook** — #01 The Shaking Heads · 0.00-3.12s (3.12s) · 2.20x · speed+trim  
  _The shaking, jeering heads — the arresting hook under 'they shook their heads and sneered the very taunt'._
- ` 1` **body/hook** — #02 David Records the Taunt · 3.12-8.16s (5.04s) · 1.30x · speed+trim  
  _David records the taunt — 'Psalm twenty-two', the psalm being written._
- ` 2` **body/hook** — #03 Let Him Deliver Him · 8.16-13.54s (5.38s) · 1.30x · speed+trim  
  _The fingertip on the Hebrew line — 'even writes his tormentors' words'._
- ` 3` **body/hook** — #06 They Shoot Out the Lip · 13.54-14.70s (1.16s) · 2.20x · speed+trim  
  _The shot-out lip — the Ps 22:7 mockery gesture under 'they shake the head'._
- ` 4` **body/hook** — #12 A Thousand Years Apart · 14.70-21.18s (6.48s) · 1.30x · speed+trim  
  _The David-to-cross diptych — 'A thousand years later', the span itself._
- ` 5` **body/hook** — #04 The Crowd at the Cross · 21.18-24.16s (2.98s) · 1.30x · speed+trim  
  _The crowd at the cross — 'Matthew records both'._
- ` 6` **body/hook** — #13 The Mockers and the Silent King · 24.16-25.98s (1.82s) · 1.30x · speed+trim  
  _The wagging crowd's backs — 'the passers-by wagging their heads'._
- ` 7` **body/hook** — #05 The Religious Leaders Jeer · 25.98-28.38s (2.40s) · 2.20x · speed+trim  
  _The religious leaders sneering and pointing — 'the religious leaders jeering'._
- ` 8` **body/hook** — #07 The Jabbing Hands · 28.38-31.96s (3.58s) · 2.20x · speed+trim  
  _The jabbing hands flung up at the cross — 'let him deliver him now'._
- ` 9` **body/hook** — #14 The Hand That Would Not Pull Free · 31.96-42.56s (10.60s) · 0.95x · speed  
  _The nailed open hand that would not pull free — 'not because Jesus lacked the power to come down'._
- `10` **body/hook** — #08 He Had Every Power · 42.56-47.06s (4.50s) · 1.30x · speed+trim  
  _The sovereign low-angle Christ — 'He had every power'._
- `11` **body/hook** — #09 Twelve Legions Restrained · 47.06-50.82s (3.76s) · 1.30x · speed+trim  
  _The restrained legions / sheathed sword — 'staying was the only way to deliver you'._
- `12` **body/hook** — #10 Looking Down in Love · 50.82-58.02s (7.20s) · 1.30x · speed+trim  
  _The face looking down in love — 'It was love'._
- `13` **hero-tail/hero** — #11 He Chose to Stay · 58.02-60.02s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — Fast, dense, coherent; mockery front, gospel crescendo back.
- **Beat-Sync** — `STRONG` — Clip-to-phrase pins hold under scrutiny; no clip fights its words.
- **No-Reuse** — `STRONG` — 13 distinct; hero once at close.
- **Pacing** — `CAUTION` — Max 2.2x at the cap; acceptable viral pace, watch fastest cuts.
- **Hero-Continuity** — `STRONG` — Hook open, cross close — lands on the gospel-pivot.
- **Jaded Viewer** — `STRONG` — Holds attention; earned landing on 'He chose to stay'.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->60.02s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #11 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `CONDITIONAL` — avg speed 1.55x, max 2.20x, 12/13 trimmed — brisk; verify it does not strobe.  
  _fix:_ Reduce clip count (lower --clips) so slots breathe.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #11 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — thread carries open->climax->close.
- **AS-G9 Beat Density** — `PASS` — 13 moments · avg slot 4.5s (target 4s) — lively.
