# v14 checks. Modes:
#  mirage_rate - Route 1 grass with the capped Mirage chance (64/256): wild battles happen again, Mirage is a share
#  you         - Mirage battle with YOU leading: no Poke Ball poof, picture drawn; a normal Pokemon still gets the poof
#  dex         - Mirage PRETA/AZHI don't mark Kabutops/Aerodactyl seen; a wild Pokemon still gets marked
#  gambler     - Viridian Pokemon Center gentleman now uses the GAMBLER sprite, Mr. Mu in Pallet keeps GENTLEMAN
#  rumour      - Pallet girl / Cerulean boy: killer rumour after a murder (D453), original line without
#  misty_kill  - Cerulean Gym: CURSE kills MISTY (murder, badge + TM from the body, gravestone), the trainers stay
#                active and swear revenge
#  misty_win   - same gym, normal win: TM text, trainers deactivated, no murder, MISTY not a gravestone
#  brock_kill  - Pewter Gym (base-game kill): the trainer now stays active and swears revenge
from harness import *
import sys,random
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
def warp_from_pallet(mapid,warpid,state='pallet_with_ghost'):
    load(state);lead(0x1f);m[0xd16b+29]=0x3f;m[0xd455]=255
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=warpid;m[0xd3af+4*i+3]=mapid
    for i in range(6):
        if m[0xd35e]==mapid:break
        walk('up',1)
    T(120);print('arrived',pos(),flush=True)
def walk_to(y,x,limit=40):
    for i in range(limit):
        if m[0xd057] or (m[0xd361]==y and m[0xd362]==x):return
        cy,cx=m[0xd361],m[0xd362]
        dirs=(['up'] if cy>y else ['down'] if cy<y else [])+(['left'] if cx>x else ['right'] if cx<x else [])
        if i%2:dirs.reverse()
        for d in dirs:
            p.button(d,8);T(24)
            if (m[0xd361],m[0xd362])!=(cy,cx) or m[0xd057]:break
import io
def bfs_to(y,x,maxn=400):
    """walk to (y,x) on the current map along a path found by trying each step in the emulator"""
    from collections import deque
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
    assert (y,x) in prev,('no path',(y,x),sorted(prev))
    path=[];c=(y,x)
    while prev[c]:c,d=prev[c];path.append(d)
    rest(st[start])
    for d in reversed(path):p.button(d,8);T(24)
    T(10);return path[::-1]
def to_route1():                                               # Pallet start (10,12) -> Route 1 grass
    for d,n in (('left',4),('up',11),('right',2),('up',4)):
        for i in range(n):walk(d,1)
def fight(limit=400,hp1=False,spare=False):
    for i in range(limit):
        if m[0xd057]==0:return
        if hp1 and m[0xcfe6]|m[0xcfe7]:m[0xcfe6]=0;m[0xcfe7]=1      # enemy at 1 HP: any hit wins
        b=clean(box())
        if spare and m[0xd05a]==3 and 'FIGHT' in b and 'RUN' in b:   # trainer phase: leave with RUN
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
    print(tag);[print('  TEXT:',s) for s in seen if s.endswith(('!','▼','?','.'))]

if MODE=='mirage_rate':
    wild=mir=0;rounds=0
    while wild+mir<24 and rounds<40:
        rounds+=1;load('pallet_with_ghost');m[0xd455]=255;m[0xd45c]=200;random.seed(rounds)
        to_route1();assert m[0xd35e]==0xc,pos()
        for step in range(2500):
            if wild+mir>=24:break
            if m[0xd057]:
                p.tick(30)
                if m[0xd45d]:mir+=1;print('  encounter',wild+mir,'MIRAGE',flush=True);break   # next round from the save
                wild+=1;print('  encounter',wild+mir,'wild species',hex(m[0xcfd8]),flush=True)
                for i in range(40):
                    if m[0xd057]==0:break
                    b=box()
                    if 'FIGHT' in b and 'RUN' in b:p.button('down',8);p.tick(10);p.button('right',8);p.tick(10);p.button('a',8);p.tick(150)
                    else:p.button('a',8);p.tick(150)
                m[0xd455]=255;continue
            walk(random.choice(['up','down','left','right']),1)
    print('RESULT wild',wild,'mirage',mir)
    assert wild>=8 and 1<=mir<=14,(wild,mir)
    print('PASS Mirage is a share of the encounters again (wild %d, Mirage %d of %d; chance 64/256)'%(wild,mir,wild+mir))

elif MODE in ('you','dex'):
    hits=[]
    def poof(ctx):
        if p.register_file.A==0xc4:hits.append(m[0xd014])
    p.hook_register(0xf,0x6fed,poof,None)
    load('mirage_battle_start')
    party=list(m[0xd164:0xd16b]);print('party',[hex(x) for x in party],'enemy',hex(m[0xcfd8]))
    if MODE=='you':
        assert 0x79 in party;lead(0x79)
    m[0xd31b]&=~0x30;m[0xd308]&=~0x30                      # Kabutops (141) / Aerodactyl (142) not seen / owned
    for i in range(60):
        T(30)
        if 'FIGHT' in clean(box()):break
        press_('a',30)
    print('battle mon',hex(m[0xd014]),'enemy',hex(m[0xcfd8]),'poof calls',[hex(x) for x in hits])
    if MODE=='you':
        shot('v14_you_sent_out')
        tiles=[m[0xc3a0+y*20+x] for y in range(7,12) for x in range(1,8)]
        assert m[0xd014]==0x79 and not hits and len(set(tiles))>3,(hits,set(tiles))
        print('PASS YOU comes out without the Poke Ball poof, picture drawn')
        # normal case: switch to another Pokemon -> poof
        load('mirage_battle_start');party=list(m[0xd164:0xd16b]);other=next(x for x in party if x not in (0x79,0xff));lead(other)
        hits.clear()
        for i in range(60):
            T(30)
            if 'FIGHT' in clean(box()):break
            press_('a',30)
        print('battle mon',hex(m[0xd014]),'poof calls',[hex(x) for x in hits])
        assert hits==[other]
        print('PASS a normal Pokemon still comes out with the poof')
    else:
        assert m[0xcfd8] in (0xb6,0xb7)
        print('dex seen byte',hex(m[0xd31b]),'owned',hex(m[0xd308]))
        assert not m[0xd31b]&0x30 and not m[0xd308]&0x30
        print('PASS PRETA/AZHI encounter does not reveal Kabutops/Aerodactyl')
        # normal case: wild Pokemon on Route 1 gets marked seen
        load('pallet_with_ghost');m[0xd455]=255;m[0xd45c]=0;m[0xd30a:0xd31d]=[0]*0x13;random.seed(3)
        to_route1();assert m[0xd35e]==0xc,pos()
        for step in range(3000):
            if m[0xd057]:break
            walk(random.choice(['up','down','left','right']),1)
        T(300);sp=m[0xcfd8]
        seenbits=sum(bin(x).count('1') for x in m[0xd30a:0xd31d])
        print('wild',hex(sp),'seen bits set',seenbits)
        assert seenbits==1
        print('PASS a wild Pokemon is still marked seen')

elif MODE=='gambler':
    def visit(mapid,warpid=0):
        load('pallet_with_ghost')
        for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=warpid;m[0xd3af+4*i+3]=mapid
        for i in range(6):
            if m[0xd35e]==mapid:break
            walk('up',1)
        T(120);return [m[0xc100+0x10*i] for i in range(1,m[0xd4e1]+1)]
    pics=visit(0x3f);shot('v14_mu_trade_house')
    print('trade house sprites',[hex(x) for x in pics]);assert 0x10 in pics
    pics=visit(0x29);shot('v14_gambler_center')                    # Viridian Pokemon Center
    print('Viridian center sprites',[hex(x) for x in pics]);assert 0x0b in pics and 0x10 not in pics
    print('PASS gentleman NPCs use the GAMBLER sprite; Mr. Mu keeps GENTLEMAN')

elif MODE=='rumour':
    for murder in (1,0):
        load('pallet_with_ghost');m[0xd453]=murder;seen.clear()
        i=next(i for i in range(1,16) if m[0xc100+0x10*i]==0x0d)   # GIRL sprite
        m[0xc206+0x10*i]=0xff;T(60)                                # she stops wandering (at x3,y8)
        for d,n in (('left',4),('up',4),('left',4)):
            for k in range(n):walk(d,1)
        for k in range(6):press_('a',100)
        t=allt();print('murder',murder,pos(),'->',t[-160:])
        if murder:assert 'killing' in t and 'ROCKET' in t and 'raising' not in t
        else:assert 'raising' in t and 'killing' not in t
    print('PASS Pallet girl: killer rumour after a murder, original line otherwise')

elif MODE in ('misty_kill','misty_win'):
    warp_from_pallet(0x41,0);m[0xd887]=0
    m[0xd75e]|=0x0c                                            # both trainers count as beaten while we walk up
    if MODE=='misty_win':m[0xd16b+8:0xd16b+12]=[0x21,0,0,0];m[0xd16b+29]=0x3f   # GHOST knows only TACKLE
    print('path',bfs_to(3,4));p.button('up',8);T(20);seen.clear();print('at',pos(),flush=True)
    for i in range(30):
        if m[0xd057]:break
        press_('a',60)
    shot('v14_misty_talk');show('talk')
    m[0xd75e]&=~0x0c                                           # ... but not any more: victory decides
    print('battle',m[0xd057],'class',m[0xd031],'D4AE/AF',m[0xd4ae],m[0xd4af],flush=True)
    assert m[0xd057]==2 and m[0xd031]==35 and m[0xd4af]==26
    if MODE=='misty_kill':
        fight()
    else:
        fight(hp1=True,spare=True)
    for i in range(30):press_('a',90)
    show(MODE)
    bag=list(m[0xd31e:0xd31e+2*m[0xd31d]])
    print('murder',m[0xd453],'graves',[hex(x) for x in m[0xd4a4:0xd4ae]],'badges',bin(m[0xd356]),'events d75e',bin(m[0xd75e]),
          'TM11 in bag',0xd3 in bag[::2],'sprite1',hex(m[0xc110]),pos())
    if MODE=='misty_kill':
        assert m[0xd453]==1 and m[0xd4a7]&0x04 and m[0xd356]&2 and m[0xd75e]&0x80 and not m[0xd75e]&0x0c
        assert 'took the' in allt() and 'CASCADEBADGE' in allt() and 0xd3 in bag[::2]
        print('PASS MISTY killed: murder flag, kill bit, badge + TM11 from the body, trainers still active')
        # the trainer at (2,3) faces right: she spots us as soon as MISTY's battle is over
        assert 'MISTY is dead!' in allt() and 'avenge' in allt()
        print('PASS remaining gym trainer swears revenge and still battles')
        fight()
        for i in range(10):press_('a',90)
        save('misty_killed')
        # enter again (any later visit: the kill bit is saved): MISTY is a gravestone
        graves=list(m[0xd4a4:0xd4ae]);load('pallet_with_ghost');m[0xd4a4:0xd4ae]=graves
        for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x41
        for i in range(6):
            if m[0xd35e]==0x41:break
            walk('up',1)
        T(120)
        print('re-entered',pos(),'sprite1',hex(m[0xc110]),'list',[hex(x) for x in m[0xd486:0xd492]]);shot('v14_misty_grave')
        assert m[0xd35e]==0x41 and m[0xc110]==0x49
        print('PASS MISTY is a gravestone after re-entering')
    else:
        assert m[0xd453]==0 and not m[0xd4a7]&0x04 and m[0xd356]&2 and m[0xd75e]&0x8c==0x8c and 0xd3 in bag[::2]
        assert 'took the' not in allt() and 'dead' not in allt()
        print('PASS normal win: no murder, badge + TM11 with the normal text, trainers deactivated')

elif MODE=='brock_kill':
    warp_from_pallet(0x36,0);m[0xd887]=0
    m[0xd755]|=0x04
    walk_to(2,4);p.button('up',8);T(20);seen.clear()
    for i in range(30):
        if m[0xd057]:break
        press_('a',60)
    m[0xd755]&=~0x04
    print('battle',m[0xd057],'class',m[0xd031],'D4AE/AF',m[0xd4ae],m[0xd4af],flush=True)
    assert m[0xd031]==34
    fight()
    for i in range(30):press_('a',90)
    show('BROCK')
    print('murder',m[0xd453],'graves',[hex(x) for x in m[0xd4a4:0xd4ae]],'badges',bin(m[0xd356]),'d755',bin(m[0xd755]))
    assert m[0xd453]==1 and m[0xd4a5]&0x10 and m[0xd356]&1 and m[0xd755]&0x80 and not m[0xd755]&0x04
    print('PASS BROCK killed (base game): badge, trainer stays active')
    seen.clear()
    for y in (3,4,5,6,7):
        walk_to(y,4)
        if m[0xd057] or 'dead' in allt():break
    for i in range(10):
        if 'dead' in allt() or m[0xd057]:break
        press_('a',60)
    T(200);show('REVENGE')
    assert 'BROCK is dead!' in allt()
    print('PASS Pewter trainer swears revenge')

elif MODE=='koga_kill':                                        # bank 1D code (shared with BLAINE / GIOVANNI)
    warp_from_pallet(0x9d,0);m[0xd887]=0
    m[0xd792]|=0xfc                                            # the six trainers count as beaten while we walk
    print('path',bfs_to(11,4,maxn=600));p.button('up',8);T(20);seen.clear()
    for i in range(30):
        if m[0xd057]:break
        press_('a',60)
    m[0xd792]&=~0xfc
    print('battle',m[0xd057],'class',m[0xd031],'D4AE/AF',m[0xd4ae],m[0xd4af],flush=True)
    assert m[0xd057]==2 and m[0xd031]==38 and m[0xd4af]==29
    fight()
    for i in range(12):press_('a',90)
    show(MODE);bag=list(m[0xd31e:0xd31e+2*m[0xd31d]])
    print('murder',m[0xd453],'graves',[hex(x) for x in m[0xd4a4:0xd4ae]],'badges',bin(m[0xd356]),'d792',bin(m[0xd792]),'TM06',0xce in bag[::2])
    assert m[0xd453]==1 and m[0xd4a7]&0x20 and m[0xd356]&0x10 and m[0xd792]&0x02 and not m[0xd792]&0xfc and 0xce in bag[::2]
    assert 'took the' in allt() and 'SOULBADGE' in allt()
    print('PASS KOGA killed: murder, kill bit, SOULBADGE + TM06 from the body, trainers still active')
