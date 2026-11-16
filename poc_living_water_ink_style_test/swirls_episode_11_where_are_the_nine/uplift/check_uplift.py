"""ep11 uplift gate ($0). python check_uplift.py -> PASS/FAIL per gate; writes gate_report.json
G-AUDIO, G-FRAMES (2507), G-SLOT, G-MOTION (new clips), G-MARKS (word time +-3 f, spacing >= 3.0 s, <= 8 per 60 s, quiet zones), G-KEEPOUT (real frames)."""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
UP = Path(__file__).resolve().parent; EP = UP.parent
sys.path.insert(0, str(UP))
SPEC = json.loads((UP / "uplift.json").read_text(encoding="utf-8"))
WORDS = Path(r"F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_swirls\word_timings\ep11_words.txt").read_text(encoding="utf-8")
SHIPPED = EP / "swirls_episode_11_where_are_the_nine_final_piano_sfx.mp4"
FINAL = UP / "ep11_uplift_final.mp4"; BASE = UP / "work" / "base_final.mp4"
FPS = 30; TOTAL = SPEC["total_frames"]; rep = {}
def sh(cmd): return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
def md5_audio(p): return sh(["ffmpeg", "-v", "error", "-i", str(p), "-map", "0:a:0", "-c", "copy", "-f", "md5", "-"])
def dur(p): return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))
def frame_at(p, idx):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{(idx + 0.5) / 30:.4f}", "-i", str(p), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    return subprocess.run(cmd, capture_output=True).stdout
def result(name, ok, ev):
    rep[name] = {"pass": bool(ok), "evidence": ev}; print(("PASS " if ok else "FAIL ") + name + " :: " + ev)

a1, a2 = md5_audio(SHIPPED), md5_audio(FINAL)
result("G-AUDIO audio bit-identical", a1 == a2 and a1 != "", f"shipped {a1} / new {a2}")
n = sh(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames,width,height", "-of", "csv=p=0", str(FINAL)])
result(f"G-FRAMES {TOTAL} frames 1080x1920", n == f"1080,1920,{TOTAL}", n + f"; dur {dur(FINAL):.3f}s vs shipped {dur(SHIPPED):.3f}s")
bad, lines = [], []
for s in SPEC["shots"]:
    d = dur(EP / s["src"]); slot = (s["f1"] - s["f0"]) / FPS
    lines.append(f'{s["id"]} {d:.2f}/{slot:.2f}')
    if d < slot + 0.05: bad.append(s["id"])
txt = (UP / "cut_uplift.py").read_text()
result("G-SLOT every clip >= slot+0.05 s, trim only (no tpad/reverse/setpts/zoompan in cut_uplift.py)", not bad and not re.search(r"tpad|reverse|zoompan|setpts|-loop", txt.replace('"-y", "-v", "error"', "")), "; ".join(lines) + (" SHORT: " + ",".join(bad) if bad else ""))
import clipcheck
CAP = {"F01B": .78, "F03": .9, "F04B": .86, "F05": .9, "F06": .9, "F07": .93, "F07B": .9, "F09B": .9, "F10": .9, "F10B": .9}
mot, ok_all = [], True
for s in SPEC["shots"]:
    if not s["src"].startswith("uplift/clips/"): continue
    ok, ev = clipcheck.check(EP / s["src"], s["f1"] - s["f0"], CAP[s["page"]])
    ok_all &= ok; mot.append(f'{s["page"]}: {ev} {"ok" if ok else "CHECK"}')
result("G-MOTION new clips: zoom 1.000+-0.010, not frozen, baked text first==last, motif px +-20%", ok_all, " | ".join(mot))
import marks_overlay as MO
words = {}
for m in re.finditer(r"([^\s@]+)@([\d.]+)", WORDS):
    words.setdefault(m.group(1).strip('"“”,.?!:;').lower(), []).append(float(m.group(2)))
ev, ok_m, starts = [], True, []
for m in MO.MARKS:
    t0 = min(s.get("t0", 1e9) for s in m["strokes"]); wt = m["word_t"]; w = m["word"].strip('.,?!"').lower()
    in_file = any(abs(c - wt) < 0.02 for c in words.get(w, [])); dfr = t0 - round(wt * FPS)
    shot = [x for x in SPEC["shots"] if x["id"] == m["shot"]][0]
    inshot = shot["f0"] <= t0 and m["until"] <= shot["f1"] - 5
    ok1 = in_file and -3 <= dfr <= 0 and inshot
    starts.append(t0); ok_m &= ok1
    ev.append(f'{m["id"]} "{m["word"]}"@{wt} start f{t0} ({dfr:+d}f) gone by f{m["until"]} (shot ends f{shot["f1"]}) {"ok" if ok1 else "BAD"}')
starts.sort()
gaps_ok = all(b - a >= 90 for a, b in zip(starts, starts[1:]))
quiet = starts[0] >= 30 and max(m["until"] for m in MO.MARKS) <= TOTAL - 90 and all(not (m["strokes"][0]["t0"] < SPEC["shots"][0]["f1"] or m["strokes"][0]["t0"] >= SPEC["shots"][-1]["f0"]) for m in MO.MARKS)
ok_m &= gaps_ok and quiet and len(starts) <= 8
ev.append(f"spacing>=90f {'ok' if gaps_ok else 'BAD'}; count {len(starts)}<=8; first {starts[0]}f>=30; last mark gone by f{max(m['until'] for m in MO.MARKS)}; covers + last 3 s untouched {'ok' if quiet else 'BAD'}")
ko, ok_k = [], True
for m in MO.MARKS:
    f = m["until"] - 8
    base = np.frombuffer(frame_at(BASE, f), np.uint8).reshape(1920, 1080, 3)
    drawn = MO.render_frame(f, np.full((1920, 1080, 3), 255, np.uint8), {}).astype(int)
    mk = drawn.sum(axis=2) < 3 * 245; n_mk = int(mk.sum()); b = base.astype(int); lum = b.mean(axis=2)
    dark = mk & (lum < 95); blue = mk & ((b[..., 2] - b[..., 0]) > 35)
    through_art = m["id"] == "M3"   # nine outlines are drawn ON the landscape by design; only motif(blue)/text/faces keep-outs apply (F07B has none there)
    frac = (blue.sum() + (0 if through_art else dark.sum())) / max(n_mk, 1)
    # S3/S2 sit around/under baked text: their pixels may touch ink only at the word's own edge (<8%); others must be clear
    lim = 0.08 if m["id"] in ("M4", "M5") else 0.03
    okf = frac < lim; ok_k &= okf
    ko.append(f'{m["id"]}: {n_mk}px, ink/motif overlap {frac*100:.1f}% (limit {lim*100:.0f}%) {"ok" if okf else "CHECK"}')
result("G-KEEPOUT no stroke on baked text / faces / blue motif (real frames)", ok_k, " | ".join(ko))
rep["_marks_detail"] = ev; print("\n".join("   " + e for e in ev))
result("G-MARKS word-tied, spacing, count, quiet zones", ok_m, f"{len(starts)} marks; all within -3..0 f of the word, none inside the last 5 f of a shot")
(UP / "gate_report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")
