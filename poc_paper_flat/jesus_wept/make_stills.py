"""Jesus Wept paper-flat POC: render the 13 stills ONE AT A TIME (gentle) on Higgsfield nano_banana_2, 9:16.
Owner yes 2026-11-10 (~$8.50 incl. animation). Skips shots whose PNG already exists.
  .venv\\Scripts\\python.exe poc_paper_flat/jesus_wept/make_stills.py [s04,s01,...]"""
import subprocess, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"; OUT.mkdir(exist_ok=True)
REF = HERE / "style_refs"
HF = str(Path.home() / "bin" / "hf.exe")

STYLE = ("Flat textured paper illustration, the exact style of the reference image: simple flat shapes, visible paper grain and "
         "speckles, muted earthy palette (sand, ochre, olive, slate blue, terracotta, cream), soft natural light, gentle "
         "editorial storybook look, first-century Judea (Bethany near Jerusalem): plain linen and wool robes, simple head "
         "coverings, sandals, stone and mud-brick houses. Vertical 9:16, full bleed. NO text, NO letters, NO borders, NO panels.")
# 2026-11-10 owner fix round: ONE consistent Jesus from style_refs/jesus_ref.png, NO halo on anyone, no AI slop.
JR = REF / "jesus_ref.png"
JESUS = ("Jesus is EXACTLY the man in the character reference sheet: about 33, warm olive-brown skin, shoulder-length wavy dark "
         "brown hair, short neat dark brown beard with NO grey, cream linen tunic, light sand wool mantle over his shoulders "
         "(head uncovered), brown sash. Same face, same hair, same clothes, same size as the other adults. ")
NOHALO = ("Nobody has a halo, glow or ring of light. Every person has normal anatomy: two hands with five fingers, hands that do "
          "not merge into other people. Every face is different (different ages, noses, beards); no cloned faces. ")
SIS = ("Martha (older sister, about 35, dark hair with a little grey: olive-green dress, cream head scarf) and Mary (younger sister: slate-blue dress, light sand "
       "head scarf, dark hair) look exactly like the two women in the reference scene. ")

SHOTS = {
    "s04": ([REF / "ref_crowd.jpg"], "Inside a plain stone house, dim light from one small window. Mary, a young woman in a slate-blue dress and light sand head scarf, sits alone on a low bench, head bowed, hands in her lap. Her older sister Martha, in an olive-green dress and cream head scarf, leans close and whispers into her ear, one hand on her shoulder. Two mourners sit far back in shadow. Quiet, tender. No halo on anyone."),
    "s01": (["s04"], "Close shot inside a dim stone room: a woman in her forties sits alone on a low wooden bench, head bowed, eyes closed, hands folded in her lap. She wears a dark charcoal-brown dress and a plain grey head scarf (NOT blue, NOT green, NOT cream; she is not one of the sisters). A single beam of window light falls on the floor beside her, lots of empty quiet space around her. Only this one woman in the picture. Lonely, still. " + NOHALO),
    "s02": ([REF / "ref_crowd.jpg"], "Wide view of the village of Bethany on a dry hillside: small stone houses, an olive tree, and in the rock face a cave tomb sealed with a large flat stone. Small groups of mourners in robes and head coverings stand near the tomb with bowed heads. Late afternoon, muted, sad. No halo on anyone."),
    "s03": ([JR, "s04"], JESUS + SIS + "On a dusty road outside the village, ONLY Martha (the older sister in the olive-green dress) stands before Jesus, her hands open in grief, face pleading. Jesus listens gently, close to her. Two disciples in plain robes wait behind Him. Mary (the slate-blue dress) is NOT in this picture. Exactly one woman. " + NOHALO),
    "s05": ([JR, "s03", "s04"], JESUS + SIS + "OUTDOORS on the dusty road just outside the village (John 11:30), stone houses behind, open sky; NOT inside a house. Mary (slate-blue dress, light sand scarf) has fallen down at Jesus's feet: she is low on the ground, bowed forward, her forehead near His sandals, weeping, her hands on the ground by His feet. Jesus STANDS over her, looking down at her with deep sorrow and compassion, both hands open toward her but not touching her head. Behind them stand exactly three other people, each clearly different: Martha (ONE woman in olive-green and a cream scarf), a bearded man in a grey cloak, a young woman in a terracotta scarf. Only one Martha, only one Mary. All at realistic human scale. " + NOHALO),
    "s06": ([JR, "s02"], JESUS + "Wide shot of a rocky path up a dry hillside toward a cave tomb sealed with a large flat stone. In the middle of the picture, Jesus walks up the path at normal human size among a small group of mourners, His head bowed in sorrow. Just ahead, one mourner turns back toward Him and points up the path to the tomb, as if saying 'come and see'. Mary walks beside Jesus. Everyone is the same realistic scale; nobody is huge in the foreground. Exactly one Jesus. " + NOHALO),
    "s07": ([JR, "s04"], JESUS + "Close-up of Jesus's face and shoulders, drawn in the same storybook style as the reference scene (not a different art style). He is weeping quietly: eyes open and wet, one clear tear on His left cheek, mouth closed, deep love and sorrow, head slightly bowed. Soft blurred background of a stone village wall. Only Jesus. " + NOHALO),
    "s08": (["s04", "s02"], "Close group of five mourners in front of a stone house: an old man with a white beard, a young man with no beard, a middle-aged woman in a terracotta head scarf wiping her eyes, an old woman in a grey scarf, a teenage boy. The old man turns to the woman and says quietly 'Behold how he loved him', their faces moved and softened, all looking toward something off-screen to the right. None of them looks like Jesus: no man in cream robes with long wavy hair. Warm afternoon light. " + NOHALO),
    "s09": ([JR, "s02"], JESUS + "Low wide shot of a cave tomb in a rock hillside; the large flat stone has been pushed aside. Lazarus, a real living man, has just stepped out of the dark doorway, stumbling a little, unsteady: long strips of loose white linen are wound loosely around his body, arms and legs, some strips hanging and trailing on the ground, and a separate white cloth is tied over his face. He looks like a man, not a mummy. Jesus stands at the left, seen from behind and the side, one arm stretched toward the tomb. Mourners at the right stare, hands to their mouths. Exactly one Jesus, normal human scale. " + NOHALO),
    "s10": (["s02"], "A plain stone council room in Jerusalem, lit by two oil lamps on a stone shelf. Five older Jewish chief priests and Pharisees sit on stone benches talking in low worried voices: one heavy-set bald man with a grey beard, one thin man with a long white beard, one man with a short black beard, one with a red-brown beard, one very old man leaning on a staff. Long linen and wool robes in cream, blue and brown, simple wrapped turbans or prayer shawls. Serious, dignified, human faces, each clearly different. NOT villains: no hoods, no cowls, no sly or evil faces. " + NOHALO),
    "s11": ([REF / "ref_crowd.jpg"], "A bare rocky hill outside Jerusalem at dusk. One plain wooden Latin cross stands upright on the hilltop, the tall upright beam and short crossbeam clearly forming a Christian cross (a lowercase t), alone against an orange and slate-blue evening sky. No people, no bodies. Quiet, solemn."),
    "s12": ([REF / "ref_crowd.jpg"], "A garden tomb cut into rock at sunrise: the large round stone has been rolled away from the doorway, the tomb is open and empty, folded white linen cloths lie inside. Soft golden morning light pours into the doorway, olive trees and grass around. No people. Hopeful, peaceful."),
    "s13": ([JR, "s12"], JESUS + "Jesus alive and risen, standing in an olive garden at sunrise near the open tomb, facing the viewer from the waist up, a gentle warm smile, eyes open and kind, both hands relaxed at His sides. Soft golden morning light, olive trees behind. Same storybook style as the reference scene. Only Jesus. Leave calm space in the lower third of the picture. " + NOHALO),
}


def refs(lst):
    for r in lst:
        p = OUT / f"{r}.png" if isinstance(r, str) else r
        yield p


def make(key):
    out = OUT / f"{key}.png"
    if out.exists():
        print(key, "exists, skip"); return
    rl, body = SHOTS[key]
    cmd = [HF, "generate", "create", "nano_banana_2", "--prompt", STYLE + " " + body, "--aspect_ratio", "9:16", "--resolution", "2k"]
    for p in refs(rl):
        cmd += ["--image", str(p)]
    cmd += ["--wait", "--wait-timeout", "10m"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    url = [l for l in r.stdout.splitlines() if l.startswith("http")]
    if not url:
        print(key, "FAILED", r.stdout[-300:], r.stderr[-300:]); return
    urllib.request.urlretrieve(url[-1], out)
    (OUT / f"{key}.url").write_text(url[-1])
    print(key, "ok", flush=True)


if __name__ == "__main__":
    keys = sys.argv[1].split(",") if len(sys.argv) > 1 else list(SHOTS)
    for k in keys:
        make(k)
