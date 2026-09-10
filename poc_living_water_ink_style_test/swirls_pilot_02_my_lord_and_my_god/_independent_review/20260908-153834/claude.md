# Independent review — claude (OK, 158s)

Independent adversarial review of `FLOW_RUN_SHEET.md` (plan artifact). Findings below, most severe first, each citing exact text.

## 1. The entire automation premise is unverified against what Google Flow actually is

Section 0: *"Paste it into a FRESH Google Flow project as one message... The agent then runs the whole thing itself, start to finish, with no human re-pasting anything in between."* This assumes Flow has a conversational agent runtime that can ingest an ~8,000-word runbook, autonomously call image/video generation, attach a *specific* prior generation as an "Ingredient" by a label it invented itself, judge fine-grained visual criteria, retry, and self-report — all without a human clicking anything per shot. Flow's actual interface (a project/scene canvas with per-shot prompt boxes and an Ingredients-to-Video picker) is a materially different tool than "a chatbot you hand a runbook to." The document's own line — *"Companion... restructured so an agent can execute it without a human operator driving each step"* — admits this execution model is new and untested. Your own memory record of this exact pilot (`project_google_flow_pilot_process.md`) describes the intended flow as **"Claude writes brief, user runs Flow, Claude assembles zip"** — i.e. a human operating Flow manually, not an unattended agent. If Flow can't actually do unattended multi-step tool orchestration this way, nothing past Section 0 executes as written. This should be smoke-tested (paste just R1+R2, see what actually happens) before betting all 18 generations on it.

## 2. "Zero tolerance" is contradicted by the plan's own fallback rule

CLIP_01's check says *"Zero tolerance — any door movement fails the clip."* CLIP_04's check repeats this. But the global retry rule (Section 3, and rule 5) is: *"Still failing → keep the attempt that passes more lines, label it, write each failed line under Flags... continue."* So if **both** attempts trigger the door-movement defect, the plan ships one of them anyway and just logs a Flag. "Zero tolerance" and "ship the better of two failures regardless" cannot both be true — the document asserts a hard gate it doesn't actually enforce.

## 3. No independent QC — the generator grades its own homework, unwatched

Every check ("the hand-gap... never touches," "Thomas's outline is visibly broken, doubled, and tremored... clearly different," "a real, continuous, readable tremor") is fine-grained visual judgment performed by the same agent that just generated the asset, with the human explicitly absent (*"I am not watching between steps"*) until the FINAL REPORT. This directly contradicts a standing, explicitly non-negotiable practice recorded elsewhere in this project: *"Look at images yourself with the Read tool... don't trust the SDK audit's pass/fail signal blindly"* (`always-independent-red-team`, `feedback-verify-by-looking-not-running`), and the whole main engine's design (independent red-team audits at every stage, separate Vision-audit passes). This plan has zero independent verification step anywhere in 18 generations.

## 4. Baked multi-line handwritten text contradicts a lesson already encoded in this project's own toolkit

Nearly every still bakes in a SEQ label, frame number, three panel captions, a main caption, and a corner note — e.g. STILL_06's two-line "My Lord and" / "my God" caption, flagged as *"this exact defect has happened on this page before."* But this project's own `marginalia` skill states plainly: an image model *"cannot be trusted to spell or stay legible even when a 'no lettering' ban is in the prompt"* — which is why that skill composites text separately rather than baking it via the generator. This plan does the opposite at far higher text density (up to 6 separate text elements per still) with no compositing fallback, only "regenerate once, then ship whichever is closer."

## 5. No cost preflight for an unattended metered run

18 generations (10 stills + 8 eight-second videos), with a retry budget that makes the real worst case up to 36, run fully unattended. There's no credit/cost estimate, no budget check, and no user sign-off before firing — a clear gap against this project's own standing rule (`/cost` skill: *"pre-flight the spend of any metered batch, get explicit user OK... BEFORE any [metered] run"*). The FINAL REPORT table also has no cost column, so there's no way to reconcile spend afterward either.

## 6. REF_THOMAS/REF_JESUS have no recovery path if they fail

*"REF_THOMAS is never regenerated after this step"* — but if it fails an identity check on both attempts (e.g. wrong face shape), the fallback is still "keep the attempt that passes more lines... continue," silently propagating a wrong-looking Thomas into 6 of the 8 downstream shots (S2–S7 all attach REF_THOMAS). There's no "stop and flag for the user" branch for a failed *reference*, even though everything else depends on it.

## 7. Audio pass/fail criteria are checked with a visual-only instruction

Every clip requires "no dialogue... ambient only," but Section 3's check procedure says only: *"watch the clip from its first frame to its last frame."* Nowhere does it say to actually listen to the track. For a document this legalistic about every other detail, that's a real gap.

---

VERDICT: REVISE
TOP FIXES:
1. Before committing to all 18 generations, smoke-test whether Flow can actually execute this chat-agent/autonomous-runbook model at all (paste just R1+R2+S1) — the whole plan is void if it can't.
2. Resolve the "zero tolerance" vs. "ship after 2 failed attempts" contradiction — either add a real stop-and-flag-for-user branch on hard-gate failures (especially on REF_THOMAS/REF_JESUS and door-movement rules), or drop the "zero tolerance" language.
3. Add an explicit second-pass check by Claude/the user on the returned assets before they're treated as final — don't rely solely on Flow's own self-graded pass/fail, consistent with this project's standing independent-review discipline.
