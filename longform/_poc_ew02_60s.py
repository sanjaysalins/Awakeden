#!/usr/bin/env python
"""EW02 Abraham — first-60s long-form POC (graphic-novel style, 16:9).

Stills-gate step: render 6 GN 16:9 stills for the opening 60s of Beat 1,
REUSING the locked base-element canonical wording (ref_library) so the look
matches the library exactly. seedream is ref-lock-broken + 9:16-keyed, so
consistency rides on the canonical TEXT, not an image attach.

Dogfoods the new poison-token linter before spending. ~6 credits.

  .venv\\Scripts\\python.exe longform\\_poc_ew02_60s.py
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ber", ROOT / "longform" / "_base_elements_refs.py")
ber = importlib.util.module_from_spec(spec); spec.loader.exec_module(ber)
ber.ASPECT = "16:9"   # long-form widescreen (library is 9:16)

OUT = ROOT / "longform" / "EW02_Abraham" / "v1" / "_poc60" / "stills"

# locked looks lifted verbatim from ref_library canonicals (knife dropped near Isaac)
ABRA = ("Abraham the patriarch, a very old Hebrew nomad well past a hundred years, tall and "
        "gaunt with deeply weathered sun-blackened bronze skin and hollow cheeks, a grave "
        "heavy-hearted lined face and sorrowful resolute eyes, long flowing white hair and a "
        "thin wind-blown white beard, robed in a dust-grey striped Chaldean desert mantle and a "
        "head-cloth bound with dark cord")
ISAAC = ("his beloved son Isaac, a strong gentle young Hebrew man with smooth sun-warmed olive "
         "skin, a trusting open face, dark hair and a soft young first beard, in a simple "
         "undyed tunic")
DONKEY = ("a small grey ancient Near-Eastern pack donkey saddled with a woven blanket")
SERVANTS = ("two lean young Hebrew servants in coarse undyed wool tunics girded with rope and "
            "simple head-cloths")
MORIAH = ("a lone rocky summit in the land of Moriah rising far off above barren grey ridges, "
          "bare stone and scattered thornbrush on its slopes under a hard clear sky")
WIDE = (" Wide cinematic 16:9 widescreen composition, epic establishing framing, vast desert "
        "landscape, dramatic natural light, deep atmospheric distance.")
CLOSE = (" Cinematic 16:9 widescreen close framing, shallow depth, intimate dramatic light.")

SCENES = [
 ("01_abraham_dawn",
  f"{ABRA}, standing alone in the cold grey light of dawn on a rise in the open wilderness, "
  f"gazing gravely out toward the far horizon, the weight of a hard calling on his bowed "
  f"shoulders, a vast empty stony desert behind him." + WIDE),
 ("02_journey",
  f"{ABRA} walking a pale dusty desert road, carrying a clay firepan of live orange coals and "
  f"small flames in one hand; {ISAAC} walking close at his side; behind them {DONKEY} led by "
  f"{SERVANTS}, the small party crossing empty rocky wilderness on a long journey, heavy and "
  f"quiet." + WIDE),
 ("03_promise_sky",
  f"{ABRA} alone at night on the open desert, his lined face lifted up in aching wonder toward "
  f"a vast dark sky ablaze with countless brilliant stars over the wilderness, a lifetime of "
  f"waiting and trust in his eyes." + WIDE),
 ("04_the_command",
  f"{ABRA} kneeling low and bowed in the open wilderness, head dropped under a crushing "
  f"burden, while high across the wide sky above him the holy presence of the LORD breaks as "
  f"radiant divine light and glory — only light, no face, no body, no figure of any kind. "
  f"Reverent and heavy." + WIDE),
 ("05_moriah_afar",
  f"{ABRA} halted on the desert road on the third day, lifting up his eyes and gazing toward "
  f"{MORIAH} seen far across the barren distance; {DONKEY} and {SERVANTS} small on the track "
  f"behind him. The appointed high place, solemn and remote." + WIDE),
 ("06_heavy_heart",
  f"A close study of {ABRA}, his grave heavy-hearted lined face and sorrowful resolute eyes in "
  f"the cold pale dawn light, a far rocky summit blurred behind him, the cost of the morning "
  f"written on him." + CLOSE),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"EW02 60s POC — {len(SCENES)} stills @ 16:9, ~{len(SCENES)} credits\n")
    for name, body in SCENES:
        ber.lint_canonical(name, body)   # dogfood the poison linter
    print()
    for name, body in SCENES:
        ber.render(body + ber.STYLE, OUT / f"{name}.png")
    print(f"\nstills -> {OUT}")


if __name__ == "__main__":
    main()
