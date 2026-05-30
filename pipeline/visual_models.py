"""Data structures for the visual stage: scenes, scene plans, audits.

Mirrors the lightweight-dataclass discipline of pipeline/models.py. Top-level
fields on ScenePlan are derived from the chosen scenes / candidates, kept for
ergonomic downstream access.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal


SCENE_TYPES = ("single", "unified")
FRAMINGS = ("wide", "mid", "close", "overhead", "low-angle")
JESUS_VARIANTS = ("ministry", "passion", "resurrection", "infant")
PACING_MODES = ("controlled", "slower", "faster")              # per SKILL_locked.md
VIRAL_ROLES = ("hook-open", "build", "pivot", "climax", "close")


def slugify(s: str) -> str:
    """Filesystem-safe lowercase-kebab slug. Mirrors match_images.py:46-50 so
    the downstream image_to_kling pipeline reads our filenames cleanly."""
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s-]+", "-", s).strip("-")
    return s or "scene"


@dataclass
class SceneCandidate:
    """A proposed scene before final selection. Pinned to an arc position and
    a framing so SP-G3 (variety) and SP-G8 (composition distribution) can be
    checked structurally, not just by vibe."""
    title: str
    scene_type: str          # "single" | "unified"
    arc_position: str        # opening-hook | biblical-setting | confrontation | revelation | response (+ extras)
    framing: str             # "wide" | "mid" | "close" | "overhead" | "low-angle"
    purpose: str             # what role this scene plays in the narration arc
    rationale: str           # why this scene over the obvious topic auto-complete
    visible_elements: str    # what must be visible in the rendered image (used by SP-G1 + image audit)
    emotional_tone: str      # one-line tone — feeds the mood_block

    @classmethod
    def from_json(cls, d: dict) -> "SceneCandidate":
        return cls(
            title=str(d.get("title", "")).strip(),
            scene_type=str(d.get("scene_type", "single")).strip().lower(),
            arc_position=str(d.get("arc_position", "")).strip().lower(),
            framing=str(d.get("framing", "mid")).strip().lower(),
            purpose=str(d.get("purpose", "")).strip(),
            rationale=str(d.get("rationale", "")).strip(),
            visible_elements=str(d.get("visible_elements", "")).strip(),
            emotional_tone=str(d.get("emotional_tone", "")).strip(),
        )


@dataclass
class Scene:
    """A chosen scene with the per-scene prose blocks the renderer will
    concatenate around VISUAL_STYLE_BASE / VISUAL_STYLE_TAIL. The model does
    NOT return the style base — it returns only `subject_block` + `mood_block`,
    so SP-G5 conformance is a regex on those two fields only.

    `macro_elements`, `pacing`, and `viral_role` are KLING-STAGE metadata —
    they do not enter the NBP/HF prompt. They are written as a sidecar so the
    downstream image_to_kling.py cut planner has anchors and pacing hints."""
    index: int
    slug: str
    title: str
    scene_type: str
    arc_position: str
    framing: str
    purpose: str
    rationale: str
    visible_elements: str
    emotional_tone: str
    subject_block: str       # per-scene prose between STYLE_BASE and STYLE_TAIL
    mood_block: str          # one-line emotional tone for the prompt
    jesus_variant: str | None = None   # "ministry" | "passion" | "resurrection" | "infant" | None
    priority: int = 0        # short-priority rank; 0 = not on the short list
    macro_elements: list[str] = field(default_factory=list)     # 3-5 cut-anchor details for Kling
    pacing: str = "controlled"                                  # SKILL_locked.md pacing mode
    viral_role: str = ""                                        # hook-open / build / pivot / climax / close
    shot_kind: str = "standard"                                 # standard | hero (gospel-pivot, bookends the cut, designed iconic/near-still) | insert (a ~2s single-macro shot for a tiny narration beat)
    vignettes: list[str] = field(default_factory=list)          # for scene_type=unified: 3-5 named background vignettes (e.g. "the running father", "the kiss on the neck", "the swine pen"). Each is a memory/echo that fades into shadow; the renderer interpolates them as "subtle background vignettes fading into shadow suggesting <comma-joined>"

    @property
    def filename_stem(self) -> str:
        """`01_<slug>` — deterministic, idempotent. Matches the convention
        the downstream match_images.py / image_to_kling.py expect."""
        return f"{self.index:02d}_{self.slug}"

    @classmethod
    def from_json(cls, d: dict, index: int) -> "Scene":
        title = str(d.get("title", "")).strip()
        macro_raw = d.get("macro_elements") or []
        macro_elements = [str(m).strip() for m in macro_raw if str(m).strip()]
        vignettes_raw = d.get("vignettes") or []
        vignettes = [str(v).strip() for v in vignettes_raw if str(v).strip()]
        return cls(
            index=index,
            slug=str(d.get("slug", "")).strip() or slugify(title),
            title=title,
            scene_type=str(d.get("scene_type", "single")).strip().lower(),
            arc_position=str(d.get("arc_position", "")).strip().lower(),
            framing=str(d.get("framing", "mid")).strip().lower(),
            purpose=str(d.get("purpose", "")).strip(),
            rationale=str(d.get("rationale", "")).strip(),
            visible_elements=str(d.get("visible_elements", "")).strip(),
            emotional_tone=str(d.get("emotional_tone", "")).strip(),
            subject_block=str(d.get("subject_block", "")).strip(),
            mood_block=str(d.get("mood_block", "")).strip(),
            jesus_variant=(
                str(d.get("jesus_variant")).strip().lower()
                if d.get("jesus_variant") not in (None, "", "null", "none")
                else None
            ),
            priority=int(d.get("priority", 0) or 0),
            macro_elements=macro_elements,
            pacing=str(d.get("pacing", "controlled")).strip().lower() or "controlled",
            viral_role=str(d.get("viral_role", "")).strip().lower(),
            shot_kind=str(d.get("shot_kind", "standard")).strip().lower() or "standard",
            vignettes=vignettes,
        )


@dataclass
class ScenePlan:
    """The full scene plan — chosen scenes + the candidates considered +
    deterministic alignment artifacts (beat_coverage) the gates check before
    the LLM judges."""
    visual_reading: str                       # 1-2 paragraph summary of the visual / emotional arc
    red_team_notes: str                       # the model's own red-team of its scene list (pre-panel)
    scenes: list[Scene] = field(default_factory=list)
    short_priority: list[int] = field(default_factory=list)   # ordered scene.index list, 5-8 picks
    candidates: list[SceneCandidate] = field(default_factory=list)
    rationale: str = ""                       # why this scene set vs. the candidates
    beat_coverage: dict[str, list[int]] = field(default_factory=dict)
    # beat_id -> list of scene indices that support that narration beat
    hero_candidate: int = 0                   # scene index of the gospel-pivot hero that bookends the cut (0 = unset; assembly picks the cross/NT-link)

    @property
    def is_empty(self) -> bool:
        return not self.scenes

    def scene_by_index(self, i: int) -> Scene | None:
        for s in self.scenes:
            if s.index == i:
                return s
        return None

    def short_scenes(self) -> list[Scene]:
        """Scenes in short_priority order (only the indices that exist)."""
        out: list[Scene] = []
        for i in self.short_priority:
            s = self.scene_by_index(i)
            if s is not None:
                out.append(s)
        return out

    @classmethod
    def from_json(cls, d: dict) -> "ScenePlan":
        raw_scenes = d.get("scenes", []) or []
        scenes = [
            Scene.from_json(s, index=int(s.get("index", i + 1)))
            for i, s in enumerate(raw_scenes)
            if str(s.get("title", "")).strip()
        ]
        candidates = [
            SceneCandidate.from_json(c)
            for c in (d.get("candidates", []) or [])
            if str(c.get("title", "")).strip()
        ]
        beat_coverage_raw = d.get("beat_coverage", {}) or {}
        beat_coverage: dict[str, list[int]] = {}
        for k, v in beat_coverage_raw.items():
            try:
                beat_coverage[str(k).strip()] = [int(x) for x in (v or [])]
            except (TypeError, ValueError):
                beat_coverage[str(k).strip()] = []
        short_priority_raw = d.get("short_priority", []) or []
        try:
            short_priority = [int(x) for x in short_priority_raw]
        except (TypeError, ValueError):
            short_priority = []
        try:
            hero_candidate = int(d.get("hero_candidate", 0) or 0)
        except (TypeError, ValueError):
            hero_candidate = 0
        return cls(
            visual_reading=str(d.get("visual_reading", "")).strip(),
            red_team_notes=str(d.get("red_team_notes", "")).strip(),
            scenes=scenes,
            short_priority=short_priority,
            candidates=candidates,
            rationale=str(d.get("rationale", "")).strip(),
            beat_coverage=beat_coverage,
            hero_candidate=hero_candidate,
        )


@dataclass
class GateResult:
    """Re-declared here to keep visual_models independent of pipeline/models;
    same shape as pipeline.models.GateResult so the audit-report writer can
    treat both uniformly."""
    gate: str
    verdict: str            # PASS | CONDITIONAL | FAIL
    evidence: str
    fix: str = ""


@dataclass
class AgentVerdict:
    agent: str
    verdict: str            # STRONG | CAUTION | REVISION NEEDED
    note: str


@dataclass
class ScenePlanReview:
    panel: list[AgentVerdict]
    gates: list[GateResult]
    overall: str                  # LOCKED | REVISE | REWORK
    priority_fixes: list[str] = field(default_factory=list)

    @property
    def failed_gates(self) -> list[GateResult]:
        return [g for g in self.gates if g.verdict.upper().strip() == "FAIL"]

    @property
    def is_acceptable(self) -> bool:
        """Publishable when no gate hard-FAILs. CONDITIONAL/CAUTION advisory."""
        return len(self.failed_gates) == 0

    @property
    def is_locked(self) -> bool:
        return self.overall.upper().strip() == "LOCKED"

    @classmethod
    def from_json(cls, d: dict) -> "ScenePlanReview":
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


@dataclass
class ImageAudit:
    """Per-image content audit (Claude Vision vs the Scene's visible_elements
    and banned-token list). Mirrors the shape produced by image_to_kling.py's
    Stage A.5 audit so the report writer can render both."""
    passed: bool
    issues: list[dict] = field(default_factory=list)         # [{"claim": str, "actual": str}, ...]
    banned_token_hits: list[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, d: dict) -> "ImageAudit":
        issues = [
            {"claim": str(i.get("claim", "")).strip(), "actual": str(i.get("actual", "")).strip()}
            for i in (d.get("issues", []) or [])
            if i
        ]
        return cls(
            passed=bool(d.get("passed", False)),
            issues=issues,
            banned_token_hits=[str(t).strip() for t in (d.get("banned_token_hits", []) or [])],
        )


@dataclass
class CohesionAudit:
    """Paper or rendered cohesion. Advisory for rendered (FAIL produces a
    re-roll list, doesn't abort); blocking for paper (FAIL blocks rendering)."""
    scope: str                                # "paper" | "rendered"
    passed: bool
    notes: str = ""
    conflict_scenes: list[int] = field(default_factory=list)

    @classmethod
    def from_json(cls, d: dict) -> "CohesionAudit":
        scope = str(d.get("scope", "")).strip().lower() or "paper"
        try:
            conflict_scenes = [int(x) for x in (d.get("conflict_scenes", []) or [])]
        except (TypeError, ValueError):
            conflict_scenes = []
        return cls(
            scope=scope,
            passed=bool(d.get("passed", False)),
            notes=str(d.get("notes", "")).strip(),
            conflict_scenes=conflict_scenes,
        )
