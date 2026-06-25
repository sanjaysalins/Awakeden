# AWAKEDEN — Eyewitness Foundation & Roadmap

> **Brand: Awakeden** (the series, the website awakeden.com, and the YouTube/TikTok/Reels/
> Facebook channels — all work ships as Awakeden). The keystone doc for Awakeden's signature
> **eyewitness format.** Everything (skills, pipelines, slate, website, publishing) derives
> from this. Proven by the Two Goats pilot (high priest, 1:49, fully produced).
> Status: **FOUNDATION — for sign-off, then execute.**

---

## 1. Vision
A reverent, Bible-driven channel where **a biblical eyewitness tells their story and points to Christ.**
One device → two formats (short + long) → many series. A distinctive Baroque-oil world.
**Every piece lands on Jesus** (CTA-on-Jesus is law, never negotiable).

Why it wins: it turns a teaching essay into a *story* — a character, dread, a turn, an
emotional reveal. People finish stories. Almost nobody does reverent first-person biblical
testimony in this Old-Master look — it is a wide-open lane.

---

## 2. The shared DNA (both formats inherit this)

**The device.** A first-person witness recounts a moment they lived through, and discovers
(with the viewer) that it was a shadow of Christ.

**The voice.** Characterful, weathered, intimate — NOT the essay narrator. Cast a distinct
voice per witness.

**The cast (the dialogue).** witness (lead) · the LORD / Jesus · named others in their story
(a son, a fellow priest, a messenger, the people) · a dedicated **scripture** voice for all
KJV quotes. Maximize multi-voice (INV-7).

**The eyewitness spine (7 beats — same skeleton as our 7-movement long, told as the witness):**
1. **"I was there"** — hook: the witness + the moment.
2. **The world** — who they were, the weight of it.
3. **The act** — the ritual / event in their own hands.
4. **The strange detail** — the thing they never understood.
5. **The wrestling** — their honest doubt / question (the steel-man objection, *internalized*).
6. **The reveal** — Christ. *"And at last I understood…"*
7. **The invitation** — the CTA, grace-anchored, **on Jesus**. "Come."

**The law (unchanged from v2/SPEC):** KJV verbatim (span-checked); CTA always Jesus;
doctrine sound (no supersession, name the substitution); freshness = faithful depth
(surprising about the *text*, never the *truth*); one spine hook→landing.

**The look:** Baroque oil, period-accurate, full-bleed 16:9 (long) / 9:16 (short),
the reuse banks. God shown as light, not a face; crosses robed; no legible text.

---

## 3. Two INDEPENDENT pipelines (shared DNA, pick & choose)

### A) Eyewitness SHORT — ~75–110s · ~230–280 words
`script(short) → voice(2–3) → stills(6–10, reuse-heavy) → assemble(slideshow/boomerang)
 → score(music_library) → sfx → caption → publish(shorts)`
- The Two Goats pilot IS this (tighten 1:49 → ~90s for the short lane).
- Intimate, cinematic, calmer than our punchy viral cuts — a NEW short lane (A/B it
  against the rapid-cut shorts; keep whichever pulls).

### B) Eyewitness LONG — ~9–11 min · ~1300–1600 words
`script(long, full cast + dialogue) → voice(cast) → stills(20–28) → boomerang-animate(veo3)
 → assemble(slow-boomerang) → score(3-segment arc) → sfx → caption → publish(long)`
- The same witness, 5× deeper: backstory, interior life, a cast of voices, more beats,
  the reveal lingered on.
- **Boomerang animation stretches the runtime** (locked-camera atmosphere drift; the
  proven long-form fill — no freeze, no continuation-clip cost).

**Shared modules (format-agnostic — built once, used by both):** voice cast · KJV gate ·
CTA gate · the reuse banks · caption · publish. **Only the SCRIPT stage and the assemble
timing differ** between short and long — that is the seam that keeps the pipelines
independent but DNA-identical.

---

## 4. Skills (the controls) — recommended structure
Reuse the existing stage tools (voice/stills/score/sfx/caption/publish are already
format-agnostic); add a thin eyewitness layer that only changes the SCRIPT + the cut timing:

- **`/witness`** — Stage 0+1 for eyewitness: pick the witness, fetch their passage + the
  Christ-type, write the eyewitness script (`--form short|long`). Folds /study + a new
  eyewitness-narrate.
- **`/witness-voice`** — cast + synth the multi-voice read (wraps per_turn_synth).
- **`/witness-world`** — the world-manifest + reuse-check + render only the gaps (wraps
  the stills renderer + the reuse banks).
- **`/witness-cut`** — assemble (short slideshow / long boomerang), then score+sfx+caption.
- **`/publish`** — unchanged (already format-agnostic).

DNA lives in **`v2/EYEWITNESS_SPEC.md`** (the binding contract these skills enforce; built
in Phase 2 from what the Two Goats long teaches us). Short and long call the SAME skills
with `--form`; the user picks short OR long per need.

---

## 5. Reuse — YES. The catalogue is the foundation bank. ✅
**Verdict: reuse absolutely works, and the eyewitness format is MORE reuse-friendly than
the essay** — each witness lives in a world we may already own.

What we have to draw on:
- **image_library** (46 Baroque 16:9 stills) + the 5 shipped long-form episodes' stills +
  the 25 Two Goats stills → a growing painted world (the cross, the risen hero, the
  tabernacle, the wilderness, the altar — reusable across witnesses).
- **clip_library** (284 animated 16:9 clips) — reuse where topically honest (the Gaza rule:
  never force a passion clip into a ministry/own-world slot).
- **sound_library** (30 SFX) + **music_library** (8 scores) — fully reusable, $0.

**The mechanism (the cost lever):** per witness, build a **world manifest** — list the
scenes, then **check the banks FIRST** (`clip_reuse.decide_for_scene` / image_library) and
**generate only the gaps.** The gaps are usually just (a) the witness's own face and (b)
their one specific moment; the cross / hero / world plates reuse.

**Honest limits:** witness FACES are episode-specific (generate own-world); a reused clip
must match aspect (9:16 vs 16:9) and topic; the bank skews passion/cross (we still lack a
deep "living-Christ" set — own-world those). Net: reuse is the economic engine, not a
total substitute.

---

## 6. The series slate (the wells)
Each **witness = 1 long deep-dive + 3–4 shorts** distilled from it (longs-first funnel).

- **Series 1 — Old Testament Shadows** *(launch first):* the high priest ✓ (Day of
  Atonement) · Abraham (the ram / Moriah) · Moses (the bronze serpent · the Passover · the
  rock that gave water) · Noah (one door) · Joseph (betrayed to save his brothers) · Boaz
  (the kinsman-redeemer) · Jonah (three days in the deep) · Melchizedek (bread & wine,
  king-priest) · the Passover father (the night of the firstborn) · Isaiah (the suffering
  servant vision).
- **Series 2 — They Met the Messiah:** the apostles (Peter, John, Thomas, Matthew…) + the
  woman at the well · Zacchaeus · the blind man (John 9) · Lazarus · Mary Magdalene ·
  Nicodemus · the centurion.
- **Series 3 — The Cross, in Their Words:** the centurion · Simon of Cyrene · the believing
  thief · the soldier who pierced Him · Mary · John.

Three deep wells; the device is effectively unlimited.

---

## 7. Parallelization — how we launch fast (agents + subagents)
Per-witness work is **independent** → fan out. Keep the human gates and the per-episode
review discipline **serial** (panel, lock, voice/stills approval stay with the user); only
the upstream, judgment-light work parallelizes.

**Parallel lanes (subagents / Workflow):**
- **Research + script DRAFT per witness** — N drafters in parallel (one per witness),
  each: fetch the passage + the Christ-type, draft the eyewitness script to the spine.
  I review + panel each serially before lock.
- **World-manifest + reuse-check per witness** — parallel: list scenes, query the banks,
  output the render gap-list.
- **Stills-gap render** — parallel batches (HF), idempotent.
- **Finish (score/sfx/caption)** — parallel once cuts exist.

**Cadence sizing:** tell me the target (e.g. *2 longs + 8 shorts / week*) and I size the
fan-out. The slate is the backlog; the gates are the throttle.

---

## 8. Website (awakeden.com) — keep it in lockstep
- Each eyewitness piece → a **catalogue card** (title / witness / verse / hook) on ship,
  then promoted to a **rich study page** (the witness · the type · the reading · the
  paintings · the cut-outs) — the existing `_website/build_catalog.py` + `make_cutouts.py`
  machinery already does this.
- Add an **"Eyewitness" section / series** to the site; group by Series 1/2/3.
- `/update-website` builds + deploys (Netlify). As each piece locks → placeholder card; on
  finish → rich page.

---

## 9. Publish & upload paths
- **`/publish`** (Stage 6) generates the per-piece social PUBLISH PACK (YouTube / TikTok /
  Facebook / Instagram copy + captions.srt + a paste-ready index) — already format-agnostic;
  add the **"told by [witness]"** hook angle.
- **Routing:** long deep-dives → **YouTube (long)** + the website; eyewitness shorts →
  **YT Shorts · TikTok · Reels · FB**. The witness hook ("the day I watched the veil tear —
  by the high priest") travels across all platforms.
- **Tracker:** the Drive posting tracker + the website catalogue stay the source of truth.

---

## 10. Roadmap (phases + milestones)
- **Phase 0 — Foundation (now):** this doc, signed off. *(Decisions in §11.)*
- **Phase 1 — Prove the long-form** on Two Goats: write the long eyewitness script → voice
  (full cast) → boomerang-animate the 25 stills we already have → score/sfx/caption.
  *Milestone: 1 long + the short pilot, both shipped — the template seed.*
- **Phase 2 — Lock the templates:** distill `v2/EYEWITNESS_SPEC.md` + the `/witness` skills
  + the gates from Phase 1.
- **Phase 3 — Slate Series 1 (OT Shadows):** fan out scripts (subagents), longs-first,
  shorts distilled. Reuse-first per the world manifest.
- **Phase 4 — Website + publish integration:** site section live, posting rhythm running.
- **Phase 5 — Scale** to Series 2 / 3.

---

## 11. Decisions to sign off (gates the execution)
1. **Launch series = OT Shadows?** (or start elsewhere)
2. **Eyewitness becomes the PRIMARY long-form** (essay kept only for witness-less topics)? *(rec: yes)*
3. **The current essay-style #06 cut:** finish as a baseline to compare, or pivot straight
   to the eyewitness long? *(rec: pivot — we already have everything for the eyewitness long)*
4. **Cadence target** (longs + shorts per week) → sizes the parallel fan-out.
5. **Skill structure:** the `/witness*` family as in §4? *(rec: yes — thin layer over the
   existing format-agnostic stage tools)*
