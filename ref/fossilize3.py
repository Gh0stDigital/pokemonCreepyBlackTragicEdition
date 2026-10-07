import pickle,sys;sys.path.insert(0,'.')
from fossilize2 import show,base,kabutops
from PIL import Image
def aerodactyl(px):
    o=base(px,1)
    start={}
    for y in range(14,28):
        for x in range(9,31):
            if px[y][x]==3 and px[y][x+1]==0:start[y]=x+1;break
    for y,s in start.items():
        nz=[x for x in range(s,32) if px[y][x]]
        for x in range(s,32):o[y][x]=0
        if nz:o[y][max(nz)]=3                                     # outer wing edge
    for x in range(min(start.values()),32):                       # top edge of the wing
        for y in range(14,28):
            if y in start and x>=start[y] and px[y][x]:o[y][x]=3;break
    sy=min(start);sx=start[sy]
    for k,(dx,dy) in enumerate(((1,1),(2,1),(3,1))):             # three bone struts fanning out
        x,y=sx,sy
        while y<28 and x<32:
            if y in start and x>=start[y] and px[y][x]:o[y][x]=3
            x+=dx;y+=dy
    for y in range(16,28):                                        # ribcage + spine in the body
        lim=start.get(y,22)
        xs=[x for x in range(3,lim) if px[y][x]==1 and o[y][x]==0]
        if len(xs)<3:continue
        a,b=min(xs),max(xs)
        if y%2==0:
            for x in range(a,b+1):
                if o[y][x]==0:o[y][x]=2
        o[y][(a+b)//2]=3
    o[9][14]=o[9][15]=o[10][14]=3;o[10][15]=2                     # hollow in the skull
    return o
k=kabutops(pickle.load(open('kabutops_back.pkl','rb')));a=aerodactyl(pickle.load(open('aerodactyl_back.pkl','rb')))
pickle.dump(k,open('kab_f.pkl','wb'));pickle.dump(a,open('aero_f.pkl','wb'))
W=Image.new('L',(4*140,140),255)
W.paste(show(pickle.load(open('kabutops_back.pkl','rb'))),(0,0));W.paste(show(k),(140,0))
W.paste(show(pickle.load(open('aerodactyl_back.pkl','rb'))),(280,0));W.paste(show(a),(420,0))
W.save('fossil_try3.png')
