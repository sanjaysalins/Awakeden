r"""Jonah wordsfix1 narration splice. Old narration.mp3 (current pinned) is kept sample-exact except 3 replaced blocks:
 N1 'He sent me ... Tarshish.'  -> take n1_b ; N2 'Then, long after I was dust, ... name:' -> n2_b ; N3 'Stop running ... live.' -> n3_b
New block keeps the old gap lengths on both sides (cut at the middle of the silence), speech trimmed to its onset/offset,
RMS-matched to the old witness speech, 12 ms fades at each join. Tail: landing hold 3.05 s after the last word.
Writes narration_wordsfix1.mp3 + alignment_wordsfix1.json + narration.spoken_wordsfix1.txt + blocks.json"""
import json, subprocess, sys
import numpy as np, scipy.io.wavfile as wf
from pathlib import Path
H = Path(__file__).resolve().parent; P = H.parent; SR = 44100
OLD = json.load(open(P/"audio/alignment.json", encoding="utf-8"))
def dec(src, out):
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(src),"-vn","-ac","1","-ar",str(SR),"-c:a","pcm_s16le",str(out)],check=True)
    return wf.read(out)[1].astype(np.float64)/32768
old = dec(P/"audio/narration.mp3", H/"_old.wav")
def widx(text, start_after=0, n=1):
    for i, w in enumerate(OLD):
        if w["w"] == text and w["start"] >= start_after: return i
def mid_gap(i_prev, i_next): return (OLD[i_prev]["end"] + OLD[i_next]["start"]) / 2
# block definitions (indexes into OLD)
def find(txt, after=0): return next(i for i, w in enumerate(OLD) if w["w"] == txt and w["start"] >= after)
i_He = find("He", 10); i_Tar = find("Tarshish."); i_The = find("The", 16)
i_Then = find("Then,"); i_name = find("name:"); i_For = find("For")
i_Stop = find("Stop"); i_live = find("live.")
assert OLD[i_Then]["start"] > 19 and OLD[i_Stop]["start"] > 53
blocks = [  # name, first word idx, last word idx, take, text
 ("n1", i_He, i_Tar, "n1_b", "He sent me to Nineveh, and I fled. I knew He is gracious, and would spare her."),
 ("n2", i_Then, i_name, "n2_b", "Then, centuries later, scribes demanded a sign — Jesus gave them only my name:"),
 ("n3", i_Stop, i_live, "n3_b", "The One who went down into your dark and rose again is Jesus. He can bring you up."),
]
# voiced RMS of old witness speech (exclude Jesus quote)
def voiced_rms(x, a, b):
    seg = x[int(a*SR):int(b*SR)]; fr = seg[:len(seg)//441*441].reshape(-1, 441); r = np.sqrt((fr**2).mean(1))
    v = r[r > 0.2*r.max()]; return float(np.sqrt((v**2).mean()))
ref = voiced_rms(old, 0.3, 6.2)
print("old witness voiced rms", ref)
def speech_bounds(x, pad=0.0):
    fr = x[:len(x)//441*441].reshape(-1, 441); r = np.sqrt((fr**2).mean(1)); th = 0.06*r.max()
    idx = np.where(r > th)[0]; return idx[0]*0.01, (idx[-1]+1)*0.01
out = []; pos = 0.0  # pos = old-time pointer
newwords = []; shift = 0.0; info = []
def add_old(a, b):
    out.append(old[int(round(a*SR)):int(round(b*SR))])
cur = 0.0
t_new = 0.0
segs = []
for k, (name, i0, i1, take, text) in enumerate(blocks):
    M1 = mid_gap(i0-1, i0)
    last_block = (i1 == i_live)
    M2 = OLD[i1]["end"] + 0.15 if last_block else mid_gap(i1, i1+1)
    segs.append(("old", cur, M1))
    nw = dec(H/f"{take}.mp3", H/f"_{take}.wav")
    s, e = speech_bounds(nw)
    nw = nw[int(s*SR):int(e*SR)+int(0.04*SR)]
    g = ref / voiced_rms(nw, 0, len(nw)/SR); nw = np.clip(nw*g, -0.98, 0.98)
    lead = OLD[i0]["start"] - M1
    trail = 0.0 if last_block else (M2 - OLD[i1]["end"])
    segs.append(("new", name, nw, lead, trail, text, take, g))
    cur = M2
if True:
    segs.append(("tail",))
# assemble
audio = np.zeros(0); words = []
def append(x, fade_in=True):
    global audio
    f = int(0.012*SR)
    if len(audio) and len(x) > 2*f:
        x = x.copy(); x[:f] *= np.linspace(0, 1, f); audio[-f:] *= np.linspace(1, 0, f)
    audio = np.concatenate([audio, x])
old_map = []  # (old_a, old_b, new_a)
blkinfo = []
for sg in segs:
    if sg[0] == "old":
        a, b = sg[1], sg[2]; old_map.append((a, b, len(audio)/SR)); append(old[int(a*SR):int(b*SR)])
    elif sg[0] == "new":
        _, name, nw, lead, trail, text, take, g = sg
        new_start = len(audio)/SR + lead
        append(np.concatenate([np.zeros(int(lead*SR)), nw, np.zeros(int(trail*SR))]))
        blkinfo.append(dict(name=name, take=take, text=text, speech_start=round(new_start, 3), speech_len=round(len(nw)/SR, 3), gain=round(g, 3)))
last_speech_end = blkinfo[-1]["speech_start"] + blkinfo[-1]["speech_len"] - 0.04
HOLD = 3.2
total_needed = last_speech_end + HOLD
total = np.ceil(total_needed*30)/30
audio = np.concatenate([audio, np.zeros(int(round(total*SR)) - len(audio))])[:int(round(total*SR))]
wf.write(H/"_narr_new.wav", SR, (np.clip(audio, -0.99, 0.99)*32767).astype(np.int16))
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/"_narr_new.wav"),"-c:a","libmp3lame","-b:a","128k","-ar","44100",str(H/"narration_wordsfix1.mp3")],check=True)
(H/"blocks.json").write_text(json.dumps(dict(blocks=blkinfo, old_map=old_map, total=total, last_speech_end=last_speech_end), indent=1))
print(json.dumps(blkinfo, indent=1), "total", total, "old_map", [(round(a,2), round(b,2), round(c,2)) for a, b, c in old_map])
