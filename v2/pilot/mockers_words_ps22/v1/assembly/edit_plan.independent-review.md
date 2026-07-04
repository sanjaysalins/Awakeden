# Edit plan — Independent red-team audit

**Verdict:** `REVISE`  ·  **Failed gates:** 0

## How the clips map to the words
The cut opens on the jeering faces under 'The crowd mocking Jesus... was reading from a script', then the psalmist seeing the far-off figure under 'A thousand years before'. David's quote plays over the mocking gesture itself (#03 shoot-out-the-lip), and Matthew's fulfillment gets its two literal pins: passers-by wagging heads (#04) and the sneering rulers (#05), with the crucified 'He Trusted In God' (#06) under the mocker's verse. 'Reciting prophecy — unwilling witnesses' carries the crowd-backs-before-the-luminous-Christ (#08); the second taunt gets the open-mouthed jeerer (#09). The landing walks restraint to mercy: 'He could have come down' (#10), 'bearing the scorn' (#11), mercy on the upturned faces 'for the very people throwing it' (#13), the sovereign low-angle King under 'They told the King to come down — and He never did' (#07), and Christ's face looking down in love under 'theirs, and ours'. The hero close is #14 — the cross against widening gold dawn — held under 'Turn, and come to the One who would not come down', a stronger on-thread close than the #07 preference because it IS the invitation image; #07 serves the cut better pinned to its own line at P31.

## Slots
- ` 0` **body/hook** — #01 The Shaking Heads · 0.00-2.48s (2.48s) · 2.03x · speed  
  _Jeering cluster of faces at the upright — the mocking crowd of the hook line._
- ` 1` **body/hook** — #02 A Script, A Thousand Years Old · 2.48-5.96s (3.48s) · 1.45x · speed  
  _The psalmist gazing at a dim far-off bound figure — 'A thousand years before, Psalm twenty-two recorded'._
- ` 2` **body/david** — #03 They Shoot Out The Lip · 5.96-11.60s (5.64s) · 0.89x · speed  
  _The shot-out lip and shaken head filling frame — Ps 22:7's own gesture under David's words._
- ` 3` **body/bridge** — #04 The Passers-By Wag Their Heads · 11.60-21.10s (9.50s) · 0.53x · speed  
  _Passers-by wagging heads at the cross — Matthew 27:39 verbatim image under its phrase._
- ` 4` **body/bridge** — #05 The Rulers Sneer · 21.10-23.70s (2.60s) · 1.94x · speed  
  _The rulers' smug contempt — 'the rulers sneering nearly line for line'._
- ` 5` **body/mocker** — #06 He Trusted In God · 23.70-25.66s (1.96s) · 2.57x · speed  
  _The crucified Christ under darkened noon — on-screen while the mocker speaks 'He trusted in God'._
- ` 6` **body/bridge** — #08 Unwilling Witnesses · 25.66-36.28s (10.62s) · 0.47x · speed  
  _The crowd's dark backs before the luminous Christ — 'reciting prophecy — unwilling witnesses that this was the One'._
- ` 7` **body/mocker** — #09 If Thou Be The Son Of God · 36.28-43.16s (6.88s) · 0.73x · speed  
  _The open-mouthed jeerer beneath the looming cross — the 'come down from the cross' taunt._
- ` 8` **body/landing** — #10 He Could Have Come Down · 43.16-47.86s (4.70s) · 1.07x · speed  
  _Calm unbroken Christ with faint restrained power in the shadows — 'But He could have come down'._
- ` 9` **body/landing** — #11 Bearing The Scorn · 47.86-53.74s (5.88s) · 0.86x · speed  
  _The willing-endurance face, jaw set — 'bearing the scorn He could have silenced'._
- `10` **body/landing** — #13 For The Very People Throwing It · 53.74-56.16s (2.42s) · 2.08x · speed  
  _Christ looking down in mercy on upturned scornful faces, one softening — 'for the very people throwing it'._
- `11` **body/landing** — #07 The King Who Would Not Come Down · 56.16-61.48s (5.32s) · 0.95x · speed  
  _The low-angle sovereign King in stillness — 'They told the King to come down — and He never did'._
- `12` **body/landing** — #18 Looking Down In Love · 61.48-76.02s (14.54s) · 0.35x · speed  
  _The face looking down in love — 'He stayed under scorn — theirs, and ours'._
- `13` **hero-tail/hero** — #14 Come To The One Who Would Not Come Down · 76.02-78.02s (2.00s) · 2.52x · speed  
  _Hero close — the whole hero clip sped to fit, landing on Christ (single appearance, no reuse)._

## Independent panel
- **Editor** — `REVISION NEEDED` — 61.5s→76.0s is one clip at 0.35x — six spoken beats, no image change; a quarter of the runtime is a freeze-frame in all but name.
- **Beat-Sync** — `STRONG` — Pins are literal and honest throughout — wagging heads, sneering rulers, the jeer under the taunt, mercy over 'the very people throwing it'.
- **No-Reuse** — `STRONG` — 13 distinct body clips, hero once at the close.
- **Pacing** — `REVISION NEEDED` — Speed extremes land on the wrong clips: the crucified Christ (#06) is the fastest at 2.57x while a static love-gaze (#18) is slowest at 0.35x; hero flashes at 2.52x.
- **Hero-Continuity** — `STRONG` — Jeer-open is a real scroll-stopper; dawn-cross hero under 'Turn, and come to the One who would not come down' lands squarely on Christ.
- **Jaded Viewer** — `REVISION NEEDED` — I would feel the screen die at the 62-second mark — exactly where the hook's script-thread pays off with no picture to show for it.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->78.02s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #14 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.23x, max 2.57x, 0 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['bridge', 'david', 'hook', 'landing', 'mocker'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #14 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G9 Beat Density** — `CONDITIONAL` — 13 moments · avg slot 5.8s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 20 (pool has 18).
- **AS-G8 Beat Continuity** — `PASS` — The script thread runs hook->fulfillment->restraint->invitation and the close is the gospel-pivot. No pin contradicts its words — the failure is rhythm, not meaning.

## Priority fixes
1. Move #02 (the psalmist and his script) from P03 to P36 'they were reading from a script they never finished' — it is the thread's payoff image and it halves the dead tail; let #01 carry the whole hook P00-P05.
2. With #02 at P36, #18 holds only 'theirs, and ours — to win the scorners' (~7s) — reverent, not dead.
3. Widen the hero window if the allocator permits (2.0s at 2.52x undersells the closing line).
