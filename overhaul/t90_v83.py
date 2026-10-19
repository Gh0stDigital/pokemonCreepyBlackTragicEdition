# v83: METAMORPHOSIS = CURSE towards trainers; pitch-black pictures are solid. Modes:
#  trainer - BLACK uses METAMORPHOSIS on a trainer's POKeMON (Viridian Forest BUG CATCHER, 2 POKeMON): no "fainted!" text, D452 = 1, the trainer's frightened
#            end-of-battle text ("What have you done!?") instead of the normal defeat line, the POKeMON joined as before; control: CURSE shows the same frightened line
#  holes   - marked POKeMON of 12 species lead a battle: no white pixel of the back picture is enclosed on all four sides by black pixels (v82 had holes / outlines)
#  normal  - a normal win without CURSE/METAMORPHOSIS: the usual defeat text, "Enemy X fainted!" still shown, D452 = 0
import sys,json,os
MY90=sys.argv[1]
sys.argv=['x','none']
exec(open('t47_v39.py').read().split("if MODE=='wild':")[0])
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
exec(open('t52_v44.py').read().split("def menu(item)")[0].split("def make_black")[0]) if False else None
def menu(item):
    press_('up',12);press_('left',12)
    if item=='item':press_('down',12)
    if item=='run':press_('down',12);press_('right',12)
    press_('a',90)
T39=json.load(open('manifest_v29.json'))['trainer_maps']
def trainer_battle():
    warp(0x33,0,make_black)
    R=open(os.environ['CB_ROM'],'rb').read()
    def off(k):b,a=k.split(':');b=int(b,16);a=int(a,16);return b*0x4000+a-0x4000
    hdrs={k:v for k,v in T39.items() if '0x33' in v}
    sprite_idx={R[off(k)]:(R[off(k)+10]|R[off(k)+11]<<8) for k in hdrs}
    tr=[i for i in range(1,m[0xd4e1]+1) if m[0xd504+2*(i-1)]>=0xc8 and i in sprite_idx]
    idx=tr[0]
    m[0xc200+16*idx+4]=m[0xd361]+5;m[0xc200+16*idx+5]=m[0xd362]+4;m[0xc200+16*idx+6]=0xff
    m[0xc100+16*idx+4]=m[0xc104]+16;m[0xc100+16*idx+6]=m[0xc106]
    T(30);press_('down',20);press_('a',300)
    for i in range(15):
        if m[0xd057]:break
        press_('a',120)
    assert m[0xd057]==2
def use_slot(slot):
    menu('fight')
    for k in range(20):
        tt=txt()
        if any(('▲' in x or '▶' in x) for x in tt) and not any('FIGHT' in x for x in tt):break
        press_('a',60)
    m[0xcc26]=slot+1;T(4);p.button('a',8);T(300)
def play(slot,mode):
    """first FIGHT menu: use the move (slot, or -1 = RUN in the trainer phase), then keep pressing A; returns the text seen"""
    seen.clear();used=0;txts=[]
    for i in range(500):
        if m[0xd057]==0 and i>20:break
        t=clean(' '.join(txt()))
        if t and (not txts or t[-60:]!=txts[-1][-60:]):txts.append(t)
        if 'FIGHT' in t and 'RUN' in t and 'dark' not in t:
            if used or m[0xd05a]==3:                          # trainer phase: leave
                if m[0xd05a]==3:break
                press_('a',90);continue
            used=1;use_slot(slot);continue
        if 'Bring out' in t or 'change' in t.lower():press_('b',60);continue
        press_('a',90)
    return ' | '.join(txts)
if MY90=='trainer':
    for slot,name in ((0,'METAMORPHOSIS'),(1,'CURSE')):
        trainer_battle();p0=party();tt=play(slot,name)
        print(name,tt[-400:],flush=True)
        ok('fainted' not in tt,'%s: no "Enemy ... fainted!" text'%name)
        ok(m[0xd452]==1,'%s: D452 (CURSE used) is set'%name)
        ok('What have you done' in tt,'%s: the trainer\'s frightened end-of-battle line'%name)
        if slot==0:ok(len(party())>len(p0),'METAMORPHOSIS: the POKeMON joined (%d -> %d)'%(len(p0),len(party())))
elif MY90=='normal':
    trainer_battle();p0=party();seen.clear()
    # normal fight: BLACK can't hurt (scared), so RUN is not possible either: win with CHARMANDER-style: set the enemy to 1 HP and attack with slot 0? METAMORPHOSIS would count: use GHOST WALK (no effect on the checks)
    for i in range(600):
        if m[0xd057]==0 and i>20:break
        t=clean(' '.join(txt()))
        if m[0xd05a]==3:break
        if 'FIGHT' in t and 'RUN' in t:
            m[0xcfe6]=0;m[0xcfe7]=1
            use_slot(2);continue
        if 'Bring out' in t or 'change' in t.lower():press_('b',60);continue
        press_('a',90)
    tt=allt();print(tt[-300:])
    ok(m[0xd452]==0,'a normal win: D452 = 0')
    ok('fainted' in tt,'"Enemy ... fainted!" is still shown after a normal knock-out')
    ok('What have you done' not in tt,'no frightened line')
elif MY90=='holes':
    MARK=json.load(open('manifest_v47.json'))['mark']
    sps=[1,2,3,4,5,6,0x99,0x70,0x7b,0xa5,0x3a,0x58]
    def holes(addr):
        px=[[0]*56 for _ in range(56)]
        for col in range(7):
            for row in range(7):
                t=col*7+row
                for j in range(8):
                    lo=m[addr+t*16+j*2];hi=m[addr+t*16+j*2+1]
                    for b in range(8):px[row*8+j][col*8+b]=((lo>>(7-b))&1)|((hi>>(7-b))&1)
        first=[None]*56;last=[None]*56
        for x in range(56):
            ys=[y for y in range(56) if px[y][x]]
            if ys:first[x]=ys[0];last[x]=ys[-1]
        n=0;grey=0
        for y in range(56):
            xs=[x for x in range(56) if px[y][x]]
            if not xs:continue
            for x in range(xs[0],xs[-1]+1):
                if not px[y][x] and first[x] is not None and first[x]<y<last[x]:n+=1
        return n,sum(map(sum,px))
    tot=0
    for sp in sps:
        load('pallet_with_ghost')
        m[0xd164]=sp;m[0xd16b]=sp;m[0xd16b+7]=MARK;m[0xd16b+1]=0;m[0xd16b+2]=0x20;m[0xd16b+34]=0;m[0xd16b+35]=0x20
        m[0xd059]=0xa5;m[0xd127]=5
        for i in range(300):
            if m[0xd057]:break
            p.tick()
        for i in range(60):
            t=clean(' '.join(txt()))
            if 'FIGHT' in t and 'RUN' in t:break
            press_('a',30)
        T(20);n,dark=holes(0x9310);print(hex(sp),'enclosed white pixels',n,'black pixels',dark,flush=True)
        ok(n==0 and dark>200,'species %s: solid black silhouette (holes %d)'%(hex(sp),n))
print('t90 done',flush=True)
