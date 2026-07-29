# Independent review — grok (OK, 134s)

I'll verify the plan's claims against the real codebase before writing an adversarial review.## Adversarial plan review — Comic Page Pipeline

Default: **skeptical**. This is better than the same-day `COMIC_PAGE_ENGINE_DESIGN.md` (separate panels + no-freeze are real), but it still over-claims “existing tools,” under-specs hard seams, and wants production modules before the timing idea is proven.

---

### Critical / high

**1. Word-align source is misnamed (and the plan leans on it as the clock)**  
§1: *“word-level forced alignment | existing WhisperX path (`assembly_align.py`)”*  

That is wrong. `C:\Users\sanjay\PycharmProjects\JesusInTheBible\pipeline\assembly_align.py` is ElevenLabs forced-alignment, with default backend `whisper` (local faster-whisper), cached as `narration.alignment.json`. WhisperX is a different path (captions / veed_io).  

If Rung 1 assumes “WhisperX words always exist on locked pieces,” you will hit missing/stale alignment or the wrong backend. CP-1, bubble pop, and spotlight all sit on this.

**2. “All on-page text from `kjv_cache`” breaks real narrations**  
CP-1 LLM: *“bubble/caption text pulled verbatim from `kjv_cache`”*  
CP-G7: *“every string byte-equal to its `kjv_cache.json` source”*  

Gospel Five-Beat hooks / conviction / CTA are mostly **original** prose, not KJV. Only quoted speech/verse blocks are cacheable. CP-G7 as written will either (a) force every caption into a verse and invent placement, or (b) FAIL every real short.  

POC only proved pure Luke dialogue. Production needs: **KJV-only for scripture speech; separate policy for narrator lines** (and still no double-caption vs bubble).

**3. “Small upgrade: `render()` accepts focus windows” is not small**  
§6 + CP-5.  

`panel_animator/grid_choreography.py` only has uniform cyclic `activeness(..., per_panel, ...)` — equal dwells, order = clip order, cyclic `% n`.  
Narration-timed unequal `focus: {t0,t1}` windows need a real schedule (order, overlap, multi-return, last-page hold). That is a rewrite of the attention model, not a flag.  

Also: **no full-bleed / 1-panel layout** in `LAYOUTS` (only `2x2`, `2v`, `2h`, `3-big-*`). §2.6 claims full-bleed hero; code path is “skip grid,” which is undefined in the contract.

**4. Freeze story is half-wrong**  
§5.2: *“grid_choreography freeze fix … already half-done … must be finished”*  

Loop-so-you-don’t-hold-last-frame is **already in** (`i % len(src_frames)`, 2026-07-25 comments). What is **not** done: boomerang vs jump-loop, physics routing, narration focus, in-pass text.  

Calling the remaining work “finish the freeze fix” hides the real gap: **CP-4 fill policy vs what composite actually does** (forward wrap only today).

**5. Mouth tails have no data contract**  
CP-6: *“tail to the TRUE speaker’s mouth”*  
`page_plan.json` has `speaker` + text, **no mouth / face coordinates**.  

POC tails were hand-placed. “In-pass, cell-relative” still needs per-panel anchors. Without Vision mouth detect or manual coords at the stills gate, production text reintroduces the POC’s attribution bugs at scale.

**6. Cost model understates directional / 10s / plan LLM**  
§5.1: directional motion → *“or get a 10s render”*  
§11: still prices only **5s** tiers.  

Also missing: Opus page-plan + review/audit (scene-plan-class, not free), Christ-body rerolls on passion pieces, and any second animate after stills gate.  
“59s short **$22–30**” vs “current ≈ $23” is marketing-tight; honest band should show **plan LLM + 10s + 1-in-3 reroll** or stop comparing to the locked short budget.

**7. Build plan over-engineers before the idea is proven**  
§12 steps 1–4: new `comic_page_plan.py`, `page_compose.py`, `page_freeze_lint.py`, `comic_page_runner.py`, `cli_comic.py` — then Rung 1.  

User ask was prove one narration-driven page. Rung 1 should be **throwaway scripts** on one locked piece (reuse `grid_choreography`, `_comic_text_layer` patterns). Wiring `cli_comic` + pipeline orchestration **before** dwell-band GO/NO-GO is premature.

---

### Medium

**8. N_pages math is under-specified**  
§2.3: `N_pages = clamp(round(T / 12), ceil(T / 16), floor(T / 8))`  

Works for 59→5 if clamp is (value, lo, hi), but:  
- dwell band is admitted hypothesis (good)  
- 5 pages × 4-panel habit → ~14–16 panels is a **guess**, not derived from phrase board  
- no rule when phrase snaps force a page &lt;8s or &gt;16s (reject? merge? split?)  
CP-G6 says “dwell in band” without a repair step.

**9. Beat→panels heuristic is hand-wavy**  
§2.5: WPS + speaker changes → 1–4 panels.  

No thresholds, no tie-break with layout capacity, no link to Gospel beats (Hook/Proof/Landing). LLM then “composition only” still chooses content that can break AS-G7 “last page = Christ” if math already filled page slots wrong.

**10. Physics gate reuse is cited, not wired**  
§5.1 cites `physics-motion-check`.  
`physics_motion_check.py` expects **scene_plan.json** fill fields, not `page_plan.json` `animation_tier` / loop mode. New adapter or it is cargo-cult.

**11. Competing assembly stacks ignored**  
CP-7: *“existing standing stages unchanged.”*  

Living-page / `run_piece` / assemble-long already own word-timed grids, score, SFX, caption, landing hold. Plan never says: **replaces** livingpage for shorts? parallel format? which finality/release path? Risk of a third incomplete film path.

**12. Technique-spec open items treated as closed by architecture**  
Technique spec still: flexible layouts untested, Seedance single-ink untested, 16:9 untested, body-gate eye-only.  
Plan lists them in §13 (good) but §0 / cost / “bank for long” still read production-ready. Rung 3 at ~$8 is thin if long page needs 3–4 new stills + animates.

**13. Text accumulate-to-page-end will clutter**  
§7: *“persists to page end (comic pages accumulate text).”*  

On a 12–16s 4-panel dialogue page that can stack 6+ elements (POC did). No max-on-screen, no expire-when-focus-leaves-panel. Muted policy makes this worse (bubbles must carry dialogue).

**14. “SP-G-style” page-plan gates**  
§2.7. Scene-plan gates (SP-G1..G9) are for a different artifact (macro_elements, vignettes, shot_kind). Reuse the **process** (self-review + independent audit), not the gate IDs. Vague = untestable.

**15. Speaker / doctrine attribution single point of failure**  
POC already mis-aimed a rebuke at Christ once. Plan relies on LLM `speaker` + eye CP-G7. No deterministic map from `voices.json` / turn tags → bubble speaker. For doctrine pieces this is not a style nit.

---

### Feasibility that *does* hold

- Separate full-res panels → `grid_choreography` is the right composite path (matches technique §0.5).  
- `LAYOUTS` names for multi-panel mostly exist.  
- `build_phrase_board` in `assembly_timing.py` is real for phrase snaps (name the function; don’t imply magic in `build_timeline` alone).  
- `asset_index.py` exists; reuse-first is real project discipline.  
- Hybrid NSFW → direct-Kling pattern exists in `pipeline/video_render.py`.  
- Freeze lint (CP-G8) is the right class of gate for Zacchaeus-class bugs.  
- Validation ladder + user OK on spend matches locked cost rules.  
- Honest Hailuo vs Seedance tension is correctly flagged.

---

### Over-engineering / reuse

| Plan invents | Already nearby |
|---|---|
| Full `cli_comic` + runner before Rung 1 | POC scripts under `poc_thief_e2e/` |
| New page-plan LLM stack “like scene-plan” | Could be one JSON schema + thin planner until Rung 2 |
| CP-7 as new assembly story | Concat + existing score/SFX/caption skills if inputs are plain mp4+mp3 |
| Parallel gate IDs CP-G* vs CSN-G* | Technique already has CSN-G1..; avoid dual registries until lock |

---

### Verification gaps in the ladder

- Rung 1 GO/NO-GO is “by eye” — must also run a **draft CP-G8** and phrase-snap dwell report, or you relearn freeze/dwell by accident on Rung 2.  
- No check that **sum(page dwell) == narration T** (plus INV-26 hold).  
- No audio/video A/V sync check after concat.  
- No sample of **non-KJV narrator-heavy** piece (most viral shorts); Thief dialogue is a best-case text layer.

---

### Verdict rationale

Not **FAIL**: direction matches user ask + validated separate-panel pivot; risks are fixable in the plan.  
Not **PASS**: false tool claim (WhisperX/`assembly_align`), broken KJV-only text policy, underspecified focus/mouth/dwell repair, inflated “small upgrade,” full CLI before proof, cost holes on 10s/LLM.

---

VERDICT: REVISE  
TOP FIXES:  
1. Fix alignment facts (name real backend + require `narration.alignment.json`); split text policy into KJV-verbatim speech vs original narrator captions; put mouth/tail coords (or Vision step) in the stills/page contract.  
2. Spec CP-4/CP-5 honestly: boomerang vs forward-loop vs 10s; rewrite focus schedule (not “small `render()` tweak”); define 1-panel full-bleed + dwell out-of-band repair; price 10s + Opus plan + rerolls.  
3. Shrink §12: Rung 1 = throwaway script on one locked short + freeze lint + dwell report; only then build `page_plan`/`page_compose`/`cli_comic` — and state what production path this replaces (livingpage vs parallel).
