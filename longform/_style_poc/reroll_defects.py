"""Targeted reroll of the 3 defective grid-anchored stills:
  crowd__b  — came out as a split two-panel (grid face leaked into a left panel)
  risen__a  — style drifted to glossy soft-anime, not the bold INKED look
  risen__b  — same glossy drift + tiny cross-shapes on the palms (want nail-scars)
Same grid anchor + same framing, but with HARD inked-style enforcement and an
explicit single-frame / no-panel guard. seedream_v4_5, 9:16. Scratchpad/POC only."""
import re, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
OUT = Path(__file__).parent / "jesus"
GRID = OUT / "JESUS__GRID.png"
ASPECT = "9:16"

JESUS = ("Jesus of Nazareth, a Jewish man of about thirty, warm olive-brown skin, a calm noble "
         "face, long dark brown hair parted in the middle falling to the shoulders, a full dark "
         "brown beard, deep compassionate brown eyes, strong gentle features")
# HARD inked enforcement — these drifted glossy/photoreal, force the bold ink look.
STYLE = (" Drawn in INKED BIBLICAL GRAPHIC-NOVEL / cinematic manga ILLUSTRATION style: bold clean "
         "black ink linework and outlines, flat cel-shaded comic colour, hand-drawn 2D artwork, "
         "dramatic ink shadows. NOT a photograph, NOT photorealistic, NOT a glossy 3D render, NOT "
         "soft airbrushed anime — strong visible ink lines. Sacred supernatural light, reverent and "
         "holy atmosphere, ancient Near-Eastern period-accurate, mature teen-and-up tone. No text, "
         "no lettering, no panels, no speech bubbles, no watermark, no signature.")
LOCK = (" Keep the exact same face, hair, beard AND correct adult body proportions as the reference "
        "grid (head about one-seventh of his standing height); natural realistic human anatomy.")
# single-frame guard — kills the split/two-panel leak.
ONE = (" ONE single uninterrupted full-bleed illustration filling the entire frame, a single "
       "unified scene — absolutely NO split screen, NO side panel, NO inset, NO portrait box, NO "
       "diptych, NO border or divider of any kind.")
HERO = (" Jesus is the single dominant central hero, large and powerful, shot from a slightly low "
        "heroic angle so he commands the frame and fills most of it; any other figures are clearly "
        "smaller, lower and secondary in the background. Correctly proportioned full figure.")

SCENES = {
 "crowd__b": ("among the sick and the poor on a sunlit dusty Galilean street, laying one hand on a "
              "kneeling sick man who is clearly smaller and lower in the frame, his own figure tall, "
              "calm, compassionate and dominant. Close intimate composition, correctly proportioned."
              + HERO + ONE + " Reverent, dignified, holy."),
 "risen__a": ("the risen Christ standing before the rolled-away tomb stone in a garden at dawn, his "
              "full radiant figure central and dominant, robed in glowing white, serene glorified "
              "face, both pierced hands gently open and lifted with clear round nail-scars in the "
              "palms (simple dark wound marks, NOT cross shapes), soft blazing golden resurrection "
              "light behind him. Wide cinematic establishing composition." + HERO + ONE
              + " Reverent, triumphant, holy."),
 "risen__b": ("the risen Christ, full glorified standing figure dominant and central, robed in "
              "radiant white, serene face, both pierced hands lifted with clear round nail-scars in "
              "the palms (simple dark wound marks, NOT cross shapes), blazing golden resurrection "
              "light behind him. Close intimate heroic composition." + HERO + ONE
              + " Reverent, triumphant, holy."),
}


def run(prompt, dest):
    if dest.exists():
        dest.unlink()
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
    assert GRID.exists(), "GRID anchor missing"
    for slug, scene in SCENES.items():
        run(JESUS + ", " + scene + LOCK + STYLE, OUT / f"JESUS__{slug}.png")
    print("[done] defect reroll ->", OUT, flush=True)
