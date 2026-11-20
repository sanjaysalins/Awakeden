"""$0 v6 TRIM rebuild of The Sign of Jonah (cut-only, 69.5 s -> ~64 s). Same recorded voice, same clips.
Beats are RE-TIMED to their own sentence starts in the forced alignment (v5 beats led the voice by up to ~2 s),
as in women_first_witnesses_luke245/trim_v6. Re-applies the v5 hook card + JONAS decode card (fixes/sign-of-jonah.json).
  .venv\\Scripts\\python.exe <this> <CUT_SET> [prep|build|score|sfx|final|all]     CUT_SET = M | B"""
import json, shutil, subprocess, sys
from pathlib import Path

H = Path(__file__).resolve().parent
P = H.parent
ROOT = P.parents[2]
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
BK = H / "_v5_backup"
SPEC = P / "visual" / "livingpage_short.spec.json"
S = json.load(open(H / "sentences.json", encoding="utf-8"))
SETS = {"M": ((6, 12, 18), "preview_M_merged.mp3"), "B": ((6, 7, 18), "preview_B_sonnet.mp3")}
CUT_IDS, PREVIEW = SETS[sys.argv[1]]
FINAL = P / "visual" / "sign_of_jonah_matt1240_sfx_v6trim.mp4"
STEM = "sign_of_jonah_matt1240"
# v5 beat -> sentence IDs; b10 starts at the word 'so' inside S10 (the second half of Matthew 12:40)
BEAT_SENT = {0: [0], 1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 6: [6], 7: [7], 8: [8, 9], 9: [10], 10: "SO",
             11: [11, 12], 12: [13], 13: [14], 14: [15], 15: [16], 16: [17, 18], 17: [19], 18: [20], 19: [21]}
CAPS = {"I went down guilty. The storm was mine.": "I went down guilty",
        "That is how far His mercy reaches. It cost Him the grave.": "That is how far His mercy reaches."}
FONT = "C\\:/Windows/Fonts/impact.ttf"


def mid(a, b): return (a + b) / 2


def cuts():
    c = []
    for i in sorted(CUT_IDS):
        a = mid(S[i - 1]["end"], S[i]["start"])
        b = mid(S[i]["end"], S[i + 1]["start"]) if i + 1 < len(S) else 10 ** 6
        if c and a <= c[-1][1] + 1e-6:
            c[-1] = (c[-1][0], b)
        else:
            c.append((a, b))
    return c


CUTS = cuts()


def f(t):
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


def src(rel): return BK / rel.replace("/", "__")


def backup():
    BK.mkdir(exist_ok=True)
    for rel in ["audio/narration.mp3", "audio/alignment.json", "audio/narration.spoken.txt", "narration.md", "piece.json",
                "FINAL_VIDEO.txt", "visual/livingpage_short.spec.json", "visual/livingpage_short.spec_preview.mp4",
                f"visual/{STEM}_scored.mp4", f"visual/{STEM}_sfx.mp4"]:
        dst = BK / rel.replace("/", "__")
        if not dst.exists():
            shutil.copy2(P / rel, dst)


def prep():
    backup()
    full = json.load(open(src("audio/alignment.json"), encoding="utf-8"))
    shutil.copy2(H / PREVIEW, P / "audio" / "narration.mp3")
    total = round(dur(P / "audio" / "narration.mp3"), 2)
    keep = [dict(w, start=f(w["start"]), end=f(w["end"])) for w in full
            if not any(x <= mid(w["start"], w["end"]) <= y for x, y in CUTS)]
    json.dump(keep, open(P / "audio" / "alignment.json", "w", encoding="utf-8"), ensure_ascii=False)
    (P / "audio" / "narration.spoken.txt").write_text(" ".join(w["w"] for w in keep), encoding="utf-8")
    so = next(w["start"] for w in full if w["w"] == "so" and w["start"] > S[10]["start"])
    sp = json.load(open(src("visual/livingpage_short.spec.json"), encoding="utf-8"))
    sp.update(total=total, _doc=f"v6 TRIM {sys.argv[1]} + RESYNC (2026-11-20, cut-only; beats re-timed to the voice): " + sp["_doc"])
    B, beats = {}, []
    for i, b in enumerate(sp["beats"]):
        m = BEAT_SENT[i]
        if m != "SO" and all(x in CUT_IDS for x in m):
            continue
        first = f(so) if m == "SO" else (0.0 if i == 0 else f(S[[x for x in m if x not in CUT_IDS][0]]["start"]))
        b["_shift"], b["t"] = first - b["t"][0], [first, None]
        if b["cap"]["text"] in CAPS:
            b["cap"]["text"] = CAPS[b["cap"]["text"]]
        B[i] = b
        beats.append(b)
    for k, b in enumerate(beats):
        b["t"][1] = beats[k + 1]["t"][0] if k + 1 < len(beats) else total
        t0, t1, sh = b["t"][0], b["t"][1], b.pop("_shift")
        clamp = lambda x: round(min(max(t0, x + sh), t1 - 0.05), 3)
        if "panel_at" in b:
            b["panel_at"] = [clamp(x) for x in b["panel_at"]]
        if b.get("takeover"):
            b["takeover"]["start"] = clamp(b["takeover"]["start"])
        if b.get("sfx"):
            b["sfx"] = [[n, clamp(t), g] for n, t, g in b["sfx"]]
        if b.get("border_break"):
            b["border_break"]["at"] = clamp(b["border_break"]["at"])
    if 7 in B:
        sp["heartbeat"]["from"], sp["heartbeat"]["to"] = B[7]["t"]
    else:
        sp.pop("heartbeat", None)  # its beat ('Three days buried alive') is cut
    sp["beats"] = beats
    SPEC.write_text(json.dumps(sp, indent=1, ensure_ascii=False), encoding="utf-8")
    s = lambda i: B[i]["t"][0]
    e = lambda i: B[i]["t"][1]
    w_my = next(w["start"] for w in keep if w["w"] == "my" and w["start"] > s(8))
    w_heart = next(w["end"] for w in keep if w["w"].startswith("heart") and w["start"] > s(8))
    pj = json.load(open(src("piece.json"), encoding="utf-8"))
    sc = pj["score"]
    sc.update(base_seconds=total, outro_hold=0.0, tpad="0", fade_out=2.5, dark_trim_end=f"{s(14) - 0.08:.1f}",
              dips=[[f"{w_my - 0.13:.2f}", f"{w_heart + 0.35:.2f}", sc["dips"][0][2]]], cta_dip=[f"{s(16):.2f}", sc["cta_dip"][1]])
    pj["score"] = sc
    (P / "piece.json").write_text(json.dumps(pj, indent=2, ensure_ascii=False), encoding="utf-8")
    sink = s(7) if 7 in B else s(8) - 1.0
    layers = [  # the v5 beds of build_jonah_sfx.py, re-anchored to the re-timed beats
        ("sea", "sea_waves_shore", "loop", 0.0, sink, -35.0, "fin=0.3, fout=2.5"),
        ("thunder1", "thunder_low_roll", "oneshot", 0.3, 4.0, -30.0, "fout=2.0"),
        ("thunder2", "thunder_low_roll", "oneshot", s(5) + 0.1, 4.0, -33.0, "fout=2.5"),
        ("creak", "boat_creak_oars", "loop", s(2), e(5) - s(2), -40.0, "fin=1.0, fout=2.0"),
        ("plunge", "rumble_deep_sub", "oneshot", e(5), 4.5, -32.0, "fin=0.2, fout=2.5"),
        ("murmur", "crowd_murmur_distant", "loop", s(8), e(8) - s(8), -38.0, "fin=0.8, fout=1.2"),
        ("hollow2", "air_hollow_desolate", "loop", s(9), s(12) - s(9), -38.0, 'filt="lowpass=f=3000", fin=1.5, fout=2.0'),
        ("wind", "wind_desert_bleak", "loop", s(12), e(13) - s(12), -41.0, "fin=2.0, fout=1.5"),
        ("stone", "stone_roll_tomb", "oneshot", s(14) - 0.08, 2.2, -27.0, "fout=0.8"),
        ("dawn", "dawn_morning_warm", "loop", s(14) + 0.4, total - s(14) - 0.4, -36.0, 'filt="lowpass=f=3400", fin=3.0'),
    ]
    if 7 in B:
        layers.append(("hollow1", "air_hollow_desolate", "loop", s(7), e(7) - s(7), -38.0, 'filt="lowpass=f=3000", fin=1.2, fout=1.0'))
    rows = "\n".join(f'    layer("{a}", "{b}", "{c}", {d:.2f}, {g:.2f}, {h}, {k}),' for a, b, c, d, g, h, k in layers)
    sfx = ('"""Ambient/SFX bed for The Sign of Jonah v6 TRIM + RESYNC (2026-11-20). GENERATED by\n'
           'batches/cluster_02_resurrection/sign_of_jonah_matt1240/trim_v6/build_v6.py from the v5 beds\n'
           '(build_jonah_sfx.py, kept unchanged), re-anchored to the re-timed beats."""\n'
           "import sys\nfrom pathlib import Path\nHERE = Path(__file__).resolve().parent\nsys.path.insert(0, str(HERE))\n"
           "import sfxlib\nfrom sfxlib import layer\n\n"
           f'CUT = Path(r"{P / "visual" / (STEM + "_scored.mp4")}")\n'
           f'OUT = CUT.with_name("{STEM}_sfx.mp4")\n\nLAYERS = [\n' + rows + "\n]\n\n"
           'if __name__ == "__main__":\n    sfxlib.show_plan("The Sign of Jonah v6", LAYERS)\n'
           '    sfxlib.build(CUT, OUT, LAYERS)\n    print(f"[ok] {OUT}")\n    sfxlib.measure(OUT)\n')
    (ROOT / "sfx_pilots" / "build_jonah_sfx_v6.py").write_text(sfx, encoding="utf-8")
    for b in beats:
        print(f'{b["t"][0]:6.2f}-{b["t"][1]:6.2f}  {b["cap"]["text"][:60]}')
    print(f"prep done: total {total} s, {len(beats)} beats, score {sc}")


def build():
    subprocess.run([PY, str(ROOT / "longform/02_Psalm_22_Song_From_The_Cross/build_livingpage_16x9.py"), "--pool", str(P / "visual"),
                    "--spec", "livingpage_short.spec.json", "--clips", "--page", "1080x1920", "--no-ticks"], check=True, cwd=ROOT)


def score():
    subprocess.run([PY, "run_piece.py", str(P), "--stage", "score"], check=True, cwd=ROOT)


def sfx():
    subprocess.run([PY, str(ROOT / "sfx_pilots" / "build_jonah_sfx_v6.py")], check=True, cwd=ROOT)


def final():
    fx = json.loads((ROOT / "poc_comic_page/_audit/fixes/sign-of-jonah.json").read_text(encoding="utf-8-sig"))
    al = json.load(open(P / "audio" / "alignment.json", encoding="utf-8"))
    jonas = next(w["start"] for w in al if w["w"].startswith("Jonas"))
    l1, l2 = [x.strip() for x in fx["hook_text"].split("/")]
    d = fx["decode_cards"][0]
    old_jonas = next(w["start"] for w in json.load(open(src("audio/alignment.json"), encoding="utf-8")) if w["w"].startswith("Jonas"))
    j0, j1 = jonas + (d["t0"] - old_jonas), jonas + (d["t1"] - old_jonas)  # same offset to the spoken word as v5
    cards = [(l1, 104, "white", 930, 0, 2.0), (l2, 104, "0xF2C14E", 1080, 0, 2.0),
             (d["old"], 104, "white", 930, j0, j1), ("= " + d["plain"], 110, "0xF2C14E", 1080, j0, j1)]
    vf = ",".join(f"drawtext=fontfile='{FONT}':text='{t.replace(':', chr(92) + ':')}':fontsize={sz}:fontcolor={c}:box=1:"
                  f"boxcolor=black@0.64:boxborderw=20:x=(w-text_w)/2:y={y}:enable='between(t,{a:.2f},{b:.2f})'"
                  for t, sz, c, y, a, b in cards)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P / "visual" / f"{STEM}_sfx.mp4"), "-vf", vf, "-c:v", "libx264",
                    "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
                    str(FINAL)], check=True)
    print("FINAL ->", FINAL, dur(FINAL))


if __name__ == "__main__":
    st = sys.argv[2] if len(sys.argv) > 2 else "all"
    for name in (["prep", "build", "score", "sfx", "final"] if st == "all" else [st]):
        globals()[name]()
