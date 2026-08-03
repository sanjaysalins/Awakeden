"""Test sl10_overhead_plan and sl16_foreground_occlusion (both just promoted
to production_approved) on two REAL Bronze Serpent LONG spreads, per the
user's own ask (2026-08-03) after seeing the finished film -- NOT a
production swap yet, just a look-see. Output goes to _test_out/, never
touches the real bronze_serpent_long/stills/ files.

Reuses the episode's own canon text/refs/render() (bronze_serpent_long/
_s2_stills.py) so results are directly comparable to what's actually in the
film -- same MOSES/BRONZE_SERPENT/PEOPLE wording, same 16:9/2k render
settings, same character ref chain.

s41_moses_long_road (sl10 overhead/isolation/map-like): adapts the original
scene ("Moses stands small at the camp's edge, looking down a long empty
road into darkness") to the style's own required high-oblique elevated
viewpoint -- same content, different camera.

s54_timeshift_enshrined (sl16 foreground occlusion/hidden-observer/
threshold): this spread has NO named character (crowd + the bronze serpent
object), so the "subject filling the gap" is the enshrined serpent itself,
not a face -- viewed as if by a hidden witness peering in on the idolatry,
which fits the "hidden-observer" beat-signal arguably better than a portrait
would. No character ref chained (matches the original spread's own empty
ref-tag). The anonymous worshippers stay softer/smaller behind it, per
PEOPLE's own restrained-crowd rule.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_identity_bakeoff/_test_real_spreads.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BSL = HERE.parent / "bronze_serpent_long"
sys.path.insert(0, str(BSL))
import _s2_stills as S  # noqa: E402 -- reuse canon text, refs, run(), cost logging

OUT = HERE / "_test_out"
OUT.mkdir(exist_ok=True)

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
    "the ground, the shadows, and the standing/walking figure. Completely wordless image -- "
    "no lettering, numerals, coordinates, scale bars, grid-reference marks, or captions "
    "anywhere."
)

SL16_V2 = (
    "Editorial documentary sketch illustration on aged warm cream paper: the scene is "
    "viewed past a large dark out-of-focus foreground element occupying the left third and "
    "top edge -- a rock face and hanging scrub, rendered in heavy loose graphite, "
    "deliberately unresolved. Framed in the gap between the foreground shapes, the "
    "primary subject fills the majority of the visible gap -- large, sharp, and "
    "unmistakably close. The foreground occludes only the EDGES of the frame, never the "
    "subject's own scale or clarity. Strong depth layering. Muted watercolour wash, "
    "halftone grain, narrow torn-paper margin. Completely wordless image -- no lettering, "
    "numerals or captions anywhere."
)

JOBS = [
    ("s41_sl10_TEST", SL10_V2,
     (f"A wide composition seen from high above at a steep oblique angle: {S.MOSES} "
      f"stands small at the very edge of the camp, staff in hand, looking down a long "
      f"empty road that stretches away into gathering darkness below, the vast "
      f"landscape and long cast evening shadows dwarfing him, a sense of a path "
      f"leading somewhere beyond what is visible. {S.FULLBLEED}"),
     ["moses"]),
    ("s54_sl16_TEST", SL16_V2,
     (f"TIME SHIFT, generations later, viewed as if by a hidden witness: past a large "
      f"dark out-of-focus foreground element occupying the left third and top edge, "
      f"{S.BRONZE_SERPENT}, now set within a small shrine-like niche of piled stones "
      f"with a woven canopy overhead -- filling the majority of the visible gap, large, "
      f"sharp, and unmistakable -- a visibly different, more elaborate staging than its "
      f"plain forge/pole appearance earlier in the episode. Smaller and softer beyond "
      f"it, {S.PEOPLE}, kneeling before it, some with small trails of incense smoke "
      f"rising from clay dishes at its base, an atmosphere of misplaced reverence and "
      f"creeping idolatry."),
     []),
]


def main():
    for name, style_prefix, scene, ref_tag in JOBS:
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name} already exists")
            continue
        refs = S.resolve_refs(ref_tag[0] if ref_tag else "")
        prompt = style_prefix + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = S.run(prompt, out, refs)
        if not ok:
            import time
            time.sleep(5)
            ok = S.run(prompt, out, refs)
        if ok:
            try:
                S.cost.record_hf("LS_BronzeSerpentLong", "long", "stills", S.MODEL,
                                  note=f"[styletest] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print(f"   ok -> {out}")
        else:
            print("   FAILED")


if __name__ == "__main__":
    main()
