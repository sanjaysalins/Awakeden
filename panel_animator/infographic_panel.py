#!/usr/bin/env python
"""Infographic Animator panel — a genuine comic DIPTYCH from two real stills.

Two of your already-rendered stills, full-bleed, divided by a torn hand-inked
gutter (not a rounded card border), joined by a hand-drawn brush-stroke arrow.
Captions sit on the same torn parchment caption band as the typography panel
(one consistent in-world caption language across both panel types). Punchy
scale-bounce reveals + impact-glow flash at each landing beat (panel lands,
arrow strikes, second panel lands).

$0, deterministic: Playwright drives real Chromium CSS animations frame-exact,
then ffmpeg encodes. No Higgsfield spend, no login.

IMPORTANT: this is for a DIAGRAM/RELATIONSHIP between two real stills — it
never asks an image model to paint the diagram or any lettering into a still.
(Tested: image models reliably invent garbled fake text even when explicitly
told not to — see panel_animator/README.md "purpose-built still, rejected".)

Two aspects: "16:9" (1920x1080) splits the diptych LEFT/RIGHT with a vertical
tear and a rightward arrow. "9:16" (1080x1920, native shorts vertical) stacks
it TOP/BOTTOM with a horizontal tear and a downward arrow — a real second
layout, not a crop (a 9:16 crop of the 16:9 diptych would show only one still).

Usage:
    python infographic_panel.py --spec spec.json --out panel.mp4 [--aspect 9:16]

spec.json:
{
  "left":  {"still": "C:/.../01_snakebite.png", "label": "FIERY SERPENTS SENT",
            "ref": "Numbers 21:6"},
  "right": {"still": "C:/.../04_venom.png",     "label": "THE VENOM ALREADY WITHIN",
            "ref": "the narration's own framing"}
}
("left"/"right" keys are reused as "first"/"second" panel in 9:16 -- first
stacks on top, second on the bottom.)
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from render_dom_clip import render as render_clip

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

# Torn-edge clip-path polygons. "v" tears run along a vertical seam (16:9,
# side-by-side); "h" tears run along a horizontal seam (9:16, stacked).
CLIP_V1 = ("polygon(0 0, 96% 0, 100% 4%, 97% 12%, 100% 22%, 96% 34%, 100% 46%, "
           "97% 58%, 100% 70%, 96% 82%, 100% 92%, 97% 100%, 0 100%)")
CLIP_V2 = ("polygon(4% 0, 100% 0, 100% 100%, 3% 100%, 6% 92%, 3% 82%, 7% 70%, "
           "4% 58%, 7% 46%, 3% 34%, 6% 22%, 3% 12%, 6% 4%)")
CLIP_H1 = ("polygon(0 0, 100% 0, 100% 96%, 96% 100%, 88% 97%, 78% 100%, 66% 96%, "
           "54% 100%, 42% 97%, 30% 100%, 18% 96%, 8% 100%, 0 97%)")
CLIP_H2 = ("polygon(0 4%, 8% 0, 18% 3%, 30% 0, 42% 4%, 54% 0, 66% 3%, 78% 0, "
           "88% 4%, 96% 0, 100% 3%, 100% 100%, 0 100%)")

LAYOUTS = {
    "16:9": dict(
        W=1920, H=1080, orient="v",
        p_w=940, p_h=1080, p2_off=980,           # panel size + panel2's left offset
        gutter=dict(top=0, left=930, w=60, h=1080),
        glow1=(470, 540), glow2=(1450, 540), glowA=(960, 568),
        arrow_box=(830, 498, 460, 140), arrow_rot=0,
        cap_w=820, cap1_pos=("left", 60), cap2_pos=("right", 60), cap_bottom=56,
    ),
    "9:16": dict(
        W=1080, H=1920, orient="h",
        p_w=1080, p_h=930, p2_off=990,
        gutter=dict(top=930, left=0, w=1080, h=60),
        glow1=(540, 465), glow2=(540, 1455), glowA=(540, 960),
        arrow_box=(440, 800, 200, 260), arrow_rot=90,
        cap_w=940, cap1_pos=("center", 0), cap2_pos=("center", 0),
        cap1_bottom=1046, cap2_bottom=390,
    ),
}


def _file_uri(p: str) -> str:
    return Path(p).resolve().as_uri()


def build_html(spec: dict, aspect: str = "16:9") -> str:
    L = LAYOUTS[aspect]
    left = spec.get("left") or spec.get("first")
    right = spec.get("right") or spec.get("second")
    left_uri, right_uri = _file_uri(left["still"]), _file_uri(right["still"])
    band_uri = _file_uri(str(ASSETS / "caption_band.png"))
    arrow_uri = _file_uri(str(ASSETS / "ink_arrow.png"))

    vertical = L["orient"] == "v"
    clip1, clip2 = (CLIP_V1, CLIP_V2) if vertical else (CLIP_H1, CLIP_H2)
    gx, gy, gw, gh = L["gutter"]["left"], L["gutter"]["top"], L["gutter"]["w"], L["gutter"]["h"]
    ax, ay, aw, ah = L["arrow_box"]
    g1x, g1y = L["glow1"]; g2x, g2y = L["glow2"]; gax, gay = L["glowA"]

    if vertical:
        panel1_pos = f"left:0; top:0; width:{L['p_w']}px; height:{L['p_h']}px;"
        panel2_pos = f"left:{L['p2_off']}px; top:0; width:{L['p_w']}px; height:{L['p_h']}px;"
        cap1_css = f"left:{L['cap1_pos'][1]}px; bottom:{L['cap_bottom']}px;"
        cap2_css = f"right:{L['cap2_pos'][1]}px; bottom:{L['cap_bottom']}px;"
    else:
        panel1_pos = f"left:0; top:0; width:{L['p_w']}px; height:{L['p_h']}px;"
        panel2_pos = f"left:0; top:{L['p2_off']}px; width:{L['p_w']}px; height:{L['p_h']}px;"
        cx = (L["W"] - L["cap_w"]) // 2
        cap1_css = f"left:{cx}px; bottom:{L['cap1_bottom']}px;"
        cap2_css = f"left:{cx}px; bottom:{L['cap2_bottom']}px;"

    arrow_transform = f"rotate({L['arrow_rot']}deg)" if L["arrow_rot"] else "none"

    return f"""<!doctype html>
<html><head><meta charset="utf-8">
<style>
  @font-face {{ font-family: "GeorgiaItalic"; src: url("file:///C:/Windows/Fonts/georgiai.ttf"); font-style: italic; }}
  @font-face {{ font-family: "GeorgiaBold"; src: url("file:///C:/Windows/Fonts/georgiab.ttf"); font-weight:700; }}

  html,body {{ margin:0; padding:0; width:{L['W']}px; height:{L['H']}px; overflow:hidden; background:#0b0805; }}

  .panel {{ position:absolute; background-size:cover; background-position:center;
            opacity:0; transform: scale(0.80); }}
  .panel1 {{ {panel1_pos} background-image:url("{left_uri}"); transform-origin: 50% 30%;
             clip-path: {clip1};
             animation: revealPunch 0.42s cubic-bezier(.2,1.7,.4,1) forwards; animation-delay:0.05s; }}
  .panel2 {{ {panel2_pos} background-image:url("{right_uri}"); transform-origin: 50% 70%;
             clip-path: {clip2};
             animation: revealPunch 0.42s cubic-bezier(.2,1.7,.4,1) forwards; animation-delay:0.95s; }}
  @keyframes revealPunch {{
    0%   {{ opacity:0; transform: scale(0.80); }}
    60%  {{ opacity:1; transform: scale(1.035); }}
    100% {{ opacity:1; transform: scale(1.0); }}
  }}

  .gutter-ink {{ position:absolute; top:{gy}px; left:{gx}px; width:{gw}px; height:{gh}px; background:#0b0805; z-index:2; }}

  .glow {{ position:absolute; width:640px; height:640px; margin-left:-320px; margin-top:-320px;
           border-radius:50%; z-index:1; opacity:0;
           background: radial-gradient(circle, rgba(196,150,62,0.55) 0%, rgba(196,150,62,0) 68%); }}
  @keyframes glowflash {{
    0%   {{ opacity:0;   transform:scale(0.55); }}
    30%  {{ opacity:0.95; transform:scale(1.0); }}
    100% {{ opacity:0;   transform:scale(1.35); }}
  }}
  .glow1 {{ left:{g1x}px; top:{g1y}px; animation: glowflash 0.55s ease-out forwards; animation-delay:0.05s; }}
  .glow2 {{ left:{g2x}px; top:{g2y}px; animation: glowflash 0.55s ease-out forwards; animation-delay:0.95s; }}
  .glowArrow {{ left:{gax}px; top:{gay}px; width:420px; height:420px; margin-left:-210px; margin-top:-210px;
                animation: glowflash 0.45s ease-out forwards; animation-delay:0.62s; }}

  .arrow-wrap {{ position:absolute; top:{ay}px; left:{ax}px; width:{aw}px; height:{ah}px; z-index:3;
                 display:flex; align-items:center; justify-content:center;
                 opacity:0; animation: arrowIn 0.32s cubic-bezier(.2,1.8,.4,1) forwards; animation-delay:0.55s; }}
  @keyframes arrowIn {{ 0% {{ opacity:0; }} 65% {{ opacity:1; }} 100% {{ opacity:1; }} }}
  .arrow-wrap img {{ width:460px; max-width:none; transform: {arrow_transform}; transform-origin:center;
                      filter: drop-shadow(0 0 10px rgba(196,150,62,0.5)) drop-shadow(0 4px 6px rgba(0,0,0,0.6)); }}

  .cap {{ position:absolute; z-index:3; width:{L['cap_w']}px; text-align:center;
          opacity:0; transform: translateY(26px) scale(0.9);
          animation: capPunch 0.4s cubic-bezier(.25,1.5,.4,1) forwards; }}
  @keyframes capPunch {{
    0%   {{ opacity:0; transform: translateY(26px) scale(0.9); }}
    60%  {{ opacity:1; transform: translateY(-4px) scale(1.03); }}
    100% {{ opacity:1; transform: translateY(0) scale(1.0); }}
  }}
  .cap1 {{ {cap1_css} animation-delay: 0.28s; }}
  .cap2 {{ {cap2_css} animation-delay: 1.18s; }}
  .cap-band {{ position:relative; }}
  .cap-band img {{ width:100%; height:170px; display:block; filter: drop-shadow(0 8px 14px rgba(0,0,0,0.5)); }}
  .cap-text {{ position:absolute; top:0; left:0; width:100%; height:170px;
               display:flex; flex-direction:column; align-items:center; justify-content:center; }}
  .cap-label {{ font-family:"GeorgiaBold", Georgia, serif; font-weight:700; font-size:32px; color:#2a1c10; }}
  .cap-ref   {{ font-family:"GeorgiaItalic", Georgia, serif; font-style:italic; font-size:22px; color:#5a3a20; margin-top:6px; }}
</style></head>
<body>
  <div class="glow glow1"></div>
  <div class="glow glowArrow"></div>
  <div class="glow glow2"></div>

  <div class="panel panel1"></div>
  <div class="panel panel2"></div>
  <div class="gutter-ink"></div>
  <div class="arrow-wrap"><img src="{arrow_uri}"></div>

  <div class="cap cap1">
    <div class="cap-band">
      <img src="{band_uri}">
      <div class="cap-text">
        <div class="cap-label">{left['label']}</div>
        <div class="cap-ref">{left.get('ref', '')}</div>
      </div>
    </div>
  </div>
  <div class="cap cap2">
    <div class="cap-band">
      <img src="{band_uri}">
      <div class="cap-text">
        <div class="cap-label">{right['label']}</div>
        <div class="cap-ref">{right.get('ref', '')}</div>
      </div>
    </div>
  </div>
</body></html>
"""


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--aspect", choices=["16:9", "9:16"], default="16:9")
    ap.add_argument("--duration", type=float, default=2.4)
    a = ap.parse_args(argv)

    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    html = build_html(spec, aspect=a.aspect)
    L = LAYOUTS[a.aspect]

    tmp_html = Path(a.out).with_suffix(".build.html")
    tmp_html.write_text(html, encoding="utf-8")
    render_clip(tmp_html, Path(a.out), a.duration, has_counter=False, width=L["W"], height=L["H"])
    tmp_html.unlink()
    print(f"wrote {Path(a.out).resolve()}")


if __name__ == "__main__":
    raise SystemExit(main())
