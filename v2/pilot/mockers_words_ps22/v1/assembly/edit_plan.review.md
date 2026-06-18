# Edit plan — Self-review panel

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Opens on the sneering rulers' faces (#05) under 'the crowd mocking Jesus was reading from a script' (the quarantined shaking-heads hook is replaced by this arresting close). The psalmist (#02) on 'a thousand years before, Psalm 22 recorded how the Messiah would be mocked'. The passers-by wagging heads (#04) on 'the passers-by wagging their heads'; Christ on the cross (#06) on 'He trusted in God'; the jeering crowd framing Christ (#08) on 'unwilling witnesses that this was the One'; Christ holding back his power (#10) on 'He could have come down'; the face bearing scorn (#11) on 'bearing the scorn'; the king they told to come down (#12) on 'they told the King to come down'; the closing call (#13) on 'come to the One who would not come down'. Hero #07 — the King who would not come down — holds the close.

## Slots
- ` 0` **body/hook** — #05 The Rulers Sneer · 0.00-2.66s (2.66s) · 1.30x · speed+trim  
  _smug sneering rulers' faces = the hook 'reading from a script' mockery_
- ` 1` **body/hook** — #02 A Script, A Thousand Years Old · 2.66-6.62s (3.96s) · 1.27x · speed  
  _aged psalmist gazing at the bound figure = 'a thousand years before, Psalm 22'_
- ` 2` **body/hook** — #04 The Passers-By Wag Their Heads · 6.62-23.12s (16.50s) · 0.31x · speed  
  _wide passers-by wagging heads = 'the passers-by wagging their heads'_
- ` 3` **body/hook** — #06 He Trusted In God · 23.12-28.16s (5.04s) · 1.00x · speed  
  _Christ on the cross, head bowed = 'He trusted in God'_
- ` 4` **body/hook** — #08 Unwilling Witnesses · 28.16-40.92s (12.76s) · 0.40x · speed  
  _jeering crowd unknowingly framing the luminous Christ = 'unwilling witnesses'_
- ` 5` **body/hook** — #10 He Could Have Come Down · 40.92-47.48s (6.56s) · 0.77x · speed  
  _Christ dominant, power held back in shadow = 'He could have come down'_
- ` 6` **body/hook** — #11 Bearing The Scorn · 47.48-54.04s (6.56s) · 0.77x · speed  
  _the face bearing scorn in willing endurance = 'bearing the scorn'_
- ` 7` **body/hook** — #12 The King They Told To Come Down · 54.04-61.62s (7.58s) · 0.67x · speed  
  _the King they jeered = 'they told the King to come down'_
- ` 8` **body/hook** — #13 For The Very People Throwing It · 61.62-68.00s (6.38s) · 0.79x · speed  
  _the closing devotional = 'come to the One who would not come down'_
- ` 9` **hero-tail/hero** — #07 The King Who Would Not Come Down · 68.00-70.00s (2.00s) · 1.00x · speed  
  _Hero close — the cut lands on Christ (single appearance, no reuse)._

## Self-review panel
- **Editor** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Beat-Sync** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **No-Reuse** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Pacing** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Hero-Continuity** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)
- **Jaded Viewer** — `STRONG` — all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 10 slots tile 0->70.00s contiguously.
- **AS-G2 No Reuse** — `PASS` — 9 distinct body clips; hero #07 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 0.81x, max 1.30x, 1 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['hook'].
- **AS-G6 Hero Close** — `CONDITIONAL` — Cut opens on #05 'The Rulers Sneer' (role=build), not a hook-open clip.  
  _fix:_ Open on the strongest hook-open scroll-stopper.
- **AS-G7 Gospel Frame** — `CONDITIONAL` — Gospel-pivot present (lands on Christ). Soft-missing: a hook-open clip.  
  _fix:_ Add a hook-open if available; cross optional when the pivot is resurrection.
- **AS-G9 Beat Density** — `CONDITIONAL` — 9 moments · avg slot 7.6s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 17 (pool has 10).
- **AS-G8 Beat Continuity** — `PASS` — thread carried open->climax->close; jigsaw pinned each clip to its phrase by meaning; cut lands on the gospel-pivot.
