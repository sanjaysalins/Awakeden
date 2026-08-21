"""SEQ "THOMAS" -- Doubting Thomas (John 20:24-29).
First real test of the FRAY -- the DEAD INK system's second motif (fear /
doubt / wavering: the afflicted figure's OWN linework destabilized -- broken,
doubled, tremored contours, scratchy overworked hatching; Jas 1:6, Matt
14:31). The Stain was validated on "The Hem" (render_the_hem.py); the Fray
has never been rendered -- no still, no clip -- until this sequence.

Two pages, designed together per NORTH_STAR_ANIMATION_PROMPT.md LAW 0:

  F01 "the eight days"      -- doubt page. Jesus deliberately ABSENT (v.24
                               "was not with them when Jesus came"). The
                               other disciples mid-telling, alight; Thomas
                               apart, palm out in refusal. Fray FR2 on Thomas
                               ONLY: contour broken and re-struck, a faint
                               tremored second line beside his true edge,
                               hatching scratchy and overworked -- against
                               every other figure's steady single-struck
                               line. Swirl Stage 1: one thread rising from
                               the telling disciple's lifted hands (the life
                               is in the testimony Thomas will not receive).
  F02 "my Lord and my God"  -- resolution page. Jesus present, both open
                               hands offered, one small faint dry ink
                               nail-mark per palm (restraint: never blood,
                               never torn flesh, no side wound depicted
                               anywhere -- the hands carry it). Thomas
                               kneeling, his half-lifted hand stopped just
                               short of touching (John records an ANSWER,
                               v.28, not a touch). Fray FR0: his contour now
                               one single unbroken confidently struck line,
                               hatching calm and even. Swirl Stage 2: threads
                               + one small bloom above Jesus's offered hands.

The Fray's resolution happens AT THE CUT between F01 and F02 -- never
animated inside a clip (DEAD INK animation rule, LAW 2: dispelling a shadow
motif is never a within-clip request; a "line steadies" ask is a face-morph
risk). The cut also IS the story beat: "then came Jesus" (v.26) -- his
arrival and the doubt's death land on the same hard cut, exactly like The
Hem's "straightway".

Fray animation defense (from The Hem's validated fix family): the fence is
PAGE-GLOBAL, not fray-local ("every ink line and mark... stays exactly as
drawn -- including the broken, tremored linework of Thomas's figure...") --
The Hem's failed veo clip proved a motif-local stillness clause cannot fence
the rest of the page. And the motion budget gets legitimate story targets so
it never dumps onto the linework: on F01 the STEADY-lined figures (the
disciples) carry the bigger motion, the frayed figure stays near-hold (one
tiny press-and-hold + one tense breath) -- moving a frayed figure hard would
force the model to redraw his fray frame-by-frame and risk smoothing it.

Model: kling3_0 pro, BOTH pages -- veo-first is the standing default, but
both beats are built on designed completing gestures (F01: the raised palm
pressing outward into refusal, the disciple's lean-in appeal; F02: the
head-bow completing into worship), veo's documented refusal lane (the Cross
blink evidence: veo never attempted the close), and an all-holds prompt is
the exact lifeless failure The Hem hit twice. Same landing spot The Hem's
validated pages reached, re-derived from the tiering rule for these beats.

COST GATE: do NOT run without the user's OK (per /cost). Full fresh spend:
F01 still ~$0.50 + F02 still ~$0.50 (nano_banana_pro 2k) + two kling3_0 pro
5s sound-off clips ~$1.31 each (8.75cr) = ~$3.62 total. (veo would be
~$0.60/clip; the delta buys the completing gestures veo will not execute.)

Run order:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_thomas.py            # F01 still
  ... eyeball QC + F01 referent check (below) ...
  ... crop Thomas's figure from the APPROVED F01 render -> save as the_thomas_ref.png in this folder ...
      (2026-08-20 standing rule: a NEW character's reference is established
      from his FIRST approved render and chained into EVERY render after --
      F02, any regen of an approved page, and any second aspect ratio of F01
      itself; two text-only generations of the same new character drift like
      two different shots. The Hem 16:9 finding.)
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_thomas.py --animate-f01
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_thomas.py --f02
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_thomas.py --animate-f02

F01 referent check (LAW 4 -- regen the still, never adapt the clause, on any fail):
  - Jesus does NOT appear anywhere on the page; NO halo on any figure
    (no jesus_ref is chained, but genre priors can inject him -- look)
  - the Fray reads at 1:1 AND at arm's length: Thomas's contour visibly
    broken and re-struck, a faint tremored second line beside his true edge
    in stretches, hatching scratchy and overworked -- while EVERY other
    figure is steady single-struck line; the contrast must be unmistakable
  - the fray never reads as a ghost / second figure / motion blur -- ONE
    solid Thomas whose ink line wavers (the pareidolia-family check: models
    over-literalize; a doubled contour invites a double man)
  - zero blue and zero gold anywhere in Thomas's figure or hatching
  - exactly ONE blue thread, rising from the foremost disciple's open lifted
    hands, touching nothing and no one else, smooth unbroken calligraphic
    line sharing nothing of Thomas's broken line character
  - a wide band of clean paper between the thread and Thomas at all points
  - Thomas's raised palm-out hand fully inside the frame, unobstructed;
    the stretch of empty floor between him and the group visible
  - baked text exact and nothing more: "SEQ: THOMAS", "F01", the three
    panel labels, caption "I will not believe", "NOTE: line unsteady"
F02 referent check:
  - Thomas matches the_thomas_ref.png; contour ONE single unbroken confident
    line, hatching calm and even -- NO fray remnant anywhere on his figure
  - one small faint dry ink nail-mark in EACH open palm, BOTH palms fully
    inside the frame (the Gold Exemplar's cropped-nail-marks lesson); no
    blood, no torn flesh, no red on or near the hands; no side wound
  - Thomas's half-lifted hand stopped short of touching -- a visible gap
  - Stage 2: a few soft threads + ONE small bloom above Jesus's offered
    hands, well clear of his head and halo, touching neither figure
  - halo on Jesus only, separate from the dose
  - NO stain, ring, or dark blot anywhere (this sequence runs the Fray, not
    the Stain -- any stain-like mark is a cross-contamination FAIL)
  - baked text exact: "SEQ: THOMAS", "F02", panel labels, two stacked
    caption lines "My Lord and" / "my God", "NOTE: line steady"
Clip QC (both): 4-frame contact sheet + real playback, both, always. FAIL if
any linework visibly redraws, steadies, boils, or breaks further -- F01's
fray must hold its EXACT drawn character for the whole clip (the between-
pages rule is only proven if the within-clip line never moves); FAIL if any
new stain, spot, or mark appears anywhere; FAIL if a speech bubble or box
appears around any caption (twice-seen Kling mode; the no-bubble clause is
in both prompts, once-proven on Hem F05 v2, not yet fully trusted). And a
technically-clean all-static clip is a FAIL too (user's standing note):
F01 PASS needs the refusal to land on playback -- the disciple's lean-in
appeal, Thomas's palm pressing outward then holding firm, the tense breath.
F02 PASS needs the worship to land -- the head-bow COMPLETES then holds,
the slow breath loosens his shoulders, the disciples lean gently in.
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
THOMAS_REF = HERE / "the_thomas_ref.png"  # human-cropped from the APPROVED F01 render before F02

F01_PNG = HERE / "the_thomas_f01_9x16.png"
F01_MP4 = HERE / "the_thomas_f01_9x16.mp4"
F02_PNG = HERE / "the_thomas_f02_9x16.png"
F02_MP4 = HERE / "the_thomas_f02_9x16.mp4"

_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
_VID_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

# Face/dress ONLY -- the Fray is applied per-page on top of this build, never
# baked into it (F02 needs the same man steady). Clay-red mantle is his
# signature, distinct from Jesus's indigo; no blue/gold on him ever (chromatic
# reservation: blue+gold belongs to the life motif and halo alone).
_THOMAS_BUILD = (
    "a sturdy middle-aged Galilean man with a squarish weathered face, heavy dark brows, deep-set "
    "questioning eyes, dark hair and a short thick dark beard flecked with grey, a plain robe of "
    "muted clay-red wash over an undyed cream tunic, a rough olive-brown mantle across one "
    "shoulder, drawn in dense workmanlike cross-hatching; he wears no blue and no gold anywhere"
)

F01_STILL_PROMPT = (
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
    'even hatching. Thomas: ' + _THOMAS_BUILD + '. Fray dosage FR2: Thomas alone is drawn with an '
    'unsteady, doubting line — his outline broken in short stretches and struck again, a second '
    'faint tremored line running close beside his true contour in places, as if the '
    "draughtsman's hand wavered and drew his edge twice, his cross-hatching scratchy and "
    'overworked, strokes crossing at restless angles and worked over each other; this unsteadiness '
    'lives in the character of the ink line only — Thomas himself stands solid and still, one '
    'single figure, never blurred, never transparent, never a double image or a second figure — '
    'and his linework stays black ink only, with no blue and no gold anywhere in his figure or '
    'hatching, so his wavering line stands out against the steady lines of every other figure on '
    'the page. Stage 1 dosage: exactly one restrained thread of blue ink, with the faintest trace '
    'of muted gold, rising from the open lifted hands of the foremost telling disciple, curling '
    'upward through the clear air of the room, touching nothing and no one else on its way, tied '
    'to no other figure, drawn as one smooth unbroken confident calligraphic line sharing nothing '
    "of the broken tremored character of Thomas's linework, with a wide band of clean paper "
    'between the thread and Thomas at all points, behaving like a single line of wet ink bled '
    'upward into the paper, quiet and restrained. Small handwritten production notes integrated '
    'naturally on the page: a caption beneath the main scene, handwrite: "I will not believe", '
    'and a corner note, handwrite: "NOTE: line unsteady". No other text, letters, numbers, or '
    'words appear anywhere on the page beyond the exact handwrite strings given above — no '
    'invented captions, signs, inscriptions, or titulus. Palette: black ink, ochre, muted brown, '
    'olive green, clay-red, touches of soft gold wash on aged cream paper with visible grain. Not '
    'photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book '
    'inking, no Renaissance religious staging, no glowing spiritual VFX — every blue or gold '
    'element behaves like literal wet ink bleeding into paper, never a magic-particle glow, and '
    "Thomas's broken tremored linework behaves like a draughtsman's own uncertain pen strokes set "
    'dry in the paper, never smoke, never motion, never a spirit or shadow in the scene.'
)

# F01 animation design notes (LAW 0 -- written with the still, before either
# renders):
#   1. Motion-mass placement is the Fray-specific safety design: the STEADY-
#      lined disciples carry the visible story motion (the lean-in appeal --
#      a completing gesture continuing their drawn telling), while the FRAYED
#      figure stays near-hold (a palm pressing a fraction further along its
#      own drawn vector, then holding, plus one tense breath). Animating a
#      frayed figure hard = the model redraws his fray frame-by-frame and
#      may smooth it; near-hold keeps the register.
#   2. The fence is PAGE-GLOBAL with an "including" callout naming the fray
#      (The Hem F04 v2's validated two-population lesson: a motif-local
#      clause leaves the rest of the page as an unfenced second population).
#      The fray gets its ONE positive stillness clause inside that fence --
#      never a steadies/dissolves ask (DEAD INK rule, mirror of LAW 2's
#      grow family).
#   3. NO_MOUTH on Thomas -- the baked caption "I will not believe" IS his
#      spoken line (John 20:25); compact lips-closed on the disciples (the
#      foremost is drawn mid-telling; without it Kling will talk him).
#   4. Panel 2's nail is a loaded object (crucifixion prior) -> in-place
#      tone/light motion only, per the template caution.
#   5. kling3_0 pro: the press-and-hold and the lean-in must COMPLETE
#      mid-clip (veo's refusal lane). "no border, box, or speech bubble"
#      clause rides in the opening line -- quoted-line caption + Kling is
#      the twice-seen bubble recurrence.
#   6. ~243 words -- above the 70-130 band but AT, not past, the validated
#      ceiling (Hem F05 v2's locked prompt ran 244). The Hem's same density
#      justification: two named motion groups + a near-hold lead + thread
#      hold + page-global fray fence + NO_MOUTH + no-bubble clause.
F01_ANIMATION_PROMPT = (
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
    "blue ink thread above the disciple's hands stays exactly as drawn, in place, for the whole "
    "clip; every ink line and mark on the page is long set and stays exactly as drawn — "
    "including the broken, tremored linework of Thomas's figure, which keeps its exact drawn "
    "character, stroke for stroke, for the whole clip; no line anywhere redraws or changes, and "
    "no new stain, spot, or mark appears anywhere on the page at any point."
)

F02_STILL_PROMPT = (
    'One single storyboard page of hand-drawn animation development art, delicate ink linework and '
    'watercolor on aged cream paper, laid out like a real found piece of production art. Top-left '
    'title, handwrite: "SEQ: THOMAS". Top-right frame number, handwrite: "F02". Across the top, a '
    'row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY '
    'label: panel 1 (handwrite: "doors being shut") a small sketch of the same shut wooden door, '
    'its heavy bar still in place, panel 2 (handwrite: "reach hither") a close quiet study of '
    "Jesus's one open hand alone, palm up, a single small faint dry ink nail-mark at its center, "
    'panel 3 (handwrite: "blessed are they") a small loose sketch of many varied ordinary '
    'figures far off on an open road, faces lifted. Below them, ONE large full-scene illustration '
    'filling the lower half of the page — a MEDIUM TWO-SHOT: the same plain room, now filled '
    'with morning light through the shuttered window, the other disciples drawn back into a '
    'loose still ring behind; Jesus stands at the left, turned fully toward Thomas, his face '
    'calm and glad and fully inside the frame, both open hands held out toward Thomas at chest '
    'height, palms toward him, and in each open palm a single small faint dry ink nail-mark, '
    'both palms and their marks fully inside the frame, drawn as quiet ink marks only, never '
    'blood, never torn flesh, no red on or near his hands; Thomas kneels before him at the '
    'right, risen upright on his knees, his face lifted to Jesus, one hand half-lifted toward '
    "Jesus's offered hands and stopped just short of touching, a clear gap between his "
    'fingertips and the offered hands, his other hand open at his side; both figures fully '
    'inside the frame. Jesus (match the attached reference): a first-century Jewish man in his '
    'early thirties, lean from travel, weathered calm face, dark textured shoulder-length hair, '
    'short natural beard, drawn in broad confident economical ink strokes, loose layered robes '
    'of deep indigo and charcoal watercolor that pool and bloom and leave paper exposed, a faint '
    'incomplete calligraphic halo of muted gold-and-blue curls close around his head, never a '
    "solid disc — this halo is separate from and unrelated to the page's Swirls of Life dose, "
    'and does not grow, spread, or merge with it. Thomas (match the attached reference): '
    + _THOMAS_BUILD + '. Fray dosage FR0: Thomas\'s linework is fully steadied — his contour one '
    'single, unbroken, confidently struck line from head to foot, his cross-hatching laid calm, '
    'even, and unhurried, matching the steady linework of every other figure on the page; no '
    'broken, doubled, or tremored line remains anywhere on his figure. Stage 2 dosage: the blue '
    'ink motif is quietly present — a few soft threads of blue ink and one small watercolor '
    'bloom, with traces of muted gold, curling in the clear air directly above Jesus\'s open '
    'offered hands, well clear of his head and halo, tied to no other figure, touching neither '
    "figure and nothing in the room, behaving like wet ink bled into the paper's morning air, "
    'quiet and restrained. Small handwritten production notes integrated naturally on the page: '
    'a caption beneath the main scene on two stacked lines, handwrite: "My Lord and", handwrite: '
    '"my God", and a corner note, handwrite: "NOTE: line steady". No other text, letters, '
    'numbers, or words appear anywhere on the page beyond the exact handwrite strings given '
    'above — no invented captions, signs, inscriptions, or titulus. Palette: black ink, ochre, '
    'muted brown, olive green, clay-red, touches of soft gold wash on aged cream paper with '
    'visible grain. Not photorealistic, not anime, not Disney, no polished graphic design, no '
    'clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX — every '
    'blue or gold element behaves like literal wet ink bleeding into paper, never a '
    'magic-particle glow, and the faint nail-marks behave like small quiet ink marks set dry in '
    'the drawing, never wounds rendered graphically.'
)

# F02 animation design notes (LAW 0):
#   1. The one human thing per figure, tied to THIS beat (the confession
#      landing, v.28): Thomas -- his head bows slowly into worship, the bow
#      COMPLETING then holding (the demanded proof dissolving into "My Lord
#      and my God"), one slow deep breath loosening his shoulders as the
#      doubt leaves him (the validated Hem F05 v2 "as the fear leaves her"
#      family); his stopped-short hand gets one positive hold -- the touch
#      never lands, as drawn. Jesus -- offered hands steady (the invitation
#      held open), expression softening into quiet warmth (in-place), halo
#      curls rotating (validated clause). The disciples' ring leans gently
#      in (validated F05 clause family).
#   2. NO_MOUTH on THOMAS this page -- the baked caption "My Lord and / my
#      God" IS his spoken line (John 20:28); compact lips-closed on Jesus.
#   3. Panel 2's open-palm study carries the nail-mark (loaded prior) ->
#      in-place light motion only. Panel 3's distant figures may genuinely
#      walk (validated panel content-motion family).
#   4. Page-global fence kept in The Hem's validated shape; the fray is
#      gone, so the fence states the steady line as the page's standing
#      condition -- never a "steadies/heals" transition ask (the resolution
#      already happened at the cut; the clip only keeps it).
#   5. kling3_0 pro: the head-bow must COMPLETE mid-clip (veo's refusal
#      lane -- the Cross blink evidence). ~242 words, above the 70-130
#      band but under the validated ceiling (Hem F05 v2 ran 244), The
#      Hem's same density justification.
F02_ANIMATION_PROMPT = (
    "Stationary camera, locked medium shot of the 2D storyboard layout, frame borders and all "
    "baked text stay completely static and unchanged the entire clip. Animate isolated motion "
    "inside each panel: panel 1 morning light shifts gently across the door, but the door "
    "itself, its wooden bar, and its shut position never move, open, swing, or change in any "
    "way — it is a fixed drawing, only the light crossing it moves; panel 2 the warm light "
    "across the open sketched palm brightens very slightly, nothing else changes; panel 3 the "
    "distant figures walk slowly onward along the road. Large bottom panel: Thomas, staying on "
    "his knees, bows his head slowly and deeply toward Jesus, the bow completing and then "
    "holding, his half-lifted hand held still, just short of the offered hands, one slow deep "
    "breath loosening his shoulders as the doubt leaves him; his lips stay closed and completely "
    "still — he is not speaking and his mouth does not move at all; Jesus holds his open hands "
    "steady toward Thomas at chest height, his expression softening into quiet warmth, his lips "
    "closed and still; the watching disciples lean gently in toward the two of them; the soft "
    "blue threads and small bloom above Jesus's open hands drift gently within their own small "
    "area; the gold-and-blue halo curls rotate slowly around Jesus's head; every ink line and "
    "mark on the page is long set and stays exactly as drawn, Thomas's steady confident "
    "linework included; no line anywhere wavers, redraws, or changes, and no new stain, spot, "
    "or mark appears anywhere on the page at any point. The two handwritten caption lines "
    "beneath the scene, \"My Lord and\" / \"my God\", and the corner note are flat ink already "
    "dry on the paper — like the other handwritten labels on this page, they are NOT spoken "
    "dialogue and never gain a speech balloon, thought bubble, tail, outline, box, panel, or "
    "any drawn shape of any kind around or behind them at any point in the clip; they remain "
    "bare handwritten ink directly on the aged paper texture, identical in treatment to the "
    "panel captions above, from the first frame to the last."
)


def _run_hf(cmd: list[str], out_path: Path, url_re: re.Pattern, timeout: int) -> bool:
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout)
    if proc.returncode != 0:
        print(f"        FAILED: hf CLI exit {proc.returncode}: {(proc.stderr or proc.stdout).strip()[-800:]}")
        return False
    match = url_re.search(proc.stdout)
    if not match:
        print(f"        FAILED: no output URL in stdout: {proc.stdout.strip()[-800:]}")
        return False
    req = urllib.request.Request(match.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        out_path.write_bytes(resp.read())
    print(f"        -> {out_path.name} ({out_path.stat().st_size:,} bytes)")
    return True


def render_still(png: Path, prompt: str, refs: list[str]) -> None:
    if png.exists():
        print(f"  [skip] {png.name} already exists")
        return
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", prompt]
    for ref in refs:
        cmd += ["--image", ref]
    cmd += ["--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    print(f"  [nano_banana_pro] rendering {png.name}...")
    if _run_hf(cmd, png, _IMG_URL_RE, 600):
        print("  NOW: eyeball at 1:1 + run this page's referent check (module docstring) "
              "BEFORE animating.")


def render_animation(mp4: Path, png: Path, prompt: str, model: str = "kling3_0") -> None:
    if mp4.exists():
        print(f"  [skip] {mp4.name} already exists")
        return
    if not png.exists():
        print(f"  FAILED: still {png.name} not rendered yet.")
        return
    # Per-shot tiering: BOTH pages on kling3_0 pro -- each is built on
    # designed completing gestures (F01 press-and-hold + lean-in; F02
    # head-bow), veo's refusal lane per the Cross blink evidence. If either
    # prompt is ever rerun on veo, re-check it for Kling-only wording first.
    cmd = [HF_CLI, "generate", "create", model, "--prompt", prompt,
           "--start-image", str(png), "--aspect_ratio", "9:16"]
    if model == "kling3_0":
        cmd += ["--mode", "pro", "--duration", "5", "--sound", "off"]
    else:
        cmd += ["--duration", "4"]
    cmd += ["--wait"]
    print(f"  [{model}] rendering {mp4.name}...")
    if _run_hf(cmd, mp4, _VID_URL_RE, 900):
        print("  NOW: 4-frame contact sheet + real playback, both (QC law). FAIL if any "
              "linework redraws, steadies, or breaks further, or any new mark appears.")


if __name__ == "__main__":
    if "--animate-f01" in sys.argv:
        render_animation(F01_MP4, F01_PNG, F01_ANIMATION_PROMPT, model="kling3_0")
    elif "--f02" in sys.argv:
        if not THOMAS_REF.exists():
            print(f"  FAILED: {THOMAS_REF.name} missing — crop Thomas's figure from the "
                  f"APPROVED F01 render and save it there first (2026-08-20 ref-chaining rule: "
                  f"a new character's ref is established from his FIRST render and chained into "
                  f"every render after — no chained ref is a hard stop).")
            sys.exit(1)
        render_still(F02_PNG, F02_STILL_PROMPT, [JESUS_REF, str(THOMAS_REF)])
    elif "--animate-f02" in sys.argv:
        render_animation(F02_MP4, F02_PNG, F02_ANIMATION_PROMPT, model="kling3_0")
    elif "--animate-f02-veo" in sys.argv:
        # Fallback after 3 consecutive Kling attempts all regrew a speech bubble around
        # the two-line "My Lord and / my God" caption despite a strengthened no-bubble
        # clause -- diagnosed as a genuine composition-triggered Kling prior (kneeling
        # figure + short exclamation reads as a comic dialogue balloon), not prompt
        # wording. veo3_1_lite doesn't share Kling's speech-bubble failure mode in this
        # project's history; the known tradeoff is veo's refusal lane may not fully
        # complete Thomas's head-bow (accepted per the user, 2026-08-21).
        render_animation(F02_MP4, F02_PNG, F02_ANIMATION_PROMPT, model="veo3_1_lite")
    else:
        # F01 is Thomas's genesis render: no ref exists yet for him, and Jesus
        # is deliberately not in the scene, so this page chains no refs at
        # all. The FIRST approved render becomes the ref (crop step in the
        # run order) — every subsequent Thomas render chains it.
        render_still(F01_PNG, F01_STILL_PROMPT, [])
