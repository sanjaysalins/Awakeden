r"""gates_uplift.py (uplift T8): the U-gates for one finished uplift film. $0. Prints PASS/FAIL + evidence, writes gates_result.json.

  U1 length/size/fps vs the shipped final        U2 audio stream MD5 == shipped audio MD5
  U3 unchanged beats ~ shipped (mean px diff)    U4 speed factor <= 1.05 for every panel slot (engine report)
  U5 same clip twice on a page / uses per clip   U6 marks: count, overlap, not-before-word, no_draw, no JESUS beat, no last beat
  U7 caption zone clear (marks-only render vs caption boxes)   U8 eye check = contact sheet (manual, printed as TODO)
  U9 blind red team = NOT RUN here (owner-gated panel)

  .venv\Scripts\python.exe poc_comic_page\_ELEVATE\uplift\gates_uplift.py woman-behold-thy-son
"""
import json, math, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from build_uplift import PIECES, paths  # noqa: E402


def probe(f, sel, entries):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", sel, "-show_entries", f"stream={entries}", "-of", "json", str(f)],
                       capture_output=True, text=True)
    return json.loads(r.stdout)["streams"][0]


def count_frames(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(f)],
                       capture_output=True, text=True)
    return int(r.stdout.strip().strip(",").split(",")[0])


def audio_md5(f):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-map", "0:a:0", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True)
    return r.stdout.strip()


def frame(f, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(f), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.uint8).reshape(1920, 1080, 3).astype(np.float32)


def main(slug):
    p = paths(slug)
    new, old = p["out"], p["shipped"]
    mk = json.loads(p["marks"].read_text(encoding="utf-8"))
    spec = json.loads(p["spec"].read_text(encoding="utf-8"))
    align = json.loads((p["folder"] / "audio" / "alignment.json").read_text(encoding="utf-8"))
    rep = json.loads((p["pool"] / "livingpage_short.uplift.spec_report.json").read_text(encoding="utf-8"))
    res = {}

    def put(g, ok, ev):
        res[g] = {"pass": bool(ok), "evidence": ev}
        print(f"{g}: {'PASS' if ok else 'FAIL'}  {ev}", flush=True)

    # U1
    nv, ov = probe(new, "v:0", "width,height,r_frame_rate,duration"), probe(old, "v:0", "width,height,r_frame_rate,duration")
    na, oa = probe(new, "a:0", "duration,codec_name,sample_rate"), probe(old, "a:0", "duration,codec_name,sample_rate")
    fn, fo = count_frames(new), count_frames(old)
    ok = (nv["width"], nv["height"]) == (1080, 1920) and nv["r_frame_rate"] == "30/1" and abs(fn - fo) <= 1 and abs(float(na["duration"]) - float(oa["duration"])) < 0.034
    put("U1", ok, f"new {nv['width']}x{nv['height']} {nv['r_frame_rate']} frames {fn} vs shipped {fo}; audio {na['duration']}s vs {oa['duration']}s; video {nv['duration']}s vs {ov['duration']}s")
    # U2
    mn, mo = audio_md5(new), audio_md5(old)
    put("U2", mn == mo and len(mn) > 8, f"audio MD5 new={mn} shipped={mo}")
    # U4
    worst = max((r["factor"] for r in rep["speed"]), default=1.0)
    boom = [r for r in rep["speed"] if r["boomerang"]]
    put("U4", worst <= 1.05 and not boom, f"{len(rep['speed'])} panel slots; worst factor {worst}x; boomerang slots {len(boom)}; stretched slots: " +
        "; ".join(f"beat {r['beat']} p{r['panel']} {r['slug']} slot {r['slot_s']}s clip {r['clip_s']}s x{r['factor']}" for r in rep["speed"] if r["factor"] > 1.0))
    # U5
    from collections import Counter
    uses, full, same_page = Counter(), Counter(), []
    for b in spec["beats"]:
        units = [(pt["tpl"], pt["clips"]) for pt in b["parts"]] if "parts" in b else [(b["tpl"], b["clips"])]
        for tpl, cl in units:
            slugs = [c["slug"] for c in cl]
            if len(set(slugs)) != len(slugs):
                same_page.append((b["t"], slugs))
            for s in slugs:
                uses[s] += 1
                if tpl == "full":
                    full[s] += 1
    over = {s: n for s, n in uses.items() if n > 3}
    fover = {s: n for s, n in full.items() if n > 1}
    put("U5", not same_page and not over and not fover,
        f"uses per clip {dict(uses)}; full-bleed uses {dict(full)}; same clip twice on a page: {same_page or 'none'}; >3 uses: {over or 'none'}; full-bleed >1: {fover or 'none'}; "
        "inserts (4-frame recalls) are exempt by design")
    # U6 (timing parts)
    marks = mk["marks"]
    fails = []
    if len(marks) > 6:
        fails.append(f"count {len(marks)} > 6")
    iv = sorted((m["at"], m.get("until", m["at"] + 30), m["id"]) for m in marks)
    for a, b in zip(iv, iv[1:]):
        if b[0] < a[1]:
            fails.append(f"{a[2]} and {b[2]} overlap in time")
    words = {}
    for w in align:
        words.setdefault(w["w"].strip(".,!?;:").lower(), []).append(w)
    for m in marks:
        wd = m.get("word")
        if wd:
            cand = [w for w in align if abs(w["start"] - wd["start"]) < 0.01 and w["w"].strip(".,!?;:").lower() == wd["w"].lower()]
            if not cand:
                fails.append(f"{m['id']} word {wd} not in alignment")
            elif m["at"] < math.ceil(cand[0]["start"] * 30) - 0:
                fails.append(f"{m['id']} starts at frame {m['at']} BEFORE word '{wd['w']}' frame {math.ceil(cand[0]['start'] * 30)}")
        if mk.get("jesus_beats"):
            for jb in mk["jesus_beats"]:
                if m["at"] < jb[1] * 30 and m.get("until", m["at"]) > jb[0] * 30:
                    fails.append(f"{m['id']} overlaps a JESUS quote beat {jb}")
        if m.get("until", m["at"]) > mk["last_beat_from"] * 30:
            fails.append(f"{m['id']} runs into the last beat")
    put("U6a", not fails, f"{len(marks)} marks; " + (", ".join(fails) if fails else "count ok, none overlap, none before their word, none in a JESUS beat, none on the last beat"))
    res["_marks"] = [{"id": m["id"], "kind": m["kind"], "at": m["at"], "until": m.get("until"), "word": m.get("word")} for m in marks]

    # U6b/U7 pixel: marks-only render vs no_draw boxes and caption boxes
    ptxt = []
    bad = []
    mo = p["rem_marks"]
    wbx = json.loads((p["pool"] / "word_boxes.json").read_text(encoding="utf-8"))
    beats = spec["beats"]
    for m in marks:
        end = m.get("until", m["at"] + 20)
        for t in np.linspace(m["at"] / 30, end / 30 - 1 / 30, 6):
            fr = frame(mo, t)
            ink = fr.max(axis=2) > 40
            for nd in mk.get("no_draw", []):
                if nd["f0"] <= t * 30 < nd["f1"]:
                    x, y, w, h = nd["box"]
                    c = int(ink[y:y + h, x:x + w].sum())
                    if c > 0:
                        bad.append(f"{m['id']} t={t:.2f}s {c}px inside no_draw {nd['label']}")
            for i, b in enumerate(beats, 1):
                if b["t"][0] <= t < b["t"][1] and str(i) in wbx and wbx[str(i)]["zone"] and not m.get("on_caption_word"):
                    x, y, w, h = wbx[str(i)]["zone"]
                    c = int(ink[y:y + h, x:x + w].sum())
                    if c > 0:
                        bad.append(f"{m['id']} t={t:.2f}s {c}px inside caption zone of beat {i}")
    put("U6b/U7", not bad, "marks-only render sampled 6 times per mark against no_draw boxes and caption zones: " + ("; ".join(bad) if bad else "0 px inside any no_draw box or caption zone"))

    # U3: unchanged beats vs shipped
    unchanged = mk.get("unchanged_beats", [])
    diffs = []
    for bi in unchanged:
        b = beats[bi - 1]
        ts = np.linspace(b["t"][0] + 0.3, b["t"][1] - 0.3, 5)
        for t in ts:
            if any(tr["at"] / 30 - 0.05 <= t <= (tr["at"] + tr["frames"]) / 30 + 0.05 for tr in mk["turns"]):
                continue
            skip = any(m["at"] / 30 - 0.05 <= t <= m.get("until", m["at"] + 20) / 30 + 0.05 for m in marks)
            if skip:
                continue
            a, c = frame(new, t), frame(old, t)
            diffs.append((bi, round(float(np.abs(a - c).mean()), 3)))
    mean = max((d for _, d in diffs), default=0.0)
    put("U3", mean < 2.0, f"unchanged beats {unchanged}: {len(diffs)} frames compared, max mean-abs pixel diff {mean} (limit 2.0); " + str(diffs))
    print("U8: eye check = contact sheets (manual, see review page).  U9: blind red team NOT RUN (owner-gated panel).")
    res["U8"] = {"pass": None, "evidence": "manual contact-sheet look, see run notes"}
    res["U9"] = {"pass": None, "evidence": "NOT RUN: needs the independent Fable seat + AI panel before any pin or upload"}
    (p["pool"] / "gates_result.json").write_text(json.dumps(res, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
