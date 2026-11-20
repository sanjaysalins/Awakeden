"""$0 v6 TRIM rebuild of Women as First Witnesses (owner pick 2026-11-20: candidate F, cut-only, 82 s -> ~63.5 s).
Same recorded voice, same clips. ALSO FIXES a shipped sync bug: the v5 spec beats ran up to ~6 s AHEAD of the voice
(21-38 s; checked by transcribing the shipped film). Here every beat is RE-TIMED to its own sentence in a fresh
forced alignment (trim_v6/align_full.py), not remapped from the old beat times.
Steps: prep | build | score | sfx | final | all   (v5 inputs backed up once to _v5_backup/)
FINAL_VIDEO.txt is NOT switched here (owner OK first)."""
import json, shutil, subprocess, sys
from pathlib import Path

H = Path(__file__).resolve().parent
P = H.parent
ROOT = P.parents[2]
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
BK = H / "_v5_backup"
SPEC = P / "visual" / "livingpage_short.spec.json"
S = json.load(open(H / "sentences.json", encoding="utf-8"))
CUT_IDS = (6, 7, 8, 9, 10, 19, 20, 23)
FINAL = P / "visual" / "women_first_witnesses_luke245_sfx_v6trim.mp4"
# v5 beat index -> the sentence IDs it carries (None = beat is cut). b11/b12 split S17 at the word 'Saying,'.
BEAT_SENT = {0: [0, 1], 1: [2], 2: [3, 4], 3: [5], 4: None, 5: None, 6: [11], 7: [12], 8: [13], 9: [14],
             10: [15, 16], 11: [17], 12: "SAYING", 13: [18], 14: None, 15: [21], 16: [22], 17: [24, 25]}
CAPS = {16: ("He still sends His word to the overlooked.", None)}


def mid(a, b): return (a + b) / 2


def cuts():
    c = []
    for i in CUT_IDS:
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
    for rel in ["audio/narration.mp3", "narration.md", "piece.json", "visual/livingpage_short.spec.json",
                "visual/livingpage_short.spec_preview.mp4", "visual/women_first_witnesses_luke245_scored.mp4",
                "visual/women_first_witnesses_luke245_sfx.mp4"]:
        dst = BK / rel.replace("/", "__")
        if not dst.exists():
            shutil.copy2(P / rel, dst)
    # alignment.json / spoken.txt were backed up (as audio_*) before align_full.py replaced them


def prep():
    backup()
    full = json.load(open(P / "audio" / "alignment.json", encoding="utf-8"))  # the full (fixed) alignment, OLD time
    if not (BK / "alignment_full_v5time.json").exists():
        json.dump(full, open(BK / "alignment_full_v5time.json", "w", encoding="utf-8"))
    full = json.load(open(BK / "alignment_full_v5time.json", encoding="utf-8"))
    shutil.copy2(H / "preview_F_fable.mp3", P / "audio" / "narration.mp3")
    total = round(dur(P / "audio" / "narration.mp3"), 2)
    keep = [dict(w, start=f(w["start"]), end=f(w["end"])) for w in full
            if not any(x <= mid(w["start"], w["end"]) <= y for x, y in CUTS)]
    json.dump(keep, open(P / "audio" / "alignment.json", "w", encoding="utf-8"), ensure_ascii=False)
    (P / "audio" / "narration.spoken.txt").write_text(" ".join(w["w"] for w in keep), encoding="utf-8")
    saying = next(w["start"] for w in full if w["w"].startswith("Saying"))
    sp = json.load(open(src("visual/livingpage_short.spec.json"), encoding="utf-8"))
    sp.update(total=total, _doc="v6 TRIM + RESYNC (2026-11-20, owner pick F, cut-only; beats re-timed to the voice): " + sp["_doc"])
    beats = []
    for i, b in enumerate(sp["beats"]):
        m = BEAT_SENT[i]
        if m is None:
            continue
        old0 = b["t"][0]
        start = f(saying) if m == "SAYING" else (0.0 if i == 0 else f(S[m[0]]["start"]))
        b["_shift"] = start - old0
        b["t"] = [start, None]
        if i in CAPS:
            b["cap"]["text"] = CAPS[i][0]
        if i == 12:  # guardrail fix (Fable + Sonnet): Luke 24:1-11 has no appearance of Jesus, so not the risen Christ here
            b["clips"] = [{"slug": "women_remember", "motion": "pushin"}]  # unused, audited PASS; Luke 24:8 'they remembered'
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
    why = next(b for b in beats if b["cap"]["text"].startswith("Why seek ye"))
    sp["heartbeat"]["from"], sp["heartbeat"]["to"] = why["t"]
    sp["beats"] = beats
    SPEC.write_text(json.dumps(sp, indent=1, ensure_ascii=False), encoding="utf-8")
    B = {i: b for i, b in zip([i for i in range(18) if BEAT_SENT[i] is not None], beats)}
    pj = json.load(open(src("piece.json"), encoding="utf-8"))
    sc = pj["score"]
    sc.update(base_seconds=total, outro_hold=0.0, tpad="0", fade_out=2.5,
              dark_trim_end=f"{B[11]['t'][0] - 1.0:.1f}", cta_dip=[f"{B[17]['t'][0]:.2f}", sc["cta_dip"][1]])
    (P / "piece.json").write_text(json.dumps(pj, indent=2, ensure_ascii=False), encoding="utf-8")
    s = lambda i: B[i]["t"][0]
    e = lambda i: B[i]["t"][1]
    layers = [  # same beds as v5 build_women_witnesses_sfx.py, anchored to the re-timed beats
        ("room", "air_hollow_desolate", "loop", 0.0, s(6), -41.0, 'filt="lowpass=f=2800", fin=1.0, fout=1.5'),
        ("grief", "wind_desert_bleak", "loop", s(6), e(7) - s(6), -38.0, "fin=1.0, fout=1.5"),
        ("dawnstep", "footsteps_dirt_approach", "oneshot", s(8) + 0.4, 2.0, -34.0, "fout=0.6"),
        ("dawnwind", "wind_desert_bleak", "loop", s(8), e(8) - s(8), -43.0, 'filt="lowpass=f=3400", fin=1.0, fout=1.0'),
        ("radiance", "dawn_morning_warm", "loop", s(9), e(9) - s(9), -40.0, 'filt="lowpass=f=3400", fin=2.0, fout=1.5'),
        ("hush", "air_hollow_desolate", "loop", s(10), e(10) - s(10), -42.0, 'filt="lowpass=f=2800", fin=1.5, fout=2.0'),
        ("dawn1", "dawn_morning_warm", "loop", s(15), e(15) - s(15), -39.0, 'filt="lowpass=f=3400", fin=2.5, fout=1.5'),
        ("dawn2", "dawn_morning_warm", "loop", s(16), total - s(16), -36.0, 'filt="lowpass=f=3400", fin=2.0'),
        ("riser", "rumble_deep_sub", "loop", s(9) - 2.0, 2.0, -29.0, 'filt="lowpass=f=1600", fin=1.9, fout=0.15'),
    ]
    rows = "\n".join(f'    layer("{a}", "{b}", "{c}", {d:.2f}, {g:.2f}, {h}, {k}),' for a, b, c, d, g, h, k in layers)
    bs = "\\"
    sfx = (f'"""Ambient/SFX bed for Women as First Witnesses v6 TRIM + RESYNC (2026-11-20). GENERATED by\n'
           f'batches/cluster_02_resurrection/women_first_witnesses_luke245/trim_v6/build_v6.py from the v5 beds\n'
           f'(build_women_witnesses_sfx.py, kept unchanged), re-anchored to the re-timed beats. The v5 stone-roll\n'
           f'one-shot is dropped with its beat (\'The promise had been kept\')."""\n'
           "import sys\nfrom pathlib import Path\nHERE = Path(__file__).resolve().parent\nsys.path.insert(0, str(HERE))\n"
           "import sfxlib\nfrom sfxlib import layer\n\n"
           f'CUT = Path(r"{P / "visual" / "women_first_witnesses_luke245_scored.mp4"}")\n'
           'OUT = CUT.with_name("women_first_witnesses_luke245_sfx.mp4")\n\nLAYERS = [\n' + rows + "\n]\n\n"
           'if __name__ == "__main__":\n    sfxlib.show_plan("Women as First Witnesses v6", LAYERS)\n'
           '    sfxlib.build(CUT, OUT, LAYERS)\n    print(f"[ok] {OUT}")\n    sfxlib.measure(OUT)\n')
    (ROOT / "sfx_pilots" / "build_women_witnesses_sfx_v6.py").write_text(sfx, encoding="utf-8")
    for b in beats:
        print(f'{b["t"][0]:6.2f}-{b["t"][1]:6.2f}  {b["cap"]["text"][:60]}')
    print(f"prep done: total {total} s, {len(beats)} beats")


def build():
    subprocess.run([PY, str(ROOT / "longform/02_Psalm_22_Song_From_The_Cross/build_livingpage_16x9.py"), "--pool", str(P / "visual"),
                    "--spec", "livingpage_short.spec.json", "--clips", "--page", "1080x1920", "--no-ticks"], check=True, cwd=ROOT)


def score():
    subprocess.run([PY, "run_piece.py", str(P), "--stage", "score"], check=True, cwd=ROOT)


def sfx():
    subprocess.run([PY, str(ROOT / "sfx_pilots" / "build_women_witnesses_sfx_v6.py")], check=True, cwd=ROOT)


def final():
    # guardrail fix (3 of 4 seats): decode the archaic KJV phrase, same card recipe as the shipped v5 decode cards
    al = json.load(open(P / "audio" / "alignment.json", encoding="utf-8"))
    t0 = next(w["start"] for w in al if w["w"].startswith("idle")) - 0.3
    font = "C\\:/Windows/Fonts/impact.ttf"
    vf = ",".join(f"drawtext=fontfile='{font}':text='{txt}':fontsize={sz}:fontcolor={col}:box=1:boxcolor=black@0.64:"
                  f"boxborderw=20:x=(w-text_w)/2:y={y}:enable='between(t,{t0:.2f},{t0 + 2.2:.2f})'"
                  for txt, sz, col, y in (("IDLE TALES", 110, "white", 170), ("= NONSENSE", 120, "0xF2C14E", 320)))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P / "visual" / "women_first_witnesses_luke245_sfx.mp4"), "-vf", vf,
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy",
                    "-movflags", "+faststart", str(FINAL)], check=True)
    print("FINAL ->", FINAL, dur(FINAL))


if __name__ == "__main__":
    st = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name in (["prep", "build", "score", "sfx", "final"] if st == "all" else [st]):
        globals()[name]()
