# Independent review — cursor (OK, 123s)

## Independent adversarial review — AWAKEDEN RELEASE PLAN (v1)

Direction is coherent and several round-1 fixes are real improvements. Against the **actual repo**, though, Phase 0–1 would still hit hard blockers if executed literally. Skepticism warranted.

---

### Feasibility vs. real codebase / tools

**§6 + Phase 1 step 6 — `/upload` + `/publish` on batch shorts will fail today.**

The plan says: *"Every release goes through the existing gate machinery: `/upload` … → `/publish`"* and *"Publish Cross shorts Mon/Wed/Fri via /upload + /publish"*.

`cli_publish.py` expects a **v2 short folder** with `narration.creation.json` and finished video under `assembly/viral_cut_*_captioned.mp4`:

```109:111:pipeline/upload_engine.py
def harvest_facts(media_dir: str) -> SourceFacts:
    d = Path(media_dir).resolve()
    creation = json.loads((d / "narration.creation.json").read_text(encoding="utf-8"))
```

```80:90:pipeline/upload_engine.py
def _find_video(media_dir: Path, fmt: str) -> ...
        a = media_dir / "assembly"
        cands = [
            a / "viral_cut_sfx_music_captioned.mp4",
            ...
```

Cluster-1 living-page pieces live under `batches/cluster_01_cross/<slug>/` with `narration.md`, `audio/alignment.json`, and scored output at `visual/<slug>_scored.mp4` (per `_CLUSTER1_ROLL_REVIEW.html`). There is **no** `narration.creation.json`, **no** `assembly/`, and **no** wiring in `upload_engine` / `publish_pack` for batch paths. Phase 1 step 6 assumes tooling that does not yet accept this artifact layout.

**§7 — Read-page generator underspecified vs. real spec shape.**

*"walks a piece folder (`livingpage_short.spec.json` … + `visual/*.png`)"* — the spec uses **clip slugs** and relative audio paths, not a flat `visual/*.png` directory:

```1:5:batches/cluster_01_cross/pierced_zech1210/visual/livingpage_short.spec.json
{
 "_doc": "PIERCED (Zech 12:10) 9:16 SHORT - living-page pilot...
 "audio": "../audio/narration.mp3",
 "total": 59.04,
```

Stills resolve through anchors/asset index, not a simple PNG glob. Also **1/8 banked pieces** (`father_forgive_them`) uses `mocomic.spec.json` / `mocomic_v2.spec.json`, not `livingpage_short.spec.json` — contradicts §12’s *"exists in all 7 cluster-1 pieces"* (roll review lists **8** shorts, not 7).

**§6 — brand/footer prerequisites not in Phase 0.**

`data/upload_brand.json` is still `FILL_ME` for channel, handles, and website. UK-G4 footer stamping will produce broken or empty copy until Phase 0 explicitly fills Awakeden handles — not listed alongside step 3 “YouTube channel dress.”

**§5 analytics loop references files and code that do not exist.**

*"append … to `data/learning/yt_analytics.jsonl` → feeds the C0 gate weights"* — repo has `data/learning/freshness_registry.json`, `calibration.jsonl`, etc., but **no** `yt_analytics.jsonl`. C0 in `LIVINGPAGE_STANDARD.md` is `narration_gate.py` (earned hook/landing); nothing in codebase connects YouTube retention to “C0 gate weights.” This is a named step with no implementation path.

**§7 Plan tracker vs. existing site pipeline — duplicate truth.**

*"auto-built from `batches/batch_manifest.json` + `asset_index.json` + … `publish_log.json`"* — `_website/build_catalog.py` already builds from **`manifest.yaml`** + `config.yaml`. `publish_log.json` does not exist. `_website/` has no references to `batch_manifest`. Introducing a second generator without a merge/sync rule will drift from the live catalogue.

---

### Hidden risks / false assumptions / SPOFs

**§5 vs Phase 1 step 7 — launch runway contradicts itself.**

§5 hard rule: *"≥3 weeks … (≥9 shorts + the current month's long) BEFORE launch"*. Phase 1 step 7: *"otherwise month 1 ships shorts only — cadence over crunch"*. Those cannot both be launch gates. EW07 Isaiah long is `"visual not built"` in `batch_manifest.json`; month-1 long is a schedule risk the plan partially acknowledges but does not reconcile with the runway rule.

**§4 + Phase 0 step 2 — “~6 remaining” vs. runway math.**

With **8 banked**, runway needs **≥9** → **one** more finished short minimum, not six. Building six before launch adds ~$18–30+ and weeks of delay unless the goal is full cluster completion, not launch readiness. `_CLUSTER1_ROLL_REVIEW.html` also notes manifest duplicates (*"thief on the cross"*, *"It is finished (last week)"*) were **not** built — the true remaining unique count may be **~4**, not ~6.

**§5 A/B discipline — hidden production multiplier.**

*"cut two hook variants … publish the loser lane on TikTok only"* — uncontested hooks are fine, but contested hooks **double** narration/audio/choreography work. No cost line or bank rule for variant pieces; under solo-operator cadence this is a silent schedule killer.

**§6 cross-post assumption.**

*"native captions already burned in"* — living-page scored MP4s may include captions, but `/publish` still expects `captions.srt` from `*.words.json` beside assembly outputs (`publish_check.py`). Even with burned-in video, the GREEN gate can FAIL without a words.json path or an explicit exception for living-page layout.

**§12 — governance SPOF.**

*"Round 2 pending … do not LOCK on round 1"* with degraded 2/5 panel — plan is explicitly pre-quorum. Treating this as release-authoritative before round 2 repeats the failure mode the project’s own INV-9 rule exists to prevent.

**§11 solo-operator burnout — understated.**

Phase 0 packs: 6 builds + channel dress + `publish_log` schema + website tracker + Read-page generator + deploy + panel round 2 — **same week** as finishing launch bank. Phase 2 adds Resurrection **~13 shorts** from Jonah long **while** publishing 3/wk. No explicit time budget or “slip schedule” trigger beyond gates.

---

### Over-engineering / premature build

**§7 Read-pages v1 in Phase 0 week 0** alongside tracker, while Phase 1 publishes with *"descriptions link Read-pages"* — if Read-pages slip, launch copy points at 404s. Safer: tracker + stub Read URLs, or delay YouTube descriptions linking Read until generator is live (plan does not sequence this).

**§5 → Phase 2 step 11 analytics → C0 weights** before any published data exists — building a feedback loop into gate weights before first week of analytics is premature; manual hook notes in a spreadsheet would prove the loop first.

**Website “identity refresh” + Plan page + Read generator** in Phase 0 while only 8 pieces exist — reasonable as user decision, but scope is large for week 0 relative to the stated launch gate.

---

### Missing steps / verification gaps

- **No handoff step** from `batches/cluster_01_cross/<slug>/visual/*_scored.mp4` → publish-ready folder (symlink, copy, or `upload_engine` extension).
- **No `corpus_diversity.py` invocation** in Phase 0–1 despite §4 *"Corpus-diversity gate runs per BATCH"* — tool exists at repo root; release plan never says when to run it before publishing Cluster 1.
- **No caption/words.json path** for living-page outputs in publish checklist.
- **No email provider** named (step 7 *"simple provider embed"*) — signup metric in §1 success metrics is unimplementable as written.
- **Phase numbering error**: Phase 2 step 9 vs Phase 3 step **10** (duplicate “10.”) — sloppy execution doc for something that governs cadence.
- **No verification** that `cli_publish.py` / `publish_check` pass on **one** cluster-1 piece end-to-end before launch (standing project verify: believe the gate, not memory).

---

### Reuse

Good: routes through existing `/publish`, `_website/build_catalog.py`, `corpus_diversity.py`, `batch_manifest.json`, living-page skill chain.

Bad: proposes **`build_readpage.py`** without checking whether `build_catalog.py` + manifest entries could expose Watch embeds first (lower lift). Proposes **`publish_log.json`** parallel to `manifest.yaml` `public_status` — duplicates status tracking instead of extending one source.

`/upload` + `/publish` in §6 is redundant; publish skill already folds upload — minor, not blocking.

---

### Cost / spend justification

**§3 ~$4–5/short** is supported by cluster-1 roll ledger (~$31–32 / 6 ≈ $5.30) — credible **for net-new living-page shorts with reuse**.

Underestimates:
- Hook-variant A/B (§5) — up to 2× per contested piece.
- Phase 0 website + Read generator — engineer time, not metered, but competes with builds.
- **`upload_engine.generate` LLM call per piece** on first `/publish` run — not in §3 cost table.
- **Living-ministry Christ ref** (§4 item 5, §8) — correctly flagged as blocker for 24 shorts; no dollar estimate or pre-flight, yet Phase 2 step 10 starts it “in parallel” with Cluster 3 harvest.

**§8 style reuse risk:** `batch_manifest.json` `style_note` warns banked Cross clips are **baroque-oil** while plan positions **inked graphic-novel** universe (§2). Reuse economics assume visual coherence; mixed-style reuse may force re-renders not in the $3–4 curve.

---

### What the plan gets right (brief)

Runway fix (≥9 not 8), hook-level A/B instead of Shorts thumbnail A/B, long-first Jonah moved off launch crunch, Read-page CSS honesty (§7), doctrine/gate non-negotiables (§9), measured vs legacy $23 note (§3) — these are real improvements over a naive release doc.

---

VERDICT: REVISE
TOP FIXES:
1. Add an explicit **batch → publish adapter** (extend `upload_engine`/`publish_pack` for `batches/cluster_01_cross/*`, or document a one-time folder normalization) and prove **`publish_check` GREEN** on one living-page short before Phase 1 step 6.
2. **Reconcile launch gates**: either drop “≥9 shorts + current month's long” or drop “month 1 shorts only”; define minimum bank as **9 finished publish-ready shorts** (likely **one** build, not six) plus a clear long policy for month 1.
3. **Remove or implement** the §5 analytics loop: create `yt_analytics.jsonl` + a real consumer, or defer “feeds C0 gate weights” until post-launch; fill **`upload_brand.json`** and wire Read-page URLs only when pages exist.
