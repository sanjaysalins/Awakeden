import sys, subprocess, numpy as np
from PIL import Image
import cv2
def frames(p, n=4, used=None):
    cap = cv2.VideoCapture(str(p)); fr = []
    while True:
        r, f = cap.read()
        if not r: break
        fr.append(f)
    k = used or len(fr)
    idx = [0, k // 3, 2 * k // 3, k - 1]
    return [Image.fromarray(cv2.cvtColor(cv2.resize(fr[i], (216, 384)), cv2.COLOR_BGR2RGB)) for i in idx], len(fr)
rows = []
for a in sys.argv[2:]:
    name, used = (a.split(":") + [None])[:2]
    ims, n = frames(f"clips/{name}.mp4", used=int(used) if used else None)
    rows.append(ims)
W = Image.new("RGB", (216 * 4 * 1, 384 * len(rows)))
for r, ims in enumerate(rows):
    for c, im in enumerate(ims): W.paste(im, (c * 216, r * 384))
W.save(sys.argv[1], quality=88)
