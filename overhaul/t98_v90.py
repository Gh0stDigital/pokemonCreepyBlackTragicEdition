# v90: BROCK's after-battle dialogue (PEWTER GYM). Modes:
#  kill  - GHOST CURSEs and kills him: "<PLAYER> took the BOULDERBADGE from BROCK's body.", badge + TM34 in the bag, murder
#  spare - GHOST CURSEs his team but RUNs in the trainer phase: a shaken BROCK ("Please. Take this and go."), TM34, no murder
#  win   - CHARMANDER wins normally: the original "Wait! Take this with you!" and the TM34 lecture
import sys
MY98=sys.argv[1]
sys.argv=['x','none'];exec(open('t28_v14.py').read().split("if MODE=='mirage_rate':")[0].replace("MODE=sys.argv[1]","MODE='x'"))
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
CHAR=0xb0
def strong(i):
    b=0xd16b+44*i
    m[b+14]=0x10;m[b+15]=0x2c;m[b+16]=0x14;m[b+33]=100;m[b+3]=100;m[b+1]=3;m[b+2]=0xe7;m[b+34]=3;m[b+35]=0xe7
    for j in range(4):m[b+36+2*j]=3;m[b+37+2*j]=0xe7
warp_from_pallet(0x36,0);m[0xd887]=0
if MY98=='win':lead(CHAR);strong(0)
m[0xd755]|=0x04
walk_to(2,4);p.button('up',8);T(20);seen.clear()
for i in range(30):
    if m[0xd057]:break
    press_('a',60)
m[0xd755]&=~0x04
ok(m[0xd057]==2 and m[0xd031]==34,'BROCK battle')
def fight_win(limit=400):
    for i in range(limit):
        if m[0xd057]==0:return
        b=clean(box())
        if 'FIGHT' in b and 'RUN' in b:
            for k in range(4):
                if '▲FIGHT' in box():break
                press_('up',20);press_('left',20)
            press_('a',60);press_('a',200);continue
        if 'Bring out' in b or 'change' in b.lower():press_('b',60);continue
        press_('a',90)
if MY98=='win':fight_win()
else:fight(spare=(MY98=='spare'))
for i in range(40):press_('a',90)
def fin(master):
    out=[]
    for i,x in enumerate(master):
        if i+1<len(master) and len(master[i+1])>len(x) and master[i+1].startswith(x.rstrip('▼ ')):continue
        out.append(x)
    return ' | '.join(out)
T_=fin(seen);print('TEXT',T_[-1200:],flush=True)
bag=list(m[0xd31e:0xd31e+2*m[0xd31d]])
print('murder',m[0xd453],'badge',m[0xd356]&1,'TM34',0xea in bag[::2],'D455 d755',bin(m[0xd755]),flush=True)
if MY98=='kill':
    ok('took the' in T_ and 'BOULDERBADGE' in T_ and "body" in T_,'killed: "took the BOULDERBADGE from BROCK\'s body."')
    ok(m[0xd453]==1 and m[0xd356]&1 and 0xea in bag[::2],'murder, badge, TM34 in the bag')
    ok('Take this with you' not in T_ and 'Please' not in T_,'no cheerful / shaken lines')
elif MY98=='spare':
    ok('Please. Take' in T_ and 'Take that thing' in T_ and 'BIDE' in T_,'spared after CURSE: the shaken BROCK')
    ok(m[0xd453]==0 and m[0xd356]&1 and 0xea in bag[::2],'no murder, badge, TM34 in the bag')
    ok('Take this with you' not in T_,'not the cheerful line')
    ok('everyone fears' in T_ and 'all kinds of trainers' not in T_,'his later talk: the shaken advice (not the cheerful one)')
else:
    ok('Take this with you' in T_,'normal win: the original "Wait! Take this with you!"')
    ok('all kinds of trainers' in T_ and 'everyone fears' not in T_,'his later talk: the original advice')
    ok('Please. Take' not in T_ and 'took the' not in T_ and m[0xd453]==0 and m[0xd356]&1 and 0xea in bag[::2],'no shaken line, badge + TM34')
