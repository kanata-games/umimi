from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
a=np.array(Image.open('src.png').convert('RGB')).astype(float)
r,g,b=a[...,0],a[...,1],a[...,2]
G=np.array([12,235,18.])
d=g-np.maximum(r,b)
alpha=np.clip(1-np.clip(d,0,None)/205,0,1)
alpha[alpha<0.07]=0
F=(a-(1-alpha[...,None])*G)/np.maximum(alpha[...,None],1e-3)
F=np.clip(F,0,255)
# final despill: green never exceeds max(r,b)+25
F[...,1]=np.minimum(F[...,1],np.maximum(F[...,0],F[...,2])+25)
rgba=np.dstack([F,alpha*255]).astype(np.uint8)
im=Image.fromarray(rgba,'RGBA')
eyes=[(108.1,236.6),(354.3,242.8),(594.5,242.7),(855.6,243.0),(1115.0,245.9),(114.6,507.2),(356.5,508.2),(603.6,518.0),(854.6,521.4),(1108.1,516.6)]
L,R,U,D=95,150,142,80
CW,CH=L+R,U+D
sheet=Image.new('RGBA',(CW*5,CH*2),(0,0,0,0))
lum=a.mean(2)
info=[]
for i,(ex,ey) in enumerate(eyes):
  ex,ey=round(ex),round(ey)
  crop=im.crop((ex-L,ey-U,ex+R,ey+D))
  sheet.paste(crop,((i%5)*CW,(i//5)*CH))
  # left eye search
  sub=(lum[ey-15:ey+15, ex-55:ex-20]<80)
  lab,n=ndimage.label(sub); 
  if n:
    sz=ndimage.sum(sub,lab,range(1,n+1)); j=int(np.argmax(sz)); cy,cx=ndimage.center_of_mass(sub,lab,j+1)
    info.append((round(cx+ex-55-ex,1),round(cy+ey-15-ey,1),int(sz[j])))
  else: info.append(None)
print('cell',CW,CH,'anchor',L,U); print('left eye offsets',info)
sheet.save('umimi-sprites.png',optimize=True)
# preview on game bg
pv=Image.new('RGBA',sheet.size,(198,207,244,255)); pv.alpha_composite(sheet)
dr=ImageDraw.Draw(pv)
for i in range(10):
  x0,y0=(i%5)*CW,(i//5)*CH; dr.rectangle([x0,y0,x0+CW-1,y0+CH-1],outline=(150,150,200)); dr.line([x0+L-4,y0+U,x0+L+4,y0+U],fill='red'); dr.text((x0+4,y0+4),str(i),fill='black')
pv.convert('RGB').save('preview_sheet.png')
