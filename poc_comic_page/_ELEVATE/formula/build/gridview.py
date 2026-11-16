"""gridview.py out.jpg video frame1 frame2 ... -> labelled 100px grid contact (half scale) for picking anchor coords."""
import sys, subprocess, numpy as np, cv2
out, vid, frames = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3:]]
cap = cv2.VideoCapture(vid); tiles = []
for fr in frames:
    cap.set(cv2.CAP_PROP_POS_FRAMES, fr); ok, im = cap.read()
    if not ok: im = np.zeros((1920, 1080, 3), np.uint8)
    im = cv2.resize(im, (540, 960))
    for v in range(0, 1080, 100):
        x = v // 2; cv2.line(im, (x, 0), (x, 959), (0, 255, 255), 1); cv2.putText(im, str(v), (x + 2, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 255, 255), 1)
    for v in range(0, 1920, 100):
        y = v // 2; cv2.line(im, (0, y), (539, y), (0, 255, 255), 1); cv2.putText(im, str(v), (2, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 255, 255), 1)
    cv2.putText(im, "f%d" % fr, (400, 940), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2); tiles.append(im)
cv2.imwrite(out, np.hstack(tiles), [cv2.IMWRITE_JPEG_QUALITY, 85])
