"""Reroll the 4 Jesus stills that had angle/scaling problems — REFRAME as HERO images.
Fixes (user: 'these stills need to be hero images'):
 - scourged a+b: Jesus was tiny/low, DWARFED by two foreground soldiers -> make Jesus the
   large dominant central hero, soldiers smaller and secondary in the background.
 - baptism a+b: Jesus was only co-equal with John + a literal camel leaked in -> make Jesus
   the dominant central hero, John smaller/secondary to the side, and NO camel anywhere.
Same style/lock/reverent tail as render_jesus_stills.py. seedream_v4_5, 9:16. Scratchpad/POC only."""
import re, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
HERE = Path(__file__).parent
OUT = HERE / "jesus"
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
# the HERO framing fix — Jesus is the unmistakable dominant subject, large in frame.
HERO = (" Jesus is the single dominant central hero of the image, large and powerful in the frame, "
        "shot from a slightly low heroic angle so he commands the composition; he fills most of the "
        "frame and all other figures are clearly smaller, lower and secondary, set back in the "
        "background. Strong hero-shot.")

REROLL = {
 "baptism__a": ("standing waist-deep in the river Jordan at dawn, head bowed, water streaming from "
                "his hair and cupped hands, a shaft of radiant light breaking through the parting "
                "sky above and a faint dove of light descending onto him. Far to one side and "
                "smaller, John the Baptist, a lean bearded prophet in a rough woven cloth tunic "
                "(plain fabric garment, absolutely NO camel, no animal anywhere). Wide cinematic "
                "establishing composition." + HERO + REVERENT),
 "baptism__b": ("chest-up, head bowed, water streaming down his hair and face, hands cupped, a shaft "
                "of radiant light and a faint descending dove of light above him. John the Baptist "
                "only faintly suggested smaller at the edge in a rough woven cloth tunic (plain "
                "fabric, absolutely NO camel, no animal anywhere). Close intimate dramatic "
                "composition." + HERO + REVERENT),
 "scourged__a": ("bound by the wrists to a low stone pillar in a Roman courtyard, his strong figure "
                 "filling the centre of the frame, head bowed in noble suffering, deep dramatic ink "
                 "shadow across the scene; two Roman soldiers in segmented armour kept small and "
                 "secondary, set back in the shadowed background, never looming. Wide cinematic "
                 "establishing composition." + HERO + REVERENT),
 "scourged__b": ("bound by the wrists to a low stone pillar, seen close and from a slightly low "
                 "angle so he dominates, head bowed in noble suffering, sweat and shadow on his "
                 "face and shoulders, deep dramatic ink shadow; a single Roman soldier only faintly "
                 "suggested small in the dark background. Close intimate dramatic composition."
                 + HERO + REVERENT),
}


def run(prompt, dest):
    if dest.exists():
        dest.unlink()  # force reroll
    for attempt in (1, 2, 3):
        r = subprocess.run([HF, "generate", "create", "seedream_v4_5", "--prompt", prompt,
                            "--image", str(REF), "--aspect_ratio", ASPECT, "--wait"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
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
    assert REF.exists(), "REF missing"
    for slug, scene in REROLL.items():
        run(JESUS + ", " + scene + LOCK + STYLE, OUT / f"JESUS__{slug}.png")
    print("[done] hero reroll", flush=True)
