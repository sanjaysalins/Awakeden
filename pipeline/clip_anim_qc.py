"""Clip-animation QC + prompt-mode loop — catch the gallery-tour failures and
prevent them next time.

The existing `clip_qc.py` checks a clip is FROZEN / NO-MORPH / ON-SCENE / PERIOD.
That misses a whole class of *composition* failures the gallery-tour recipe makes:
  - a single full-figure portrait crop-jumped into nonsense (a foot, a swath of
    robe) so the figure looks like it is "dancing" (caught on #31 scene 06);
  - a crop that lands on EMPTY space (bare floor, an empty dawn-landscape corner)
    — a wasted cut that shows nothing (caught on #31 scenes 08 + 14);
  - a clip that ENDS off its subject (the hero panned to grave-cloths, not Christ).

This module adds:
  1. choose_anim_mode(scene)  — PREVENTION. Pick the right camera MODE before
     animating: full-figure single-subject portraits get a slow PUSH-IN/HOLD
     (one camera move, no crop-jumps); detail-rich scenes (unified vignettes,
     close-on-object plates) get the GALLERY-TOUR hard-cut. Feeds the prompt.
  2. build_filmstrip(mp4)     — tile N frames into ONE image so a single Vision
     call can judge the WHOLE tour (you cannot see "dancing" frame-by-frame).
  3. review_clip(...)         — DETECTION. A Vision pass with the composition
     rubric below; writes a fail-closed `<clip>.animqc.json` + a recommended
     re-render mode. Routes through the agent bridge in agent mode (no metered API).

Run:  .venv\\Scripts\\python.exe -m pipeline.clip_anim_qc "<v1 folder>"
      .venv\\Scripts\\python.exe -m pipeline.clip_anim_qc "<v1 folder>" --scenes 6,8,14
      .venv\\Scripts\\python.exe -m pipeline.clip_anim_qc "<v1 folder>" --provider nbp
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import config
from pipeline import clip_qc
from pipeline import engine as text_engine


# ---- 1. PREVENTION: pick the camera mode before animating ---------------------
_EXPRESSIVE = ("face", "eyes", "eye", "hand", "finger", "tear", "flame", "lamp",
               "wound", "footprint", "chain", "box", "chest", "veil", "scroll",
               "stone", "lips", "mouth", "woman", "child", "cowering", "kneeling")


def choose_anim_mode(scene: dict) -> str:
    """Return 'gallery' (the punchy default) or 'pushin' (rare fallback).

    LESSON (#31, 2026-06-23): a slow push-in on a full-figure portrait is BLAND —
    it has no viral edit (the user rejected it). The dancing on #06 was NOT caused
    by gallery-touring a figure; it was caused by touring the WRONG anchors (a foot,
    a swath of robe). The fix is the GALLERY-TOUR with CURATED anchors (face, eyes,
    hands, key objects — never feet/fabric/floor), which is punchy AND coherent.
    So gallery is the default for every body clip. push-in is reserved only for a
    pure atmosphere/landscape plate that has NO expressive anchor at all (rare).
    The hero closes the cut as a frozen still in assembly, so its mode is moot.
    """
    macros = [str(m).lower() for m in (scene.get("macro_elements") or [])]
    has_expressive = any(any(g in m for g in _EXPRESSIVE) for m in macros)
    jv = scene.get("jesus_variant")
    # a figure or face always has a face/hands to crop to -> gallery.
    if has_expressive or jv or (scene.get("scene_type") == "unified"):
        return "gallery"
    # genuinely anchor-less plate (pure atmosphere/landscape) -> a gentle push-in
    # beats touring empty space.
    return "pushin"


# ---- 2. filmstrip: one image, the whole tour ----------------------------------
def build_filmstrip(mp4: Path, out_dir: Path, n: int = 6) -> Path | None:
    """Extract n evenly-spaced frames and tile them L->R into one labelled strip
    so a single Vision call sees the whole camera move at once."""
    frames = clip_qc.extract_frames(mp4, out_dir, n=n)
    if not frames:
        return None
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return frames[0]  # degrade: at least hand back the first frame
    imgs = [Image.open(p).convert("RGB") for p in frames]
    h = 360
    scaled = [im.resize((int(im.width * h / im.height), h)) for im in imgs]
    gap = 6
    W = sum(im.width for im in scaled) + gap * (len(scaled) + 1)
    strip = Image.new("RGB", (W, h + 26), (16, 16, 16))
    d = ImageDraw.Draw(strip)
    x = gap
    for i, im in enumerate(scaled):
        strip.paste(im, (x, 22))
        d.text((x + 3, 4), f"{i + 1}/{len(scaled)}", fill=(230, 220, 140))
        x += im.width + gap
    out = out_dir / f"{mp4.stem}_strip.png"
    strip.save(out)
    return out


# ---- 3. DETECTION: review the tour --------------------------------------------
ANIM_RUBRIC = (
    "You are auditing a short ANIMATED clip used in a 60s gospel Short. The clip "
    "is a frozen Baroque oil painting that the camera crops/moves over (a hard-cut "
    "'gallery tour' between crops, OR a slow push-in). You are given a FILMSTRIP: "
    "N panels left->right sampling the clip start->end. Judge the SEQUENCE as motion.\n\n"
    "FAIL (passed:false) on ANY of these composition failures:\n"
    "1. WASTED CROP — one or more panels land on essentially EMPTY or meaningless "
    "space: bare floor/ground, an empty sky or landscape corner, a plain swath of "
    "fabric/drapery, or an isolated body part (a lone foot, a patch of robe) with "
    "the scene's MAIN SUBJECT absent from the panel. The tour must always show the "
    "subject or a MEANINGFUL detail of it.\n"
    "2. DANCING / JITTER — the clip is one dominant full-figure subject (a standing "
    "or seated person) and the panels jump between disjoint crops of it so the "
    "figure appears to shift, move, or 'dance'. Full-figure subjects should be a "
    "slow push-in/hold, NOT crop-jumped.\n"
    "3. OFF-SUBJECT ENDING — the LAST panel does not show the scene's main subject. "
    "(For a Christ / hero clip the final panel MUST land on Christ.)\n"
    "4. MORPH / INVENT — a face, hand, or form melts/warps between panels, or a new "
    "element appears that is not in the painting.\n"
    "5. SUBJECT IDENTITY — the intended main subject is not actually the focus of the "
    "tour at all.\n\n"
    "If it PASSES, the subject (or a meaningful detail of it) is present and stable "
    "in every panel, the motion reads as intentional, and it ends on the subject.\n\n"
    "Also RECOMMEND for a re-render if it failed:\n"
    "  - 'gallery' : the FIX for both dancing AND empty crops -> re-render the hard-cut "
    "viral edit but tour only EXPRESSIVE anchors (the face, eyes, hands, the key named "
    "object), never feet/fabric/floor/empty. List those anchors in good_anchors. (A slow "
    "push-in is NOT the fix for a figure — it is bland and has no viral edit.)\n"
    "  - 'pushin'  : ONLY for a pure atmosphere/landscape plate with genuinely no expressive anchor.\n"
    "  - 'keep'    : passes, no re-render.\n\n"
    "Return ONLY JSON:\n"
    '{"passed": true|false, "recommend_mode": "keep|gallery|pushin", '
    '"issues": ["short concrete problem, name the panel #"], '
    '"good_anchors": ["the EXPRESSIVE crop targets actually present (face, eyes, hands, named object)"], '
    '"note": "one line"}'
)


def _sidecar(mp4: Path) -> Path:
    return mp4.with_suffix(mp4.suffix + ".animqc.json")


def review_clip(mp4: Path, scene: dict, strip_png: Path, mode_used: str | None = None) -> dict:
    """One Vision review of a clip's filmstrip. Writes the fail-closed sidecar."""
    strip_bytes = strip_png.read_bytes()
    media = "image/png"
    macro = ", ".join(m for m in (scene.get("macro_elements") or []) if m)
    user_text = (
        f"SCENE {scene.get('index')}: {scene.get('title')}\n"
        f"TYPE: {scene.get('scene_type')} · FRAMING: {scene.get('framing')} · "
        f"SHOT: {scene.get('shot_kind')} · JESUS: {scene.get('jesus_variant') or '(none)'}\n"
        f"MODE ANIMATED: {mode_used or 'unknown'}\n\n"
        f"MAIN SUBJECT (must stay the focus of the tour):\n{scene.get('subject_block')}\n\n"
        f"INTENDED MEANINGFUL CROP ANCHORS: {macro or '(none listed)'}\n\n"
        "The attached FILMSTRIP samples the clip start->end (panel 1 = start). "
        "Audit the sequence as motion against the rubric."
    )
    if config.agent_mode():
        from pipeline import agent_bridge
        text = agent_bridge.call_vision(
            role=ANIM_RUBRIC, user=user_text, image_bytes=strip_bytes, media=media,
            model=config.MODEL, label=f"clip-anim-qc:scene-{scene.get('index')} {str(scene.get('title'))[:34]}",
        )
        data = text_engine._extract_json(text)
    else:
        b64, _ = _b64(strip_bytes)
        client = text_engine._client()
        resp = client.messages.create(
            model=config.MODEL, max_tokens=1200, system=ANIM_RUBRIC,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media, "data": b64}},
                {"type": "text", "text": user_text},
            ]}],
        )
        data = text_engine._extract_json("".join(b.text for b in resp.content if b.type == "text"))
    data.setdefault("passed", False)
    data["mode_used"] = mode_used
    _sidecar(mp4).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return data


def _b64(raw: bytes) -> tuple[str, str]:
    import base64
    return base64.b64encode(raw).decode(), "image/png"


def is_anim_verified(mp4: Path) -> bool:
    sc = _sidecar(mp4)
    if not sc.exists():
        return False
    try:
        return bool(json.loads(sc.read_text(encoding="utf-8")).get("passed"))
    except (OSError, ValueError):
        return False


# ---- orchestration ------------------------------------------------------------
def _load_scenes(v1: Path) -> dict[int, dict]:
    sp = json.loads((v1 / "visual" / "scene_plan.json").read_text(encoding="utf-8"))
    plan = sp.get("plan", sp)
    return {s["index"]: s for s in plan.get("scenes", [])}


def run(v1: Path, provider: str = "nbp", only: list[int] | None = None) -> list[dict]:
    nbp = v1 / "visual" / provider
    qc_dir = nbp / "_animqc_frames"
    scenes = _load_scenes(v1)
    rows = []
    for mp4 in sorted(nbp.glob("[0-9][0-9]_*.mp4")):
        idx = int(mp4.stem[:2])
        if only and idx not in only:
            continue
        scene = scenes.get(idx, {"index": idx, "title": mp4.stem[3:]})
        mode = choose_anim_mode(scene)
        strip = build_filmstrip(mp4, qc_dir)
        if strip is None:
            rows.append({"idx": idx, "clip": mp4.name, "passed": False, "note": "no frames", "recommend_mode": "rerender", "mode_for_scene": mode})
            continue
        print(f"  [reviewing] {mp4.name}  (scene mode -> {mode})", flush=True)
        v = review_clip(mp4, scene, strip, mode_used=mode)
        rows.append({"idx": idx, "clip": mp4.name, "passed": bool(v.get("passed")),
                     "recommend_mode": v.get("recommend_mode", "keep"),
                     "mode_for_scene": mode, "issues": v.get("issues", []),
                     "note": v.get("note", ""), "strip": strip})
    _write_html(v1, provider, rows)
    return rows


def _write_html(v1: Path, provider: str, rows: list[dict]) -> Path:
    nbp = v1 / "visual" / provider
    out = nbp / "_animqc_review.html"
    cards = []
    for r in rows:
        ok = r["passed"]
        strip = r.get("strip")
        rel = strip.name if strip else ""
        badge = "PASS" if ok else "FAIL"
        color = "#2e7d32" if ok else "#c62828"
        issues = "".join(f"<li>{i}</li>" for i in r.get("issues", []))
        cards.append(
            f'<div style="margin:18px 0;border-left:6px solid {color};padding:8px 14px">'
            f'<b>#{r["idx"]:02d} {r["clip"]}</b> '
            f'<span style="background:{color};color:#fff;padding:1px 8px;border-radius:4px">{badge}</span> '
            f'<span style="color:#888">scene-mode={r.get("mode_for_scene")} · recommend={r.get("recommend_mode")}</span>'
            f'<div style="color:#aaa;font-size:13px">{r.get("note","")}</div>'
            f'<ul style="color:#e0a0a0;font-size:13px">{issues}</ul>'
            f'<img src="_animqc_frames/{rel}" style="max-width:100%;border:1px solid #333">'
            f'</div>')
    out.write_text(
        "<html><body style='background:#111;color:#ddd;font-family:sans-serif;max-width:1100px;margin:auto'>"
        f"<h2>Clip-animation QC — {v1.name}</h2>" + "".join(cards) + "</body></html>",
        encoding="utf-8")
    return out


if __name__ == "__main__":
    argv = sys.argv[1:]
    pos = [a for a in argv if not a.startswith("--")]
    if not pos:
        print("usage: python -m pipeline.clip_anim_qc \"<v1 folder>\" [--scenes 6,8,14] [--provider nbp]")
        raise SystemExit(2)
    v1 = Path(pos[0])
    provider = "nbp"
    only = None
    for a in argv:
        if a.startswith("--provider"):
            provider = a.split("=", 1)[1] if "=" in a else "nbp"
        if a.startswith("--scenes"):
            only = [int(x) for x in (a.split("=", 1)[1] if "=" in a else pos[1]).split(",") if x.strip()]
    rows = run(v1, provider=provider, only=only)
    print()
    for r in rows:
        tag = "PASS" if r["passed"] else "FAIL"
        print(f"  [{tag}] #{r['idx']:02d} {r['clip']:42} mode={r.get('mode_for_scene'):7} "
              f"recommend={r.get('recommend_mode'):7} {r.get('note','')}")
    fails = [r for r in rows if not r["passed"]]
    print(f"\n{len(rows)-len(fails)}/{len(rows)} clips PASS anim-QC; {len(fails)} need a re-render.")
    if fails:
        print("Re-render guidance:")
        for r in fails:
            print(f"  - #{r['idx']:02d}: recommend mode '{r.get('recommend_mode')}'  ({r.get('note','')})")
