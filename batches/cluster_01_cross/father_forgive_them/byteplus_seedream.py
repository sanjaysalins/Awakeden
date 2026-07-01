#!/usr/bin/env python
"""Direct BytePlus ModelArk -> Seedream image test (bypasses the Higgsfield CLI).

Lets us test the EXACT problem prompts against Seedream over a real API, WITH an optional
reference image (`--ref`) — the ref-lock lever the hf.exe path can't give us. Uses BYTEPLUS_API_KEY
(an `ark-...` ModelArk key). Saves PNGs to visual/_byteplus/.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --which 1
  ...  --which 1 --ref <path-or-url-to-christ-face.png>     # test WITH reference lock
  ...  --prompt "..." --name my_test                         # arbitrary prompt

Env overrides if defaults are wrong: BYTEPLUS_BASE_URL, BYTEPLUS_IMG_MODEL.
"""
import argparse, base64, json, os, re, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
OUT = HERE / "visual" / "_byteplus"; OUT.mkdir(parents=True, exist_ok=True)


def _load_key() -> str:
    for envp in (ROOT / ".env", ROOT.parent / "PythonProject1" / ".env"):
        if envp.exists():
            m = re.search(r"^BYTEPLUS_API_KEY=(.*)$", envp.read_text(encoding="utf-8"), re.M)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    return os.getenv("BYTEPLUS_API_KEY", "")


BASE = os.getenv("BYTEPLUS_BASE_URL", "https://ark.ap-southeast.bytepluses.com/api/v3")
MODEL = os.getenv("BYTEPLUS_IMG_MODEL", "seedream-4-0-250828")

STYLE = (" Drawn in INKED BIBLICAL GRAPHIC-NOVEL / cinematic manga ILLUSTRATION style: bold clean "
         "black ink linework and outlines, flat cel-shaded comic colour, hand-drawn 2D artwork, "
         "dramatic ink shadows. NOT a photograph, NOT photorealistic, NOT a glossy 3D render, NOT "
         "soft airbrushed anime — strong visible ink lines. Reverent and holy atmosphere, ancient "
         "Near-Eastern period-accurate, mature teen-and-up tone. ABSOLUTELY NO text, letters, words, "
         "numbers, captions, labels, titles, inscriptions, speech bubbles, scrolls of legible writing, "
         "watermark or signature ANYWHERE in the image.")
ONE = (" ONE single uninterrupted full-bleed illustration filling the entire frame — absolutely NO "
       "split screen, NO side panel, NO inset, NO grid, NO border or divider of any kind.")

PROMPTS = {
    "1": ("pierced_hand",
        "A CLOSE shot of the crucified Christ's face and outstretched wounded hand (the SAME man "
        "throughout: a bearded man in his early thirties with a calm Near-Eastern face, a lean face "
        "with high cheekbones and a slightly aquiline nose, warm olive skin, deep brown eyes, a short "
        "dark full beard and long dark wavy hair parted in the middle): his head lifted, his near hand "
        "OPEN and flat, palm forward, reaching toward the viewer, showing a dark ragged pierced hole in "
        "the centre of the open palm with dark red blood running toward the wrist; his other arm rests "
        "along the wooden crossbeam, its hand also OPEN and flat with a matching pierced wound. A dark "
        "storm sky, one warm shaft of light across his face and the wounded open hand. Reverent, merciful."),
    "2": ("nailed_hands",
        "A stark close macro of BOTH of the crucified Christ's hands, OPEN and flat against the dark "
        "rough wooden crossbeam, palms facing the viewer, fingers relaxed and gently parted, a dark "
        "ragged pierced wound in the CENTRE of each open palm with dark red blood running down toward "
        "the wrists. Behind, a black storm sky. Reverent, visceral."),
}


def _ref_to_field(ref: str) -> str:
    if ref.startswith("http"):
        return ref
    data = Path(ref).read_bytes()
    return "data:image/png;base64," + base64.b64encode(data).decode()


def generate(prompt: str, name: str, size: str, ref: str | None):
    key = _load_key()
    if not key:
        raise SystemExit("no BYTEPLUS_API_KEY found")
    body = {"model": MODEL, "prompt": prompt + STYLE + ONE, "size": size,
            "response_format": "url", "watermark": False}
    if ref:
        body["image"] = _ref_to_field(ref)
        body["sequential_image_generation"] = "disabled"
    req = urllib.request.Request(
        f"{BASE}/images/generations", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    print(f"POST {BASE}/images/generations  model={MODEL} size={size} ref={'yes' if ref else 'no'}")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()[:600]}")
        return
    url = resp.get("data", [{}])[0].get("url")
    if not url:
        print("no url in response:", json.dumps(resp)[:600]); return
    dest = OUT / f"{name}.png"
    with urllib.request.urlopen(url, timeout=180) as im:
        dest.write_bytes(im.read())
    print(f"SAVED {dest}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--which", help="1 or 2 (built-in problem prompts)")
    ap.add_argument("--prompt", help="arbitrary prompt (raw; STYLE+ONE appended)")
    ap.add_argument("--name", default="test")
    ap.add_argument("--size", default="1440x2560", help="9:16 portrait; total px within [1280x720,4096x4096]")
    ap.add_argument("--ref", default=None, help="reference image path or URL (ref-lock test)")
    a = ap.parse_args()
    if a.which:
        name, prompt = PROMPTS[a.which]
        generate(prompt, name + ("_ref" if a.ref else ""), a.size, a.ref)
    elif a.prompt:
        generate(a.prompt, a.name, a.size, a.ref)
    else:
        ap.error("pass --which 1|2 or --prompt")


if __name__ == "__main__":
    main()
