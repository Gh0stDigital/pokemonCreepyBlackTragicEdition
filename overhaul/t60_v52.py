# v52: where MR. MU is + the Mansion AMBER -> AZHI awakening. Modes:
#  cerulean - trade house (map 3F): Mu is there normally; gone when AGATHA took the DOME FOSSIL (D464 >= 2, D460 < 2) or a KABUTO
#             was revived at the lab (dex #140 owned); not gone when PRETA was awakened (D460 2) with D464 >= 2
#  mansion  - Mansion 1F (map A5): Mu only with D460 == 3; gone with D460 0/2/4, with D464 >= 2, or an AERODACTYL revived (#142)
#  azhi     - Mansion Mu with OLD AMBER: the question, THEY WOULD NOT changes nothing, THEY WOULD gives a Lv35 AZHI (perfect DVs,
#             amber gone, D460 = 4, Mu gone on re-entering); party full: "make room", nothing changes; no amber: his usual lines
import sys
MY60=sys.argv[1]
sys.argv=['x'];exec(open('t21_mansion_mu.py').read().split("# before: Mansion without PRETA")[0])
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:sys.exit(1)
def go(mapid,state,stage=0,dex=0,extra=None):
    load('pallet_with_ghost');m[0xd455]=255;m[0xd460]=state;m[0xd464]=stage;m[0xd308]=(m[0xd308]&~0x2a)|dex
    if extra:extra()
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=mapid
    for i in range(6):
        if m[0xd35e]==mapid:break
        walk('up',1)
    p.tick(120);m[0xd887]=0
    return m[0xc130] if mapid==0x3f else m[0xc140]
if MY60=='cerulean':
    ok(go(0x3f,1)!=0,'normal: Mu is in the trade house')
    ok(go(0x3f,1,stage=2)==0,'AGATHA took the DOME FOSSIL (stage 2, no PRETA): Mu is gone')
    ok(go(0x3f,0,stage=3)==0,'...also before he introduced himself')
    ok(go(0x3f,1,dex=0x08)==0,'a KABUTO was revived at the lab: Mu is gone')
    ok(go(0x3f,1,dex=0x20)!=0,'an AERODACTYL revived (the AMBER side) does not affect the Cerulean Mu')
    ok(go(0x3f,2,stage=2)!=0,'PRETA awakened: Mu stays until the player leaves (even after the quest started)')
    ok(go(0x3f,1,stage=1)!=0,'quest stage 1 only: Mu is still there')
elif MY60=='mansion':
    ok(go(0xa5,3)!=0,'D460 3 (DOME awakened, left Cerulean): Mu is at the Mansion')
    for st,name in ((0,'not met'),(1,'introduced'),(4,'AZHI awakened')):ok(go(0xa5,st)==0,'D460 %d (%s): no Mu at the Mansion'%(st,name))
    ok(go(0xa5,3,stage=2)==0,'AGATHA took the OLD AMBER: Mu is gone from the Mansion')
    ok(go(0xa5,3,dex=0x20)==0,'an AERODACTYL was revived at the lab: Mu is gone')
    ok(go(0xa5,3,dex=0x08)!=0,'a KABUTO revived (the DOME side) does not affect the Mansion Mu')
elif MY60=='azhi':
    def amber():n=m[0xd31d];m[0xd31e+2*n]=0x1f;m[0xd31f+2*n]=1;m[0xd320+2*n]=0xff;m[0xd31d]=n+1
    def to_mu():
        for i in range(5):walk('up',1)
        walk('right',2);p.button('up',8);p.tick(30)
    def talk2(answer=None,n=40):
        lines=[];p.button('a',8);p.tick(60);quiet=0;given=answer is None
        for i in range(n*3):
            b=box();s=' '.join(txt())
            if b and (not lines or lines[-1]!=b):lines.append(b)
            if 'THEY WOULD' in s and not given:
                p.tick(30)
                for k in range(3):
                    if answer!='yes' or m[0xcc26]==1:break
                    p.button('down',8);p.tick(20)
                p.button('a',8);p.tick(90);given=True;continue
            quiet=0 if b else quiet+1
            if quiet>(14 if given and answer=='yes' else 3):break
            p.button('a',8);p.tick(60)
        return ' '.join(' '.join(''.join(c for c in l if c not in '│─┌┐└┘|').split()) for l in lines)
    def bag():return [(m[0xd31e+2*i],m[0xd31f+2*i]) for i in range(m[0xd31d])]
    go(0xa5,3);to_mu();t=talk2();print('no amber:',t)
    ok('mansion' in t and 'amber' in t and m[0xd460]==3,'no OLD AMBER: his usual lines, nothing changes')
    go(0xa5,3,extra=amber);to_mu();t=talk2('no');print('NO:',t[-160:])
    ok('they would ask' in t.replace('  ',' ') and (0x1f,1) in bag() and m[0xd460]==3 and 0xb7 not in list(m[0xd164:0xd16a]),'THEY WOULD NOT: the question, nothing changes (amber kept)')
    t=talk2('yes');print('YES:',t[-200:]);pt=list(m[0xd164:0xd164+m[0xd163]])
    ok(0xb7 in pt and (0x1f,1) not in bag() and m[0xd460]==4,'THEY WOULD: AZHI joined, the amber is gone, D460 = 4')
    i=pt.index(0xb7);b=0xd16b+44*i;st=[m[b+34+2*j]<<8|m[b+35+2*j] for j in range(5)]
    print('AZHI',m[b+33],st,[hex(x) for x in m[b+8:b+12]],hex(m[b+27]),hex(m[b+28]))
    ok(m[b+33]==35 and m[b+3]==35 and m[b+27]==m[b+28]==0xff and list(m[b+8:b+12])==[0xa8,0x13,0x52,0x8f] and (m[b+12],m[b+13])==(m[0xd359],m[0xd35a]),'AZHI Lv35, perfect DVs, BLACK FLAME / FLY / DRAGON RAGE / SKY ATTACK, the player\'s OT')
    ok('AZHI' in t and 'received' in t,'"<PLAYER> received AZHI!"')
    shot('v52_azhi')
    ok(go(0xa5,m[0xd460])==0,'D460 4: Mu is gone when the player comes back')
    def full():
        amber()
        for i in range(m[0xd163],6):m[0xd163]+=1;m[0xd164+i]=m[0xd164];m[0xd164+i+1]=0xff
    go(0xa5,3,extra=full);to_mu();t=talk2('yes');print('FULL:',t[-120:])
    ok('room' in t and (0x1f,1) in bag() and m[0xd460]==3 and 0xb7 not in list(m[0xd164:0xd16a]),'party full: "make room", nothing changes')
