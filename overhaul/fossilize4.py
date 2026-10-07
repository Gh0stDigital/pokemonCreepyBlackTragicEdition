import pickle,sys;sys.path.insert(0,'.')
from PIL import Image
H=28  # back sprites are cut off at the bottom; rows 28-31 are empty
def show(px,s=4):
    im=Image.new('L',(32,32))
    for y in range(32):
        for x in range(32):im.putpixel((x,y),[255,170,85,0][px[y][x]])
    return im.resize((32*s,32*s),Image.NEAREST)
def edge(px,y,x):
    for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
        if yy>=H:continue
        if not(0<=yy<32 and 0<=xx<32) or px[yy][xx]==0:return True
    return False
def membrane(px,y,x):
    c=px[y][x];l=px[y][x-1] if x>0 else 0;r=px[y][x+1] if x<31 else 0
    return c in (1,2) and l not in (0,c) and r not in (0,c)
def fossil(px,bone,rib_rows,spine):
    o=[[0]*32 for _ in range(32)]
    mem=[[membrane(px,y,x) for x in range(32)] for y in range(32)]
    for y in range(H):
        for x in range(32):
            c=px[y][x]
            if c==0:continue
            if mem[y][x]:o[y][x]=0                         # wing membrane gone
            elif edge(px,y,x) or c==3:o[y][x]=3            # outline / bones
            elif c==bone:o[y][x]=0                         # bleached bone
            else:o[y][x]=1                                 # soft shading
    # outline the bleached areas where the membrane was removed next to bone
    for y in range(H):
        for x in range(32):
            if px[y][x] and not mem[y][x] and o[y][x]==0:
                if any(0<=xx<32 and mem[yy][xx] for yy,xx in ((y,x-1),(y,x+1),(y-1,x),(y+1,x)) if yy<H):o[y][x]=3
    # ribs + spine over the given body rows
    for y,(a,b) in rib_rows.items():
        if y%2==0:
            for x in range(a,b+1):
                if o[y][x]==0 and px[y][x]:o[y][x]=2
    for y,x in spine:o[y][x]=3
    return o
kab=pickle.load(open('kabutops_back.pkl','rb'));aero=pickle.load(open('aerodactyl_back.pkl','rb'))
kab_ribs={y:(5,22) for y in range(13,27)}
kab_spine=[(y,14) for y in range(12,27)]+[(y,13) for y in range(12,27,3)]+[(y,15) for y in range(12,27,3)]
aero_ribs={y:(8+max(0,(y-16)//2)-max(0,y-20),14-(y-16)//2) for y in range(16,24)}
aero_spine=[(15,14),(16,13),(17,12),(18,12),(19,11),(20,11),(21,10),(22,10),(23,9),(24,9)]
k=fossil(kab,2,kab_ribs,kab_spine)
a=fossil(aero,1,aero_ribs,aero_spine)
for y,x in ((10,15),(10,16),(11,15)):a[y][x]=3            # skull hollow
pickle.dump(k,open('kab_f.pkl','wb'));pickle.dump(a,open('aero_f.pkl','wb'))
W=Image.new('L',(4*140,140),255)
W.paste(show(kab),(0,0));W.paste(show(k),(140,0));W.paste(show(aero),(280,0));W.paste(show(a),(420,0));W.save('fossil_try4.png')
for n,g in (('kab',k),('aero',a)):
    print(n);[print('%2d '%y+''.join('.:#@'[c] for c in g[y])) for y in range(H)]
