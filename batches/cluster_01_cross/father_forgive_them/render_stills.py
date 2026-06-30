#!/usr/bin/env python
"""Stage 1 — render the 7 inked motion-comic stills for 'Father, forgive them'.

Reuses the locked inked seedream renderer (longform/_base_elements_refs.py: render + hf_upload
+ STYLE + ONE) so identity/world is ref-locked to ref_library anchors. Idempotent (skips PNGs
that already exist). ~1 credit/still. Writes a gallery.html for the look-gate review.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/render_stills.py
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("ber", ROOT / "longform" / "_base_elements_refs.py")
ber = importlib.util.module_from_spec(spec); spec.loader.exec_module(ber)

NBP = HERE / "visual" / "nbp"; NBP.mkdir(parents=True, exist_ok=True)
A = ROOT / "ref_library"

# seedream input_images ref-lock is BROKEN (memory: seedream-no-negative-channel) -> render no-ref
# and carry a SHARED Christ descriptor in each prompt for face consistency across panels.
CHRIST = ("the SAME man throughout: a dark-haired bearded man in his early thirties with a calm "
          "Near-Eastern face")
# (slug, subject_block)  — STYLE + ONE are appended by render(). Positive end-states only.
PANELS = [
    ("01_golgotha_hook",
     "A wide vertical view of Golgotha under a black storm sky: a single rough wooden cross stands "
     f"against the darkened heavens, the crucified Christ upon it ({CHRIST}, robed at the waist) seen "
     "from a reverent distance, his hands fixed to the crossbeam; at the foot of the cross several Roman "
     "soldiers in first-century legionary dress crouch in the dust dividing a folded robe between them. "
     "Clean, reverent, restrained."),
    ("02_jesus_prays",
     f"The crucified Christ on the cross ({CHRIST}, robed at the waist), his head lifted toward the dark "
     "sky and his lips parted as he speaks, his face calm and merciful; far below and small, Roman "
     "soldiers divide his clothing. One cold shaft of light falls across his upturned face. Reverent."),
    ("03_prayer_close",
     f"An intimate close view of the face of the crucified Christ ({CHRIST}), eyes lifted toward heaven "
     "in prayer, sorrow and mercy together in his expression, a single shaft of light across his "
     "features against deep ink shadow. Reverent and holy."),
    ("04_cast_lots",
     "Framed low on the dusty ground at the foot of the cross: the weathered hands of Roman soldiers "
     "casting small carved lots and knucklebones in the dirt, a folded seamless robe heaped beside them, "
     "plain low torchlight against deep shadow. The hands and the lots fill the frame."),
    ("05_pierced_hand",
     f"An intimate study of the crucified Christ's open wounded hand ({CHRIST}) against the dark grained "
     "wood of the cross, the palm open with fingers gently spread in a gesture of mercy, a single shaft "
     "of warm light across it. Clean and reverent."),
    ("06_cross_over_us",
     f"The cross seen from low below against a breaking storm sky, the crucified Christ high above "
     f"({CHRIST}, robed at the waist); in the near shadowed foreground one ordinary kneeling figure seen "
     "from behind, small beneath the cross, a single shaft of light falling between them. Reverent, humble."),
    ("07_risen_hero",
     f"The risen Christ standing in warm golden morning light ({CHRIST}, in clean flowing robes), alive "
     "and serene, his glorified face healed and at peace, reaching one open hand with a round healed scar "
     "in the palm gently toward the viewer in welcome, soft deep shadow behind him. The tender gospel "
     "hero image."),
]


def main():
    results = []
    for slug, subj in PANELS:
        dest = NBP / f"{slug}.png"
        ber.lint_canonical(slug, subj)                       # poison linter (warn-only)
        status = ber.render(subj + ber.STYLE + ber.ONE, dest, refs=None)
        results.append((slug, status, "no-ref (consistent prompt)"))

    # gallery.html for the look-gate review
    cards = []
    for slug, status, note in results:
        cards.append(
            f'<figure><img src="nbp/{slug}.png" alt="{slug}">'
            f'<figcaption>{slug} &nbsp;<small>[{status}] {note}</small></figcaption></figure>'
        )
    html = (
        "<!doctype html><meta charset=utf-8><title>Father, forgive them - inked look gate</title>"
        "<style>body{background:#111;color:#eee;font-family:system-ui;margin:24px}"
        "h1{font-size:18px}.g{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}"
        "figure{margin:0}img{width:100%;border:1px solid #444;border-radius:6px}"
        "figcaption{font-size:12px;color:#bbb;margin-top:4px}small{color:#888}</style>"
        "<h1>Father, forgive them - 7 inked panels (Stage 1 look gate)</h1>"
        '<div class=g>' + "".join(cards) + "</div>"
    )
    (HERE / "visual" / "gallery.html").write_text(html, encoding="utf-8")
    ok = sum(1 for _, s, _ in results if s in ("ok", "skip"))
    print(f"\n[stage1] {ok}/{len(results)} stills ready -> {HERE/'visual'/'gallery.html'}")


if __name__ == "__main__":
    main()
