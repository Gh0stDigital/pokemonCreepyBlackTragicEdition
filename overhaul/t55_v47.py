# v47: Black Tamer redux part 1. Modes:
#  meta    - BLACK uses METAMORPHOSIS on a wild RATTATA: "BLACK used METAMORPHOSIS!", THUNDERBOLT's animation plays, then
#            the black ball; RATTATA joins and is marked (struct byte 7 = MARK)
#  back    - a marked CHARMANDER leading a battle: its back picture is pitch black (only white/black pixels);
#            normal: an unmarked CHARMANDER's back picture keeps its grey shades
#  status  - status screen of a marked CHARMANDER: black front picture; normal: shades as before
#  icon    - party menu: the marked POKeMON's icon uses the black palette (OBP1 = FF), the others don't
#  curse   - BLACK's party submenu shows CURSE (no CONSUME): CHARMANDER is eaten at once (no "Take which move?"),
#            BLACK gains its experience, BLACK's moves stay METAMORPHOSIS + CURSE
#  moves   - an older BLACK (BANE + SCRATCH, low PP) has METAMORPHOSIS + CURSE with full PP after one step
#  map     - METAMORPHOSIS on the map: "METAMORPHOSIS?", the ball, picking it up: the new POKeMON is marked
#  bcurse  - BLACK uses CURSE in battle: the wild POKeMON dies, the battle ends
#  normal  - a POKeMON caught/received the usual way (CHARMANDER, PRETA struct) is not marked
import sys,json
MY55=sys.argv[1]
if MY55=='map':
    sys.argv=['x','none'];exec(open('t48_v40.py').read().split("if MODE=='bane':")[0]);MODE=MY55
else:
    sys.argv=['x','none'];exec(open('t47_v39.py').read().split("if MODE=='wild':")[0]);MODE=MY55
MAN=json.load(open('manifest_v47.json'));MARK=MAN['mark']
META,CURSE=0xaa,0xa5
BMOVES=[META,CURSE,0xab,0xac] if VERSION>=48 else [META,CURSE,0,0];BPP=[10,1,15,1] if VERSION>=48 else [10,1,0,0]
def marked(i):return m[0xd16b+44*i+7]==MARK
def colors(addr,n=784):
    c=[0,0,0,0]
    for i in range(0,n,2):
        lo,hi=m[addr+i],m[addr+i+1]
        for b in range(8):c[((hi>>b)&1)<<1|((lo>>b)&1)]+=1
    return c
def battle_with(setup):
    load('pallet_with_ghost');make_black();setup();m[0xd059]=0xa5;m[0xd127]=5;seen.clear()
    for i in range(300):
        if m[0xd057]:break
        p.tick()
    for i in range(60):
        t=clean(' '.join(txt()))
        if 'FIGHT' in t and 'RUN' in t:break
        press_('a',30)
    T(20);return colors(0x9310)
def char_lead(mark):
    def s():
        lead(CHAR)
        if mark:m[0xd16b+7]=MARK
    return s
def status_of(slot):
    p.button('start',8);T(40);pick('POK');press_('a',90)
    m[0xcc26]=slot;T(4);press_('a',90)
    pick('STATS');press_('a',150);T(60)
    return colors(0x9000)
if MODE=='meta':
    anims=[]
    p.hook_register(0x1e,0x4d5e,lambda c:anims.append(m[0xd07c]),None)
    best=wild(0xa5);pt=party();t=allt()
    print('anims',[hex(a) for a in anims],'party',[hex(x) for x in pt],t[-160:])
    ok('METAMORPHOSIS' in t and 'BANE' not in t,'"BLACK used METAMORPHOSIS!"')
    ok(0x55 in anims,"THUNDERBOLT's animation plays")
    ok(best>40,'then the black POKe BALL (%d dark pixels)'%best)
    ok(pt==[BLK,CHAR,0xa5] and marked(2),'RATTATA joined and is marked (byte 7 = %d)'%MARK)
    ok(not marked(0) and not marked(1),'BLACK and CHARMANDER are not marked')
elif MODE=='back':
    c=battle_with(char_lead(True));shot('v47_black_back');print('marked back colours',c,'out',hex(m[0xd014]))
    ok(m[0xd014]==CHAR and c[1]==0 and c[2]==0 and c[3]>150,'a marked CHARMANDER out: pitch-black back picture (%s)'%c)
    c=battle_with(char_lead(False));print('normal back colours',c)
    ok(m[0xd014]==CHAR and c[1]+c[2]>50,'normal: an unmarked CHARMANDER keeps its shades (%s)'%c)
elif MODE=='status':
    load('pallet_with_ghost');make_black();m[0xd16b+44+7]=MARK;T(20)
    c=status_of(1);shot('v47_black_status');print('marked front',c,txt()[:3])
    ok(c[1]==0 and c[2]==0 and c[3]>150,'status screen: marked CHARMANDER is pitch black (%s)'%c)
    load('pallet_with_ghost');make_black();T(20)
    c=status_of(1);print('normal front',c)
    ok(c[1]+c[2]>50,'normal: an unmarked CHARMANDER keeps its shades (%s)'%c)
elif MODE=='icon':
    load('pallet_with_ghost');make_black();m[0xd16b+44+7]=MARK;T(20)
    p.button('start',8);T(40);pick('POK');press_('a',120);T(30);shot('v47_black_icon')
    pal=[[bool(m[0xfe00+4*(4*s+k)+3]&0x10) for k in range(4)] for s in range(2)]
    print('palette bits',pal,'OBP1',hex(m[0xff49]))
    ok(all(pal[1]) and m[0xff49]==0xff,'party menu: the marked CHARMANDER icon is drawn with the black palette')
    ok(not any(pal[0]),'BLACK\'s icon is not')
    for k in range(40):T(4)
    ok(all(m[0xfe00+4*(4+k)+3]&0x10 for k in range(4)),'still black while the icons animate')
elif MODE=='curse':
    load('pallet_with_ghost');make_black();T(20)
    B=0xd16b
    def exp(i):b=B+44*i;return m[b+14]<<16|m[b+15]<<8|m[b+16]
    e0,ec=exp(0),exp(1);seen.clear()
    p.button('start',8);T(40);pick('POK');press_('a',90)
    m[0xcc26]=0;T(4);press_('a',90);sub=' '.join(txt())
    ok('CURSE' in sub and 'CONSUME' not in sub,"BLACK's party submenu offers CURSE (no CONSUME)")
    pick('CURSE');press_('a',90)
    for k in range(8):
        if 'Choose' in ' '.join(txt()):break
        press_('a',60)
    m[0xcc26]=1;T(4);press_('a',90)
    for k in range(8):press_('a',60)
    for k in range(6):press_('b',30)
    t=allt();print(t[-200:],'party',[hex(x) for x in party()],'exp',e0,'->',exp(0))
    ok('Curse which' in t,'"Curse which POKeMON?"')
    ok('Take which' not in t and 'consumed' in t,'no move choice: "BLACK consumed CHARMANDER!"')
    ok(party()==[BLK] and exp(0)==e0+ec,"CHARMANDER is gone, BLACK gained its experience (%d)"%ec)
    ok(list(m[B+8:B+12])==BMOVES,'BLACK still knows METAMORPHOSIS + CURSE (and v48\'s moves)')
elif MODE=='moves':
    load('pallet_with_ghost');make_black();m[0xd16b+8:0xd16b+12]=[META,0x0a,0,0];m[0xd16b+29:0xd16b+33]=[3,5,0,0];T(20)
    p.button('up',8);T(30);p.button('down',8);T(30)
    mv=list(m[0xd16b+8:0xd16b+12]);pp=list(m[0xd16b+29:0xd16b+33]);print('moves',[hex(x) for x in mv],'pp',pp)
    ok(mv==BMOVES and pp==BPP,'after a step BLACK knows METAMORPHOSIS + CURSE with full PP')
    load('pallet_with_ghost');lead(CHAR);T(20);mv0=list(m[0xd16b+8:0xd16b+12])
    p.button('up',8);T(30);p.button('down',8);T(30)
    ok(list(m[0xd16b+8:0xd16b+12])==mv0,'normal: a CHARMANDER\'s moves are untouched')
elif MODE=='map':
    start()
    ns=[n for n in npcs() if n[1] in (0xd,0x2f) and n[4]==0];b=ns[1];p0=party()
    t=talk(b[0],answers=['yes']);T(60);print(t[-120:])
    ok('METAMORPHOSIS?' in t and 'BANE' not in t,'the question is "METAMORPHOSIS?"')
    sp=pending()[0][2];t=talk(b[0]);T(60);pt=party()
    ok(pt==p0+[sp] and m[0xd16b+44*(len(pt)-1)+7]==MARK,'the black ball\'s POKeMON (%s) joins marked'%hex(sp))
elif MODE=='normal':
    load('pallet_with_ghost');T(20)
    ok(not any(marked(i) for i in range(m[0xd163])),'the usual party (GHOST, CHARMANDER) is not marked')
    sp=ROM[SP:SP+44];ok(sp[7]!=MARK,'the PRETA struct is not marked')
elif MODE=='bcurse':                                   # BLACK's CURSE in battle (move 2) kills a wild POKeMON at once
    load('pallet_with_ghost');make_black();m[0xd059]=0xa5;m[0xd127]=5
    for i in range(300):
        if m[0xd057]:break
        p.tick()
    seen.clear();p0=party()
    hps=[]
    for i in range(200):
        hps.append(m[0xcfe6]<<8|m[0xcfe7])
        if m[0xd057]==0:break
        t=clean(' '.join(txt()))
        if 'FIGHT' in t and 'RUN' in t:
            press_('a',60)
            for k in range(5):
                if 'CURSE' in cursor_line():break
                press_('down',10)
            press_('a',300);continue
        press_('a',60)
    t=allt();i=t.find('used CURSE');print(t[i:i+400],'enemy HP',hps[-6:])
    ok('used CURSE' in t and m[0xd057]==0 and party()==p0,"BLACK's CURSE ends the wild battle like GHOST's (the curse kill; nobody joins)")
