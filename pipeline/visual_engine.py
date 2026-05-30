"""Visual stage engine: scene plan discovery + (in later chunks) review,
independent audit, revise, and cohesion audits.

Mirrors the discipline of pipeline.engine — same cached system prefix
(constitution + series library), same JSON-only output contract, same
writer-side / auditor-side block split (writer sees the thread as spine to
execute on; auditor sees it as a contract to verify).
"""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import replace
from typing import Iterable

import config
from pipeline import engine as text_engine  # reuse _call / _extract_json / _episode_block / _INDEPENDENT_PREAMBLE
from pipeline.models import Draft, Thread
from pipeline.series import Episode, Series
from pipeline.visual_models import (
    AgentVerdict,
    CohesionAudit,
    GateResult,
    ScenePlan,
    ScenePlanReview,
)


# --------------------------------------------------------------------------
# Writer-side / auditor-side blocks
# --------------------------------------------------------------------------
def _scene_thread_block(thread: Thread | None) -> str:
    """Writer-side: the thread is the spine of the visual arc, same way it is
    the spine of the script. Open on the anchor detail, mirror at the climax,
    close on the gospel landing."""
    if thread is None or thread.is_empty:
        return ""
    return (
        "\n\n=== VISUAL SPINE — THREAD (carry this through opening -> climax -> closing scenes) ===\n"
        f"THREAD: {thread.thread}\n"
        f"LEVER: {thread.lever}\n"
        f"ANCHOR: {thread.anchor_ref} — {thread.anchor_detail}\n"
        f"WHY FRESH: {thread.why_fresh}\n"
        f"GOSPEL LANDING: {thread.gospel_landing}\n"
        "Open the visual arc on the anchor detail (the hook scene IS the thread "
        "made visible). Mirror the thread at the central confrontation scene. "
        "Close on the gospel-landing scene. Do not abandon the thread for a "
        "Sunday-school highlight reel."
    )


def _narration_block(draft: Draft) -> str:
    """The narration laid out beat-by-beat so the planner can produce
    `beat_coverage` (SP-G2). Beat ids are the structure ids — for the Gospel
    Five-Beat that is hook / point / proof / conviction / landing."""
    rows = "\n".join(f"[{b.id}] {b.text}" for b in draft.beats)
    return (
        "\n\n=== NARRATION (locked) ===\n"
        f"TITLE: {draft.title}\n"
        f"SCRIPTURE REFERENCE: {draft.scripture_reference}\n"
        f"SCRIPTURE QUOTED: {draft.scripture_quoted}\n"
        f"NON-NARRATOR SPEAKERS: {', '.join(draft.speakers) if draft.speakers else '(narrator only)'}\n"
        f"BEAT IDS: {draft.beat_ids}\n\n"
        f"BEATS (id-tagged):\n{rows}"
    )


def _passage_block(passage: str | None) -> str:
    if not passage:
        return ""
    return (
        "\n\n=== WIDER PERICOPE (verse-numbered; mine for symbolic supporting scenes "
        "and overlooked details — cite specific verses in `rationale` where relevant) ===\n"
        + passage
    )


# Short narration windows (seconds) that deserve a purpose-built INSERT shot
# (a single macro detail) rather than a full tableau.
INSERT_WINDOW_MAX_S = 2.6


def _board_block(timeline) -> str:
    """The audio timeline so the planner maps scenes to the spoken beats and
    knows which beats are TINY (→ insert shots). `timeline` is a list of
    NarrationSegment (duck-typed: .section/.speaker/.start_s/.end_s/.duration_s/.text)
    or None. Built by assembly_timing.build_timeline upstream."""
    if not timeline:
        return ""
    rows = []
    tiny = []
    for s in timeline:
        flag = "  <-- TINY beat: give it a dedicated ~2s INSERT shot (single macro)" \
            if s.duration_s <= INSERT_WINDOW_MAX_S else ""
        rows.append(f"[{s.section}] {s.start_s:.1f}-{s.end_s:.1f}s ({s.duration_s:.1f}s) "
                    f"{s.speaker}: {s.text}{flag}")
        if s.duration_s <= INSERT_WINDOW_MAX_S:
            tiny.append(f"{s.section} ({s.duration_s:.1f}s)")
    note = (f"\nTINY beats needing a dedicated INSERT shot: {', '.join(tiny)}." if tiny
            else "\n(no sub-2.6s beats — no inserts strictly required.)")
    return (
        "\n\n=== NARRATION TIMELINE (the audio the cut runs against — map scenes to "
        "these spoken windows) ===\n" + "\n".join(rows) + note
    )


# --------------------------------------------------------------------------
# JSON contract
# --------------------------------------------------------------------------
def _scene_plan_json_contract(beat_ids: Iterable[str]) -> str:
    """The exact JSON shape ScenePlan.from_json parses. Lower-case enum values
    everywhere; index is 1-based to match the deterministic filename stem."""
    beat_keys = ", ".join(f'"{b}"' for b in beat_ids)
    return (
        "{\n"
        '  "visual_reading": "1-2 paragraph summary of the visual + emotional arc",\n'
        '  "red_team_notes": "your own honest red-team of the candidate list before selection — what would the Jaded Viewer say?",\n'
        '  "candidates": [\n'
        "    {\n"
        '      "title": "short evocative scene title",\n'
        '      "scene_type": "single | unified",\n'
        '      "arc_position": "opening-hook | biblical-setting | public-misunderstanding | central-conflict | personal-confrontation | emotional-turning | theological-centre | revelation | nt-gospel-link | human-response | closing-devotional | symbolic-support",\n'
        '      "framing": "wide | mid | close | overhead | low-angle",\n'
        '      "purpose": "what this scene does in the narration arc",\n'
        '      "rationale": "why this scene rather than the topic auto-complete",\n'
        '      "visible_elements": "what MUST be visible in the rendered image (used by SP-G1 + image audit)",\n'
        '      "emotional_tone": "one-line tone"\n'
        "    }\n"
        "    // propose 6-10 candidates spanning the arc beats; you will pick from these\n"
        "  ],\n"
        '  "scenes": [\n'
        "    {\n"
        '      "index": 1,\n'
        '      "slug": "lowercase-kebab-slug-for-the-filename",\n'
        '      "title": "...",\n'
        '      "scene_type": "single | unified",\n'
        '      "arc_position": "...",\n'
        '      "framing": "...",\n'
        '      "purpose": "...",\n'
        '      "rationale": "...",\n'
        '      "visible_elements": "...",\n'
        '      "emotional_tone": "...",\n'
        '      "subject_block": "prose describing the main subject(s), action HELD AS STATE, supporting figures, and the setting — this goes BETWEEN the fixed style base and the fixed style tail. Do NOT include the style base wording. STATE WORDS ONLY (no verbs of motion: \'caught mid-sprint\' not \'running\'; \'lips parted around an unfinished word\' not \'speaking\'; \'dust caught mid-air\' not \'dust rising\'). ~50-100 words.",\n'
        '      "mood_block": "one-line emotional / atmospheric tone (e.g. \\"atmosphere of holy confrontation and personal decision\\")",\n'
        '      "jesus_variant": "ministry | passion | resurrection | infant | null",\n'
        '      "priority": 0,\n'
        '      "macro_elements": ["3-5 distinct small visual details a downstream cut planner can macro-insert (a fingertip, a torn parchment edge, a sandalled foot, a signet ring, a single tear, a frayed garment edge). These are CUT ANCHORS for the Kling stage — make sure they are explicitly visible in your subject_block too."],\n'
        '      "vignettes": ["FOR scene_type=unified ONLY: 3-5 short named background vignettes that the renderer will interpolate as \'subtle background vignettes fading into shadow suggesting <comma-joined>\'. Gold-standard pattern: \'the running father\', \'the kiss on the neck\', \'the swallowed bargain\', \'a robe being carried\', \'the elder brother at the threshold\'. Each is a memory/echo bleeding into shadow; the foreground subject stays dominant. Leave as [] for scene_type=single."],\n'
        '      "pacing": "controlled | slower | faster   (recommended pacing mode for the downstream Kling cut plan, per SKILL_locked.md — reverent/contemplative -> slower, dramatic/climactic -> faster, default -> controlled)",\n'
        '      "viral_role": "hook-open | build | pivot | climax | close   (this scene\'s role in a viral-style edit; advisory metadata for the final cut sequencing)",\n'
        '      "shot_kind": "standard | hero | insert   (hero = the gospel-pivot image that BOOKENDS the final cut open+end, so the Short lands on Christ — make it iconic, near-still, loop-friendly; insert = a single-macro ~2s shot purpose-built for a TINY narration beat, see the NARRATION BOARD; standard = everything else)"\n'
        "    }\n"
        f"    // produce between {config.VISUAL_MIN_SCENES} and {config.VISUAL_MAX_SCENES} scenes, "
        "indices 1..N in order. Adaptive: short reflective verses get 4-6; medium passages 8-12; **rich parables and Gospel encounters should land at 14-20 scenes** so the user picks from a deeper field. Do NOT self-limit at 8-12 for rich passages — the candidate pool feeds downstream selection.\n"
        "  ],\n"
        '  "short_priority": [<scene indices in rank order, ' + str(config.VISUAL_SHORT_PRIORITY_DEFAULT) + " picks (5-8 ok)>],\n"
        '  "hero_candidate": <scene index of the ONE gospel-pivot image that bookends the final cut (open + close) so it lands on Jesus — the cross / passion / NT-gospel-link scene, NOT the most emotional moment. Mark that same scene shot_kind:\\"hero\\".>,\n'
        '  "rationale": "why this scene set vs. the candidates you rejected",\n'
        '  "beat_coverage": {\n'
        f"    {beat_keys}: [<scene indices that support this beat>, ...]\n"
        "  }\n"
        "}"
    )


# --------------------------------------------------------------------------
# Stage V0 — discover_scenes
# --------------------------------------------------------------------------
def discover_scenes(
    series: Series,
    episode: Episode,
    draft: Draft,
    thread: Thread | None,
    kjv_passage: str | None,
    timeline=None,
) -> ScenePlan:
    """Mine the locked narration + wider pericope to produce a full visual
    arc: 6-10 candidate scenes via the visual cliché blocklist + the four
    levers, choose 4-12 final scenes, fill beat_coverage so SP-G2 can be
    checked deterministically, and rank the 5-8 strongest for the short cut.

    The thread (if present) is the spine — opening / climax / closing scenes
    must carry it. See constitution -> "VISUAL ARC — SCENES AS A SECOND CHARTER".

    `timeline` (optional, list of NarrationSegment) is the AUDIO timeline; when
    present the planner sees each spoken window's length and designs cut-aware:
    a gospel-pivot HERO that bookends the cut, and dedicated ~2s INSERT shots for
    tiny beats. Provider-agnostic (helps the cut regardless of video backend)."""
    beat_ids = draft.beat_ids
    role = (
        "YOUR TASK: produce a complete VISUAL SCENE PLAN for the LOCKED narration "
        "below, obeying the charter's \"VISUAL ARC — SCENES AS A SECOND CHARTER\" "
        "section verbatim. Be surprising about the moment, never about the truth.\n\n"
        "Process (do this internally before emitting JSON):\n"
        "1. Read the narration's thread (if present). It is the visual spine.\n"
        "2. Mine the wider pericope AND the broader gospel context — overlooked "
        "objects, cultural details, OT echoes the NT confirms, AND the Jesus / "
        "NT-gospel link this passage echoes (for parables: Jesus telling the story, "
        "the murmuring audience He addressed it to, the cross as the cost the "
        "parable previews, 'joy in heaven over one sinner', the elder brother as "
        "the Pharisee mirror; for Gospel encounters: passion / resurrection link, "
        "explicit OT echoes Jesus or an apostle named).\n"
        "3. Propose 6-10 candidates spanning the available arc beats — opening-hook, "
        "biblical-setting, public-misunderstanding, central-conflict, "
        "personal-confrontation, emotional-turning, theological-centre, revelation, "
        "nt-gospel-link, human-response, closing-devotional, symbolic-support. Use "
        "the beats the narration earns; do not force all 11. Refuse cliché-blocklist "
        "auto-completes and write a rationale explaining what you chose instead.\n"
        "4. Red-team your candidate list in `red_team_notes` BEFORE selecting. What "
        "would the Jaded Viewer say? Which scenes are obvious? Which arc beat is "
        "underserved? Which scenes overlap?\n"
        "5. Select the final scenes from the candidates. Aim for the visual cliché "
        "blocklist to be visible in your rejection rationale, not your selection.\n"
        f"6. Fill `beat_coverage` so every beat id in {beat_ids} has at least one "
        "supporting scene index. This is a hard FAIL gate if any beat is uncovered.\n"
        "7. Pick a short_priority of 5-8 scenes for the rendered cut. Set "
        "`priority` on those scenes from 1 (highest) downward.\n\n"
        "TARGET SCENE COUNT (lifted): rich parables and Gospel encounters land at "
        "**14-20 scenes**. The user picks the rendered short_priority list (5-8) from "
        "this richer field — DO NOT self-limit at 8-12. Medium passages 8-12; short "
        "reflective verses 4-6. The candidate pool BEFORE selection should be even "
        "larger (18-25 candidates). Quantity at the planning stage is free; missing a "
        "strong scene at the rendering stage is not.\n\n"
        "TARGET SCENE MIX (SP-G9 deterministic gate — non-negotiable for rich passages):\n"
        "  - **5+ hero `single` scenes** (for n>=14) or 3-4 (for n=8-13) — the focused "
        "literal moments (one subject, one held state, one emotional centre).\n"
        "  - **4+ `unified` multi-dimension scenes** (for n>=14) or 2-3 (for n=8-13) — "
        "one coherent painted image with subtle background vignettes (≤20% canvas each, "
        "soft-edged, never in panels/arches/windows). These carry the theological "
        "centre AND act as the gospel-link / OT-echo carriers.\n"
        "  - **2+ Jesus / NT-gospel-link scenes** (for n>=14) or 1-2 (smaller) — "
        "`arc_position: nt-gospel-link`. For a parable: Jesus telling the story to the "
        "audience He defended (Luke 15:1-3 — murmuring Pharisees + publicans/sinners); "
        "vignette tying the parable to its gospel fulfilment (cross as the running "
        "Father's cost; elder brother as Pharisee mirror Christ took on; 'joy in "
        "heaven over one sinner'). For Gospel scenes: passion or resurrection link.\n"
        "  - **2+ OT-echo scenes** (for n>=14) or 1-2 (smaller) — `arc_position: "
        "ot-echo`. An Old Testament passage Jesus or an apostle explicitly anchored "
        "this scene to. For the prodigal: Hosea 14 'I will heal their backsliding, I "
        "will love them freely'; Deuteronomy 30 'thou shalt return unto the LORD'; "
        "Isaiah 49 'a father pitieth his children'. Real cited echoes only — no "
        "typological reach.\n\n"
        "NEVER produce a plan that is 100% `single` for a rich passage. The Jaded "
        "Viewer will read that as a slideshow of illustrations, not a study.\n\n"
        "KLING-FRIENDLY IMAGES (the downstream `image_to_kling.py` cut planner reads "
        "the rendered image and writes 6-9 camera-only cuts inside a 10s clip — crop, "
        "push-in, macro insert. The image must be cut-plannable):\n"
        "  - **State-only subject_block.** No motion verbs. 'caught mid-sprint', not "
        "'running'. 'lips parted around an unfinished word', not 'saying'. 'dust "
        "caught mid-air', not 'dust rising'. The painting is a frozen tableau; only "
        "the camera moves.\n"
        "  - **3-5 distinct macro-insertable details per scene**, listed in the "
        "`macro_elements` field AND visible in `subject_block`. These are the anchors "
        "the cut planner will macro-insert (a fingertip, a torn parchment edge, a "
        "sandalled foot, a signet ring, a single tear, a frayed garment edge, an oil "
        "lamp's flame). A scene with one undifferentiated visual mass yields a weak "
        "10s clip.\n"
        "  - **Pacing recommendation per scene** (`pacing` field) — reverent / "
        "contemplative scenes -> 'slower'; dramatic / climactic -> 'faster'; default "
        "-> 'controlled'. This is consumed by the downstream cut planner.\n"
        "  - **Viral-edit role per scene** (`viral_role` field) — `hook-open | build "
        "| pivot | climax | close`. The eventual cut sequence wants variety in role "
        "as well as content; declaring this up front lets the editor reach for a "
        "real arc when assembling.\n\n"
        "MULTI-ELEMENT UNIFIED SCENE DISCIPLINE (when scene_type = 'unified'):\n"
        "- Subject_block describes the FOREGROUND subject FIRST (one dominant "
        "centre, with postures and expressions). Then a single phrase listing "
        "3-5 named background vignettes in this exact form: 'subtle background "
        "vignettes fading into shadow suggesting <vignette 1>, <vignette 2>, "
        "<vignette 3>, and <vignette 4>'. Gold-standard example from the user: "
        "\"Jesus standing before his disciples with calm searching authority, "
        "the disciples gathered close in a half-circle, some looking down in "
        "reflection, some looking at Jesus with dawning conviction, subtle "
        "background vignettes fading into shadow suggesting miracles, parables, "
        "mercy toward sinners, and power over creation.\"\n"
        "- ALSO list those same 3-5 vignettes in the structured `vignettes` "
        "field as short noun phrases — this is the cut planner's anchor list. "
        "Counts: minimum 3, maximum 5. Each vignette must be a memory / echo / "
        "fading detail that supports the foreground, not a competing scene.\n"
        "- NEVER use frames / panels / arches / windows / split-screen. The "
        "vignettes BLEED into the painted surface as soft-edged shadow.\n"
        "- Image models tend to promote vignettes to competing main subjects — "
        "the 'subtle background vignettes fading into shadow' phrasing + "
        "'half-dissolved' / 'soft-edged' qualifiers anchor them as supporting.\n\n"
        "SUBJECT/MOOD BLOCK DISCIPLINE (renderer concatenates STYLE_BASE + subject_"
        "block + ',' + mood_block + STYLE_TAIL):\n"
        "- `subject_block`: prose ~50-100 words; state words, not action verbs; "
        "  begin mid-sentence; do NOT restate the style base.\n"
        "- `mood_block`: one short line — \"atmosphere of <core meaning>\" / "
        "  \"warm golden light illuminating <focus>\".\n\n"
        "WHEN JESUS IS IN THE SCENE: set `jesus_variant` — \"ministry\" (default "
        "for teaching / parables / encounters), \"passion\" (trial / cross), "
        "\"resurrection\" (post-empty-tomb), \"infant\" (nativity / temple-at-12). "
        "Leave null when Jesus is not literally present.\n\n"
        "COMPOSITION DISCIPLINE (SP-G8): at least 3 distinct framings across the "
        "scene set, no single framing on >50% of scenes.\n\n"
        "DESIGN FOR THE CUT (the scene plan feeds a 60s assembled Short — design so "
        "the clips drop into the cut cleanly):\n"
        "  - **Nominate a HERO** (`hero_candidate` + that scene's `shot_kind:\"hero\"`). "
        "It bookends the cut's OPEN and CLOSE, so it MUST be the gospel-pivot — the "
        "cross / passion / NT-gospel-link image the CTA points to (NOT the most "
        "emotional moment). Design it iconic, near-still, and loop-friendly (open and "
        "close land on the same held image).\n"
        "  - **Tiny narration beats get a dedicated INSERT** (`shot_kind:\"insert\"`). "
        "If the NARRATION TIMELINE shows a sub-2.6s window (a one-line aside, a single "
        "quoted phrase), plan a purpose-built ~2s shot = ONE macro detail (a torn "
        "parchment, a clenched hand, a single tear), not a full tableau that must be "
        "crushed into 2s.\n"
        "  - **One dominant motion per scene.** Each clip will be sped/trimmed to fit "
        "its slot; favour ONE clear camera move on a held tableau, not busy multi-"
        "action that turns to mush when accelerated.\n"
        "  - **Front-load the emotional payload** (the tear, the embrace, the wound) in "
        "the composition's centre so it survives a head-biased trim.\n"
        "  - Sacred scenes (cross / Christ / the landing) are played near full speed "
        "downstream — design them to READ in a slow, reverent hold.\n\n"
        "Return ONLY a JSON object (optionally inside a ```json fence) in this exact "
        "shape:\n"
        f"{_scene_plan_json_contract(beat_ids)}\n"
        "No prose outside the JSON object."
    )

    user = (
        text_engine._episode_block(series, episode, draft.scripture_quoted or None, "")
        + _passage_block(kjv_passage)
        + _scene_thread_block(thread)
        + _narration_block(draft)
        + _board_block(timeline)
    )
    reply = text_engine._call(role, user)
    return ScenePlan.from_json(text_engine._extract_json(reply))


# --------------------------------------------------------------------------
# Stage V3 — paper_cohesion (one Opus call before any image renders)
# --------------------------------------------------------------------------
def paper_cohesion(
    series: Series,
    episode: Episode,
    draft: Draft,
    plan: ScenePlan,
    thread: Thread | None,
    kjv_passage: str | None,
) -> CohesionAudit:
    """Plan-level cohesion check, run AFTER the scene plan reaches LOCKED and
    BEFORE any image renders. Catches set-level theology drift, narration-
    scene mismatch, or a freshness lever that breaks across scenes — issues
    the per-scene gates may miss because they only see one scene at a time.
    Blocking: if `passed` is false, the runner does not proceed to Phase B."""
    role = (
        "YOUR TASK: paper-cohesion audit of a LOCKED scene plan against its "
        "narration, intended thread, and wider pericope. The per-scene gates have "
        "passed; you are checking the SET as a whole.\n\n"
        "Check for:\n"
        "- Plan-level theology drift: scenes that individually pass biblical "
        "accuracy but as a set imply a doctrine the narration does not teach.\n"
        "- Narration-scene mismatch: any narration beat the plan covers only "
        "weakly (one scene that doesn't really carry the beat).\n"
        "- Thread fracture: the opening / climax / closing scenes don't actually "
        "form a coherent visual spine.\n"
        "- Freshness drift across the set: the visual cliché blocklist applies "
        "scene-by-scene, but the SET can still feel like a generic Bible-reel — "
        "flag that here.\n"
        "- Character-of-Jesus drift across scenes (different mood / posture / "
        "purpose in a way that breaks coherence even if each is technically right).\n\n"
        "Return ONLY a JSON object (optionally inside a ```json fence):\n"
        "{\n"
        '  "scope": "paper",\n'
        '  "passed": true | false,\n'
        '  "notes": "1-2 paragraph summary of what you found",\n'
        '  "conflict_scenes": [<scene indices that drive the failure if passed=false>]\n'
        "}\n"
        "No prose outside the JSON object. Set `passed=false` only when a real "
        "structural failure is present — otherwise PASS with notes."
    )
    user = (
        text_engine._episode_block(series, episode, draft.scripture_quoted or None, "")
        + _passage_block(kjv_passage)
        + _scene_thread_review_block(thread)
        + _narration_block(draft)
        + _scene_plan_block(plan)
    )
    reply = text_engine._call(role, user, model=config.REVIEW_MODEL)
    data = text_engine._extract_json(reply)
    data.setdefault("scope", "paper")
    return CohesionAudit.from_json(data)


# --------------------------------------------------------------------------
# Auditor-side block + deterministic gate pre-checks (SP-G2 / G5 / G8)
# --------------------------------------------------------------------------
def _scene_thread_review_block(thread: Thread | None) -> str:
    """Auditor-side: the thread is a contract to verify — does the plan
    actually carry it from the opening scene through the climax to the
    closing scene? Or has it drifted to a Sunday-school highlight reel?"""
    if thread is None or thread.is_empty:
        return ""
    return (
        "\n\n=== INTENDED VISUAL SPINE — THREAD (the plan was written to carry this) ===\n"
        f"THREAD: {thread.thread}\n"
        f"LEVER: {thread.lever}\n"
        f"ANCHOR: {thread.anchor_ref} — {thread.anchor_detail}\n"
        f"WHY FRESH: {thread.why_fresh}\n"
        f"GOSPEL LANDING: {thread.gospel_landing}\n"
        "Check whether the opening / climax / closing scenes actually carry "
        "this thread and whether the freshness remains exegetically honest "
        "(no contrarian eisegesis dressed as visual surprise)."
    )


def _check_sp_g2(plan: ScenePlan, beat_ids: list[str]) -> GateResult:
    """Narration Alignment: every narration beat id must appear in
    beat_coverage with >=1 scene index. Hard FAIL if any beat is uncovered."""
    covered = {k.strip() for k, v in plan.beat_coverage.items() if v}
    missing = [b for b in beat_ids if b not in covered]
    if missing:
        return GateResult(
            gate="SP-G2 Narration Alignment",
            verdict="FAIL",
            evidence=(
                f"Beat(s) without supporting scene: {missing}. "
                f"Covered beats: {sorted(covered)}."
            ),
            fix=f"Add at least one scene to beat_coverage for each missing beat: {missing}.",
        )
    return GateResult(
        gate="SP-G2 Narration Alignment",
        verdict="PASS",
        evidence=f"Every beat id in {beat_ids} has >=1 supporting scene.",
    )


def _check_sp_g5(plan: ScenePlan) -> GateResult:
    """Prompt Conformance: per-scene subject_block + mood_block carry no
    banned tokens (case-insensitive substring). Style base + tail are Python
    constants, so this gate only judges what the model returned."""
    hits: list[tuple[int, str, str]] = []
    for scene in plan.scenes:
        blob = (scene.subject_block + " " + scene.mood_block).lower()
        for tok in config.VISUAL_BANNED_TOKENS:
            if tok in blob:
                hits.append((scene.index, scene.title, tok))
    if hits:
        sample = "; ".join(f"scene {i} '{t}' contains '{tok}'" for i, t, tok in hits[:5])
        more = "" if len(hits) <= 5 else f" (+{len(hits) - 5} more)"
        return GateResult(
            gate="SP-G5 Prompt Conformance",
            verdict="FAIL",
            evidence=f"Banned token(s) in per-scene blocks: {sample}{more}.",
            fix="Rewrite affected subject_block / mood_block to avoid banned tokens (see constitution VISUAL ARC).",
        )
    return GateResult(
        gate="SP-G5 Prompt Conformance",
        verdict="PASS",
        evidence="All subject_block + mood_block content clear of the banned-token list.",
    )


_NT_LINK_TOKENS = ("nt-link", "nt-gospel-link", "gospel-link", "gospel-frame")
_OT_LINK_TOKENS = ("ot-echo", "ot-link", "ot-fulfilment", "old-testament")


def _matches_any(s: str, tokens: tuple[str, ...]) -> bool:
    s_low = s.lower()
    return any(tok in s_low for tok in tokens)


def _check_sp_g9(plan: ScenePlan) -> GateResult:
    """Scene Mix & Gospel Frame (deterministic). Scales by scene count so
    reflective short narrations are not over-constrained while rich parables
    get the full mix the user expects.

    Targets (`#` = required, `.` = strongly recommended):
    | scene_count | single | unified | nt-link | ot-echo |
    | 14+         | #5+    | #4+     | #2+     | #2+     |
    | 8-13        | #3+    | #2+     | #1+     | #1+     |
    | 5-7         | #2+    | #1+     | #1+     | . 0+    |
    | <5          | #2+    | . 0+    | . 0+    | . 0+    |

    See constitution -> 'Mandatory scene mix' for the binding rules."""
    n = len(plan.scenes)
    single_count = sum(1 for s in plan.scenes if s.scene_type == "single")
    unified_count = sum(1 for s in plan.scenes if s.scene_type == "unified")
    nt_link_count = sum(1 for s in plan.scenes if _matches_any(s.arc_position, _NT_LINK_TOKENS))
    ot_echo_count = sum(1 for s in plan.scenes if _matches_any(s.arc_position, _OT_LINK_TOKENS))

    failures: list[str] = []
    if n >= 14:
        if single_count < 5:
            failures.append(f"only {single_count} `single` scene(s); need >=5 hero singles for a 14+ plan")
        if unified_count < 4:
            failures.append(f"only {unified_count} `unified` scene(s); need >=4 multi-element scenes for a 14+ plan")
        if nt_link_count < 2:
            failures.append(f"only {nt_link_count} Jesus / NT-gospel-link scene(s); need >=2 for a 14+ plan")
        if ot_echo_count < 2:
            failures.append(f"only {ot_echo_count} OT-echo scene(s); need >=2 for a 14+ plan")
    elif n >= 8:
        if single_count < 3:
            failures.append(f"only {single_count} `single` scene(s); need >=3 hero singles for an 8+ plan")
        if unified_count < 2:
            failures.append(f"only {unified_count} `unified` scene(s); need >=2 multi-element scenes for an 8+ plan")
        if nt_link_count < 1:
            failures.append("no Jesus / NT-gospel-link scene (need >=1 with arc_position like nt-gospel-link / gospel-link)")
        if ot_echo_count < 1:
            failures.append("no OT-echo scene (need >=1 with arc_position like ot-echo / ot-link — an OT passage the NT confirms)")
    elif n >= 5:
        if single_count < 2:
            failures.append(f"only {single_count} `single` scene(s); need >=2")
        if unified_count < 1:
            failures.append("no `unified` scenes; need >=1 multi-element scene for the theological centre / gospel link")
        if nt_link_count < 1:
            failures.append(f"no Jesus / NT-gospel-link scene (none of arc_position in {_NT_LINK_TOKENS})")
    else:
        if single_count < 2:
            failures.append(f"only {single_count} `single` scene(s); need >=2")

    if failures:
        return GateResult(
            gate="SP-G9 Scene Mix & Gospel Frame",
            verdict="FAIL",
            evidence="; ".join(failures),
            fix="Add the missing scenes — see constitution -> 'Mandatory scene mix' for the target mix per plan size.",
        )
    return GateResult(
        gate="SP-G9 Scene Mix & Gospel Frame",
        verdict="PASS",
        evidence=(
            f"n={n}: single={single_count}, unified={unified_count}, "
            f"nt-link={nt_link_count}, ot-echo={ot_echo_count}"
        ),
    )


def _check_sp_g8(plan: ScenePlan) -> GateResult:
    """Composition Distribution: at least 3 distinct framings; no single
    framing on more than 50% of scenes."""
    framings = [s.framing for s in plan.scenes if s.framing]
    n = len(framings)
    if n == 0:
        return GateResult(
            gate="SP-G8 Composition Distribution",
            verdict="FAIL",
            evidence="No `framing` declared on any scene.",
            fix="Add framing ∈ {wide, mid, close, overhead, low-angle} to every scene.",
        )
    counts = Counter(framings)
    distinct = len(counts)
    most_common, most_n = counts.most_common(1)[0]
    failures: list[str] = []
    if distinct < 3:
        failures.append(f"only {distinct} distinct framing(s) {sorted(counts)}; need >=3")
    if most_n / n > 0.5:
        failures.append(f"'{most_common}' covers {most_n}/{n} scenes (>50%)")
    if failures:
        return GateResult(
            gate="SP-G8 Composition Distribution",
            verdict="FAIL",
            evidence="; ".join(failures),
            fix="Diversify framings across the scene set (mix wide / mid / close / overhead / low-angle).",
        )
    return GateResult(
        gate="SP-G8 Composition Distribution",
        verdict="PASS",
        evidence=f"{distinct} distinct framings; max '{most_common}' at {most_n}/{n}.",
    )


def _check_sp_g6_vignettes(plan: ScenePlan) -> GateResult:
    """SP-G6 (deterministic side): every `scene_type: unified` scene must
    declare 3-5 named `vignettes` so the Kling cut planner has multiple
    macro-insertable anchors (mirrors the user's gold-standard example —
    'subtle background vignettes fading into shadow suggesting miracles,
    parables, mercy toward sinners, power over creation'). The LLM panel
    still judges 'no comic panels / split-screen' qualitatively; this code
    check only enforces the count and named-vignette structure."""
    failures: list[str] = []
    for s in plan.scenes:
        if s.scene_type != "unified":
            continue
        n = len(s.vignettes)
        if n < 3:
            failures.append(
                f"scene {s.index} '{s.title}' is unified but has only {n} vignettes; need 3-5 named vignettes"
            )
        elif n > 5:
            failures.append(
                f"scene {s.index} '{s.title}' has {n} vignettes; cap is 5 to keep the foreground dominant"
            )
    if failures:
        return GateResult(
            gate="SP-G6 Type Discipline",
            verdict="FAIL",
            evidence="; ".join(failures[:4]) + (f" (+{len(failures) - 4} more)" if len(failures) > 4 else ""),
            fix="Add 3-5 named vignettes to each unified scene — see constitution → 'Multi-element unified scene discipline'.",
        )
    return GateResult(
        gate="SP-G6 Type Discipline",
        verdict="PASS",
        evidence=(
            f"every unified scene declares 3-5 vignettes (counts: "
            + ", ".join(f"#{s.index}={len(s.vignettes)}" for s in plan.scenes if s.scene_type == "unified")
            + ")"
        ) if any(s.scene_type == "unified" for s in plan.scenes) else "no unified scenes; check skipped.",
    )


def _deterministic_gates(plan: ScenePlan, beat_ids: list[str]) -> list[GateResult]:
    """All deterministic gates run in code, in order, before the LLM panel
    weighs in. Results are passed to the model as evidence AND override the
    model's verdict on those gates after the fact."""
    return [
        _check_sp_g2(plan, beat_ids),
        _check_sp_g5(plan),
        _check_sp_g6_vignettes(plan),
        _check_sp_g8(plan),
        _check_sp_g9(plan),
    ]


# --------------------------------------------------------------------------
# Stage V1 — review_scene_plan (self) and independent_review_scene_plan
# --------------------------------------------------------------------------
_SCENE_PANEL_BRIEF = """\
6-agent panel. Each: verdict (STRONG | CAUTION | REVISION NEEDED) + one concrete note quoting the offending scene index / title / subject_block fragment:
1. The Scene Director — does the arc actually carry the narration through hook -> proof -> conviction -> landing? Or do scenes just illustrate moments without driving the turn?
2. The Theologian — biblical accuracy: every literal scene defensible against the wider pericope? No invented narrative details? Halos / aureoles only where painting tradition supports? Paired with the Jaded Viewer — freshness must remain exegetically honest.
3. The Visual Skeptic — would these feel like merchandise / Sunday-school illustration / generic stock religious art? Would they hold a sceptical scroller through 60 seconds?
4. The Character-Consistency Checker — Jesus / named disciples described consistently across scenes? `jesus_variant` field correctly set (ministry / passion / resurrection / infant / null) and consistent with each scene's content? Same Jesus body / face / wardrobe in every Jesus-bearing subject_block?
5. The Editor — prompt prose quality, scene count within the adaptive window, subject_block / mood_block are state-only (no action verbs to spook image gen), every scene earns its slot.
6. The Jaded Viewer — they have seen 10,000 Bible reels. Could they predict every scene from the topic? Are any on the visual cliché blocklist (Rembrandt prodigal collapse, Jesus-pointing-at-himself, heaven-opens beam, etc.) without an honest payoff? Paired with the Theologian — surprise without honesty fails."""

_SCENE_GATES_BRIEF_TEMPLATE = """\
Quality gates — each PASS | CONDITIONAL | FAIL, with evidence quoted from the plan and (if not PASS) a specific fix:
- SP-G1 Biblical Accuracy: every literal scene is defensible against the verified KJV passage; no invented narrative details; halos / aureoles only where painting tradition supports.
- SP-G2 Narration Alignment: deterministic — every narration beat id ({beat_ids_csv}) has at least one supporting scene index in beat_coverage. (PRE-CHECKED in code; the result is supplied below as ground truth — copy that verdict verbatim into your gates JSON.)
- SP-G3 Visual Variety: scenes not repetitive; mix of single + unified types; no obvious topic auto-completes from the cliché blocklist unless rationalised.
- SP-G4 Theological Honesty: symbolic scenes do not smuggle in foreign doctrine; the freshness lever is honest, not contrarian.
- SP-G5 Prompt Conformance: deterministic — per-scene subject_block + mood_block carry no banned tokens. (PRE-CHECKED; copy verdict verbatim.)
- SP-G6 Type Discipline: `single` scenes are one subject / one action / one centre with no collage; `unified` scenes are one coherent painted image with subtle vignettes — never a comic page / split-screen / panel layout. Subject_block prose must match the declared scene_type.
- SP-G7 Character Consistency: Jesus / named disciples use an identical canonical description; jesus_variant is set consistently. FAIL if Jesus' description drifts between scenes. (Note: provider-specific downgrade to CONDITIONAL on HF runs is handled by the runner, not by you — judge content only.)
- SP-G8 Composition Distribution: deterministic — at least 3 distinct framings, no single framing on >50% of scenes. (PRE-CHECKED; copy verdict verbatim.)
- SP-G9 Scene Mix & Gospel Frame: deterministic — when scene_count >= 5, at least one `scene_type: unified` AND at least one scene with arc_position naming the Jesus / NT-gospel link (nt-link / gospel-link / gospel-frame). Always ≥2 `single` scenes. (PRE-CHECKED; copy verdict verbatim.)

Verdict rules:
- overall = LOCKED when NO gate is FAIL. CONDITIONAL / CAUTION are advisory.
- overall = REVISE if any gate is FAIL but the concept is sound.
- overall = REWORK if the concept itself is broken.

Return ONLY a JSON object (optionally inside a ```json fence):
{{
  "panel": [{{"agent": "Scene Director", "verdict": "...", "note": "..."}}, ... 6 agents],
  "gates": [{{"gate": "SP-G1 Biblical Accuracy", "verdict": "...", "evidence": "...", "fix": "..."}}, ... 9 gates in order SP-G1..SP-G9],
  "overall": "LOCKED | REVISE | REWORK",
  "priority_fixes": ["the most important fix first", "..."]
}}
No prose outside the JSON object."""


def _scene_review_role(beat_ids: list[str]) -> str:
    return (
        "YOUR TASK: red-team the SCENE PLAN against the charter's \"VISUAL ARC\" "
        "section, the verified KJV passage, and the intended thread. Be a genuine "
        "critic — a panel that returns all STRONG verdicts on a first draft is not "
        "doing its job. Quote the offending scene in every note.\n\n"
        f"{_SCENE_PANEL_BRIEF}\n\n"
        f"{_SCENE_GATES_BRIEF_TEMPLATE.format(beat_ids_csv=', '.join(beat_ids))}"
    )


def _scene_plan_block(plan: ScenePlan) -> str:
    """Render the ScenePlan as the reviewer's input. Includes the deterministic
    pre-check results so the panel's verdicts on SP-G2/G5/G8 align."""
    scenes_rendered = "\n\n".join(
        (
            f"[{s.index}] {s.title}  ({s.scene_type}/{s.framing}/{s.arc_position}"
            f"{', jesus=' + s.jesus_variant if s.jesus_variant else ''})\n"
            f"  purpose: {s.purpose}\n"
            f"  rationale: {s.rationale}\n"
            f"  visible_elements: {s.visible_elements}\n"
            f"  emotional_tone: {s.emotional_tone}\n"
            f"  subject_block: {s.subject_block}\n"
            f"  mood_block: {s.mood_block}\n"
            f"  priority: {s.priority}"
        )
        for s in plan.scenes
    )
    coverage = ", ".join(f"{k}={v}" for k, v in plan.beat_coverage.items())
    return (
        "\n\n=== SCENE PLAN UNDER REVIEW ===\n"
        f"VISUAL READING:\n{plan.visual_reading}\n\n"
        f"RED-TEAM NOTES (the writer's own pre-selection critique):\n{plan.red_team_notes}\n\n"
        f"RATIONALE: {plan.rationale}\n\n"
        f"SCENES ({len(plan.scenes)}):\n{scenes_rendered}\n\n"
        f"SHORT PRIORITY (rank order): {plan.short_priority}\n"
        f"BEAT COVERAGE: {coverage}"
    )


def _deterministic_block(deterministic: list[GateResult]) -> str:
    """Render the pre-checked deterministic gates as ground-truth evidence."""
    rows = "\n".join(
        f"- {g.gate}: {g.verdict}"
        + (f" — evidence: {g.evidence}" if g.evidence else "")
        + (f" — fix: {g.fix}" if g.verdict != "PASS" and g.fix else "")
        for g in deterministic
    )
    return (
        "\n\n=== DETERMINISTIC PRE-CHECK RESULTS (ground truth — your gate verdicts on SP-G2 / SP-G5 / SP-G8 MUST match these) ===\n"
        + rows
    )


def _merge_deterministic_into_review(
    review: ScenePlanReview, deterministic: list[GateResult]
) -> ScenePlanReview:
    """Override the model's verdict on the deterministic gates. If any
    deterministic gate FAILs, overall is downgraded to at least REVISE."""
    det_by_name = {g.gate: g for g in deterministic}
    merged: list[GateResult] = []
    for g in review.gates:
        if g.gate in det_by_name:
            merged.append(det_by_name[g.gate])
        else:
            merged.append(g)
    # Ensure any deterministic gate the model omitted is appended.
    seen = {g.gate for g in merged}
    for g in deterministic:
        if g.gate not in seen:
            merged.append(g)
    failed = [g for g in merged if g.verdict.upper().strip() == "FAIL"]
    overall = review.overall
    if failed and overall.upper().strip() == "LOCKED":
        overall = "REVISE"
    return ScenePlanReview(
        panel=review.panel,
        gates=merged,
        overall=overall,
        priority_fixes=review.priority_fixes,
    )


def review_scene_plan(
    series: Series,
    episode: Episode,
    draft: Draft,
    plan: ScenePlan,
    thread: Thread | None,
    kjv_passage: str | None,
    timeline=None,
) -> ScenePlanReview:
    """Self-review the scene plan against the 8 gates + 6 panel agents.
    Deterministic gates (SP-G2, G5, G8) are checked in Python and override
    the model's verdict on those gates after merge."""
    beat_ids = draft.beat_ids
    deterministic = _deterministic_gates(plan, beat_ids)
    role = _scene_review_role(beat_ids)
    user = (
        text_engine._episode_block(series, episode, draft.scripture_quoted or None, "")
        + _passage_block(kjv_passage)
        + _scene_thread_review_block(thread)
        + _narration_block(draft)
        + _scene_plan_block(plan)
        + _board_block(timeline)
        + _deterministic_block(deterministic)
    )
    reply = text_engine._call(role, user)
    review = ScenePlanReview.from_json(text_engine._extract_json(reply))
    return _merge_deterministic_into_review(review, deterministic)


_SCENE_INDEPENDENT_PREAMBLE = """\
You are an INDEPENDENT visual-arc red-team auditor brought in from outside the
production team. You did not write this scene plan and you did not run the
internal review. Assume the writer AND the internal review may be biased,
over-confident, or have missed things. Verify everything from scratch and be
hard to please:
- Do NOT give the benefit of the doubt. If a scene is unproven against the text, FAIL.
- The verified KJV passage and the intended thread are the source of truth for
  every claim about \"what is in the scene\" and \"what arc this carries\".
- Hunt specifically for: scenes that look beautiful but illustrate nothing in
  the narration; freshness that drifts into eisegesis; halos / aureoles applied
  inconsistently across scenes; jesus_variant mismatches; framing monotony; per-
  scene subject_blocks that contain action verbs likely to spook image gen.
- Surface every real weakness as a CAUTION panel note or a CONDITIONAL gate.
  Reserve a FAIL gate for something that genuinely falls short of the standard.
  Award LOCKED only when no gate FAILs — a clean bill of health is allowed,
  but only after you have honestly tried to break it.
- The deterministic pre-checks (SP-G2 / SP-G5 / SP-G8) are authoritative — copy
  their verdicts verbatim. Focus your independent judgment on SP-G1 / G3 / G4 /
  G6 / G7 and the panel critique.

"""


def independent_review_scene_plan(
    series: Series,
    episode: Episode,
    draft: Draft,
    plan: ScenePlan,
    thread: Thread | None,
    kjv_passage: str | None,
    timeline=None,
) -> ScenePlanReview:
    """A fresh, hostile, model-independent audit of the scene plan. Authoritative
    for LOCKED. Uses REVIEW_MODEL if set, else MODEL."""
    beat_ids = draft.beat_ids
    deterministic = _deterministic_gates(plan, beat_ids)
    role = _SCENE_INDEPENDENT_PREAMBLE + _scene_review_role(beat_ids)
    user = (
        text_engine._episode_block(series, episode, draft.scripture_quoted or None, "")
        + _passage_block(kjv_passage)
        + _scene_thread_review_block(thread)
        + _narration_block(draft)
        + _scene_plan_block(plan)
        + _board_block(timeline)
        + _deterministic_block(deterministic)
    )
    reply = text_engine._call(role, user, model=config.REVIEW_MODEL)
    review = ScenePlanReview.from_json(text_engine._extract_json(reply))
    return _merge_deterministic_into_review(review, deterministic)


# --------------------------------------------------------------------------
# Surgical enrich: rewrite ONLY unified scenes' subject_block + vignettes
# without touching singles. Used to backfill the gold-standard multi-vignette
# pattern on a plan that already passed all other gates.
# --------------------------------------------------------------------------
def enrich_unified_scenes(
    series: Series,
    episode: Episode,
    draft: Draft,
    plan: ScenePlan,
    thread: Thread | None,
    kjv_passage: str | None,
    log=print,
) -> ScenePlan:
    """One Opus call per unified scene. Preserves foreground subject, framing,
    arc_position, intent; rewrites subject_block to include the gold-standard
    multi-vignette phrasing and populates the structured `vignettes` field
    with 3-5 short noun phrases. Single scenes are not touched."""
    role = (
        "YOUR TASK: rewrite the SUBJECT_BLOCK and produce the VIGNETTES list "
        "for ONE multi-element unified scene, following the gold-standard pattern "
        "from the charter VISUAL ARC section.\n\n"
        "Constraints:\n"
        "- PRESERVE the scene's foreground subject, framing, arc-position, and intent. "
        "You are POLISHING this scene, not redesigning it. The current foreground "
        "subject must remain dominant in the new subject_block.\n"
        "- The new subject_block must:\n"
        "  1. Describe the foreground subject FIRST (one dominant centre, with postures and expressions), "
        "as state, not action.\n"
        "  2. Include the exact phrasing 'subtle background vignettes fading into shadow "
        "suggesting <X>, <Y>, <Z>, and <W>' with 3-5 named vignettes.\n"
        "- The vignettes must be short noun phrases (e.g. 'the running father', 'the kiss on "
        "the neck', 'the swallowed bargain', 'a robe being carried out') — memories / echoes "
        "/ fading details that support the foreground, never competing scenes.\n"
        "- For parables: anchor vignettes to actual moments in the wider pericope.\n"
        "- For Jesus / NT-gospel-link scenes: vignettes should be moments from the parable "
        "or gospel link (the running father, the kiss, the robe / ring / shoes, the cross, "
        "the elder brother).\n"
        "- For OT-echo scenes: vignettes should be cited OT imagery (returning exiles, "
        "withered tree budding, ruined city restored, father pitying child).\n"
        "- Do NOT include the fixed style base wording — the renderer adds it.\n"
        "- Banned tokens are still banned in the new subject_block.\n\n"
        "Return ONLY a JSON object (optionally inside a ```json fence):\n"
        "{\n"
        '  "subject_block": "<rewritten ~80-130 words>",\n'
        '  "vignettes": ["<noun phrase 1>", "<noun phrase 2>", "<noun phrase 3>", "<noun phrase 4>"]\n'
        "}\n"
        "No prose outside the JSON object."
    )

    new_scenes: list = []
    for s in plan.scenes:
        if s.scene_type != "unified":
            new_scenes.append(s)
            continue
        log(f"      enriching scene #{s.index:02d} '{s.title}' (unified/{s.arc_position})")
        user = (
            text_engine._episode_block(series, episode, draft.scripture_quoted or None, "")
            + _passage_block(kjv_passage)
            + _scene_thread_review_block(thread)
            + _narration_block(draft)
            + "\n\n=== SCENE TO ENRICH (preserve foreground, expand vignettes) ===\n"
            + f"[{s.index}] {s.title}  ({s.scene_type}/{s.framing}/{s.arc_position}"
            + (f"/jesus={s.jesus_variant}" if s.jesus_variant else "") + ")\n"
            + f"  purpose: {s.purpose}\n"
            + f"  rationale: {s.rationale}\n"
            + f"  visible_elements: {s.visible_elements}\n"
            + f"  emotional_tone: {s.emotional_tone}\n"
            + f"  CURRENT subject_block:\n  {s.subject_block}\n"
            + f"  CURRENT vignettes: {s.vignettes}\n"
            + f"  CURRENT mood_block: {s.mood_block}\n"
            + f"  macro_elements (cut anchors): {s.macro_elements}"
        )
        reply = text_engine._call(role, user)
        data = text_engine._extract_json(reply)
        new_subject = str(data.get("subject_block", "")).strip()
        new_vignettes = [str(v).strip() for v in (data.get("vignettes") or []) if str(v).strip()]
        new_scenes.append(replace(s, subject_block=new_subject, vignettes=new_vignettes))

    return replace(plan, scenes=new_scenes)


# --------------------------------------------------------------------------
# Stage V2 — revise_scene_plan
# --------------------------------------------------------------------------
def revise_scene_plan(
    series: Series,
    episode: Episode,
    draft: Draft,
    plan: ScenePlan,
    review: ScenePlanReview,
    thread: Thread | None,
    kjv_passage: str | None,
    timeline=None,
) -> ScenePlan:
    """Revise the plan to fix every FAIL gate + priority fix. Preserves the
    thread spine (does not swap threads to placate freshness feedback) and
    the chosen scene_type / framing where they still work — reshape only what
    the review asks for."""
    beat_ids = draft.beat_ids
    panel_str = "\n".join(f"- {a.agent}: {a.verdict} — {a.note}" for a in review.panel)
    gates_str = "\n".join(
        f"- {g.gate}: {g.verdict}"
        + (f" — FIX: {g.fix}" if g.verdict.upper().strip() != "PASS" and g.fix else "")
        for g in review.gates
    )
    fixes_str = "\n".join(f"- {f}" for f in review.priority_fixes)
    role = (
        "YOUR TASK: revise the scene plan to fix every issue the review raised, "
        "especially the FAIL gates and the priority fixes. Preserve what works. "
        "Keep the charter VISUAL ARC rules, the visual cliché blocklist, and the "
        "thread spine — do NOT swap threads to answer freshness/cliché feedback; "
        "reshape the SCENES or rewrite the subject_block / mood_block to carry the "
        "same thread more cleanly.\n\n"
        "Return ONLY a JSON object with the SAME shape as the original scene plan "
        "(see contract below). Keep scene indices stable where possible; add new "
        "scenes with the next free index; remove scenes by omission. Re-fill "
        "beat_coverage and short_priority accordingly.\n\n"
        f"{_scene_plan_json_contract(beat_ids)}\n"
        "No prose outside the JSON object."
    )
    user = (
        text_engine._episode_block(series, episode, draft.scripture_quoted or None, "")
        + _passage_block(kjv_passage)
        + _scene_thread_block(thread)
        + _narration_block(draft)
        + _scene_plan_block(plan)
        + _board_block(timeline)
        + "\n\n=== REVIEW PANEL ===\n"
        + panel_str
        + "\n\n=== GATES ===\n"
        + gates_str
        + "\n\n=== PRIORITY FIXES ===\n"
        + fixes_str
    )
    reply = text_engine._call(role, user)
    return ScenePlan.from_json(text_engine._extract_json(reply))
