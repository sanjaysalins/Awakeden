"""contacts_v2.py - contact_v2.jpg: one frame per page + mid-read frames (transitions / slams / dives)."""
import cv2, numpy as np
from pathlib import Path
R = Path(r"F:\slk\PycharmProjects\JesusInTheBible"); HERE = Path(__file__).parent; NEW = R / "poc_comic_page/_ELEVATE/arms/TP_S32_COMIC_v2.mp4"
F = [(40, "A hook page"), (60, "A 4 panels"), (100, "A dive Why?"), (125, "B 2-stack"), (160, "B slam"), (195, "B read-in"), (215, "C slam_cut"), (240, "C shout"), (300, "C lines"), (324, "zoom"),
     (345, "mocker face"), (384, "D slash"), (420, "D shift"), (455, "E dissolve"), (500, "E prayer"), (560, "flip"), (600, "F rays"), (655, "F slam"), (668, "fall"), (720, "Jesus splash"),
     (830, "answer"), (886, "iris"), (920, "G page"), (950, "G join"), (962, "flip"), (1000, "H you"), (1056, "rise"), (1130, "hold")]
cap = cv2.VideoCapture(str(NEW)); t = []
for f, l in F:
    cap.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = cap.read(); im = cv2.resize(im, (270, 480)); cv2.rectangle(im, (0, 0), (270, 18), (30, 30, 30), -1); cv2.putText(im, "f%d %s" % (f, l), (3, 13), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1); t.append(im)
while len(t) % 7: t.append(np.zeros_like(t[0]))
cv2.imwrite(str(HERE / "contact_v2.jpg"), np.vstack([np.hstack(t[i:i + 7]) for i in range(0, len(t), 7)]), [cv2.IMWRITE_JPEG_QUALITY, 85]); print("ok")
