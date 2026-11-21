"""qc_sheet.py <clip> <out.jpg> [y0 y1]: 6 frames (first..literal last) of the lower picture side by side + motion per step."""
import sys, subprocess, numpy as np, cv2
src, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
n = len(fr); idx = [0, n//5, 2*n//5, 3*n//5, 4*n//5, n-1]
y0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0; y1 = int(sys.argv[4]) if len(sys.argv) > 4 else fr[0].shape[0]
tiles = [cv2.resize(fr[i][y0:y1], (360, int(360*(y1-y0)/fr[0].shape[1]))) for i in idx]
for t, i in zip(tiles, idx): cv2.putText(t, str(i), (8, 28), 0, 0.9, (0, 0, 255), 2)
cv2.imwrite(out, np.hstack(tiles), [cv2.IMWRITE_JPEG_QUALITY, 85])
d = [float(np.abs(fr[i+1].astype(int)-fr[i].astype(int)).mean()) for i in range(n-1)]
print(src, n, 'frames; mean motion', round(np.mean(d),2), 'max', round(max(d),2))
