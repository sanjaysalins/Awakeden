import sys
from PIL import Image
d=sys.argv[1]; out=sys.argv[2]; fr=sys.argv[3].split(","); w=int(sys.argv[4]) if len(sys.argv)>4 else 540
ims=[Image.open("%s/f%04d.jpg"%(d,int(f))).resize((w,int(w*16/9))) for f in fr]
o=Image.new("RGB",(w*len(ims),ims[0].height))
for i,im in enumerate(ims): o.paste(im,(i*w,0))
o.save(out,quality=88)
