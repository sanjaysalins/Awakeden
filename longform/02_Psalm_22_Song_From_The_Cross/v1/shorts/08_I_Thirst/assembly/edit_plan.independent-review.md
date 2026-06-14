# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Hook #01 parched crucified face. David/Psalm-22 -> #02. Three named images: potsherd -> #03, tongue cleaveth -> #04, dust of death -> #05. John records the cry -> #06; a thousand years before -> #07. Conviction: #08 (Maker of every river), #09 (living water offered), #10 (hanging with nothing). Landing: #13 (drink and never thirst), #12 (come every one that thirsteth), #11 (the Rock = never-failing water), hero #14 'that water is Himself'.

## Slots
- ` 0` **body/hook** — #01 Two Words on a Cross · 0.00-4.38s (4.38s) · 1.30x · speed+trim  
  _Two Words on a Cross — hook._
- ` 1` **body/hook** — #02 The King Who Wrote It · 4.38-9.04s (4.66s) · 2.15x · speed  
  _The King Who Wrote It — 'Psalm twenty-two'._
- ` 2` **body/hook** — #03 Dried Like a Potsherd · 9.04-18.04s (9.00s) · 1.12x · speed  
  _Dried Like a Potsherd — 'dried up like a potsherd'._
- ` 3` **body/hook** — #04 The Tongue Cleaveth · 18.04-20.76s (2.72s) · 2.20x · speed+trim  
  _The Tongue Cleaveth — 'my tongue cleaveth to my jaws'._
- ` 4` **body/hook** — #05 The Dust of Death · 20.76-24.16s (3.40s) · 2.20x · speed+trim  
  _The Dust of Death — 'the dust of death'._
- ` 5` **body/hook** — #06 The Cry Recorded · 24.16-33.72s (9.56s) · 1.05x · speed  
  _The Cry Recorded — 'John records the dying Jesus' cry'._
- ` 6` **body/hook** — #07 A Thousand Years Apart · 33.72-38.48s (4.76s) · 1.30x · speed+trim  
  _A Thousand Years Apart — 'a thousand years before He felt it'._
- ` 7` **body/hook** — #08 Who Made Every River · 38.48-46.94s (8.46s) · 1.19x · speed  
  _Who Made Every River — 'the One who made every river and spring'._
- ` 8` **body/hook** — #09 Living Water Offered · 46.94-50.06s (3.12s) · 1.30x · speed+trim  
  _Living Water Offered — 'who offers the world living water'._
- ` 9` **body/hook** — #10 Hanging There With Nothing · 50.06-51.24s (1.18s) · 1.30x · speed+trim  
  _Hanging There With Nothing — 'hanging there with nothing'._
- `10` **body/hook** — #13 Drink and Never Thirst · 51.24-57.94s (6.70s) · 1.50x · speed  
  _Drink and Never Thirst — 'drink and never thirst again'._
- `11` **body/hook** — #12 Come, Every One That Thirsteth · 57.94-60.48s (2.54s) · 1.30x · speed+trim  
  _Come, Every One That Thirsteth — behind 'cried out in thirst'._
- `12` **body/hook** — #11 Water from the Rock · 60.48-65.06s (4.58s) · 1.30x · speed+trim  
  _Water from the Rock — 'the one water that never fails' (1 Cor 10:4)._
- `13` **hero-tail/hero** — #14 That Water Is Himself · 65.06-67.06s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — Dense 13-clip gated crop-cut body, hero held at close.
- **Beat-Sync** — `STRONG` — Verbatim spans on their literal images; thousand-years on #07.
- **No-Reuse** — `STRONG` — 13 distinct; living-water hero #14 only at close.
- **Pacing** — `CAUTION` — Sub-1s verse beats fast; hero near full speed.
- **Hero-Continuity** — `STRONG` — Hook-open + clean hero #14 close.
- **Jaded Viewer** — `CAUTION` — #11 typological pin; NT-named (1 Cor 10:4) holds.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->67.06s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #14 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `CONDITIONAL` — avg speed 1.48x, max 2.20x, 8/13 trimmed — brisk; verify it does not strobe.  
  _fix:_ Reduce clip count (lower --clips) so slots breathe.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #14 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — Thirst->cross->living-water; close on Christ.
- **AS-G9 Beat Density** — `CONDITIONAL` — 13 moments · avg slot 5.0s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 17 (pool has 14).
