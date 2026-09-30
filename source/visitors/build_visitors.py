import sys, json
sys.path.insert(0,'/home/claude/umimi/costumes')
import numpy as np
from PIL import Image
from scipy import ndimage
exec(open('/home/claude/umimi/costumes/proc4.py').read().split('names=sys.argv')[0])
ORDER=['jelly','star','seahorse','crab','dolphin','penguin','turtle','octopus','puffer','otter']
# display size in game units (longest side), anchor: 'b' bottom-center (walkers) / 'c' center (floaty)
SIZE={'jelly':105,'star':88,'seahorse':110,'crab':110,'dolphin':145,'penguin':100,'turtle':130,'octopus':100,'puffer':98,'otter':125}
ANCH={'jelly':'c','star':'b','seahorse':'c','crab':'b','dolphin':'c','penguin':'b','turtle':'b','octopus':'b','puffer':'c','otter':'c'}
RES=1.6   # sheet pixels per game unit
frames={}; meta={}
for n in ORDER:
    a=np.array(Image.open(f'src/{n}.png').convert('RGB')).astype(float)
    G=bgcolor(a); rgba,dist=key(a,G); fg=dist>80
    boxes=halves(fg); fr=[]
    for (x0,x1,y0,y1) in boxes:
        sub=rgba[y0:y1,x0:x1].copy(); m=sub[...,3]>20
        lab,k=ndimage.label(m); sz=ndimage.sum(m,lab,range(1,k+1)); big=sz.max()
        keep=np.isin(lab,[i+1 for i in range(k) if sz[i]>big*.03])
        keep=ndimage.binary_dilation(keep,iterations=3)
        sub[...,3]=np.where(keep,sub[...,3],0)
        fr.append(Image.fromarray(sub,'RGBA'))
    L=max(max(f.size) for f in fr)
    sc=SIZE[n]*RES/L
    fr=[f.resize((max(1,round(f.width*sc)),max(1,round(f.height*sc))),Image.LANCZOS) for f in fr]
    cw=max(f.width for f in fr)+4; ch=max(f.height for f in fr)+4
    cells=[]
    for f in fr:
        c=Image.new('RGBA',(cw,ch),(0,0,0,0))
        x=(cw-f.width)//2; y=(ch-f.height)//2 if ANCH[n]=='c' else ch-2-f.height
        c.paste(f,(x,y),f); cells.append(c)
    frames[n]=cells; meta[n]={'w':cw,'h':ch,'a':ANCH[n]}
# pack: one row per visitor, 2 frames
SW=max(m['w']*2 for m in meta.values()); SH=sum(m['h'] for m in meta.values())
sheet=Image.new('RGBA',(SW,SH),(0,0,0,0)); y=0
for n in ORDER:
    m=meta[n]; m['y']=y
    for i,c in enumerate(frames[n]): sheet.paste(c,(i*m['w'],y))
    y+=m['h']
sheet.save('/home/claude/umimi/visitors.png',optimize=True)
json.dump({'res':RES,'m':meta},open('visitors_meta.json','w'),separators=(',',':'))
print(SW,SH); print(json.dumps(meta))
# preview on dark + light bg
pv=Image.new('RGBA',(SW*2+20,SH),(60,70,120,255)); pv.paste(sheet,(0,0),sheet)
lt=Image.new('RGBA',(SW,SH),(215,230,250,255)); lt.paste(sheet,(0,0),sheet); pv.paste(lt,(SW+20,0))
pv.save('/tmp/claude-0/-home-claude-umimi/bc41eef5-1a2e-59db-a53d-ab76a0d631f5/scratchpad/vprev.png')
