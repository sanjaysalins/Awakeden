"""WAVE TOOLING (rollout A(a) deliverable, 2026-07-14) — the shared helpers the panel
required before any Wave A(b) spend. Reuses build_filmstrip (never a second QC stack).

  .venv\\Scripts\\python.exe -m pipeline.wave_tools backup    <piece_dir>
  .venv\\Scripts\\python.exe -m pipeline.wave_tools strips    <piece_dir> [slug ...]
  .venv\\Scripts\\python.exe -m pipeline.wave_tools compare   <piece_dir> t1,t2,...
  .venv\\Scripts\\python.exe -m pipeline.wave_tools checklist <piece_dir>
"""
import datetime
import json
import shutil
import subprocess
import sys
from pathlib import Path

CHECKLIST_ITEMS = [   # the un-gateable gold-master bars (ROLLOUT_PLAN.md human checklist)
    "scale_variety",          # CU + wide + detail + medium all present
    "grids_multi_figure",     # grids only on multi-figure stills; Christ singles full
    "audio_diff",             # spec beat sfx vs the piece's bed builder - no doubles
    "bookend",                # motion hook open, close on Christ
    "filmstrip_qc",           # every new clip strip-checked; rejects parked
    "before_after_review",    # compare page built and eyeballed
    "fit_gate_disposition",   # builder fit warnings reviewed and accepted/fixed
]


def final_mp4(piece_dir: Path) -> Path:
    return piece_dir / "visual" / f"{piece_dir.name}_sfx.mp4"


def backup_final(piece_dir: Path) -> Path | None:
    """Pre-rebuild backup (idempotent: first backup wins — it preserves the SHIPPED look)."""
    src = final_mp4(piece_dir)
    if not src.is_file():
        print(f"[backup] no final yet at {src.name} - nothing to back up")
        return None
    dst = src.with_name(src.stem + ".bak_prelivinglight.mp4")
    if dst.exists():
        print(f"[backup] already exists (kept): {dst}")
        return dst
    shutil.copy2(src, dst)
    print(f"[backup] {dst}")
    return dst


def strips(piece_dir: Path, slugs: list[str] | None = None) -> list[Path]:
    """Filmstrip every (or the named) clip into visual/_review/strips/ for the eye QC."""
    from pipeline.clip_anim_qc import build_filmstrip
    clips = piece_dir / "visual" / "clips"
    out_dir = piece_dir / "visual" / "_review" / "strips"
    out_dir.mkdir(parents=True, exist_ok=True)
    made = []
    for mp4 in sorted(clips.glob("*.mp4")):
        if slugs and mp4.stem not in slugs:
            continue
        strip = build_filmstrip(mp4, out_dir)
        if strip:
            made.append(strip)
            print(f"[strip] {strip}")
    return made


def compare_page(piece_dir: Path, times: list[float]) -> Path:
    """BEFORE/AFTER page: frames from the .bak_prelivinglight final vs the new final at
    the given timestamps, plus both videos. The wave-gate user review artifact."""
    vis = piece_dir / "visual"
    new = final_mp4(piece_dir)
    old = new.with_name(new.stem + ".bak_prelivinglight.mp4")
    out = vis / "_review" / "wave_compare"
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for t in times:
        pair = []
        for tag, src in (("before", old), ("after", new)):
            png = out / f"{tag}_{t}.png"
            if src.is_file():
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t),
                                "-i", str(src), "-frames:v", "1", str(png)], check=False)
            pair.append(f'<figure><img src="{png.name}"><figcaption>{tag} @ {t}s'
                        f'</figcaption></figure>' if png.exists() else
                        f"<figure><figcaption>{tag} @ {t}s (missing)</figcaption></figure>")
        rows.append(f'<div class="pair">{pair[0]}{pair[1]}</div>')
    html = out / "index.html"
    html.write_text(
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>Wave compare - {piece_dir.name}</title>"
        "<style>body{background:#1a1714;color:#eee8dc;font-family:Georgia,serif;margin:24px}"
        ".pair{display:flex;gap:12px;margin-bottom:14px}.pair img{width:300px;border-radius:6px}"
        "figure{margin:0}figcaption{font-size:13px;color:#b9ac93;text-align:center;padding:4px}"
        "video{width:340px;border-radius:8px;margin-right:12px}</style></head><body>"
        f"<h1>{piece_dir.name} - before / after</h1>" + "".join(rows) +
        f'<h2>Videos</h2><video controls src="../../{old.name}"></video>'
        f'<video controls src="../../{new.name}"></video></body></html>',
        encoding="utf-8")
    print(f"[compare] {html}")
    return html


def write_checklist(piece_dir: Path, reviewer: str = "sanjay") -> Path:
    """Seed visual/wave_checklist.json (all items pending). The wave gate flips them."""
    out = piece_dir / "visual" / "wave_checklist.json"
    if out.exists():
        print(f"[checklist] exists (kept): {out}")
        return out
    out.write_text(json.dumps({
        "piece": piece_dir.name,
        "created": datetime.date.today().isoformat(),
        "items": [{"name": n, "pass": None, "note": "", "reviewer": reviewer}
                  for n in CHECKLIST_ITEMS],
    }, indent=1), encoding="utf-8")
    print(f"[checklist] seeded {out}")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd, piece_dir = argv[0], Path(argv[1]).resolve()
    if cmd == "backup":
        backup_final(piece_dir)
    elif cmd == "strips":
        strips(piece_dir, argv[2:] or None)
    elif cmd == "compare":
        compare_page(piece_dir, [float(x) for x in argv[2].split(",")])
    elif cmd == "checklist":
        write_checklist(piece_dir)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
