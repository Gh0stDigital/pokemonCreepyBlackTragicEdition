# v86: Route 22 rival gate for BLACK, no victory fanfare after League / BLUE battles, GHOST WALK power by level, BLUE's object gone at once + AGATHA faces up
#      in the Hall of Fame, OAK'S LAB aide (same picture after a redraw, METAMORPHOSIS question). Modes: gate, gw, fanfare, hof, lab
import sys
MY94=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY94
if MODE=='gate':
    def setup(mode,black):
        def f():
            m[0xd463]=mode;m[0xd7eb]|=0x82
            if black:make_black()
            else:m[0xd46c]=0
        return f
    for mode,black,gone,name in ((0,True,True,'BLACK'),(1,False,True,'shock mode'),(2,False,True,'hero mode'),(0,False,False,'normal game (control)')):
        warp(0x21,0,setup(mode,black));T(60)
        ok(bool(m[0xd7eb]&0x80)!=gone,'Route 22: %s -> the rival %s (D7EB=%s)'%(name,'does not want a battle' if gone else 'still wants his battle',hex(m[0xd7eb])))
elif MODE=='gw':
    sys.argv=['x','gwalk']
    exec(open('t56_v48.py').read().split("if MODE=='moves':")[0])
    pw=[]
    p.hook_register(0xf,0x578f,lambda c:pw.append((m[0xcfd2],m[0xcfd4],m[0xd022])),None)
    for lvl in (5,50,100):
        pw.clear()
        start_wild(make_black,lv=40)
        m[0xd022]=lvl
        use_move(2,400)
        for k in range(12):press_('a',50)
        g=[x for x in pw if x[0]==0xab]
        print('level',lvl,'GHOST WALK power',g[:2],flush=True)
        ok(bool(g) and g[0][1]==min(250,20+lvl+lvl//2),'GHOST WALK power at level %d = %d'%(lvl,20+lvl+lvl//2))
    pw.clear();start_wild(make_black,lv=40);m[0xd022]=50;m[0xd16b+9]=0x0a;m[0xd01d]=0x0a;m[0xd02e]=35;use_move(1,400)
    for k in range(4):press_('a',60)
    print('other moves',pw,flush=True)
    ok(pw!=[] and all(x[1]==40 for x in pw if x[0]==0x0a),'SCRATCH keeps its own power 40 (%s)'%pw[:2])
elif MODE=='lab':
    lab_src=open('t67_v59.py').read().split("if MODE=='black':")[0]
    sys.argv=['x','none'];exec(lab_src.replace("MY67=sys.argv[1]","MY67='black'"))
    def aide_tile():
        return [p.memory[0xfe00+4*k+2] for k in range(40) if 0<p.memory[0xfe00+4*k]<160 and p.memory[0xfe00+4*k+1] in range(8,20)]
    lab(4)
    t0=aide_tile();img0=m[0xc1a2]>>4;print('aide tiles before',t0,'slot',img0)
    bfs_to(10,1,maxn=300);p.button('left',8);T(30);seen.clear();press_('a',60)
    for i in range(60):
        if box():press_('a',70)
        else:T(20)
        if m[0xd876]==5 and ('METAMORPH' in allt()):break
    t=allt();print('LAB TEXT:',t[-300:])
    ok('want to die' in t and 'METAMORPH' in t,'after the aide\'s speech: the METAMORPHOSIS question')
    ok(m[0xd876]==5,'the speech still sets D876 = 5')
    # NO
    for i in range(3):
        if 'METAMORPH' in ' '.join(txt()):break
        press_('a',60)
    press_('down',10);press_('a',80);T(60)
    ok(m[0xc1a0]==0x20,'NO: the aide is still there (picture 20)')
    # the picture after a redraw (menu): same slot as before
    press_('start',30);press_('b',30);T(30)
    pic=m[0xc1a0];print('after menu pic',hex(pic),'img',hex(m[0xc1a2]),'tiles',aide_tile())
    ok(pic==0x20 and m[0xc1a2]>>4==img0,'after a redraw the aide is still picture 20 in the same VRAM slot (%d -> %d)'%(img0,m[0xc1a2]>>4))
    # YES
    seen.clear();press_('a',60)
    for i in range(60):
        if box():press_('a',70)
        else:T(20)
        if 'METAMORPH' in ' '.join(txt()) and '▶' in ''.join(txt()) or 'YES' in ' '.join(txt()):break
    press_('a',60)
    for i in range(30):
        if box():press_('a',90)
        else:T(30)
    T(120);t=allt();print('after yes',t[-200:],hex(m[0xc1a0]))
    ok(m[0xc1a0]==0x47,'YES: the aide is a black ball (picture 47)')
    shot('v86_lab_ball')
elif MODE=='hof':
    src66=open('t66_v58.py').read().replace("MY66=sys.argv[1]","MY66='black'")
    head66,rest66=src66.split("if MODE=='black':",1)
    sys.argv=['x','black'];exec(head66)
    exec("if MODE=='black':"+rest66.split("    seen.clear();maps=set()",1)[0])
    pics=[]
    for i in range(300):
        if box():press_('a',40)
        else:T(3)
        if m[0xd876]>=1 and m[0xd35e]==0x78:pics.append(m[0xc110])
        if m[0xd876]>=4:break
    print('BLUE pictures while stage>=1 in the champion room',pics[:12])
    ok(pics and pics[0]==0 and all(x==0 for x in pics),'BLUE is gone from the first frame of the walk')
    ok(m[0xd876]==4 and m[0xd35e]==0x76,'AGATHA scene finished in the Hall of Fame')
    T(30)
    ok(m[0xc119]==4 and (m[0xc112]&0xf)<4+4 and (m[0xc112]&0xf)>=4,'AGATHA faces up (c119=%d img %s)'%(m[0xc119],hex(m[0xc112])))
    ok(m[0xd35b]==0xff,'the HALL OF FAME is silent for BLACK (music id %s)'%hex(m[0xd35b]))
elif MODE=='fanfare':
    ids=[]
    p.hook_register(0,0x23de,lambda c:ids.append(p.register_file.A),None)
    def setup():
        make_black();lead(CHAR);strong(0)
        b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35
    to_battle(0xf5,3,5,setup,one=True)
    menu('fight');m[0xcc26]=1;T(4);seen.clear();p.button('a',8);ids.clear()
    for k in range(2500):
        p.tick()
        if k%4==0:T(1)
        if m[0xd05a]==3 and 'FIGHT' in clean(' '.join(txt())):break
        if k%90==0:p.button('a',8)
    print('LORELEI ids',sorted(set(ids)),flush=True)
    ok(m[0xd05a]==3,'LORELEI is beaten (phase)')
    ok(not ({0xf6,0xf9,0xfc}&set(ids)),'no victory fanfare after a League trainer (ids %s)'%sorted(set(ids)))
    # control: an ordinary trainer (PEWTER GYM) still plays it
    def setup2():
        lead(CHAR);strong(0);m[0xd46c]=0
    warp(0x36,0,setup2);T(30)
    objs=[(i,m[0xc204+16*i]-4,m[0xc205+16*i]-4) for i in range(1,m[0xd4e1]+1) if m[0xd504+2*(i-1)]!=0]
    print('trainers',objs,flush=True)
    ty,tx=objs[-1][1],objs[-1][2]
    bfs_to(ty+1,tx);press_('up',20);seen.clear();press_('a',200)
    for i in range(20):
        if m[0xd057]:break
        press_('a',120)
    ok(m[0xd057]==2,'a PEWTER GYM trainer fights')
    wait_menu();ids.clear()
    for r in range(6):
        if m[0xd057]==0:break
        use_move(0,400)
        for k in range(6):press_('a',50)
        m[0xd89c]=1
    for k in range(200):p.tick()
    print('control ids',sorted(set(ids)),flush=True)
    ok(bool({0xf6,0xf9,0xfc}&set(ids)),'an ordinary trainer win still plays the fanfare (control)')
