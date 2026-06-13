# Edit plan — Self-review panel

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Pinned by meaning in time order. Open on #01 the cry at 'the loneliest sentence... wasn't His own line'; #02 David's forsaken psalm on 'Psalm twenty-two opens in the voice of a forsaken man'; #03 the Hebrew first line on 'David's very first line'; #05 the My-God cry face on the Psalm 22:1 quote; #12 the David-to-cross diptych on 'A thousand years later'; #04 the ninth-hour cross on 'at the ninth hour'; #06 the darkness over the land on 'Jesus cried it from the cross'; #07 the same-words Hebrew-and-cross on 'The very same words'; #08 the still-trusting face on 'even forsaken, He still calls God my God'; #09 bearing-the-forsaking (lamb + chains) on 'the sinless Son taking our place, bearing the forsaking'; #10 the face turning to light on 'forsaken so that you never will be'; #13 the lone road on 'However far you've run'; #14 the nailed hand + breaking light on 'He opened it from the dark'. Hero #11 (the cross against the breaking light) closes.

## Slots
- ` 0` **body/hook** — #01 The Cry · 0.00-4.06s (4.06s) · 1.30x · speed+trim  
  _The forsaken cry face — the arresting hook under 'the loneliest sentence... wasn't His own line'._
- ` 1` **body/hook** — #02 David's Forsaken Psalm · 4.06-9.40s (5.34s) · 1.30x · speed+trim  
  _David in the voice of a forsaken man — 'Psalm twenty-two opens in the voice of a forsaken man'._
- ` 2` **body/hook** — #03 The First Line · 9.40-15.16s (5.76s) · 1.30x · speed+trim  
  _The fingertip on the first Hebrew line — 'David's very first line'._
- ` 3` **body/hook** — #05 My God, My God · 15.16-16.58s (1.42s) · 1.30x · speed+trim  
  _The upturned My-God cry face — on the quoted Psalm 22:1._
- ` 4` **body/hook** — #12 A Thousand Years Apart · 16.58-20.46s (3.88s) · 1.30x · speed+trim  
  _The David-to-cross diptych — 'A thousand years later'._
- ` 5` **body/hook** — #04 The Ninth Hour · 20.46-21.58s (1.12s) · 1.30x · speed+trim  
  _The ninth-hour crucifixion with the darkened sun — 'at the ninth hour'._
- ` 6` **body/hook** — #06 Darkness Over the Land · 21.58-23.88s (2.30s) · 1.30x · speed+trim  
  _The darkness over the land at the cross — 'Jesus cried it from the cross'._
- ` 7` **body/hook** — #07 The Same Words · 23.88-30.54s (6.66s) · 1.51x · speed  
  _The Hebrew line held before the cross — 'The very same words'._
- ` 8` **body/hook** — #08 Still 'My God' · 30.54-36.88s (6.34s) · 1.30x · speed+trim  
  _The steady, trusting face — 'even forsaken, He still calls God my God'._
- ` 9` **body/hook** — #09 Bearing the Forsaking · 36.88-39.22s (2.34s) · 1.30x · speed+trim  
  _Christ bearing the dark with the lamb and broken chains — 'the sinless Son taking our place, bearing the forsaking'._
- `10` **body/hook** — #10 So You Never Will Be · 39.22-46.68s (7.46s) · 1.30x · speed+trim  
  _The face turning into the first light — 'He was forsaken so that you never will be'._
- `11` **body/hook** — #13 However Far You've Run · 46.68-48.28s (1.60s) · 2.20x · speed+trim  
  _The lone figure on the dark road toward the cross — 'However far you've run'._
- `12` **body/hook** — #14 He Opened It from the Dark · 48.28-49.84s (1.56s) · 1.30x · speed+trim  
  _The nailed hand before the breaking light — 'He opened it from the dark'._
- `13` **hero-tail/hero** — #11 The Way Opened from the Dark · 49.84-51.84s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Self-review panel
- **Editor** — `STRONG` — 13 clips at avg 1.39x — fast, lots of moments; dark cry front, progressive light-turn to the hero break-of-light.
- **Beat-Sync** — `STRONG` — Each clip on its phrase: cry on the open, David on 'forsaken man', ninth-hour cross on 'at the ninth hour', diptych on 'a thousand years later', nailed hand on 'He opened it from the dark'.
- **No-Reuse** — `STRONG` — 13 distinct; hero #11 once at close.
- **Pacing** — `CAUTION` — Brisk (max 2.2x) by design; sacred frames near the close at lower speed.
- **Hero-Continuity** — `STRONG` — Opens on the cry, closes on the cross against the breaking light — lands on the gospel-pivot.
- **Jaded Viewer** — `STRONG` — The cry cold-open grips; the dark-to-light progression gives the landing weight.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->51.84s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #11 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `CONDITIONAL` — avg speed 1.39x, max 2.20x, 12/13 trimmed — brisk; verify it does not strobe.  
  _fix:_ Reduce clip count (lower --clips) so slots breathe.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #11 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — cry -> ninth-hour darkness -> 'still my God' -> bearing -> light-turn carries open->climax->close.
- **AS-G9 Beat Density** — `PASS` — 13 moments · avg slot 3.8s (target 4s) — lively.
