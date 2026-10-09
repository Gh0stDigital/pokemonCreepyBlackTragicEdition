# Experiment: RED's overworld sprite (5:4180, 6 frames of 16x16 = 24 tiles) blacked out with white eyes,
# the map version of the BLACK TAMER (RED+GHOST fusion, option A0 eyes).
# Frames (pokered order): 0 down, 1 up, 2 left, 3 down walk, 4 up walk, 5 left walk (right = left mirrored).
import sys
from PIL import Image
from collections import deque
SPRITE=(5,0x4180)
def fo(b,a):return b*0x4000+a-0x4000
def frames(r):
    o=fo(*SPRITE);out=[]
    for f in range(6):
        g=[[0]*16 for _ in range(16)]
        for t,(ty,tx) in enumerate(((0,0),(0,1),(1,0),(1,1))):
            b=r[o+(f*4+t)*16:o+(f*4+t)*16+16]
            for y in range(8):
                lo,hi=b[2*y],b[2*y+1]
                for x in range(8):g[ty*8+y][tx*8+x]=((lo>>(7-x))&1)|(((hi>>(7-x))&1)<<1)
        out.append(g)
    return out
def dump(g):return '\n'.join(''.join(' .+#'[c] for c in row) for row in g)
if __name__=='__main__':
    r=open(sys.argv[1],'rb').read()
    for i,g in enumerate(frames(r)):print('frame',i);print(dump(g))

def outside(g):
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
# white eyes (colour 1 = white with the sprite palette; colour 0 would be see-through): GHOST's slanted eyes,
# outer corner up, on RED's eye rows. Walking frames sit one row lower (frame 3) like RED's own.
EYES={0:[(7,4),(7,5),(8,5),(8,6), (7,11),(7,10),(8,10),(8,9)],
      2:[(6,6),(6,7),(7,5),(7,6)]}          # side view: the slant flipped up (back corner high), one pixel back from the face
EYES[3]=[(y+1,x) for y,x in EYES[0]]           # walking frames are drawn one row lower than the standing ones
EYES[5]=[(y+1,x) for y,x in EYES[2]]
BACKPACK={1:[(10,x) for x in range(6,10)],4:[(11,x) for x in range(6,10)]}  # RED's long black line across the backpack, in white: shows it's his back
def ghost_frames(r):
    out=[]
    for i,g in enumerate(frames(r)):
        bg=outside(g);n=[[0 if bg[y][x] else 3 for x in range(16)] for y in range(16)]
        edge=lambda y,x:any(not(0<=y+dy<16 and 0<=x+dx<16) or bg[y+dy][x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
        n=[[2 if n[y][x] and edge(y,x) else n[y][x] for x in range(16)] for y in range(16)]   # grey outline
        for y,x in EYES.get(i,[])+BACKPACK.get(i,[]):
            if n[y][x]:n[y][x]=1
        out.append(n)
    return out
SHADE_OBJ=[None,255,170,0]       # OBP0 $D0: colour 1 -> white, 2 -> light grey, 3 -> black; 0 = transparent
def to_image(g,scale=8,bgcol=(160,200,160)):
    im=Image.new('RGB',(16,16),bgcol)
    for y in range(16):
        for x in range(16):
            if g[y][x]:v=SHADE_OBJ[g[y][x]];im.putpixel((x,y),(v,v,v))
    return im.resize((16*scale,16*scale),Image.NEAREST)
