# v93: HUD levels (YOU Lv10, MR. MU Lv68), silent MR. MU death, silent MASTER BALL catch, quiet GHOST battle start, OAK gone as BLACK, Route 22 gate (GHOST + 8 badges).
#  Modes: ritual (HUD + faint + catch), control (an ordinary trainer's faint still plays), climax, oak, gate
import sys,re
MY101=sys.argv[1]
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:sys.exit(1)
if MY101=='ritual':
    import pyboy
    _o=pyboy.PyBoy
    pyboy.PyBoy=lambda *a,**k:_o(*a,**{**k,'sound_emulated':True})
    s=open('t34_v23.py').read()
    s=s.replace("def clean(s):","ids=[]\np.hook_register(0,0x23de,lambda c:ids.append(p.register_file.A),None)\ndef clean(s):",1)
    s=s.replace("    assert wait_menu(),'no battle menu'","    assert wait_menu(),'no battle menu'\n    hud=' '.join(txt());print('HUD',hud,flush=True)\n    ok(' 68' in ' '+hud.replace('MR. MU ','MR. MU ') and 'RED' in hud and re.search(r'@\\s+10',hud) is not None,'HUD: MR. MU Lv68, RED Lv10')",1)
    s=s.replace("    seen.clear();turns=0;minhp=999","    ids.clear();seen.clear();turns=0;minhp=999",1)
    s=s.replace("    t=allt();print('fight:',t[-300:])","    print('fight ids',sorted(set(hex(i) for i in ids)),flush=True)\n    ok(0x9e not in ids and 0x95 not in ids,'MR. MU dies without the faint fall / thud');ok(turns==4,'still 4 STRUGGLE turns (%d) - stats and damage unchanged'%turns)\n    t=allt();print('fight:',t[-300:])",1)
    s=s.replace("    pick_item('MASTER');seen.clear();press_('a',10)","    pick_item('MASTER');seen.clear();press_('a',10);apu=[]",1)
    s=s.replace("            if 'caught' in b and not black:","            apu.append(m[0xff26]>>7)\n            if 'caught' in b and not black:\n                apu_caught=m[0xff26]>>7",1)
    s=s.replace("    print('catch:',allt()[-200:])","    print('catch:',allt()[-200:])\n    ok(0 in apu and apu_caught==0,'the catch is silent: the sound hardware is off from the toss on (%s)'%sorted(set(apu)))",1)
    s=s.replace("    T(400)\n    after=party()","    T(400)\n    ok(m[0xff26]>>7==1 and m[0xff24]==0x77,'speakers back after the ritual (NR52 %02X NR50 %02X)'%(m[0xff26],m[0xff24]))\n    after=party()",1)
    s=s.replace("MODE=sys.argv[1]","MODE='ritual'",1)
    sys.argv=['x','ritual']
    exec(compile("def ok(c,msg):\n    print(('PASS ' if c else 'FAIL ')+msg,flush=True)\n    if not c:sys.exit(1)\n"+s,'t34mod','exec'))
elif MY101=='control':
    sys.argv=['x','none']
    exec(open('t94_v86.py').read().split("if MODE=='gate':")[0].replace("MY94=sys.argv[1]","MY94='x'"))
    ids=[]
    p.hook_register(0,0x23de,lambda c:ids.append(p.register_file.A),None)
    def setup2():
        lead(CHAR);strong(0);m[0xd46c]=0
    warp(0x36,0,setup2);T(30)
    objs=[(i,m[0xc204+16*i]-4,m[0xc205+16*i]-4) for i in range(1,m[0xd4e1]+1) if m[0xd504+2*(i-1)]!=0]
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
    print('ids',sorted(set(hex(i) for i in ids)))
    ok(0x9e in ids and 0x95 in ids,'an ordinary trainer\'s faint still plays the fall and the thud (control)')
elif MY101=='climax':
    s=open('t85_v77.py').read()
    s=s.replace("snd=[]\n","snd=[]\nALLT=[]\n_T0=T\ndef T(n):\n    for _ in range(n):\n        p.tick();b=clean(box())\n        if b and (not ALLT or ALLT[-1]!=b):ALLT.append(b)\n",1)
    tail="full=' '.join(ALLT);print('ALL TEXTS',full[-700:],flush=True)\nok('Wild GHOST appeared' in full,'the GHOST battle intro was shown')\nok('Go!' not in full,'no \"Go! RED!\" in the GHOST battle')\nok(0x14 not in [a for a,mp in snd],'no send-out sound for RED in the GHOST battle (ids %s)'%sorted(set(hex(a) for a,mp in snd)))\nprint('t101 done',flush=True)"
    i=s.rindex("print('t85 done',flush=True)");s=s[:i]+tail.replace("\\n","\n")+s[i+len("print('t85 done',flush=True)"):]
    sys.argv=['x','climax']
    exec(compile(s.replace("MY85=sys.argv[1]","MY85='climax'"),'t85mod','exec'))
elif MY101=='oak':
    sys.argv=['x','black']
    exec(open('t67_v59.py').read().split("if MODE=='black':")[0])
    def hidden_oak():   # OAK objects (picture 3) still on the map
        return [(i,hex(m[0xc102+16*i])) for i in range(1,12) if m[0xc100+16*i]==3 and m[0xc204+16*i]!=0xff]
    def setup(black,stage=0):
        def f():
            if black:make_black();m[0xd876]=stage
            else:m[0xd46c]=0
        return f
    for mp,name in ((0x28,"OAK'S LAB"),):
        warp(mp,0,setup(True));T(90)
        ok(m[0xd35e]==mp and not hidden_oak(),'%s: as BLACK OAK is gone (%s)'%(name,hidden_oak()))
        press_('start',30);press_('b',40);T(60)
        ok(not hidden_oak(),'%s: still gone after the START menu'%name)
        warp(mp,0,setup(False));T(90)
        ok(m[0xd35e]==mp and bool(hidden_oak()),'%s: not BLACK -> OAK is there as before (control)'%name)
elif MY101=='gate':
    sys.argv=['x','none']
    exec(open('t52_v44.py').read().split("if MODE=='block':")[0])
    def case(ghost,badges,mode,black):
        def f():
            m[0xd463]=mode;m[0xd7eb]|=0x82;m[0xd451]=ghost;m[0xd356]=badges
            m[0xd46c]=1 if black else 0
            if black:make_black()
        return f
    for ghost,badges,mode,black,gone,name in ((1,0xff,0,False,True,'GHOST route + 8 badges'),(1,0x7f,0,False,False,'GHOST route, 7 badges (control)'),(0,0xff,0,False,False,'no GHOST, 8 badges (control)'),(0,0xff,0,True,True,'BLACK'),(1,0x03,1,False,True,'shock mode')):
        warp(0x21,0,case(ghost,badges,mode,black));T(60)
        ok(bool(m[0xd7eb]&0x80)!=gone,'Route 22: %s -> the rival %s'%(name,'is switched off' if gone else 'still wants his battle'))
