"""Preview sheet — eyeball the WHOLE comic layout before spending on clips.
  python preview_episode.py [spec.json]
Renders each beat via the shared geometry (comic_engine.render_still_page) from the
STILL pngs (not the mp4s), then montages every beat into one page for review.
$0 / no render. Use this as the GATE before generating/animating art."""
import sys, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import comic_engine as ce

HERE = Path(__file__).parent
SPEC = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "ew04.spec.json"
spec = json.loads(SPEC.read_text(encoding="utf-8"))

EW = (HERE / spec["anim_dir"]).resolve().parent          # ../  (episode root)
STILLS = EW / "stills"
WORK = HERE / "_work"; WORK.mkdir(exist_ok=True)
OUT = HERE / f"{spec['episode']}_preview.png"


def still(slug):
    return str(STILLS / f"{slug}.png")


def norm(entry):
    """spec clip entry -> dict pointing at the STILL png (keeps bias/zoom/anchors)."""
    if isinstance(entry, dict):
        d = dict(entry); d["path"] = still(d.pop("slug")); return d
    slug, motion = entry
    return {"path": still(slug), "motion": motion}


pages = []
for i, b in enumerate(spec["beats"]):
    clips = [norm(e) for e in b["clips"]]
    p = WORK / f"_prev{i:02d}.png"
    ce.render_still_page(b["tpl"], clips, b.get("cap"), p)
    pages.append((i, b, p))

# montage: thumbnails in a row of N, with a caption strip under each
THUMB_W = 300
THUMB_H = round(THUMB_W * ce.PAGE_H / ce.PAGE_W)
COLS = 5
LABEL_H = 64
rows = (len(pages) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * THUMB_W + (COLS + 1) * 16,
                          rows * (THUMB_H + LABEL_H) + 16), (24, 22, 20))
d = ImageDraw.Draw(sheet)
font = ImageFont.truetype(ce.FONT, 22)
for n, (i, b, p) in enumerate(pages):
    r, c = divmod(n, COLS)
    x = 16 + c * (THUMB_W + 16)
    y = 16 + r * (THUMB_H + LABEL_H)
    thumb = Image.open(p).convert("RGB").resize((THUMB_W, THUMB_H), Image.LANCZOS)
    sheet.paste(thumb, (x, y))
    t0, t1 = b["t"]
    tags = "+".join(e["motion"] if isinstance(e, dict) else e[1] for e in b["clips"])
    d.text((x + 4, y + THUMB_H + 6), f"#{i} {b['tpl']}", font=font, fill=(245, 235, 210))
    d.text((x + 4, y + THUMB_H + 34), f"{t0:.0f}-{t1:.0f}s  {tags}", font=font, fill=(170, 165, 155))
sheet.save(OUT)
print("PREVIEW ->", OUT, flush=True)
