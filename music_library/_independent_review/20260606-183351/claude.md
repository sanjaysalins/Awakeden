# Independent review — claude (OK, 117s)

I verified every round-2 fix against the actual code, not just the prose. Findings below.

## What genuinely checks out in CODE (not just prose)

- **Glory is layer-only, enforced.** `_specs.py:31` `LAYER_ONLY_MOODS={"glory"}`, `music_library.py:118` subtracts it from `find_for_beat` allowed set, and `find_layer` (`:132`) only returns glory. Glory is absent from every `BEAT_ALLOWED` list (`_specs.py:18-24`). Real, not prose.
- **Energy-fit is real.** `BEAT_PREFERRED_ENERGY` (`_specs.py:35`) + the `+1.5` bonus at `music_library.py:126`. An exposition Point (`pref={"low"}`) won't outrank-grab a grace swell. Confirmed.
- **One-primary-per-base is enforced at approval.** `approved_sibling` (`music_library.py:151`) + the `[blocked]` exit at `approve.py:47`. Real.
- **--swell required for arc beds.** `approve.py:51` gates `energy in (build, climax, swell-and-rest)`, and `swell_s` is on `MusicEntry` (`music_library.py:56`). Real and buildable.
- **Pilot-gating is real.** `ingest.py:89` `if not args.all and base not in PILOT_SLUGS: [gate]`. Real.
- **Reuse chain exists.** `forced_align_script` and `transcribe_align` both exist (`veed_io/aligner.py:181,104`); `enhance.py` `mix()` sidechain graph is at `enhance.py:195`. The acceptance gate's `transcribe_align` is a real function.

The doctrine matrix in the artifact matches `BEAT_ALLOWED` exactly, beat-for-beat. **Round-2 convergent findings are resolved in code, not just narrative.** That's the core thing the brief asked me to confirm, and it holds.

## Remaining real issues (none a hard blocker before Suno spend)

1. **PLACER algorithm guards the wrong end.** `PLACER.md:39-42` clamps `bed_start < 0` but never guards `bed_start + clip_len > bed_duration`. If a take's swell is *early* and `t_cta` is *late* (e.g. swell=15s, CTA=50s → bed_start=35), the trim window can run off the end of a short Suno track and produce silence under the landing — the most doctrinally important beat. Low-probability with 2-min+ tracks, but it's an unhandled edge on the CTA. Add a one-line guard + "pick a take with a later swell" fallback.

2. **The intelligibility gate measures the aligner's own weakness.** `PLACER.md:46` ducks the bed because "word alignment is known to drop words under music," then `PLACER.md:52` *verifies* with the same `transcribe_align` at ≥98%. You're using the tool whose under-music word-dropping motivated the duck to certify the duck worked — it can fail-closed on the tool's blind spot or pass while a human still can't hear it. It's an acceptable proxy *only because* the human listen gate (`PLACER.md:56`) backs it. Keep both; don't let the 98% number stand alone.

3. **"Generalizes `mix()`" understates the work.** `enhance.py` `mix()` is not a reusable function — `SRC_VIDEO` (`:32`) and the whole `PLAN` list (`:62-68`) are hardcoded to the Well clip. The filtergraph technique is genuinely proven (sidechaincompress, adelay, afade, alimiter), so the reuse direction is honest, but "~30% to build" (`PLACER.md:18`) omits the parameterization of inputs the current `mix()` bakes in. Directionally true, mildly optimistic.

4. **~9 of 20 beds can't be used in the shorts pilot at all.** Under the "ONE CTA-safe whole-clip bed" architecture, the hook/narrative moods (lonely×2, lament×2, tension×2, urgent×2) and the glory layers are never the shorts primary — their value depends entirely on Phase-2 long-form per-movement beds, which is explicitly out of scope. Suno is flat-rate so the $ cost is ~0, but generating them now is speculative until long-form is designed. Worth a one-line note that the batch-16 is mostly long-form inventory.

**Cost lens:** effectively moot — Suno is flat-rate ($0 marginal), the only metered path is the Eleven Music fallback (correctly marked metered + `--yes` gated in `enhance.py:101`). The real cost is human audition time across 40 takes; the pilot-gate to 4 takes handles that correctly.

Nothing here blocks the 4-bed pilot. The plan is honest about `placer.py` not existing yet, reuses correctly, and is doctrine-in-code.

VERDICT: PASS
TOP FIXES:
1. Add the missing `bed_start + clip_len > bed_duration` guard in PLACER step 2 — the early-swell/late-CTA case can drop silence under the landing.
2. State explicitly that the ≥98% `transcribe_align` gate is a proxy backed by the human listen gate (same aligner whose under-music weakness motivated the KJV duck), not a standalone pass.
3. Correct the "~30% to build" framing — `mix()` is fully hardcoded (SRC_VIDEO + PLAN), so generalizing it includes input parameterization, not only trim/swell/KJV-duck.
