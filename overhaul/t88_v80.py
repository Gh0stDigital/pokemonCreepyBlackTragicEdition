# v80: as BLACK ordinary alive trainers speak scared (before and after the battle); not BLACK: the usual text
import sys,re
MY=sys.argv[1]
src0=open('t77_v69.py').read().split("for MAP,SPR in")[0]
sys.argv=['x',MY]
exec(src0.replace("MY=sys.argv[1]","MY=sys.argv[1]"))
b=open('build_v80.py',encoding='utf-8').read()
b=b[b.index('PRE=['):b.index('tx=bytearray')]
FR=[s for s in re.findall(r'"([^"]*)"',b) if len(s)>=9]
def scared(t):return any(f in t for f in FR)
for MAP,SPR in ((0x0e,2),(0x0f,2)):
    print('=== map',hex(MAP),'sprite',SPR,flush=True)
    warp_from_pallet(MAP,0);m[0xd887]=0
    m[0xd16b+1]=1;m[0xd16b+2]=0x2c;m[0xd16b+34]=1;m[0xd16b+35]=0x2c
    if MY=='black':m[0xd46c]=1
    t=talk_up(SPR)
    print('before:',t[-200:],flush=True)
    ok(m[0xd057]!=0,'battle still starts')
    if MY=='black':ok(scared(t),'BLACK: scared line before the battle')
    else:ok(not scared(t),'not BLACK: usual text')
    fight(limit=1500,hp1=True,spare=True)
    for k in range(10):press_('b',60)
    ok(m[0xd057]==0,'trainer does not challenge again')
    t=talk_up(SPR);print('after:',t[-200:],flush=True)
    if MY=='black':ok(scared(t),'BLACK: scared line after the battle')
    else:ok(not scared(t),'not BLACK: usual after text')
print('t88 done',flush=True)
