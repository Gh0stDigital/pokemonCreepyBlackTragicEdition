# v18 SILPH CO. on the GHOST route. Modes:
#  unlock    - first visit to Pokemon Tower 7F: Saffron gates open, hideout GIOVANNI gone (beaten flag + hidden),
#              SILPH SCOPE ball shown; off the GHOST route nothing changes; hideout already done -> scope ball untouched
#  giovanni  - SILPH 11F: new GIOVANNI speech, battle with GHOST + CURSE: "Damn that cult...!", no trainer phase,
#              "forces ... you can't even understand", he leaves; PRESIDENT: MASTER BALL story + the ball
#  normal    - same floor off the GHOST route (GHOST not owned, CHARMANDER fights): original GIOVANNI/PRESIDENT texts
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
def lead(species):
    i=list(m[0xd164:0xd16a]).index(species)
    if i:
        for base,size in ((0xd16b,44),(0xd2b5,11),(0xd273,11)):
            a=list(m[base:base+size]);b=list(m[base+size*i:base+size*(i+1)])
            m[base:base+size]=b;m[base+size*i:base+size*(i+1)]=a
        m[0xd164],m[0xd164+i]=m[0xd164+i],m[0xd164]
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
def fight(limit=600):
    for i in range(limit):
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
def bag():return {m[0xd31e+2*i]:m[0xd31f+2*i] for i in range(m[0xd31d])}
HB=0xd5a6+0x83//8

if MODE=='unlock':
    for ghost,done in ((1,0),(0,0),(1,1)):
        def s():
            m[0xd451]=ghost;m[0xd728]&=~0x40
            if done:m[0xd81b]|=0x80;m[HB]|=0x88          # hideout already cleared, scope ball already taken
            else:m[0xd81b]&=~0x80;m[HB]=(m[HB]&~0x08)|0x80
        warp(0x94,0,s)
        st=(m[0xd728]>>6&1,m[0xd81b]>>7,m[HB]>>3&1,m[HB]>>7&1)
        print('ghost',ghost,'done before',done,'-> gates open, hideout done, GIOVANNI hidden, scope ball hidden =',st)
        if ghost and not done:assert st==(1,1,1,0)
        elif ghost:assert st==(1,1,1,1)
        else:assert st==(0,0,0,1)
    print('PASS Tower 7F opens Saffron/SILPH and clears GIOVANNI out of the hideout (GHOST route only)')
    # the hideout B4F really has no GIOVANNI now
    warp(0xca,0,lambda:(m.__setitem__(0xd81b,m[0xd81b]|0x80),m.__setitem__(HB,(m[HB]|0x08)&~0x80)));T(60)
    print('B4F toggle list',[hex(x) for x in m[0xd5ce:0xd5d8]],'flags',hex(m[HB]))
    lst=list(m[0xd5ce:0xd5e0]);pairs=dict(zip(lst[0::2],lst[1::2]))
    assert pairs.get(1)==0x83 and m[HB]&0x08                   # the game's own check: sprite 1 -> toggle 83, hidden
    print('PASS hideout B4F: GIOVANNI is not there')
elif MODE in ('giovanni','normal'):
    def s():
        m[0xd837]|=0x30;m[0xd838]|=0x01                       # the two 11F grunts beaten, card-key door open
        if MODE=='normal':m[0xd451]=0
    warp(0xeb,3,s)                                            # the teleport pad into the PRESIDENT's room
    if MODE=='giovanni':lead(0x1f);m[0xd16b+29]=0x3f
    else:lead(0xb0);m[0xd16b+29]=0x3f;m[0xd16b+30]=0x3f      # CHARMANDER leads, PP to spare
    print('objects',[(hex(m[0xc100+16*k]),m[0xc204+16*k]-4,m[0xc205+16*k]-4) for k in range(1,6)])
    phase3=[]
    def watch(c):
        if m[0xd05a]==3:phase3.append(1)
    seen.clear()
    bfs_to(14,6);p.button('up',16);T(60)                       # GIOVANNI's trigger tile (13,6)
    for i in range(40):
        if m[0xd057]:break
        press_('a',90)
    print('battle',m[0xd057],'class',hex(m[0xd031]),flush=True);assert m[0xd057]==2 and m[0xd031]==0x1d
    pre=allt();seen_pre=list(seen);seen.clear()
    if MODE=='normal':
        for i in range(1,6):m[0xd8a5+44*i]=0;m[0xd8a6+44*i]=0  # his other POKeMON already down: one hit ends it
    for i in range(800):
        if m[0xd05a]==3:phase3.append(1)
        if MODE=='normal' and m[0xd057]:m[0xcfe6]=0;m[0xcfe7]=1;m[0xd015]=0;m[0xd016]=99   # enemy at 1 HP, ours healthy
        if m[0xd057]==0:break
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
    battle=allt();seen.clear()
    for i in range(40):press_('a',90)
    post=allt()
    print('PRE',[x for x in seen_pre if x.endswith(('!','.','?'))][:8]);print('BATTLE',battle[-300:]);print('POST',post[-300:]);print('trainer phase seen',bool(phase3),'D838',bin(m[0xd838]))
    if MODE=='giovanni':
        assert 'watching you' in pre and 'weapon' in pre and 'Damn' in battle and 'cult' in battle
        assert not phase3 and 'forces' in post and m[0xd838]&0x80
        print('PASS GIOVANNI: speech, cult line, no trainer phase, warning, he leaves')
    else:
        assert 'grown-up' in pre and 'lost again' in battle and 'never fall' in post and 'cult' not in battle+post
        print('PASS off the GHOST route: original GIOVANNI texts')
    # PRESIDENT (object 1 at y5 x7): talk from his left
    seen.clear();bfs_to(5,6);p.button('right',8);T(30);press_('a',90)
    for i in range(30):
        if not box() and i>3:break
        press_('a',90)
    t=allt();print('PRESIDENT',t[-300:],bag())
    assert 0x01 in bag()
    if MODE=='giovanni':assert 'old' in t and 'vanished' in t
    else:assert 'vanished' not in t
    print('PASS PRESIDENT gives the MASTER BALL%s'%(' after the vanished-friend story' if MODE=='giovanni' else ' with his usual line'))
