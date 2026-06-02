"""Centralized HERO-STILLS LIBRARY — unique Baroque stills + one cached Kling
animation each, REUSED across episodes.

Two rules (the user's, enforced downstream by the assembler's AS-G2/G6/G7):
  1. A still may NOT repeat WITHIN a single mp3's cut (per-episode uniqueness).
  2. A still CAN be reused ACROSS different mp3s.
Each unique still is animated ONCE (Kling viral cut-plan); the .mp4 is cached
here and reused wherever the still appears.

This module is a SELECTION + MATERIALIZE layer in FRONT of the existing,
unchanged assembler. It does not re-implement image gen / animation / assembly —
it reuses visual_render.render_scene, video_render.animate_clip, and feeds the
assembler a real `<v1>/visual/<provider>/` folder + a synthesized scene_plan.json.

Layout (under config.NARRATION_PROJECT_DIR):
  _hero_library/
    library.json                         manifest (one entry per unique still)
    index.html                           human browse page
    stills/<slug>.png .mp4 .kling.json .cut_hint.json .png.audit.json
"""
from __future__ import annotations

import json
import re
import shutil
from dataclasses import asdict
from pathlib import Path

import config
from pipeline import engine, visual_render, video_render
from pipeline.visual_models import ImageAudit, Scene, ScenePlan

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
LIB_DIR = config.NARRATION_PROJECT_DIR / "_hero_library"
STILLS_DIR = LIB_DIR / "stills"
MANIFEST = LIB_DIR / "library.json"

# Shipped keeper episodes whose stills we harvest to SEED the library.
SEED_EPISODES = (
    "12 The Kiss That Cut Off the Bargain",
    "16 The Fire Jesus Built",
    "18 He Never Said Yes",
)

# Coarse theme-tag derivation (the LLM selector does the real matching; these
# are just a prefilter / browse aid). Keyword -> tags.
_TAG_HINTS = {
    "bread": ["bread", "loaf", "hunger", "manna", "table", "feast"],
    "loaf": ["bread", "loaf"],
    "manna": ["manna", "wilderness", "bread"],
    "hunger": ["hunger", "bread", "empty"],
    "water": ["water", "well", "thirst"],
    "well": ["well", "water", "samaritan", "thirst"],
    "storm": ["storm", "sea", "boat", "waves", "fear"],
    "fire": ["fire", "coals", "shore", "charcoal"],
    "door": ["door", "gate", "sheepfold", "threshold"],
    "shepherd": ["shepherd", "sheep", "fold"],
    "light": ["light", "lamp", "darkness", "fire"],
    "cross": ["cross", "crucifixion", "calvary", "passion", "gospel"],
    "crucif": ["cross", "crucifixion", "passion", "gospel"],
    "tomb": ["tomb", "resurrection", "empty"],
    "risen": ["resurrection", "risen", "gospel"],
    "father": ["father", "embrace", "prodigal", "return"],
    "prodigal": ["prodigal", "father", "return", "swine"],
    "pool": ["pool", "bethesda", "healing"],
    "crowd": ["crowd", "multitude", "people"],
    "throne": ["throne", "glory", "king"],
}

_GOSPEL_ARC_TOKENS = ("nt-gospel-link", "gospel-link", "passion", "resurrection")
_CROSS_RX = re.compile(r"\b(cross|crucif|calvary|golgotha)", re.IGNORECASE)


# --------------------------------------------------------------------------
# Manifest I/O
# --------------------------------------------------------------------------
def load() -> list[dict]:
    if not MANIFEST.exists():
        return []
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def save(entries: list[dict]) -> None:
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def by_slug(entries: list[dict], slug: str) -> dict | None:
    return next((e for e in entries if e["slug"] == slug), None)


# --------------------------------------------------------------------------
# Tagging / classification
# --------------------------------------------------------------------------
def _theme_tags(title: str, subject: str, arc: str, extra: list[str] | None = None) -> list[str]:
    tags: set[str] = set(extra or [])
    text = f"{title} {subject} {arc}".lower()
    for key, ts in _TAG_HINTS.items():
        if key in text:
            tags.update(ts)
    for w in re.split(r"[\s\-_]+", title.lower()):
        if len(w) > 3:
            tags.add(w)
    return sorted(tags)


def is_gospel_pivot(entry: dict) -> bool:
    """Mirror assembly_engine._is_gospel_pivot so a reused still is classified
    the same way the assembler will classify it (the close/hero must be this)."""
    arc = (entry.get("arc_position") or "").lower()
    if any(tok in arc for tok in _GOSPEL_ARC_TOKENS):
        return True
    if (entry.get("jesus_variant") or "") in ("passion", "resurrection"):
        return True
    return bool(_CROSS_RX.search(entry.get("title") or ""))


# --------------------------------------------------------------------------
# Entry <-> Scene
# --------------------------------------------------------------------------
def entry_to_scene(entry: dict, index: int) -> Scene:
    """Build a visual_models.Scene from a library entry, using a per-episode
    index. The .slug carries the library slug so the materialized filename
    stem (`NN_<libslug>`) round-trips and stays unique across episodes."""
    return Scene(
        index=index,
        slug=entry["slug"],
        title=entry.get("title", entry["slug"]),
        scene_type=entry.get("scene_type", "single"),
        arc_position=entry.get("arc_position", ""),
        framing=entry.get("framing", "mid"),
        purpose=entry.get("purpose", ""),
        rationale=entry.get("rationale", ""),
        visible_elements=entry.get("visible_elements", ""),
        emotional_tone=entry.get("emotional_tone", ""),
        subject_block=entry.get("subject_block", ""),
        mood_block=entry.get("mood_block", ""),
        jesus_variant=entry.get("jesus_variant") or None,
        priority=index,
        macro_elements=entry.get("macro_elements", []) or [],
        pacing=entry.get("pacing", "controlled") or "controlled",
        viral_role=entry.get("viral_role", "") or "",
        shot_kind=entry.get("shot_kind", "standard") or "standard",
        vignettes=entry.get("vignettes", []) or [],
    )


def _scene_to_plan_dict(scene: Scene) -> dict:
    """Serialize a Scene back to the dict shape ScenePlan.from_json reads."""
    return {
        "index": scene.index,
        "slug": scene.slug,
        "title": scene.title,
        "scene_type": scene.scene_type,
        "arc_position": scene.arc_position,
        "framing": scene.framing,
        "purpose": scene.purpose,
        "rationale": scene.rationale,
        "visible_elements": scene.visible_elements,
        "emotional_tone": scene.emotional_tone,
        "subject_block": scene.subject_block,
        "mood_block": scene.mood_block,
        "jesus_variant": scene.jesus_variant,
        "priority": scene.priority,
        "macro_elements": scene.macro_elements,
        "pacing": scene.pacing,
        "viral_role": scene.viral_role,
        "shot_kind": scene.shot_kind,
        "vignettes": scene.vignettes,
    }


# --------------------------------------------------------------------------
# SEED — harvest the shipped stills
# --------------------------------------------------------------------------
def _episode_num(folder_name: str) -> str:
    m = re.match(r"\s*(\d+)", folder_name)
    return m.group(1) if m else folder_name.split()[0]


def harvest(log=print) -> list[dict]:
    """Copy the shipped episodes' stills (+ cached .mp4/.kling.json) into the
    library and build manifest entries, tagged from each episode's scene_plan."""
    STILLS_DIR.mkdir(parents=True, exist_ok=True)
    entries = load()
    have = {e["slug"] for e in entries}
    added = 0
    for ep in SEED_EPISODES:
        epnum = _episode_num(ep)
        v1 = config.NARRATION_TREE_DIR / ep / "v1"
        plan_path = v1 / "visual" / "scene_plan.json"
        hf = v1 / "visual" / "hf"
        if not plan_path.exists() or not hf.exists():
            log(f"  ! {ep}: no scene_plan.json or hf/ — skipping")
            continue
        plan = ScenePlan.from_json(json.loads(plan_path.read_text(encoding="utf-8")).get("plan", {}))
        for scene in plan.scenes:
            png_src = hf / f"{scene.filename_stem}.png"
            if not png_src.exists():
                continue
            slug = f"{epnum}-{scene.slug}"
            if slug in have:
                continue
            # copy media + sidecars into the library
            shutil.copy2(png_src, STILLS_DIR / f"{slug}.png")
            mp4_src = hf / f"{scene.filename_stem}.mp4"
            kling_src = hf / f"{scene.filename_stem}.kling.json"
            has_mp4 = mp4_src.exists()
            if has_mp4:
                shutil.copy2(mp4_src, STILLS_DIR / f"{slug}.mp4")
            if kling_src.exists():
                shutil.copy2(kling_src, STILLS_DIR / f"{slug}.kling.json")
            entry = {
                "id": f"hero:{slug}",
                "slug": slug,
                "title": scene.title,
                "scene_type": scene.scene_type,
                "arc_position": scene.arc_position,
                "framing": scene.framing,
                "purpose": scene.purpose,
                "rationale": scene.rationale,
                "visible_elements": scene.visible_elements,
                "emotional_tone": scene.emotional_tone,
                "subject_block": scene.subject_block,
                "mood_block": scene.mood_block,
                "jesus_variant": scene.jesus_variant,
                "macro_elements": scene.macro_elements,
                "vignettes": scene.vignettes,
                "pacing": scene.pacing or "controlled",
                "viral_role": scene.viral_role or "",
                "shot_kind": scene.shot_kind or "standard",
                "theme_tags": _theme_tags(scene.title, scene.subject_block, scene.arc_position),
                "style": "baroque",
                "png": f"stills/{slug}.png",
                "mp4": f"stills/{slug}.mp4" if has_mp4 else None,
                "kling_json": f"stills/{slug}.kling.json" if kling_src.exists() else None,
                "audit_passed": True,  # shipped = already approved by the user
                "source": f"harvested:{ep}/{scene.filename_stem}",
                "episodes_used_in": [],
            }
            entry["gospel_pivot"] = is_gospel_pivot(entry)
            entries.append(entry)
            have.add(slug)
            added += 1
            log(f"  + {slug}  [{entry['arc_position'] or '?'}] "
                f"{'mp4' if has_mp4 else 'png-only'}{' PIVOT' if entry['gospel_pivot'] else ''}")
    save(entries)
    log(f"harvest: +{added} stills ({len(entries)} total in library)")
    return entries


# --------------------------------------------------------------------------
# SELECT — match a narration's beats to library stills (+ gaps)
# --------------------------------------------------------------------------
def _read_beats(v1: Path) -> list[str]:
    md = (v1 / "narration.md").read_text(encoding="utf-8")
    return [p.strip() for p in md.split("\n\n") if p.strip()]


def _candidate_block(entries: list[dict]) -> str:
    lines = []
    for e in entries:
        subj = (e.get("subject_block") or "")[:140]
        lines.append(
            f'- id="{e["slug"]}" | role={e.get("viral_role") or "?"} | arc={e.get("arc_position") or "?"} '
            f'| jesus={e.get("jesus_variant") or "-"} | pivot={"Y" if e.get("gospel_pivot") else "n"} '
            f'| tags={",".join(e.get("theme_tags", [])[:6])} | {e.get("title")}: {subj}'
        )
    return "\n".join(lines)


_SELECT_ROLE = (
    "You are the VISUAL EDITOR for a 60s Baroque-oil gospel Short. You assemble a "
    "cut by SELECTING from a shared library of existing hero stills, and only "
    "request a NEW still when nothing in the library fits a beat. Style is Flemish "
    "Baroque oil painting — NEVER modern objects (no fridge/phone/car); translate "
    "modern hooks into Baroque equivalents (a laden table, a coin, hungry eyes)."
)


def select_for_episode(v1: Path, entries: list[dict], target_clips: int = 8, log=print) -> dict:
    """One LLM call: choose ordered library stills for this narration + list
    gaps (new stills to generate). Returns a dict with 'selection' and 'gaps'."""
    beats = _read_beats(v1)
    beats_block = "\n".join(f"[{i}] {b}" for i, b in enumerate(beats))
    user = (
        f"NARRATION BEATS (hook→point→proof→conviction→landing):\n{beats_block}\n\n"
        f"LIBRARY STILLS available to reuse (pick by id):\n{_candidate_block(entries)}\n\n"
        f"TASK: design a ~{target_clips}-clip cut (6-10). Return JSON:\n"
        "{\n"
        '  "reading": "<2-3 sentence visual arc>",\n'
        '  "selection": [\n'
        '     {"id": "<library slug OR null if this slot needs a new still>",\n'
        '      "gap_ref": "<slug-hint if id is null, else null>",\n'
        '      "arc_position": "opening-hook|biblical-setting|...|nt-gospel-link|closing-devotional",\n'
        '      "viral_role": "hook-open|build|pivot|climax|close",\n'
        '      "why": "<why this image under this beat>"} , ...\n'
        '  ],\n'
        '  "hero_id": "<the library slug OR gap_ref that CLOSES the cut — MUST be a cross/Christ/NT-gospel-link>",\n'
        '  "gaps": [\n'
        '     {"slug_hint": "<kebab>", "title": "...", "arc_position": "...", "viral_role": "...",\n'
        '      "jesus_variant": "ministry|passion|resurrection|infant|null",\n'
        '      "scene_type": "single|unified",\n'
        '      "framing": "wide|mid|close|overhead|low-angle",\n'
        '      "subject_block": "<~50-90 words, state-only Baroque tableau, no motion verbs, no modern items>",\n'
        '      "mood_block": "<one line>",\n'
        '      "visible_elements": "<concrete nouns the audit checks>",\n'
        '      "emotional_tone": "<one line>",\n'
        '      "macro_elements": ["3-5 cut anchors"],\n'
        '      "theme_tags": ["..."]} , ...\n'
        '  ]\n'
        "}\n\n"
        "RULES: (1) NEVER use the same id twice in one selection. (2) Prefer reusing "
        "a fitting library still over a gap. (3) The CLOSE clip = hero_id and MUST be a "
        "cross/Christ/NT-gospel-link (gospel frame). (4) Include ≥1 cross/Christ in the cut. "
        "(5) Vary framing. (6) Every gap subject_block is a still Baroque tableau (camera-only "
        "motion later), no modern objects. Each selection slot references either a library id "
        "OR a gap_ref that exactly matches a gaps[].slug_hint."
    )
    raw = engine._call(_SELECT_ROLE, user, label="hero-select")
    doc = engine._extract_json(raw)
    return doc


# --------------------------------------------------------------------------
# GAPS — generate new stills and register them
# --------------------------------------------------------------------------
def generate_gaps(gap_specs: list[dict], provider_name: str = "hf", log=print) -> list[dict]:
    """Render each gap spec into the library (idempotent) and register it.
    Returns the newly-added entries."""
    STILLS_DIR.mkdir(parents=True, exist_ok=True)
    entries = load()
    have = {e["slug"] for e in entries}
    provider = visual_render.get_provider(provider_name)
    added: list[dict] = []
    for g in gap_specs:
        slug = g["slug_hint"].strip().lower()
        if slug in have:
            log(f"  [skip] {slug} already in library")
            continue
        scene = Scene(
            index=1, slug=slug, title=g.get("title", slug),
            scene_type=g.get("scene_type", "single"),
            arc_position=g.get("arc_position", ""),
            framing=g.get("framing", "mid"),
            purpose=g.get("purpose", ""), rationale=g.get("rationale", ""),
            visible_elements=g.get("visible_elements", ""),
            emotional_tone=g.get("emotional_tone", ""),
            subject_block=g.get("subject_block", ""),
            mood_block=g.get("mood_block", ""),
            jesus_variant=(g.get("jesus_variant") or None
                           if g.get("jesus_variant") not in (None, "", "null", "none") else None),
            macro_elements=g.get("macro_elements", []) or [],
            pacing=g.get("pacing", "controlled"),
            viral_role=g.get("viral_role", ""),
            vignettes=g.get("vignettes", []) or [],
        )
        slug_png = STILLS_DIR / f"{slug}.png"
        if slug_png.exists():
            # already on disk (e.g. a prior partial run) — reuse, don't re-pay HF
            audit_ok = True
            ap = STILLS_DIR / f"{slug}.png.audit.json"
            if ap.exists():
                try:
                    audit_ok = ImageAudit.from_json(json.loads(ap.read_text(encoding="utf-8"))).passed
                except Exception:
                    pass
            log(f"  [reuse-on-disk] {slug}.png exists — registering without re-render")
        else:
            visual_render.render_scene(scene, provider, STILLS_DIR, log=log)
            # render_scene names files by stem (NN_<slug>); normalize to <slug>.*
            stem = scene.filename_stem
            for src_name, dst_name in (
                (f"{stem}.png", f"{slug}.png"),
                (f"{stem}.png.audit.json", f"{slug}.png.audit.json"),
                (f"{stem}.cut_hint.json", f"{slug}.cut_hint.json"),
            ):
                src = STILLS_DIR / src_name
                if src.exists():
                    src.replace(STILLS_DIR / dst_name)
            audit_ok = True
            ap = STILLS_DIR / f"{slug}.png.audit.json"
            if ap.exists():
                try:
                    audit_ok = ImageAudit.from_json(json.loads(ap.read_text(encoding="utf-8"))).passed
                except Exception:
                    pass
        entry = {
            "id": f"hero:{slug}", "slug": slug, "title": scene.title,
            "scene_type": scene.scene_type, "arc_position": scene.arc_position,
            "framing": scene.framing, "purpose": scene.purpose, "rationale": scene.rationale,
            "visible_elements": scene.visible_elements, "emotional_tone": scene.emotional_tone,
            "subject_block": scene.subject_block, "mood_block": scene.mood_block,
            "jesus_variant": scene.jesus_variant, "macro_elements": scene.macro_elements,
            "vignettes": scene.vignettes, "pacing": scene.pacing or "controlled",
            "viral_role": scene.viral_role or "", "shot_kind": scene.shot_kind or "standard",
            "theme_tags": g.get("theme_tags") or _theme_tags(scene.title, scene.subject_block, scene.arc_position),
            "style": "baroque", "png": f"stills/{slug}.png", "mp4": None, "kling_json": None,
            "audit_passed": bool(audit_ok),
            "source": "generated", "episodes_used_in": [],
        }
        entry["gospel_pivot"] = is_gospel_pivot(entry)
        entries.append(entry)
        have.add(slug)
        added.append(entry)
        log(f"  + generated {slug}  audit={'PASS' if audit_ok else 'FAIL'}")
    save(entries)
    return added


# --------------------------------------------------------------------------
# ANIMATE ONCE — animate uncached library stills, cache the .mp4
# --------------------------------------------------------------------------
def animate_uncached(slugs: list[str], log=print) -> int:
    """For each slug lacking a cached stills/<slug>.mp4, run the Kling viral
    cut-plan ONCE and cache it. Returns count animated."""
    entries = load()
    provider = video_render.get_video_provider()
    made = 0
    for slug in slugs:
        e = by_slug(entries, slug)
        if e is None:
            log(f"  ! {slug} not in library; skip")
            continue
        png = STILLS_DIR / f"{slug}.png"
        mp4 = STILLS_DIR / f"{slug}.mp4"
        if mp4.exists():
            log(f"  [skip] {slug}.mp4 cached")
            e["mp4"] = f"stills/{slug}.mp4"
            continue
        if not png.exists():
            log(f"  ! {slug}.png missing; skip")
            continue
        video_render.animate_clip(
            png, mp4, pacing=e.get("pacing", "controlled"),
            viral_role=e.get("viral_role", ""), provider=provider, log=log,
        )
        e["mp4"] = f"stills/{slug}.mp4"
        kj = png.with_suffix(".kling.json")
        if kj.exists():
            e["kling_json"] = f"stills/{slug}.kling.json"
        made += 1
        log(f"  + animated {slug}")
    save(entries)
    return made


# --------------------------------------------------------------------------
# MATERIALIZE — copy selected stills into an episode + write scene_plan.json
# --------------------------------------------------------------------------
def materialize_into_episode(v1: Path, provider: str, ordered_slugs: list[str],
                             hero_slug: str, log=print) -> Path:
    """Copy each selected still's png+mp4(+sidecars) into <v1>/visual/<provider>/
    as NN_<slug>.* and write a synthesized scene_plan.json. The existing
    assembler then runs unchanged."""
    entries = load()
    render_dir = v1 / "visual" / provider
    render_dir.mkdir(parents=True, exist_ok=True)
    scenes_doc: list[dict] = []
    hero_index = 0
    for i, slug in enumerate(ordered_slugs, start=1):
        e = by_slug(entries, slug)
        if e is None:
            raise SystemExit(f"materialize: '{slug}' not in library")
        scene = entry_to_scene(e, i)
        stem = scene.filename_stem  # NN_<slug>
        shutil.copy2(STILLS_DIR / f"{slug}.png", render_dir / f"{stem}.png")
        if e.get("mp4"):
            shutil.copy2(STILLS_DIR / f"{slug}.mp4", render_dir / f"{stem}.mp4")
        for ext in ("kling.json", "cut_hint.json", "png.audit.json"):
            src = STILLS_DIR / f"{slug}.{ext}"
            if src.exists():
                shutil.copy2(src, render_dir / f"{stem}.{ext}")
        scenes_doc.append(_scene_to_plan_dict(scene))
        if slug == hero_slug:
            hero_index = i
        # track cross-episode reuse
        epname = v1.parent.name
        if epname not in e.setdefault("episodes_used_in", []):
            e["episodes_used_in"].append(epname)
    save(entries)
    plan_doc = {
        "plan": {
            "visual_reading": "Assembled from the centralized hero-stills library.",
            "red_team_notes": "",
            "scenes": scenes_doc,
            "short_priority": [s["index"] for s in scenes_doc],
            "candidates": [],
            "rationale": "Library selection (animate-once, reuse-across).",
            "beat_coverage": {},
            "hero_candidate": hero_index,
        }
    }
    out = v1 / "visual" / "scene_plan.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan_doc, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"  materialized {len(ordered_slugs)} stills -> {render_dir} (hero scene {hero_index})")
    return out


# --------------------------------------------------------------------------
# Browse page
# --------------------------------------------------------------------------
def _episode_hero_index(v1: Path, plan: ScenePlan | None) -> int:
    """Best-effort hero scene index: assembly edit_plan -> scene_plan.hero_candidate
    -> first gospel-pivot scene."""
    ep = v1 / "assembly" / "edit_plan.json"
    if ep.exists():
        try:
            d = json.loads(ep.read_text(encoding="utf-8"))
            h = (d.get("plan", d) or {}).get("hero_scene_index") or d.get("hero_scene_index")
            if h:
                return int(h)
        except Exception:
            pass
    if plan and plan.hero_candidate:
        return plan.hero_candidate
    for s in (plan.scenes if plan else []):
        if is_gospel_pivot({"arc_position": s.arc_position, "jesus_variant": s.jesus_variant, "title": s.title}):
            return s.index
    return 0


def _find_v_folder(ep_dir: Path) -> Path | None:
    """Pick the v-folder to report: prefer one with visual/scene_plan.json, else
    one with a _library_selection.json, else the highest-numbered v* with narration.md."""
    vs = sorted([d for d in ep_dir.iterdir() if d.is_dir() and re.match(r"v\d+$", d.name)],
                key=lambda p: p.name)
    if not vs:
        return None
    for v in vs:
        if (v / "visual" / "scene_plan.json").exists():
            return v
    for v in vs:
        if (v / "visual" / "_library_selection.json").exists():
            return v
    for v in reversed(vs):
        if (v / "narration.md").exists():
            return v
    return vs[-1]


def write_master_index(log=print) -> Path:
    """Scan every narration and build ONE consolidated index: the central
    library (heroes flagged) + per-narration stills & hero. Read-only."""
    lib = load()
    out = LIB_DIR / "master_index.html"
    LIB_DIR.mkdir(parents=True, exist_ok=True)

    def rel(p: Path) -> str:
        try:
            return str(Path(__import__("os").path.relpath(p, LIB_DIR))).replace("\\", "/")
        except Exception:
            return str(p).replace("\\", "/")

    # ---- per-narration sections ----
    tree = config.NARRATION_TREE_DIR
    ep_dirs = sorted([d for d in tree.iterdir()
                      if d.is_dir() and not d.name.startswith("_")
                      and d.name not in ("per_turn_synth.py",)],
                     key=lambda p: p.name)
    rows = []
    counts = {"rendered": 0, "planned": 0, "none": 0, "stills": 0}
    for ep in ep_dirs:
        v1 = _find_v_folder(ep)
        if v1 is None or not (v1 / "narration.md").exists():
            continue
        plan_path = v1 / "visual" / "scene_plan.json"
        sel_path = v1 / "visual" / "_library_selection.json"
        cards = ""
        status = "none"; hero_label = "—"
        if plan_path.exists():
            status = "rendered"
            plan = ScenePlan.from_json(json.loads(plan_path.read_text(encoding="utf-8")).get("plan", {}))
            hero_idx = _episode_hero_index(v1, plan)
            # locate a provider dir with media
            prov = next((p.name for p in (v1 / "visual").iterdir()
                         if p.is_dir() and any(p.glob("*.png"))), "hf") if (v1 / "visual").exists() else "hf"
            pdir = v1 / "visual" / prov
            for s in plan.scenes:
                png = pdir / f"{s.filename_stem}.png"
                mp4 = pdir / f"{s.filename_stem}.mp4"
                thumb = (f'<img src="{rel(png)}" loading=lazy>' if png.exists()
                         else '<div class=ph>planned</div>')
                if png.exists():
                    counts["stills"] += 1
                badge = " 👑HERO" if s.index == hero_idx else (" ⛪" if is_gospel_pivot(
                    {"arc_position": s.arc_position, "jesus_variant": s.jesus_variant, "title": s.title}) else "")
                cls = "s hero" if s.index == hero_idx else "s"
                cards += (f'<div class="{cls}">{thumb}<div class=cap>{s.index:02d} {s.title}{badge}'
                          f'<br><i>{s.viral_role or "?"} · {s.arc_position or "?"}</i></div></div>')
            hpln = plan.scene_by_index(hero_idx)
            hero_label = f"{hero_idx:02d} {hpln.title}" if hpln else "—"
        elif sel_path.exists():
            status = "planned"
            sel = json.loads(sel_path.read_text(encoding="utf-8"))
            hero_slug = sel.get("hero_slug", "")
            for slug in sel.get("ordered_slugs", []):
                e = by_slug(lib, slug)
                png = STILLS_DIR / f"{slug}.png"
                mp4 = STILLS_DIR / f"{slug}.mp4"
                if e and png.exists():
                    thumb = f'<img src="{rel(png)}" loading=lazy>'
                else:
                    thumb = '<div class=ph>to&nbsp;generate</div>'
                badge = " 👑HERO" if slug == hero_slug else ""
                reuse = "" if e else " (gap)"
                cls = "s hero" if slug == hero_slug else "s"
                cards += (f'<div class="{cls}">{thumb}<div class=cap>{slug}{badge}{reuse}</div></div>')
            hero_label = hero_slug or "—"
        counts[status] += 1
        n_stills = cards.count('class="s')
        rows.append(
            f'<section><h3>{ep.name} <span class="st {status}">{status}</span></h3>'
            f'<div class=meta>hero: <b>{hero_label}</b> · {n_stills} stills</div>'
            f'<div class=grid>{cards or "<i style=color:#777>no visuals yet</i>"}</div></section>'
        )

    # ---- central library section ----
    def lib_card(e):
        png = STILLS_DIR / f"{e['slug']}.png"
        thumb = f'<img src="{rel(png)}" loading=lazy>'
        pivot = " ⛪" if e.get("gospel_pivot") else ""
        used = f' · used×{len(e.get("episodes_used_in", []))}' if e.get("episodes_used_in") else ""
        return (f'<div class=s>{thumb}<div class=cap>{e["slug"]}{pivot}'
                f'<br><i>{e.get("viral_role") or "?"}{used}</i></div></div>')
    lib_cards = "".join(lib_card(e) for e in lib)
    n_pivot = sum(1 for e in lib if e.get("gospel_pivot"))

    html = f"""<!doctype html><meta charset=utf-8><title>Narration Stills &amp; Heroes — Master Index</title>
<style>body{{background:#15151a;color:#eee;font:14px system-ui;margin:0;padding:22px}}
h1{{font-size:22px}} h2{{color:#ffd86c;margin-top:30px}} h3{{font-size:15px;margin:18px 0 4px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}}
.s{{background:#222;border-radius:7px;overflow:hidden}} .s img,.s video{{width:100%;display:block;aspect-ratio:9/16;object-fit:cover}}
.s.hero{{outline:2px solid #ffd86c}} .ph{{aspect-ratio:9/16;display:flex;align-items:center;justify-content:center;color:#888;background:#1b1b22;font-size:12px}}
.cap{{padding:5px 7px;font-size:11px;line-height:1.3}} .cap i{{color:#9a9;font-style:normal}}
.meta{{color:#aaa;font-size:12px;margin-bottom:6px}}
.st{{font-size:11px;padding:1px 7px;border-radius:9px;vertical-align:middle}}
.st.rendered{{background:#1c4}} .st.planned{{background:#46c}} .st.none{{background:#444;color:#aaa}}
section{{border-top:1px solid #2a2a33;padding-top:6px}}</style>
<h1>Narration Stills &amp; Heroes — Master Index</h1>
<p style="color:#aaa">👑 = hero (the gospel-pivot that bookends/closes the cut) · ⛪ = gospel-pivot eligible.
Status: <span class="st rendered">rendered</span> images on disk · <span class="st planned">planned</span> library-selected, not yet generated · <span class="st none">none</span>.</p>
<p style="color:#ccc">{counts['rendered']} rendered · {counts['planned']} planned · {counts['none']} text-only · {counts['stills']} stills on disk across narrations.</p>
<h2>Central Hero-Stills Library ({len(lib)} stills · {n_pivot} gospel-pivot)</h2>
<div class=grid>{lib_cards}</div>
<h2>Per-narration</h2>
{''.join(rows)}"""
    out.write_text(html, encoding="utf-8")
    log(f"wrote {out}  ({counts['rendered']} rendered, {counts['planned']} planned, {counts['none']} text-only)")
    return out


def write_index_html(log=print) -> Path:
    entries = load()
    def card(e):
        png = f'stills/{e["slug"]}.png'
        link = (e["mp4"] if e.get("mp4") else png)  # click-through plays the clip if animated
        play = " ▶" if e.get("mp4") else ""
        media = f'<img src="{png}" loading=lazy>'
        pivot = " ⛪PIVOT" if e.get("gospel_pivot") else ""
        used = f' · used in {len(e.get("episodes_used_in", []))}' if e.get("episodes_used_in") else ""
        tags = " ".join(f"<i>{t}</i>" for t in e.get("theme_tags", [])[:8])
        return (f'<div class=c><a href="{link}">{media}</a>'
                f'<div class=l>{e["slug"]}{play}</div>'
                f'<div class=r>{e.get("viral_role") or "?"} · {e.get("arc_position") or "?"}{pivot}{used}</div>'
                f'<div class=t>{tags}</div></div>')
    n_mp4 = sum(1 for e in entries if e.get("mp4"))
    cards = "".join(card(e) for e in entries)
    html = f"""<!doctype html><meta charset=utf-8><title>Hero Stills Library</title>
<style>body{{background:#16161a;color:#eee;font:15px system-ui;margin:0;padding:20px}}
h1{{font-size:21px}} .g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px}}
.c{{background:#222;border-radius:8px;overflow:hidden}} .c img,.c video{{width:100%;display:block}}
.l{{padding:7px 10px 1px;font-weight:700;font-size:13px}}
.r{{padding:0 10px;color:#9c9;font-size:12px}} .t{{padding:4px 10px 10px;color:#888;font-size:11px}}
.t i{{font-style:normal;background:#333;border-radius:3px;padding:1px 5px;margin:0 3px 2px 0;display:inline-block}}</style>
<h1>Hero Stills Library — {len(entries)} stills ({n_mp4} animated)</h1>
<p style="color:#aaa">Unique stills, reused across cuts; each animated once. ⛪ = gospel-pivot (eligible to close a cut).</p>
<div class=g>{cards}</div>"""
    out = LIB_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    log(f"wrote {out}")
    return out
