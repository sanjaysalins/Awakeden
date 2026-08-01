#!/usr/bin/env python
"""margin_sentinel.py — the MARGIN SENTINEL ($0, deterministic).

The chink in the armour (Fable, round 3, 2026-07-30): the s09_rebuke signature
defect (Kling hallucinated a cursive signature-like mark into the blank paper
corner beside the wave spray, growing in from ~1s onward) shipped through FOUR
human review rounds and was only caught on a fifth, full-context eye-check.
Nothing in this project mechanically audits TIME -- the one dimension where
the animator invents. This gate is a structural detector with no drawing hand
at all: it can flag a hallucination, it cannot create one.

WHY THIS IS VALID: every clip in the living-sketchbook style is rendered
under a strict camera-lock prompt ("the camera does not move, zoom, or change
angle at all" -- see poc_living_sketchbook/storm/_s3_animate.py's LOCK
constant). That guarantee is what makes frame-0 registration valid across an
entire clip: nothing should ever shift position, so any pixel that reads as
blank paper in frame 0 should still read as blank paper in frame 119.

ALGORITHM
  1. Build a QUIET MASK from frame 0: pixels that (a) match this style's
     paper/kraft/gold palette in HSV, AND (b) sit in a locally FLAT
     neighbourhood (low Sobel edge energy -- ink linework is never flat).
     A size filter keeps only large contiguous flat-paper regions, so small
     bright ink highlights (foam flecks, spray droplets) that happen to pass
     the color test in isolation don't pollute the mask.
  2. For every later frame, diff against frame 0, restricted to the quiet
     mask, thresholded, morphologically opened (grain/compression noise
     removed).
  3. Track PER-PIXEL consecutive persistence (small grace window tolerates
     1-2 frame flicker). A hit requires the run to still be active at the
     LAST frame of the clip, having lasted >=0.5s -- not just "persisted for
     half a second at some point." This distinction is load-bearing: this
     style's own legitimate ambient motion (a wave sweeping into a corner
     margin then receding, a "breathing" light pulsing) can ALSO hold a
     quiet-mask region for well over 0.5s before it recedes back to frame-0
     baseline. A real Kling hallucination, once it grows in, never recedes --
     it holds to the end of the clip. Requiring survival to the final frame
     is what separates "the wave washed through and left" from "the mark is
     still there."
  4. Nearby hit components are merged (dilate + relabel) into one flagged
     region per event, then a short filmstrip (frame 0 + N samples across the
     hit's active window, cropped tight with padding) is exported as PNGs to
     a sibling `_sentinel/<clip-stem>/` folder for a human eye-check.

THIS IS A LEAD GENERATOR, NOT A VERDICT. It never modifies, mutes, or rejects
anything -- it only exports evidence and says "look here." Read-only over the
source clip; $0/deterministic (numpy + cv2 only, no model calls).

HONEST LIMITS (see .claude/skills/margin-sentinel/SKILL.md for the full
writeup): a hallucination fully inside busy drawing motion (an extra face in
wave chop) is invisible to this tool -- it only watches pixels that were
QUIET in frame 0. And this style's own "breathing golden glow" / "parting
clouds" ambient devices share blank-paper's pale, low-saturation, locally-flat
signature, so scenes built around a glow (s13_landing) or a soft cloud bank
(s11_exactly) will legitimately trip this gate; a human glancing at the
exported crop tells the difference in under a second (recognizable glow/cloud
content vs. a genuinely new ink mark on bare paper).

Usage:
    .venv\\Scripts\\python.exe margin_sentinel.py <clip.mp4> [<clip2.mp4> ...]
    .venv\\Scripts\\python.exe margin_sentinel.py <folder>       # scans every *.mp4 in it

Exit codes: 0 = no candidate hits on any clip scanned (quiet).
            1 = at least one candidate hit was exported -- go eye-check it.
            2 = nothing could be scanned (bad paths / unreadable video).
"""
from __future__ import annotations
import sys
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

# ---------------------------------------------------------------------------
# Quiet-mask calibration (from poc_living_sketchbook/storm/stills/*.png and
# the corresponding rendered clips -- cream margin, kraft torn-edge border,
# gold accent strip, and any large flat blank-paper interior all read as
# roughly H 13-21, S 25-90, V 185-255 in OpenCV HSV; dark ink/wave/cloud
# content reads V well below 170; a lower S bound (>=25) keeps the mask off
# near-white/desaturated content like pale cloud banks and light fabric).
# ---------------------------------------------------------------------------
PAPER_V_MIN = 170
PAPER_S_MIN = 25
PAPER_S_MAX = 150
EDGE_WINDOW = 11          # px, local-flatness averaging window
EDGE_FLAT_THRESH = 12.0   # local Sobel-magnitude ceiling to count as "flat"
MIN_QUIET_AREA_FRAC = 0.0008  # drop small paper-colored islands (foam highlights)

# ---------------------------------------------------------------------------
# Change detection + persistence
# ---------------------------------------------------------------------------
DIFF_THRESH = 40          # per-pixel max-channel abs diff vs frame 0
GRACE_SECONDS = 0.10      # tolerate this many seconds of dropout mid-run (flicker/compression)
MIN_PERSIST_SECONDS = 0.5 # the spec floor: must hold this long, unbroken, through clip end
MIN_HIT_AREA_PX = 250     # drop thin compression-edge slivers after persistence filtering
MERGE_RADIUS_PX = 50      # merge nearby flagged components into one reported hit

# ---------------------------------------------------------------------------
# Filmstrip export
# ---------------------------------------------------------------------------
FILMSTRIP_FRAMES = 5      # sampled frames across the hit's active window (plus a frame-0 reference)
CROP_PAD_PX = 40


@dataclass
class Hit:
    bbox: tuple          # (x, y, w, h) in the ORIGINAL (undilated) flagged pixels
    area_px: int
    first_frame: int
    fps: float

    @property
    def first_appear_s(self) -> float:
        return self.first_frame / self.fps


def _read_all_frames(clip_path: Path) -> tuple[list, float]:
    cap = cv2.VideoCapture(str(clip_path))
    if not cap.isOpened():
        raise IOError(f"could not open {clip_path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    frames = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        frames.append(f)
    cap.release()
    if not frames:
        raise IOError(f"no frames read from {clip_path}")
    return frames, fps


def build_quiet_mask(frame0: np.ndarray) -> np.ndarray:
    """Pixels that are BOTH paper-palette AND locally flat, restricted to
    large contiguous regions. Returns a uint8 0/255 mask same size as frame0."""
    hsv = cv2.cvtColor(frame0, cv2.COLOR_BGR2HSV)
    s = hsv[:, :, 1].astype(np.float32)
    v = hsv[:, :, 2].astype(np.float32)
    paper_color = (v >= PAPER_V_MIN) & (s >= PAPER_S_MIN) & (s <= PAPER_S_MAX)

    gray = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    local_edge = cv2.blur(cv2.magnitude(gx, gy), (EDGE_WINDOW, EDGE_WINDOW))
    flat = local_edge < EDGE_FLAT_THRESH

    candidate = (paper_color & flat).astype(np.uint8)

    n, lbl, stats, _ = cv2.connectedComponentsWithStats(candidate, connectivity=8)
    h, w = candidate.shape
    min_area = MIN_QUIET_AREA_FRAC * h * w
    mask = np.zeros_like(candidate)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            mask[lbl == i] = 255
    return mask


def _diff_map(frame0: np.ndarray, framei: np.ndarray) -> np.ndarray:
    return np.abs(framei.astype(np.int16) - frame0.astype(np.int16)).max(axis=2).astype(np.uint8)


def find_hits(clip_path: Path) -> tuple[list[Hit], float, int]:
    """Scan one clip. Returns (hits, fps, n_frames)."""
    frames, fps = _read_all_frames(clip_path)
    frame0 = frames[0]
    mask = build_quiet_mask(frame0)
    kernel = np.ones((3, 3), np.uint8)
    grace_frames = max(1, round(GRACE_SECONDS * fps))
    persist_frames = max(1, round(MIN_PERSIST_SECONDS * fps))

    h, w = mask.shape
    consec = np.zeros((h, w), np.int32)
    grace_left = np.zeros((h, w), np.int32)
    run_start = np.zeros((h, w), np.int32)

    for t in range(1, len(frames)):
        d = _diff_map(frame0, frames[t])
        changed = ((d > DIFF_THRESH) & (mask > 0)).astype(np.uint8) * 255
        changed = cv2.morphologyEx(changed, cv2.MORPH_OPEN, kernel, iterations=1) > 0

        new_run = changed & (consec == 0)
        run_start[new_run] = t
        consec[changed] += 1
        grace_left[changed] = grace_frames

        not_changed = ~changed
        in_grace = not_changed & (consec > 0) & (grace_left > 0)
        consec[in_grace] += 1
        grace_left[in_grace] -= 1

        ended = not_changed & (consec > 0) & (grace_left <= 0) & ~in_grace
        consec[ended] = 0
        run_start[ended] = 0

    # A hit is a pixel whose CURRENT run (at the clip's last processed frame)
    # has lasted >=0.5s -- i.e. it appeared and never recovered since.
    final_persisting = consec >= persist_frames

    n, lbl, stats, _ = cv2.connectedComponentsWithStats(final_persisting.astype(np.uint8), connectivity=8)
    sig_mask = np.zeros_like(final_persisting, dtype=np.uint8)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= MIN_HIT_AREA_PX:
            sig_mask[lbl == i] = 1

    if not sig_mask.any():
        return [], fps, len(frames)

    # Merge nearby flagged components into single reported hits.
    dil_kernel = np.ones((MERGE_RADIUS_PX, MERGE_RADIUS_PX), np.uint8)
    dilated = cv2.dilate(sig_mask, dil_kernel)
    n2, lbl2 = cv2.connectedComponents(dilated)

    hits = []
    sig_bool = sig_mask.astype(bool)
    for group_id in range(1, n2):
        group_pixels = sig_bool & (lbl2 == group_id)
        if not group_pixels.any():
            continue
        ys, xs = np.where(group_pixels)
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        area = int(group_pixels.sum())
        first_frame = int(run_start[group_pixels].min())
        hits.append(Hit(bbox=(int(x0), int(y0), int(x1 - x0 + 1), int(y1 - y0 + 1)),
                         area_px=area, first_frame=first_frame, fps=fps))
    hits.sort(key=lambda hh: hh.area_px, reverse=True)
    return hits, fps, len(frames)


def export_filmstrip(clip_path: Path, frames: list, hit: Hit, hit_idx: int, out_root: Path) -> Path:
    out_dir = out_root / clip_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    x, y, w, h = hit.bbox
    fh, fw = frames[0].shape[:2]
    x0 = max(0, x - CROP_PAD_PX)
    y0 = max(0, y - CROP_PAD_PX)
    x1 = min(fw, x + w + CROP_PAD_PX)
    y1 = min(fh, y + h + CROP_PAD_PX)

    last_frame_idx = len(frames) - 1
    sample_idxs = sorted(set(
        [0] +  # frame-0 reference, so the human can see the "before"
        [int(round(hit.first_frame + i * (last_frame_idx - hit.first_frame) / (FILMSTRIP_FRAMES - 1)))
         for i in range(FILMSTRIP_FRAMES)]
    ))

    paths = []
    for i in sample_idxs:
        crop = frames[i][y0:y1, x0:x1].copy()
        label = "REF-f0" if i == 0 else f"f{i}_t{i / hit.fps:.2f}s"
        p = out_dir / f"hit{hit_idx:02d}_t{hit.first_appear_s:.2f}s__{label}.png"
        cv2.imwrite(str(p), crop)
        paths.append(p)
    return out_dir


def scan_clip(clip_path: Path) -> int:
    """Returns number of hits found (0 = clean)."""
    try:
        hits, fps, n_frames = find_hits(clip_path)
    except IOError as e:
        print(f"  SKIP  {clip_path.name}: {e}")
        return -1

    dur = n_frames / fps
    if not hits:
        print(f"  quiet  {clip_path.name}  ({n_frames} frames, {dur:.1f}s, {fps:.1f}fps)")
        return 0

    print(f"  HIT!!  {clip_path.name}  ({n_frames} frames, {dur:.1f}s) -- {len(hits)} candidate region(s)")
    # re-read frames once for cropping (find_hits already read+freed its own copy)
    frames, _ = _read_all_frames(clip_path)
    out_root = clip_path.parent / "_sentinel"
    for i, hit in enumerate(hits, start=1):
        out_dir = export_filmstrip(clip_path, frames, hit, i, out_root)
        print(f"         hit {i}: area={hit.area_px}px bbox={hit.bbox} "
              f"first_appears={hit.first_appear_s:.2f}s -> {out_dir}\\")
    return len(hits)


def _iter_clip_paths(argv: list[str]) -> list[Path]:
    paths = []
    for a in argv:
        p = Path(a)
        if p.is_dir():
            paths += sorted(p.glob("*.mp4"))
        else:
            paths.append(p)
    return paths


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2

    clips = _iter_clip_paths(argv)
    if not clips:
        print("No .mp4 files found.")
        return 2

    print("=== MARGIN SENTINEL -- quiet-paper tripwire ===\n")
    total_hits = 0
    scanned = 0
    for clip in clips:
        n = scan_clip(clip)
        if n >= 0:
            scanned += 1
            total_hits += n

    print(f"\n{scanned}/{len(clips)} clip(s) scanned, {total_hits} candidate hit(s) exported.")
    if scanned == 0:
        return 2
    if total_hits > 0:
        print("This is a LEAD GENERATOR, not a verdict -- eye-check every exported filmstrip"
              " before treating any hit as a confirmed defect.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
