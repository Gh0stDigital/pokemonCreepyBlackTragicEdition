# Creepy Black Mu v26: BLACK's battle back picture without the "square": the silhouette is scaled to 80%, centred with a
# margin, and its GHOST-style halo is smaller (red_ghost_fusion.fuse_back_soft), so neither reaches the 32x32 picture edges.
# Repoints the three users of the back picture: BLACK's header, YOU-as-BLACK's header (bank E) and the battle intro stub (F).
# Logged patches on top of verified Mu v25 (patchlib).
import io,json,sys
from patchlib import *
from patchguard import fo
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
import red_ghost_fusion as FUSION

V25_SHA='8e06876abf0db4af57388b0319d0f169076470037bd6d305c96b0a5baa26c8e9'
rom=Rom('Creepy_Black_Mu_v25.gb',V25_SHA)
r=rom.r
P23=json.load(open(ROOT/'manifest_v23.json'))['pics']
OLD_BACK=0x41c0+P23['mirage_front']                  # the v23 fusion back picture (2D:42BD)
NEW_BACK=0x6e00
def tobytes(g):
    H,W=len(g),len(g[0]);out=bytearray()
    for tx in range(W//8):
        for ty in range(H//8):
            for y in range(8):
                lo=hi=0
                for x in range(8):c=g[ty*8+y][tx*8+x];lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
                out+=bytes([lo,hi])
    return bytes(out)
d=tobytes(FUSION.fuse_back_soft(bytes(r),0.8,2,4))
packed=bytes(pic.compress(d));assert bytes(pic.decompress(io.BytesIO(packed)))==d and packed[0]==0x44
rom.put(fo(0x2d,NEW_BACK),packed,'Bank 2D: BLACK back picture v26 (80%%, small halo; %d bytes)'%len(packed))
new=bytes.fromhex(le(NEW_BACK));old=bytes.fromhex(le(OLD_BACK))
# bank E: BLACK header (back pointer at +12) and YOU-as-BLACK header (front+back at +10)
E0,E1=fo(0xe,0x7e41),fo(0xe,0x8000)
black_hdr=bytes([100,110,100,110,160,8,8,3,255,0x77])+bytes.fromhex(le(0x41c0))+old
i=bytes(r).find(black_hdr,E0,E1);assert i>0
rom.data(i+12,new,'BLACK header: back picture -> v26',old)
you_black=bytes([15,5,5,5,5,0,0,0,0,0x44])+old*2
j=bytes(r).find(you_black,E0,E1);assert j>0
rom.data(j+10,new*2,'YOU-as-BLACK header: pictures -> v26',old*2)
# bank F: LoadPlayerBackPic stub (ld de,<back>) at F:7CED
stub=fo(0xf,0x7ced);k=bytes(r).find(bytes([0x11])+old,stub,stub+19);assert k>0
rom.data(k+1,new,'LoadPlayerBackPic stub: BLACK back picture -> v26',old)
rom.finish('Creepy_Black_Mu_v26.gb','manifest_v26.json','CREEPY MU V26',extra=dict(back_pic=dict(addr=hex(NEW_BACK),bytes=len(packed))))
