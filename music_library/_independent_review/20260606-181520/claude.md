# Independent review — claude (OK, 140s)

I verified the artifact against the actual code in `music_library/` and `11labs-testing/`. The round-2 claims mostly hold up — but two real reuse/accuracy flags remain.

## What genuinely checks out (round-1 fixes verified in code, not just prose)

- **Doctrine is really code-enforced.** `_specs.py:17` `BEAT_ALLOWED` + `music_library.py:106` `find_for_beat` hard-filter `mood not in allowed` and exclude tension/urgent/lonely/lament from `conviction`/`landing`. The matrix in the artifact matches `BEAT_ALLOWED` exactly. Round-1's "doctrine is only prose" is genuinely resolved.
- **Audition gate is real.** `MusicEntry.status="pending"` default (`music_library.py:57`), `find()`/`find_for_beat()` both skip non-approved (`:92`, `:116`), `ingest.py:94` writes `pending`, `approve.py` flips it. Not selectable until a human approves — as claimed.
- **LUFS is actually measured.** `ingest.py:38-46` runs `loudnorm=print_format=json` and parses `input_i`. Real EBU R128, not a dBFS rename.
- **Single-source-of-truth.** `_specs.py` → `_gen_catalogue.py` → `CATALOGUE.md`; per-track `beats:` derive from `beats_for_mood`. Consistent.
- **The narrow enhance.py claim is accurate.** `enhance.py:177` does `atrim=0:{length}` — trims from t=0 only. The artifact's "trims from t=0, not a reusable placer" is literally true.

## Remaining real flags

**1. Reuse gap — the placer is ~70% already built in `enhance.py`, and the plan frames it as build-from-scratch.** The artifact says the beat-aligned placer is "NOT built yet … the Phase-1 pilot job." But the *hard* parts already work and are proven on the Well clip:
- forced-align word timing → `_align.py` (reuses `veed_io.aligner`)
- sidechain-duck under voice → `enhance.py:194` `sidechaincompress=threshold=0.05:ratio=6...`
- event-timed placement at a word timestamp → `enhance.py:66` waterpot anchored to "she dropped her waterpot" @ 37.8s
- gated metered spend + red banner → `enhance.py:100`

Only the *trim-to-arbitrary-in-point* + *align-swell-to-CTA* pieces are missing. The honest task is "generalize `enhance.py`'s `mix()` into a reusable Suno placer," not "build a placer." CLAUDE.md's locked rule is *"Reuse downstream pipelines, do not duplicate."* As written, Phase-1 risks re-implementing the align+duck+gated-mix that already runs.

**2. The stated Eleven Music fallback is currently broken.** The artifact (Status + Boundaries) leans on *"Eleven Music remains the fallback for a bespoke per-clip score."* But `enhance.py:120` already has a comment — *"continuing without music — fix key scope then re-run"* — and memory `audio-enhancement-postpro` records the blocker: **the project key lacks `music_generation`+`user_read` scope → Eleven Music 401s.** Presenting a 401-blocked path as the live safety net is misleading. Either fix the key scope or mark the fallback as currently-unavailable.

## Minor (not blockers)

- **Layering rule is prose-only — asymmetric with the "doctrine is DATA" boast.** `LAYERABLE_MOODS={"glory"}` exists (`_specs.py:29`) but nothing enforces "one melodic bed per clip." The placer could stack two melodic beds; the rule lives only in the markdown.
- **`find_for_beat` ignores energy.** It filters mood only, so `sacred_grace_rise` (energy=`build`/`climax`, a grace *swell*) is selectable under the exposition `point` beat — energetically wrong for a teaching moment. No energy/beat fitness check.
- **"≤20 final beds" is a wish, not enforced.** `ingest.py:88` registers `_a` and `_b` as separate selectable slugs, so up to 40 entries can be approved. Fine, just don't state ≤20 as a guarantee.
- **`tempo_bpm` kept while claiming "Suno ignores numeric BPM."** Harmless (prompts use words like "slow adagio"; BPM is metadata), but it's a mild internal contradiction.

The substance is sound and the built parts do what they claim. The two flags above are directives to bake into Phase-1, not defects in the current library.

VERDICT: PASS
TOP FIXES:
1. Build the Phase-1 placer by **generalizing `enhance.py`'s proven `mix()` (align + sidechaincompress duck + gated spend)**, not from scratch — only add trim-to-in-point + swell-to-CTA. State this reuse explicitly so the working ducking/align code isn't re-implemented.
2. Stop presenting Eleven Music as a live fallback until the key scope is fixed — the project key 401s on `music_generation` (per `enhance.py:120` + memory). Mark it "currently unavailable" or resolve the scope first.
3. Move the "one melodic bed per clip" / energy-fit rules from prose into the selector (mirror how doctrine became `BEAT_ALLOWED`), and stop claiming "≤20 final beds" since `_a`/`_b` both register as approvable.
