# v41: CONSUME. Modes (pallet_with_ghost made BLACK: BLACK + CHARMANDER):
#  consume - BLACK's party submenu offers CONSUME; CHARMANDER -> "Take which move?" -> SCRATCH: "BLACK learned SCRATCH!",
#            "BLACK consumed CHARMANDER!", CHARMANDER is gone, BLACK has its experience and level 5 (stats at 5 + 9)
#  full    - BLACK knows 4 moves: LearnMove asks which to forget; BANE can't be forgotten; a non-BANE move is replaced
#  refuse  - PRETA can't be consumed; cancelling the move choice (B) keeps everything as it was
#  normal  - CHARMANDER's submenu has no CONSUME; PRETA's field moves (CUT/SURF/STRENGTH) are listed as before
import sys,json,re
MY=sys.argv[1]
import os as _os,re as _re
if int(_re.search(r'_v(\d+)',_os.environ.get('CB_ROM','')).group(1))>=47:
    print('SKIP CONSUME was replaced by the party-menu CURSE in v47 (t55_v47.py curse)');sys.exit(0)
sys.argv=['x','none'];exec(open('t46_v38.py').read().split("if MODE in ('join','owned'):")[0]);MODE=MY
B=0xd16b
def stats(i):b=B+44*i;return [m[b+34+2*j]<<8|m[b+35+2*j] for j in range(5)]
def moves(i):b=B+44*i;return list(m[b+8:b+12])
def calc(base,L):return [((base[0]+15)*2*L)//100+L+10]+[((x+15)*2*L)//100+5 for x in base[1:]]
def choose(slot):
    m[0xcc26]=slot;T(4);press_('a',90)
def wait_for(word,n=8):
    for k in range(n):
        if word in ' '.join(txt()):return True
        press_('a',60)
    return False
def submenu(slot):
    p.button('start',8);T(40);pick('POK');press_('a',90)
    choose(slot);return ' '.join(txt())
def consume(victim_slot,move_slot=0,cancel=False,forget=None):
    seen.clear();submenu(0);pick('CONSUME');press_('a',90)
    wait_for('Choose');choose(victim_slot)
    if not wait_for('Take which',5):
        for k in range(6):press_('a',60)
        for k in range(6):press_('b',30)
        return allt()
    T(30)
    for k in range(6):                                  # the move menu (cursor on the first move)
        if any(('▲' in l or '▶' in l) and any(w in l for w in ('SCRATCH','GROWL','TACKLE','CUT')) for l in txt()):break
        press_('a',60)
    if cancel:
        press_('b',120)
        for k in range(6):press_('b',40)
        return allt()
    choose(move_slot)
    fl=list(forget or [])
    for k in range(40):
        t=' '.join(txt())
        if fl and 'YES' in t and 'NO' in t and 'forgotten' not in allt():press_('a',90);continue   # delete an older move? YES
        if fl and 'forgotten' in allt() and ('▶' in t or '▲' in t) and 'SCRATCH' not in t.split('forgotten')[-1][:0]:
            if any(x in t for x in ('BANE','TACKLE','GROWL','LEER')) and ('learn' not in t.lower()):
                choose(fl.pop(0));continue
        press_('a',70)
    for k in range(6):press_('b',30)
    return allt()
if MODE=='consume':
    load('pallet_with_ghost');make_black();T(30);c_exp=exp(1)
    t=submenu(0);print('BLACK submenu:',re.sub(r'\s+',' ',t)[-80:])
    ok('CONSUME' in t,'BLACK\'s party submenu offers CONSUME')
    for k in range(6):press_('b',30)
    t=consume(1,0)
    print('party',[hex(x) for x in party()],'lv',m[B+33],'exp',exp(0),'moves',[hex(x) for x in moves(0)],'stats',stats(0))
    ok('Take which move' in t,'"Take which move?"')
    ok('learned SCRATCH' in t and moves(0)[:2]==[0xaa,0x0a],'BLACK learned SCRATCH (BANE kept)')
    ok('consumed CHARMANDER' in t and party()==[BLK],'"BLACK consumed CHARMANDER!": it is gone')
    ok(exp(0)==1+c_exp and m[B+33]==5 and 'level 5' in t,'BLACK has CHARMANDER\'s experience (%d) and grew to level 5'%exp(0))
    ok(stats(0)==calc([100,110,100,110,160],14),'stats computed at level 5 + 9: %s'%stats(0))
elif MODE=='full':
    load('pallet_with_ghost');make_black();T(30)
    m[B+8:B+12]=[0xaa,0x21,0x2d,0x2b];m[B+29:B+33]=[10,35,40,30]       # BANE, TACKLE, GROWL, LEER
    t=consume(1,0,forget=[0,1])                                         # try BANE first, then TACKLE
    print(t[-300:]);print('moves',[hex(x) for x in moves(0)],'party',[hex(x) for x in party()])
    ok('techniques' in t or 'deleted' in t,'BANE can\'t be forgotten ("HM techniques can\'t be deleted!")')
    ok(moves(0)==[0xaa,0x0a,0x2d,0x2b] and party()==[BLK],'TACKLE forgotten, SCRATCH learned, CHARMANDER consumed')
elif MODE=='refuse':
    load('pallet_with_ghost');make_black()
    SP=fo(0x2d,int(L['s_preta'],16));n=m[0xd163];m[0xd164+n]=PRETA;m[0xd164+n+1]=0xff;m[0xd163]=n+1
    m[B+44*n:B+44*n+44]=list(ROM[SP:SP+44]);m[0xd2b5+11*n:0xd2b5+11*n+11]=[0x8f,0x91,0x84,0x93,0x80]+[0x50]*6;T(30)
    p0=party();e0=exp(0)
    t=consume(2,0);print('PRETA:',t[-120:],[hex(x) for x in party()])
    ok('consume that' in t and party()==p0,'PRETA can\'t be consumed ("BLACK can\'t consume that.")')
    t=consume(1,cancel=True);print('cancel:',t[-120:],[hex(x) for x in party()])
    if VERSION>=46:                                                     # v46: taking a move is optional
        ok(party()==[BLK,PRETA] and exp(0)>e0 and moves(0)[1]==0 and 'consumed' in t,'B at the move choice: CHARMANDER consumed anyway, no move taken')
    else:ok(party()==p0 and exp(0)==e0 and moves(0)[1]==0,'cancelling the move choice keeps everything as it was')
elif MODE=='normal':
    load('pallet_with_ghost');make_black()
    SP=fo(0x2d,int(L['s_preta'],16));n=m[0xd163];m[0xd164+n]=PRETA;m[0xd164+n+1]=0xff;m[0xd163]=n+1
    m[B+44*n:B+44*n+44]=list(ROM[SP:SP+44]);m[0xd2b5+11*n:0xd2b5+11*n+11]=[0x8f,0x91,0x84,0x93,0x80]+[0x50]*6;T(30)
    t=submenu(1);print('CHARMANDER:',re.sub(r'\s+',' ',t)[-60:])
    ok('CONSUME' not in t and 'STATS' in t,'CHARMANDER\'s submenu: no CONSUME')
    for k in range(6):press_('b',30)
    t=submenu(2);print('PRETA:',re.sub(r'\s+',' ',t)[-90:])
    ok('CUT' in t and 'SURF' in t and 'STRENGTH' in t and 'CONSUME' not in t,'PRETA\'s field moves are listed as before')
