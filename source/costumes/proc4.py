from PIL import Image, ImageDraw
import numpy as np, sys, json
from scipy import ndimage
CW,CH,AX,AY=280,240,105,150
def load(n): return np.array(Image.open(f'src/{n}.png').convert('RGB')).astype(float)
def bgcolor(a):
    b=np.concatenate([a[:8].reshape(-1,3),a[-8:].reshape(-1,3),a[:,:8].reshape(-1,3),a[:,-8:].reshape(-1,3)])
    return np.median(b,axis=0)
def key(a,G):
    dist=np.sqrt(((a-G)**2).sum(-1))
    alpha=np.clip((dist-45)/(150-45),0,1); alpha[alpha<0.06]=0
    F=(a-(1-alpha[...,None])*G)/np.maximum(alpha[...,None],1e-3); F=np.clip(F,0,255)
    if G[1]>G[0] and G[1]>G[2]:
        edge=alpha<0.9; F[...,1]=np.where(edge,np.minimum(F[...,1],np.maximum(F[...,0],F[...,2])+25),F[...,1])
    else:
        edge=alpha<0.9; lim=np.minimum(F[...,0],F[...,2])
        mx=np.maximum(F[...,0],F[...,2]); F[...,0]=np.where(edge&(F[...,0]>F[...,1]+40)&(F[...,2]>F[...,1]+40),F[...,1]+30,F[...,0]); F[...,2]=np.where(edge&(F[...,2]>F[...,1]+40),F[...,1]+30,F[...,2])
    return np.dstack([F,alpha*255]).astype(np.uint8), dist
def halves(fg):
    cols=fg.sum(0)>2; W=len(cols); c=W//2
    # find widest empty run near center
    best=None; i=int(W*.3)
    while i<int(W*.7):
        if not cols[i]:
            j=i
            while j<W and not cols[j]: j+=1
            if not best or j-i>best[1]-best[0]: best=(i,j)
            i=j
        else: i+=1
    mid=(best[0]+best[1])//2
    out=[]
    for x0,x1 in [(0,mid),(mid,W)]:
        sub=fg[:,x0:x1]; lab,k=ndimage.label(sub); sz=ndimage.sum(sub,lab,range(1,k+1))
        keep=np.isin(lab,[i+1 for i in range(k) if sz[i]>40])
        ys,xs=np.where(keep); out.append((x0+xs.min(),x0+xs.max()+1,ys.min(),ys.max()+1))
    return out
def eyes(a,box):
    x0,x1,y0,y1=box; sub=a[y0:y1,x0:x1]; lum=sub.mean(2)
    dark=(lum<75)&(sub[...,2]>=sub[...,1]-10)
    h,w=dark.shape; m=np.zeros_like(dark); m[int(h*.3):int(h*.9),:int(w*.6)]=1; dark&=m.astype(bool)
    lab,n=ndimage.label(dark); sz=ndimage.sum(dark,lab,range(1,n+1)); objs=ndimage.find_objects(lab)
    cand=[]
    for j in range(n):
        if sz[j]<15: continue
        sl=objs[j]; hh=sl[0].stop-sl[0].start; ww=sl[1].stop-sl[1].start
        if 0.6<hh/ww<2.6 and hh<h*.2:
            cy,cx=ndimage.center_of_mass(dark,lab,j+1); cand.append((sz[j],cx+x0,cy+y0))
    cand.sort(reverse=True); cand=cand[:6]; best=None
    for i in range(len(cand)):
        for j in range(i+1,len(cand)):
            A,B=sorted([cand[i],cand[j]],key=lambda t:t[1])
            if abs(A[2]-B[2])<20 and 25<B[1]-A[1]<170 and abs(A[0]/B[0]-1)<1.6:
                sc=A[0]+B[0]
                if not best or sc>best[0]: best=(sc,[A,B])
    return best[1] if best else None
names=sys.argv[1].split(','); tag=sys.argv[2]
info={}; cells={}
for n in names:
    a=load(n); G=bgcolor(a); rgba,dist=key(a,G); im=Image.fromarray(rgba,'RGBA')
    fg=dist>80; boxes=halves(fg); fr=[]; ei=[]
    for box in boxes:
        e=eyes(a,box)
        MAN={'devil2':[[(1,517,520),(1,586,522)],[(1,975,520),(1,1045,522)]],'gothic':[[(1,456,516),(1,538,521)],[(1,1012,516),(1,1094,521)]]}
        if n in MAN: e=MAN[n][0 if box[0]<a.shape[1]//2 else 1]
        if not e: print('NO EYES',n,box); e=[(1,0,0),(1,39,0)]
        L,Rr=e; sc=39.0/(Rr[1]-L[1]); ei.append([round(L[1]),round(L[2]),round(Rr[1]),round(Rr[2]),round(sc,3)])
        x0,x1,y0,y1=box; pad=10
        crop=im.crop((x0-pad,y0-pad,x1+pad,y1+pad)); cw,ch=crop.size
        crop=crop.resize((max(1,round(cw*sc)),max(1,round(ch*sc))),Image.LANCZOS)
        ex=(Rr[1]-(x0-pad))*sc; ey=(Rr[2]-(y0-pad))*sc
        cell=Image.new('RGBA',(CW,CH),(0,0,0,0)); cell.paste(crop,(round(AX-ex),round(AY-ey)),crop)
        al=np.array(cell)[...,3]; colz=al[:,AX+10:AX+100]>128; rows=np.where(colz.any(1))[0]
        bottom=rows.max() if len(rows) else AY+52; k2=52.0/max(30,bottom-AY)
        if abs(k2-1)>0.12:
            print('  rescale',n,round(k2,2))
            sc2=sc*k2; crop=im.crop((x0-pad,y0-pad,x1+pad,y1+pad)); crop=crop.resize((max(1,round(cw*sc2)),max(1,round(ch*sc2))),Image.LANCZOS)
            ex=(Rr[1]-(x0-pad))*sc2; ey=(Rr[2]-(y0-pad))*sc2
            cell=Image.new('RGBA',(CW,CH),(0,0,0,0)); cell.paste(crop,(round(AX-ex),round(AY-ey)),crop)
        fr.append(cell)
    cells[n]=fr; info[n]={'bg':G.astype(int).tolist(),'eyes':ei}
    print(n,info[n])
cols=6; rows=(len(names)+cols-1)//cols
pv=Image.new('RGBA',(CW*cols,CH*rows),(198,207,244,255)); d=ImageDraw.Draw(pv)
for i,n in enumerate(names):
    pv.alpha_composite(cells[n][0],((i%cols)*CW,(i//cols)*CH)); d.text(((i%cols)*CW+6,(i//cols)*CH+6),n,fill='black')
pv.convert('RGB').save(tag+'-preview.png')
import pickle; pickle.dump({n:[c.tobytes() for c in cells[n]] for n in names},open(tag+'.pkl','wb'))
json.dump(info,open(tag+'-info.json','w'))
