# RENDER GUARDRAILS — common defect themes (distilled from the 17 quarantined stills)

Derived 2026-06-17 from the user-confirmed bad stills (`_rejected_coherence/`). Each theme is a
recurring AI-render failure; the FIX is a subject_block / prompt rule to prevent recurrence, and
the matching gate code (F1–F5 in `pipeline/coherence_gate.py`) that catches it if it slips.

> Apply these at STILL generation (scene_plan `subject_block` + the negative/style tail) so the
> model never gets the chance. The gate is the backstop, not the first line of defense.

---

## T1 — Written Scripture renders as GARBLED text  → gate F5 / IMG-NOTEXT
**Seen:** the-greek-word, the-scroll-line, the-fingertip-on-the-final-word, the *a-thousand-years* scrolls.
**Why:** when a verse/word is the SUBJECT, the model fills a scroll/book with gibberish lettering that dominates the frame.
**FIX (prompt):**
- NEVER make written text the subject. Convey "the Word / the verse" through a *gesture* (a hand resting on a closed book, a finger tracing an unseen line) — not legible script.
- If a scroll/book must appear, keep it **small, peripheral, edge-on, or deep in shadow**; spec "no legible or decorative lettering — surface bare or abstract indistinct marks only."
- Forbid: `lettering, script, Hebrew/Greek text, inscription, writing covering the page, words visible`.

## T2 — Split-screen / diptych / triptych / frame  → gate F2
**Seen:** a-thousand-years-apart (David ↔ Christ diptych, ×3), glory_exalted (triptych), isa53_servant (gilded frame + grey panels).
**Why:** "two moments across time" concepts (then-vs-now) invite a two-panel layout; ornate-painting prompts invite a frame.
**FIX (prompt):**
- Render across-time ideas as **ONE unified scene** — e.g. the scribe in the foreground with the cross as a soft *vision/memory* behind him, NOT two side-by-side panels.
- Always spec: "a single full-bleed scene, edge to edge; **no frame, no border, no canvas edge, no dividing line, no diptych/triptych panels, no split screen.**"
- Forbid: `frame, border, panel, diptych, triptych, split screen, vertical divider`.

## T3 — Faces: divergent eyes / sickly / grotesque expression  → gate F3  (THE #1 risk)
**Seen:** gods-staggering-word, aimed-at-you, look-at-him, they-shoot-out-the-lip, the-shaking-heads, if-thou-be, come-to-the-one.
**Why:** tight close-ups + a direct wide-eyed or upward stare make the model render mismatched/divergent/dead eyes or a teeth-baring grimace. (NOTE: a *gaunt, sorrowful, anguished* face is GOOD — the failure is broken eyes or a grotesque grimace, not suffering.)
**FIX (prompt):**
- Spec eyes explicitly: "both eyes level, the same size, looking in the SAME direction; calm and sorrowful, not staring."
- Prefer **downcast or closed eyes, or a 3/4-turned head** over a head-on wide-eyed gaze.
- Prefer a **mid-shot** over an extreme tight face close-up (tight crops magnify eye errors).
- Mouth **closed or barely parted**; no bared teeth, no open-mouth grimace.

## T4 — Wrong sacred object (gem instead of iron nail)  → gate F4/F3-object
**Seen:** the-marks-of-one.
**Why:** a macro of a nail head reads to the model as a faceted dark gem/bead.
**FIX (prompt):** spec "a rough, dull, hand-forged **IRON spike**, dark grey, no shine." Forbid: `gem, jewel, crystal, faceted, glossy bead, ornament`.

## T5 — Crowd face mush  → gate F3/F5
**Seen:** the-shaking-heads, exiled_nation_column_grey.
**Why:** many prominent faces = many chances for distortion.
**FIX (prompt):** keep **≤3 sharply-rendered faces**; push the rest into shadow, soft-focus, back-turned, or hooded. "Crowd reads as a mass, not individual portraits."

## T6 — Modern / anachronistic props  → gate F1
**Seen:** exiled_nation_column_grey (a modern-reading flag/banner).
**Why:** flags/banners/objects drift modern.
**FIX (prompt):** "strictly first-century / ancient Near East; **no modern flags, banners, fabrics, objects, dress, or hairstyles.**" Forbid: `modern, contemporary, flag, banner, logo`.

---

## Wiring plan (where these go)
1. **Constitution VISUAL ARC** (`data/constitution.md`) — add T1–T6 as binding render rules so the scene-plan stage bakes them into every `subject_block` (prompt-cached, $0).
2. **Negative tail** in `pipeline/visual_render.assemble_final_prompt` — append the forbid-lists (T1/T2/T4/T6 tokens) to every render.
3. **`config.VISUAL_BANNED_TOKENS`** — add `frame, border, panel, diptych, triptych, split screen, gem, jewel, faceted, flag, banner, modern` so the deterministic banned-token check + the audit prompt both carry them.
4. **Gate** already covers all six (F1–F5) as the backstop.
