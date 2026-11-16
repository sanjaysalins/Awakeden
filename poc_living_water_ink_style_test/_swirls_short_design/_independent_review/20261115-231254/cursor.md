# Independent review — cursor (OK, 95s)

Adversarial review of the **v3.2 plan artifact** (treating it as the binding design text, cross-checked against the POC tree and `BUILD_REPORT.md` where the doc itself has drifted).

## Feasibility vs codebase / tools

**§0 “Fact” table is a pre-build snapshot, not current truth.** It still claims e.g. “Paid call in `assemble` … `build_srt.build()` → `align(force=True)`” and “`page_plan.json` … code reads `heads / recurring / turn`”, while §6 and the changelog say many of those items are redesigned. The header **Honesty rule** says “Section 6 is the one status table”, but §6 still labels bridge, guard, G15h, align/G2w, etc. as **DESIGNED** even though `BUILD_REPORT.md` (same folder, same date) claims **414 checks ALL PASS** and lists them as built. A reader following only this plan cannot tell “target” from “shipped” without a sidecar report—undermining the contract in the opening lines.

**RUN entry point understates the real surface.** The banner defines `RUN = … swirls_episode.py`, but the v3.2 command/guard behavior lives in **`swirls_short_run.py`** + **`swirls_guard.py`** (acknowledged only in §9.1 table, not in the RUN block). Feasible once wired (`swirls_episode.py` docstring does delegate), but the plan’s top-of-file operator contract is incomplete.

**Probes R1–R3 are prerequisites for the spend model but explicitly “Not verified” (§0, §5.6).** The guard’s auto-confirm path assumes `openart_creation_show` returns `credits_spent` and faithful `sent_params` (§5.2 step 5, §5.3 `after()`). `BUILD_REPORT.md` §“Still not run” repeats that R1–R3 are open and **“Design v3.2 must still go back through the plan panel before the pilot spends.”** The plan’s §9.2 Phase **C** (“the pilot may spend: steps 2–5”) is therefore **ahead of its own evidence gate** unless you treat T6’s mocked receipts as substituting for R1—which the design itself says is not allowed (“Typed numbers … are not receipts”).

**ElevenLabs forced alignment is a hard dependency with no fallback.** Step 2: “**No whisper fallback for timing**” and `timing` refuses whisper backend (T10). R2 is “Stop; the owner decides.” That’s honest, but feasibility for this account/key is **unproven at plan time**; meanwhile legacy Swirls episodes in the same POC used whisper/whisperx alignment (e.g. ep12/ep16 patterns). The pilot is not reusing a path that already worked there—it’s betting on a permissioned API the plan hasn’t probed.

**Attended bridge is mandatory, not optional.** §3 Prerequisites: a live session must service `gen_requests_guarded\` per `SWIRLS_SHORT_SERVICER.md`, plus in-chat Vision. That matches `openart_bridge.py` (MCP-only OpenArt) but means the “pipeline” **cannot run unattended**; any claim of resumable automation stops at “human servicer + heartbeat + claim protocol.” Feasible only as a **paired human+agent** workflow.

**G1k “in-lane wrapper” vs shared `verify_span` is a footgun.** §3 SWS-G1k rejects `...`/`…` and demands whole-word runs, but also “(4) interior punctuation must match (also run `verify_span`; both must pass).” §0 admits `kjv_strict.verify_span` **accepts** `"I am ... the Christ"` for John 1:20. §13.2 defers fixing `pipeline\kjv_strict.py` as **out of lane**. T5 is supposed to FAIL that splice in the wrapper; if the two checks ever disagree or the wrapper regresses, you get either false FAILs or a silent hole—exactly what §0 flags “Not safe alone.”

## Hidden risks / SPOFs

**Spend guard ≠ owner consent.** §5: “It does **not** prove the owner said yes: the session types `approve`.” §13.1 (coordinator task) defers owner-only approval to a settings `ask` rule. Until then, caps are **session-typable**; the elaborate G0 machinery mainly prevents *accidental* over-spend, not *social-engineering* spend.

**MCP/generate bypass remains.** Same §5: “A direct call to the OpenArt generate tools goes around every guard” with only post-hoc `RUN reconcile`. Single compromised or tired operator session can spend off-ledger; caps won’t bind that spend to an `approve` row.

**`LATE_PENDING` can brick an episode.** §5.1 rule 3: if cancel rename fails after claim, “no new request for that unit is allowed” and settlement is only `RUN fetch`. Combined with “**no open row**” blocking all paid commands (§5.3 `before()`), a lost `creation_id`, bad receipt dump, or servicer crash mid-job creates an **exclusive lock** until manual archaeology—high operational risk for a pilot.

**Shared OpenArt balance (§0: 7,885 cr).** Caps are per-episode grants, not wallet isolation. Parallel repos/sessions can drain credits and cause false “balance < cap” refusals or surprise insolvency mid-pilot.

**Heartbeat vs long renders.** §5.1: client heartbeat every 10 s; stale at 60 s triggers cancel/sweep. Kling jobs can run long; the design assumes polling loop keeps heartbeats fresh—reasonable, but any blocking call or stuck client risks **`CANCELLED_UNCLAIMED` / `LATE_PENDING`** false positives.

## Over-engineering / premature build

**Phase C unlocks picture money before Phase D proves clip gates on real media.** §9.2: Phase **C** enables steps 2–5 (includes **~840 cr** pictures, §8); Phase **D** (G13/T7b, G15h/T8, score T14) is “before step 6” only. You can burn most of the visual budget on stills/animatic **before** G13 strip QC and G15h calibration are validated on real back-cover motion—the exact failure mode prior red teams cared about (moving hold, clip text melt).

**T12 explicitly disclaims quality.** §9.3 T12: “**Plumbing and order only — nothing about film quality**.” Yet §3 Step 10’s film panel is the first holistic quality gate **after** clip ask 3 (~3,120 cr cap). The plan invests heavily in spend plumbing ($0 tests) while leaving the expensive creative risk **un gated until late**.

**414-test harness + dual bridge folders** may be justified given red-team history, but §9.4 still defers owner-only approve, shared score/SFX, adopt, mouth pixel check, etc.—so the **highest-risk human trust gap** is deferred while the **lowest-risk deterministic layer** is maximal. That’s a prioritization mismatch for “ship one pilot.”

## Missing steps / verification gaps

**§12 admits the hold and timing story are unproven:** “A back clip that keeps moving for 10-11 s: **unproven**”; “G2w thresholds are a guess until T10b”; “Sampled frames miss defects **shorter than half a second**” (G13 at 2 fps). G15h “Honest limits: a **slow camera drift** counts as motion” can PASS non-narrative motion. BUILD_REPORT notes frozen-control **N ≈ 0**, so the **absolute floor 0.5** does the real work—not the ratio design emphasizes—meaning T8 may not tune what production needs.

**G10 cover FAIL was downgraded in implementation, not in the binding plan.** Design Step 5 / SWS-G10: “**FAIL on covers**”. `BUILD_REPORT.md` changed covers to **WARN** because T9 didn’t separate good/bad shipped covers. The plan text still promises FAIL; operators following only v3.2 will expect a gate that code intentionally softened.

**Step 11 / publish:** `release_check.py` handling for `POC\` is “**unverified**” (§3 step 11, §13.8)—a hole if anyone treats Step 10 as “done” for release.

**G2w depends on local `faster_whisper`** with T10b allowed to **skip** if the model isn’t cached—so CI/$0 runs may never set thresholds on real audio (§3 SWS-G2w, T10b skip path in validator).

**Voice pricing placeholders.** BUILD_REPORT: “Voice price rates … are placeholders marked **UNVERIFIED**.” §8 caps (“at most $1.20”, etc.) are built on numbers the plan itself marks unverified—caps can be wrong in either direction.

## Reuse vs duplication

**Guard/bridge stay POC-local** (§13.6 “Later: move … into a shared place”) while echoing main-engine concerns (ledger, provenance, landing hold). Reasonable for a pilot, but you now have **two spend philosophies** (main `cli_pipeline` vs Swirls G0) without adoption path in-lane.

**Per-episode copies** of `generate_score_piano.py` / `build_sfx.py` (Step 8–9) instead of shared modules—deferred in §9.4, but duplication debt is baked into the pilot path.

**Good reuse:** `narration_gate.py` (SWS-G1g), `independent_review.py` (Step 1), `check_landing_hold.py` (Step 9)—called out correctly.

## Cost / spend justification

**~$6.25 / at most ~$10.62** (§8) is plausible for one 45 s piece **if** rerolls stay inside planned counts—but **strict G9** (“any wording difference” FAIL) + Vision misreads (§12) can force rerolls **outside** the cap math without automatic unit grants; each extra still (40 cr) or clip (35 cr × seconds) erodes the “at most” story quickly.

**Back cover `min(15, ceil(slot + 2.0))`** (§1) can order **up to 10 s** Kling—350 cr for one unit—making a single back-cover reroll disproportionately expensive relative to the global clip cap.

**Wasted narrator synth at stability 0.3** (Step 2, pass 1) is admitted as “a few cents”; the real cost is **complexity and cache invalidation risk**, not dollars.

---

**Bottom line:** The plan is unusually honest about weaknesses (§12, §5 limits), but as a **binding** document it **overstates spend safety and build status**, **under-specifies owner authentication**, **advances picture spend before clip/hold proof**, and **leaves R1–R3 unproven** while Phase C would already spend. Substantial engineering may exist beside the text, but the artifact itself still reads like a pre-implementation target—not a synchronized operator contract.

VERDICT: REVISE  
TOP FIXES:
1. **Do not open Phase C real spend until R1–R3 pass and §13.1 owner-only `approve` exists** (or rewrite §5 to stop claiming cap discipline until then).
2. **Reconcile §0/§6 with reality**: one status table (PASS/FAIL per item), fold `BUILD_REPORT` deviations (especially G10 WARN, `swirls_guard.py` split, scored vs draft receipts) into the binding doc.
3. **Gate picture money on clip-risk proof**: complete Phase D (T8/T7b on real back-cover clips) or add explicit reroll slack + stop rules before closing the pictures ask—not only before step 6.
