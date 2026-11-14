from PIL import Image
import numpy as np
def hx(a): return "#%02X%02X%02X"%tuple(int(v) for v in a)
def med(fn,x,y,r=3):
    im=np.array(Image.open(fn).convert("RGB"))
    p=im[y-r:y+r+1,x-r:x+r+1].reshape(-1,3); return hx(np.median(p,axis=0))
def line(fn,x,y0,y1,step=8):
    im=np.array(Image.open(fn).convert("RGB"))
    return [(y,hx(im[y,x])) for y in range(y0,y1,step)]
print("s02 flame col",line("fr/s02_1.png",525,1190,1330,10))
print("s06 stars", med("fr/s06_1.png",110,90),med("fr/s06_1.png",100,88,1), med("fr/s06_1.png",610,92,1))
print("s06 sea",med("fr/s06_1.png",800,1100),med("fr/s06_1.png",300,1700), med("fr/s06_1.png",100,1500))
print("s05 orange sky",med("fr/s05_1.png",100,200),med("fr/s05_1.png",300,100),med("fr/s05_1.png",900,300))
print("s12 sky",med("fr/s12_1.png",100,100),med("fr/s12_1.png",200,100),med("fr/s12_1.png",300,100),med("fr/s12_1.png",400,100))
print("cream cloud",med("fr/s12_1.png",360,150))
print("s07 flowers", [med("fr/s07_1.png",x,y,2) for x,y in [(520,1830),(560,1800),(880,1750)]])
print("s17 stone/coals", med("fr/s17_1.png",300,1650), med("fr/s17_1.png",550,1830))
print("s02 coal dark", med("fr/s02_1.png",470,1300,1))
print("s04 rooster sat", med("fr/s04_1.png",250,1480,2))
print("s10 steam tan", line("fr/s10_1.png",472,520,760,12)[:6])
print("s10 fish grey", med("fr/s10_1.png",800,1180,2), med("fr/s10_1.png",470,1090,2))
print("s11 star teal in top sky", med("fr/s11_1.png",60,40,1))
print("s12 flower petals", med("fr/s12_1.png",330,1860,3), med("fr/s12_1.png",250,1890,2),med("fr/s12_1.png",600,1780,2))
print("s17 ink", med("fr/s17_1.png",470,1560,1))
