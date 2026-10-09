# v19 secret chamber. Modes:
#  closed  - quest before stage 5: 7F looks as in v17 (AGATHA at x11, no stairs behind her, second AGATHA hidden)
#  chamber - stage 5 + MISTY: graves behind AGATHA open into stairs, AGATHA beside them at (2,10); walk up the stairs
#            -> map 0x69 (TOWER CHAMBER): MR. MU in the centre, no wild POKeMON, talk to him; walk the room; back down
#            the stairs -> 7F on the stairs step; leave and come back -> still open
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
    T(10);return prev
def tower(stage,consort=1):
    load('pallet_with_ghost');m[0xd455]=255
    m[0xd769]|=0x8e;m[0xd7e0]|=0x80;m[0xd5ae]|=0x0f;m[0xd464]=stage;m[0xd465]=consort
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x94
    for i in range(6):
        if m[0xd35e]==0x94:break
        p.button('up',8);T(24)
    T(120);m[0xd887]=0;print('7F',pos(),flush=True)
def spr(k):return (hex(m[0xc100+16*k]),m[0xc204+16*k]-4,m[0xc205+16*k]-4)
def block_at(y,x):                                            # current block id under a step (wOverworldMap, border 3)
    w=m[0xd369]
    return m[0xc6e8+(y//2+3)*(w+6)+x//2+3]
V20=VERSION>=20
STAIRS=(19,11) if V20 else (18,11);MU=(11,11) if V20 else (10,10)
S='/tmp/claude-0/-home-user-pokemonCreepyBlackTragicEdition/f8b43b79-da25-5b1d-8781-e68cb6d59e07/scratchpad/'

if MODE=='closed':
    tower(4,0)
    print('AGATHA objects',spr(5),spr(9),'block behind',hex(block_at(1,11)))
    assert spr(5)==('0x39',3,11) and m[0xc190]==0 and block_at(1,11)==0x02
    print('PASS before stage 5: no secret stairs, AGATHA in front of the wall')
elif MODE=='chamber':
    tower(5)
    print('AGATHA objects',spr(5),spr(9),'girl',spr(6),'block behind',hex(block_at(1,11)))
    assert m[0xc150]==0 and spr(9)==('0x39',2,10) and block_at(1,11)==0x11
    bfs_to(2,11);p.screen.image.save(S+'v19_7f_door.png')
    p.button('up',16);T(200)
    print('after the stairs',pos(),'grass',m[0xd887],'music',hex(m[0xc0ee]),'tileset',hex(m[0xd367]))
    assert pos()==(0x69,STAIRS[1],STAIRS[0])
    print('chamber objects',[spr(k) for k in range(1,3)],'missable list',[hex(x) for x in m[0xd5ce:0xd5d2]])
    assert spr(1)==('0x10',MU[0],MU[1]) and m[0xd887]==0
    p.screen.image.save(S+'v19_chamber_entry.png')
    reach=bfs_to(MU[0]+1,MU[1])                               # in front of MR. MU (he faces down)
    print('reachable steps',len(reach))
    if VERSION<23:                                            # v23: his last talk + the ritual battle (t34_v23.py)
        seen.clear();p.button('up',8);T(30)
        for k in range(10):
            press_('a',90)
            if not box() and k>2:break
        print('MU says',[s for s in seen if s.endswith(('.','!','?'))])
        assert 'found' in allt()
        p.screen.image.save(S+'v19_chamber_mu.png')
    for y,x in (((4,11),(11,4),(11,18),(17,11)) if V20 else ((4,10),(10,4),(10,16),(16,10))):   # around the circle
        bfs_to(y,x);print('walked to',(y,x))
    print('PASS the chamber loads, MR. MU stands in the centre and talks, the room can be walked')
    bfs_to(STAIRS[0]-1,11);p.button('down',16);T(200)
    print('back',pos(),'AGATHA',spr(9))
    assert pos()==(0x94,11,1)
    p.button('down',16);T(60);print('off the stairs',pos())
    assert pos()==(0x94,11,2)
    print('PASS the stairs lead back to Tower 7F behind AGATHA')
elif MODE=='saveload':
    import harness
    from pyboy import PyBoy
    tower(5);bfs_to(2,11);p.button('up',16);T(200);assert pos()[0]==0x69
    bfs_to(14,11 if V20 else 10);where=pos()
    p.button('start',8);T(90)
    for i in range(8):
        if '▲SAVE' in ' '.join(txt()):break
        p.button('down',8);T(30)
    p.button('a',8);T(200);p.button('a',8)
    for i in range(900):
        T(1)
        if i%120==60 and seen and 'SAVE' in seen[-1] and 'saved' not in seen[-1].lower():p.button('a',8)
    assert any('saved' in s.lower() for s in seen)
    sram=[[m[bk,ad] for ad in range(0xa000,0xc000)] for bk in range(4)]
    p.stop(save=False)
    harness.p=PyBoy(ROM,window='null',sound_emulated=False);harness.p.set_emulation_speed(0);harness.m=harness.p.memory
    p=harness.p;m=harness.m
    for bk in range(4):
        for i,v in enumerate(sram[bk]):m[bk,0xa000+i]=v
    p.tick(300)
    for i in range(40):
        if 'CONTINUE' in ' '.join(txt()):break
        p.button('start' if i%2 else 'a',8);p.tick(120)
    p.button('a',8);p.tick(200);p.button('a',8);p.tick(400)
    for i in range(10):
        if m[0xd35e]==0x69 and not box():break
        p.button('a',8);p.tick(120)
    p.tick(120);print('saved at',where,'continued at',pos(),'MU',spr(1))
    assert pos()==where and spr(1)==('0x10',MU[0],MU[1])
    p.screen.image.save(S+'v19_continue.png')
    bfs_to(STAIRS[0]-1,11);p.button('down',16);T(200);print('down the stairs',pos())
    assert pos()==(0x94,11,1)
    print('PASS save in the chamber -> power cycle -> CONTINUE in the chamber, stairs still work')
elif MODE=='fossils':                                          # v22: a fossil on each statue's stand
    tower(5);bfs_to(2,11);p.button('up',16);T(200)
    objs=[spr(k) for k in range(2,5)];print('fossil objects',objs)
    assert objs==[('0x3e',7,11),('0x3e',15,6),('0x3e',15,16)]
    for (y,x),name in (((8,11),'OLD AMBER'),((16,6),'DOME FOSSIL'),((16,16),'HELIX FOSSIL')):
        bfs_to(y,x);seen.clear();p.button('up',8);T(30)
        for k in range(6):
            press_('a',90)
            if not box() and k>1:break
        assert name in allt() and 'stand' in allt(),allt()[-80:]
    print('PASS three fossils on the stands in front of the statues, each named')
