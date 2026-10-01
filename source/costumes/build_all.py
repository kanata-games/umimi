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
# 2026-10 ピッちゃん（ChatGPT）作の39種。1枚に4種×2コマで届いたものを src/ に1種ずつ切り出し済み。目は MANEYE で指定
SRC.update({k:k for k in ['kinoko', 'dragonarmor', 'mummy', 'diver', 'pumpkin', 'knight', 'obake', 'mahouhood', 'hibiscus', 'pumpkinhood', 'mintdress', 'forest', 'clover', 'ranger', 'darkwitch', 'dragonknight', 'pinkprincess', 'wizard', 'saint', 'hero', 'sakuradress', 'marine', 'starwizard', 'snow', 'ume', 'painter', 'circus', 'angel3', 'harugi', 'headphone', 'alice', 'prince', 'sumire', 'marine2', 'ichigocake', 'patchwork', 'queen', 'sweets', 'toy']})
MANEYE={'devil2':(517,520,586,522),'gothic':(456,516,538,521)}
MANEYE.update({'kinoko': (45, 202, 101, 206), 'dragonarmor': (55, 219, 111, 223), 'mummy': (55, 204, 111, 208), 'diver': (55, 195, 111, 199), 'pumpkin': (55, 172, 111, 176), 'knight': (55, 190, 111, 194), 'obake': (50, 168, 106, 172), 'mahouhood': (55, 179, 111, 183), 'hibiscus': (49, 162, 105, 168), 'pumpkinhood': (49, 186, 106, 193), 'mintdress': (59, 165, 116, 169), 'forest': (48, 163, 105, 170), 'clover': (61, 165, 117, 170), 'ranger': (53, 173, 109, 178), 'darkwitch': (59, 192, 115, 198), 'dragonknight': (56, 176, 112, 181), 'pinkprincess': (48, 169, 104, 175), 'wizard': (48, 171, 103, 177), 'saint': (51, 181, 107, 186), 'hero': (52, 160, 107, 166), 'sakuradress': (52, 175, 111, 182), 'marine': (51, 175, 110, 182), 'starwizard': (51, 174, 111, 181), 'snow': (51, 172, 110, 179), 'ume': (46, 155, 101, 163), 'painter': (46, 158, 100, 165), 'circus': (62, 236, 123, 234), 'angel3': (46, 173, 101, 180), 'harugi': (56, 178, 118, 186), 'headphone': (52, 177, 114, 186), 'alice': (56, 178, 117, 188), 'prince': (52, 180, 115, 190), 'sumire': (52, 179, 114, 186), 'marine2': (52, 178, 114, 186), 'ichigocake': (51, 181, 114, 187), 'patchwork': (52, 179, 113, 186), 'queen': (46, 163, 101, 170), 'sweets': (52, 163, 107, 169), 'toy': (54, 165, 109, 171)})
# 顔がかくれている衣装（まばたきを描かない）。目の位置は体の大きさからの見当
# 2026-10 2回目（ピッちゃん作）35種
MANEYE.update({'teahat': (49, 162, 103, 167), 'detective': (65, 161, 119, 166), 'cyber': (51, 165, 105, 171), 'starangel': (53, 176, 109, 182), 'tiara': (50, 155, 103, 160), 'strawdress': (48, 156, 101, 161), 'blackmaid': (47, 157, 100, 162), 'planet': (47, 158, 100, 164), 'akiha': (53, 159, 109, 164), 'candy': (52, 160, 108, 166), 'yozora': (51, 163, 107, 168), 'fox': (51, 162, 108, 166), 'candycorn': (59, 200, 116, 207), 'spider': (61, 188, 119, 194), 'scarecrow': (84, 190, 141, 197), 'hbunny': (59, 202, 118, 211), 'mummyhood': (78, 201, 136, 208), 'blackcat': (60, 194, 117, 201), 'bat': (63, 191, 120, 197), 'usagihood': (65, 164, 112, 171), 'bard': (48, 172, 102, 175), 'thief': (67, 161, 121, 167), 'flameknight': (52, 164, 106, 170), 'sakuraangel': (48, 181, 103, 186), 'starsailor': (50, 169, 104, 175), 'leafdress': (59, 168, 114, 174), 'nightwitch': (56, 175, 111, 181), 'lion': (72, 191, 128, 197), 'panda': (64, 190, 120, 192), 'giraffe': (63, 186, 119, 192), 'penguin': (63, 188, 119, 194), 'elephant': (70, 195, 127, 202), 'zebra': (62, 193, 117, 200), 'monkey': (78, 188, 134, 195), 'flamingo': (67, 223, 123, 231)})
SRC.update({k:k for k in ['teahat', 'detective', 'cyber', 'starangel', 'tiara', 'strawdress', 'blackmaid', 'planet', 'akiha', 'candy', 'yozora', 'fox', 'candycorn', 'spider', 'scarecrow', 'hbunny', 'mummyhood', 'blackcat', 'bat', 'usagihood', 'bard', 'thief', 'flameknight', 'sakuraangel', 'starsailor', 'leafdress', 'nightwitch', 'lion', 'panda', 'giraffe', 'penguin', 'elephant', 'zebra', 'monkey', 'flamingo']})
NEWSET=set(MANEYE)-{'devil2','gothic'}
NOEYE=set(['kinoko', 'dragonarmor', 'mummy', 'diver', 'pumpkin', 'knight', 'obake', 'mahouhood'])
SCALEFIX={'giraffe':.94,'bath':.9,'maid':1.22,'hoodie':.92,'jugoya':.8,'zansho':.88,'camping':.92,'goldfish':.92,'ghostmaid':.92}
S=0.8; CW,CH=240,208  # stored cell (scale-1 coords 300x260)
EX,EY=130,165          # right-eye position in scale-1 cell coords
# 分類ごとに別シート c_<分類>.png にする（ゲーム側は使うときだけ読み込む）。新しい衣装は SRC と CAT の両方に足す
CAT={'animal':['bear','chick','dog','cat','rabbit',
   'usagihood','fox','lion','panda','giraffe','penguin','elephant','zebra','monkey','flamingo'],
 'food':['strawberry','lemon','matcha','blueberry','mango','grape','ichigocake','sweets','teahat','strawdress','candy'],
 'season':['sakura','randoseru','yukata','goldfish','asagao','higanbana','jugoya','momiji','witch','santa','newyear',
           'sakuradress','hibiscus','pumpkin','pumpkinhood','obake','mummy','snow','ume','harugi',
           'akiha','scarecrow','candycorn','spider','hbunny','mummyhood','blackcat','bat','sakuraangel'],
 'work':['explorer','chef','nurse','musician','delivery','miko','idol','maid','painter','circus','diver','detective','bard'],
 'fashion':['ribbon','flower','crown','sailor','knit','hoodie','gothic','marine','marine2','headphone','alice','patchwork','toy','cyber','blackmaid'],
 'relax':['pajama','bath','camping','raincoat','kinoko','forest','leafdress'],
 'dream':['constellation','space','angel','devil','ghostmaid','angel3','starangel','planet','yozora','starsailor'],
 'adv':['knight','hero','ranger','wizard','starwizard','mahouhood','darkwitch','dragonarmor','dragonknight','thief','flameknight','nightwitch'],
 'princess':['pinkprincess','sumire','queen','prince','mintdress','clover','saint','tiara']}
_all=[k for v in CAT.values() for k in v]; assert sorted(_all)==sorted(SRC), set(_all)^set(SRC)
cols=4; cells={}; meta={}
for k in SRC:
    n=SRC[k]; a=load(n); G=bgcolor(a); rgba,dist=key(a,G); im=Image.fromarray(rgba,'RGBA')
    fg=dist>80
    if n in NEWSET:
        # 新しい39種：左のコマの体だけを使う（となりのコマのキラキラの切れはしは消す）
        lab,kk=ndimage.label(ndimage.binary_dilation(fg,iterations=2)); sz=ndimage.sum(fg,lab,range(1,kk+1)); objs=ndimage.find_objects(lab)
        j=min([j for j in np.argsort(sz)[::-1][:3] if sz[j]>sz.max()*.3],key=lambda j:objs[j][1].start)
        body=(lab==j+1); rgba=rgba.copy(); rgba[...,3]=np.where(body,rgba[...,3],0); im=Image.fromarray(rgba,'RGBA')
        sl=objs[j]; box=(sl[1].start,sl[1].stop,sl[0].start,sl[0].stop)
    else:
      try: box=halves(fg)[0]
      except Exception:
        lab,kk=ndimage.label(fg); sz=ndimage.sum(fg,lab,range(1,kk+1)); objs=ndimage.find_objects(lab)
        s0=sorted([objs[j] for j in np.argsort(sz)[::-1][:2]],key=lambda s:s[1].start)[0]; box=(s0[1].start,s0[1].stop,s0[0].start,s0[0].stop); print('fallback',k)
    if n in MANEYE: lx,ly,rx,ry=MANEYE[n]; e=[(1,lx,ly),(1,rx,ry)]
    else: e=eyes(a,box)
    L,Rr=e; sc=39.0/(Rr[1]-L[1])*SCALEFIX.get(n,1)
    if n in NOEYE:   # 顔がかくれている子は体の幅でそろえ、目の位置は見当（顔の出ている子の平均）
        sc=39.0*5.45/(box[1]-box[0])*SCALEFIX.get(n,1); lx=box[0]+21/sc; yy=box[3]-82/sc; L,Rr=(1,lx,yy),(1,lx+39/sc,yy)
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
    cells[k]=cell
    meta[k]={'ne':1} if n in NOEYE else {}
    meta[k].update({'g':round(float(ground),1),'lid':'#%02x%02x%02x'%tuple(lid),'le':[round(float(ldx),1),round(float(ldy),1)]})
pv_all=[]
for cat,ks in CAT.items():
    rows=(len(ks)+cols-1)//cols; sheet=Image.new('RGBA',(CW*cols,CH*rows),(0,0,0,0))
    for i,k in enumerate(ks):
        sheet.paste(cells[k],((i%cols)*CW,(i//cols)*CH)); meta[k]['s']=cat; meta[k]['i']=i
    q=sheet.quantize(colors=256,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE)
    q.save('../../c_%s.png'%cat,optimize=True)
    pv=Image.new('RGBA',sheet.size,(198,207,244,255)); pv.alpha_composite(q.convert('RGBA')); d=ImageDraw.Draw(pv)
    for i,k in enumerate(ks):
        X=(i%cols)*CW; Y=(i//cols)*CH; d.text((X+4,Y+4),k,fill='black'); gy=Y+meta[k]['g']*S; d.line([X+60,gy,X+200,gy],fill=(255,0,0))
    pv.convert('RGB').save('preview-%s.png'%cat)
json.dump({'cw':CW,'ch':CH,'cols':cols,'s':S,'ex':EX,'ey':EY,'m':meta},open('costumes.json','w'))
print(len(meta))
