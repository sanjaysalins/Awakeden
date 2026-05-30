"""Build the narration timeline ("jigsaw board") and load the rendered clips.

The timeline is derived from the per-turn audio in <v1>/_turns (the __atempo
variants are the final-length renders that went into narration.mp3), NOT from
narration.meta.json's `final_seconds` field — that field is scrambled in the
prodigal run (lists Jesus' 13.3s quote as 0.4s) and must not be trusted.

Pre-quote pauses are re-inserted before each quote turn exactly as per_turn_synth
does, so the absolute windows match the muxed MP3 to within a few ms.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import config
from pipeline.assembly_ffmpeg import ffprobe_duration
from pipeline.assembly_models import ClipAsset, NarrationSegment
from pipeline.visual_models import ScenePlan


_TURN_RE = re.compile(r"^(\d+)_([a-zA-Z]+)(__atempo)?\.mp3$")
_SPEAKER_RE = re.compile(r'<speaker name="([^"]+)">(.*?)</speaker>', re.DOTALL)
_BRACKET_TAG_RE = re.compile(r"\[[^\]]*\]")


# --------------------------------------------------------------------------
# Timeline
# --------------------------------------------------------------------------
def _collect_turn_files(turns_dir: Path) -> list[tuple[int, str, Path]]:
    """Return [(index, speaker, audio_path)] ordered by index. Prefers the
    __atempo variant (the final-length render) when both exist."""
    by_index: dict[int, dict[str, Path]] = {}
    for f in turns_dir.iterdir():
        m = _TURN_RE.match(f.name)
        if not m:
            continue
        idx = int(m.group(1))
        speaker = m.group(2).lower()
        is_atempo = bool(m.group(3))
        slot = by_index.setdefault(idx, {})
        slot["speaker"] = speaker  # same for both variants
        slot["atempo" if is_atempo else "plain"] = f
    out: list[tuple[int, str, Path]] = []
    for idx in sorted(by_index):
        slot = by_index[idx]
        path = slot.get("atempo") or slot.get("plain")
        if path is None:
            continue
        out.append((idx, slot["speaker"], path))
    return out


def _parse_tagged_chunks(tagged_md: Path) -> list[tuple[str, str]]:
    """Parse narration-tagged.md into ordered (speaker, text) chunks. Narrator
    text is everything outside <speaker> tags, with [emotion] tags stripped."""
    raw = tagged_md.read_text(encoding="utf-8")
    lines = [
        ln for ln in raw.splitlines()
        if ln.strip() and not ln.strip().startswith("<!--")
    ]
    full = " ".join(lines)
    full = _BRACKET_TAG_RE.sub(" ", full)
    chunks: list[tuple[str, str]] = []
    pos = 0
    for m in _SPEAKER_RE.finditer(full):
        pre = full[pos:m.start()].strip()
        if pre:
            chunks.append(("narrator", _norm_ws(pre)))
        chunks.append((m.group(1).strip().lower(), _norm_ws(m.group(2))))
        pos = m.end()
    tail = full[pos:].strip()
    if tail:
        chunks.append(("narrator", _norm_ws(tail)))
    return chunks


def _norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _section_label(index: int, speaker: str, first_narr: int, last_narr: int) -> str:
    if speaker != "narrator":
        return "quote" if speaker == "jesus" else speaker
    if index == first_narr:
        return "hook"
    if index == last_narr:
        return "landing"
    return "bridge"


def build_timeline(v1_folder: Path, log=print) -> list[NarrationSegment]:
    """Reconstruct the absolute narration timeline from the per-turn audio."""
    turns_dir = v1_folder / "_turns"
    if not turns_dir.exists():
        raise SystemExit(f"No _turns folder at {turns_dir} — run the audio stage first.")
    tagged = v1_folder / "narration-tagged.md"
    if not tagged.exists():
        raise SystemExit(f"No narration-tagged.md at {tagged}.")

    turns = _collect_turn_files(turns_dir)
    chunks = _parse_tagged_chunks(tagged)
    if len(chunks) != len(turns):
        log(f"      ! tagged chunks ({len(chunks)}) != turn files ({len(turns)}); "
            "aligning by speaker where possible.")
    texts = _align_text(turns, chunks)

    pre_quote_pause = _pre_quote_pause(v1_folder)

    narrator_idxs = [idx for idx, sp, _ in turns if sp == "narrator"]
    first_narr = narrator_idxs[0] if narrator_idxs else -1
    last_narr = narrator_idxs[-1] if narrator_idxs else -1

    segments: list[NarrationSegment] = []
    t = 0.0
    for i, (idx, speaker, path) in enumerate(turns):
        is_quote = speaker != "narrator"
        if is_quote:
            t += pre_quote_pause  # silence gap before a quoted line
        start = t
        dur = ffprobe_duration(path)
        t += dur
        end = t
        segments.append(NarrationSegment(
            index=idx,
            section=_section_label(idx, speaker, first_narr, last_narr),
            speaker=speaker,
            text=texts[i] if i < len(texts) else "",
            start_s=round(start, 3),
            end_s=round(end, 3),
        ))

    # Reconcile the reconstructed total against the ACTUAL muxed MP3 — the
    # per-turn sum + heuristic pauses can drift a few ms/frames from the real
    # narration.mp3 the cut is laid against. Pin the last segment's end to it.
    mp3 = v1_folder / "narration.mp3"
    if segments and mp3.exists():
        try:
            real = ffprobe_duration(mp3)
            if abs(real - segments[-1].end_s) > 0.05:
                log(f"      (timeline total {segments[-1].end_s:.3f}s -> pinned to "
                    f"narration.mp3 {real:.3f}s)")
                segments[-1].end_s = round(real, 3)
        except Exception:
            pass
    return segments


def _align_text(turns: list[tuple[int, str, Path]], chunks: list[tuple[str, str]]) -> list[str]:
    """Map tagged-narration chunks onto the ordered turn files by SPEAKER sequence
    (not blind position), so narrator asides between two quotes don't shift every
    text onto the wrong audio window. Falls back to next-unused on no match."""
    pool = list(chunks)
    used = [False] * len(pool)
    out: list[str] = []
    for _idx, speaker, _path in turns:
        j = next((k for k, (sp, _t) in enumerate(pool) if not used[k] and sp == speaker), None)
        if j is None:
            j = next((k for k in range(len(pool)) if not used[k]), None)
        if j is None:
            out.append("")
        else:
            used[j] = True
            out.append(pool[j][1])
    return out


def _pre_quote_pause(v1_folder: Path) -> float:
    meta = v1_folder / "narration.meta.json"
    if meta.exists():
        try:
            d = json.loads(meta.read_text(encoding="utf-8"))
            v = d.get("pre_quote_pause_seconds")
            if v is not None:
                return float(v)
        except Exception:
            pass
    return config.SHORTS_PRE_QUOTE_PAUSE


def total_seconds(segments: list[NarrationSegment]) -> float:
    return max((s.end_s for s in segments), default=0.0)


# --------------------------------------------------------------------------
# Clip assets
# --------------------------------------------------------------------------
def load_clips(
    v1_folder: Path, provider: str, exclude: set[int] | None = None, log=print
) -> list[ClipAsset]:
    """Load every rendered clip for `provider` from scene_plan.json + ffprobe.
    Skips scenes whose .mp4 is missing (warns) and any scene index in `exclude`
    (the user-marked glitchy/hallucinated clips — never enter the cut)."""
    exclude = exclude or set()
    plan_path = v1_folder / "visual" / "scene_plan.json"
    if not plan_path.exists():
        raise SystemExit(f"No scene_plan.json at {plan_path} — run the visual stage first.")
    plan_doc = json.loads(plan_path.read_text(encoding="utf-8"))
    plan = ScenePlan.from_json(plan_doc.get("plan", {}))
    short_set = set(plan.short_priority)
    render_dir = v1_folder / "visual" / provider

    clips: list[ClipAsset] = []
    for scene in plan.scenes:
        if scene.index in exclude:
            log(f"      [exclude] scene {scene.index} ({scene.title}) — user-rejected; skipping")
            continue
        stem = scene.filename_stem
        mp4 = render_dir / f"{stem}.mp4"
        png = render_dir / f"{stem}.png"
        if not mp4.exists():
            log(f"      ! scene {scene.index} ({scene.title}) has no .mp4 at {mp4.name}; skipping")
            continue
        clips.append(ClipAsset(
            scene_index=scene.index,
            title=scene.title,
            slug=scene.slug,
            mp4_path=str(mp4),
            png_path=str(png),
            natural_duration_s=round(ffprobe_duration(mp4), 3),
            scene_type=scene.scene_type,
            framing=scene.framing,
            arc_position=scene.arc_position,
            viral_role=scene.viral_role,
            pacing=scene.pacing,
            jesus_variant=scene.jesus_variant,
            subject_block=scene.subject_block,
            visible_elements=scene.visible_elements,
            emotional_tone=scene.emotional_tone,
            macro_elements=scene.macro_elements,
            short_priority=scene.index in short_set,
        ))
    return sorted(clips, key=lambda c: c.scene_index)


# --------------------------------------------------------------------------
# Debug print
# --------------------------------------------------------------------------
def print_board(segments: list[NarrationSegment], clips: list[ClipAsset], log=print) -> None:
    log("\n=== NARRATION BOARD ===")
    for s in segments:
        log(f"  [{s.section:>8}] {s.start_s:6.2f}-{s.end_s:6.2f}s ({s.duration_s:5.2f}s) "
            f"{s.speaker}: {s.text[:60]}{'...' if len(s.text) > 60 else ''}")
    log(f"  total: {total_seconds(segments):.3f}s")
    log(f"\n=== CLIPS ({len(clips)}) ===")
    for c in clips:
        flag = "*" if c.short_priority else " "
        log(f"  {flag} #{c.scene_index:02d} {c.title[:34]:<34} "
            f"{c.viral_role:<10} {c.pacing:<11} {c.natural_duration_s:5.2f}s")
