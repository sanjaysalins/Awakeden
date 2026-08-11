"""POC -- 2 sketchbook-style stills for "The Forsaken Cry" (Psalm 22:1 /
Matt 27:46), to pair with Noah's exact hand-ink caption treatment. Reuses
the proven living-sketchbook recipe verbatim (same STYLE constant, same
nano_banana_pro via hf CLI, same jesus_ref.png identity-lock anchor) from
poc_living_sketchbook/bronze_serpent/_s2_stills.py -- nothing invented, just
applied to this piece's own content instead of Bronze Serpent's.

Two scenes, matching two of the real beats in visual/livingpage_short.spec.json
(golgotha_hill_wide, bowed_head_finished) so the sketchbook art covers content
this piece's narration actually names:
  s_golgotha_sketchbook  -- wide, the three crosses on the hill
  s_bowedhead_sketchbook -- close, Jesus on the cross, the forsaken cry

  .venv\\Scripts\\python.exe batches/cluster_01_cross/forsaken_cry_ps221/_poc_sketchbook_stills.py
"""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "POC_ForsakenCry_Sketchbook"
HERE = Path(__file__).resolve().parent
JESUS_REF = ROOT / "poc_living_sketchbook" / "cast" / "jesus_ref.png"
OUT = HERE / "_poc_sketchbook_stills"
OUT.mkdir(parents=True, exist_ok=True)

JESUS = (
    "Jesus: a Judean man in his early thirties, long dark wavy hair past "
    "the shoulders parted center, short close-cropped dark beard, a "
    "strong straight nose and defined cheekbones, warm deep brown eyes "
    "level and calm, sun-weathered olive skin, lean wiry-strong build. "
    "the SAME man as the reference image -- identical face, beard, hair."
)

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge. CRITICAL: absolutely NO lettering, numerals, words, newsprint, "
    "printed book-page text, handwriting, ruler markings, dates, or captions "
    "ANYWHERE on ANY layer -- every paper surface is BLANK textured stock."
)

FULLBLEED = (
    "CRITICAL FRAMING: zoom in close enough that the illustrated subject "
    "and its immediate surroundings occupy the ENTIRE frame, corner to "
    "corner. No large empty cream-paper or kraft-paper region anywhere "
    "inside the frame."
)

SHOTS = [
    ("s_golgotha_sketchbook", "jesus",
     f"VAST WIDE view, low horizon: three crosses stand on a bare hill "
     f"outside a walled Near-Eastern city, the sky gone unnaturally dark "
     f"at midday, flat heavy stillness, not storm clouds. {JESUS} on the "
     f"center cross, arms outstretched, wound-free reverent restrained "
     f"silhouette, no visible wound or blood, head bowed. Two smaller "
     f"crosses flank Him at a respectful distance, their figures indistinct "
     f"silhouettes. A small group of mourners stands far below at the base "
     f"of the hill, no individual faces readable at this distance. "
     f"{FULLBLEED}"),
    ("s_bowedhead_sketchbook", "jesus",
     f"Close, reverent view on {JESUS}'s upper body and face as He hangs "
     f"upon the cross, head lifted toward the dark sky, mouth just open "
     f"as though crying out, an expression of anguish carried with dignity "
     f"-- wound-free, no visible blood, no graphic detail of any kind. "
     f"The crossbeam behind His outstretched arms, deep shadow surrounding "
     f"Him, only His face and upper chest caught in a narrow band of grim "
     f"light. {FULLBLEED}"),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for name, tag, scene in SHOTS:
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        refs = [JESUS_REF] if "jesus" in tag and JESUS_REF.exists() else []
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, refs)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[forsaken_cry_poc] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
