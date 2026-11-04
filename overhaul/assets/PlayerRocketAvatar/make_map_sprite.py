import sys
sys.path.insert(0,'/home/user/pokemonCreepyBlackTragicEdition/overhaul')
import red_ghost_overworld as G
from PIL import Image,ImageDraw
OUT=sys.argv[1]
R=open('/home/user/pokemonCreepyBlackTragicEdition/overhaul/Creepy_Black_Mu_v1.gb','rb').read()
G.SPRITE=(5,0x4180);red=G.frames(R)
CAPEND={0:4,1:5,2:5,3:5,4:6,5:6}
BAG={1:(range(9,13),range(4,12)),4:(range(10,14),range(3,11)),2:(range(9,13),range(10,13)),5:(range(10,13),range(11,13))}
def make(f):
    g=[row[:] for row in red[f]]
    bag=BAG.get(f,(range(0),range(0)))
    for y in range(16):
        for x in range(16):
            inbag=y in bag[0] and x in bag[1]
            if red[f][y][x]==2:g[y][x]=2 if inbag else 3     # clothes black; RED's grey bag ring stays grey
            elif inbag and f in (1,4) and red[f][y][x]==1:g[y][x]=3         # inside the bag: black
            if f in (1,4) and y<=CAPEND[f] and g[y][x]==1:g[y][x]=3   # back of the cap: no tip
            if f not in (1,4) and y<=CAPEND[f] and red[f][y][x]==1:g[y][x]=2   # the hat tip: grey/green
    CHEST={0:[(11,7),(11,8)],3:[(12,6),(12,7)]}   # grey lapels / jacket front
    for y,x in CHEST.get(f,[]):
        if g[y][x]==3:g[y][x]=2
    return g
new=[make(f) for f in range(6)]
PAL={1:(232,240,224),2:(150,160,150),3:(16,20,24)}
S=8;BG=(196,214,190)
rows=[('RED',red),('ROCKET RED',new)]
labels=['down','up','left','right','down walk','up walk','left walk']
W=7*(16*S+10)+140;H=len(rows)*(16*S+24)+30
im=Image.new('RGB',(W,H),(255,255,255));d=ImageDraw.Draw(im)
for c,l in enumerate(labels):d.text((140+c*(16*S+10)+30,6),l,fill=(0,0,0))
for r,(name,fr) in enumerate(rows):
    y0=26+r*(16*S+24);d.text((6,y0+16*S//2),name,fill=(0,0,0))
    views=[fr[0],fr[1],fr[2],[row[::-1] for row in fr[2]],fr[3],fr[4],fr[5]]
    for c,g in enumerate(views):
        x0=140+c*(16*S+10);d.rectangle([x0,y0,x0+16*S-1,y0+16*S-1],fill=BG)
        for y in range(16):
            for x in range(16):
                v=g[y][x]
                if v:d.rectangle([x0+x*S,y0+y*S,x0+x*S+S-1,y0+y*S+S-1],fill=PAL[v])
im.save(OUT+'/rocket_allblack5.png')
fr=[]
for seq in ([0,3,0,3],[1,4,1,4],[2,5,2,5]):
    for k in seq:
        a=Image.new('RGB',(96,96),BG);dd=ImageDraw.Draw(a)
        for y in range(16):
            for x in range(16):
                v=new[k][y][x]
                if v:dd.rectangle([x*6,y*6,x*6+5,y*6+5],fill=PAL[v])
        fr.append(a)
fr[0].save(OUT+'/rocket_allblack5_walk.gif',save_all=True,append_images=fr[1:],duration=220,loop=0)
