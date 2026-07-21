"""Refresh the per-clips-dir _CLIPQC_REVIEW.html galleries after the qcfix promotions.

The 2026-07-19 backfill galleries were built by a (lost) scratchpad script; their
_clipqc_frames/ filmstrips still show the OLD defective clips for every slug promoted
during the repair batch. This script:
  1. re-extracts the 12-frame filmstrip for any clip whose mp4 is newer than its qc0
     frame (or has no frames yet),
  2. rebuilds _CLIPQC_REVIEW.html from the CURRENT .clipqc.json sidecars (FAILs first),
     same card format as the 2026-07-19 original.

$0, ffmpeg/ffprobe only. EW01 is archived and deliberately not touched.
"""
import html
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CLIP_DIRS = [
    ROOT / "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked/clips",
    ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked/clips",
    ROOT / "longform/04_The_Bronze_Serpent/v1/visual_16x9_inked/clips",
]
N_FRAMES = 12


def ffprobe_duration(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def extract_frames(mp4: Path, frames_dir: Path, slug: str) -> None:
    dur = ffprobe_duration(mp4)
    for i in range(N_FRAMES):
        t = min(dur * i / (N_FRAMES - 1), max(dur - 0.05, 0.0))
        out = frames_dir / f"{slug}_qc{i}.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
             "-frames:v", "1", "-vf", "scale=-1:270", "-q:v", "4", str(out)],
            check=True)


def build_gallery(clips_dir: Path) -> tuple[int, int, int]:
    frames_dir = clips_dir / "_clipqc_frames"
    frames_dir.mkdir(exist_ok=True)
    cards, refreshed = [], 0
    for mp4 in sorted(clips_dir.glob("*.mp4")):
        if mp4.name.startswith("_"):
            continue
        sc = clips_dir / f"{mp4.name}.clipqc.json"
        if not sc.is_file():
            print(f"  [skip] no sidecar: {mp4.name}")
            continue
        v = json.loads(sc.read_text(encoding="utf-8"))
        slug = mp4.stem
        qc0 = frames_dir / f"{slug}_qc0.jpg"
        if not qc0.exists() or mp4.stat().st_mtime > qc0.stat().st_mtime:
            print(f"  [frames] {slug}")
            extract_frames(mp4, frames_dir, slug)
            refreshed += 1
        cards.append((bool(v.get("passed")), slug, mp4.name,
                      v.get("issues") or [], v.get("note", "")))

    fails = [c for c in cards if not c[0]]
    passes = [c for c in cards if c[0]]
    body = []
    for passed, slug, name, issues, note in fails + passes:
        cls, badge = ("", "pass") if passed else ("fail", "fail")
        issues_html = (f"<div class='issues'>{html.escape('; '.join(issues))}</div>"
                       if issues else "")
        strip = "".join(
            f'<img src="_clipqc_frames/{slug}_qc{i}.jpg">' for i in (0, 3, 6, 9, 11))
        body.append(
            f"<div class='card {cls}'><b>{html.escape(name)}</b> "
            f"<span class='badge {badge}'>{badge.upper()}</span>"
            f"{issues_html}"
            f"<div class='note'>{html.escape(note)}</div>"
            f"<div class='strip'>{strip}</div>"
            f"<video controls preload='none' src='{html.escape(name)}'></video></div>")

    n, nf = len(cards), len(fails)
    fail_txt = (f"<b style='color:#c0392b'>{nf} FAIL</b> (FAILs listed first)"
                if nf else "<b style='color:#3a7d44'>0 FAIL — all clips PASS</b>")
    page = (
        "<!doctype html><meta charset='utf-8'><title>clip QC — visual_16x9_inked</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;background:#14120f;color:#e8e2d5;margin:20px}\n"
        "h1{font-size:22px}.card{background:#1e1b16;border-radius:10px;padding:14px;margin:14px 0;\n"
        "border-left:6px solid #3a7d44}.card.fail{border-left-color:#c0392b}\n"
        ".badge{display:inline-block;padding:2px 10px;border-radius:12px;font-weight:700;font-size:13px}\n"
        ".badge.pass{background:#3a7d44}.badge.fail{background:#c0392b}\n"
        ".strip{display:flex;gap:4px;margin:8px 0;overflow-x:auto}\n"
        ".strip img{height:110px;border-radius:4px}\n"
        "video{max-width:640px;width:100%;border-radius:6px;margin-top:6px}\n"
        ".note{color:#b9b2a0;font-size:14px}.issues{color:#e67e22;font-size:14px}</style>"
        f"<h1>Clip QC — {clips_dir}</h1>"
        f"<p>{n} clips · {fail_txt}. Verdict sidecars are written; overriding a verdict "
        "= tell Claude or edit the .clipqc.json.</p>" + "".join(body))
    (clips_dir / "_CLIPQC_REVIEW.html").write_text(page, encoding="utf-8")
    return n, nf, refreshed


for d in CLIP_DIRS:
    print(f"\n== {d.parent.parent.parent.name} ==")
    n, nf, refreshed = build_gallery(d)
    print(f"  {n} clips, {nf} FAIL, {refreshed} filmstrips re-extracted")
    print(f"  -> {d / '_CLIPQC_REVIEW.html'}")
