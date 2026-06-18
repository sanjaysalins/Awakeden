# Independent review — codex (OK, 197s)

**Findings**

1. **Architecture contradicts itself.** The plan says “extends `music_library/`, source=`eleven`” ([plan:14](C:/Users/sanjay/PycharmProjects/JesusInTheBible/v2/FIX_ALL_PLUS_MUSIC_LIBRARY_PLAN.md:14)), then says build a separate `eleven_music/` mirror ([plan:51](C:/Users/sanjay/PycharmProjects/JesusInTheBible/v2/FIX_ALL_PLUS_MUSIC_LIBRARY_PLAN.md:51)), then says long-form pulls from `music_library` ([plan:84](C:/Users/sanjay/PycharmProjects/JesusInTheBible/v2/FIX_ALL_PLUS_MUSIC_LIBRARY_PLAN.md:84)). Existing `MusicEntry` already has `source`/`license` fields ([music_library.py:62](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/music_library.py:62)). Forking tooling is unjustified duplication.

2. **“`find_for_beat(...)` … already built” is false for this plan.** The claim at [plan:63](C:/Users/sanjay/PycharmProjects/JesusInTheBible/v2/FIX_ALL_PLUS_MUSIC_LIBRARY_PLAN.md:63) only applies to the existing Suno-rooted library. `MusicLibrary` is hard-bound to its own `LIB_ROOT/index.json` ([music_library.py:35](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/music_library.py:35)) and `find_for_beat` imports `_specs` as a top-level module ([music_library.py:114](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/music_library.py:114)). There is no federated eleven+suno selector.

3. **Phase 3’s reuse-first path is not implemented.** The plan says `find_for_beat` then `add_music.py` ([plan:72](C:/Users/sanjay/PycharmProjects/JesusInTheBible/v2/FIX_ALL_PLUS_MUSIC_LIBRARY_PLAN.md:72)), but current batch music always uses `best_prompt` and `regen=True` ([music_batch.py:15](C:/Users/sanjay/PycharmProjects/JesusInTheBible/sfx_pilots/music_batch.py:15)). `add_music.py` generates Eleven music when `music.mp3` is absent ([add_music.py:56](C:/Users/sanjay/PycharmProjects/JesusInTheBible/sfx_pilots/add_music.py:56)); it has no `--score path` or library-track input.

4. **The deliverable chain is missing SFX.** Phase 1 promises only clean `viral_cut.mp4` ([plan:43](C:/Users/sanjay/PycharmProjects/JesusInTheBible/v2/FIX_ALL_PLUS_MUSIC_LIBRARY_PLAN.md:43)), but `add_music.py` requires `assembly/viral_cut_sfx.mp4` ([add_music.py:42](C:/Users/sanjay/PycharmProjects/JesusInTheBible/sfx_pilots/add_music.py:42)). The plan must explicitly rebuild SFX before music.

5. **`music_designs.json` is not a tag schema.** The plan says tag each score with mood/beat/doctrine-fit from `music_designs.json` ([plan:59](C:/Users/sanjay/PycharmProjects/JesusInTheBible/v2/FIX_ALL_PLUS_MUSIC_LIBRARY_PLAN.md:59)), but that file contains `winner_lens`, `best_prompt`, and prose `why`, not normalized `mood`, `energy`, `beat`, or `doctrine` fields ([music_designs.json:3](C:/Users/sanjay/PycharmProjects/JesusInTheBible/v2/coherence_audit/music_designs.json:3)). `MusicEntry` requires explicit `mood`, `energy`, and `tags` ([music_library.py:43](C:/Users/sanjay/PycharmProjects/JesusInTheBible/music_library/music_library.py:43)).

6. **Full-length Eleven scores are being treated like reusable beat beds.** `add_music.py` generates music to exact cut duration plus outro ([add_music.py:58](C:/Users/sanjay/PycharmProjects/JesusInTheBible/sfx_pilots/add_music.py:58)). Reusing a score on a different-length short can misplace the emotional pivot and tail. The plan has no trim/loop/time-align proof before scaling.

7. **Cost control is overstated.** The plan says “quote the count + ask first” for new music ([plan:75](C:/Users/sanjay/PycharmProjects/JesusInTheBible/v2/FIX_ALL_PLUS_MUSIC_LIBRARY_PLAN.md:75)), but current notes say Eleven Music quota is invisible ([RESUME.md:53](C:/Users/sanjay/PycharmProjects/JesusInTheBible/RESUME.md:53)), and `credits_left()` is defined but unused in `add_music.py` ([add_music.py:24](C:/Users/sanjay/PycharmProjects/JesusInTheBible/sfx_pilots/add_music.py:24)). “Mostly $0” is not a reliable spend model.

8. **The catalogue gate is not a true prerequisite.** The plan says catalogue sweep “before/while” ([plan:46](C:/Users/sanjay/PycharmProjects/JesusInTheBible/v2/FIX_ALL_PLUS_MUSIC_LIBRARY_PLAN.md:46)), but safe reuse depends on it being done before reuse. Current `clip_library.materialize` copies coherence and records clip QC, not element-gate/manifest state ([clip_library.py:49](C:/Users/sanjay/PycharmProjects/JesusInTheBible/clip_library/clip_library.py:49)).

9. **The locked music directive is still footgunnable.** Plan locks gain −8 ([plan:73](C:/Users/sanjay/PycharmProjects/JesusInTheBible/v2/FIX_ALL_PLUS_MUSIC_LIBRARY_PLAN.md:73)), but the CLI default is `-17.0` ([add_music.py:98](C:/Users/sanjay/PycharmProjects/JesusInTheBible/sfx_pilots/add_music.py:98)). Single-short runs can silently violate the standard.

VERDICT: REVISE
TOP FIXES:
1. Resolve the music architecture: one `music_library` with `source` filtering, or a real federated selector; no duplicated `eleven_music` toolchain without proof.
2. Implement and prove the end-to-end reuse path: catalogue-gated clip reuse → SFX rebuild → library-score selection → path-based mix → caption → approval state.
3. Replace the cost/verification claims with concrete gates: music quota visibility or explicit “unknown,” normalized score metadata, duration/arc alignment checks, and final user ear approval.
