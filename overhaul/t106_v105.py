# v105: legendary birds and fixed METAMORPHOSIS forms. Modes:
#  birds        - as BLACK the bird at POWER PLANT (ZAPDOS) / VICTORY ROAD 2F (MOLTRES) / SEAFOAM B4F (ARTICUNO) is hidden;
#                 control: not BLACK, the bird is there
#  oak          - PROF. OAK's party: no bird fought before = MR. MIME, VENUSAUR, ARTICUNO, ZAPDOS, MOLTRES, MEW; ZAPDOS fought = without
#                 ZAPDOS; all three fought = MR. MIME, VENUSAUR, MEW
#  meta <WHO>   - LORELEI / BRUNO / LANCE / BLUE / BILL beaten as BLACK, METAMORPHOSIS in the phase: the fixed POKeMON joins
#  (control: t47_v39.py's trainer METAMORPHOSIS still gives a random POKeMON)
import sys
MY=sys.argv[1:]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY[0]
RB=open(ROM,'rb').read()
def spname(x):
    cm={0x80+i:c for i,c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')};cm[0xe8]='.'
    return ''.join(cm.get(b,'?') for b in RB[0x1c21e+10*(x-1):0x1c21e+10*x] if b!=0x50)
def summon(i):
    y,x=m[0xd361],m[0xd362];b1=0xc100+i*16;b2=0xc200+i*16
    m[b2+4]=y-1+4;m[b2+5]=x+4;m[b2+6]=0xff
BIRDS=[('ZAPDOS',0x53,9,(0xd5b0,5),(0xd7d4,1)),('MOLTRES',0xc2,6,(0xd5b1,3),(0xd7ee,6)),('ARTICUNO',0xa2,3,(0xd5c2,3),(0xd882,2))]
if MODE=='birds':
    for name,mp,obj,tog,beat in BIRDS:
        for black in (False,True):
            warp(mp,0,make_black if black else (lambda:None));T(30)
            summon(obj);T(60)
            hid=bool(m[tog[0]]&(1<<tog[1]));img=m[0xc102+16*obj]
            print(name,'black',black,'toggle',hid,'image',hex(img),'pic',hex(m[0xc100+16*obj]),flush=True)
            if black:ok(hid and img==0xff,'%s: gone as BLACK (show/hide bit set, not drawn)'%name)
            else:ok(not hid and img!=0xff and not (m[beat[0]]&(1<<beat[1])),'%s: there when not BLACK (control)'%name)
elif MODE=='oak':
    def setup(mask):
        def f():
            make_black();lead(CHAR);strong(0)
            b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35
            m[0xd867]|=2;m[0xd876]=6
            for i,(name,mp,obj,tog,beat) in enumerate(BIRDS):
                if mask&(1<<i):m[beat[0]]|=1<<beat[1]
        return f
    for mask,want in ((0,['MR.MIME','VENUSAUR','ARTICUNO','ZAPDOS','MOLTRES','MEW']),(1,['MR.MIME','VENUSAUR','ARTICUNO','MOLTRES','MEW']),
                      (7,['MR.MIME','VENUSAUR','MEW'])):
        warp(0xe3,0,setup(mask));T(100)
        m[0xd877]=0x10
        for i in range(400):
            if m[0xd057] and m[0xd89c]:break
            if box():press_('a',80)
            else:T(20)
        n=m[0xd89c];sp=[spname(x) for x in m[0xd89d:0xd89d+n]]
        print('mask',mask,'party',sp,flush=True)
        ok(m[0xd031]==26 and sp==want,'birds fought %s: OAK has %s'%([b[0] for i,b in enumerate(BIRDS) if mask&(1<<i)] or 'none',', '.join(want)))
elif MODE=='meta':
    WHO=MY[1]
    WANT={'LORELEI':'GOLDEEN','BRUNO':'GOLEM','LANCE':'CHARIZARD','BLUE':'FEAROW','BILL':'MR.MIME'}.get(WHO)
    def setup():
        make_black();lead(CHAR);strong(0)
        b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35
        if WHO=='BLUE':m[0xd866]|=0x40
        if WHO=='BILL':m[0xd867]|=2;m[0xd876]=5
    if WHO=='LORELEI':to_battle(0xf5,3,5,setup,one=True)
    elif WHO=='BRUNO':to_battle(0xf6,3,5,setup,one=True)
    elif WHO=='LANCE':to_battle(0x71,None,None,setup,one=True)
    elif WHO in ('BLUE','BILL'):
        warp(0x78 if WHO=='BLUE' else 0x58,0,setup)
        for i in range(60):
            if m[0xd057]:break
            if box():press_('a',100)
            else:T(20)
        m[0xd89c]=1;wait_menu()
    print(WHO,'class',hex(m[0xd031]),'no',m[0xd05d],flush=True)
    if True:
        menu('fight');m[0xcc26]=1;T(4);seen.clear();p.button('a',8)
        for k in range(2500):
            p.tick()
            if k%4==0:T(1)
            if m[0xd05a]==3 and 'FIGHT' in clean(' '.join(txt())):break
            if k%90==0:p.button('a',8)
        ok(m[0xd05a]==3,'%s beaten, the phase began'%WHO)
        p0=party();seen.clear();use_move(0,300,in_moves=True)
        for i in range(30):
            if m[0xd057]==0:break
            press_('a',100)
        for i in range(8):press_('a',60)
        T(120);pt=party();got=spname(pt[-1]) if len(pt)>len(p0) else None
        print(WHO,'joined',got,'|',allt()[-160:],flush=True)
        ok(got==WANT,'METAMORPHOSIS on %s: %s joins'%(WHO,WANT))
print('t106 done',flush=True)
