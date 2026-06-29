"""Build ref_library/index.html — the central reference-card catalogue gallery,
grouped by kind (characters / objects / places). Each card shows its anchor image,
canonical description and tags. Also copies to a clean Desktop folder for one-click
review. Reads catalogue.json. POC tooling; catalogue is permanent."""
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LIB = ROOT / "ref_library"
DEST = Path.home() / "Desktop" / "REF_library"
(DEST / "img").mkdir(parents=True, exist_ok=True)

cat = json.loads((LIB / "catalogue.json").read_text(encoding="utf-8"))
ORDER = {"character": 0, "object": 1, "place": 2}
cat.sort(key=lambda c: (ORDER.get(c["kind"], 9), c["name"]))

groups = {}
for c in cat:
    src = LIB / c["anchor"]
    flat = c["anchor"].replace("/", "__")
    if src.exists():
        shutil.copy2(src, DEST / "img" / flat)
    tags = "".join(f"<span class=tag>{t}</span>" for t in c.get("tags", []))
    badge = "REGISTERED" if c["name"] == "JESUS" else "NEW"
    card = (f'<div class=card><a href="img/{flat}" target="_blank">'
            f'<img src="img/{flat}"><div class=vk>{c["name"]}</div>'
            f'<div class=badge>{badge}</div></a>'
            f'<div class=desc>{c["canonical"]}</div><div class=tags>{tags}</div></div>')
    groups.setdefault(c["kind"], []).append(card)

LABELS = {"character": "Characters (face / body identity lock)",
          "object": "Objects (shape lock)", "place": "Places (world / palette lock)"}
sections = ""
for kind in ("character", "object", "place"):
    if kind in groups:
        sections += (f'<h2>{LABELS[kind]}</h2><div class=grid>'
                     + "".join(groups[kind]) + "</div>")

html = f"""<!doctype html><meta charset=utf-8><title>Awakeden reference-card catalogue</title>
<style>
body{{background:#0e0e10;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:28px;max-width:1500px}}
h1{{margin:0 0 6px}} .sub{{color:#9ab;margin:0 0 26px;max-width:1050px;line-height:1.5}}
h2{{color:#ffd98a;font-size:20px;margin:30px 0 12px;border-top:1px solid #2a2a30;padding-top:18px}}
.grid{{display:flex;gap:18px;flex-wrap:wrap}}
.card{{width:300px}} .card a{{position:relative;display:block}}
.card img{{width:300px;border-radius:8px;border:1px solid #333;display:block;background:#000}}
.vk{{position:absolute;left:8px;top:8px;background:#000b;color:#fff;font-size:13px;
     font-weight:700;padding:3px 10px;border-radius:9px}}
.badge{{position:absolute;right:8px;top:8px;background:#2a6;color:#001;font-size:11px;
     font-weight:700;padding:2px 8px;border-radius:9px}}
.desc{{color:#bcd;font-size:12.5px;line-height:1.4;margin:8px 0 6px}}
.tags{{display:flex;gap:5px;flex-wrap:wrap}}
.tag{{background:#1c1c22;color:#9ab;font-size:11px;padding:1px 8px;border-radius:8px}}
</style>
<h1>Awakeden &mdash; central reference-card catalogue</h1>
<p class=sub>The reusable identity bank (<code>ref_library/</code>). Each card is a locked
<b>inked anchor</b> + canonical description; pass the anchor as <code>--image</code> on any future
scene so the same face / object / world is inherited, never re-invented &mdash; across all long AND
short form. <b>Click any card for full resolution.</b></p>
{sections}
"""
out = DEST / "REF_library.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
