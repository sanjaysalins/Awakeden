#!/usr/bin/env python
"""Render the 5 NEW panels for the 12-panel v2 beat sheet — with render_lint pre-flight.

Default = LINT ONLY ($0): runs the deterministic pre-flight on each prompt, no spend.
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/render_new_stills.py
Add --render to actually render (~5 cr) after the prompts are approved:
  … render_new_stills.py --render
Add --brief to print the LLM red-team brief for a given panel index:
  … render_new_stills.py --brief 4
"""
import argparse, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]

def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

ber = _load("ber", "longform/_base_elements_refs.py")
rl = _load("render_lint_lint", "render_lint/lint.py")

NBP = HERE / "visual" / "nbp"
CHRIST = ("the SAME man throughout: a dark-haired bearded man in his early thirties with a calm "
          "Near-Eastern face")
STYLE_NO_TEXT = ber.STYLE.split(" ABSOLUTELY NO text")[0]

# (slug, beat-context, subject, style)
PANELS = [
    ("01b_nailed_hands",
     "HOOK 0-3.4s: 'Nails through his hands.' — a punchy macro open",
     "A stark macro of both of the crucified Christ's hands nailed to the dark grained wood of the "
     "cross-beam: a single rough forged-iron spike driven through the centre of each open palm, dark "
     "blood beading where the black iron enters the flesh, the fingers relaxed and open. A black storm "
     "sky beyond. Only the two nailed hands and the timber fill the frame — no face.",
     ber.STYLE),
    ("01c_soldiers_gamble",
     "HOOK 3.4-6.8s: 'Soldiers at his feet, gambling for his clothes.'",
     "Three Roman soldiers in first-century legionary dress crouched in the dust at the foot of the "
     "great timber cross, their cold indifferent faces bent over a small game of carved lots on the "
     f"ground; dim storm light, deep ink shadow, period-accurate ancient Near-Eastern setting.",
     ber.STYLE),
    ("06b_our_sin",
     "CONVICTION 32.4-35.9s: 'the sin that put him there was ours too.'",
     "The long dark shadow of the cross falls across a small group of ordinary ancient Near-Eastern "
     "figures who stand with bowed heads in the shadow beneath it, the weight of shared guilt on them; "
     "muted storm light, period-accurate robes, deep ink shadow. Reverent, sorrowful.",
     ber.STYLE),
    ("06c_intercession_lives",
     "CONVICTION 39.4-42.8s: 'still lives to make intercession for sinners.' — living Christ bridge",
     f"The living risen Christ standing in warm golden light ({CHRIST}), both hands lifted in "
     "intercession, each open palm bearing one small neat pale healed round scar flat and level with "
     "the skin; his glorified face calm and at peace. Soft deep shadow behind him. Reverent, alive.",
     STYLE_NO_TEXT),
    ("07b_gospel_wide",
     "LANDING 42.8-49.0s: 'while we were yet sinners, Christ died for us.' — wide gospel hero",
     f"The risen Christ standing at the threshold of golden morning light ({CHRIST}, in clean flowing "
     "robes), his arms beginning to open in welcome toward the viewer, his glorified face at peace, "
     "feet planted; warm light breaking wide behind him. A wide reverent gospel-invitation composition.",
     STYLE_NO_TEXT),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", action="store_true", help="actually render (~5 cr)")
    ap.add_argument("--brief", type=int, default=-1, help="print the LLM red-team brief for panel index N")
    a = ap.parse_args()

    if a.brief >= 0:
        slug, ctx, subj, _ = PANELS[a.brief]
        print(rl.redteam_brief(subj, stage="still", context=ctx))
        return

    for slug, ctx, subj, style in PANELS:
        print(f"\n########## {slug} ##########\n{ctx}")
        rl.report(subj, stage="still", context=ctx)
        if a.render:
            dest = NBP / f"{slug}.png"
            ber.lint_canonical(slug, subj)
            status = ber.render(subj + style + ber.ONE, dest, refs=None)
            print(f"  -> RENDER {slug}: {status}")
    if not a.render:
        print("\n[lint-only] no credits spent. Re-run with --render once the prompts are approved.")


if __name__ == "__main__":
    main()
