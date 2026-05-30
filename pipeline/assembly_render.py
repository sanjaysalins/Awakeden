"""Render the edit plan to MP4 (viral cut + all-takes reel) and Vision-verify it.

render_cut drives the validated per-segment → concat-copy → mux chain in
assembly_ffmpeg. verify_cut is an advisory per-slot Claude Vision check (does
each clip match the words spoken under it) — it never blocks the render, it
produces a re-plan/re-roll list. Per CLAUDE.md, also eyeball frames yourself.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import config
from pipeline import engine as text_engine
from pipeline import assembly_ffmpeg as F
from pipeline.assembly_models import (
    AssemblyAudit,
    ClipAsset,
    EditPlan,
    NarrationSegment,
    SlotVerdict,
)
from pipeline.visual_render import _encode_image_for_vision


SEGMENTS_SUBDIR = "segments"
VIRAL_CUT_NAME = "viral_cut.mp4"
REEL_NAME = "all_takes_reel.mp4"


# --------------------------------------------------------------------------
# Render the viral cut
# --------------------------------------------------------------------------
def render_cut(
    plan: EditPlan,
    clips_by_index: dict[int, ClipAsset],
    narration_mp3: Path,
    out_dir: Path,
    rebuild: bool = False,
    log=print,
) -> Path:
    """Per-segment intermediates → stream-copy concat → mux narration."""
    F.require_ffmpeg()
    out_dir.mkdir(parents=True, exist_ok=True)
    final = out_dir / VIRAL_CUT_NAME
    if final.exists() and not rebuild:
        log(f"      [skip] {final.name} exists — pass rebuild=True to re-render")
        return final

    seg_dir = out_dir / SEGMENTS_SUBDIR
    seg_dir.mkdir(parents=True, exist_ok=True)

    # Hero bookend stills (default): any hero-head / hero-tail slot renders as a frozen
    # still of the hero image rather than the animated clip. In the default "hook" open
    # mode only the CLOSING hero hold exists (motion open on the hook clip, reverent still
    # close on Christ); legacy "hero" mode stills both ends. We resolve ONE still source
    # for the hero and reuse it for whatever bookend slots exist.
    hero_still_src: Path | None = None
    if config.ASSEMBLY_HERO_STILL:
        hero_idx = next((s.scene_index for s in plan.slots if s.role == "hero-head"),
                        next((s.scene_index for s in plan.slots if s.role == "hero-tail"), None))
        hero_clip = clips_by_index.get(hero_idx) if hero_idx is not None else None
        if hero_clip is not None:
            png = Path(hero_clip.mp4_path).with_suffix(".png")
            if not png.exists():
                png = F.extract_frame(Path(hero_clip.mp4_path), seg_dir / "_hero_still.png", t=0.0)
            hero_still_src = png

    seg_paths: list[Path] = []
    for s in sorted(plan.slots, key=lambda x: x.order):
        clip = clips_by_index.get(s.scene_index)
        if clip is None:
            raise SystemExit(f"Slot {s.order} references missing clip #{s.scene_index}.")
        seg = seg_dir / f"seg{s.order:02d}_{s.role}_{s.scene_index:02d}.mp4"
        is_bookend = s.role in ("hero-head", "hero-tail")
        if is_bookend and hero_still_src is not None:
            log(f"      [seg {s.order:>2}] {s.role:<10} #{s.scene_index:02d} "
                f"{s.slot_duration_s:4.2f}s STILL bookend (frozen hero)")
            F.render_still(
                image_src=hero_still_src, out=seg,
                duration_s=s.slot_duration_s, log=log,
            )
        else:
            log(f"      [seg {s.order:>2}] {s.role:<10} #{s.scene_index:02d} "
                f"{s.slot_duration_s:4.2f}s @ {s.speed_factor:.2f}x ({s.op})")
            F.render_segment(
                src=Path(clip.mp4_path), out=seg,
                source_in_s=s.source_in_s, source_out_s=s.source_out_s,
                speed_factor=s.speed_factor, slot_duration_s=s.slot_duration_s, log=log,
            )
        seg_paths.append(seg)

    body = out_dir / "_body_concat.mp4"
    log(f"      [concat] {len(seg_paths)} segments -> {body.name}")
    F.concat_copy(seg_paths, body, log=log)
    expected = sum(s.slot_duration_s for s in plan.slots)
    actual = F.ffprobe_duration(body)
    if abs(actual - expected) > 0.3:
        log(f"      ! WARNING: concat duration {actual:.2f}s != expected {expected:.2f}s "
            "(a segment may have rendered wrong) — inspect segments/.")
    log(f"      [mux] narration -> {final.name}")
    F.mux_narration(body, narration_mp3, final, log=log)
    log(f"      viral cut: {final}  ({F.ffprobe_duration(final):.2f}s)")
    return final


# --------------------------------------------------------------------------
# Render the all-takes reel (every clip, full length, scene order)
# --------------------------------------------------------------------------
def render_reel(
    clips: list[ClipAsset], out_dir: Path, rebuild: bool = False, log=print
) -> Path:
    """Normalise every clip to the canvas (speed 1.0, full length) and concat —
    a silent ~160s review reel of all clips in scene order."""
    F.require_ffmpeg()
    out_dir.mkdir(parents=True, exist_ok=True)
    reel = out_dir / REEL_NAME
    if reel.exists() and not rebuild:
        log(f"      [skip] {reel.name} exists")
        return reel
    seg_dir = out_dir / SEGMENTS_SUBDIR / "reel"
    seg_dir.mkdir(parents=True, exist_ok=True)
    seg_paths: list[Path] = []
    for c in sorted(clips, key=lambda x: x.scene_index):
        seg = seg_dir / f"reel_{c.scene_index:02d}.mp4"
        F.render_segment(
            src=Path(c.mp4_path), out=seg,
            source_in_s=0.0, source_out_s=c.natural_duration_s,
            speed_factor=1.0, slot_duration_s=c.natural_duration_s, log=log,
        )
        seg_paths.append(seg)
    log(f"      [reel] concat {len(seg_paths)} clips -> {reel.name}")
    F.concat_copy(seg_paths, reel, log=log)
    log(f"      reel: {reel}  ({F.ffprobe_duration(reel):.2f}s)")
    return reel


# --------------------------------------------------------------------------
# Per-slot Vision verification (advisory)
# --------------------------------------------------------------------------
def _extract_frame(video: Path, t: float, out_png: Path) -> Path:
    # Output seek (-ss AFTER -i) is frame-accurate — important for short slots,
    # where input-seek could grab a frame from the neighbouring clip and make the
    # Vision verify judge the wrong image.
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-i", str(video), "-ss", f"{t:.3f}", "-vframes", "1", str(out_png)],
        capture_output=True, text=True, check=True,
    )
    return out_png


def _verify_slot_vision(frame_png: bytes, words: str, clip: ClipAsset, sacred: bool) -> tuple[bool, str]:
    """Vision check that a frame matches its narration line. Coarse non-sacred
    frames run on the cheap model; SACRED frames (Christ / cross / resurrection)
    escalate to Opus with a strict theological-state prompt — a small model misses
    the 'standing beside the cross vs crucified' class of error (scene-11 lesson)."""
    b64, media = _encode_image_for_vision(frame_png)
    if sacred:
        model = config.MODEL  # Opus for doctrinal fidelity
        role = (
            "You are a STRICT theological-fidelity auditor for a gospel Short. The frame "
            "depicts Christ / the cross / a sacred moment. FAIL if the depicted "
            "theological STATE differs from the words in any way that matters — e.g. "
            "Jesus standing BESIDE the cross when crucifixion is meant; a resurrection "
            "Christ when passion is meant (or vice versa); the wrong figure as the "
            "central subject. 'Close enough' is a FAIL. Do NOT pass on vibes. Return "
            'ONLY JSON: {"passed": true|false, "note": "one short line"}'
        )
    else:
        model = config.VISION_AUDIT_MODEL  # cheap model for coarse match
        role = (
            "You verify that a video frame matches the narration line shown under it in "
            "a 60-second gospel Short. Pass UNLESS the image clearly contradicts or is "
            "irrelevant to the words. Minor literalness is fine (symbolic/echo images "
            "count as matching). Return ONLY JSON:\n"
            '{"passed": true|false, "note": "one short line"}'
        )
    user = (
        f"NARRATION WORDS under this frame:\n\"{words}\"\n\n"
        f"CLIP: \"{clip.title}\" — intended subject: {clip.subject_block[:240]}\n\n"
        "Does the frame match the words? Answer JSON."
    )
    if config.agent_mode():
        from pipeline import agent_bridge
        text = agent_bridge.call_vision(
            role=role, user=user, image_bytes=frame_png, media=media, model=model,
            label=f"slot-verify:{clip.title[:40]}{' [SACRED]' if sacred else ''}",
        )
        d = text_engine._extract_json(text)
        return bool(d.get("passed", False)), str(d.get("note", "")).strip()
    client = text_engine._client()
    resp = client.messages.create(
        model=model, max_tokens=600,
        system=role,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": media, "data": b64}},
            {"type": "text", "text": user},
        ]}],
    )
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    d = text_engine._extract_json(text)
    return bool(d.get("passed", False)), str(d.get("note", "")).strip()


def _section_words(segments: list[NarrationSegment], section: str) -> str:
    for s in segments:
        if s.section == section:
            return s.text
    return ""


def verify_cut(
    plan: EditPlan,
    segments: list[NarrationSegment],
    clips_by_index: dict[int, ClipAsset],
    viral_cut: Path,
    out_dir: Path,
    log=print,
) -> AssemblyAudit:
    """Extract one mid-slot frame per body slot from the rendered cut and ask
    Claude Vision whether it matches the words spoken there. Advisory."""
    from pipeline.assembly_engine import _is_sacred  # local import avoids any cycle

    frames_dir = out_dir / SEGMENTS_SUBDIR / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    verdicts: list[SlotVerdict] = []
    reroll: list[int] = []
    doctrinal_fails: list[int] = []
    for s in plan.body_slots:
        clip = clips_by_index.get(s.scene_index)
        if clip is None:
            continue
        sacred = _is_sacred(clip)
        mid = (s.slot_start_s + s.slot_end_s) / 2
        words = _section_words(segments, s.section)
        png = _extract_frame(viral_cut, mid, frames_dir / f"slot{s.order:02d}.png")
        try:
            passed, note = _verify_slot_vision(png.read_bytes(), words, clip, sacred)
        except Exception as e:
            # FAIL-CLOSED: a skipped audit must flag, never silently pass — most
            # important on sacred frames (a doctrinal contradiction must surface).
            passed, note = False, f"(audit ERROR — flagged for human review: {e})"
        tag = "SACRED " if sacred else ""
        log(f"      [verify {s.order:>2}] {tag}#{s.scene_index:02d} {clip.title[:28]:<28} "
            f"{'PASS' if passed else 'FAIL'} — {note}")
        verdicts.append(SlotVerdict(order=s.order, scene_index=s.scene_index,
                                    section=s.section, words=words[:80], passed=passed, note=note))
        if not passed:
            reroll.append(s.scene_index)
            if sacred:
                doctrinal_fails.append(s.scene_index)
    notes = "All slots matched their words."
    if doctrinal_fails:
        notes = (f"BLOCKING: doctrinal-fidelity FAIL on sacred clip(s) {sorted(doctrinal_fails)} "
                 "— review before publishing (look at the frames yourself).")
    elif reroll:
        notes = f"{len(reroll)} slot(s) flagged for re-plan/re-roll: {sorted(reroll)}."
    return AssemblyAudit(
        passed_overall=not reroll,
        slots=verdicts,
        reroll_scene_indices=reroll,
        notes=notes,
    )
