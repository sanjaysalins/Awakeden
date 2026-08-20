"""F06 "THE STORM" -- Jesus calms the storm (Mark 4:35-41), still + animation
designed together (Fable, 2026-08-20) per NORTH_STAR_ANIMATION_PROMPT.md LAW 0.

Deliberate stress test of the design-together process on the hardest LAW 3 case
so far: the ink motif on a page whose SUBJECT is dramatic water. Solution is a
triple lock (see the design walkthrough in the session notes):
  1. chromatic reservation -- the storm sea is explicitly green-black ink/wash
     with bare-paper foam, "no blue anywhere in the water"; disciples wear no
     blue; blue on the page belongs ONLY to the motif, the halo, and Jesus's
     locked indigo robe (which gets its own boundary clause).
  2. zone separation -- Stage 2 dose lives in a stated clear-dry-air pocket
     directly above Jesus's raised open hand (over the DECK column, not open
     water); the sky is explicitly rainless -- Mark 4:37 is a storm OF WIND,
     rain is not in the text.
  3. form separation -- motif is smooth calligraphic curls "never wave-shaped,
     never foam-shaped"; waves are jagged black-ink forms.

Beat: the mid-rebuke moment ("Peace, be still") -- storm at its peak AND the
miracle on the same page. Stage 2 dose (the turn happening now). NO_MOUTH on
Jesus (he has the spoken line). Model: kling3_0 pro (the only model the
template is validated on; veo has the documented vessel/water invention prior).

Run (still only -- eyeball QC + LAW 4 referent check REQUIRED before animating):
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_storm_f06.py
Then, after the still passes QC:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_storm_f06.py --animate

Referent check before --animate (LAW 4 -- regen the still, never adapt the clause,
if any of these fail):
  - blue threads + small bloom present ABOVE the raised open hand, NOT merged
    with the halo, touching nothing
  - every wave green-black/grey -- ANY blue in ANY wave = regen
  - sail furled and lashed; Peter gripping gunwale; John braced at mast
  - no rain/spray drawn in the sky; raised open hand fully in frame
"""
from __future__ import annotations

import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
REFS_DIR = HERE.parents[1] / ".claude" / "skills" / "swirls-of-life" / "references"
JESUS_REF = str(REFS_DIR / "jesus_ref.png")
STILL_PNG = HERE / "the_storm_f06_9x16.png"
CLIP_MP4 = HERE / "the_storm_f06_9x16.mp4"
_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
_VID_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

STILL_PROMPT = (
    'One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE STORM". Top-right frame number, handwrite: "F06". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "asleep astern") a small sketch of the boat\'s stern bench with its pillow lying empty, still carrying the pressed hollow where Jesus slept a moment before, panel 2 (handwrite: "carest thou not") a close study of Peter\'s storm-lit face, eyes wide with dread, mouth closed, one wet hand clutched in his beard, panel 3 (handwrite: "wind and sea") a small establishing sketch of the empty storm sea alone, jagged wave crests and wind-torn cloud drawn entirely in black ink and grey-green wash with bare-paper foam, no boat in it and no blue in it. Below them, ONE large full-scene illustration filling the lower half of the page — a WIDE shot: a broad open wooden Galilean fishing boat caught at night in a great storm of wind, its weathered hull of warm ochre-brown timber crossing the frame on a gentle diagonal, stern larger at the lower right, bow smaller toward the mid-left, heeled at one steady lean on a heavy swell, its single square sail furled and lashed tight along the yard, fully inside the frame; Jesus stands upright at the stern, planted and calm, fully inside the frame, his right arm raised straight up above his head, his open hand fully inside the frame with clear dark sky above it, his robes and hair streaming sideways in the gale while his face stays composed; Peter grips the gunwale with both hands just forward of him, fully inside the frame, his face turned up toward Jesus in mingled fear and awe; John braces low against the mast with both arms wrapped around it, staring out at the sea; every hand on the boat grips the boat itself; around and below the hull the storm sea stands in heavy jagged swells drawn in black ink and dark olive-green and grey wash, foam picked out as bare cream paper along the crests, the water carrying no blue anywhere — a green-black night sea, never a blue one; above the wave tops the sky is massed dark storm cloud in charcoal and grey wash torn by wind, and the air itself is dry — this is a storm of wind with no rain, no falling water, and no spray hanging anywhere in the air, leaving the pocket of sky above Jesus\'s raised hand clear and empty. Jesus (match the attached reference): a first-century Jewish man in his early thirties, lean from travel, weathered calm face, dark textured shoulder-length hair, short natural beard, drawn in broad confident economical ink strokes, loose layered robes of deep indigo and charcoal watercolor that pool and bloom and leave paper exposed, a faint incomplete calligraphic halo of muted gold-and-blue curls close around his head, never a solid disc — this halo is separate from and unrelated to the page\'s Swirls of Life dose, and does not grow, spread, or merge with it; his indigo robe is cloth with its own drawn ink outline, always distinct from the green-black sea beyond the hull and from the blue ink motif above his hand. Peter: a burly weather-beaten fisherman with heavy shoulders, thick grey-streaked dark hair and a full beard, garments of muted olive-green wash over an undyed tunic, drawn in dense cross-hatching. John: a lean young beardless fisherman with dark curling hair, a clay-red mantle over an undyed cream tunic. Neither disciple wears any blue — their garments keep to olive-green, clay-red, and undyed cream, so that on this page blue belongs only to Jesus\'s robe, his halo, and the ink motif. Stage 2 dosage: the blue Swirls of Life ink motif is quietly present — a few soft threads of blue ink and one small watercolor bloom, with the barest trace of muted gold, curling in the pocket of clear dry air directly above Jesus\'s raised open hand, well above the highest wave crest and well clear of his head and halo, tied to nothing else in the scene, touching neither the sea, nor the boat, nor any figure, drawn as smooth calligraphic curls that are never wave-shaped and never foam-shaped, behaving like wet ink bled into the paper\'s night sky, quiet and restrained, not spectacular. Small handwritten production notes integrated naturally on the page: a caption beneath the main scene, handwrite: "Peace, be still", and a corner note, handwrite: "NOTE: sea green-black". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash on aged cream paper with visible grain. Not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX — every blue or gold element behaves like literal wet ink bleeding into paper, never a magic-particle glow.'
)

ANIMATION_PROMPT = (
    "Stationary camera, locked wide shot of the 2D storyboard layout, frame borders and all "
    "baked text stay static. Animate isolated motion inside each panel: panel 1 light on the "
    "empty pillow deepens slightly; panel 2 storm light on Peter's face dims slowly; panel 3 "
    "the sea sketch's wash deepens slightly. Large bottom panel: Jesus stands firm at the "
    "stern, raised open hand held steady, robes and hair streaming in the wind; his lips stay "
    "closed and completely still — he is not speaking and his mouth does not move at all; "
    "Peter keeps gripping the gunwale, his mantle stirring; John stays braced against the "
    "mast, holding still; the green-black waves rise and fall within their own band around "
    "the hull, the boat rocking gently in place, keeping its steady lean; the golden halo "
    "line swirls rotate slowly around Jesus's head; the soft blue threads above his raised "
    "hand drift gently within their own small area; the furled sail stays lashed along the yard."
)


def render_still() -> bool:
    if STILL_PNG.exists():
        print(f"  [skip] {STILL_PNG.name} already exists")
        return True
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", STILL_PROMPT,
           "--image", JESUS_REF, "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    print("  [nano_banana_pro] rendering still...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=600)
    if proc.returncode != 0:
        print(f"        FAILED: hf CLI exit {proc.returncode}: {(proc.stderr or proc.stdout).strip()[-800:]}")
        return False
    match = _IMG_URL_RE.search(proc.stdout)
    if not match:
        print(f"        FAILED: no image URL in stdout: {proc.stdout.strip()[-800:]}")
        return False
    req = urllib.request.Request(match.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        STILL_PNG.write_bytes(resp.read())
    print(f"        -> {STILL_PNG.name} ({STILL_PNG.stat().st_size:,} bytes)")
    print("  NOW: eyeball the still at 1:1 + run the LAW 4 referent check (see module "
          "docstring) BEFORE re-running with --animate.")
    return True


def render_animation() -> None:
    if CLIP_MP4.exists():
        print(f"  [skip] {CLIP_MP4.name} already exists")
        return
    if not STILL_PNG.exists():
        print("  FAILED: still not rendered yet -- run without --animate first.")
        return
    cmd = [HF_CLI, "generate", "create", "kling3_0", "--prompt", ANIMATION_PROMPT,
           "--start-image", str(STILL_PNG), "--aspect_ratio", "9:16",
           "--mode", "pro", "--duration", "5", "--sound", "off", "--wait"]
    print("  [kling3_0 pro] rendering animation...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=900)
    if proc.returncode != 0:
        print(f"        FAILED: hf CLI exit {proc.returncode}: {(proc.stderr or proc.stdout).strip()[-800:]}")
        return
    match = _VID_URL_RE.search(proc.stdout)
    if not match:
        print(f"        FAILED: no video URL in stdout: {proc.stdout.strip()[-800:]}")
        return
    req = urllib.request.Request(match.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        CLIP_MP4.write_bytes(resp.read())
    print(f"        -> {CLIP_MP4.name} ({CLIP_MP4.stat().st_size:,} bytes)")
    print("  NOW: 4-frame contact sheet + real playback, both (QC law).")


if __name__ == "__main__":
    if "--animate" in sys.argv:
        render_animation()
    else:
        render_still()
