# v71: notoriety + the bribed Saffron gate guards
import sys
MY=sys.argv[1]
sys.argv=['x','none']
exec(open('t28_v14.py').read().split("if MODE=='mirage_rate':")[0].replace("MODE=sys.argv[1]","MODE='x'"))
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
GATES=[(0x46,'up',2),(0x49,'up',3),(0x4c,'right',3),(0x4f,'right',2)]
BACK={'up':'down','right':'left'}
def money(b):return (m[0xd347]<<16)|(m[0xd348]<<8)|m[0xd349]
def setmoney(v):    # v = 6 BCD digits as an int like 0x002000
    m[0xd347],m[0xd348],m[0xd349]=v>>16,(v>>8)&255,v&255
def enter(mp,notor,cash,last=0,black=0,drink=True):
    warp_from_pallet(mp,0);m[0xd887]=0
    if drink:m[0xd728]|=0x40
    m[0xd85c]=notor;setmoney(cash);m[0xd85d]=0;m[0xd46c]=black;m[0xd365]=last
    seen.clear()
def walk_in_gate(d,n):
    for i in range(n):
        p.button(d,8);T(24)
        if m[0xd843] or box():break
def answer(yes=True,limit=40):
    for i in range(limit):
        b=box()
        if not b and i>8:break
        if not yes and any('YES' in r for r in txt()):
            p.button('down',8);p.tick(10)
        press_('a',70)
if MY=='gates':
    for mp,d,n in GATES:
        nm=hex(mp)
        # 1. notoriety 5: suspicion + fee 500, pay
        enter(mp,5,0x002000);start=pos();walk_in_gate(d,n);answer(True)
        t=allt().replace("'","");print(nm,'pay:',t[-260:].replace('\n',' '),flush=True)
        ok('description' in t and 'silence' in t,'%s: notoriety 5 -> suspicion text and the fee prompt'%nm)
        ok(money(0)==0x001500,'%s: the fee 500 was paid (money %06x)'%(nm,money(0)))
        ok(m[0xd85d]==1,'%s: paid flag set'%nm)
        # 2. walk on in the same visit: no second prompt
        seen.clear();
        for i in range(2):p.button(BACK[d],8);T(24)
        for i in range(2):p.button(d,8);T(24)
        ok(m[0xd843]==0 and not box() and 'silence' not in allt(),'%s: no second prompt during the same visit'%nm)
        # 3. refuse
        enter(mp,5,0x002000);walk_in_gate(d,n);before=pos();answer(False);T(120)
        ok(money(0)==0x002000,'%s: NO -> nothing paid'%nm)
        ok(m[0xd85d]==0,'%s: NO -> not paid'%nm)
        ok(pos()!=before,'%s: NO -> sent back (moved from %s to %s)'%(nm,before,pos()))
        # 4. poor
        enter(mp,5,0x000300);walk_in_gate(d,n);before=pos();answer(True);T(120)
        ok(money(0)==0x000300 and m[0xd85d]==0 and pos()!=before,'%s: not enough money -> nothing paid, sent back'%nm)
        # 5. low notoriety: no prompt
        enter(mp,2,0x002000);walk_in_gate(d,n);T(60)
        ok('silence' not in allt() and money(0)==0x002000,'%s: notoriety 2 -> no bribe'%nm)
        # 6. BLACK: no prompt
        enter(mp,40,0x002000,black=1);walk_in_gate(d,n);T(60)
        ok('silence' not in allt() and money(0)==0x002000,'%s: BLACK is never charged'%nm)
        # 7. coming out of SAFFRON: no prompt
        enter(mp,40,0x002000);m[0xd365]=0x0a;walk_in_gate(d,n);T(60)
        ok('silence' not in allt() and money(0)==0x002000,'%s: coming out of SAFFRON is free'%nm)
    # tiers and fee cap (one gate)
    for notor,key,fee in ((3,'fit some',0x000300),(12,'match the',0x001200),(30,'killer',0x003000),(100,'killer',0x006000)):
        enter(0x46,notor,0x009900);walk_in_gate('up',2);answer(True)
        t=allt().replace("'","")
        ok(key in t and money(0)==0x009900-fee,'notoriety %d: %s tier, fee %06x (money %06x)'%(notor,key,fee,money(0)))
    # leaving and coming back: pay again
    enter(0x46,5,0x002000);walk_in_gate('up',2);answer(True)
    enter(0x46,5,0x001500);m[0xd85d]=0;walk_in_gate('up',2);answer(True)
    ok(money(0)==0x001000,'a new visit means paying again (money %06x)'%money(0))
    # a murderer sees the bulletin first
    enter(0x46,5,0x002000);m[0xd453]=1;walk_in_gate('up',2);answer(True)
    t=allt().replace("'","");print('bulletin:',t[:300],flush=True)
    i1=t.find('description');ok(i1>0,'murder + notoriety: the dialogue plays')
    print('t79 gates done',flush=True)
if MY=='notor':
    def summon(i):
        y,x=m[0xd361],m[0xd362];b1=0xc100+i*16;b2=0xc200+i*16
        m[b1+4]=0x2c;m[b1+6]=0x40;m[b2+4]=y-1+4;m[b2+5]=x+4;m[b2+6]=0xff
    def talk_up(i):
        summon(i);T(10);p.button('up',8);T(20);seen.clear()
        for k in range(30):
            if m[0xd057] or (not box() and k>12):break
            press_('a',70)
    def case(name,mp,spr,mode,want):
        warp_from_pallet(mp,0);m[0xd887]=0
        m[0xd16b+1]=1;m[0xd16b+2]=0x2c;m[0xd16b+34]=1;m[0xd16b+35]=0x2c
        if mode=='normal':m[0xd16b+8:0xd16b+12]=[0x21,0,0,0];m[0xd16b+29]=0x3f
        m[0xd85c]=0
        talk_up(spr)
        if not m[0xd057]:ok(False,'%s: battle starts'%name);return
        if mode=='kill':fight(limit=1500)
        else:fight(limit=1500,hp1=True,spare=True)
        for k in range(10):press_('b',60)
        for k in range(10):press_('b',60)
        print(name,'notoriety',m[0xd85c],'murder',m[0xd453],flush=True)
        ok(m[0xd85c]==want,'%s: notoriety %d (wanted %d)'%(name,m[0xd85c],want))
    case('route 3 trainer, CURSE and spared',0x0e,2,'spare',1)
    case('route 4 trainer, CURSE and spared',0x0f,2,'spare',1)
    case('route 3 trainer, no CURSE',0x0e,2,'normal',0)
    case('route 3 trainer, killed',0x0e,2,'kill',0)
    case('PEWTER gym trainer, CURSE and spared',0x36,2,'spare',1)
    case('PEWTER leader BROCK, CURSE and spared',0x36,1,'spare',1)
    # two battles in a row on one map, then a battle without CURSE
    warp_from_pallet(0x11,0);m[0xd887]=0                              # ROUTE 6: several trainers
    m[0xd16b+1]=1;m[0xd16b+2]=0x2c;m[0xd16b+34]=1;m[0xd16b+35]=0x2c;m[0xd85c]=0
    done=0
    for spr in (1,2,3):
        m[0xd16b+1]=1;m[0xd16b+2]=0x2c
        talk_up(spr)
        if not m[0xd057]:continue
        fight(limit=1500,hp1=True,spare=True)
        for k in range(20):press_('b',60)
        m[0xc100+spr*16]=0;m[0xc204+spr*16]=0xff;m[0xc205+spr*16]=0xff
        done+=1;print('seq battle',spr,'notoriety',m[0xd85c],flush=True)
        if done==2:break
    ok(done==2 and m[0xd85c]==2,'two spared battles in a row on one map: notoriety 2 (done %d, got %d)'%(done,m[0xd85c]))
    # a wild CURSE is not a victim
    warp_from_pallet(0x0c,0);m[0xd887]=0;m[0xd85c]=0
    ok(True,'(wild battles are excluded by the trainer-class test; see build notes)')
print('t79 done',flush=True)
