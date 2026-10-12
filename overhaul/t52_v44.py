# v44: the POKeMON LEAGUE as BLACK (LORELEI / BRUNO / LANCE, AGATHA's room). Modes:
#  block   - LORELEI, BLACK out: BANE is refused (a flash, "A strange power blocks the move BANE!", LORELEI's MOON STONE
#            line), the move menu comes back, no turn passes (both sides' HP unchanged); BRUNO's / LANCE's lines likewise
#  shatter - LORELEI (one POKeMON), a strong CHARMANDER beats it: flash, "The MOON STONE shatters!", BLACK is sent out, the
#            phase starts; RUN, ITEM and SCRATCH -> AGATHA's words, still in the phase; BANE -> LORELEI dies, a POKeMON
#            joins, the way to BRUNO opens
#  agatha  - AGATHA's room as BLACK: nobody there, the way north leads to LANCE's room
#  normal  - not BLACK (GHOST route): GHOST's CURSE is not refused in LORELEI's battle, no MOON STONE text; AGATHA is
#            in her room
import sys
MY52=sys.argv[1]
sys.argv=['x','none'];exec(open('t46_v38.py').read().split("if MODE in ('join','owned'):")[0]);MODE=MY52
CHAR=0xb0
_mb=make_black
def make_black():
    _mb();m[0xd16b+29]=20                                  # BANE with PP
def strong(i):
    b=0xd16b+44*i
    m[b+14]=0x10;m[b+15]=0x2c;m[b+16]=0x14;m[b+33]=100;m[b+3]=100;m[b+1]=3;m[b+2]=0xe7;m[b+34]=3;m[b+35]=0xe7
    for j in range(4):m[b+36+2*j]=3;m[b+37+2*j]=0xe7
def ehp():return m[0xcfe6]<<8|m[0xcfe7]
def php():return m[0xd015]<<8|m[0xd016]
def to_battle(mapid,y,x,setup,one=False):
    if y is None:                                 # LANCE: arrive through his north door, right above him
        warp(mapid,2,setup);face='down'
    else:warp(mapid,0,setup);bfs_to(y,x);face='up'
    press_(face,20);seen.clear();press_('a',200)
    for i in range(20):
        if m[0xd057]:break
        press_('a',120)
    if one:m[0xd89c]=1
    wait_menu()
def wait_menu(n=40):
    for i in range(n):
        t=clean(' '.join(txt()))
        if 'FIGHT' in t and 'RUN' in t:return True
        if 'change' in t.lower():press_('b',60);continue
        press_('a',80)
    return False
def menu(item):                                   # 'fight' / 'item' / 'run' in the battle menu
    press_('up',12);press_('left',12)
    if item=='item':press_('down',12)
    if item=='run':press_('down',12);press_('right',12)
    press_('a',90)
def use_move(slot,frames=400,in_moves=False):
    if not in_moves:menu('fight')
    for k in range(20):
        tt=txt()
        if any(('▲' in x or '▶' in x) for x in tt) and not any('FIGHT' in x for x in tt):break
        press_('a',60)
    m[0xcc26]=slot+1;T(4);seen.clear();lo=255
    p.button('a',8)
    for k in range(frames):
        p.tick();lo=min(lo,p.memory[0xff47])
        if k%4==0:T(1)
    return lo
def read_until_menu(n=12):
    for i in range(n):
        t=clean(' '.join(txt()))
        if ('FIGHT' in t and 'RUN' in t) or 'BANE' in t and '▶' in ''.join(txt()):return
        press_('a',70)
if MODE=='block':
    for mapid,cls,name in ((0xf5,0x2c,'LORELEI'),(0xf6,0x21,'BRUNO'),(0x71,0x2f,'LANCE')):
        yx={0xf5:(3,5),0xf6:(3,5),0x71:(None,None)}[mapid]
        to_battle(mapid,yx[0],yx[1],make_black)
        ok(m[0xd031]==cls and m[0xd014]==BLK,'%s battle, BLACK out'%name)
        e0,p0=ehp(),php()
        lo=use_move(0,300);read_until_menu();t=allt()
        print(name,'flash min BGP',hex(lo),'|',t[-260:])
        ok(lo==0,'%s: a light flashes (BGP white)'%name)
        ok('strange power' in t and 'BANE!' in t,'%s: "A strange power blocks the move BANE!"'%name)
        ok('MOON STONE' in t and name in t,'%s comments on the MOON STONE'%name)
        ok(m[0xd057]==2 and ehp()==e0 and php()==p0 and m[0xd05a]!=3,'no turn passed (HP unchanged), still fighting')
        if mapid==0xf5:
            for mv,nm in ((0xa9,'MACABRE'),(0xa8,'BLACK FLAME')):    # PRETA's / AZHI's death moves are blocked too
                m[0xd01e]=mv;m[0xd02f]=10;seen.clear();use_move(2,300,in_moves=True);read_until_menu()
                if nm=='BLACK FLAME':shot('v44_block')
                for k in range(8):
                    if 'here!' in allt():break
                    press_('a',70)
                ok('strange power' in allt() and nm+'!' in allt() and ehp()==e0,'%s is blocked too'%nm)
            m[0xd16b+9]=0x0a;m[0xd01d]=0x0a;m[0xd02e]=35        # SCRATCH (a normal move) is still allowed
            use_move(1,400,in_moves=True)
            for k in range(12):
                if ehp()<e0:break
                press_('a',70)
            ok(ehp()<e0 and 'strange power' not in allt(),'a normal move (SCRATCH) works as before')
elif MODE=='shatter':
    def setup():
        make_black();lead(CHAR);strong(0)
        b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35                     # BLACK: BANE + SCRATCH
    to_battle(0xf5,3,5,setup,one=True)
    ok(m[0xd014]==CHAR,'CHARMANDER fights LORELEI (BLACK is in the party)')
    menu('fight');m[0xcc26]=1;T(4);seen.clear();p.button('a',8);lo=255
    for k in range(2500):
        p.tick();lo=min(lo,p.memory[0xff47])
        if k%4==0:T(1)
        if m[0xd05a]==3 and 'FIGHT' in clean(' '.join(txt())):break
        if k%90==0:p.button('a',8)
    t=allt();print('to phase:',t[-400:]);shot('v44_black_out')
    ok('MOON STONE' in t and 'shatters' in t and lo==0,'flash + "The MOON STONE shatters!"')
    ok(m[0xd014]==BLK and m[0xd05a]==3,'BLACK was sent out, the after-win phase began')
    ok(m[0xcfd9]==BLK,"BLACK's own back picture (wBattleMonSpecies2 = BLACK)")
    ok('come back' in t.lower() or 'enough' in t.lower() or 'Go!' in t or 'BLACK' in t,'CHARMANDER called back, BLACK sent out')
    for what in ('run','item'):
        seen.clear();menu(what);read_until_menu();t=allt()
        print(what,':',t[-600:])
        i=t.find('AGATHA');print('  ...',t[i:i+60] if i>=0 else 'no AGATHA')
        ok('AGATHA' in t and 'echo within you' in t and 'destroy' in t and 'them all' in t and 'intruders' in t,'%s -> AGATHA\'s words echo'%what.upper())
        ok(m[0xd057]==2 and m[0xd05a]==3,'still in the phase after %s'%what.upper())
    seen.clear();use_move(1,300);read_until_menu();t=allt();print('scratch:',t[-150:])
    ok('AGATHA' in t and 'intruders' in t and m[0xd05a]==3,'SCRATCH -> AGATHA\'s words, still in the phase')
    p0=party();seen.clear();use_move(0,300,in_moves=True)
    for i in range(30):
        if m[0xd057]==0:break
        press_('a',100)
    for i in range(8):press_('a',60)
    T(200);t=allt();print('bane:',t[-200:])
    ok(m[0xd057]==0 and len(party())==len(p0)+1 and 'became' in t,'BANE: LORELEI dies, a POKeMON joins (%s)'%hex(party()[-1]))
    ok(m[0xd863]&2 and m[0xc102+16]==0xff,'LORELEI is gone and her room counts as beaten')
    bfs_to(0,4,maxn=400)
    for k in range(4):p.button('up',8);T(40)
    ok(m[0xd35e]==0xf6,'the way to BRUNO is open')
elif MODE=='agatha':
    warp(0xf7,0,make_black);T(60)
    ok(m[0xc110]==0 and m[0xd865]&2,"AGATHA's room is empty (her flag counts as beaten)")
    bfs_to(0,4,maxn=400)
    for k in range(4):p.button('up',8);T(40)
    ok(m[0xd35e]==0x71,"the way north leads to LANCE's room")
elif MODE=='normal':
    def setup():lead(GHOST)
    to_battle(0xf5,3,5,setup)
    ok(m[0xd014]==GHOST and m[0xd46c]==0,'not BLACK: GHOST fights LORELEI')
    mv=list(m[0xd01c:0xd020]);i=mv.index(0xa5) if 0xa5 in mv else None
    ok(i is not None,'GHOST knows CURSE')
    lo=use_move(i,500);read_until_menu();t=allt();print('normal:',t[-200:])
    ok('strange power' not in t and 'MOON STONE' not in t and 'CURSE' in t,'CURSE is used as before (no MOON STONE)')
    warp(0xf7,0);T(60)
    ok(m[0xc110]!=0 and not m[0xd865]&2,'AGATHA is in her room as before')
