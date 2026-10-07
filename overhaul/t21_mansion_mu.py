# v8: after receiving PRETA and leaving the trade house, Mr. Mu is gone from it and waits in Pokemon Mansion 1F.
from harness import *
def talk(n=40):
    lines=[];empty=0;p.button('a',8);p.tick(60)
    for i in range(n):
        b=box()
        if b and (not lines or lines[-1]!=b):lines.append(b)
        if not b:
            empty+=1
            if empty>2:break
        else:empty=0
        p.button('a',8);p.tick(60)
    return [''.join(c for c in l if c not in '│─┌┐└┘|').strip() for l in lines]
# before: Mansion without PRETA -> no Mu
load('pallet_with_ghost')
for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0xa5
for i in range(6):
    if m[0xd35e]==0xa5:break
    walk('up',1)
p.tick(120);print('mansion (no PRETA)',pos(),'D460',m[0xd460],'mu pic',m[0xc140],[hex(m[0xc100+16*s]) for s in range(5)])
assert m[0xd35e]==0xa5 and m[0xc140]==0;print('PASS no Mu in Mansion before PRETA')
# after PRETA
load('v6_with_preta')
for i in range(4):p.button('b',8);p.tick(60)
print('trade house',pos(),'D460',m[0xd460],'mu pic',hex(m[0xc130]));assert m[0xd460]==2 and m[0xc130]==0x10
for i in range(6):
    if m[0xd35e]!=0x3f:break
    walk('down',1)
p.tick(120);print('outside',pos(),'D460',m[0xd460]);assert m[0xd35e]!=0x3f and m[0xd460]==3;print('PASS Mu state -> 3 on leaving')
for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x3f
walk('up',1);p.tick(120);print('back inside',pos(),'mu pic',m[0xc130],'y/x',m[0xc234],m[0xc235]);shot('v8_house_empty')
assert m[0xd35e]==0x3f and m[0xc130]==0;print('PASS Mu gone from trade house')
for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0xa5
for i in range(6):
    if m[0xd35e]==0xa5:break
    walk('down',1)
p.tick(120);print('mansion',pos(),'mu pic',hex(m[0xc140]),'y/x',m[0xc244]-4,m[0xc245]-4)
assert m[0xd35e]==0xa5 and m[0xc140]==0x10
m[0xd887]=0                                                    # no wild encounters while walking to him
for i in range(5):walk('up',1)
walk('right',2);p.button('up',8);p.tick(30);print('at',pos());shot('v8_mansion_mu')
t=talk();print('TEXT:',t);assert any('mansion' in x for x in t);print('PASS Mu talks in Mansion 1F')
