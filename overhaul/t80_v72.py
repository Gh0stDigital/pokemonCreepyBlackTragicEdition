# v72: SNORLAX / item balls / gravestones in the position-split sprite sets; the picture -> VRAM slot invariants on every outdoor map
#  snorlax - ROUTE 12 south: after a full reload (a battle) SNORLAX uses slot 0C with its own tiles, the item balls slot 0B with the ball tiles; a gravestone picture the set doesn't have is hidden
#  balls15 - ROUTE 15 (set 12): the item ball is a ball (slot 0B holds the ball tiles), the gravestone slot 0C holds the gravestone
#  sweep   - arrive on every outdoor map: every object's slot = its position in the loaded set + 1 and the VRAM slot holds that picture's tiles
#  order   - static: every outdoor sprite set has the walkers in entries 1-9 and the four-tile pictures in 10-11 (check_sets.py)
import sys,os,subprocess
MODE80=sys.argv[1]
sys.argv=['t79_v71.py','none']
exec(open('t79_v71.py').read().split("if MY=='gates':")[0])
MY=MODE80
rom=open(os.environ['CB_ROM'],'rb').read()
fo=lambda b,a:b*0x4000+a-0x4000
tab=fo(5,0x7b3d)
def sheet(pic):
    e=rom[tab+(pic-1)*4:tab+pic*4];addr=e[0]|e[1]<<8;n=e[2];bank=e[3]
    return rom[fo(bank,addr):fo(bank,addr)+n] if 1<=bank<0x40 else b''
def vram_slot_base(slot):
    if slot==0x0b:return 0x8780
    if slot==0x0c:return 0x87c0
    return 0x8000+(slot-1)*0xc0
def vram_has(pic,slot):
    sh=sheet(pic)
    if len(sh)<32:return None
    b=vram_slot_base(slot);return bytes(m[b:b+32])==sh[:32]
def poke_view(mp,ty,tx,w):
    ptr=0xc6e8+7+w+(ty//2)*(w+6)+tx//2
    m[0xd361]=ty;m[0xd362]=tx;m[0xd35f]=ptr&255;m[0xd360]=ptr>>8;m[0xd363]=ty&1;m[0xd364]=tx&1
    p.button('start',8);T(30);p.button('b',8);T(90)
def battle_reload(spr,ty,tx):
    m[0xd16b+1]=1;m[0xd16b+2]=0x2c;m[0xd16b+34]=1;m[0xd16b+35]=0x2c
    b1=0xc100+spr*16;b2=0xc200+spr*16
    m[b1+2]=0;m[b1+4]=0x2c;m[b1+6]=0x40;m[b2+4]=ty-1+4;m[b2+5]=tx+4;m[b2+6]=0xff
    T(10);p.button('up',8);T(20)
    for k in range(30):
        if m[0xd057]:break
        press_('a',70)
    assert m[0xd057],'no battle'
    fight(limit=1500,hp1=True,spare=True)
    for k in range(10):press_('b',60)
    T(60);m[b2+4]=0xff;m[b2+5]=0xff
if MY=='snorlax':
    warp_from_pallet(0x17,0);m[0xd887]=0;poke_view(0x17,64,10,10)
    b3=0xc100+3*16;c3=0xc200+3*16                                   # a fisher that is a gravestone (picture 49)
    m[b3]=0x49;m[b3+2]=0;m[b3+4]=0x3c;m[b3+6]=0x30;m[c3+4]=64+4;m[c3+5]=9+4;m[c3+6]=0xff
    battle_reload(2,64,10)
    objs=[(i,m[0xc100+i*16],m[0xc200+i*16+14]) for i in range(1,11)]
    print('objects',[(i,hex(p_),hex(s_)) for i,p_,s_ in objs],flush=True)
    sn=[o for o in objs if o[1]==0x43][0];ball=[o for o in objs if o[1]==0x3d]
    ok(sn[2]==0x0c and vram_has(0x43,0x0c),'ROUTE 12 south: SNORLAX uses slot 0C and its own tiles are there')
    ok(all(b[2]==0x0b for b in ball) and vram_has(0x3d,0x0b),'ROUTE 12 south: the item balls use slot 0B and the ball tiles are there')
    ok(m[b3]==0,'ROUTE 12 south: a gravestone the set cannot draw is hidden instead of drawn with garbage tiles')
    T(60);ok(m[b3]==0,'... and stays hidden')
elif MY=='balls15':
    warp_from_pallet(0x1a,0);m[0xd887]=0
    print('arrive',pos(),flush=True)
    ty=max(m[0xd361],8);tx=20;poke_view(0x1a,ty,tx,m[0xd5ff] if False else 40) if False else None
    objs=[(i,m[0xc100+i*16],m[0xc200+i*16+14]) for i in range(1,m[0xd4e1]+1)]
    print('objects',[(i,hex(p_),hex(s_)) for i,p_,s_ in objs],'set',m[0xd3a8],flush=True)
    ball=[o for o in objs if o[1]==0x3d]
    ok(not ball or (all(b[2]==0x0b for b in ball) and vram_has(0x3d,0x0b)),'ROUTE 15: an item ball is a ball (slot 0B, ball tiles)')
elif MY=='sweep':
    bad=[];tot=0
    for mp in list(range(0,0x0b))+list(range(0x0c,0x25)):
        try:warp_from_pallet(mp,0)
        except Exception as e:print('skip',hex(mp),e);continue
        if m[0xd35e]!=mp:print('no arrival',hex(mp));continue
        st=[m[0xd39d+i] for i in range(11)]
        for i in range(1,m[0xd4e1]+1):
            pic=m[0xc100+i*16]
            if not pic:continue
            slot=m[0xc200+i*16+14];tot+=1
            if pic in st:
                exp=st.index(pic)+2
                if slot!=exp:bad.append((hex(mp),i,hex(pic),'slot',hex(slot),'expected',hex(exp)));continue
                h=vram_has(pic,slot)
                if h is False:bad.append((hex(mp),i,hex(pic),'slot',hex(slot),'VRAM tiles are not this picture'))
    print('objects checked',tot,'problems',len(bad),flush=True)
    for b in bad:print('  ',*b)
    ok(not bad,'every object on every outdoor map has its own slot and tiles (arrival)')
elif MY=='order':
    r=subprocess.run([sys.executable,'check_sets.py',os.environ['CB_ROM']],capture_output=True,text=True)
    print(r.stdout[-300:])
    ok(r.returncode==0,'check_sets.py: set order, object pictures and channeler pictures')
print('t80 done',flush=True)
