import sys,io;sys.path.insert(0,'.')
from make_backs import load,to_img,encode
from PIL import Image
srcs={'kab':to_img(load(0x0b*0x4000+0x79e8-0x4000)),'aero':to_img(load(0x0d*0x4000+0x6536-0x4000))}
for k,v in srcs.items():print(k,v.size,v.point(lambda x:255 if x<255 else 0).getbbox())
def window(name,x,y,shift_down=0):
    s=srcs[name];c=s.crop((x,y,x+32,y+32)).transpose(Image.FLIP_LEFT_RIGHT)
    out=Image.new('L',(32,32),255);out.paste(c.crop((0,0,32,32-shift_down)),(0,shift_down))
    comp=bytes(encode(out));return out,comp
opts={'kab':[(6,2,0),(8,6,0),(7,0,4)],'aero':[(0,4,0),(4,10,0),(10,14,0),(18,8,0)]}
W=Image.new('L',(4*140,2*140+20),255);res={}
for ri,(name,ws) in enumerate(opts.items()):
    for ci,(x,y,sd) in enumerate(ws):
        im,comp=window(name,x,y,sd);res[(name,ci)]=comp
        W.paste(im.resize((128,128),Image.NEAREST),(ci*140,ri*150));print(name,ci,(x,y,sd),len(comp),'bytes')
        open('%s_win%d.bin'%(name,ci),'wb').write(comp)
W.save('backs_windows.png')
# front pics for reference
F=Image.new('L',(260,120),255);F.paste(srcs['kab'].resize((96,96),Image.NEAREST),(0,0));F.paste(srcs['aero'].resize((112,112),Image.NEAREST),(120,0));F.save('fronts.png')
