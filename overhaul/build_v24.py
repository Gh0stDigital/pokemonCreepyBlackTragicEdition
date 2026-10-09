# Creepy Black Mu v24: the MIRAGE ????? (species 7A, caught in the v23 ritual) keeps the Mirage's own look: the
# blacked-out silhouette that the random Mirage encounters show (class 13 pic, 13:7FA5) as its front pic, and the same
# silhouette mirrored and scaled to 32x32 as its back pic. The RED+GHOST fusion pics v23 used are for the BLACK TAMER
# (a separate thing, not built yet); they stay in 2D:41C0 unused.
# Logged patches on top of verified Mu v23 (patchlib).
import io,json,sys
from patchlib import *
from patchguard import fo
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
from PIL import Image
import red_ghost_fusion as F

V23_SHA='04fb2d3cdb63ffe4cb3b9776da5bb12d6426d58393833d0158250e4aeadcd4d0'
rom=Rom('Creepy_Black_Mu_v23.gb',V23_SHA)
r=rom.r
MIR=0x7a
P23=json.load(open(ROOT/'manifest_v23.json'))['pics']
OLD_FRONT=0x41c0;OLD_BACK=OLD_FRONT+P23['mirage_front']

def tobytes(g):
    H,W=len(g),len(g[0]);out=bytearray()
    for tx in range(W//8):
        for ty in range(H//8):
            for y in range(8):
                lo=hi=0
                for x in range(8):c=g[ty*8+y][tx*8+x];lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
                out+=bytes([lo,hi])
    return bytes(out)
def packed(d):
    c=bytes(pic.compress(d));assert bytes(pic.decompress(io.BytesIO(c)))==d;return c

sil=F.grid(bytes(r),0x13,0x7fa5)                                  # the Mirage trainer pic (v11), 7x7
assert r[fo(0x13,0x7fa5)]==0x77 and set(v for row in sil for v in row)<={0,3}
front=packed(tobytes(sil))
# back: the silhouette mirrored (seen from behind) and scaled to the 32x32 back-pic size, pure black
ys=[y for y in range(56) for x in range(56) if sil[y][x]];xs=[x for y in range(56) for x in range(56) if sil[y][x]]
y0,y1,x0,x1=min(ys),max(ys),min(xs),max(xs)
im=Image.new('L',(x1-x0+1,y1-y0+1),255)
for y in range(y0,y1+1):
    for x in range(x0,x1+1):
        if sil[y][x]:im.putpixel((x-x0,y-y0),0)
im=im.transpose(Image.FLIP_LEFT_RIGHT);w=max(1,round(im.width*32/im.height))
sm=im.resize((w,32),Image.BOX).point(lambda v:0 if v<160 else 255);bk=Image.new('L',(32,32),255);bk.paste(sm,((32-w)//2,0))
back=packed(tobytes([[3 if bk.getpixel((x,y))==0 else 0 for x in range(32)] for y in range(32)]))
NEW_FRONT=OLD_BACK+P23['mirage_back'];NEW_BACK=NEW_FRONT+len(front)
rom.put(fo(0x2d,NEW_FRONT),front+back,'Bank 2D: ????? front = Mirage silhouette, back = it mirrored at 32x32')

# ????? header (bank E, from v23): front/back pointers
hdr=bytes([60,65,60,110,130,8,8,3,200,0x77])+bytes.fromhex(le(OLD_FRONT)+le(OLD_BACK))
o=bytes(r).find(hdr,fo(0xe,0x7de0),fo(0xe,0x8000));assert o>0
rom.data(o+10,bytes.fromhex(le(NEW_FRONT)+le(NEW_BACK)),'????? header: front/back pics -> Mirage silhouette',le(OLD_FRONT)+le(OLD_BACK))

rom.finish('Creepy_Black_Mu_v24.gb','manifest_v24.json','CREEPY MU V24',
           extra=dict(pics=dict(front=hex(NEW_FRONT),front_len=len(front),back=hex(NEW_BACK),back_len=len(back))))
