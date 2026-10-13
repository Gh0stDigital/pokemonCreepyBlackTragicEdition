# v40: BANE on the map. Modes (Pallet Town as BLACK; t36's helpers):
#  bane     - NO: the usual dialogue; YES ("BANE them?"): black screen, the NPC is a black POKe BALL (sprite 47, drawn),
#             the kill list holds (map, sprite|80), a ball waits (D722); talking to the ball: an uncaught POKeMON (Lv5,
#             no badges) joins the party, the ball is gone; after leaving and coming back the NPC stays gone (no
#             gravestone), the spared NPC is still there
#  persist  - leave the map before picking the ball up: it is still there after coming back and can be picked up
#  overflow - three BANEs: the third one collects the oldest ball at once (party grows), two balls wait
#  trainer  - talking to a trainer as BLACK starts its battle (no BANE question)
import sys
MY=sys.argv[1]
sys.argv=['x','none'];exec(open('t36_v28.py').read().split("if MODE=='panic':")[0]);MODE=MY
PEND=0xd722
def pending():return [(m[PEND+3*i],m[PEND+3*i+1],m[PEND+3*i+2]) for i in range(2) if m[PEND+3*i+2]]
def party():return list(m[0xd164:0xd164+m[0xd163]])
def drawn(i):return m[0xc102+16*i]!=0xff
DEX=open(os.environ['CB_ROM'],'rb').read()[0x4102e:0x4102e+0xbe]
def owned(sp):d=DEX[sp-1];return bool(m[0xd2f7+(d-1)//8]&(1<<((d-1)&7)))
def bane(idx):
    owned_before=list(m[0xd2f7:0xd30a]);t=talk(idx,answers=['yes']);T(60);return t
if MODE=='bane':
    start()
    ns=[n for n in npcs() if n[1] in (0xd,0x2f) and n[4]==0];a,b=ns[0],ns[1];p0=party()
    t=talk(a[0],answers=['no'])
    ok(('METAMORPHOSIS?' if VERSION>=47 else 'BANE them?') in t and 'CURSE' not in t,'the panicking NPC is asked "BANE them?"')
    ok(killed()==[] and pic(a[0])!=0x47,'NO: nothing happens to them (the usual dialogue)')
    t=bane(b[0]);shot('v40_ball');print(t[-120:])
    pd=pending();print('pending',pd,'kill list',killed(),'pic',hex(pic(b[0])),'drawn',drawn(b[0]))
    ok('black ball' in t,'YES: "Only a black ball remains..."')
    ok(pic(b[0])==0x47 and drawn(b[0]),'the NPC is a black POKe BALL on the ground (sprite 47, drawn)')
    ok(killed()==[(0,b[0]|0x80)],'kill list: (map 0, sprite %d | 80) = BANEd'%b[0])
    ok(len(pd)==1 and pd[0][:2]==(0,b[0]) and not owned(pd[0][2]),'a ball waits: species %s, not caught before'%hex(pd[0][2]))
    sp=pd[0][2]
    t=talk(b[0]);T(60);print(t[-120:])
    pt=party()
    ok(pt==p0+[sp] and 'joined your party' in t,'picking the ball up: %s joins the party'%hex(sp))
    ok(m[0xd16b+44*(len(pt)-1)+33]==5,'Lv5 (no badges)')
    ok(not pending() and not drawn(b[0]),'the ball is gone')
    go_map(0x25,0);go_map(0,0);T(60);freeze()
    try:spot(b[0])
    except AssertionError:pass
    T(30);print('back: player',pos(),'NPC',(m[0xc204+16*b[0]]-4,m[0xc205+16*b[0]]-4),'pic',hex(pic(b[0])),'drawn',drawn(b[0]))
    ok(not drawn(b[0]) and pic(b[0])!=0x49 and abs(m[0xc204+16*b[0]]-4-pos()[2])+abs(m[0xc205+16*b[0]]-4-pos()[1])<=2,'after coming back: the BANEd NPC is gone (no gravestone), checked standing next to its spot')
    spot(a[0]);T(30)
    ok(drawn(a[0]) and pic(a[0]) not in (0x47,0x49),'the spared NPC is still there')
elif MODE=='persist':
    start()
    ns=[n for n in npcs() if n[1] in (0xd,0x2f) and n[4]==0];b=ns[1];p0=party()
    bane(b[0]);sp=pending()[0][2]
    go_map(0x25,0);go_map(0,0);T(60);freeze();spot(b[0]);T(30)
    ok(pic(b[0])==0x47 and drawn(b[0]) and pending(),'after leaving and coming back the black ball is still there (drawn)')
    t=talk(b[0]);T(60)
    ok(party()==p0+[sp] and not pending(),'and can be picked up (%s joins)'%hex(sp))
elif MODE=='overflow':
    start()
    m[PEND:PEND+6]=[0x25,9,0x99,0x25,10,0x24]          # two balls already wait (elsewhere): KRABBY, PIDGEY
    ns=[n for n in npcs() if n[1] in (0xd,0x2f) and n[4]==0];b=ns[1];p0=party()
    t=bane(b[0]);pd=pending();print('pending',pd,'party',[hex(x) for x in party()],t[-120:])
    ok(party()==p0+[0x99] and 'joined your party' in t,'a third BANE collects the oldest waiting ball at once (KRABBY joins)')
    ok(pd==[(0x25,10,0x24),(0,b[0],pd[1][2])],'two balls wait: the second old one and the new one')
elif MODE=='trainer':
    warp(0x33,0,black=True)
    tr=[n for n in npcs() if n[4]>=0xc8][0];idx=tr[0]
    m[0xc200+16*idx+4]=m[0xd361]+5;m[0xc200+16*idx+5]=m[0xd362]+4;m[0xc200+16*idx+6]=0xff
    m[0xc100+16*idx+4]=m[0xc104]+16;m[0xc100+16*idx+6]=m[0xc106]
    T(30);seen.clear();p.button('down',8);T(30);press_('a',200)
    for i in range(15):
        if m[0xd057]:break
        press_('a',120)
    ok(m[0xd057]==2 and 'BANE them' not in allt() and 'METAMORPHOSIS?' not in allt(),'talking to a trainer as BLACK starts its battle (no BANE question)')
