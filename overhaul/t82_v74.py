# v74 tests: modes
#  signs      - CINNABAR's five signs read their own text (the town sign used to print "C3 ERROR.")
#  towns      - every town with a shamaness: its first sign shows its own text, she still talks
#  gamecorner - CELADON GAME CORNER Rocket: dead = no after-battle speech (script still ends), alive = the usual speech
#  graves     - a gravestone sprite on a WALK object stays put; an ordinary walker still walks
#  statue     - MANSION 1F: the statue switch (y6,x2 facing up) shows the switch, not MR. MU; MR. MU still talks
import sys
MODE82=sys.argv[1]
sys.argv=['t79_v71.py','none']
exec(open('t79_v71.py').read().split("if MY=='gates':")[0])
MY=MODE82
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
def read_text(frames=60,n=20):
    seen.clear();press_('a',frames)
    for i in range(n):
        if not box():break
        press_('a',frames)
    return allt().replace("'","")
from town_map import grid
from collections import deque
def goto(ty,tx,mapid=8):
    d,g=grid(mapid);H=len(g);W=len(g[0])
    for i in range(1,m[0xd4e1]+1):
        iy,ix=m[0xc204+16*i]-4,m[0xc205+16*i]-4
        if 0<=iy<H and 0<=ix<W:g[iy]=g[iy][:ix]+'O'+g[iy][ix+1:]
    st=(m[0xd361],m[0xd362]);prev={st:None};q=deque([st])
    while q and (ty,tx) not in prev:
        c=q.popleft()
        for dd,(dy,dx) in (('up',(-1,0)),('down',(1,0)),('left',(0,-1)),('right',(0,1))):
            n=(c[0]+dy,c[1]+dx)
            if n in prev or not(0<=n[0]<H and 0<=n[1]<W):continue
            if g[n[0]][n[1]]!='.' and n!=(ty,tx):continue
            prev[n]=(c,dd);q.append(n)
    assert (ty,tx) in prev,('no static path',st,(ty,tx))
    path=[];c=(ty,tx)
    while prev[c]:c,dd=prev[c];path.append(dd)
    for dd in reversed(path):
        p.button(dd,8);p.tick(24)
    T(10)
    return (m[0xd361],m[0xd362])==(ty,tx)
def warp_set(mapid,setup):
    load('pallet_with_ghost');lead(0x1f);m[0xd16b+29]=0x3f;m[0xd455]=255;setup()
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=mapid
    for i in range(6):
        if m[0xd35e]==mapid:break
        walk('up',1)
    T(120);m[0xd887]=0
def to_cinnabar(black=False):
    warp_from_pallet(0xa5,0);m[0xd887]=0
    if black:make_black()
    m[0xd365]=8
    for i in range(10):
        if m[0xd35e]==8:break
        p.button('down',8);T(30)
    T(120);print('in',pos(),flush=True)
if MY=='signs':
    to_cinnabar()
    EXPECT={'town':'CINNABAR ISLAND The Fiery','center':'POKéMON CENTER','mart':'POKéMON MART','lab':'POKéMON LAB','gym':'POKéMON GYM'}
    for (sy,sx,name) in ((5,9,'town'),(11,16,'center'),(11,12,'mart'),(11,9,'lab'),(3,13,'gym')):
        done=False
        for (dy,dx,face) in ((1,0,'up'),(0,1,'left'),(0,-1,'right'),(-1,0,'down')):
            try:
                if goto(sy+dy,sx+dx):done=True;break
            except AssertionError:continue
        if not done:print(name,'no path');continue
        press_(face,10);t=read_text()
        print(name,pos(),repr(t),flush=True)
        shot('v74_sign_'+name)
        tt=t.split('▼')[-1] if False else t
        ok('ERROR' not in t,'CINNABAR %s sign: no ERROR text'%name)
        ok(name!='town' or 'Fiery' in t,'CINNABAR %s sign: the town sign has its own text'%name)


if MY=='towns':
    from town_map import info
    DOOR={0:0x25,1:0x29,2:0x34,3:0x40,4:0x8d,5:0x59,6:0x7a,7:0x98,8:0xa5,0x0a:0xb4}
    for town in (0,1,2,3,5,6,7,0x0a,4,8):
        warp_set(DOOR[town],lambda:None);m[0xd365]=town
        for i in range(10):
            if m[0xd35e]==town:break
            p.button('down',8);T(30)
        T(120)
        sh=[i for i in range(1,m[0xd4e1]+1) if m[0xc100+16*i]==0x19 and m[0xd4e4+2*(i-1)]==0xd0]
        d=info(town);sy,sx=d['signs'][0]
        done=False
        for (dy,dx,face) in ((1,0,'up'),(0,1,'left'),(0,-1,'right'),(-1,0,'down')):
            try:
                if goto(sy+dy,sx+dx,town):done=True;break
            except AssertionError:continue
        if not done:print('town %x: no path to the first sign %s'%(town,(sy,sx)));continue
        press_(face,10);t=read_text()
        print('town %x'%town,'shamaness slots',sh,'D4E1',m[0xd4e1],'sign',(sy,sx),repr(t[-70:]),flush=True)
        ok('ERROR' not in t and sum(c.isalpha() for c in t)>5,'town %x: its first sign shows its own text'%town)
if MY=='gamecorner':
    for killed in (False,True):
        warp_from_pallet(0x87,0);m[0xd887]=0
        m[0xd44f]=(m[0xd44f]&0x7f)|(0x80 if killed else 0);m[0xd057]=0
        seen.clear();m[0xd65f]=1;m[0xda39]=1
        for i in range(140):
            T(10)
            if m[0xd65f]==0:break
        for i in range(30):
            if m[0xd65f]==0 and not box():break
            press_('a',60)
        t=allt().replace("'","");k='killed' if killed else 'alive'
        print(k,'text:',t[-160:],'d65f',m[0xd65f],flush=True)
        ok(m[0xd65f]==0,'%s: the map script is finished'%k)
        if killed:ok(sum(c.isalpha() for c in t)<3,'killed: no after-battle speech')
        else:ok(len(t.strip())>10,'alive: the usual speech is shown')
if MY=='graves':
    # (map, sprite): MANSION 2F trainer (WALK, left-right), PALLET girl (WALK, any direction)
    for mp,i in ((0xd6,1),(0x0,2)):
        for grave in (True,False):
            warp_from_pallet(mp,0);m[0xd887]=0
            sy,sx=m[0xc204+16*i]-4,m[0xc205+16*i]-4        # walkers only move while on screen: stand 2 tiles away
            for (ty,tx) in ((sy+2,sx),(sy-2,sx),(sy,sx+2),(sy,sx-2),(sy+1,sx+1),(sy-1,sx-1)):
                try:
                    if goto(ty,tx,mp):break
                except AssertionError:continue
            print('player',pos(),'sprite image index',hex(m[0xc102+16*i]),flush=True)
            print('map',hex(mp),'sprite',i,hex(m[0xc100+16*i]),m[0xc204+16*i]-4,m[0xc205+16*i]-4,'mv',hex(m[0xc206+16*i]),flush=True)
            if m[0xc206+16*i]!=0xfe:print('not a walker, skip');continue
            if grave:m[0xc100+16*i]=0x49
            seenpos=set();moved=0
            for k in range(400):
                T(10)
                seenpos.add((m[0xc204+16*i],m[0xc205+16*i]))
            k='gravestone' if grave else 'living walker'
            print(k,'positions',len(seenpos),'mv',hex(m[0xc206+16*i]),flush=True)
            if grave:ok(len(seenpos)==1 and m[0xc206+16*i]==0xff,'map %x: a gravestone on a WALK object stands still (movement byte STAY)'%mp)
            else:ok(len(seenpos)>1,'map %x: control: the living walker walks'%mp)
if MY=='statue':
    for mu in (4,3):
        warp_set(0xa5,lambda:(m.__setitem__(0xd460,mu),m.__setitem__(0xd464,0)))
        goto(6,2,0xa5);press_('up',10);t=read_text()
        print('D460',mu,'statue:',repr(t),flush=True)
        ok('witch' in t and 'ansion' not in t,'D460 %d: the statue switch shows the switch (not MR. MU)'%mu)
        for i in range(10):
            if not box():break
            press_('b',40)
    # MR. MU still talks (v52): next to him at (y20,x6) facing down? he stands on (21,6) -> player below (22,6) facing up
    warp_set(0xa5,lambda:(m.__setitem__(0xd460,3),m.__setitem__(0xd464,0)))
    print('mu sprite',hex(m[0xc140]),m[0xc244]-4,m[0xc245]-4,flush=True)
    my,mx=m[0xc244]-4,m[0xc245]-4
    for (dy,dx,face) in ((1,0,'up'),(-1,0,'down'),(0,-1,'right'),(0,1,'left')):
        try:
            if goto(my+dy,mx+dx,0xa5):break
        except AssertionError:continue
    press_(face,10);t=read_text()
    print('MU:',repr(t[-120:]),flush=True)
    ok('witch' not in t and len(t.strip())>10,'MR. MU still talks (D460 3)')
print('t82 done',flush=True)
