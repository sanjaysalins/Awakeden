r"""build_uplift.py (uplift T8): the comic-uplift chain for ONE piece. $0: ffmpeg + Remotion only.

  engine  -> the livingpage engine builds seg_NN.mp4 from <pool>/livingpage_short.uplift.spec.json (--no-sfx)
  join    -> segs back to back -> base video (silent), staged into _remotion/public/uplift/<slug>/
  remotion-> UpliftFilm: page turns + hand marks on top of the base (and a marks-only render for the gates)
  cards   -> hook + decode cards by ffmpeg drawtext (same recipe + numbers as the shipped film)
  mux     -> video new, audio COPIED from the shipped final -> <slug>_uplift_v1.mp4

Never overwrites the shipped final, FINAL_VIDEO.txt, publish\ or any ledger. Writes only under <piece>\visual\uplift_v1\
and the one output mp4 name given in PIECES below.

  .venv\\Scripts\\python.exe poc_comic_page\\_ELEVATE\\uplift\\build_uplift.py woman-behold-thy-son [engine|join|remotion|cards|mux|all]
"""
import json, subprocess, sys, shutil
from pathlib import Path

ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
ENGINE = ROOT / "longform" / "02_Psalm_22_Song_From_The_Cross" / "build_livingpage_16x9.py"
PY = ROOT / ".venv" / "Scripts" / "python.exe"
REMOTION = ROOT / "_remotion"
FIX_DIR = ROOT / "poc_comic_page" / "_audit" / "fixes"

PIECES = {
    "woman-behold-thy-son": dict(
        folder=ROOT / "batches" / "cluster_01_cross" / "woman_behold_john1926",
        shipped="visual/woman_behold_john1926_sfx_v5hook.mp4",
        out="visual/woman_behold_john1926_uplift_v1.mp4"),
}
FONT = "C\\:/Windows/Fonts/impact.ttf"


def run(cmd, what, timeout=3600):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout)
    if r.returncode:
        raise RuntimeError(f"{what} failed:\n{(r.stderr or r.stdout)[-1500:]}")
    return r


def paths(slug):
    cfg = PIECES[slug]
    f = cfg["folder"]
    pool = f / "visual" / "uplift_v1"
    return dict(folder=f, pool=pool, work=pool / "_livingpage_work", shipped=f / cfg["shipped"], out=f / cfg["out"],
                spec=pool / "livingpage_short.uplift.spec.json", marks=pool / "uplift_marks.json",
                base=pool / "_uplift_base_silent.mp4", rem=pool / "_uplift_remotion.mp4",
                rem_marks=pool / "_uplift_marks_only.mp4", cards=pool / "_uplift_cards.mp4",
                pub=REMOTION / "public" / "uplift" / slug)


def stage_engine(slug):
    p = paths(slug)
    run([PY, ENGINE, "--pool", p["pool"], "--spec", p["spec"].name, "--page", "1080x1920", "--clips", "--no-sfx"],
        "engine", timeout=7200)


def stage_join(slug):
    p = paths(slug)
    spec = json.loads(p["spec"].read_text(encoding="utf-8"))
    n = len(spec["beats"])
    lst = p["work"] / "_uplift_concat.txt"
    lst.write_text("".join(f"file '{(p['work'] / f'seg_{i:02d}.mp4').as_posix()}'\n" for i in range(1, n + 1)), encoding="utf-8")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", p["base"]], "join")  # stream copy: no extra generation
    p["pub"].mkdir(parents=True, exist_ok=True)
    shutil.copy2(p["base"], p["pub"] / "base.mp4")


def stage_remotion(slug, marks_only=False):
    p = paths(slug)
    m = json.loads(p["marks"].read_text(encoding="utf-8"))
    nframes = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                                  "stream=nb_read_packets", "-of", "csv=p=0", str(p["base"])], capture_output=True, text=True).stdout.strip())
    film = {"film": {"src": f"uplift/{slug}/base.mp4", "frames": nframes, "turns": m["turns"], "marks": m["marks"]}, "marksOnly": marks_only}
    pj = p["pool"] / ("_film_props_marks.json" if marks_only else "_film_props.json")
    pj.write_text(json.dumps(film), encoding="utf-8")
    out = p["rem_marks"] if marks_only else p["rem"]
    r = subprocess.run(f'npx remotion render src/index.ts UpliftFilm "{out}" --props="{pj}" --muted --crf=10 --image-format=png --concurrency=2',
                       cwd=str(REMOTION), shell=True, capture_output=True, text=True, timeout=3600)
    if r.returncode:
        raise RuntimeError("remotion failed:\n" + (r.stderr or r.stdout)[-2000:])


def _dt(text, size, color, y, t0, t1, boxa=0.64, bw=20):
    return (f"drawtext=fontfile='{FONT}':text='{text}':fontsize={size}:fontcolor={color}:box=1:boxcolor=black@{boxa}:"
            f"boxborderw={bw}:x=(w-text_w)/2:y={y}:enable='between(t,{t0},{t1})'")


def stage_cards(slug):
    """compose: base (stream copy of the segs) + Remotion frames ONLY where a page turn or a mark is live + hook/decode cards,
    all in ONE encode. Frames with no turn/mark keep the base pixels (no Remotion generation), so unchanged beats stay close to the shipped film."""
    p = paths(slug)
    card = json.loads((FIX_DIR / f"{slug}.json").read_text(encoding="utf-8-sig"))
    m = json.loads(p["marks"].read_text(encoding="utf-8"))
    spans = [(t["at"], t["at"] + t["frames"] - 1) for t in m["turns"]] + [(k["at"], k.get("until", k["at"] + 30)) for k in m["marks"]]
    en = "+".join(f"between(n,{a},{b})" for a, b in spans)
    vf = []
    h = card["hook_text"].upper()
    words = h.split()
    # hook: 2 lines, white then gold (shipped film: y 170 / 320, Impact 104, black@0.64 box)
    l1, l2 = " ".join(words[:3]), " ".join(words[3:])
    vf.append(_dt(l1, 104, "white", 170, 0, 2.0))
    if l2:
        vf.append(_dt(l2, 104, "0xF2C14E", 320, 0, 2.0))
    for d in card["decode_cards"]:
        vf.append(_dt(d["old"], 110, "white", 170, d["t0"], d["t1"]))
        vf.append(_dt("= " + d["plain"], 120, "0xF2C14E", 320, d["t0"], d["t1"]))
    nfr = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets",
                              "-of", "csv=p=0", str(p["rem"])], capture_output=True, text=True).stdout.strip().strip(",").split(",")[0])
    fc = f"[0:v][1:v]overlay=0:0:enable='{en}'[o];[o]" + ",".join(vf) + "[v]"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", p["base"], "-i", p["rem"], "-filter_complex", fc, "-map", "[v]", "-frames:v", str(nfr), "-c:v", "libx264",
         "-crf", "12", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30", p["cards"]], "cards")


def stage_mux(slug):
    p = paths(slug)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", p["cards"], "-i", p["shipped"], "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", p["out"]], "mux")


if __name__ == "__main__":
    slug = sys.argv[1]
    stage = sys.argv[2] if len(sys.argv) > 2 else "all"
    order = ["engine", "join", "remotion", "cards", "mux"]
    for s in (order if stage == "all" else [stage]):
        print("[uplift]", s, flush=True)
        if s == "remotion":
            stage_remotion(slug, False)
            stage_remotion(slug, True)
        else:
            globals()["stage_" + s](slug)
    print("DONE", paths(slug)["out"])
