"""Zacchaeus scratchy-ink test stills (owner yes 2026-11-10, quoted 4 x 2 credits ~USD 0.40). One at a time (gentle).
Style refs = the owner's own Google Flow pictures. Skips stills that exist.
  .venv\\Scripts\python.exe poc_scratchy_ink/zacchaeus/make_stills.py [t1,t2,...]"""
import subprocess, sys, urllib.request
from pathlib import Path
HERE = Path(__file__).resolve().parent; OUT = HERE/"stills"; OUT.mkdir(exist_ok=True)
REF = HERE/"style_refs"; HF = str(Path.home()/"bin"/"hf.exe")
R1, R2, R3 = REF/"owner_flow_teaching_crowd.jpg", REF/"owner_flow_teaching_water.jpg", REF/"owner_flow_lazarus.jpg"
STYLE = ("Hand-drawn comic illustration in the exact style of the reference images: bold scratchy black ink lines, loose cross-hatching, "
         "flat mustard-yellow sky, grungy texture and black ink spatter, muted earthy robes (teal, olive, rust, sand, slate). "
         "First-century Judea, Jericho: palm trees, mud-brick and stone houses, dusty road. Vertical 9:16, full bleed. "
         "NO text, NO letters, NO signature, NO speech bubbles, NO panels, NO border. ")
JESUS = ("Jesus is EXACTLY the man in the reference images: about 33, long wavy dark-brown hair, full dark beard, deep RED mantle over an "
         "olive-green tunic, brown sash, sandals. His face is warm, kind and earnest, never angry. ")
ZAC = ("Zacchaeus: a short middle-aged man, neat greying black beard, fine deep-teal robe with a thin gold trim, a rich wine-coloured "
       "head wrap, a leather coin purse at his belt. A real person, drawn with dignity, not a joke. ")
NOHALO = "Nobody has a halo or glow. Normal anatomy: two hands with five fingers each. Every face in the crowd is different; no cloned faces. "
SHOTS = {
 "t1": ([R1, R2], "Character sheet of Jesus on a plain mustard-yellow ground: one full-body front view and one full-body three-quarter view side by side, "
        "plus a head-and-shoulders close-up above them. " + JESUS + "Only Jesus, three times, same face and clothes. " + NOHALO),
 "t2": ([R1, R3], "A big leafy sycamore-fig tree on a Jericho street. " + ZAC + "He sits up on a thick low branch, peering down through broad leaves, "
        "holding the branch with both hands, eager to see. Below, the top of a dense crowd of heads and head-cloths fills the bottom of the picture. " + NOHALO),
 "t3": (["t1", "t2", R1], "Close, low camera at the foot of the sycamore-fig tree, looking UP the trunk. In the lower half, Jesus is seen from the FRONT, chest and head large in frame, face fully visible, tilted up toward the branch. " + JESUS + "He smiles warmly and calls, one open hand raised toward the branch. In the upper half, on a branch among broad leaves, " + ZAC + "leans down looking straight at Jesus in total surprise, eyes wide, mouth open. Their eyes meet. Only these two people are in the picture. " + NOHALO),
 "t4": (["t1", "t2", R2], "Street in Jericho. " + JESUS + "walks calmly beside " + ZAC + "toward the open wooden door of a large house. In the foreground, "
        "the crowd frowns and mutters: an old man shaking his head, a woman whispering behind her hand, two men with crossed arms, a teenage boy pointing. "
        "Big expressive cartoon eyes. Nobody is a villain; they are ordinary people grumbling. " + NOHALO),
}
FARMER = ("A poor, thin farmer in a patched sand-coloured tunic and a faded slate head-cloth, sun-lined face, grey stubble. ")
ONEZ = "Exactly ONE Zacchaeus in the picture. "
ONEJ = "Exactly ONE Jesus in the picture. "
SHOTS.update({
 "s01": (["t2", R1], "Wide shot on a Jericho street. " + ZAC + "is halfway up the trunk of a big leafy sycamore-fig tree, climbing fast, one foot on a knot, "
        "reaching for the low branch, eager, his fine robe hitched up. Behind and below, the backs of a dense crowd fill the road. " + ONEZ + NOHALO),
 "s02": (["t2", R1], "A tax table under a cloth awning at a Jericho town gate: scales, stacks of coins, a wax tablet. " + ZAC + "sits behind the table "
        "counting coins into his purse, calm and cold. Across the table, " + FARMER + "hands over his last coins, unhappy, head bowed. "
        "Only these two people. " + ONEZ + NOHALO),
 "s03": (["t2", R2], "Street in Jericho, low camera. " + ZAC + "stands on tiptoe at the back of the crowd, straining to see over a wall of tall backs, "
        "shoulders and head-cloths that block his view completely. We see his frustrated, eager face from the side. " + ONEZ + NOHALO),
 "s06": (["t2", R1], "Close to the sycamore-fig trunk. " + ZAC + "scrambles down from the low branch, dropping toward the road, beaming with joy, "
        "head wrap slipping, robe flapping. " + ONEZ + "No other figure. " + NOHALO),
 "s08": (["t1", "t2", R2], "Inside a fine Jericho house, warm lamp light, a low table with bread, figs, olives and a cup. " + JESUS + "reclines at the table, "
        "relaxed and smiling, as host and guest. Across from him, " + ZAC + "pours wine for him, shy and amazed. Only these two people. " + ONEJ + ONEZ + NOHALO),
 "s09": (["t1", "t2", R2], "Same lamp-lit room in a fine Jericho house. " + ZAC + "stands up from the table, one hand on his heart, the other holding out his "
        "open leather coin purse. His face is earnest and changed. Seated at the table, " + JESUS + "looks up at him, listening. "
        "Only these two people. " + ONEJ + ONEZ + NOHALO),
 "s10": (["s02", "t2", R1], "A Jericho street in daylight. " + ZAC + "presses a big handful of coins into the cupped hands of " + FARMER +
        "The farmer is the SAME man as in the reference picture of the tax table. The farmer stares, astonished; Zacchaeus is humble. "
        "Only these two people. " + ONEZ + NOHALO),
 "s11": (["t1", "t2", R1], "The open wooden doorway of a large Jericho house. " + JESUS + "stands in the doorway, one hand resting on the shoulder of " + ZAC +
        ", speaking warmly to him. Zacchaeus looks up at Jesus, overwhelmed. Only these two people. " + ONEJ + ONEZ + NOHALO),
 "s12": (["t2", R2], "Close-up portrait of " + ZAC + "His eyes are wet with tears of joy, a small trembling smile, warm lamp light on his face. "
        "Plain dark background. " + ONEZ + NOHALO),
 "s13": (["t1", R1], "Close portrait, head and shoulders, of " + JESUS + "He is speaking, looking just past the camera, kind and earnest, "
        "soft evening light. Plain mustard-yellow background. " + ONEJ + NOHALO),
 "s14": (["t2", R1], "The big leafy sycamore-fig tree on the empty Jericho road at sunset, long shadows, warm orange sky over the mustard-yellow. "
        "No people at all. The branch where a man sat is empty. " + NOHALO),
 "s15": ([R1, R3], "Early morning outside a rock-cut tomb in a garden near Jerusalem. The large round stone is rolled away from the dark, empty opening. "
        "First sunrise light on the rock, olive trees. No people at all. No glow from the tomb. " + NOHALO),
})

# Redraw round 1 (proposed 2026-11-11; t2 ref dropped where it forced the "sitting" pose; s12 = Zacchaeus face ref)
SHOTS.update({
 "s01b": (["s12", R1], "Side view of a big sycamore-fig tree trunk on a Jericho street. " + ZAC + "is CLIMBING: both arms hugging the trunk, one knee "
        "pushed up against it, one sandal on a knot, body vertical against the bark, face straining upward. His feet are off the ground; "
        "he is NOT sitting on any branch. Crowd heads small in the far background. " + ONEZ + NOHALO),
 "s03b": (["s12", R2], "Camera low, BEHIND Zacchaeus, looking over his shoulder. " + ZAC + "is small in the lower middle of the picture, seen from behind "
        "and slightly from the side, up on tiptoe, heels lifted. In front of him a solid wall of the BACKS of tall men in head-cloths towers "
        "over him and blocks the whole view; we see only their backs and shoulders, no faces. " + ONEZ + NOHALO),
 "s06b": (["s12", R1], "Close to the sycamore-fig trunk. " + ZAC + "is in mid-air, JUMPING DOWN from the low branch to the road, knees bent, arms out "
        "for balance, robe flying up, head wrap slipping, laughing with joy. Both feet are off the branch and off the ground. " + ONEZ + "No other figure. " + NOHALO),
 "s14b": ([R1], "A big leafy sycamore-fig tree beside an empty dusty Jericho road at sunset, long shadows, warm orange glow over the mustard-yellow sky, "
        "mud-brick houses and palms in the distance. The tree is EMPTY: no person, no figure, no clothing, no shape on any branch. "
        "Nobody anywhere in the picture. " + NOHALO),
})

# Consistency round (owner yes 2026-11-11): one tree (t2's sycamore-fig) + one room (s08's)
TREE = ("The tree is EXACTLY the sycamore-fig tree from the reference that shows the tree: same broad lobed fig leaves, same pale "
        "grey-brown trunk and branch shapes. ")
SHOTS.update({
 "s01c": (["s01b", "t2", "s12"], "Redraw the FIRST reference picture: same climbing pose, same framing, same street and crowd. " + ZAC +
        "is CLIMBING the trunk, arms hugging it, one sandal on a knot, NOT sitting. " + TREE + "Only change the tree to match. " + ONEZ + NOHALO),
 "s14c": (["s14b", "t2"], "Redraw the FIRST reference picture: same empty road at sunset, same framing and light. " + TREE +
        "The tree is EMPTY: no person, no figure, no clothing on any branch. Nobody anywhere in the picture. " + NOHALO),
 "s09b": (["s08", "s09", "t1"], "The SAME lamp-lit room as the FIRST reference: same window, same plaster wall, same low table with bread, figs and olives. "
        "Jesus still reclines at the low table exactly as in the first reference, looking up at Zacchaeus, listening. " + JESUS +
        "Zacchaeus now STANDS beside the table, one hand on his heart, the other holding out his open leather coin purse, earnest. " + ZAC +
        "Only these two people. " + ONEJ + ONEZ + NOHALO),
})

SHOTS.update({
 "s14d": (["t2", R1], "Redraw the SAME sycamore-fig tree and street as the reference: same broad lobed fig leaves, same trunk and the same low "
        "branch, same houses and palms. But now it is SUNSET: warm orange glow low in the sky, long shadows across the dusty road. "
        "The man is GONE. The crowd is GONE. The low branch is EMPTY. No person, no figure, no clothing, no sandals anywhere in the picture. " + NOHALO),
})
def refs(lst):
    for r in lst: yield OUT/f"{r}.png" if isinstance(r, str) else r
def make(k):
    out = OUT/f"{k}.png"
    if out.exists(): print(k, "exists"); return
    rl, body = SHOTS[k]
    cmd = [HF, "generate", "create", "nano_banana_2", "--prompt", STYLE + body, "--aspect_ratio", "9:16", "--resolution", "2k"]
    for p in refs(rl): cmd += ["--image", str(p)]
    cmd += ["--wait", "--wait-timeout", "10m"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    url = [l for l in r.stdout.splitlines() if l.startswith("http")]
    if not url: print(k, "FAILED", r.stdout[-300:], r.stderr[-300:]); return
    urllib.request.urlretrieve(url[-1], out); (OUT/f"{k}.url").write_text(url[-1]); print(k, "ok", flush=True)
if __name__ == "__main__":
    for k in (sys.argv[1].split(",") if len(sys.argv) > 1 else list(SHOTS)): make(k)
