import pickle,sys,io;sys.path.insert(0,'.')
from PIL import Image
def show(px,s=4):
    im=Image.new('L',(32,32))
    for y in range(32):
        for x in range(32):im.putpixel((x,y),[255,170,85,0][px[y][x]])
    return im.resize((32*s,32*s),Image.NEAREST)
def nb(px,y,x):
    return [px[yy][xx] if 0<=yy<32 and 0<=xx<32 else 0 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
def bleach(px):
    out=[[0]*32 for _ in range(32)]
    for y in range(32):
        for x in range(32):
            c=px[y][x]
            if c==0:continue
            edge=0 in nb(px,y,x)
            out[y][x]=3 if edge else {1:0,2:1,3:3}[c]   # outline black, light->bone white, dark->light shading, black detail kept
    return out
for n in ('kabutops','aerodactyl'):
    px=pickle.load(open(n+'_back.pkl','rb'))
    b=bleach(px)
    W=Image.new('L',(270,128),255);W.paste(show(px),(0,0));W.paste(show(b),(140,0));W.save(n+'_fossil_try1.png')
    # print grid for hand editing
    print(n);[print(''.join('.:#@'[c] for c in row)) for row in px]
