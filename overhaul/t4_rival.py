from harness import *
load('lab_arrived')
for i in range(28):
    if m[0xd5f0]==6:break
    press('a')
press('right',30);press('a',200)
for i in range(30):
    if m[0xd5f0]==9:break
    if any('nickname' in x for x in txt()):press('b')
    else:press('a')
print('party before',list(m[0xd164:0xd16a]),'hunger',m[0xd455])
p.button('down',48);p.tick(200)
for i in range(140):
    if m[0xd5f0]==10 and m[0xd057]==0:p.button('down',48);p.tick(200)
    if m[0xd5f0]==18 and m[0xd057]==0:break
    press('a',220)
save('after_rival');print('party after',list(m[0xd164:0xd16a]),'ghost flag',m[0xd451],'hunger',m[0xd455],'steps',m[0xd456])
START=67 if VERSION>=14 else 160                              # v14: GHOST starts hungrier (~400 steps)
assert m[0xd451]==1 and 0x1f in m[0xd164:0xd16a] and m[0xd455]==START;print('PASS ghost + hunger init',START)
