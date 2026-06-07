# Independent review — claude (OK, 267s)

I verified the v2 claims against the real codebase. The core lock logic is sound, but the artifact oversells what it checks and the exemption story has a real hole. Findings below, each cited.

## What genuinely IS closed (confirmed against real files)

- **v1 crash on real XML** — ✅ closed. Real tagged files (`01_Isaiah_53.../narration-tagged.md`, the Psalm 22 shorts) use `<speaker name="narrator">` / `<speaker name="the_LORD">` with **only** the `name` attribute, so `_XML_SPEAKER` (`narration_parse.py:92`) matches. I confirmed a real `narration.md` ↔ `narration-tagged.md` pair (Psalm 22 short #1) canonicalizes identically, so parity does NOT spuriously block real content.
- **Split-brain** — ✅ closed. KJV/Rule-8/cluster run on `narration.md` (the ref-bearing file), the hash binds tagged-when-present (`_spoken_source`, `lock.py:43`), and `parity_mismatch` (`lock.py:68`) blocks divergence. A tagged-only folder is refused early (`run_lock` requires `narration.md`, `lock.py:151`).
- **Punctuation-blind hash** — ✅ closed. `_canon_spoken` uses `kjv_strict._canon` (preserves punctuation), `test_punctuation_edit_busts_lock` proves a comma edit goes stale.
- **Multi-door** — partly. Audio (`handoff.run_audio_pipeline`) + assembly (`run_assembly:120` + `cli_assemble.py:67`) are guarded, all fail-closed. But see the exemption below.

## New problems / overclaims (not rubber-stamped)

**1. The engine exemption is a bigger hole than disclosed — and it dead-ends `cli_pipeline`.**
The engine writes `narration.md` as **plain prose** (`handoff.py:105` → `draft.narration`, docstring `:6`). That has no `**[speaker]**` blocks, so `NP.parse` raises `EmptyNarrationError` → `run_lock` returns `{"ok": False, "blocking": ["parse: ..."]}`. Consequences the artifact understates:
- The **cluster/templating check never runs on the engine generation path** (`runner.py:145`, `enforce_lock=False`). Templating across a cluster is *exactly* what shipped the bad Psalm 22 set — and that's the one door left open on the path most likely to produce it.
- Worse, `runner.py:144` claims hand-authored content "is enforced via cli_lock" — but `cli_lock` can't lock plain prose either. And `orchestrator._seg_d` (`orchestrator.py:168`) calls `run_assembly` → `require_lock`, which will **hard-refuse** engine-generated content (it can never be locked). So `cli_pipeline` on a fresh engine topic renders audio, then dead-ends at assembly. That's a latent break, not just a "documented follow-up."

**2. The docstring lies about two checks that don't exist.** `lock.py:8-10` (and the artifact summary) claim the lock runs "**anchor-verse**" and cluster "vs the folder's siblings **+ the catalogue**." Neither is real: `_anchor_findings` (`lock.py:135`) returns `[]` unconditionally, and `cluster_check(arts, ...)` (`lock.py:183`) is fed **only siblings** — never the registry/catalogue, so cross-*episode* templating is invisible. A security gate's docstring must not claim coverage it doesn't have.

**3. The tests mutate a tracked data file.** `test_clean_folder_locks_and_registers` (and stale/kjv/rule8 tests) → `run_lock` success → `register()` → writes the real `data/learning/freshness_registry.json` with **tempdir phantom paths** (`lock.py:207-215`). 13/13 "passing" includes this side effect on a repo file.

## Secondary

- **XML regex is fragile.** `name="([^"]*)"\s*>` requires `>` immediately after the name attr. `voices.json` carries an `audio_tag` per speaker; if the tagger ever emits `<speaker name="x" tag="...">`, it parses **zero** blocks → fail-closed refuse on legit content. Safe direction, but brittle.
- **Cluster is checked only at lock time.** `is_locked` re-checks hash + parity, never cluster. A short locked while standing alone (warning "locked WITHOUT cross-artifact scrutiny", `lock.py:188`) stays valid even after templated siblings are added beside it.
- A `narration.md` whose DEPTH ledger merely contains the substring `<speaker` flips `parse_blocks` to the XML branch (`narration_parse.py:108`) → likely `EmptyNarrationError` → can't lock a legit file. Fail-closed, but a foot-gun.

None of these let bad text get *falsely certified* — the lock itself is sound and fail-closed. But #1 means the gate's headline purpose (catch templated clusters) is bypassed on the generation path and breaks the orchestrator, and #2/#3 are real defects that shouldn't land as-is.

VERDICT: REVISE
TOP FIXES:
1. Resolve the engine exemption, don't just document it: either emit `**[speaker]**`-block `narration.md` from the engine so it CAN be locked (closing the cluster door on the generation path), or explicitly handle it in `orchestrator._seg_d` so `cli_pipeline` doesn't render engine audio with zero cluster scrutiny and then hard-refuse at assembly.
2. Fix the docstring/summary overclaims — `lock.py:8-10` advertises "anchor-verse" and "+ the catalogue," but `_anchor_findings` is a no-op and the cluster check only sees siblings. Remove the claims or implement them (registry-backed cross-episode cluster check).
3. Isolate the tests from the real registry — `register()` writes `data/learning/freshness_registry.json` with tempdir paths during the suite; monkeypatch `_REGISTRY` (or skip `register` under test).
