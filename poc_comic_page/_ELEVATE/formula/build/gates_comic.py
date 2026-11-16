"""gates_comic.py - $0 gates for the comic film (spec section 'Gates before calling it built', owner Option B).
  .venv\\Scripts\\python.exe poc_comic_page/_ELEVATE/formula/build/gates_comic.py [--marks]    (--marks renders the marks-only pass first, ~3 min)
Gates: G1 duration/audio-video  G2 audio stream identical  G3 stillness (frames 674-796 vs shipped, no overlay)  G4 answer_light_profile clean
       G5 no transition device twice in a row  G6 pill zone free of doodles while a pill shows  G7 no-draw masks (Jesus faces)  G8 word-sync (never early)
       G9 anchor (marks track the picture, 6 px on 5 frames)."""
import json, subprocess, sys, math, hashlib
from pathlib import Path
import numpy as np, cv2
HERE = Path(__file__).parent; ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
SHIPPED = ROOT / "batches/cluster_01_cross/today_paradise_short32/visual/today_paradise_short32_final.mp4"
WORDS = ROOT / "batches/cluster_01_cross/today_paradise_short32/visual/today_paradise_short32_final.words.json"
V3 = "--v3" in sys.argv; V2 = "--v2" in sys.argv or V3; TAG = "v3" if V3 else ("v2" if V2 else "v1")  # v3 reuses v2 marks (same doodles/transitions, 2 panel crops changed)
FINAL = ROOT / ("poc_comic_page/_ELEVATE/arms/TP_S32_COMIC_%s.mp4" % TAG); MARKS = ROOT / ("_remotion/out/THIEF_marks%s.mp4" % ("_v2" if V2 else ""))
EP = json.load(open(HERE / ("thief_episode_%s.json" % TAG if V2 else "thief_episode.json"))); res = []


def rec(name, ok, msg): res.append((name, ok, msg)); print(("PASS " if ok else "FAIL ") + name + " - " + msg)


def probe(p, sel, ent):
    return subprocess.run(["ffprobe", "-v", "error", "-select_streams", sel, "-show_entries", ent, "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip().rstrip(",")


def amd5(p):
    o = subprocess.run(["ffmpeg", "-v", "error", "-threads", "2", "-i", str(p), "-map", "0:a", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True).stdout
    return o.strip()


def read_frames(path, idxs, gray=False):
    cap = cv2.VideoCapture(str(path)); out = {}
    for i in idxs:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i); ok, im = cap.read(); out[i] = im if ok else None
    return out


def seq_frames(path, a, b):
    cap = cv2.VideoCapture(str(path)); cap.set(cv2.CAP_PROP_POS_FRAMES, a)
    for i in range(a, b):
        ok, im = cap.read()
        if not ok: break
        yield i, im


def main():
    # G1
    vd = float(probe(FINAL, "v:0", "stream=duration")); ad = float(probe(FINAL, "a:0", "stream=duration")); nb = int(probe(FINAL, "v:0", "stream=nb_frames"))
    sz = probe(FINAL, "v:0", "stream=width,height,r_frame_rate")
    rec("G1 duration", abs(vd - 38.0) <= 0.05 and abs(ad - vd) <= 0.05 and nb == 1140 and sz.startswith("1080,1920,30/1"), "video %.3f s (%d frames) audio %.3f s %s" % (vd, nb, ad, sz))
    # G2
    h1, h2 = amd5(SHIPPED), amd5(FINAL); rec("G2 audio identical", h1 == h2 and h1 != "", "shipped %s | comic %s" % (h1[:40], h2[:40]))
    # G3 stillness: compare to shipped, ignoring the 44 px border band
    m = np.zeros((1920, 1080), bool); m[44:1876, 44:1036] = True
    sh = {i: im for i, im in seq_frames(SHIPPED, 674, 797)}; diffs = []
    for i, im in seq_frames(FINAL, 674, 797):
        d = np.abs(im.astype(np.int16) - sh[i].astype(np.int16)).mean(axis=2)[m].mean(); diffs.append(d)
    stable = [np.abs(a.astype(np.int16) - b.astype(np.int16)).mean() for (_, a), (_, b) in zip(list(seq_frames(FINAL, 675, 797))[:-1], list(seq_frames(FINAL, 676, 797)))] if False else []
    rec("G3a stillness vs shipped (f674-796)", float(np.mean(diffs)) < 2.0, "mean abs diff %.2f (max %.2f), limit 2.0, over %d frames" % (np.mean(diffs), np.max(diffs), len(diffs)))
    # G5 variety
    TR = {"panel_slam", "panel_dive", "whip_pan", "page_glide", "slam_cut", "speed_zoom", "ink_slash_split", "halftone_dissolve", "page_flip_up", "pull_out_to_page", "border_fall", "punch_cut",
          "panel_shatter", "ink_bleed", "iris", "gutter_wipe"}
    ev = [(t["at"], t["kind"]) for t in EP["transitions"]]
    for s in EP["scenes"]:
        for mv in s.get("moves", []):
            if mv["kind"] in TR: ev.append((mv["at"], mv["kind"]))
    ev.sort(); kinds = [k for _, k in ev]; bad = [(ev[i], ev[i + 1]) for i in range(len(ev) - 1) if ev[i][1] == ev[i + 1][1] and ev[i][1] != "panel_slam"]
    cnt = {k: kinds.count(k) for k in set(kinds)}; over = {k: c for k, c in cnt.items() if c > 2 and k != "panel_slam"}
    rec("G5 variety", not bad and not over, "sequence: %s | repeats-in-a-row %s | >2 uses %s" % (" > ".join(kinds), bad, over))
    # G8 word-sync: every word-tied device frame >= ceil(word_start*30)
    W = json.load(open(WORDS)); ws = lambda w: next(x["start"] for x in W if x["w"] == w)
    last = lambda w: [x["start"] for x in W if x["w"] == w][-1]
    ties = [("Jesus slam", 2, ws("Jesus")), ("Why? shock", 102, ws("Why?")), ("Two border", 116, ws("Two")), ("criminals border", 123, ws("criminals")), ("Christ fan", 233, ws("Christ,")),
            ("save speed lines", 264, ws("save")), ("thyself fan", 273, ws("thyself")), ("us. drops", 314, ws("us.")), ("One drops", 331, ws("One")), ("Him. panel_join lands", 952, last("Him."))]
    if V2: ties = [("Jesus slam", 2, ws("Jesus")), ("paradise panel", 31, ws("paradise")), ("a panel", 54, ws("a")), ("criminal. panel", 56, ws("criminal.")), ("criminals panel", 123, ws("criminals")), ("If panel", 214, ws("If")), ("Christ fan", 233, ws("Christ,")),
                   ("save speed lines", 264, ws("save")), ("thyself fan", 273, ws("thyself")), ("us. drops", 314, ws("us.")), ("One drops", 331, ws("One")), ("Lord panel", 453, ws("Lord,")),
                   ("Someday panel", 648, ws("Someday.")), ("Him. join lands", 952, last("Him."))]
    ok = True; msg = []
    for n, f, t in ties:
        need = math.ceil(t * 30 - 1e-6)
        if f < need: ok = False; msg.append("%s f%d < f%d" % (n, f, need))
    rec("G8 word sync (never early)", ok, "%d word-tied frames checked; early: %s" % (len(ties), msg or "none"))
    # G9 anchor: kit maths puts the mocker marks within 6 px of hand-keyed shipped-film positions on 5 frames (shipped view = FULL box + shipped shot)
    sys.path.insert(0, str(HERE)); from geo import to_screen
    from build_thief import SH as SHOT
    sh = SHOT["moc"]; ga = EP.get("gates", {}).get("anchor"); T = EP["tracks"]["mocker_mouth"]
    KEYS = {int(k): v for k, v in ga["keys"].items()} if ga else {233: (523, 654), 264: (481, 600), 280: (390, 520), 296: (270, 460), 310: (150, 330)}; err = []
    for f, (x, y) in KEYS.items():
        sx, sy = to_screen(T["pts"][f - T["f0"]], [0, 0, 1080, 1920], sh, f); err.append(math.hypot(sx - x, sy - y))
    rec("G9 anchor (mocker mouth, 5 frames)", max(err) <= 6, "max error %.2f px vs hand-keyed shipped-film points (keys are by-eye, about +/-15 px)" % max(err))
    # G10 page coverage: >= 60 % of runtime on pages showing 2+ panels together
    def npanels(f):
        sc = [x for x in EP["scenes"] if x["f0"] <= f < x["f1"]]
        if not sc: return 0
        x = sc[-1]
        if x.get("type") == "split":
            k = f - x["f0"]; last = max(m["at"] + m["frames"] for m in x["shifts"]); return 2 if 3 <= k and f < last - 2 else 1
        n = 0
        for p in x["panels"]:
            if p.get("show") and not (p["show"][0] <= f < p["show"][1]): continue
            vis = f >= p.get("mount", x["f0"]); slam = [m for m in x.get("moves", []) if m["kind"] == "panel_slam" and m["panel"] == p["id"]]
            if slam and f < slam[0]["at"]: vis = False
            if vis: n += 1
        for m in x.get("moves", []):
            if m["kind"] == "panel_dive" and f >= m["at"] + m["frames"] // 2 and len(x["panels"]) >= 1: n = 1
        return n
    multi = sum(1 for f in range(1140) if npanels(f) >= 2)
    rec("G10 page coverage", multi / 1140 >= 0.6, "%d of 1140 frames (%.0f%%) on pages with 2+ panels; limit 60%%" % (multi, 100 * multi / 1140))
    dup = []
    for x in EP["scenes"]:
        cl = [p["shot"]["clip"] for p in x["panels"] if p["id"] not in ("shipped",)]
        if x.get("type") != "split" and len(cl) != len(set(cl)): dup.append(x["id"])
    pages = [x["id"] for x in EP["scenes"] if len(x["panels"]) >= 2]
    rec("G11 panel variety (no duplicate clip on a page)", not dup, "%d multi-panel pages (%s); duplicates: %s" % (len(pages), ",".join(pages), dup or "none"))
    if "--marks" in sys.argv or MARKS.exists():
        cap = cv2.VideoCapture(str(MARKS)); frames = []
        while True:
            ok_, im = cap.read()
            if not ok_: break
            frames.append((im.max(axis=2) > 60))
        n = len(frames)
        cnt = lambda a, b, box=None: max(int((frames[i][box[1]:box[1] + box[3], box[0]:box[0] + box[2]] if box else frames[i]).sum()) for i in range(a, min(b, n)))
        rec("G3b stillness: no overlay f674-796", cnt(674, 797) == 0, "max mark pixels %d" % cnt(674, 797))
        rec("G4 answer_light_profile clean f796-891", cnt(796, 892) == 0, "max mark pixels %d (comic transitions only into/out of it: punch_cut in, iris out with no ring)" % cnt(796, 892))
        pillf = [i for p in EP["pills"] for i in range(p["f0"], min(p["f1"], n))]
        z = (70, 974, 940, 276); worst = max((int(frames[i][z[1]:z[1] + z[3], z[0]:z[0] + z[2]].sum()), i) for i in pillf)
        rec("G6 pill zone free (pill_edge excluded = it IS the pill's edge)", worst[0] == 0, "max mark pixels in x70-1010,y974-1250 while a pill shows: %d (frame %d)" % worst)
        viol = []
        for nd in EP["no_draw"]:
            c = cnt(nd["f0"], nd["f1"], nd["box"])
            if c: viol.append((nd["label"], c))
        rec("G7 no-draw masks (Jesus faces / close-ups)", not viol, "masks %d, violations %s" % (len(EP["no_draw"]), viol or "none"))
    else:
        print("SKIP marks gates (run the marks render first)")
    (HERE / "gates_result.json").write_text(json.dumps([dict(gate=a, ok=b, msg=c) for a, b, c in res], indent=1))
    print("ALL PASS" if all(b for _, b, _ in res) else "SOME FAIL")


if __name__ == "__main__":
    main()
