"""Still DEDUP + canonical-reuse pass (v2/COHERENCE_GATE_SPEC.md companion).

The user spotted the pipeline RE-RENDERING the same concept across shorts instead of reusing
one good plate ('a-thousand-years-apart' rendered 7x). This finds those near-duplicates and
picks ONE canonical (best-quality, coherence-verified) per cluster, so the rebuild happens
ONCE and every short reuses it.

How:
  - dhash(png): a 64-bit perceptual hash (gradient of a 9x8 grayscale) — robust to small
    render/lighting differences, so it catches look-alikes with DIFFERENT filenames too.
  - cluster(): union near-identical stills (Hamming distance <= threshold). Exact-slug
    duplicates are forced into the same cluster regardless of pixels.
  - pick_canonical(): per cluster, prefer a coherence-verified PASS, then a non-flagged still,
    then the largest file (most detail).
  - build_report(): writes dedup_clusters.json + a clusters_review.html for human sign-off.

No new dependency (PIL + numpy are already used by the render stage).

Run: .venv\\Scripts\\python.exe -m pipeline.dedup            # scan + report
     .venv\\Scripts\\python.exe -m pipeline.dedup --threshold 8
"""
from __future__ import annotations
import html
import json
from pathlib import Path

import numpy as np
from PIL import Image

from pipeline import coherence

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "v2" / "coherence_audit"
DEFAULT_THRESHOLD = 10           # max Hamming distance (of 64 bits) to call two stills the same
HASH_SIZE = 8


def dhash(png: Path, hash_size: int = HASH_SIZE) -> int:
    """64-bit difference hash: compare adjacent pixels of a (size+1 x size) grayscale."""
    img = Image.open(png).convert("L").resize((hash_size + 1, hash_size), Image.LANCZOS)
    px = np.asarray(img, dtype=np.int16)
    diff = px[:, 1:] > px[:, :-1]          # row-wise gradient -> hash_size*hash_size bits
    bits = 0
    for b in diff.flatten():
        bits = (bits << 1) | int(b)
    return bits


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def _slug(p: Path) -> str:
    """The concept slug: filename minus the NN_ index prefix and extension."""
    stem = p.stem
    parts = stem.split("_", 1)
    return parts[1] if len(parts) == 2 and parts[0].isdigit() else stem


def sweep_stills() -> list[Path]:
    out: list[Path] = []
    for base in ("longform", "v2/pilot"):
        for p in (ROOT / base).rglob("*.png"):
            s = str(p).replace("\\", "/")
            if "/visual/" not in s:
                continue
            if any(t in s for t in ("_qc", "_old", "_rejected", "_clipqc", "/refs/", "/_audit")):
                continue
            out.append(p)
    for base in ("image_library", "_library"):
        for p in (ROOT / base).rglob("*.png"):
            s = str(p).replace("\\", "/")
            if any(t in s for t in ("_qc", "/refs/")):
                continue
            out.append(p)
    return sorted(set(out))


def cluster(paths: list[Path], threshold: int = DEFAULT_THRESHOLD) -> list[list[Path]]:
    """Union-find clustering. Two stills join if (a) same concept slug, OR (b) perceptual
    Hamming distance <= threshold. Returns clusters with >= 2 members only."""
    hashes: dict[Path, int] = {}
    for p in paths:
        try:
            hashes[p] = dhash(p)
        except Exception:  # noqa - unreadable image: skip from clustering
            continue
    items = list(hashes)
    parent = {p: p for p in items}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    # (a) exact-slug duplicates
    by_slug: dict[str, list[Path]] = {}
    for p in items:
        by_slug.setdefault(_slug(p), []).append(p)
    for grp in by_slug.values():
        for q in grp[1:]:
            union(grp[0], q)
    # (b) perceptual near-duplicates (O(n^2); n~185 is fine)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if hamming(hashes[items[i]], hashes[items[j]]) <= threshold:
                union(items[i], items[j])

    groups: dict[Path, list[Path]] = {}
    for p in items:
        groups.setdefault(find(p), []).append(p)
    return [sorted(g) for g in groups.values() if len(g) > 1]


def _flagged_bad() -> set[str]:
    f = OUT_DIR / "flagged_bad.json"
    if not f.exists():
        return set()
    try:
        rels = json.loads(f.read_text(encoding="utf-8")).get("flagged_bad", [])
    except (OSError, ValueError):
        return set()
    return {str((ROOT / r).resolve()).replace("\\", "/") for r in rels}   # resolve: match sweep paths


def _audit_failed(p: Path) -> bool:
    """True if the coherence sidecar exists, was audited, and did NOT pass."""
    sc = Path(p).with_suffix(Path(p).suffix + ".coherence.json")
    if not sc.exists():
        return False
    try:
        d = json.loads(sc.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return bool(d.get("audited")) and not d.get("passed")


def pick_canonical(members: list[Path], flagged: set[str]) -> Path:
    """Best member, in priority: coherence-verified PASS > not-audit-FAILED > not-user-flagged >
    largest file. A canonical must never be a still that itself failed the gate (INV-24 — no
    laundering a FAIL into the reuse registry)."""
    def score(p: Path) -> tuple:
        verified = coherence.is_verified(p)
        not_failed = not _audit_failed(p)
        not_flagged = str(p.resolve()).replace("\\", "/") not in flagged
        size = p.stat().st_size if p.exists() else 0
        return (verified, not_failed, not_flagged, size)
    return max(members, key=score)


def build_report(threshold: int = DEFAULT_THRESHOLD) -> dict:
    stills = sweep_stills()
    flagged = _flagged_bad()
    clusters = cluster(stills, threshold)
    clusters.sort(key=len, reverse=True)

    report = {"threshold": threshold, "total_stills": len(stills),
              "clusters": [], "duplicate_stills": 0, "avoidable_renders": 0}
    for members in clusters:
        canon = pick_canonical(members, flagged)
        rel = lambda p: str(p.relative_to(ROOT)).replace("\\", "/")
        report["clusters"].append({
            "slug": _slug(canon),
            "size": len(members),
            "canonical": rel(canon),
            "canonical_verified": coherence.is_verified(canon),
            "members": [{"path": rel(m),
                         "coherence": "PASS" if coherence.is_verified(m) else coherence.verdict_reason(m),
                         "flagged_bad": str(m).replace("\\", "/") in flagged,
                         "is_canonical": m == canon} for m in members],
        })
        report["duplicate_stills"] += len(members)
        report["avoidable_renders"] += len(members) - 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "dedup_clusters.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    _write_html(report)
    # the canonical-reuse registry: ONLY clusters whose canonical is coherence-verified PASS
    # (never advertise a still that itself failed the gate — that would launder a FAIL into reuse).
    registry = {c["slug"]: c["canonical"] for c in report["clusters"] if c["canonical_verified"]}
    needs_rebuild = [c["slug"] for c in report["clusters"] if not c["canonical_verified"]]
    (OUT_DIR / "canonical_concepts.json").write_text(
        json.dumps({"_README": "concept slug -> canonical coherence-verified still to REUSE "
                    "(rebuild once, reuse everywhere). Only VERIFIED canonicals are listed; "
                    "concepts whose every copy failed the gate are in 'needs_rebuild'. Built by pipeline/dedup.py.",
                    "canonical": registry, "needs_rebuild": needs_rebuild},
                   indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def _write_html(report: dict) -> Path:
    rows = []
    for c in report["clusters"]:
        cards = []
        for m in c["members"]:
            src = "file:///" + str(ROOT / m["path"]).replace("\\", "/")
            badge = "CANONICAL ✓" if m["is_canonical"] else "→ reuse canonical"
            cls = "canon" if m["is_canonical"] else "dup"
            coh = m["coherence"]
            cohcls = "pass" if coh == "PASS" else "fail"
            flag = '<span class="flag">🚩 you flagged</span>' if m["flagged_bad"] else ""
            cards.append(f'''<div class="m {cls}">
   <img loading="lazy" src="{html.escape(src)}">
   <div class="cap"><b>{badge}</b> <span class="b {cohcls}">{coh}</span>{flag}
     <div class="pp">{html.escape(m["path"])}</div></div></div>''')
        rows.append(f'''<div class="cluster"><h3>{html.escape(c["slug"])}
   <span class="n">×{c["size"]} — {c["size"]-1} render(s) avoidable</span></h3>
   <div class="mrow">{''.join(cards)}</div></div>''')
    doc = f'''<!doctype html><html><head><meta charset="utf-8"><title>Duplicate stills — canonical picks</title>
<style>
 body{{font-family:system-ui,Arial;margin:0;background:#14161a;color:#e8e6e0}}
 .bar{{position:sticky;top:0;background:#0d0f12;border-bottom:1px solid #333;padding:14px 18px}}
 .bar b{{font-size:18px}} .big{{color:#ffd24d;font-size:22px;font-weight:700}}
 .cluster{{padding:10px 18px;border-bottom:1px solid #23262e}}
 h3{{font-size:16px;margin:10px 0 8px}} .n{{color:#ff9}}
 .mrow{{display:flex;flex-wrap:wrap;gap:12px}}
 .m{{width:240px;border:3px solid #2a2e36;border-radius:9px;overflow:hidden;background:#1d2026}}
 .m.canon{{border-color:#ffd24d;box-shadow:0 0 0 2px #ffd24d inset}}
 .m img{{width:100%;display:block;background:#000}}
 .cap{{padding:7px 9px;font-size:12px}} .pp{{font-family:monospace;font-size:9px;color:#7fa;word-break:break-all;margin-top:4px;user-select:all}}
 .b{{padding:1px 6px;border-radius:4px;font-weight:700}} .pass{{background:#1c3;color:#031}} .fail{{background:#f44;color:#fff}}
 .flag{{background:#ff3b3b;color:#fff;padding:1px 6px;border-radius:4px;margin-left:5px}}
</style></head><body>
<div class="bar"><b>Duplicate concepts — pick canonical, rebuild once, reuse everywhere</b><br>
 <span class="big">{report["duplicate_stills"]} stills in {len(report["clusters"])} clusters · {report["avoidable_renders"]} renders avoidable</span>
 &nbsp;(gold = the canonical the registry will reuse)</div>
{''.join(rows)}
</body></html>'''
    p = OUT_DIR / "clusters_review.html"
    p.write_text(doc, encoding="utf-8")
    return p


if __name__ == "__main__":
    import sys
    th = DEFAULT_THRESHOLD
    if "--threshold" in sys.argv:
        th = int(sys.argv[sys.argv.index("--threshold") + 1])
    rep = build_report(th)
    print(f"{rep['duplicate_stills']} duplicate stills in {len(rep['clusters'])} clusters; "
          f"{rep['avoidable_renders']} renders avoidable (threshold={th}).")
    print(f"  -> {OUT_DIR / 'dedup_clusters.json'}")
    print(f"  -> {OUT_DIR / 'canonical_concepts.json'}")
    print(f"  -> {OUT_DIR / 'clusters_review.html'}")
