# v15 checks. Modes:
#  cer_curse  - GHOST route + a murder: BLUE asks about the killer and wants to test you; GHOST kills his team
#               -> shock mode starts, "Are YOU the killer!?" instead of the BILL chat
#  cer_win    - same, but won without GHOST (TACKLE, RUN in the trainer phase): "gotten stronger" + usual BILL chat
#  cer_normal - GHOST route, no murder, won without GHOST: the original BLUE lines
#  cer_curse_nomurder - no murder, GHOST kills his team: shock mode, grief line without the killer question
#  cer_shock_skip - shock mode from an earlier battle: no BLUE at Cerulean, the Rocket thief flag is untouched
#  bill       - BILL: lore once, right after the S.S. TICKET; later talks: original line only
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
def warp_from_pallet(mapid,warpid):
    load('pallet_with_ghost');lead(0x1f);m[0xd16b+29]=0x3f;m[0xd455]=255
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=warpid;m[0xd3af+4*i+3]=mapid
    for i in range(6):
        if m[0xd35e]==mapid:break
        p.button('up',8);T(24)
    T(120);print('arrived',pos(),flush=True)
def bfs_to(y,x,maxn=900):
    def snap():
        f=io.BytesIO();p.save_state(f);f.seek(0);return f.read()
    def rest(b):p.load_state(io.BytesIO(b))
    start=(m[0xd361],m[0xd362]);prev={start:None};st={start:snap()};q=deque([start]);mp=m[0xd35e]
    while q and (y,x) not in prev and len(prev)<maxn:
        c=q.popleft()
        for d,(dy,dx) in (('up',(-1,0)),('down',(1,0)),('left',(0,-1)),('right',(0,1))):
            n=(c[0]+dy,c[1]+dx)
            if n in prev:continue
            rest(st[c]);p.button(d,8);p.tick(24)
            if m[0xd35e]!=mp or m[0xd057] or box():continue
            if (m[0xd361],m[0xd362])==n:prev[n]=(c,d);st[n]=snap();q.append(n)
    assert (y,x) in prev,('no path',(y,x),len(prev),sorted(prev)[:5],min(prev),max(prev))
    path=[];c=(y,x)
    while prev[c]:c,d=prev[c];path.append(d)
    rest(st[start])
    for d in reversed(path):p.button(d,8);T(24)
    T(10)
def fight(limit=500,hp1=False,spare=False):
    for i in range(limit):
        if m[0xd057]==0:return
        if hp1 and m[0xcfe6]|m[0xcfe7]:m[0xcfe6]=0;m[0xcfe7]=1
        b=clean(box())
        if spare and m[0xd05a]==3 and 'FIGHT' in b and 'RUN' in b:
            press_('down',20);press_('right',20);press_('a',200);continue
        if 'FIGHT' in b and 'RUN' in b:
            for k in range(4):
                if '▲FIGHT' in box():break
                press_('up',20);press_('left',20)
            press_('a',60)
            for k in range(4):press_('up',10)
            press_('a',200);continue
        if 'Bring out' in b or 'change' in b.lower():press_('b',60);continue
        press_('a',90)
def show(tag):
    print(tag);[print('  TEXT:',s) for s in dict.fromkeys(seen) if s.endswith(('!','?','.'))]

if MODE.startswith('cer'):
    warp_from_pallet(0x40,0);m[0xd365]=3                       # Cerulean Pokemon Center; its door now leads to Cerulean
    for i in range(6):
        if m[0xd35e]==3:break
        p.button('down',8);T(24)
    T(120);print('Cerulean',pos(),flush=True);m[0xd887]=0
    m[0xd75b]|=0x80                                            # Rocket thief already beaten: his trigger stays quiet
    m[0xd453]=0 if MODE in ('cer_normal','cer_curse_nomurder') else 1;m[0xd463]=1 if MODE=='cer_shock_skip' else 0
    if MODE=='cer_shock_skip':m[0xd75b]&=~0x80;m[0xd75a]|=1   # what v15 shock mode leaves: BLUE flag set, thief open
    if MODE in ('cer_win','cer_normal'):m[0xd16b+8:0xd16b+12]=[0x21,0,0,0]      # GHOST knows only TACKLE
    bfs_to(8,21);seen.clear()
    for i in range(3):
        if m[0xd361]<=6:break
        p.button('up',16);T(60)
    for i in range(40):
        if m[0xd057]:break
        press_('a',90)
    show('PRE');print('battle',m[0xd057],'class',m[0xd031],pos(),'script',m[0xd60f],'d75a',m[0xd75a],flush=True);shot('v15_cer_pre')
    if MODE=='cer_shock_skip':
        assert m[0xd057]==0 and 'RIVAL' not in allt() and 'BLUE' not in allt()
        print('PASS shock mode: no BLUE at Cerulean');raise SystemExit
    assert m[0xd057]==2 and m[0xd031]==25
    if MODE in ('cer_normal','cer_curse_nomurder'):assert 'struggling' in allt() and 'killing' not in allt()
    else:assert 'killing' in allt() and 'test you' in allt() and 'struggling' not in allt()
    seen.clear()
    if MODE.startswith('cer_curse'):fight()
    else:fight(hp1=True,spare=True)
    for i in range(30):
        press_('a',90)
        if m[0xd75a]&1 and not box() and i>4:break
    show('POST')
    print('mode',m[0xd463],'cerulean',m[0xd75a]&1,'thief',m[0xd75b]>>7,'ssanne',m[0xd665],'r22',m[0xd7eb]>>7,'murder',m[0xd453])
    t=allt()
    if MODE=='cer_curse':
        assert m[0xd463]==1 and 'died' in t and 'Are YOU the' in t and 'Stay away' in t and 'BILL' not in t
        print('PASS murder + GHOST: shock mode starts at Nugget Bridge, BLUE asks if you are the killer')
    elif MODE=='cer_curse_nomurder':
        assert m[0xd463]==1 and 'died' in t and 'Stay away' in t and 'killer' not in t and 'BILL' not in t
        print('PASS no murder + GHOST: shock mode, grief line without the killer question')
    elif MODE=='cer_win':
        assert m[0xd463]==0 and 'gotten stronger' in t and 'cocky' in t and 'BILL' in t and 'Stay away' not in t
        print('PASS murder, no GHOST: killer pre-battle text, "gotten stronger" + usual BILL chat')
    else:
        assert m[0xd463]==0 and 'BILL' in t and 'stronger' not in t and 'Stay away' not in t
        print('PASS no murder: original BLUE lines')

elif MODE=='bill':
    warp_from_pallet(0x58,0);m[0xd887]=0
    # the real scene: talk to BILL (still a POKeMON), YES, then run the Cell Separator on the PC
    bfs_to(6,6);p.button('up',8);T(30)
    for k in range(30):
        press_('a',90)
        if 'YES' in box():press_('a',90)
    bfs_to(5,1);p.button('up',8);T(30)
    for k in range(12):
        press_('a',120)
        if 'YES' in box():press_('a',90)
    T(600)
    for k in range(12):press_('a',120)
    T(300);print('BILL',(m[0xc204+0x20]-4,m[0xc205+0x20]-4),'visible',m[0xc122]!=0xff,'box',clean(box()))
    for k in range(6):
        if not box():break
        press_('b',60)
    def talk_bill():
        bfs_to(m[0xc204+0x20]-4+1,m[0xc205+0x20]-4);seen.clear();p.button('up',8);T(30)
        for k in range(60):
            press_('a',90)
            if not box() and k>3:break
        return allt()
    t1=talk_bill();show('FIRST');n=m[0xd31d];bag=[m[0xd31e+2*i] for i in range(n)]
    print('ticket flag',m[0xd7f2]>>4&1,'S.S.TICKET in bag',0x3f in bag)
    assert m[0xd7f2]&0x10 and 0x3f in bag and 'cruise' in t1 and 'LAVENDER TOWN' in t1 and 'PROF.OAK' in t1
    assert t1.index('cruise')<t1.index('LAVENDER')                 # after his usual S.S. ANNE line
    t2=talk_bill();show('SECOND')
    assert 'LAVENDER' not in t2 and 'cruise' in t2
    print('PASS BILL tells the tribe story once, right after the S.S. TICKET; later talks are unchanged')
