# Edit plan — Self-review panel

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
The cut opens on the one forsaken man alone, then Abraham under the stars carries 'every nation on earth' and the psalm scroll 'the song throws its arms open'. The cross-over-the-world lands the quoted 'all the ends of the world', the gathered kindreds land 'shall worship', and the tiny Golgotha lands 'one corner of the Roman Empire'. Light-to-the-gentiles carries 'the ends of the earth will turn to God', the empty tomb lands 'the empty tomb', the travellers land 'the gospel went out', and the pilgrim procession lands 'nation after nation'. The lone traveller lands 'wherever you are', the cross over the whole earth lands 'swept the whole earth', and the open road lands 'room for you to turn to Him' — with hero #4, the cross radiating to the horizons, closing the cut.

## Slots
- ` 0` **body/hook** — #01 One Man, Alone · 0.00-3.82s (3.82s) · 1.30x · speed+trim  
  _The lone forsaken man alone = the hook-open, pinned to beat 0 ('one forsaken man dying alone')._
- ` 1` **body/hook** — #07 In Thee All Nations Blessed · 3.82-6.56s (2.74s) · 1.30x · speed+trim  
  _Abraham beneath countless stars on 'ends with every nation on earth' — the ancient promise of the nations._
- ` 2` **body/hook** — #02 The Song Opens Its Arms · 6.56-11.20s (4.64s) · 1.30x · speed+trim  
  _The psalm scroll, light widening outward, on 'the song throws its arms open to every nation'._
- ` 3` **body/hook** — #03 All the Ends of the World · 11.20-13.82s (2.62s) · 1.30x · speed+trim  
  _The cross on its hill against a whole-world horizon on the quoted 'All the ends of the world'._
- ` 4` **body/hook** — #08 Kindreds of the Nations · 13.82-18.60s (4.78s) · 2.10x · speed  
  _The gathered kindreds of many nations on 'all the kindreds of the nations shall worship'._
- ` 5` **body/hook** — #05 One Corner of the Empire · 18.60-21.88s (3.28s) · 2.20x · speed+trim  
  _The tiny Golgotha dwarfed by a vast landscape on 'a man dying in one corner of the Roman Empire'._
- ` 6` **body/hook** — #09 A Light to the Gentiles · 21.88-24.38s (2.50s) · 1.30x · speed+trim  
  _Light reaching a far people on 'the ends of the earth will turn to God'._
- ` 7` **body/hook** — #10 The Empty Tomb · 24.38-30.48s (6.10s) · 1.65x · speed  
  _The open empty tomb on 'and the empty tomb'._
- ` 8` **body/hook** — #06 The Gospel Goes Out · 30.48-32.08s (1.60s) · 1.30x · speed+trim  
  _The travellers and ship setting out on 'the gospel went out'._
- ` 9` **body/hook** — #11 Nation After Nation · 32.08-35.78s (3.70s) · 2.20x · speed+trim  
  _The pilgrim procession of many lands on 'nation after nation have turned to the LORD'._
- `10` **body/hook** — #12 Wherever You Are · 35.78-50.86s (15.08s) · 0.67x · speed  
  _The lone traveller turned toward distant light on 'includes wherever you are'._
- `11` **body/hook** — #14 The Whole Earth at Dawn · 50.86-56.44s (5.58s) · 1.30x · speed+trim  
  _The cross over the whole earth at dawn on 'has swept the whole earth'._
- `12` **body/hook** — #13 Room to Turn · 56.44-59.82s (3.38s) · 2.20x · speed+trim  
  _The open road to the cross on 'still has room for you to turn to Him'._
- `13` **hero-tail/hero** — #04 The Reach of the Cross · 59.82-61.82s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Self-review panel
- **Editor** — `STRONG` — 13 distinct moments over 61.8s, time-ordered; opens on the lone man, closes on the cross radiating to the horizons — the 'one becomes all' arc reads.
- **Beat-Sync** — `STRONG` — Quote lands right (cross+world on 'all the ends of the world', kindreds on 'shall worship'); object/echo clips on their phrases (empty tomb, gospel goes out, Abraham on 'every nation').
- **No-Reuse** — `STRONG` — 13 distinct body clips; hero #04 only at the close.
- **Pacing** — `STRONG` — avg 1.55x brisk but the 61.8s narration gives slots ~4.6s to breathe; hero held full-speed for a reverent landing.
- **Hero-Continuity** — `STRONG` — Opens on the lone forsaken man (scroll-stopper), closes on the cross reaching the ends of the earth — lands on Christ.
- **Jaded Viewer** — `STRONG` — The 'one man's song swept the whole earth' arc plus the lone-to-all bookends earns the watch.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->61.82s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #04 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `CONDITIONAL` — avg speed 1.55x, max 2.20x, 10/13 trimmed — brisk; verify it does not strobe.  
  _fix:_ Reduce clip count (lower --clips) so slots breathe.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #04 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — Thread one->all carried open->proof->close; no clip fights its words.
- **AS-G9 Beat Density** — `CONDITIONAL` — 13 moments · avg slot 4.6s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 15 (pool has 14).
