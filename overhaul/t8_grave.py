from harness import *
load('after_curse');p.tick(60);shot('grave_0_after_battle')
def sprites():return [(i,hex(m[0xc100+16*i]),m[0xc204+16*i]-4,m[0xc205+16*i]-4,m[0xc102+16*i]) for i in range(1,m[0xd4e1]+1)]
print('sprites (idx,pic,y,x,img)',sprites())
walk('down',3);print('left?',pos())
for i in range(4):
    if m[0xd35e]!=0x33:break
    walk('down',1)
print('now',pos());walk('up',1);p.tick(120);print('back',pos(),'grave table',list(m[0xd4a4:0xd4ae]))
print('sprites (idx,pic,y,x,img)',sprites())
# go look at trainer 2's original spot
shot('grave_1_reentered')
