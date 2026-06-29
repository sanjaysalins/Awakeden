"""Reroll the 2 dropped Jesus stills with fixed prompts, reference-locked to the REF.
 - baptism a: kill the literal-camel hallucination ('camel-hair' -> 'rough garment of coarse
   woven camel-hair cloth', explicitly NOT an animal).
 - cross a: the wide framing drifted to roped + fully-robed; force nailed wrists + bare torso +
   loincloth so it matches the faithful crucifixion (cross b already correct).
Same style/lock tail as render_jesus_stills.py. seedream_v4_5, 9:16. Scratchpad/POC only."""
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

REROLL = {
 "baptism__a": ("standing waist-deep in the river Jordan at dawn, head bowed, water streaming from "
                "his hair and hands, beside him John the Baptist, a lean wild-haired bearded prophet "
                "wearing a rough garment of coarse woven camel-hair cloth (a fabric tunic, NOT an "
                "animal, no camel present), a shaft of radiant light breaking through the parting sky "
                "above, a faint dove of light descending. Wide cinematic establishing composition, "
                "full scene." + REVERENT),
 "cross__a":   ("crucified on a tall rough wooden cross seen from a low reverent angle, his arms "
                "nailed wide along the beam with iron spikes through the wrists, bare torso, wearing "
                "only a simple loincloth at the waist, head fallen forward, a vast darkening sky of "
                "storm cloud and broken gold light behind him. Wide cinematic establishing "
                "composition, full scene." + REVERENT),
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
    print("[done] reroll", flush=True)
