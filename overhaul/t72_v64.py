# v64: the secret door in the HALL OF FAME (corner y1 x0) leads to the League lobby. Modes: black (the end of the League as BLACK), normal (GHOST route)
import sys
MY72=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY72
def setup():
    if MODE=='black':
        make_black();lead(CHAR);strong(0);m[0xd866]|=0x40;m[0xd867]|=2;m[0xd876]=4
    else:lead(GHOST)
warp(0x76,0,setup)
print('arrived',pos(),flush=True)
shot('v72_hof')
ok(m[0xd35e]==0x76,'in the Hall of Fame')
if MODE=='black':bfs_to(1,1)
else:
    ok(m[0xd3ae]==3 and m[0xd3af+3]==0x78 and m[0xd3b3+3]==0x78,'GHOST route: the HALL OF FAME keeps its two original doors (+ the secret one)');print('t72 done',flush=True);sys.exit(0)
if 0:
    T(60)
    for d,n in (('up',2),('left',3)):
        for i in range(n):p.button(d,8);T(30)
print('at the corner',pos(),flush=True)
for i in range(2):p.button('left',8);T(60)         # walk into the left edge of the room: the warp (like the bottom door)
T(120)
print('after the door',pos(),flush=True)
shot('v72_lobby')
ok(m[0xd35e]==0xae,'the secret door leads to the League lobby')
ok(m[0xd362]==8 and m[0xd361]<=1,'arriving at the lobby\'s top door')
for i in range(3):
    p.button('down',8);T(30)
ok(m[0xd35e]==0xae and m[0xd361]>=2,'the player walks on in the lobby')
# and the way back: the top door leads to LORELEI's room as before
bfs_to(1,8)
p.button('up',8);T(120)
print('up from the lobby',pos(),flush=True)
ok(m[0xd35e]==0xf5,"the lobby's top door still leads to LORELEI's room")
print('t72 done',flush=True)
