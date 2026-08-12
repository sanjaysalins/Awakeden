"""God Hung Up a Snake (Bronze Serpent short #2, Numbers 21:9) -- step 1: 13
spreads, 9:16. Moses REUSED from the repo-level cast anchor (this narration
names his action, unlike short #1). The bronze serpent object chains from
Look and Live's own approved reference (kling_omni_image, doctrine-correct:
plain bronze/copper, never gold) instead of re-solving the design -- see
_PLAN.md's reuse section. kling_omni_image is the proven cheap default for
this cluster (0.5cr); the landing pair (s12a/s12b) goes straight to
seedream_v4_5 (1cr) since that's what actually worked for the torn-page
device on short #1 -- no need to re-discover that Kling can't do it.

Run all (idempotent, skips existing):
  .venv\\Scripts\\python.exe poc_living_sketchbook/god_hung_up_a_snake/_s1_stills.py
Run specific shots only (e.g. the test batch):
  .venv\\Scripts\\python.exe poc_living_sketchbook/god_hung_up_a_snake/_s1_stills.py s02_pole_reveal s05_forge_acting
"""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "kling_omni_image"
EPISODE = "LS_GodHungUpASnake"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

LYL_SERPENT_REF = (ROOT / "poc_living_sketchbook" / "look_and_live" / "stills" /
                    "s02_object_reveal.png")
MOSES_REF = ROOT / "poc_living_sketchbook" / "cast" / "moses_ref.png"
JESUS_REF = ROOT / "poc_living_sketchbook" / "cast" / "jesus_ref.png"

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge."
)

MOSES = (
    "Moses: an elderly Hebrew man of about 120 years, at the very end of his "
    "life -- his eye not dim, his natural force not abated, drawn upright and "
    "vital despite his extreme age, never frail or feeble. Broad weathered "
    "forehead, deep-set eyes beneath heavy grey brows, hollowed cheeks, a "
    "strong jaw beneath the beard. Long white and grey hair swept back, "
    "thinning at the crown. Long full beard, white streaked with iron-grey, "
    "reaching mid-chest. Deeply sun-weathered leathery skin. An old man's "
    "spare, sinewed frame, still upright and strong-shouldered. Plain undyed "
    "woolen robe, a coarse mantle over one shoulder, a woven cord girdle, "
    "plain leather sandals. THE SAME man as the reference image -- identical "
    "face, beard, hair, and clothing."
)

# (name, refs, chain_from, scene)
SHOTS = [
    ("s01_hook", [], None,
     "WIDE, dusk: a plague-struck wilderness camp, real anguish visible -- a "
     "few unnamed figures mourning or reacting near tents, harsh dust haze, "
     "deep blue-wash evening shadow. No serpent, no pole, anywhere in frame."),

    ("s02_pole_reveal", [LYL_SERPENT_REF], None,
     "LOW ANGLE, looking steeply up: THE SAME bronze serpent-on-pole as the "
     "reference image, same design and material -- plain bronze/copper, "
     "never gold -- standing alone against a cold night sky, starkly "
     "silhouetted, no warm or hopeful light anywhere on it; deep blue-wash "
     "dark behind it."),

    ("s03_texture_insert", [LYL_SERPENT_REF], "s02_pole_reveal",
     "CLOSE-UP, unmistakably a section of a serpent's coiled body wrapped "
     "around the wooden pole from the reference image, same cast bronze "
     "material -- the pole's own wood grain is clearly visible alongside "
     "the scales so the coiled shape and what it is wrapped around both "
     "read immediately, this is a reptile's body, not an abstract "
     "texture, not water, not fish scales, not tree bark; cold moonlit "
     "metal, tight unflinching detail."),

    ("s04_camp_gathered", [LYL_SERPENT_REF], "s02_pole_reveal",
     "WIDE, HIGH angle looking down: THE SAME bronze serpent-on-pole as the "
     "reference image standing at the center, the whole camp gathered "
     "around its base, every visible face turned upward toward it; scale "
     "emphasized, deep blue-wash night."),

    ("s05_forge_acting", [MOSES_REF], None,
     f"{MOSES} EXTREME CLOSE on his weathered hands and a stone hammer, "
     f"striking a glowing piece of bronze on a rough anvil, sparks "
     f"scattering; his face and upper body visible just behind, lit by the "
     f"forge's orange glow; deep shadow beyond the firelight."),

    ("s06_mother_child_look", [], None,
     "An ancient Hebrew mother, Semitic Middle Eastern features, dark eyes, "
     "sun-weathered olive skin, kneeling with a small child of the same "
     "features in her arms, both faces turned upward toward something "
     "off-frame, tired and afraid but hopeful; wilderness dust and tents "
     "soft-focus behind them; warm light beginning to touch their faces "
     "from off-frame."),

    ("s07_moses_face", [MOSES_REF], "s05_forge_acting",
     f"{MOSES} His robe covers both shoulders completely and both upper "
     f"arms down past the elbow, exactly like the reference image -- no "
     f"bare shoulder, no bare chest, no skin visible above his hands and "
     f"neck anywhere. CLOSE portrait, his face resolute and troubled, no "
     f"glorified or warm light -- plain even daylight, honest weight in "
     f"his expression; deep shadow behind him."),

    ("s08_raw_bronze_insert", [], None,
     "CLOSE object-insert: plain unshaped lumps of raw bronze and a few "
     "rough forge tools laid on bare stone, undecorated, no polish, no "
     "figure, no hands, soft raking light."),

    ("s09_reaching_soft", [], None,
     "A close still-life composition, no face, no body, only two hands "
     "entering the frame from the bottom edge: the hands are reaching "
     "down toward bare dry ground and picking up a small soft woven grass "
     "wreath and a folded length of plain pale cloth resting there. "
     "Nothing else is in the frame -- no person, no forge, no pole, no "
     "sky. Warm light on the hands, the ground fading into soft-focus "
     "shadow behind."),

    ("s10_heavy_sky", [], None,
     "WIDE, no figure: a heavy dark night sky over the wilderness, thick "
     "clouds, no stars visible, a distant hint of dawn just beginning at "
     "the horizon's edge; generous still empty sky, a transitional hush."),

    ("s11_pole_night", [LYL_SERPENT_REF], "s02_pole_reveal",
     "WIDE, night: THE SAME bronze serpent-on-pole as the reference image "
     "standing quietly at the center of a now-calm, quiet camp, tents "
     "resting in the darkness around it; deep blue-wash night, still."),

    ("s12a_torn_to_gold", [LYL_SERPENT_REF], None,
     "A landing-device spread: a ragged hole torn through the center of "
     "the cream paper page, in the exact silhouette shape of the serpent "
     "coiled once around a pole shown in the reference image, same dull "
     "bronze and copper coloring as that reference where any of the "
     "serpent's own surface is still visible at the torn edge. The torn "
     "paper's fibrous edges are lit warm gold from behind. Radiant gold "
     "light pours out through the opening. The paper surrounding the tear "
     "stays plain, flat, and untouched."),

    ("s12b_landing_christ", [JESUS_REF], "s12a_torn_to_gold",
     "Through the same torn paper opening as the reference image, same "
     "shape and same ragged fibrous torn edges: Christ hangs lifted up on "
     "a plain wooden cross, seen from a respectful distance, arms extended "
     "along the crossbeam, head bowed, reverent, no visible wounds, no "
     "blood -- the SAME man as the other reference image, identical face, "
     "beard, and hair -- His whole figure filling the opening, radiant "
     "warm gold light surrounding Him. Small and dark in the immediate "
     "foreground below the tear, a plain dull bronze serpent coiled on a "
     "wooden pole sits earthbound and unlit, dull metal in shadow, clearly "
     "smaller and lower than the radiant figure above. Everywhere outside "
     "the tear stays plain aged cream paper, untouched."),
]


def run(prompt, out, refs, model=MODEL):
    cmd = [HF, "generate", "create", model, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--wait"]
    cmd += ["--quality", "high"] if model == "seedream_v4_5" else ["--resolution", "2k"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    only = set(sys.argv[1:]) or None
    for name, refs, chain, scene in SHOTS:
        if only and name not in only:
            continue
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        use_refs = list(refs)
        if chain:
            src = OUT / f"{chain}.png"
            if not src.exists():
                print(f"[HOLD] {name}: chain source {chain} missing")
                continue
            use_refs.append(src)
        model = "seedream_v4_5" if name.startswith("s12") else MODEL
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (model={model}, refs={len(use_refs)}) ...", flush=True)
        ok = run(prompt, out, use_refs, model=model)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, use_refs, model=model)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", model, note=f"[god-hung-up-a-snake] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
