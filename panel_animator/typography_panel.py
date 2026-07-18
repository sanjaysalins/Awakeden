#!/usr/bin/env python
"""Typography Animator panel — in-world kinetic-type reveal over a real still.

A torn hand-inked parchment caption band sits directly on the still (no UI
box/card/drop-shadow chrome), words pop in with a punchy spring/back-out
bounce, the emphasis word gets a red "rubrication" ink accent (illuminated-
manuscript convention) instead of a highlight chip. An optional ticking-number
counter can precede the caption: digits scramble like a real stat reveal, then
either land on a VERIFIED number, or — if none exists — land honestly on a
drawn ink dash with a caption explaining why, on its own parchment band (never
bare text floating on the raw scene). Never fabricates a number.

$0, deterministic: Playwright drives real Chromium CSS animations frame-exact,
then ffmpeg encodes. No Higgsfield spend, no login.

Two aspects: "16:9" (1920x1080, long-form comic-grid slot) and "9:16"
(1080x1920, native shorts vertical) — pass --aspect 9:16 for shorts. Layout
constants (band size/position, word wrap width, font sizes, safe-zone bottom
margin) are aspect-specific, not a crop of the 16:9 render: the 9:16 layout
keeps captions clear of the bottom ~18% platform-UI band (SHORTS_SAFE_BOT).

Usage:
    python typography_panel.py --spec spec.json --out panel.mp4 [--aspect 9:16]

spec.json:
{
  "still": "C:/path/to/an/existing/rendered/still.png",
  "ref": "Numbers 21:6",                 // optional, small italic top-left
  "phrase": [
    {"text": "much", "accent": false},
    {"text": "people", "accent": false},
    {"text": "of", "accent": false},
    {"text": "israel", "accent": false},
    {"text": "died", "accent": true}      // accent = red rubrication ink
  ],
  "counter": {                            // optional — omit for no counter
    "value": null,                        // a VERIFIED integer, or null/omit
    "not_recorded_caption": "no number is recorded — Scripture says only \"much people\""
  }
}
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from render_dom_clip import render as render_clip

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

WORD_TPL = '<span class="word {cls}" style="animation-delay:{delay:.2f}s">{text}</span>'

# Aspect-specific layout constants. 9:16 is a real vertical layout, not a crop
# of the 16:9 render (a centre-crop would slice multi-word lines off both
# edges) -- narrower word-wrap so text stacks into more, shorter lines, and
# the caption band + counter sit above the platform-UI safe zone.
LAYOUTS = {
    "16:9": dict(
        W=1920, H=1080,
        ref_top=56, ref_left=74, ref_fs=30,
        band_left=10, band_bottom=60, band_w=1900, band_h=260,
        stage_bottom=120, stage_maxw=1740, gap=20, word_fs=88,
        counter_top=150, counter_fs=220, scrim_top=120, scrim_w=1000, scrim_h=340,
        cap_band_w=900, cap_band_h=100, cap_fs=28,
        glow_left=960, glow_top=330,
    ),
    "9:16": dict(
        W=1080, H=1920,
        ref_top=64, ref_left=46, ref_fs=26,
        band_left=20, band_bottom=400, band_w=1040, band_h=320,
        stage_bottom=460, stage_maxw=980, gap=16, word_fs=72,
        counter_top=260, counter_fs=160, scrim_top=190, scrim_w=940, scrim_h=420,
        cap_band_w=940, cap_band_h=120, cap_fs=26,
        glow_left=540, glow_top=420,
    ),
}


def _file_uri(p: str) -> str:
    return Path(p).resolve().as_uri()


def build_html(spec: dict, aspect: str = "16:9") -> tuple[str, bool]:
    L = LAYOUTS[aspect]
    still_uri = _file_uri(spec["still"])
    band_uri = _file_uri(str(ASSETS / "caption_band.png"))
    ref = spec.get("ref", "")
    phrase = spec["phrase"]
    counter = spec.get("counter")
    has_counter = counter is not None

    # stagger the words; if a counter precedes them, push the band in later
    base_delay = 1.35 if has_counter else 0.10
    words_html = []
    for i, w in enumerate(phrase):
        cls = "accent" if w.get("accent") else ""
        words_html.append(WORD_TPL.format(cls=cls, delay=base_delay + i * 0.13,
                                           text=w["text"]))
    band_delay = base_delay - 0.05

    counter_html = ""
    counter_js = "window.setCounterTime = function(){};"
    if has_counter:
        value = counter.get("value")
        cap = counter.get("not_recorded_caption", "no number is recorded")
        if value is not None:
            land_js = f"el.textContent = '{value:,}';"
            cap_html = ""
        else:
            land_js = "el.innerHTML = '<span class=\"dash\"></span>';"
            # Same torn-parchment band as the main phrase gets -- no bare text
            # floating on the raw scene (illegible over a busy/dark still).
            cap_html = (f'<div class="counter-cap-wrap">'
                        f'<img class="counter-cap-band" src="{band_uri}">'
                        f'<div class="counter-cap">{cap}</div></div>')
        counter_html = f"""
  <div class="counter-scrim"></div>
  <div class="counter-wrap">
    <div class="counter" id="counter">000</div>
    {cap_html}
  </div>"""
        counter_js = f"""
  window.setCounterTime = function(tMs) {{
    var el = document.getElementById('counter');
    var glow = document.getElementById('glow');
    var settleAt = 950;
    if (tMs < settleAt) {{
      var seed = Math.sin(tMs * 12.9898) * 43758.5453;
      var frac = seed - Math.floor(seed);
      var n = Math.floor(frac * 900) + 100;
      el.textContent = String(n);
      el.style.transform = 'scale(1)';
    }} else {{
      {land_js}
      var since = tMs - settleAt;
      var punch = Math.max(0, 1 - since / 260);
      el.style.transform = 'scale(' + (1 + punch * 0.32) + ')';
      if (glow) {{
        var g = Math.max(0, 1 - since / 500);
        glow.style.opacity = g * 0.9;
        glow.style.transform = 'scale(' + (0.6 + (1 - g) * 0.7) + ')';
      }}
    }}
  }};"""

    html = f"""<!doctype html>
<html><head><meta charset="utf-8">
<style>
  @font-face {{ font-family: "BookAntiquaBold"; src: url("file:///C:/Windows/Fonts/BOOKOSB.TTF"); font-weight: 700; }}
  @font-face {{ font-family: "GeorgiaItalic"; src: url("file:///C:/Windows/Fonts/georgiai.ttf"); font-style: italic; }}

  html,body {{ margin:0; padding:0; width:{L['W']}px; height:{L['H']}px; overflow:hidden; background:#000; }}
  .bg {{ position:absolute; top:0; left:0; width:{L['W']}px; height:{L['H']}px;
         background: url("{still_uri}") center/cover no-repeat; }}
  .grade {{ position:absolute; left:0; right:0; bottom:0; width:{L['W']}px; height:{L['H']}px;
            background: radial-gradient(ellipse at 50% 38%, rgba(10,8,6,0) 30%, rgba(10,8,6,0.45) 78%),
                        linear-gradient(180deg, rgba(10,8,6,0) 55%, rgba(10,8,6,0.55) 100%); }}

  .impact-glow {{ position:absolute; left:{L['glow_left']}px; top:{L['glow_top']}px; width:900px; height:900px;
                  margin-left:-450px; margin-top:-450px; border-radius:50%;
                  background: radial-gradient(circle, rgba(196,150,62,0.55) 0%, rgba(196,150,62,0) 68%);
                  opacity:0; transform:scale(0.6); }}

  .counter-scrim {{ position:absolute; left:50%; top:{L['scrim_top']}px; width:{L['scrim_w']}px; height:{L['scrim_h']}px;
                     margin-left:{-L['scrim_w']//2}px;
                     background: radial-gradient(ellipse at center, rgba(8,6,4,0.62) 0%, rgba(8,6,4,0) 72%);
                     z-index:2; }}
  .counter-wrap {{ position:absolute; left:0; right:0; top:{L['counter_top']}px; text-align:center; z-index:3; }}
  .counter {{ font-family:"BookAntiquaBold", Georgia, serif; font-weight:700;
              font-size:{L['counter_fs']}px; color:#f4f0d8; letter-spacing:4px;
              text-shadow: 0 0 50px rgba(196,150,62,0.65), 0 6px 20px rgba(0,0,0,0.7);
              display:inline-block; min-width:1.2em;
              opacity:0; animation: counterin 0.35s ease forwards; animation-delay:0.15s; }}
  .counter .dash {{ display:inline-block; width:0.62em; height:0.09em; background:#f4f0d8;
                     border-radius:0.05em; vertical-align:0.38em;
                     box-shadow: 0 0 40px rgba(196,150,62,0.55); }}
  @keyframes counterin {{ to {{ opacity:1; }} }}
  .counter-cap-wrap {{ position:relative; display:block; width:{L['cap_band_w']}px; margin:18px auto 0; }}
  .counter-cap-band {{ display:block; width:{L['cap_band_w']}px; height:{L['cap_band_h']}px;
                        filter: drop-shadow(0 8px 14px rgba(0,0,0,0.5)); }}
  .counter-cap {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
                  padding:0 40px; text-align:center;
                  font-family:"GeorgiaItalic", Georgia, serif; font-style:italic; font-size:{L['cap_fs']}px;
                  color:#3a2611; opacity:0; animation: fadein 0.6s ease forwards; animation-delay:1.15s; }}
  @keyframes fadein {{ to {{ opacity:1; }} }}

  .ref {{ position:absolute; top:{L['ref_top']}px; left:{L['ref_left']}px; z-index:3;
          font-family:"GeorgiaItalic", Georgia, serif; font-style:italic; font-size:{L['ref_fs']}px;
          color:#e9c877; opacity:0;
          animation: fadein 0.8s ease forwards; animation-delay: 0.10s;
          text-shadow: 0 2px 8px rgba(0,0,0,0.8); }}

  .band-wrap {{ position:absolute; left:{L['band_left']}px; bottom:{L['band_bottom']}px;
                width:{L['band_w']}px; height:{L['band_h']}px; z-index:3;
                opacity:0; animation: bandin 0.45s ease forwards; animation-delay:{band_delay:.2f}s; }}
  @keyframes bandin {{ to {{ opacity:1; }} }}
  .band-wrap img {{ width:100%; height:100%; display:block;
                     filter: drop-shadow(0 10px 18px rgba(0,0,0,0.5)); }}

  .stage {{ position:absolute; left:0; right:0; bottom:{L['stage_bottom']}px; width:{L['W']}px;
            display:flex; justify-content:center; z-index:4; }}
  .line {{ display:flex; gap:{L['gap']}px; flex-wrap:wrap; justify-content:center; max-width:{L['stage_maxw']}px; }}
  .word {{ font-family:"BookAntiquaBold", Georgia, serif; font-weight:700; font-size:{L['word_fs']}px; line-height:1.05;
           color:#2a1c10; opacity:0; transform: translateY(46px) scale(0.42);
           animation: pop 0.46s cubic-bezier(.2,1.9,.4,1) forwards; }}
  .word.accent {{ color:#8a2318; text-shadow: 0 0 22px rgba(138,35,24,0.35); }}
  @keyframes pop {{
    0%   {{ opacity:0; transform: translateY(46px) scale(0.42); }}
    55%  {{ opacity:1; transform: translateY(-10px) scale(1.14); }}
    78%  {{ transform: translateY(3px) scale(0.97); }}
    100% {{ opacity:1; transform: translateY(0)    scale(1.0); }}
  }}
</style></head>
<body>
  <div class="bg"></div>
  <div class="grade"></div>
  <div class="impact-glow" id="glow"></div>
  {'<div class="ref">' + ref + '</div>' if ref else ''}
  {counter_html}
  <div class="band-wrap"><img src="{band_uri}"></div>
  <div class="stage"><div class="line">{''.join(words_html)}</div></div>
<script>{counter_js}</script>
</body></html>
"""
    return html, has_counter


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--aspect", choices=["16:9", "9:16"], default="16:9")
    ap.add_argument("--duration", type=float, default=None,
                     help="seconds; default auto-sized to the word count / counter")
    a = ap.parse_args(argv)

    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    html, has_counter = build_html(spec, aspect=a.aspect)
    L = LAYOUTS[a.aspect]

    tmp_html = Path(a.out).with_suffix(".build.html")
    tmp_html.write_text(html, encoding="utf-8")

    n_words = len(spec["phrase"])
    duration = a.duration or (1.35 + n_words * 0.13 + 1.0 if has_counter else 0.6 + n_words * 0.13 + 1.0)

    render_clip(tmp_html, Path(a.out), duration, has_counter=has_counter, width=L["W"], height=L["H"])
    tmp_html.unlink()
    print(f"wrote {Path(a.out).resolve()}")


if __name__ == "__main__":
    raise SystemExit(main())
