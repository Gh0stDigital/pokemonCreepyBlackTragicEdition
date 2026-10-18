# v81: GHOST WALK. Modes:
#  battle    - turn 2's attack (hit or miss) gives BLACK's back picture back (tiles of the 7x7 picture are on the screen again)
#  field     - BLACK's party menu lists CURSE and GHOST WALK; GHOST WALK switches D878 on (screen inverted BGP 1B / OBP0 2F / OBP1 1F, text),
#              stays inverted after the START menu and after leaving/entering a building; selecting it again switches it off (palette e4/d0/e0)
#  encounters- flag on: 600 grass steps on ROUTE 1 and no battle; flag off: a battle starts within the same walk; a battle with the flag on has the normal palette
#  normal    - GHOST (not BLACK) has no GHOST WALK entry; palette normal; encounters happen (the usual)
import sys,random
MY81=sys.argv[1]
sys.argv=['x','none'];exec(open('t47_v39.py').read().split("if MODE=='wild':")[0]);MODE=MY81
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
INV=(0x1b,0x2f,0x1f);NORM=(0xe4,0xd0,0xe0)
def pal():return (p.memory[0xff47],p.memory[0xff48],p.memory[0xff49])
def to_route1():                                               # Pallet start (10,12) -> Route 1 grass
    for d,n in (('left',4),('up',11),('right',2),('up',4)):
        for i in range(n):walk(d,1)
def ghost_walk_menu():
    p.button('start',8);T(40);pick('POK');press_('a',90)
    m[0xcc26]=0;T(4);press_('a',90);sub=' '.join(txt())
    pick('GHOST');press_('a',90)
    for k in range(10):
        if 'Choose' in ' '.join(txt()):break
        press_('a',60)
    t=allt()
    for k in range(4):press_('b',40)
    return sub,t
if MODE=='battle':
    sys.argv=['x','gwalk'];src=open('t56_v48.py').read().split("if MODE=='moves':")[0];MODE='battle';exec(src.replace("MY56=sys.argv[1]","MY56='battle'"));MODE='battle'
    def pic():return [[m[0xc3a0+(5+r)*20+1+c] for c in range(7)] for r in range(7)]
    for miss in (0,1):
        start_wild(make_black,lv=40)
        if miss:m[0xcd2e+5]=13          # enemy evasion +6: turn 2 usually misses
        h0=ehp();seen.clear();use_move(2,400)
        for k in range(12):
            if 'dark!' in allt():break
            press_('a',40)
        T(40)
        ok(pic()[3][0]==0x7f,'turn 1: BLACK slid away (picture hidden)')
        for k in range(60):
            if m[0xd057]==0:break
            if 'FIGHT' in clean(' '.join(txt())) and k>10:break
            press_('a',40)
        T(100);t=allt()
        ok(('missed' in t) if miss else (ehp()<h0),'turn 2: %s'%('the attack missed' if miss else 'the attack hit'))
        row=[pic()[r][c] for r in range(7) for c in range(7)]
        ok(all(x!=0x7f for x in row),"BLACK's back picture is back after turn 2 (%s)"%('miss' if miss else 'hit'))
elif MODE=='field':
    load('pallet_with_ghost');make_black();T(20)
    ok(m[0xd878]==0 and pal()==NORM,'start: ghost walk off, normal palette %s'%[hex(x) for x in pal()])
    sub,t=ghost_walk_menu()
    print(sub[:200]);print(t[-200:])
    ok('CURSE' in sub and 'GHOST WALK' in sub,"BLACK's submenu lists CURSE and GHOST WALK")
    ok(m[0xd878]==1 and pal()==INV,'GHOST WALK on: flag set, screen inverted %s'%[hex(x) for x in pal()])
    ok('dark' in t,'text: BLACK slips into the dark')
    T(60);ok(pal()==INV,'still inverted in the overworld')
    p.button('start',8);T(40);ok(pal()==INV,'START menu: inverted')
    p.button('b',8);T(40);ok(pal()==INV,'after the START menu: inverted')
    # leave/enter a building: warp (walk into the house door is tool-heavy: use the map warp helper)
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x25
    for i in range(6):
        if m[0xd35e]==0x25:break
        p.button('up',8);T(24)
    T(200);print('map',hex(m[0xd35e]))
    ok(pal()==INV,'after changing map (fade in): still inverted %s'%[hex(x) for x in pal()])
    sub,t=ghost_walk_menu()
    ok(m[0xd878]==0 and pal()==NORM,'GHOST WALK again: off, palette normal %s'%[hex(x) for x in pal()])
    ok('light' in t,'text: back into the light')
    T(60);ok(pal()==NORM,'stays normal')
elif MODE=='encounters':
    for flag in (1,0):
        random.seed(5+flag);load('pallet_with_ghost');make_black();m[0xd455]=255;m[0xd878]=flag
        to_route1();assert m[0xd35e]==0xc,pos()
        hit=False
        for step in range(600):
            if flag:p.tick(1)
            m[0xd455]=255;walk_in(0x0c,random.choice(['up','down','left','right']))
            if m[0xd057]:hit=True;break
        if flag:
            ok(not hit,'ghost walk on: 600 grass steps, no battle')
        else:
            ok(hit,'ghost walk off: a wild battle starts (control)')
    # a battle with the flag on (forced) shows the normal battle palette
    load('pallet_with_ghost');make_black();m[0xd878]=1;T(10);m[0xd059]=0xa5;m[0xd127]=5
    for i in range(300):
        if m[0xd057]:break
        p.tick()
    for i in range(60):
        if 'FIGHT' in clean(' '.join(txt())):break
        press_('a',30)
    T(20);print('battle pal',[hex(x) for x in pal()])
    ok(m[0xd057]!=0 and pal()[0]==0xe4,'in battle the palette is the normal one')
    for i in range(12):                                                   # leave the battle (RUN; a wild one may refuse: retry)
        if m[0xd057]==0:break
        p.button('down',8);T(10);p.button('right',8);T(10);p.button('a',8);T(120)
    T(200);print('after battle pal',[hex(x) for x in pal()],'in battle',m[0xd057])
    ok(m[0xd057]==0 and pal()==INV,'back in the overworld after the battle: inverted again')
elif MODE=='normal':
    load('pallet_with_ghost');T(20)
    p.button('start',8);T(40);pick('POK');press_('a',90);m[0xcc26]=0;T(4);press_('a',90);sub=' '.join(txt())
    print(sub[:160])
    ok('GHOST WALK' not in sub,'GHOST (not BLACK) has no GHOST WALK entry')
    for k in range(4):press_('b',40)
    ok(m[0xd878]==0 and pal()==NORM,'palette normal, flag off')
    random.seed(3);load('pallet_with_ghost');m[0xd455]=255;to_route1();hit=False
    for step in range(600):
        m[0xd455]=255;walk_in(0x0c,random.choice(['up','down','left','right']))
        if m[0xd057]:hit=True;break
    ok(hit,'wild encounters happen as usual')
print('t89 done',flush=True)
