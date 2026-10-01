from PIL import Image
names=['shelltile','pinkwood','pearlstripe','pearlnight']; T=256
sheet=Image.new('RGB',(T*len(names),T))
for i,n in enumerate(names):
    im=Image.open(f'src/tex_{n}.png').convert('RGB').resize((T,T),Image.LANCZOS); sheet.paste(im,(i*T,0))
sheet.quantize(colors=200,method=Image.MEDIANCUT,dither=Image.NONE).save('../../roomtex.png',optimize=True)
# seam preview: 2x2 tiling of each
pv=Image.new('RGB',(T*2*len(names)+10*len(names),T*2),'white')
for i,n in enumerate(names):
    t=sheet.crop((i*T,0,(i+1)*T,T))
    for a in (0,1):
        for b in (0,1): pv.paste(t,(i*(2*T+10)+a*T,b*T))
pv.save('tex_preview.png')
