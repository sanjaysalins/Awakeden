# Independent review — codex (OK, 183s)

Findings:

1. The lock chokepoint is not yet non-bypassable. The plan says downstream “refuses without the token,” but the real sibling synth paths already have bypass semantics: `per_turn_synth.py` and `narration_pipeline.py --stage synth` both expose `--no-gate`, and both currently skip gate enforcement when `episode.manifest.json` is absent. The Psalm 22 short folders currently have no `episode.manifest.json`, `scripture.json`, or gate stamp. v3 must explicitly remove/disable those bypasses and require `.locked` regardless of manifest presence.

2. The `.locked` hash target is underspecified. The plan says the token stores the “commit-ish of the narration text” / “matching narration hash,” but synth consumes `narration-tagged.md`, not just `narration.md`. A stale or edited tagged file could be rendered while the raw narration hash still matches. The lock must bind the effective spoken text actually consumed by synth/captions, or force regeneration and round-trip verification before render.

3. Scoped canon is right in principle, but B2 is not a true witness. The phrase “spot-check it against a second independent source … for the known-hard cases” leaves every non-hard used verse trusted from one baseline. For ~used verses only, every ref should be compared against at least two independent witnesses, with disagreements adjudicated before entering `kjv_verified.json`.

4. A1’s block-ref mapping misses real current prose. The plan says `quoted_spans_with_refs(md)` maps quotes to “its block’s tagged ref,” but current shorts contain spoken KJV snippets in untagged narrator blocks, e.g. short #1 `"that the scripture might be fulfilled"` and short #2 `"Let him deliver him,"`. Either require every Scripture quote/echo to be in a tagged KJV block or add explicit inline ref syntax.

5. The plan ignores existing `short_gate`. The sibling repo already has `short_gate` with KJV checks, freshness registry, manifests, stamps, and downstream validation. Creating `verify_narration.py` without a migration/reuse decision risks parallel gate systems and inconsistent lock semantics.

6. Ledger append is not idempotent. “Appends the artifact’s phrases to the ledger” can duplicate entries on re-lock/backfill and make the artifact collide with itself unless entries are keyed by artifact id/hash and excluded from self-comparison.

VERDICT: REVISE
TOP FIXES:
1. Make the lock truly fail-closed across all render/caption entrypoints and bind it to the actual spoken artifact.
2. Strengthen scoped KJV witnessing and require explicit refs for every spoken Scripture quote/echo.
3. Reconcile `verify_narration.py`/`cli_lock.py` with the existing `short_gate` stack and make ledger writes idempotent.
