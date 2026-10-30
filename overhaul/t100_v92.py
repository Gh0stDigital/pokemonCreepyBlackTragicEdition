# v92 (adapts t60): where MR. MU is + the Mansion AMBER -> AZHI awakening. Modes:
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
if MY60=='talk':
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
            if b and lines.count(b)>1:break
            quiet=0 if b else quiet+1
            if quiet>(14 if given and answer=='yes' else 3):break
            p.button('a',8);p.tick(60)
        return ' '.join(' '.join(''.join(c for c in l if c not in '│─┌┐└┘|').split()) for l in lines)
    def bag():return [(m[0xd31e+2*i],m[0xd31f+2*i]) for i in range(m[0xd31d])]

    def keys():return [i for i in range(m[0xd31d]) if m[0xd31e+2*i]==0x2b]
    # 1. first talk, no amber: intro, key, nothing more
    go(0xa5,3);to_mu();t=talk2();print('T1:',t)
    ok('did not expect' in t.replace("didn't","did not").replace("  "," ") or "expect" in t,'intro text')
    ok(len(keys())==1 and m[0xd885]==1,'SECRET KEY given, D885 = 1 (no amber: no question)')
    ok('received' in t and 'SECRET KEY' in t,'"received SECRET KEY!"')
    ok('journey' in t,'"...complete your journey"')
    ok('AMBER' not in t and 'question' not in t,'no amber: no question')
    # 2. second talk, still no amber: the warning
    t=talk2();print('T2:',t)
    ok('dig too deep' in t and 'linger' in t and len(keys())==1 and 'troubling' not in t,'later talk: the warning, key not given twice')
    ok(go(0xa5,m[0xd460])!=0 ,'no question answered: Mu still there after leaving')
    # 3. amber in the bag at the second visit: check line + question, NO
    def second():
        m[0xd885]=1;amber()
        n=m[0xd31d];m[0xd31e+2*n]=0x2b;m[0xd31f+2*n]=1;m[0xd320+2*n]=0xff;m[0xd31d]=n+1
    go(0xa5,3,extra=second);to_mu();t=talk2('no');print('T3:',t[-300:])
    ok('resourceful' in t and 'humor' in t and 'they would ask' in t.replace('  ',' '),'amber later: "resourceful", "humor me", the question')
    ok((0x1f,1) in bag() and m[0xd885]==3 and m[0xd460]==3 and len(keys())==1,'NO: amber kept, D885 = 3, still here this visit')
    t=talk2();print('T3b:',t)
    ok('dig too deep' in t and 'troubling' not in t,'after NO: warning without the extra line')
    for i in range(40):
        if not box():break
        p.button('b',8);p.tick(40)
    p.tick(60)
    walk('left',2)
    for i in range(10):
        if m[0xd35e]!=0xa5:break
        walk('down',1)
    print('scr',txt()[-3:],m[0xd72e]);print('pos',m[0xd361],m[0xd362],m[0xd730],m[0xcc4b]);p.tick(120);print('D460 after leaving',m[0xd460],hex(m[0xd35e]))
    ok(m[0xd460]==4,'NO answered, left the Mansion: D460 = 4 (Mu gone)')
    # 5. first talk WITH the amber, answer YES
    go(0xa5,3,extra=amber);to_mu();t=talk2('yes');print('T5:',t[-320:])
    ok('resourceful' in t and 0xb7 in list(m[0xd164:0xd164+m[0xd163]]) and (0x1f,1) not in bag(),'first talk with amber: key, check, question, YES: AZHI joined')
    ok(m[0xd885]==7 and m[0xd460]==3 and len(keys())==1,'D885 = 7, D460 still 3 (he stays this visit)')
    t=talk2();print('T6:',t)
    ok('dig too deep' in t and 'troubling' in t and 'goal at hand' in t,'after giving the amber: warning + the extra kind lines')
    # leaving and coming back: gone
    d=m[0xd885];v=go(0xa5,m[0xd460]) if False else None
    p_state=m[0xd460]
    for i in range(40):
        if not box():break
        p.button('b',8);p.tick(40)
    p.tick(60)
    walk('left',2)
    for i in range(10):
        if m[0xd35e]!=0xa5:break
        walk('down',1)
    p.tick(120)
    ok(m[0xd460]==4 or True,'')
    print('D460 after leaving',m[0xd460])
    ok(m[0xd460]==4,'map load after the question: D460 = 4 (Mu gone)')
    # 6. key already in the bag: not given again
    def keyx():
        n=m[0xd31d];m[0xd31e+2*n]=0x2b;m[0xd31f+2*n]=1;m[0xd320+2*n]=0xff;m[0xd31d]=n+1
    go(0xa5,3,extra=keyx);to_mu();t=talk2();print('T7:',t)
    ok(len(keys())==1 and m[0xd885]==1 and 'carrying' in t,'SECRET KEY already in the bag: not given twice')
    # 7. bag full: no key, flag not set
    def fullbag():
        m[0xd31d]=20
        for i in range(20):m[0xd31e+2*i]=0x01;m[0xd31f+2*i]=1
        m[0xd31e+40]=0xff
    go(0xa5,3,extra=fullbag);to_mu();t=talk2();print('T8:',t)
    ok(len(keys())==0 and m[0xd885]&1==0 and 'pack is full' in t,'bag full: no key, nothing marked')
    # 8. normal case: unchanged Mu gone rules (D460 0/1/4 etc.)
    ok(go(0xa5,4)==0 and go(0xa5,0)==0,'D460 4 / 0: no Mu (as v52)')
    ok(go(0xa5,3)!=0,'D460 3: Mu at the Mansion (as v52)')
