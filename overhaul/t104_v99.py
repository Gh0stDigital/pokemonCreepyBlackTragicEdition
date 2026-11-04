# v99: CINNABAR GYM. Modes:
#  kill   - a quiz trainer (object 2) beaten with GHOST and CURSEd in the trainer phase: D886 bit 0, hidden at once, a gravestone on the next visit
#  spare  - control: CURSE used but RUN in the trainer phase: alive, D886 = 0
#  quiz   - quiz machine 1 (trainer object 3) with the trainer dead (D886 bit 1): "ERROR! DESIGNATED TRAINER MISSING." and no question;
#           control: machine 2 (trainer alive) asks its question as before
#  blaine - a quiz trainer dead: BLAINE's new surprised speech (OAK and FUJI, their twisted project); control: no kill -> his usual speech
#  lore   - BLAINE beaten with CURSE and spared: the FUJI / OAK / MANSION lore before his badge text; control: a win without CURSE -> no lore
import sys
MY104=sys.argv[1]
sys.argv=['x','none']
exec(open('t28_v14.py').read().split("if MODE=='mirage_rate':")[0].replace("MODE=sys.argv[1]","MODE='x'"))
MODE=MY104
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:globals()['bad']=globals().get('bad',0)+1
def summon(i):
    y,x=m[0xd361],m[0xd362];b1=0xc100+i*16;b2=0xc200+i*16
    m[b1+4]=0x2c;m[b1+6]=0x40;m[b1+2]=1 if m[b1+2]==0xff else m[b1+2];m[b2+4]=y-1+4;m[b2+5]=x+4;m[b2+6]=0xff
def talk_up(i,n=40):
    summon(i);T(10);p.button('up',8);T(20);seen.clear()
    for k in range(n):
        if m[0xd057] or (not box() and k>12):break
        press_('a',70)
    return allt().replace("'","")
def gym(setup=None):
    warp_from_pallet(0xa6,0);m[0xd887]=0
    if setup:setup()
def after(n=40):
    for i in range(n):
        if not box() and i>6:break
        press_('a',80)
if MODE in ('kill','spare'):
    gym();talk_up(2)
    ok(m[0xd057]==2 and m[0xd059]==0xd0,'talking to quiz trainer 2 starts his battle (SUPER NERD)')
    fight(spare=(MODE=='spare'));after()
    idx=m[0xd4ae]<<8|m[0xd4af];print('kill index',hex(idx),flush=True)
    ok(idx==0x23b0,'the trainer phase gave him kill index 23B0 (D886 bit 0)')
    print('D886',hex(m[0xd886]),'texts',allt()[-200:],flush=True)
    if MODE=='kill':
        ok(m[0xd886]==1 and 'failed' not in allt(),'CURSE killed him: D886 bit 0 (no "But, it failed!")')
        hid={}
        p.hook_register(0x2d,0x6248,lambda c:hid.__setitem__(m[0xffda]>>4,p.register_file.A),None);T(60)
        ok(hid.get(2)==1 and all(hid.get(k)==0 for k in (3,4,5,6,7,8) if k in hid),'he is hidden at once, the other quiz trainers are drawn (%s)'%hid)
        d=m[0xd886];warp_from_pallet(0xa6,0);m[0xd886]=d;T(5)
        load_again=None
    else:
        ok(m[0xd886]==0,'spared: D886 stays 0 (control)')
if MODE=='kill':
    # a fresh visit with the kill bit: the map-load pass turns him into a gravestone
    def s():m[0xd886]=1
    load('pallet_with_ghost');lead(0x1f);m[0xd455]=255;m[0xd886]=1
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0xa6
    for i in range(6):
        if m[0xd35e]==0xa6:break
        walk('up',1)
    T(120)
    pics=[hex(m[0xc100+16*i]) for i in range(1,m[0xd4e1]+1)];print('pics on the next visit',pics,flush=True)
    ok(m[0xc120]==0x49 and m[0xc130]!=0x49,'next visit: he is a gravestone, the others are not')
if MODE=='quiz':
    def machine(y,x):
        m[0xd361]=y+1;m[0xd362]=x;m[0xc109]=4;seen.clear();press_('a',90)
        for k in range(12):
            t=clean(' '.join(txt()))
            if 'YES' in t and 'NO' in t:break
            if not box() and k>3:break
            press_('a',80)
        return clean(' '.join(txt())),allt()
    gym(lambda:m.__setitem__(0xd886,2))
    s,t=machine(7,15);print('machine 1 (trainer dead):',t[-160:],flush=True)
    ok('ERROR' in t and 'MISSING' in t and 'YES' not in s,'machine 1, trainer dead: "ERROR! DESIGNATED TRAINER MISSING." and no question')
    for k in range(6):press_('b',40)
    s,t=machine(1,10);print('machine 2 (trainer alive):',t[-160:],s[-80:],flush=True)
    ok('ERROR' not in t and 'certified' in t,'machine 2, trainer alive: the usual question (control)')
if MODE=='blaine':
    for dead in (True,False):
        gym((lambda:m.__setitem__(0xd886,1)) if dead else None)
        t=talk_up(1);print('BLAINE dead=%s:'%dead,t[:300],flush=True)
        if dead:ok('twisted' in t and 'OAK and FUJI' in t,'a quiz trainer killed: BLAINE knows who you are (OAK and FUJI, the twisted project)')
        else:ok('twisted' not in t and len(t)>20,'no kill: his usual speech (control)')
if MODE=='lore':
    for cursed in (True,False):
        if cursed:
            gym()
        else:
            def s():lead(0xb0)
            gym(s)
        talk_up(1)
        ok(m[0xd057]==2,'BLAINE fights (%s)'%('GHOST' if cursed else 'CHARMANDER'))
        if cursed:fight(spare=True)
        else:fight(hp1=True)
        seen.clear();after(60);t=allt().replace("'","")
        print('after (cursed=%s):'%cursed,t[:500],flush=True)
        if cursed:ok('FUJI was obsessed' in t and 'buried' in t and m[0xd452],'spared after CURSE: the FUJI / OAK / MANSION lore')
        else:ok('FUJI was obsessed' not in t,'a win without CURSE: no lore (control)')
print('t104 done',flush=True)
