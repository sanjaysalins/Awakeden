# Edit plan — Self-review panel

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Opens on the spear entering the side (#01) under the hook. The pierced side (#02) on 'whom they have pierced'. The wounded One (#04) on 'God says they pierced Me'. The crowd looking and mourning (#08) on 'John watched... they shall look on him whom they pierced'. The shaft of grace over the bowed mourners (#09) on 'grace poured out... when they finally look'. The closing 'and live' (#11) on 'Look at Him — and live'. Hero #05 — the cross — holds the close. A thin 7-clip pilot, so spread wide to soften the slow holds.

## Slots
- ` 0` **body/hook** — #01 The Spear · 0.00-3.04s (3.04s) · 1.30x · speed+trim  
  _the spear entering the side = the hook 'a soldier drove a spear into His side'_
- ` 1` **body/hook** — #02 The Pierced Side · 3.04-20.56s (17.52s) · 0.29x · speed  
  _the pierced side close = 'whom they have pierced'_
- ` 2` **body/hook** — #04 The Wounded One · 20.56-29.24s (8.68s) · 0.58x · speed  
  _the wounded One = 'God says they pierced Me'_
- ` 3` **body/hook** — #08 They Look And Mourn · 29.24-45.72s (16.48s) · 0.31x · speed  
  _the crowd looking up and mourning = 'they shall look on him whom they pierced'_
- ` 4` **body/hook** — #09 The Spirit Of Grace · 45.72-55.14s (9.42s) · 0.54x · speed  
  _the shaft of grace over bowed mourners = 'grace poured out... when they finally look'_
- ` 5` **body/hook** — #11 And Live · 55.14-68.01s (12.87s) · 0.39x · speed  
  _the closing devotional = 'Look at Him — and live'_
- ` 6` **hero-tail/hero** — #05 The Cross · 68.01-70.01s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Self-review panel
- **Editor** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Beat-Sync** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **No-Reuse** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Pacing** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Hero-Continuity** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Jaded Viewer** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 7 slots tile 0->70.01s contiguously.
- **AS-G2 No Reuse** — `PASS` — 6 distinct body clips; hero #05 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 0.57x, max 1.30x, 1 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #05 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G9 Beat Density** — `CONDITIONAL` — 6 moments · avg slot 11.3s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 18 (pool has 7).
- **AS-G8 Beat Continuity** — `PASS` — thread carried open->climax->close; jigsaw pinned each clip to its phrase by meaning; cut lands on the gospel-pivot.
