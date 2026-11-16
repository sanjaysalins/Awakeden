"""contacts.py - contact_v1.jpg (one frame per beat + mid-transition frames) and old_vs_new.jpg (shipped | comic)."""
import sys, cv2, numpy as np
from pathlib import Path
R = Path(r"F:\slk\PycharmProjects\JesusInTheBible"); HERE = Path(__file__).parent
NEW = R / "poc_comic_page/_ELEVATE/arms/TP_S32_COMIC_v1.mp4"; OLD = R / "batches/cluster_01_cross/today_paradise_short32/visual/today_paradise_short32_final.mp4"
BEATS = [(40, "1 page+hook"), (62, "1 slams"), (77, "2 dive"), (105, "2 why"), (128, "3 two"), (152, "4 glide"), (240, "5 mocker"), (264, "5 jolt"), (324, "6 zoom"), (355, "6 ticks"),
         (384, "7 slash"), (420, "7 shift"), (440, "7 gone"), (455, "8 dots"), (500, "8 hush"), (562, "9 flip"), (600, "9 rays"), (655, "10 pull"), (668, "11 fall"), (720, "11 Jesus"),
         (830, "12 answer"), (886, "14 iris"), (950, "14 join"), (962, "15 flip"), (1002, "15 whisper"), (1056, "16 rise"), (1090, "16 border"), (1130, "16 still")]
def grab(p, f):
    c = cv2.VideoCapture(str(p)); c.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = c.read(); return im
def tile(im, w, lab):
    im = cv2.resize(im, (w, int(w * 1920 / 1080))); cv2.rectangle(im, (0, 0), (w, 18), (30, 30, 30), -1); cv2.putText(im, lab, (3, 13), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1); return im
def sheet(tiles, cols):
    while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
    return np.vstack([np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)])
cv2.imwrite(str(HERE / "contact_v1.jpg"), sheet([tile(grab(NEW, f), 270, "f%d %s" % (f, l)) for f, l in BEATS], 7), [cv2.IMWRITE_JPEG_QUALITY, 85])
ov = [(40, ""), (105, ""), (152, ""), (240, ""), (384, ""), (455, ""), (600, ""), (700, ""), (830, ""), (950, ""), (1000, ""), (1130, "")]
t = []
for f, _ in ov: t += [tile(grab(OLD, f), 200, "old f%d" % f), tile(grab(NEW, f), 200, "new f%d" % f)]
cv2.imwrite(str(HERE / "old_vs_new.jpg"), sheet(t, 8), [cv2.IMWRITE_JPEG_QUALITY, 85])
print("ok")
