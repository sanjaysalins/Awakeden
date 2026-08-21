"""THOMAS F01 v2 -- swirl-legibility redesign (build 1 of SWIRLS_OF_LIFE_SERIES_PLAN.md).

Fixes the one open flag from the 2026-08-20 session (see
NORTH_STAR_ANIMATION_PROMPT.md's OPEN ledger): F01's Stage 1 thread rose
straight up out of the telling disciple's hands, tied to him alone. The
design rationale ("the life is in the testimony Thomas won't receive") only
makes sense explained in prose -- on watch it read as a decorative squiggle
near a random hand, not a real turn of the beat's own action.

Redesign: the SAME thread, same source (the disciple's lifted hands), now
arcs low across the open floor TOWARD Thomas's raised refusing palm and
stops dead in the empty air just short of it -- a visible, deliberate gap
between the thread's tip and his hand. This needs no narration to read: life
is offered, plainly reaching toward him, and not received. It also sets up
F02's payoff on its own terms -- the gap that testimony alone could not
close is closed there by Christ's own hands, not by a continuation of this
exact thread (Stage transitions only happen between pages, DEAD INK LAW 2).

Nothing else about the page changes -- Thomas's Fray, the disciples, the
three panels, the captions all already passed QC and stay byte-identical
in substance. Thomas's reference (the_thomas_ref.png, cropped from the
original approved F01) is chained in this time, unlike the original F01
which had no ref yet to chain -- this is a second render of the same shot
per the 2026-08-20 ref-chaining rule, so chaining it prevents his likeness
drifting from the one F02 will also use.

COST GATE: do NOT run without the user's OK (per /cost). ~$0.50 still
(nano_banana_pro 2k) + ~$1.31 kling3_0 pro 5s sound-off clip (8.75cr) = ~$1.81.

Run order:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_thomas_f01_v2.py
  ... eyeball QC at 1:1 (referent check below) ...
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_thomas_f01_v2.py --animate

Referent check (still): everything in the original F01 referent check
(module docstring, render_the_thomas.py), PLUS:
  - the thread now runs LOW, roughly at hand height, arcing from the
    disciple's hands toward Thomas -- not rising vertically into open air
  - the thread's tip plainly STOPS before reaching Thomas's palm -- a clear,
    visible gap must remain; FAIL if it touches his hand, his figure, or
    reads as fading/dissolving rather than a plain stop
  - the thread must still read as ONE thing reaching toward him, not a
    vague cloud or scatter -- one smooth calligraphic line, same as before
Clip QC: 4-frame contact sheet + real playback. FAIL if the thread grows,
extends, or closes the gap at any point in the clip (Stage 1 holds, exactly
as drawn -- the gap closing is F02's job, not this clip's); FAIL if any of
Thomas's Fray linework redraws/steadies/boils; FAIL if a speech bubble
appears. PASS needs the disciple's lean-in appeal and Thomas's held refusal
to actually read as story motion, not a static hold.
"""
from __future__ import annotations

import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
THOMAS_REF = HERE / "the_thomas_ref.png"

PNG = HERE / "the_thomas_f01_v2_9x16.png"
MP4 = HERE / "the_thomas_f01_v2_9x16.mp4"

_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
_VID_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

# Unchanged from the original F01 (render_the_thomas.py) -- face/dress only,
# the Fray is applied on top per-page.
_THOMAS_BUILD = (
    "a sturdy middle-aged Galilean man with a squarish weathered face, heavy dark brows, deep-set "
    "questioning eyes, dark hair and a short thick dark beard flecked with grey, a plain robe of "
    "muted clay-red wash over an undyed cream tunic, a rough olive-brown mantle across one "
    "shoulder, drawn in dense workmanlike cross-hatching; he wears no blue and no gold anywhere"
)

STILL_PROMPT = (
    'One single storyboard page of hand-drawn animation development art, delicate ink linework and '
    'watercolor on aged cream paper, laid out like a real found piece of production art. Top-left '
    'title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F01". Across the top, a '
    'row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY '
    'label: panel 1 (handwrite: "not with them") a small sketch of a shut wooden door with its '
    'heavy bar in place, panel 2 (handwrite: "the proof") a small plain study of a single iron '
    'nail lying on its side, drawn as a quiet dry object, panel 3 (handwrite: "eight days") a '
    'small sketch of a low-burned oil lamp beside a shuttered window, its oil nearly spent. Below '
    'them, ONE large full-scene illustration filling the lower half of the page — a MEDIUM WIDE '
    'shot: a plain lamplit room at evening, a shuttered window on the back wall; three of the '
    'other disciples stand together at the left of the frame, faces alight with joy, the foremost '
    'of them mid-gesture of telling, his open hands lifted toward Thomas and fully inside the '
    'frame; Thomas stands apart at the right, fully inside the frame, turned half away from them, '
    'his near arm raised with his palm out toward the group in refusal, that raised palm-out hand '
    'fully inside the frame and unobstructed, his jaw set, his mouth closed, his eyes averted '
    'from theirs; a stretch of empty lamplit floor stands open between Thomas and the group. '
    'Jesus is not in this scene and does not appear anywhere on the page, and no halo appears on '
    'any figure. The three disciples are drawn in steady, confident, single-struck ink lines and '
    'even hatching. Thomas (match the attached reference): ' + _THOMAS_BUILD + '. Fray dosage '
    'FR2: Thomas alone is drawn with an unsteady, doubting line — his outline broken in short '
    'stretches and struck again, a second faint tremored line running close beside his true '
    "contour in places, as if the draughtsman's hand wavered and drew his edge twice, his "
    'cross-hatching scratchy and overworked, strokes crossing at restless angles and worked over '
    'each other; this unsteadiness lives in the character of the ink line only — Thomas himself '
    'stands solid and still, one single figure, never blurred, never transparent, never a double '
    'image or a second figure — and his linework stays black ink only, with no blue and no gold '
    'anywhere in his figure or hatching, so his wavering line stands out against the steady lines '
    'of every other figure on the page. Stage 1 dosage: exactly one restrained thread of blue '
    'ink, with the faintest trace of muted gold, rising from the open lifted hands of the '
    "foremost telling disciple and arcing low across the open floor directly toward Thomas's "
    'raised palm, reaching nearly to the level of his outstretched hand before it ends there, '
    "a clear and deliberate gap remaining between the thread's end and his palm — the life "
    'offered, plainly visible, not yet received; the thread touches nothing and no one else on '
    'its way, tied to no other figure, drawn as one smooth unbroken confident calligraphic line '
    "of even, consistent thickness from its start at the disciple's hands to its very end, "
    "sharing nothing of the broken tremored character of Thomas's linework; unlike the wet "
    'bleeding watercolor wash used elsewhere on this page, this one thread is drawn as a single '
    'dry, decisive brush-ink stroke, as if the draughtsman lifted the pen cleanly off the page at '
    'the instant it ends — a clean, solid, unbroken end with no trailing dots, no dashes, no '
    'fading, no feathering, no blur, and no thinning taper anywhere along its length. Small '
    'handwritten production notes integrated naturally on the page: a caption beneath the main '
    'scene, handwrite: "I will not believe", and a corner note, handwrite: "NOTE: line unsteady". No '
    'other text, letters, numbers, or words appear anywhere on the page beyond the exact '
    'handwrite strings given above — no invented captions, signs, inscriptions, or titulus. '
    'Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash on '
    'aged cream paper with visible grain. Not photorealistic, not anime, not Disney, no polished '
    'graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing '
    'spiritual VFX — every blue or gold element behaves like literal wet ink bleeding into paper, '
    "never a magic-particle glow, and Thomas's broken tremored linework behaves like a "
    "draughtsman's own uncertain pen strokes set dry in the paper, never smoke, never motion, "
    'never a spirit or shadow in the scene.'
)

# Animation design notes (LAW 0, unchanged reasoning from the original F01 --
# only the swirl clause's wording changed to match the new geometry):
#   1. Motion-mass placement unchanged: steady disciples carry visible
#      motion (lean-in appeal), Thomas stays near-hold (palm press + tense
#      breath) so nothing forces the model to redraw his fray frame-by-frame.
#   2. Page-global fence unchanged, "including" callout naming the fray.
#   3. NO_MOUTH on Thomas; disciples lips-closed.
#   4. The thread's fixed gap is now the one thing this clip must hold
#      exactly -- Stage 1 does not advance mid-clip (DEAD INK LAW 2), so the
#      gap between the thread's tip and Thomas's palm must not close, drift,
#      or grow at any point.
ANIMATION_PROMPT = (
    "Stationary camera, locked medium wide shot of the 2D storyboard layout, frame borders and "
    "all baked text stay static, with no border, box, or speech bubble ever appearing around any "
    "caption or note. Animate isolated motion inside each panel: panel 1 lamplight shifts gently "
    "across the barred door; panel 2 the light across the sketched nail shifts gently, nothing "
    "else changes; panel 3 the small lamp flame sways softly. Large bottom panel: the foremost "
    "disciple leans in toward Thomas, his open lifted hands rising a little further in appeal, "
    "then holding; the two disciples behind him stir gently in place; their lips stay closed and "
    "still; Thomas holds his ground, his raised palm pressing a fraction further outward toward "
    "them, then holding firm, his shoulders rising and falling with one tense breath, his face "
    "staying turned from them, jaw set, eyes steady and averted; his lips stay closed and "
    "completely still — he is not speaking and his mouth does not move at all; the single thin "
    "blue ink thread reaching from the disciple's hands toward Thomas's raised palm stays exactly "
    "as drawn, its tip held in the same fixed gap short of his hand, for the whole clip; every "
    "ink line and mark on the page is long set and stays exactly as drawn — including the broken, "
    "tremored linework of Thomas's figure, which keeps its exact drawn character, stroke for "
    "stroke, for the whole clip; no line anywhere redraws or changes, and no new stain, spot, or "
    "mark appears anywhere on the page at any point."
)


def render_still() -> bool:
    if PNG.exists():
        print(f"  [skip] {PNG.name} already exists")
        return True
    if not THOMAS_REF.exists():
        print(f"  FAILED: {THOMAS_REF.name} missing.")
        return False
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", STILL_PROMPT,
           "--image", str(THOMAS_REF), "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
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
        PNG.write_bytes(resp.read())
    print(f"        -> {PNG.name} ({PNG.stat().st_size:,} bytes)")
    return True


def render_animation() -> None:
    if MP4.exists():
        print(f"  [skip] {MP4.name} already exists")
        return
    if not PNG.exists():
        print(f"  FAILED: still {PNG.name} not rendered yet.")
        return
    cmd = [HF_CLI, "generate", "create", "kling3_0", "--prompt", ANIMATION_PROMPT,
           "--start-image", str(PNG), "--aspect_ratio", "9:16",
           "--mode", "pro", "--duration", "5", "--sound", "off", "--wait"]
    print("  [kling3_0] rendering animation...")
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
        MP4.write_bytes(resp.read())
    print(f"        -> {MP4.name} ({MP4.stat().st_size:,} bytes)")


if __name__ == "__main__":
    if "--animate" in sys.argv:
        render_animation()
    else:
        render_still()
