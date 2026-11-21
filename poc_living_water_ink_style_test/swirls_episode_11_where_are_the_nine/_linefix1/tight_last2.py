import subprocess
from pathlib import Path
H=Path(__file__).resolve().parent
CUTS=[(1.45,1.80),(3.25,3.70),(4.95,5.30)]
FMT="aformat=sample_fmts=fltp:channel_layouts=mono:sample_rates=44100"
edges=[0.0]+[x for c in CUTS for x in c]+[None]
parts=[]; fc=[]
for i in range(len(CUTS)+1):
    a=edges[2*i]; b=edges[2*i+1]
    tr=f"atrim={a}" + (f":{b}" if b is not None else "")
    fi="" if i==0 else ",afade=t=in:st=0:d=0.025"
    fo="" if b is None else f",afade=t=out:st={b-a-0.025:.3f}:d=0.025"
    fc.append(f"[0:a]{FMT},{tr},asetpts=PTS-STARTPTS{fi}{fo}[p{i}]"); parts.append(f"[p{i}]")
fc.append("".join(parts)+f"concat=n={len(parts)}:v=0:a=1[o]")
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/"last2_narrator_b.mp3"),"-filter_complex",";".join(fc),"-map","[o]","-c:a","pcm_s16le",str(H/"last2_b_tight.wav")],check=True)
