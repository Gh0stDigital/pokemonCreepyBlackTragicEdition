# v77: the ritual. Modes:
#  chamber - entering the TOWER CHAMBER: map music id FF (stop) and nothing playing; MR. MU's battle: "stepped into the circle" and then the menu - no "Go!" / send-out;
#            no victory fanfare (ids F6/F9/FC) during the whole ritual
#  fossils - the three fossil sprites are on their stands at RIT 0..5 and gone at RIT 6 (BLACK)
#  climax  - the GHOST battle: the first menu is the player's turn (RIT 7): PKMN / ITEM / RUN refused, FIGHT -> "used STRUGGLE!" and GHOST does not move;
#            at the next menu GHOST takes its turn: "used CURSE!" ... BLACK. The chamber music comes back with BLACK (map music id = the Tower's)
import sys
#  victory - normal case: a wild fight outside the chamber still plays the victory fanfare (id F9)
MY85=sys.argv[1]
sys.argv=['x','none']
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
if MY85=='victory':
    exec(open('t28_v14.py').read().split("if MODE=='mirage_rate':")[0].replace("MODE=sys.argv[1]","MODE='x'"))
    import random
    random.seed(3)
    ids=[]
    p.hook_register(0,0x23de,lambda c:ids.append(p.register_file.A),None)
    load('pallet_with_ghost');m[0xd45c]=0;m[0xd455]=255
    to_route1()
    for i in range(800):
        if m[0xd057]:break
        walk_in(0xc,random.choice(['up','down','left','right']))
    ids.clear();fight(hp1=True)
    for k in range(200):p.tick()
    ok(0xf9 in ids,'a normal wild win plays the victory fanfare (F9): %s'%sorted(set(ids)))
    print('t85 done',flush=True);sys.exit(0)
exec(open('t35_v25.py').read().split("if MODE=='items':")[0])
snd=[]
p.hook_register(0,0x23de,lambda c:snd.append((p.register_file.A,m[0xd35e])),None)
def sprites69():return {i:m[0xc100+16*i] for i in range(2,5)}
if MY85=='chamber':
    chamber();T(60)
    print('music id (D35B)',hex(m[0xd35b]),'last music',hex(m[0xcfca]),flush=True)
    ok(m[0xd35b]==0xff and m[0xcfca]==0xff,'the chamber has no music (map music id FF, nothing playing)')
    set_bag([(POTION,3)])
    bfs_to(12,11);seen.clear();p.button('up',8);T(30);press_('a',90);texts=[]
    for k in range(200):
        if m[0xd057]:break
        b=scr()
        if 'YES' in b and 'NO' in b:press_('a',90);continue
        if not box():T(10);continue
        press_('a',60)
    seen.clear()
    for k in range(80):
        press_('a',30)
        if menu_shown() and m[0xd057]:break
    t=allt();print('battle start texts:',t[:160],flush=True)
    ok('stepped' in t and 'Go!' not in t,'MR. MU stepped into the circle, then the menu: no "Go! RED!"')
    ok(menu_shown(),'the battle menu is there')
    # the rest of the ritual (battle, MIRAGE, catch) is covered by t34; here: no victory music in the chamber
    snd.clear()
    for k in range(60):
        if m[0xcfe5]==MIR:break
        if menu_shown():choose('FIGHT');press_('a',60)
        else:press_('a',60)
    for k in range(10):
        if menu_shown():break
        press_('a',60)
    choose('ITEM');T(30);pick_item('MASTER');press_('a',10)
    for k in range(3000):
        p.tick()
        if k%120==0:p.button('a',8)
        if not m[0xd057] and k>200:break
    T(300)
    ids=sorted({a for a,mp in snd if mp==0x69 and a in (0xf6,0xf9,0xfc)})
    print('victory ids played in the chamber',ids,'RIT',m[RIT],flush=True)
    ok(not ids and m[RIT]==3,'no victory fanfare during the ritual (MR. MU, the MIRAGE, the catch)')
elif MY85=='fossils':
    for rit in (0,3,4,6):
        chamber();T(40)
        m[RIT]=rit;T(40)
        pic=sprites69()
        print('RIT',rit,pic,flush=True)
        if rit<6:ok(all(v==0x3e for v in pic.values()),'RIT %d: the three fossils stand on their stands'%rit)
        else:ok(all(v==0 for v in pic.values()),'RIT 6 (BLACK): the fossils are gone')
elif MY85=='climax':
    ritual_state();T(30)
    print('chamber music before',hex(m[0xd35b]),flush=True)
    p.button('down',8);T(24);p.button('down',8);T(30)
    for k in range(600):
        T(1)
        if MIR not in party():break
    for k in range(40):
        if 'MIRAGE' in allt() and not box():break
        press_('a',45)
    for k in range(2):
        press_a_until(lambda:not box(),n=10,wait=40)
        p.button('down',8);T(24)
    for k in range(400):
        if m[0xd057]:break
        p.tick()
    ok(m[0xd057]==1 and m[RIT]==5,'the GHOST battle starts (RIT 5)')
    seen.clear()
    for k in range(300):
        press_('a',30)
        if menu_shown():break
    ok(menu_shown() and m[RIT]==7,'the first menu is shown normally: the player\'s turn (RIT 7, no CURSE yet): %s'%allt()[-60:])
    ok('CURSE' not in allt(),'GHOST has not acted before the first command')
    seen.clear();choose('RUN');T(40)
    for k in range(6):
        if menu_shown():break
        press_('a',40)
    ok('aura' in allt() and m[0xd057]==1 and m[RIT]==7,'RUN is refused ("GHOST\'s aura holds you here!"): %s'%allt()[-50:])
    seen.clear()
    for k in range(6):
        if menu_shown():break
        press_('a',40)
    choose('FIGHT');press_('a',60)
    texts=[];black_ran=False
    for k in range(9000):
        p.tick();b=clean(box())
        if b and (not texts or texts[-1]!=b):texts.append(b)
        if m[0xd057]==0 and k>300:break
        if k%40==20:p.button('a',8)
    full=' '.join(texts)
    i1=full.find('STRUGGLE');i2=full.find('CURSE')
    print('order: STRUGGLE at',i1,'CURSE at',i2,flush=True)
    ok(0<=i1<i2,'the player used STRUGGLE first, then GHOST used CURSE')
    between=full[i1:i2]
    print('between:',between[:200],flush=True)
    import re
    rest=re.sub(r'GHOST used( C(U(R(S(E!?)?)?)?)?)?','',between)
    ok('GHOST used' not in between or ('used' not in rest),'GHOST did nothing else in between')
    T(300)
    ok(m[0xd46c]==1 and m[RIT]==6,'BLACK is born (flag, RIT 6)')
    print('chamber music after',hex(m[0xd35b]),'last',hex(m[0xcfca]),flush=True)
    ok(m[0xd35b]!=0xff,'the chamber music id is back with BLACK (D35B %02X)'%m[0xd35b])
print('t85 done',flush=True)
