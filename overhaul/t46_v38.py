# v38: the BLACK TAMER as a party member. Modes:
#  join     - the real climax (t35's cached ritual state): evolution starts on RED's picture (species 86) and ends on
#             BLACK; afterwards BLACK is party slot 1 (Lv1, perfect DVs, stats as Lv10), PRETA and AZHI join
#  owned    - same, PRETA already in the party: no second PRETA, AZHI still joins
#  card     - trainer card: BLACK TAMER picture when BLACK, RED's otherwise
#  faint    - BLACK at 1 HP takes a hit: stays at 1 HP, no "fainted"; CHARMANDER at 1 HP faints as before
#  exp      - BLACK wins a battle: no experience; CHARMANDER wins: experience as before
#  items    - POTION on BLACK: "It won't have any effect.", bag unchanged; POTION on CHARMANDER heals
#  pc       - PC deposit: BLACK refused (stays in the party); CHARMANDER is deposited
#  daycare  - Day Care: BLACK refused; Name Rater: BLACK not renamed (CHARMANDER is offered a rename)
#  poison   - poison outside battle can't kill BLACK; a poisoned CHARMANDER still loses HP
from harness import *
import sys,io,json
from collections import deque
MODE=sys.argv[1]
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:sys.exit(1)
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
seen=[]
def T(n):
    for _ in range(n):
        p.tick();b=clean(' '.join(txt()))
        if b and (not seen or seen[-1]!=b):seen.append(b)
def press_(k,n=60):p.button(k,8);T(n)
def allt():return ' '.join(seen)
def party():return list(m[0xd164:0xd164+m[0xd163]])
ROM=open(os.environ['CB_ROM'],'rb').read()
def fo(b,a):return b*0x4000+a-0x4000
L=json.load(open('manifest_v38.json'))['labels']['bank2d']
SB=fo(0x2d,int(L['s_black'],16));SP=fo(0x2d,int(L['s_preta'],16))
BLK,PRETA,AZHI,GHOST,CHAR=0x7f,0xb6,0xb7,0x1f,0xb0
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
    assert (y,x) in prev,('no path',(y,x))
    path=[];c=(y,x)
    while prev[c]:c,d=prev[c];path.append(d)
    rest(st[start])
    for d in reversed(path):p.button(d,8);T(24)
    T(10)
def lead(species):
    i=list(m[0xd164:0xd16a]).index(species)
    if i:
        for base,size in ((0xd16b,44),(0xd2b5,11),(0xd273,11)):
            a=list(m[base:base+size]);b=list(m[base+size*i:base+size*(i+1)])
            m[base:base+size]=b;m[base+size*i:base+size*(i+1)]=a
        m[0xd164],m[0xd164+i]=m[0xd164+i],m[0xd164]
def make_black():
    """pallet_with_ghost as BLACK: the ROM's own BLACK struct in slot 1 (where GHOST was), CHARMANDER in slot 2"""
    m[0xd46c]=1;m[0xd467]=6;lead(GHOST)
    m[0xd164]=BLK;m[0xd16b:0xd16b+44]=list(ROM[SB:SB+44]);m[0xd16b+12]=m[0xd359];m[0xd16b+13]=m[0xd35a]
    m[0xd2b5:0xd2b5+11]=[0x81,0x8b,0x80,0x82,0x8a]+[0x50]*6
def warp(mapid,warpid=0,setup=None):
    load('pallet_with_ghost');m[0xd455]=255
    if setup:setup()
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=warpid;m[0xd3af+4*i+3]=mapid
    for i in range(6):
        if m[0xd35e]==mapid:break
        p.button('up',8);T(24)
    T(120);m[0xd887]=0;print('arrived',hex(mapid),pos(),flush=True)
def cursor_line():
    l=[x for x in txt() if '▶' in x or '▲' in x];return l[0] if l else ''
def pick(name,n=10):
    for k in range(n):
        if name in cursor_line():return True
        press_('down',20)
    return name in cursor_line()
def to_menu():
    for k in range(10):
        if 'Choose a' in ' '.join(txt()):return True
        press_('a',60)
    return False
def yes():
    """BLACK: the person panics and offers CURSE (v40+: BANE) first -> NO (usual dialogue); then YES to the real question"""
    cursed=False
    for k in range(30):
        t=' '.join(txt())
        if 'YES' in t and ('CURSE' in allt() or 'BANE them' in allt() or 'METAMORPHOSIS?' in allt()) and not cursed:cursed=True;press_('down',20);press_('a',90);continue
        if 'YES' in t:press_('a',90);return True
        press_('a',60)
    return False
def hp(i):b=0xd16b+44*i;return m[b+1]<<8|m[b+2]
def exp(i):b=0xd16b+44*i;return m[b+14]<<16|m[b+15]<<8|m[b+16]

def climax(state_name,setup=None):
    load(state_name);T(30)
    if setup:setup()
    for k in range(80):
        if m[0xd057]:break
        if box() or m[0xcd6b]:press_('a',45);continue
        p.button('down',8);T(40)
    shots=[]
    for k in range(9000):
        p.tick()
        if k%50==25:p.button('a',8)
        if k%20==0 and m[0xd057] and m[0xff47]!=0xff:shots.append(bytes(m[a] for a in range(0x9000,0x9310)))
        if m[0xd057]==0 and k>600:break
    T(600)
    for k in range(10):press_('a',60)
    return shots

if MODE in ('join','owned'):
    ritual='v25_after_ritual_v25a'
    if MODE=='join':
        shots=climax(ritual)
        # the evolution frames: RED's front picture tiles (bank 4) appear in VRAM before BLACK's
        sys.path.insert(0,'../ref');import pic
        red=bytes(pic.decompress(io.BytesIO(ROM[fo(4,0x6f2a):fo(4,0x6f2a)+1000])))[:16*8]
        red_seen=any(s.find(red[16:48])>=0 for s in shots)
        print('frames',len(shots),'RED tiles seen',red_seen)
        ok(red_seen,'evolution scene shows RED\'s trainer picture (species 86) before the BLACK TAMER')
    else:
        def s():
            n=m[0xd163];m[0xd164+n]=PRETA;m[0xd164+n+1]=0xff;m[0xd163]=n+1
            m[0xd16b+44*n:0xd16b+44*n+44]=list(ROM[SP:SP+44])
        climax(ritual,s)
    pt=party();print('party',[hex(x) for x in pt],'BLACK',m[0xd46c],'RIT',m[0xd467])
    b=0xd16b;st=[m[b+34+2*j]<<8|m[b+35+2*j] for j in range(5)]
    print('BLACK lv',m[b+33],'stats',st,'DVs',hex(m[b+27]),hex(m[b+28]),'OT',hex(m[b+12]),hex(m[b+13]),'nick',''.join(cm.get(v,'') for v in m[0xd2b5:0xd2ba]))
    ok(m[0xd46c]==1 and pt[0]==BLK and m[b+33]==1 and st==[43,30,28,30,40] and m[b+27]==m[b+28]==0xff
       and (m[b+12],m[b+13])==(m[0xd359],m[0xd35a]),'BLACK is party slot 1: Lv1, perfect DVs, stats of a Lv10, the player\'s OT')
    ok(pt.count(PRETA)==1 and pt.count(AZHI)==1 and GHOST not in pt,
       'PRETA and AZHI in the party once'+(' (PRETA already owned: not given twice)' if MODE=='owned' else ''))
elif MODE=='card':
    def card(black):
        warp(0x29,0,make_black if black else None);T(30)
        p.button('start',8);T(40)
        name=''.join(cm.get(v,'') for v in m[0xd158:0xd15b])
        pick(name);press_('a',120)
        im=p.screen.image.convert('L').crop((112,8,160,64))
        dark=sum(1 for v in im.getdata() if v<60)/(48*56);shot('v38_card_%s'%('black' if black else 'red'))
        return dark
    d0=card(False);d1=card(True);print('trainer card picture dark ratio: RED',round(d0,2),'BLACK',round(d1,2))
    ok(d1>d0+0.12,'trainer card shows the BLACK TAMER picture when BLACK, RED\'s otherwise')
elif MODE in ('faint','exp'):
    def battle(black,species,lv=30):
        load('pallet_with_ghost');m[0xd455]=255
        if black:make_black()
        else:lead(CHAR)
        b=0xd16b
        if MODE=='faint':m[b+1]=0;m[b+2]=1;m[b+8]=0x2d;m[b+29]=0x3f                 # 1 HP, GROWL
        else:m[b+8]=0x0a;m[b+29]=0x3f                                            # SCRATCH
        m[0xd059]=species;m[0xd127]=lv
        for i in range(300):
            if m[0xd057]:break
            p.tick()
        seen.clear();turns=0
        for i in range(500):
            if MODE=='exp' and m[0xd057]:m[0xcfe6]=0;m[0xcfe7]=1
            if m[0xd057]==0:break
            t=clean(' '.join(txt()))
            if 'FIGHT' in t and 'RUN' in t:
                if turns>=2:
                    for k in range(3):press_('down',15);press_('right',15)
                    press_('a',150);continue
                turns+=1
                for k in range(4):
                    if '▶FIGHT' in t.replace(' ',''):break
                    press_('up',20);press_('left',20);t=clean(' '.join(txt()))
                press_('a',60);press_('a',200);continue
            if 'fainted' in t and MODE=='faint':break
            press_('a',60)
        return allt()
    if MODE=='faint':
        t=battle(True,0xa5)
        print('BLACK:',t[-200:])
        ok('BLACK fainted' not in t and (m[0xd015]<<8|m[0xd016])==1 or (not m[0xd057] and hp(0)==1),'BLACK at 1 HP takes hits and stays at 1 HP')
        ok(hp(0)>=1 and 'fainted' not in t,'no "fainted" for BLACK')
        t=battle(False,0xa5)
        print('CHARMANDER:',t[-160:])
        ok('fainted' in t,'CHARMANDER at 1 HP faints as before (normal case)')
    else:
        load('pallet_with_ghost');make_black();e0=exp(0)
        battle(True,0xa5,5);e1=exp(0);print('BLACK exp',e0,'->',e1,'lv',m[0xd16b+33])
        ok(e1==e0 and m[0xd16b+33]==1,'BLACK gains no experience in battle')
        load('pallet_with_ghost');lead(CHAR);c0=exp(0)
        battle(False,0xa5,5);c1=exp(0);print('CHARMANDER exp',c0,'->',c1)
        ok(c1>c0,'CHARMANDER gains experience as before (normal case)')
elif MODE=='items':
    POTION=0x14
    def use_potion(slot):
        load('pallet_with_ghost');make_black()
        m[0xd31d]=1;m[0xd31e]=POTION;m[0xd31f]=3;m[0xd320]=0xff
        for i in range(m[0xd163]):b=0xd16b+44*i;m[b+1]=0;m[b+2]=5
        T(30);p.button('start',8);T(40);pick('ITEM');press_('a',60)
        seen.clear();press_('a',50);press_('a',60)                    # POTION, USE
        for k in range(slot):press_('down',20)
        press_('a',90)
        for k in range(6):press_('a',60)
        return allt(),m[0xd31f] if m[0xd31d] else 0
    t,left=use_potion(0);print('BLACK:',t[-120:],'potions',left,'HP',hp(0))
    ok('effect' in t and left==3 and hp(0)==5,'POTION on BLACK: "It won\'t have any effect.", nothing used, HP unchanged')
    t,left=use_potion(1);print('CHARMANDER:',t[-120:],'potions',left,'HP',hp(1))
    ok(left==2 and hp(1)>5,'POTION on CHARMANDER heals as before (normal case)')
elif MODE=='pc':
    def deposit(slot):
        warp(0x29,0,make_black);bfs_to(4,13);p.button('up',8);T(30)
        seen.clear();press_('a',90)
        for k in range(10):
            if 'PC' in cursor_line() or 'LOG' in ' '.join(txt()):break
            press_('a',60)
        press_('a',120)                                              # first entry: the POKeMON storage
        for k in range(8):
            if 'DEPOSIT' in ' '.join(txt()):break
            press_('a',60)
        pick('DEPOSIT');press_('a',90)
        for k in range(slot):press_('down',20)
        press_('a',60);pick('DEPOSIT');press_('a',150)
        for k in range(6):press_('a',60)
        return allt()
    n0=2;t=deposit(0);pt=party();print('BLACK:',t[-150:],'party',[hex(x) for x in pt],'box',m[0xda80])
    ok('stored' in t and BLK in pt and len(pt)==n0,'PC: BLACK can\'t be deposited ("BLACK can\'t be stored away.")')
    t=deposit(1);pt=party();print('CHARMANDER:',t[-150:],'party',[hex(x) for x in pt],'box',m[0xda80])
    ok(CHAR not in pt and m[0xda80]>=1,'PC: CHARMANDER is deposited as before (normal case)')
elif MODE=='daycare':
    def black2():make_black();lead(CHAR)                        # CHARMANDER first, BLACK second (slot 1 can't be picked here)
    def daycare(slot):
        warp(0x48,0,black2);bfs_to(4,2);p.button('up',8);T(30);seen.clear();press_('a',90)
        yes();to_menu()
        for k in range(slot):press_('down',20)
        press_('a',120)
        for k in range(8):press_('a',60)
        return allt()
    def daycare_char():
        warp(0x48,0,make_black);bfs_to(4,2);p.button('up',8);T(30);seen.clear();press_('a',90)
        yes();to_menu();press_('down',20);press_('a',120)
        for k in range(8):press_('a',60)
        return allt()
    t=daycare(1);print('DAYCARE BLACK:',t[-150:]);ok('your side' in t and BLK in party(),'Day Care: BLACK won\'t be left there')
    t=daycare(0) if False else daycare_char();print('DAYCARE CHARMANDER:',t[-200:]);ok(CHAR not in party() or 'raise' in t.lower(),'Day Care: CHARMANDER is accepted as before (normal case)')
    def rater(slot):
        warp(0xe5,0,black2);bfs_to(4,5);p.button('up',8);T(30);seen.clear();press_('a',90)
        yes();to_menu()
        for k in range(slot):press_('down',20)
        press_('a',120)
        for k in range(8):
            if 'YES' in ' '.join(txt()):break
            press_('a',60)
        return allt()
    t=rater(1);print('RATER BLACK:',t[-200:])
    ok('impeccable' in t and 'like me to give' not in t,'Name Rater: BLACK isn\'t offered a new name ("truly impeccable name")')
    for k in range(6):press_('b',30)
    t=rater(0);print('RATER CHARMANDER:',t[-200:])
    ok('like me to give' in t or 'decent' in t,'Name Rater: CHARMANDER is offered a new name as before (normal case)')
elif MODE=='poison':
    import random;random.seed(3)
    def walk_poisoned(black):
        load('pallet_with_ghost')
        if black:make_black()
        else:lead(CHAR);m[0xd46c]=1                                  # BLACK flag on (hunger off) for both runs
        b=0xd16b;m[b+1]=0;m[b+2]=6;m[b+4]=0x08                        # 6 HP, poisoned
        steps=0
        for i in range(60):
            if box():press_('a',40);continue
            y=m[0xd361];p.button('down' if i%2 else 'up',8);T(24);steps+=m[0xd361]!=y
        for k in range(6):press_('a',40)
        return hp(0),m[b+4],allt(),steps
    h,st,t,n=walk_poisoned(True);print('BLACK: steps',n,'HP',h,'status',hex(st))
    ok(n>=20 and 1<=h<=4 and st==0 and 'fainted' not in t,'poison outside battle can\'t kill BLACK (HP 6 -> %d, poison cleared)'%h)
    h,st,t,n=walk_poisoned(False);print('CHARMANDER: steps',n,'HP',h,'status',hex(st))
    ok(n>=20 and h<6,'a poisoned CHARMANDER still loses HP outside battle (normal case)')
