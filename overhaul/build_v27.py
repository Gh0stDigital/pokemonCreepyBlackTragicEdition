# Creepy Black Mu v27: BLACK's battle back picture at FULL size again (v26 shrank it) but without the boxy look: the silhouette is nudged
# 2 px right / 4 px down so it and its small GHOST-style halo (reach 2) stay off the 32x32 edges on the top and sides (red_ghost_fusion.fuse_back_shift).
# Repoints the three users of the back picture: BLACK's header, YOU-as-BLACK's header (bank E) and the battle intro stub (F).
# Logged patches on top of verified Mu v26 (patchlib).
import io,json,sys
from patchlib import *
from patchguard import fo
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
import red_ghost_fusion as FUSION

V26_SHA='28580d1b047e392589b94a79f80a121da23b4579ee20ef874c5916ba2f11ca00'
rom=Rom('Creepy_Black_Mu_v26.gb',V26_SHA)
r=rom.r
OLD_BACK=0x6e00                                       # the v26 back picture
NEW_BACK=0x6f00
def tobytes(g):
    H,W=len(g),len(g[0]);out=bytearray()
    for tx in range(W//8):
        for ty in range(H//8):
            for y in range(8):
                lo=hi=0
                for x in range(8):c=g[ty*8+y][tx*8+x];lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
                out+=bytes([lo,hi])
    return bytes(out)
d=tobytes(FUSION.fuse_back_shift(bytes(r),2,2,4))
packed=bytes(pic.compress(d));assert bytes(pic.decompress(io.BytesIO(packed)))==d and packed[0]==0x44
rom.put(fo(0x2d,NEW_BACK),packed,'Bank 2D: BLACK back picture v27 (full size, shifted, small halo; %d bytes)'%len(packed))
new=bytes.fromhex(le(NEW_BACK));old=bytes.fromhex(le(OLD_BACK))
# bank E: BLACK header (back pointer at +12) and YOU-as-BLACK header (front+back at +10)
E0,E1=fo(0xe,0x7e41),fo(0xe,0x8000)
black_hdr=bytes([100,110,100,110,160,8,8,3,255,0x77])+bytes.fromhex(le(0x41c0))+old
i=bytes(r).find(black_hdr,E0,E1);assert i>0
rom.data(i+12,new,'BLACK header: back picture -> v27',old)
you_black=bytes([15,5,5,5,5,0,0,0,0,0x44])+old*2
j=bytes(r).find(you_black,E0,E1);assert j>0
rom.data(j+10,new*2,'YOU-as-BLACK header: pictures -> v27',old*2)
# bank F: LoadPlayerBackPic stub (ld de,<back>) at F:7CED
stub=fo(0xf,0x7ced);k=bytes(r).find(bytes([0x11])+old,stub,stub+19);assert k>0
rom.data(k+1,new,'LoadPlayerBackPic stub: BLACK back picture -> v27',old)
rom.finish('Creepy_Black_Mu_v27.gb','manifest_v27.json','CREEPY MU V27',extra=dict(back_pic=dict(addr=hex(NEW_BACK),bytes=len(packed))))
