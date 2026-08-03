"""Reroll sl10_overhead_plan and sl16_foreground_occlusion, per the user's
explicit ask (2026-08-02) despite STYLE_LAB.md's own note that sl10 was
already "USER-ACCEPTED despite the text" and marked don't-reword -- this is
a deliberate second attempt anyway, not a silent override of that record.

Reuses _run_bakeoff.py's exact constants (character text, refs, FULLBLEED,
run()) so results stay comparable to the original bake-off. Renders BOTH
Moses and Jesus for each style (4 renders total, ~2cr/~$0.30 each = ~$1.20),
same as the original methodology.

sl16 fix: the original prompt's own "the figure is small, sharp and framed
in the gap" line directly fought the appended close-mid-shot scene -- reworded
to require the face/upper body fill the gap large and unmistakable, framing
occlusion as an edge effect, not a subject-scale effect.

sl10 fix (harder problem, flagged honestly): the diagnosis in STYLE_LAB.md
found the CONCEPT of "overhead/survey" alone pulls in document vocabulary
(labels, scale bars) even with the word "surveyor" removed and an explicit
"no labels" ban in place -- reworded to explicitly deny it's a page/chart/
document of any kind, not just ban the labels. Also: a strict top-down
angle structurally cannot show a face, so this reroll uses a HIGH OBLIQUE
angle (steep but not vertical) and a WALKING scene (not the bake-off's
face-forward mid-shot, which is incompatible with any overhead framing --
same incompatibility STYLE_LAB.md's own diagnosis names as why Moses's
original attempt "just ignored the overhead framing and rendered a plain
portrait"). Identity-lock for this style will likely still score lower than
face-forward styles by construction, not because of wording -- flagged, not
hidden.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_identity_bakeoff/_reroll_sl10_sl16.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _run_bakeoff as B  # noqa: E402 -- reuse MOSES/JESUS/refs/run()/cost logging exactly

OUT_MOSES = HERE / "stills"
OUT_JESUS = HERE / "stills_jesus"

SL16_V2 = (
    "Editorial documentary sketch illustration on aged warm cream paper: the scene is "
    "viewed past a large dark out-of-focus foreground element occupying the left third and "
    "top edge -- a rock face and hanging scrub, rendered in heavy loose graphite, "
    "deliberately unresolved. Framed in the gap between the foreground shapes, the "
    "subject's face and upper body fill the majority of the visible gap -- large, sharp, "
    "and unmistakably close. The foreground occludes only the EDGES of the frame, never "
    "the subject's own scale or clarity. Strong depth layering. Muted watercolour wash, "
    "halftone grain, narrow torn-paper margin. Completely wordless image -- no lettering, "
    "numerals or captions anywhere."
)

SL10_V2 = (
    "Editorial documentary sketch illustration: an extreme high vantage point, as if "
    "standing on a cliff or ridge far above and looking down at a steep oblique angle -- "
    "the stony ground and long cast shadows fill most of the frame, with the walking "
    "figure seen at an angle steep enough that hair, robe colour, and silhouette remain "
    "identifiable -- not a flat vertical blueprint view. Loose graphite-and-ink linework, "
    "muted watercolour wash, soft raking light, halftone grain, narrow torn-paper margin "
    "only at the very outer edge. This is a single continuous outdoor ground plane seen "
    "from height -- NOT a page, chart, map, blueprint, survey document, or any object with "
    "its own border, label, or frame-within-a-frame; nothing appears in the image except "
    "the ground, the shadows, and the walking figure. Completely wordless image -- no "
    "lettering, numerals, coordinates, scale bars, grid-reference marks, or captions "
    "anywhere."
)

JOBS = [
    ("sl16_foreground_occlusion.v2", SL16_V2,
     {"moses": B.MOSES_SCENE, "jesus": B.JESUS_SCENE}),  # same scene -- only the technique changed
    ("sl10_overhead_plan.v2", SL10_V2, {
        "moses": (f"{B.MOSES}, seen walking across open stony wilderness ground from high "
                  f"above, staff in hand, at the steep high angle described above. "
                  f"{B.FULLBLEED}"),
        "jesus": (f"{B.JESUS}, seen walking across open stony wilderness ground from high "
                  f"above, at the steep high angle described above. {B.FULLBLEED}"),
    }),
]


def main():
    for slug, style_prefix, scenes in JOBS:
        for char, scene in scenes.items():
            cfg = B.CHARACTERS[char]
            out_dir = HERE / cfg["out"]
            out_dir.mkdir(parents=True, exist_ok=True)
            out = out_dir / f"{slug}.png"
            if out.exists():
                print(f"[skip] {char}/{slug}")
                continue
            prompt = style_prefix + "\n\nSCENE: " + scene
            print(f"[img] {char}/{slug} ...", flush=True)
            ok = B.run(prompt, out, cfg["ref"])
            if not ok:
                import time
                time.sleep(5)
                ok = B.run(prompt, out, cfg["ref"])
            if ok:
                try:
                    B.cost.record_hf(B.EPISODE, "poc", "stills", B.MODEL,
                                      note=f"[reroll:{char}] {slug}")
                except Exception as e:
                    print(f"   (ledger skipped: {e})")
                print(f"   ok -> {out}")
            else:
                print("   FAILED")


if __name__ == "__main__":
    main()
