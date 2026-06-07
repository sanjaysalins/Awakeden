# PIPELINE_HARDENING_PLAN.md — verification hardening for narration (long + short)

**Status:** PLAN **v5** — REUSE-FIRST, after four 5-CLI panel rounds (v1 4×REVISE → v2 PASS+4REVISE → v3 4×REVISE → v4 5×REVISE, all "direction correct / execution specs"). v4's reviewers unanimously endorsed the reuse-first direction and surfaced two genuine **design** corrections (folded in below) plus a set of **implementation specs** (now in the Implementation Contract). User decision 2026-06-07: build the gate in THIS repo, reusing `short_gate`'s proven pieces, re-verify all locked content; panel before code; red-team + panel the build.

> **v4 → v5 design corrections (the two that were genuinely wrong):**
> 1. **The cluster gate flags repeated CTA *phrasing/shape DENSITY within a cluster* — it NEVER bans the CTA-to-Jesus destination.** v4's "CTA never whitelisted, blocking catalogue-wide" collided with the LOCKED CTA-to-Jesus model (no two gospel shorts could ever both lock). The real defect was 8× the *identical tag wording* in one cluster, not that they invite to Jesus. So: **within-cluster/series density of near-identical CTA/opener WORDING is blocking; the gospel destination is always allowed; catalogue-wide is advisory, not a permanent phrase ban.**
> 2. **Fix the corrupt cache at the INPUT, not only at lock.** Point drafting (`pipeline/scripture.fetch_kjv` / `kjv_check`) at the witnessed corpus (via `JESUS_KJV_CORPUS`), so the author never drafts against a wrong verse; the lock check is the backstop.

---

## Context — the two root causes

The Psalm 22 short cluster shipped 8 narrations each individually sound but **collectively templated** (8/8 close on the "Come to Him" family; repeated "thousand years" hooks, "bring you home" bridges, "That's Jesus" tags). It is the **Word of God** — *cheesy / tired / sloppy* is unacceptable. Neither the red-team nor the 5-CLI panel caught it. Root causes:

1. **No one is ever forced to check the SET or the catalogue before lock.** Per-artifact review can't see "all 8 end the same." A cross-episode freshness gate *exists* (`short_gate.gate_g7_freshness` + `_registry/freshness.json`) — but it (a) **never ran** on this cluster (hand-authored, in *this* repo, "lean process"; `short_gate` lives in the sibling repo and needs a `manifest`+`scripture.json` these folders lack), and (b) is **too weak even if run** (fingerprints the whole landing beat, not the CTA clause; landing match is **non-blocking**; checks thread-slug not the hook opener).
2. **Scripture is trusted from a corrupt cache with no independent witness.** `data/kjv_cache.json` holds `Psalm 22:7` as `"…shake the head saying,"` (missing comma); `pipeline/kjv_check.py` compares against that same cache and never checks NT cross-refs. Meanwhile the **HF-POC KJV corpus** (`C:\Users\sanjay\PycharmProjects\HF-POC\series\03_furgiven\tools\data\kjv.json`, used by `short_gate`) has Ps 22:7 **correct** — but `short_gate.kjv.norm()` strips punctuation, so its verbatim check is **punctuation-blind** and would miss the comma anyway.

Everything below targets exactly these two, reusing existing assets, at the scale of 10 series / ~76 catalog shorts + ~12–21 long-forms.

---

## Reusable assets (full paths) and how each is used

| Asset | Path | Reuse |
|---|---|---|
| Correct KJV corpus (has Ps 22:7 comma; `{italics}`/`{notes}` markers) | `C:\Users\sanjay\PycharmProjects\HF-POC\series\03_furgiven\tools\data\kjv.json` | Source of truth for the verbatim check; copied/pinned into this repo as `data/kjv_corpus.json` with provenance metadata |
| Verbatim checker — ref parse, ranges, ellipsis, book aliases | `…\PythonProject1\jesus\narration\short_gate\kjv.py` (`check_quote`, `verses_for`, `quotes_from_narration`) | Port the logic; **add a punctuation-strict comparison mode** (current `norm()` is punctuation-blind) |
| Cross-episode freshness registry + gate | `…\short_gate\gates.py` (`register_episode`, `gate_g7_freshness`, `landing_fingerprint`) | Port; **extend** with CTA-clause + hook-opener fingerprints; make CTA/opener repetition **BLOCKING** |
| Sha-stamp lock (`narration_sha256`, verdict gate before register) | `…\short_gate\gates.py` | Pattern for the `.locked` chokepoint, hashing the **spoken text** (not raw md) |
| Single-artifact external panel | `…\JesusInTheBible\independent_review.py` | Add `--type cluster` + `LENS_CLUSTER` (multi-artifact) |

**Do NOT edit the sibling-repo `short_gate` or `per_turn_synth`** (reuse-don't-duplicate). Port the proven logic into this repo's `pipeline/` and wrap it.

---

## The keystone: a fail-closed LOCK CHOKEPOINT (`cli_lock.py`)

The panel's dominant finding (v2/v3): a standalone CLI nobody is *required* to run reproduces the failure. So one non-bypassable lock step gates everything.

- `cli_lock.py "<narration-folder>"`: runs the deterministic verify tier (KJV strict, Rule-8 [short-only], anchor-verse) + the cluster/freshness check; on 0 FAIL / 0 unverified, **appends to the registry** and writes `<folder>/.locked` whose hash is the **A1-parsed spoken text** (so editing a non-spoken `## DEPTH` note does not bust the lock; re-tagging the spoken read does). Exits non-zero on any FAIL/unverified.
- **Enforcement inventory (every audio/caption entrypoint must check `.locked`):** `handoff.run_audio_pipeline` (the canonical guard this repo owns — called by `pipeline/runner.py` and `_finalize.py` and `_fix26_audio.py`), plus the veed_io caption/timing entry. The sibling `per_turn_synth.py` / `narration_pipeline.py` expose `--no-gate` and skip when a manifest is absent — since we don't edit them, **`handoff` is declared the sole sanctioned audio entry**, and a guard refuses to call synth without a current `.locked`. Direct invocation of the foreign script is a documented, discouraged bypass (named, not silently possible).
- **Proof obligation:** the 8 shorts + 2 long-forms flow through `cli_lock.py` (after the Phase-A re-verification rewrite that lets them pass cluster).

---

## Phase A — PROVE THE CATCH FIRST (the actual miss; ~$0)

### A1 — Shared spoken + ref parser (`pipeline/narration_parse.py`), fail-closed
Replaces the broken `veed_io/_extract_spoken.py` (MOVEMENT-only → empty on shorts).
- `spoken_blocks(md)` → `{speaker, ref|None, text}` for `**[speaker — KJV, <ref>]**` short blocks AND `## MOVEMENT` long sections; strips status front-matter / `## DEPTH` / `## VOICE PLAN`; normalizes smart quotes/dashes/whitespace.
- `quoted_spans_with_refs(md)` → quotes mapped to the block's tagged ref; **range refs** (`Psalm 22:6-7`) handled; **untagged inline quotes** (e.g. #01 `"that the scripture might be fulfilled"`, #02 `"Let him deliver him,"`) resolved via the ported `quotes_from_narration` best-effort ref lookup, NOT failed.
- `sentences(text)` for hook (first 1–2 sentences) / CTA (last sentence/clause).
- **Fail-closed:** zero spoken blocks → raise; callers ABORT.
- **veed_io decoupling (gemini):** do NOT import `pipeline` into `veed_io`. `pipeline` parses and passes **plain spoken strings** down to `veed_io` caption/aligner; retire `_extract_spoken.py` and route `caption.load_script_text`'s short path through the string it's handed.
- **Acceptance:** the 8 shorts + 2 longs parse to non-empty spoken text; every **tagged-block** KJV quote ref-maps; untagged spans resolve or are explicitly listed (not silently dropped).

### A2 — Cluster / freshness check (ported + strengthened registry)
- Port `register_episode` / `gate_g7_freshness` into `pipeline/freshness.py` with the registry at `data/learning/freshness_registry.json`. **Single source of truth:** rebuild the registry from on-disk `.locked` folders at check time (no append-only phantom entries on rewrite/delete — gemini); writes idempotent, keyed by artifact slug, self-excluded.
- **Strengthen beyond the original G7:** add `cta_fingerprint` (last sentence/clause, **normalized substring**) and `opener_family` (general normalized opening-n-gram/stem family — "thousand years" is a *regression fixture*, NOT the detection strategy; the family check must also catch "come unto me", "bring you home", "the door is open", etc., per codex). The detection is **structural sameness of WORDING**, computed by normalized suffix/opener similarity.
- **Density, not a destination ban (v5 correction):** within-cluster / within-series **density of near-identical CTA/opener WORDING is BLOCKING** (e.g. ≥2 shorts in one cluster sharing a normalized CTA suffix; ≥N in a series sharing an opener family). The **CTA-to-Jesus destination is ALWAYS allowed** (it is the locked model) — the gate flags repeated *phrasing/shape*, never the gospel invitation itself. **Across-catalogue** repetition is **advisory/conditional**, never a permanent phrase ban (a writer years later using a phrase once must not be blocked — gemini). The doctrinal whitelist ("the cross", "Christ", "grace") suppresses only mid-body shared-truth phrases in the near-duplicate layer.
- **Scope:** within-cluster + within-series (blocking) and across-catalogue (advisory), via a manifest auto-built by globbing **both** `longform/**/v1/**/narration.md` (this repo) and the engine `NARRATION_TREE_DIR`, ingesting `short_gate`'s existing `_registry/freshness.json` history, and handling legacy spaced folders — so the actual content is in scope (cursor, grok).
- **LLM backstop:** `independent_review.py --type cluster` + `LENS_CLUSTER`, input = a folder list/manifest, concatenates **spoken-only** text, **blocking** verdict; tolerate per-provider failure if ≥3 reviewers return; non-zero exit on a flagged cluster.

### A3 — Acceptance test (gates the whole effort)
On the real 8 Psalm 22 shorts, A2 **must** flag the **normalized `come to him` closer in 8/8** (exact catches 7; #02's lowercase em-dash needs the normalized substring — claude) and the **"thousand years" opener family** (present in #01/#02/#03/#05/#08 + #07 "a thousand years before Rome"; #04/#06 don't open with it — honest, not "6/8"). Committed as a fixture. If A2 misses the 8/8 CTA, stop and fix A2 before B/C.

---

## Phase B — KJV integrity (reuse the good corpus, punctuation-strict, fail-closed)

### B1 — Audit
`pipeline/_audit_kjv.py` compares every span actually quoted in the 8 shorts + 2 longs against the corpus, **punctuation-strict**; lists real divergences (expect Ps 22:7 comma where quoted). Drives the rest.

### B2 — Corpus as witnessed source (scoped, no full-Bible project)
- Copy `HF-POC/.../kjv.json` → `data/kjv_corpus.json`, pin source path + provenance. It already carries correct punctuation + `{italics}`/`{translator-note}` markers.
- **Spot-check** the used + known-hard verses (Ps 22:7 comma, Matt 8:27 "!") against a second independent KJV source; record the witness. Not a blanket full-Bible reconciliation. New verses witnessed on demand by a **separate** tool `cli_witness_verse.py` — **manual witnessing never lives inside the automated `cli_lock.py`** (gemini); an unwitnessed verse simply **FAILs** the lock.

### B3 — Punctuation-strict, ref-mapped check (port + harden `short_gate.kjv`)
- Port `check_quote`/`verses_for` but **add a punctuation-strict mode**: strip only the corpus's `{…}` markers, then compare the quote as a **contiguous substring of its own tagged verse** with **interior punctuation preserved** (the existing `norm()` is punctuation-blind — that's why the comma would slip). Boundary ellipsis allowed; smart-quotes/dashes normalized first.
- **NT quotes checked against the NT verse**, never the Masoretic OT verse (no LXX false-fail). Range refs joined across verse boundaries.
- Unwitnessed/unmappable ref → **BLOCK** lock (not soft WARN). bible-api is **not** a lock fallback.

---

## Phase C — wire it + honest learning status

### C1 — `verify_narration.py` (one CLI; single artifact OR set)
Deterministic tier (A1 + B3): KJV strict check; **Rule-8 short-only**; **anchor-verse-quoted** (ref from the narration's own tag / best-effort). LLM tier = `LENS_NARRATION` on **raw prose** — **no five-beat coercion** of hand-authored content (no `Draft`/`Beat` adapter → no false G5). Cluster mode = A2 when given a set. Deterministic tier free/always-on; LLM tier on demand. Quote logic consolidated (no parallel module).

### C2 — Registry append at the chokepoint + backfill
`cli_lock.py` is the single append point; **backfill** the 8 shorts + 2 longs through it (after the A2 rewrite makes them pass). **HONEST:** the `calibration.jsonl` learning loop is **inert** (`panel_misses` has no writer; `append_record` has no caller — verified) — the **freshness registry + cluster gate are the real guarantee**; the `defect_classes.json` additions are bookkeeping unless a writer is later wired (optional follow-up, not a dependency).

### C3 — Regression test
A synthetic 9th short ending "Come to Him" **MUST FAIL** `cli_lock.py` within-series AND cross-series.

---

## Phase D — DEFERRED
- Conviction-strength scoring in the external lens **iff** a `flat-conviction` defect appears (engine already gates G3/G8).
- `pacing-atempo` re-validation after any text edit.

---

## Re-verification of all locked content (after A–C + chokepoint)
1. **B1 audit** → repair real KJV divergences (Ps 22:7 etc.).
2. **A2 cluster gate** on the 8 shorts (+ long movements) → **de-template hooks + CTAs so no two land the same** — a content rewrite of 8 LOCKED shorts, each re-run through red-team + 5-CLI panel (real authoring + review time).
3. **C1 deterministic tier** (free) on all 10.
4. Re-lock via `cli_lock.py`; backfill registry.
5. **Audio/caption/timing re-validation:** a fixed short re-renders that short (~$0–$3); a fixed long-form also re-runs captions + word-timings (+ maybe video).

## Verification — how to test
- **A1:** 8+2 parse non-empty; tagged quotes ref-map; garbage raises; veed_io captions still work via the handed string.
- **A2 (acceptance):** normalized `come to him` flagged 8/8 + "thousand years" opener family, on the real shorts. **The whole-effort gate.**
- **B:** Ps 22:7 (comma required), Matt 8:27 ("!"), interior elision, NT-of-OT (vs NT verse), boundary ellipsis PASS, smart-quote PASS; unwitnessed ref BLOCKS.
- **C1:** Rule-8 fires on a 3-quote short, not a long-form; paraphrased anchor flags.
- **Chokepoint:** 8 shorts flow through `cli_lock.py`; `handoff.run_audio_pipeline` refuses without a current `.locked`.
- **C3:** synthetic "Come to Him" short FAILs within- and cross-series.

## Cost (honest)
Deterministic layers + corpus reuse = **$0/offline**. LLM tiers via local CLIs / agent-bridge — no metered API (agent-bridge is human-babysat). Biggest real cost = **re-verification**: rewriting 8 LOCKED shorts + re-panel (authoring + review time), per-short audio (~$0–$3), long-form caption/timing re-runs. I quote metered spend before running.

## Sequencing
Chokepoint skeleton + **A** (parser → ported+strengthened freshness check → acceptance test) → prove A3 on the real 8 → **B** (audit → corpus witness → punctuation-strict ref check) → **C** (one verify CLI → backfill via chokepoint → regression) → **D** deferred. A3 gates B/C.

## Review discipline
Plan: v1→REVISE, v2→PASS+REVISE, v3→REVISE (execution specs), **v4 = reuse-first** per user. One optional confirm-panel on v4, else build. Implementation: red-team + 5-CLI panel before done; re-verified narrations re-lock through the gauntlet.

## Implementation Contract (the v4 panel's execution specs — resolved in code)

1. **Real reuse, not copy-paste.** Make `short_gate`'s `kjv.py` + freshness core importable (shared `sys.path`/package) and add strict-mode + new fingerprints as **extensions/parameters**; OR if vendored, add a **provenance record + an equivalence fixture test** that runs the source and local functions on the same inputs and asserts behavioral parity (documenting strict-mode deltas). No silent fork. (gemini, codex, grok, cursor.)
2. **KJV marker handling (flagship Ps 22:7 case).** Reuse the existing `norm()` brace logic — it already removes notes `{…: …}` (e.g. `{shoot…: Heb. open}`) and **keeps supplied-word italics** `{saying}` → `saying`. Strict mode = that brace handling **minus** the punctuation-stripping, so the comma is compared. Ps 22:7 is a hard regression fixture. (codex.)
3. **Fix the input, not just the lock.** Redirect `pipeline/scripture.fetch_kjv` / `pipeline/kjv_check.py` off `data/kjv_cache.json` to the witnessed corpus (read via `JESUS_KJV_CORPUS`, don't fork a stale copy). (claude.)
4. **Quote classifier.** A1 classifies each quoted span: **tagged KJV block** (must verify, BLOCK on fail), **inline spoken KJV echo** (best-effort ref + verify), **narrator rhetoric** (e.g. `"that the scripture might be fulfilled"` — not a KJV claim, not blocked), **non-spoken ledger quote** (ignored). Only KJV-claimed spans hit the BLOCK-on-unverified path — resolves the A1↔B3 contradiction. (codex, cursor.)
5. **Lock enforcement, honestly scoped.** Implement the `.locked` + spoken-hash check inside `handoff.run_audio_pipeline` first; **enumerate and guard every owned audio/caption/assembly/alignment entry** (`runner.py`, `_finalize.py`, `_fix26_audio.py`, `cli_assemble.py`/`orchestrator` reusing `narration.mp3`, `assembly_align` reusing `narration.alignment.json`, `veed_io` caption). For the foreign `per_turn_synth`/`narration_pipeline` (`--no-gate`, manifest-absent skip): a **this-repo pre-flight wrapper refuses to launch them without a current `.locked`**. Drop the word "non-bypassable"; state the residual direct-invocation bypass explicitly. (codex, cursor, grok.)
6. **`.locked` hash binds the RENDERED text.** Hash the A1-parsed spoken content of `narration-tagged.md` (what synth/captions consume), and validate tagged-vs-narration parity at lock — not just raw `narration.md`. (codex, cursor.)
7. **Registry authority = rebuild-from-disk.** The on-disk `.locked` snapshot set is the source of truth (glob `.locked`, not `narration.md`); append is a cache. Include the **in-flight batch atomically** (a fresh set of 8 rewritten shorts must be compared against each other, not only prior locks). Idempotent, self-excluded, slug-keyed. (codex, gemini, grok.)
8. **No false-lock window.** `cli_lock.py` must not write `.locked` until B3 punctuation-strict + the quote classifier are live (no skeleton that certifies before the real KJV check exists). (cursor.)

## Deliberately NOT doing
- No editing/duplicating `short_gate`, `per_turn_synth`, `narration_pipeline`, `image_to_kling` — port proven logic into this repo, wrap, reuse.
- No change to locked doctrine, Gospel Five-Beat, CTA-to-Jesus.
- No auto-rewrite of locked narrations — flag; user approves each.
- No full-Bible canon build; no forcing hand-authored/long-form into five-beat gates; no model-ID switches.
