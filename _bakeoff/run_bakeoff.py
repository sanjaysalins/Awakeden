"""Animation engine bake-off: HF Kling pro  vs  direct-Kling.
SAME still, SAME byte-identical prompt, SAME 5s duration — only the engine differs.
Run with the PythonProject1 venv (has Kling creds + deps). METERED (~$5.06).

  C:\\Users\\sanjay\\PycharmProjects\\PythonProject1\\.venv\\Scripts\\python.exe _bakeoff\\run_bakeoff.py
"""
import os, re, sys, json, time, subprocess
from pathlib import Path

# MUST set before importing kling_video (reads DURATION_SEC at import time)
os.environ["KLING_DURATION"] = "5"

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_bakeoff"
PP1 = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1")
JESUS = PP1 / "jesus"
HF = Path.home() / "bin" / "hf.exe"
SHORT = ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/03_The_Forsaken_Cry/visual/nbp"
STILLS = ["01_the-cry", "04_the-ninth-hour"]

# creds + direct-Kling render path
from dotenv import load_dotenv
load_dotenv(PP1 / ".env")
sys.path.insert(0, str(JESUS))
import image_to_kling as itk          # noqa
from adhoc import trim_kling_prompt_if_needed  # noqa

AK = os.getenv("KLING_ACCESS_KEY"); SK = os.getenv("KLING_SECRET_KEY")
assert AK and SK, "KLING creds missing"


def make_5s_prompt(src_kling: Path):
    d = json.loads(src_kling.read_text(encoding="utf-8"))
    p = d["prompt"].replace("10.0s", "5.0s").replace("10s", "5s")
    # apply the SAME normalisation direct-Kling applies, so both engines get an identical string
    p = itk.ensure_tableau_sentence(trim_kling_prompt_if_needed(p))
    return p, d.get("negative_prompt") or ""


def hf_render(png: Path, prompt: str, out: Path):
    cmd = [str(HF), "generate", "create", "kling3_0", "--start-image", str(png),
           "--prompt", prompt, "--duration", "5", "--mode", "pro",
           "--sound", "off", "--aspect_ratio", "9:16", "--wait"]
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    blob = (r.stdout or "") + (r.stderr or "")
    m = re.search(r'https?://[^\s"]+\.mp4', blob)
    if not m:
        return None, time.time() - t, blob.strip()[-300:]
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
    return (out if out.exists() and out.stat().st_size > 0 else None), time.time() - t, "ok"


def direct_render(png: Path, prompt: str, neg: str, out: Path):
    kp = OUT / f"{png.stem}_direct.kling.json"
    kp.write_text(json.dumps({"prompt": prompt, "negative_prompt": neg}, ensure_ascii=False, indent=2),
                  encoding="utf-8")
    t = time.time()
    try:
        itk.render_kling_for_image(image_path=png, kling_path=kp, mp4_path=out,
                                   access_key=AK, secret_key=SK)
        return (out if out.exists() else None), time.time() - t, "ok"
    except Exception as e:
        return None, time.time() - t, f"{type(e).__name__}: {e}"[:300]


def main():
    OUT.mkdir(exist_ok=True)
    rows = []
    for stem in STILLS:
        png = SHORT / f"{stem}.png"
        prompt, neg = make_5s_prompt(SHORT / f"{stem}.kling.json")
        (OUT / f"{stem}.prompt.txt").write_text(prompt, encoding="utf-8")
        (OUT / f"{stem}.negative.txt").write_text(neg, encoding="utf-8")
        print(f"\n===== {stem} =====  (prompt {len(prompt)} chars, identical to both)")

        print(" [HF Kling pro] rendering...")
        hf_mp4, hf_t, hf_note = hf_render(png, prompt, OUT / f"{stem}_HF.mp4")
        print(f"   -> {'OK' if hf_mp4 else 'FAIL'} {hf_t:.0f}s  {hf_note}")

        print(" [direct-Kling] rendering...")
        dk_mp4, dk_t, dk_note = direct_render(png, prompt, neg, OUT / f"{stem}_DIRECT.mp4")
        print(f"   -> {'OK' if dk_mp4 else 'FAIL'} {dk_t:.0f}s  {dk_note}")

        rows.append(dict(stem=stem, png=str(png), prompt_chars=len(prompt),
                         hf=bool(hf_mp4), hf_sec=round(hf_t), hf_note=hf_note,
                         dk=bool(dk_mp4), dk_sec=round(dk_t), dk_note=dk_note))

    (OUT / "results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    # cost: HF pro 5s = 12.5cr*$0.15 = $1.88 ; direct-Kling = $0.65
    hf_n = sum(r["hf"] for r in rows); dk_n = sum(r["dk"] for r in rows)
    print(f"\n==== BAKE-OFF DONE ====")
    print(f"  HF Kling pro : {hf_n} ok  ~${hf_n*1.88:.2f}")
    print(f"  direct-Kling : {dk_n} ok  ~${dk_n*0.65:.2f}")
    print(f"  results -> {OUT/'results.json'}")


if __name__ == "__main__":
    main()
