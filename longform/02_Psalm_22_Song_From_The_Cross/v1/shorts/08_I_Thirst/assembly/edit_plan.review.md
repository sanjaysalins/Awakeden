# Edit plan — Self-review panel

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
The parched crucified face (#01) opens cold on 'gasped two words on a cross: I thirst'. The body-failure quote gets its literal images: the clay potsherd (#03) on 'dried up like a potsherd', the dying mouth (#04) on 'my tongue cleaveth to my jaws', the body half-sunk in dust (#05) on 'the dust of death'. The crucified Christ with cracked lips (#06) lands on John's 'I thirst'. The turn: Christ who made the waters (#08) on 'the One who made every river and spring', Jesus offering at the well (#09) on 'who offers the world living water', the empty-handed cross (#10) on 'hanging there with nothing'. The living-water finale: the kneeling drinker (#13) on 'drink and never thirst again', Moses' struck rock (#11) on 'the God who made every ocean cried out in thirst', the never-failing spring (#12) on 'the one water that never fails'. Hero #14 'That Water Is Himself' closes on 'And that water is Himself'.

## Slots
- ` 0` **body/hook** — #01 Two Words on a Cross · 0.00-4.38s (4.38s) · 1.15x · speed  
  _parched crucified face — 'gasped two words on a cross: I thirst'._
- ` 1` **body/hook** — #03 Dried Like a Potsherd · 4.38-18.04s (13.66s) · 0.37x · speed  
  _broken clay potsherd in cracked dust — 'My strength is dried up like a potsherd'._
- ` 2` **body/hook** — #04 The Tongue Cleaveth · 18.04-20.76s (2.72s) · 1.85x · speed  
  _dying man's face, lips cracked — 'my tongue cleaveth to my jaws'._
- ` 3` **body/hook** — #05 The Dust of Death · 20.76-24.16s (3.40s) · 1.48x · speed  
  _body half-sunk into pale dust — 'thou hast brought me into the dust of death'._
- ` 4` **body/hook** — #06 The Cry Recorded · 24.16-33.72s (9.56s) · 0.53x · speed  
  _crucified Christ, cracked lips parted — 'Then John records the dying Jesus' cry: I thirst'._
- ` 5` **body/hook** — #08 Who Made Every River · 33.72-46.94s (13.22s) · 0.38x · speed  
  _Christ dominant, waters faint in shadow — 'the One who made every river and spring'._
- ` 6` **body/hook** — #09 Living Water Offered · 46.94-50.06s (3.12s) · 1.30x · speed+trim  
  _Jesus at the well offering — 'who offers the world living water'._
- ` 7` **body/hook** — #10 Hanging There With Nothing · 50.06-51.24s (1.18s) · 1.30x · speed+trim  
  _full crucified Christ, hands empty — 'hanging there with nothing'._
- ` 8` **body/hook** — #13 Drink and Never Thirst · 51.24-57.94s (6.70s) · 0.75x · speed  
  _kneeling figure drinking at a spring — 'drink and never thirst again'._
- ` 9` **body/hook** — #11 Water from the Rock · 57.94-60.48s (2.54s) · 1.30x · speed+trim  
  _Moses' struck rock pouring water — 'the God who made every ocean cried out in thirst'._
- `10` **body/hook** — #12 Come, Every One That Thirsteth · 60.48-65.06s (4.58s) · 1.10x · speed  
  _an opened never-failing spring — 'the one water that never fails'._
- `11` **hero-tail/hero** — #14 That Water Is Himself · 65.06-67.06s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Self-review panel
- **Editor** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Beat-Sync** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **No-Reuse** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Pacing** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Hero-Continuity** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Jaded Viewer** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 12 slots tile 0->67.06s contiguously.
- **AS-G2 No Reuse** — `PASS` — 11 distinct body clips; hero #14 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.05x, max 1.85x, 3 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #14 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G9 Beat Density** — `CONDITIONAL` — 11 moments · avg slot 5.9s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 17 (pool has 12).
- **AS-G8 Beat Continuity** — `PASS` — thread carried open->climax->close; jigsaw pinned each clip to its phrase by meaning; cut lands on the gospel-pivot.
