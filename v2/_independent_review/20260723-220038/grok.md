# Independent review — grok (OK, 173s)

I'll review this plan adversarially against the real codebase — reading the full artifact first, then checking the claims it makes about tools, paths, and wiring.Key claims need verification — `_retro_dna` may be missing, and the model recipe may still conflict with `STATE.md` / `RESUME.md`.Checking path claims, remaining contradictions, and pilot cost grounding against the real EW01 tree.# Independent adversarial review — AWAKEDEN COMIC DNA v0.3

Default: skepticism. Verified against the repo, not the doc’s self-score.

---

## What improved (briefly, then the problems)

Round-1 Seedream-as-identity false claim is correctly retracted. User choice of HF `nano_banana_pro` is explicit. Pilot is ONE piece (EW01), A/B is between-subjects, `/dna-check` is not oversold as pure $0, and `VISUAL_BANNED_TOKENS` + `render_scene(..., extra_ref_paths=)` exist in code. That is real progress.

It is still **not an executable production plan**.

---

## Critical findings

### 1. Top-of-doc still re-asserts the wrong lock memory

**§ Red-team outcome:**  
“`nano_banana_pro` + a chained `--image` reference (the `_painted_comic_bright.py` path, **`[[locked-stills-provider-split]]`**)”

**§1 correction** then admits that memory is a *different* path (Google NBP $0.50) and that citing it was wrong.

The summary badge still wears the old label. Anyone who only reads the green checkboxes inherits the same silent overturn the last panel already failed.

---

### 2. “FIXED” character lock is still half a fix — production never supplies refs

**§1 / §8:**  
“`render_scene()` now accepts + passes through `extra_ref_paths`; proved end to end… Still open: nothing auto-resolves refs”

Verified:

- `render_scene` *can* take `extra_ref_paths` (`pipeline/visual_render.py`).
- Smoke test works only by **manual** `extra_ref_paths=[REF]` + monkeypatching a throwaway `retro` style (`longform/EW01_Two_Goats/_retro_dna/_smoke_render_scene.py`).
- Real runner still does **not** pass refs:

```323:326:C:\Users\sanjay\PycharmProjects\JesusInTheBible\pipeline\visual_runner.py
        png_path, audit = visual_render.render_scene(
            scene, provider_obj, render_dir,
            max_retries=config.MAX_NBP_RETRIES, log=log,
        )
```

`HFProvider.supports_character_anchor` remains **`False`**.  
So: plumbing parameter ≠ production path. A pilot run through `visual_runner` / normal stills flow still renders **without** character refs unless someone keeps using ad-hoc scripts.

---

### 3. Long-form pilot vs production still provider: **hardcoded 9:16**

EW01 is **16:9**. Ad-hoc `_prove_it.py` correctly uses `--aspect_ratio 16:9`.

Production `HFProvider` does not:

```226:240:C:\Users\sanjay\PycharmProjects\JesusInTheBible\pipeline\visual_render.py
    ASPECT = "9:16"
    ...
        self._aspect = "2:3" if self._model == "openai_hazel" else self.ASPECT
```

§9 budgets a **16:9 long** rebuild through the “production function.” That path, as written, would mint **shorts-shaped** stills unless another unstated fork is used. Feasibility hole for the named pilot.

---

### 4. “Two models, split by role” is not a runner capability

**§1:** character → `nano_banana_pro`; plates → `seedream_v4_5`.

**Reality:**

- `STYLE_REGISTRY` has one `still_model` per style; no `retro` key (`config.py` ~478–495).
- No per-scene model router.
- Smoke test forces `HF_MODEL_ID=nano_banana_pro` **globally**.

You cannot run the cost table’s 17/8 split through one production pass today. The table assumes routing that does not exist.

---

### 5. Same section contradicts itself on Aaron

**§1:**  
“**Also open: only Christ has a locked ref — Aaron … does not**”

**Same §1, later:**  
“**Aaron's locked reference — DONE** … `aaron_retro_ref.png` … **Not yet chain-tested**”

File exists under  
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\EW01_Two_Goats\_retro_dna\aaron_retro_ref.png`.  
A ref PNG is not multi-scene lock. Leaving both “does not” and “DONE” is load-bearing sloppiness: pilot identity for Aaron is still unproven.

---

### 6. §1 still says the character path is unchosen after claiming it is binding

**§1 correction:** user chose HF `nano_banana_pro` — “**binding call**”.

**§1 recipe note:** “The two [HF nano_banana_pro vs NBPProvider] **are not yet reconciled; treat them as separate until one is chosen for production.**”

Binding *and* unchosen cannot both be true. Operational docs still disagree again:

- `RESUME.md` / `STATE.md`: **recipe locked = `seedream_v4_5` + chained ref**.
- This DNA doc: character = HF `nano_banana_pro`.

Three sources of truth. That is how the last false model claim happened.

---

### 7. “Deterministic teeth” on passion body can self-FAIL correct copy

**§5a / §10 punch-list:** ban `muscular / heroic / athletic / six-pack / v-taper / bodybuilder` in `VISUAL_BANNED_TOKENS`.

Tokens are present in `config.py` (good intent).

But SP-G5 is a **substring lint on scene-plan text**. The prove-it prompt itself says **“NO heroic muscle”**. That string contains `heroic` and would trip a text gate if used as a subject_block. Same trap the doc warns about for generation negatives — now on the gate. “Closes Vision-only gap” overstates; it can punish correct anti-heroic language and still miss a bodybuilder frame the vision audit fails to catch.

---

### 8. Path claims treat `_retro_dna` as repo-root

Throughout: `_retro_dna/_prove_it/`, `_smoke_render_scene.py`, etc.

**Actual location:**  
`C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\EW01_Two_Goats\_retro_dna\`  
(not repo root; root listing has no `_retro_dna`).

Feasibility/nav risk for any agent or human following the plan literally.

---

### 9. Gate order still fights itself

| Claim | Says |
|---|---|
| Status header | full-quorum panel → **pilot batch** → sign-off → wire |
| §9.2 | **free kitsch test FIRST, always** (`_KITSCH_TEST.html`) |
| §9.1 | ONE piece, not a batch |
| §10 | kitsch → full-quorum panel → pilot |

“Pilot batch (not 76)” in the header undoes the round-2 “ONE piece” correction. Sequence is not one ordered checklist.

---

### 10. Dot-crawl deferred as “lower severity” while the pilot **is** animated

**§1 / §10:** print-finish not proven on animation; crawl/moiré risk; “revisit before the pilot, not before this correction pass.”

**§9 cost table:** 25 clips Kling/Seedance as the pilot deliverable.

If the DNA look depends on print finish (or baked plate dots), **animation proof is pilot-blocking**, not a polish item after correction. Shipping an animated EW01 without that test can “prove” the wrong finish.

---

### 11. Cost table is grounded on counts, incomplete on delivery

**Grounded (good):** 17 character / 8 empty refs matches `scene_plan.json` refs (`aaron`×11 + `christ`×6 + empty×8). Kling set `{6,11,13,14,18,20,21,24}` matches `_animate_inked.py`. Unit costs match that script’s comments (~$1.13 / ~$0.72).

**Missing / understated:**

- **Full re-spend** of stills+clips after ~$35.80 already spent on inked EW01 — justified only if kitsch wins; not framed as incremental.
- **No line** for Remotion pipeline build (word-timed slams, 6/9 grid, balloons, DoD gates) that §6 admits is **BUILD, not port**.
- **No line** for paid Vision DNA audits the plan itself says are the substance of `/dna-check`.
- **No line** for new retro scene plan (current plan is still baroque/`period-documentary`, golden vestments, not the retro recipe).
- Border crop is **manual ad-hoc**, not production; “budget occasional retry/crop” assumes process that is not wired.

~$29–34 is “re-render stills+clips like last migration,” not “finished Remotion retro long.”

---

### 12. Remotion-as-parallel-engine is large overbuild relative to reuse

**§6 (user decision):** Remotion stays separate from locked `/livingpage` (`v2/LIVINGPAGE_STANDARD.md` — word-timed slams ±0.05s, DoD, richness counters).

That is an explicit product choice, but the plan then requires **rebuilding** livingpage’s hardest parts on Remotion while:

- livingpage already finishes longs/shorts,
- `panel_animator/print_grade.py` already grades clips,
- painted-comic already documents HF `nano_banana_pro` + ref chaining.

§8 “~55% owned” counts POC Remotion comps (`DnaSplashHook`, captions, SFX). It does **not** mean 55% of a production episode engine. Risk: pilot money buys another parallel stack before free audience kill-gate proves the look.

---

### 13. Border mitigation overclaims production automation

**§1:** `VISUAL_BANNED_TOKENS` includes border/frame → “retry-on-audit-fail loop catches… automatically”; else crop ~4.5%.

Vision audit *does* mention frames/borders. Crop rescue is proven only as a hand fix for a **reference** (`aaron_retro_ref_v2_cropped.png`). There is **no** production crop step in `render_scene`. Stochastic bordered pages remain a cost/variance risk for 25 pilot stills.

---

### 14. “Character drift FIXED” still oversells evidence

Evidence remains: 3 Christ poses from one ref (`_prove_it/`), not:

- Aaron multi-scene chain,
- crowd occlusion / side light / passion vs glory,
- blind re-audit,
- production auto-ref resolution.

“MANDATORY character lock” + “FIXED” at the top is stronger language than the evidence.

---

## Smaller but real

- **§3 / fonts:** Kalam/Bangers/PermanentMarker claims look consistent with `_remotion` + prior panel fixes; low concern.
- **§9.3 livingpage ratio:** 60–70% shorts full-bleed vs ≤50% long matches `LIVINGPAGE_STANDARD.md` §7 — correct.
- **NSFW cross path:** `_prove_it.py` still has bare-torso NSFW reject branch; plan’s robed preference is right but not codified as a hard production rule for HF refusal fallback.
- **`/dna-check`:** sketched before wire-in; mostly provenance. Fine as honesty; bad if treated as a pre-pilot deliverable that blocks look proof.

---

## Bottom line

v0.3 is a **better draft**, not a **ready plan**. The model contradiction that killed prior rounds is fixed in the body but **not fully cleaned from the summary**, and the operational docs still say Seedream for identity. The pilot cannot honestly run on the “production path” without: aspect 16:9, dual-model routing, runner-level ref resolution, Aaron multi-scene prove, animation print/dot strategy, and a single ordered gate list that puts free kitsch **before** paid pilot spend.

---

VERDICT: REVISE  
TOP FIXES:  
1. Make one executable character recipe end-to-end before any pilot spend: HF `nano_banana_pro` + refs only (or NBP only) — wire `visual_runner` to resolve scene refs, dual-model or single-model routing, **16:9 aspect for long**, delete leftover “not reconciled” / Seedream-identity / `[[locked-stills-provider-split]]` summary lines; sync `RESUME.md`/`STATE.md`.  
2. Demote “FIXED” / “Aaron DONE”: require Aaron multi-scene chain proof + remove the §1 self-contradiction; treat print/dot-on-animation as pilot-blocking, not post-correction polish.  
3. Fix sequencing and cost honesty: free kitsch → (optional) quorum panel → quoted pilot; cost table must include Remotion build work, scene-plan rewrite, Vision DNA audits, and re-spend of already-paid inked EW01 — not just stills+clips unit math.
