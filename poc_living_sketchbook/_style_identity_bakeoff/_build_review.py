"""Build the side-by-side review gallery for the style x identity-lock
bake-off -- baseline + 35 variants, per character (Moses / Jesus), so the
human eye-gate (this project's standing rule -- never trust the render
pipeline without looking, feedback-verify-by-looking-not-running) has one
page to work from. Re-run any time; overwrites the HTML, never the PNGs.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_identity_bakeoff/_build_review.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _run_bakeoff import build_jobs, CHARACTERS  # noqa: E402

OUT_HTML = HERE / "_REVIEW.html"


def cards_for(char_key):
    cfg = CHARACTERS[char_key]
    stills_dir = HERE / cfg["out"]
    jobs = build_jobs()
    cards = []
    for slug, name, prefix, src in jobs:
        png = stills_dir / f"{slug}.png"
        if not png.exists():
            continue
        rel = f"{cfg['out']}/{slug}.png"
        cards.append((slug, name, src, rel))
    return cards


def render_section(char_key, title):
    cards = cards_for(char_key)
    if not cards:
        return f"<h2>{title}</h2><p class='empty'>No renders yet.</p>"
    baseline = [c for c in cards if c[0] == "baseline"]
    rest = [c for c in cards if c[0] != "baseline"]
    html = [f"<h2>{title} <span class='count'>({len(cards)}/36)</span></h2>"]
    html.append("<div class='grid'>")
    for slug, name, src, rel in baseline + rest:
        cls = "card baseline" if slug == "baseline" else "card"
        html.append(f"""
        <div class="{cls}">
          <a href="{rel}" target="_blank"><img src="{rel}" loading="lazy"></a>
          <div class="meta">
            <div class="name">{name}</div>
            <div class="slug">{slug} &middot; {src}</div>
          </div>
        </div>""")
    html.append("</div>")
    return "\n".join(html)


def main():
    body = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Style x Identity-Lock Bake-off</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Arial, sans-serif; background:#1a1712; color:#eee6d8; margin:0; padding:24px 32px 64px; }}
  h1 {{ font-size: 22px; margin-bottom:4px; }}
  .sub {{ color:#a99; margin-bottom:24px; font-size:14px; }}
  h2 {{ margin-top:40px; border-bottom:1px solid #444; padding-bottom:8px; }}
  .count {{ color:#998; font-weight:normal; font-size:15px; }}
  .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(200px,1fr)); gap:14px; margin-top:16px; }}
  .card {{ background:#242018; border-radius:8px; overflow:hidden; border:1px solid #3a352a; }}
  .card.baseline {{ border-color:#c9a04a; border-width:2px; }}
  .card img {{ width:100%; display:block; aspect-ratio: 9/16; object-fit:cover; }}
  .meta {{ padding:8px 10px; }}
  .name {{ font-size:13px; font-weight:600; }}
  .slug {{ font-size:11px; color:#998; margin-top:2px; }}
  .empty {{ color:#876; font-style:italic; }}
  .note {{ background:#2a2418; border-left:3px solid #c9a04a; padding:10px 14px; margin:16px 0; font-size:13px; color:#ccc; }}
</style></head><body>
<h1>Style x Identity-Lock Bake-off</h1>
<div class="sub">36 renders per character (1 baseline + 15 STYLE_VARIANTS.md + 20 STYLE_LAB.md), same control scene/pose, chained to the repo cast anchor. Judge on: (a) handmade/alive, (b) still reads as the SAME character as the baseline card (gold border).</div>
<div class="note">Click any image to open full-res -- never judge from the shrunk grid (feedback-audit-stills-fullres). Baseline card in each section is the plain frozen SKILL.md style, for comparison.</div>
{render_section("moses", "Moses")}
{render_section("jesus", "Jesus")}
</body></html>"""
    OUT_HTML.write_text(body, encoding="utf-8")
    print(f"[out] {OUT_HTML}")


if __name__ == "__main__":
    main()
