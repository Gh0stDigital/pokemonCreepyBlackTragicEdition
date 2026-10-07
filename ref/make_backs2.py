import sys,io;sys.path.insert(0,'.')
from make_backs import load,to_img,encode
from PIL import Image
def snap(v):return 0 if v<96 else 85 if v<150 else 170 if v<215 else 255
def variant(off,scale,yshift,name):
    src=to_img(load(off));bbox=src.point(lambda v:255 if v<255 else 0).getbbox();c=src.crop(bbox)
    w,h=c.size;nw,nh=round(w*scale),round(h*scale)
    sm=c.resize((nw,nh),Image.LANCZOS).point(snap).transpose(Image.FLIP_LEFT_RIGHT)
    out=Image.new('L',(32,32),255);out.paste(sm,((32-nw)//2,32-nh+yshift))
    comp=bytes(encode(out));return out,len(comp),comp
rows=[]
for name,off in (('kab',0x0b*0x4000+0x79e8-0x4000),('aero',0x0d*0x4000+0x6536-0x4000)):
    ims=[]
    for sc,ys in ((0.70,0),(0.85,8),(1.0,14)):
        im,n,comp=variant(off,sc,ys,name);ims.append((im,n));open('%s_back_%d.bin'%(name,int(sc*100)),'wb').write(comp)
        print(name,sc,'bytes',n)
    rows.append(ims)
W=Image.new('L',(3*140,2*140),255)
for ri,ims in enumerate(rows):
    for ci,(im,n) in enumerate(ims):W.paste(im.resize((128,128),Image.NEAREST),(ci*140,ri*140))
W.save('backs_variants.png')
