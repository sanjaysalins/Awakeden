"""$0 pace test: python pace_test.py <episode_dir> --pages f01,f02 [--out DIR]. ffmpeg only."""
import argparse, importlib.util, json, re, subprocess, sys
from pathlib import Path

FRONT, PAGE, BACK = 2.5, 6.0, 7.0
OUT = Path(__file__).resolve().parent

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"FAILED: {' '.join(map(str,cmd))}\n{r.stderr[-1500:]}")
    return r.stdout

def dur(p):
    return float(run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(p)]).strip())

ap = argparse.ArgumentParser(); ap.add_argument("ep"); ap.add_argument("--pages", required=True)
a = ap.parse_args()
ep = Path(a.ep).resolve(); tag = "ep" + re.search(r"episode_(\d+)", ep.name).group(1)
sys.dont_write_bytecode = True
sys.path.insert(0, str(ep))
sp = importlib.util.spec_from_file_location("epmod", ep / "episode.py")
m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
units = m.MANIFEST.units
words = [w for w in json.load(open(ep/"narration.alignment.json", encoding="utf-8"))["words"] if re.search(r"[A-Za-z0-9]", w["text"])]

# unit -> (first_idx, last_idx_excl); starts
total = sum(u.words for u in units)
sound = total == len(words)
note = "" if sound else f"MISMATCH manifest words {total} vs alignment {len(words)}: built SILENT"
spans, i = {}, 0
for u in units:
    spans[u.tag] = (i, i + u.words); i += u.words
ut = ep / "unit_timing.json"
if ut.exists():
    t = json.load(open(ut))["units"]; ustart = {k: v["start_s"] for k, v in t.items()}; uend = {k: v["end_s"] for k, v in t.items()}
else:
    ustart = {}; uend = {}
    for k, (s, e) in spans.items():
        if sound and e > s: ustart[k] = words[s]["start"]
    ks = [u.tag for u in units]
    for n, k in enumerate(ks):
        if k in ustart: uend[k] = ustart[ks[n+1]] if n+1 < len(ks) else 1e9
    if "front" in ustart: ustart["front"] = 0.0

def clip(t):
    if t == "front": return ep/"front_cover.mp4"
    if t == "back": return ep/"back_cover.mp4"
    return ep/f"{ep.name}_{t}_9x16.mp4"

order = [("front", FRONT)] + [(p.strip(), PAGE) for p in a.pages.split(",")] + [("back", BACK)]
byname = {u.tag: u for u in units}
table, slots, logs = [], [], []
for t, want in order:
    c = clip(t); L = dur(c); s = min(want, L)
    if s < want: logs.append(f"{tag} {t}: slot capped {want}->{s:.3f} (clip {L:.3f}s)")
    slots.append((t, c, s))
    row = {"unit": t, "slot_s": round(s, 3)}
    spec = getattr(m, t.upper(), None) if t.startswith("f") else None
    if spec:
        row["baked"] = {"seq_title": spec.seq_title, "frame_label": spec.frame_label,
                        "panel_labels": [p.label for p in spec.panels],
                        "caption_lines": list(spec.caption_lines), "corner_note": spec.corner_note}
    if sound and t in spans:
        a0, a1 = spans[t]; ws = words[a0:a1]; st = ustart[t]
        inside = [w for w in ws if w["end"] <= st + s + 1e-6]
        row["unit_words_total"] = len(ws)
        row["spoken_in_slot"] = " ".join(w["text"] for w in inside)
        row["spoken_in_slot_count"] = len(inside)
        row["words_cut_off_by_slot"] = len(ws) - len(inside)
        row["cut_off_text"] = " ".join(w["text"] for w in ws[len(inside):])
        row["_cut"] = (st, inside[-1]["end"] if inside else st)
    table.append(row)

# ffmpeg
cmd = ["ffmpeg","-y","-hide_banner","-loglevel","error","-threads","3"]
for t, c, s in slots: cmd += ["-ss","0","-t",f"{s:.3f}","-i",str(c)]
nin = len(slots)
if sound: cmd += ["-i", str(ep/"narration.mp3")]
fc = []
for k, (t, c, s) in enumerate(slots):
    fc.append(f"[{k}:v]fps=24,scale=1080:1920:flags=lanczos,setsar=1,trim=duration={s:.3f},setpts=PTS-STARTPTS[v{k}]")
    r = next(x for x in table if x["unit"] == t)
    if sound and "_cut" in r and r["_cut"][1] > r["_cut"][0]:
        a0, a1 = r["_cut"]
        fc.append(f"[{nin}:a]atrim={a0:.3f}:{a1:.3f},asetpts=PTS-STARTPTS,aresample=48000,apad=whole_dur={s:.3f},atrim=0:{s:.3f}[a{k}]")
    else:
        fc.append(f"anullsrc=r=48000:cl=mono,atrim=0:{s:.3f}[a{k}]")
fc.append("".join(f"[v{k}][a{k}]" for k in range(nin)) + f"concat=n={nin}:v=1:a=1[v][a]")
outp = OUT/f"{tag}_pace_6s.mp4"
cmd += ["-filter_complex",";".join(fc),"-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","160k","-ar","48000","-movflags","+faststart",str(outp)]
run(cmd)
for r in table: r.pop("_cut", None)
# phone frames
for t, c, s in slots:
    if t.startswith("f"):
        run(["ffmpeg","-y","-hide_banner","-loglevel","error","-threads","3","-i",str(c),"-frames:v","1","-vf","scale=390:-2","-q:v","3",str(OUT/f"phone_{tag}_{t}.jpg")])
tp = OUT/"pace_table.json"
db = json.load(open(tp)) if tp.exists() else {}
db[tag] = {"film": outp.name, "sound": "own narration per unit" if sound else note, "logs": logs, "pages": table}
json.dump(db, open(tp, "w", indent=1) if False else open(tp,"w",encoding="utf-8"), indent=1, ensure_ascii=False)
print(tag, "built", outp, f"{dur(outp):.2f}s", note, *logs, sep="\n")
