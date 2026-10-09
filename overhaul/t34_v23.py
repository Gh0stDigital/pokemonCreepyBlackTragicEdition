# v23 MR. MU's last talk + the ritual battle. Modes:
#  ritual   - stage 5 chamber: talk to MR. MU (YES), MASTER BALL handed over, battle: YOU alone with STRUGGLE,
#             PKMN/ITEM/RUN refused, MR. MU never attacks, dies (gravestone bit) -> the MIRAGE ????? appears, FIGHT/RUN
#             and a POTION refused, MASTER BALL catches it with a black ball, no nickname; after: party back + ?????,
#             MASTER BALL gone, MR. MU is a (silent) gravestone
#  no       - answer NO: "this is truly goodbye", same battle starts (answer changes nothing)
#  bagfull  - 20 item kinds: MR. MU asks to make room, no battle, nothing changes
#  boxfull  - party 6 + PC box 20: same, "PC BOX is full"
#  partyfull- party of 6 (box not full): ????? goes to the PC box after the battle, the party comes back unchanged
#  wild     - normal case: a wild catch with a MASTER BALL still asks for a nickname and the ball stays normal
from harness import *
import sys,io,random
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
def scr():return clean(' '.join(txt()))
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
def spr(k):return (hex(m[0xc100+16*k]),m[0xc204+16*k]-4,m[0xc205+16*k]-4)
def bag():return [(m[0xd31e+2*i],m[0xd31f+2*i]) for i in range(m[0xd31d])]
def set_bag(items):
    m[0xd31d]=len(items)
    for i,(it,q) in enumerate(items):m[0xd31e+2*i]=it;m[0xd31f+2*i]=q
    m[0xd31e+2*len(items)]=0xff
def party():return list(m[0xd164:0xd164+m[0xd163]])
def nick(i):return ''.join(cm.get(v,'') for v in m[0xd2b5+11*i:0xd2b5+11*i+10]).split('@')[0].strip()
def tower(stage=5,consort=1):
    load('pallet_with_ghost');m[0xd455]=255
    m[0xd769]|=0x8e;m[0xd7e0]|=0x80;m[0xd5ae]|=0x0f;m[0xd464]=stage;m[0xd465]=consort
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x94
    for i in range(6):
        if m[0xd35e]==0x94:break
        p.button('up',8);T(24)
    T(120);m[0xd887]=0
def chamber():
    tower();bfs_to(2,11);p.button('up',16);T(200);assert pos()[0]==0x69,pos()
RIT=0xd467;MU,MIR,YOU=0x20,0x7a,0x79;POTION,MB=0x14,0x01
S='/tmp/claude-0/-home-user-pokemonCreepyBlackTragicEdition/f8b43b79-da25-5b1d-8781-e68cb6d59e07/scratchpad/'

def talk_mu(answer='yes',n=200):
    """talk to MR. MU from below; answer the YES/NO; stop when a battle starts or the talk ends"""
    bfs_to(12,11);seen.clear();p.button('up',8);T(30);press_('a',90);quiet=0
    for k in range(n):
        if m[0xd057]:break
        b=scr()
        if 'YES' in b and 'NO' in b and answer:
            if answer=='no':press_('down',30)
            press_('a',90);answer=None;continue
        if not box():
            quiet+=1
            if quiet>=6:break
            T(40);continue
        quiet=0;press_('a',90)
def menu_shown():s=scr();return 'FIGHT' in s and 'RUN' in s
def wait_menu(n=60):
    for k in range(n):
        if menu_shown() and m[0xd057]:return True
        if not m[0xd057]:return False
        press_('a',60)
    return False
def pick_item(name):
    for k in range(8):
        row=[l for l in txt() if '▶' in l or '▲' in l]
        if row and name in row[0]:return
        press_('down' if k<6 else 'up',20)
    raise AssertionError('cursor not on '+name+': '+str(txt()))
def choose(item):
    keys={'FIGHT':('left','up'),'ITEM':('left','down'),'PKMN':('right','up'),'RUN':('right','down')}[item]
    for k in keys:press_(k,20)
    press_('a',60)

if MODE in ('ritual','no','partyfull'):
    chamber()
    if MODE=='partyfull':                                   # six party members: copy GHOST's slot into 2..6
        n=m[0xd163]
        for i in range(n,6):
            m[0xd164+i]=m[0xd164];m[0xd16b+44*i:0xd16b+44*(i+1)]=m[0xd16b:0xd16b+44]
            m[0xd273+11*i:0xd273+11*(i+1)]=m[0xd273:0xd27e];m[0xd2b5+11*i:0xd2b5+11*(i+1)]=m[0xd2b5:0xd2c0]
        m[0xd163]=6;m[0xd16a]=0xff
    set_bag([(POTION,3)])
    before=party();before_mons=bytes(m[0xd16b:0xd16b+44*len(before)]);box_before=m[0xda80]
    print('party before',[hex(x) for x in before],'box',box_before,flush=True)
    talk_mu('no' if MODE=='no' else 'yes')
    t=allt();print('talk:',t[:200],'...',t[-260:])
    for key in ('meet again','successor','birth to you','LAVENDER','BLACK TAMER','transformation','missing',
                'ritual circle','replacement','received','MASTER BALL','life after death','no test'):
        assert key in t,key
    assert ('meet again.' in t or 'perhaps we' in t) and (('goodbye' in t) if MODE=='no' else ('perhaps we' in t))
    assert m[0xd057]==2 and m[RIT]==1,(m[0xd057],m[RIT])
    print('PASS the talk: speech, vessel, the question (%s) -> battle'%MODE.upper(),flush=True)
    assert wait_menu(),'no battle menu'
    print('battle: enemy',hex(m[0xcfe5]),'mine',hex(m[0xd014]),'party',[hex(x) for x in party()],'bag',bag())
    assert m[0xcfe5]==MU and m[0xd014]==YOU and party()==[YOU] and (MB,1) in bag()
    assert 'MR. MU wants' in allt() and 'stepped' in allt()
    p.screen.image.save(S+'v23_mu_battle.png')
    for cmd in ('PKMN','ITEM','RUN'):
        seen.clear();choose(cmd);T(60)
        for k in range(4):
            if menu_shown():break
            press_('a',60)
        assert 'kill me' in allt() and m[0xd057]==2,(cmd,allt())
    print('PASS PKMN / ITEM / RUN -> "No! You must kill me with your own hands!"',flush=True)
    if MODE=='no':sys.exit(0)
    # FIGHT: STRUGGLE only, until MR. MU dies
    seen.clear();turns=0;minhp=999
    for k in range(40):
        if m[0xcfe5]==MIR:break
        if menu_shown():
            choose('FIGHT');s=scr();assert 'STRUGGLE' in s,s
            press_('a',60);turns+=1
        else:press_('a',60)
        minhp=min(minhp,m[0xd015]<<8|m[0xd016])
    t=allt();print('fight:',t[-300:])
    assert m[0xcfe5]==MIR and m[RIT]==2 and m[0xd057]==1 and 'fight back' in t and 'died with' in t,(hex(m[0xcfe5]),m[RIT])
    assert m[0xd4a8]&2 and minhp>0 and 'gained' not in t
    print('PASS %d STRUGGLE turns, MR. MU never attacked (YOU kept %d HP), died, no EXP'%(turns,minhp),flush=True)
    for k in range(10):
        if menu_shown():break
        press_('a',60)
    assert 'MIRAGE' in allt() and 'appeared' in allt()
    p.screen.image.save(S+'v23_mirage.png')
    for cmd in ('FIGHT','PKMN','RUN'):
        seen.clear();choose(cmd);T(60)
        for k in range(4):
            if menu_shown():break
            press_('a',60)
        assert 'MASTER' in allt() and m[0xd057]==1 and m[0xcfe5]==MIR,(cmd,allt())
    seen.clear();choose('ITEM');T(30);s=scr();assert 'POTION' in s and 'MASTER' in s,s
    pick_item('POTION');press_('a',90)
    for k in range(3):
        if 'MASTER BALL can' in allt():break
        press_('a',60)
    assert 'MASTER BALL can' in allt() and m[0xd057]==1 and (POTION,3) in bag(),allt()
    print('PASS the MIRAGE: FIGHT / PKMN / RUN / POTION refused ("Only the MASTER BALL can hold it!")',flush=True)
    def bag_active():return any('▲' in l and ('POTION' in l or 'MASTER' in l or 'CANCEL' in l) for l in txt())
    for k in range(8):                                       # BagWasSelected brings the bag back after the text
        if bag_active():break
        if menu_shown():choose('ITEM')
        else:press_('a',60)
    assert bag_active(),txt()
    save('v23_mirage_bag')
    pick_item('MASTER');seen.clear();press_('a',10)
    black=False;nickname=False
    for k in range(3000):
        p.tick()
        if k%30==0:
            b=clean(box())
            if b and (not seen or seen[-1]!=b):seen.append(b)
            if 'caught' in b and not black:
                black=m[0xff48]==0xff;p.screen.image.save(S+'v23_black_ball.png');print('OBP0 at "caught":',hex(m[0xff48]),flush=True)
            if 'nickname' in b:nickname=True
            if not m[0xd057]:break
            if k%120==0:p.button('a',8)
    print('catch:',allt()[-200:])
    assert 'caught' in allt() and black and not nickname and m[0xd057]==0
    print('PASS MASTER BALL caught ?????: the ball turned black, no nickname prompt, the battle ended',flush=True)
    T(400)
    after=party();print('party after',[hex(x) for x in after],'nicks',[nick(i) for i in range(len(after))],'box',m[0xda80],'RIT',m[RIT],'bag',bag())
    assert m[RIT]==3 and (MB,1) not in bag()
    if MODE=='partyfull':
        n=m[0xda80];assert after==before and bytes(m[0xd16b:0xd16b+44*6])==before_mons and n==box_before+1 and m[0xda81+n-1]==MIR
        bn=''.join(cm.get(v,'') for v in m[0xde06+11*(n-1):0xde06+11*n]).split('@')[0].strip()
        assert bn=='?????' and m[0xda96+33*(n-1)]==MIR,bn
        print('PASS full party: ????? went to the PC box, the party came back unchanged',flush=True)
    else:
        assert after==before+[MIR] and bytes(m[0xd16b:0xd16b+44*len(before)])==before_mons and nick(len(before))=='?????'
        lvl=m[0xd16b+44*len(before)+33];print('????? level',lvl,'moves',[hex(x) for x in m[0xd16b+44*len(before)+8:0xd16b+44*len(before)+12]])
        print('PASS the party came back unchanged and ????? joined it',flush=True)
    print('MR. MU object',spr(1));assert spr(1)[0]=='0x49',spr(1)
    p.screen.image.save(S+'v23_after.png')
    if MODE=='ritual':save('v23_after_ritual')        # partyfull must not overwrite it (t34 sendout needs ????? in the party)
    seen.clear();p.button('up',8);T(30)
    for k in range(3):press_('a',90)
    print('grave talk:',repr(allt()))
    assert not allt() and m[0xd057]==0 and m[RIT]==3              # silent like every gravestone; no second ritual
    print('PASS MR. MU is a gravestone (silent like the others), the ritual cannot start again',flush=True)
elif MODE in ('bagfull','boxfull'):
    chamber()
    if MODE=='bagfull':set_bag([(0x14+i,1) for i in range(20)])
    else:
        n=m[0xd163]
        for i in range(n,6):m[0xd164+i]=m[0xd164];m[0xd16b+44*i:0xd16b+44*(i+1)]=m[0xd16b:0xd16b+44]
        m[0xd163]=6;m[0xd16a]=0xff;m[0xda80]=20
    b0=bag();p0=party()
    talk_mu();t=allt();print(t)
    assert ('bag is full' if MODE=='bagfull' else 'PC BOX is') in t and 'successor' not in t
    assert m[0xd057]==0 and m[RIT]==0 and m[0xd059]==0 and bag()==b0 and party()==p0
    print('PASS %s: MR. MU asks to make room first, no battle'%MODE,flush=True)
elif MODE=='wild':
    random.seed(3);load('pallet_with_ghost');m[0xd45c]=0;m[0xd455]=255           # no Mirage, GHOST fed
    set_bag([(MB,1),(POTION,1)])
    bfs_to(0,10)                                             # Pallet's north exit, around whatever is in the way
    for i in range(30):
        if m[0xd35e]==0xc and pos()[2]<30:break
        p.button('up',8);T(24)
    for i in range(800):
        if m[0xd057]:break
        walk_in(0xc,random.choice(['up','down','left','right']))
    assert m[0xd057]==1,'no wild battle'
    sp=m[0xcfe5];assert wait_menu()
    choose('ITEM');T(30);pick_item('MASTER');press_('a',10);black=None;nickname=False;seen.clear()
    for k in range(3000):
        p.tick()
        if k%30==0:
            b=clean(box())
            if b and (not seen or seen[-1]!=b):seen.append(b)
            if 'caught' in b and black is None:black=m[0xff48]==0xff;print('OBP0 at "caught":',hex(m[0xff48]))
            if 'nickname' in b and not nickname:nickname=True;p.screen.image.save(S+'v23_wild_nickname.png')
            if 'YES' in scr() and 'NO' in scr() and nickname:p.button('b',8)
            elif k%120==0:p.button('a',8)
            if not m[0xd057]:break
    print(allt()[-200:])
    assert black is False and nickname and m[RIT]==0 and party()[-1]==sp
    print('PASS normal wild catch (species %02x): nickname asked, ball not blackened'%sp,flush=True)
elif MODE=='sendout':                                         # v24: ????? (from the ritual) sent out shows its back pic
    load('v23_after_ritual');n=m[0xd163];i=list(m[0xd164:0xd164+n]).index(MIR)
    st=bytes(m[0xd16b+44*i:0xd16b+44*(i+1)]);ot=bytes(m[0xd273+11*i:0xd273+11*(i+1)]);nk=bytes(m[0xd2b5+11*i:0xd2b5+11*(i+1)])
    random.seed(4);load('pallet_with_ghost');m[0xd45c]=0;m[0xd455]=255
    m[0xd164]=MIR;m[0xd16b:0xd16b+44]=st;m[0xd273:0xd27e]=ot;m[0xd2b5:0xd2c0]=nk     # ????? leads
    bfs_to(0,10)
    for i in range(30):
        if m[0xd35e]==0xc and pos()[2]<30:break
        p.button('up',8);T(24)
    for i in range(800):
        if m[0xd057]:break
        walk_in(0xc,random.choice(['up','down','left','right']))
    assert m[0xd057]==1 and wait_menu()
    print('out:',hex(m[0xd014]),allt()[-80:]);p.screen.image.save(S+'v24_sendout.png')
    assert m[0xd014]==MIR and 'Go! ?????' in allt()
    print('PASS ????? sent out in a wild battle (back pic shown: see v24_sendout.png)',flush=True)
