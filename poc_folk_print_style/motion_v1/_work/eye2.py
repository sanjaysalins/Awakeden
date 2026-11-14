from PIL import Image
import numpy as np
im=np.array(Image.open("fr/s02_1.png").convert("RGB")).astype(int)
# star near (200,178) and (325,245)
for (x,y) in [(200,178),(325,245)]:
    p=im[y-14:y+15,x-14:x+15].reshape(-1,3); lum=p.sum(1); print((x,y),"brightest","#%02X%02X%02X"%tuple(p[lum.argmax()]), "bg", "#%02X%02X%02X"%tuple(int(v) for v in np.median(p,axis=0)))
im=np.array(Image.open("fr/s06_1.png").convert("RGB")).astype(int)
for (x,y) in [(95,90),(390,70),(500,190),(640,268)]:
    p=im[y-14:y+15,x-14:x+15].reshape(-1,3); lum=p.sum(1); print("s06",(x,y),"brightest","#%02X%02X%02X"%tuple(p[lum.argmax()]), "bg", "#%02X%02X%02X"%tuple(int(v) for v in np.median(p,axis=0)))
# s10 steam curl pixel colours: find darkest-ish tan pixels in region around art steam
im=np.array(Image.open("fr/s10_1.png").convert("RGB")).astype(int)
reg=im[450:850,350:650].reshape(-1,3); d=np.abs(reg-np.array([0xF9,0xD3,0xA7])).sum(1)
sel=reg[d>40]; print("steam px", "#%02X%02X%02X"%tuple(int(v) for v in np.median(sel[sel.sum(1)<640],axis=0)))
# s02 moon
print("moon", "#%02X%02X%02X"%tuple(im[0,0]))
im=np.array(Image.open("fr/s13_1.png").convert("RGB")).astype(int)
print("s13 sky stripes", ["#%02X%02X%02X"%tuple(im[y,x]) for x,y in [(100,200),(300,150),(700,300),(900,200)]])
print("night teals s02", ["#%02X%02X%02X"%tuple(np.array(Image.open('fr/s02_1.png').convert('RGB'))[y,x]) for x,y in [(500,50),(500,200),(900,300)]])
