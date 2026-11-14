from PIL import Image, ImageDraw
import sys,json
# keep-out from spec (x1,y1,x2,y2)
KO={1:[(330,560,750,1090)],7:[(100,700,590,1600)],9:[(644,457,904,717)],12:[(230,990,700,1720),(530,900,1080,1300)],
13:[(150,960,580,1640)],14:[(250,520,830,1500)],15:[(80,930,640,1560)],16:[(230,990,720,1720)],
17:[(540,0,1080,1330),(60,250,560,800),(250,820,830,1300)],5:[(680,930,900,1200)]}
S=0.5
def strip(n,boxes=True,grid=True):
    ims=[]
    for k in range(3):
        im=Image.open("fr/s%02d_%d.png"%(n,k)).convert("RGB")
        d=ImageDraw.Draw(im)
        if grid:
            for x in range(0,1080,100):
                d.line([(x,0),(x,1920)],fill=(255,255,255) if x%200 else (255,255,0),width=1)
                if x%200==0: d.text((x+3,3),str(x),fill=(255,255,0))
            for y in range(0,1920,100):
                d.line([(0,y),(1080,y)],fill=(255,255,255) if y%200 else (255,255,0),width=1)
                if y%200==0: d.text((3,y+3),str(y),fill=(255,255,0))
        if boxes:
            for b in KO.get(n,[]): d.rectangle(b,outline=(255,0,0),width=4)
        ims.append(im.resize((int(1080*S*0.9),int(1920*S*0.9))))
    w=sum(i.width for i in ims); out=Image.new("RGB",(w,ims[0].height))
    x=0
    for i in ims: out.paste(i,(x,0)); x+=i.width
    return out
if __name__=="__main__":
    for n in map(int,sys.argv[1:]):
        strip(n).save("strip_%02d.jpg"%n,quality=85)
