"""SEQ "THE HEM" -- the woman with the issue of blood (Mark 5:25-34).
First real test of the DEAD INK companion motif system (Fable, 2026-08-20):
the cold in-paper STAIN (sin / uncleanness / the burden) sharing a page with
the blue-gold Swirls of Life motif, and being dispelled BETWEEN pages, never
within a clip.

Two pages, designed together per NORTH_STAR_ANIMATION_PROMPT.md LAW 0:

  F04 "the touch"   -- confrontation page. Swirl Stage 1 (one thread rising
                       from the hem at her fingertips) + Stain D2 (cold
                       grey-umber damp-stain soaked into the paper under her,
                       crossing the frame border into the margin, its edge
                       nearest the hem already dried pale). The QUAD lock keeps
                       them apart: chromatic (no blue/gold in stain, no umber
                       in swirl) + zone (band of clean paper between them,
                       always) + form (formless blot vs calligraphic curl) +
                       substrate (stain lies IN the paper under the linework;
                       swirl is drawn ON it).
  F05 "made whole"  -- resolution page. Swirl Stage 2 above Jesus's extended
                       hand + Stain D1 (only a thin pale dried watermark ring;
                       the paper inside it the cleanest cream on the page --
                       "whiter than snow"). The stain's disappearance happens
                       AT THE CUT between F04 and F05 ("straightway", Mark
                       5:29) -- never animated inside a clip.

Animation (v2, 2026-08-20): the first F04 attempt (veo3_1_lite, all-holds
prompt) FAILED on the contact sheet -- a NEW warm-brown stain grew into the
sky and panel 3, and the drawn stain expanded, despite the stain's positive
stillness clause. Full diagnosis in the comment above F04_ANIMATION_PROMPT.
v2 plan: F04 on kling3_0 pro (the standing switch-models rule, plus the
redesigned prompt asks for completing gestures -- her fingers close on the
hem, his step settles to a stop -- Kling's validated lane); F05 stays on
veo3_1_lite (pure holds, Storm F06's validated strength) [SUPERSEDED, next
paragraph]. The stain family
still NEVER gets a fade/shrink/dissolve verb (mirror of LAW 2's grow family);
both clips now also carry a page-global "every mark is old, dry, long set /
nothing new appears" fence, because the failed clip's growth was PAGE-level
(the paper's own warm aging animated, not the cold grey stain itself) -- a
stain-local clause cannot fence the rest of the paper.

F05 v2 (2026-08-20, later the same day): F05's veo all-holds clip passed
technical QC (stain/ring stable, no escalation) but FAILED on the user's
watch -- "this was not that good... too static/lifeless." Same disease as
F04's first attempt (all-holds prompt forgets the larger story), diagnosed
there by the user's own note, never applied here. F05 v2 applies the
identical fix family, tuned to THIS beat's drama (relief/blessing, not the
desperate touch): Jesus inclines his head in one small kind nod ("Daughter"),
the woman draws one deep breath and her shoulders release as the fear leaves
her, panel 2's tear-streaked face gets a full-arc blink, the crowd that just
witnessed the miracle leans gently in; the page-global fence stays verbatim.
Model moves to kling3_0 pro: the nod and the blink are completing gestures --
veo's known refusal lane (the Cross blink evidence: veo never attempted the
close) -- plus the switch-models rule after a failed attempt, plus F04 v2's
own validated precedent on this exact fix family.

COST GATE: do NOT run without the user's OK (per /cost). Remaining spend from
here: F05 clip v2 retest ~$1.31 (Kling pro 5s sound-off, 8.75cr) -- vs $0.60
if it had stayed on veo; the delta buys the completing gestures veo will not
execute. (Everything else is spent: F04 still + v2 clip rendered and passed;
F04's failed veo clip ~$0.60; F05 still ~$0.50; F05's lifeless veo clip
~$0.60.)

Run order:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_hem.py            # F04 still
  ... eyeball QC + referent check (below) ...
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_hem.py --animate-f04
  ... crop the woman's figure from the F04 render -> save as the_hem_woman_ref.png in this folder ...
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_hem.py --f05
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_hem.py --animate-f05

F04 referent check (LAW 4 -- regen the still, never adapt the clause, on any fail):
  - fingertips in contact with the hem's woven border, contact point unobstructed
  - exactly ONE blue thread, rising from the hem, touching nothing else,
    clearly separate from Jesus's halo
  - stain: cold grey-umber, matte, formless, UNDER the linework (drawn lines
    pass over it unbroken), crossing the frame border into the margin;
    ZERO blue, gold, or red in it; a clean-paper band between stain and thread
    at every point; no face/figure/creature shape readable in the blot
    (pareidolia check); not touching Jesus, the hem, or any face
  - the stain's edge nearest the hem dried to a pale watermark ring
  - no red anywhere on or near the woman
F05 referent check:
  - no dark stain anywhere; only the thin pale dried ring around where she
    kneels, paper inside it clean bright cream
  - Stage 2 threads + small bloom above Jesus's extended hand, clear of halo
  - woman matches the F04 crop ref; cross-hatching calm and even
Clip QC (both): 4-frame contact sheet + real playback. FAIL if the stain
changes shape, size, or position at all, if the thread grows/travels, or if
ANY new stain, spot, or darkening appears anywhere on the page (the veo
failure mode -- watch the sky, the margins, and panel 3 specifically).
F04 PASS also requires the story motion to actually be present on playback:
her fingers close on the hem, Jesus's step settles to a stop, the crowd
stirs -- a technically-clean all-static clip is a FAIL too (user's note).
F05 v2 PASS requires the same on playback: his small nod lands, her breath /
shoulder-release reads, panel 2's blink COMPLETES (closes AND reopens), the
crowd visibly stirs -- and no speech bubble or box appears around any caption
(the twice-seen Kling failure mode; the no-bubble clause is in the prompt but
still unproven as a fix).
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
WOMAN_REF = HERE / "the_hem_woman_ref.png"  # human-cropped from the F04 render before F05

F04_PNG = HERE / "the_hem_f04_9x16.png"
# the_hem_f04_9x16.mp4 (v1) = the failed 2026-08-20 veo3_1_lite attempt (new
# stain grew into the sky + panel 3) -- kept on disk as evidence, not reused.
F04_MP4 = HERE / "the_hem_f04_9x16_v2.mp4"
F05_PNG = HERE / "the_hem_f05_9x16.png"
# the_hem_f05_9x16.mp4 (v1) = the 2026-08-20 veo3_1_lite all-holds attempt --
# technically clean, rejected by the user on watch as static/lifeless. Kept on
# disk as evidence, not reused.
F05_MP4 = HERE / "the_hem_f05_9x16_v2.mp4"

_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
_VID_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

_WOMAN_BUILD = (
    "a gaunt weary woman with a drawn, hollowed face and large hopeful dark eyes, dark hair "
    "fully under a plain undyed head covering, layered garments of faded olive-green and muted "
    "grey-brown wash over an undyed cream tunic, drawn in dense fine cross-hatching; she wears "
    "no blue and no red anywhere"
)

F04_STILL_PROMPT = (
    'One single storyboard page of hand-drawn animation development art, delicate ink linework and '
    'watercolor on aged cream paper, laid out like a real found piece of production art. Top-left '
    'title, handwrite: "SEQ: THE HEM". Top-right frame number, handwrite: "F04". Across the top, a '
    'row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY '
    'label: panel 1 (handwrite: "spent all") a small sketch of an empty open coin purse lying flat '
    'with two small worn coins beside it, panel 2 (handwrite: "the reach") a close study of the '
    "woman's reaching hand alone, fingers extended, drawn in fine tentative cross-hatching, panel 3 "
    '(handwrite: "the throng") a small sketch of the pressing crowd from behind, tight shoulders and '
    'backs and head coverings packed close, no faces. Below them, ONE large full-scene illustration '
    'filling the lower half of the page — a MEDIUM WIDE shot: a dusty daylight street thick with a '
    'pressing crowd; Jesus stands at the left third of the frame in three-quarter view from behind, '
    'caught mid-step and fully inside the frame, the woven border at the hem of his outer garment '
    'hanging clear at his heel; the woman kneels low at the center-right, crouched forward with one '
    'arm stretched toward him, and her extended fingertips are touching the woven border of the hem, '
    'the point of contact fully inside the frame and unobstructed; her face is turned up in desperate '
    'hope beneath her plain head covering; around and behind them the thronging crowd presses in, '
    "drawn slightly smaller and fainter toward the background, every crowd figure's attention forward "
    'along the street, none of them noticing her. Jesus (match the attached reference): a '
    'first-century Jewish man in his early thirties, lean from travel, weathered calm face, dark '
    'textured shoulder-length hair, short natural beard, drawn in broad confident economical ink '
    'strokes, loose layered robes of deep indigo and charcoal watercolor that pool and bloom and '
    'leave paper exposed, a faint incomplete calligraphic halo of muted gold-and-blue curls close '
    "around his head, never a solid disc — this halo is separate from and unrelated to the page's "
    "Swirls of Life dose and the page's stain, and does not grow, spread, or merge with either. "
    'The woman: ' + _WOMAN_BUILD + '. Stage 1 dosage: exactly one restrained thread of blue ink, '
    'with the faintest trace of muted gold, rising from the woven hem at the exact point her '
    "fingertips touch it, curling upward through the clear air above the crowd's heads, touching "
    'nothing and no one else on its way, tied to no other figure, behaving like a single line of wet '
    'ink bled upward into the paper, quiet and restrained. Stain dosage D2: one cold grey-umber '
    'stain lies soaked into the paper itself, an old mark long since set and fully dry, lying '
    'around and beneath the kneeling woman in the lower-right of the page, its soft feathered '
    "edge reaching across the drawn frame border into the page's own bottom-right margin, where "
    'it ends in a fine dried tide-line — a plain, formless, matte water-stain set in the paper '
    'long ago, even and abstract, depicting nothing; it lies beneath the ink linework, so every '
    'drawn line and figure passes over it unbroken; it is distinctly colder and greyer than the '
    "page's warm cream aging, contains no blue and no gold and no red, is never swirl-shaped and "
    'never smoke or cast shadow inside the scene; it touches neither Jesus, nor the hem, nor the '
    'blue ink thread, and a wide band of clean warm paper stands between the stain and the blue '
    "thread at all points; the stain's edge nearest the hem has long since dried down to a thin "
    'pale watermark ring. Small handwritten production notes '
    'integrated naturally on the page: a caption beneath the main scene on two stacked lines, '
    'handwrite: "If I may touch", handwrite: "but his clothes", and a corner note, handwrite: '
    '"NOTE: stain in paper". No other text, letters, numbers, or words appear anywhere on the page '
    'beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or '
    'titulus. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold '
    'wash on aged cream paper with visible grain. Not photorealistic, not anime, not Disney, no '
    'polished graphic design, no clean comic-book inking, no Renaissance religious staging, no '
    'glowing spiritual VFX — every blue or gold element behaves like literal wet ink bleeding into '
    'paper, never a magic-particle glow, and the cold stain behaves like the dry, long-set mark '
    "of old damp in the paper's fibers, never smoke, never darkness in the scene's air."
)

# v2 redesign, 2026-08-20, after the failed veo attempt. Diagnosis of v1:
#   1. The growth was PAGE-level, not stain-local: the new blobs were WARM
#      BROWN (the paper's own aging/foxing color), not the cold grey of the
#      drawn stain. The model animated "old stained paper" as a class; v1's
#      clause fenced only "the cold stain," leaving the foxing/margins as a
#      second, unfenced stain population. Fix: one page-global clause in the
#      validated Stage-0 absence shape ("no new X appears anywhere... at any
#      point"), plus temporal reframing -- every mark is OLD, DRY, LONG SET
#      (a dried stain and a damp one look identical in a still, so this
#      contradicts no pixel; it only kills the wet-process prior).
#   2. Motion-mass misallocation: v1's only repeated dynamic verb was
#      "deepens" (x3 across the panel row) on an otherwise all-holds prompt.
#      The model's motion budget flowed into the page's one darkening-capable
#      material -- the stains -- and the blob grew into panel 3, one of the
#      three panels explicitly asked to "deepen." Fix: delete every darkening
#      ask and give the motion budget legitimate story targets instead (the
#      user's own note): her fingers CLOSE on the hem, his step SETTLES to a
#      stop (he cannot keep walking -- that would tear the hem from her
#      fingers), the halo quickens as he stops, the crowd jostles.
#   3. Completing gestures (close, settle-to-stop) are Kling's validated lane
#      (veo never attempts them -- the blink evidence), and the standing rule
#      says switch models after a shot fights one: so v2 renders on
#      kling3_0 pro, not veo. "glinting softly" is Kling-legal wording; if
#      this prompt is ever rerun on veo, swap it to "slowly warming".
#   4. Runs ~200 words, above the template's 70-130 band, deliberately: this
#      page carries more locked elements than any validated page (two named
#      figures + crowd + thread + halo + a two-population stain fence +
#      mandatory NO_MOUTH -- the baked caption IS her spoken line, Mark 5:28).
#      The thread keeps its verbatim hold (stage-1 rule: never animate it).
F04_ANIMATION_PROMPT = (
    "Stationary camera, locked medium wide shot of the 2D storyboard layout, frame borders and all "
    "baked text stay static. Animate isolated motion inside each panel: panel 1 light shifts gently "
    "across the purse and coins; panel 2 the sketched fingers curl slowly toward a grasp; panel 3 "
    "the crowd stirs, shoulders shifting. Large bottom panel: Jesus's forward step settles to a "
    "stop, robes falling still, gaze forward along the street; the halo curls circle his head a "
    "touch faster, glinting softly; the woman stays low on her knees, her outstretched fingers "
    "closing gently around the woven hem and holding it, the garment undisturbed, her arm trembling "
    "faintly, her face lifted, eyes steady on Jesus; her lips stay closed and completely still — "
    "she is not speaking and her mouth does not move at all; the packed crowd shifts and jostles "
    "gently in place; the single thin blue ink thread above the hem stays exactly as drawn, in "
    "place, for the whole clip; every stain and mark in the paper — including the grey stain "
    "beneath the woman — is old, dry, and long set, staying exactly as drawn; no new stain, spot, "
    "or darkening appears anywhere on the page at any point."
)

F05_STILL_PROMPT = (
    'One single storyboard page of hand-drawn animation development art, delicate ink linework and '
    'watercolor on aged cream paper, laid out like a real found piece of production art. Top-left '
    'title, handwrite: "SEQ: THE HEM". Top-right frame number, handwrite: "F05". Across the top, a '
    'row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY '
    'label: panel 1 (handwrite: "he turned") a small sketch of Jesus\'s head and shoulder from '
    'behind, mid-turn, panel 2 (handwrite: "all the truth") a close study of the woman\'s upturned '
    'face, tear-streaked but steady, mouth closed, panel 3 (handwrite: "go in peace") a small '
    'sketch of the street ahead where the crowd has opened a clear path between its figures. Below '
    'them, ONE large full-scene illustration filling the lower half of the page — a MEDIUM '
    'TWO-SHOT: the dusty daylight street, the crowd fallen still and drawn back a pace into a loose '
    'ring; Jesus stands at the left, now turned fully toward the woman, his face calm and kind and '
    'fully inside the frame, one open hand extended toward her at chest height, held still in '
    'blessing; the woman kneels upright before him at the right, risen tall on her knees, her face '
    'lifted to his, her hands open at her sides; both figures fully inside the frame. Jesus (match '
    'the attached reference): a first-century Jewish man in his early thirties, lean from travel, '
    'weathered calm face, dark textured shoulder-length hair, short natural beard, drawn in broad '
    'confident economical ink strokes, loose layered robes of deep indigo and charcoal watercolor '
    'that pool and bloom and leave paper exposed, a faint incomplete calligraphic halo of muted '
    'gold-and-blue curls close around his head, never a solid disc — this halo is separate from '
    "and unrelated to the page's Swirls of Life dose, and does not grow, spread, or merge with it. "
    'The woman (match the attached reference): ' + _WOMAN_BUILD + ', her cross-hatching now laid '
    'calm and even. Stage 2 dosage: the blue ink motif is quietly present — a few soft threads of '
    'blue ink and one small watercolor bloom, with traces of muted gold, curling in the clear air '
    "directly above Jesus's extended open hand, well clear of his head and halo, tied to no other "
    "figure, touching neither figure and nothing in the scene, behaving like wet ink bled into the "
    'paper\'s daylight air, quiet and restrained. Stain dosage D1: around where the woman kneels, '
    'one thin, faint, pale dried watermark ring lies in the paper — only the dried edge of an old '
    'damp stain, the stain itself gone from the paper, with the paper inside that ring the '
    'cleanest, brightest cream on the whole page; the ring contains no blue, no gold, and no red, '
    "and it touches neither figure's drawn lines. Small handwritten production notes integrated "
    'naturally on the page: a caption beneath the main scene on two stacked lines, handwrite: '
    '"thy faith hath", handwrite: "made thee whole", and a corner note, handwrite: "NOTE: stain '
    'dried". No other text, letters, numbers, or words appear anywhere on the page beyond the exact '
    'handwrite strings given above — no invented captions, signs, inscriptions, or titulus. '
    'Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash on '
    'aged cream paper with visible grain. Not photorealistic, not anime, not Disney, no polished '
    'graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing '
    'spiritual VFX — every blue or gold element behaves like literal wet ink bleeding into paper, '
    'never a magic-particle glow, and the pale dried ring behaves like the watermark edge of old '
    "damp long gone from the paper's fibers."
)

# v2 redesign, 2026-08-20, after the user rejected the veo all-holds clip on
# watch ("too static/lifeless"). Same fix family as F04 v2, tuned to THIS
# beat (the blessing landing, Mark 5:33-34 -- her fear resolving into peace,
# his kindness reaching her, a crowd that just saw it happen):
#   1. Real story motion per element, referents rewritten against the RENDERED
#      still (LAW 4): Jesus -- one small kind nod toward her, then holds
#      ("Daughter..."); the woman -- one slow deep breath, shoulders easing
#      down as the fear leaves her (her hands rendered open and outstretched,
#      NOT at her sides as the still prompt asked -- described as rendered);
#      the crowd (rendered as a watching ring, several foreground figures
#      kneeling) leans gently in; panel 2's tear-streaked close-up gets the
#      full-arc blink (close THEN reopen, per the template rule). Panel 1 is
#      Jesus from behind mid-turn -- its motion is robe-only, deliberately:
#      continuing the turn would force the model to invent his face.
#   2. NO_MOUTH moves to JESUS this page: the baked caption "thy faith hath /
#      made thee whole" IS his spoken line (Mark 5:34). The woman (who spoke
#      "all the truth" in this beat, Mark 5:33) keeps a compact lips-closed
#      clause. The no-bubble clause rides in the opening line -- quoted-line
#      caption + Kling is exactly the twice-seen speech-bubble recurrence.
#   3. Dose clause upgraded to match pixels: the render shows threads AND one
#      small bloom above his hand; halo rendered gold-and-blue. Page-global
#      old/dry/long-set fence kept verbatim from F04 v2 (validated).
#   4. kling3_0 pro, not veo: the nod and the blink must COMPLETE mid-clip
#      (veo never attempts completing gestures -- the blink evidence), plus
#      the switch-models rule after veo's failed attempt. ~230 words, above
#      the 70-130 band with F04 v2's same justification (two named figures +
#      crowd + dose + halo + ring fence + NO_MOUTH + no-bubble clause).
F05_ANIMATION_PROMPT = (
    "Stationary camera, locked medium shot of the 2D storyboard layout, frame borders and all "
    "baked text stay static, with no border, box, or speech bubble ever appearing around any "
    "caption or note. Animate isolated motion inside each panel: panel 1 the turning figure's "
    "robe stirs gently and settles; panel 2 her eyes close slowly, then open again fully, ending "
    "wide open, her gaze steady upward; panel 3 a thin banner of dust drifts across the opened "
    "path. Large bottom panel: Jesus inclines his head gently toward the woman in one small kind "
    "nod, then holds, his extended open hand steady at chest height; his lips stay closed and "
    "completely still — he is not speaking and his mouth does not move at all; the woman draws "
    "one slow deep breath, her shoulders easing down and settling as the fear leaves her, her "
    "open hands held still, her face lifted to his, eyes steady on him, lips closed and still; "
    "the watching crowd stirs gently in place, leaning slightly in toward the two of them; the "
    "soft blue threads and small bloom above his open hand drift gently within their own small "
    "area; the gold-and-blue halo curls rotate slowly around Jesus's head; every stain and mark "
    "in the paper — including the pale dried ring around where the woman kneels — is old, dry, "
    "and long set, staying exactly as drawn; no new stain, spot, or darkening appears anywhere "
    "on the page at any point."
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


def render_animation(mp4: Path, png: Path, prompt: str, model: str = "veo3_1_lite") -> None:
    if mp4.exists():
        print(f"  [skip] {mp4.name} already exists")
        return
    if not png.exists():
        print(f"  FAILED: still {png.name} not rendered yet.")
        return
    # Per-shot tiering (2026-08-20 v2): F04 -> kling3_0 pro (switch-models
    # rule after veo's failed attempt + the v2 prompt's completing gestures,
    # Kling's validated lane). F05 v2 -> kling3_0 pro too: its redesign
    # carries completing gestures (the nod, panel 2's full-arc blink) after
    # the veo all-holds clip failed on watch -- same rule, same lane.
    cmd = [HF_CLI, "generate", "create", model, "--prompt", prompt,
           "--start-image", str(png), "--aspect_ratio", "9:16"]
    if model == "kling3_0":
        cmd += ["--mode", "pro", "--duration", "5", "--sound", "off"]
    else:
        cmd += ["--duration", "4"]
    cmd += ["--wait"]
    print(f"  [{model}] rendering {mp4.name}...")
    if _run_hf(cmd, mp4, _VID_URL_RE, 900):
        print("  NOW: 4-frame contact sheet + real playback, both (QC law). FAIL if the "
              "stain/ring changes shape, size, or position at all.")


if __name__ == "__main__":
    if "--animate-f04" in sys.argv:
        render_animation(F04_MP4, F04_PNG, F04_ANIMATION_PROMPT, model="kling3_0")
    elif "--f05" in sys.argv:
        if not WOMAN_REF.exists():
            print(f"  FAILED: {WOMAN_REF.name} missing — crop the woman's figure from the "
                  f"F04 render and save it there first (ref-chaining rule: recurring subject "
                  f"with no chained ref is a hard stop).")
            sys.exit(1)
        render_still(F05_PNG, F05_STILL_PROMPT, [JESUS_REF, str(WOMAN_REF)])
    elif "--animate-f05" in sys.argv:
        render_animation(F05_MP4, F05_PNG, F05_ANIMATION_PROMPT, model="kling3_0")
    else:
        render_still(F04_PNG, F04_STILL_PROMPT, [JESUS_REF])
