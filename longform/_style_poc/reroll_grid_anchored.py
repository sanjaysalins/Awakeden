"""Re-render every Jesus hero still LOCKED TO THE FACE+BODY GRID (JESUS__GRID.png).
Root cause of the persistent scaling issues: the old anchor was head-and-shoulders
only, so seedream had no locked BODY to scale against and invented per-scene
proportions. The grid carries both the face AND the full standing body, so the model
now has a true scale reference. Every scene passes --image JESUS__GRID.png + explicit
hero framing + correct-proportions guidance. seedream_v4_5, 9:16. Scratchpad/POC only."""
import re, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
HERE = Path(__file__).parent
OUT = HERE / "jesus"
GRID = OUT / "JESUS__GRID.png"        # the new face+body anchor
ASPECT = "9:16"

JESUS = ("Jesus of Nazareth, a Jewish man of about thirty, warm olive-brown skin, a calm noble "
         "face, long dark brown hair parted in the middle falling to the shoulders, a full dark "
         "brown beard, deep compassionate brown eyes, strong gentle features")
STYLE = (" Biblical epic graphic novel style, cinematic manga composition, sacred supernatural "
         "light, dramatic ink shadows, reverent and holy atmosphere, ancient Near-Eastern "
         "period-accurate, mature teen-and-up tone. No text, no lettering, no panels, no speech "
         "bubbles, no watermark, no signature.")
# lock to the GRID — face AND body, so proportions/scale are inherited, not invented.
LOCK = (" Keep the exact same face, hair, beard AND correct adult body proportions as the "
        "reference grid (head about one-seventh of his standing height); natural realistic human "
        "anatomy, no stretched, shrunken or distorted scale.")
REVERENT = " Reverent, dignified and restrained, sorrowful not gory, no explicit wounds, holy."
HERO = (" Jesus is the single dominant central hero, large and powerful in the frame, shot from a "
        "slightly low heroic angle so he commands the composition; he fills most of the frame and "
        "any other figures are clearly smaller, lower and secondary, set back in the background. "
        "Correctly proportioned full figure, strong hero-shot.")

# every hero moment, re-rendered against the grid. framing baked in per slug.
SCENES = {
 "baptism__a": ("standing waist-deep in the river Jordan at dawn, full heroic figure, head bowed, "
                "water streaming from his hair and cupped hands, a shaft of radiant light breaking "
                "through the parting sky above and a faint dove of light descending onto him. Far to "
                "one side and clearly smaller, John the Baptist, a lean bearded prophet in a rough "
                "woven cloth tunic (plain fabric garment, absolutely NO camel, no animal anywhere). "
                "Wide cinematic establishing composition." + HERO + REVERENT),
 "baptism__b": ("chest-up, head bowed, water streaming down his hair and face, hands cupped, a shaft "
                "of radiant light and a faint descending dove of light above him. John the Baptist "
                "only faintly suggested smaller at the edge in a rough woven cloth tunic (plain "
                "fabric, absolutely NO camel, no animal anywhere). Close intimate dramatic "
                "composition, correctly proportioned." + HERO + REVERENT),
 "crowd__a":   ("moving through a press of ancient Galilean villagers on a sunlit dusty street, his "
                "full standing figure central and dominant, face calm and compassionate, the poor "
                "and the sick reaching their hands toward him from below, robed villagers clearly "
                "smaller and crowding around him. Wide cinematic establishing composition."
                + HERO + REVERENT),
 "crowd__b":   ("among the sick and the poor, laying one hand on a kneeling sick man who is clearly "
                "smaller and lower in the frame, his own figure tall, calm and compassionate and "
                "dominant. Close intimate composition, correctly proportioned." + HERO + REVERENT),
 "scourged__a":("bound by the wrists to a low stone pillar in a Roman courtyard, his strong full "
                "figure filling the centre of the frame, head bowed in noble suffering, deep "
                "dramatic ink shadow across the scene; two Roman soldiers in segmented armour kept "
                "small and secondary, set back in the shadowed background, never looming. Wide "
                "cinematic establishing composition." + HERO + REVERENT),
 "scourged__b":("bound by the wrists to a low stone pillar, seen close and from a slightly low angle "
                "so he dominates, bare-torso, head bowed in noble suffering, sweat and shadow on his "
                "face and shoulders, deep dramatic ink shadow; a single Roman soldier only faintly "
                "suggested small in the dark background. Close intimate dramatic composition."
                + HERO + REVERENT),
 "cross__b":   ("crucified on a tall rough wooden cross seen from a low reverent angle, his full "
                "figure dominant against the sky, arms nailed wide along the beam with spikes "
                "through the wrists, bare torso, a simple loincloth at the waist, head fallen "
                "forward, a vast darkening sky of storm cloud and broken gold light behind him. "
                "Close reverent composition." + HERO + REVERENT),
 "risen__a":   ("the risen Christ standing before the rolled-away tomb stone in a garden at dawn, "
                "his full radiant figure central and dominant, robed in glowing white, serene "
                "glorified face, both pierced hands gently open and lifted, clear nail-scars in the "
                "palms, soft blazing golden resurrection light behind him. Wide cinematic "
                "establishing composition." + HERO + " Reverent, triumphant, holy."),
 "risen__b":   ("the risen Christ, full glorified standing figure dominant and central, robed in "
                "radiant white, serene face, both pierced hands lifted with clear nail-scars, "
                "blazing golden resurrection light behind him. Close intimate heroic composition."
                + HERO + " Reverent, triumphant, holy."),
}


def run(prompt, dest):
    if dest.exists():
        dest.unlink()  # force re-render against the grid
    for attempt in (1, 2, 3):
        r = subprocess.run([HF, "generate", "create", "seedream_v4_5", "--prompt", prompt,
                            "--image", str(GRID), "--aspect_ratio", ASPECT, "--wait"],
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
    assert GRID.exists(), "GRID anchor missing — run build_ref_grid.py first"
    for slug, scene in SCENES.items():
        run(JESUS + ", " + scene + LOCK + STYLE, OUT / f"JESUS__{slug}.png")
    print("[done] grid-anchored re-render ->", OUT, flush=True)
