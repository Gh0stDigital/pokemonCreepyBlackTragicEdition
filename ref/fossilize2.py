import pickle,sys,io;sys.path.insert(0,'.')
from PIL import Image
def show(px,s=4):
    im=Image.new('L',(32,32))
    for y in range(32):
        for x in range(32):im.putpixel((x,y),[255,170,85,0][px[y][x]])
    return im.resize((32*s,32*s),Image.NEAREST)
def edge(px,y,x):
    return any((not(0<=yy<32 and 0<=xx<32)) or px[yy][xx]==0 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)))
def base(px,shell_val):
    out=[[0]*32 for _ in range(32)]
    for y in range(32):
        for x in range(32):
            c=px[y][x]
            if c==0:continue
            if edge(px,y,x):out[y][x]=3
            elif c==shell_val:out[y][x]=0          # main body colour -> bleached bone
            elif c==3:out[y][x]=3
            else:out[y][x]=1
    return out
def kabutops(px):
    o=base(px,2)
    # shell region = original dark pixels; ribs: every 3rd row inside the shell a dark gap, spine down the middle
    rows={}
    for y in range(32):
        xs=[x for x in range(32) if px[y][x]==2]
        if xs:rows[y]=(min(xs),max(xs))
    for y,(a,b) in rows.items():
        if y<8:continue
        cx=(a+b)//2
        if y%3==0:
            for x in range(a+1,b):
                if o[y][x]==0:o[y][x]=2
        if b-a>=4:
            o[y][cx]=3
            if y%2==0:o[y][cx-1]=o[y][cx+1]=3 if o[y][cx-1]!=0 or True else 3
    return o
def aerodactyl(px):
    o=base(px,1)
    # wing membrane = checkered dark/light area right of the diagonal arm line: clear it, keep struts
    for y in range(15,28):
        row=px[y];start=None
        for x in range(9,31):
            if row[x]==3 and row[x+1]==0:start=x+1;break
        if start is None:continue
        for x in range(start,32):
            if px[y][x] in (1,2) and not edge(px,y,x):o[y][x]=0
        for x in range(start,32):     # struts: diagonal bone lines radiating down-right
            if (x-start)-(y-15)//2 in (2,7,12) and px[y][x]!=0:o[y][x]=3
    # body ribcage: inside original light area left of the wing, dark rib rows and a spine
    for y in range(9,28):
        xs=[x for x in range(4,22) if px[y][x]==1 and o[y][x]==0]
        if len(xs)<3:continue
        a,b=min(xs),max(xs);cx=(a+b)//2
        if y%2==1:
            for x in range(a,b+1):
                if o[y][x]==0:o[y][x]=2
        o[y][cx]=3
    # skull: dark socket near the top of the head
    for y in range(7,10):
        for x in range(12,17):
            if px[y][x]==1 and o[y][x]==0 and (x+y)%2==0:o[y][x]=2
    return o
res={}
for n,f in (('kabutops',kabutops),('aerodactyl',aerodactyl)):
    px=pickle.load(open(n+'_back.pkl','rb'));o=f(px);res[n]=o;pickle.dump(o,open(n+'_fossil2.pkl','wb'))
W=Image.new('L',(4*140,140),255)
fr=[Image.open('kabutops_front.png'),Image.open('aerodactyl_front.png')]
W.paste(show(pickle.load(open('kabutops_back.pkl','rb'))),(0,0));W.paste(show(res['kabutops']),(140,0))
W.paste(show(pickle.load(open('aerodactyl_back.pkl','rb'))),(280,0));W.paste(show(res['aerodactyl']),(420,0))
W.save('fossil_try2.png')
