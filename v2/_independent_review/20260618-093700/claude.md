# Independent review — claude (OK, 119s)

I've verified the plan against the codebase. Findings below cite exact files/claims.

## Findings

**1. The central "teeth" has no mechanism (§3, §7 CLIP-ELEMENT-GATE).** The plan's load-bearing claim is *"sampled frames' detected object classes must be ⊆ locked element set (no new object class)."* But `pipeline/clip_qc.py` has **no object detector and no LLM judge** — it only does `extract_frames()` + `record_verdict()` (a boolean written by an external agent) against qualitative prose `CRITERIA` (frozen / no-morph / on-scene / period). There is no code, and no Claude-Vision capability, that returns a *canonical, stable taxonomy of "object classes"* you can do set-subset math on. A Baroque crop contains dozens of describable things (tear, cheek-shadow, cloth-fold, highlight); whether "a faceted gem on a wound" is a *new object class* or "a glint already inside element `wounds`" is a judgment call, not `⊆`. The `⊆` framing is **pseudo-rigor dressed as a deterministic gate.** This is the whole point of the spec and it's the least specified part.

**2. Internal contradiction: "one beat per phrase" vs. the count math (§1 B vs §2).** Step B says *"one beat per narration phrase."* §2 gives `#03`: 127 words → **11 stills**. 127 words is ~25–35 phrases, not 11. The `beat_board.json` example (§4) shows phrases mapped 1:1 to stills, which can't both be true. Pick one: stills map to *grouped* beats (~2–3 phrases each), and fix step B.

**3. Reuse-first is blocked by its own manifest rule (§6 vs the existing library).** §6 says a reused clip *"carries its own already-locked manifest (it was verified when made)."* The **125 clips already in `clip_library/index.json` have no manifest** — they predate INV-25. So the "default cost lever" (§6, §10 "near-$0 … reuse-first") **cannot fire on any existing clip** until every one is back-filled, OR the gate must exempt legacy clips. The plan never mentions backfill or an exemption. This is a single point of failure for the cost story.

**4. The plan edits a reused, externally-owned pipeline (§9 step F).** Step F: *"image_to_kling cut-planner … consume the manifest."* `image_to_kling.py` lives in `PythonProject1/jesus/` and CLAUDE.md's locked rule is *"Reuse downstream pipelines, do not duplicate … subprocess'd, not re-implemented."* Threading a manifest into it means either modifying the external tool or passing it via env/file like `KLING_SKILL_PATH`. The plan hand-waves this as "surgical" — it's the riskiest integration and crosses the reuse boundary. Name the mechanism.

**5. Wrong file paths / stale counts.** `clip_library.py` is at `clip_library/clip_library.py`, **not** root (§9 says "`clip_library.py`"). The sidecar is `<stem>.png.coherence.json` (`pipeline/coherence.py:47`), not `coherence.json` (§3). Library is **125 entries**, not "115" (§6); memory says 34 neutral-reusable — so the reusable pool is far smaller than "115 clean-reusable" implies. INV numbering jumps to 25 but `v2/SPEC.md` runs INV-1..22 — INV-23/24 unaccounted (§8).

**6. No retry bound → unbounded re-render spend (§3, §7).** "A still cannot LOCK unless every declared element reconciled … else it re-renders." No max-retries, no fallback. A declared element vision keeps failing to confirm (e.g. "anguished eyes searching the dark" is subjective) = re-render loop at $0.30–0.50 each. The escape valve ("human-cut the element") isn't wired as a default.

**7. `region` is declared but never enforced (§3).** Each element carries `"region":"center-left"` but nothing checks the cut-planner's crop actually landed there, nor that vision confirmed the element *is* in that region. It's decorative metadata that looks like a constraint.

**8. Over-built before the idea is proven (§8, §10).** 4 invariants + 2 new artifacts + 7 gates + 8 code-site changes — all built in step 1, *then* proven on #03 in step 2. The user's actual insight is smaller: **declare → render → vision-verify → lock → edit only to verified elements.** That core (and #1's mechanism) is what needs proving on #03 first. Beat-board ordering, scale-to-length math, and reuse-manifest are separable and could follow. Prove the spine on one short before specifying INV-25..28.

**What's genuinely good:** `png_sha256` binding the lock (catches silent re-renders) is right; gating everything behind `JITB_REQUIRE_*` + a green regression mirrors the proven coherence rollout; keeping the locked Kling hard-cut recipe and the "close on Christ / never-animate-writing / no-within-cut-reuse" carries is correct; declaring the element list *before* rendering the still (so the still is painted to support the tour) is the real fix and worth doing.

VERDICT: REVISE
TOP FIXES:
1. Specify the actual mechanism for CLIP-ELEMENT-GATE (§3/§7) — there is no object-class detector in `clip_qc.py` and Claude Vision yields no stable taxonomy for `⊆` math. Define it as a vision *judgment* ("does any frame show an object not described by the locked elements? fail-closed") and prove it discriminates on #03's known-bad frames, or drop the set-subset framing.
2. Resolve the manifest-vs-reuse deadlock (§6): the 125 existing library clips have no manifest, so reuse-first can't fire — add a legacy exemption or a backfill step, and fix the "one beat per phrase" vs "11 stills" contradiction (§1 B / §2).
3. Cut scope to prove the spine first (§10): build only declare→verify→lock→element-gated-edit on #03 before committing INV-25..28, the beat-board math, and edits to the externally-owned `image_to_kling.py` (§9 F) — name how the manifest reaches that subprocess.
