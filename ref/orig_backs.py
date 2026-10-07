import sys,io;sys.path.insert(0,'.')
import pic
from PIL import Image
r=open('../overhaul/Creepy_Black_Mu_v4.gb','rb').read()
BASE=0x383e4   # CB BaseStats (bank E 43e4), 28 bytes per dex entry
def bank_for(idx):
    if idx==0x15:return 1
    if idx==0x1f:return 0x2d
    if idx==0xb6:return 0xb
    if idx<0x1f:return 9
    if idx<0x4a:return 0xa
    if idx<0x74:return 0xb
    if idx<0x99:return 0xc
    return 0xd
def decode(off):
    d=bytes(pic.decompress(io.BytesIO(r),offset=off));n=int((len(d)//16)**0.5);px=[[0]*(n*8) for _ in range(n*8)]
    for t in range(n*n):
        tx,ty=t//n,t%n
        for row in range(8):
            b0=d[t*16+row*2];b1=d[t*16+row*2+1]
            for x in range(8):px[ty*8+row][tx*8+x]=((b0>>(7-x))&1)|(((b1>>(7-x))&1)<<1)
    return px
def img(px,s=4):
    h=len(px);w=len(px[0]);im=Image.new('L',(w,h))
    for y in range(h):
        for x in range(w):im.putpixel((x,y),[255,170,85,0][px[y][x]])
    return im.resize((w*s,h*s),Image.NEAREST)
info={}
for name,dex,idx in (('kabutops',141,0x5b),('aerodactyl',142,0xab)):
    e=BASE+28*(dex-1);hdr=r[e:e+28];front=hdr[11]|hdr[12]<<8;back=hdr[13]|hdr[14]<<8;b=bank_for(idx)
    fo=b*0x4000+front-0x4000;bo=b*0x4000+back-0x4000
    import pic as P
    comp_len=len(P.compress(bytes(P.decompress(io.BytesIO(r),offset=bo))))
    info[name]=dict(dex=hdr[0],bank=b,front=hex(front),back=hex(back),back_compressed_est=comp_len)
    print(name,info[name])
    img(decode(fo),2).save(name+'_front.png');img(decode(bo),4).save(name+'_back_orig.png')
    import pickle;pickle.dump(decode(bo),open(name+'_back.pkl','wb'))
kf=img(decode(0x0b*0x4000+0x79e8-0x4000),2);af=img(decode(0x0d*0x4000+0x6536-0x4000),2)
W=Image.new('L',(130*4+10,300),255)
for i,(a,b) in enumerate(((Image.open('kabutops_front.png'),kf),(Image.open('aerodactyl_front.png'),af))):
    W.paste(a,(i*260,0));W.paste(b,(i*260+125,0))
W.paste(Image.open('kabutops_back_orig.png'),(0,150));W.paste(Image.open('aerodactyl_back_orig.png'),(260,150))
W.save('orig_vs_fossil.png')
