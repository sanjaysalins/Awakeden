"""Jesus Wept paper-flat POC: animate each approved still ONE AT A TIME (gentle) with gemini_omni_flash_1_2 image-to-video, 720p 9:16.
Owner yes 2026-11-10 (~$8.50 total incl. stills). Skips clips that already exist.
  .venv\\Scripts\\python.exe poc_paper_flat/jesus_wept/make_clips.py [s01,...]"""
import subprocess, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ST = HERE / "stills"; OUT = HERE / "clips"; OUT.mkdir(exist_ok=True)
HF = str(Path.home() / "bin" / "hf.exe")
KEEP = ("Keep the exact image, flat paper illustration style, colours, framing and every person exactly as drawn. "
        "Nothing new appears. Nobody has a halo or glow. The light stays as warm and steady as it already is. ")

CLIPS = {  # key: (seconds, motion)
    "s01": (6, "Very slow gentle push-in toward the woman. She breathes slowly, her shoulders rise and fall once, a few dust motes drift in the window light. She stays seated, head bowed, alone."),
    "s02": (6, "Very slow drift across the village toward the tomb. The olive leaves sway a little in a light breeze, the mourners shift their weight quietly. Nobody walks away."),
    "s03": (4, "Gentle slow push-in. Martha speaks with open pleading hands, her lips move; Jesus listens, His head tilting slightly toward her. The disciples stay still."),
    "s04": (6, "Slow gentle push-in. Martha leans closer and whispers into Mary's ear; Mary slowly lifts her head and opens her eyes. The others stay still in the shadow."),
    "s05": (6, "Slow gentle push-in. Mary stays low at Jesus's feet, weeping, her shoulders shaking softly; Jesus stays standing and slowly bends His head lower toward her in sorrow, His open hand still. The three people behind stand still, sad. Nobody new appears."),
    "_old05": (6, "Slow gentle push-in. Mary weeps at Jesus's feet, her shoulders shaking softly; Jesus bends a little lower toward her, His hand reaching out to her. The mourners behind wipe their eyes."),
    "s06": (6, "Slow gentle camera drift up the hillside path. The small group walks slowly toward the tomb; the man in front turns and points up the path to the tomb; Jesus walks slowly with His head bowed. Everyone keeps their size."),
    "_old06": (6, "Slow gentle camera drift up the path toward the tomb. The man in front turns and gestures toward the tomb; the mourners walk slowly forward; Jesus walks slowly, His face heavy with sorrow."),
    "s07": (4, "Very slow push-in on His face. A single tear slowly rolls down His cheek; His eyes blink once, slowly; lips tremble slightly. Deep, quiet sorrow."),
    "s08": (4, "Slow gentle push-in. The older man turns and speaks quietly to the man beside him; the woman wipes her eye with her scarf; the others watch, moved."),
    "s09": (4, "Slow gentle push-in toward the tomb. Lazarus takes one unsteady step forward, the loose linen strips trailing and swaying; the mourners lean back in amazement, hands to their mouths; Jesus keeps His arm stretched toward him."),
    "_old09": (4, "Slow gentle push-in toward the tomb doorway. Lazarus, wrapped in grave cloths, takes one small slow step forward out of the dark doorway; the mourners lean back in amazement; Jesus keeps His arm raised."),
    "s10": (4, "Slow gentle drift. The seated leaders talk in low voices; one leans toward another; the small oil lamp flame flickers softly. Nobody stands up."),
    "s11": (4, "Very slow push-in toward the cross on the hilltop. Thin clouds drift slowly across the evening sky. The cross stays exactly the same shape, upright and still."),
    "s12": (4, "Very slow push-in toward the open, empty tomb. Morning light slowly brightens inside the doorway, grass and olive leaves sway gently in a breeze. The tomb stays empty."),
    "s13": (6, "Very slow gentle push-in toward Jesus's face. He looks at the viewer, His warm smile grows a little, He breathes calmly. Olive leaves sway softly and morning light glows behind Him."),
    "_old13": (6, "Very slow gentle push-in. Jesus looks at the viewer, His warm smile grows a little, He breathes calmly, His raised hand stays still. Olive leaves sway softly behind Him."),
}


def make(key):
    out = OUT / f"{key}.mp4"
    if out.exists():
        print(key, "exists, skip"); return
    secs, motion = CLIPS[key]
    cmd = [HF, "generate", "create", "gemini_omni_flash_1_2", "--mode", "image-to-video", "--start-image", str(ST / f"{key}.png"),
           "--prompt", KEEP + motion, "--duration", str(secs), "--resolution", "720p", "--aspect_ratio", "9:16",
           "--wait", "--wait-timeout", "15m"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    url = [l for l in r.stdout.splitlines() if l.startswith("http")]
    if not url:
        print(key, "FAILED", r.stdout[-300:], r.stderr[-300:], flush=True); return
    urllib.request.urlretrieve(url[-1], out)
    (OUT / f"{key}.url").write_text(url[-1])
    print(key, "ok", flush=True)


if __name__ == "__main__":
    for k in (sys.argv[1].split(",") if len(sys.argv) > 1 else [c for c in CLIPS if not c.startswith("_")]):
        make(k)
