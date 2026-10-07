from harness import *
import sys
branch=sys.argv[1] if len(sys.argv)>1 else 'trainer'
load('choice');p.tick(120)
if branch=='pokemon':press('down',30)
press('a')
for i in range(10):
    if m[0xd454]==2 and not box():break
    press('a')
print(branch,'answer',m[0xd450],'state',m[0xd454]);assert m[0xd450]==(1 if branch=='trainer' else 2)
save(branch+'_pallet')
p.button('up',16);p.tick(250);print('inside',pos(),m[0xd454])
p.button('down',24);p.tick(200);print('returned',pos(),m[0xd454],'mu pic',m[0xc140])
assert m[0xd454]==3;save(branch+'_returned');print('PASS',branch)
