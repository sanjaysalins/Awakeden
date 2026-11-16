r"""make_marks_woman_behold.py: writes uplift_marks.json for the pilot (4 marks, 2 page turns, no_draw boxes).
Positions are picture points on the finished segs, tracked with track_pts.py (LK similarity / LK point). $0.
"""
import json, math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from track_pts import track, track_similarity  # noqa: E402

POOL = Path(r"F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross\woman_behold_john1926\visual\uplift_v1")
W = POOL / "_livingpage_work"
spec = json.loads((POOL / "livingpage_short.uplift.spec.json").read_text(encoding="utf-8"))
align = json.loads((POOL.parent.parent / "audio" / "alignment.json").read_text(encoding="utf-8"))
starts = []
for b in spec["beats"]:
    starts.append(round(b["t"][0] * 30))


def seg(i):
    return W / f"seg_{i:02d}.mp4", starts[i - 1]


def word(w, near):
    c = [x for x in align if x["w"].strip(".,!?;:").lower() == w and abs(x["start"] - near) < 0.05]
    assert c, (w, near)
    return {"w": w, "start": c[0]["start"], "frame": math.ceil(c[0]["start"] * 30)}


def tr(t):  # track -> {"track": [[f,x,y]...]} thinned
    return {"track": [[a, round(x, 1), round(y, 1)] for a, x, y in t][::2] + [[t[-1][0], round(t[-1][1], 1), round(t[-1][2], 1)]]}


marks = []
# ---- M1 thread, beat 3: shadow (top panel) -> foot of centre cross, around the feet (never on Him)
s3, f3 = seg(3)
ta = track_similarity(s3, f3, 347, 392, [(570, 700)], [40, 60, 1000, 780])[0]
tb = track_similarity(s3, f3, 347, 392, [(553, 1265)], [60, 900, 960, 440])[0]
wd = word("sword", 11.54)
marks.append({"id": "M1", "kind": "thread", "at": wd["frame"], "frames": 16, "until": 392, "word": wd,
              "from": tr(ta), "to": tr(tb), "via": [[800, 860], [790, 1150], [690, 1255]], "seed": 11})
# ---- M2 gaze line, beat 5b: from below His panel to just above Mary's brow
s5, f5 = seg(5)
tb2 = track(s5, f5, 600, 645, 640, 1310, 21)
wd = word("her", 19.93)
marks.append({"id": "M2", "kind": "route", "dash": "gaze", "tone": "bone", "at": 600, "frames": 10, "until": 645, "word": wd,
              "pts": [[700, 866], {"track": [[a, round(x, 1), round(y, 1)] for a, x, y in tb2]}], "seed": 17})
# ---- M3 route, beat 9: up the road to the lit gate
s9, f9 = seg(9)
pts3 = [(985, 1140), (960, 990), (900, 810), (760, 685), (610, 640)]
tt = track_similarity(s9, f9, 1147, 1198, pts3, [0, 60, 1080, 600])
wd = word("took", 38.23)
marks.append({"id": "M3", "kind": "route", "tone": "ink", "at": wd["frame"], "frames": 39, "until": 1198, "word": wd,
              "pts": [tr(t) for t in tt], "seed": 19})
# ---- M4 thread, beat 10: Mary's shoulder -> John's shoulder, knot on "home"
s10, f10 = seg(10)
ma = track_similarity(s10, f10, 1265, 1308, [(380, 1180)], [60, 60, 460, 1300])[0]
mb = track_similarity(s10, f10, 1265, 1308, [(850, 1500)], [580, 60, 440, 1300])[0]
wd = word("son", 42.14)
marks.append({"id": "M4", "kind": "thread", "at": 1265, "frames": 12, "until": 1308, "word": wd,
              "from": tr(ma), "to": tr(mb), "bow": 40, "seed": 23, "knot_at": 1298})

turns = [{"kind": "page_flip_up", "at": 1087, "frames": 8}, {"kind": "halftone_dissolve", "at": 1595, "frames": 8, "mode": "rise"}]
# beat 9 starts frame 1087 (36.22s); beat 13 starts frame 1595 (53.16s)
no_draw = [
    {"label": "jesus_looks_down panel (5b)", "box": [30, 30, 1020, 821], "f0": 560, "f1": 663},
    {"label": "Jesus feet and cross body, golgotha bottom panel (beat 3)", "box": [450, 940, 220, 245], "f0": 235, "f1": 392},
    {"label": "beat 7 Jesus panel", "box": [30, 873, 1020, 821], "f0": 863, "f1": 956},
    {"label": "beat 11 (all Jesus)", "box": [0, 0, 1080, 1920], "f0": 1308, "f1": 1476},
    {"label": "beat 13b landing", "box": [0, 0, 1080, 1920], "f0": 1655, "f1": 1772},
]
out = {"marks": marks, "turns": turns, "no_draw": no_draw, "jesus_beats": [[28.75, 36.22]], "last_beat_from": 55.18,
       "unchanged_beats": [1, 2, 4, 9]}
(POOL / "uplift_marks.json").write_text(json.dumps(out), encoding="utf-8")
for m in marks:
    print(m["id"], m["kind"], m["at"], m.get("until"), m["word"])
print("tracks M2 end:", tb2[0], tb2[-1])
