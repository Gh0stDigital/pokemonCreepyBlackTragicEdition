# v50: PRETA and AZHI. Modes:
#  nervous - PRETA's CUT on a wild RATTATA: the damage after the type step is doubled (defense counts half);
#            normal: CHARMANDER's SCRATCH is not changed
#  anxious - AZHI out: the wild RATTATA's move accuracy is halved; normal: with CHARMANDER out it is not
#  revive  - PRETA fainted in the party: back after 2 turns with half its HP ("PRETA rose from the dead!"); AZHI after 3
#  posthp  - after a battle PRETA and AZHI (damaged) are at full HP; a damaged CHARMANDER stays damaged
#  preta25 - the PRETA MR. MU awakens (2E struct) is Lv25 with Lv25 stats and experience
#  xitem   - X ATTACK with BLACK out: no effect; with CHARMANDER out it works
#  ritual  - the climax with a Lv25 PRETA in the party and a Lv35 AZHI in the box: PRETA is Lv50 afterwards (stats, full HP),
#            the boxed AZHI Lv50 (experience), neither is given twice
import sys,json
MY58=sys.argv[1]
if MY58=='ritual':
    sys.argv=['x','none'];exec(open('t46_v38.py').read().split("if MODE in ('join','owned'):")[0]);MODE=MY58
else:
    sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY58
from patchlib import enc
MAN=json.load(open('manifest_v50.json'))['labels'];L2F={k:int(v,16) for k,v in MAN['bank2f'].items()}
SA=fo(0x2d,int(L['s_azhi'],16))
def start_wild(setup,species=0xa5,lv=5):
    load('pallet_with_ghost');setup();m[0xd059]=species;m[0xd127]=lv
    for i in range(300):
        if m[0xd057]:break
        p.tick()
    wait_menu();T(20)
def put(slot,struct,name):
    b=0xd16b+44*slot;m[b:b+44]=list(struct);m[0xd164+slot]=struct[0];m[b+12]=m[0xd359];m[b+13]=m[0xd35a]
    m[0xd2b5+11*slot:0xd2b5+11*slot+11]=list(enc(name))+[0x50]*(11-len(name))
def turn(slot):
    seen.clear();use_move(slot,300)
    for k in range(12):
        tt=clean(' '.join(txt()))
        if ('FIGHT' in tt and 'RUN' in tt) or m[0xd057]==0:break
        press_('a',60)
    return allt()
def mhp(slot):b=0xd16b+44*slot;return m[b+34]<<8|m[b+35]
def hp(slot):b=0xd16b+44*slot;return m[b+1]<<8|m[b+2]
if MODE=='nervous':
    seen_d=[]
    p.hook_register(0x2f,L2F['nerv50'],lambda c:seen_d.append(('in',m[0xd0d7]<<8|m[0xd0d8])),None)
    p.hook_register(0xf,0x57d0,lambda c:seen_d.append(('out',m[0xd0d7]<<8|m[0xd0d8])),None)
    start_wild(lambda:(make_black(),put(0,ROM[SP:SP+44],'PRETA')),lv=60);seen_d.clear();turn(1)   # CUT
    print('PRETA CUT',seen_d)
    pairs=[(a[1],b[1]) for a,b in zip(seen_d,seen_d[1:]) if a[0]=='in' and b[0]=='out']
    ok(pairs and all(o==min(2*i,999) and i>0 for i,o in pairs),'PRETA\'s CUT: damage doubled after the type step %s'%pairs)
    start_wild(lambda:lead(CHAR),lv=8);seen_d.clear();turn(0)
    print('CHARMANDER SCRATCH',seen_d)
    pairs=[(a[1],b[1]) for a,b in zip(seen_d,seen_d[1:]) if a[0]=='in' and b[0]=='out']
    ok(pairs and all(o==i for i,o in pairs),'normal: CHARMANDER\'s SCRATCH damage unchanged %s'%pairs)
elif MODE=='anxious':
    acc=[]
    p.hook_register(0x2f,L2F['anx50'],lambda c:acc.append(('in',m[0xcfd0])),None)
    p.hook_register(0xf,0x66cb,lambda c:acc.append(('out',m[0xcfd0])),None)
    start_wild(lambda:(make_black(),put(0,ROM[SA:SA+44],'AZHI')),lv=60);acc.clear()
    for k in range(3):turn(2)                                     # AZHI's DRAGON RAGE, the RATTATA attacks
    print('AZHI',acc)
    en=[(a[1],b[1]) for a,b in zip(acc,acc[1:]) if a[0]=='in' and b[0]=='out']
    ok(any(o==i//2 and i>1 for i,o in en),'AZHI out: the RATTATA\'s accuracy is halved %s'%en)
    start_wild(lambda:lead(CHAR),lv=8);acc.clear()
    for k in range(2):turn(1)
    en=[(a[1],b[1]) for a,b in zip(acc,acc[1:]) if a[0]=='in' and b[0]=='out'];print('CHARMANDER',en)
    ok(all(o==i for i,o in en),'normal: with CHARMANDER out the accuracy is unchanged')
elif MODE=='revive':
    for struct,name,turns in ((ROM[SP:SP+44],'PRETA',2),(ROM[SA:SA+44],'AZHI',3)):
        def s():
            lead(CHAR);put(1,struct,name);b=0xd16b+44;m[b+1]=0;m[b+2]=0;m[b+4]=0
            b0=0xd16b;m[b0+1]=0;m[b0+2]=200;m[b0+34]=0;m[b0+35]=200      # a sturdy CHARMANDER
        start_wild(s,lv=3);log=[]
        for k in range(turns+2):
            t=turn(1);log.append((hp(1),'rose from' in t.replace('  ',' ')))   # GROWL
            if m[0xd057]==0:break
        print(name,log,'max',mhp(1))
        first=[i for i,(h,r) in enumerate(log) if h>0]
        ok(first and first[0]==turns-1 and log[first[0]][0]==mhp(1)//2,'%s comes back after %d turns with half its HP (%d/%d)'%(name,turns,log[first[0]][0] if first else 0,mhp(1)))
        ok(any(r for h,r in log),'"%s rose from the dead!"'%name)
elif MODE=='posthp':
    def s():
        lead(CHAR);put(1,ROM[SP:SP+44],'PRETA');put(2,ROM[SA:SA+44],'AZHI');m[0xd163]=3;m[0xd164+3]=0xff
        for sl in (0,1,2):b=0xd16b+44*sl;m[b+1]=0;m[b+2]=10
    start_wild(s,lv=3);menu('run')
    for k in range(10):press_('a',60)
    print('after',[(hp(i),mhp(i)) for i in range(3)],'in battle',m[0xd057])
    ok(m[0xd057]==0 and hp(1)==mhp(1) and hp(2)==mhp(2),'after the battle PRETA and AZHI are at full HP')
    ok(hp(0)==10,'a damaged CHARMANDER stays damaged (normal case)')
elif MODE=='preta25':
    PS=fo(0x2e,0x469a);s=ROM[PS:PS+44]
    st=[s[34+2*i]<<8|s[35+2*i] for i in range(5)];print('MU PRETA',s[3],s[33],st,s[14]<<16|s[15]<<8|s[16],s[1]<<8|s[2])
    ok(s[0]==0xb6 and s[3]==s[33]==25 and st==[72,70,65,52,47] and (s[14]<<16|s[15]<<8|s[16])==5*25**3//4 and (s[1]<<8|s[2])==72,'MR. MU\'s PRETA: Lv25, Lv25 stats, full HP')
    ok(list(s[8:12])==[0xa9,0x0f,0x39,0x46] and s[27]==s[28]==0xff,'still MACABRE / CUT / SURF / STRENGTH and perfect DVs')
elif MODE=='ritual':
    PS=fo(0x2e,0x469a)
    def s():
        n=m[0xd163];m[0xd164+n]=PRETA;m[0xd164+n+1]=0xff;m[0xd163]=n+1
        m[0xd16b+44*n:0xd16b+44*n+44]=list(ROM[PS:PS+44])
        k=m[0xda80];m[0xda80]=k+1;m[0xda81+k]=AZHI;m[0xda81+k+1]=0xff
        b=0xda96+33*k;m[b:b+33]=list(ROM[SA:SA+33]);m[b+3]=35
    climax('v25_after_ritual_v25a',s)
    pt=party();i=pt.index(PRETA);b=0xd16b+44*i;st=[m[b+34+2*j]<<8|m[b+35+2*j] for j in range(5)]
    print('party',[hex(x) for x in pt],'PRETA lv',m[b+33],m[b+3],'stats',st,'hp',m[b+1]<<8|m[b+2])
    ok(pt.count(PRETA)==1 and m[b+33]==50 and m[b+3]==50 and st==[135,135,125,100,90] and (m[b+1]<<8|m[b+2])==135,'the Lv25 PRETA is Lv50 after the ritual (stats, full HP)')
    bx=[m[0xda81+j] for j in range(m[0xda80])];k=bx.index(AZHI);bb=0xda96+33*k
    print('box',[hex(x) for x in bx],'AZHI lv',m[bb+3],'exp',m[bb+14]<<16|m[bb+15]<<8|m[bb+16])
    ok(bx.count(AZHI)==1 and AZHI not in pt and m[bb+3]==50 and (m[bb+14]<<16|m[bb+15]<<8|m[bb+16])==5*50**3//4,'the boxed Lv35 AZHI is Lv50 (experience), not given twice')
elif MODE=='xitem':                                     # X ATTACK with BLACK out: no effect; with CHARMANDER: +1 ATTACK
    def bag_x():m[0xd31d]=1;m[0xd31e]=0x41;m[0xd31f]=3;m[0xd320]=0xff
    for who,setup in (('BLACK',lambda:(make_black(),bag_x())),('CHARMANDER',lambda:(lead(CHAR),bag_x()))):
        start_wild(setup,lv=3);seen.clear();mod0=m[0xcd1a];menu('item')
        for k in range(12):
            if m[0xcd1a]!=mod0 or 'effect' in allt():break
            press_('a',60)
        for k in range(6):press_('a',60)
        t=allt();print(who,'attack mod',mod0,'->',m[0xcd1a],'items left',m[0xd31f],t[-120:])
        if who=='BLACK':ok('effect' in t and m[0xcd1a]==mod0,'X ATTACK on BLACK: "It won\'t have any effect.", no stat change')
        else:ok(m[0xcd1a]==mod0+1,'normal: X ATTACK raises CHARMANDER\'s ATTACK')
