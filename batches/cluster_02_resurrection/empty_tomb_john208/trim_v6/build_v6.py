"""$0 v6 TRIM rebuild of The Empty Tomb (owner pick 2026-11-20: candidate D, cut-only, 79 s -> ~65 s).
Same recorded voice, same clips. Steps (each idempotent; v5 inputs backed up once to _v5_backup/):
  prep   -> narration.mp3 (= preview_D, voice + 3.0 s hold), alignment.json, spec, piece.json, sfx script, all remapped
  build  -> living-page engine (preview mp4)
  score  -> run_piece --stage score (2.5 s fade, no frozen outro: the 3 s hold is real moving picture)
  sfx    -> sfx_pilots/build_empty_tomb_sfx_v6.py
  cards  -> the v5 SEPULCHRE = TOMB decode card, remapped -> visual/empty_tomb_john208_sfx_v6trim.mp4
FINAL_VIDEO.txt is NOT switched here (owner OK first).
  .venv\\Scripts\\python.exe <this> [prep|build|score|sfx|cards|all]"""
import json, shutil, subprocess, sys
from pathlib import Path

H = Path(__file__).resolve().parent
P = H.parent
ROOT = P.parents[2]
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
BK = H / "_v5_backup"
SPEC = P / "visual" / "livingpage_short.spec.json"
S = json.load(open(H / "sentences.json", encoding="utf-8"))
HOLD = 3.0
FONT = "C\\:/Windows/Fonts/impact.ttf"
FINAL = P / "visual" / "empty_tomb_john208_sfx_v6trim.mp4"


def mid(a, b): return (a + b) / 2


def cuts_D():
    c = [(mid(S[1]["end"], S[2]["start"]), 7.20)]  # 'The first day of the week, while it was still dark,'
    for i in (12, 13, 14, 15, 21, 28, 32):
        a = mid(S[i - 1]["end"], S[i]["start"])
        b = mid(S[i]["end"], S[i + 1]["start"]) if i + 1 < len(S) else 10 ** 6
        c.append((a, b))
    c.sort()
    out = []
    for a, b in c:  # merge touching
        if out and a <= out[-1][1] + 1e-6:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


CUTS = cuts_D()
VOICE_END = S[-1]["end"]


def f(t):
    """old time -> new time (a time inside a cut snaps to the cut point)."""
    sh = 0.0
    for a, b in CUTS:
        if t >= b:
            sh += b - a
        elif t > a:
            return round(a - sh, 3)
    return round(t - sh, 3)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout.strip())


def backup():
    BK.mkdir(exist_ok=True)
    for rel in ["audio/narration.mp3", "audio/alignment.json", "audio/narration.spoken.txt", "narration.md", "piece.json",
                "visual/livingpage_short.spec.json", "visual/livingpage_short.spec_preview.mp4",
                "visual/empty_tomb_john208_scored.mp4", "visual/empty_tomb_john208_sfx.mp4"]:
        dst = BK / rel.replace("/", "__")
        if not dst.exists():
            shutil.copy2(P / rel, dst)


def src(rel): return BK / rel.replace("/", "__")


def prep():
    backup()
    # 1. voice: cut-only from the v5 narration, + 3.0 s hold (same recipe as the owner-heard preview_D)
    shutil.copy2(H / "preview_D_merged_at_linen.mp3", P / "audio" / "narration.mp3")
    total = round(dur(P / "audio" / "narration.mp3"), 2)
    # 2. alignment
    a = json.load(open(src("audio/alignment.json"), encoding="utf-8"))
    keep = [dict(w, start=f(w["start"]), end=f(w["end"])) for w in a
            if not any(x <= mid(w["start"], w["end"]) <= y for x, y in CUTS)]
    json.dump(keep, open(P / "audio" / "alignment.json", "w", encoding="utf-8"), ensure_ascii=False)
    (P / "audio" / "narration.spoken.txt").write_text(" ".join(w["w"] for w in keep), encoding="utf-8")
    # 3. spec
    sp = json.load(open(src("visual/livingpage_short.spec.json"), encoding="utf-8"))
    sp["audio"] = "../audio/narration.mp3"
    sp["total"] = total
    sp["_doc"] = "v6 TRIM (2026-11-20, owner pick D, cut-only): " + sp["_doc"]
    sp.pop("heartbeat", None)  # its whole window ('No angel ... Only the linen') is cut
    beats = []
    for b in sp["beats"]:
        t0, t1 = f(b["t"][0]), f(b["t"][1])
        if t1 - t0 < 0.3:
            continue
        b["t"] = [t0, t1]
        if "panel_at" in b:
            b["panel_at"] = [max(t0, f(x)) for x in b["panel_at"]]
        if b.get("takeover"):
            b["takeover"]["start"] = min(max(t0, f(b["takeover"]["start"])), t1)
        if b.get("sfx"):
            b["sfx"] = [[n, f(t), g] for n, t, g in b["sfx"] if not any(x <= t <= y for x, y in CUTS)]
        beats.append(b)
    beats[-1]["t"][1] = total  # last beat (the risen Christ, 'the Lord is risen') carries the 3 s hold
    caps = {"While it was still dark, the stone stood rolled away": ("She found the stone rolled away", "ROLLED AWAY"),
            "He did not yet know the scripture. The linen was enough.": ("He did not yet know the scripture", "NOT YET")}
    for b in beats:
        c = b.get("cap") or {}
        if c.get("text") in caps:
            c["text"], c["kw"] = caps[c["text"]]
    for i in range(len(beats) - 1):
        assert abs(beats[i]["t"][1] - beats[i + 1]["t"][0]) < 1e-6, (i, beats[i]["t"], beats[i + 1]["t"])
    sp["beats"] = beats
    SPEC.write_text(json.dumps(sp, indent=1, ensure_ascii=False), encoding="utf-8")
    # 4. score: total = voice+hold already in the mp3, so no frozen outro; 2.5 s fade (owner rule 2026-11-16)
    pj = json.load(open(src("piece.json"), encoding="utf-8"))
    sc = pj["score"]
    sc.update(base_seconds=total, outro_hold=0.0, tpad="0", fade_out=2.5,
              dark_trim_end=f"{f(float(sc['dark_trim_end'])):.1f}",
              cta_dip=[f"{f(float(sc['cta_dip'][0])):.2f}", sc["cta_dip"][1]])
    (P / "piece.json").write_text(json.dumps(pj, indent=2, ensure_ascii=False), encoding="utf-8")
    # 5. sfx layers remapped
    v5 = (ROOT / "sfx_pilots" / "build_empty_tomb_sfx.py").read_text(encoding="utf-8")
    sys.path.insert(0, str(ROOT / "sfx_pilots"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("et5", ROOT / "sfx_pilots" / "build_empty_tomb_sfx.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    lines = []
    for L in m.LAYERS:
        d = dict(L) if isinstance(L, dict) else vars(L)
        lines.append(d)
    print("sfx layer fields:", list(lines[0]))
    (H / "_sfx_layers_v5.json").write_text(json.dumps(lines, indent=1, default=str), encoding="utf-8")
    print(f"prep done: total {total} s, {len(beats)} beats, cuts {CUTS}")


def build():
    subprocess.run([PY, str(ROOT / "longform/02_Psalm_22_Song_From_The_Cross/build_livingpage_16x9.py"), "--pool", str(P / "visual"),
                    "--spec", "livingpage_short.spec.json", "--clips", "--page", "1080x1920", "--no-ticks"], check=True, cwd=ROOT)


def score():
    subprocess.run([PY, "run_piece.py", str(P), "--stage", "score"], check=True, cwd=ROOT)


def sfx():
    subprocess.run([PY, str(ROOT / "sfx_pilots" / "build_empty_tomb_sfx_v6.py")], check=True, cwd=ROOT)


def cards():
    fx = json.loads((ROOT / "poc_comic_page/_audit/fixes/the-empty-tomb.json").read_text(encoding="utf-8-sig"))
    vf = []
    # v5 cards are in OLD time (remapped); the v6 guardrail panel added NAPKIN (3 of 4 seats), already in NEW time
    cards_new = [(f(d["t0"]), f(d["t1"]), d) for d in fx["decode_cards"]]
    cards_new.append((19.4, 21.3, {"old": "NAPKIN", "plain": "HEAD CLOTH"}))
    for t0, t1, d in cards_new:
        for txt, size, col, y in ((d["old"], 110, "white", 170), ("= " + d["plain"], 120, "0xF2C14E", 320)):
            vf.append(f"drawtext=fontfile='{FONT}':text='{txt}':fontsize={size}:fontcolor={col}:box=1:boxcolor=black@0.64:"
                      f"boxborderw=20:x=(w-text_w)/2:y={y}:enable='between(t,{t0},{t1})'")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P / "visual/empty_tomb_john208_sfx.mp4"), "-vf", ",".join(vf),
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy",
                    "-movflags", "+faststart", str(FINAL)], check=True)
    print("FINAL ->", FINAL, dur(FINAL))


if __name__ == "__main__":
    st = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name in (["prep", "build", "score", "sfx", "cards"] if st == "all" else [st]):
        globals()[name]()
