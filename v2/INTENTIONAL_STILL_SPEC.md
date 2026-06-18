# SPEC — Intentional Still + Element-Gated Edit (Visual v3) — **v2 (post-review)**

> **Status: REVISED DRAFT (2026-06-18).** v1 was red-teamed by 3 internal hostile
> reviewers + the external 5-CLI panel (cursor/claude/codex returned **REVISE**;
> grok hit max-turns, gemini timed out — a degraded 3/5 panel). **All 6 returning
> reviewers said REVISE.** This v2 folds in every convergent finding. The headline
> change they all demanded: **prove the risky spine on #03 FIRST**, before building
> beat-boards, new invariants, assembly rewrites, or touching the external
> `image_to_kling`. Reviews archived at `v2/_independent_review/20260618-093700/`.
>
> Redesigns Stages 2–3 of `v2/SPEC.md`. INV-25..28 are promoted into `v2/SPEC.md`
> **only after Phase 1 proves on #03.**

---

## 0. The problem (tightened after review)

Reviewers corrected my v1 overstatement. `verify_image()` already runs a 6-check
Vision audit (subject_block · visible_elements · vignettes · period · reverence ·
anatomy), and `coherence_gate.py` adds the F1–F5 default-PASS still gate. So it is
**not** true that "nothing checks the still." The **real** gaps are narrower and
specific:

1. **No per-element ID binding for the gallery tour.** The cut-plan names elements in
   free prose; nothing ties "cut to the wounds" to a verified thing in *this* painting.
2. **No post-animation check that the clip invented nothing.** The gem-on-a-wound,
   garbled text, extra figure — all slip through because no gate looks at the *clip's*
   frames against a known element set.
3. **Still / edit / assembly live in silos**, so a still isn't composed to support a
   clean tour, and the jigsaw speeds clips arbitrarily at the end.
4. **The visual story isn't designed to the narration, in order.**

**The fix is a verified element contract + narration-ordered design — but built
spine-first and calibrated, not as a big-bang stack.**

---

## 1. Guiding principle (the unanimous review note)

> Build and PROVE the one risky hypothesis on #03 before anything else:
> **can a manifest-bound, element-only cut-plan make Kling tour a painting
> without inventing new things — and can an automated gate reliably catch it
> when it does?**

Everything else (beat-board math, scale-to-length, reuse-first, the 4 invariants,
the assembly rewrite) is **separable and deferred to Phase 2**, after the spine works.

---

## 2. PHASE 1 — the spine (build + prove on #03 only)

```
A. DECLARE   Compose the still per the constitution FIRST (arc · mix · vignette-as-
             theology · anti-cliché). THEN derive its element list — the things the
             finished painting must contain to be both theologically complete AND
             tourable. Stored by PROMOTING the existing Scene.macro_elements into
             {id, label, region?} (NOT a new parallel schema).
B. RENDER    Render the still (direct path; provider per the locked split).
C. RECONCILE EXTEND verify_image (one vision pass, not four stacked gates) to also
             confirm each declared element is present and mark it verified:true/false,
             and to set the period/reverence verdict from its existing checks + the
             constitution's T1–T6 guardrails. Write the manifest as an EXTENSION of the
             coherence sidecar, png_sha256-bound via coherence.is_verified.
             POSTURE: default-PASS on the subtle (faces, "anguished eyes"); a missing
             declared element → CUT IT FROM THE TOUR (default), do NOT auto-re-render;
             fail-closed ONLY on a clear defect (modern/horror/NSFW/broken-anatomy/
             dominant-garbled-text). Calibrate against blind human labels before trust.
D. EDIT      The agent cut-planner (the existing .agent_bridge servicer / SKILL via the
             KLING_SKILL_PATH env — we DO NOT modify the externally-owned
             image_to_kling.py) builds the gallery tour from VERIFIED element IDs ONLY.
             A deterministic validator (extend validators.gate_cutplan) REJECTS any beat
             whose description names a noun not in the manifest's verified elements.
E. RENDER    Animate via the locked hard-cut recipe (frozen tableau, camera-only).
F. GATE      THE ELEMENT GATE = a fail-closed VISION JUDGMENT (NOT object-class set math —
             see §3): "does any sampled frame show a clear object NOT described by the
             locked elements (a gem, an extra figure, text, a modern prop)? → FAIL."
             k-vote + content-hash pooling (like INV-23) for determinism; default-PASS
             on low confidence; reject = gate ∪ human flag.
```

**Acceptance criteria for the #03 proof (explicit — reviewers demanded this):**
- The element gate must **FAIL the known-bad frames** (e.g. the gem-on-wound clips in
  RESUME) and **PASS the good ones** — measured, with the bad frames saved as fixtures
  in `pipeline/validation_fixtures/`.
- A defined regression command runs the new deterministic pieces green.
- Human sign-off (by ear + eye) is the *final* gate, not the *only* one.

---

## 3. The element gate mechanism (the central fix — was "unbuildable" in v1)

**v1 said:** "each frame's detected object classes must be ⊆ the locked element set."
**Every reviewer killed this:** the repo has no object detector; Claude Vision yields
no stable taxonomy; a Baroque crop has dozens of describable things; `⊆` is pseudo-rigor.

**v2 mechanism — a calibrated vision *judgment*, not set math:**
- Per clip, sample N frames (N defined, default 5; reuse `clip_qc.extract_frames`).
- One vision call per frame (or one multi-image call) asks a **single fail-closed
  question:** *"List anything in this frame that is a distinct object/figure/text NOT
  described by this element list: [labels]. If you find a clear foreign object (gem,
  extra person, legible/garbled text, modern item), FAIL; if only the listed elements
  and their natural paint detail are present, PASS. When unsure, PASS."*
- **Determinism:** k-vote, pool votes by content hash (INV-23 pattern), default-PASS.
- **Calibration FIRST:** label #03's frames blind, tune the threshold to the human bar
  before flipping the gate on — the exact lesson from the coherence gate's precision-0.08
  over-strict failure (`feedback-gate-calibration-human-authority`).
- Lives as a new check in `clip_qc.py` (or a small `clip_element_gate.py`), recorded in a
  fail-closed sidecar. **Note:** `clip_qc` today is *manual* (no automated frame-diff);
  automating CLIP-FROZEN/NOMORPH is a separate small build, not "(exists)" as v1 claimed.

---

## 4. PHASE 2 — expand (only after Phase 1 proves on #03)

- **Beat board is a PRIOR, not a replacement.** It feeds the agent jigsaw; the jigsaw
  stays **agent-only** (locked in `v2/SPEC.md`) and owns the final order, because meaning
  overrides scene index (#03's shipped cut already runs 5→7→8→6). The board gives order +
  roles + target seconds as a strong default the jigsaw refines.
- **Scale-to-length, PUNCHY by default** ([[feedback-always-punchier]]). Target **many distinct
  moments** — `target_stills = clamp(round(sec/3.5), 10, 24)` (≈ one moment per 3–4s, NOT 5s) —
  and **speed the clips up** to land each on its beat. `n_hero = ceil(target/2)` (includes the
  mandatory **hook-open** + **hero-bookend**), `n_multi = floor(target/2)`. Min internal cut ≥0.6s.
- **Backfill-to-punchy is the RULE, not optional.** Never ship a slow/long-hold cut: if a cut comes
  out thin/slow (AS-G9 long holds / high avg slot), **backfill more clips** — reuse-first from
  `clip_library` (element-gated by eye first; `reuse_swap` can create empty slots), create new only
  on no clean fit — until the pace is punchy. Fast cuts also cover *minor* flaws; HORRIBLE clips
  (gloves/modern-dress/gems/garbled-scrolls) are still deleted, never speed-hidden.
- **Graduated mix + passage-tone bias** [decision B]: use the constitution's mix table
  keyed to scene count (not flat 50/50); bias intimate/dereliction passages (like #03)
  toward hero singles; keep only the binding ≥1 NT-gospel-link + close-on-Christ.
- **Ambient layer + variety** (so clips aren't a uniform slideshow): the manifest may
  carry an allowlisted `ambient_layer` (period-plausible atmospherics — dust, smoke,
  shifting light, fabric stir — NOT new figures/objects/text) that the element gate does
  NOT punish. Carry `viral_role`/`pacing` into the cut-plan: **the hook-open clip is
  EXEMPT from the leisurely tour** (one bold arresting beat), ≥3 distinct cut-shapes
  across the cut (mirrors SP-G8 framing variety + the cliché blocklist + Jaded-Scroller).
- **Reuse** [decision A]: loose clip-reuse (speed-to-fit) is restricted to
  **ambient/establishing/topic-neutral plates** (via `clip_reuse.py`, with a speed-cap +
  ear-review). For hero/story beats, reuse the **still** and **re-cut the motion fresh**
  ($0 agent-mode; only Kling render costs) — protecting the locked "each clip matches its
  phrase" rule (`feedback-no-reuse-beat-match`). Counts corrected: **125 clips, ~34
  clean-reusable** (not "115"). Reuse routes through `clip_reuse.py`, not raw
  `clip_library.find`.
- **Reverence speed-cap** carried onto the sacred/Christ close (exempt from speed-to-fit).

---

## 5. Backfill + rollout (was an unreachable flip in v1)

The flip precondition ("all shipped shorts carry manifests") was unreachable — legacy
stills/clips never had a declared list. Fix:
- **Backfill manifest** per legacy still/clip: vision emits the element list FROM the
  render (`declared_by:"backfill-vision"`, so the declared-vs-real diff is skipped but
  period + coherence still run), png_sha256-bound, flagged `provenance:"legacy"`. This
  satisfies the flip precondition and unblocks reuse-first on the existing bank.
- Flags (`JITB_REQUIRE_ELEMENT_GATE`, etc.) default **OFF** until: backfill done +
  green regression + the gate calibrated. Same discipline as `JITB_REQUIRE_COHERENCE`
  (still OFF — sequence this AFTER that debt, don't stack a fifth gate first).
- **Re-lock path:** an approved re-render recomputes png_sha256, re-runs reconcile +
  period, rewrites the manifest with a bumped `lock_version` + `approved_by`/timestamp.
  A PNG whose bytes don't match the hash with no lock-version bump = tamper, fail-closed.

---

## 6. Resolution ladder — the NBP-gem money-pit fix (INV-20)

v1 had no retry ceiling → the wound-renders-as-a-gem-every-time loop would burn money.
Defined ladder:
```
STILL-RECONCILE / element fail →
  retry ≤2 (same provider)
  → switch provider NBP↔HF ≤1
  → quarantine the still, then EITHER
       (a) human-cut the element AND re-validate the beat role
           (a hero dropping below 4 verified elements is demoted to multi-story
            or the beat is re-designed), OR
       (b) drop the beat and recompute target_stills.
Max 4 PAID renders per still; beyond that requires explicit user OK (INV-20).
Every render logged to data/spend_ledger.jsonl.
```

---

## 7. The manifest — extend the coherence sidecar (single name, no parallel stack)

One artifact, one name: `visual/<provider>/<stem>.png.coherence.json` **extended** with
the manifest block (do NOT introduce `element_manifest.json` / a 3rd sidecar — reviewers
flagged three names for one thing as a guaranteed wiring bug; and `cut_hint.json` is
already *unread* by the live Kling path — don't add another unread file).

```jsonc
{
  // … existing coherence fields (audited, passed, png_sha256, votes) …
  "manifest": {
    "subject_type": "hero",                  // hero | multi-story
    "role": "hook-open",                     // hook-open | hero | multi-story | hero-bookend  (beat-board view; must agree with subject_type)
    "elements": [
      {"id":"full",  "label":"the crucified face lifted to a dark sky", "region":{"box":[0,0,1,1]}, "verified":true},
      {"id":"mouth", "label":"the open, crying mouth",                  "region":{"box":[0.35,0.45,0.3,0.25]}, "verified":true},
      {"id":"crown", "label":"crown of thorns on the brow",             "region":{"box":[0.3,0.1,0.4,0.2]}, "verified":true}
    ],
    "ambient_layer": ["faint drifting dust", "slow shadow shift"],  // allowlisted atmospherics; element gate ignores
    "period_real": {"T1":"pass","T2":"pass","T3":"pass","T4":"pass","T5":"pass","T6":"pass"},  // constitution guardrails by ID, NOT vague booleans
    "declared_by": "design",                 // design | backfill-vision
    "provenance": "fresh",                   // fresh | legacy
    "lock_version": 1,
    "locked": true
  }
}
```

`region` is an **advisory** normalized box `[x,y,w,h]` the agent cropper MAY use; in
Phase 1 it is not a hard gate (no deterministic region-enforcer exists yet). For
multi-story sub-vignettes, vision emits a tight bounding box; a vignette that can't be
bounded to ≤40% of the frame fails reconcile.

---

## 8. Integration — extend, don't parallel (honest §9)

| Step | Real change | Honest size |
|---|---|---|
| Declare elements | **promote** `Scene.macro_elements` → `{id,label,region?}` in `visual_models.py` | small add |
| Reconcile + manifest | **extend** `verify_image` (`visual_render.py`) to mark per-element verified + write the manifest block | medium (schema change to ImageAudit) |
| Period via T1–T6 | surface the EXISTING `verify_image` check-6 + `coherence_gate` F1/F3 as the manifest `period_real`; **don't stack a 4th gate** | small |
| Element-gated edit | the `.agent_bridge` servicer / `KLING_SKILL_PATH` SKILL consumes the manifest; **inject via env/file — never modify the externally-owned `image_to_kling.py`** | medium |
| Cut-plan validator | extend `validators.gate_cutplan` to reject beats naming non-manifest nouns (deterministic, unit-testable) | small |
| Element gate | new vision-judgment check in `clip_qc.py` (+ k-vote/hash-pool) + fixtures | **net-new (the spine)** |
| Beat board (P2) | `discover_scenes` already takes `timeline`/`beat_coverage`; emit an ordered board as a **prior** to the agent jigsaw | net-new artifact |
| Assembly order (P2) | route through `v2/servicers/assembly_servicer.py` + `assembly_runner` + `lock.require_visual_coherence` (the LIVE path — v1 omitted these); board is a prior, jigsaw stays agent-only | medium |
| Reuse-first (P2) | via `clip_reuse.py` (not raw `clip_library.find`); + backfill | medium |

Naming/path corrections from review: module is `clip_library/clip_library.py`; sidecar
is `<stem>.png.coherence.json`; library is **125 / ~34 clean**; INV numbering continues
at **25** (INV-23/24 already exist for coherence/no-fabricated-verdicts).

---

## 9. Honest cost (v1's "near-$0" was false)

- Vision reconcile + the element gate run via the **agent bridge = hand-serviced
  requests** today. #03 ≈ 11 stills × (reconcile) + ~11 clips × ~5 frames (gate) ≈ **dozens
  of bridge calls**. **Therefore: land the image-audit fan-out Workflow (already scoped in
  RESUME) FIRST** to relieve the toil, or batch frames into one multi-image call.
- Kling re-rolls on a gate fail cost ~$0.65 each; gap stills $0.30 (HF) / $0.50 (NBP).
- **Quote the spend and ask before any batch render (INV-20).** Building + the #03 proof
  is low-$ (reuse + existing renders) but **not $0** — say the real number.

---

## 10. Open reconciliations to fix in `v2/SPEC.md` (surfaced by review)

1. **Animation provider — RESOLVED 2026-06-18 by a bake-off (decision A):**
   **HF Kling pro is the shorts default; direct-Kling is the fallback ONLY for
   NSFW/bare-torso stills HF refuses.** Evidence (`_bakeoff/compare.html`, same still +
   byte-identical prompt + 5s): HF rendered **1076×1924** and stayed faithful; direct-Kling
   rendered **716×1284**, was ~3× cheaper / ~6× faster, but **hallucinated a garbled
   "BINTX" titulus not in the painting** on the wide scene — the exact defect this spec
   exists to kill. Quality + faithfulness > cost for the first-class product.
   **Action:** update `v2/SPEC.md` + `config.py` (which still say direct-Kling default)
   and the CLAUDE.md locked-decision block to this split.
2. **SP-G1..G9 + cohesion** assume a 14–20 scene pool; scale-to-length 6–20 stills needs
   those gates updated, not bypassed.
3. Sequence INV-25..28 **after** the still-coherence rollout debt (INV-23/24 flags still
   OFF), not before.

---

## 11. New invariants (promote into `v2/SPEC.md` §5 ONLY after Phase 1 proves) — all *(rollout-gated)*

- **INV-25 — Element-manifest contract.** Every still carries a png_sha256-bound,
  vision-reconciled, locked element list (an extension of the coherence sidecar). The
  edit may target only verified elements; a deterministic validator rejects non-manifest
  cut targets; the clip element gate is a calibrated, default-PASS vision *judgment*
  (not object-class set math). *(rollout-gated)*
- **INV-26 — Narration-ordered design.** Stills are designed to the narration via a beat
  board (grouped beats, scale-to-length, graduated mix + tone-bias, mandatory hook-open +
  Christ-close bookends) that is a **prior to** the agent-only jigsaw, not a replacement.
  *(rollout-gated)*
- **INV-27 — Period + reality, by checklist.** Each still's `period_real` is the
  constitution's T1–T6 guardrails verified item-by-item (not vague booleans), human-
  calibrated before enforced. *(rollout-gated)*
- **INV-28 — Reuse-first, neutral-only loose.** Query the catalogue (via `clip_reuse.py`)
  before rendering; loose speed-to-fit reuse is limited to topic-neutral/ambient plates;
  hero/story beats reuse the still and re-cut; legacy assets are backfilled or exempt;
  never reuse a clip twice in one cut. *(rollout-gated)*

---

## 12. Decisions resolved (2026-06-18)

- Edit unit = **5 cuts inside ONE clip.**  ·  Count = **scale to length** (~1 still/5s, 6–20).
- **A — Reuse:** loose clip-reuse **only for neutral/ambient plates**; hero/story beats
  reuse the **still** + re-cut fresh. *(adopted, overrides v1 "reuse all clips loosely")*
- **B — Mix:** **graduated** (constitution table) + **tone bias** toward hero singles for
  intimate passages. *(adopted, overrides v1 flat 50/50)*
- Element list = **declare → render → vision reconcile → LOCK**, as a **calibrated
  judgment**, default-PASS, with a retry ceiling.
- Mapping = **beat board (grouped beats) as a prior + agent jigsaw owns final order +
  hook-open & Christ-close bookends.**
- Rollout = **spec → build & prove the SPINE on #03 → then Phase 2 → then batch.**
- Carried forward: close on Christ · biblical-period/reverent (T1–T6) · no within-cut
  reuse · reverence speed-cap · never-animate-writing · cliché blocklist/Jaded-Scroller.

---

## 13. Proof plan (#03 The Forsaken Cry) — spine first

1. Build Phase-1 pieces only: promote macro_elements → manifest; extend verify_image to
   reconcile + write it; agent cut-planner constrained to manifest IDs + the deterministic
   validator; the calibrated element gate + #03 known-bad fixtures + regression command.
2. Run #03 through the spine end-to-end; **calibrate the element gate against your blind
   labels**; confirm it fails the gem frames and passes the good ones.
3. **You sign off on #03** (by ear + eye) AND the gate's measured discrimination.
4. Only then build Phase 2 (beat board, scale-to-length, graduated mix, reuse-first) and
   batch the remaining shorts. Quote spend + ask before any batch render.
