"""swirls_verify.py -- the $0-first verification layer for Swirls of Life.

Zero automated verification existed anywhere in this flow before this file
-- 100% human eyeballing. Ordered: V0 prompt/spec lints ($0, before any
render spend) -> render -> V1 freeze-hold budget gate ($0, before animate
spend) -> V2 image content audit (one Vision call per still/cover, mirrors
pipeline/visual_render.py's proven _vision_call/verify_image pattern) -> V3
assembly checks ($0, inside swirls_assemble.assemble()).

Every check returns (or is built from) pipeline.models.GateResult --
gate/verdict/evidence/fix -- the same shape the main engine's SP-G*/AS-G*
deterministic gates use, run BEFORE any LLM/human judgment.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent / "test_the_cross"))

import config  # noqa: E402
from pipeline.models import GateResult  # noqa: E402
from pipeline.visual_models import ImageAudit  # noqa: E402
from swirls_cover import CoverSpec, COOL_TOKENS, TEXT_LOCK_COVER, WARM_TOKENS, \
    EDGE_TO_EDGE_CLAUSE, assemble_cover_still_prompt  # noqa: E402
from swirls_page import PageSpec, Ref  # noqa: E402

sys.path.insert(0, str(ROOT))
import check_landing_hold  # noqa: E402


# ============================================================ V0: LINTS ===

def sw_l1_cover_lighting_contrast(spec: CoverSpec) -> GateResult:
    """Catches defect #1's exact failure mode: episode 2's cover lighting
    slot asked for 'flat grey sky, no vivid color anywhere' -- zero warm
    tokens. See NORTH_STAR_COVER_PROMPT.md's lighting-contrast law."""
    text = spec.lighting.lower()
    warm = [t for t in WARM_TOKENS if t in text]
    cool = [t for t in COOL_TOKENS if t in text]
    if warm and cool:
        return GateResult("SW-L1", "PASS", f"warm={warm[:1]} cool={cool[:1]}")
    missing = ("warm" if not warm else "") + (" and cool" if not cool else "")
    return GateResult(
        "SW-L1", "FAIL",
        f"lighting slot missing a {missing.strip()} token: {spec.lighting!r}",
        "add at least one warm-family and one cool-family word to CoverSpec.lighting "
        f"(warm examples: {WARM_TOKENS[:4]}; cool examples: {COOL_TOKENS[:4]})",
    )


def sw_l2_cover_text_lock(spec: CoverSpec) -> GateResult:
    """Regression guard on the assembled module output, not the author's
    input -- catches an accidental future edit dropping the text-lock or
    edge-to-edge clause from swirls_cover.py itself."""
    prompt = assemble_cover_still_prompt(spec)
    missing = [c for c in (TEXT_LOCK_COVER, EDGE_TO_EDGE_CLAUSE) if c not in prompt]
    if not missing:
        return GateResult("SW-L2", "PASS", "text-lock + edge-to-edge clause both present")
    return GateResult("SW-L2", "FAIL", f"missing from assembled prompt: {missing}",
                       "swirls_cover.py's constants were edited -- restore them")


def sw_l3_panel_style_consistency(manifest_panel_style: str,
                                   pages: dict[str, PageSpec]) -> GateResult:
    """Catches a page silently drifting from the episode's own declared
    panel_style (an inconsistent declaration). SCOPE, corrected 2026-08-23
    (independent-review catch, codex): this does NOT make defect #3 (the
    wrong template used) structurally impossible on its own -- a manifest
    and every page could all consistently declare "ink_wash" and this gate
    would pass cleanly while still shipping the wrong template. The actual
    defense against THAT is NORTH_STAR_PROMPT.md's stated default (hybrid is
    now standard) plus a human choosing panel_style deliberately when writing
    episode.py; this gate only catches accidental inconsistency between the
    manifest and an individual page after that choice is made."""
    mismatched = [pid for pid, p in pages.items() if p.panel_style != manifest_panel_style]
    if not mismatched:
        return GateResult("SW-L3", "PASS", f"all {len(pages)} pages match "
                           f"panel_style={manifest_panel_style!r}")
    return GateResult(
        "SW-L3", "FAIL",
        f"pages {mismatched} declare a different panel_style than the manifest "
        f"({manifest_panel_style!r})",
        "set each page's panel_style to match MANIFEST.panel_style, or split the episode "
        "manifest if a per-page override is genuinely intended",
    )


def sw_l4_refs_exist(specs: list[PageSpec | CoverSpec]) -> GateResult:
    missing = []
    for spec in specs:
        for r in spec.refs:
            if not Path(r.path).exists():
                missing.append((r.subject, r.path))
    if not missing:
        total = sum(len(s.refs) for s in specs)
        return GateResult("SW-L4", "PASS", f"{total} ref(s) across {len(specs)} spec(s), all exist")
    return GateResult("SW-L4", "FAIL", f"missing ref files: {missing}",
                       "crop the missing ref from its first approved render before spending "
                       "(ref-chaining rule -- a hard stop, not a warning)")


def narration_word_count(episode_dir: Path) -> int | None:
    """Plain whitespace-split count over narration.md. WARN-only source, not
    authoritative -- added 2026-08-23 wiring SW-L5 in for real (independent-
    review catch, codex/cursor: it was specified but never called anywhere).
    A naive split does NOT match this project's own hand-counted totals
    exactly (episode 2: split()=163 vs. the documented 157 -- KJV quote
    punctuation/ellipses get counted differently by whatever convention
    produced 157, which isn't formalized anywhere). Returns None if
    narration.md doesn't exist."""
    path = episode_dir / "narration.md"
    if not path.exists():
        return None
    return len(path.read_text(encoding="utf-8").split())


def sw_l5_word_count_parity(unit_words: list[int], narration_word_count_: int | None,
                             tolerance: int = 8) -> GateResult:
    total = sum(unit_words)
    if narration_word_count_ is None:
        return GateResult("SW-L5", "PASS", "no narration.md found -- skipped")
    gap = abs(total - narration_word_count_)
    if gap == 0:
        return GateResult("SW-L5", "PASS", f"{total} words, matches narration.md's plain split exactly")
    if gap <= tolerance:
        return GateResult(
            "SW-L5", "CONDITIONAL",
            f"unit word counts sum to {total}, narration.md plain-split count is "
            f"{narration_word_count_} (gap={gap}, within the {tolerance}-word tolerance for "
            "quote-punctuation counting differences) -- sanity-check, not authoritative",
        )
    return GateResult(
        "SW-L5", "FAIL",
        f"unit word counts sum to {total}, narration.md plain-split count is "
        f"{narration_word_count_} (gap={gap}, exceeds the {tolerance}-word tolerance)",
        "re-check each Unit's word count against the real narration.md text",
    )


# ================================================ V1: FREEZE-HOLD BUDGET ===
# Applies ONLY to units with mode=="freeze" -- red-team catch, 2026-08-23:
# episode 1's own shipped, human-approved BOOMERANG units run 41-68% static-
# equivalent by the same raw formula (F02 61%, F04 68%, F07 41%, back 55%,
# recomputed from the real files). Boomerang pages are DESIGNED to spend
# most of their slot ping-ponging a short clip -- that is not a defect, and
# applying this gate un-scoped would spuriously FAIL 4 of the north star's
# own approved units.

MAX_FREEZE_STATIC_RATIO = 0.35   # FAIL above this
WARN_FREEZE_STATIC_RATIO = 0.25  # CONDITIONAL above this

# Legal duration sets, confirmed 2026-08-23 via `hf generate cost` dry-runs
# (no metered render spend) -- do not guess these again, re-verify if the
# CLI/model versions change.
_KLING_MIN, _KLING_MAX = 3, 15          # kling3_0 mode=pro sound=off: any INTEGER 3-15
_VEO_DURATIONS = (4, 6, 8)              # veo3_1_lite: ONLY these three values


def _clamp_duration(model_tier: str, required_seconds: float) -> int | None:
    """Smallest legal native duration >= required_seconds, or None if even
    the model's max legal duration can't satisfy the budget."""
    if model_tier == "kling3_0":
        d = max(_KLING_MIN, math.ceil(required_seconds))
        return d if d <= _KLING_MAX else None
    for d in _VEO_DURATIONS:  # veo3_1_lite
        if d >= required_seconds:
            return d
    return None


# Model default durations (what render_animation()/render_cover_animation() use when
# a spec's clip_duration is None) -- needed so the PROJECTED check below still means
# something for a spec that hasn't set clip_duration explicitly.
_MODEL_DEFAULT_DURATION = {"kling3_0": 5, "veo3_1_lite": 4}


def sw_f1_freeze_budget(plan_stats: list[dict], model_tier_by_tag: dict[str, str],
                         clip_duration_by_tag: dict[str, int | None] | None = None) -> list[GateResult]:
    """plan_stats: swirls_assemble.plan_units()'s return value -- each dict
    has tag/mode/words/slot/native (native is None if not rendered yet).

    FIXED 2026-08-23 (independent-review catch, converged on by 3/4 reviewers
    -- cursor, codex, claude): the original version PASSED unconditionally
    when native was None ("not rendered yet, nothing to check"), which meant
    the gate could only ever catch an undersized clip AFTER a bad render
    already existed and cost real money -- exactly the "afterthought, not a
    gate" failure the plan claimed to fix. Now, when no clip exists yet, it
    PROJECTS the ratio using the spec's requested `clip_duration` (or the
    model's default if unset) and evaluates the SAME thresholds against that
    -- so a too-short `clip_duration` fails BEFORE the first paid render,
    not just on a retry."""
    clip_duration_by_tag = clip_duration_by_tag or {}
    results = []
    for stat in plan_stats:
        if stat["mode"] != "freeze":
            continue
        tag = stat["tag"]
        tier = model_tier_by_tag.get(tag, "kling3_0")
        slot = stat["slot"]
        if stat["native"] is not None:
            native, projected = stat["native"], False
        else:
            native = clip_duration_by_tag.get(tag) or _MODEL_DEFAULT_DURATION.get(tier, 5)
            projected = True
        ratio = max(slot - native, 0) / slot if slot > 0 else 0.0
        note = " [PROJECTED from clip_duration -- not rendered yet]" if projected else ""
        evidence = f"static_ratio={ratio:.1%} (slot={slot:.2f}s native={native:.2f}s, model={tier}){note}"
        if ratio > MAX_FREEZE_STATIC_RATIO:
            required = slot * (1 - MAX_FREEZE_STATIC_RATIO)
            fix_duration = _clamp_duration(tier, required)
            fix = (f"set this unit's clip_duration to {fix_duration}s ({tier}) before rendering"
                   if fix_duration is not None else
                   f"{tier}'s max legal duration cannot hit the {MAX_FREEZE_STATIC_RATIO:.0%} "
                   "budget for this slot -- switch to boomerang (if the gesture allows reversing) "
                   "or split the beat across two pages")
            results.append(GateResult(f"SW-F1[{tag}]", "FAIL",
                                       f"{evidence} > {MAX_FREEZE_STATIC_RATIO:.0%} FAIL line", fix))
        elif ratio > WARN_FREEZE_STATIC_RATIO:
            results.append(GateResult(f"SW-F1[{tag}]", "CONDITIONAL",
                                       f"{evidence} > {WARN_FREEZE_STATIC_RATIO:.0%} warn line"))
        else:
            results.append(GateResult(f"SW-F1[{tag}]", "PASS", evidence))
    return results


# =================================================== V2: IMAGE CONTENT AUDIT ===
# Mirrors pipeline/visual_render.py's _vision_call/verify_image pattern
# (fail-closed NEEDS-EYE on API unavailability, agent-bridge first / metered
# API fallback) -- but with SWIRLS-SPECIFIC rubrics, not the main engine's
# generic banned-token list, which would false-positive on swirls' own
# legitimate captions/panel borders. No auto-retry loop (deliberate: keeps
# the human eyeball + ref-crop + regen culture this style already has).

COVER_AUDIT_ROLE = (
    "You are an INDEPENDENT visual content auditor for a book-cover style illustration. "
    "The user wrote a prompt spec; an image model rendered an image. Verify the required "
    "elements and check for defects that have shipped silently before on this exact style.\n\n"
    "AUDIT IN THIS ORDER (any one failing = passed:false):\n"
    "1. **Edge-to-edge composition.** The artwork must fill the entire frame. FAIL "
    "(passed:false) if you see ANY drawn border, picture frame, decorative frame, caption "
    "strip, or margin band around the scene -- this exact defect has shipped before on this "
    "style undetected by a human eyeball pass.\n"
    "2. **Baked text.** The title and subtitle strings given below must appear, verbatim, "
    "legible, and ONLY those two lines of text anywhere on the image -- no watermark, no "
    "extra invented caption, no speech bubble.\n"
    "3. **Warm/cool lighting contrast.** The image should visibly show both a warm-toned "
    "and a cool-toned element in its lighting (not a flat monochrome/grey wash) -- this is a "
    "style requirement, not a taste preference.\n"
    "4. **Figure/subject correctness.** The described figure(s) should be recognizably "
    "present, matching the scene description below.\n\n"
    "Return ONLY a JSON object (optionally inside a ```json fence):\n"
    '{"passed": true|false, "issues": [{"claim": "...", "actual": "..."}], '
    '"banned_token_hits": ["..."]}\n'
    "List a border/frame/caption-strip hit in banned_token_hits explicitly if found."
)

PAGE_AUDIT_ROLE = (
    "You are an INDEPENDENT visual content auditor for a hand-drawn storyboard-page style "
    "illustration (baked title, frame number, 3 small top panels, one large main scene, "
    "handwritten notes). Verify the required structure and content.\n\n"
    "AUDIT IN THIS ORDER (any one failing = passed:false):\n"
    "1. **Layout.** Exactly 3 small top panels + ONE large main scene below them, in that "
    "order, must be present.\n"
    "2. **Baked text.** Only the exact handwritten strings given below should appear "
    "anywhere on the page -- no invented captions, signs, or extra text; no speech bubble or "
    "box around any caption/note.\n"
    "3. **Panel-style conformance.** {PANEL_STYLE_CHECK}\n"
    "4. **Content match.** The main scene and panels should recognizably match the "
    "descriptions given below.\n\n"
    "Return ONLY a JSON object (optionally inside a ```json fence):\n"
    '{"passed": true|false, "issues": [{"claim": "...", "actual": "..."}], '
    '"banned_token_hits": ["..."]}\n'
)


def _vision_audit(image_bytes: bytes, role: str, user_text: str, label: str) -> ImageAudit:
    from pipeline.visual_render import _encode_image_for_vision
    from pipeline import engine as text_engine
    b64, media = _encode_image_for_vision(image_bytes)
    try:
        if config.agent_mode():
            from pipeline import agent_bridge
            text = agent_bridge.call_vision(role=role, user=user_text, image_bytes=image_bytes,
                                             media=media, model=config.MODEL, label=label)
        else:
            client = text_engine._client()
            resp = client.messages.create(
                model=config.MODEL, max_tokens=2000, thinking={"type": "adaptive"}, system=role,
                messages=[{"role": "user", "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media, "data": b64}},
                    {"type": "text", "text": user_text},
                ]}])
            text = "".join(b.text for b in resp.content if b.type == "text").strip()
        return ImageAudit.from_json(text_engine._extract_json(text))
    except Exception as e:
        msg = str(e)
        if "usage limit" in msg.lower() or "usage limits" in msg.lower() or "regain access" in msg.lower():
            print(f"        ! Vision audit UNAVAILABLE -- {label} marked NEEDS-EYE (NOT passed). "
                  "Service the agent-bridge (see feedback_agent_bridge_no_api memory) and re-run.")
            return ImageAudit(passed=False, issues=[{
                "claim": "AUDIT_SKIPPED_NEEDS_EYE",
                "actual": f"Vision audit unavailable ({msg[:150]}) -- eyeball this image directly "
                          "before it ships",
            }], banned_token_hits=[])
        raise


def _sidecar_path(png: Path) -> Path:
    return png.with_suffix(png.suffix + ".audit.json")


def _png_hash(png_bytes: bytes) -> str:
    import hashlib
    return hashlib.sha256(png_bytes).hexdigest()


def _load_valid_sidecar(sidecar: Path, current_hash: str) -> ImageAudit | None:
    """FIXED 2026-08-23 (independent-review catch, codex): the original
    sidecar cache trusted any existing passed sidecar at the same filename,
    with no binding to the actual image content -- regenerating a still in
    place (same filename, different pixels) would silently reuse a stale
    PASS. Now bound to a sha256 of the PNG bytes; a content change forces
    re-audit."""
    if not sidecar.exists():
        return None
    try:
        data = json.loads(sidecar.read_text(encoding="utf-8"))
    except Exception:
        return None
    if data.get("png_sha256") != current_hash:
        return None
    existing = ImageAudit.from_json(data)
    return existing if existing.passed else None


def _write_sidecar(sidecar: Path, audit: ImageAudit, png_hash: str) -> None:
    payload = dict(audit.__dict__)
    payload["png_sha256"] = png_hash
    sidecar.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def audit_cover_still(png: Path, spec: CoverSpec) -> ImageAudit:
    png_bytes = png.read_bytes()
    png_hash = _png_hash(png_bytes)
    sidecar = _sidecar_path(png)
    existing = _load_valid_sidecar(sidecar, png_hash)
    if existing is not None:
        return existing
    user_text = (
        f"SIDE: {spec.side}\nTITLE: \"{spec.title}\" / SUBTITLE: \"{spec.subtitle}\" "
        f"(position: {spec.title_position})\nSCENE: {spec.scene}\nLIGHTING: {spec.lighting}"
    )
    audit = _vision_audit(png_bytes, COVER_AUDIT_ROLE, user_text,
                           label=f"swirls-cover-audit:{png.stem}")
    _write_sidecar(sidecar, audit, png_hash)
    return audit


def audit_page_still(png: Path, spec: PageSpec) -> ImageAudit:
    png_bytes = png.read_bytes()
    png_hash = _png_hash(png_bytes)
    sidecar = _sidecar_path(png)
    existing = _load_valid_sidecar(sidecar, png_hash)
    if existing is not None:
        return existing
    panel_check = (
        "The 3 top panels must visibly read as denser/woodcut-style linework against a "
        "softer main scene wash (a hybrid page)."
        if spec.panel_style == "woodcut_hybrid" else
        "All panels and the main scene should share the same gentle ink-wash style "
        "(no woodcut-style panels)."
    )
    # .replace(), not .format() -- PAGE_AUDIT_ROLE's JSON example contains literal
    # {"passed": ...} braces that .format() would misparse as placeholders.
    role = PAGE_AUDIT_ROLE.replace("{PANEL_STYLE_CHECK}", panel_check)
    user_text = (
        f"FRAME: {spec.frame_label}\nPANELS: {[(p.label, p.content) for p in spec.panels]}\n"
        f"MAIN SCENE: {spec.main_scene_still}\nCAPTIONS: {spec.caption_lines}\n"
        f"panel_style={spec.panel_style}"
    )
    audit = _vision_audit(png_bytes, role, user_text, label=f"swirls-page-audit:{png.stem}")
    _write_sidecar(sidecar, audit, png_hash)
    return audit


# ================================================== V3: ASSEMBLY CHECKS ===

def sw_a1_duration_parity(mp4: Path) -> GateResult:
    ok, msg = check_landing_hold.check_parity(mp4)
    return GateResult("SW-A1", "PASS" if ok else "FAIL", msg)


def sw_a2_unit_duration(units_with_held_duration: list[dict], tolerance: float = 0.15) -> list[GateResult]:
    """Each entry needs tag/mode/slot/native/held_duration (measured AFTER
    encode -- the regression tooth that would have caught the duplicate-`-vf`
    bug the day it shipped, since it checks the REALIZED clip length, not
    just the freeze-math input).

    FIXED 2026-08-23 (independent-review catch, codex): a naive `held ==
    slot` check spuriously FAILS episode 1's own approved freeze units
    (front/F05/F06) -- `make_freeze()` never trims a clip that's already
    LONGER than its slot (by design; trimming would cut approved content),
    so their held_duration correctly stays at their native length, well past
    slot. Expected duration for a freeze unit is `max(slot, native)`, not
    `slot` -- this still catches the real regression (an intended extension
    that silently failed to apply, leaving held stuck near native when slot
    > native) exactly as before. Boomerang units are unaffected -- they
    always trim to `slot` exactly."""
    results = []
    for u in units_with_held_duration:
        expected = max(u["slot"], u["native"]) if u["mode"] == "freeze" else u["slot"]
        gap = abs(u["held_duration"] - expected)
        verdict = "PASS" if gap <= tolerance else "FAIL"
        results.append(GateResult(
            f"SW-A2[{u['tag']}]", verdict,
            f"held={u['held_duration']:.3f}s expected={expected:.3f}s (mode={u['mode']}) "
            f"gap={gap:.3f}s (tolerance {tolerance}s)",
        ))
    return results


def sw_a3_total_duration(final_duration: float, narration_len: float, outro_hold: float,
                          tolerance: float = 0.3) -> GateResult:
    expected = narration_len + outro_hold
    gap = abs(final_duration - expected)
    verdict = "PASS" if gap <= tolerance else "FAIL"
    return GateResult("SW-A3", verdict,
                       f"final={final_duration:.3f}s expected={expected:.3f}s gap={gap:.3f}s "
                       f"(tolerance {tolerance}s)")


# SW-A4 (score audibility heuristic) was proposed, then DROPPED 2026-08-23 per
# independent review: 2 of 4 reviewers (gemini, cursor) independently flagged it as a
# known-flawed heuristic being shipped anyway ("cannot judge a sparse score's own
# written silences" was already an acknowledged limitation) -- and the human already
# watches the final file before it ships, which is the actual check for this. Dropped
# outright rather than kept-but-unused, per this project's own "no speculative code"
# engineering rule.


# ============================================================ OVERRIDES ===
# Named in the original plan ("document known-defective inputs via an override file,
# not by silencing the gate") but left undesigned -- independent review (cursor,
# codex) correctly flagged this as an escape hatch with no schema. Minimal design:
# one JSON file per episode, `<episode_dir>/_overrides.json`, mapping a gate tag
# (e.g. "SW-F1[f01]") to {"reason": str, "by": str, "date": str}. A FAIL on a gate
# with a matching override is downgraded to CONDITIONAL and the override is echoed
# in the evidence -- visible, greppable, never a silent bypass.

def load_overrides(episode_dir: Path) -> dict[str, dict]:
    path = episode_dir / "_overrides.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def apply_overrides(gates: list[GateResult], episode_dir: Path) -> list[GateResult]:
    overrides = load_overrides(episode_dir)
    if not overrides:
        return gates
    out = []
    for g in gates:
        entry = overrides.get(g.gate)
        if g.verdict == "FAIL" and entry:
            out.append(GateResult(
                g.gate, "CONDITIONAL",
                f"{g.evidence} -- OVERRIDDEN by {entry.get('by', '?')} on {entry.get('date', '?')}: "
                f"{entry.get('reason', '(no reason given)')}",
                g.fix,
            ))
        else:
            out.append(g)
    return out
