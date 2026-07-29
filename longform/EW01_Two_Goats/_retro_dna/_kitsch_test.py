"""Build a self-contained, share-able 'premium vs cringe' style test (2026-07-23).
Neutral A/B/C (viewers don't see which is which). Answers the ONE open question the
red-team said to test for $0: does the retro look read premium or cringe/tract?
Images embedded as data URIs -> one portable HTML the user can send to cold viewers.

  A = current inked look   B = restrained retro   C = loud (holy-card) retro
  (mapping kept OFF the page; told to the user in chat)

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_kitsch_test.py
"""
import base64, io, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent.parent
INK = ROOT / "longform" / "EW01_Two_Goats" / "v1" / "visual_16x9_inked"
FIN = Path(__file__).resolve().parent / "_true_retro_finished"
PRV = Path(__file__).resolve().parent / "_prove_it"
OUT = Path(__file__).resolve().parent / "_KITSCH_TEST.html"

# rows of (A inked, B restrained-retro, C loud-retro) — matched subject (Christ)
ROWS = [
    ("Christ — welcoming", INK / "25_will_you_come_in_be_carried_clean.png",
     FIN / "welcome_finished.png", PRV / "christ_welcome_finished.png"),
    ("Christ — standing", INK / "17_by_his_own_blood_he_entered_in_once.png",
     FIN / "jesus_finished.png", PRV / "christ_hero_finished.png"),
]


def datauri(p: Path, w=860) -> str:
    im = Image.open(p).convert("RGB")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    cells = []
    for label, a, b, c in ROWS:
        missing = [p for p in (a, b, c) if not p.exists()]
        if missing:
            print("MISSING:", *[str(m) for m in missing]); sys.exit(1)
        row = "".join(
            f"<figure><div class='tag'>{letter}</div><img src='{datauri(p)}'></figure>"
            for letter, p in (("A", a), ("B", b), ("C", c)))
        cells.append(f"<div class='rowlabel'>{label}</div><div class='grid'>{row}</div>")
    html = f"""<!doctype html><meta charset=utf-8>
<meta name=viewport content="width=device-width, initial-scale=1">
<title>Quick art pick — 30 seconds</title>
<style>
 body{{margin:0;background:#faf7f0;color:#20242c;font-family:system-ui,-apple-system,Arial;line-height:1.5}}
 .wrap{{max-width:1000px;margin:0 auto;padding:24px 18px 70px}}
 h1{{font-size:24px;margin:0 0 6px}} .lead{{color:#5a616e;margin:0 0 18px;font-size:16px}}
 .rowlabel{{font-weight:700;color:#7a818e;font-size:13px;text-transform:uppercase;letter-spacing:1px;margin:22px 0 8px}}
 .grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}}
 @media(max-width:720px){{.grid{{grid-template-columns:1fr}}}}
 figure{{margin:0;position:relative}}
 img{{width:100%;border-radius:8px;display:block;box-shadow:0 3px 14px rgba(0,0,0,.18)}}
 .tag{{position:absolute;top:8px;left:8px;background:#111;color:#fff;font-weight:800;font-size:15px;
   width:30px;height:30px;border-radius:6px;display:flex;align-items:center;justify-content:center}}
 .q{{background:#fff;border:1px solid #e6e0d4;border-radius:12px;padding:18px 20px;margin:26px 0 0;box-shadow:0 3px 14px rgba(0,0,0,.06)}}
 .q h2{{font-size:18px;margin:0 0 12px}} ol{{margin:0;padding-left:20px}} li{{margin:10px 0;font-size:16px}}
 .pick{{color:#8a6d1a;font-weight:700}}
</style>
<div class="wrap">
<h1>Help me pick an art style 🎨 (30 seconds, no wrong answers)</h1>
<p class="lead">Same picture, three styles — <b>A</b>, <b>B</b>, <b>C</b>. Just go with your gut and reply with your three picks.</p>
{''.join(cells)}
<div class="q">
  <h2>Reply with these 3:</h2>
  <ol>
    <li>Which looks the most <b>premium / professional</b>? <span class="pick">A / B / C</span></li>
    <li>Does any look <b>cheap, cheesy, or like a religious tract</b>? Which? <span class="pick">A / B / C / none</span></li>
    <li>Which would most make you <b>stop scrolling</b>? <span class="pick">A / B / C</span></li>
  </ol>
  <p style="color:#5a616e;margin:6px 0 0">e.g. &ldquo;1: B &nbsp; 2: C &nbsp; 3: B&rdquo; — thank you! 🙏</p>
</div>
</div>"""
    OUT.write_text(html, encoding="utf-8")
    kb = len(html.encode()) // 1024
    print(f"[ok] {OUT}  ({kb} KB, self-contained)")
    print(f"file:///{str(OUT).replace(chr(92), '/')}")


if __name__ == "__main__":
    main()
