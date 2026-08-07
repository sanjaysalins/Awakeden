# Independent review — grok (OK, 216s)

I'll read the full plan and check it against the real codebase, skills, and existing tools.Continuing through the plan and checking device claims against what actually exists.Checking timing artifacts, device existence, Seedance duration rules, and POC30 state.## Independent adversarial review — Seed of the Woman LONG spread plan

**Stance:** This is a real plan with serious craft (movement pacing, verse-register map, open questions). It is **not** ready to spend against. Several claims treat prose designs as existing tools, sell estimated timing as “real alignment,” and understate build risk relative to what the repo actually has.

---

### Critical — false tool / codebase assumptions

**1. “wash-creep CONVERGE” is not a real mode of the library**  
Spread 52: *“wash-creep CONVERGE ($0 — reverse grammar; the payoff of s14)”*.  
`panel_animator/wash_creep.py` only advances or retreats a wash front along an isolated storm-wash mask (`advance_px` / `backrun`). That is **edge retreat**, not “gathers onto the cross.” Radial/converge-to-figure geometry is **not implemented**. Calling it “reverse grammar” of s14 is wrong and will force mid-build invention on a climax beat.

**2. “Thread Device draw-on / gleam-pass” overclaims `thread_device.py`**  
Spreads 21, 25, 37, 45, etc.: *“Thread Device draw-on”* / *“gleam-pass”*.  
`panel_animator/thread_device.py` has `make_thread_layer`, `thread_opacity`, `thread_swell` only — static stroke + opacity fade + luminance swell. There is **no progressive path draw-on**. Opacity fade is not a stroke revealing itself through curse-lines.

**3. `hunt_and_lock` is not a shared $0 skill**  
Spread 16: *“hunt_and_lock ($0 — the device's literal design case)”*.  
No `panel_animator/hunt_and_lock.py`. The only real implementation found is **episode-local** code in `poc_living_sketchbook/jericho/_j5_assemble.py`. This is copy/adapt work, not “reuse a locked device.”

**4. `tear_hole` is not a drop-in production module either**  
Landing s71: *“tear_hole (mandatory landing device)”*.  
Repo history treats tear_hole as **per-episode assembly custom** (Bronze Serpent / DoA notes: “genuinely not yet built” / custom). Skill names it; there is no stable shared API with proven filmstrips for *this* folder’s assembler.

**5. Bespoke holds are design prose, not proven code**  
s09 gold-fleck breathe, s55 shadow-sweep, s59 dual-glow: *“Fable pre-designed in _PREFLIGHT”*.  
E6 writeups specify px/coords — good discipline — but **no demo clip, no module, no filmstrip QC**. That is exactly the Day-of-Atonement “design mid-build” risk, only moved into a markdown file.

**6. Cast sheets claimed; they do not exist**  
`_PREFLIGHT.md`: *“`cast/ADAM.md` + `cast/EVE.md`”*.  
`poc_living_sketchbook/cast/` has `adam_ref.png` / `eve_ref.png` only. No `ADAM.md` / `EVE.md`. Skill §2 requires canon sheets for recurring figures. Plan §5 skips this hole.

**7. Build scripts are still POC30-only**  
`_s4_animate.py` docstring: *“Only 2 clips… s02 and s04”*; `JOBS` has two entries.  
`_devices.py`: only s01/s03/s04 (+ empty SPECIAL_CARDS).  
Plan presents 71 spreads as production-ready while **devices table, animate jobs, and lettering map for 6–71 are not authored in code**. `_spread_table.py` has the numbers; the spend path does not.

---

### Critical — timing honesty / verification gaps

**8. Table header contradicts the plan’s own caveats**  
Header: *“The spread table (real alignment timing, not estimated)”*.  
Same artifact: sub-turn seams are *“word-proportional ESTIMATES”*; PREFLIGHT E8 lists ~20 multi-spread turns (s12–15, s54–59, s68–71, etc.) as estimates. That header is false.

**9. Spreads 1–5 still carry excerpt times while claiming full-file continuity**  
Table s05: *“30.7–33.0 | 2.3”* while timing note and `_spread_table.py` use **33.80**.  
Full-file `_turn_boundaries.json`: turn 2 ends **32.476**, turn 3 (*“Where art thou?”*) is **33.18–33.764**. s04 ending at 30.7 is excerpt residue. Chain is **not** cleanly full-file-aligned for 1–5.

**10. Alignment-correction is required but not a hard go/no-go gate**  
Header and E8 say run alignment correction *before build*. §7 open questions list serpent/Mary/variants/spend — **not** “alignment pass complete, seams locked.” Building stills/clips on estimated seams reopens cost when M6–M7 shifts (s56 already flagged mid-turn).

**11. Seedance duration law is invisible in the plan**  
Skill / DoA `_s4_animate.py`: Seedance ∈ **{4, 8, 12} only**; holds >8s loop at assembly.  
This plan assigns Seedance to holds like 5.6, 7.2, 9.5, 10.4 without a duration→legal-snap→loop table. DoA documented 27 loop cases explicitly. This plan does not — cost and QC both under-specified.

**12. Camera push on s22 conflicts with locked camera-animate discipline**  
s22: *“whole arrival + slow push”*.  
DoA animate notes: generated clips are camera-locked; push must be **assembly-side deterministic**. Plan buries that under the lettering device column.

---

### High risk — content / motion / single points of failure

**13. Validation scope is oversold**  
*“validated the Day of Atonement retrospective's fixes on this exact content”* — true for **5 spreads / process**. It does **not** validate serpent identity ×18, thread grammar, wash pair, naming-page accumulation, s51 NSFW path, or tear_hole landing. Promoting POC30 ≠ proving the 71-spread device stack.

**14. Highest-risk still is not gated first**  
s06 ACTING 1: multi-figure **Adam + Eve + first serpent** + designed arm/turn motion (Kling).  
That is the episode’s hardest identity+motion still. Plan does not require: serpent anchor approved → s06 still full-res QC → then batch. Failure there cascades into ~18 serpent appearances.

**15. Seedance asked to “lengthen / pivot / widen” light and shadow**  
s10 *“shadow lengthens”*, s18 *“light pivots”*, s70 *“light widens”*.  
Skill §3–4: no morphing state changes in one generative clip; ambient motion only. These are progressive state changes — high invention risk. s55 correctly moves shadow travel to $0; s10/s18/s70 do not get the same rigor.

**16. Jesus multi-pose + NSFW is a cost and schedule SPOF**  
§5: Jesus ~8 spreads, multi-pose lock from s51, *“NSFW fallback note”*.  
One fail-closed cross re-roll chain (still + Kling + multi-pose second-ref) can blow the animation subtotal. Plan cost treats 9 Kling as flat ~$1.20 each with no NSFW/fallback line.

**17. Mary “no anchor” is a deliberate identity gamble**  
§5.5 / open Q3: face averted, 2 spreads + vignette.  
Reasoning is clear; risk is three different women in s30/s42/s31-bg if the model freelances. Acceptable only with user OK — correctly open-questioned, still a production risk if answered “yes” without a one-still identity test.

**18. s55 claims “same still” but cost accounting omits it**  
E6-I: s54/s55 share composition; §6 shared-art list names s23, s31, s34–36, s53, s47/60/66, s68 — **not s55←s54**. Minor, but it shows the stills math was not fully cross-checked against E6.

---

### Cost / spend

**19. §6 is honest that it is not a quote — and still likely low**  
*“No API called, no estimator run… ~$50–75”*. Good ask-before-spending posture. Gaps:

| Under-count | Why |
|---|---|
| Flat Seedance ~$0.65 | 4s vs 8s vs 12s bills differ; several holds need ≥8s source |
| 20–25% re-roll | Weak for multi-figure acting, hands (s69), serpent×18, Jesus cross |
| No NSFW/fallback line | s51 may leave HF pro |
| No sequential multi-pose cost | Second-ref chaining blocks “batch all stills in one go” |
| POC ~$4 already spent | Not rolled into episode total |

**20. “Higher $0-device share” is not free of engineering cost**  
39% $0 devices includes unproven converge/draw-on/bespoke/hunt — calendar and rewrite risk, not just $0 runtime.

---

### Over-engineering vs proof

**21. Full 71-spread pre-design is the right DoA lesson; full spend is not yet justified**  
Pre-design of table + E6 is good. What is premature is treating the plan as *build-complete* while:

- high-risk devices are uncoded  
- alignment seams are estimated  
- animate/devices code still says “extend as the full plan is authored”  
- no **risk-tier test gate** (DoA had explicit 3-job test gate before full animate)

**22. Two style-variant candidates before identity test is fine; don’t bundle into main stills spend**  
§5b: sl13@s08, sl16@s65 pending test. Open Q4 is correct. Keep them **out of** the main estimator until tests pass.

---

### What the plan gets right (brief, not praise)

- Movement pacing argument vs blind 65/76 copy is coherent.  
- Verse-register map + LAW 1 on Gen 3:15 + naming-page Typeset rationale is careful.  
- Serpent theology (creature vs Rev 12:9 naming; shed skin; freeze before crush) is disciplined.  
- Open questions on serpent / naming adjacency / Mary / spend are the right user gates.  
- PREFLIGHT E7 device-budget tally and raking-light cap show DoA learning.  
- Explicit “run real estimator + independent_review before build” is correct process.

Those do not cancel the false “tool exists” and “timing is real” claims.

---

### Missing steps (must be in the plan before spend)

1. **Alignment-correction pass** → lock `_spread_windows.json` / table ends (especially s56, s68–71).  
2. **Author missing tools or redesign**: wash converge → real API or multi-stage stills; thread progressive reveal; hunt_and_lock port; tear_hole in this episode’s assembler.  
3. **Cast canon**: `ADAM.md` / `EVE.md` + `SERPENT.md` + desk/tomb/Golgotha reuse-check results.  
4. **Extend** `_devices.py`, `_s4_animate.py` (with duration snap + loop list), `finish_config.py` for full episode.  
5. **Risk-tier stills gate**: serpent anchor → s06 → s51 → then batches of ~10 + `motion_lint` / `_layer_check`.  
6. **Real cost quote** with 4/8/12 tiers + NSFW contingency.  
7. Fix table header and s05 row to match `_spread_table.py` / full-file turns.

---

VERDICT: REVISE  
TOP FIXES:  
1. Remove or re-spec every device that does not match real APIs today (wash-creep CONVERGE, Thread draw-on/gleam-pass, library hunt_and_lock, tear_hole-as-shared-skill); implement or redesign with filmstrip proof before any full stills batch.  
2. Make alignment-correction a hard gate; rewrite the table header and s05 (and any hybrid excerpt times) so nothing is sold as “real alignment timing, not estimated.”  
3. Add a risk-tier build order + real estimator: serpent + s06 + s51 first; extend `_devices.py`/`_s4_animate.py`; Seedance {4,8,12}+loop table; cast `.md` sheets; cost contingency for multi-figure/Jesus/NSFW — then re-quote before spend.
