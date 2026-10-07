# v10/v11: ????? trainer name, AZHI (moves, name, immunities), BLACK FLAME party faint, DRAGON RAGE,
#      real Kabutops / Aerodactyl keep their original sprites.
from harness import *
import random,sys
MODE=sys.argv[1] if len(sys.argv)>1 else 'bf'
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
def hp(i):return m[0xd16c+44*i]<<8|m[0xd16d+44*i]
def run_turn(move_index,seen,limit=1500):
    def T(n):                                                   # tick n frames, recording every text box
        for _ in range(n):
            p.tick();b=clean(box())
            if b and (not seen or seen[-1]!=b):seen.append(b)
    def press_(k,n):p.button(k,8);T(n)
    for i in range(30):
        if 'FIGHT' in box():break
        press_('a',120)
    T(60)
    for k in range(4):
        if '▲FIGHT' in box():break
        press_('up',20);press_('left',20)
    for k in range(5):
        press_('a',60)
        if 'TYPE' in ' '.join(txt()):break
    for k in range(4):                                          # the move cursor remembers the last move used
        if m[0xcc26]==0:break
        press_('up',20)
    for k in range(move_index):press_('down',20)
    p.button('a',8)
    for i in range(limit):
        T(1)
        if i%60==30 and box() and 'FIGHT' not in box() and 'Bring out' not in box():p.button('a',8)
        if m[0xd057]==0 or ('FIGHT' in box() and i>300) or 'Bring out' in box():break
def find_mirage(want):
    for seed in range(40,90):
        random.seed(seed);load('v6_after_macabre');m[0xd45c]=200;found=False
        for step in range(3000):
            if m[0xd057]:
                p.tick(30)
                if m[0xd45d]:found=True;break
                for i in range(40):
                    if m[0xd057]==0:break
                    if 'FIGHT' in box():p.button('down',8);p.tick(10);p.button('right',8);p.tick(10);p.button('a',8);p.tick(150)
                    else:p.button('a',8);p.tick(150)
                continue
            m[0xd455]=255;walk(random.choice(['up','down','left','right']),1)
        assert found;intro=[]
        for i in range(40):
            b=clean(box())
            if b and (not intro or intro[-1]!=b):intro.append(b)
            if 'FIGHT' in box() and m[0xd014]==0xb6:break
            p.button('a',8);p.tick(160)
        print('seed',seed,'enemy',hex(m[0xcfe5]),flush=True)
        if m[0xcfe5]==want:return intro
if MODE in ('bf','fireblast','dragonrage'):
    intro=find_mirage(0xb7);print('INTRO:',intro)
    print('enemy moves',[hex(x) for x in m[0xcfed:0xcff1]],'party',list(m[0xd164:0xd16b]),'HP',[hp(i) for i in range(m[0xd163])])
    assert list(m[0xcfed:0xcff1])==[0xa8,0x13,0x52,0x7e]
    assert any('????? wants to fight' in x or '?????' in x for x in intro) and any('sent out AZHI' in x for x in intro) and not any('TAMER' in x for x in intro)
    force={'bf':0xa8,'fireblast':0x7e,'dragonrage':0x52}[MODE];m[0xcfed]=m[0xcfee]=m[0xcfef]=m[0xcff0]=force
    seen=[];h0=[hp(i) for i in range(m[0xd163])];ehp=m[0xcfe6]<<8|m[0xcfe7]
    nm={'bf':'BLACK FLAME','fireblast':'FIRE BLAST','dragonrage':'DRAGON RAGE'}[MODE]
    for t in range(4):                                          # PRETA: MACABRE until AZHI's move lands
        hb=[hp(i) for i in range(m[0xd163])];run_turn(0,seen)
        if any('used '+nm in x for x in seen) and not any('missed' in x for x in seen[-6:]):break
    for s in seen:
        if s.endswith('!') or s.endswith('▼'):print('  TEXT:',s)
    h1=[hp(i) for i in range(m[0xd163])];print('party',list(m[0xd164:0xd16b]),'HP',h0,'->',h1,'enemy HP',ehp,'->',m[0xcfe6]<<8|m[0xcfe7])
    allt=' '.join(seen)
    assert (m[0xcfe6]<<8|m[0xcfe7])==ehp
    if MODE!='bf':assert 'affect Enemy AZHI' in allt
    if MODE=='bf':
        assert 'Enemy AZHI used BLACK FLAME' in allt and 'affect PRETA' in allt and h1[0]==h0[0] and h1[1]==0 and h1[2]==h0[2],'BLACK FLAME v11'
        print('PASS ????? / AZHI names; BLACK FLAME: PRETA spared, CHARMANDER fainted, stand-in untouched')
        m[0xd015]=0;m[0xd016]=0;seen2=[]                          # PRETA drops: only the stand-in is left
        for i in range(40):
            b=clean(box())
            if b and (not seen2 or seen2[-1]!=b):seen2.append(b)
            if 'Bring out' in b or 'Choose' in b:
                for k in range(2):p.button('down',8);p.tick(20)
                p.button('a',8);p.tick(120);continue
            if 'FIGHT' in box() and m[0xd014]==0x79:break
            p.button('a',8);p.tick(120)
        print('stand-in out:',hex(m[0xd014]))
        assert m[0xd014]==0x79
        run_turn(0,seen2);allt2=' '.join(seen2)
        print([x for x in seen2 if x.endswith('!') or x.endswith('▼')][-6:])
        assert 'Enemy AZHI used BLACK FLAME' in allt2 and 'affect RED' in allt2 and m[0xd057] and m[0xd014]==0x79 and m[0xd45d]==1   # still in the same battle: no death/reset
        print('PASS BLACK FLAME on the player: "doesn\'t affect", no death, battle goes on')
    else:
        assert 'Enemy AZHI used %s'%nm in allt and 0<h1[0]<hb[0] and h1[1]==h0[1],(hb,h1)
        print('PASS AZHI %s does normal damage (PRETA %d -> %d), MACABRE no effect on AZHI'%(nm,hb[0],h1[0]))
elif MODE=='wild':                                              # wild AZHI: CURSE and MACABRE don't affect it
    load('v6_after_macabre')
    def swap(i,j):
        for base,size in ((0xd16b,44),(0xd2b5,11),(0xd273,11)):
            a=list(m[base+size*i:base+size*(i+1)]);b=list(m[base+size*j:base+size*(j+1)])
            m[base+size*i:base+size*(i+1)]=b;m[base+size*j:base+size*(j+1)]=a
        m[0xd164+i],m[0xd164+j]=m[0xd164+j],m[0xd164+i]
    swap(0,1);print('party',list(m[0xd164:0xd168]),'lead moves',[hex(x) for x in m[0xd16b+8:0xd16b+12]])
    for k in range(10):m[0xd888+2*k]=2;m[0xd889+2*k]=0xb7
    random.seed(9)
    for i in range(800):
        if m[0xd057]:break
        walk(random.choice(['up','down','left','right']),1);m[0xd455]=255
        for k in range(10):m[0xd888+2*k]=2;m[0xd889+2*k]=0xb7
    assert m[0xd057]==1;p.tick(60);print('wild',hex(m[0xcfe5]),'lv',m[0xcff3])
    for i in range(30):
        if 'FIGHT' in box():break
        p.button('a',8);p.tick(120)
    m[0xcfed]=m[0xcfee]=m[0xcfef]=m[0xcff0]=0x13;seen=[];ehp=m[0xcfe6]<<8|m[0xcfe7]
    run_turn(0,seen)                                            # GHOST: CURSE (first move)
    allt=' '.join(seen);print(seen);print('enemy HP',ehp,'->',m[0xcfe6]<<8|m[0xcfe7],'in battle',m[0xd057])
    assert 'affect Enemy AZH' in allt and m[0xd057] and (m[0xcfe6]<<8|m[0xcfe7])==ehp
    print('PASS CURSE does not affect AZHI')
elif MODE=='wild_bf':                                           # wild AZHI's BLACK FLAME: GHOST and PRETA spared
    load('v6_after_macabre')
    def swap(i,j):
        for base,size in ((0xd16b,44),(0xd2b5,11),(0xd273,11)):
            a=list(m[base+size*i:base+size*(i+1)]);b=list(m[base+size*j:base+size*(j+1)])
            m[base+size*i:base+size*(i+1)]=b;m[base+size*j:base+size*(j+1)]=a
        m[0xd164+i],m[0xd164+j]=m[0xd164+j],m[0xd164+i]
    swap(0,2);print('party',list(m[0xd164:0xd168]))                 # CHARMANDER, GHOST, PRETA
    random.seed(9)
    for i in range(800):
        if m[0xd057]:break
        for k in range(10):m[0xd888+2*k]=30;m[0xd889+2*k]=0xb7
        walk(random.choice(['up','down','left','right']),1);m[0xd455]=255
    assert m[0xd057]==1
    for i in range(30):
        if 'FIGHT' in box():break
        p.button('a',8);p.tick(120)
    m[0xcfed]=m[0xcfee]=m[0xcfef]=m[0xcff0]=0xa8;h0=[hp(i) for i in range(3)];seen=[]
    run_turn(0,seen);h1=[hp(i) for i in range(3)]
    print('HP',h0,'->',h1,[x for x in seen if x.endswith('!')][:6])
    assert 'Enemy AZHI used BLACK FLAME' in ' '.join(seen) and h1[0]==0 and h1[1]==h0[1] and h1[2]==h0[2] and m[0xd453]==0
    print('PASS wild AZHI BLACK FLAME: CHARMANDER fainted, GHOST and PRETA spared')
elif MODE=='player_bf':                                         # a player AZHI's BLACK FLAME vs a wild Pidgey
    load('v6_after_macabre');s=0xd16b+44*2
    m[s]=0xb7;m[0xd166]=0xb7;m[s+8:s+12]=[0xa8,0x13,0xaa,0x7e];m[s+29:s+33]=[10,15,20,5];m[s+5]=8;m[s+6]=2;m[s+33]=50;m[s+3]=50
    for k,v in enumerate([0,180,0,150,0,100,0,200,0,100]):m[s+34+k]=v
    m[s+1]=0;m[s+2]=180
    def swap(i,j):
        for base,size in ((0xd16b,44),(0xd2b5,11),(0xd273,11)):
            a=list(m[base+size*i:base+size*(i+1)]);b=list(m[base+size*j:base+size*(j+1)])
            m[base+size*i:base+size*(i+1)]=b;m[base+size*j:base+size*(j+1)]=a
        m[0xd164+i],m[0xd164+j]=m[0xd164+j],m[0xd164+i]
    swap(0,2);random.seed(5)
    for i in range(800):
        if m[0xd057]:break
        walk(random.choice(['up','down','left','right']),1);m[0xd455]=255
    assert m[0xd057]==1;p.tick(60)
    seen=[];anims=set()
    for i in range(30):
        if 'FIGHT' in box():break
        p.button('a',8);p.tick(120)
    print('lead',hex(m[0xd014]),'moves',[hex(x) for x in m[0xd01c:0xd020]],'enemy',hex(m[0xcfe5]))
    run_turn(0,seen);allt=' '.join(seen);print([x for x in seen if x.endswith('!') or x.endswith('▼')][:6])
    assert 'used BLACK FLAME' in allt and ('fainted' in allt) ;print('PASS player AZHI BLACK FLAME knocks out the wild Pokemon')
    shot('v10_player_bf')
elif MODE=='sprites':                                           # real Kabutops (wild) vs real Aerodactyl (player)
    load('v6_after_macabre');s=0xd16b
    m[s]=0xab;m[0xd164]=0xab;m[s+5]=5;m[s+6]=2
    for k in range(10):m[0xd888+2*k]=20;m[0xd889+2*k]=0x5b
    random.seed(9)
    for i in range(800):
        if m[0xd057]:break
        walk(random.choice(['up','down','left','right']),1);m[0xd455]=255
        for k in range(10):m[0xd888+2*k]=20;m[0xd889+2*k]=0x5b
    assert m[0xd057]==1
    for i in range(30):
        if 'FIGHT' in box():break
        p.button('a',8);p.tick(120)
    print('enemy',hex(m[0xcfe5]),'mine',hex(m[0xd014]),txt()[0],txt()[7]);shot('v10_real_kab_vs_aero')
    assert m[0xcfe5]==0x5b and m[0xd014]==0xab;print('PASS screenshot: wild KABUTOPS vs player AERODACTYL')
