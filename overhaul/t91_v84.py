# v84 batch. Modes:
#  balls  - Pallet (set 1: four-tile slots 0B = item ball $8780, 0C = $48 $87C0): with an item ball, a second four-tile sprite and a black ball (pic 47) on the map
#           after a redraw the black ball uses neither slot (a free walker slot with the ball tiles), the item ball's / the other sprite's tiles are unchanged;
#           with only the item ball the black ball takes 0C; with only the 0C sprite it takes 0B (the old code overwrote the ITEM BALLS' slot)
#  snorlax - (see below)
import sys,json
MY91=sys.argv[1]
sys.argv=['x','none'];exec(open('t36_v28.py').read().split("if MODE=='panic':")[0]);MODE=MY91
ROMB=open(os.environ['CB_ROM'],'rb').read()
SHEET=int(json.load(open('manifest_v40.json'))['labels']['bank2f']['sheet'],16)
BALL=list(ROMB[0x2f*0x4000+SHEET-0x4000:][:64])
def vram(a,n):return [p.memory[a+k] for k in range(n)]
def slot(i):return m[0xc20e+16*i]
def redraw():
    p.button('start',8);T(40);p.button('b',8);T(60)
if MODE=='balls':
    start();ns=[n[0] for n in npcs() if n[4]==0][:3];a,b,c=ns
    def setpic(i,pc):m[0xc100+16*i]=pc
    def scenario(pics,label):
        for i,pc in zip((a,b,c),pics):setpic(i,pc)
        t0=(vram(0x8780,64),vram(0x87c0,64))
        redraw()
        return t0
    # full conflict: item ball (3d), other four-tile (48), black ball (47)
    t0=scenario((0x3d,0x48,0x47),'all')
    sa,sb,sc=slot(a),slot(b),slot(c)
    print('slots',sa,sb,sc)
    ok(sc not in (0x0b,0x0c) and 2<=sc<=10,'item ball + other four-tile sprite + black ball: the black ball gets a free walker slot (%d)'%sc)
    ok(vram(0x8780,64)==t0[0] and vram(0x87c0,64)==t0[1],'the item ball\'s and the other sprite\'s tiles are unchanged')
    base=0x8000+(sc-1)*0xc0
    ok(vram(base,64)==BALL and vram(base+64,64)==BALL and vram(base+128,64)==BALL,'the ball tiles are in the three standing frames of that slot')
    ok(sa==0x0b and sb==0x0c,'the other sprites keep their slots (%d, %d)'%(sa,sb))
elif MODE=='free':
    start();ns=[n[0] for n in npcs() if n[4]==0][:3];a,b,c=ns
    for pics,want,label in (((0x3d,0,0x47),0x0c,'only an item ball: slot 0C'),((0x48,0,0x47),0x0b,'only the 0C sprite: slot 0B'),((0,0,0x47),0x0c,'alone: slot 0C')):
        for i,pc in zip((a,b,c),pics):m[0xc100+16*i]=pc
        redraw()
        s=slot(c);ad={0x0b:0x8780,0x0c:0x87c0}.get(s)
        ok(s==want and ad and vram(ad,64)==BALL,label+' (got %s)'%hex(s))
elif MODE=='snorlax':
    sys.argv=['x','gwalk'];exec(open('t56_v48.py').read().split("if MODE=='moves':")[0]);MODE='snorlax'
    start_wild(make_black,species=0x84,lv=30);seen.clear()
    ok(m[0xd452]==0,'before the move: D452 = 0')
    use_move(0,500)
    for k in range(14):
        if m[0xd057]==0:break
        press_('a',60)
    T(60)
    ok(m[0xd057]==0 and 0x84 in list(m[0xd164:0xd16b]),'METAMORPHOSIS on a wild SNORLAX: the battle is over and SNORLAX joined')
    ok(m[0xd452]==1,'D452 (CURSE used) is set, so the "returned to the mountains" text is skipped (v73)')
elif MODE=='slide':
    sys.argv=['x','gwalk'];exec(open('t56_v48.py').read().split("if MODE=='moves':")[0]);MODE='slide'
    load('pallet_with_ghost');make_black()
    a=list(m[0xd16b:0xd16b+44]);b=list(m[0xd16b+44:0xd16b+88])
    m[0xd16b:0xd16b+44]=b;m[0xd16b+44:0xd16b+88]=a
    sp=m[0xd164];m[0xd164]=m[0xd165];m[0xd165]=sp
    na=list(m[0xd2b5:0xd2b5+11]);nb=list(m[0xd2b5+11:0xd2b5+22]);m[0xd2b5:0xd2b5+11]=nb;m[0xd2b5+11:0xd2b5+22]=na
    m[0xd059]=0x70;m[0xd127]=5
    for i in range(300):
        if m[0xd057]:break
        p.tick()
    for i in range(60):
        t=clean(' '.join(txt()))
        if 'FIGHT' in t and 'RUN' in t:break
        press_('a',30)
    T(20)
    ok(m[0xd014]!=0x7f,'CHARMANDER leads')
    press_('up',12);press_('left',12);press_('right',12);press_('a',90)
    press_('down',12);press_('a',60);T(20)
    seen.clear();p.button('a',8)
    parts=set();went=False;full=False
    for k in range(500):
        T(1)
        row=[m[0xc3a0+8*20+1+c] for c in range(7)]
        n=sum(1 for x in row if x!=0x7f)
        if 0<n<7 and m[0xd014]==0x7f:parts.add(n)
        if n==7 and m[0xd014]==0x7f:full=True
        t=clean(' '.join(txt()))
        if k>60 and full and ('scared' in t or 'FIGHT' in t):break
    tt=allt()
    ok(m[0xd014]==0x7f,'BLACK is out')
    ok('Go!' not in tt and 'Come back' not in tt.replace('good','') or 'Go!' not in tt,'no "Go! BLACK!"')
    ok(len(parts)>=4,'the picture slides in column by column (partial widths seen: %s)'%sorted(parts))
    ok(full,'the whole picture stands there at the end')
print('t91 done',flush=True)
