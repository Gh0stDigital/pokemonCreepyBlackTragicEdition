# v45: BLUE replaces the POKeMON the player CURSEd. Modes:
#  tower  - Pokemon Tower: GHOST CURSEs BLUE's whole team: every killed line gets a replacement (from the original 149,
#           no MEW/MEWTWO, none of BLUE's lines, all different), saved at D86A
#  silph  - SILPH 7F with a replacement for his PIDGEY line: PIDGEOT's slot holds the replacement at the same level, at
#           its stage for that level; the rest of the team is unchanged (compared with the normal team)
#  chain  - SILPH 7F: CURSE the replacement -> that line gets a new, different replacement
#  champion - hero-mode Champion with his MEWTWO line replaced: the replacement at Lv70 in its slot
#  normal - no kills recorded: BLUE's SILPH team is exactly the original one
import sys,json
MY53=sys.argv[1]
sys.argv=['x','none'];exec(open('t25_blue.py').read().split("if MODE=='tower':")[0]);MODE=MY53
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:sys.exit(1)
MAN=json.load(open('manifest_v45.json'))
FAMS=[int(x,16) for x in MAN['blue_fams']];CAND=[int(x,16) for x in MAN['cand']];TBL=int(MAN['tbl'],16)
ROMB=open(os.environ['CB_ROM'],'rb').read()
L=MAN['labels']['bank2f'];CODE=0x2f*0x4000-0x4000
def lab(n):return CODE+int(L[n],16)
BT=lab('blue_fam')+len(FAMS)+1+len(CAND)                  # base_tab follows cand
ST=BT+256
def base(s):return ROMB[BT+s]
def stage(s,lv):
    rec=ROMB[ST+6*s:ST+6*s+6];sp=rec[1]
    for i in (2,4):
        if rec[i]==0xff or lv<rec[i]:break
        sp=rec[i+1]
    return sp
assert base(0xb4)==0xb0 and stage(0xb4,20)==0xb2 and stage(0xb4,40)==0xb4
def tbl():return list(m[TBL:TBL+len(FAMS)])
def enemy():return [(m[0xd8a4+44*i+33],m[0xd89d+i]) for i in range(m[0xd89c])]
def silph(setup=None):
    warp_from_pallet(0xd4,4);m[0xd463]=1;m[0xd764]|=0x80;m[0xd887]=0
    if setup:setup()
    walk_to(3,3)
    for i in range(60):
        if m[0xd057]:break
        press_('a',90)
    return enemy()
PIDGEY=0x24
if MODE=='tower':
    warp_from_pallet(0x8f,1);m[0xd887]=0;m[0xd7eb]|=0x80
    ok(tbl()==[0]*len(FAMS),'no replacements before any kill')
    walk_to(6,14)
    for i in range(40):
        if m[0xd057]:break
        press_('a',90)
    team=enemy();print('Tower team',[(l,hex(s)) for l,s in team])
    ok(m[0xd057]==2 and m[0xd031]==0x2a,'BLUE battle at the Tower')
    TW=m[0xd35e]
    if VERSION>=51:m[0xd35e]=0                          # GHOST refuses in the Tower since v51: fight as if elsewhere
    fight_with_curse();m[0xd35e]=TW;after_battle(30)
    t=tbl();print('table',[hex(x) for x in t])
    killed=[FAMS.index(base(s)) for l,s in team]
    ok(all(t[k] for k in killed),'every CURSEd line got a replacement (%d)'%len(killed))
    ok(all(t[k]==0 for k in range(len(FAMS)) if k not in killed),'lines that were not killed have none')
    reps=[t[k] for k in killed]
    ok(all(r in CAND for r in reps),'replacements come from the original 149 (no MEW/MEWTWO, none of BLUE\'s lines)')
    ok(len(set(base(r) for r in reps))==len(reps),'all replacements are different lines')
elif MODE in ('silph','normal','chain'):
    normal=silph()
    print('normal SILPH team',[(l,hex(s)) for l,s in normal])
    ok(m[0xd057]==2,'BLUE battle at SILPH')
    if MODE=='normal':
        R2=ROMB;ok(all(base(s) in FAMS for l,s in normal),'no kills recorded: BLUE\'s SILPH team is his original one')
    else:
        rep=0xb0 if False else [c for c in CAND if base(c)==c and stage(c,60)!=c][0]   # a line that evolves
        k=FAMS.index(PIDGEY)
        team=silph(lambda:m.__setitem__(TBL+k,rep))
        print('with replacement',hex(rep),[(l,hex(s)) for l,s in team])
        i=[j for j,(l,s) in enumerate(normal) if base(s)==PIDGEY][0]
        lv=normal[i][0]
        ok(team[i]==(lv,stage(rep,lv)) and stage(rep,lv)!=rep,'PIDGEOT\'s slot: the replacement at Lv%d, evolved to its stage (%s)'%(lv,hex(stage(rep,lv))))
        ok([x for j,x in enumerate(team) if j!=i]==[x for j,x in enumerate(normal) if j!=i],'the rest of his team is unchanged')
        if MODE=='chain':
            # make the replacement BLUE's first POKeMON out, then CURSE it
            fight_with_curse(limit=60) if False else None
            for n in range(300):
                if m[0xd057]==0 or m[TBL+k]!=rep:break
                b=clean(box())
                if 'FIGHT' in b and 'RUN' in b:
                    for kk in range(4):
                        if '▲FIGHT' in box():break
                        press_('up',20);press_('left',20)
                    press_('a',60)
                    if 'CURSE' in ' '.join(txt()):press_('a',200)
                    continue
                if 'Bring out' in b or 'change' in b.lower():press_('b',60);continue
                press_('a',90)
            new=m[TBL+k];print('after CURSE on it:',hex(rep),'->',hex(new))
            ok(new and new!=rep and new in CAND and base(new)!=base(rep),'CURSing the replacement rolls a new one (%s)'%hex(new))
elif MODE=='champion':                                    # hero-mode Champion: his MEWTWO line was CURSEd before
    rep=[c for c in CAND if base(c)==c and stage(c,70)!=c][-1];k=FAMS.index(0x83)
    load('blue_hero');m[0xd64c]=1
    prior=tbl();print('replacements already in blue_hero (earlier CURSEs in the chain):',[hex(x) for x in prior])
    m[TBL:TBL+len(FAMS)]=[0]*len(FAMS);m[TBL+k]=rep           # only the MEWTWO line replaced
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x78
    for d in ('up','down','left','right'):
        if m[0xd35e]==0x78:break
        for kk in range(8):
            if m[0xd35e]==0x78:break
            walk(d,1)
    T(60)
    for i in range(80):
        if m[0xd057]:break
        press_('a',90)
    T(200);team=enemy();print('Champion team',[(l,hex(s)) for l,s in team])
    ok(m[0xd031]==0x2b and team[5]==(70,stage(rep,70)) and 0x83 not in [s for l,s in team],'Champion: MEWTWO\'s slot holds the replacement at Lv70 (%s)'%hex(stage(rep,70)))
    ok(all(base(s) in FAMS for l,s in team[:5]),'his other five are his own')
