# v12: rival BLUE on the GHOST route. Modes:
#  tower   - Pokemon Tower 2F, GHOST CURSEs his team: "died" text, GHOST hesitates / BLUE ran away (no murder),
#            shock mode, encounters skipped, "bastard" after-battle text            -> saves blue_after_tower
#  silph   - from blue_after_tower: Silph Co 7F avenge text, win -> hero mode         -> saves blue_hero
#  silph_rocket - fresh GHOST-route save (no shock): "TEAM ROCKET told me" text
#  route22 - from blue_hero: Route 22 rival-wants-battle flag is cleared
#  champion- from blue_hero: Champion's last Pokemon is Lv70 MEWTWO
from harness import *
CER=lambda:(m[0xd75a]&1) if VERSION>=15 else m[0xd75b]>>7   # v15: BLUE's real Cerulean flag (v12-v14 set the Rocket thief's)
import sys,random
MODE=sys.argv[1]
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
seen=[]
def T(n):
    for _ in range(n):
        p.tick();b=clean(box())
        if b and (not seen or seen[-1]!=b):seen.append(b)
def press_(k,n=60):p.button(k,8);T(n)
def ghost_lead():
    i=list(m[0xd164:0xd16a]).index(0x1f)
    if i:
        for base,size in ((0xd16b,44),(0xd2b5,11),(0xd273,11)):
            a=list(m[base:base+size]);b=list(m[base+size*i:base+size*(i+1)])
            m[base:base+size]=b;m[base+size*i:base+size*(i+1)]=a
        m[0xd164],m[0xd164+i]=m[0xd164+i],m[0xd164]
    m[0xd16b+29]=0x3f                                           # plenty of CURSE PP for the test
    m[0xd455]=255
def warp_from_pallet(mapid,warpid):
    load('pallet_with_ghost');ghost_lead()
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=warpid;m[0xd3af+4*i+3]=mapid
    for i in range(6):
        if m[0xd35e]==mapid:break
        walk('up',1)
    T(120);print('arrived',pos(),flush=True)
def walk_to(y,x,limit=40):
    for i in range(limit):
        if m[0xd057] or (m[0xd361]==y and m[0xd362]==x):return
        cy,cx=m[0xd361],m[0xd362]
        dirs=(['up'] if cy>y else ['down'] if cy<y else [])+(['left'] if cx>x else ['right'] if cx<x else [])
        if i%2:dirs.reverse()
        for d in dirs:
            p.button(d,8);T(24)
            if (m[0xd361],m[0xd362])!=(cy,cx) or m[0xd057]:break
def fight_with_curse(limit=400):
    for i in range(limit):
        if m[0xd057]==0:return
        b=clean(box())
        if 'FIGHT' in b and 'RUN' in b:
            for k in range(4):
                if '▲FIGHT' in box():break
                press_('up',20);press_('left',20)
            press_('a',60)
            if 'CURSE' in ' '.join(txt()):press_('a',200)
            continue
        if 'Bring out' in b or 'change' in b.lower():press_('b',60);continue
        press_('a',90)
def after_battle(n=40):
    for i in range(n):
        press_('a',90)
def show(tag):
    print(tag);[print('  TEXT:',s) for s in seen if s.endswith('!') or s.endswith('▼') or s.endswith('?') or s.endswith('.')]
if MODE=='tower':
    warp_from_pallet(0x8f,1);m[0xd887]=0
    print('mode',m[0xd463],'tower beaten',m[0xd764]>>7,'cerulean',CER(),'ssanne script',m[0xd665],'r22 wants',m[0xd7eb]>>7)
    m[0xd7eb]|=0x80                                             # pretend Oak's Pokedex set Route 22 rival wanting a battle
    walk_to(6,14)
    for i in range(40):
        if m[0xd057]:break
        press_('a',90)
    print('battle',m[0xd057],'class',m[0xd031],'opp',hex(m[0xd059]),'enemy party',list(m[0xd89d:0xd8a3]),flush=True)
    assert m[0xd057]==2 and m[0xd031]==42
    fight_with_curse();after_battle(30)
    show('TOWER')
    allt=' '.join(seen)
    print('mode',m[0xd463],'murder',m[0xd453],'tower beaten',m[0xd764]>>7,'cerulean',CER(),'ssanne script',m[0xd665],'r22 wants',m[0xd7eb]>>7,'graves',list(m[0xd4a4:0xd4ae]),pos())
    assert 'died' in allt and 'hesitates' in allt and 'ran away' in allt and 'bastard' in allt
    assert m[0xd463]==1 and m[0xd453]==0 and m[0xd764]>>7 and CER() and (VERSION<15 or not m[0xd75b]>>7) and m[0xd665]==4 and not m[0xd7eb]>>7
    print('PASS Tower: died text, GHOST hesitates, no murder, shock mode, encounters skipped, bastard text')
    save('blue_after_tower')
elif MODE in ('silph','silph_rocket'):
    warp_from_pallet(0xd4,4)
    if MODE=='silph':m[0xd463]=1;m[0xd764]|=0x80               # state left by the Tower test: shock mode, Tower rival beaten
    print('silph',pos(),'mode',m[0xd463],flush=True);assert m[0xd35e]==0xd4;m[0xd887]=0
    walk_to(3,3)
    for i in range(60):
        if m[0xd057]:break
        press_('a',90)
    print('battle',m[0xd057],'class',m[0xd031])
    if MODE=='silph_rocket':
        show('SILPH (no shock)');assert 'TEAM ROCKET' in ' '.join(seen) and 'dangerous' in ' '.join(seen)
        print('PASS Silph: TEAM ROCKET told him (GHOST route, no shock)');raise SystemExit
    fight_with_curse();after_battle(30);show('SILPH')
    allt=' '.join(seen);print('mode',m[0xd463],'silph beaten',m[0xd82f]&1,'murder',m[0xd453])
    assert 'avenge' in allt and 'dangerous' in allt and m[0xd463]==2 and m[0xd82f]&1 and m[0xd453]==0
    print('PASS Silph: avenge text, win -> hero mode');save('blue_hero')
elif MODE=='route22':
    load('blue_hero');m[0xd7eb]|=0x80                          # Giovanni would set "rival wants battle" here
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x21
    for d in ('up','down','left','right'):
        if m[0xd35e]==0x21:break
        for k in range(8):
            if m[0xd35e]==0x21:break
            walk(d,1)
    T(120);print('route22',pos(),'wants',m[0xd7eb]>>7);assert m[0xd35e]==0x21 and not m[0xd7eb]>>7
    print('PASS Route 22: hero mode clears the rival battle flag')
elif MODE=='champion':
    load('blue_hero');m[0xd64c]=1                              # Lance's room sets the "player enters" script
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x78
    for d in ('up','down','left','right'):
        if m[0xd35e]==0x78:break
        for k in range(8):
            if m[0xd35e]==0x78:break
            walk(d,1)
    T(60);print('champion room',pos())
    for i in range(80):
        if m[0xd057]:break
        press_('a',90)
    T(200)
    sp=list(m[0xd89d:0xd8a3]);lv=[m[0xd8a4+44*i+33] for i in range(6)]
    print('battle',m[0xd057],'class',m[0xd031],'trainerNo',m[0xd05d],'party',[hex(x) for x in sp],'levels',lv)
    assert m[0xd031]==43 and sp[5]==0x83 and lv[5]==70
    print('PASS Champion: last Pokemon is Lv70 MEWTWO')
if MODE=='champion_curse':                                      # Champion: CURSE his team, then the trainer phase
    load('blue_hero');m[0xd64c]=1;ghost_lead()
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x78
    for d in ('up','down','left','right'):
        if m[0xd35e]==0x78:break
        for k in range(8):
            if m[0xd35e]==0x78:break
            walk(d,1)
    for i in range(80):
        if m[0xd057]:break
        press_('a',90)
    print('battle',m[0xd057],'class',m[0xd031],flush=True)
    for i in range(300):                                        # CURSE until the trainer phase (battle type 3)
        if m[0xd05a]==3 or m[0xd057]==0:break
        b=clean(box())
        if 'FIGHT' in b and 'RUN' in b:
            press_('a',60)
            if 'CURSE' in ' '.join(txt()):press_('a',200)
            continue
        if 'Bring out' in b or 'change' in b.lower():press_('b',60);continue
        press_('a',90)
    show('CHAMPION fight');print('trainer phase type',m[0xd05a],flush=True);del seen[:]
    for i in range(30):
        b=clean(box())
        if 'FIGHT' in b and 'RUN' in b:break
        press_('a',60)
    press_('a',60);press_('a',200);T(300)
    for i in range(6):press_('a',90)
    show('CHAMPION trainer CURSE');print('battle',m[0xd057],'type',m[0xd05a],'murder',m[0xd453],pos(),flush=True)
    del seen[:]
    for i in range(20):                                         # leave the trainer phase with RUN
        if m[0xd057]==0:break
        b=clean(box())
        if 'FIGHT' in b and 'RUN' in b:press_('down',20);press_('right',20);press_('a',200);continue
        press_('a',90)
    T(300);show('CHAMPION after RUN');print('battle',m[0xd057],'murder',m[0xd453],pos())
    assert m[0xd057]==0 and m[0xd453]==0;print('PASS Champion: CURSE on BLUE fails like any scripted trainer; RUN leaves the trainer phase')
if MODE in ('tower_pre','tower_normal'):                        # pre-battle text only
    warp_from_pallet(0x8f,1);m[0xd887]=0
    if MODE=='tower_pre':m[0xd463]=1                            # shocked in an earlier battle (e.g. Cerulean)
    walk_to(6,14)
    for i in range(40):
        if m[0xd057]:break
        press_('a',90)
    allt=' '.join(seen);show('TOWER pre-battle '+MODE)
    if MODE=='tower_pre':assert 'monster' in allt and 'mourn' in allt and m[0xd057];print('PASS Tower: shock-mode pre-battle text, then the battle')
    else:assert 'monster' not in allt and m[0xd057];print('PASS Tower: normal pre-battle text when not in shock mode')
