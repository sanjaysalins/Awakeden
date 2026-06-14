# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Hook #01 the out-of-joint crucified body. David/Psalm-22 -> #02. Quoted spans on their images: 'poured out like water' -> #03, 'hangs when suspended by the arms' -> #07, 'I may tell all my bones' -> #05, 'they look and stare upon me' -> #06, onlookers staring -> #08, 'bears the marks of one' -> #11. Centuries-early thread -> #09. Landing #13 -> #10 -> #12 -> #14, hero #04 'crushed in your place' closes.

## Slots
- ` 0` **body/hook** — #01 Out of Joint · 0.00-3.28s (3.28s) · 1.30x · speed+trim  
  _Out of Joint — hook-open crucified body._
- ` 1` **body/hook** — #02 The King Who Wrote It · 3.28-8.76s (5.48s) · 1.83x · speed  
  _The King Who Wrote It — David/scroll, Psalm 22 author._
- ` 2` **body/hook** — #03 Poured Out Like Water · 8.76-18.50s (9.74s) · 1.03x · speed  
  _Poured Out Like Water — 'I am poured out like water'._
- ` 3` **body/hook** — #07 Hung by the Arms · 18.50-27.40s (8.90s) · 1.13x · speed  
  _Hung by the Arms — 'hangs when suspended by the arms'._
- ` 4` **body/hook** — #05 I May Tell All My Bones · 27.40-29.68s (2.28s) · 1.30x · speed+trim  
  _I May Tell All My Bones — 'I may tell all my bones'._
- ` 5` **body/hook** — #06 They Look and Stare · 29.68-32.24s (2.56s) · 1.30x · speed+trim  
  _They Look and Stare — 'they look and stare upon me'._
- ` 6` **body/hook** — #08 Whom They Pierced · 32.24-38.62s (6.38s) · 1.30x · speed+trim  
  _Whom They Pierced — 'onlookers stood and stared at him'._
- ` 7` **body/hook** — #09 A Thousand Years Apart · 38.62-40.76s (2.14s) · 1.30x · speed+trim  
  _A Thousand Years Apart — 'David never saw a crucifixion'._
- ` 8` **body/hook** — #11 The Marks of One · 40.76-46.24s (5.48s) · 1.30x · speed+trim  
  _The Marks of One — 'bears the marks of one'._
- ` 9` **body/hook** — #13 To Bring You Home · 46.24-51.20s (4.96s) · 2.02x · speed  
  _To Bring You Home — 'to bring you home'._
- `10` **body/hook** — #10 Wounded for Us · 51.20-52.58s (1.38s) · 1.30x · speed+trim  
  _Wounded for Us — 'every wrenched joint'._
- `11` **body/hook** — #12 Crushed So Another Goes Free · 52.58-53.50s (0.92s) · 1.30x · speed+trim  
  _Crushed So Another Goes Free — gospel turn into the close._
- `12` **body/hook** — #14 Come to Him · 53.50-58.07s (4.57s) · 1.30x · speed+trim  
  _Come to Him — gospel light under 'none of it was chance'._
- `13` **hero-tail/hero** — #04 Crushed in Your Place · 58.07-60.07s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — Dense 13-clip body, hero held at close; gated crop-cuts.
- **Beat-Sync** — `STRONG` — Verbatim spans on their literal images; thread on #09/#02.
- **No-Reuse** — `STRONG` — 13 distinct; Christ hero #04 only at close.
- **Pacing** — `CAUTION` — Sub-1s landing beats fast; hero near full speed.
- **Hero-Continuity** — `STRONG` — Hook-open + clean hero #04 close.
- **Jaded Viewer** — `CAUTION` — #12 loose pin; passes as transition.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->60.07s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #04 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `CONDITIONAL` — avg speed 1.36x, max 2.02x, 9/13 trimmed — brisk; verify it does not strobe.  
  _fix:_ Reduce clip count (lower --clips) so slots breathe.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #04 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — Thread carried; close on the cross.
- **AS-G9 Beat Density** — `PASS` — 13 moments · avg slot 4.5s (target 4s) — lively.
