import sys, cv2, numpy as np
slot = {"f01b_5s": 120, "f02a_3s": 81, "f03a_5s": 135, "f03_5s": 120, "f03b_7s": 186, "f04_5s": 132, "f06b_5s": 144, "f06c_5s": 141, "back_7s": 177}
for cid in sys.argv[1:]:
    cap = cv2.VideoCapture(f"clips/{cid}.mp4"); fr = []
    while True:
        r, f = cap.read()
        if not r: break
        fr.append((cv2.cvtColor(cv2.resize(f, (360, 640)), cv2.COLOR_BGR2GRAY).astype(np.float32), f[int(.3 * f.shape[0]):].astype(int)))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    n = round(slot[cid] / 30 * fps) + 1
    fr = fr[:n]
    blue = lambda f: int(((f[..., 0] - f[..., 2]) > 35).sum())
    b0, b1 = blue(fr[0][1]), blue(fr[-1][1]); g = [x[0] for x in fr]
    a, b = g[0], g[-1]
    md = float(np.mean([np.mean(np.abs(g[i] - g[i + 1])) for i in range(len(g) - 1)]))
    W = np.eye(2, 3, dtype=np.float32)
    try:
        cc, W = cv2.findTransformECC(a / 255, b / 255, W, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)); z = float(np.sqrt(abs(np.linalg.det(W[:, :2]))))
    except Exception: z = -1
    band = lambda im, y0, y1: im[int(y0 * 640):int(y1 * 640), :]
    tt = float(np.mean(np.abs(band(a, 0, .06) - band(b, 0, .06)))); tc = float(np.mean(np.abs(band(a, .78, 1) - band(b, .78, 1))))
    print(f"{cid}: used {len(fr)}f fps{fps:.0f} zoom {z:.3f} meandiff {md:.2f} title {tt:.2f} caption {tc:.2f} blue {b0}->{b1} ({(b1-b0)/max(b0,1)*100:+.0f}%)")
