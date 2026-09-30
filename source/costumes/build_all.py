from PIL import Image, ImageDraw
import numpy as np, json, sys
from scipy import ndimage
exec(open('proc4.py').read().split("names=sys.argv")[0])   # reuse load/bgcolor/key/halves/eyes
# game key -> source file
SRC = {'bear':'bear','space':'space','explorer':'explorer','newyear':'newyear','witch':'witch','santa':'santa','yukata':'yukata','knit':'knit','hoodie':'hoodie','miko':'miko',
 'idol':'idol','maid':'maid','gothic':'gothic','sakura':'sakura2','blueberry':'blueberry2','lemon':'lemon2','strawberry':'strawberry2','chick':'chick',
 'dog':'dog','mango':'mango3','raincoat':'raincoat','matcha':'matcha2','chef':'chef','musician':'musician','nurse':'nurse','camping':'camping','pajama':'pajama','ghostmaid':'ghostmaid',
 'constellation':'constellation','asagao':'zansho','grape':'grape','higanbana':'higanbana','momiji':'momiji','randoseru':'randoseru','goldfish':'goldfish','angel':'angel2','jugoya':'jugoya','devil':'devil2',
 'crown':'crown','flower':'flower','cat':'cat','sailor':'sailor2','rabbit':'rabbit','ribbon':'ribbon','delivery':'delivery','bath':'bath'}
MANEYE={'devil2':(517,520,586,522),'gothic':(456,516,538,521)}
SCALEFIX={'bath':.9,'maid':1.22,'hoodie':.92,'jugoya':.8,'zansho':.88,'camping':.92,'goldfish':.92,'ghostmaid':.92}
S=0.8; CW,CH=240,208  # stored cell (scale-1 coords 300x260)
EX,EY=130,165          # right-eye position in scale-1 cell coords
keys=list(SRC); cols=8; rows=(len(keys)+cols-1)//cols
sheet=Image.new('RGBA',(CW*cols,CH*rows),(0,0,0,0)); meta={}
for i,k in enumerate(keys):
    n=SRC[k]; a=load(n); G=bgcolor(a); rgba,dist=key(a,G); im=Image.fromarray(rgba,'RGBA')
    fg=dist>80
    try: box=halves(fg)[0]
    except Exception:
        lab,kk=ndimage.label(fg); sz=ndimage.sum(fg,lab,range(1,kk+1)); objs=ndimage.find_objects(lab)
        s0=sorted([objs[j] for j in np.argsort(sz)[::-1][:2]],key=lambda s:s[1].start)[0]; box=(s0[1].start,s0[1].stop,s0[0].start,s0[0].stop); print('fallback',k)
    if n in MANEYE: lx,ly,rx,ry=MANEYE[n]; e=[(1,lx,ly),(1,rx,ry)]
    else: e=eyes(a,box)
    L,Rr=e; sc=39.0/(Rr[1]-L[1])*SCALEFIX.get(n,1)
    x0,x1,y0,y1=box; pad=10
    crop=im.crop((x0-pad,y0-pad,x1+pad,y1+pad)); cw,ch=crop.size
    s2=sc*S; crop=crop.resize((max(1,round(cw*s2)),max(1,round(ch*s2))),Image.LANCZOS)
    ex=(Rr[1]-(x0-pad))*s2; ey=(Rr[2]-(y0-pad))*s2
    cell=Image.new('RGBA',(CW,CH),(0,0,0,0)); cell.paste(crop,(round(EX*S-ex),round(EY*S-ey)),crop)
    al=np.array(cell)[...,3]
    body=al[:, int((EX-20)*S):int((EX+110)*S)]>140
    rws=np.where(body.sum(1)>3)[0]; ground=(rws.max()+1)/S if len(rws) else EY+52
    # lid color: median of pixels around right eye ring
    arr=np.array(cell).astype(int); cx,cy=int(EX*S),int(EY*S)
    ring=arr[cy-14:cy+14, cx+9:cx+16].reshape(-1,4); ring=ring[ring[:,3]>200]
    lid=np.median(ring[:,:3],axis=0).astype(int).tolist() if len(ring) else [246,244,252]
    ldx=(L[1]-Rr[1])*sc; ldy=(L[2]-Rr[2])*sc
    sheet.paste(cell,((i%cols)*CW,(i//cols)*CH))
    meta[k]={'i':i,'g':round(float(ground),1),'lid':'#%02x%02x%02x'%tuple(lid),'le':[round(float(ldx),1),round(float(ldy),1)]}
q=sheet.quantize(colors=256,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE)
q.save('../../costumes.png',optimize=True)
json.dump({'cw':CW,'ch':CH,'cols':cols,'s':S,'ex':EX,'ey':EY,'m':meta},open('costumes.json','w'))
pv=Image.new('RGBA',sheet.size,(198,207,244,255)); pv.alpha_composite(q.convert('RGBA')); d=ImageDraw.Draw(pv)
for k,m in meta.items():
    i=m['i']; X=(i%cols)*CW; Y=(i//cols)*CH; d.text((X+4,Y+4),k,fill='black'); gy=Y+m['g']*S; d.line([X+60,gy,X+200,gy],fill=(255,0,0))
pv.convert('RGB').save('all-preview.png'); print(len(meta))
