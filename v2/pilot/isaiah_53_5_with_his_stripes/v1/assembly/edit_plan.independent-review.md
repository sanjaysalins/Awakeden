# Edit plan — Independent red-team audit

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

## Independent panel
- **Editor** — `CAUTION` — The arc reads clean and the pins are honest, but three body slots run 8.3-9.4s at ~0.6x — for a 74s short that is three long holds; the middle never accelerates.
- **Beat-Sync** — `STRONG` — Word-for-image discipline is genuinely tight: flogging under 'wounded', burden under 'chastisement', welts under 'stripes', pointing apostle under 'laid them on Christ', closed scar under 'let His wounds close yours'. No clip fights its words.
- **No-Reuse** — `STRONG` — 13 distinct + hero once at the close. The #01/#14 same-man bookend is intentional payoff, not reuse — but the render must keep the actor visually identical.
- **Pacing** — `REVISION NEEDED` — The two most sacred frames are the fastest: hero #13 at 2.52x and the scar-payoff #14 at 2.21x. A 2-second hero at 2.5x will read as a flash, not a landing — this inverts the reverence rule even though the deterministic cap technically passed.
- **Hero-Continuity** — `STRONG` — Hook is a genuine scroll-stopper premise (a wound that won't close), and the close is Christ's opened healed hands under 'His stripes — your healing' — lands on Jesus.
- **Jaded Viewer** — `CAUTION` — I would stop at the first line; whether I stay through an 8.3s slow sheep hold at second 3 is a coin flip.

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
- **AS-G8 Beat Continuity** — `PASS` — One thread (wound -> His stripes -> your healing) runs hook to hero with each image under its own words; the close is the gospel-pivot, not an emotional frame.

## Priority fixes
1. Hero speed: re-time the hero-tail toward >=P31 (~4.3s window) so #13 plays near 1.2x — the single most important frame currently flashes at 2.52x.
2. Split slot 1: end #08 at P03 and bring #03 in at 'Seven hundred years before the cross' so the hook stretch carries two moments.
3. Keep #14 under ~1.5x so the scar-closed payoff registers before the hero.
