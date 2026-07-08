# Season score identity map (L4 — 2026-07-08)

**Problem:** every published piece scores `lonely_searching_a → sacred_grace_rise_a`.
One piece sounds right; a binge session sounds like one song looping. **Rule: each
season owns a score pair (dark → rise). Within a season the pair IS the identity;
across seasons the pair changes.**

## The map

| Season | dark (first act) | rise (grace turn) | status |
|---|---|---|---|
| S1 THE CROSS | `lonely_searching_a` | `sacred_grace_rise_a` | LOCKED — this is S1's sound; do not retrofit |
| S2 HE IS RISEN | `tomb_hush_low` (NEW — brief below) | `glory_holy_stillness_a` (approved, unused!) | rise ready today; dark needs one Suno gen |
| S3 SHADOWS | `neutral_teaching_warm_a` (approved, unused) | `sacred_grace_rise_b` (pending audition) | audition _b |
| S4+ | new pair per season, briefed at season build | | |

- Interim ($0, today): S2 pieces can ship `lonely_searching_a → glory_holy_stillness_a`
  — the rise carries the identity change where the landing lives.
- The Jonah pilot (S2 opener) currently carries the S1 pair. Swap its grace side to
  `glory_holy_stillness_a` ONLY with the user's ear-approval (the pilot is approved
  as-is; a score change re-opens the ear gate).

## Suno briefs (user generates; `ingest.py` → audition → doctrine gate → approve)

**S2 dark — `tomb_hush_low`** (instrumental, ~2:30, seamless-loopable)
> Slow sacred instrumental, 60 BPM. Low sustained cello and double-bass drones in D
> minor, sparse deep piano notes with long decay, a distant low taiko pulse every two
> bars like a heartbeat under stone. Cold, hollow, cavernous reverb - a sealed tomb
> before dawn - but expectant, not despairing. No choir, no melody hook, no percussion
> fills. Cinematic film-score texture, dynamics flat and low.

**S2 rise alt — `risen_dawn_glory`** (instrumental, ~2:30, if glory_holy_stillness
> ever feels too still) Slow-building orchestral sunrise in D major, 70 BPM. Warm
> strings opening from a single sustained violin line, French horns entering at the
> halfway point, timpani rolls under the final third, resolving to a full radiant
> major chord held long. Reverent triumph - an empty tomb at first light - never
> pop-epic. No choir pad, no drum kit.

**S3 pair briefs:** written when S3 enters production (warm ancient-ceremony texture:
lyre, frame drum, low winds).

## Process (unchanged, per music-library memory)
Suno gen (user) → `_inbox/` → `ingest.py` → my QC + doctrine gate → user audition →
`approve.py` → available to `score` blocks. Never score a piece with a pending track.
