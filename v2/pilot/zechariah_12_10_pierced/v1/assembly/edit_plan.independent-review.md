# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
All 15 clips. Hook on the spear/wounded body (#01 poured-out) and the pierced side (#02). The LORD's 'look upon me whom they have pierced' rides the pierced/cross frames (#03 face, #06 reach-of-the-cross, #08 they-look-and-mourn, #07 hung). 'The pierced man is God Himself / God's own Son' on #14 crushed-in-your-place + #04 wounded-one. John's witness + 'look on him whom they pierced' on #10 the-cry + #12 ninth-hour. The mercy lands: grace poured out (#09 spirit-of-grace), forgiven (#13 it-is-finished), God pierced for you (#11 come-to-him), and the CTA 'Look at Him and live' (#15 room-to-turn dawn cross). Hero #05 (the pierced crucified Christ) closes as the gospel-pivot.

## Slots
- ` 0` **body/hook** — #01 The Spear · 0.00-3.06s (3.06s) · 1.65x · speed  
  _poured-out wounded body — 'drove a spear into His side'_
- ` 1` **body/hook** — #02 The Pierced Side · 3.06-8.16s (5.10s) · 0.99x · speed  
  _the pierced side, blood and water_
- ` 2` **body/hook** — #03 God's Staggering Word · 8.16-13.80s (5.64s) · 0.89x · speed  
  _Christ's face — 'look upon me'_
- ` 3` **body/bridge** — #06 Whom They Pierced · 13.80-20.36s (6.56s) · 0.77x · speed  
  _the reach of the cross — 'whom they have pierced'_
- ` 4` **body/bridge** — #08 They Look And Mourn · 20.36-21.98s (1.62s) · 3.00x · speed+trim  
  _they look and mourn — 'they shall mourn for him'_
- ` 5` **body/bridge** — #07 John Saw It · 21.98-28.06s (6.08s) · 1.65x · speed  
  _hung by the arms — 'they pierced Me'_
- ` 6` **body/bridge** — #14 Crushed In Your Place · 28.06-33.14s (5.08s) · 0.99x · speed  
  _crushed-in-your-place — 'the pierced man is God Himself'_
- ` 7` **body/john** — #04 The Wounded One · 33.14-35.34s (2.20s) · 2.29x · speed  
  _the wounded One — 'God's own Son'_
- ` 8` **body/landing** — #10 Look At Him · 35.34-38.04s (2.70s) · 1.87x · speed  
  _the cry — 'John watched the spear go in'_
- ` 9` **body/landing** — #12 The Ninth Hour · 38.04-43.04s (5.00s) · 1.01x · speed  
  _the cross — 'look on him whom they pierced'_
- `10` **body/landing** — #09 The Spirit Of Grace · 43.04-47.30s (4.26s) · 1.18x · speed  
  _the spirit of grace poured out_
- `11` **body/landing** — #13 It Is Finished · 47.30-53.78s (6.48s) · 0.78x · speed  
  _it is finished — 'they are forgiven'_
- `12` **body/landing** — #11 And Live · 53.78-60.24s (6.46s) · 0.78x · speed  
  _come to him — 'He was God, pierced for you'_
- `13` **body/landing** — #15 Room To Turn · 60.24-65.04s (4.80s) · 1.05x · speed  
  _the cross at dawn, a path — 'Look at Him, and live'_
- `14` **hero-tail/hero** — #05 The Cross · 65.04-67.04s (2.00s) · 2.52x · speed  
  _Hero close — the whole hero clip sped to fit, landing on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — Punchy, longest hold 6.6s; pierced-theme flows to the grace landing.
- **Beat-Sync** — `STRONG` — Clips under their words; pierced frames on the piercing lines, grace on the mercy, CTA on look-and-live.
- **No-Reuse** — `STRONG` — 14 distinct; hero #05 (pierced Christ) once at close.
- **Pacing** — `STRONG` — Sacred near full speed; narrator 1.075x; lively.
- **Hero-Continuity** — `STRONG` — Hook-open (#01) -> pierced-Christ gospel-pivot #05 close.
- **Jaded Viewer** — `STRONG` — The pierced One they look upon; lands on Christ.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 15 slots tile 0->67.04s contiguously.
- **AS-G2 No Reuse** — `PASS` — 14 distinct body clips; hero #05 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.35x, max 3.00x, 1 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['bridge', 'hook', 'john', 'landing'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #05 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — thread carried; clips fit words.
- **AS-G9 Beat Density** — `CONDITIONAL` — 14 moments · avg slot 4.6s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 17 (pool has 15).
