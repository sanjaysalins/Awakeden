# Independent review — codex (OK, 166s)

**Findings**

1. The one-bed shorts architecture makes hook-only pilot beds unusable. The plan says “60s shorts = ONE primary melodic bed for the whole clip” and picked via `find_for_beat('landing', …)` ([CATALOGUE.md](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/CATALOGUE.md:16)), but `lonely_searching` is pilot-listed and only has hook use cases ([`_specs.py`](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/_specs.py:55), [`_specs.py`](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/_specs.py:58), [`_specs.py`](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/_specs.py:149)). If it is selected for the whole clip, it violates Landing safety; if selection is Landing-safe, it is dead inventory.

2. The intelligibility gate is design-only, not code. The claim “Music ducks to near-silent under the verbatim KJV quote” and “STT word-recovery ≥ 98%” ([CATALOGUE.md](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/CATALOGUE.md:17)) has no executable checker. `enhance.py` only has global sidechain compression ([enhance.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/11labs-testing/enhance.py:195)); the KJV-specific envelope and recovery threshold live only in `PLACER.md` ([PLACER.md](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/PLACER.md:45), [PLACER.md](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/PLACER.md:52)).

3. “Energy-fit” does not guarantee the thing claimed. The brief says Point “won’t grab a grace swell,” but `find_for_beat` only gives preferred energy a `+1.5` bonus, not a hard filter ([music_library.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/music_library.py:119), [music_library.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/music_library.py:125), [music_library.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/music_library.py:126)). If only `sacred_grace_rise` is approved, Point can still return it because `sacred` is allowed on Point.

4. The “one primary take per base slug” claim is overstated. `approve.py` blocks a sibling by default, but it also exposes `--force` to approve both ([approve.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/approve.py:24), [approve.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/approve.py:48)). That is not enforcement; it is a warning with an override.

5. The placer is still not build-proven in code. The artifact’s status phrase “Designed, built+proven during the pilot” ([CATALOGUE.md](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/CATALOGUE.md:12)) is future tense disguised as status. There is no `music_library/placer.py`; `PLACER.md` itself says it is “implemented + proven during the pilot … not before” ([PLACER.md](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/PLACER.md:5)). Step 1 still orders “generate” before “Build `placer.py`” ([CATALOGUE.md](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/CATALOGUE.md:22)).

Resolved items I verified: `swell_s` exists, `approve.py --swell` gates arc beds, `glory` is layer-only in selection, pilot-only ingest is real unless `--all`, and LUFS measurement is present.

VERDICT: REVISE
TOP FIXES:
1. Resolve one-bed vs hook-only catalogue: either remove hook-only beds from Phase 1, allow scoped hook layers/crossfades, or make all shorts primaries CTA-safe.
2. Build `placer.py` and the automated 98% word-recovery/KJV duck test before any Suno pilot batch.
3. Make energy fit and one-primary rules hard where the plan says they are hard; remove or narrow `--force`.
