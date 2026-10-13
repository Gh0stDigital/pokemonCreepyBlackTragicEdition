# v46: seven changes. Modes:
#  start  - BLACK leading a wild battle: no "Go! BLACK!", BLACK's picture is there at once (no slide, no send-out
#           animation), the battle menu works; normal: a CHARMANDER lead still gets "Go! CHARMANDER!"
#  ball   - BANE in battle: the throw POKe BALL, fully black, is in the enemy picture (exact tiles); map ball: sprite 47's
#           sheet is the item POKe BALL fully black
#  lv100  - the climax: right after "GHOST consumed the MIRAGE!" GHOST is Lv100 (stats + full HP), "grew to level 100!"
#  gates  - as BLACK: Route 22 gate and Route 23 badge checks don't stop BLACK, the guards are scared; normal (not BLACK,
#           no badges): the Route 22 gate guard still stops the player with the badge text
#  agatha - AGATHA's shell text: the energy line, no "My people drew it"
import sys
MY54=sys.argv[1]
sys.argv=['x','none'];exec(open('t47_v39.py').read().split("if MODE==")[0]);MODE=MY54
from patchlib import enc
ROMB=open(os.environ['CB_ROM'],'rb').read()
def fo2(b,a):return b*0x4000+a-0x4000
def pic_tiles():return sum(1 for y in range(5,12) for x in range(1,8) if m[0xc3a0+20*y+x]!=0x7f)
def start_wild(setup):
    load('pallet_with_ghost');setup();m[0xd059]=0xa5;m[0xd127]=5;seen.clear()
    for i in range(300):
        if m[0xd057]:break
        p.tick()
    lo=0
    for i in range(60):
        t=clean(' '.join(txt()))
        if 'FIGHT' in t and 'RUN' in t:break
        T(10)
        if i>3:lo=max(lo,pic_tiles())
        if 'Go!' not in t:press_('a',30) if i%3==2 else None
    return allt()
if MODE=='start':
    t=start_wild(make_black);n=pic_tiles();print('BLACK start:',t[-160:],'pic tiles',n)
    ok(m[0xd057]==1 and m[0xd014]==BLK,'wild battle, BLACK is out')
    ok('Go!' not in t,'no "Go! BLACK!"')
    ok(n>=20,"BLACK's picture is on the screen (%d tiles)"%n)
    shot('v46_black_start')
    ok('FIGHT' in ' '.join(txt()),'the battle menu is ready')
    def charm():make_black();lead(0xb0)
    t=start_wild(charm);print('CHARMANDER start:',t[-120:])
    ok('Go! CHARMANDER' in t.replace('  ',' ') or 'CHARMANDER!' in t,'normal lead: "Go! CHARMANDER!" as before')
    ok(pic_tiles()>=20,'and its picture is shown')
elif MODE=='ball':
    o=fo2(0x2f,0x430c);exp_b=ROMB[o:o+0x310];hits=[]
    def cb(ctx):hits.append(bytes(m[a] for a in range(0x9000,0x9310))==exp_b)
    p.hook_register(0x2f,0x40a8,cb,None)                    # right after black_ball copied its tiles to the enemy picture
    wild(0xa5);best=100 if hits and all(hits) else 0;print('ball copies',hits)
    ok(best==100,'BANE in battle: the throw POKe BALL, fully black (exact tiles in the enemy picture)')
    ib=ROMB[fo2(4,0x5140):fo2(4,0x5140)+64];sh=ROMB[fo2(0x2f,0x5159):fo2(0x2f,0x5159)+64]
    def pix(d,t,x,y):return ((d[t*16+y*2+1]>>(7-x))&1)<<1|((d[t*16+y*2]>>(7-x))&1)
    same=all((pix(sh,t,x,y)==3)==(pix(ib,t,x,y)!=0) and pix(sh,t,x,y) in (0,3) for t in range(4) for y in range(8) for x in range(8))
    ok(same,'map ball: sprite 47 = the item POKe BALL shape, every pixel black')
elif MODE=='lv100':
    load('v25_after_ritual_v25a');T(30);seen.clear()
    g=list(m[0xd164:0xd16a]).index(0x1f);b=0xd16b+44*g;print('GHOST before Lv',m[b+33])
    for k in range(80):
        if m[0xd467]>=4:break
        if box() or m[0xcd6b]:press_('a',45);continue
        p.button('down',8);T(40)
    for k in range(10):
        if 'level 100' in allt():break
        press_('a',60)
    g=list(m[0xd164:0xd16a]).index(0x1f);b=0xd16b+44*g
    lv,hp,mx=m[b+33],m[b+1]<<8|m[b+2],m[b+34]<<8|m[b+35];print('after consume: Lv',lv,'HP',hp,mx,allt()[-120:])
    ok(m[0xd467]>=4 and 'consumed' in allt(),'GHOST consumed the MIRAGE')
    ok(lv==100 and m[b+3]==100 and mx>200 and hp==mx,'GHOST is Lv100 at once (max HP %d, full)'%mx)
    ok('grew to' in allt() and 'level 100' in allt(),'"GHOST grew to level 100!"')
elif MODE=='gates':
    def go_gate(black):
        load('pallet_with_ghost');m[0xd356]=0;m[0xd455]=255
        if black:make_black()
        for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0xc1
        for i in range(6):
            if m[0xd35e]==0xc1:break
            p.button('up',8);T(24)
        T(60);m[0xd887]=0;seen.clear()
    def north(n):
        for k in range(n):
            if box():press_('b',30)
            p.button('up',8);T(24)
    go_gate(True);y0=m[0xd361];print('gate start',pos())
    north(12);t=allt();print('BLACK gate:',t[-120:],pos())
    ok('BADGE' not in t and m[0xd35e]==0x22,'Route 22 gate as BLACK: no badge check, BLACK walks out onto Route 23')
    north(30);t=allt();print('BLACK Route 23:',t[-120:],pos())
    ok('BADGE' not in t and m[0xd361]<136,'Route 23 as BLACK: past the first badge check row with no badge (y %d)'%m[0xd361])
    # talk to the nearest Route 23 guard as BLACK: "BANE them?" -> NO -> the scared line, no badge talk
    me=(m[0xd361],m[0xd362])
    gs=sorted([(abs(m[0xc204+16*i]-4-me[0])+abs(m[0xc205+16*i]-4-me[1]),i) for i in range(1,m[0xd4e1]+1) if m[0xc100+16*i]])
    gi=gs[0][1];gy,gx=m[0xc204+16*gi]-4,m[0xc205+16*gi]-4;print('guard',gi,(gy,gx),'me',me)
    for tgt,face in (((gy+1,gx),'up'),((gy,gx-1),'right'),((gy,gx+1),'left'),((gy-1,gx),'down')):
        try:bfs_to(*tgt,maxn=400);break
        except AssertionError:continue
    press_(face,20);seen.clear();press_('a',90)
    for k in range(20):
        t=' '.join(txt())
        if 'YES' in t and ('BANE' in allt() or 'METAMORPHOSIS?' in allt()):press_('down',20);press_('a',90);continue
        press_('a',60)
    t=allt();print('guard talk:',t[-200:])
    ok('scared' in t or 'shaking' in t,'a Route 23 guard as BLACK: too scared ("G-go ahead...")')
    ok('BADGE' not in t,'no badge talk')
    go_gate(False);print('normal gate',pos())
    north(6)
    for k in range(6):press_('a',60)
    t=allt();print('normal gate:',t[-160:],pos())
    ok('BADGE' in t and m[0xd35e]==0xc1,'not BLACK, no badges: the gate guard stops the player with the badge text as before')
elif MODE=='agatha':
    o=0xbb22f;s=ROMB[o:o+71]
    ok(enc('Feel its energy?') in s and enc('who truly love.') in s,"AGATHA: the shell's energy text")
    ok(enc('My people') not in ROMB[o-20:o+200] and enc('See the mark') not in ROMB,'no "See the mark on it? My people drew it"')
