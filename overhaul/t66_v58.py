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
    seen.clear();use_move(0,300,in_moves=True)
    for i in range(30):
        if m[0xd057]==0:break
        press_('a',100)
    print('after bane:',allt()[-500:],m[0xd057],m[0xd05a],hex(m[0xd4ae]),hex(m[0xd4af]))
    ok(m[0xd057]==0,'the battle is over (BANE)')
    seen.clear();maps=set()
    for i in range(40):
        if box():press_('a',60)
        else:T(20)
        maps.add(m[0xd35e])
        if m[0xd876]>=3 and m[0xd35e]==0x76:break
    print('maps seen',[hex(x) for x in maps],'pos',pos(),'d876',m[0xd876],flush=True)
    ok(0x76 in maps,'the player walked into the Hall of Fame by himself')
    ok(m[0xd867]&2 and list(m[0xd863:0xd867])==flags0[:4],'the Champion is beaten; the Elite Four flags are unchanged (no reset)')
    ok(0x03 not in [m[0xc100+16*i] for i in range(1,5)],'no Oak anywhere')
    ok(m[0xc110]==0x39,'AGATHA (picture 39) is in the room')
    seen.clear()
    for i in range(120):
        if m[0xd876]==4:break
        if box():press_('a',80)
        else:T(20)
    t=allt().replace('  ',' ');print('AGATHA:',t[-300:],flush=True)
    keys=['It is done','Those fools','ancestors are smiling','not yet finished','had hoped to avoid','must be settled','How curious','given up interfering','perhaps I was mistaken','traitor of our clan','remains a threat','must be eliminated','final ritual']
    print([k for k in keys if k not in t])
    ok(all(k in t for k in keys),"AGATHA's speech")
    ok(m[0xd876]==4,'the scene is over')
    T(30)
    ok(not box() and m[0xcd6b]==0,'the player is free (no text, joypad not ignored)')
    y0=pos()[2];p.button('left',8);T(30);p.button('right',8);T(30)
    p.button('left',8);T(30)
    ok(pos()[1]!=4,'the player moves freely')
    shot('v58_agatha')
    # leave and come back: the short talk; the champion's room is quiet
    bfs_to(7,4,maxn=200)
    p.button('down',8);T(120)
    ok(m[0xd35e]==0x78,'back in the Champion\'s room')
    T(200)
    ok(m[0xd057]==0 and m[0xc110]==0 and not box(),'BLUE is gone and the cut-scene does not start again')
elif MODE=='normal':
    def setup2():lead(GHOST);m[0xd64c]=1
    warp(0x78,0,setup2)
    for i in range(30):
        if m[0xd057]:break
        press_('a',120)
    t=allt().replace('  ',' ');print('normal:',t[-300:],m[0xd46c],m[0xd64c])
    ok(m[0xd46c]==0 and 'No... BLACK' not in t and m[0xd876]==0,'GHOST route: not the BLACK speech, no stage')
