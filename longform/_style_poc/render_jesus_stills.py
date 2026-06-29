"""JESUS HERO-STILL TEST — the crucial one (Jesus is in nearly every clip).
One canonical reverent Jesus REF portrait, then EVERY hero moment reference-locked
to it (--image) so the face is identical across all scenes. 2 framings per scene.
Inked biblical-graphic-novel style, seedream_v4_5 (1cr). 9:16 for shorts.
Idempotent, rate-limit-aware. Review at full res BEFORE animating. POC/scratchpad only."""
import re, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
HERE = Path(__file__).parent
OUT = HERE / "jesus"
OUT.mkdir(parents=True, exist_ok=True)
REF = OUT / "JESUS__REF.png"
ASPECT = "9:16"

JESUS = ("Jesus of Nazareth, a Jewish man of about thirty, warm olive-brown skin, a calm noble "
         "face, long dark brown hair parted in the middle falling to the shoulders, a full dark "
         "brown beard, deep compassionate brown eyes, strong gentle features")
STYLE = (" Biblical epic graphic novel style, cinematic manga composition, sacred supernatural "
         "light, dramatic ink shadows, reverent and holy atmosphere, realistic proportions, "
         "ancient Near-Eastern period-accurate, mature teen-and-up tone. No text, no lettering, "
         "no panels, no speech bubbles, no watermark, no signature.")
LOCK = " Keep the exact same face, hair and beard as the reference portrait."
REVERENT = " Reverent, dignified and restrained, sorrowful not gory, no explicit wounds, holy."

REF_PROMPT = (JESUS + ", clean character reference portrait, head and shoulders, facing forward, "
              "serene calm expression, even soft light, plain dark neutral background." + STYLE)

# slug -> scene description (the action/setting; face comes from the locked REF)
SCENES = {
 "baptism": ("standing waist-deep in the river Jordan at dawn, head bowed, water streaming from his "
             "hair and hands, John the Baptist in rough camel-hair beside him, a shaft of radiant "
             "light breaking through the parting sky above, a faint dove of light descending."
             + REVERENT),
 "crowd":   ("moving through a press of ancient Galilean villagers on a sunlit dusty street, his face "
             "calm and compassionate, the poor and the sick reaching their hands toward him, robed "
             "figures crowding close around him." + REVERENT),
 "scourged":("bound by the wrists to a low stone pillar in a Roman courtyard, head bowed in suffering, "
             "two Roman soldiers in segmented armour standing over him, deep dramatic ink shadow "
             "across the scene, his back turned partly away." + REVERENT),
 "cross":   ("crucified on a tall rough wooden cross seen from a low reverent angle, arms nailed wide "
             "along the beam, head fallen forward, a simple cloth at the waist, a vast darkening sky "
             "of storm cloud and broken gold light behind him." + REVERENT),
 "risen":   ("the risen Christ standing before the rolled-away tomb stone in a garden at dawn, robed "
             "in radiant white, a serene glorified face, both pierced hands gently open and lifted, "
             "clear nail-scars in the palms, soft blazing golden resurrection light behind him."
             + " Reverent, triumphant, holy."),
}
VARIANTS = {
 "a": " Wide cinematic establishing composition, full scene.",
 "b": " Closer, more intimate and dramatic composition centred on him.",
}


def run(args, dest):
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {dest.name}", flush=True); return True
    for attempt in (1, 2, 3):
        try:
            r = subprocess.run([HF, "generate", "create", *args, "--aspect_ratio", ASPECT, "--wait"],
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=600)
        except Exception as e:
            print(f"[ERR ] {dest.name}: {e}", flush=True); continue
        blob = (r.stdout or "") + (r.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                dest.write_bytes(resp.read())
            print(f"[ok  ] {dest.name}", flush=True); return True
        print(f"[{'retry' if attempt<3 else 'FAIL'}] {dest.name} (rc={r.returncode})"
              f"{'' if attempt<3 else chr(10)+blob[-240:]}", flush=True)
    return False


if __name__ == "__main__":
    # 1) canonical REF portrait
    run(["seedream_v4_5", "--prompt", REF_PROMPT], REF)
    assert REF.exists(), "REF failed — cannot face-lock the scenes"
    # 2) every hero moment, reference-locked, 2 framings
    for slug, scene in SCENES.items():
        for v, framing in VARIANTS.items():
            prompt = JESUS + ", " + scene + LOCK + framing + STYLE
            run(["seedream_v4_5", "--prompt", prompt, "--image", str(REF)],
                OUT / f"JESUS__{slug}__{v}.png")
    print("\n[done] jesus hero stills ->", OUT, flush=True)
