from harness import *
import random;random.seed(5)
load('pallet_with_ghost')
# Ghost to lead
a=list(m[0xd16b:0xd197]);b=list(m[0xd197:0xd1c3]);m[0xd16b:0xd197]=b;m[0xd197:0xd1c3]=a
m[0xd164],m[0xd165]=m[0xd165],m[0xd164]
na=list(m[0xd2b5:0xd2c0]);nb=list(m[0xd2c0:0xd2cb]);m[0xd2b5:0xd2c0]=nb;m[0xd2c0:0xd2cb]=na
oa=list(m[0xd273:0xd27e]);ob=list(m[0xd27e:0xd289]);m[0xd273:0xd27e]=ob;m[0xd27e:0xd289]=oa
for i in range(12):
    if pos()[1]<=10:break
    walk('left',1)
for i in range(30):
    if m[0xd35e]==0xc and pos()[2]<30:break
    walk('up',1)
print('route1',pos(),flush=True)
m[0xd453]=0
for i in range(600):
    if m[0xd057]:break
    walk(random.choice(['up','up','down','left','right']),1)
assert m[0xd057]==1,'no wild battle found '+str(pos())
m[0xd455]=20;m[0xd456]=0
print('wild battle at',pos(),'lead',hex(m[0xd014]),flush=True)
seen=[]
for i in range(60):
    b=box()
    if b and (not seen or seen[-1]!=b):seen.append(b)
    if i>4 and m[0xd057]==0:break
    if 'change' in b or 'Bring out' in b or 'nickname' in b:p.button('b',8)
    else:p.button('a',8)
    p.tick(200)
for s in seen:print('  TEXT:',''.join(c for c in s if c not in '│─┌┐└┘|').strip())
print('curse_used',m[0xd452],'killed flag',m[0xd453],'hunger',m[0xd455])
assert m[0xd453]==0 and m[0xd455]>=20+16;print('PASS wild Curse: fed, no murder flag')
save('after_wild')
