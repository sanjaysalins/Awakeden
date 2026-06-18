# Independent review — claude (OK, 171s)

Verified against the codebase. Findings below.

## Confirmed facts
- `pipeline/element_manifest.py declare-short` exists ✓; `music_library/` with `find_for_beat`, `ingest`, `approve`, `qc` exists ✓; the index already carries `source`/`license` fields ✓; 11 `music.mp3` scores exist (8 Psalm-22 + 3 pilots) ✓ — the "11 scores" count is correct.

## Findings

**1. FEASIBILITY GAP — Phase 3's reuse path does not exist in the tool.** The plan says: *"`find_for_beat` the best-fit approved score → mix at the new directive (`add_music.py` …)."* But `sfx_pilots/add_music.py:40-69` only reuses a score if `assembly/music.mp3` is *already present on disk*; otherwise it **generates from `--prompt` via Eleven Music (metered)**. It has no input-file argument, no `find_for_beat` call, and no way to take a library mp3. To "reuse-first" you'd have to (a) copy the library score into `assembly/music.mp3` and (b) **length-match it** — the music_library pad is 223 s, a short is ~59 s. None of that is built. So "$0 per reuse" in Phase 3 is **unverified and requires new code**, not just calling the existing tool.

**2. INTERNAL CONTRADICTION — separate `eleven_music/` store breaks `find_for_beat`.** Decision #2 puts eleven scores in a SEPARATE dir, but Phase 2 claims *"`find_for_beat` then returns the best eleven/suno score by fit (already built)"* and Phase 4 leans on it for reuse. The existing `find_for_beat` (`music_library/music_library.py:108`) reads **only `music_library/index.json`** — it will never see a separate store. You'd have to duplicate or fork it to query two stores. And the existing index **already has `source`/`license` fields designed for multi-source** — so the separation duplicates `ingest/approve/qc/find` code AND disables the one reuse function the whole plan depends on. The plan footnotes "some tooling duplication" but understates that it breaks the reuse lever.

**3. "120 clean catalogue clips" is wrong twice.** It's **125** (`clip_library/index.json`), and the plan itself adds Phase 1b *because the catalogue is NOT element-gate-clean*. Calling them "120 clean" while scheduling a sweep to find their defects is contradictory framing.

**4. $0 baseline generalizes from N=1.** The whole "mostly $0" headline rests on #03, where reuse happened to cover the holes. Your own memory says #02/#03/#04/#06 clips predate the v2 servicer fix and are "worse" — multiple shorts likely have holes reuse can't fill. The table's "**$0 baseline**" oversells; a realistic worst-case render count is never estimated up front, only "quote per case."

**5. The "LOCKED directive" isn't a set of knobs.** `add_music.py` exposes only `--gain` (argparse default −17, function default −8 — already inconsistent). `outro=2.5`, `threshold=0.12`, `ratio=2.5` are **hardcoded** (`add_music.py:73-79`), not flags. So locking "the directive" is fine today only because the hardcoded values match — but it's a code edit to change, not config, and the plan presents them as dials. Separately, −8 dB under voice is meaningfully **louder** than the −17 default; "gentle bed" is debatable and should be ear-checked, not asserted.

**6. Over-engineering before proof.** Phase 4 (wire long-form to the library) and the separate-store infra are built before Phase 1 proves the reuse pattern scales past one short. "≈2 lenses × a few moods covering most short/long beats" is an unproven coverage claim for ~8–11 harvested scores.

**7. Verification gap in the re-sweep.** Phase 1 step 5 "re-sweep → confirm clean" uses the same agent-look gate that already *missed* the catalogue defect ("hid a gem"). The guardrail says calibrate-vs-blind-labels before any HARD enable, but no step schedules that calibration for the sweep gate itself — so "confirm clean" inherits the gate's known blind spots.

## What's solid
`declare-short`, the sweep page, user-as-authority, ask-before-spending, audition-by-ear, and the strict-numeric one-short-at-a-time order are all real and well-grounded. The *spirit* (sweep → reuse-rebuild → bank a music palette) is sound; the wiring claims are where it overreaches.

VERDICT: REVISE
TOP FIXES:
1. Fix Phase 3: `add_music.py` cannot reuse a library score — add an explicit step/PR to give it a `--from-library`/input-mp3 path WITH length-matching (trim/extend to clip duration), or stop claiming "$0 per reuse via add_music.py." Right now that path doesn't exist.
2. Resolve the `eleven_music/`-vs-`find_for_beat` contradiction: either keep eleven scores in `music_library/` (it already has `source`/`license` fields — no duplication, reuse works) or commit to forking `find_for_beat` to span both stores and say so. As written, the separate store silently disables the reuse lever Phases 2–4 depend on.
3. Replace the "$0 baseline" headline with an up-front worst-case estimate: sweep all 11 first, count beats with no clean reuse match, quote the render/music spend BEFORE committing — and correct "120 clean" to "125, not yet element-gate-clean."
