import sys, cv2, numpy as np
slot = {"f01b_5s": 120, "f02a_3s": 81, "f03a_5s": 135, "f03_5s": 120, "f03b_7s": 186, "f04_5s": 132, "f06b_5s": 144, "f06c_5s": 141, "back_7s": 177}
for cid in sys.argv[1:]:
    cap = cv2.VideoCapture(f"clips/{cid}.mp4"); fps = cap.get(cv2.CAP_PROP_FPS) or 24; n = round(slot[cid] / 30 * fps)
    pts = []
    for i in range(n + 1):
        r, f = cap.read()
        if not r: break
        if i % 12 and i != n: continue
        m = (f[..., 0].astype(int) - f[..., 2].astype(int)) > 35
        m[:int(.3 * f.shape[0])] = False
        ys, xs = np.nonzero(m)
        pts.append((i, len(xs), (round(xs.mean() / f.shape[1] * 1080), round(ys.mean() / f.shape[0] * 1920)) if len(xs) else None))
    print(cid, pts)
