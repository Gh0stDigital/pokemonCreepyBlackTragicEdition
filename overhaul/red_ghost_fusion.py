# Experiment: RED's battle picture as a black silhouette with GHOST's face (white eyes + grin) on his face.
# CHOSEN for the Mirage Black Tamer's trainer pic: option A0 (eyes only, no mouth) -> fuse(rom, small='A0').
# Builds a 7x7-tile picture (56x56, 4 shades) from the ROM's own RED front pic (4:6F2A) and GHOST front pic (2D:4000).
import sys,io,os
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,os.path.join(HERE,'..','ref'));import pic
from PIL import Image
from collections import deque
def fo(b,a):return b*0x4000+a-0x4000
def grid(r,bank,addr):
    o=fo(bank,addr);w=r[o]>>4;h=r[o]&15
    d=bytes(pic.decompress(io.BytesIO(r),offset=o));g=[[0]*(w*8) for _ in range(h*8)];i=0
    for tx in range(w):
        for ty in range(h):
            for y in range(8):
                lo,hi=d[i],d[i+1];i+=2
                for x in range(8):g[ty*8+y][tx*8+x]=((lo>>(7-x))&1)|(((hi>>(7-x))&1)<<1)
    return g
def outside(g,light=lambda c:c==0):
    """pixels reachable from the border through light pixels = background"""
    H,W=len(g),len(g[0]);bg=[[False]*W for _ in range(H)];q=deque()
    for y in range(H):
        for x in range(W):
            if (y in (0,H-1) or x in (0,W-1)) and light(g[y][x]):bg[y][x]=True;q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and not bg[ny][nx] and light(g[ny][nx]):bg[ny][nx]=True;q.append((ny,nx))
    return bg
def ghost_face(r):
    """GHOST's eyes and grin: white pixels enclosed by its dark body, upper half of the picture"""
    g=grid(r,0x2d,0x4000);bg=outside(g,lambda c:c<=1)
    pts=[(y,x) for y in range(len(g)//2+4) for x in range(len(g[0])) if g[y][x]==0 and not bg[y][x]]
    y0=min(p[0] for p in pts);x0=min(p[1] for p in pts);y1=max(p[0] for p in pts);x1=max(p[1] for p in pts)
    return [(y-y0,x-x0) for y,x in pts],(y1-y0+1,x1-x0+1)
SMALL_FACES={   # hand-shrunk versions of GHOST's face: slanted eyes + lopsided grin ('#' = white)
 'A':['##......##','###....###','..........','...#####..','...####...'],
 'B':['#......#','##....##','........','..####..','..###...'],
 'C':['#.....#','##...##','.......','..###..'],
 'A0':['##......##','###....###','..........','..........','..........'],   # A without the mouth (eyes stay where A has them)
 'A3':['.+##......##:+','.:###....###:.','..............','..............','..............'],   # A0 + grey rim on each eye's outer side (as A2)
 # A0 + HAUNTER's mouth: a white grin split by a jagged row of teeth (place with face_at=EYES_AT so the eyes stay put)
 'H1':['##......##','###....###','..........','#........#','##########','.#.#.#.#..'],
 'H2':['##......##','###....###','..........','##......##','.#.#.#.#..','..#.#.#...'],
 'H3':['##......##','###....###','..........','#........#','#.#.#.#.##','.#.#.#.#..'],
 # A with GHOST's grin (crescent, one end curls up, shadow under the upper lip; stored mirrored so it ends up
 # leaning like GHOST's after the face flip) and a grey rim on each eye's outer side. ':' light, '+' dark grey
 'A2':['.+##......##:+','.:###....###:.','...+..........','...####::++...','...#####:+....','....+###+.....'],
}
SHADE={'#':0,':':1,'+':2}
def small_face(k,flip=True):
    rows=[row[::-1] if flip else row for row in SMALL_FACES[k]]   # mirrored: grin leans the other way
    return [(y,x,SHADE[c]) for y,row in enumerate(rows) for x,c in enumerate(row) if c in SHADE],(len(rows),len(rows[0]))
EYES_AT=(12,19)                                      # where option A's eyes sit (A/A0)
FACE_CENTRE=(14.5,23.5)                                # RED's face: under the cap brim, centred on the head (x 15-32)
def fuse(r,face_at=None,small=None,halo=True):
    red=grid(r,4,0x6f2a);H,W=len(red),len(red[0]);bg=outside(red)
    out=[[0 if bg[y][x] else 3 for x in range(W)] for y in range(H)]       # silhouette: everything inside = black
    face,(fh,fw)=small_face(small) if small else ghost_face(r)
    if face_at is None and small:face_at=(int(FACE_CENTRE[0]-fh/2+0.5),int(FACE_CENTRE[1]-(fw-1)/2+0.5))
    if face_at is None:                                                     # centre the face on RED's face
        face_at=(5,17)                                                      # eyes + grin on RED's head (rows 2-19, x 16-34)
    for y,x,*c in face:
        Y,X=y+face_at[0],x+face_at[1]
        if 0<=Y<H and 0<=X<W and out[Y][X]==3:out[Y][X]=c[0] if c else 0
    if halo:out=aura(out)
    return out,(fh,fw),face_at
def aura(out,reach=5):
    """GHOST's halo around the silhouette: dark-grey checker on the edge, light-grey checker next to it,
    then scattered light dots that thin out with distance (same dithering as GHOST's front pic)"""
    H,W=len(out),len(out[0]);dist=[[None]*W for _ in range(H)];q=deque();bg=outside(out)   # face holes stay white
    for y in range(H):
        for x in range(W):
            if out[y][x]==3:dist[y][x]=0;q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                ny,nx=y+dy,x+dx
                if 0<=ny<H and 0<=nx<W and dist[ny][nx] is None:dist[ny][nx]=dist[y][x]+1;q.append((ny,nx))
    for y in range(H):
        for x in range(W):
            d=dist[y][x];chk=(x+y)%2==0;h=(x*7+y*13+x*y)%5
            if not d or not bg[y][x]:continue
            if d==1:out[y][x]=2 if chk else 1
            elif d==2:out[y][x]=1 if chk or h==0 else 0
            elif d<=reach and chk and h<{3:3,4:2,5:1}[d]:out[y][x]=1
    return out
def to_image(g,scale=4):
    pal=[255,170,85,0];H,W=len(g),len(g[0]);im=Image.new('L',(W,H))
    for y in range(H):
        for x in range(W):im.putpixel((x,y),pal[g[y][x]])
    return im.resize((W*scale,H*scale),Image.NEAREST)
if __name__=='__main__':
    r=open(sys.argv[1],'rb').read();out,size,at=fuse(r);print('ghost face size',size,'placed at',at)
    to_image(out).save(sys.argv[2])
