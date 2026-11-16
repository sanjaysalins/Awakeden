"""episode_mockers.json for the LOCKED Y4 words. PROVISIONAL timings (2.75 words/sec estimate).
Re-derive every time from alignment.json after the (separately approved) recording. Nothing rendered, nothing spent."""
import json, re
from pathlib import Path
D = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page")
Y4 = (D / "_words_mockers_r4" / "cand_Y7.md").read_text(encoding="utf-8").split("\n")
OUT = D / "_living_comic" / "episode_mockers.json"
WPS, PAUSE = 2.75, 0.35
import glob, subprocess
TD = "F:/slk/PycharmProjects/JesusInTheBible/batches/cluster_01_cross/mockers_words_ps227/audio_y4/_turns"
def _real(i):
    f = [str(x) for x in Path(TD).glob("%02d_*.mp3" % i)]; f = [x for x in f if "atempo" in x] or f
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",f[0]]).decode())
segs, t, prev = [], 0.0, None
Y4 = [l.strip() for l in Y4 if l.strip()]
for i, line in enumerate(Y4):
    m = re.match(r"\[(narrator|david|mocker)\] (.*)", line)
    sp, txt = m.group(1), m.group(2)
    ref = re.search(r"\[((?:Psalm|Matthew|Luke|John) [\d:]+)\]", txt)
    txt = re.sub(r"\s*\[(?:Psalm|Matthew|Luke|John) [\d:]+\]", "", txt)
    if prev is not None and (sp != "narrator" or prev != "narrator"): t += PAUSE
    dur = _real(i)
    segs.append(dict(sp=sp, txt=txt, ref=ref.group(1) if ref else None, a=round(t, 1), b=round(t + dur, 1)))
    t += dur; prev = sp
END = round(t, 1)

def chunks(words, k=5):
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 3 and re.search(r"[;,:.]$", w) or len(cur) >= k: out.append(" ".join(cur)); cur = []
    if cur: out.append(" ".join(cur))
    return out

S = segs
# panel map: id, t0, t1, beat, still idea, tier, flags
cuts = [
 ("m01_cross_dying", 0.0, S[0]["b"] + 0.2, "Jesus ... dying on a cross. The leaders shout", "the cross at dusk, level camera, Jesus calm, leaders' hands pointing up from below", "kling", dict(role="first", ink_wake=True, sacred=True)),
 ("m02_leader_shouts", S[1]["a"], S[1]["b"] + 0.3, "[mocker] Matt 27:43", "single leader close, mouth open, pointing up, level eye height", "kling", {}),
 ("m03_back_to_david", S[2]["a"], S[2]["a"] + 7.0, "a thousand years back, a king named David", "aged King David writing by lamp, harp on wall", "seedance", {}),
 ("m04_psalm_scroll", S[2]["a"] + 7.0, S[3]["b"] + 0.3, "he writes their words into a song, Psalm 22 / [david] Ps 22:8", "open psalm scroll by clay lamp, close", "seedance", {}),
 ("m05_passersby", S[4]["a"], S[4]["b"] + 0.2, "Almost the same words ... people passing by shout", "three passers-by on the road below the cross, heads mid-shake (Witness Edge)", "kling", {}),
 ("m06_come_down", S[5]["a"], S[5]["b"] + 0.3, "[mocker] Matt 27:40", "crowd from below, hands pointing up, cross above", "kling", {}),
 ("m07_he_stayed", S[6]["a"], S[6]["b"] + 0.2, "He could have come down ... He stayed", "Jesus on the cross close, calm, nailed hand in frame, no glow", "seedance", dict(sacred=True)),
 ("m08_forgive", S[7]["a"], S[7]["b"] + 0.4, "Father, forgive them (Luke 23:34)", "Jesus face calm, looking out over the crowd, no glow", "seedance", dict(role="jesus", ink_wake=False, sacred=True)),
 ("m09_he_died", S[8]["a"] + 0.4, S[8]["b"] + 0.2, "They said, come down. He did not. He died there. He stayed.", "darkness over the cross, Jesus still, no glow", "seedance", dict(sacred=True)),
 ("m10_landing", S[9]["a"], END + 3.0, "A Roman soldier, watching Him die: Truly this was the Son of God.", "cross at dawn, Jesus calm, one human figure turning toward Him (landing: locked face, no glow)", "seedance", dict(sacred=True)),
]
# make panels contiguous (each starts where the previous ended)
panels = []
for i, (pid, a, b, beat, still, tier, fl) in enumerate(cuts):
    a = 0.0 if i == 0 else panels[-1]["t"][1]
    b = cuts[i + 1][1] if i + 1 < len(cuts) else b
    d = dict(id=pid, t=[round(a, 1), round(b, 1)], beat=beat, still_prompt=still, clip_tier=tier,
             status="TODO still + clip", ink_wake=False, role="listener"); d.update(fl); panels.append(d)

balloons = []
for s in segs:
    if not s["ref"]: continue
    sp = s["sp"]; who = {"mocker": "A MOCKER", "david": "DAVID", "narrator": ("THE OFFICER" if s["ref"] == "Matthew 27:54" else "JESUS")}[sp]
    text = re.sub(r'^"|"$', "", s["txt"]).strip(); text = text.strip('"')
    parts = chunks(text.split()); span = s["b"] - s["a"]
    if sp == "narrator":  # Luke 23:34 is Jesus' own prayer -> a KJV-checked Jesus balloon chain
        sp = "soldier" if s["ref"] == "Matthew 27:54" else "jesus"
    for i, p in enumerate(parts):
        a = s["a"] + span * i / len(parts) * 0.5
        d = dict(speaker=sp, kjv_ref=s["ref"], text=p, t=[round(a, 1), round(s["b"] + 0.3, 1)])
        if i == 0: d["tabs"] = [[who, 90], [s["ref"].upper().replace("MATTHEW", "MATT").replace("PSALM", "PSALM"), 790]]
        balloons.append(d)

card_decode_t = [round(S[3]["a"] - 0.0, 1), 0]
# decode card: DELIVER = RESCUE, shown right after the mocker's first quote ends (during the plain-words line)
dec_a = round(S[1]["b"] + 0.7, 1); dec_b = round(dec_a + 2.6, 1)
kjv = {"Luke 23:34": "Father, forgive them; for they know not what they do.", "Matthew 27:54": "Truly this was the Son of God."}
ep = dict(
    episode="the_mockers_ps22_7_y7", status="PANEL MAP ONLY - Y4 words LOCKED + RECORDED (71.26s); timings from real audio; no stills, no clips, no spend",
    format=dict(w=1080, h=1920, fps=30), first_episode=False,
    audio=dict(file="batches/cluster_01_cross/mockers_words_ps227/audio_y4/narration.mp3", t0=0.0, dur=round(END + 3.0, 1),
               note="Y4 recording, 71.26s natural speed, real turn timings. Add >=3.0s landing hold (INV-26) at assembly."),
    panels=panels, kjv=kjv, balloons=balloons,
    cards=[dict(kind="hook", lines=["WHOSE WORDS", "ARE THESE?"], t=[0.2, 2.8], decodes=[]),
           dict(kind="decode", lines=["DELIVER", "= RESCUE"], t=[dec_a, dec_b], decodes=["deliver"])],
    decode_words=["deliver"], sfx=[], sketch_dir="poc_comic_page/_piece1/stills_v2/_sketch",
    output="poc_comic_page/_living_comic/out/the_mockers_y7.mp4",
    cost_estimate=dict(stills="~10 unique stills, about $3-4 (re-quote from the real invoice)",
        clips="~4 Kling about $1.13 + ~6 Seedance about $0.72 = about $9; reuse-first check could cut this",
        voice="DONE about $0.50 spent 2026-11-07", total="about $13-14. ESTIMATE ONLY. Each paid step needs its own yes + quoted price."))
json.dump(ep, open(OUT, "w", encoding="utf-8"), indent=1)
print("wrote", OUT, "end", END, "panels", len(panels), "balloons", len(balloons))
for s in segs: print(s["a"], s["b"], s["sp"], s["txt"][:50])
