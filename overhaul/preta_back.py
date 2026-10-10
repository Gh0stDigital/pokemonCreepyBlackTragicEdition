# PRETA (fossil KABUTOPS) back picture variants for v32: grey shading on the black-and-white v8 picture.
import io,sys
sys.path.insert(0,'../ref');import pic
from patchguard import fo
BACK=(0xb,0x7f3c)
def grid(raw,w=4,h=4):
    g=[[0]*(w*8) for _ in range(h*8)];i=0
    for tx in range(w):
        for ty in range(h):
            for y in range(8):
                lo,hi=raw[i],raw[i+1];i+=2
                for x in range(8):g[ty*8+y][tx*8+x]=((lo>>(7-x))&1)|(((hi>>(7-x))&1)<<1)
    return g
def raw(g,w=4,h=4):
    out=bytearray()
    for tx in range(w):
        for ty in range(h):
            for y in range(8):
                lo=hi=0
                for x in range(8):c=g[ty*8+y][tx*8+x];lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
                out+=bytes([lo,hi])
    return bytes(out)
def load(path):
    r=open(path,'rb').read();return grid(bytes(pic.decompress(io.BytesIO(r),offset=fo(*BACK))))
def variant(cur,v6,v7,k):
    """cur = v8 black/white; v7 had dark-grey rib lines, v6 also light-grey patches"""
    out=[row[:] for row in cur]
    for y in range(32):
        for x in range(32):
            if cur[y][x]!=0:continue
            if k in ('A','C') and v7[y][x]==2:out[y][x]=1        # rib lines in light grey
            if k=='B' and v7[y][x]==2:out[y][x]=2                # rib lines in dark grey (= v7)
            if k=='C' and v6[y][x]==1:out[y][x]=1                # + v6's light patches
    return out
