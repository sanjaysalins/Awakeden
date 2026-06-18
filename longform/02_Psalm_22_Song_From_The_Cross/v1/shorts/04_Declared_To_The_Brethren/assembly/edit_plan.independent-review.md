# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
13 body clips spread fast (~every 1.5 beats). Empty tomb opens; risen Christ on 'doesn't end in a grave'; the Reach-of-the-Cross radiance on 'the psalm turns'; risen-Christ-proclaiming on 'I will declare thy name'; among-the-brethren on 'midst of the congregation'; living-face on 'who is that praising voice'; scarred-hands on 'Hebrews word for word'; welcomed-into-family on 'the psalm's turn is Jesus, alive'; invitation-face on 'hear what He calls us'; not-ashamed on 'not ashamed to call them brethren'; brethren-rejoicing on 'Family'; wounded-hand on 'the same Jesus who cried forsaken now lives'; Come-to-Him on 'calling you into that family'. Hero #10 (calling-you-in, risen Christ welcoming) closes.

## Slots
- ` 0` **body/hook** — #01 The Empty Tomb · 0.00-3.38s (3.38s) · 1.49x · speed  
  _Empty tomb — 'it doesn't end in a grave.'_
- ` 1` **body/hook** — #04 The Risen Christ · 3.38-7.72s (4.34s) · 1.16x · speed  
  _Risen Christ — the cry doesn't stay forsaken._
- ` 2` **body/hook** — #02 The Psalm Turns · 7.72-10.14s (2.42s) · 1.30x · speed+trim  
  _The cross radiating glory — 'the psalm turns.'_
- ` 3` **body/hook** — #03 I Will Declare Thy Name · 10.14-16.16s (6.02s) · 0.84x · speed  
  _Risen Christ proclaiming — 'I will declare thy name unto my brethren.'_
- ` 4` **body/hook** — #05 Among the Brethren · 16.16-22.14s (5.98s) · 0.84x · speed  
  _Among the brethren — 'in the midst of the congregation.'_
- ` 5` **body/hook** — #06 The Living Face · 22.14-25.02s (2.88s) · 1.30x · speed+trim  
  _The living face — 'who is that praising voice?'_
- ` 6` **body/hook** — #14 The Scarred Hands in Praise · 25.02-28.15s (3.13s) · 1.30x · speed+trim  
  _The scarred hands — 'Hebrews takes that line, word for word.'_
- ` 7` **body/hook** — #13 Welcomed into the Family · 28.15-33.24s (5.09s) · 0.99x · speed  
  _Welcomed into the family — 'the psalm's turn is Jesus, alive.'_
- ` 8` **body/hook** — #11 The Invitation · 33.24-39.52s (6.28s) · 0.80x · speed  
  _The invitation face — 'hear what He calls us.'_
- ` 9` **body/hook** — #08 Not Ashamed to Call Them Brethren · 39.52-43.68s (4.16s) · 1.21x · speed  
  _Christ embracing — 'not ashamed to call them brethren.'_
- `10` **body/hook** — #12 A Thousand Years Apart · 43.68-47.08s (3.40s) · 1.30x · speed+trim  
  _The brethren rejoicing — 'Family.'_
- `11` **body/hook** — #09 The Wounded Hand on the Shoulder · 47.08-50.63s (3.55s) · 1.30x · speed+trim  
  _The wounded hand — 'the same Jesus who cried forsaken now lives.'_
- `12` **body/hook** — #07 Hebrews Names Him · 50.63-56.31s (5.68s) · 0.89x · speed  
  _Come to Him — 'calling you into that family.'_
- `13` **hero-tail/hero** — #10 Calling You In · 56.31-58.31s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — 13 distinct moments at ~4.3s — punchy, no dead hold; clean risen arc.
- **Beat-Sync** — `STRONG` — each clip under its words; the 2 fresh risen creates land on proclaim/Family beats.
- **No-Reuse** — `STRONG` — 13 distinct body clips; hero once.
- **Pacing** — `STRONG` — avg 1.13x; risen close near full speed.
- **Hero-Continuity** — `STRONG` — empty-tomb hook open; lands on the risen Christ calling-you-in (resurrection gospel-pivot).
- **Jaded Viewer** — `STRONG` — punchy, fresh risen content; minor crop flaws flash by under the pace.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->58.31s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #10 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.13x, max 1.49x, 5 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #10 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `CONDITIONAL` — Gospel-pivot present (lands on Christ). Soft-missing: a cross/passion image (ok if the pivot is resurrection/NT-link).  
  _fix:_ Add a hook-open if available; cross optional when the pivot is resurrection.
- **AS-G8 Beat Continuity** — `PASS` — forsaken->risen->declared-to-brethren->calling-you-in; each clip under its words.
- **AS-G9 Beat Density** — `PASS` — 13 moments · avg slot 4.3s (target 4s) — lively.
