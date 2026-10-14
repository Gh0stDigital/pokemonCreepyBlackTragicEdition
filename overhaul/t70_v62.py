# v62: CERULEAN CAVE: PROF. OAK. Modes:
#  scene  - BLACK, D876 = 6: OAK stands where MEWTWO waits; talking plays the white-screen scene (no music), his speech, then the battle
#           (name PROF.OAK, his picture, the six POKeMON, forbidden moves refused with his line); BANE kills him; D876 = 7, the end starts
#  normal - not BLACK / D876 < 6: MEWTWO is as before
import sys
MY70=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY70
def setup():
    make_black();lead(CHAR);strong(0)
    b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35
    m[0xd867]|=2;m[0xd876]=6
def to_oak():
    bfs_to(13,26,maxn=2000);p.button('right',8);T(30)
if MODE=='scene':
    warp(0xe3,0,setup)
    to_oak()
    print('at',pos(),'objects',[(i,hex(m[0xc100+16*i]),m[0xc204+16*i]-4,m[0xc205+16*i]-4) for i in range(1,4)],flush=True)
    ok(m[0xc110]==3,'object 1 is OAK (picture 3)')
    shot('v70_oak_cave')
    seen.clear();press_('a',60)
    mus=[]
    for i in range(30):
        T(10)
        if i==6:shot('v70_scene');mus.append(m[0xcfca])
        if box():break
    print('scene: pic?','last music',hex(m[0xcfca]),flush=True)
    t=allt().replace('  ',' ')
    for i in range(70):
        if m[0xd057]:break
        if box():press_('a',80)
        else:T(20)
    t=allt().replace('  ',' ');print('speech:',t[-300:],flush=True)
    keys=['So youve found me','BILL would buy me','Forgive me','mistakes','I was a fool','ambitions of that clan','gave the LEAGUE','mountain goddess','ocean god','BLUE must have failed',"MEWTWO",'one chance left',"I'm sorry",'make things right','fix everything']
    print([k for k in keys if k not in t.replace("'","")])
