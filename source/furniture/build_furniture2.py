import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage
exec(open('../costumes/proc4.py').read().split('names=sys.argv')[0])
RES = 2.0
# series -> items: key: (room width, tank width[, frames, anchor])
SERIES = {
 'base':    {'rug':(170,0),'bed':(150,0),'lamp':(66,0),'cushion':(80,0),'plant':(62,0),'shelf':(105,0),'window':(135,0),'windowday':(135,0),'frame':(72,0),'table':(115,0)},
 'pearl':   {'shellbed':(175,110),'shelltable':(125,82),'shellchair':(105,72),'bottle':(58,42),'crystal2':(90,62),'shellcake':(78,54)},
 'autumn':  {'lanternstand':(100,95),'stall':(200,180),'kingyo':(190,160),'mcushion':(115,90),'garland':(300,200),'chochin':(80,80),'omen':(200,180),'acorn':(60,42),'yakiimo':(70,48),'bridge':(230,200)},
 'craft':   {'cbench':(130,110),'cbench_f':(130,110),'ctable':(110,92),'ctable_f':(110,92),'cshelllamp':(70,62),'cshelllamp_f':(70,62),'ccoralpot':(72,60),'ccoralpot_f':(72,60),'cmobile':(80,72),'cmobile_f':(80,72),'bwork':(190,190),'bsign':(150,150),'bkiln':(160,160)},
 'halloween':{'pumpkinstand':(85,80),'hrug':(170,120),'ghostcushion':(85,72),'hframe':(80,0),'candytable':(105,82),'hshelf':(115,100),'jbox':(85,74,4,'b'),'chandelier':(130,0,3,'t')},
}
def keyed(a):
    G=bgcolor(a); rgba,dist=key(a,G)
    if G[1]>G[0]+80:
        g=a; spill=(g[...,1]>g[...,0]+30)&(g[...,1]>g[...,2]+30)&(g.mean(-1)>90); rgba[...,3]=np.where(spill,0,rgba[...,3])
    m=rgba[...,3]>20
    lab,k=ndimage.label(m)
    if k:
        sz=ndimage.sum(m,lab,range(1,k+1)); keep=np.isin(lab,[i+1 for i in range(k) if sz[i]>sz.max()*.02])
        rgba[...,3]=np.where(ndimage.binary_dilation(keep,iterations=2),rgba[...,3],0)
    return rgba
ONLY=sys.argv[1:]  # 例: python3 build_furniture2.py craft （指定したシリーズだけ作り直す）
meta=json.load(open('furniture_meta.json')) if ONLY else {}
for sname,items in SERIES.items():
    if ONLY and sname not in ONLY: continue
    cells=[]
    for n,spec in items.items():
        rw,tw=spec[0],spec[1]; nf=spec[2] if len(spec)>2 else 1
        a=np.array(Image.open(f'src/{n}.png').convert('RGB')).astype(float)
        H,W,_=a.shape; cw=W//nf
        frames=[keyed(a[:, i*cw:(i+1)*cw].copy()) for i in range(nf)]
        # union bbox so all frames stay aligned
        ys=[];xs=[]
        for f in frames:
            yy,xx=np.where(f[...,3]>20); ys+= [yy.min(),yy.max()]; xs+=[xx.min(),xx.max()]
        y0,y1,x0,x1=min(ys),max(ys)+1,min(xs),max(xs)+1
        for i,f in enumerate(frames):
            im=Image.fromarray(f[y0:y1,x0:x1],'RGBA'); Wd=round(rw*RES); Hd=round(im.height*Wd/im.width); im=im.resize((Wd,Hd),Image.LANCZOS)
            cells.append((n if nf==1 else f'{n}_{i}', im, rw, tw))
    # pack into columns of max height ~2000 px
    cols=[]; col=[]; h=0
    for c in cells:
        if h+c[1].height>2000 and col: cols.append(col); col=[]; h=0
        col.append(c); h+=c[1].height+2
    if col: cols.append(col)
    SW=sum(max(c[1].width for c in co)+2 for co in cols); SH=max(sum(c[1].height+2 for c in co) for co in cols)
    sheet=Image.new('RGBA',(SW,SH),(0,0,0,0)); x=0
    for co in cols:
        y=0
        for n,im,rw,tw in co:
            sheet.paste(im,(x,y)); rh=round(im.height/RES)
            meta[n]={'s':sname,'x':x,'y':y,'w':im.width,'h':im.height,'rw':rw,'rh':rh,'tw':tw,'th':round(rh*tw/rw) if tw else 0}
            y+=im.height+2
        x+=max(c[1].width for c in co)+2
    sheet.quantize(colors=255,method=Image.FASTOCTREE,dither=Image.NONE).save(f'../../f_{sname}.png',optimize=True)
    print(sname, sheet.size)
json.dump(meta,open('furniture_meta.json','w'),separators=(',',':'))
