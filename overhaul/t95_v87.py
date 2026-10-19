# v87: BILL's cottage (position, sprite after a redraw, gone when the battle is over), the consort's sprite / LAVENDER music in the house, the CERULEAN cave guard.
#  Modes: bill, house, cer, normal
import sys
MY95=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY95
if MODE=='bill':
    def pics():return {i:(m[0xc100+16*i],m[0xc204+16*i]-4,m[0xc205+16*i]-4,m[0xc102+16*i]) for i in range(1,4) if m[0xc100+16*i] and m[0xc204+16*i]!=0xff}
    def setup():
        make_black();lead(CHAR);strong(0)
        b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35
        m[0xd867]|=2;m[0xd876]=5
    warp(0x58,0,setup)
    slots=set();seen_after=[];last={}
    p.hook_register(0,0x0040,lambda c:seen_after.append((m[0xd057],m[0xd35e],m[0xc120],m[0xc122],m[0xc224])) if m[0xd877]>=3 else None,None)
    for i in range(80):
        if m[0xd057]:break
        if box():press_('a',80)
        else:T(8)
        if m[0xc122]!=0xff and m[0xd877]>=1:slots.add(m[0xc122]>>4)
        if pics().get(2) and pics()[2][3]!=0xff:last=pics()
    pc=last;print('BILL before the battle',pc,slots)
    ok(pc.get(2,(0,))[0]==0xc and pc[2][1:3]==(6,2),'BILL stands at (6,2), directly in front of the player (%s)'%(pc.get(2),))
    ok(pc[2][3]&0xf==0,'BILL faces down')
    ok(len(slots)==1,'BILL keeps one VRAM slot from the walk to the battle (slots %s)'%sorted(slots))
    m[0xd89c]=1;wait_menu()
    ok(m[0xd031]==26,'BILL fights BLACK')
    menu('fight');m[0xcc26]=1;T(4);seen.clear();p.button('a',8)
    for k in range(2500):
        p.tick()
        if k%4==0:T(1)
        if m[0xd05a]==3 and 'FIGHT' in clean(' '.join(txt())):break
        if k%90==0:p.button('a',8)
    use_move(0,300,in_moves=True)
    for i in range(30):
        if m[0xd057]==0:break
        press_('a',100)
    seen_after.clear()
    for i in range(14):press_('a',60)
    T(120)
    after=[x for x in seen_after if x[0]==0 and x[1]==0x58]
    print('frames after the battle',len(after),'BILL drawn:',[x for x in after if x[2]!=0 and x[3]!=0xff][:3])
    dr=[k for k,x in enumerate(after) if x[2]!=0 and x[3]!=0xff];print('drawn frames',len(dr),dr[:5],dr[-3:],'toggle flag',hex(m[0xd5a6+12]))
    ok(after and not dr,'BILL is never drawn after the battle')
    ok(m[0xd876]==6,'D876 = 6 as before')
elif MODE=='house':
    sys.argv=['x','house']
    exec(open('t35_v25.py').read().split("elif MODE=='house':")[0].replace("if MODE=='items':","if False:"))
    for k in range(1):
        def setup():m[RIT]=6;m[0xd465]=1;m[0xd46c]=1
        warp(0x25,0,setup);T(60)
    img0=m[0xc122]>>4
    print('music in the house',hex(m[0xd35b]),'consort pic',hex(m[0xc120]),'slot',img0)
    ok(m[0xd35b]==0xd4,'the house plays the LAVENDER theme as BLACK')
    bfs_to(6,6);p.button('up',8);T(30);seen.clear()
    for k in range(40):
        press_('a',70)
        if not box() and k>2:break
    T(120)
    print('after: pic',hex(m[0xc120]),'slot',m[0xc122]>>4,'music',hex(m[0xd35b]),[hex(m[0xc026+k]) for k in range(3)])
    ok(m[0xc120]==0x1d and m[0xc122]>>4==img0,'the consort keeps her picture and VRAM slot after the text')
    ok(m[0xd35b]==0xd4 and m[0xc026]==0xd4,'after the heal the LAVENDER theme is playing again')
    # a redraw by the START menu
    press_('start',30);press_('b',30);T(30)
    ok(m[0xc122]>>4==img0,'and after a menu redraw')
elif MODE=='cer':
    def guard():
        return [(i,m[0xc100+16*i]) for i in range(1,m[0xd4e1]+1) if (m[0xc204+16*i]-4,m[0xc205+16*i]-4)==(12,4) and m[0xc100+16*i]]
    for stage,black,vis in ((0,1,True),(1,1,False),(1,0,True)):
        def setup(stage=stage,black=black):
            m[0xd46c]=black;m[0xd876]=stage
            m[0xd5a7]&=0xfe
        warp(3,0,setup);T(90)
        print('stage',stage,'black',black,'guard',guard())
        ok(bool(guard())==vis,'CERULEAN guard %s (D876=%d, BLACK=%d)'%('stands there' if vis else 'is gone',stage,black))
elif MODE=='normal':
    def setup():m[0xd46c]=0;m[0xd467]=0
    warp(0x25,0,setup);T(60)
    ok(m[0xd35b]==0xba,'not BLACK: the house keeps its own music (%s)'%hex(m[0xd35b]))
    warp(0x24,0,setup);T(60)
    ok(m[0xd35b]!=0xd4,'not BLACK: other maps unchanged (%s)'%hex(m[0xd35b]))
    def setupb():make_black()
    warp(0x26,0,setupb);T(60)
    ok(m[0xd35b]!=0xd4,'BLACK: the next building (map 26) keeps its own music (%s)'%hex(m[0xd35b]))
elif MODE=='blue':
    src66=open('t66_v58.py').read().replace("MY66=sys.argv[1]","MY66='black'")
    head66,rest66=src66.split("if MODE=='black':",1)
    sys.argv=['x','black'];exec(head66)
    m[0xd5a7]&=0xfe
    exec("if MODE=='black':"+rest66.split("    seen.clear();maps=set()",1)[0])
    for i in range(10):
        if m[0xd876]>=1:break
        press_('a',60)
    T(60)
    print('D876',m[0xd876],'flags',hex(m[0xd5a7]))
    ok(m[0xd5a7]&1==1,'beating BLUE as BLACK hides the CERULEAN cave guard (toggle 8)')
