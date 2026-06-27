"""Generalized Awakeden SHORT builder (gallery hard-cut engine). Renders an episode's NEW
stills + gallery clips, reuses the shared Christ bank (risen-Christ landing + living close +
generic crucifixion), and assembles: speed-to-fit racing middle + breathing living-Christ
close + dread->hope music + kinetic captions. Run:  _gallery_build_episode.py <EPISODE>"""
import sys, time, subprocess, importlib
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT/"longform"))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render
gs = importlib.import_module("_gallery_short")   # gallery_prompt + make_clip

config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
    "Rembrandt lighting, deep shadow and warm golden light, reverent sacred art, muted "
    "earth tones, fine visible brushwork")
config.VISUAL_STYLE_TAIL = "no text, no modern elements, vertical 9:16 composition"

# ---- shared reuse bank ----
EW01 = ROOT/"longform/EW01_Two_Goats/v1/short"
CHRIST_LANDING = EW01/"visual_9x16_test/christ.png"
PUNCH_CLIP = EW01/"gallery_clips/08_punch.mp4"
LIVING_CHRIST = EW01/"gallery_clips/living_christ.mp4"
BANK = ROOT/"longform/_shorts_bank"; BANK.mkdir(exist_ok=True)
GENERIC_CRUX = BANK/"crucifixion_generic.png"
GENERIC_CRUX_SUBJ = ("Christ crucified upon the cross at the moment of his death on a dark "
    "barren hill, the sky darkened with a shaft of broken light piercing behind him; his "
    "head bowed beneath a crown of thorns, his nail-pierced hands outstretched on the wooden "
    "beam, a wound in his side; an upright cross, no other figures, no water, reverent and "
    "dignified, deep shadow")
CRUX_ELEMS = ["Christ's bowed face and crown of thorns","the nail-pierced hand","the wood of the cross","the wound in his side"]

# ---- episode painting tables: (slug, subject_core | "CRUX" | "PUNCH", [elements], kind) ----
EPISODES = {
 "EW02_Abraham": [
  ("01_hook", "An aged shepherd-patriarch alone in a dim tent at night, a clay lamp throwing warm light across his weathered face; one hand cradling a sleeping infant boy against his chest, the other resting on a sheathed sacrificial knife on a low table; a shaft of cold moonlight through the tent flap points toward a dark distant mountain; one dominant figure, deep negative space",
    ["Abraham's stricken weathered face","the sleeping infant's face","Abraham's hand on the sheathed knife","the dark mountain through the tent flap"], "fast"),
  ("02_wood", "A young man bowed under a heavy bundle of split firewood lashed across his shoulders, climbing a rocky mountain path at dawn; his aged father a step behind carrying fire and a knife, head lowered in grief; two figures only, vast empty hillside, the boy's burden the bright focal mass",
    ["the bundle of wood on Isaac's back","Isaac's straining young face","Abraham's grieving lowered eyes","the knife and fire-pot in Abraham's hand"], "fast"),
  ("03_lamb", "Father and son paused on the mountain path, the boy turned back looking up into his father's face, lips parted in a question; the old man's face breaking with sorrow, one hand half-raised toward heaven; warm low side-light on both faces, the slope falling into shadow",
    ["Isaac's questioning upturned face","Abraham's anguished eyes","Abraham's hand raised toward heaven","the empty path ahead vanishing into dark"], "fast"),
  ("04_altar", "A boy bound with rope lying upon a rough stone altar stacked with firewood, eyes open and trusting; his father standing over him with a knife raised high in a trembling fist; a sudden burst of golden light tearing the upper sky with an outstretched radiant hand of restraint within it, the knife caught at the top of its arc",
    ["the raised knife frozen at its peak","Abraham's trembling fist on the hilt","Isaac's bound trusting face","the radiant restraining hand in the torn light"], "fast"),
  ("05_ram", "A single ram caught fast by its curling horns in the dense branches of a desert thicket, struggling in a pool of warm light, a thin line of blood at its flank; behind it the empty altar and the freed boy embraced by his father in soft shadow; the ram the bright dominant subject",
    ["the ram's horns tangled in the thicket","the ram's straining eye","the wound at the ram's flank","the freed boy in his father's arms behind"], "fast"),
  ("06_waiting", "An old man descending a mountain at dusk, his rescued son walking ahead into the valley, the father pausing to look back up at the bare dark summit with a searching unfinished expression, one empty open hand at his side; long amber dusk light, deep negative sky",
    ["Abraham's searching backward gaze","his empty open hand","the bare dark summit behind","the son walking ahead into the valley"], "fast"),
  ("07_turn", "CRUX", CRUX_ELEMS, "crux"),
  ("08_punch", "PUNCH", ["the risen Christ's living face","his extended open hand","the torn veil doorway light","the pierced wrist"], "punch"),
 ],
}

EP = sys.argv[1] if len(sys.argv) > 1 else "EW02_Abraham"
paintings = EPISODES[EP]
SHORT = ROOT/"longform"/EP/"v1"/"short"
OUT = SHORT/"gallery_clips"; OUT.mkdir(exist_ok=True)
VO = SHORT/"narration.mp3"; SPOKEN = SHORT/"narration.spoken.txt"
ML = ROOT/"music_library/clips"; T = OUT/"_t"; T.mkdir(exist_ok=True)
NORM = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
def run(c): subprocess.run(c, check=True)
def dur(f):
    o = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nk=1:nw=1",str(f)],capture_output=True,text=True).stdout.strip()
    return float(o) if o else 0.0

# ---- 0: shared generic crucifixion (render once into the bank) ----
if not GENERIC_CRUX.exists():
    sc = Scene(index=0, slug="crux", title="crucifixion", scene_type="single", arc_position="turn",
        framing="wide", purpose="generic cross", rationale="bank", visible_elements="Christ on the cross",
        emotional_tone="grief, awe", subject_block=GENERIC_CRUX_SUBJ, mood_block="reverent, period, vertical", jesus_variant=None)
    print("[bank] generic crucifixion ...", flush=True)
    GENERIC_CRUX.write_bytes(visual_render.HFProvider().generate(sc))

# ---- 1: render NEW stills + clips ----
prov = visual_render.HFProvider()
clips = []   # (slug, clip_path, kind)
for slug, subj, elems, kind in paintings:
    if kind == "punch":
        clips.append((slug, PUNCH_CLIP, kind)); continue   # reuse landing clip
    png = OUT/f"{slug}.png"
    if subj == "CRUX":
        png = GENERIC_CRUX
    elif not png.exists():
        sc = Scene(index=0, slug=slug, title=slug, scene_type="single", arc_position="body",
            framing="medium", purpose=slug, rationale="ep", visible_elements=subj[:160],
            emotional_tone="reverent", subject_block=subj, mood_block="reverent, period, vertical", jesus_variant=None)
        print(f"[still] {EP} {slug} ...", flush=True); png.write_bytes(prov.generate(sc))
    clip = OUT/f"{slug}.mp4"
    for _attempt in range(3):                       # retry transient HF 502s
        if gs.make_clip(png, elems, clip, 10) and clip.exists():
            break
    if not clip.exists():
        print(f"[WARN] {slug} clip missing after retries — skipping from cut")
        continue
    clips.append((slug, clip, kind))

# ---- 2: assemble (fast middle compressed, crux breathes, punch tour + living hold) ----
VOL = dur(VO)
PUNCH_TOUR, LIVING_HOLD, CRUX_WIN = 6.0, 11.0, 10.0
n_fast = sum(1 for _,_,k in clips if k == "fast")
fast_win = (VOL - PUNCH_TOUR - LIVING_HOLD - CRUX_WIN) / n_fast
segfiles = []
for i,(slug, clip, kind) in enumerate(clips):
    o = T/f"s{i:02d}.mp4"
    if kind == "punch":
        run(["ffmpeg","-y","-loglevel","error","-t",f"{PUNCH_TOUR}","-i",str(clip),"-vf",NORM,"-an",
             "-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(o)]); segfiles.append(o)
        h = T/"hold.mp4"; ld = dur(LIVING_CHRIST)
        run(["ffmpeg","-y","-loglevel","error","-i",str(LIVING_CHRIST),"-vf",f"{NORM},setpts=PTS*{LIVING_HOLD/ld:.5f}",
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
bed = T/"bed.mp3"; run(["ffmpeg","-y","-loglevel","error","-stream_loop","-1","-i",str(T/"arc.mp3"),"-t",f"{VOL+1:.2f}","-c","copy",str(bed)])
muxed = OUT/f"{EP}_short_nocap.mp4"
run(["ffmpeg","-y","-loglevel","error","-i",str(silent),"-i",str(VO),"-i",str(bed),
     "-filter_complex","[1:a]volume=1.0[vo];[2:a]volume=0.18[mu];[vo][mu]amix=inputs=2:duration=first[a]",
     "-map","0:v","-map","[a]","-t",f"{VOL:.2f}","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac",str(muxed)])
out = OUT/f"{EP}_short.mp4"
print("[caption] impact ...")
r = subprocess.run([str(ROOT/".venv/Scripts/python.exe"),"-m","veed_io.caption","--video",str(muxed),
     "--script",str(SPOKEN),"--style","impact","--out",str(out)],cwd=str(ROOT),capture_output=True,text=True)
print(r.stdout[-150:] if r.returncode==0 else "CAPTION FAIL:\n"+r.stderr[-300:])
print(f"\nDONE -> {out if out.exists() else muxed}")
