# v51: TOWER rules, LAVENDER music as BLACK, MR. MU's quiet battle. Modes:
#  lead    - POKeMON TOWER 3F wild battle, GHOST leads: CHARMANDER goes out instead; normal: on Route 1 GHOST goes out
#  switch  - TOWER battle, CHARMANDER out: switching to GHOST -> "GHOST refuses your command!", CHARMANDER stays out
#  only    - TOWER battle with only GHOST able to fight: GHOST comes out, its move -> "refuses your command!", the enemy
#            keeps its HP; normal: on Route 1 GHOST's move works
#  music   - as BLACK: Pallet Town and Route 1 have the LAVENDER TOWN song, OAK's lab keeps its own; not BLACK: Pallet's own
#  mu      - MR. MU's battle: no battle music, his picture never slides away, no send-out cry, "stepped forward" stays
import sys
MY59=sys.argv[1]
if MY59=='mu':
    sys.argv=['x','none'];exec(open('t34_v23.py').read().split("if MODE in ('ritual','no','partyfull'):")[0]);MODE=MY59
    def ok(c,msg):
        print(('PASS ' if c else 'FAIL ')+msg,flush=True)
        if not c:sys.exit(1)
else:
    sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY59
ROMB=open(os.environ['CB_ROM'],'rb').read();MU_OPP=0xe3
def songs(mp):o=3*0x4000+0x404d-0x4000+2*mp;return ROMB[o]
def tower_battle(setup,mp=0x90,lv=5):
    warp(mp,0,setup);m[0xd059]=0xa5;m[0xd127]=lv
    for i in range(300):
        if m[0xd057]:break
        p.tick()
    wait_menu();T(20)
def ghost_first():lead(GHOST);m[0xd455]=255
def ehp():return m[0xcfe6]<<8|m[0xcfe7]
if MODE=='lead':
    tower_battle(ghost_first);print('out',hex(m[0xd014]),'party',[hex(x) for x in party()])
    ok(m[0xd057] and party()[0]==GHOST and m[0xd014]==CHAR,'TOWER: GHOST leads but CHARMANDER goes out')
    tower_battle(ghost_first,mp=0x0c);print('Route 1 out',hex(m[0xd014]))
    ok(m[0xd014]==GHOST,'normal: on Route 1 GHOST goes out first')
elif MODE=='switch':
    tower_battle(lambda:(lead(CHAR),m.__setitem__(0xd455,255)));seen.clear()
    menu('fight') if False else None
    press_('up',12);press_('right',12);press_('a',90)                 # PKMN
    for k in range(6):
        if 'Choose' in ' '.join(txt()) or 'Bring' in ' '.join(txt()):break
        press_('a',40)
    m[0xcc26]=1;T(4);press_('a',90)                                   # GHOST (slot 2)
    for k in range(6):
        if 'SWITCH' in ' '.join(txt()):press_('a',90);break
        T(20)
    for k in range(6):press_('a',60)
    for k in range(4):press_('b',40)
    t=allt();print(t[-200:],'out',hex(m[0xd014]))
    ok('refuses' in t and m[0xd014]==CHAR,'switching to GHOST in the TOWER: "GHOST refuses your command!", CHARMANDER stays')
elif MODE=='only':
    def s():
        ghost_first();b=0xd16b+44;m[b+1]=0;m[b+2]=0                      # CHARMANDER fainted
    tower_battle(s);e0=ehp();print('out',hex(m[0xd014]))
    ok(m[0xd014]==GHOST,'only GHOST can fight: it comes out')
    seen.clear();use_move(0,400)
    for k in range(8):
        if 'FIGHT' in clean(' '.join(txt())):break
        press_('a',60)
    t=allt();print(t[-200:],'enemy HP',e0,'->',ehp())
    ok('refuses' in t and 'used' not in t.split('refuses')[0][-30:] and ehp()==e0,'GHOST refuses the command, the enemy keeps its HP')
    tower_battle(s,mp=0x0c);e0=ehp();seen.clear();use_move(0,400)
    for k in range(8):
        if 'FIGHT' in clean(' '.join(txt())) or not m[0xd057]:break
        press_('a',60)
    t=allt();print('Route 1:',t[-150:])
    ok('refuses' not in t and 'GHOST used' in t.replace('  ',' '),'normal: on Route 1 GHOST\'s move works')
elif MODE=='music':
    LAV=songs(4)
    load('pallet_with_ghost');make_black();T(10)
    warp(0x0c,0,make_black);s1=m[0xd35b];print('Route 1 as BLACK',hex(s1),'lavender',hex(LAV),'own',hex(songs(0x0c)))
    ok(s1==LAV and songs(0x0c)!=LAV,'as BLACK: Route 1 plays the LAVENDER TOWN song')
    warp(0x28,0,make_black);s2=m[0xd35b];print('OAK lab as BLACK',hex(s2),'own',hex(songs(0x28)))
    ok(s2==songs(0x28),'as BLACK: OAK\'s lab keeps its own music')
    warp(0x0c,0,None);s3=m[0xd35b];ok(s3==songs(0x0c),'not BLACK: Route 1 has its own music')
    ok(m[0xc026] or m[0xc027] or m[0xc028],'music is playing')
elif MODE=='mu':
    slides=[];cries=[]
    p.hook_register(0xf,0x490a,lambda c:slides.append((p.register_file.HL,m[0xd059])),None)
    p.hook_register(0,0x13ff,lambda c:cries.append(p.register_file.A),None)
    chamber();set_bag([(POTION,3)]);talk_mu('yes')
    assert wait_menu(),'no battle menu'
    tiles=[m[0xc3a0+20*y+x] for y in range(0,7) for x in range(12,19)]
    t=allt();print('slides',[(hex(h),hex(o)) for h,o in slides],'cries',[hex(c) for c in cries],'music',[hex(m[0xc026+i]) for i in range(4)])
    ok(not any(h==0xc3b2 and o==MU_OPP for h,o in slides),'MR. MU\'s picture does not slide away')
    ok(MU not in cries,'no send-out cry')
    ok(sum(1 for v in tiles if v!=0x7f)>20,'his picture stands in the battle frame')
    ok(not any(m[0xc026+i] in (0xea,0xed,0xf0,0xf3) for i in range(8)),'no battle music (channels %s)'%[hex(m[0xc026+i]) for i in range(4)])
    ok('stepped' in t and m[0xcfe5]==MU,'"MR. MU stepped forward" as before, his HUD is there')
