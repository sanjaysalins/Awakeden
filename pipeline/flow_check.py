"""flow_check — deterministic morph/melt pre-filter for animated clips ($0, no LLM).

A frozen tableau under CAMERA-ONLY motion (push-in, crop-cut, crane) relates any two
frames by a global affine transform: after compensating the camera, the residual
difference is near zero. Morphing/melting/subject motion (limbs moving, faces
redrawing, AI-invented detail) survives the compensation as residual.

Verdicts (fail-open to the vision layer, never fail-closed):
  PASS      — residual below threshold on every sampled pair: camera-only, no vision
              call needed for the FROZEN/NOMORPH axes (composition axes still apply).
  ESCALATE  — high residual or the affine fit failed: send to the vision QC
              (pipeline/clip_anim_qc). NOT a fail verdict — dancing subjects and
              deliberate effects also land here.

Writes <clip>.flowqc.json beside the clip (metrics + verdict + threshold).

  .venv\\Scripts\\python.exe -m pipeline.flow_check "<clip.mp4>" [--threshold 0.045]
  .venv\\Scripts\\python.exe -m pipeline.flow_check "<clips dir>"          # sweep
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np

# Calibration (2026-07-08, into_thy_hands pool + synthetics, edge-map metric):
#   clean camera-only clips:      max 0.010-0.035, worst_block < 0.23
#   ambient-life clips (lightning pulses, light rays — human-passed): max 0.05-0.10
#   synthetic dissolve morph:     max 0.115, worst_block 0.31
# PASS is dual-gated (strict max, OR moderate max + low block) so a PASS is
# bulletproof; ambient-life clips deliberately ESCALATE to the vision layer —
# fail-open by design, never fail-closed.
DEFAULT_THRESHOLD = 0.045          # strict max-residual gate
SOFT_MAX = 0.07                    # moderate max…
SOFT_BLOCK = 0.15                  # …allowed only with a quiet worst block
N_FRAMES = 13
WORK_WIDTH = 480


def _sample_frames(mp4: Path, n: int = N_FRAMES) -> list[np.ndarray]:
    cap = cv2.VideoCapture(str(mp4))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total < 2:
        cap.release()
        raise ValueError(f"unreadable clip: {mp4}")
    idxs = np.linspace(0, total - 1, min(n, total)).astype(int)
    frames = []
    for i in idxs:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(i))
        ok, frame = cap.read()
        if not ok:
            continue
        g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = g.shape
        scale = WORK_WIDTH / w
        frames.append(cv2.resize(g, (WORK_WIDTH, int(h * scale))))
    cap.release()
    return frames


def _pair_residual(a: np.ndarray, b: np.ndarray) -> tuple[float, float] | None:
    """(mean, block_max) residual (0..1) between b and a warped by the best global
    HOMOGRAPHY — the art is a flat panel, so any camera move (push, crop-cut, arc,
    crane) is a plane-to-plane homography. Morph/melt survives the compensation.
    block_max = worst 1/8-grid block: real melt is LOCALIZED (a hand redrawing)
    and pops out of the block metric even when the global mean stays low.
    None = the fit failed (huge displacement / featureless)."""
    pts = cv2.goodFeaturesToTrack(a, maxCorners=400, qualityLevel=0.01, minDistance=8)
    if pts is None or len(pts) < 20:
        return None
    nxt, st, _err = cv2.calcOpticalFlowPyrLK(
        a, b, pts, None, winSize=(31, 31), maxLevel=5,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 40, 0.01))
    good = (st.reshape(-1) == 1)
    if good.sum() < 20:
        return None
    m, _inliers = cv2.findHomography(pts[good], nxt[good], cv2.RANSAC, 2.0)
    if m is None:
        return None
    warped = cv2.warpPerspective(a, m, (b.shape[1], b.shape[0]),
                                 flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    # EDGE-map residual, not intensity: Kling adds harmless lighting shimmer to a
    # frozen panel (intensity drifts), but the art is INKED LINE WORK — melt/morph
    # REDRAWS LINES. Sobel magnitude is illumination-invariant; a light gaussian
    # tolerates ~1px warp error.
    def edges(img: np.ndarray) -> np.ndarray:
        gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3)
        mag = cv2.magnitude(gx, gy)
        mag = cv2.GaussianBlur(mag, (5, 5), 0)
        return mag / max(float(mag.max()), 1e-6)

    # central 80% crop — border reflection artifacts stay out of the metric
    h, w = b.shape
    ch, cw = int(h * 0.1), int(w * 0.1)
    ea = edges(warped)[ch:h - ch, cw:w - cw]
    eb = edges(b)[ch:h - ch, cw:w - cw]
    diff = np.abs(ea - eb)
    mean = float(np.mean(diff))
    gh, gw = diff.shape[0] // 8, diff.shape[1] // 8
    blocks = [float(np.mean(diff[r * gh:(r + 1) * gh, c * gw:(c + 1) * gw]))
              for r in range(8) for c in range(8)]
    return mean, max(blocks)


def flow_metrics(mp4: Path) -> dict:
    frames = _sample_frames(Path(mp4))
    means, block_maxes, failed = [], [], 0
    # consecutive pairs catch fast melt; two HALF-RANGE anchor hops (first<->mid,
    # mid<->last) catch SLOW morph (a gradual dissolve changes little per pair but
    # is already different art by the midpoint — a camera-only clip shows the SAME
    # art throughout). Half hops keep the warp small enough that resampling error
    # doesn't drown the signal.
    pairs = list(zip(frames, frames[1:]))
    if len(frames) > 4:
        mid = len(frames) // 2
        pairs += [(frames[0], frames[mid]), (frames[mid], frames[-1])]
    for a, b in pairs:
        r = _pair_residual(a, b)
        if r is None:
            failed += 1
        else:
            means.append(round(r[0], 4))
            block_maxes.append(round(r[1], 4))
    return {"pairs": len(pairs), "failed_fits": failed,
            "mean_residuals": means, "block_max_residuals": block_maxes,
            "max_residual": max(means) if means else None,
            "mean_residual": round(float(np.mean(means)), 4) if means else None,
            "worst_block": max(block_maxes) if block_maxes else None}


def flow_check(mp4: Path, threshold: float = DEFAULT_THRESHOLD, write: bool = True) -> dict:
    mp4 = Path(mp4)
    m = flow_metrics(mp4)
    ok = (m["failed_fits"] == 0 and m["max_residual"] is not None
          and (m["max_residual"] <= threshold
               or (m["max_residual"] <= SOFT_MAX and m["worst_block"] <= SOFT_BLOCK)))
    rec = {"clip": mp4.name, "verdict": "PASS" if ok else "ESCALATE",
           "threshold": threshold, **m}
    if write:
        mp4.with_suffix(".flowqc.json").write_text(
            json.dumps(rec, indent=2), encoding="utf-8")
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="deterministic morph pre-filter")
    ap.add_argument("target", help="clip .mp4 or a directory of clips")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args(argv)
    t = Path(a.target)
    clips = sorted(t.glob("*.mp4")) if t.is_dir() else [t]
    n_esc = 0
    for c in clips:
        try:
            r = flow_check(c, a.threshold, write=not a.no_write)
        except Exception as e:  # noqa - report and move on in a sweep
            print(f"{c.name:40} ERROR {e}")
            n_esc += 1
            continue
        n_esc += r["verdict"] == "ESCALATE"
        print(f"{c.name:40} {r['verdict']:8} max={r['max_residual']} "
              f"worst_block={r['worst_block']} fails={r['failed_fits']}")
    print(f"\n{len(clips)} clip(s): {len(clips) - n_esc} PASS, {n_esc} ESCALATE (to vision QC)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
