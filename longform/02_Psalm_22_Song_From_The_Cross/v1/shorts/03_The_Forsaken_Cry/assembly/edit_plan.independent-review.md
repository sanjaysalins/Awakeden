# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
#01 crying-face hook; #02 David/prophet records; #08 bowed face on 'David's very first line'; #05 crying face under DAVID'S spoken cry; #04 ninth-hour crucifixion on 'a thousand years later, at the ninth hour'; #06 three crosses on 'Jesus cried it from the cross'; #09 crucifixion under JESUS' spoken cry; #10 It-Is-Finished on 'the sinless Son taking our place'; #12 the dawn cross on 'He was forsaken so that you never will be'; #13 Come-to-Him (Christ + dawn) on 'however far you've run / the way home is open'. Hero #11 (the way opening from the dark) closes.

## Slots
- ` 0` **body/hook** — #01 The Cry · 0.00-4.06s (4.06s) · 1.24x · speed  
  _crying-face hook_
- ` 1` **body/hook** — #02 David's Forsaken Psalm · 4.06-9.40s (5.34s) · 0.94x · speed  
  _David/prophet records the words_
- ` 2` **body/hook** — #08 Still 'My God' · 9.40-15.16s (5.76s) · 0.88x · speed  
  _bowed face on 'David's very first line'_
- ` 3` **body/david** — #05 My God, My God · 15.16-16.58s (1.42s) · 1.30x · speed+trim  
  _crying face under DAVID'S cry_
- ` 4` **body/bridge** — #04 The Ninth Hour · 16.58-20.46s (3.88s) · 1.30x · speed  
  _ninth-hour crucifixion_
- ` 5` **body/bridge** — #06 Darkness Over the Land · 20.46-23.88s (3.42s) · 1.30x · speed+trim  
  _three crosses on 'Jesus cried it'_
- ` 6` **body/quote** — #09 Bearing the Forsaking · 23.88-25.62s (1.74s) · 1.30x · speed+trim  
  _crucifixion under JESUS' cry_
- ` 7` **body/landing** — #10 So You Never Will Be · 25.62-32.96s (7.34s) · 0.69x · speed  
  _It Is Finished on 'sinless Son taking our place'_
- ` 8` **body/landing** — #12 A Thousand Years Apart · 32.96-46.68s (13.72s) · 0.37x · speed  
  _the dawn cross on 'forsaken so you never will be' (light breaks)_
- ` 9` **body/landing** — #13 However Far You've Run · 46.68-52.98s (6.30s) · 0.80x · speed  
  _Christ + dawn on 'the way home is open'_
- `10` **hero-tail/hero** — #11 The Way Opened from the Dark · 52.98-54.98s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — punchier (10 body); 2 dawn beats add variety from the crucifixions.
- **Beat-Sync** — `STRONG` — cries on right faces; dawn on the grace turn.
- **No-Reuse** — `STRONG` — no repeat.
- **Pacing** — `STRONG` — natural; hand-free clips now.
- **Hero-Continuity** — `STRONG` — lands on the gospel-pivot.
- **Jaded Viewer** — `STRONG` — cleaner + more varied.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 11 slots tile 0->54.98s contiguously.
- **AS-G2 No Reuse** — `PASS` — 10 distinct body clips; hero #11 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.01x, max 1.30x, 3 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['bridge', 'david', 'hook', 'landing', 'quote'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #11 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — David->Christ->dawn arc; scenes 12/13 clean.
- **AS-G9 Beat Density** — `CONDITIONAL` — 10 moments · avg slot 5.3s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 14 (pool has 11).
