# v36 checks. Modes:
#  tower    - Tower 7F with hidden objects (picture ID 0): START menu open/close keeps the map tiles (was garbage) and the
#             visible sprites' tiles; MISTY's gym after she left (her picture 0) too; a map without hidden objects as before
#  agatha   - quest stage 3: GHOST Lv49 is still too weak, Lv50 is enough (HELIX FOSSIL back, stage 4)
#  cap      - GHOST can't pass Lv50 (exp capped at the Lv50 value); a GHOST already above 50 keeps its level;
#             CHARMANDER still grows past 50
#  giovanni - SILPH 11F defeat line: "GIOVANNI:" once, then "Damn that cult..."
#  blue     - SILPH 7F after the win, GHOST route: new "dark power" lines; off the GHOST route the original text
from harness import *
import sys,io
from collections import deque
MODE=sys.argv[1]
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:sys.exit(1)
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
seen=[];screens=[]
def T(n):
    for _ in range(n):
        p.tick();b=clean(box())
        if b and (not seen or seen[-1]!=b):seen.append(b);screens.append(txt()[12:])
def press_(k,n=60):p.button(k,8);T(n)
def allt():return ' '.join(seen)
def bfs_to(y,x,maxn=900):
    def snap():
        f=io.BytesIO();p.save_state(f);f.seek(0);return f.read()
    def rest(b):p.load_state(io.BytesIO(b))
    for k in range(10):
        if not box() and m[0xcd6b]==0:break
        p.button('b',8);T(40)
    T(30);start=(m[0xd361],m[0xd362]);prev={start:None};st={start:snap()};q=deque([start]);mp=m[0xd35e]
    while q and (y,x) not in prev and len(prev)<maxn:
        c=q.popleft()
        for d,(dy,dx) in (('up',(-1,0)),('down',(1,0)),('left',(0,-1)),('right',(0,1))):
            n=(c[0]+dy,c[1]+dx)
            if n in prev:continue
            rest(st[c]);p.button(d,8);p.tick(24)
            if m[0xd35e]!=mp or m[0xd057] or box():continue
            if (m[0xd361],m[0xd362])==n:prev[n]=(c,d);st[n]=snap();q.append(n)
    assert (y,x) in prev,('no path',(y,x),sorted(prev))
    path=[];c=(y,x)
    while prev[c]:c,d=prev[c];path.append(d)
    rest(st[start])
    for d in reversed(path):p.button(d,8);T(24)
    T(10)
def warp(mapid,warpid=0,setup=None):
    load('pallet_with_ghost');m[0xd455]=255
    if setup:setup()
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=warpid;m[0xd3af+4*i+3]=mapid
    for i in range(6):
        if m[0xd35e]==mapid:break
        p.button('up',8);T(24)
    T(120);m[0xd887]=0;print('arrived',pos(),flush=True)
def lead(species):
    i=list(m[0xd164:0xd16a]).index(species)
    if i:
        for base,size in ((0xd16b,44),(0xd2b5,11),(0xd273,11)):
            a=list(m[base:base+size]);b=list(m[base+size*i:base+size*(i+1)])
            m[base:base+size]=b;m[base+size*i:base+size*(i+1)]=a
        m[0xd164],m[0xd164+i]=m[0xd164+i],m[0xd164]
def fight(limit=800,weak_enemy=False):
    for i in range(limit):
        if weak_enemy and m[0xd057]:m[0xcfe6]=0;m[0xcfe7]=1;m[0xd015]=0;m[0xd016]=99
        if m[0xd057]==0:return
        b=clean(box())
        if 'FIGHT' in b and 'RUN' in b:
            for k in range(4):
                if '▲FIGHT' in box():break
                press_('up',20);press_('left',20)
            press_('a',60)
            for k in range(4):press_('up',10)
            press_('a',200);continue
        if 'Bring out' in b or 'change' in b.lower():press_('b',60);continue
        press_('a',90)
ROM=open(os.environ['CB_ROM'],'rb').read()
def map_tiles_ok():
    b=m[0xd52b];g=m[0xd52e]|m[0xd52f]<<8;o=b*0x4000+g-0x4000
    v=bytes(m[a] for a in range(0x9000,0x9600))
    return all(v[i:i+16]==ROM[o+i:o+i+16] for i in range(0,0x600,16) if i//16 not in (3,20))   # 3/20 = animated flower/water
def menu_roundtrip():
    T(30);before=p.screen.image.copy()
    press_('start',60);press_('b',90);T(30)
    return map_tiles_ok(),before.tobytes()==p.screen.image.tobytes()     # same picture (still map, still sprites)

if MODE=='tower':
    def s():
        m[0xd769]|=0x8e;m[0xd7e0]|=0x80;m[0xd5ae]|=0x0f        # FUJI rescued, 7F ROCKETs + FUJI hidden
        m[0xd464]=5;m[0xd465]=1                                # stage 5, MISTY the consort
    warp(0x94,0,s);T(60)
    hidden=[k for k in range(1,m[0xd4e1]+1) if m[0xc100+16*k]==0]
    print('7F pictures',[hex(m[0xc100+16*k]) for k in range(1,m[0xd4e1]+1)],'hidden (picture 0)',hidden)
    ok(hidden and map_tiles_ok(),'Tower 7F has objects hidden with picture 0, map tiles fine before the menu')
    t,s_=menu_roundtrip();shot('v36_tower7f_menu')
    ok(t,'Tower 7F: map tiles unchanged after START menu open/close (was overwritten by a picture-0 sprite sheet)')
    ok(s_,'Tower 7F: the screen looks exactly the same after the menu')
    for i in range(3):t,_=menu_roundtrip()
    ok(t,'Tower 7F: still fine after three more menus')
    # MISTY left her gym (consort): her slot is picture 0 there
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x41
    m[0xd75e]|=0xcc;m[0xd365]=0x94
    bfs_to(16,10);p.button('left',16);T(200);T(60)
    ok(m[0xd35e]==0x41 and m[0xc110]==0,'in MISTY\'s gym, her object hidden (picture 0)')
    t,s_=menu_roundtrip();shot('v36_gym_menu')
    print('gym tiles',t);ok(t,'MISTY\'s gym: map tiles unchanged after the START menu (v35: all 96 overwritten)')
    # normal case: Pallet (no hidden objects) as before
    load('pallet_with_ghost');T(30);t,s_=menu_roundtrip()
    ok(t,'Pallet Town (nothing hidden): START menu as before')
elif MODE=='agatha':
    def s():
        m[0xd769]|=0x8e;m[0xd7e0]|=0x80;m[0xd5ae]|=0x0f;m[0xd464]=3
    warp(0x94,0,s)
    gi=list(m[0xd164:0xd16a]).index(0x1f)
    def talk():
        bfs_to(4,11);seen.clear();p.button('up',8);T(30);press_('a',90);quiet=0
        for k in range(60):
            if not box():
                quiet+=1
                if quiet>=4:break
                T(40);continue
            quiet=0;press_('a',90)
        return allt()
    m[0xd16b+44*gi+33]=49;t=talk();print('Lv49:',t[-120:])
    ok('too weak' in t and m[0xd464]==3,'AGATHA: GHOST Lv49 is still too weak')
    m[0xd16b+44*gi+33]=50;t=talk();print('Lv50:',t[-160:])
    ok(('devotion' in t if VERSION<46 else 'truly love' in t) and m[0xd464]==4,'AGATHA: GHOST Lv50 is enough (HELIX FOSSIL back, consort stage)')
elif MODE=='cap':
    def exp(i):b=0xd16b+44*i;return m[b+14]<<16|m[b+15]<<8|m[b+16]
    def battle(species,lv,ex):
        load('pallet_with_ghost');lead(species);b=0xd16b
        m[b+33]=lv;m[b+14]=ex>>16;m[b+15]=ex>>8&255;m[b+16]=ex&255
        m[b+8]=0x0a;m[b+29]=0x3f;m[0xd455]=255                  # SCRATCH in slot 1 for the test
        m[0xd059]=0xa5;m[0xd127]=5                              # a wild Lv5 RATTATA right away
        for i in range(300):
            if m[0xd057]:break
            p.tick()
        assert m[0xd057]==1,'no battle'
        fight(weak_enemy=True)
        for i in range(30):press_('a',60)
        return m[b+33],exp(0)
    CURVE={125000,117360,100000,156250}                         # Lv50 exp on the four growth curves
    lv,e=battle(0x1f,49,124990)                                 # just below Lv50 (medium fast: 125000)
    print('GHOST 49 ->',lv,e);ok(lv==50,'GHOST grows to Lv50')
    lv,e=battle(0x1f,50,0x0f0000)                               # far above any Lv50 value
    print('GHOST 50 + huge exp ->',lv,e);ok(lv==50 and e in CURVE,'GHOST stays Lv50, exp capped at the Lv50 value (%d)'%e)
    lv,e=battle(0x1f,60,0x0f0000)
    print('GHOST 60 (older save) ->',lv,e);ok(lv==60,'a GHOST already above 50 keeps its level and grows no further')
    lv,e=battle(0xb0,50,0x0f0000)
    print('CHARMANDER 50 + huge exp ->',lv,e);ok(lv>50,'CHARMANDER still grows past Lv50 (normal case)')
elif MODE=='giovanni':
    def s():m[0xd837]|=0x30;m[0xd838]|=0x01
    warp(0xeb,3,s);lead(0x1f);m[0xd16b+29]=0x3f
    bfs_to(14,6);p.button('up',16);T(60)
    for i in range(40):
        if m[0xd057]:break
        press_('a',90)
    ok(m[0xd057]==2 and m[0xd031]==0x1d,'GIOVANNI battle at SILPH 11F')
    seen.clear();screens.clear();fight()
    lines=[l for sc in screens for l in sc if 'cult' in l or 'GIOVANNI:' in l]
    shown=[sc for sc in screens if any('cult' in l for l in sc)]
    print('defeat screen',shown[-1] if shown else None)
    ok(shown and not any('GIOVANNI: GIOVANNI' in l for sc in screens for l in sc),'no doubled "GIOVANNI: GIOVANNI:"')
    ok(any('GIOVANNI:' in l for l in shown[-1]) and any('Damn that cult' in l for l in shown[-1]),'"GIOVANNI:" then "Damn that cult..."')
elif MODE in ('blue','blue_normal'):
    def s():
        if MODE=='blue_normal':m[0xd451]=0
    warp(0xd4,4,s)
    lead(0x1f if MODE=='blue' else 0xb0);m[0xd16b+29]=0x3f
    for i in range(40):                                        # walk to BLUE (3,3); his trigger starts the battle
        if m[0xd057] or (m[0xd361],m[0xd362])==(3,3):break
        cy,cx=m[0xd361],m[0xd362]
        for d in ((['up'] if cy>3 else ['down'] if cy<3 else [])+(['left'] if cx>3 else ['right'] if cx<3 else []))[::(1 if i%2 else -1)]:
            p.button(d,8);T(24)
            if (m[0xd361],m[0xd362])!=(cy,cx) or m[0xd057]:break
    for i in range(60):
        if m[0xd057]:break
        press_('a',90)
    ok(m[0xd057]==2,'BLUE battle at SILPH 7F')
    if MODE=='blue_normal':
        for i in range(1,6):m[0xd8a5+44*i]=0;m[0xd8a6+44*i]=0
    fight(weak_enemy=MODE=='blue_normal');seen.clear()
    for i in range(45):press_('a',90)
    t=allt();print('AFTER',t[-400:])
    if MODE=='blue':
        ok('happened to you' in t and 'dark power' in t and 'moving on up' not in t and m[0xd463]==2,
           'GHOST route: BLUE doesn\'t understand, sees the corruption, vows to overcome the dark power (hero mode set)')
    else:
        ok('moving on up' in t and 'dark power' not in t,'off the GHOST route: BLUE\'s original after-battle text')
