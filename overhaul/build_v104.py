# Creepy Black Mu v104 (on v103): the eye moved two rows down and one left, out of the hat (rows 11-12). Originally v103: BLACK's battle back picture shows one white eye on the right side of the head (side view, the same
# slanted eye as his map sprite's side frames: two pixels, then one lower toward the front). The v37 silhouette + halo is unchanged
# otherwise; the picture is rewritten in place at 2D:7A00 (114 bytes; v37's was 112, the two bytes after it were free).
# Pixel grid (32x32, colours 0 white .. 3 black): assets/BlackBackEye/black_back_v104.json.
import io,sys,json
from patchlib import *
from patchguard import fo
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
V103_SHA='77f3a31d1e52100ff981ad5289adec0c1592d20deea135cbbbb3efbca240c914'
rom=Rom('Creepy_Black_Mu_v103.gb',V103_SHA)
R=bytes(rom.r)
AT=0x7a00;OLD_LEN=114
OLDEYE=[(9,17),(9,18),(10,19)];EYE=[(11,16),(11,17),(12,18)]
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
for y,x in OLDEYE:assert g[y][x]==0;g[y][x]=3          # v103's eye (in the hat) back to black
for y,x in EYE:assert g[y][x]==3;g[y][x]=0
assert g==json.load(open(ROOT/'assets/BlackBackEye/black_back_v104.json'))
d=tobytes(g);new=bytes(pic.compress(d));assert bytes(pic.decompress(io.BytesIO(new)))==d
assert len(new)<=OLD_LEN or not any(R[o+OLD_LEN:o+len(new)])
rom.data(o,new+bytes(max(0,OLD_LEN-len(new))),"BLACK's back picture: white eye two rows lower (under the hat)",old+bytes(max(0,len(new)-OLD_LEN)))
rom.finish('Creepy_Black_Mu_v104.gb','manifest_v104.json','CREEPY MU V104',extra=dict(back_pic=dict(addr=hex(AT),bytes=len(new),eye=EYE)))
