"""Post-render CLIP QC — the teeth that catch Kling DISOBEYING the cut-plan.

The deterministic cut-plan gate (validators.gate_cutplan) stops the *prompt* from seeding
hallucination, but only a look at the rendered frames catches Kling actually inventing
motion/elements or melting a face. This module makes that a FAIL-CLOSED gate:

  - extract_frames(mp4)         : pull first/mid/last(+2) frames for a real look (deterministic).
  - CRITERIA                    : the rules a clip must satisfy (frozen / no-morph / on-scene / period).
  - record_verdict / is_verified: a clip is "verified" only once a PASSING <clip>.clipqc.json sidecar
                                  exists. No sidecar = UNVERIFIED (fail-closed) — it must not ship.

Run:  .venv\\Scripts\\python.exe -m pipeline.clip_qc "<short folder>"   # status of every clip
      .venv\\Scripts\\python.exe -m pipeline.clip_qc "<short folder>" --frames   # also dump QC frames
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

CRITERIA = (
    "A rendered Kling clip PASSES only if, across its frames:\n"
    "  1. FROZEN: nothing inside the painting moves, flows, brightens, bleeds, or appears. "
    "Only the camera crops/reframes. No invented blood, water, light, lava, fire, smoke, or new element.\n"
    "  2. NO-MORPH: faces, hands, and forms stay stable frame-to-frame; no melting, warping, "
    "halo-bloom, or morphing.\n"
    "  3. ON-SCENE: every frame is a crop of the SAME painting (the scene), not a different image.\n"
    "  4. PERIOD/TONE: still reads as a reverent period Baroque oil (no modern/horror/NSFW drift).\n"
    "FAIL if any frame violates these. Fail-closed: when unsure, FAIL."
)


def extract_frames(mp4: Path, out_dir: Path, n: int = 12) -> list[Path]:
    """Extract n frames spread across the clip (first .. last) for a real look."""
    out_dir.mkdir(parents=True, exist_ok=True)
    dur = _duration(mp4)
    if dur <= 0:
        return []
    stem = mp4.stem
    paths: list[Path] = []
    for i in range(n):
        # spread from ~0.2s to ~ (dur-0.3s)
        t = 0.2 + (dur - 0.5) * (i / (n - 1)) if n > 1 else dur / 2
        p = out_dir / f"{stem}_qc{i}.jpg"
        subprocess.run(["ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(mp4),
                        "-frames:v", "1", str(p), "-loglevel", "error"], check=False)
        if p.exists():
            paths.append(p)
    return paths


def _duration(mp4: Path) -> float:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(mp4)],
            capture_output=True, text=True, check=False).stdout.strip()
        return float(out)
    except (ValueError, OSError):
        return 0.0


def _sidecar(mp4: Path) -> Path:
    return mp4.with_suffix(mp4.suffix + ".clipqc.json")


def record_verdict(mp4: Path, passed: bool, issues: list | None = None, note: str = "") -> Path:
    """Write the fail-closed QC sidecar after a real look."""
    sc = _sidecar(mp4)
    sc.write_text(json.dumps({"passed": bool(passed), "issues": issues or [], "note": note},
                             ensure_ascii=False, indent=1), encoding="utf-8")
    return sc


def is_verified(mp4: Path) -> bool:
    """A clip is verified ONLY if a passing sidecar exists (fail-closed)."""
    sc = _sidecar(mp4)
    if not sc.exists():
        return False
    try:
        return bool(json.loads(sc.read_text(encoding="utf-8")).get("passed"))
    except (OSError, ValueError):
        return False


LF_CRITERIA = (
    "A rendered veo3 LONG-FORM clip PASSES only if, across its frames (LF-CLIP-*, "
    "v2/LONGFORM_SPEC.md §4):\n"
    "  1. ATMOSPHERE-ONLY: motion is atmospheric (drifting dust/smoke/light, cloth "
    "stirring, flame wavering) — never subject locomotion (no walking, running, "
    "reaching, striking; figures may breathe or turn slightly).\n"
    "  2. NO-MORPH: faces, hands, and forms stay stable frame-to-frame; no melting, "
    "warping, or morphing.\n"
    "  3. NO-INVENT: nothing appears that isn't in the source still — no invented "
    "blood, water, figures, objects, or text.\n"
    "  4. STYLE-FAITHFUL: every frame keeps the source still's art style (inked "
    "graphic-novel or Baroque oil per episode) — no photoreal softening.\n"
    "  5. NO-WRITING-ANIMATED: scroll/titulus/sign content never animates (INV-17).\n"
    "FAIL if any frame violates these. Fail-closed: when unsure, FAIL."
)


def _status_row(mp4: Path) -> dict:
    sc = _sidecar(mp4)
    if not sc.exists():
        state = "UNVERIFIED"
    else:
        try:
            state = "PASS" if json.loads(sc.read_text(encoding="utf-8")).get("passed") else "FAIL"
        except (OSError, ValueError):
            state = "BAD-SIDECAR"
    return {"clip": mp4.name, "state": state}


def short_status(short_folder: Path, provider: str = "nbp") -> list[dict]:
    """Status of every rendered clip in a short: verified / unverified / failed."""
    return dir_status(short_folder / "visual" / provider)


def dir_status(clips_dir: Path) -> list[dict]:
    """Status of every clip in ANY directory (the long-form 16:9 lane keeps its
    clips at <episode>/v1/visual_16x9*/(clips/)?NN_*.mp4 — pass that dir here).
    Added 2026-07-19 so the long lane shares the same fail-closed sidecar
    discipline instead of the assemble-long skill claiming a chokepoint nothing
    read."""
    return [_status_row(mp4) for mp4 in sorted(clips_dir.glob("*.mp4"))]


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dump = "--frames" in sys.argv
    long_mode = "--dir" in sys.argv   # pass a clips DIR directly (long-form 16:9 lane)
    if not args:
        print("usage: python -m pipeline.clip_qc <short folder> [--frames]\n"
              "       python -m pipeline.clip_qc <clips dir> --dir [--frames]   # long-form")
        raise SystemExit(2)
    folder = Path(args[0])
    clips_dir = folder if long_mode else folder / "visual" / "nbp"
    rows = dir_status(clips_dir)
    unv = [r for r in rows if r["state"] != "PASS"]
    for r in rows:
        print(f"  [{r['state']:>11}] {r['clip']}")
    print(f"\n{len(rows)-len(unv)}/{len(rows)} clips verified PASS; {len(unv)} need a look.")
    print("\nCRITERIA:\n" + (LF_CRITERIA if long_mode else CRITERIA))
    if dump:
        qc = clips_dir / "_clipqc_frames"
        for mp4 in sorted(clips_dir.glob("*.mp4")):
            extract_frames(mp4, qc)
        print(f"\nframes -> {qc}")
