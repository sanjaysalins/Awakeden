"""$0 motion check for a new clip. python clipcheck.py <clip> <slot_frames_30fps> <caption_y0 0..1>"""
import sys, cv2, numpy as np
def check(p, slot, y0=.9):
    cap = cv2.VideoCapture(str(p)); fr = []
    while True:
        r, f = cap.read()
        if not r: break
        fr.append((cv2.cvtColor(cv2.resize(f, (360, 640)), cv2.COLOR_BGR2GRAY).astype(np.float32), f[int(.3 * f.shape[0]):].astype(int)))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    fr = fr[:round(slot / 30 * fps) + 1]
    blue = lambda f: int(((f[..., 0] - f[..., 2]) > 35).sum())
    b0, b1 = blue(fr[0][1]), blue(fr[-1][1])
    g = [x[0] for x in fr]; a, b = g[0], g[-1]
    md = float(np.mean([np.mean(np.abs(g[i] - g[i + 1])) for i in range(len(g) - 1)]))
    W = np.eye(2, 3, dtype=np.float32)
    try:
        cc, W = cv2.findTransformECC(a / 255, b / 255, W, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)); z = float(np.sqrt(abs(np.linalg.det(W[:, :2]))))
    except Exception: z = 1.0
    band = lambda img, y0, y1: img[int(y0 * 640):int(y1 * 640), :]
    tt = float(np.mean(np.abs(band(a, 0, .06) - band(b, 0, .06)))); tc = float(np.mean(np.abs(band(a, y0, 1) - band(b, y0, 1))))
    ok = 0.99 <= z <= 1.01 and md > 0.15 and tt < 4.5 and tc < 5.0 and abs(b1 - b0) <= 0.20 * max(b0, 1)
    return ok, f"zoom {z:.3f} meandiff {md:.2f} title {tt:.2f} caption {tc:.2f} blue-motif px {b0}->{b1} used {len(fr)}f"
if __name__ == "__main__":
    p, slot = sys.argv[1], int(sys.argv[2]); y0 = float(sys.argv[3]) if len(sys.argv) > 3 else .9
    ok, s = check(p, slot, y0); print("OK" if ok else "CHECK", s)
