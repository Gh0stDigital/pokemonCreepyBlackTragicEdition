# Build 32x32 Gen-1 back sprites from the fossil front pics (crop, scale, mirror, 4 shades).
import sys,io;sys.path.insert(0,'.')
import pic
from PIL import Image
r=open('../overhaul/Creepy_Black_Mu_v3.gb','rb').read()
def load(off):
    d=bytes(pic.decompress(io.BytesIO(r),offset=off));n=int((len(d)//16)**0.5)
    px=[[0]*(n*8) for _ in range(n*8)]
    for t in range(n*n):
        tx,ty=t//n,t%n
        for row in range(8):
            b0=d[t*16+row*2];b1=d[t*16+row*2+1]
            for x in range(8):px[ty*8+row][tx*8+x]=((b0>>(7-x))&1)|(((b1>>(7-x))&1)<<1)
    return px
def to_img(px):
    h=len(px);w=len(px[0]);im=Image.new('L',(w,h))
    for y in range(h):
        for x in range(w):im.putpixel((x,y),[255,170,85,0][px[y][x]])
    return im
def encode(im):
    s=bytearray(256)
    for t in range(16):
        tx,ty=t//4,t%4
        for row in range(8):
            lo=hi=0
            for x in range(8):
                v=im.getpixel((tx*8+x,ty*8+row));c={255:0,170:1,85:2,0:3}[v]
                lo|=(c&1)<<(7-x);hi|=(c>>1)<<(7-x)
            s[t*16+row*2]=lo;s[t*16+row*2+1]=hi
    return pic.compress(bytes(s))
def make(off,name):
    src=to_img(load(off));bbox=src.point(lambda v:255 if v<255 else 0).getbbox()
    c=src.crop(bbox);w,h=c.size;k=32/max(w,h)
    nw,nh=max(1,round(w*k)),max(1,round(h*k))
    # area-average then snap to the 4 GB shades
    sm=c.resize((nw,nh),Image.BOX).point(lambda v:[255,170,85,0][min(3,int((255-v)/64+0.35))])
    sm=sm.transpose(Image.FLIP_LEFT_RIGHT)
    out=Image.new('L',(32,32),255);out.paste(sm,((32-nw)//2,32-nh))
    comp=bytes(encode(out));print(name,'bbox',bbox,'->',(nw,nh),'compressed',len(comp))
    open(name+'_back.bin','wb').write(comp);out.save(name+'_back.png')
    big=Image.new('L',(64*2+56*2+20,112),255);big.paste(src.resize((src.width*2,src.height*2),Image.NEAREST),(0,0));big.paste(out.resize((64,64),Image.NEAREST).resize((128,128),Image.NEAREST).crop((0,0,128,112)),(src.width*2+20,0))
    big.save(name+'_compare.png')
make(0x0b*0x4000+0x79e8-0x4000,'kab')
make(0x0d*0x4000+0x6536-0x4000,'aero')
