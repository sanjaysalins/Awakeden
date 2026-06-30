#!/usr/bin/env python
"""Vision-audit pre-pass for the base-element reference renders.

The 5-CLI panel only ever saw the TEXT descriptions — it cannot see the rendered
pixels. This closes that gap. Two layers:

  (1) DETERMINISTIC ($0, no LLM): flags black/blank frames (failed renders) and
      near-duplicate images (the "they all look alike" risk) via an average hash.
  (2) HUMAN/VISION review: tiles every ref into paginated contact sheets so a
      human (or a vision model) can eyeball the whole set and flag wrong subject /
      irreverent / garbled-text / atom-bomb issues a pixel metric can't catch.

Output:
  ref_library/_audit/contact_<kind>_<n>.png   -- review sheets
  ref_library/_audit/flags.json               -- deterministic flags
  prints a summary (blank frames + near-dup pairs)

Run AFTER a render batch:
  .venv\\Scripts\\python.exe longform\\_base_elements_audit.py
"""
import json, os
from pathlib import Path
from PIL import Image, ImageDraw

LIB = Path(__file__).resolve().parents[1] / "ref_library"
AUD = LIB / "_audit"
SUBS = [("characters", "CHARACTER"), ("objects", "OBJECT"),
        ("places", "PLACE"), ("motifs", "MOTIF")]
BLANK_MEAN = 20      # mean brightness below this => likely black/failed
BLANK_STD = 10       # stddev below this => flat/blank
DUP_HAMMING = 4      # avg-hash hamming distance <= this => near-duplicate


def ahash(im):
    g = im.convert("L").resize((8, 8))
    px = list(g.getdata())
    avg = sum(px) / len(px)
    bits = 0
    for i, v in enumerate(px):
        if v >= avg:
            bits |= (1 << i)
    return bits


def stats(im):
    g = im.convert("L").resize((64, 64))
    px = list(g.getdata())
    mean = sum(px) / len(px)
    var = sum((p - mean) ** 2 for p in px) / len(px)
    return mean, var ** 0.5


def main():
    AUD.mkdir(exist_ok=True)
    blanks, hashes, n = [], {}, 0
    for sub, label in SUBS:
        d = LIB / sub
        if not d.exists():
            continue
        pngs = sorted(d.glob("*.png"))
        # blank + hash
        for p in pngs:
            n += 1
            try:
                im = Image.open(p)
            except Exception as e:
                blanks.append((p.stem, sub, f"unreadable: {e}")); continue
            mean, std = stats(im)
            if mean < BLANK_MEAN or std < BLANK_STD:
                blanks.append((p.stem, sub, f"mean={mean:.0f} std={std:.0f}"))
            hashes[(sub, p.stem)] = ahash(im)
        # contact sheets, 16 per page
        per, cw, ch, cols = 16, 300, 533, 4
        for pg in range((len(pngs) + per - 1) // per):
            chunk = pngs[pg * per:(pg + 1) * per]
            rows = (len(chunk) + cols - 1) // cols
            sheet = Image.new("RGB", (cw * cols, ch * rows), (20, 22, 28))
            dr = ImageDraw.Draw(sheet)
            for i, p in enumerate(chunk):
                try:
                    im = Image.open(p).convert("RGB").resize((cw, ch))
                except Exception:
                    continue
                x, y = (i % cols) * cw, (i // cols) * ch
                sheet.paste(im, (x, y))
                dr.rectangle([x, y, x + cw, y + 18], fill=(0, 0, 0))
                dr.text((x + 4, y + 4), p.stem, fill=(255, 235, 120))
            sheet.save(AUD / f"contact_{sub}_{pg+1}.png")

    # near-duplicate pairs (within same kind)
    dups = []
    items = list(hashes.items())
    for i in range(len(items)):
        (s1, n1), h1 = items[i]
        for j in range(i + 1, len(items)):
            (s2, n2), h2 = items[j]
            if s1 != s2:
                continue
            ham = bin(h1 ^ h2).count("1")
            if ham <= DUP_HAMMING:
                dups.append((s1, n1, n2, ham))

    (AUD / "flags.json").write_text(json.dumps({
        "n_images": n,
        "blank_or_failed": [{"name": b[0], "kind": b[1], "why": b[2]} for b in blanks],
        "near_duplicates": [{"kind": d[0], "a": d[1], "b": d[2], "hamming": d[3]} for d in dups],
    }, indent=2), encoding="utf-8")

    print(f"audited {n} images")
    print(f"  BLANK/FAILED ({len(blanks)}): " + ", ".join(b[0] for b in blanks) if blanks else "  BLANK/FAILED: none")
    print(f"  NEAR-DUP PAIRS ({len(dups)}): " + ", ".join(f'{d[1]}~{d[2]}' for d in dups) if dups else "  NEAR-DUP PAIRS: none")
    print(f"  contact sheets + flags.json -> {AUD}")


if __name__ == "__main__":
    main()
