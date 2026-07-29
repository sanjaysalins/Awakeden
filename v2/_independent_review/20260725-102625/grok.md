# Independent review — grok (OK, 87s)

I'll read the full plan and cross-check its claims against the real codebase and the related comic-strip-native / Christ-body rules.Reading the full E2E proposal and the load-bearing source docs next.Verifying the parent-review failure points against the E2E plan and the real tools.# Independent adversarial review — E2E Workflow Proposal

**Artifact:** `v2/E2E_WORKFLOW_PROPOSAL.md`  
**Type:** plan / design proposal  
**Stance:** Hostile. DRAFT labels and a long open-item list do not make a false or doctrine-unsafe runbook safe.

The document is careful about status language. That honesty does **not** make the plan executable. It **inherits and operationalizes** confirmed failures from `COMIC_STRIP_NATIVE_SPEC.md`, then wraps them in a Stage 0→8 “topic to published website” path that reads ready enough to spend on.

---

## Critical findings

### 1. False claim: external Christ reference “has never been tried”

**Cite (§14):**
> “Comic-strip-native has never been tried against a locked EXTERNAL reference image — only page-to-page self-chaining within one piece.”

**False.** `poc_thief_e2e/_comic_strip_native.py` (2026-07-24) explicitly tests:

- Strip 1: no ref  
- Strip 2: `christ_pc_ref.png` chained via `--image`  
- Docstring: *“does chaining a reference help hold Christ across 3 panels”*

Ledger rows exist:

- `[comic-strip-native] strip1_rebuke_noref` — `est_usd: 0.3`  
- `[comic-strip-native] strip2_promise_ref` — `est_usd: 0.3`

The later “validated” recipe dropped that path. This plan never says why, never cites the abandoned test, then re-proposes the **same experiment** as “the concrete next experiment” (§14). That is not gap analysis; it is amnesia that **compounds** the parent-spec review failure.

---

### 2. Wrong page cost inherited and multiplied into the production budget

**Cite (§6d, §16):**
> “~$0.40/page at 2k, 9:16 (today's actual rate)”  
> “Comic pages, 3 pages @ $0.40 | ~$1.20”  
> “≈ $4.80-5.63 visual … ≈ $10-12/piece”

**Ledger truth** for this exact POC: every `EW_Thief_POC` / `nano_banana_pro` still row (including `[comic-strip-native]`, `[poc-pages]`-style page runs, user-prompt pages) is `est_credits: 2.0`, **`est_usd: 0.3`**, not 0.40.

So:

- Unit cost is overstated vs the project’s own ledger.  
- Worse: the plan still understates **expected** spend by selling a zero-reroll base while §6d admits body-gate recurrence and parent §1.4 proved it. One whole-page Christ-gate reroll costs a full page, not one panel.  
- Kling ledger rows for the same episode are often `8.75cr / $1.312` or even `10.0cr / $1.5` (panel-technique tests), not cleanly “~$1.13 billed.” Production table mixes optimistic rates without a reroll band.

Same cost falsehood the parent review already failed — now promoted into an end-to-end budget.

---

### 3. Doctrine-unsafe production default: “accept invention” on passion pages

**Cite (§6e heading + body):**
> “Animate with intent (Kling 3.0 direct — the current best-of-tested default)”  
> “accept some invention as a real, named cost — not a solvable prompting problem”

Then (§1 sequence): Stage 2d is **Kling 3.0 direct** as the normal path; crop-and-recomposite is only “if invention becomes unacceptable for a specific real piece.”

That is inverted against this project’s locked bar (sound doctrine both ways; sacred frames fail-closed). Parent bake-off already recorded pose violations, invented scratches/blood/expression shifts, panel replacement. On a Penitent-Thief / Passion batch (§2 explicitly recommends clustering Passion Narrative pieces), those are **CSN-G3 / doctrinal failures**, not “named cost.”

Worse: crop-and-recompose (open item 1) — the only path that might fix invention — remains **untested**, while the broken path is the Stage-2 default in a full publish workflow.

**Also missing:** NSFW fallback. `_thief_poc_animate.py` does `NSFW-REJECTED` → `continue`. Production uses Hybrid / direct-Kling for bare-torso crosses. §6e never names this single point of failure for the primary recommended cluster.

---

### 4. Christ body gate: inherits over-hardening + ignores DNA prompt rule

**Cite (§6b, CSN-G3 in §6d):**  
Anchors “carrying the Christ body gate §2a” from the parent spec; CSN-G3: “no blood beyond faint brow marks.”

Parent §2a “validated fix” still mandates **unmarked hands/wrists/feet/torso** and multi-negation (“absolutely NO blood, no red marks, no wounds…”).

`v2/AWAKEDEN_COMIC_DNA.md` §5a allows **faint/matted blood**, bans **bright decorative** blood / heroic musculature, and explicitly warns: **do not put negated banned words into prompts** (seedream/negative-channel anti-pattern + SP-G5 substring match).

This E2E plan:

- Treats parent §2a wording as the gate to carry into every page (§6b).  
- Never reconciles with DNA §5a (open item 21 only says “not reconciled,” then continues).  
- Never flags that the “fix” is the DNA anti-pattern.  
- Softens CSN-G3 text slightly (“faint brow marks”) while still pointing operators at the stricter §2a anchor block.

A careful review will flag **sanitized crucifixion** (no wounds on hands/feet) as badly as heroic abs. The plan operationalizes that tension instead of resolving it.

---

### 5. §0 contradicts itself: “only Stage 2 redesigned” vs Stage 3 fully invented

**Cite (§0):**
> “The **only stage this document redesigns is Stage 2 (Visual)**”  
> Stages 0, 1, 1b, 3b, 4, 5, 6 “existing pipeline, unchanged.”

**Cite (§1 / §7):** Stage 3 is **“NEW (this doc, proposal)”** — word-timed choreography over multi-panel pages; `cli_assemble.py` is “the wrong shape.”

You cannot ship website content without Stage 3. Calling this an E2E “reuse nearly everything” plan while the cut itself is unbuilt is marketing structure, not engineering. Score / SFX / caption / thumbnail all assume a finished full-length final that Stage 3 does not yet know how to make.

---

### 6. Stage 3 tool reuse is architecturally mismatched (false feasibility)

**Cite (§7):**
> treat each page like living-page’s panel grid — “a `grid_choreography` pass timed to the narration’s word-alignment” over “live panels”

**Reality of `panel_animator/grid_choreography.py`:**

- CLI: `--clips a.mp4 b.mp4 c.mp4 d.mp4` — **separate** clips  
- **Draws its own** gutters + ink borders  
- Layouts (2x2, 2v, …) **compose** cells onto a canvas  

A comic-strip-native page is **one** model-drawn multi-panel image/clip with borders already baked in. You cannot “grid_choreography” a whole-page clip without:

1. Cropping panels out (unbuilt), **and**  
2. Either accepting double borders / wrong paper treatment, or redesigning the tool  

Living-page (`build_livingpage_16x9.py` + per-beat stills/clips) is a **different product**, not a drop-in for 3 long 5s page clips.

**Timing hole the plan never solves:** §6a maps Page 2 ≈ **18–52s (~34s)**; §6e produces **one 5s Kling clip** per page. Three clips ≈ **15s unique motion** for a ~59s short. No loop / boomerang / hold / multi-pass / multi-duration rule appears in Stage 3. Open item 3 admits assembly never built — yet §16 prices Build/score/SFX/caption as **$0** as if the path exists.

---

### 7. Gates are human-only where doctrine is load-bearing; G6 is vapor

**Cite (§6d, §6f, §18):** CSN-G1..G4 / CSN-G5 are “human eye only.”  
§18 also says **CSN-G1..G6** “named and documented” — **G6 is never defined in this document** (it only exists in the parent technique checklist).

Rest of engine: deterministic + Vision fail-closed before spend. This plan puts Christ body gate, baked text, and animation invention on **eyeballing** as the production gate, then continues to website deploy stages. Single point of failure at scale; regression vs locked discipline.

No reuse of:

- Claude Vision still audit (`pipeline/visual_render.py`)  
- DNA body-gate Vision pattern  
- `VISUAL_BANNED_TOKENS` lint (open item 17 only *proposes* it)  
- `SKILL_locked.md` frozen-tableau / gallery-cut discipline (never tested on multi-panel pages; bake-off used ad-hoc prompts only)

---

### 8. Stage 0.5 / bible-check mis-framed as “existing research stage”

**Cite (§3):** Reuses `bible_kb` / BC-G1–G2; positions apocryphal sweep **before Stage 1**.

**Real `/bible-check`:** Stage **2a+**, after scene-plan, fact cards bound to scenes/stills hash, gates GREEN before animate.

Apocryphal-name hygiene (Gestas/Dismas) is **correct doctrine**. Calling BC-G1/G2 the gate for a pre-draft name sweep overclaims an existing system that does not run there. Open item 16 admits bible_kb was never pointed at comic panel specs — so §3’s “reused” framing is half real, half aspirational.

---

### 9. Premature full publish stack; third visual lane unreconciled

The plan sequences Stages 5–8 (thumbs, publish pack, website, SYNC) in detail while:

- Open item 1 (crop-and-recomposite) untested  
- Open item 3 (e2e assembly) untested  
- Open item 7 (`PAINTED_COMIC_SPEC` §5 contradiction) unresolved  
- Open item 21 (`AWAKEDEN_COMIC_DNA` parallel lane) unresolved  

**Cite (§2):** first pieces should be a “Passion Narrative in comic-strip-native” **batch** — i.e. series-scale spend **before** series-scale character lock (§14) and before a finished cut exists.

That is over-engineering the packaging and under-proving the product. Website cutout / `build_study_figures` notes (§12) are fine *later*; they do not belong ahead of “can we make one 60s cut that holds doctrine?”

---

### 10. Smaller but real integrity issues

| Issue | Cite |
|---|---|
| “check **three** things” then lists **four** | §2 intro + items 1–4 |
| Cross-ref: audio timing “matters for **§8**, the build/caption discussion” — captions are **§9**; §8 is score/SFX | §5 |
| Cross-ref: character gap “in **§6**” — it is **§14** | §2 item 3 |
| §15 shrugs off INV-19 asset reuse; crop path would make shorts-clip reuse relevant again | §15 vs CLAUDE.md reuse-first |
| Seedance 1.5 Pro “avoid entirely” (§6e via parent bake-off) is scoped only to **full-page** input; plan never says so — agents will treat Seedance as banned project-wide vs locked calm-panel tiering | §6e |
| “$37.36” POC spend restated without reconciling that production `$10–12` is not a measured first-piece expectation with passion rerolls | §16 |
| Provenance claims “verified by reading” pipelines, yet load-bearing cost / ref-chaining / assembly claims fail against ledger and `poc_thief_e2e/` | Provenance vs §14 / §16 |

---

## What is actually solid (so this is not blanket dismissal)

- Clear DRAFT / not-in-SPEC framing.  
- Correct that `cli_assemble.py` jigsaw ≠ native multi-panel pages.  
- Caption reasoning (§9): WhisperX default until a panel-aware layer exists is coherent.  
- Honest that `$25` ceiling is not wired to this lane.  
- Website / finality / upload tooling mostly correctly cited.  
- Open-item list is long and often accurate — but the **runbook still sequences past the open items as if the next step is a production short**, not a falsifying experiment.

---

## Bottom line

This is not a safe E2E plan. It is a **packaging document around a technique that just failed independent review**, with:

1. a **false** “never tried external Christ ref” claim,  
2. **wrong costs** baked into the budget,  
3. **invention accepted** as the default animation step for Passion content,  
4. an **assembly “solution” that does not match the tool it cites**, and  
5. a **60s fill strategy that does not exist** for 3×5s page clips.

Do **not** run Stages 2–8 as written. Fix the foundation first.

VERDICT: FAIL
TOP FIXES:
1. Demote Kling-direct whole-page from Stage-2 default; require a tested crop-and-recomposite (or frozen-tableau) path with a hard reject bar for passion invention / NSFW hybrid fallback before any E2E runbook spend.
2. Correct ledger costs ($0.30/page, reroll-inclusive range); delete false “external ref never tried” language and document `_comic_strip_native.py` + why the validated recipe dropped Christ ref chaining; align body gate with DNA §5a (faint/matted blood, positive end-state wording — not unmarked hands / multi-negation).
3. Rewrite Stage 3 as an explicit unproven experiment (page→panel crop, fill 5s→beat durations, livingpage vs grid_choreography interface truth) — do not sequence website/publish until one full 60s cut exists with doctrine-safe motion and measured spend.
