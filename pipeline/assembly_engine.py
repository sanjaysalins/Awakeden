"""The assembly intelligence: the LLM jigsaw matcher + the deterministic slot
allocator + the gate set + self/independent review + revise.

Division of labour: the LLM does the SEMANTIC jigsaw (which clip sits under
which words, in what order, which to drop when over budget, the hero pick). The
allocator does the ARITHMETIC (slot durations, speed-up vs trim-past-cap) in
Python, so the timeline tiles exactly and the speed policy is deterministic.
"""
from __future__ import annotations

import json

import config
from pipeline import engine as text_engine
from pipeline.assembly_models import (
    AgentVerdict,
    ClipAsset,
    EditPlan,
    EditPlanReview,
    EditSlot,
    GateResult,
    NarrationSegment,
)
from pipeline.assembly_timing import total_seconds


# --------------------------------------------------------------------------
# Allocation weights
# --------------------------------------------------------------------------
ROLE_WEIGHT = {
    "climax": 1.6, "close": 1.3, "hook-open": 1.2, "pivot": 1.1, "build": 0.8,
}
PACE_MULT = {"slower": 1.25, "controlled": 1.0, "faster": 0.8}


def _weight(clip: ClipAsset) -> float:
    w = ROLE_WEIGHT.get(clip.viral_role, 1.0) * PACE_MULT.get(clip.pacing, 1.0)
    if _is_sacred(clip):
        w *= 1.4  # sacred clips get more time so the reverence cap rarely forces a trim
    return w


# --------------------------------------------------------------------------
# Gospel-frame / reverence classification (the message-integrity backbone)
# --------------------------------------------------------------------------
import re as _re

_GOSPEL_PIVOT_ARC = ("nt-gospel-link", "gospel-link", "passion", "resurrection")
# word-boundary so "across"/"crossed the threshold" don't false-match "cross"
_CROSS_RE = _re.compile(r"\b(cross|crucif|calvary|golgotha)", _re.IGNORECASE)
_SACRED_ARC = _GOSPEL_PIVOT_ARC + ("ot-echo", "theological-centre", "theological-center")


def _is_gospel_pivot(clip: ClipAsset) -> bool:
    """A clip that explicitly carries the Christ / cross / NT-gospel link — the
    only kind allowed to bookend the close (constitution: land on Jesus). Keyed
    on arc_position + jesus_variant (the reliable signals), with a word-boundary
    cross check on the TITLE as a backstop."""
    arc = clip.arc_position or ""
    if any(tok in arc for tok in _GOSPEL_PIVOT_ARC):
        return True
    if clip.jesus_variant in ("passion", "resurrection"):
        return True
    return bool(_CROSS_RE.search(clip.title))


def _is_cross(clip: ClipAsset) -> bool:
    return clip.jesus_variant == "passion" or bool(_CROSS_RE.search(clip.title))


def _is_sacred(clip: ClipAsset) -> bool:
    """Reverence-protected: depicts Christ / cross / a sacred moment, OR is the
    climax / close. These get a lower speed cap so they are never trivialised."""
    if clip.jesus_variant:
        return True
    if any(tok in (clip.arc_position or "") for tok in _SACRED_ARC):
        return True
    if clip.viral_role in ("climax", "close"):
        return True
    return _is_gospel_pivot(clip)


def _speed_cap_for(clip: ClipAsset) -> float:
    """Reverence cap for sacred clips, else the normal cap."""
    if _is_sacred(clip):
        return min(config.ASSEMBLY_REVERENCE_CAP, config.ASSEMBLY_SPEED_CAP)
    return config.ASSEMBLY_SPEED_CAP


def _pick_hero(clips: list[ClipAsset], hero_pref: int) -> int:
    """Choose the hero (bookends open+close). MUST be a gospel-pivot so the cut
    lands on Christ. Honour hero_pref only if it is itself a gospel-pivot."""
    by_index = {c.scene_index: c for c in clips}
    if hero_pref and hero_pref in by_index and _is_gospel_pivot(by_index[hero_pref]):
        return hero_pref
    crosses = [c for c in clips if _is_cross(c)]
    if crosses:
        return crosses[0].scene_index
    pivots = [c for c in clips if _is_gospel_pivot(c)]
    if pivots:
        # prefer a climax/close pivot, else any pivot
        pivots.sort(key=lambda c: (c.viral_role not in ("climax", "close"), c.scene_index))
        return pivots[0].scene_index
    return clips[0].scene_index if clips else 0


def _sanitize_assignment(
    section_assignment: dict[str, list[int]],
    valid_sections: list[str],
    clips_by_index: dict[int, ClipAsset],
    budget: int,
    hero_idx: int,
    log,
) -> dict[str, list[int]]:
    """Make the LLM's placement safe + budget-bounded WITHOUT silently losing
    clips: drop unknown clip indices, de-dupe, re-home clips placed under unknown
    section keys into the last real section, and trim DOWN to budget by dropping
    only the lowest-weight clips that are NOT the hero / gospel-frame / hook / close."""
    seen: set[int] = set()
    cleaned: dict[str, list[int]] = {s: [] for s in valid_sections}
    homeless: list[int] = []
    for k, idxs in section_assignment.items():
        target = k if k in valid_sections else None
        for i in idxs:
            if i not in clips_by_index or i in seen:
                continue
            seen.add(i)
            (cleaned[target] if target else homeless).append(i)  # type: ignore[index]
    if homeless and valid_sections:
        host = valid_sections[-1]
        cleaned[host].extend(homeless)
        log(f"      ! re-homed clips {homeless} from unknown section key(s) into '{host}'")

    total = sum(len(v) for v in cleaned.values())
    if budget and total > budget:
        droppable: list[tuple[int, str, float]] = []
        for sec, idxs in cleaned.items():
            for i in idxs:
                c = clips_by_index[i]
                if i == hero_idx or _is_gospel_pivot(c) or c.viral_role in ("hook-open", "close", "climax"):
                    continue  # gospel-frame / hero protected
                droppable.append((i, sec, _weight(c)))
        droppable.sort(key=lambda t: t[2])  # lowest weight first
        to_drop = total - budget
        dropped: list[int] = []
        for i, sec, _w in droppable:
            if to_drop <= 0:
                break
            cleaned[sec].remove(i)
            dropped.append(i)
            to_drop -= 1
        if dropped:
            log(f"      [budget] dropped lowest-weight clip(s) {sorted(dropped)} to hit budget {budget}")
        if to_drop > 0:
            log(f"      [budget] kept {budget + to_drop} clips (rest are gospel-frame/hero-protected)")
    return {s: v for s, v in cleaned.items() if v}


# --------------------------------------------------------------------------
# Deterministic slot allocator
# --------------------------------------------------------------------------
def _video_windows(
    segments: list[NarrationSegment], hero_head: float, hero_tail: float
) -> list[tuple[str, float, float]]:
    """Tile the body timeline [hero_head, total-hero_tail] into one contiguous
    block per narration section (pauses fold into the preceding section)."""
    total = total_seconds(segments)
    body_start = hero_head
    body_end = total - hero_tail
    windows: list[tuple[str, float, float]] = []
    for i, seg in enumerate(segments):
        raw_start = 0.0 if i == 0 else seg.start_s
        raw_end = total if i == len(segments) - 1 else segments[i + 1].start_s
        # clip each section's video window into the body range [body_start, body_end].
        # A section that falls entirely under the hero head/tail collapses to ~0 and
        # its clips get folded into a neighbour by the allocator (no negative windows).
        start = min(max(raw_start, body_start), body_end)
        end = min(max(raw_end, body_start), body_end)
        windows.append((seg.section, start, max(start, end)))
    return windows


def _distribute(window_len: float, clips: list[ClipAsset], min_slot: float) -> list[float]:
    """Split `window_len` among `clips` by weight, clamp to [min_slot, natural],
    redistribute residual, then normalise to sum exactly to window_len."""
    if not clips:
        return []
    if len(clips) == 1:
        return [max(min_slot, window_len)]
    weights = [_weight(c) for c in clips]
    wsum = sum(weights) or 1.0
    slots = [window_len * w / wsum for w in weights]
    # clamp + redistribute residual across unclamped clips (a few passes)
    for _ in range(6):
        residual = 0.0
        unclamped: list[int] = []
        for i, c in enumerate(clips):
            lo, hi = min_slot, c.natural_duration_s
            if slots[i] < lo:
                residual += slots[i] - lo
                slots[i] = lo
            elif slots[i] > hi:
                residual += slots[i] - hi
                slots[i] = hi
            else:
                unclamped.append(i)
        if abs(residual) < 1e-4 or not unclamped:
            break
        share = residual / len(unclamped)
        for i in unclamped:
            slots[i] += share
    # final exact normalisation (guarantees the section tiles its window), then a
    # gentle re-clamp so normalisation can't push a slot back below MIN_SLOT.
    s = sum(slots) or 1.0
    slots = [x * window_len / s for x in slots]
    if any(x < min_slot - 1e-3 for x in slots) and window_len >= min_slot * len(slots):
        # rare: rescale pushed something under the floor — lift to floor and
        # shave the surplus off the largest slots until the sum matches again.
        slots = [max(min_slot, x) for x in slots]
        over = sum(slots) - window_len
        order = sorted(range(len(slots)), key=lambda i: -slots[i])
        k = 0
        while over > 1e-3 and k < len(order) * 4:
            i = order[k % len(order)]
            take = min(over, slots[i] - min_slot)
            slots[i] -= take
            over -= take
            k += 1
    return slots


def _slot_op(clip: ClipAsset, slot_dur: float, cap: float | None = None) -> tuple[float, float, float, str]:
    """Return (speed, src_in, src_out, op) for one slot. Speed-first; trim only
    the overflow past the cap. Sacred clips use the (lower) reverence cap."""
    if cap is None:
        cap = _speed_cap_for(clip)
    D = clip.natural_duration_s
    if slot_dur <= 0:
        return 1.0, 0.0, D, "speed"
    required = D / slot_dur
    if required <= cap:
        return required, 0.0, D, "speed"
    # trim-past-cap: cap the speed, take a (cap*slot) window of the source
    src_span = min(cap * slot_dur, D)
    if clip.viral_role in ("climax", "pivot"):
        src_in = min(max(0.0, D - src_span), 0.3 * D)   # head-biased: keep the payload
    else:
        src_in = max(0.0, (D - src_span) / 2)           # centered: drop ease-in / drift
    src_out = min(D, src_in + src_span)
    return cap, src_in, src_out, "speed+trim"


def allocate(
    segments: list[NarrationSegment],
    clips_by_index: dict[int, ClipAsset],
    hero_scene_index: int,
    section_assignment: dict[str, list[int]],
    narration_reading: str = "",
    red_team_notes: str = "",
    slot_rationales: dict[int, str] | None = None,
    notes: str = "",
) -> EditPlan:
    """Turn the LLM skeleton into a fully-timed EditPlan with computed slots."""
    min_slot = config.ASSEMBLY_MIN_SLOT
    hero_head = config.ASSEMBLY_HERO_HEAD
    hero_tail = config.ASSEMBLY_HERO_TAIL
    total = total_seconds(segments)
    slot_rationales = slot_rationales or {}

    windows = _video_windows(segments, hero_head, hero_tail)
    # Walk sections in order. Fold the time AND clips of any section whose window
    # is too small to host a clip (collapsed under the hero bookend, or unassigned)
    # forward into the next real section — so every clip is placed and the body
    # still tiles exactly.
    carry = 0.0
    pending: list[ClipAsset] = []
    sized: list[tuple[str, float, list[ClipAsset]]] = []
    for section, ws, we in windows:
        wlen = max(0.0, we - ws) + carry
        idxs = section_assignment.get(section, [])
        section_clips = pending + [clips_by_index[i] for i in idxs if i in clips_by_index]
        if not section_clips or wlen < min_slot:
            carry = wlen
            pending = section_clips
            continue
        carry = 0.0
        pending = []
        sized.append((section, wlen, section_clips))
    if (pending or carry > 0) and sized:  # flush trailing into the last block
        sec, wlen, cl = sized[-1]
        sized[-1] = (sec, wlen + carry, cl + pending)
    elif pending and not sized:  # degenerate: everything collapsed — one block
        sized.append((segments[-1].section if segments else "landing",
                      total - hero_head - hero_tail, pending))

    slots: list[EditSlot] = []
    order = 0
    # hero head — same opening moment at start and end for a seamless loop feel
    hero = clips_by_index.get(hero_scene_index)
    if hero is not None and hero_head > 0:
        slots.append(EditSlot(
            order=order, role="hero-head", scene_index=hero.scene_index,
            section="hero", slot_start_s=0.0, slot_end_s=hero_head,
            source_in_s=0.0, source_out_s=min(hero_head, hero.natural_duration_s),
            speed_factor=1.0, op="speed",
            rationale="Hero bookend (open) — the most on-thread image holds for a continuous/loop feel.",
        ))
        order += 1

    # body slots, section by section
    cursor = hero_head if hero is not None and hero_head > 0 else 0.0
    for section, wlen, section_clips in sized:
        durs = _distribute(wlen, section_clips, min_slot)
        for clip, dur in zip(section_clips, durs):
            # cap=None → _slot_op uses the per-clip cap (reverence cap for sacred clips)
            S, src_in, src_out, op = _slot_op(clip, dur)
            slots.append(EditSlot(
                order=order, role="body", scene_index=clip.scene_index,
                section=section, slot_start_s=round(cursor, 3),
                slot_end_s=round(cursor + dur, 3),
                source_in_s=round(src_in, 3), source_out_s=round(src_out, 3),
                speed_factor=round(S, 4), op=op,
                rationale=slot_rationales.get(clip.scene_index, ""),
            ))
            cursor += dur
            order += 1

    # hero tail
    if hero is not None and hero_tail > 0:
        slots.append(EditSlot(
            order=order, role="hero-tail", scene_index=hero.scene_index,
            section="hero", slot_start_s=round(total - hero_tail, 3), slot_end_s=round(total, 3),
            source_in_s=0.0, source_out_s=min(hero_tail, hero.natural_duration_s),
            speed_factor=1.0, op="speed",
            rationale="Hero bookend (close) — mirrors the open; same image closes the loop.",
        ))
        order += 1

    selected = [i for _, _, cl in sized for i in [c.scene_index for c in cl]]
    return EditPlan(
        narration_reading=narration_reading,
        red_team_notes=red_team_notes,
        hero_scene_index=hero_scene_index,
        hero_head_s=hero_head,
        hero_tail_s=hero_tail,
        total_seconds=round(total, 3),
        clip_budget=len(selected),
        selected_scene_indices=selected,
        section_assignment={k: list(v) for k, v in section_assignment.items()},
        slots=slots,
        notes=notes,
    )


# --------------------------------------------------------------------------
# LLM jigsaw matcher
# --------------------------------------------------------------------------
def _board_block(segments: list[NarrationSegment]) -> str:
    lines = ["=== NARRATION BOARD (sections, absolute times, words) ==="]
    for s in segments:
        lines.append(
            f"[{s.section}] {s.start_s:.2f}-{s.end_s:.2f}s ({s.duration_s:.2f}s) "
            f"{s.speaker}: {s.text}"
        )
    lines.append(f"TOTAL: {total_seconds(segments):.3f}s")
    return "\n".join(lines)


def _clips_block(clips: list[ClipAsset]) -> str:
    lines = ["=== CLIPS (each ~10s natural; you place + select, code times them) ==="]
    for c in clips:
        sub = c.subject_block[:200] + ("…" if len(c.subject_block) > 200 else "")
        lines.append(
            f"#{c.scene_index:02d} \"{c.title}\" — {c.scene_type}/{c.framing}/{c.arc_position} "
            f"· role={c.viral_role} · pacing={c.pacing} · short_priority={c.short_priority}"
            + (f" · jesus={c.jesus_variant}" if c.jesus_variant else "")
            + f"\n     subject: {sub}"
        )
    return "\n".join(lines)


def _plan_json_contract(sections: list[str], budget: int) -> str:
    return (
        "Return ONLY a JSON object (optionally inside a ```json fence):\n"
        "{\n"
        '  "narration_reading": "2-4 sentences: how you mapped clips to the spoken words",\n'
        '  "red_team_notes": "your own honest doubts about this cut",\n'
        '  "hero_scene_index": <int — the single most on-thread clip; bookends start+end>,\n'
        '  "section_assignment": {\n'
        + "".join(f'    "{s}": [<scene indices in play order>],\n' for s in sections)
        + "  },\n"
        '  "slot_rationales": {"<scene_index>": "why this clip under these words"}\n'
        "}\n"
    )


def _matcher_role(sections: list[str], budget: int, all_clips: bool) -> str:
    budget_rule = (
        f"Use ALL {budget} clips (the user asked for every clip in the cut)."
        if all_clips else
        f"Use EXACTLY {budget} distinct clips total across all sections — choose the "
        f"strongest and DROP the weakest 'build' clips."
    )
    return (
        "You are the EDITOR of a 60-second vertical gospel Short. You have a fixed "
        "narration audio (words + who speaks + when) and a set of ~10s clips. Fit the "
        "clips to the words like a JIGSAW: the right image under the right line. Use "
        "the NARRATION BOARD and each clip's subject/role to decide what sits where — "
        "do not rely on any one episode's specifics.\n\n"
        "RULES:\n"
        f"- {budget_rule}\n"
        "- Every narration section that has words MUST get at least one clip.\n"
        "- Each clip appears in exactly ONE section.\n"
        "- Order clips within a section to follow the spoken words.\n"
        "- Match by MEANING: put a clip under the line it depicts (the action verb on "
        "the verb, the named object on its mention, the OT/NT echo on the line it "
        "echoes). Hook-open clips open; the emotional climax sits under the climactic "
        "line; the CTA / close clip lands last.\n"
        "- The HERO bookends the very start AND end, so it carries the gospel landing: "
        "it MUST be the Christ / cross / NT-gospel-pivot image (the one the CTA points "
        "to), NOT merely the most emotional frame. Put the hero in your "
        "section_assignment under its natural section too.\n"
        "- Keep the GOSPEL FRAME intact even when dropping clips: always keep the "
        "cross / passion clip, at least one Jesus / NT-gospel-link clip, one hook-open, "
        "and one close. Drop only the weakest 'build' clips.\n"
        "- You do NOT set durations or speeds — Python computes those. Just SELECT, "
        "PLACE, and ORDER.\n\n"
        f"Sections available (use these exact keys): {sections}\n\n"
        + _plan_json_contract(sections, budget)
        + "No prose outside the JSON object."
    )


def plan_edit(
    segments: list[NarrationSegment],
    clips: list[ClipAsset],
    clip_budget: int,
    thread_summary: str = "",
    hero_pref: int = 0,
    log=print,
) -> EditPlan:
    """LLM jigsaw → deterministic allocation → fully-timed EditPlan."""
    clips_by_index = {c.scene_index: c for c in clips}
    sections = []
    for s in segments:
        if s.section not in sections:
            sections.append(s.section)
    all_clips = clip_budget >= len(clips)
    budget = len(clips) if all_clips else clip_budget

    role = _matcher_role(sections, budget, all_clips)
    user = _board_block(segments) + "\n\n" + _clips_block(clips)
    if thread_summary:
        user += f"\n\n=== THREAD SPINE (carry through open → climax → close) ===\n{thread_summary}"
    if hero_pref:
        user += f"\n\nHERO PREFERENCE: scene #{hero_pref:02d} (use unless a stronger on-thread image exists)."

    reply = text_engine._call(role, user)
    d = text_engine._extract_json(reply)

    section_assignment = {}
    for k, v in (d.get("section_assignment", {}) or {}).items():
        try:
            section_assignment[str(k).strip().lower()] = [int(x) for x in (v or [])]
        except (TypeError, ValueError):
            section_assignment[str(k).strip().lower()] = []
    # Hero MUST be a gospel-pivot so the cut lands on Christ (overrides the LLM if it
    # nominated an emotional non-pivot). _pick_hero honours a valid pivot preference.
    hero_idx = _pick_hero(clips, int(d.get("hero_scene_index", hero_pref) or hero_pref or 0))
    section_assignment = _sanitize_assignment(
        section_assignment, sections, clips_by_index, budget, hero_idx, log)
    rationales = {}
    for k, v in (d.get("slot_rationales", {}) or {}).items():
        try:
            rationales[int(k)] = str(v).strip()
        except (TypeError, ValueError):
            continue

    return allocate(
        segments=segments,
        clips_by_index=clips_by_index,
        hero_scene_index=hero_idx,
        section_assignment=section_assignment,
        narration_reading=str(d.get("narration_reading", "")).strip(),
        red_team_notes=str(d.get("red_team_notes", "")).strip(),
        slot_rationales=rationales,
    )


# --------------------------------------------------------------------------
# Deterministic gates (run in Python; override the LLM verdict on these)
# --------------------------------------------------------------------------
def _check_g1_coverage(plan: EditPlan) -> GateResult:
    slots = sorted(plan.slots, key=lambda s: s.order)
    if not slots:
        return GateResult("AS-G1 Timeline Coverage", "FAIL", "No slots.", "Produce slots.")
    gaps = []
    for a, b in zip(slots, slots[1:]):
        if abs(b.slot_start_s - a.slot_end_s) > 0.05:
            gaps.append(f"{a.slot_end_s:.2f}->{b.slot_start_s:.2f}")
    start_ok = abs(slots[0].slot_start_s) <= 0.05
    end_ok = abs(slots[-1].slot_end_s - plan.total_seconds) <= 0.05
    if gaps or not start_ok or not end_ok:
        return GateResult(
            "AS-G1 Timeline Coverage", "FAIL",
            f"start={slots[0].slot_start_s:.2f} end={slots[-1].slot_end_s:.2f} "
            f"total={plan.total_seconds:.2f} gaps={gaps}",
            "Slots must tile [0, total] contiguously with no gaps/overlaps.",
        )
    return GateResult(
        "AS-G1 Timeline Coverage", "PASS",
        f"{len(slots)} slots tile 0->{plan.total_seconds:.2f}s contiguously.",
    )


def _check_g2_budget(plan: EditPlan) -> GateResult:
    body = plan.body_slots
    body_idxs = [s.scene_index for s in body]
    distinct = set(body_idxs)
    dupes = len(body_idxs) != len(distinct)
    hero_ok = plan.hero_scene_index in distinct
    if dupes:
        return GateResult("AS-G2 Clip Budget", "FAIL",
                          f"Body clips repeat: {body_idxs}.",
                          "Each body clip must appear exactly once.")
    if not hero_ok:
        return GateResult("AS-G2 Clip Budget", "FAIL",
                          f"Hero #{plan.hero_scene_index:02d} not in body set {sorted(distinct)}.",
                          "Add the hero to its natural (climax) section.")
    return GateResult("AS-G2 Clip Budget", "PASS",
                      f"{len(distinct)} distinct body clips; hero #{plan.hero_scene_index:02d} present.")


def _check_g3_speed(plan: EditPlan) -> GateResult:
    body = plan.body_slots
    if not body:
        return GateResult("AS-G3 Speed/Trim Health", "FAIL", "No body slots.", "")
    speeds = [s.speed_factor for s in body]
    trimmed = [s for s in body if s.op == "speed+trim"]
    avg = sum(speeds) / len(speeds)
    mx = max(speeds)
    if avg > 2.0 or len(trimmed) > len(body) / 2:
        return GateResult(
            "AS-G3 Speed/Trim Health", "CONDITIONAL",
            f"avg speed {avg:.2f}x, max {mx:.2f}x, {len(trimmed)}/{len(body)} trimmed — "
            "brisk; verify it does not strobe.",
            "Reduce clip count (lower --clips) so slots breathe.",
        )
    return GateResult("AS-G3 Speed/Trim Health", "PASS",
                      f"avg speed {avg:.2f}x, max {mx:.2f}x, {len(trimmed)} trimmed.")


def _check_g4_min_slot(plan: EditPlan) -> GateResult:
    short = [(s.scene_index, round(s.slot_duration_s, 2))
             for s in plan.body_slots if s.slot_duration_s < config.ASSEMBLY_MIN_SLOT - 1e-3]
    if short:
        return GateResult("AS-G4 Min Slot", "FAIL",
                          f"Slots below {config.ASSEMBLY_MIN_SLOT}s: {short}.",
                          "Drop a clip from the oversubscribed section.")
    return GateResult("AS-G4 Min Slot", "PASS",
                      f"All body slots >= {config.ASSEMBLY_MIN_SLOT}s.")


def _check_g5_section_coverage(plan: EditPlan, segments: list[NarrationSegment]) -> GateResult:
    covered = {s.section for s in plan.body_slots}
    missing = [seg.section for seg in segments if seg.text and seg.section not in covered]
    if missing:
        return GateResult("AS-G5 Section Coverage", "FAIL",
                          f"Narration section(s) with no clip: {missing}.",
                          "Assign at least one clip to every spoken section.")
    return GateResult("AS-G5 Section Coverage", "PASS",
                      f"Every spoken section has a clip: {sorted(covered)}.")


def _check_g6_hero(plan: EditPlan, clips_by_index: dict[int, ClipAsset]) -> GateResult:
    head = [s for s in plan.slots if s.role == "hero-head"]
    tail = [s for s in plan.slots if s.role == "hero-tail"]
    if not head or not tail:
        return GateResult("AS-G6 Hero Bookend", "FAIL",
                          f"head={bool(head)} tail={bool(tail)}.",
                          "Bookend the hero at both the start and the end.")
    h, t = head[0], tail[0]
    if h.scene_index != t.scene_index or h.scene_index != plan.hero_scene_index:
        return GateResult("AS-G6 Hero Bookend", "FAIL",
                          f"head #{h.scene_index} tail #{t.scene_index} hero #{plan.hero_scene_index}.",
                          "Both bookends must be the same hero clip.")
    # The close lands on the hero — so the hero MUST be a gospel-pivot (cross / Christ /
    # NT-link), per the constitution's 'every short ends pointing to Jesus'.
    hero_clip = clips_by_index.get(plan.hero_scene_index)
    if hero_clip is not None and not _is_gospel_pivot(hero_clip):
        return GateResult("AS-G6 Hero Bookend", "FAIL",
                          f"Hero #{plan.hero_scene_index:02d} '{hero_clip.title}' is NOT a "
                          f"gospel-pivot (arc={hero_clip.arc_position}); the cut would close "
                          "on a non-Christ image.",
                          "Make the hero the cross / Christ / NT-gospel-link image.")
    if not (2.0 <= h.slot_duration_s <= 3.0 and 2.0 <= t.slot_duration_s <= 3.0):
        return GateResult("AS-G6 Hero Bookend", "CONDITIONAL",
                          f"head {h.slot_duration_s:.2f}s, tail {t.slot_duration_s:.2f}s (target 2-3s).",
                          "Keep each bookend in the 2-3s range.")
    return GateResult("AS-G6 Hero Bookend", "PASS",
                      f"Gospel-pivot hero #{plan.hero_scene_index:02d} bookends "
                      f"{h.slot_duration_s:.1f}s + {t.slot_duration_s:.1f}s.")


def _check_g7_gospel_frame(plan: EditPlan, clips_by_index: dict[int, ClipAsset]) -> GateResult:
    """AS-G7 Gospel-Frame Survival (deterministic). After any curation/exclusion,
    the cut must still carry the gospel frame: the cross/passion clip, ≥1 Jesus/
    NT-link, a hook-open, and a close. Protects the LOCKED thread-spine rule."""
    body = [clips_by_index[s.scene_index] for s in plan.body_slots if s.scene_index in clips_by_index]
    if not body:
        return GateResult("AS-G7 Gospel Frame", "FAIL", "No body clips.", "")
    has_cross = any(_is_cross(c) for c in body)
    has_pivot = any(_is_gospel_pivot(c) for c in body)
    has_open = any(c.viral_role == "hook-open" for c in body)
    has_close = any(c.viral_role == "close" for c in body)
    missing = []
    if not has_pivot:
        missing.append("a Jesus/NT-gospel-link clip")
    if not has_cross:
        missing.append("the cross/passion clip")
    if not has_open:
        missing.append("a hook-open clip")
    if not has_close:
        missing.append("a close clip")
    # cross is the strongest requirement; pivot/open/close are strongly recommended.
    if not has_pivot or not has_cross:
        return GateResult("AS-G7 Gospel Frame", "FAIL",
                          f"Cut is missing: {', '.join(missing)}.",
                          "Keep the gospel frame in the selection — never drop the cross / Jesus-link.")
    if missing:
        return GateResult("AS-G7 Gospel Frame", "CONDITIONAL",
                          f"Present: cross+pivot. Missing: {', '.join(missing)}.",
                          "Add a hook-open and/or close clip if available.")
    return GateResult("AS-G7 Gospel Frame", "PASS",
                      "Cross + Jesus/NT-link + hook-open + close all present.")


def deterministic_gates(plan: EditPlan, segments: list[NarrationSegment],
                        clips_by_index: dict[int, ClipAsset]) -> list[GateResult]:
    return [
        _check_g1_coverage(plan),
        _check_g2_budget(plan),
        _check_g3_speed(plan),
        _check_g4_min_slot(plan),
        _check_g5_section_coverage(plan, segments),
        _check_g6_hero(plan, clips_by_index),
        _check_g7_gospel_frame(plan, clips_by_index),
    ]


# --------------------------------------------------------------------------
# Review (6-agent panel + gates) / independent audit / revise
# --------------------------------------------------------------------------
def _plan_block(plan: EditPlan, clips_by_index: dict[int, ClipAsset]) -> str:
    lines = ["=== EDIT PLAN UNDER REVIEW ===",
             f"narration_reading: {plan.narration_reading}",
             f"hero: #{plan.hero_scene_index:02d}  ·  budget: {plan.clip_budget}  "
             f"·  total: {plan.total_seconds:.2f}s",
             "slots (order · role · section · scene · window · dur · speed · op · title):"]
    for s in plan.slots:
        title = clips_by_index.get(s.scene_index)
        title = title.title if title else "?"
        lines.append(
            f"  {s.order:>2} {s.role:<10} {s.section:<8} #{s.scene_index:02d} "
            f"{s.slot_start_s:5.2f}-{s.slot_end_s:5.2f} ({s.slot_duration_s:4.2f}s) "
            f"{s.speed_factor:.2f}x {s.op:<11} {title}"
        )
    if plan.red_team_notes:
        lines.append(f"writer red-team notes: {plan.red_team_notes}")
    return "\n".join(lines)


def _deterministic_block(gates: list[GateResult]) -> str:
    lines = ["=== DETERMINISTIC GATE PRE-CHECKS (authoritative on AS-G1..G7) ==="]
    for g in gates:
        lines.append(f"- {g.gate}: {g.verdict} — {g.evidence}"
                     + (f"  FIX: {g.fix}" if g.fix and g.verdict != "PASS" else ""))
    return "\n".join(lines)


_PANEL = (
    "PANEL (each returns a verdict STRONG | CAUTION | REVISION NEEDED + one-line note):\n"
    "- Editor — does the cut flow; are slots paced for a 60s Short, not a strobe?\n"
    "- Narration-Sync — does each clip sit under the RIGHT words (the action on its verb, "
    "the named object on its mention, the echo on the line it echoes)?\n"
    "- Pacing — are speed-ups/trims tasteful for slow Baroque footage? Are SACRED clips "
    "(Christ / cross / the landing) kept near full speed, never jittery?\n"
    "- Hero-Continuity — does the hero bookend open and close cleanly, AND is the hero a "
    "Christ / gospel-pivot image so the cut LANDS on Jesus (not on a merely emotional frame)?\n"
    "- Thread-Keeper — is the episode's ONE thread visible open → climax → close, and does "
    "the gospel frame (cross + a Jesus/NT-link) survive the selection?\n"
    "- Jaded Viewer — would a scroller stop, or feel the seams?\n"
)


def _review_role(sections: list[str], independent: bool = False) -> str:
    preamble = (
        ("You are a FRESH, INDEPENDENT red-team auditor. You did not build this cut. "
         "Re-judge it from scratch and be hard to please. Your verdict is authoritative.\n\n")
        if independent else
        ("You are the self-review panel for a 60-second vertical gospel Short's EDIT PLAN.\n\n")
    )
    return (
        preamble
        + _PANEL
        + "\nGATES (return PASS | CONDITIONAL | FAIL + evidence + fix):\n"
        "- AS-G1 Timeline Coverage, AS-G2 Clip Budget, AS-G3 Speed/Trim Health, "
        "AS-G4 Min Slot, AS-G5 Section Coverage, AS-G6 Hero Bookend, AS-G7 Gospel "
        "Frame — these are pre-checked deterministically; echo them and DEFER to the "
        "pre-check verdict.\n"
        "- AS-G8 Thread Continuity — YOUR call: is the episode's thread carried "
        "open → climax → close, with no clip fighting its words? FAIL if a clip "
        "clearly contradicts the line it sits under, or if the close does not land "
        "on the gospel-pivot.\n\n"
        "Return ONLY a JSON object (optionally inside a ```json fence):\n"
        "{\n"
        '  "panel": [{"agent": "Editor", "verdict": "STRONG|CAUTION|REVISION NEEDED", "note": "..."}, ...],\n'
        '  "gates": [{"gate": "AS-G1 Timeline Coverage", "verdict": "PASS|CONDITIONAL|FAIL", "evidence": "...", "fix": "..."}, ...],\n'
        '  "overall": "LOCKED | REVISE | REWORK",\n'
        '  "priority_fixes": ["..."]\n'
        "}\n"
        "LOCKED only when no gate FAILs. No prose outside the JSON object."
    )


def _merge_deterministic(review: EditPlanReview, deterministic: list[GateResult]) -> EditPlanReview:
    det_by_name = {g.gate: g for g in deterministic}
    merged: list[GateResult] = []
    seen: set[str] = set()
    for g in review.gates:
        if g.gate in det_by_name:
            merged.append(det_by_name[g.gate]); seen.add(g.gate)
        else:
            merged.append(g)
    for g in deterministic:
        if g.gate not in seen and g.gate not in {m.gate for m in merged}:
            merged.append(g)
    overall = review.overall
    if any(g.verdict.upper().strip() == "FAIL" for g in merged) and overall.upper().strip() == "LOCKED":
        overall = "REVISE"
    return EditPlanReview(panel=review.panel, gates=merged, overall=overall,
                          priority_fixes=review.priority_fixes)


def _run_review(segments, clips, plan, independent: bool) -> EditPlanReview:
    clips_by_index = {c.scene_index: c for c in clips}
    sections = []
    for s in segments:
        if s.section not in sections:
            sections.append(s.section)
    deterministic = deterministic_gates(plan, segments, clips_by_index)
    role = _review_role(sections, independent=independent)
    user = (_board_block(segments) + "\n\n" + _clips_block(clips) + "\n\n"
            + _plan_block(plan, clips_by_index) + "\n\n" + _deterministic_block(deterministic))
    model = config.REVIEW_MODEL if independent else None
    reply = text_engine._call(role, user, model=model)
    review = EditPlanReview.from_json(text_engine._extract_json(reply))
    return _merge_deterministic(review, deterministic)


def review_edit_plan(segments, clips, plan) -> EditPlanReview:
    return _run_review(segments, clips, plan, independent=False)


def independent_review_edit_plan(segments, clips, plan) -> EditPlanReview:
    return _run_review(segments, clips, plan, independent=True)


def revise_edit_plan(segments, clips, plan, review: EditPlanReview,
                     thread_summary: str = "", log=print) -> EditPlan:
    """Ask the LLM for a corrected skeleton (placement/selection/hero), then
    re-allocate deterministically. Keeps the thread spine; reshapes placement."""
    clips_by_index = {c.scene_index: c for c in clips}
    sections = []
    for s in segments:
        if s.section not in sections:
            sections.append(s.section)
    all_clips = plan.clip_budget >= len(clips)
    budget = len(clips) if all_clips else plan.clip_budget

    panel_str = "\n".join(f"- {a.agent}: {a.verdict} — {a.note}" for a in review.panel)
    gates_str = "\n".join(
        f"- {g.gate}: {g.verdict}" + (f" — FIX: {g.fix}" if g.verdict.upper() != "PASS" and g.fix else "")
        for g in review.gates)
    fixes_str = "\n".join(f"- {f}" for f in review.priority_fixes)

    role = (
        "YOUR TASK: revise the edit plan to fix every issue the review raised, "
        "especially FAIL gates and priority fixes. Keep the thread spine and the "
        "clips that already sit well; only reshape placement/selection/hero as "
        "needed. You still only SELECT, PLACE, and ORDER — Python re-times.\n\n"
        f"Sections (exact keys): {sections}\n\n"
        + _plan_json_contract(sections, budget)
        + "No prose outside the JSON object."
    )
    user = (_board_block(segments) + "\n\n" + _clips_block(clips) + "\n\n"
            + _plan_block(plan, clips_by_index)
            + "\n\n=== REVIEW PANEL ===\n" + panel_str
            + "\n\n=== GATES ===\n" + gates_str
            + "\n\n=== PRIORITY FIXES ===\n" + fixes_str)
    if thread_summary:
        user += f"\n\n=== THREAD SPINE ===\n{thread_summary}"

    reply = text_engine._call(role, user)
    d = text_engine._extract_json(reply)
    section_assignment = {}
    for k, v in (d.get("section_assignment", {}) or {}).items():
        try:
            section_assignment[str(k).strip().lower()] = [int(x) for x in (v or [])]
        except (TypeError, ValueError):
            section_assignment[str(k).strip().lower()] = []
    hero_idx = _pick_hero(clips, int(d.get("hero_scene_index", plan.hero_scene_index) or plan.hero_scene_index))
    section_assignment = _sanitize_assignment(
        section_assignment, sections, clips_by_index, budget, hero_idx, log)
    rationales = {}
    for k, v in (d.get("slot_rationales", {}) or {}).items():
        try:
            rationales[int(k)] = str(v).strip()
        except (TypeError, ValueError):
            continue
    return allocate(
        segments=segments, clips_by_index=clips_by_index, hero_scene_index=hero_idx,
        section_assignment=section_assignment,
        narration_reading=str(d.get("narration_reading", "")).strip() or plan.narration_reading,
        red_team_notes=str(d.get("red_team_notes", "")).strip(),
        slot_rationales=rationales,
    )
