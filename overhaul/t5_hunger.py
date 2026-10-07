from harness import *
load('after_rival')
# leave the lab to Pallet
for i in range(12):
    if m[0xd35e]==0:break
    walk('down',1)
walk('right',1);walk('down',1)
print('outside',pos(),'hunger',m[0xd455],'ctr',m[0xd456])
h0=m[0xd455];c0=m[0xd456]
n=0
for d in ['right','left']*7:
    x=pos();walk(d,1)
    if pos()!=x:n+=1
print('steps',n,'hunger',m[0xd455],'ctr',m[0xd456])
assert (h0*6+ (6-c0)) - (m[0xd455]*6+(6-m[0xd456])) == n, 'drain mismatch'
print('PASS drain: 1 hunger per 6 steps')
save('pallet_with_ghost')
# --- eat test: starving next step
m[0xd455]=1;m[0xd456]=5
before=list(m[0xd164:0xd16a]);black=0;cry=set()
p.button('right',8)
for f in range(400):
    p.tick(1)
    if m[0xff47]==0xff:black+=1
    for a in range(0xc026,0xc02e):
        if m[a]:cry.add(m[a])
print('party',before,'->',list(m[0xd164:0xd16a]),'count',m[0xd163],'black frames',black,'sound ids',sorted(map(hex,cry)),'hunger',m[0xd455])
assert m[0xd163]==1 and m[0xd164]==0x1f and black>20 and m[0xd455]==12
print('PASS eat own pokemon');shot('v2_after_eat');save('only_ghost')
