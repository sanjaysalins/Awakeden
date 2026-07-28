"""Jericho — step 3: 13 spreads, 9:16. Wall stages image-chain (multi-stage
hard-cut rule: the CUT tells the event, never a morph).

  .venv\\Scripts\\python.exe poc_living_sketchbook/jericho/_j3_stills.py
"""
import importlib.util
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

spec = importlib.util.spec_from_file_location(
    "_e2", ROOT / "poc_castbible_look" / "episode_door" / "_e2_stills.py")
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "LS_Jericho"
HERE = Path(__file__).resolve().parent
CAST = HERE / "cast"
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)
RAHAB_REF = CAST / "rahab_sketch_ref.png"

RAHAB = (
    "Rahab: a Canaanite woman of Jericho in her mid-thirties -- a strong, "
    "handsome, weathered face with dark watchful eyes and dark brows; long "
    "dark hair in a loose braid under a simple cloth head wrap; layered "
    "earth-toned Canaanite wool dress with a deep scarlet sash at the "
    "waist. the SAME woman as the reference image -- identical face, hair, "
    "and clothing."
)
WALLS = ("the massive tiered mud-brick and stone walls of ancient Jericho, "
         "high revetment wall below, brick parapet above, small dark windows "
         "set in the wall face")

STYLE = E.STYLE

# (name, refs, chain_from, scene)
SHOTS = [
    ("j01_walls", [], None,
     f"Wide low view across the plain at dawn: {WALLS} towering over the "
     f"paper spread, deep blue-wash shadow on the land; far below, a long "
     f"thin column of marching figures rendered as small dark silhouettes "
     f"circling the base of the wall, banners and a distant ark-chest "
     f"catching one glint of gold; vast still sky in ink wash."),

    ("j02_feet", [], None,
     "Close on marching feet: worn leather thong sandals of many men "
     "striding left to right across dusty cracked earth, robes' hems "
     "swinging, long morning shadows, dust hanging low; drawn close and "
     "fast, sketch lines energetic."),

    ("j03_laps", [], None,
     f"Top-down bird's-eye spread drawn like a hand-sketched siege plan: "
     f"the walled city of Jericho compact at center -- {WALLS} seen from "
     f"above -- and a single dashed marching path looping around the city "
     f"in a wide circle on the plain, drawn in ink with small arrowheads; "
     f"blue-wash shadows, aged paper, engineering hairlines."),

    ("j04_wallface", [], None,
     f"A tall face-on elevation of {WALLS}, filling the spread edge to "
     f"edge, drawn in patient detail -- brick courses, cracks, worn "
     f"stairs -- and at ONE small upper window a thin SCARLET CORD hangs "
     f"down the wall face, the only red in the whole drawing, a tiny "
     f"thread of color against the vast stone."),

    ("j05_rahab", [RAHAB_REF], None,
     f"{RAHAB} She stands at her small stone window inside the wall, "
     f"lamplight warm on her face, tying the scarlet cord fast to the "
     f"window bar, the cord spilling out over the sill into the night "
     f"air; deep blue night beyond."),

    ("j06_thread", [], None,
     "A quiet stark spread: a single scarlet thread laid across blank aged "
     "cream paper, gently curved, drawn with one confident stroke and a "
     "faint blue-wash shadow; generous still empty paper all around; the "
     "gold leaf strip at the spread's edge."),

    ("j07_trumpets", [], None,
     "A row of priests seen as strong dark silhouettes against a torn "
     "kraft-paper dawn sky, rams-horn trumpets raised high and catching "
     "one line of gold light, robes still, the moment before sound; "
     "energetic ink linework, faces in shadow silhouette only."),

    ("j08_stage_a", [], "j04_wallface",
     f"THE SAME wall face as the reference image, same framing, same "
     f"window with its scarlet cord -- but now deep dark CRACKS split "
     f"through the brick courses in jagged ink lines, dust beginning to "
     f"sift from the joints, small stones loosening; the scarlet cord "
     f"still hanging untouched."),

    ("j09_stage_b", [], "j08_stage_a",
     f"THE SAME wall face as the reference image, same framing -- now "
     f"mid-collapse, frozen at the instant of fall: great slabs of brick "
     f"and stone tilting outward and hanging in the air, huge dust plumes "
     f"billowing up in ink wash, the wall's outline breaking apart -- "
     f"while the ONE section holding the small window and its scarlet "
     f"cord stands unbroken amid the ruin."),

    ("j10_stage_c", [], "j09_stage_b",
     f"THE SAME view as the reference image, same framing, after the "
     f"fall: a vast field of tumbled rubble and settling dust in blue-grey "
     f"ink wash, the city laid open behind -- and ONE tall fragment of "
     f"wall still standing alone, holding the small window with its "
     f"scarlet cord, first warm light touching it."),

    ("j11_spared", [RAHAB_REF], None,
     f"{RAHAB} She stands with a small huddle of family close behind her "
     f"(their faces soft and indistinct) in the doorway of the one "
     f"standing wall fragment amid the rubble field, morning gold light "
     f"breaking over them, the scarlet cord hanging beside her from the "
     f"window above; quiet, spared, still."),

    ("j12_line", [], None,
     "A long horizontal genealogy spread: a single SCARLET THREAD runs "
     "across the aged paper from left to right, passing through faint "
     "graphite sketches of successive generations -- a mother and child, "
     "a shepherd with a harp, a carpenter's family -- each sketch fainter "
     "than real, the thread unbroken through them all, running toward a "
     "warm gold glow at the right edge of the spread."),

    ("j13_landing", [], None,
     "A wide quiet landing spread: the aged paper TORN OPEN at its center "
     "in a tall arched tear, radiant warm gold light glowing from beneath "
     "the page through the tear, and within the gold light the faint "
     "silhouette of a cross on a low hill; the single scarlet thread runs "
     "across the paper and disappears INTO the torn opening; generous "
     "still paper around; a thin gold leaf strip at the edge."),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
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
    for name, refs, chain, scene in SHOTS:
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
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(use_refs)}) ...", flush=True)
        ok = run(prompt, out, use_refs)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, use_refs)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[jericho] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
