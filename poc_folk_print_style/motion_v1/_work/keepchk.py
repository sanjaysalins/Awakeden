import subprocess,json,re,sys,os
import numpy as np
from PIL import Image, ImageDraw
src=open("F:/slk/PycharmProjects/JesusInTheBible/_remotion/src/SecondFireV1.tsx",encoding="utf8").read()
cam=eval(re.search(r"const CAM: Record<number, number\[\]\[\]> = (\{.*?\n\});",src,re.S).group(1).replace("{","{").replace("\n"," ").replace("}","}") ,{}) if False else None
m=re.findall(r"^  (\d+): (\[\[.*\]\]),$",src,re.M)
CAM={int(a):json.loads(b) for a,b in m}
CUT=[0,99,240,396,471,567,711,867,1023,1101,1206,1434,1596,1806,2034,2256,2409,2637]
A={1:6,4:6,5:7,6:8,8:3,9:6,11:10,16:8}
def camat(i,t):
    k=CAM.get(i)
    if not k: return 1,0,0
    j=0
    while j<len(k)-2 and t>k[j+1][0]: j+=1
    a,b=k[j],k[j+1]; w=min(1,max(0,(t-a[0])/((b[0]-a[0]) or 1)))
    return [a[c]+(b[c]-a[c])*w for c in (1,2,3)]
KO={0:[(330,560,750,1090)],2:[(40,880,200,1030),(540,760,820,970)],4:[(680,930,900,1200)],6:[(100,700,590,1600)],8:[(730,500,860,690),(260,560,500,800)],
11:[(230,990,700,1720),(530,900,1080,1300)],12:[(150,960,580,1640),(680,1000,860,1190)],13:[(250,520,830,1500)],14:[(60,760,660,1700)],
15:[(230,990,720,1720),(640,1060,830,1260),(70,950,200,1060),(540,900,640,990),(700,870,800,960),(900,930,1010,1040)],
16:[(540,0,1080,1330),(60,250,560,800),(250,820,830,1300)]}
FR={0:[20,60,95],2:[260,330,390],4:[480,520,565],6:[730,790,860],8:[1032,1060,1090],11:[1445,1500,1590],12:[1610,1700,1800],13:[1820,1990,2030],14:[2050,2160,2250],15:[2270,2330,2400],16:[2420,2500,2630]}
os.makedirs("../qc",exist_ok=True)
tot={}
for i,frs in FR.items():
    S=CUT[i]-A.get(i,0)
    for f in frs:
        t=(f-S)/30
        subprocess.run(["ffmpeg","-y","-v","error","-threads","3","-ss","%.3f"%t,"-i","F:/slk/PycharmProjects/JesusInTheBible/_remotion/public/sf/s%02d.mp4"%(i+1),"-frames:v","1","-vf","scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920","raw.png"])
        raw=np.array(Image.open("raw.png").convert("RGB")).astype(int)
        comp=Image.open("qk/f%04d.jpg"%f).convert("RGB"); ca=np.array(comp).astype(int)
        diff=(np.abs(ca-raw).sum(2)>110)
        s,tx,ty=camat(i,t)
        d=ImageDraw.Draw(comp); res=[]
        for (x1,y1,x2,y2) in KO.get(i,[]):
            X1,Y1,X2,Y2=[int(round(v)) for v in (s*x1+tx,s*y1+ty,s*x2+tx,s*y2+ty)]
            X1=max(0,X1);Y1=max(0,Y1);X2=min(1080,X2);Y2=min(1920,Y2)
            n=int(diff[Y1:Y2,X1:X2].sum()); res.append(n)
            d.rectangle([X1,Y1,X2,Y2],outline=(255,0,0),width=4)
            ys,xs=np.nonzero(diff[Y1:Y2,X1:X2])
            if n>150: print("  HIT shot",i+1,"f",f,"box",(x1,y1,x2,y2),n,"bbox of hits",(int(xs.min())+X1,int(ys.min())+Y1,int(xs.max())+X1,int(ys.max())+Y1))
        print("s%02d f%d boxes diff px:"%(i+1,f),res)
        comp.save("../qc/keepout_s%02d_f%04d.jpg"%(i+1,f),quality=85)
