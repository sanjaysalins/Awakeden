# JesusInTheBible — Domain Glossary

The ubiquitous language for the gospel-short content engine: a Bible topic
becomes a 60-second, viral-hook, CTA-to-Jesus YouTube Short (and its long-form
companion). This file is a glossary only — no implementation detail. The binding
contract lives in `v2/SPEC.md`; operational context in `CLAUDE.md`.

## Language

### Products

**Short**:
A ~60-second 9:16 vertical gospel video — the first-class product, the highest-QC deliverable.
_Avoid_: clip (a clip is one ingredient of a Short), reel.

**Long-form**:
A 16:9 ~6–8 minute deep-dive companion that supplies the research a Short is distilled from.
_Avoid_: video, deep-dive (use "long-form").

**Episode**:
One produced unit of a series — a single topic taken through the stages to a finished Short or long-form.

**Pilot**:
A v2 Short built outside the main series numbering to prove the pipeline on a new passage.

### The Stages

**Stage**:
One independent step in the pipeline, each with its own gates, panel, and red-team. The chain is Study → Narrate → Voice → Scene-plan → Stills → Animate → Assemble → SFX → Caption → Upload.

**Study**:
Stage 0 — fetch the exact KJV passage + pericope and lock one fresh, faithful Thread.

**Narrate**:
Stage 1 — write the locked KJV narration via the Draft Tournament + self-review + red-team + panel.

**Voice**:
Stage 1b — render the locked narration to a duration-locked ~59s multi-voice MP3.

**Scene-plan**:
Stage 2a — design the visual Scene set (paper only, no render).

**Stills**:
Stage 2b — render one Baroque oil PNG per Scene, each Vision-audited.

**Animate**:
Stage 2c — turn each approved still into a Clip (the Gallery-Tour cut).

**Assemble**:
Stage 3 — fit Clips + narration into the 60s cut (Hero bookend, jigsaw by phrase).

### Narration

**Thread**:
The single fresh-but-faithful spine that runs unbroken through hook → middle → CTA. One per Short; never swapped to placate feedback.
_Avoid_: angle, spine (spine is acceptable as a synonym; "thread" is canonical).

**Gospel Five-Beat**:
The narration structure: Hook → Point → Proof → Conviction → Landing, each timed.

**Hook**:
The opening scroll-stopper beat that earns the next second of attention.

**Landing**:
The closing beat. Must do NEW work and end on Christ; never a tired bare "Will you trust Him?".
_Avoid_: outro, close (close is fine informally; "landing" is canonical).

**CTA-to-Jesus**:
The grace-anchored invitation the Short drives toward — the model is preachy-with-CTA, NOT the no-CTA "Attenborough" style.

**Grace-anchored conviction**:
Conviction that invites rather than pressures — no gain/loss, fear, or manufactured-urgency framing.

**Freshness**:
Surprising about the *text*, never about the *truth* — novelty in the entry point, orthodoxy in the claim and landing.
_Avoid_: novelty, originality.

**Lever**:
The specific textual move that carries the Thread's freshness (e.g. Peter's "we"→"ye" pronoun shift in Isaiah 53:5 → 1 Peter 2:24).

**Draft Tournament**:
The default generation mode — N divergent candidate drafts → judge the hook→CTA arc → synthesize a winner + graft the best beats.

**KJV-verbatim**:
Quoted Scripture must be exact KJV (ordered, non-overlapping ellipsis fragments allowed); attribution frames stay in narrator voice.

**Multi-voice**:
The default for any scene with speakers — a dedicated Scripture voice for all KJV quotes plus a distinct voice per quoted speaker (Jesus / David / mockers). Narrator-only is the exception.

### Visual

**Scene**:
One planned image in the Scene-plan, carrying a subject, framing, beat, and cut anchors.

**Subject block**:
The state-only prose describing a Scene's central subject for the image renderer (no motion verbs — the image is a frozen tableau).

**Macro elements**:
The 3–5 named details inside a still that the Gallery-Tour is allowed to crop to. The animation may show only what is in this list.
_Avoid_: details, features.

**Vignette**:
A soft-edged background memory inside a Unified scene (3–5 per scene), never rendered in a panel, arch, or window.

**Unified scene**:
A multi-element Scene carrying several Vignettes around one foreground subject.
_Avoid_: collage, montage, split-screen.

**Hero**:
The single gospel-pivot image (the cross / Christ / NT-gospel-link) that bookends the cut open and close so the Short lands on Christ. It is NOT the emotional climax.
_Avoid_: climax, key frame.

**Gallery-Tour**:
The animation discipline — a frozen painting toured by camera-only crop-cuts (full → element → element → return); nothing new ever appears.
_Avoid_: pan-and-zoom, Ken Burns.

**Frozen tableau**:
The principle that the still never moves; only the camera does (Kling-friendly, state-only).

**Jesus variant**:
The character-consistency tag on a Christ-bearing Scene (e.g. `passion`) that pins His appearance across the set.

### Quality discipline

**Gate**:
A named pass/fail check (e.g. SP-G9, AS-G6). Deterministic gates run in Python and override the LLM verdict on their dimension.

**Red-team**:
An independent adversarial audit by a fresh hostile reviewer — standard practice at every stage, authoritative on 0-FAIL gates.

**Panel**:
The external 5-CLI independent review (cursor + claude/gemini/codex/grok) run on every LOCKED narration and significant plan, via local CLI subscriptions (no metered API).
_Avoid_: review (too generic — say "panel" for the external one, "self-review" for the in-engine one).

**Lock / LOCKED**:
The fail-closed sign-off state — reached only when no gate FAILs (plus, for any lock, the 5-CLI panel).

**Element manifest**:
The png-hash-bound, locked list of a still's verified elements; the Gallery-Tour and its gate are checked against it.

**Element gate**:
The calibrated Vision check that a Clip tours only its manifest's elements (default-PASS, any-fail, human-authoritative on the subtle).

**Coherence**:
The still-quality property a frame must hold (no floating heads, garbled text, modern props, etc.); verified and shareable by content hash.

**Speed-to-fit**:
The assembly rule to SPEED a Clip to fill its slot (show the whole Gallery-Tour) rather than TRIM it.
_Avoid_: trim-to-fit (the rejected approach).

### Reuse

**Clip library**:
The central reuse bank of finished Clips, indexed by reference and tag; pulled reuse-first to save render spend.

**Reuse-swap**:
Substituting a clean library Clip into a Scene slot at $0, re-pointing the slot's Macro elements and re-locking its manifest.

**Neutral plate**:
A thread-neutral, story-agnostic Clip (a cross, candle, hands, dawn) — the only kind allowed to be reused across unrelated Episodes.
_Avoid_: generic clip.

**Topical-fit**:
The constraint that story-specific stills (prodigal swine, Peter's denial-fire) may never be imported into an unrelated Episode.

**Backfill**:
Adding clean reuse Clips into new slots to reach a punchy clip count (~16, ~5s/slot).

**Do-not-use**:
A durable blacklist marker on a rejected Clip so reuse never pulls it again.
