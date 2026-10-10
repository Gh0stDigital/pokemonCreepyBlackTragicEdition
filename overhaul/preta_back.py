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

def outside(g):
    """white pixels connected to the picture border (background), not the body"""
    from collections import deque
    H,W=len(g),len(g[0]);bg=[[False]*W for _ in range(H)];q=deque()
    for y in range(H):
        for x in range(W):
            if (y in (0,H-1) or x in (0,W-1)) and g[y][x]==0:bg[y][x]=True;q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and not bg[ny][nx] and g[ny][nx]==0:bg[ny][nx]=True;q.append((ny,nx))
    return bg
def front_style(g,kind):
    """v33: shade the body the way the front picture does - grey gradients hugging the black lines inside the body
       D: ring 1 next to a black line = dark grey on the shadow side (black below/right), light grey elsewhere;
          ring 2 on the shadow side = light grey
       E: ring 1 light grey everywhere, dark grey only in corners (black on two sides)
       F: like D but ring 1 on the lit side stays white (only the shadow sides are shaded)"""
    H,W=len(g),len(g[0]);bg=outside(g);out=[row[:] for row in g]
    blk=lambda y,x:0<=y<H and 0<=x<W and g[y][x]==3
    for y in range(H):
        for x in range(W):
            if g[y][x]!=0 or bg[y][x]:continue
            s=blk(y+1,x) or blk(y,x+1);n=blk(y-1,x) or blk(y,x-1)
            cnt=sum((blk(y+1,x),blk(y-1,x),blk(y,x+1),blk(y,x-1)))
            if kind=='D':
                if s:out[y][x]=2
                elif n:out[y][x]=1
                elif blk(y+2,x) or blk(y,x+2):out[y][x]=1
            elif kind=='E':
                if cnt>=2:out[y][x]=2
                elif cnt==1:out[y][x]=1
            elif kind=='F':
                if s:out[y][x]=2
                elif blk(y+2,x) or blk(y,x+2):out[y][x]=1
    return out
def front_style2(g,kind):
    """gentler versions: thin white bands (1-2 px between black lines) stay white; only wider white areas get shaded.
       G: in wide areas, ring 1 on the shadow side (black below/right) = light grey, corners (black below AND right) = dark grey
       H: G plus a light-grey checker dither in ring 2 of the shadow side (the front's dithered shading)
       I: G but dark grey on all of ring 1's shadow side, light grey on ring 2's shadow side (strongest of the three)"""
    H,W=len(g),len(g[0]);bg=outside(g);out=[row[:] for row in g]
    blk=lambda y,x:0<=y<H and 0<=x<W and g[y][x]==3
    wht=lambda y,x:0<=y<H and 0<=x<W and g[y][x]==0 and not bg[y][x]
    for y in range(H):
        for x in range(W):
            if g[y][x]!=0 or bg[y][x]:continue
            bS,bE=blk(y+1,x),blk(y,x+1)
            wideS=bS and wht(y-1,x) and wht(y-2,x)          # room above for a gradient
            wideE=bE and wht(y,x-1) and wht(y,x-2)
            ring2=(blk(y+2,x) and wht(y+1,x) and wht(y-1,x)) or (blk(y,x+2) and wht(y,x+1) and wht(y,x-1))
            if kind in ('G','H'):
                if wideS and wideE:out[y][x]=2
                elif wideS or wideE:out[y][x]=1
                elif kind=='H' and ring2 and (x+y)%2==0:out[y][x]=1
            elif kind=='I':
                if wideS or wideE:out[y][x]=2
                elif ring2:out[y][x]=1
    return out
