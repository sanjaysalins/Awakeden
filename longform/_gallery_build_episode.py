"""Generalized Awakeden SHORT builder (gallery hard-cut engine) with WORLD + CAST +
REFERENCE-LOCK for cross-still consistency. Per episode: a World Bible (period+place,
lighting, no-modern/no-stray-bearded-men negatives) + a continuity CAST; one reference image
is generated per recurring character and ATTACHED (nano_banana_2 --image) to every scene
they appear in, so the same person/world holds across all stills. Then renders gallery clips,
reuses the Christ bank, and assembles (speed-to-fit racing middle + breathing living-Christ
close + dread->hope music + kinetic captions). Run:  _gallery_build_episode.py <EPISODE>"""
import sys, time, subprocess, importlib, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT/"longform"))
import config
from pipeline.visual_render import _HF_URL_RE
gs = importlib.import_module("_gallery_short")   # gallery_prompt + make_clip

STYLE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and Rembrandt lighting, "
    "fine visible brushwork, reverent sacred art")
TAIL = "no text, vertical 9:16 composition"

# ---- shared reuse bank ----
EW01 = ROOT/"longform/EW01_Two_Goats/v1/short"
PUNCH_CLIP = EW01/"gallery_clips/08_punch.mp4"
LIVING_CHRIST = EW01/"gallery_clips/living_christ.mp4"
CHRIST_LANDING = EW01/"visual_9x16_test/christ.png"   # reusable risen-Christ ref + still
BANK = ROOT/"longform/_shorts_bank"; BANK.mkdir(exist_ok=True)
GENERIC_CRUX = BANK/"crucifixion_generic.png"
GENERIC_CRUX_SUBJ = ("Christ crucified upon the cross at the moment of his death on a dark "
    "barren hill, broken light piercing behind him; head bowed beneath a crown of thorns, "
    "nail-pierced hands on the wooden beam; an upright cross, no other figures, no water, "
    "reverent and dignified")
CRUX_ELEMS = ["Christ's bowed face and crown of thorns","the nail-pierced hand","the wood of the cross"]

# ---- PREVENTION: Christ/crux scenes must not tour wound / nail-hand TIGHT crops ----
# Kling repaints a tight wound/nail-hand framing into a hallucination (a nail-pierced hand
# morphs into a SEVERED hand on the ground; a wrist wound sprouts a FLAME). Tour only safe
# anchors: face / cross / arms / composition. Caught on EW03 05_cross + 06_calls (2026-06-28).
import re as _re
_RISKY_CHRIST_ELEM = _re.compile(r"nail-pierced|nail-mark|\bnail\b|\bpierced\b|\bwound\b|\bflame\b", _re.I)
SAFE_CRUX_ANCHORS  = ["Christ's bowed face and crown of thorns","the upright wooden cross","the torn darkened sky"]
SAFE_RISEN_ANCHORS = ["the risen Christ's face","the extended open welcoming hand","the wide-open arms"]
def safe_christ_elements(elems, is_crux):
    """Drop wound/nail tight crops for Christ scenes; backfill safe anchors (>=3, <=4)."""
    kept = [e for e in elems if not _RISKY_CHRIST_ELEM.search(e)]
    for f in (SAFE_CRUX_ANCHORS if is_crux else SAFE_RISEN_ANCHORS):
        if len(kept) >= 3: break
        if f not in kept: kept.append(f)
    return kept[:4]

# ---- nano_banana_2 render with optional reference images ----
def hf_image(prompt, refs=()):
    cmd = [str(config.HF_CLI_PATH), "generate", "create", "nano_banana_2",
           "--prompt", prompt, "--aspect_ratio", "9:16", "--wait"]
    for r in refs: cmd += ["--image", str(r)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=600)
    m = _HF_URL_RE.search(res.stdout or "")
    if not m: raise RuntimeError(f"no image URL: {(res.stdout or res.stderr or '')[-400:]}")
    req = urllib.request.Request(m.group(0), headers={"User-Agent":"JITB/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp: return resp.read()

# ---- episode tables: world bible + continuity cast + paintings(with cast) ----
EPISODES = {
 "EW02_Abraham": {
  "world": {
   "period_place": ("Setting: the Patriarchal age, Middle Bronze Age Canaan and the stony hill "
      "country toward Moriah, about 2000 BC — black goat-hair tents, rocky scrubland, stony hill "
      "paths, a desert thicket; ancient and pre-Iron-Age"),
   "lighting": ("warm low chiaroscuro, deep shadow with a single dominant warm light per scene; "
      "muted ochre/umber/bone earth tones, consistent across every painting"),
   "negatives": ("STRICTLY no modern or anachronistic elements; no Greco-Roman/medieval/European "
      "objects, no metal armour, no eyeglasses. Abraham is the ONLY elderly grey-bearded man — do "
      "NOT add other old bearded men; background figures are younger and clearly Bronze-Age Semitic"),
  },
  "characters": {
   "abraham": ("ABRAHAM: an aged Semitic patriarch about one hundred years old, lean and upright, "
      "long flowing iron-grey beard, deeply lined sun-darkened face, deep-set sorrowful brown eyes, "
      "plain undyed coarse-wool robe and simple draped head-cloth"),
   "isaac": ("ISAAC: a strong Hebrew youth of about twenty, dark wavy hair and a short dark beard, "
      "smooth olive skin, plain undyed linen tunic"),
  },
  "paintings": [
   ("01_hook", ["abraham"], "Abraham (the man in the reference image) alone in a dim goat-hair tent at night, a clay lamp lighting his weathered face, cradling a sleeping swaddled infant against his chest, his other hand resting on a sheathed knife on a low table; a shaft of moonlight through the tent flap points to a dark distant mountain",
     ["Abraham's stricken face","the sleeping infant's face","Abraham's hand on the sheathed knife"], "fast"),
   ("02_wood", ["abraham","isaac"], "the youth Isaac (from the reference) bowed under a heavy bundle of split firewood on his shoulders, climbing a rocky path at dawn; Abraham (from the reference) a step behind carrying fire and a knife, head lowered in grief; two figures, vast hillside",
     ["the bundle of wood on Isaac's back","Isaac's young face","Abraham's grieving eyes"], "fast"),
   ("03_lamb", ["abraham","isaac"], "the youth Isaac (from the reference) turned back looking up into Abraham's face with a question; Abraham (from the reference) breaking with sorrow, one hand half-raised to heaven; warm side-light on both faces",
     ["Isaac's questioning upturned face","Abraham's anguished eyes","Abraham's hand raised to heaven"], "fast"),
   ("04_altar", ["abraham","isaac"], "the youth Isaac (from the reference) bound with rope on a rough stone altar of firewood, eyes trusting; Abraham (from the reference) over him with a knife raised in a trembling fist; a burst of golden light tears the sky with a radiant restraining hand",
     ["the raised knife at its peak","Abraham's trembling fist","Isaac's bound trusting face"], "fast"),
   ("05_ram", ["abraham","isaac"], "a single ram caught by its horns in a desert thicket, a thin line of blood at its flank, the dominant subject; behind it the youth Isaac (from the reference) embraced by Abraham (from the reference) in soft shadow",
     ["the ram's horns in the thicket","the ram's straining eye","the freed Isaac in Abraham's arms"], "fast"),
   ("06_waiting", ["abraham","isaac"], "Abraham (from the reference) descending a mountain at dusk, the youth Isaac (from the reference) walking ahead into the valley; Abraham pausing to look back up at the bare dark summit, one empty open hand at his side; amber dusk",
     ["Abraham's searching backward gaze","his empty open hand","the bare dark summit"], "fast"),
   ("07_turn", [], "CRUX", CRUX_ELEMS, "crux"),
   ("08_punch", [], "PUNCH", ["the risen Christ's living face","his extended open hand","the torn veil doorway light"], "punch"),
  ],
 },
 "EW03_Joseph": {
  "world": {
   "period_place": ("Setting: ancient biblical period across two worlds — the patriarchs' Canaan "
      "(a dry desert stone cistern, scrubland under a bruised sky) and the stone-columned court of "
      "Egypt; everything ancient and pre-modern"),
   "lighting": ("warm low chiaroscuro, deep shadow with a single dominant warm light per scene, "
      "muted ochre and umber earth tones, consistent across every painting"),
   "negatives": ("STRICTLY no modern or anachronistic elements; no European/medieval objects, no "
      "eyeglasses, no modern fabric; background figures are clearly ancient Near-Eastern or "
      "Egyptian; do not multiply identical old bearded men"),
  },
  "characters": {
   "joseph": ("JOSEPH: the SAME young Hebrew man of about twenty-five in every scene — dark hair, "
      "fine features, smooth olive skin, a short neat dark beard; his DRESS changes by scene (a "
      "plain undyed Canaanite robe when young, fine white Egyptian linen with a broad gold collar "
      "when he is the vizier) but it is always the same man's face"),
  },
  "ref_images": {"christ": str(CHRIST_LANDING)},
  "paintings": [
   ("01_pit", ["joseph"], "A young Hebrew man, Joseph (from the reference), thrown down into a dry desert stone cistern, his hands grasping the stone rim from below, his upturned betrayed face the one lit point; above him in warm low sun the hard shadowed silhouettes of his older brothers, one stretching a fist of silver coins toward an unseen merchant; deep negative space of empty pit-wall",
     ["Joseph's upturned betrayed face","his hands clutching the stone rim","the brother's fist of silver coins"], "fast"),
   ("02_bowing", ["joseph"], "The stone-columned throne hall of Egypt's governor; gaunt road-worn Hebrew brothers kneel low with faces to the floor holding out empty grain-sacks; above them on a dais a robed Egyptian ruler — Joseph (from the reference), now in fine white Egyptian linen and a broad gold collar — watches in silence, his face the only one turned toward us; one shaft of high window-light; attendants in shadow",
     ["the ruler Joseph's still watching face","a single kneeling brother's bowed head off to one side","the shaft of high window-light on the stone floor"], "fast"),
   ("03_descent", ["joseph"], "A single dark canvas of four soft-edged vignettes bleeding into one another, a descent then a climb: a hand spilling silver pieces; a falsely-accused man turning from a pointing accuser; a chained figure in a dungeon's barred shaft of light; and the same man Joseph (from the reference) risen, standing at the right hand of an enthroned Pharaoh with a signet ring on his finger; each vignette a memory-soft pool of light in darkness, no panels",
     ["the hand spilling the silver pieces","the chained hands in the dungeon light","the signet ring on Joseph's finger"], "fast"),
   ("04_betrayals", ["joseph","christ"], "One canvas, two soft-edged vignettes across a band of shadow: upper and smaller, young Joseph (from the reference) handed away as a clutch of silver coins changes hands; lower and larger, in a torch-lit olive garden, a robed disciple presses a kiss while a fist of silver coins glints, and Jesus (from the Christ reference) stands calm, sorrowful and bound at the centre light",
     ["Joseph's clutch of silver in the upper memory","the silver coins in the betrayer's fist","the betrayer's kiss against Jesus' cheek","Jesus' calm bound face"], "fast"),
   ("05_cross", ["christ"], "A darkened Golgotha at the ninth hour; an upright cross stands central against a torn blackened sky, the crucified Christ (from the Christ reference) with head bowed; a soldier's fallen iron nail and hammer in the foreground gloom; the earth opening below into deepest shadow, a low edge of dawn-grey light bleeding at the horizon; one dominant hero subject, vast negative sky",
     ["Christ's bowed head and face","the upright wooden cross","the torn black sky"], "crux"),
   ("06_calls", ["christ"], "REUSE_CHRIST",
     ["the risen Christ's face","the extended open welcoming hand","the wide-open arms"], "fast"),
   ("07_armswide", ["christ"], "The risen Christ (from the Christ reference) seen frontally, both arms thrown wide in an open embrace, no weapon anywhere, open empty hands showing the nail-marks, blood-tokened but glorified; a single ragged kneeling figure at the lower edge in shadow looking up; warm light pours from Christ over the kneeler; one dominant hero, deep negative space",
     ["Christ's open nail-marked hands","his face turned in welcome","the wide-thrown arms","the kneeling figure's upturned face"], "fast"),
   ("08_punch", [], "PUNCH", ["the risen Christ's living face","his extended open hand","the torn veil doorway light"], "punch"),
  ],
 },
}

EP = sys.argv[1] if len(sys.argv) > 1 else "EW02_Abraham"
spec = EPISODES[EP]; W = spec["world"]
SHORT = ROOT/"longform"/EP/"v1"/"short"
OUT = SHORT/"gallery_clips"; OUT.mkdir(exist_ok=True)
REFS = OUT/"_refs"; REFS.mkdir(exist_ok=True)
VO = SHORT/"narration.mp3"; SPOKEN = SHORT/"narration.spoken.txt"
ML = ROOT/"music_library/clips"; T = OUT/"_t"; T.mkdir(exist_ok=True)
NORM = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
def run(c): subprocess.run(c, check=True)
def dur(f):
    o = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of",
        "default=nk=1:nw=1",str(f)],capture_output=True,text=True).stdout.strip()
    return float(o) if o else 0.0

def scene_prompt(subject):
    return (f"{STYLE}. {W['period_place']}. {W['lighting']}. SCENE: {subject}. {W['negatives']}. {TAIL}")

# ---- 0a: shared generic crucifixion (bank) ----
if not GENERIC_CRUX.exists():
    print("[bank] generic crucifixion ...", flush=True)
    GENERIC_CRUX.write_bytes(hf_image(f"{STYLE}. {GENERIC_CRUX_SUBJ}. no modern elements. {TAIL}"))

# ---- 0b: one REFERENCE per recurring character (cached) ----
refp = {}
for name, desc in spec.get("characters", {}).items():     # generated references
    p = REFS/f"{name}.png"
    if not p.exists():
        print(f"[ref] {EP} {name} ...", flush=True)
        p.write_bytes(hf_image(f"{STYLE}. A single clear full-length character portrait. {desc}. "
            f"Standing in neutral warm light against a plain dark background, face clearly visible. "
            f"{W['negatives']}. {TAIL}"))
    refp[name] = p
for name, path in spec.get("ref_images", {}).items():     # existing references (e.g. christ)
    refp[name] = Path(path)

# ---- 1: render stills (world + attached refs) + gallery clips ----
clips = []
for slug, cast, subj, elems, kind in spec["paintings"]:
    if kind == "punch":
        clips.append((slug, PUNCH_CLIP, kind)); continue
    if subj == "CRUX":         png = GENERIC_CRUX           # shared generic cross
    elif subj == "REUSE_CHRIST": png = CHRIST_LANDING        # reuse the risen-Christ landing still
    else:
        png = OUT/f"{slug}.png"
        if not png.exists():
            print(f"[still] {EP} {slug} refs={cast} ...", flush=True)
            png.write_bytes(hf_image(scene_prompt(subj), [refp[c] for c in cast]))
    is_crux = (kind == "crux") or (subj == "CRUX")
    is_christ = is_crux or (subj == "REUSE_CHRIST") or ("christ" in cast)
    use_elems = safe_christ_elements(elems, is_crux) if is_christ else elems
    clip = OUT/f"{slug}.mp4"
    for _ in range(3):
        if gs.make_clip(png, use_elems, clip, 10) and clip.exists(): break
    if not clip.exists():
        print(f"[WARN] {slug} clip missing — skipped"); continue
    clips.append((slug, clip, kind))

# ---- 2: assemble (fast middle compressed, crux breathes, punch tour + living hold) ----
VOL = dur(VO); PUNCH_TOUR, LIVING_HOLD, CRUX_WIN = 6.0, 11.0, 10.0
LINGER = 2.5   # hold the living Christ + music this long AFTER the last word, then cut
n_fast = sum(1 for _,_,k in clips if k == "fast")
fast_win = (VOL - PUNCH_TOUR - LIVING_HOLD - CRUX_WIN) / max(n_fast,1)
segfiles = []
for i,(slug, clip, kind) in enumerate(clips):
    o = T/f"s{i:02d}.mp4"
    if kind == "punch":
        run(["ffmpeg","-y","-loglevel","error","-t",f"{PUNCH_TOUR}","-i",str(clip),"-vf",NORM,"-an",
             "-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(o)]); segfiles.append(o)
        h = T/"hold.mp4"; ld = dur(LIVING_CHRIST)
        run(["ffmpeg","-y","-loglevel","error","-i",str(LIVING_CHRIST),"-vf",f"{NORM},setpts=PTS*{(LIVING_HOLD+LINGER)/ld:.5f}",
             "-an","-c:v","libx264","-pix_fmt","yuv420p","-r","30",str(h)]); segfiles.append(h)
    else:
        win = CRUX_WIN if kind == "crux" else fast_win
        src = min(10.0, dur(clip))
        run(["ffmpeg","-y","-loglevel","error","-t",f"{src}","-i",str(clip),
             "-vf",f"{NORM},setpts=PTS*{win/src:.5f}","-an","-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(o)])
        segfiles.append(o)
lf = T/"list.txt"; lf.write_text("".join(f"file '{f.as_posix()}'\n" for f in segfiles),encoding="utf-8")
silent = T/"silent.mp4"; run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(lf),"-c","copy",str(silent)])
print(f"video {dur(silent):.1f}s  vo {VOL:.1f}s")

run(["ffmpeg","-y","-loglevel","error","-i",str(ML/"lonely_searching_a.mp3"),"-i",str(ML/"sacred_grace_rise_a.mp3"),
     "-filter_complex","[0:a][1:a]acrossfade=d=3:c1=tri:c2=tri[arc]","-map","[arc]",str(T/"arc.mp3")])
bed = T/"bed.mp3"; run(["ffmpeg","-y","-loglevel","error","-stream_loop","-1","-i",str(T/"arc.mp3"),"-t",f"{VOL+LINGER+1:.2f}","-c","copy",str(bed)])
muxed = OUT/f"{EP}_short_nocap.mp4"
run(["ffmpeg","-y","-loglevel","error","-i",str(silent),"-i",str(VO),"-i",str(bed),
     "-filter_complex",
     f"[1:a]volume=1.0[vo];[2:a]volume=0.18[mu];[vo][mu]amix=inputs=2:duration=longest[mix];"
     f"[mix]afade=t=out:st={VOL:.2f}:d={LINGER:.2f}[a]",   # music tapers over the linger, then cut
     "-map","0:v","-map","[a]","-t",f"{VOL+LINGER:.2f}","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac",str(muxed)])
out = OUT/f"{EP}_short.mp4"
print("[caption] impact ...")
r = subprocess.run([str(ROOT/".venv/Scripts/python.exe"),"-m","veed_io.caption","--video",str(muxed),
     "--script",str(SPOKEN),"--style","impact","--out",str(out)],cwd=str(ROOT),capture_output=True,text=True)
print(r.stdout[-150:] if r.returncode==0 else "CAPTION FAIL:\n"+r.stderr[-300:])
print(f"\nDONE -> {out if out.exists() else muxed}")
