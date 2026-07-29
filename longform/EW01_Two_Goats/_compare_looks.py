"""Side-by-side: OLD inked look vs NEW painted-comic look, same scenes (2026-07-23).
Helps the user decide if the painted re-render is worth it, or if inked was fine.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_compare_looks.py
"""
import glob
from pathlib import Path

HERE = Path(__file__).resolve().parent
INKED = HERE / "v1" / "visual_16x9_inked"
PAINTED = HERE / "v1" / "visual_16x9_painted"
OUT = HERE / "v1" / "_LOOK_COMPARE.html"

# scenes that have a CLEAN painted version to compare
SCENES = [(1, "Once a year, only once"), (3, "Plain white linen"),
          (4, "I went in alone"), (5, "The cloud on the mercy seat"),
          (17, "By his own blood he entered in once")]


def find(d, sid):
    m = sorted(glob.glob(str(d / f"{sid:02d}_*.png")))
    return Path(m[0]).resolve().as_uri() if m else ""


def main():
    rows = []
    for sid, title in SCENES:
        old = find(INKED, sid)
        new = find(PAINTED, sid)
        rows.append(f"""
        <div class='row'>
          <div class='ti'>#{sid:02d} · {title}</div>
          <div class='pair'>
            <figure><figcaption>OLD — inked</figcaption><img src='{old}'></figure>
            <figure><figcaption>NEW — painted-comic</figcaption><img src='{new}'></figure>
          </div>
        </div>""")
    html = f"""<!doctype html><meta charset=utf-8>
<title>EW01 — look compare: inked vs painted</title>
<style>
 body{{background:#14110d;color:#f0e9dc;font-family:system-ui,Arial;margin:0;padding:26px}}
 h1{{font-size:22px;margin:0 0 4px}} p.sub{{color:#b7ab97;margin:0 0 24px;max-width:820px}}
 .row{{margin:0 0 34px}} .ti{{font-size:17px;color:#e9c877;font-weight:700;margin:0 0 8px}}
 .pair{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
 figure{{margin:0}} figcaption{{font-size:13px;color:#b7ab97;margin:0 0 5px;text-transform:uppercase;letter-spacing:1px}}
 img{{width:100%;border-radius:7px;display:block;box-shadow:0 5px 20px rgba(0,0,0,.5)}}
 @media(max-width:900px){{.pair{{grid-template-columns:1fr}}}}
</style>
<h1>EW01 · same scenes — OLD inked (left) vs NEW painted-comic (right)</h1>
<p class='sub'>Look at them side by side. Is the painted version clearly better, or was the inked look already good enough? Remember: the motion problem is fixed either way by the new engine — this is only about the still look.</p>
{''.join(rows)}
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"file:///{str(OUT).replace(chr(92), '/')}")


if __name__ == "__main__":
    main()
