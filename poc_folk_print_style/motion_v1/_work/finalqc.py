import subprocess,re,json,os
from PIL import Image,ImageDraw
src=open("F:/slk/PycharmProjects/JesusInTheBible/_remotion/src/SecondFireV1.tsx",encoding="utf8").read()
CAM={int(a):json.loads(b) for a,b in re.findall(r"^  (\d+): (\[\[.*\]\]),$",src,re.M)}
CUT=[0,99,240,396,471,567,711,867,1023,1101,1206,1434,1596,1806,2034,2256,2409,2637]
A={1:6,4:6,5:7,6:8,8:3,9:6,11:10,16:8}
def camat(i,t):
    k=CAM.get(i)
    if not k: return 1,0,0
    j=0
    while j<len(k)-2 and t>k[j+1][0]: j+=1
    a,b=k[j],k[j+1]; w=min(1,max(0,(t-a[0])/((b[0]-a[0]) or 1)))
    return [a[c]+(b[c]-a[c])*w for c in (1,2,3)]
V="F:/slk/PycharmProjects/JesusInTheBible/_remotion/out/sf_motion_v1.mp4"
def grab(f,w=1080):
    out="fq.png"
    subprocess.run(["ffmpeg","-y","-v","error","-threads","3","-ss","%.4f"%(f/30),"-i",V,"-frames:v","1",out])
    return Image.open(out).convert("RGB")
Q="../qc/"
def sheet(ims,name,cols,w=360):
    h=int(w*16/9); rows=(len(ims)+cols-1)//cols
    o=Image.new("RGB",(w*cols,h*rows),(20,20,20))
    for k,im in enumerate(ims): o.paste(im.resize((w,h)),((k%cols)*w,(k//cols)*h))
    o.save(Q+name,quality=86)
# 1 shots mid
mids=[(CUT[i]+CUT[i+1])//2 for i in range(17)]
sheet([grab(f) for f in mids],"QC_1_shots_mid.jpg",6)
# 2 transitions mid
TF=[("1-2",100),("4-5",472),("5-6",567),("6-7",710),("8-9",1025),("9-10",1102),("11-12",1431),("16-17",2408)]
ims=[]
for n,f in TF:
    im=grab(f); ims.append(im)
sheet(ims,"QC_2_transitions_mid.jpg",4,w=450)
# 3 keepouts
KO={0:[(330,560,750,1090)],6:[(100,700,590,1600)],8:[(730,500,860,690)],11:[(230,990,700,1720),(530,900,1080,1300)],12:[(150,960,580,1640),(680,1000,860,1190)],14:[(60,760,660,1700)],
15:[(230,990,720,1720),(640,1060,830,1260),(70,950,200,1060),(540,900,640,990),(700,870,800,960),(900,930,1010,1040)],16:[(540,0,1080,1330),(60,250,560,800),(250,820,830,1300)]}
FR={0:[10,50,95],6:[730,790,860],8:[1032,1060,1095],11:[1445,1500,1590],12:[1620,1710,1800],14:[2060,2160,2250],15:[2270,2330,2400],16:[2425,2500,2630]}
for i,frs in FR.items():
    S=CUT[i]-A.get(i,0); ims=[]
    for f in frs:
        im=grab(f); d=ImageDraw.Draw(im); s,tx,ty=camat(i,(f-S)/30)
        for (x1,y1,x2,y2) in KO[i]: d.rectangle([s*x1+tx,s*y1+ty,s*x2+tx,s*y2+ty],outline=(255,0,0),width=5)
        ims.append(im)
    sheet(ims,"KEEPOUT_s%02d.jpg"%(i+1),3,w=540)
print("ok")
