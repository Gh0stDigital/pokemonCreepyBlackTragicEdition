# v6: Mom's heal (HealParty) restores MACABRE to its 10 max PP.
from harness import *
load('v6_after_macabre');print('start',pos(),'PP',list(m[0xd16b+29:0xd16b+33]))
def step(d):
    m[0xd0db]=200;a=pos();walk(d,1);return pos()!=a
for i in range(80):
    if m[0xd35e]==0 and pos()[2]>=6:break
    if not step('down'):step('left' if pos()[1]>11 else 'right')
print('pallet',pos())
for i in range(12):
    if pos()[1]<=5:break
    if not step('left'):step('down')
for i in range(6):
    if m[0xd35e]==0x25:break
    step('up')
p.tick(60);print('house',pos());assert m[0xd35e]==0x25
# Mom: find her sprite and walk next to her
mom=[(m[0xc204+16*s]-4,m[0xc205+16*s]-4) for s in range(1,4) if m[0xc100+16*s]]
print('sprites',mom)
my,mx=mom[0]
for i in range(6):
    if pos()[1]>=mx:break
    step('right')
for i in range(6):
    if pos()[2]<=my+1:break
    step('up')
p.button('up',8);p.tick(30);print('at',pos(),'mom x/y',mx,my)
seen=[]
for i in range(30):
    p.button('a',8);p.tick(120);b=box()
    if b and (not seen or seen[-1]!=b):seen.append(b)
print('TEXT:',[s[-40:] for s in seen][:6])
pp=list(m[0xd16b:0xd16b+44])[29:33];print('PP after Mom',pp,'species',hex(m[0xd164]))
assert pp==[10,30,15,15];print('PASS HealParty restores MACABRE to 10 PP')
