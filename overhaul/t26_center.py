# v13: Pokemon Center visit all the way through the nurse's goodbye (froze since v1), GHOST kept out of the heal
# (same party slot afterwards), and a Poke Mart visit (same broken hook).
from harness import *
import sys
MODE=sys.argv[1] if len(sys.argv)>1 else 'center'
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
load('v6_after_macabre');pt=list(m[0xd163:0xd2f7]);dx=list(m[0xd2f7:0xd31d])
load('pallet_with_ghost');m[0xd163:0xd2f7]=pt;m[0xd2f7:0xd31d]=dx;m[0xd455]=255
# party PRETA, GHOST, CHARMANDER -> put GHOST in the middle of three so the slot restore is visible
for i in range(3):s=0xd16b+44*i;m[s+1]=0;m[s+2]=5
order=list(m[0xd164:0xd168]);nicks=[list(m[0xd2b5+11*i:0xd2b5+11*i+5]) for i in range(3)]
print('party',order,'HP',[m[0xd16c+44*i]<<8|m[0xd16d+44*i] for i in range(3)])
mapid=0x29 if MODE=='center' else 0x38
for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=mapid
for i in range(6):
    if m[0xd35e]==mapid:break
    walk('up',1)
p.tick(120);print('map',pos())
for i in range(8):
    if pos()[2]<=(4 if MODE=='center' else 5):break
    walk('up',1)
if MODE=='mart':walk('left',2)
p.button('up' if MODE=='center' else 'left',8);p.tick(30);print('at',pos())
seen=[];maxcount=0;mincount=9
for i in range(80):
    b=clean(box())
    if b and (not seen or seen[-1]!=b):seen.append(b)
    if 'fighting' in b or 'POKéMON back' in b:mincount=min(mincount,m[0xd163])
    if MODE=='mart' and ('BUY' in b and 'SELL' in b):p.button('down',8);p.tick(20);p.button('down',8);p.tick(20)   # QUIT
    if MODE=='center' and 'again' in b:
        for k in range(4):p.button('b',8);p.tick(60)
        break
    p.button('a' if i<60 else 'b',8)
    for _ in range(30):
        p.tick()
        if m[0xd163]<mincount:mincount=m[0xd163];shot('v13_heal_machine')
    if MODE!='center' and i>20 and not b:break
p.tick(120)
shot('v13_center_end');print('box at end',repr(clean(box())),'joyignore',hex(m[0xcd6b]));before=pos();walk('down',1);print('after walking',pos(),'(game still running)');assert pos()!=before,'player cannot move'
print('TEXT:',[s for s in seen if s.endswith('!') or s.endswith('▼') or s.endswith('?')][:10])
hp=[m[0xd16c+44*i]<<8|m[0xd16d+44*i] for i in range(3)]
print('party',list(m[0xd164:0xd168]),'count',m[0xd163],'HP',hp,'nicks same',[list(m[0xd2b5+11*i:0xd2b5+11*i+5]) for i in range(3)]==nicks)
assert m[0xd163]==3 and list(m[0xd164:0xd168])==order
if MODE=='center':
    gi=order.index(0x1f);ci=order.index(0xb0);pi=order.index(0xb6)
    assert hp[gi]==5 and hp[pi]==5 and hp[ci]>5 and any('see you again' in s or 'again' in s for s in seen)
    print('lowest party count during the heal',mincount);assert mincount==2
    print('PASS Pokemon Center: no freeze after the goodbye, GHOST kept out (back in slot %d), PRETA skipped, CHARMANDER healed'%gi)
else:
    print('PASS Poke Mart: no freeze after the clerk\'s goodbye')
