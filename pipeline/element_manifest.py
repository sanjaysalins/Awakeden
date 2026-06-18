"""ELEMENT MANIFEST — the locked, vision-verified element contract for a still (INV-25).

The spine of Visual v3 (`v2/INTENTIONAL_STILL_SPEC.md`). A still's manifest is the single
source of truth for (a) what the painting contains, (b) the ONLY things the animation edit
may crop to, and (c) what every rendered clip frame is checked against. It is a companion
sidecar to the coherence verdict — `<png>.manifest.json` — bound by the SAME png_sha256 so a
silent re-render busts both (we reuse `coherence.png_sha256`/binding rather than reinvent it).

Lifecycle (declare -> render -> reconcile -> LOCK):
  1. DECLARE   — promote the scene's macro_elements into elements[{id,label,region}] at design.
  2. RENDER    — the still is painted to contain them.
  3. RECONCILE — verify_image marks each declared element verified true/false against the real
                 render (default-PASS on the subtle; a missing element is CUT from the tour, not
                 auto-re-rendered) and sets period_real (the constitution T1-T6 guardrails).
  4. LOCK      — write the manifest, png_sha256-bound, locked=True. Only verified elements may
                 be targeted by the edit; the clip element gate checks frames ⊆ verified set.

A re-render is legal ONLY through relock(): it recomputes the hash, bumps lock_version, and
stamps approved_at — so an approved fix is distinguishable from a silent tamper.

Run:  .venv\\Scripts\\python.exe -m pipeline.element_manifest show "<png>"
"""
from __future__ import annotations
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path

from . import coherence  # reuse png_sha256 + the hash-binding discipline

# the constitution render guardrails the period_real verdict is keyed to (T1-T6)
PERIOD_REAL_KEYS = ("T1", "T2", "T3", "T4", "T5", "T6")
SUBJECT_TYPES = ("hero", "multi-story")
ROLES = ("hook-open", "hero", "multi-story", "hero-bookend")


def manifest_path(png: Path) -> Path:
    return Path(png).with_suffix(Path(png).suffix + ".manifest.json")


@dataclass
class Element:
    id: str
    label: str
    region: dict | None = None          # advisory normalized {"box":[x,y,w,h]}; not a hard gate in P1
    verified: bool = False              # set True only after vision confirms it IS in the render


@dataclass
class ElementManifest:
    still_id: str
    subject_type: str = "hero"          # hero | multi-story
    role: str = "hero"                  # hook-open | hero | multi-story | hero-bookend
    elements: list = field(default_factory=list)        # list[Element]
    ambient_layer: list = field(default_factory=list)   # allowlisted atmospherics; element gate ignores
    period_real: dict = field(default_factory=dict)     # {T1..T6: pass|fail}
    declared_by: str = "design"         # design | backfill-vision
    provenance: str = "fresh"           # fresh | legacy
    lock_version: int = 1
    png_sha256: str = ""
    locked: bool = False
    note: str = ""

    def verified_elements(self) -> list:
        return [e for e in self.elements if (e.get("verified") if isinstance(e, dict) else e.verified)]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["elements"] = [e if isinstance(e, dict) else asdict(e) for e in self.elements]
        return d


def _as_elements(raw: list) -> list[dict]:
    out = []
    for e in raw or []:
        if isinstance(e, Element):
            out.append(asdict(e))
        elif isinstance(e, dict):
            out.append({"id": e.get("id", ""), "label": e.get("label", ""),
                        "region": e.get("region"), "verified": bool(e.get("verified", False))})
        else:
            raise TypeError(f"element must be dict/Element, got {type(e)}")
    return out


def declare(png: Path, still_id: str, elements: list, *, subject_type: str = "hero",
            role: str = "hero", ambient_layer: list | None = None,
            provenance: str = "fresh", declared_by: str = "design") -> dict:
    """Write the DECLARED (not-yet-verified) manifest. Elements start verified=False.
    No lock yet — reconcile() + lock() finish the contract."""
    assert subject_type in SUBJECT_TYPES, f"bad subject_type {subject_type!r}"
    assert role in ROLES, f"bad role {role!r}"
    m = ElementManifest(still_id=still_id, subject_type=subject_type, role=role,
                        elements=_as_elements(elements), ambient_layer=ambient_layer or [],
                        declared_by=declared_by, provenance=provenance, locked=False,
                        png_sha256=coherence.png_sha256(png) if Path(png).exists() else "")
    _write(png, m.to_dict())
    return m.to_dict()


def reconcile_and_lock(png: Path, *, verified_ids: list[str], period_real: dict,
                       note: str = "") -> dict:
    """RECONCILE the declared manifest against the real render then LOCK it.
    verified_ids = the element ids vision confirmed ARE present (others stay verified=False
    and are simply not tour-targetable — 'cut from the tour', not a re-render). period_real =
    {T1..T6: 'pass'|'fail'}. Lock requires the hash to bind to the current PNG."""
    d = read(png)
    if d is None:
        raise FileNotFoundError(f"no declared manifest for {png}")
    vset = set(verified_ids)
    for e in d["elements"]:
        e["verified"] = e["id"] in vset
    d["period_real"] = {k: period_real.get(k, "pass") for k in PERIOD_REAL_KEYS}
    d["png_sha256"] = coherence.png_sha256(png)
    d["locked"] = bool(d.get("elements")) and any(e["verified"] for e in d["elements"]) \
        and all(v == "pass" for v in d["period_real"].values())
    d["note"] = note
    _write(png, d)
    return d


def relock(png: Path, *, verified_ids: list[str] | None = None, period_real: dict | None = None,
           approved_by: str = "user", note: str = "approved re-render") -> dict:
    """Legal re-lock path after an APPROVED re-render: bump lock_version, re-stamp the hash,
    record approved_by. (A PNG whose bytes don't match png_sha256 with NO lock-version bump
    is a tamper -> is_locked returns False, fail-closed.)"""
    d = read(png)
    if d is None:
        raise FileNotFoundError(f"no manifest for {png}")
    if verified_ids is not None:
        vset = set(verified_ids)
        for e in d["elements"]:
            e["verified"] = e["id"] in vset
    if period_real is not None:
        d["period_real"] = {k: period_real.get(k, "pass") for k in PERIOD_REAL_KEYS}
    d["lock_version"] = int(d.get("lock_version", 1)) + 1
    d["png_sha256"] = coherence.png_sha256(png)
    d["approved_by"] = approved_by
    d["locked"] = any(e["verified"] for e in d["elements"])
    d["note"] = note
    _write(png, d)
    return d


def _write(png: Path, d: dict) -> Path:
    p = manifest_path(png)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def declare_from_scene_plan(short_dir: Path, provider: str = "nbp") -> list[str]:
    """The automated DECLARE step: promote a short's scene_plan macro_elements (or vignettes
    for multi-story scenes) into a DECLARED manifest per rendered still. Reconcile/lock still
    needs the per-render vision look — this only writes the not-yet-verified contract so the
    cut-planner + gate have something to ground against. Returns the still names declared."""
    short_dir = Path(short_dir)
    sp = json.loads((short_dir / "visual" / "scene_plan.json").read_text(encoding="utf-8"))
    scenes = (sp.get("plan", {}) or {}).get("scenes") or sp.get("scenes") or []
    nbp = short_dir / "visual" / provider
    out: list[str] = []
    for s in scenes:
        idx, slug = s.get("index"), s.get("slug", "")
        png = nbp / f"{idx:02d}_{slug}.png"
        if not png.exists():
            continue
        if is_locked(png):          # never clobber an already-locked manifest (idempotent)
            out.append(f"{png.name} (already locked — skipped)")
            continue
        vigs = s.get("vignettes") or []
        subject_type = "multi-story" if len(vigs) >= 3 else "hero"
        role = s.get("viral_role") if s.get("viral_role") in ROLES else \
            ("multi-story" if subject_type == "multi-story" else "hero")
        elements = [{"id": "full", "label": s.get("title") or "the full composition"}]
        seen = {"full"}
        for e in (vigs if subject_type == "multi-story" else (s.get("macro_elements") or [])):
            label = e if isinstance(e, str) else (e.get("name") or e.get("label") or str(e))
            eid = (re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:24]) or f"e{len(elements)}"
            if eid in seen:
                eid = f"{eid}-{len(elements)}"
            seen.add(eid)
            elements.append({"id": eid, "label": label})
        declare(png, png.stem, elements, subject_type=subject_type, role=role)
        out.append(png.name)
    return out


def read(png: Path) -> dict | None:
    p = manifest_path(png)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def is_locked(png: Path) -> bool:
    """Locked AND the hash binds to the current PNG (anti-tamper, fail-closed)."""
    d = read(png)
    if not d or not d.get("locked"):
        return False
    rec = d.get("png_sha256") or ""
    return bool(rec) and Path(png).exists() and rec == coherence.png_sha256(png)


def verified_ids(png: Path) -> list[str]:
    d = read(png)
    if not d:
        return []
    return [e["id"] for e in d.get("elements", []) if e.get("verified")]


def verified_labels(png: Path) -> list[str]:
    """The labels the edit may target AND the clip gate checks frames against (verified only)."""
    d = read(png)
    if not d:
        return []
    labels = [e["label"] for e in d.get("elements", []) if e.get("verified")]
    return labels + list(d.get("ambient_layer", []))


if __name__ == "__main__":
    import sys
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) >= 2 and args[0] == "show":
        d = read(Path(args[1]))
        if not d:
            print("no manifest")
        else:
            print(json.dumps(d, indent=2, ensure_ascii=False))
            print(f"\nlocked={is_locked(Path(args[1]))}  verified={verified_ids(Path(args[1]))}")
        raise SystemExit(0)
    if len(args) >= 2 and args[0] == "declare-short":
        names = declare_from_scene_plan(Path(args[1]))
        print(f"declared {len(names)} manifests (UNVERIFIED — reconcile/lock at render):")
        for n in names:
            print(f"  {n}")
        raise SystemExit(0)
    print("usage: python -m pipeline.element_manifest show <png> | declare-short <short folder>")
