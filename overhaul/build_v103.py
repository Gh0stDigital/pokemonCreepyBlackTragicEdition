# Creepy Black Mu v103 (on v102): BLACK's battle back picture shows one white eye on the right side of the head (side view, the same
# slanted eye as his map sprite's side frames: two pixels, then one lower toward the front). The v37 silhouette + halo is unchanged
# otherwise; the picture is rewritten in place at 2D:7A00 (114 bytes; v37's was 112, the two bytes after it were free).
# Pixel grid (32x32, colours 0 white .. 3 black): assets/BlackBackEye/black_back_v103.json.
import io,sys,json
from patchlib import *
from patchguard import fo
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
V102_SHA='2ef6562d4b02adcbc5bfd1543a9d244e741b94a6d2354ee011c99003e9c0882c'
rom=Rom('Creepy_Black_Mu_v102.gb',V102_SHA)
R=bytes(rom.r)
AT=0x7a00;OLD_LEN=112
EYE=[(9,17),(9,18),(10,19)]
def tobytes(g):
    out=bytearray()
    for tx in range(4):
        for ty in range(4):
            for y in range(8):
                lo=hi=0
                for x in range(8):c=g[ty*8+y][tx*8+x];lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
                out+=bytes([lo,hi])
    return bytes(out)
def frombytes(d):
    g=[[0]*32 for _ in range(32)];k=0
    for tx in range(4):
        for ty in range(4):
            for y in range(8):
                lo,hi=d[k],d[k+1];k+=2
                for x in range(8):g[ty*8+y][tx*8+x]=((lo>>(7-x))&1)|(((hi>>(7-x))&1)<<1)
    return g
o=fo(0x2d,AT);old=R[o:o+OLD_LEN]
g=frombytes(bytes(pic.decompress(io.BytesIO(old))))
for y,x in EYE:assert g[y][x]==3;g[y][x]=0
assert g==json.load(open(ROOT/'assets/BlackBackEye/black_back_v103.json'))
d=tobytes(g);new=bytes(pic.compress(d));assert bytes(pic.decompress(io.BytesIO(new)))==d
assert len(new)<=OLD_LEN+2 and not any(R[o+OLD_LEN:o+len(new)])
rom.data(o,new,"BLACK's back picture: white eye on the right side of the head (side view)",old+bytes(len(new)-OLD_LEN))
rom.finish('Creepy_Black_Mu_v103.gb','manifest_v103.json','CREEPY MU V103',extra=dict(back_pic=dict(addr=hex(AT),bytes=len(new),eye=EYE)))
