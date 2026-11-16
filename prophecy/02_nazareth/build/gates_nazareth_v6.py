"""gates_nazareth_v6.py - $0 gates for the Nazareth comic film v6 (adapted from the Thief gates_comic.py).
  .venv\\Scripts\\python.exe prophecy/02_nazareth/build/gates_nazareth_v6.py [--marks]   (marks gates need _remotion/out/NAZARETH_marks_v6.mp4)"""
import json, subprocess, sys, math
from pathlib import Path
import numpy as np, cv2
HERE = Path(__file__).parent; EPD = HERE.parent; ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
FINAL = EPD / "film/NAZARETH_COMIC_v6.mp4"; AUDIO = EPD / "audio/narration_v7.mp3"; MARKS = ROOT / "_remotion/out/NAZARETH_marks_v6.mp4"
WORDS = json.load(open(EPD / "audio/narration_v7.words.json")); EP = json.load(open(HERE / "nazareth_episode_v6.json")); res = []
NEAR = [0]
FR = EP["frames"]; JL = (572, 666); CL = (1380, 1496); CROSS = (1210, 1506); HOLD = (FR - 90, FR)


def rec(n, ok, m): res.append((n, ok, m)); print(("PASS " if ok else "FAIL ") + n + " - " + m)


def probe(p, sel, ent):
    return subprocess.run(["ffprobe", "-v", "error", "-select_streams", sel, "-show_entries", ent, "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip().rstrip(",")


def amd5(p):
    return subprocess.run(["ffmpeg", "-v", "error", "-threads", "2", "-i", str(p), "-map", "0:a", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True).stdout.strip()


def main():
    if FINAL.exists():
        vd = float(probe(FINAL, "v:0", "stream=duration")); ad = float(probe(FINAL, "a:0", "stream=duration")); nb = int(probe(FINAL, "v:0", "stream=nb_frames")); sz = probe(FINAL, "v:0", "stream=width,height,r_frame_rate")
        src = float(probe(AUDIO, "a:0", "stream=duration"))
        rec("G1 duration", abs(vd - src) <= 0.05 and abs(ad - src) <= 0.03 and nb == FR and sz.startswith("1080,1920,30/1"), "video %.3f s (%d frames) audio %.3f s (source %.3f s) %s" % (vd, nb, ad, src, sz))
        h1, h2 = amd5(AUDIO), amd5(FINAL); rec("G2 audio identical", h1 == h2 and h1 != "", "narration.mp3 %s | film %s" % (h1[:40], h2[:40]))
    else:
        print("SKIP G1/G2 (film not rendered yet)")
    land = [x for x in EP["scenes"] if x["id"] == "land"][0]
    rec("G15 landing S14 starts on 'rose again' (>= 49.81 s) and fits its clip", land["f0"] / 30 >= 49.81 and land["panels"][0]["shot"]["clip"] == "S14" and (FR - land["f0"]) / 30 <= 10.04 + .07, "S14 starts f%d = %.3f s (rose at %.2f s); runs %.2f s of 10.04 s" % (land["f0"], land["f0"] / 30, min(t for w, t in [(w["w"].strip(".,?!:").lower(), w["start"]) for w in WORDS] if w == "rose"), (FR - land["f0"]) / 30))
    # G3a stillness: Jesus line + hold scenes have a locked camera, no moves, no doodles/transition-in marks inside the window
    bad = []
    for s in EP["scenes"]:
        if s["id"] in ("jesus", "land"):
            sh = s["panels"][0]["shot"]
            if sh["z0"] != sh["z1"] or s.get("moves") or len(s["panels"]) != 1: bad.append(s["id"])
    dood = [d for d in EP["doodles"] if (d["at"] < JL[1] and d.get("until", d["at"] + d.get("frames", 1)) > JL[0]) or d.get("until", d["at"] + d.get("frames", 1)) > HOLD[0] and d["at"] < HOLD[1]]
    rec("G3a stillness (Jesus line + hold): locked camera, no moves, no doodles", not bad and not dood, "bad scenes %s; doodles in window %s" % (bad or "none", [d["kind"] for d in dood] or "none"))
    pk = [x for x in EP["scenes"] if x["id"] == "pgK"][0]
    cam = all(p["shot"]["z0"] == p["shot"]["z1"] for p in pk["panels"]); mv = [m for m in pk.get("moves", []) if CL[0] <= m["at"] < CL[1]]
    cd = [d["kind"] for d in EP["doodles"] if d["at"] < CROSS[1] and d.get("until", d["at"] + d.get("frames", 1)) > CROSS[0]]
    rec("G3a2 cross reverent: locked camera, no moves in the cross line, no doodle at all on the cross page", cam and not mv and not cd, "camera locked %s; moves in window %s; doodles %s" % (cam, mv or "none", cd or "none"))
    TR = {"panel_slam", "panel_dive", "whip_pan", "page_glide", "slam_cut", "speed_zoom", "ink_slash_split", "halftone_dissolve", "page_flip_up", "pull_out_to_page", "border_fall", "punch_cut", "panel_shatter", "ink_bleed", "iris", "gutter_wipe"}
    ev = [(t["at"], t["kind"]) for t in EP["transitions"]]
    for s in EP["scenes"]:
        for mv in s.get("moves", []):
            if mv["kind"] in TR: ev.append((mv["at"], mv["kind"]))
    ev.sort(); kinds = [k for _, k in ev]; badr = [(ev[i], ev[i + 1]) for i in range(len(ev) - 1) if ev[i][1] == ev[i + 1][1] and ev[i][1] != "panel_slam"]
    cnt = {k: kinds.count(k) for k in set(kinds)}; over = {k: c for k, c in cnt.items() if c > 2 and k != "panel_slam"}
    rec("G5 variety", not badr and not over, "sequence: %s | repeats-in-a-row %s | >2 uses %s" % (" > ".join(kinds), badr, over))
    # G8 word sync: every word-tied frame >= ceil(word_start*30)
    W = [(w["w"].strip(".,?!:").lower(), w["start"]) for w in WORDS]
    def ws(word, nth=0):
        word = word.strip(".,?!:").lower()
        return min([t for w, t in W if w == word], key=lambda t: abs(t - NEAR[0] / 30))
    T = [("Jesus slam", 0, "jesus"), ("stopped splat", 10, "stopped"), ("sentence dive", 54, "sentence"), ("Nazareth slam", 90, "nazareth"), ("He read slam", 137, "he"),
         ("someone slam", 175, "someone"), ("time slam", 254, "time"), ("news rays", 207, "news"), ("The slam", 303, "the"), ("Isaiah's jolt", 317, "isaiah's"),
         ("And (Isaiah) slam", 374, "and"), ("He left", 462, "he"), ("sat slam", 529, "sat"), ("This: Jesus line", 576, "this"),
         ("It was about Him", 678, "it"), ("They slam", 739, "they"), ("Physician slam", 809, "physician"), ("He reminded slam", 885, "he"), ("God sent slam", 911, "god"), ("not-to-their-own slam", 989, "not"),
         ("Furious page", 1058, "furious"), ("He walked slam", 1152, "he"), ("walked slam", 1159, "walked"), ("Later: cross slam", 1210, "later"), ("cross: leaders crop", 1237, "cross"),
         ("LANDING S14 on rose again", 1496, "rose")]
    ties = []
    for n, f, w in T:
        NEAR[0] = f; ties.append((n, f, ws(w)))
    okw = True; msg = []
    for n, f, t in ties:
        need = math.ceil(t * 30 - 1e-6)
        if f < need: okw = False; msg.append("%s f%d < f%d" % (n, f, need))
    rec("G8 word sync (never early)", okw, "%d word-tied frames checked; early: %s" % (len(ties), msg or "none"))
    # G10 coverage
    def npanels(f):
        sc = [x for x in EP["scenes"] if x["f0"] <= f < x["f1"]]
        if not sc: return 0
        x = sc[-1]; n = 0
        for p in x["panels"]:
            if p.get("show") and not (p["show"][0] <= f < p["show"][1]): continue
            vis = f >= p.get("mount", x["f0"]); sl = [m for m in x.get("moves", []) if m["kind"] == "panel_slam" and m["panel"] == p["id"]]
            if sl and f < sl[0]["at"]: vis = False
            if vis: n += 1
        for m in x.get("moves", []):
            if m["kind"] == "panel_dive" and f >= m["at"] + m["frames"] // 2: n = 1
        return n
    multi = sum(1 for f in range(FR) if npanels(f) >= 2)
    rec("G10 page coverage", multi / FR >= 0.6, "%d of %d frames (%.0f%%) on pages with 2+ panels; limit 60%%" % (multi, FR, 100 * multi / FR))
    dup = [x["id"] for x in EP["scenes"] if len(x["panels"]) != len({p["shot"]["clip"] for p in x["panels"] if not p.get("show") or True}) and False]
    dup = []
    for x in EP["scenes"]:
        for i, p in enumerate(x["panels"]):
            for q in x["panels"][i + 1:]:
                if p["shot"]["clip"] == q["shot"]["clip"]:
                    a = p.get("show") or [p["mount"], x["f1"]]; b = q.get("show") or [q["mount"], x["f1"]]
                    if a[0] < b[1] and b[0] < a[1] and not (p["shot"]["clip"] == "S17" and abs(p["shot"]["cy"] - q["shot"]["cy"]) >= .4): dup.append((x["id"], p["id"], q["id"]))
    pages = [x["id"] for x in EP["scenes"] if len(x["panels"]) >= 2]
    rec("G11 panel variety (no duplicate clip on screen at once; only exception: S17 cross + its brief-allowed leaders crop, cy differs >= .4)", not dup, "%d multi-panel pages (%s); simultaneous duplicates: %s" % (len(pages), ",".join(pages), dup or "none"))
    # G12 clip life: every panel's on-screen life must be <= its clip length (never loop/freeze/stretch)
    CLP = {"S09": 10.04, "S14": 10.04, "S17": 10.04, "S15": 6.04, "S16": 6.04, "S18": 5.04, "S02": 2.1, "S03": 2.6, "S08": 2.6, "S10": 3.1}; lifebad = []
    for x in EP["scenes"]:
        for p in x["panels"]:
            a = p["mount"]; b = p["show"][1] if p.get("show") else x["f1"]
            if any(m["kind"] == "panel_dive" and m["panel"] != p["id"] and m["at"] + m["frames"] <= b for m in x.get("moves", [])): pass
            avail = (CLP.get(p["shot"]["clip"], 5.04) - p["shot"]["t_in"]) * 30
            for m in x.get("moves", []):  # covered once another panel's dive finishes
                if m["kind"] == "panel_dive" and m["panel"] != p["id"]: b = min(b, m["at"] + m["frames"])
            if b - a > avail + 2: lifebad.append((x["id"], p["id"], b - a, round(avail)))
    rec("G12 clip life <= clip length (no freeze/loop)", not lifebad, "violations: %s" % (lifebad or "none"))
    # G13 repeats (v3): Jesus clips S01/S03/S09 up to 3 pages, all others <= 2; S05/S06 exactly 1 page each (own beat only)
    pg = {}
    for x in EP["scenes"]:
        for p in x["panels"]: pg.setdefault(p["shot"]["clip"].rstrip("w"), set()).add(x["id"])
    JES = {"S01", "S03", "S09"}
    over = {k: sorted(v) for k, v in pg.items() if len(v) > (3 if k in JES else 2)}
    own = {k: sorted(pg.get(k, [])) for k in ("S05",) if len(pg.get(k, [])) != 1}
    rec("G13 repeats (Jesus S01/S03/S09 <=3 pages, others <=2; S05 =1 page)", not over and not own, "pages per clip: %s | over: %s | S05 not 1 page: %s" % ({k: len(v) for k, v in sorted(pg.items())}, over or "none", own or "none"))
    # G14 S04 shown on hands/scroll only (cy >= .55: face is at y~.18); S13 clip is the warm one (no grey tint file)
    s04 = [(x["id"], p["id"], p["shot"]["cy"]) for x in EP["scenes"] for p in x["panels"] if p["shot"]["clip"] == "S04"]
    rec("G14 S04 crop on hands (cy>=.55)", all(c >= .55 for *_, c in s04) , "S04 crops %s" % s04)
    if MARKS.exists():
        cap = cv2.VideoCapture(str(MARKS)); frames = []
        while True:
            ok, im = cap.read()
            if not ok: break
            frames.append(im.max(axis=2) > 60)
        n = len(frames)
        cnt2 = lambda a, b, box=None: max(int((frames[i][box[1]:box[1] + box[3], box[0]:box[0] + box[2]] if box else frames[i]).sum()) for i in range(a, min(b, n)))
        rec("G3b stillness: no overlay on Jesus line (f%d-%d)" % JL, cnt2(*JL) == 0, "max mark pixels %d" % cnt2(*JL))
        rec("G3b2 reverence: no overlay on the cross line (f%d-%d)" % CL, cnt2(*CL) == 0, "max mark pixels %d" % cnt2(*CL))
        rec("G3c stillness: no overlay on the 3 s hold (f%d-%d)" % HOLD, cnt2(*HOLD) == 0, "max mark pixels %d" % cnt2(*HOLD))
        pillf = [i for p in EP["pills"] for i in range(p["f0"], min(p["f1"], n))]
        z = (70, 974, 940, 276); worst = max((int(frames[i][z[1]:z[1] + z[3], z[0]:z[0] + z[2]].sum()), i) for i in pillf)
        rec("G6 pill zone free (pill_edge excluded)", worst[0] == 0, "max mark pixels in x70-1010,y974-1250 while a pill shows: %d (frame %d)" % worst)
        top = max(int(frames[i][0:200].sum()) for i in range(min(n, FR)))
        rec("G6b top 200 px clear of marks", top == 0, "max mark pixels y<200: %d" % top)
        viol = [(nd["label"], c) for nd in EP["no_draw"] for c in [cnt2(nd["f0"], nd["f1"], nd["box"])] if c]
        rec("G7 no-draw masks (Jesus faces + the cross)", not viol, "masks %d, violations %s" % (len(EP["no_draw"]), viol or "none"))
    else:
        print("SKIP marks gates (run the marks render first)")
    print("ALL PASS" if all(b for _, b, _ in res) else "SOME FAIL")


if __name__ == "__main__":
    main()
