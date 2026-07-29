"""Model bake-off gallery: reference + every model, labelled with cost."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTD = HERE / "_model_bakeoff"
REF = HERE.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png"
NBP = HERE / "_prove_it" / "christ_hero.png"  # nano_banana_pro, already rendered
HTML = OUTD / "_MODEL_BAKEOFF.html"

# model, label, cost
MODELS = [
    ("seedream_v4_5", "Seedream 4.5 (current)", "$0.15"),
    ("seedream_v5_pro", "Seedream 5.0 PRO (new)", "$0.45"),
    ("seedream_v5_lite", "Seedream 5.0 Lite (new)", "$0.15"),
    ("flux_2", "FLUX.2", "$0.15"),
    ("flux_kontext", "Flux Kontext (character)", "$0.23"),
    ("recraft_v4_1", "Recraft V4.1", "$0.19"),
    ("gpt_image_2", "GPT Image 2", "$1.05"),
    ("z_image", "Z Image", "$0.02"),
    ("grok_image", "Grok Image", "$0.15"),
    ("text2image_soul_v2", "Higgsfield Soul 2.0", "$0.02"),
    ("soul_cinematic", "Soul Cinematic", "$0.02"),
    ("kling_omni_image", "Kling O1 Image", "$0.08"),
    ("openai_hazel", "OpenAI Hazel (3:2 only)", "~$1"),
    ("soul_cast", "Soul Cast (photoreal casting tool)", "$0.02"),
]


def card(src, label, cost=""):
    if src and Path(src).exists():
        img = f"<img src='{Path(src).resolve().as_uri()}'>"
    else:
        img = "<div class='miss'>rendering / failed</div>"
    c = f"<span class='cost'>{cost}</span>" if cost else ""
    return f"<figure><figcaption>{label} {c}</figcaption>{img}</figure>"


def main():
    cards = [card(REF, "★ REFERENCE (must match this face)"),
             card(NBP, "nano_banana_pro (tested)", "$0.30")]
    for m, label, cost in MODELS:
        cards.append(card(OUTD / f"{m}.png", label, cost))
    html = f"""<!doctype html><meta charset=utf-8>
<title>Image model bake-off</title>
<style>
 body{{background:#14110d;color:#efe7d6;font-family:system-ui,Arial;margin:0;padding:24px}}
 h1{{font-size:22px;margin:0 0 4px}} p.sub{{color:#b7ab97;margin:0 0 20px}}
 .grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}}
 @media(max-width:900px){{.grid{{grid-template-columns:1fr 1fr}}}}
 figure{{margin:0}} figcaption{{font-size:14px;color:#e9c877;font-weight:700;margin:0 0 6px}}
 .cost{{color:#8f846c;font-weight:400;font-size:12px}}
 img{{width:100%;border-radius:7px;display:block;border:2px solid #000;box-shadow:0 4px 16px rgba(0,0,0,.5)}}
 .miss{{padding:60px;text-align:center;background:#221e18;border-radius:7px;color:#8a7f6c}}
</style>
<h1>Image model bake-off — same Christ, same reference</h1>
<p class='sub'>Which one (a) looks best (rich retro), and (b) kept the SAME man as the ★ reference? Pick your top 2.</p>
<div class='grid'>{''.join(cards)}</div>
"""
    HTML.write_text(html, encoding="utf-8")
    print(f"file:///{str(HTML).replace(chr(92), '/')}")


if __name__ == "__main__":
    main()
