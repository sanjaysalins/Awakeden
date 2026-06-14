# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Pinned by meaning in time order, matching the prior locked cut: #01 the psalm's-last-line/last-breath hook; #09 'it is done'; #02 'accomplished, told to a people not yet born'; #03 'that he hath done this'; #10 'Done.'; #05 'John records His final word'; #07 'It is finished'; #11 'Different words, different tongues'; #06 'a thousand years apart'; #08 'a finished work'; #12 'what's left for you to finish?'; #13 'Someone to come home to'; #14 'the One who said it is done'. Hero #04 (the finished cross) closes.

## Slots
- ` 0` **body/hook** — #01 The Psalm's Last Line · 0.00-4.26s (4.26s) · 2.20x · speed+trim  
  _psalm's last line + Jesus' last breath — the hook._
- ` 1` **body/hook** — #09 The Day Is Done · 4.26-7.74s (3.48s) · 2.20x · speed+trim  
  _'it is done'._
- ` 2` **body/hook** — #02 A People Not Yet Born · 7.74-15.02s (7.28s) · 1.30x · speed+trim  
  _'accomplished, told to a people not yet born'._
- ` 3` **body/hook** — #03 The Fingertip on the Final Word · 15.02-19.10s (4.08s) · 1.30x · speed+trim  
  _'that he hath done this'._
- ` 4` **body/hook** — #10 Hands at Rest · 19.10-20.08s (0.98s) · 1.30x · speed+trim  
  _'Done.'_
- ` 5` **body/hook** — #05 The Greek Word · 20.08-24.58s (4.50s) · 1.30x · speed+trim  
  _'John records His final word'._
- ` 6` **body/hook** — #07 The Bowed Head · 24.58-26.68s (2.10s) · 1.30x · speed+trim  
  _'It is finished'._
- ` 7` **body/hook** — #11 The Finished Work · 26.68-29.24s (2.56s) · 1.30x · speed+trim  
  _'Different words, in different tongues'._
- ` 8` **body/hook** — #06 A Thousand Years Apart · 29.24-31.00s (1.76s) · 1.30x · speed+trim  
  _'a thousand years apart'._
- ` 9` **body/hook** — #08 The Torn Veil · 31.00-34.58s (3.58s) · 1.30x · speed+trim  
  _'a finished work'._
- `10` **body/hook** — #12 Nothing Left to Carry · 34.58-37.44s (2.86s) · 2.20x · speed+trim  
  _'what's left for you to finish?'_
- `11` **body/hook** — #13 The Open Door Home · 37.44-38.81s (1.37s) · 2.20x · speed+trim  
  _'Someone to come home to'._
- `12` **body/hook** — #14 The One Who Said It Is Done · 38.81-41.91s (3.11s) · 1.30x · speed+trim  
  _'the One who said it is done'._
- `13` **hero-tail/hero** — #04 It Is Finished · 41.91-43.91s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — Dense 13-clip gated crop-cut body; hero #04 held close.
- **Beat-Sync** — `STRONG` — Exact-phrase pins throughout.
- **No-Reuse** — `STRONG` — 13 distinct; hero only at close.
- **Pacing** — `STRONG` — Sacred close near full speed.
- **Hero-Continuity** — `STRONG` — Hook-open + hero #04 close.
- **Jaded Viewer** — `STRONG` — Coherent, tight.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->43.91s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #04 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `CONDITIONAL` — avg speed 1.58x, max 2.20x, 13/13 trimmed — brisk; verify it does not strobe.  
  _fix:_ Reduce clip count (lower --clips) so slots breathe.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #04 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — Thread carried; close on Christ.
- **AS-G9 Beat Density** — `PASS` — 13 moments · avg slot 3.2s (target 4s) — lively.
