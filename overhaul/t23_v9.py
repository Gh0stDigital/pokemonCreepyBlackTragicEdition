# v9: Black Tamer's PRETA vs player's PRETA (names, MACABREBLADE immunity, win by SURF);
#     Rare Candy refused for GHOST/PRETA; Pokemon Center skips GHOST/PRETA.
from harness import *
import random,sys
MODE=sys.argv[1] if len(sys.argv)>1 else 'mirage'
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
if MODE=='mirage':
    def find_mirage(seed):
        random.seed(seed);load('v6_after_macabre');m[0xd45c]=200
        for step in range(3000):
            if m[0xd057]:
                p.tick(30)
                if m[0xd45d]:return True
                for i in range(40):
                    if m[0xd057]==0:break
                    if 'FIGHT' in box():p.button('down',8);p.tick(10);p.button('right',8);p.tick(10);p.button('a',8);p.tick(150)
                    else:p.button('a',8);p.tick(150)
                continue
            m[0xd455]=255;walk(random.choice(['up','down','left','right']),1)
    for seed in range(20,40):
        assert find_mirage(seed);intro=[]
        for i in range(40):
            b=clean(box())
            if b and (not intro or intro[-1]!=b):intro.append(b)
            if 'FIGHT' in box() and m[0xd014]==0xb6:break
            p.button('a',8);p.tick(160)
        if m[0xcfe5]==0xb6:break
    print('intro:',[x for x in intro if 'PRETA' in x or 'KABUTOPS' in x])
    seen=[];moves=['MACABRE','SURF','SURF','SURF']
    for turn,mv in enumerate(moves):
        if m[0xd057]==0:break
        for i in range(30):
            if 'FIGHT' in box():break
            p.button('a',8);p.tick(120)
        hp=m[0xd015]<<8|m[0xd016];ehp=m[0xcfe6]<<8|m[0xcfe7]
        p.tick(60)
        for k in range(4):
            if '▲FIGHT' in box():break
            p.button('up',8);p.tick(20);p.button('left',8);p.tick(20)
        for k in range(5):
            p.button('a',8);p.tick(60)
            if 'MACABRE' in ' '.join(txt()):break
        for k in range(4):
            if ('▲'+mv) in ' '.join(txt()):break
            p.button('down',8);p.tick(20)
        p.button('a',8)
        for i in range(1500):
            p.tick()
            if i%4==0:
                b=clean(box())
                if b and (not seen or seen[-1]!=b):seen.append(b)
            if i%60==30 and box() and 'FIGHT' not in box():p.button('a',8)
            if m[0xd057]==0 or ('FIGHT' in box() and i>300) or 'Bring out' in box():break
        print('turn',turn,mv,'my HP',hp,'->',m[0xd015]<<8|m[0xd016],'enemy HP',ehp,'->',m[0xcfe6]<<8|m[0xcfe7],flush=True)
        assert 'Bring out' not in box(),'PRETA died'
    full=[s for s in seen if s.endswith('!') or s.endswith('▼')]
    for s in full:print('  TEXT:',s)
    allt=' '.join(seen+intro)
    assert 'KABUTOPS' not in allt and 'Enemy PRETA used MACABREBLADE' in allt and 'affect PRETA' in allt and 'affect Enemy PRETA' in allt
    for i in range(60):
        if m[0xd057]==0:break
        p.button('a',8);p.tick(120)
    p.tick(200);print('after: party',list(m[0xd164:0xd16b]),'mirage',m[0xd45d])
    assert m[0xd057]==0 and 0xb6 in m[0xd164:0xd16b] and 0x1f in m[0xd164:0xd16b]
    print('PASS PRETA vs PRETA: names, MACABREBLADE/MACABRE no effect, SURF wins')
elif MODE=='candy':
    load('v6_after_macabre');p.tick(60)
    n=m[0xd31d];m[0xd31e+2*n]=0x28;m[0xd31f+2*n]=5;m[0xd320+2*n]=0xff;m[0xd31d]=n+1   # RARE CANDY x5
    def use_candy(slot):
        press('start',90)
        for i in range(6):
            if '▲ITEM' in ' '.join(txt()):break
            press('down',30)
        press('a',150)
        for i in range(6):
            if '▲RARE CANDY' in ' '.join(txt()):break
            press('up',20)
        press('a',90);press('a',90)                      # USE
        for i in range(6):
            if m[0xcc26]==0:break
            press('up',20)
        for i in range(slot):press('down',20)
        lv0=m[0xd16b+44*slot+33];press('a',150);seen=[]
        for i in range(12):
            b=clean(box())
            if b and (not seen or seen[-1]!=b):seen.append(b)
            press('a',90)
        for i in range(4):press('b',60)
        return lv0,m[0xd16b+44*slot+33],seen
    res={}
    for slot,name in ((0,'PRETA'),(1,'GHOST'),(2,'CHARMANDER')):
        res[name]=use_candy(slot);print(name,'level',res[name][0],'->',res[name][1],[s for s in res[name][2] if 'effect' in s or 'grew' in s][:2])
    assert res['PRETA'][0]==res['PRETA'][1]==50 and res['GHOST'][0]==res['GHOST'][1] and res['CHARMANDER'][1]>res['CHARMANDER'][0]
    assert any('effect' in s for s in res['PRETA'][2]+res['GHOST'][2])
    print('PASS Rare Candy refused for PRETA and GHOST, works on CHARMANDER')
elif MODE=='center':
    load('pallet_with_ghost');party=None
    load('v6_after_macabre');pt=list(m[0xd163:0xd2f7]);dx=list(m[0xd2f7:0xd31d])
    load('pallet_with_ghost');m[0xd163:0xd2f7]=pt;m[0xd2f7:0xd31d]=dx;m[0xd455]=255
    for i in range(3):
        s=0xd16b+44*i;m[s+1]=0;m[s+2]=5                 # every party member at 5 HP
    m[0xd16b+29]=3                                      # PRETA's MACABRE at 3 PP
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x29   # door -> Viridian Pokemon Center
    for i in range(6):
        if m[0xd35e]==0x29:break
        walk('up',1)
    p.tick(120);print('center',pos());assert m[0xd35e]==0x29
    for i in range(8):
        if pos()[2]<=4:break
        walk('up',1)
    p.button('up',8);p.tick(30);print('at',pos())
    seen=[]
    for i in range(40):
        b=clean(box())
        if b and (not seen or seen[-1]!=b):seen.append(b)
        if 'fighting fit' in b:break        # (pressing on past the nurse's goodbye hangs PyBoy, also on v1)
        p.button('a',8);p.tick(30)
    print('TEXT:',[s for s in seen if 'POK' in s][:4])
    hp=[m[0xd16c+44*i]<<8|m[0xd16d+44*i] for i in range(3)];print('party',list(m[0xd164:0xd167]),'HP',hp,'MACABRE PP',m[0xd16b+29])
    assert hp[0]==5 and hp[1]==5 and hp[2]>5 and m[0xd16b+29]==3 and any('restored' in s or 'healthy' in s or 'fighting' in s for s in seen)
    print('PASS Pokemon Center heals CHARMANDER but not PRETA or GHOST')
