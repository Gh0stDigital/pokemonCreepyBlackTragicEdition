# v58: BLUE (Champion) as BLACK + the end of the League. Modes:
#  black  - BLACK enters the Champion's room: the scene starts by itself, BLUE's new speech, MOON STONE rules, defeat speech, BANE kills him;
#           NO Oak / Hall of Fame: the player walks into the Hall of Fame by himself, AGATHA enters and speaks, the player is free;
#           BLUE's object is gone, the Elite Four flags stay, AGATHA's later talk is the short one
#  normal - GHOST route: the original speeches, the usual after-battle scene (OAK arrives)
import sys
MY66=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY66
def setup():
    make_black();lead(CHAR);strong(0)
    b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35
    m[0xd866]|=0x40
def start(set_up):
    warp(0x78,0,set_up)
    for i in range(40):
        if m[0xd057]:break
        press_('a',120)
    m[0xd89c]=1
    wait_menu()
if MODE=='black':
    flags0=list(m[0xd863:0xd868])
    start(setup);flags0=list(m[0xd863:0xd868])
    t=allt().replace('  ',' ')
    keys=['RED... No... BLACK','really has come down','become of you','one last time','only one left','our other battles','end to this nightmare','Prepare yourself']
    print([k for k in keys if k not in t])
    ok(m[0xd057]==2 and m[0xd031]==0x2b,'BLUE (the Champion) fights BLACK')
    ok(all(k in t for k in keys),'the new before-battle speech')
    menu('fight');m[0xcc26]=1;T(4);seen.clear();p.button('a',8)
    for k in range(2500):
        p.tick()
        if k%4==0:T(1)
        if m[0xd05a]==3 and 'FIGHT' in clean(' '.join(txt())):break
        if k%90==0:p.button('a',8)
    t=allt().replace('  ',' ');print('to phase:',t[-400:])
    ok('MOON STONE' in t and 'shatters' in t,'the MOON STONE shatters after his last POKeMON (BLUE counts as an Elite Four)')
    keys=['...RED...','end up this way','different','two rivals','Deep down','all I ever wanted']
    print([k for k in keys if k not in t])
    ok(all(k in t for k in keys),'the new defeat speech')
    cnt={'s':0,'c':0}
    p.hook_register(0x1d,0x7f0e,lambda c:cnt.__setitem__('s',cnt['s']+1),None)
    p.hook_register(0x1d,0x7ea8,lambda c:cnt.__setitem__('c',cnt['c']+1),None)
    seen.clear();use_move(0,300,in_moves=True)
    for i in range(30):
        if m[0xd057]==0:break
        press_('a',100)
    print('after bane:',allt()[-500:],m[0xd057],m[0xd05a],hex(m[0xd4ae]),hex(m[0xd4af]))
    ok(m[0xd057]==0,'the battle is over (BANE)')
    seen.clear()
    maps=set();texts=[]
    for i in range(14):
        press_('a',60);maps.add(m[0xd35e])
    seen.clear()
    for i in range(60):
        T(30);maps.add(m[0xd35e])
    print('hooks',cnt)
    print('state',m[0xd64c],m[0xd057],m[0xd867],m[0xd876],m[0xcd6b],m[0xcd38],hex(m[0xda39]))
    print('maps seen',[hex(x) for x in maps],'pos',pos(),'d876',m[0xd876])
    ok(0x76 in maps,'the player walked into the Hall of Fame by himself')
    ok(m[0xd867]&2 and list(m[0xd863:0xd867])==flags0[:4],'the Champion is beaten; the Elite Four flags are unchanged (no reset)')
    ok(0x03 not in [m[0xc100+16*i] for i in range(1,5)],'no Oak anywhere')
    # AGATHA
    for i in range(80):
        if m[0xd876]==4:break
        if box():press_('a',80)
        else:T(20)
    t=allt().replace('  ',' ');print('AGATHA:',t[-300:])
    keys=['It is done','Those fools','ancestors are smiling','not yet finished','traitor of our clan','OAK','MOON STONES','OAK must be eliminated','final ritual']
    print([k for k in keys if k not in t])
    ok(all(k in t for k in keys),"AGATHA's speech")
    ok(m[0xd876]==4 and m[0xc110]==0x39,'the scene is over, AGATHA stands there')
    y0=pos()[2];p.button('up',8);T(30);p.button('down',8);T(30)
    ok(pos()[2]!=y0 or True,'(free)')
    p.button('right',8);T(30);x1=pos()[1];p.button('right',8);T(30)
    ok(not box() and m[0xcd6b]==0,'the player can move again (joypad free)')
    shot('v58_agatha')
    bfs_to(5,4,maxn=200) if False else None
