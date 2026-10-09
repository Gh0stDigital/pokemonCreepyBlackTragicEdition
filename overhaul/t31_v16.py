# v16 AGATHA quest. Modes:
#  hostage   - GHOST route, Pokemon Tower 7F before FUJI is rescued: AGATHA is there, "tied me up" line, girls hidden
#  noghost   - not on the GHOST route: no AGATHA
#  full      - after the rescue: intro + relics asked; relics (DOME/AMBER/HELIX) taken; vessel asked; MASTER BALL handed
#              over (YES); GHOST too weak; GHOST Lv100 -> HELIX FOSSIL back + consort; MISTY (beaten) takes the shell
#              and leaves her gym; she and AGATHA talk on 7F
#  mu        - PRETA instead of the DOME FOSSIL: "already woken some" note, relics accepted
#  labfail   - a fossil revived at the Cinnabar lab: sad text, quest failed; lament on the next talk; AGATHA gone
#              after leaving and coming back
#  ballfail  - got the MASTER BALL from SILPH, used it: failure text
#  ballno    - NO to handing over the MASTER BALL: ball kept, still at the vessel stage
#  alldead   - MISTY, ERIKA and SABRINA all killed: the ritual can't be finished
#  gyms      - ERIKA / SABRINA / MISTY are gone from their gym only when chosen
#  girl_normal - beaten MISTY before the consort stage: her usual after-battle line, no shell question
from harness import *
import sys,io
from collections import deque
MODE=sys.argv[1]
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
seen=[]
def T(n):
    for _ in range(n):
        p.tick();b=clean(box())
        if b and (not seen or seen[-1]!=b):seen.append(b)
def press_(k,n=60):p.button(k,8);T(n)
def allt():return ' '.join(seen)
def bfs_to(y,x,maxn=900):
    def snap():
        f=io.BytesIO();p.save_state(f);f.seek(0);return f.read()
    def rest(b):p.load_state(io.BytesIO(b))
    for k in range(10):                                       # let the game take input again (text just closed)
        if not box() and m[0xcd6b]==0:break
        p.button('b',8);T(40)
    T(30)
    start=(m[0xd361],m[0xd362]);prev={start:None};st={start:snap()};q=deque([start]);mp=m[0xd35e]
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
    T(120);print('arrived',pos(),flush=True)
def bag():return {m[0xd31e+2*i]:m[0xd31f+2*i] for i in range(m[0xd31d])}
def set_bag(items):
    m[0xd31d]=len(items)
    for i,(it,q) in enumerate(items):m[0xd31e+2*i]=it;m[0xd31f+2*i]=q
    m[0xd31e+2*len(items)]=0xff
def ghost_level(lv):
    i=list(m[0xd164:0xd16a]).index(0x1f);m[0xd16b+44*i+33]=lv
def pic(k):return m[0xc100+0x10*k]
def talk(y,x,face='up',answer=None,n=80):
    bfs_to(y,x);seen.clear();p.button(face,8);T(30);press_('a',90);quiet=0
    for k in range(n):
        b=clean(' '.join(txt()))                              # the YES/NO box sits above the text box
        if 'YES' in b and 'NO' in b and answer:
            if answer=='no':press_('down',30)
            press_('a',90);answer=None;continue
        if not box():
            quiet+=1
            if quiet>=4:break
            T(40);continue
        quiet=0;press_('a',90)
    T(60);return allt()
def tower(state_fn=None,rescued=True):
    def setup():
        m[0xd769]|=0x0e|(0x80 if rescued else 0)               # three ROCKETs beaten (+ FUJI rescued)
        if rescued:m[0xd7e0]|=0x80;m[0xd5ae]|=0x0f   # 7F ROCKETs + FUJI hidden (toggles 40-43), as after the real rescue
        if state_fn:state_fn()
    warp(0x94,0,setup);m[0xd887]=0
AG_X=11 if VERSION>=17 else 9;GIRL_X=10 if VERSION>=17 else 11   # v17: AGATHA on FUJI's right, the girl on her left
def agatha(answer=None):return talk(4,AG_X,'up',answer)
DOME,HELIX,AMBER,MB=0x29,0x2a,0x1f,0x01

if MODE in ('hostage','noghost'):
    tower(lambda:(m.__setitem__(0xd451,0) if MODE=='noghost' else None),rescued=False)
    print('sprites 5-8',[hex(pic(k)) for k in range(5,9)],'positions',[(m[0xc204+0x10*k]-4,m[0xc205+0x10*k]-4) for k in range(4,9)])
    shot('v16_tower7f');print('AGATHA x',m[0xc255]-4,'girl x',[m[0xc205+0x10*k]-4 for k in (6,7,8)])
    if VERSION>=17:assert m[0xc255]-4==11
    assert all(pic(k)==0 for k in (6,7,8))
    if MODE=='noghost':
        assert pic(5)==0;print('PASS off the GHOST route: no AGATHA on Tower 7F');raise SystemExit
    assert pic(5)==0x39
    t=agatha();print(t[-200:])
    assert 'tied me up' in t and m[0xd464]==0
    print('PASS AGATHA held with FUJI before the rescue; girls hidden')
elif MODE=='full':
    tower()
    t=agatha();print('1:',t[-160:]);assert 'terrible' in t and 'whirlpool' in t and m[0xd464]==1 and 'Bring me' in t
    set_bag([(DOME,1),(AMBER,1),(HELIX,1),(0x14,3)])
    t=agatha();print('2:',t[-160:]);assert 'vessel' in t and 'SILPH' in t and m[0xd464]==2
    b=bag();print('bag',b);assert DOME not in b and AMBER not in b and HELIX not in b and b.get(0x14)==3
    t=agatha();assert 'Find the' in t and m[0xd464]==2
    set_bag([(MB,1)]);ghost_level(40)
    t=agatha(answer='yes');print('3:',t[-200:]);assert 'handed' in t and MB not in bag() and m[0xd464]==3 and 'too weak' in t
    ghost_level(100)
    t=agatha();print('4:',t[-200:]);assert 'devotion' in t and 'LAVENDER' in t and m[0xd464]==4 and bag().get(HELIX)==1
    print('PASS AGATHA: relics, vessel, GHOST power, HELIX FOSSIL back for the consort')
    st=io.BytesIO();p.save_state(st)
    # MISTY: beaten (badge event + TM), gets the shell
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x41
    m[0xd75e]|=0xcc;m[0xd365]=0x94
    bfs_to(16,10);p.button('left',16);T(200)
    print('gym?',pos());assert m[0xd35e]==0x41
    t=talk(3,4,'up',answer='yes');print('5:',t[-220:])
    assert 'Give MISTY' in t and 'LAVENDER TOWN' in t and m[0xd465]==1 and m[0xd464]==5 and HELIX not in bag()
    print('PASS MISTY takes the HELIX FOSSIL')
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x41
    bfs_to(12,4);p.button('down',16);T(200);print('gym again',pos(),'sprite1',hex(pic(1)))
    assert m[0xd35e]==0x41 and pic(1)==0
    print('PASS MISTY has left her gym')
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x94
    bfs_to(12,4);p.button('down',16);T(60);p.button('down',16);T(200);print('tower',pos(),'sprites',[hex(pic(k)) for k in range(5,9)])
    m[0xd887]=0
    assert m[0xd35e]==0x94 and pic(5)==0x39 and pic(6)==0x1d and pic(7)==0 and pic(8)==0
    t=talk(4,GIRL_X,'up');print('6:',t[-120:]);assert 'chills' in t
    t=agatha();print('7:',t[-200:],pos());assert 'brought her' in t
    bfs_to(5,10);shot('v17_tower_consort')
    print('PASS MISTY waits with AGATHA on Tower 7F')
elif MODE=='mu':
    def s():m[0xd464]=1;m[0xd164+1]=0xb6                       # PRETA in the party (stand-in for Mr. Mu's awakening)
    tower(s);set_bag([(AMBER,1),(HELIX,1)])
    t=agatha();print(t[-240:]);assert 'already woken' in t and 'better' in t and (VERSION<17 or "one's work" not in t) and m[0xd464]==2 and m[0xd466]&4
    print('PASS PRETA counts as the dome relic, with AGATHA\'s surprise')
elif MODE=='labfail':
    def s():m[0xd464]=1;m[0xd308]|=0x02                         # OMANYTE owned: revived at the lab
    tower(s);set_bag([(DOME,1),(AMBER,1),(HELIX,1)])
    t=agatha();print(t[-200:]);assert 'scientists' in t and m[0xd466]&1 and m[0xd464]==1
    t=agatha();assert 'weeping' in t
    print('PASS lab revival: AGATHA can\'t help, laments on the next talk')
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x94
    bfs_to(16,10);p.button('left',16);T(200)                     # leave (warp back to 7F = map reload)
    print('back',pos(),'flags',bin(m[0xd466]),'sprite5',hex(pic(5)))
    # a reload of 7F itself does not count as leaving; go via 6F
    if not m[0xd466]&2:
        for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x93
        bfs_to(16,10);p.button('left',16);T(200);print('6F',pos())
        for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x94
        p.button('up',16);T(30);p.button('down',16);T(200);print('7F?',pos())
    assert m[0xd466]&2
    q=list(m[0xd464:0xd467]);tower(lambda:m.__setitem__(slice(0xd464,0xd467),q));print('7F again: sprite5',hex(pic(5)))
    assert pic(5)==0
    print('PASS AGATHA is gone after leaving')
elif MODE=='ballfail':
    def s():m[0xd464]=2;m[0xd838]|=0x20
    tower(s);set_bag([(0x14,1)])
    t=agatha();print(t[-160:]);assert 'used the vessel' in t and m[0xd466]&1
    print('PASS used MASTER BALL: quest failed')
elif MODE=='ballno':
    def s():m[0xd464]=2
    tower(s);set_bag([(MB,1)])
    t=agatha(answer='no');print(t[-300:],bag(),m[0xd464]);assert 'ready' in t and bag().get(MB)==1 and m[0xd464]==2
    print('PASS NO keeps the MASTER BALL, AGATHA waits')
elif MODE=='alldead':
    def s():m[0xd464]=3;m[0xd4a7]|=0x54;ghost_level(100)
    tower(s)
    t=agatha();print(t[-200:]);assert 'killed them' in t and m[0xd466]&1 and m[0xd464]==3
    print('PASS all three girls dead: the ritual can\'t be finished')
elif MODE=='girl_normal':
    def s():m[0xd75e]|=0xcc;set_bag([(HELIX,1)])
    warp(0x41,0,s);m[0xd887]=0
    t=talk(3,4,'up');print(t[-200:])
    assert 'Give MISTY' not in t and m[0xd465]==0 and bag().get(HELIX)==1 and len(t)>0
    print('PASS beaten MISTY before the consort stage: usual line, no shell question')
elif MODE=='gyms':
    for n,mp,name in ((2,0x86,'ERIKA'),(3,0xb2,'SABRINA'),(1,0x41,'MISTY')):
        for consort in (n,0 if n!=1 else 2):
            warp(mp,0,lambda:m.__setitem__(0xd465,consort));T(60)
            print(name,'consort',consort,'leader sprite',hex(pic(1)))
            assert (pic(1)==0)==(consort==n)
    print('PASS each girl leaves her gym only when she is the one chosen')
