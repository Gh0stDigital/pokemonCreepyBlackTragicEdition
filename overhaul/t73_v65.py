# v65: MR. MU's first meeting in PALLET TOWN. Modes:
#  intro  - leaving the house: the player cannot move while MR. MU walks up; his new speech (no name, the TRAINER question), menu; he waits; entering
#           a building and coming back: he is gone for good (no sprite left, object off the map)
#  load   - a save loaded while he waits (state 2): he is placed at his post again
import sys
MODE=sys.argv[1]
from harness import *
import io
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:globals()['bad']=globals().get('bad',0)+1
seen=[]
def T(n):
    for _ in range(n):
        p.tick();b=' | '.join(x for x in txt()[12:] if x)
        if b and (not seen or seen[-1]!=b):seen.append(b)
def allt():return ' '.join(seen)
def mu():return (hex(m[0xc140]),m[0xc244]-4,m[0xc245]-4,m[0xc144],m[0xc146])
load('bedroom')
if MODE=='load':
    pass
p.button('right',64);p.tick(100);p.button('up',80);p.tick(200)
p.button('right',40);p.tick(200);p.button('down',80);p.tick(100);p.button('left',56);p.tick(100)
# the last step out of the house
p.button('down',40)
trace=[]
for i in range(200):
    if m[0xd35e]==0 and m[0xd454]==1 and i%2==0:p.button(['left','down','right','up'][(i//2)%4],2)     # spam the D-pad while he walks
    T(8)
    trace.append((m[0xd35e],m[0xd362],m[0xd361],m[0xd454],m[0xcd6b],mu()))
print([(x[1],x[2],x[3],x[4],x[5][1:3]) for x in trace if x[0]==0 and x[3]==1][::3],flush=True)
t0=[x for x in trace if x[0]==0 and x[3]==1]
ok(len(t0)>0,'the meeting started by itself right outside the house (D454 = 1)')
ok(len({(x[1],x[2]) for x in t0 if x[5][1]!=6 or x[5][2]!=6 or True})==1,'the player did not move at all (D-pad spammed while MR. MU walked up): %s'%sorted({(x[1],x[2]) for x in t0}))
# try to walk away while he walks
y,x=m[0xd361],m[0xd362]
for d in ('left','down','right'):p.button(d,8);p.tick(20)
ok((m[0xd361],m[0xd362])==(y,x) and m[0xd454] in (1,2),'pressing the D-pad does nothing')
for i in range(40):
    if m[0xd454]==2 or any('THE TRAINER' in z for z in txt()):break
    T(20)
shot('v73_mu')
for i in range(60):
    if any('THE TRAINER' in z for z in txt()):break
    p.button('a',8);T(60)
t=allt().replace("'","")
print('text:',t[-700:],flush=True)
keys=['Hello young lad.','Sorry to intrude','suddenly...','help but','notice...','You are about to','as a TRAINER,','You certainly','about you.','I was wondering','humor an old','question.','responsible']
print([k for k in keys if k not in t])
ok(all(k in t for k in keys),'the new speech and the question')
ok('MR. MU' not in t and 'I am' not in t,'he does not give his name')
ok(any('THE TRAINER' in z for z in txt()),'the TRAINER / POKeMON menu')
p.button('a',8);p.tick(120)               # THE TRAINER
for i in range(20):
    if m[0xd454]==2 and not box_open() if False else m[0xd454]==2:break
    p.button('a',8);p.tick(60)
T(60)
ok(m[0xd450]==1,'the answer is saved (THE TRAINER = 1)')
for i in range(10):
    p.button('b',8);p.tick(40)
ok(m[0xd454]==2 and m[0xcd6b]==0,'the player is free again; MR. MU waits')
print('mu',mu(),flush=True)
ok(m[0xc140]==0x10 and m[0xc244]-4==6,'MR. MU stands at his post')
T(200)
ok(m[0xc140]==0x10,'he stays while the player is outside')
m[0xc244]=0xff;m[0xc245]=0xff;m[0xc140]=0;T(30)          # what a loaded save looks like (the object starts off the map)
ok(mu()[:3]==('0x10',6,6),'a loaded save while he waits: he is placed at his post again')
shot('v73_post')
# enter a building (the house) and come back
p.button('up',8);p.tick(60)
for i in range(6):
    if m[0xd35e]!=0:break
    p.button('up',8);p.tick(30)
print('map',hex(m[0xd35e]),flush=True)
T(120)
ok(m[0xd454]==3,'entering a building: MR. MU is done (D454 = 3)')
m[0xd365]=0
for i in range(8):
    if m[0xd35e]==0:break
    p.button('down',8);p.tick(30)
T(150)
print('back',pos(),'mu',mu(),flush=True)
ok(m[0xd35e]==0 and m[0xc140]==0 and m[0xc244]==0xff,'back in PALLET: MR. MU is gone (picture 0, position FF)')
ok(all(m[0xc100+16*i]!=0x10 for i in range(1,m[0xd4e1]+1)),'no GENTLEMAN sprite left on the map')
shot('v73_gone')
print('t73 done',bad if 'bad' in globals() else 0,flush=True)
