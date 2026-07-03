# Edit plan — Self-review panel

**Verdict:** `LOCKED`  ·  **Failed gates:** 0

## How the clips map to the words
The cut opens on the wounded man (#01) under 'a wound nothing has been able to close', moves to Isaiah's own imagery (#08 sheep/burden) as he writes, then walks the verse word-by-word: the flogging post under 'wounded for our transgressions', the burden-bearing crucified under 'chastisement', the welted shoulder under 'with his stripes'. The bridge lands the wounding on Jesus (#06) and pins Peter literally pointing at Christ (#07) under 'laid them on Christ'. Peter's verse gets the freed man with broken chains under 'live unto righteousness' and Christ's face aimed at the viewer under 'ye were healed'. The landing runs finished-dawn (#12), clean-new-life dawn (#19), the path to the cross under 'bring Him the guilt' (#21), and the opening man HEALED — scar closed — under 'let His wounds close yours' (#14). The hero close is #13: Christ's opened, nail-marked hands extended in welcome, held under 'His stripes — your healing.'

## Slots
- ` 0` **body/hook** — #01 The Wound That Won't Close · 0.00-2.50s (2.50s) · 2.02x · speed  
  _The weathered man, hand pressed over his chest — literally 'a wound nothing has been able to close' at P00._
- ` 1` **body/hook** — #08 All We Like Sheep · 2.50-10.80s (8.30s) · 0.61x · speed  
  _Isaiah's own chapter imagery (the straying sheep, the burdened figure) under 'Isaiah wrote that the healing... would come through someone else's wounds'._
- ` 2` **body/isaiah** — #03 Wounded For Our Transgressions · 10.80-14.76s (3.96s) · 1.27x · speed  
  _Christ bound at the flogging post, welted back — the exact action of 'wounded for our transgressions'._
- ` 3` **body/isaiah** — #09 He Bare Our Sins · 14.76-20.36s (5.60s) · 0.90x · speed  
  _The crucified Christ with the burdens half-dissolved around him — 'the chastisement of our peace was upon him'._
- ` 4` **body/isaiah** — #05 Wounded For Us · 20.36-23.76s (3.40s) · 1.48x · speed  
  _Close welted shoulder — on-screen exactly as 'with his stripes we are healed' is spoken._
- ` 5` **body/bridge** — #06 Whom They Pierced · 23.76-29.84s (6.08s) · 0.83x · speed  
  _The wound on Jesus' body with mourners beyond — 'the wounding Isaiah foresaw... fell on Jesus'._
- ` 6` **body/bridge** — #07 The Apostle Lays It On Christ · 29.84-32.66s (2.82s) · 1.79x · speed  
  _The apostle with his open hand turned toward the crucified figure — a literal picture of 'Peter took up Isaiah's words and laid them on Christ'._
- ` 7` **body/peter** — #23 Crushed In Your Place · 32.66-41.58s (8.92s) · 0.57x · speed  
  _The freed kneeling man with broken chains beneath the crucified Christ — 'being dead to sins, should live unto righteousness'._
- ` 8` **body/landing** — #11 Aimed At You · 41.58-50.96s (9.38s) · 0.54x · speed  
  _Christ's face inclined toward the viewer, meeting one set of eyes — 'ye were healed', the promise aimed at the listener._
- ` 9` **body/landing** — #12 Finished At The Cross · 50.96-55.24s (4.28s) · 1.18x · speed  
  _The finished cross against widening gold dawn — 'for them it was already done'._
- `10` **body/landing** — #19 Come To Him · 55.24-61.18s (5.94s) · 0.85x · speed  
  _The cross at dawn — 'so a new life could start clean'._
- `11` **body/landing** — #21 Room To Turn · 61.18-69.74s (8.56s) · 0.59x · speed  
  _The empty cross with a path winding toward it — the walk of 'bring Him the guilt that keeps reopening'._
- `12` **body/landing** — #14 The Wound He Closed · 69.74-72.02s (2.28s) · 2.21x · speed  
  _The SAME man from the hook, head lifted, scar closed — 'let His wounds close yours' pays off the opening image._
- `13` **hero-tail/hero** — #13 Come And Receive · 72.02-74.02s (2.00s) · 2.52x · speed  
  _Hero close — the whole hero clip sped to fit, landing on Christ (single appearance, no reuse)._

## Self-review panel
- **Editor** — `CAUTION` — Solid arc, but the hook rides one slow clip (#08 at 0.61x) for 8.3s of the first 11 seconds — the most scroll-critical stretch is the slowest part of the cut.
- **Beat-Sync** — `STRONG` — Every pin is literal: flogging post under 'wounded', burden-bearer under 'chastisement', welted shoulder under 'stripes', apostle-pointing under 'laid them on Christ', scar-closed man under 'let His wounds close yours'.
- **No-Reuse** — `STRONG` — 13 distinct body clips + hero #13 exactly once at the close; the #01/#14 pair is the same actor by design (bookend), not reuse.
- **Pacing** — `CAUTION` — Hero #13 lands at 2.52x and payoff clip #14 at 2.21x — the two most sacred/emotional frames are the fastest in the cut; both deserve near-full speed even at 2s windows.
- **Hero-Continuity** — `STRONG` — Opens on the wound-man hook, closes on Christ's opened nail-marked hands under 'His stripes — your healing' — the cut lands on Jesus, not on an emotional frame.
- **Jaded Viewer** — `CAUTION` — Would stop at the hook line, but the 2.5-10.8s slow sheep hold risks a swipe before Isaiah's verse arrives.

## Gates
- **AS-G1 Timeline Coverage** — `PASS` — 14 slots tile 0->74.02s contiguously.
- **AS-G2 No Reuse** — `PASS` — 13 distinct body clips; hero #13 appears once (close only) — no reuse.
- **AS-G3 Speed/Trim Health** — `PASS` — avg speed 1.14x, max 2.21x, 0 trimmed.
- **AS-G4 Min Slot** — `PASS` — All body slots >= 0.8s.
- **AS-G5 Section Coverage** — `PASS` — Every spoken section has a clip: ['bridge', 'hook', 'isaiah', 'landing', 'peter'].
- **AS-G6 Hero Close** — `PASS` — Opens on hook #01; gospel-pivot hero #13 closes 2.0s (single appearance).
- **AS-G7 Gospel Frame** — `PASS` — Gospel-pivot + hook-open + close all present; cut lands on Christ.
- **AS-G9 Beat Density** — `CONDITIONAL` — 13 moments · avg slot 5.5s > target 4s — feels slow for 'lots of moments'.  
  _fix:_ Raise --clips toward 19 (pool has 20).
- **AS-G8 Beat Continuity** — `PASS` — The wound->stripes->healing thread is carried open (wound-man) -> climax (stripes on Christ, Peter's application) -> close (scar closed, Christ's healed hands); no clip contradicts the words under it.

## Priority fixes
1. Rebalance slot 1: shorten #08's window (start #03 earlier at P03 'Seven hundred years before the cross') so the hook section carries two moments instead of one 8.3s slow hold.
2. Give the hero more room: extend the hero-tail to start at P31 (~69.7s) so #13 plays nearer 1.2x instead of 2.52x — the reverence cap should bind the close hardest.
3. If re-timed, keep #14 at or under ~1.5x — the scar-closed payoff must register.
