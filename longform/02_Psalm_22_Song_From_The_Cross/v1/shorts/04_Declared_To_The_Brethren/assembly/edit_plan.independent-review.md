# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
The cut opens on the empty tomb under 'stop reading Psalm 22 at the cross' — the visual rebuttal to ending in a grave. The Psalm-scroll and the David-to-Christ diptych carry 'the psalm turns / anguish to praise'; the fingertip-under-Hebrew lands exactly on 'I will declare thy name', and Christ among the gathered on 'in the midst of the congregation'. The living face asks 'who is that voice?', the Greek codex carries 'Hebrews takes that opening line', and the risen Christ standing alive lands 'in the mouth of the risen Christ'; the scarred hands in praise land 'alive on the far side of the cross'. The embrace, the hand-on-shoulder, and the welcomed-family beat the 'not ashamed / brothers / family' run; the inviting face closes the spoken brethren line, and hero #10 (arms opening to the viewer) holds the final 'calling you into that family'.

## Slots
- ` 0` **body/hook** — #01 The Empty Tomb · 0.00-3.38s (3.38s) · 2.20x · speed+trim  
  _Empty tomb = the most arresting hook-open; the visual answer to 'it doesn't end in a grave', pinned to beat 0._
- ` 1` **body/hook** — #02 The Psalm Turns · 3.38-12.22s (8.84s) · 1.14x · speed  
  _The Psalm scroll, lower lines breaking into light, on 'Later, the psalm turns'._
- ` 2` **body/hook** — #12 A Thousand Years Apart · 12.22-16.16s (3.94s) · 1.30x · speed+trim  
  _David-to-risen-Christ diptych across a band of light = 'the same voice moves from anguish to praise' across a thousand years._
- ` 3` **body/hook** — #03 I Will Declare Thy Name · 16.16-18.06s (1.90s) · 1.30x · speed+trim  
  _Fingertip under the warmly lit Hebrew line on the quoted 'I will declare thy name unto my brethren'._
- ` 4` **body/hook** — #05 Among the Brethren · 18.06-22.14s (4.08s) · 1.30x · speed+trim  
  _Risen Christ amid the close-gathered group, speaking the Name, on 'in the midst of the congregation will I praise thee'._
- ` 5` **body/hook** — #06 The Living Face · 22.14-25.02s (2.88s) · 1.30x · speed+trim  
  _Close living face on 'Who is that praising voice?' — the question answered by the face._
- ` 6` **body/hook** — #07 Hebrews Names Him · 25.02-26.96s (1.94s) · 1.30x · speed+trim  
  _Open Greek codex page on 'Hebrews takes that opening line — word for word'._
- ` 7` **body/hook** — #04 The Risen Christ · 26.96-31.55s (4.59s) · 1.30x · speed+trim  
  _Risen Christ standing alive, low angle, on 'puts it in the mouth of the risen Christ'._
- ` 8` **body/hook** — #14 The Scarred Hands in Praise · 31.55-37.04s (5.49s) · 1.30x · speed+trim  
  _Two scarred hands lifted in praise on 'alive on the far side of the cross' — the marks that prove it._
- ` 9` **body/hook** — #08 Not Ashamed to Call Them Brethren · 37.04-43.68s (6.64s) · 1.30x · speed+trim  
  _Christ drawing the kneeling man into embrace on the quoted 'not ashamed to call them brethren'._
- `10` **body/hook** — #09 The Wounded Hand on the Shoulder · 43.68-45.24s (1.56s) · 1.30x · speed+trim  
  _Scarred hand on the man's shoulder on 'brothers' — brotherhood made tangible._
- `11` **body/hook** — #13 Welcomed into the Family · 45.24-47.08s (1.84s) · 1.30x · speed+trim  
  _The gathered family drawing a newcomer in on 'Family'._
- `12` **body/hook** — #11 The Invitation · 47.08-56.31s (9.23s) · 1.09x · speed  
  _Risen face turned warmly to the viewer on 'the risen Christ is not ashamed to call His own brethren'._
- `13` **hero-tail/hero** — #10 Calling You In · 56.31-58.31s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — 13 moments over 58s, time-ordered, with two longer holds to breathe — paced for a Short, no strobe.
- **Beat-Sync** — `STRONG` — Object/echo/action clips all land on their words; the only quoted KJV lines (P06/P07, P16) carry the matching scroll, gathered-brethren, and embrace images.
- **No-Reuse** — `STRONG` — All 13 body clips distinct; hero #10 only at the close.
- **Pacing** — `CAUTION` — 1.34x avg is brisk for Baroque; the open at 2.20x is the fastest — fine since it is the empty-tomb hook, and the sacred close holds at 1.0x.
- **Hero-Continuity** — `CAUTION` — Lands correctly on the risen Christ, but slot 12 (#11 risen face) immediately precedes hero #10 (risen figure) — two Christ frames in a row at the close; distinct framings keep it from reading as a repeat, acceptable for the landing.
- **Jaded Viewer** — `STRONG` — The 'Psalm 22 doesn't end in a grave' hook plus the death->family turn earns the watch.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->58.31s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #10 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `CONDITIONAL` — avg speed 1.34x, max 2.20x, 11/13 trimmed — brisk; verify it does not strobe.  
  _fix:_ Reduce clip count (lower --clips) so slots breathe.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #10 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `CONDITIONAL` — Gospel-pivot present (lands on Christ). Soft-missing: a cross/passion image (ok if the pivot is resurrection/NT-link).  
  _fix:_ Add a hook-open if available; cross optional when the pivot is resurrection.
- **AS-G8 Beat Continuity** — `PASS` — Thread open (empty tomb) -> climax (risen Christ/scarred hands) -> close (calling you in); no clip fights its words.
- **AS-G9 Beat Density** — `PASS` — 13 moments · avg slot 4.3s (target 4s) — lively.
