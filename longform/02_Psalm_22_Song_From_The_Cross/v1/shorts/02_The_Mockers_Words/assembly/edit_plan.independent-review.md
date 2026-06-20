# Edit plan — Independent red-team audit

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
Hook opens on the mockers shaking their heads (#01). David recording the taunt (#02) on 'David, describing a mocked and dying man'. The Ps 22 quote takes the mocking crowd 'let him deliver him' (#03). The fulfilment bridge: the crowd at the cross (#04) on 'Matthew records both', the passers-by wagging (#06) on 'wagging their heads', the religious leaders pointing (#07) on 'the religious leaders jeering'. The live mocker taunt 'He trusted in God; let him deliver him now' takes the leaders jeering (#05). The landing: the silent suffering king enduring it (#13) on 'flung at Him by people who never saw', the twelve legions restrained (#09) on 'not because He lacked power', He-had-every-power with the angels (#08) on 'He had every power', looking down in love (#10) on 'to deliver you', the hand that would not pull free (#14) on 'could have come down in an instant'. Hero #11 (He chose to stay) closes on 'with you in view'.

## Slots
- ` 0` **body/hook** — #01 The Shaking Heads · 0.00-3.12s (3.12s) · 1.62x · speed  
  _hook-open: the crowd shaking their heads, under 'they shook their heads and sneered'_
- ` 1` **body/hook** — #02 David Records the Taunt · 3.12-10.82s (7.70s) · 0.65x · speed  
  _David recording the tormentors' words, under 'David, describing a mocked and dying man'_
- ` 2` **body/david** — #03 Let Him Deliver Him · 10.82-14.70s (3.88s) · 1.30x · speed  
  _the mocking crowd at the cross, under the Ps 22 quote 'let him deliver him'_
- ` 3` **body/bridge** — #04 The Crowd at the Cross · 14.70-24.16s (9.46s) · 0.53x · speed  
  _the crowd gathered at the cross, under 'Matthew records both'_
- ` 4` **body/bridge** — #06 They Shoot Out the Lip · 24.16-25.98s (1.82s) · 2.77x · speed  
  _the passers-by jeering, under 'the passers-by wagging their heads'_
- ` 5` **body/bridge** — #07 The Religious Leaders Sneer · 25.98-28.38s (2.40s) · 2.10x · speed  
  _the religious leaders pointing and sneering, under 'the religious leaders jeering'_
- ` 6` **body/mocker** — #05 The Religious Leaders Jeer · 28.38-29.96s (1.58s) · 3.19x · speed  
  _the religious leaders' live taunt, under 'He trusted in God; let him deliver him now'_
- ` 7` **body/landing** — #13 The Mockers and the Silent King · 29.96-38.04s (8.08s) · 0.62x · speed  
  _the silent suffering king enduring the scorn, under 'flung at Him by people who never saw'_
- ` 8` **body/landing** — #09 Twelve Legions Restrained · 38.04-45.32s (7.28s) · 0.69x · speed  
  _the twelve legions restrained, under 'not because Jesus lacked the power to come down'_
- ` 9` **body/landing** — #08 He Had Every Power · 45.32-47.06s (1.74s) · 2.90x · speed  
  _the crucified Christ in dignity with the angels he could have called, under 'He had every power'_
- `10` **body/landing** — #10 Looking Down in Love · 47.06-50.82s (3.76s) · 1.34x · speed  
  _Christ looking down in love, under 'staying was the only way to deliver you'_
- `11` **body/landing** — #14 The Hand That Would Not Pull Free · 50.82-63.02s (12.20s) · 0.41x · speed  
  _the hand that would not pull free of the nail, under 'He could have come down in an instant'_
- `12` **hero-tail/hero** — #11 He Chose to Stay · 63.02-65.02s (2.00s) · 2.52x · speed  
  _Hero close — the whole hero clip sped to fit, landing on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `STRONG` — 12 distinct moments ~5s/slot — punchy, clean open->climax->close.
- **Beat-Sync** — `STRONG` — shaking-heads/let-him-deliver/wagging/leaders-jeer/He-had-every-power all land under their words.
- **No-Reuse** — `STRONG` — 12 distinct; hero only at close.
- **Pacing** — `STRONG` — sacred clips near full speed; one short mocker plate at 3.19x; reverent.
- **Hero-Continuity** — `STRONG` — shaking-heads hook open; lands on He-chose-to-stay.
- **Jaded Viewer** — `STRONG` — would stop; mockers drama + multi-voice taunt.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 13 slots tile 0->65.02s contiguously.
- **AS-G2 No Reuse** — `PASS` — 12 distinct body clips; hero #11 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.51x, max 3.19x, 0 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['bridge', 'david', 'hook', 'landing', 'mocker'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #11 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G8 Beat Continuity** — `PASS` — mockers-taunt thread carried open->climax->close; close on the chose-to-stay gospel pivot.
- **AS-G9 Beat Density** — `CONDITIONAL` — 12 moments · avg slot 5.3s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 16 (pool has 14).
