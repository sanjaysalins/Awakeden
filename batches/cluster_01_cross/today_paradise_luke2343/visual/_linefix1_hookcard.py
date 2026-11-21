from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
H=Path(__file__).resolve().parent; FONT=r"C:\Windows\Fonts\Oswald-Bold.ttf"
def card(txt,y0,y1,fill,name,size=112,pad=20):
    im=Image.new("RGBA",(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); f=ImageFont.truetype(FONT,size)
    bb=d.textbbox((0,0),txt,font=f); w=bb[2]-bb[0]; h=bb[3]-bb[1]
    x0=(1080-w)//2-pad; d.rectangle([x0,y0,x0+w+2*pad,y1],fill=(0,0,0,185))
    tx=(1080-w)//2-bb[0]; ty=y0+((y1-y0)-h)//2-bb[1]
    d.text((tx+3,ty+3),txt,font=f,fill=(0,0,0,255)); d.text((tx,ty),txt,font=f,fill=fill)
    im.save(H/"_linefix1_pool"/name); print(name,w)
card("TWO GUILTY MEN",148,278,(255,255,255,255),"hook1.png")
card("NO TIME LEFT",298,428,(241,191,77,255),"hook2.png")
