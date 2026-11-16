import sys, cv2, numpy as np
for cid, n in (a.split(":") for a in sys.argv[1:]):
    cap = cv2.VideoCapture(f"clips/{cid}.mp4"); fr = []
    while True:
        r, f = cap.read()
        if not r: break
        fr.append(f)
    n = int(n); a, b = fr[0], fr[min(n, len(fr) - 1)]
    out = []
    for name, (y0, y1) in (("upper", (.38, .62)), ("lower", (.62, .90)), ("main", (.38, .90))):
        g = lambda im: cv2.cvtColor(cv2.resize(im[int(y0*im.shape[0]):int(y1*im.shape[0])], (270, int(480*(y1-y0)))), cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
        W = np.eye(2, 3, dtype=np.float32)
        try:
            cc, W = cv2.findTransformECC(g(a), g(b), W, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 60, 1e-5)); z = float(np.sqrt(abs(np.linalg.det(W[:, :2]))))
        except Exception: z = -1
        out.append(f"{name} {z:.3f}")
    print(cid, "frame", n, " ".join(out))
