#!/usr/bin/env python
"""BytePlus Seedream BAKE-OFF: 4.0 vs 4.5 vs 5.0-lite, on our problem prompts, no-ref vs ref-lock.

Matrix = 3 models x 3 problem prompts x {no-ref, ref-locked to JESUS__REF.png} = 18 renders (~$0.65).
9:16 at 1440x2560 (meets the 4.5/5.0 >=2K minimum). Idempotent (existing PNG skipped). Builds compare.html.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_bakeoff.py --test   # 1 ref render, validate image param
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_bakeoff.py           # full matrix
"""
import argparse, base64, json, re, urllib.request
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
OUT = HERE / "visual" / "_byteplus" / "bakeoff"; OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
SIZE = "1440x2560"
REF_SRC = ROOT / "longform" / "_style_poc" / "jesus" / "JESUS__REF.png"

MODELS = {"4_0": "seedream-4-0-250828", "4_5": "seedream-4-5-251128", "5_0lite": "seedream-5-0-260128"}

STYLE = (" Drawn in INKED BIBLICAL GRAPHIC-NOVEL / cinematic manga ILLUSTRATION style: bold clean "
         "black ink linework and outlines, flat cel-shaded comic colour, hand-drawn 2D artwork, "
         "dramatic ink shadows. NOT a photograph, NOT photorealistic, NOT a glossy 3D render, NOT "
         "soft airbrushed anime — strong visible ink lines. Reverent and holy atmosphere, ancient "
         "Near-Eastern period-accurate, mature teen-and-up tone. ABSOLUTELY NO text, letters, words, "
         "numbers, captions, labels, titles, inscriptions, speech bubbles, watermark or signature.")
ONE = (" ONE single uninterrupted full-bleed illustration filling the entire frame — absolutely NO "
       "split screen, NO side panel, NO inset, NO grid, NO border or divider of any kind.")

PROMPTS = {
 "pierced_hand": ("A CLOSE shot of the crucified Christ's face and outstretched wounded hand: his head "
   "lifted, his near hand OPEN and flat, palm forward, reaching toward the viewer, showing a dark ragged "
   "pierced hole in the centre of the open palm with dark red blood running toward the wrist; his other "
   "arm rests along the wooden crossbeam, its hand also OPEN and flat with a matching pierced wound. A "
   "dark storm sky, one warm shaft of light across his face and the wounded open hand. Reverent, merciful."),
 "nailed_hands": ("A stark close macro of BOTH of the crucified Christ's hands, OPEN and flat against the "
   "dark rough wooden crossbeam, palms facing the viewer, fingers relaxed and gently parted, a dark ragged "
   "pierced wound in the CENTRE of each open palm with dark red blood running down toward the wrists. "
   "Behind, a black storm sky. Reverent, visceral."),
 "jesus_prays": ("The crucified Christ on a wooden cross, his body hanging with EXACTLY TWO arms — one arm "
   "stretched straight out to each side ALONG the horizontal crossbeam, both hands OPEN and flat against "
   "the beam, palms forward, a dark pierced wound in the centre of each open palm. His head lifted and "
   "tilted back toward heaven, his lips parting as he speaks a prayer. A warm shaft of light across his "
   "face. A dark storm sky; far below, small Roman soldiers gather his garment. Only two arms and two hands."),
}
# a lightweight character line only used in the NO-REF condition (ref condition carries identity via image)
CHRIST = (" The man is in his early thirties with a calm Near-Eastern face, warm olive skin, deep brown "
          "eyes, a short dark full beard and long dark wavy hair parted in the middle.")


def _key() -> str:
    for envp in (ROOT / ".env", ROOT.parent / "PythonProject1" / ".env"):
        if envp.exists():
            m = re.search(r"^BYTEPLUS_API_KEY=(.*)$", envp.read_text(encoding="utf-8"), re.M)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    return ""


def _ref_data_url() -> str:
    """Downscale the ref to a sane size and return a base64 data URL."""
    small = OUT / "_ref_small.png"
    if not small.exists():
        im = Image.open(REF_SRC).convert("RGB")
        im.thumbnail((1024, 1024), Image.LANCZOS)
        im.save(small)
    return "data:image/png;base64," + base64.b64encode(small.read_bytes()).decode()


def call(model_id: str, prompt: str, dest: Path, ref_url: str | None) -> str:
    if dest.exists() and dest.stat().st_size > 0:
        return "skip"
    body = {"model": model_id, "prompt": prompt, "size": SIZE, "response_format": "url", "watermark": False}
    if ref_url:
        body["image"] = ref_url                       # single reference image (identity lock)
        body["sequential_image_generation"] = "disabled"
    else:
        body["prompt"] = prompt + CHRIST
    body["prompt"] = body["prompt"] + STYLE + ONE
    req = urllib.request.Request(BASE, data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {_key()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()[:300]}"
    url = resp.get("data", [{}])[0].get("url")
    if not url:
        return "no-url: " + json.dumps(resp)[:300]
    with urllib.request.urlopen(url, timeout=240) as im:
        dest.write_bytes(im.read())
    return "ok"


def build_html():
    rows = []
    for pkey in PROMPTS:
        rows.append(f'<h2>{pkey}</h2><table><tr><th></th>' +
                    "".join(f"<th>Seedream {m.replace('_','.')}</th>" for m in MODELS) + "</tr>")
        for cond in ("noref", "ref"):
            cells = f"<td class=c>{'ref-locked' if cond=='ref' else 'no ref'}</td>"
            for m in MODELS:
                p = f"{m}__{pkey}__{cond}.png"
                cells += f'<td>{"<img src=\'"+p+"\'>" if (OUT/p).exists() else "-"}</td>'
            rows.append(f"<tr>{cells}</tr>")
        rows.append("</table>")
    html = ("<!doctype html><meta charset=utf-8><title>Seedream bake-off</title>"
            "<style>body{background:#14110d;color:#eee;font-family:Arial;padding:20px}"
            "h2{color:#e8c069;margin:26px 0 8px} table{border-collapse:collapse;margin-bottom:10px}"
            "td,th{border:1px solid #3a3226;padding:4px;vertical-align:top} img{width:230px;display:block}"
            ".c{color:#c9b892;font-size:13px;writing-mode:vertical-rl;text-align:center}</style>"
            "<h1>BytePlus Seedream bake-off — 4.0 vs 4.5 vs 5.0-lite · problem prompts · no-ref vs ref-lock</h1>"
            f"<p>Ref = JESUS__REF.png · 9:16 1440x2560</p>{''.join(rows)}")
    (OUT / "compare.html").write_text(html, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--test", action="store_true")
    a = ap.parse_args()
    ref = _ref_data_url()
    if a.test:
        dest = OUT / "4_0__pierced_hand__ref.png"
        print("validate ref param:", call(MODELS["4_0"], PROMPTS["pierced_hand"], dest, ref))
        return
    for m, mid in MODELS.items():
        for pkey, ptext in PROMPTS.items():
            for cond, rurl in (("noref", None), ("ref", ref)):
                dest = OUT / f"{m}__{pkey}__{cond}.png"
                print(f"{m:8} {pkey:13} {cond:6} -> {call(mid, ptext, dest, rurl)}", flush=True)
    build_html()
    print("HTML ->", OUT / "compare.html")


if __name__ == "__main__":
    main()
