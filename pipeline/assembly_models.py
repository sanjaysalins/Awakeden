"""Data structures for the assembly stage: the narration timeline, the clip
assets, and the edit plan that fits clips to words.

Mirrors the lightweight-dataclass discipline of pipeline/visual_models.py.
GateResult and AgentVerdict are reused from there so the review/report writers
treat every stage uniformly.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from pipeline.visual_models import AgentVerdict, GateResult  # reused as-is


# --------------------------------------------------------------------------
# The narration timeline ("jigsaw board")
# --------------------------------------------------------------------------
@dataclass
class NarrationSegment:
    """One spoken section of the narration, with its absolute time window on
    the final 0..total timeline. Built by assembly_timing.build_timeline from
    the per-turn audio (NOT from narration.meta.json's scrambled final_seconds).
    """
    index: int                 # 0-based turn order
    section: str               # "hook" | "quote" | "bridge" | "son" | "landing" | <speaker>
    speaker: str               # narrator | jesus | son | ...
    text: str                  # the words spoken in this section
    start_s: float             # absolute start on the final timeline
    end_s: float               # absolute end (next section begins after any pause)

    @property
    def duration_s(self) -> float:
        return max(0.0, self.end_s - self.start_s)

    @classmethod
    def from_json(cls, d: dict) -> "NarrationSegment":
        return cls(
            index=int(d.get("index", 0) or 0),
            section=str(d.get("section", "")).strip().lower(),
            speaker=str(d.get("speaker", "")).strip().lower(),
            text=str(d.get("text", "")).strip(),
            start_s=float(d.get("start_s", 0.0) or 0.0),
            end_s=float(d.get("end_s", 0.0) or 0.0),
        )


# --------------------------------------------------------------------------
# A phrase/beat — the fine-grained unit a clip is pinned to (Rule 3)
# --------------------------------------------------------------------------
@dataclass
class Phrase:
    """One spoken phrase/clause with REAL per-word start/end times (from forced
    alignment), the matching unit for beat-accurate clip placement. A clip is
    pinned to the phrase it depicts so the image sits under the exact words."""
    index: int                 # 0-based order along the timeline
    section: str               # the narration section this phrase belongs to
    speaker: str               # narrator | jesus | ...
    text: str                  # the spoken words of this phrase
    start_s: float             # absolute start on the final timeline (first word)
    end_s: float               # absolute end (last word)

    @property
    def duration_s(self) -> float:
        return max(0.0, self.end_s - self.start_s)

    @property
    def word_count(self) -> int:
        return len(self.text.split())

    @classmethod
    def from_json(cls, d: dict) -> "Phrase":
        return cls(
            index=int(d.get("index", 0) or 0),
            section=str(d.get("section", "")).strip().lower(),
            speaker=str(d.get("speaker", "")).strip().lower(),
            text=str(d.get("text", "")).strip(),
            start_s=float(d.get("start_s", 0.0) or 0.0),
            end_s=float(d.get("end_s", 0.0) or 0.0),
        )


# --------------------------------------------------------------------------
# A rendered clip the planner can place
# --------------------------------------------------------------------------
@dataclass
class ClipAsset:
    """A rendered Kling clip + the scene metadata the matcher reasons over.
    Loaded from scene_plan.json + ffprobe of the .mp4 (natural_duration_s)."""
    scene_index: int
    title: str
    slug: str
    mp4_path: str
    png_path: str
    natural_duration_s: float
    scene_type: str
    framing: str
    arc_position: str
    viral_role: str
    pacing: str
    jesus_variant: str | None
    subject_block: str
    visible_elements: str
    emotional_tone: str
    macro_elements: list[str] = field(default_factory=list)
    short_priority: bool = False

    @classmethod
    def from_json(cls, d: dict) -> "ClipAsset":
        macro = [str(m).strip() for m in (d.get("macro_elements", []) or []) if str(m).strip()]
        jv = d.get("jesus_variant")
        return cls(
            scene_index=int(d.get("scene_index", 0) or 0),
            title=str(d.get("title", "")).strip(),
            slug=str(d.get("slug", "")).strip(),
            mp4_path=str(d.get("mp4_path", "")).strip(),
            png_path=str(d.get("png_path", "")).strip(),
            natural_duration_s=float(d.get("natural_duration_s", 0.0) or 0.0),
            scene_type=str(d.get("scene_type", "")).strip().lower(),
            framing=str(d.get("framing", "")).strip().lower(),
            arc_position=str(d.get("arc_position", "")).strip().lower(),
            viral_role=str(d.get("viral_role", "")).strip().lower(),
            pacing=str(d.get("pacing", "controlled")).strip().lower() or "controlled",
            jesus_variant=(str(jv).strip().lower() if jv not in (None, "", "null", "none") else None),
            subject_block=str(d.get("subject_block", "")).strip(),
            visible_elements=str(d.get("visible_elements", "")).strip(),
            emotional_tone=str(d.get("emotional_tone", "")).strip(),
            macro_elements=macro,
            short_priority=bool(d.get("short_priority", False)),
        )


# --------------------------------------------------------------------------
# An edit slot — one clip occupying one window on the final timeline
# --------------------------------------------------------------------------
@dataclass
class EditSlot:
    """One placement: scene `scene_index` plays from source [source_in_s,
    source_out_s] at `speed_factor`, occupying [slot_start_s, slot_end_s] on
    the final timeline. `role` distinguishes the hero bookend from body clips."""
    order: int                 # position in the final concat (0..N-1)
    role: str                  # "hero-head" | "body" | "hero-tail"
    scene_index: int
    section: str               # which narration section this slot sits under
    slot_start_s: float
    slot_end_s: float
    source_in_s: float
    source_out_s: float
    speed_factor: float
    op: str                    # "speed" | "speed+trim"
    rationale: str = ""
    beat_index: int = -1       # which phrase/beat this clip is pinned to (-1 = hero/none)
    beat_phrase: str = ""      # the exact spoken words this clip plays under (Rule 3)

    @property
    def slot_duration_s(self) -> float:
        return max(0.0, self.slot_end_s - self.slot_start_s)

    @property
    def source_span_s(self) -> float:
        return max(0.0, self.source_out_s - self.source_in_s)

    @classmethod
    def from_json(cls, d: dict) -> "EditSlot":
        return cls(
            order=int(d.get("order", 0) or 0),
            role=str(d.get("role", "body")).strip().lower() or "body",
            scene_index=int(d.get("scene_index", 0) or 0),
            section=str(d.get("section", "")).strip().lower(),
            slot_start_s=float(d.get("slot_start_s", 0.0) or 0.0),
            slot_end_s=float(d.get("slot_end_s", 0.0) or 0.0),
            source_in_s=float(d.get("source_in_s", 0.0) or 0.0),
            source_out_s=float(d.get("source_out_s", 0.0) or 0.0),
            speed_factor=float(d.get("speed_factor", 1.0) or 1.0),
            op=str(d.get("op", "speed")).strip().lower() or "speed",
            rationale=str(d.get("rationale", "")).strip(),
            beat_index=int(d.get("beat_index", -1) if d.get("beat_index") is not None else -1),
            beat_phrase=str(d.get("beat_phrase", "")).strip(),
        )


# --------------------------------------------------------------------------
# The full edit plan
# --------------------------------------------------------------------------
@dataclass
class EditPlan:
    """The semantic jigsaw (from the LLM) + the computed slots (from the
    deterministic allocator). `slots` is the source of truth for rendering."""
    narration_reading: str                                  # how clips map to words
    red_team_notes: str                                     # writer's own doubts
    hero_scene_index: int
    hero_head_s: float
    hero_tail_s: float
    total_seconds: float
    clip_budget: int
    selected_scene_indices: list[int] = field(default_factory=list)        # body clips, arc order
    section_assignment: dict[str, list[int]] = field(default_factory=dict)  # section -> [scene_index] ordered
    slots: list[EditSlot] = field(default_factory=list)
    notes: str = ""

    @property
    def body_slots(self) -> list[EditSlot]:
        return [s for s in self.slots if s.role == "body"]

    def slot_by_order(self, order: int) -> EditSlot | None:
        for s in self.slots:
            if s.order == order:
                return s
        return None

    @classmethod
    def from_json(cls, d: dict) -> "EditPlan":
        sa_raw = d.get("section_assignment", {}) or {}
        section_assignment: dict[str, list[int]] = {}
        for k, v in sa_raw.items():
            try:
                section_assignment[str(k).strip().lower()] = [int(x) for x in (v or [])]
            except (TypeError, ValueError):
                section_assignment[str(k).strip().lower()] = []
        try:
            selected = [int(x) for x in (d.get("selected_scene_indices", []) or [])]
        except (TypeError, ValueError):
            selected = []
        return cls(
            narration_reading=str(d.get("narration_reading", "")).strip(),
            red_team_notes=str(d.get("red_team_notes", "")).strip(),
            hero_scene_index=int(d.get("hero_scene_index", 0) or 0),
            hero_head_s=float(d.get("hero_head_s", 0.0) or 0.0),
            hero_tail_s=float(d.get("hero_tail_s", 0.0) or 0.0),
            total_seconds=float(d.get("total_seconds", 0.0) or 0.0),
            clip_budget=int(d.get("clip_budget", 0) or 0),
            selected_scene_indices=selected,
            section_assignment=section_assignment,
            slots=[EditSlot.from_json(s) for s in (d.get("slots", []) or [])],
            notes=str(d.get("notes", "")).strip(),
        )


# --------------------------------------------------------------------------
# Review of the edit plan (mirrors ScenePlanReview shape)
# --------------------------------------------------------------------------
@dataclass
class EditPlanReview:
    panel: list[AgentVerdict]
    gates: list[GateResult]
    overall: str                  # LOCKED | REVISE | REWORK
    priority_fixes: list[str] = field(default_factory=list)

    @property
    def failed_gates(self) -> list[GateResult]:
        return [g for g in self.gates if g.verdict.upper().strip() == "FAIL"]

    @property
    def is_acceptable(self) -> bool:
        return len(self.failed_gates) == 0

    @property
    def is_locked(self) -> bool:
        return self.overall.upper().strip() == "LOCKED"

    @classmethod
    def from_json(cls, d: dict) -> "EditPlanReview":
        panel = [
            AgentVerdict(
                agent=str(p.get("agent", "")).strip(),
                verdict=str(p.get("verdict", "")).strip(),
                note=str(p.get("note", "")).strip(),
            )
            for p in (d.get("panel", []) or [])
        ]
        gates = [
            GateResult(
                gate=str(g.get("gate", "")).strip(),
                verdict=str(g.get("verdict", "")).strip(),
                evidence=str(g.get("evidence", "")).strip(),
                fix=str(g.get("fix", "")).strip(),
            )
            for g in (d.get("gates", []) or [])
        ]
        return cls(
            panel=panel,
            gates=gates,
            overall=str(d.get("overall", "")).strip(),
            priority_fixes=[
                str(x).strip() for x in (d.get("priority_fixes", []) or []) if str(x).strip()
            ],
        )


# --------------------------------------------------------------------------
# Per-slot Vision verification of the rendered cut
# --------------------------------------------------------------------------
@dataclass
class SlotVerdict:
    order: int
    scene_index: int
    section: str
    words: str
    passed: bool
    note: str = ""

    @classmethod
    def from_json(cls, d: dict) -> "SlotVerdict":
        return cls(
            order=int(d.get("order", 0) or 0),
            scene_index=int(d.get("scene_index", 0) or 0),
            section=str(d.get("section", "")).strip().lower(),
            words=str(d.get("words", "")).strip(),
            passed=bool(d.get("passed", False)),
            note=str(d.get("note", "")).strip(),
        )


@dataclass
class AssemblyAudit:
    """Advisory per-slot Vision check: does each clip match the words spoken
    during its window? Produces a re-plan/re-roll list; never blocks render."""
    passed_overall: bool
    slots: list[SlotVerdict] = field(default_factory=list)
    reroll_scene_indices: list[int] = field(default_factory=list)
    notes: str = ""

    @classmethod
    def from_json(cls, d: dict) -> "AssemblyAudit":
        try:
            reroll = [int(x) for x in (d.get("reroll_scene_indices", []) or [])]
        except (TypeError, ValueError):
            reroll = []
        return cls(
            passed_overall=bool(d.get("passed_overall", False)),
            slots=[SlotVerdict.from_json(s) for s in (d.get("slots", []) or [])],
            reroll_scene_indices=reroll,
            notes=str(d.get("notes", "")).strip(),
        )
