"""Zacchaeus clips: ONE AT A TIME (gentle), gemini_omni_flash_1_2 i2v 720p 9:16. Owner yes 2026-11-11 (~$10.45).
Owner rule: no freeze / boomerang / zoom fill -> each clip >= its slot (CLIP_PLAN.md), trimmed only. Skips existing.
  ..\..\.venv\Scripts\python.exe make_clips.py [c01,...]"""
import subprocess, sys, urllib.request
from pathlib import Path
HERE = Path(__file__).resolve().parent; ST = HERE/"stills"; OUT = HERE/"clips"; OUT.mkdir(exist_ok=True)
HF = str(Path.home()/"bin"/"hf.exe")
KEEP = ("Keep the exact image, the bold scratchy hand-inked comic style, colours, framing and every person exactly as drawn. "
        "The camera stays steady: no zoom, no push-in, no cuts. Nothing new appears. Nobody has a halo or glow. "
        "The light stays as warm and steady as it already is. Faces and hands stay the same. ")
CLIPS = {  # key: (still, seconds, motion)
 "c01": ("s01c", 6, "Zacchaeus pulls himself up the trunk, one hand reaching higher, his sandal pushing on the knot. Leaves sway. The small crowd below shifts and murmurs."),
 "c02": ("s02", 8, "The farmer slowly sets his last coins on the table one by one; Zacchaeus sweeps them into his purse without looking up. The awning cloth flutters a little."),
 "c03": ("s03b", 5, "Zacchaeus rises up on his toes and leans left, then right, trying to see past the men. The men in front stay shoulder to shoulder, still."),
 "c04": ("t2", 4, "Zacchaeus pushes a leaf aside and peers down eagerly. Leaves sway gently. The crowd below shifts."),
 "c05": ("t3", 7, "Jesus smiles and calls up, His raised hand beckoning once. Zacchaeus's eyes widen, he grips the branch, his mouth opening in surprise. Leaves sway."),
 "c06": ("s06b", 6, "Zacchaeus lands on the road on both feet, wobbles, laughs, and straightens his head wrap. Dust puffs softly at his feet."),
 "c07": ("t4", 8, "The crowd mutters: the old man shakes his head, the woman whispers behind her hand, the boy points. Jesus and Zacchaeus keep walking slowly toward the open door."),
 "c08": ("s08", 5, "Zacchaeus pours wine into the cup; Jesus smiles and gestures warmly as He talks. The lamp flames flicker softly."),
 "c09": ("s09b", 5, "Zacchaeus speaks earnestly, one hand on his heart, holding the cup out. Jesus, still reclining, listens and nods slowly. Lamp flames flicker."),
 "c10": ("s10", 7, "Zacchaeus pours coins into the farmer's cupped hands; the farmer looks at the coins, then up at Zacchaeus, astonished, and slowly smiles."),
 "c11": ("s11", 8, "Jesus speaks warmly, His hand resting on Zacchaeus's shoulder. Zacchaeus looks up at Him, his eyes fill with tears, and he smiles."),
 "c12": ("s13", 9, "Jesus speaks to us, His lips moving, His eyes kind and earnest. He breathes calmly; His hair stirs in a light breeze."),
 "c13": ("s14d", 6, "Leaves sway in a soft evening breeze; long shadows stir a little on the road. The tree stays empty; no person appears anywhere."),
 "c14": ("s15", 9, "Olive leaves sway gently in a morning breeze. The sunrise light rests steady on the rock. The tomb stays empty and still; no person appears."),
}
def make(k):
    out = OUT/f"{k}.mp4"
    if out.exists(): print(k, "exists"); return
    st, secs, motion = CLIPS[k]
    cmd = [HF, "generate", "create", "gemini_omni_flash_1_2", "--mode", "image-to-video", "--start-image", str(ST/f"{st}.png"),
           "--prompt", KEEP + motion, "--duration", str(secs), "--resolution", "720p", "--aspect_ratio", "9:16", "--wait", "--wait-timeout", "15m"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    url = [l for l in r.stdout.splitlines() if l.startswith("http")]
    if not url: print(k, "FAILED", r.stdout[-300:], r.stderr[-300:], flush=True); return
    urllib.request.urlretrieve(url[-1], out); (OUT/f"{k}.url").write_text(url[-1]); print(k, "ok", flush=True)
if __name__ == "__main__":
    for k in (sys.argv[1].split(",") if len(sys.argv) > 1 else list(CLIPS)): make(k)
