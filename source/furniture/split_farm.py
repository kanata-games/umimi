# はたけの「そだつようす」（1枚に 芽・そだちかけ・みのった の3つが よこならび）を 3まいに わける
# 出力：src/p_<さくもつ>_1〜3.png（背景は 元の色のまま。build_furniture2.py が 背景を ぬく）
import numpy as np
from PIL import Image
from scipy import ndimage
for k in ['lettuce','berry','mush','moonfruit']:
    im=Image.open(f'src/grow_{k}.png').convert('RGB'); a=np.array(im).astype(int)
    bg=np.median(np.concatenate([a[:8].reshape(-1,3),a[-8:].reshape(-1,3)]),axis=0)
    fg=np.abs(a-bg).sum(-1)>90
    col=ndimage.binary_dilation(fg.any(0),iterations=6)
    lab,n=ndimage.label(col); segs=ndimage.find_objects(lab)
    segs=sorted([s[0] for s in segs if s[0].stop-s[0].start>30], key=lambda s:s.start)
    assert len(segs)==3, (k,len(segs))
    for i,s in enumerate(segs):
        x0=max(0,s.start-10); x1=min(a.shape[1],s.stop+10)
        im.crop((x0,0,x1,a.shape[0])).save(f'src/p_{k}_{i+1}.png')
        ys=np.where(fg[:,s].any(1))[0]; print(k,i+1,'w',s.stop-s.start,'h',ys.max()-ys.min(),'bottom',ys.max())
