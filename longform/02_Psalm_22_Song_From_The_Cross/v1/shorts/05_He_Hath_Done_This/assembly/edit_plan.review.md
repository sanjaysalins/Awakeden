# Edit plan — Self-review panel

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Opens on #07 (Christ's bowed head at the moment of death) under 'a psalm's last line and Jesus' last breath... it is done'. #09 (the wide day-is-done) on 'the psalm closes looking ahead to God's saving work'. #11 (the finished-work centre) on 'its final line: that he hath done this. Done.' #08 (the torn veil) on 'as Jesus hung dying, John records: It is finished'. #10 (the hands at rest) on 'different words a thousand years apart — the same note: a finished work'. #12 (nothing left to carry) on 'what's left for you to finish?'. #13 (the open door home) on 'Nothing — only Someone to come home to'. #14 (the One who said it is done) on the closing line. Hero #04 (It Is Finished, the cross) closes.

## Slots
- ` 0` **body/hook** — #07 The Bowed Head · 0.00-4.26s (4.26s) · 1.18x · speed  
  _Christ's bowed head at the last breath = 'a psalm's last line and Jesus' last breath... it is done'._
- ` 1` **body/hook** — #09 The Day Is Done · 4.26-9.54s (5.28s) · 0.95x · speed  
  _the wide day-is-done = 'the psalm closes looking ahead to God's saving work'._
- ` 2` **body/hook** — #11 The Finished Work · 9.54-15.92s (6.38s) · 0.79x · speed  
  _the finished-work theological centre = 'its final line: that he hath done this. Done.'_
- ` 3` **body/hook** — #08 The Torn Veil · 15.92-22.44s (6.52s) · 0.77x · speed  
  _the torn veil at his death = 'as Jesus hung dying, John records: It is finished'._
- ` 4` **body/hook** — #10 Hands at Rest · 22.44-29.24s (6.80s) · 0.74x · speed  
  _the hands at rest = 'different words a thousand years apart — the same note: a finished work'._
- ` 5` **body/hook** — #12 Nothing Left to Carry · 29.24-37.44s (8.20s) · 0.61x · speed  
  _nothing left to carry = 'so what's left for you to finish?'._
- ` 6` **body/hook** — #13 The Open Door Home · 37.44-38.90s (1.46s) · 2.20x · speed+trim  
  _the open door home = 'only Someone to come home to'._
- ` 7` **body/hook** — #14 The One Who Said It Is Done · 38.90-41.91s (3.01s) · 1.30x · speed+trim  
  _the One who said it is done = the closing devotional line._
- ` 8` **hero-tail/hero** — #04 It Is Finished · 41.91-43.91s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Self-review panel
- **Editor** — `STRONG` — Tight 44s cut, 8 clips with internal hard cuts; brisk.
- **Beat-Sync** — `STRONG` — bowed-head->it is done, finished-work->that he hath done this, torn-veil->it is finished, open-door->Someone to come home to.
- **No-Reuse** — `STRONG` — 8 distinct body clips; hero #04 only at close.
- **Pacing** — `STRONG` — Sacred frames near full speed; max 2.20x on a wide.
- **Hero-Continuity** — `CAUTION` — Opens on #07 bowed-head (the hook-open scene was an excluded writing scroll); still lands on the cross hero #04. Acceptable.
- **Jaded Viewer** — `STRONG` — The 'it is finished / it is done' echo gives a strong payoff.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 9 slots tile 0->43.91s contiguously.
- **AS-G2 No Reuse** — `PASS` — 8 distinct body clips; hero #04 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.07x, max 2.20x, 2 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `CONDITIONAL` — Cut opens on #07 'The Bowed Head' (role=pivot), not a hook-open clip.  
  _fix:_ Open on the strongest hook-open scroll-stopper.
- **AS-G7 Gospel Frame** — `CONDITIONAL` — Gospel-pivot present (lands on Christ). Soft-missing: a hook-open clip.  
  _fix:_ Add a hook-open if available; cross optional when the pivot is resurrection.
- **AS-G8 Beat Continuity** — `PASS` — finished-work thread carried open->climax->close.
- **AS-G9 Beat Density** — `CONDITIONAL` — 8 moments · avg slot 5.2s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 11 (pool has 9).
