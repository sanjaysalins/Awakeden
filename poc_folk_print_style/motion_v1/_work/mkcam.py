import json,numpy as np
r=json.load(open('track.json'))
out={}
for n in [1,2,3,5,7,10,12,13,14,15,16,17]:
    d=np.array(r[str(n)]); t=d[:,0]; 
    keep=d[:,4]>=60
    t=t[keep]; 
    kf=[]
    T=d[-1,0]
    ts=np.linspace(0,T,6)
    row=[]
    for col in (1,2,3):
        y=d[keep][:,col]; c=np.polyfit(t,y,2); 
        row.append(np.polyval(c,ts))
    # force start identity
    row=[np.array(v)-(v[0]-(1 if i==0 else 0)) for i,v in enumerate(row)]
    out[n]=[[round(float(ts[k]),2),round(float(row[0][k]),4),round(float(row[1][k]),1),round(float(row[2][k]),1)] for k in range(6)]
s="const CAM: Record<number, number[][]> = {\n"+"".join("  %d: %s,\n"%(n-1,json.dumps(v)) for n,v in out.items())+"};\n"
open('cam_block.txt','w').write(s); print(s)
