"""Deterministic validators for the validation engine (see VALIDATION_ENGINE_PLAN.md).

These are PURE-CODE checks that run every change ($0, no LLM) and lock in the fixes
from the 2026-06-14 session of misses:
  - CLIP-VIRAL          : a Kling cut-plan must use the viral crop-cut sequence, NOT a slow zoom.
  - CLIP-IMAGE-GROUNDED : a cut-plan must not inject the scene's rich subject_block nouns
                          (blood / lamplight / first-light / pen) that made Kling hallucinate.
  - prompt_has_criteria : verify_image's audit prompt must still carry the period/tone + text + anatomy checks.
  - rules_integrity     : data/rules.json is well-formed and its memories/fixtures exist.

Vision-based rules (IMG-*, CLIP-FROZEN, CLIP-NOMORPH) are NOT unit-tested here (non-deterministic);
they are exercised by the on-demand vision calibration runner (validate_fixtures.py).
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = ROOT / "data" / "rules.json"
MEMORY_DIR = Path(r"C:\Users\sanjay\.claude\projects\C--Users-sanjay-PycharmProjects-JesusInTheBible\memory")


# ---------------------------------------------------------------- rules registry

def load_rules() -> list[dict]:
    data = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    return data["rules"]


# ---------------------------------------------------------------- cut-plan shape

# Signatures of the OLD rich-text / hallucination-seeding cut-plan prompt. These are
# UNIQUE to the original build_cutplan (which injected the subject_block + a flame line);
# they are NOT present in the clean v2 camera-only plan, nor in the harmless boilerplate
# ("Scene contains: the scene is a painted tableau ... nothing moves") that image_to_kling
# appends to EVERY clip — so we must not flag a bare "Scene contains:".
_RICHTEXT_MARKERS = ("micro-motion", "flame stirs", "oil painting video clip",
                     "classical devotional oil painting realism")
# Phrases that prove the prompt forbids invented content (the anti-hallucination clause).
_FROZEN_MARKERS = ("nothing inside the painting", "frozen", "only the camera",
                   "fixed photograph", "static")
# A single-slow-zoom (the over-correction regression) reads like this.
_SLOWZOOM_MARKERS = ("one single", "single, very slow", "single slow", "slowly zooms in")


def _beats(kling_json: dict) -> list[dict]:
    return kling_json.get("beats", []) or []


def cutplan_viral(kling_json: dict) -> tuple[bool, str]:
    """CLIP-VIRAL: must be a crop-cut sequence (>=6 beats), not a 1-2 beat slow zoom."""
    beats = _beats(kling_json)
    prompt = (kling_json.get("prompt") or "").lower()
    if any(m in prompt for m in _SLOWZOOM_MARKERS) and len(beats) <= 3:
        return False, f"slow-zoom cut-plan ({len(beats)} beats, single push-in) — not a viral crop-cut edit"
    if len(beats) < 6:
        return False, f"only {len(beats)} beats — viral edit needs >=6 crop-cuts (full->mid->close->macro->return)"
    # at least a few distinct framings present in the beat descriptions
    descs = " ".join((b.get("description") or "").lower() for b in beats)
    framings = sum(1 for w in ("full", "mid", "close", "macro", "insert", "detail") if w in descs)
    if framings < 3:
        return False, f"beats lack framing variety (only {framings} framing words) — reads as a static hold"
    return True, f"viral crop-cut sequence ({len(beats)} beats, {framings} framings)"


def gate_cutplan(kling_json: dict) -> tuple[bool, list[str]]:
    """Submit-gate: a cut-plan may only be used if it is BOTH viral (crop-cuts) AND
    image-grounded (no rich-text injection). Deterministic, $0, fail-closed. Wire this
    in wherever a .kling.json is authored, BEFORE it reaches Kling."""
    problems: list[str] = []
    ok_v, r_v = cutplan_viral(kling_json)
    if not ok_v:
        problems.append(f"CLIP-VIRAL: {r_v}")
    ok_g, r_g = cutplan_image_grounded(kling_json)
    if not ok_g:
        problems.append(f"CLIP-IMAGE-GROUNDED: {r_g}")
    return (not problems), problems


def cutplan_image_grounded(kling_json: dict) -> tuple[bool, str]:
    """CLIP-IMAGE-GROUNDED: prompt must NOT inject rich scene-text nouns, and MUST carry
    the anti-invention clause. This is the deterministic discriminator between the old
    text-seeded plan (hallucinated blood/lava/writing) and the clean camera-only plan."""
    prompt = (kling_json.get("prompt") or "").lower()
    hits = [m for m in _RICHTEXT_MARKERS if m in prompt]
    if hits:
        return False, f"prompt injects rich scene text ({', '.join(hits)}) — seeds Kling hallucination"
    if not any(m in prompt for m in _FROZEN_MARKERS):
        return False, "prompt lacks the anti-invention clause (frozen / only the camera / nothing moves)"
    return True, "camera-only, image-grounded (no rich-text injection, anti-invention clause present)"


# ---------------------------------------------------------------- prompt criteria guard

def prompt_has_criteria() -> tuple[bool, str]:
    """The verify_image audit prompt must still contain the period/tone, text, and anatomy
    checks. Guards against accidental removal (the period/tone check was added 2026-06-14)."""
    src = (ROOT / "pipeline" / "visual_render.py").read_text(encoding="utf-8").lower()
    required = {
        "period authenticity": "period authenticity",
        "horror tone": "horror",
        "nsfw": "nsfw",
        "modern faces": "modern",
        "anatomy": "finger",
        "banned tokens": "banned",
    }
    missing = [name for name, needle in required.items() if needle not in src]
    if missing:
        return False, f"verify_image prompt missing checks: {', '.join(missing)}"
    return True, "verify_image carries period/tone + text + anatomy checks"


# ---------------------------------------------------------------- banned tokens

def banned_tokens(text: str) -> list[str]:
    """Return any banned visible-token strings present in text (reuses config list)."""
    from . import config as _cfg  # noqa
    toks = getattr(_cfg, "VISUAL_BANNED_TOKENS", set())
    low = (text or "").lower()
    return sorted(t for t in toks if t.lower() in low)


# ---------------------------------------------------------------- registry integrity

def rules_integrity() -> tuple[bool, list[str]]:
    """Every rule well-formed; validator + memory present; referenced fixtures exist in the
    manifest; referenced memory files exist on disk."""
    problems: list[str] = []
    rules = load_rules()
    ids = set()
    man_path = ROOT / "pipeline" / "validation_fixtures" / "manifest.json"
    manifest = {}
    if man_path.exists():
        manifest = json.loads(man_path.read_text(encoding="utf-8")).get("fixtures", {})
    for r in rules:
        rid = r.get("id", "<no-id>")
        if rid in ids:
            problems.append(f"{rid}: duplicate id")
        ids.add(rid)
        for key in ("id", "scope", "title", "description", "severity", "check", "validator", "memory"):
            if not r.get(key):
                problems.append(f"{rid}: missing/empty '{key}'")
        if r.get("scope") not in ("still", "clip", "cut", "text", "audio"):
            problems.append(f"{rid}: bad scope '{r.get('scope')}'")
        if r.get("severity") not in ("fail", "warn"):
            problems.append(f"{rid}: bad severity '{r.get('severity')}'")
        if r.get("check") not in ("deterministic", "vision"):
            problems.append(f"{rid}: bad check '{r.get('check')}'")
        mem = r.get("memory", "")
        if mem and not (MEMORY_DIR / f"{mem}.md").exists():
            problems.append(f"{rid}: memory '{mem}.md' not found")
        for fx in r.get("fixtures", []):
            if manifest and fx not in manifest:
                problems.append(f"{rid}: fixture '{fx}' not in manifest")
    return (not problems), problems
