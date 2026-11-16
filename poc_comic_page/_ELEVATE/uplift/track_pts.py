"""track_pts.py (uplift T7): follow a picture point through a clip segment ($0, OpenCV LK).
Start from build_thief.track() idea. Output [[abs_frame, x, y], ...] for the frames asked.
Usage: python track_pts.py <seg.mp4> <seg_start_abs_frame> <f_from_abs> <f_to_abs> <x> <y> [patch=21]
(x,y = the point on frame f_from_abs, in 1080x1920 screen px; the segment frame of an abs frame = abs - seg_start.)
Note: captions are burned into the segs; pick points away from the caption box. Tracks forward from f_from.
"""
import json, sys
import cv2
import numpy as np


def track(seg, seg_start, f_from, f_to, x, y, patch=21):
    cap = cv2.VideoCapture(str(seg))
    frames = []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        frames.append(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY))
    cap.release()
    i0, i1 = f_from - seg_start, min(f_to - seg_start, len(frames) - 1)
    assert 0 <= i0 < len(frames), (i0, i1, len(frames))
    lk = dict(winSize=(patch * 2 + 1, patch * 2 + 1), maxLevel=4,
              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
    pt = np.array([[[x, y]]], dtype=np.float32)
    out = [[f_from, float(x), float(y)]]
    for i in range(i0, i1):
        nxt, st, err = cv2.calcOpticalFlowPyrLK(frames[i], frames[i + 1], pt, None, **lk)
        if st[0][0]:
            pt = nxt
        out.append([seg_start + i + 1, float(pt[0][0][0]), float(pt[0][0][1])])
    return out


if __name__ == "__main__":
    a = sys.argv
    r = track(a[1], int(a[2]), int(a[3]), int(a[4]), float(a[5]), float(a[6]), int(a[7]) if len(a) > 7 else 21)
    print(json.dumps(r))


def track_similarity(seg, seg_start, f_from, f_to, pts, roi):
    """Follow SEVERAL static picture points through a push-in/pan: track many background features inside `roi`
    [x,y,w,h] with LK, fit a similarity transform (RANSAC) frame to frame, apply it to `pts`.
    Returns one list per point: [[abs_frame, x, y], ...]. Robust where a point itself has no texture (a road, a brow)."""
    cap = cv2.VideoCapture(str(seg))
    frames = []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        frames.append(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY))
    cap.release()
    i0, i1 = f_from - seg_start, min(f_to - seg_start, len(frames) - 1)
    x, y, w, h = roi
    mask = np.zeros_like(frames[i0]); mask[y:y + h, x:x + w] = 255
    P = np.array([[p[0], p[1], 1.0] for p in pts], dtype=np.float64).T  # 3 x n
    M = np.eye(3)
    out = [[[f_from, float(p[0]), float(p[1])]] for p in pts]
    lk = dict(winSize=(31, 31), maxLevel=4, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
    for i in range(i0, i1):
        m2 = np.zeros_like(frames[i]); m2[y:y + h, x:x + w] = 255
        # features are re-picked every frame inside the ROI warped by the running transform (ROI stays on the same content)
        cur = cv2.goodFeaturesToTrack(frames[i], 400, 0.01, 8, mask=m2)
        if cur is None or len(cur) < 8:
            A = np.eye(3)
        else:
            nxt, st, _ = cv2.calcOpticalFlowPyrLK(frames[i], frames[i + 1], cur, None, **lk)
            good = st.ravel() == 1
            A2, _ = cv2.estimateAffinePartial2D(cur[good], nxt[good], method=cv2.RANSAC, ransacReprojThreshold=2.0)
            A = np.vstack([A2, [0, 0, 1]]) if A2 is not None else np.eye(3)
        M = A @ M
        Q = M @ P
        for k in range(len(pts)):
            out[k].append([seg_start + i + 1, float(Q[0, k]), float(Q[1, k])])
    return out
