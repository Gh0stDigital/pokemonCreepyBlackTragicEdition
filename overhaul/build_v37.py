# Creepy Black Mu v37: BLACK's battle back picture fits the battle screen. The screen shows only the top-left 28x28 of a
# 32x32 back picture (7x7 tiles, like RED's own back pic, which is exactly 28x28); v27 had nudged the silhouette 2 px right /
# 4 px down and drawn the halo around it, so its right side and bottom were cut off in battle. Same silhouette + halo as v27,
# scaled so both fit the visible 28x28 (24 px wide + 2 px halo each side, flush with the bottom): red_ghost_fusion.fuse_back_fit.
# Repoints the three users of the back picture (BLACK's header, YOU-as-BLACK's header, the battle intro stub), as v27 did.
import io,sys
from patchlib import *
from patchguard import fo
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
import red_ghost_fusion as FUSION

V36_SHA='c2179afa6a02cf44771854f82e55b47482d2a2a9214eed99c0a7e04f239d005a'
rom=Rom('Creepy_Black_Mu_v36.gb',V36_SHA)
r=rom.r
OLD_BACK=0x6f00                                       # the v27 back picture
NEW_BACK=0x7a00
def tobytes(g):
    H,W=len(g),len(g[0]);out=bytearray()
    for tx in range(W//8):
        for ty in range(H//8):
            for y in range(8):
                lo=hi=0
                for x in range(8):c=g[ty*8+y][tx*8+x];lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
                out+=bytes([lo,hi])
    return bytes(out)
g=FUSION.fuse_back_fit(bytes(r))
assert not any(g[y][x] for y in range(32) for x in range(32) if y>=FUSION.VIS or x>=FUSION.VIS)
d=tobytes(g)
packed=bytes(pic.compress(d));assert bytes(pic.decompress(io.BytesIO(packed)))==d and packed[0]==0x44
rom.put(fo(0x2d,NEW_BACK),packed,'Bank 2D: BLACK back picture v37 (fits the visible 28x28; %d bytes)'%len(packed))
new=bytes.fromhex(le(NEW_BACK));old=bytes.fromhex(le(OLD_BACK))
E0,E1=fo(0xe,0x7e41),fo(0xe,0x8000)
black_hdr=bytes([100,110,100,110,160,8,8,3,255,0x77])+bytes.fromhex(le(0x41c0))+old
i=bytes(r).find(black_hdr,E0,E1);assert i>0
rom.data(i+12,new,'BLACK header: back picture -> v37',old)
you_black=bytes([15,5,5,5,5,0,0,0,0,0x44])+old*2
j=bytes(r).find(you_black,E0,E1);assert j>0
rom.data(j+10,new*2,'YOU-as-BLACK header: pictures -> v37',old*2)
stub=fo(0xf,0x7ced);k=bytes(r).find(bytes([0x11])+old,stub,stub+19);assert k>0
rom.data(k+1,new,'LoadPlayerBackPic stub: BLACK back picture -> v37',old)
rom.finish('Creepy_Black_Mu_v37.gb','manifest_v37.json','CREEPY MU V37',extra=dict(back_pic=dict(addr=hex(NEW_BACK),bytes=len(packed))))
