# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Opened on the three crosses at dusk (09) for 'a psalm's last line and Jesus' last breath... it is done', then the bowed head (07) on 'it is done'. 'The psalm closes looking ahead' rides The Way Opened From The Dark (18) — Christ lit, dawn breaking; the scribe writing for a people not yet born (02) follows. 'That he hath done this' sits on the finished cross at dawn (15); the bridge to John runs over the pierced hands (10) and the face of Christ (16); 'It is finished' lands on the rending veil (08). The landing runs Looking Down In Love (19) on 'different words a thousand years apart' -> the burden set down (12) on 'what's left to finish' -> the open door home (13) -> 'come to Him' (17), and the hero crucifixion 'It Is Finished' (04) closes as a held still.

## Slots
- ` 0` **body/hook** — #09 The Day Is Done · 0.00-4.26s (4.26s) · 1.18x · speed  
  _three bare crosses at dusk — the arresting hook for 'Jesus' last breath... it is done'_
- ` 1` **body/hook** — #07 The Bowed Head · 4.26-7.74s (3.48s) · 1.45x · speed  
  _the bowed head in completion — 'it is done'_
- ` 2` **body/hook** — #18 The Way Opened From The Dark · 7.74-9.54s (1.80s) · 2.80x · speed  
  _the way opened from the dark, dawn breaking — 'the psalm closes looking ahead'_
- ` 3` **body/hook** — #02 A People Not Yet Born · 9.54-15.02s (5.48s) · 1.83x · speed  
  _the scribe over the psalm — 'told to a people not yet born'_
- ` 4` **body/scripture** — #15 Finished At The Cross · 15.02-19.10s (4.08s) · 1.24x · speed  
  _the finished work at the cross, dawn — under 'that he hath done this'_
- ` 5` **body/bridge** — #10 Hands at Rest · 19.10-22.44s (3.34s) · 1.51x · speed  
  _the pierced hands at rest — 'as Jesus hung dying'_
- ` 6` **body/bridge** — #16 His Name Is Jesus · 22.44-24.58s (2.14s) · 2.36x · speed  
  _the face of the crucified Christ — 'John records His final word'_
- ` 7` **body/quote** — #08 The Torn Veil · 24.58-26.68s (2.10s) · 2.00x · speed+trim  
  _the temple veil rent top to bottom — the moment of 'It is finished'_
- ` 8` **body/landing** — #19 Looking Down In Love · 26.68-29.24s (2.56s) · 1.97x · speed  
  _the crucified Christ looking down in love — the tender unifying figure on 'different words a thousand years apart'_
- ` 9` **body/landing** — #12 Nothing Left to Carry · 29.24-37.44s (8.20s) · 0.61x · speed  
  _the heavy burden set down at the cross — 'what's left for you to finish? Nothing'_
- `10` **body/landing** — #13 The Open Door Home · 37.44-39.25s (1.81s) · 2.79x · speed  
  _the open door home in warm lamplight — 'Someone to come home to'_
- `11` **body/landing** — #17 Come To Him · 39.25-40.70s (1.45s) · 3.00x · speed+trim  
  _the cross at dawn, an invitation — 'the One who said it is done'_
- `12` **hero-tail/hero** — #04 It Is Finished · 40.70-42.70s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — Flows; 10/12 clips play full tour (speed-to-fit), 2 short closers trim ~15%.
- **Beat-Sync** — `STRONG` — Clips sit under the right phrases; no clip fights its words.
- **No-Reuse** — `STRONG` — 12 distinct; hero only at close.
- **Pacing** — `CAUTION` — Intentionally brisk to preserve richness; sacred capped at 2x, hero at 1x.
- **Hero-Continuity** — `CAUTION` — No clean hook-open survives (scroll opener was a defect); #09 substitutes; closes on Christ #04.
- **Jaded Viewer** — `STRONG` — Rich, lively, resolves on the cross.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 13 slots tile 0->42.70s contiguously.
- **AS-G2 No Reuse** — `PASS` — 12 distinct body clips; hero #04 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.89x, max 3.00x, 2 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['bridge', 'hook', 'landing', 'quote', 'scripture'].
- **AS-G6 Hero Close** — `CONDITIONAL` — Cut opens on #09 'The Day Is Done' (role=build), not a hook-open clip.  
  _fix:_ Open on the strongest hook-open scroll-stopper.
- **AS-G7 Gospel Frame** — `CONDITIONAL` — Gospel-pivot present (lands on Christ). Soft-missing: a hook-open clip.  
  _fix:_ Add a hook-open if available; cross optional when the pivot is resurrection.
- **AS-G8 Beat Continuity** — `PASS` — thread carried open->climax->close; lands on hero crucifixion.
- **AS-G9 Beat Density** — `PASS` — 12 moments · avg slot 3.4s (target 4s) — lively.
