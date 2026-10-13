# v49: what BLACK is. Modes:
#  scared   - BLACK out (wild RATTATA): the RATTATA is "too scared to move", BLACK keeps its HP;
#             normal: with CHARMANDER out the RATTATA attacks as before
#  moon     - LORELEI (MOON STONE): her DEWGONG still attacks BLACK
#  status   - PRETA out, the wild POKeMON only knows SPORE / THUNDER WAVE / CONFUSE RAY / TOXIC: "It doesn't affect PRETA!",
#             no status; FIRE BLAST can still burn PRETA; normal: CHARMANDER falls asleep from SPORE
#  bstatus  - LORELEI's DEWGONG with SPORE and FIRE BLAST: BLACK is never asleep nor burned
#  tower    - as BLACK no random encounter in POKeMON TOWER 3F (150 steps); not BLACK: encounters happen there
#  services - as BLACK: nurse, mart, prize vendor, coin clerk, bike shop, MAGIKARP salesman, DAY CARE, NAME RATER, a trade,
#             the fossil scientist: all "shaking", no service; not BLACK: the nurse, the mart and the trade work as before
import sys,json
MY57=sys.argv[1]
if MY57 in ('tower','services'):
    sys.argv=['x','none'];exec(open('t36_v28.py').read().split("if MODE=='panic':")[0]);MODE=MY57
else:
    sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY57
from patchlib import enc
SPORE,TWAVE,CRAY,TOXIC,FIREBLAST=0x93,0x56,0x6d,0x5c,0x7e
def start_wild(setup,species=0xa5,lv=5):
    load('pallet_with_ghost');setup();m[0xd059]=species;m[0xd127]=lv
    for i in range(300):
        if m[0xd057]:break
        p.tick()
    wait_menu();T(20)
def lead_struct(struct):
    make_black();m[0xd16b:0xd16b+44]=list(struct);m[0xd164]=struct[0];m[0xd16b+12]=m[0xd359];m[0xd16b+13]=m[0xd35a]
    m[0xd2b5:0xd2b5+11]=list(enc('PRETA'))+[0x50]*6 if struct[0]==0xb6 else m[0xd2b5:0xd2b5+11]
def enemy_moves(mv):
    m[0xcfed:0xcff1]=[mv]*4;m[0xcffe:0xd002]=[30]*4
def turn(slot):
    seen.clear();use_move(slot,300)
    for k in range(12):
        tt=clean(' '.join(txt()))
        if ('FIGHT' in tt and 'RUN' in tt) or m[0xd057]==0:break
        press_('a',60)
    return allt()
if MODE=='scared':
    start_wild(make_black);h0=php();t=turn(2);print(t[-200:])
    ok('scared to move' in t and php()==h0,'BLACK out: the wild RATTATA is too scared to move (BLACK HP %d)'%php())
    start_wild(lambda:lead(CHAR));h0=php();t=turn(0);print(t[-200:])
    ok('scared' not in t and 'RATTATA used' in t.replace('  ',' '),'normal: with CHARMANDER out the RATTATA attacks')
elif MODE=='moon':
    to_battle(0xf5,3,5,make_black);ok(m[0xd031]==0x2c and m[0xd014]==BLK,'LORELEI, BLACK out')
    t=turn(2);t+=turn(2);print(t[-250:])
    ok('scared' not in t and 'DEWGONG used' in t.replace('  ',' '),'the MOON STONE\'s DEWGONG still attacks BLACK')
elif MODE=='status':
    SPR=ROM[SP:SP+44]
    for mv,name in ((SPORE,'SPORE'),(TWAVE,'THUNDER WAVE'),(CRAY,'CONFUSE RAY'),(TOXIC,'TOXIC')):
        start_wild(lambda:lead_struct(SPR),lv=30);enemy_moves(mv);t=turn(0)    # PRETA uses MACABRE (target left at 1 HP)
        print(name,t[-160:],'status',m[0xd018],'conf',m[0xd062]&0x80)
        ok(m[0xd014]==0xb6 and 'affect' in t and m[0xd018]==0 and not (m[0xd062]&0x80),'%s on PRETA: "It doesn\'t affect PRETA!", no status'%name)
    start_wild(lambda:lead_struct(SPR),lv=60);burned=False
    for k in range(20):
        enemy_moves(FIREBLAST);turn(0)
        if m[0xd018]&0x10:burned=True;break
        if m[0xd057]==0:start_wild(lambda:lead_struct(SPR),lv=60)
    ok(burned,'FIRE BLAST can still burn PRETA (burn is not blocked)')
    start_wild(lambda:lead(CHAR),lv=5);enemy_moves(SPORE);t=turn(1);print(t[-120:])
    ok(m[0xd018]&7 or 'fell asleep' in t.replace('  ',' '),'normal: CHARMANDER falls asleep from SPORE')
elif MODE=='bstatus':
    to_battle(0xf5,3,5,make_black);ok(m[0xd014]==BLK,'LORELEI, BLACK out')
    t=''
    for k in range(4):
        enemy_moves(SPORE);t+=turn(2)
        if 'affect' in t:break
    print(t[-200:])
    ok('affect' in t and m[0xd018]==0,'SPORE on BLACK: "It doesn\'t affect BLACK!"')
    hit=0
    for k in range(10):
        enemy_moves(FIREBLAST);t=turn(2);hit+='FIRE BLAST' in t
        if m[0xd018] or m[0xd057]==0:break
    print('FIRE BLAST turns',hit,'status',m[0xd018])
    ok(hit>=3 and m[0xd018]==0,'%d FIRE BLASTs: BLACK is never burned'%hit)
elif MODE=='tower':
    def walk_tower(black,n=150):
        warp(0x90,0,black=black);freeze();battles=0           # (wGrassRate D887 left as the map set it)
        if not black:m[0xd46c]=0
        if black:bfs_to(4,10)                          # an open corridor on 3F (not BLACK: a battle comes on the way anyway)
        for i in range(n):
            p.button(('left','right','up','down')[(i//2)%4] if not black else ('left' if i%2 else 'right'),8);T(24)
            if m[0xd057]:battles+=1;break
            if box():press_('b',30)
        return battles
    b=walk_tower(True);print('BLACK battles',b)
    ok(b==0 and m[0xd35e]==0x90,'as BLACK: 150 steps in POKeMON TOWER 3F, no encounter')
    b=walk_tower(False);print('normal battles',b)
    ok(b>0,'not BLACK: an encounter happens there')
elif MODE=='services':
    def refused(t):return 'scared to' in t or 'too much to help' in t
    def party():return list(m[0xd164:0xd164+m[0xd163]]) if m[0xd163] else []
    def text_of(i):return m[0xd4e4+2*(i-1)+1]
    def by_text(t):return [x for x in npcs() if text_of(x[0])==t][0]
    STAND={(0x87,2):(8,5,'up')}                          # the coin clerk is behind the counter: stand two tiles below
    def serve(mapid,tid,black=True,answers=('no','no','no')):
        global p0,money
        warp(mapid,0,black=black);freeze();n=by_text(tid);p0=party();money=list(m[0xd347:0xd34a])
        if (mapid,tid) in STAND:
            y,x,d=STAND[(mapid,tid)];bfs_to(y,x,maxn=3000);p.button(d,8);T(30)
            seen.clear();press_('a',90);ans=list(answers)
            for k in range(14):
                b=clean(' '.join(txt()))
                if 'YES' in b and 'NO' in b and ans:
                    if ans.pop(0)=='no':press_('down',30)
                press_('a',80)
            return allt()
        return talk(n[0],answers=list(answers),n=40)
    for mapid,tid,name in ((0x8d,1,'nurse'),(0x96,1,'mart clerk'),(0x42,1,'BIKE SHOP'),(0x44,4,'MAGIKARP salesman'),
                           (0x48,1,'DAY CARE'),(0xe5,1,'NAME RATER'),(0x30,2,'Route 2 trade'),(0xaa,1,'fossil scientist')):
        t=serve(mapid,tid)
        print(name,'|',t[-160:],'| shaking',(refused(t)),'party',party()==p0,'money',list(m[0xd347:0xd34a])==money)
        ok(refused(t) and party()==p0 and list(m[0xd347:0xd34a])==money,'as BLACK, %s: too scared, nothing happens'%name)
    # prize vendor (a counter sign in the prize room)
    warp(0x89,0);freeze()
    signs=[(m[0xd4b1+2*i],m[0xd4b1+2*i+1],m[0xd4d1+i]) for i in range(m[0xd4b0])]
    sy,sx,_=[s for s in signs if s[2]==3][0];bfs_to(sy+1,sx);p.button('up',8);T(30);seen.clear();press_('a',90)
    for k in range(8):press_('a',60)
    t=allt();print('prize |',t[-150:]);ok(refused(t),'as BLACK, the prize vendor: too scared')
    # not BLACK: the nurse heals, the mart sells, the trade is offered
    t=serve(0x8d,1,black=False,answers=('no',));ok(not refused(t) and 'POK' in t,'not BLACK: the nurse as before: %s'%t[:40])
    t=serve(0x96,1,black=False,answers=());print(t[-100:]);ok('Hi there' in t and not refused(t),'not BLACK: "Hi there! May I help you?"')
    for k in range(6):press_('b',30)
    t=serve(0x30,2,black=False,answers=('no',));print(t[-120:]);ok(not refused(t) and ('trade' in t.lower() or 'want' in t.lower()),'not BLACK: the trade is offered')
