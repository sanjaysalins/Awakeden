#!/usr/bin/env python
"""EW04 landscape motion-page — render ONE wide 16:9 hero still (the veo source).

The bronze serpent lifted high on the pole over the wilderness camp, the bitten
multitude looking up — the episode's type-of-Christ pivot, composed NATIVELY 16:9
(so no lossy portrait->wide crop). Inked GN style. ~1 credit. Eyeball before veo.

  .venv\\Scripts\\python.exe longform/_style_poc/ew04/_mocomic/_hero_still.py
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("ber", ROOT / "longform" / "_base_elements_refs.py")
ber = importlib.util.module_from_spec(spec); spec.loader.exec_module(ber)
ber.ASPECT = "16:9"

OUT = Path(__file__).resolve().parent / "_landscape" / "hero_serpent_wide.png"

BODY = (
    "A towering bronze serpent, coiled around and gleaming dull burnished metal, mounted high "
    "atop a tall rough-hewn wooden pole planted upright in the desert ground and lifted far "
    "above a wide encampment of ragged Israelite tents spread across a vast barren wilderness "
    "plain; below the pole a great multitude of weary robed ancient Hebrew people, many lifting "
    "their faces and turning to look up toward the serpent on the pole; low grey desert ridges "
    "far in the hazy distance under a heavy pale sky. Wide cinematic 16:9 widescreen establishing "
    "composition, epic scale, the lifted pole standing tall at the centre, dramatic natural "
    "daylight, deep atmospheric distance."
)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ber.lint_canonical("hero_serpent_wide", BODY)
    ber.render(BODY + ber.STYLE, OUT)
    print(f"\nhero still -> {OUT}")


if __name__ == "__main__":
    main()
