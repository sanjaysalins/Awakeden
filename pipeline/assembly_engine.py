"""The assembly intelligence: the LLM jigsaw matcher + the deterministic slot
allocator + the gate set + self/independent review + revise.

Division of labour: the LLM does the SEMANTIC jigsaw (which clip sits under
which words, in what order, which to drop when over budget, the hero pick). The
allocator does the ARITHMETIC (slot durations, speed-up vs trim-past-cap) in
Python, so the timeline tiles exactly and the speed policy is deterministic.
"""
from __future__ import annotations

import json
import math

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
    Phrase,
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
            # Rule 1 (no reuse): the hero appears ONCE — as the closing still — so it
            # must never also sit in the body. Drop unknown clips, dupes, and the hero.
            if i not in clips_by_index or i in seen or i == hero_idx:
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


def _beat_windows(beats: list[Phrase], body_end: float) -> list[tuple[float, float]]:
    """Contiguous video windows that tile [0, body_end] one-per-phrase. Window i
    runs [phrase_i.start, phrase_{i+1}.start); the first starts at 0 (leading
    silence folds in) and the last ends at body_end. Pauses between phrases fold
    into the preceding beat — so a clip pinned to a phrase plays from when that
    phrase begins until the next begins."""
    n = len(beats)
    if n == 0:
        return []
    starts = [0.0] + [max(0.0, beats[i].start_s) for i in range(1, n)]
    out: list[tuple[float, float]] = []
    for i in range(n):
        s = min(starts[i], body_end)
        e = body_end if i == n - 1 else min(max(starts[i + 1], s), body_end)
        out.append((s, max(s, e)))
    return out


def _sanitize_beats(
    beat_assignment: dict[int, list[int]],
    n_beats: int,
    clips_by_index: dict[int, ClipAsset],
    budget: int,
    hero_idx: int,
    log,
) -> dict[int, list[int]]:
    """Make the LLM's clip→phrase placement safe + budget-bounded: drop unknown
    clips, de-dupe, DROP THE HERO (it is close-only — Rule 1 no reuse), re-home
    clips on unknown beats to the last beat, trim to budget by lowest weight
    (never the gospel frame / hook / close)."""
    seen: set[int] = set()
    cleaned: dict[int, list[int]] = {}
    homeless: list[int] = []
    for k, idxs in beat_assignment.items():
        try:
            b = int(k)
        except (TypeError, ValueError):
            b = None
        target = b if (b is not None and 0 <= b < n_beats) else None
        for i in idxs:
            if i not in clips_by_index or i in seen or i == hero_idx:
                continue
            seen.add(i)
            (cleaned.setdefault(target, []) if target is not None else homeless).append(i)
    if homeless and n_beats:
        host = n_beats - 1
        cleaned.setdefault(host, []).extend(homeless)
        log(f"      ! re-homed clips {homeless} from unknown beat index(es) into beat {host}")

    total = sum(len(v) for v in cleaned.values())
    if budget and total > budget:
        droppable: list[tuple[int, int, float]] = []
        for b, idxs in cleaned.items():
            for i in idxs:
                c = clips_by_index[i]
                if _is_gospel_pivot(c) or c.viral_role in ("hook-open", "close", "climax"):
                    continue
                droppable.append((i, b, _weight(c)))
        droppable.sort(key=lambda t: t[2])
        to_drop = total - budget
        dropped: list[int] = []
        for i, b, _w in droppable:
            if to_drop <= 0:
                break
            cleaned[b].remove(i)
            dropped.append(i)
            to_drop -= 1
        if dropped:
            log(f"      [budget] dropped lowest-weight clip(s) {sorted(dropped)} to hit budget {budget}")
    return {b: v for b, v in cleaned.items() if v}


def allocate(
    segments: list[NarrationSegment],
    clips_by_index: dict[int, ClipAsset],
    hero_scene_index: int,
    section_assignment: dict[str, list[int]] | None = None,
    narration_reading: str = "",
    red_team_notes: str = "",
    slot_rationales: dict[int, str] | None = None,
    notes: str = "",
    beats: list[Phrase] | None = None,
    beat_assignment: dict[int, list[int]] | None = None,
) -> EditPlan:
    """Turn the LLM skeleton into a fully-timed EditPlan with computed slots.

    Two matching modes:
      • BEAT mode (Rule 3): `beats` (phrases w/ real word times) + `beat_assignment`
        ({beat_index: [scene_index]}) pin each clip under the exact words it depicts.
      • Legacy SECTION mode: `section_assignment` ({section: [scene_index]}).
    In BOTH, the hero (Christ / cross / NT-pivot) appears EXACTLY ONCE — as the
    closing still (Rule 1 no reuse) — and is never placed in the body."""
    min_slot = config.ASSEMBLY_MIN_SLOT
    # Hero is single-appearance: it only holds at the CLOSE. The legacy "hero" open
    # mode (both-ends hold) would reuse the hero, so it is disabled in beat mode.
    use_beats = bool(beats) and beat_assignment is not None
    hero_head = (config.ASSEMBLY_HERO_HEAD
                 if (config.ASSEMBLY_OPEN_MODE == "hero" and not use_beats) else 0.0)
    hero_tail = config.ASSEMBLY_HERO_TAIL
    total = total_seconds(segments)
    slot_rationales = slot_rationales or {}
    section_assignment = section_assignment or {}
    body_end = total - hero_tail

    # sized: ordered list of (window_len, [(clip, beat_or_None)]) blocks. Empty/too-small
    # windows fold their time + clips forward so the body tiles exactly and every clip
    # keeps the beat phrase it was assigned (for beat-accurate verification).
    sized: list[tuple[float, list[tuple[ClipAsset, Phrase | None]]]] = []
    carry = 0.0
    pending: list[tuple[ClipAsset, Phrase | None]] = []

    if use_beats:
        windows = _beat_windows(beats, body_end)
        for i, beat in enumerate(beats):
            ws, we = windows[i]
            wlen = max(0.0, we - ws) + carry
            here = pending + [(clips_by_index[j], beat)
                              for j in beat_assignment.get(i, []) if j in clips_by_index]
            if not here or wlen < min_slot:
                carry, pending = wlen, here
                continue
            carry, pending = 0.0, []
            sized.append((wlen, here))
    else:
        windows_s = _video_windows(segments, hero_head, hero_tail)
        for section, ws, we in windows_s:
            wlen = max(0.0, we - ws) + carry
            here = pending + [(clips_by_index[i], _FakeBeat(section))
                              for i in section_assignment.get(section, []) if i in clips_by_index]
            if not here or wlen < min_slot:
                carry, pending = wlen, here
                continue
            carry, pending = 0.0, []
            sized.append((wlen, here))

    if (pending or carry > 0) and sized:        # flush trailing into the last block
        wl, cl = sized[-1]
        sized[-1] = (wl + carry, cl + pending)
    elif pending and not sized:                 # degenerate: everything collapsed
        sized.append((max(min_slot, body_end), pending))

    slots: list[EditSlot] = []
    order = 0
    hero = clips_by_index.get(hero_scene_index)

    # body slots
    cursor = hero_head if (hero is not None and hero_head > 0) else 0.0
    for wlen, pairs in sized:
        clips_here = [c for c, _b in pairs]
        durs = _distribute(wlen, clips_here, min_slot)
        for (clip, beat), dur in zip(pairs, durs):
            S, src_in, src_out, op = _slot_op(clip, dur)
            slots.append(EditSlot(
                order=order, role="body", scene_index=clip.scene_index,
                section=(beat.section if beat else ""),
                slot_start_s=round(cursor, 3), slot_end_s=round(cursor + dur, 3),
                source_in_s=round(src_in, 3), source_out_s=round(src_out, 3),
                speed_factor=round(S, 4), op=op,
                rationale=slot_rationales.get(clip.scene_index, ""),
                beat_index=(beat.index if isinstance(beat, Phrase) else -1),
                beat_phrase=(beat.text if isinstance(beat, Phrase) else ""),
            ))
            cursor += dur
            order += 1

    # hero close (single appearance — the CTA landing on Christ, held as a still)
    if hero is not None and hero_tail > 0:
        slots.append(EditSlot(
            order=order, role="hero-tail", scene_index=hero.scene_index,
            section="hero", slot_start_s=round(total - hero_tail, 3), slot_end_s=round(total, 3),
            source_in_s=0.0, source_out_s=min(hero_tail, hero.natural_duration_s),
            speed_factor=1.0, op="speed",
            rationale="Hero close — the cut lands on Christ (single appearance, no reuse).",
        ))
        order += 1

    selected = [c.scene_index for _wl, pairs in sized for c, _b in pairs]
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


class _FakeBeat:
    """Lightweight section carrier for the legacy (no-alignment) path so body slots
    still record their section without a real Phrase."""
    index = -1
    text = ""

    def __init__(self, section: str):
        self.section = section


# --------------------------------------------------------------------------
# Episode-fit safety net — drop clips that visibly tell ANOTHER story (the last
# line of defence behind the library's topical-fit gate; also covers non-library
# episodes). Flagged non-pivot clips are excluded before matching.
# --------------------------------------------------------------------------
_OFFTOPIC_ROLE = (
    "You are a topical-coherence auditor for a 60-second gospel Short. Given the episode "
    "NARRATION and a list of clips (title + subject), flag any clip that visibly tells a "
    "DIFFERENT story — an element from another parable or scene that is NOT in this "
    "narration (e.g. a swine / carob husks / feeding-trough = the Prodigal; a courtyard "
    "charcoal fire with a denying man = Peter's denial; a well / pool / storm the narration "
    "never mentions). A clip is FINE if it is a generic plate (bread, candle, hands, table, "
    "light, a cross, Christ, an anonymous figure) OR depicts something in this narration. "
    "Do NOT flag the cross / Christ. Be conservative: only flag a clear foreign story.\n"
    'Return ONLY JSON: {"offtopic": [{"scene_index": <int>, "foreign_element": "...", "reason": "..."}]}'
)


def flag_offtopic_clips(clips: list[ClipAsset], narration_text: str, log=print) -> dict[int, str]:
    """LLM check: which clips import a foreign story not in this narration?
    Returns {scene_index: foreign_element}. Empty on any parse failure (fail-open
    so a flaky audit never blocks a good cut)."""
    if not clips or not narration_text.strip():
        return {}
    block = "\n".join(f'#{c.scene_index:02d} "{c.title}": {c.subject_block[:170]}' for c in clips)
    user = (f"EPISODE NARRATION:\n{narration_text}\n\nCLIPS:\n{block}\n\n"
            "Flag only clips that clearly depict a different story. Return the JSON.")
    try:
        d = text_engine._extract_json(text_engine._call(_OFFTOPIC_ROLE, user, label="assembly-episode-fit"))
    except Exception as e:
        log(f"      (episode-fit audit skipped: {e})")
        return {}
    out: dict[int, str] = {}
    for r in (d.get("offtopic") or []):
        try:
            out[int(r.get("scene_index"))] = str(r.get("foreign_element") or r.get("reason") or "off-topic")
        except (TypeError, ValueError):
            continue
    return out


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
        '  "hero_scene_index": <int — the gospel-pivot (Christ/cross/NT-link) clip that CLOSES the cut as the CTA landing>,\n'
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
        "- OPEN on the single most ARRESTING hook-open clip — the scroll-stopper that "
        "makes a viewer stop in the first second. It is topic-driven and does NOT have to "
        "be Jesus. Place it first in the first section.\n"
        "- The HERO is the Christ / cross / NT-gospel-pivot image (the one the CTA points "
        "to), NOT merely the most emotional frame. It CLOSES the cut as the gospel landing. "
        "Put the hero in your section_assignment under its natural section too.\n"
        "- Keep the GOSPEL FRAME intact even when dropping clips: always keep the "
        "cross / passion clip, at least one Jesus / NT-gospel-link clip, one hook-open, "
        "and one close. Drop only the weakest 'build' clips.\n"
        "- You do NOT set durations or speeds — Python computes those. Just SELECT, "
        "PLACE, and ORDER.\n\n"
        f"Sections available (use these exact keys): {sections}\n\n"
        + _plan_json_contract(sections, budget)
        + "No prose outside the JSON object."
    )


# ---- Beat-pinning (Rule 3) prompt + parsing ----
def _phrase_block(beats: list[Phrase]) -> str:
    lines = ["=== PHRASE BOARD (numbered BEATS — pin each clip to the beat it depicts) ==="]
    for p in beats:
        lines.append(f"P{p.index:02d} [{p.section}/{p.speaker}] "
                     f"{p.start_s:.2f}-{p.end_s:.2f}s: {p.text}")
    return "\n".join(lines)


def _beat_json_contract() -> str:
    return (
        "Return ONLY a JSON object (optionally inside a ```json fence):\n"
        "{\n"
        '  "narration_reading": "2-4 sentences: how you pinned clips to the spoken beats",\n'
        '  "red_team_notes": "your own honest doubts about this cut",\n'
        '  "hero_scene_index": <int — the gospel-pivot (Christ/cross/NT-link) clip that CLOSES the cut>,\n'
        '  "beat_assignment": {"<beat index, e.g. 0 or 3>": [<scene indices, in play order>]},\n'
        '  "slot_rationales": {"<scene_index>": "why this clip sits under that beat\'s words"}\n'
        "}\n"
    )


def _beat_matcher_role(n_beats: int, budget: int, all_clips: bool) -> str:
    budget_rule = (
        f"Use ALL {budget} clips."
        if all_clips else
        f"Use EXACTLY {budget} distinct clips — keep the strongest, DROP the weakest 'build' clips."
    )
    return (
        "You are the EDITOR of a 60-second vertical gospel Short. The narration is split "
        "into numbered BEATS (short phrases, each with real start/end times). Pin each clip "
        "to the BEAT it depicts, so the image is on-screen exactly while those words are "
        "spoken. Reason from each clip's subject/role and the beat's words.\n\n"
        "RULES:\n"
        f"- {budget_rule}\n"
        "- NO REUSE (Rule 1): each clip appears at most ONCE across all beats.\n"
        "- PIN BY MEANING (Rule 3): the clip showing an action goes on the beat that speaks "
        "that action; the named object on the beat naming it; the OT/NT echo on the beat it "
        "echoes. The image must match the words playing under it.\n"
        "- LOTS OF MOMENTS (Rule 2): spread clips so MANY beats each get a fresh image — do "
        "not park several clips on one beat while others go bare. Prefer one strong clip per "
        "beat, in time order.\n"
        "- OPEN on the single most ARRESTING hook-open clip — pin it to beat 0. It is "
        "topic-driven and need NOT be Jesus.\n"
        "- HERO CLOSE: the hero is the Christ / cross / NT-gospel-pivot image. It CLOSES the "
        "cut as a held still and is its ONLY appearance — do NOT put the hero in "
        "beat_assignment; just name it in hero_scene_index.\n"
        "- Keep the gospel frame: a hook-open at the start and the gospel-pivot as the hero close.\n"
        "- You do NOT set durations/speeds — Python times each clip to its beat window. Just "
        "SELECT, PIN, and ORDER.\n\n"
        f"Beats available: 0..{n_beats - 1} (use these integer indices as keys).\n\n"
        + _beat_json_contract()
        + "No prose outside the JSON object."
    )


def _parse_beat_assignment(raw: dict | None, n_beats: int) -> dict[int, list[int]]:
    out: dict[int, list[int]] = {}
    for k, v in (raw or {}).items():
        ks = _re.sub(r"\D", "", str(k))   # 'P03' / 'beat 3' -> '03'
        if ks == "":
            continue
        try:
            b = int(ks)
        except ValueError:
            continue
        try:
            out[b] = [int(x) for x in (v or [])]
        except (TypeError, ValueError):
            out[b] = []
    return out


def _parse_rationales(raw: dict | None) -> dict[int, str]:
    out: dict[int, str] = {}
    for k, v in (raw or {}).items():
        try:
            out[int(k)] = str(v).strip()
        except (TypeError, ValueError):
            continue
    return out


def plan_edit(
    segments: list[NarrationSegment],
    clips: list[ClipAsset],
    clip_budget: int,
    thread_summary: str = "",
    hero_pref: int = 0,
    beats: list[Phrase] | None = None,
    log=print,
) -> EditPlan:
    """LLM jigsaw → deterministic allocation → fully-timed EditPlan. When `beats`
    (phrases with real word times) are provided, the matcher pins each clip to the
    beat it depicts (Rule 3); otherwise it falls back to section-level placement."""
    clips_by_index = {c.scene_index: c for c in clips}
    sections = []
    for s in segments:
        if s.section not in sections:
            sections.append(s.section)
    all_clips = clip_budget >= len(clips)
    budget = len(clips) if all_clips else clip_budget
    use_beats = bool(beats)

    if use_beats:
        role = _beat_matcher_role(len(beats), budget, all_clips)
        user = (_board_block(segments) + "\n\n" + _phrase_block(beats)
                + "\n\n" + _clips_block(clips))
    else:
        role = _matcher_role(sections, budget, all_clips)
        user = _board_block(segments) + "\n\n" + _clips_block(clips)
    if thread_summary:
        user += f"\n\n=== THREAD SPINE (carry through open → climax → close) ===\n{thread_summary}"
    if hero_pref:
        user += f"\n\nHERO PREFERENCE: scene #{hero_pref:02d} (use unless a stronger on-thread image exists)."

    reply = text_engine._call(role, user)
    d = text_engine._extract_json(reply)

    # Hero MUST be a gospel-pivot so the cut lands on Christ (_pick_hero overrides the
    # LLM if it nominated an emotional non-pivot; honours a valid pivot preference).
    hero_idx = _pick_hero(clips, int(d.get("hero_scene_index", hero_pref) or hero_pref or 0))
    rationales = _parse_rationales(d.get("slot_rationales"))

    if use_beats:
        beat_assignment = _parse_beat_assignment(d.get("beat_assignment"), len(beats))
        beat_assignment = _sanitize_beats(beat_assignment, len(beats), clips_by_index,
                                          budget, hero_idx, log)
        return allocate(
            segments=segments, clips_by_index=clips_by_index, hero_scene_index=hero_idx,
            beats=beats, beat_assignment=beat_assignment,
            narration_reading=str(d.get("narration_reading", "")).strip(),
            red_team_notes=str(d.get("red_team_notes", "")).strip(),
            slot_rationales=rationales,
        )

    section_assignment = {}
    for k, v in (d.get("section_assignment", {}) or {}).items():
        try:
            section_assignment[str(k).strip().lower()] = [int(x) for x in (v or [])]
        except (TypeError, ValueError):
            section_assignment[str(k).strip().lower()] = []
    section_assignment = _sanitize_assignment(
        section_assignment, sections, clips_by_index, budget, hero_idx, log)
    return allocate(
        segments=segments, clips_by_index=clips_by_index, hero_scene_index=hero_idx,
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
    """Rule 1 — no clip reused within the cut. Every body clip is distinct AND the
    hero (the closing still) does NOT also appear in the body (that would show the
    same image twice)."""
    body = plan.body_slots
    body_idxs = [s.scene_index for s in body]
    distinct = set(body_idxs)
    if len(body_idxs) != len(distinct):
        dupes = sorted({i for i in body_idxs if body_idxs.count(i) > 1})
        return GateResult("AS-G2 No Reuse", "FAIL",
                          f"Body clips repeat: {dupes}.",
                          "Each clip may appear at most once in the cut (Rule 1).")
    if plan.hero_scene_index in distinct:
        return GateResult("AS-G2 No Reuse", "FAIL",
                          f"Hero #{plan.hero_scene_index:02d} also plays in the body — that "
                          "reuses the closing image.",
                          "The hero appears ONCE, as the closing still. Remove it from the body.")
    tail = [s for s in plan.slots if s.role == "hero-tail"]
    if not tail or tail[0].scene_index != plan.hero_scene_index:
        return GateResult("AS-G2 No Reuse", "FAIL",
                          "No closing hero still on the gospel-pivot.",
                          "Close on the hero (Christ / cross / NT-link) as a single held still.")
    return GateResult("AS-G2 No Reuse", "PASS",
                      f"{len(distinct)} distinct body clips; hero #{plan.hero_scene_index:02d} "
                      "appears once (close only) — no reuse.")


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
    # The hero close still covers the tail window — credit the section(s) it sits over
    # (the hero is no longer a body clip, so its landing section is covered by the close).
    if plan.hero_tail_s > 0 and segments:
        tail_start = plan.total_seconds - plan.hero_tail_s
        for seg in segments:
            if seg.end_s > tail_start:
                covered.add(seg.section)
    missing = [seg.section for seg in segments if seg.text and seg.section not in covered]
    if missing:
        return GateResult("AS-G5 Section Coverage", "FAIL",
                          f"Narration section(s) with no clip: {missing}.",
                          "Assign at least one clip to every spoken section.")
    return GateResult("AS-G5 Section Coverage", "PASS",
                      f"Every spoken section has a clip: {sorted(covered)}.")


def _check_g6_hero(plan: EditPlan, clips_by_index: dict[int, ClipAsset]) -> GateResult:
    """The cut OPENS on a scroll-stopping hook clip and CLOSES on the gospel-pivot
    hero as a single held still (the CTA landing on Christ). The hero appears only
    here — never in the body (Rule 1)."""
    tail = [s for s in plan.slots if s.role == "hero-tail"]
    if not tail:
        return GateResult("AS-G6 Hero Close", "FAIL", "No hero close slot.",
                          "Close the cut on the gospel-pivot hero (the CTA landing).")
    t = tail[0]
    if t.scene_index != plan.hero_scene_index:
        return GateResult("AS-G6 Hero Close", "FAIL",
                          f"close #{t.scene_index} != hero #{plan.hero_scene_index}.",
                          "The closing hold must be the hero clip.")
    hero_clip = clips_by_index.get(plan.hero_scene_index)
    if hero_clip is not None and not _is_gospel_pivot(hero_clip):
        return GateResult("AS-G6 Hero Close", "FAIL",
                          f"Hero #{plan.hero_scene_index:02d} '{hero_clip.title}' is NOT a "
                          f"gospel-pivot (arc={hero_clip.arc_position}); the cut would close "
                          "on a non-Christ image.",
                          "Make the hero the cross / Christ / NT-gospel-link image.")
    body = sorted(plan.body_slots, key=lambda s: s.order)
    first = clips_by_index.get(body[0].scene_index) if body else None
    if first is not None and first.viral_role != "hook-open":
        return GateResult("AS-G6 Hero Close", "CONDITIONAL",
                          f"Cut opens on #{first.scene_index:02d} '{first.title}' "
                          f"(role={first.viral_role}), not a hook-open clip.",
                          "Open on the strongest hook-open scroll-stopper.")
    if not (2.0 <= t.slot_duration_s <= 3.0):
        return GateResult("AS-G6 Hero Close", "CONDITIONAL",
                          f"hero close {t.slot_duration_s:.2f}s (target 2-3s).",
                          "Keep the closing hero hold in the 2-3s range.")
    return GateResult("AS-G6 Hero Close", "PASS",
                      f"Opens on hook #{body[0].scene_index:02d}; gospel-pivot hero "
                      f"#{plan.hero_scene_index:02d} closes {t.slot_duration_s:.1f}s (single appearance).")


def _check_g7_gospel_frame(plan: EditPlan, clips_by_index: dict[int, ClipAsset]) -> GateResult:
    """AS-G7 Gospel-Frame Survival (deterministic). The cut must still land on
    Christ: a gospel-pivot (cross / resurrection / NT-link) must be present — the
    HERO close counts, since the hero is no longer a body clip. A hook-open and an
    explicit close clip are recommended. Protects the LOCKED thread-spine rule."""
    body = [clips_by_index[s.scene_index] for s in plan.body_slots if s.scene_index in clips_by_index]
    if not body:
        return GateResult("AS-G7 Gospel Frame", "FAIL", "No body clips.", "")
    hero_clip = clips_by_index.get(plan.hero_scene_index)
    frame = body + ([hero_clip] if hero_clip is not None else [])
    has_pivot = any(_is_gospel_pivot(c) for c in frame)  # cross OR resurrection OR NT-link
    has_cross = any(_is_cross(c) for c in frame)
    has_open = any(c.viral_role == "hook-open" for c in body)
    has_close = any(c.viral_role == "close" for c in frame) or (hero_clip is not None)
    if not has_pivot:
        return GateResult("AS-G7 Gospel Frame", "FAIL",
                          "No gospel-pivot anywhere (cross / resurrection / NT-link) — the cut "
                          "would not land on Christ.",
                          "Keep a Jesus / cross / NT-gospel-link clip; close on it.")
    missing = []
    if not has_cross:
        missing.append("a cross/passion image (ok if the pivot is resurrection/NT-link)")
    if not has_open:
        missing.append("a hook-open clip")
    if not has_close:
        missing.append("a close clip")
    if missing:
        return GateResult("AS-G7 Gospel Frame", "CONDITIONAL",
                          f"Gospel-pivot present (lands on Christ). Soft-missing: {', '.join(missing)}.",
                          "Add a hook-open if available; cross optional when the pivot is resurrection.")
    return GateResult("AS-G7 Gospel Frame", "PASS",
                      "Gospel-pivot + hook-open + close all present; cut lands on Christ.")


def _check_g9_density(plan: EditPlan, n_pool: int, all_clips: bool) -> GateResult:
    """AS-G9 Beat Density (Rule 2: more clips, sped up, lots of moments). ADVISORY
    ONLY — never FAIL: a small pool cannot be fixed by the matcher (re-running would
    just thrash), so this flags slow cuts and reports how many more clips to RENDER
    upstream, rather than blocking."""
    body = plan.body_slots
    if not body:
        return GateResult("AS-G9 Beat Density", "CONDITIONAL", "No body slots.", "")
    target = config.ASSEMBLY_TARGET_SLOT
    moments = len(body)
    body_window = sum(s.slot_duration_s for s in body)
    avg = body_window / moments
    if avg <= target + 0.5:
        return GateResult("AS-G9 Beat Density", "PASS",
                          f"{moments} moments · avg slot {avg:.1f}s (target {target:.0f}s) — lively.")
    want = max(moments + 1, int(math.ceil(body_window / target)))
    deficit = max(1, want - moments)
    if all_clips:
        fix = (f"Pool-bound (only {n_pool} clips). Render ~{deficit} more clip(s) upstream "
               f"(cli_visual) to reach ~{want} fast moments at ~{target:.0f}s each.")
    else:
        fix = f"Raise --clips toward {want} (pool has {n_pool})."
    return GateResult("AS-G9 Beat Density", "CONDITIONAL",
                      f"{moments} moments · avg slot {avg:.1f}s > target {target:.0f}s — feels slow "
                      f"for 'lots of moments'.", fix)


def deterministic_gates(plan: EditPlan, segments: list[NarrationSegment],
                        clips_by_index: dict[int, ClipAsset],
                        clip_budget: int | None = None) -> list[GateResult]:
    n_pool = len(clips_by_index)
    all_clips = clip_budget is None or clip_budget >= n_pool
    return [
        _check_g1_coverage(plan),
        _check_g2_budget(plan),
        _check_g3_speed(plan),
        _check_g4_min_slot(plan),
        _check_g5_section_coverage(plan, segments),
        _check_g6_hero(plan, clips_by_index),
        _check_g7_gospel_frame(plan, clips_by_index),
        _check_g9_density(plan, n_pool, all_clips),
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
        beat = f'  ⤷ under: "{s.beat_phrase}"' if s.beat_phrase else ""
        lines.append(
            f"  {s.order:>2} {s.role:<10} {s.section:<8} #{s.scene_index:02d} "
            f"{s.slot_start_s:5.2f}-{s.slot_end_s:5.2f} ({s.slot_duration_s:4.2f}s) "
            f"{s.speed_factor:.2f}x {s.op:<11} {title}{beat}"
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
    "- Editor — does the cut flow; are slots paced for a 60s Short, with LOTS of distinct "
    "moments (not a few long static holds, not a strobe)?\n"
    "- Beat-Sync — does each clip sit under the EXACT phrase it depicts (the 'under: \"...\"' "
    "line)? The action clip on the beat that speaks the action; the named object on the beat "
    "naming it; the echo on the beat it echoes. Flag any clip fighting its words.\n"
    "- No-Reuse — is every clip used at most once, and does the Christ/hero image appear "
    "only at the close (never also in the body)?\n"
    "- Pacing — are speed-ups/trims tasteful for slow Baroque footage? Are SACRED clips "
    "(Christ / cross / the landing) kept near full speed, never jittery?\n"
    "- Hero-Continuity — does the cut OPEN on a strong hook (a scroll-stopper) and CLOSE "
    "cleanly on the Christ / gospel-pivot hero, so it LANDS on Jesus (not on a merely "
    "emotional frame)?\n"
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
        "- AS-G1 Timeline Coverage, AS-G2 No Reuse, AS-G3 Speed/Trim Health, "
        "AS-G4 Min Slot, AS-G5 Section Coverage, AS-G6 Hero Close, AS-G7 Gospel "
        "Frame, AS-G9 Beat Density — these are pre-checked deterministically; echo them "
        "and DEFER to the pre-check verdict (AS-G9 is advisory and never FAILs).\n"
        "- AS-G8 Beat Continuity — YOUR call: is the episode's thread carried "
        "open → climax → close, with each clip sitting under the right phrase? FAIL if a "
        "clip clearly contradicts the words it plays under, or if the close does not land "
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


def _run_review(segments, clips, plan, independent: bool, beats=None) -> EditPlanReview:
    clips_by_index = {c.scene_index: c for c in clips}
    sections = []
    for s in segments:
        if s.section not in sections:
            sections.append(s.section)
    deterministic = deterministic_gates(plan, segments, clips_by_index,
                                        clip_budget=plan.clip_budget)
    role = _review_role(sections, independent=independent)
    board = _phrase_block(beats) if beats else _board_block(segments)
    user = (board + "\n\n" + _clips_block(clips) + "\n\n"
            + _plan_block(plan, clips_by_index) + "\n\n" + _deterministic_block(deterministic))
    model = config.REVIEW_MODEL if independent else None
    reply = text_engine._call(role, user, model=model)
    review = EditPlanReview.from_json(text_engine._extract_json(reply))
    return _merge_deterministic(review, deterministic)


def review_edit_plan(segments, clips, plan, beats=None) -> EditPlanReview:
    return _run_review(segments, clips, plan, independent=False, beats=beats)


def independent_review_edit_plan(segments, clips, plan, beats=None) -> EditPlanReview:
    return _run_review(segments, clips, plan, independent=True, beats=beats)


def revise_edit_plan(segments, clips, plan, review: EditPlanReview,
                     thread_summary: str = "", beats=None, log=print) -> EditPlan:
    """Ask the LLM for a corrected skeleton (placement/selection/hero), then
    re-allocate deterministically. Keeps the thread spine; reshapes placement.
    In beat mode it re-pins clips to phrases (Rule 3)."""
    clips_by_index = {c.scene_index: c for c in clips}
    sections = []
    for s in segments:
        if s.section not in sections:
            sections.append(s.section)
    all_clips = plan.clip_budget >= len(clips)
    budget = len(clips) if all_clips else plan.clip_budget
    use_beats = bool(beats)

    panel_str = "\n".join(f"- {a.agent}: {a.verdict} — {a.note}" for a in review.panel)
    gates_str = "\n".join(
        f"- {g.gate}: {g.verdict}" + (f" — FIX: {g.fix}" if g.verdict.upper() != "PASS" and g.fix else "")
        for g in review.gates)
    fixes_str = "\n".join(f"- {f}" for f in review.priority_fixes)

    if use_beats:
        contract = _beat_json_contract()
        keys_line = f"Beats available: 0..{len(beats) - 1} (integer keys).\n\n"
    else:
        contract = _plan_json_contract(sections, budget)
        keys_line = f"Sections (exact keys): {sections}\n\n"
    role = (
        "YOUR TASK: revise the edit plan to fix every issue the review raised, "
        "especially FAIL gates and priority fixes. Keep the thread spine and the "
        "clips that already sit well; only reshape placement/selection/hero as "
        "needed. Honour NO REUSE (each clip once; hero only at the close, never in "
        "the body) and pin each clip to the beat it depicts. You still only SELECT, "
        "PIN, and ORDER — Python re-times.\n\n"
        + keys_line
        + contract
        + "No prose outside the JSON object."
    )
    board = _phrase_block(beats) if use_beats else _board_block(segments)
    user = (board + "\n\n" + _clips_block(clips) + "\n\n"
            + _plan_block(plan, clips_by_index)
            + "\n\n=== REVIEW PANEL ===\n" + panel_str
            + "\n\n=== GATES ===\n" + gates_str
            + "\n\n=== PRIORITY FIXES ===\n" + fixes_str)
    if thread_summary:
        user += f"\n\n=== THREAD SPINE ===\n{thread_summary}"

    reply = text_engine._call(role, user)
    d = text_engine._extract_json(reply)
    hero_idx = _pick_hero(clips, int(d.get("hero_scene_index", plan.hero_scene_index) or plan.hero_scene_index))
    rationales = _parse_rationales(d.get("slot_rationales"))

    if use_beats:
        beat_assignment = _parse_beat_assignment(d.get("beat_assignment"), len(beats))
        beat_assignment = _sanitize_beats(beat_assignment, len(beats), clips_by_index,
                                          budget, hero_idx, log)
        return allocate(
            segments=segments, clips_by_index=clips_by_index, hero_scene_index=hero_idx,
            beats=beats, beat_assignment=beat_assignment,
            narration_reading=str(d.get("narration_reading", "")).strip() or plan.narration_reading,
            red_team_notes=str(d.get("red_team_notes", "")).strip(),
            slot_rationales=rationales,
        )

    section_assignment = {}
    for k, v in (d.get("section_assignment", {}) or {}).items():
        try:
            section_assignment[str(k).strip().lower()] = [int(x) for x in (v or [])]
        except (TypeError, ValueError):
            section_assignment[str(k).strip().lower()] = []
    section_assignment = _sanitize_assignment(
        section_assignment, sections, clips_by_index, budget, hero_idx, log)
    return allocate(
        segments=segments, clips_by_index=clips_by_index, hero_scene_index=hero_idx,
        section_assignment=section_assignment,
        narration_reading=str(d.get("narration_reading", "")).strip() or plan.narration_reading,
        red_team_notes=str(d.get("red_team_notes", "")).strip(),
        slot_rationales=rationales,
    )
