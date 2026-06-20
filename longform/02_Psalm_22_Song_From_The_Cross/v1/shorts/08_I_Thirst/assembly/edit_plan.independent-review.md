# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Same meaning-pinned spine, fixing AS-G5: every spoken section now carries a clip. Hook opens on the parched crucified face (#01), then king-at-scroll #02 ('David wrote it') and king-with-distant-cross #07 ('picturing someone else's death'). The David quote lands its objects: #03 potsherd, #04 tongue. The bridge now carries #05 (body sunk in dust) on 'a man sinking into the dust of death', and the jesus 'I thirst' quote section gets #06 (the crucified Christ, the dying word). The gospel turn maps exactly: #08 'made every river', #09 living-water-at-the-well 'offers living water', #10 'hanging there with nothing', then water clips #11 rock / #12 every-one-that-thirsteth / #13 drink-and-never-thirst. Hero #14 (pierced side, water and blood, glory) closes on 'that water is Himself'.

## Slots
- ` 0` **body/hook** — #01 Two Words on a Cross · 0.00-4.38s (4.38s) · 1.15x · speed  
  _hook-open: the parched crucified face under 'two words on a cross: I thirst'_
- ` 1` **body/hook** — #02 The King Who Wrote It · 4.38-9.04s (4.66s) · 2.15x · speed  
  _the king at his scroll under 'Psalm twenty-two. David wrote it'_
- ` 2` **body/hook** — #07 A Thousand Years Apart · 9.04-13.32s (4.28s) · 2.35x · speed  
  _king-at-scroll with the distant cross under 'picturing someone else's death'_
- ` 3` **body/david** — #03 Dried Like a Potsherd · 13.32-18.04s (4.72s) · 1.07x · speed  
  _the potsherd object exactly under 'My strength is dried up like a potsherd'_
- ` 4` **body/david** — #04 The Tongue Cleaveth · 18.04-20.76s (2.72s) · 1.85x · speed  
  _the dying parched face under 'my tongue cleaveth to my jaws'_
- ` 5` **body/bridge** — #05 The Dust of Death · 20.76-30.42s (9.66s) · 0.52x · speed  
  _the body half-sunk in dust under the bridge line 'a man sinking into the dust of death' (covers the bridge section)_
- ` 6` **body/quote** — #06 The Cry Recorded · 30.42-38.48s (8.06s) · 0.63x · speed  
  _the crucified Christ, cracked lips around the dying word, under the jesus quote 'I thirst' / 'that cry' (covers the quote section)_
- ` 7` **body/landing** — #08 Who Made Every River · 38.48-46.94s (8.46s) · 0.60x · speed  
  _the crucified Christ with the waters faint in shadow under 'the One who made every river and spring'_
- ` 8` **body/landing** — #09 Living Water Offered · 46.94-50.06s (3.12s) · 1.62x · speed  
  _Jesus at the well offering the waterpot under 'who offers the world living water'_
- ` 9` **body/landing** — #10 Hanging There With Nothing · 50.06-51.24s (1.18s) · 3.00x · speed+trim  
  _the full crucified Christ, empty open hands, under 'hanging there with nothing'_
- `10` **body/landing** — #11 Water from the Rock · 51.24-57.94s (6.70s) · 0.75x · speed  
  _Moses' struck rock pouring water under 'He went dry so that you could drink'_
- `11` **body/landing** — #12 Come, Every One That Thirsteth · 57.94-60.48s (2.54s) · 1.99x · speed  
  _the opened spring with thirsting figures under 'The God who made every ocean cried out in thirst' — the invitation to all who thirst_
- `12` **body/landing** — #13 Drink and Never Thirst · 60.48-68.94s (8.46s) · 0.60x · speed  
  _the kneeling figure drinking in relief under 'so He could hand you the one water that never fails'_
- `13` **hero-tail/hero** — #14 That Water Is Himself · 68.94-70.94s (2.00s) · 2.52x · speed  
  _Hero close — the whole hero clip sped to fit, landing on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — Open->climax->close reads clean; 13 distinct moments, no strobe, no dead holds with speed-to-fit.
- **Beat-Sync** — `STRONG` — Object beats land exactly (potsherd/tongue/dust/every-river/living-water/hanging); the dying cry plays the crucified-Christ image.
- **No-Reuse** — `STRONG` — Each clip once; hero #14 only at the close.
- **Pacing** — `STRONG` — Crucifixion/landing clips near full speed; only a short symbolic plate hits 3.0x; reverent.
- **Hero-Continuity** — `STRONG` — Arresting parched-face hook open; lands on the pierced-side water-and-blood Christ — the gospel pivot.
- **Jaded Viewer** — `CAUTION` — Would stop; only seam is two king-at-scroll compositions, but spaced and distinct in meaning.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->70.94s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #14 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.41x, max 3.00x, 1 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['bridge', 'david', 'hook', 'landing', 'quote'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #14 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — thread carried open->climax->close; no clip fights its words; close on the gospel-pivot.
- **AS-G9 Beat Density** — `CONDITIONAL` — 13 moments · avg slot 5.3s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 18 (pool has 14).
