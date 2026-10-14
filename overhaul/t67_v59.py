# v59: OAK'S LAB after the League (BLACK, D876 >= 4): empty but for a hiding aide in the lower-left corner; his fear speech; D876 = 5.
#  black  - as above; at D876 = 3 (League not finished) or on the GHOST route the lab is as before
import sys
MY67=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY67
def pics():return {i:(m[0xc100+16*i],m[0xc204+16*i]-4,m[0xc205+16*i]-4) for i in range(1,12) if m[0xc100+16*i] and m[0xc204+16*i]!=0xff}
def lab(stage,black=True):
    def setup():
        make_black();m[0xd867]|=2;m[0xd876]=stage
        if not black:m[0xd46c]=0
    warp(0x28,0,setup);T(60)
if MODE=='black':
    lab(4)
    pc=pics();print('visible',pc)
    ok(list(pc.keys())==[10] and pc[10][0]==0x20,'the lab is empty but for one researcher (object 10)')
    print('at',pc[10][1:])
    ok(pc[10][1:]==(10,0),'he hides in the lower-left corner (10,0)')
    shot('v59_lab')
    bfs_to(10,1,maxn=300);p.button('left',8);T(30);seen.clear();press_('a',60)
    for i in range(40):
        if box():press_('a',70)
        else:T(20)
        if m[0xd876]==5:break
    for i in range(10):
        if box():press_('a',70)
    t=allt().replace('  ',' ');print('AIDE:',t[-300:])
    keys=["hurt me","Everyone fled","PROF.OAK","not here","BILL","CERULEAN CITY","finishing a project","all I know","want to die"]
    print([k for k in keys if k not in t])
    ok(all(k in t for k in keys),"the aide's speech")
    ok(m[0xd876]==5,'D876 = 5 (OAK is at BILL\'s)')
    lab(3);pc=pics();ok(len(pc)>=6,'League not finished (stage 3): the lab is as before (%d people)'%len(pc))
    lab(4,black=False);pc=pics();ok(len(pc)>=6,'GHOST route: the lab is as before (%d people)'%len(pc))
