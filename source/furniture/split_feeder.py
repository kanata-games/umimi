# えさばこの絵（1枚に いくつも ならんで 届いた）を 1こずつに わける
# feeder_treat_src.png → tbox_0（から）tbox_1（はんぶん）tbox_2（いっぱい）
# feeder_aosa_src.png  → abox_1（はんぶん）abox_2（いっぱい）aosa1 aosa2（しずむ アオサ）
import numpy as np
from PIL import Image
from scipy import ndimage
def parts(fn):
    im=Image.open(fn).convert('RGB'); a=np.array(im).astype(int)
    bg=np.median(np.concatenate([a[:6].reshape(-1,3),a[-6:].reshape(-1,3)]),axis=0)
    fg=np.abs(a-bg).sum(-1)>90
    lab,n=ndimage.label(ndimage.binary_dilation(fg,iterations=2)); sz=ndimage.sum(fg,lab,range(1,n+1))
    objs=[(s, sz[i]) for i,s in enumerate(ndimage.find_objects(lab)) if sz[i]>sz.max()*.05]
    objs=sorted(objs,key=lambda o:o[0][1].start)
    out=[]
    for (ys,xs),_ in objs:
        out.append(im.crop((max(0,xs.start-8),max(0,ys.start-8),min(a.shape[1],xs.stop+8),min(a.shape[0],ys.stop+8))))
    return out
t=parts('src/feeder_treat_src.png'); assert len(t)==3,len(t)
for i,p in enumerate(t): p.save(f'src/tbox_{i}.png')
a=parts('src/feeder_aosa_src.png'); assert len(a)==4,len(a)
for k,p in zip(['abox_1','abox_2','aosa1','aosa2'],a): p.save(f'src/{k}.png')
print([p.size for p in t],[p.size for p in a])
