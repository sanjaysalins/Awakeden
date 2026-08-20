"""North-star prompt lock — John 4 short-form, 8 shots x 2 aspect ratios.

HF CLI ONLY (no direct Gemini calls). Refs chained via --image on every shot
that needs them. Fable-authored prompts, verbatim from the 2026-08-19 session
(see ../../.claude/skills/swirls-of-life/NORTH_STAR_PROMPT.md).

Run a subset first (go/no-go): .venv\\Scripts\\python.exe render_northstar.py --shots 1,4 --ratios 9:16,16:9
Then the rest:                 .venv\\Scripts\\python.exe render_northstar.py --shots 2,3,5,6,7,8 --ratios 9:16,16:9
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
REFS_DIR = HERE.parent.parent / ".claude" / "skills" / "swirls-of-life" / "references"
JESUS_REF = str(REFS_DIR / "jesus_ref.png")
WOMAN_REF = str(REFS_DIR / "john4_woman_ref.png")
MODEL = "nano_banana_pro"
_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)

CONTINUITY_JESUS = (
    'Jesus (match the attached reference): a first-century Jewish man in his early '
    'thirties, lean from travel, weathered calm face, dark textured shoulder-length '
    'hair, short natural beard, drawn in broad confident economical ink strokes, '
    'loose layered robes of deep indigo and charcoal watercolor that pool and bloom '
    'and leave paper exposed, a faint incomplete calligraphic halo of muted '
    'gold-and-blue curls, never a solid disc.'
)
CONTINUITY_WOMAN = (
    'The Samaritan woman (match the attached reference): an ordinary first-century '
    'working woman with a strong distinctive face and expressive eyes, dark hair '
    'partly under a practical head covering, layered garments in burnt umber wash '
    'with muted olive-green and clay-red accents, drawn in dense cross-hatching and '
    'short dry-brush strokes.'
)
FOOTER = (
    'Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft '
    'gold wash on aged cream paper with visible grain. Not photorealistic, not anime, '
    'not Disney, no polished graphic design, no clean comic-book inking, no '
    'Renaissance religious staging, no glowing spiritual VFX — every blue or gold '
    'element behaves like literal wet ink bleeding into paper, never a magic-particle '
    'glow.'
)

SHOTS = [
    {
        "n": 1, "label": "wide_the_ask", "refs": ["jesus", "woman"], "stage": "0",
        "prompt": (
            'One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE WELL". Top-right frame number, handwrite: "F01". Across the top, a row of exactly three small labeled storyboard panels numbered 1, 2, 3: panel 1 a small establishing sketch of the old stone well standing alone in open country, panel 2 a study of the woman\'s round clay waterpot carried on her shoulder, panel 3 a quick sketch of Jesus\'s dusty travel-worn sandaled feet resting at the base of the well. Below them, ONE large full-scene illustration filling the lower half of the page — a WIDE shot: noon, hard flat overhead light, an old stone well in open country under a pale ochre sky; Jesus sits on the well\'s edge, travel-worn and still, while the Samaritan woman approaches on the dirt path carrying her waterpot and hesitates mid-step, seeing him — two strangers, real open distance kept between them across the frame. '
            + CONTINUITY_JESUS + ' ' + CONTINUITY_WOMAN +
            ' Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page — no loose blue threads, curls, or blue watercolor blooms; the only blue on the page belongs to Jesus himself, his indigo robes and the faint curls of his halo. Small handwritten production notes integrated naturally on the page: a caption beneath the main scene, handwrite: "Give me to drink", and a corner note, handwrite: "NOTE: noon, strangers". '
            + FOOTER
        ),
    },
    {
        "n": 2, "label": "medium_2shot_living_water", "refs": ["jesus", "woman"], "stage": "1",
        "prompt": (
            'One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE WELL". Top-right frame number, handwrite: "F02". Across the top, a row of exactly three small labeled storyboard panels numbered 1, 2, 3: panel 1 a small sketch of the clay waterpot now set down on the ground beside the woman\'s feet, panel 2 a view straight down the deep stone well shaft to dark water far below, panel 3 a study of the woman\'s skeptical face, one eyebrow raised, guarded. Below them, ONE large full-scene illustration filling the lower half of the page — a MEDIUM TWO-SHOT: the first real two-shot across the well, Jesus seated on the well\'s edge speaking with open unhurried hands, the Samaritan woman standing on the other side facing him, her waterpot set down on the ground — the first sign she is staying; noon light, dry open country behind them. '
            + CONTINUITY_JESUS + ' ' + CONTINUITY_WOMAN +
            ' Stage 1 dosage: exactly one restrained thread of blue ink curling up out of the dark mouth of the well between them, behaving like wet ink bleeding into the paper — nothing more, no other blue swirl anywhere on the page. Small handwritten production notes integrated naturally on the page: a caption beneath the main scene, handwrite: "living water", a second small caption, handwrite: "the well is deep", and a corner note, handwrite: "NOTE: she stays". '
            + FOOTER
        ),
    },
    {
        "n": 3, "label": "2shot_breaking_to_singles", "refs": ["jesus", "woman"], "stage": "1-2",
        "prompt": (
            'One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE WELL". Top-right frame number, handwrite: "F03". Across the top, a row of exactly three small labeled storyboard panels numbered 1, 2, 3: panel 1 a near-single sketch of Jesus mid-word, leaning slightly forward, calm and sure, panel 2 a near-single sketch of the woman leaning in across the well, skepticism turning into attention, panel 3 a small study of the still dark water surface far down the well shaft. Below them, ONE large full-scene illustration filling the lower half of the page — a TWO-SHOT breaking toward singles: the exchange across the well sharpens, the framing tighter than before, Jesus and the Samaritan woman each turned fully toward the other, the well mouth between them, her hand resting on the well\'s stone rim; hard noon light, the open country falling away soft and unfinished at the page edges. '
            + CONTINUITY_JESUS + ' ' + CONTINUITY_WOMAN +
            ' Stage 1 to 2 dosage: still one single restrained thread of blue ink rising from the well\'s mouth, now deepened — it puts out one small blue watercolor bloom where it meets the paper between the two figures, quiet and restrained, wet ink bleeding into the paper, nothing spectacular, no other blue anywhere on the page. Small handwritten production notes integrated naturally on the page: a caption beneath the main scene, handwrite: "shall never thirst", a second small caption, handwrite: "give me this water", and a corner note, handwrite: "NOTE: break to singles". '
            + FOOTER
        ),
    },
    {
        "n": 4, "label": "closeup_jesus_five_husbands", "refs": ["jesus", "woman"], "stage": "2",
        "prompt": (
            'One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE WELL". Top-right frame number, handwrite: "F04". Across the top, a row of exactly three small labeled storyboard panels numbered 1, 2, 3: panel 1 a small sketch of the Samaritan woman\'s guarded face, caught off guard — an alert widening of the eyes, a sharp realization, never shame, panel 2 a study of her hands gone still on the rope of her waterpot, panel 3 a small quiet sketch of the well mouth in flat midday light. Below them, ONE large full-scene illustration filling the lower half of the page — a CLOSE-UP: the first true close-up of the whole sequence, Jesus\'s face filling the frame, mid-speech, calm and direct and unaccusing, his gaze level with the viewer, nothing hidden and nothing withheld; soft warm midday light on his features. '
            + CONTINUITY_JESUS +
            ' The Samaritan woman in panel 1 (match the attached reference): an ordinary first-century working woman with a strong distinctive face and expressive eyes, dark hair partly under a practical head covering, drawn in dense cross-hatching and short dry-brush strokes. Stage 2 dosage: the blue ink motif is quietly present — a few soft blue threads and one small watercolor bloom curling near Jesus as he speaks, kept close to him in the main illustration only, wet ink bleeding into the paper, quiet and unspectacular, never filling the scene. Small handwritten production notes integrated naturally on the page: a caption beneath the main scene, handwrite: "Go, call thy husband", a second small caption, handwrite: "I have no husband", and a corner note, handwrite: "NOTE: nothing hidden". '
            + FOOTER
        ),
    },
    {
        "n": 5, "label": "compressed_2shot_spirit_truth", "refs": ["jesus", "woman"], "stage": "2",
        "prompt": (
            'One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE WELL". Top-right frame number, handwrite: "F05". Across the top, a row of exactly three small labeled storyboard panels numbered 1, 2, 3: panel 1 a small establishing sketch of the great mountain rising on the horizon, panel 2 a tiny far-off sketch of a temple silhouette on a distant hill, panel 3 a study of the woman\'s face open now, listening, her hatching drawn looser. Below them, ONE large full-scene illustration filling the lower half of the page — a COMPRESSED TWO-SHOT: Jesus and the Samaritan woman close together in one calm frame across the well, the argument gone out of their postures, she gesturing once toward the mountain on the horizon, he answering quietly, both settled; softening afternoon light, the mountain a pale wash behind them. '
            + CONTINUITY_JESUS +
            ' The Samaritan woman (match the attached reference): an ordinary first-century working woman with a strong distinctive face and expressive eyes, dark hair partly under a practical head covering, layered garments in burnt umber wash with muted olive-green and clay-red accents, drawn in dense cross-hatching and short dry-brush strokes, her cross-hatching drawn visibly looser now. Stage 2 dosage: the blue ink motif holds at exactly the same quiet dose as the previous frame — a few soft blue threads and one small watercolor bloom low in the scene between the two figures, wet ink bleeding into the paper, calmer than before, no escalation, never spectacular. Small handwritten production notes integrated naturally on the page: a caption beneath the main scene, handwrite: "in this mountain", a second small caption, handwrite: "the true worshippers", and a corner note, handwrite: "NOTE: hold calm". '
            + FOOTER
        ),
    },
    {
        "n": 6, "label": "held_single_jesus_i_am_he", "refs": ["jesus"], "stage": "2-3",
        "prompt": (
            'One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE WELL". Top-right frame number, handwrite: "F06". Across the top, a row of exactly three small labeled storyboard panels numbered 1, 2, 3: panel 1 a small study of Jesus\'s steady eyes, direct and kind, panel 2 a small study of his mouth mid-word, calm, unhurried, panel 3 a study of his open hand resting still on the well\'s stone rim. Below them, ONE large full-scene illustration filling the lower half of the page — a HELD SINGLE, Jesus only: Jesus close and still on the well\'s edge, speaking directly toward the viewer, no movement anywhere in the frame, complete stillness and complete plainness — the moment he says who he is; low warm afternoon light. '
            + CONTINUITY_JESUS +
            ' Stage 2 to 3 dosage: one single directed current of blue ink with a trace of muted gold moves from Jesus outward across the page toward the viewer\'s side of the frame — one deliberate swirl, drawn like wet ink pulled along the grain of the paper, not yet diffused, not filling the scene, no other blue anywhere on the page. Small handwritten production notes integrated naturally on the page: a caption in two short stacked lines beneath the main scene, handwrite: "I that speak", handwrite: "unto thee am he", and a corner note, handwrite: "NOTE: one swirl". '
            + FOOTER
        ),
    },
    {
        "n": 7, "label": "wide_moving_she_runs", "refs": ["woman"], "stage": "3-begin",
        "prompt": (
            'One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE WELL". Top-right frame number, handwrite: "F07". Across the top, a row of exactly three small labeled storyboard panels numbered 1, 2, 3: panel 1 a small sketch of the clay waterpot left abandoned on the well\'s edge, panel 2 a study of the woman\'s face mid-run, alight with urgent joy, panel 3 a small sketch of the town\'s flat rooftops and gate ahead on the road. Below them, ONE large full-scene illustration filling the lower half of the page — a WIDE MOVING shot: the Samaritan woman runs down the dirt path away from the well toward the distant town, her garments and head covering streaming with motion, the abandoned waterpot sitting alone on the well\'s edge behind her in the foreground; afternoon light long across the open country. '
            + CONTINUITY_WOMAN +
            ' her cross-hatching drawn visibly looser now, almost flying. Stage 3 beginning dosage: the blue ink motif begins to diffuse — blue threads with traces of muted gold trail from the well and the abandoned waterpot and bleed along the path after the running woman, like wet ink following spilled water across the paper, spreading now, no longer one single thread, but not yet filling the whole scene. Small handwritten production notes integrated naturally on the page: a caption beneath the main scene, handwrite: "Come, see a man", and a corner note, handwrite: "NOTE: pot left behind". '
            + FOOTER
        ),
    },
    {
        "n": 8, "label": "wide_landing_town_arrives", "refs": ["jesus", "woman"], "stage": "3",
        "prompt": (
            'One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE WELL". Top-right frame number, handwrite: "F08". Across the top, a row of exactly three small labeled storyboard panels numbered 1, 2, 3: panel 1 a loose sketchy crowd of townspeople streaming out through the town gate, panel 2 a small sketch of the woman among the crowd, turning back to lead them on, panel 3 a study of Jesus\'s open-handed welcome at the well. Below them, ONE large full-scene illustration filling the lower half of the page — a WIDE LANDING shot: the whole town arriving at the well, a loose sketchy crowd of Samaritan townspeople drawn in quick gestural ink strokes crossing the open country, the Samaritan woman among them near the front, and Jesus standing at the well receiving them with open unhurried arms; warm late-afternoon light over everything. '
            + CONTINUITY_JESUS + ' ' + CONTINUITY_WOMAN +
            ' The crowd stays loose and sketchy, faces suggested not detailed. Stage 3 dosage: the blue ink motif, with traces of muted gold, is fully diffused — delicate blue threads and small blue-and-gold watercolor blooms woven through the whole air of the scene, through the sky, the path, the crowd, and the well, tied to no single figure, all of it behaving like wet ink bled deep into the fibers of the paper. Small handwritten production notes integrated naturally on the page: a caption beneath the main scene, handwrite: "Saviour of the world", and a corner note, handwrite: "NOTE: swirl everywhere". '
            + FOOTER
        ),
    },
]


def render_one(shot: dict, ratio: str) -> dict:
    ratio_dir = HERE / ratio.replace(":", "x")
    ratio_dir.mkdir(parents=True, exist_ok=True)
    stem = f"shot{shot['n']:02d}_{shot['label']}"
    out_path = ratio_dir / f"{stem}.png"
    result = {"shot": shot["n"], "label": shot["label"], "ratio": ratio, "stem": stem,
              "ok": False, "error": None, "skipped": False}
    if out_path.exists():
        result["ok"] = True
        result["skipped"] = True
        print(f"  [skip] {ratio}/{stem}.png already exists")
        return result

    cmd = [HF_CLI, "generate", "create", MODEL, "--prompt", shot["prompt"]]
    if "jesus" in shot["refs"]:
        cmd += ["--image", JESUS_REF]
    if "woman" in shot["refs"]:
        cmd += ["--image", WOMAN_REF]
    cmd += ["--aspect_ratio", ratio, "--resolution", "2k", "--wait"]

    print(f"  [{MODEL}] {ratio}/{stem} (refs={shot['refs']})")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
    if proc.returncode != 0:
        result["error"] = f"hf CLI exit {proc.returncode}: {(proc.stderr or proc.stdout).strip()[-500:]}"
        print(f"        FAILED: {result['error']}")
        return result
    match = _URL_RE.search(proc.stdout)
    if not match:
        result["error"] = f"no image URL in stdout: {proc.stdout.strip()[-500:]}"
        print(f"        FAILED: {result['error']}")
        return result
    url = match.group(0)
    req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        out_path.write_bytes(resp.read())
    print(f"        -> {ratio_dir.name}/{out_path.name} ({out_path.stat().st_size:,} bytes)")
    result["ok"] = True
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", default="1,2,3,4,5,6,7,8", help="comma-separated shot numbers")
    ap.add_argument("--ratios", default="9:16,16:9", help="comma-separated aspect ratios")
    args = ap.parse_args()

    wanted = {int(x) for x in args.shots.split(",")}
    ratios = args.ratios.split(",")
    shots = [s for s in SHOTS if s["n"] in wanted]

    # Save the full prompt set once, for the record / the report.
    (HERE / "_prompts.json").write_text(
        json.dumps([{k: v for k, v in s.items()} for s in SHOTS], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    results_path = HERE / "results.json"
    results = json.loads(results_path.read_text(encoding="utf-8")) if results_path.exists() else []

    for shot in shots:
        for ratio in ratios:
            r = render_one(shot, ratio)
            results.append(r)
            results_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    n_ok = sum(1 for r in results if r["ok"])
    n_fail = sum(1 for r in results if not r["ok"])
    print(f"\nDone. {n_ok} ok, {n_fail} failed. See {results_path}")
