"""cli_library.py — drive the centralized HERO-STILLS LIBRARY.

Subcommands:
  seed                      harvest the shipped stills (eps 12/16/18) + tag + index.html   (free)
  status                    print library contents
  select  "<v1>" [...]      paper: choose library stills per episode + list gaps           (free, agent-mode)
  gaps    [--apply]         generate the deduped new stills across all pending selections  (metered HF)
  animate [--apply]         animate uncached selected library stills ONCE (Kling)           (metered)
  materialize "<v1>" [...]  copy selected stills into each episode + write scene_plan.json   (free)
  index                     rebuild index.html                                              (free)

Selections are written to <v1>/visual/_library_selection.json (the GATE-1 artifact).
Metered steps require --apply (otherwise they print what they WOULD do).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import config
from pipeline import hero_library as HL


def _v1(p: str) -> Path:
    path = Path(p)
    if path.name != "v1" and (path / "v1").exists():
        path = path / "v1"
    if not (path / "narration.md").exists():
        raise SystemExit(f"not a narration v1 folder (no narration.md): {path}")
    return path


def _gap_is_pivot(g: dict) -> bool:
    return HL.is_gospel_pivot({
        "arc_position": g.get("arc_position", ""),
        "jesus_variant": g.get("jesus_variant"),
        "title": g.get("title", ""),
    })


def _resolve_and_validate(doc: dict, entries: list[dict]) -> dict:
    """Normalize the LLM selection doc into ordered_slugs + hero_slug + validation."""
    gaps = {g["slug_hint"].strip().lower(): g for g in doc.get("gaps", [])}
    ordered: list[str] = []
    for slot in doc.get("selection", []):
        sid = (slot.get("id") or "").strip().lower()
        if sid:
            ordered.append(sid)
        else:
            ref = (slot.get("gap_ref") or "").strip().lower()
            ordered.append(ref)
    hero = (doc.get("hero_id") or "").strip().lower()

    def pivot(slug: str) -> bool:
        e = HL.by_slug(entries, slug)
        if e:
            return bool(e.get("gospel_pivot"))
        if slug in gaps:
            return _gap_is_pivot(gaps[slug])
        return False

    dupes = [s for s in set(ordered) if ordered.count(s) > 1]
    val = {
        "unique_within_episode": not dupes,
        "duplicate_slugs": dupes,
        "hero_in_cut": hero in ordered,
        "hero_is_gospel_pivot": pivot(hero),
        "cross_or_christ_present": any(pivot(s) for s in ordered),
        "clip_count": len(ordered),
    }
    val["PASS"] = (val["unique_within_episode"] and val["hero_in_cut"]
                   and val["hero_is_gospel_pivot"] and val["cross_or_christ_present"])
    return {
        "reading": doc.get("reading", ""),
        "ordered_slugs": ordered,
        "hero_slug": hero,
        "selection": doc.get("selection", []),
        "gaps": list(gaps.values()),
        "validation": val,
    }


def cmd_seed(args):
    HL.harvest()
    HL.write_index_html()


def cmd_status(args):
    entries = HL.load()
    n_mp4 = sum(1 for e in entries if e.get("mp4"))
    n_pivot = sum(1 for e in entries if e.get("gospel_pivot"))
    print(f"library: {len(entries)} stills · {n_mp4} animated · {n_pivot} gospel-pivot")
    for e in entries:
        print(f"  {e['slug']:<34} {('mp4' if e.get('mp4') else 'png'):<4} "
              f"{e.get('viral_role') or '-':<9} {e.get('arc_position') or '-':<20} "
              f"{'PIVOT' if e.get('gospel_pivot') else ''}")


def cmd_select(args):
    entries = HL.load()
    if not entries:
        raise SystemExit("library empty — run `seed` first")
    all_gaps: dict[str, dict] = {}
    for p in args.folders:
        v1 = _v1(p)
        print(f"\n=== select: {v1.parent.name} ===")
        doc = HL.select_for_episode(v1, entries, target_clips=args.clips)
        norm = _resolve_and_validate(doc, entries)
        out = v1 / "visual" / "_library_selection.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(norm, indent=2, ensure_ascii=False), encoding="utf-8")
        v = norm["validation"]
        print(f"  ordered: {norm['ordered_slugs']}")
        print(f"  hero:    {norm['hero_slug']}")
        print(f"  gaps:    {[g['slug_hint'] for g in norm['gaps']]}")
        print(f"  GATE: {'PASS' if v['PASS'] else 'FAIL'} {v}")
        for g in norm["gaps"]:
            all_gaps.setdefault(g["slug_hint"].strip().lower(), g)
        print(f"  -> {out}")
    print(f"\nDEDUP'd GAP LIST across all episodes ({len(all_gaps)} new stills to generate):")
    for slug, g in all_gaps.items():
        print(f"  - {slug}  [{g.get('arc_position','?')}/{g.get('viral_role','?')}] {g.get('title','')}")


def _pending_selections(folders: list[str]) -> list[tuple[Path, dict]]:
    out = []
    for p in folders:
        v1 = _v1(p)
        sel = v1 / "visual" / "_library_selection.json"
        if sel.exists():
            out.append((v1, json.loads(sel.read_text(encoding="utf-8"))))
    return out


def cmd_gaps(args):
    sels = _pending_selections(args.folders)
    all_gaps: dict[str, dict] = {}
    for _, norm in sels:
        for g in norm.get("gaps", []):
            all_gaps.setdefault(g["slug_hint"].strip().lower(), g)
    print(f"{len(all_gaps)} deduped gap stills to generate (provider={args.provider}):")
    for slug in all_gaps:
        print(f"  - {slug}")
    if not args.apply:
        print("\n(dry run — pass --apply to generate; metered HF spend)")
        return
    HL.generate_gaps(list(all_gaps.values()), provider_name=args.provider)
    HL.write_index_html()


def cmd_animate(args):
    sels = _pending_selections(args.folders)
    entries = HL.load()
    used: list[str] = []
    for _, norm in sels:
        for s in norm.get("ordered_slugs", []):
            if s not in used:
                used.append(s)
    uncached = [s for s in used if not (HL.by_slug(entries, s) or {}).get("mp4")]
    print(f"{len(used)} stills used across episodes · {len(uncached)} need animation:")
    for s in uncached:
        print(f"  - {s}")
    if not args.apply:
        print("\n(dry run — pass --apply to animate; metered Kling spend)")
        return
    HL.animate_uncached(uncached)
    HL.write_index_html()


def cmd_materialize(args):
    for v1, norm in _pending_selections(args.folders):
        print(f"\n=== materialize: {v1.parent.name} ===")
        HL.materialize_into_episode(v1, args.provider, norm["ordered_slugs"], norm["hero_slug"])
    HL.write_index_html()


def cmd_index(args):
    HL.write_index_html()


def cmd_index_all(args):
    HL.write_master_index()


def main():
    ap = argparse.ArgumentParser(description="Centralized hero-stills library")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("seed").set_defaults(func=cmd_seed)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("index").set_defaults(func=cmd_index)
    sub.add_parser("index-all").set_defaults(func=cmd_index_all)

    sp = sub.add_parser("select"); sp.add_argument("folders", nargs="+")
    sp.add_argument("--clips", type=int, default=8); sp.set_defaults(func=cmd_select)

    gp = sub.add_parser("gaps"); gp.add_argument("folders", nargs="+")
    gp.add_argument("--apply", action="store_true")
    gp.add_argument("--provider", default=config.VISUAL_DEFAULT_PROVIDER); gp.set_defaults(func=cmd_gaps)

    an = sub.add_parser("animate"); an.add_argument("folders", nargs="+")
    an.add_argument("--apply", action="store_true"); an.set_defaults(func=cmd_animate)

    mp = sub.add_parser("materialize"); mp.add_argument("folders", nargs="+")
    mp.add_argument("--provider", default="hf"); mp.set_defaults(func=cmd_materialize)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
