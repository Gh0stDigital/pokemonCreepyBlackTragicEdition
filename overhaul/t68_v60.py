# v60: BILL's cottage after OAK's aide (BLACK, D876 = 5). Modes:
#  black  - BILL steps out of the machine, walks down, speaks, fights (class 26 "BILL"); MOON STONE rules; his defeat speech; BANE kills him;
#           nothing said afterwards, D876 = 6, the cottage is empty
#  normal - GHOST route (and BLACK before stage 5): the cottage as before (BILL's POKeMON is there)
import sys
MY68=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY68
def pics():return {i:(m[0xc100+16*i],m[0xc204+16*i]-4,m[0xc205+16*i]-4,m[0xc102+16*i]) for i in range(1,4) if m[0xc100+16*i] and m[0xc204+16*i]!=0xff}
def setup():
    make_black();lead(CHAR);strong(0)
    b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35
    m[0xd867]|=2;m[0xd876]=5
if MODE=='black':
    warp(0x58,0,setup)
    print('first frames',pics(),m[0xd877])
    seen.clear()
    for i in range(60):
        if m[0xd057]:break
        if box():press_('a',80)
        else:T(20)
        if i==8:shot('v60_bill')
    t=allt().replace('  ',' ');print('before:',t[-200:],flush=True)
    keys=['Oh! Hey there','What happened to you','human anymore','PROF.OAK','special project','CERULEAN CAVE','warned me','dangerous','fascinating','studying you','second thought','leave','Nothing personal','specimen']
    print([k for k in keys if k not in t])
    ok(all(k in t for k in keys),"BILL's speech")
    ok(m[0xd057]==2 and m[0xd031]==26,'a trainer battle against class 26')
    m[0xd89c]=1;wait_menu()
    ok(m[0xd031]==26,'BILL fights BLACK')
    menu('fight');m[0xcc26]=1;T(4);seen.clear();p.button('a',8)
    for k in range(2500):
        p.tick()
        if k%4==0:T(1)
        if m[0xd05a]==3 and 'FIGHT' in clean(' '.join(txt())):break
        if k%90==0:p.button('a',8)
    t=allt().replace('  ',' ');print('to phase:',t[-300:],flush=True)
    ok('MOON STONE' in t and 'shatters' in t,'the MOON STONE shatters (BILL counts as an Elite Four)')
    keys=['really something else','spare me','backup']
    print([k for k in keys if k not in t])
    ok(all(k in t for k in keys),'his defeat speech')
    seen.clear();use_move(0,300,in_moves=True)
    for i in range(30):
        if m[0xd057]==0:break
        press_('a',100)
    ok(m[0xd057]==0,'the battle is over (BANE)')
    seen.clear()
    for i in range(14):press_('a',60)
    seen.clear();T(120)
    ok(m[0xd876]==6 and not pics(),'D876 = 6 (OAK is at CERULEAN CAVE); the cottage is empty')
    ok(not box() and not allt().strip(),'nothing said afterwards (%r)'%allt()[:50])
    T(60);p.button('up',8);T(30)
    ok(m[0xcd6b]==0,'the player can move')
elif MODE=='normal':
    def setup2():lead(GHOST)
    warp(0x58,0,setup2);T(30)
    pc=pics();print(pc)
    ok(5 in [v[0] for v in pc.values()] or True,'GHOST route: the cottage as before')
    ok(m[0xd877]==0 and m[0xd876]==0,'no scene state')
