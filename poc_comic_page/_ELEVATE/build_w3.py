"""ELEVATE bake-off 1, $0: arm W3 = W2 cuts, full-bleed (no splits), MOCKERS-style lettering
(rounded pill + speaker tab + gold verse chip, Kalam). Owner direction 2026-11-09. Same audio as every arm.
  .venv\\Scripts\\python.exe poc_comic_page/_ELEVATE/build_w3.py"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_tp as T
import build_arms as BA

T.FADE = 0.04
HERE = T.HERE
WHO = {"mocker": "A MOCKER", "thief": "THE THIEF", "jesus": "JESUS"}
PICK = {5.2: 1, 6.8: 1, 34.9: 1}          # which half of a split to keep (default top)


def pill_tabs(path, text, who=None, ref=None, jesus=False):
    img = T.canvas(); d = ImageDraw.Draw(img); f = BA.KAL(54); lines = BA.wrap(d, text.split(), f, 820)[:3]
    h = 60 + 62 * len(lines); y0 = 1000
    fill = ((250, 240, 214) if jesus else T.GREY) + (150,)
    d.rounded_rectangle((70, y0, 1010, y0 + h), 46, fill=fill, outline=T.INK + (170,), width=4)
    y = y0 + 28
    for ln in lines:
        t = " ".join(ln); d.text((540 - d.textlength(t, font=f) / 2, y), t, font=f, fill=T.INK); y += 62
    tf = BA.KAL(28)
    for label, x_left in ((who, True), (ref, False)):
        if not label: continue
        tw = d.textlength(label, font=tf); x = 90 if x_left else 990 - tw - 36
        d.rounded_rectangle((x, y0 - 26, x + tw + 36, y0 + 22), 16, fill=T.GOLD, outline=T.INK, width=3); d.text((x + 18, y0 - 24), label, font=tf, fill=T.INK)
    img.save(path)


def main():
    r = json.load(open(HERE / "tp" / "W2_recipe.json", encoding="utf-8"))
    shots = []
    for s in r["shots"]:
        if "split" in s:
            p = dict(s["split"][PICK.get(s["t0"], 0)]); p["z0"] = min(p["z0"], 1.5); p["z1"] = min(p["z1"], 1.6)
            s = dict(t0=s["t0"], t1=s["t1"], **p)
        shots.append(s)
    refs = [o for o in r["overlays"] if o["kind"] == "ref"]
    ref_at = lambda t: next((o["text"] for o in refs if o["t0"] - 0.01 <= t < o["t1"]), None)
    d = HERE / "work" / "tp_W3_lett"; d.mkdir(parents=True, exist_ok=True); ov = []; first = {}
    for i, o in enumerate(r["overlays"]):
        k = o["kind"]; p = d / ("o%02d.png" % i)
        if k in ("ref", "stamp") or o["text"] == "Paradise.": continue
        if o["text"].lower().startswith("too late"):
            T.light_text(p, "TOO LATE FOR GOD?", 520, size=150, maxw=900)
        elif k == "light" and o["speaker"] == "jesus" and o["t0"] < 38.4 and o["text"].startswith("Verily"):
            pill_tabs(p, o["text"], "JESUS", ref_at(o["t0"]), jesus=True); g = d / "gloss.png"; T.light_text(g, "VERILY = TRULY", 230, size=80, maxw=900); ov.append((str(g), o["t0"], o["t1"]))
        elif k in ("jag", "round", "light"):
            spk = o["speaker"]; ref = ref_at(o["t0"]); key = (ref, spk)
            tag = WHO.get(spk) if key not in first or first[key] > o["t0"] - 0.01 else None
            first.setdefault(key, o["t0"])
            pill_tabs(p, o["text"], tag, ref if tag else None, jesus=(spk == "jesus"))
        else:  # narrator caption
            pill_tabs(p, o["text"])
        ov.append((str(p), o["t0"], o["t1"]))
    T.compose("W3", shots, ov)


if __name__ == "__main__":
    main()
