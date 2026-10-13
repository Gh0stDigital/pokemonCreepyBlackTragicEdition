# v39: BANE in battle. Modes:
#  wild     - BLACK uses BANE on a wild RATTATA: "BLACK used BANE!", black screen, the black POKe BALL in the enemy
#             picture, RATTATA joins (nickname RATTATA, the wild one's DVs), the battle ends
#  wildbox  - party full: the RATTATA goes to the PC box
#  immune   - BANE on a wild GHOST does nothing (party unchanged, battle goes on); CHARMANDER's SCRATCH as before
#  trainer  - Viridian Forest trainer: BANE takes each of its POKeMON (they count as fainted), then the trainer phase
#             starts with BLACK out; BANE on the trainer: it dies (kill bit) and becomes a POKeMON not caught yet, which
#             joins the party ("The trainer became ...!")
#  migrate  - a v38 BLACK (knows CURSE) knows BANE after one step
from harness import *
import sys,io,json
from collections import deque
MY=sys.argv[1]
sys.argv=['x','none'];exec(open('t46_v38.py').read().split("if MODE in ('join','owned'):")[0]);MODE=MY
L39=json.load(open('manifest_v39.json'))['labels']
BANE=0xaa
def vram_ball():
    v=bytes(m[a] for a in range(0x9000,0x9310))
    dark=sum(bin(b).count('1') for b in v[16*(3*7+4):16*(3*7+6)])    # tiles in the middle column, rows 4-5
    return dark
def fight_bane(limit=600,watch=True):
    """pick FIGHT / first move (BANE) whenever the menu shows; A through texts"""
    best=0
    for i in range(limit):
        if m[0xd057]==0:return best
        t=clean(' '.join(txt()))
        if 'FIGHT' in t and 'RUN' in t:
            for k in range(4):
                if '▶FIGHT' in t.replace(' ','') or '▲FIGHT' in t.replace(' ',''):break
                press_('up',20);press_('left',20);t=clean(' '.join(txt()))
            press_('a',60)
            for k in range(4):press_('up',10)
            press_('a',20)
            for k in range(60):
                T(4);best=max(best,vram_ball())
            continue
        if 'Bring out' in t or 'change' in t.lower():press_('b',60);continue
        press_('a',60)
    return best
def wild(species,setup=None,lv=5):
    load('pallet_with_ghost');make_black()
    if setup:setup()
    m[0xd059]=species;m[0xd127]=lv
    for i in range(300):
        if m[0xd057]:break
        p.tick()
    seen.clear();best=fight_bane(300);T(60)
    return best
def nick(i):return ''.join(cm.get(v,'') for v in m[0xd2b5+11*i:0xd2b5+11*i+10]).split('@')[0]
def owned(dex):return bool(m[0xd2f7+(dex-1)//8]&(1<<((dex-1)&7)))

if MODE=='wild':
    best=wild(0xa5);pt=party();t=allt()
    print('party',[hex(x) for x in pt],'nicks',[nick(i) for i in range(len(pt))],'ball pixels',best,'in battle',m[0xd057])
    ok(('BLACK used BANE' in t or (VERSION>=47 and 'METAMORPHOSIS' in t)) and 'joined your party' in t,'"BLACK used BANE!" / "RATTATA joined your party."')
    ok(best>40,'the black POKe BALL stands in the enemy picture (%d dark pixels)'%best)
    ok(pt==[BLK,CHAR,0xa5] and nick(2)=='RATTATA' and m[0xd057]==0,'RATTATA joined (nickname RATTATA) and the battle is over')
    b=0xd16b+44*2;ok(m[b+33]==5 and (m[b+12],m[b+13])==(m[0xd359],m[0xd35a]),'it is Lv5 with the player\'s OT')
elif MODE=='wildbox':
    def full():
        for i in range(2,6):
            n=m[0xd163];m[0xd164+n]=CHAR;m[0xd164+n+1]=0xff;m[0xd163]=n+1
            m[0xd16b+44*n:0xd16b+44*n+44]=list(m[0xd16b+44:0xd16b+88]);m[0xd2b5+11*n:0xd2b5+11*n+11]=list(m[0xd2b5+11:0xd2b5+22])
    b0=None
    def s():
        full();global b0;b0=m[0xda80]
    wild(0xa5,s);t=allt()
    print('party',len(party()),'box',b0,'->',m[0xda80],[hex(m[0xda81+i]) for i in range(m[0xda80])],t[-80:])
    ok(len(party())==6 and m[0xda80]==b0+1 and m[0xda81+m[0xda80]-1]==0xa5 and 'sent to the PC' in t,'party full: RATTATA goes to the PC box')
    ok(owned(19),'RATTATA is registered as owned')
elif MODE=='immune':
    load('pallet_with_ghost');make_black();m[0xd059]=0x1f;m[0xd127]=5
    for i in range(300):
        if m[0xd057]:break
        p.tick()
    seen.clear()
    for i in range(80):
        t=clean(' '.join(txt()))
        if 'FIGHT' in t and 'RUN' in t:
            press_('a',60);press_('a',300);break
        press_('a',60)
    for i in range(10):press_('a',60)
    print('party',[hex(x) for x in party()],'in battle',m[0xd057],allt()[-100:])
    ok(party()==[BLK,CHAR] and m[0xd057],'BANE on a wild GHOST does nothing: party unchanged, the battle goes on')
    load('pallet_with_ghost');lead(CHAR);m[0xd16b+8]=0x0a;m[0xd16b+29]=0x3f;m[0xd059]=0xa5;m[0xd127]=5
    for i in range(300):
        if m[0xd057]:break
        p.tick()
    h0=None;seen.clear()
    for i in range(200):
        if m[0xd057]==0:break
        t=clean(' '.join(txt()))
        if 'FIGHT' in t and 'RUN' in t:
            if h0 is not None:break
            h0=m[0xcfe6]<<8|m[0xcfe7];press_('a',60);press_('a',300);continue
        press_('a',60)
    h1=m[0xcfe6]<<8|m[0xcfe7];print('CHARMANDER SCRATCH: enemy HP',h0,'->',h1,'party',[hex(x) for x in party()])
    ok(h1<h0 and 0xa5 not in party(),'CHARMANDER\'s SCRATCH works as before (normal case)')
elif MODE=='trainer':
    T39=json.load(open('manifest_v29.json'))['trainer_maps']
    warp(0x33,0,make_black)
    R=open(os.environ['CB_ROM'],'rb').read()
    def off(k):b,a=k.split(':');b=int(b,16);a=int(a,16);return b*0x4000+a-0x4000
    hdrs={k:v for k,v in T39.items() if '0x33' in v}
    sprite_idx={R[off(k)]:(R[off(k)+10]|R[off(k)+11]<<8) for k in hdrs}
    tr=[i for i in range(1,m[0xd4e1]+1) if m[0xd504+2*(i-1)]>=0xc8 and i in sprite_idx]
    idx=tr[0];want=sprite_idx[idx];owned_before=list(m[0xd2f7:0xd30a])
    print('trainer sprite',idx,'kill index',want)
    m[0xc200+16*idx+4]=m[0xd361]+5;m[0xc200+16*idx+5]=m[0xd362]+4;m[0xc200+16*idx+6]=0xff
    m[0xc100+16*idx+4]=m[0xc104]+16;m[0xc100+16*idx+6]=m[0xc106]
    T(30);press_('down',20);press_('a',300)
    for i in range(15):
        if m[0xd057]:break
        press_('a',120)
    ok(m[0xd057]==2,'trainer battle started')
    enemy=[m[0xd89d+i] for i in range(m[0xd89c])];p0=party();seen.clear()
    phase=[False]
    for i in range(900):
        if m[0xd05a]==3:phase[0]=True
        if m[0xd057]==0 and i>20:break
        t=clean(' '.join(txt()))
        if 'FIGHT' in t and 'RUN' in t:
            for k in range(4):
                if '▶FIGHT' in t.replace(' ','') or '▲FIGHT' in t.replace(' ',''):break
                press_('up',20);press_('left',20);t=clean(' '.join(txt()))
            press_('a',60)
            for k in range(4):press_('up',10)
            press_('a',300);continue
        if 'Bring out' in t or 'change' in t.lower():press_('b',60);continue
        press_('a',90)
    T(300);pt=party();new=pt[len(p0):];t=allt()
    print('enemy party',[hex(x) for x in enemy],'new members',[hex(x) for x in new],'phase',phase[0],'nicks',[nick(i) for i in range(len(pt))])
    ok(new[:len(enemy)]==enemy,'BANE took each of the trainer\'s POKeMON (%s)'%[hex(x) for x in enemy])
    ok(phase[0] and 'The trainer became' in t,'the trainer phase started with BLACK out; "The trainer became ...!"')
    def bitset(i):
        base=0xd430 if i>=0x100 else 0xd4a4;j=i&0xff
        return bool(m[base+j//8]&(1<<(j&7)))
    ok(bitset(want),'the trainer died (kill bit %d)'%want)
    ok(len(new)==len(enemy)+1,'the trainer became a POKeMON that joined the party (%s)'%hex(new[-1]))
    DEX=open(os.environ['CB_ROM'],'rb').read()[0x4102e:0x4102e+0xbe];dx=DEX[new[-1]-1]
    was=bool(owned_before[(dx-1)//8]&(1<<((dx-1)&7)))
    ok(1<=dx<=151 and not was,'...one not caught before (dex %d)'%dx)
elif MODE=='migrate':
    load('pallet_with_ghost');make_black();m[0xd16b+8]=0xa5;m[0xd16b+29]=5;T(20)
    p.button('up',8);T(30);p.button('down',8);T(30)
    print('moves',[hex(x) for x in m[0xd16b+8:0xd16b+12]],'pp',m[0xd16b+29])
    ok(m[0xd16b+8]==BANE and m[0xd16b+29]==10,'a v38 BLACK (CURSE) knows BANE after a step')
