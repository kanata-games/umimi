# umimi-sprites.png の 10コマ（base10.png）の うしろに、追加の表情コマ（ext1〜3.png、5列×2行の 1280x720）を つなげる
# 体（いちばん大きい かたまり）の 下の はしと 横の まんなかを、base の 0コマめに そろえる
import numpy as np
from PIL import Image
from scipy import ndimage
CW,CH=245,222
# (ファイル, 行, 列) の順で 10コマめ から ならぶ。ゲームの SPRX と 同じ順
PICK=[('ext1',0,2),('ext1',0,3),('ext1',1,0),('ext1',1,1),('ext2',1,0),('ext2',1,1),('ext2',1,2),('ext2',1,3),('ext2',1,4),('ext1',1,3),
      ('ext2',0,4),('ext1',1,2),('ext3',1,2),('ext3',1,0),('ext3',1,1)]
def key(a):
    r,g,b=a[...,0],a[...,1],a[...,2]
    G=np.array([12,235,18.])
    d=g-np.maximum(r,b)
    alpha=np.clip(1-np.clip(d,0,None)/205,0,1); alpha[alpha<0.07]=0
    F=(a-(1-alpha[...,None])*G)/np.maximum(alpha[...,None],1e-3); F=np.clip(F,0,255)
    F[...,1]=np.minimum(F[...,1],np.maximum(F[...,0],F[...,2])+25)
    return np.dstack([F,alpha*255]).astype(np.uint8)
def body_box(rgba):
    m=rgba[...,3]>120; lab,n=ndimage.label(m); sz=ndimage.sum(m,lab,range(1,n+1)); j=int(np.argmax(sz))+1
    ys,xs=np.where(lab==j); return xs.min(),xs.max(),ys.min(),ys.max()
base=Image.open('base10.png').convert('RGBA'); b=np.array(base)
bx0,bx1,by0,by1=body_box(b[0:CH,0:CW]); bw=bx1-bx0; bcx=(bx0+bx1)/2
# 大きさの 目安：ext2 の ふつうの顔（0行0列）の 体の はば
src={k:np.array(Image.open(k+'.png').convert('RGB')).astype(float) for k in ['ext1','ext2','ext3']}
def tile(k,r,c):
    a=src[k][r*360:(r+1)*360, c*256:(c+1)*256].copy(); t=key(a)
    if (k,r,c)==('ext1',1,0):   # ごはんの 海藻は 緑なので、左下だけ にじみ消しを ゆるめて 色を もどす
        h,w=t.shape[:2]; reg=np.zeros((h,w),bool); reg[int(h*.5):, :int(w*.42)]=True
        g=a[...,1]; leaf=reg & (g<205) & (g>a[...,0]+20) & (g>a[...,2]+20) & (t[...,3]>0)
        for ch,(m,o) in enumerate([(.7,45),(.8,40),(.7,60)]): t[...,ch][leaf]=np.clip(a[...,ch][leaf]*m+o,0,255)
        t[...,3][leaf]=255
    return t
rx0,rx1,_,_=body_box(tile('ext2',0,0)); S=bw/(rx1-rx0)
n=10+len(PICK); rows=(n+4)//5
sheet=Image.new('RGBA',(CW*5,CH*rows),(0,0,0,0)); sheet.paste(base,(0,0))
for i,(k,r,c) in enumerate(PICK):
    t=Image.fromarray(tile(k,r,c),'RGBA'); t=t.resize((round(t.width*S),round(t.height*S)),Image.LANCZOS); ta=np.array(t)
    x0,x1,y0,y1=body_box(ta); cx=(x0+x1)/2
    f=10+i; ox=(f%5)*CW + round(bcx-cx); oy=(f//5)*CH + (by1-y1)
    cell=Image.new('RGBA',(CW,CH),(0,0,0,0)); cell.paste(t,(round(bcx-cx),by1-y1)); sheet.paste(cell,((f%5)*CW,(f//5)*CH))
sheet.quantize(colors=256,method=Image.FASTOCTREE,dither=Image.NONE).save('../../umimi-sprites.png',optimize=True)
print('scale',round(S,3),'frames',n,'sheet',sheet.size,'ground',by1)
