"""ELEVATE bake-off 2 ($0): Thirty Pieces of Silver (Zech 11:12-13). Same audio in every arm (shipped film mix).
  .venv\\Scripts\\python.exe poc_comic_page/_ELEVATE/build_tz.py <arm>      arm in R0 B0 W3
R0 = shipped film (copy). B0 = one shot per line, opaque grey pills (old style).
W3 = fast cuts + Mockers-style translucent pills with speaker tab + verse chip + hook card (owner direction 2026-11-09)."""
import json, sys, re, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_tp as T
import build_w3 as W
HERE = T.HERE; ROOT = T.ROOT
EP = ROOT / "batches/cluster_01_cross/thirty_pieces_zech11"
T.CL = EP / "visual/clips"; T.FILM = EP / "visual/thirty_pieces_zech11_sfx.mp4"; T.TOTAL = 59.07; T.FADE = 0.04

# narration line index -> clip (story order)
CLIP = {0: "thirty_coins_scatter", 1: "thirty_coins_scatter", 2: "judas_bag_priests", 3: "judas_bag_priests", 4: "thirty_coins_scatter",
        5: "potter_at_wheel", 6: "potter_at_wheel", 7: "judas_bag_priests", 8: "judas_casting_coins", 9: "potters_field",
        10: "potters_field", 11: "nail_through_hand", 12: "blood_water_wood"}
CLIP_LATE = {"Receive": "risen_mercy_hand", "Stop": "face_on_cross"}      # last line: switch clip on these words
SCRIPT_TAG = {2: ("ZECHARIAH", "ZECH 11:12"), 4: ("ZECHARIAH", "ZECH 11:13"), 6: ("ZECHARIAH", "ZECH 11:13"), 8: ("JUDAS", "MATT 27:5")}
VIEWS = [(.5, .5, 1.0, 1.12), (.5, .38, 1.7, 1.9), (.35, .5, 1.6, 1.8), (.65, .5, 1.6, 1.8), (.5, .62, 1.3, 1.5)]


def lines_and_chunks():
    raw = [l for l in (EP / "narration.md").read_text(encoding="utf-8").splitlines() if re.match(r"\[(narrator|scripture)\]", l)]
    al = json.load(open(EP / "audio/alignment.json", encoding="utf-8")); k = 0; chunks = []
    for li, l in enumerate(raw):
        spk = "scripture" if l.startswith("[scripture]") else "narrator"; toks = l.split("] ", 1)[1].split()
        ws = al[k:k + len(toks)]; k += len(toks); assert len(ws) == len(toks), (li, len(ws), len(toks))
        cur = []
        for tok, w in zip(toks, ws):
            cur.append((tok, w["start"], w["end"]))
            if (re.search(r"[.?!:]$", tok) and len(cur) >= 3) or len(cur) >= 10: chunks.append(dict(li=li, spk=spk, toks=cur)); cur = []
        if cur:
            if chunks and chunks[-1]["li"] == li and len(cur) < 3: chunks[-1]["toks"] += cur
            else: chunks.append(dict(li=li, spk=spk, toks=cur))
    assert k == len(al), (k, len(al))
    for i, c in enumerate(chunks):
        c["t0"] = 0.0 if i == 0 else max(0.0, c["toks"][0][1] - 0.05); c["text"] = " ".join(t[0] for t in c["toks"])
    for i, c in enumerate(chunks): c["t1"] = chunks[i + 1]["t0"] if i + 1 < len(chunks) else T.TOTAL
    return chunks


def clip_for(c):
    if c["li"] == 12:
        for t in c["toks"]:
            for w, cl in CLIP_LATE.items():
                if t[0].startswith(w): return cl
    return CLIP[c["li"]]


def main(arm):
    if arm == "R0": (HERE / "arms").mkdir(exist_ok=True); shutil.copy(T.FILM, HERE / "arms" / "TP_TZ_R0.mp4"); print("R0 copied"); return
    ch = lines_and_chunks(); d = HERE / "work" / ("tz_%s_lett" % arm); d.mkdir(parents=True, exist_ok=True); shots = []; ov = []
    if arm == "B0":
        i = 0
        while i < len(ch):                                   # one shot per narration line
            j = i
            while j + 1 < len(ch) and ch[j + 1]["li"] == ch[i]["li"]: j += 1
            clip = clip_for(ch[i]); shots.append(dict(t0=ch[i]["t0"], t1=ch[j]["t1"], clip=clip, t_in=0.0, cx=.5, cy=.5, z0=1.0, z1=1.12)); i = j + 1
        for n, c in enumerate(ch):
            tag = SCRIPT_TAG.get(c["li"]); first = n == 0 or ch[n - 1]["li"] != c["li"]
            p = d / ("p%02d.png" % n); T.pill(p, c["text"], tag[1] if (tag and first) else None, "narrator"); ov.append((str(p), c["t0"], c["t1"]))
        T.compose("TZ_B0", shots, ov); return
    for n, c in enumerate(ch):                               # W3: one shot per chunk, varied views
        cx, cy, z0, z1 = VIEWS[n % len(VIEWS)]; shots.append(dict(t0=c["t0"], t1=c["t1"], clip=clip_for(c), t_in=(n % 3) * 1.5, cx=cx, cy=cy, z0=z0, z1=z1))
        tag = SCRIPT_TAG.get(c["li"]); first = n == 0 or ch[n - 1]["li"] != c["li"]
        p = d / ("p%02d.png" % n)
        if tag: W.pill_tabs(p, c["text"], tag[0] if first else None, tag[1] if first else None, jesus=False)
        else: W.pill_tabs(p, c["text"])
        ov.append((str(p), c["t0"], c["t1"]))
    h = d / "hook.png"; T.light_text(h, "500 YEARS EARLY", 520, size=150, maxw=900); ov.append((str(h), 0.0, 2.0))
    T.compose("TZ_W3", shots, ov)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "plan":
        for c in lines_and_chunks(): print(c["li"], c["spk"][:3], "%.2f-%.2f" % (c["t0"], c["t1"]), c["text"])
    else: main(sys.argv[1])
