from PIL import Image
import numpy as np, math, sys
for n,(cx,cy) in {12:(535,500),16:(535,500)}.items():
    im=np.array(Image.open("fr/s%02d_t0.png"%n).convert("RGB")).astype(int)
    for R in (300,420):
        prev=None; edges=[]
        cols=[]
        for a10 in range(1800,3601,5):
            a=math.radians(a10/10); x=int(cx+R*math.cos(a)); y=int(cy+R*math.sin(a))
            if not(0<=x<1080 and 0<=y<1920): cols.append(None); continue
            cols.append(im[y,x])
        last=None
        for i,c in enumerate(cols):
            if c is None: continue
            if last is not None and np.abs(c-last).sum()>90: edges.append(round(180+i*0.5,1))
            last=c
        print(n,R,edges)
