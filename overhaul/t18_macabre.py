# v6: PRETA's MACABRE in a wild battle (enemy left at 1 HP, Slash animation, no crit), PP display,
# then Mom's heal (HealParty) restores MACABRE to 10 PP.
from harness import *
import random;random.seed(11)
load('v6_with_preta');party=list(m[0xd163:0xd2f7]);dex=list(m[0xd2f7:0xd31d])
load('pallet_with_ghost');m[0xd163:0xd2f7]=party;m[0xd2f7:0xd31d]=dex;m[0xd455]=255
def swap(i,j):
    for base,size in ((0xd16b,44),(0xd2b5,11),(0xd273,11)):
        a=list(m[base+size*i:base+size*(i+1)]);b=list(m[base+size*j:base+size*(j+1)])
        m[base+size*i:base+size*(i+1)]=b;m[base+size*j:base+size*(j+1)]=a
    m[0xd164+i],m[0xd164+j]=m[0xd164+j],m[0xd164+i]
swap(0,2);print('party',list(m[0xd164:0xd168]),pos());p.tick(30)
walk('left',3)
for i in range(60):
    if m[0xd35e]==0xc and pos()[2]<30:break
    a=pos();walk('up',1)
    if pos()==a:walk('right' if pos()[1]<10 else 'left',1)
print('route',pos(),flush=True)
for i in range(600):
    if m[0xd057]:break
    walk(random.choice(['up','up','down','left','right']),1);m[0xd455]=255
assert m[0xd057]==1,(pos(),box())
print('wild battle lead',hex(m[0xd014]),'enemy',hex(m[0xcfe5]),'lv',m[0xcff3],flush=True)
def hp():return m[0xcfe6]<<8|m[0xcfe7]
def to_menu():
    for i in range(40):
        if 'FIGHT' in box():return
        p.button('a' if 'nickname' not in box() else 'b',8);p.tick(120)
    raise SystemExit('FAIL no fight menu')
results=[]
for turn in range(2):
    to_menu();h0=hp()
    p.button('a',8);p.tick(40);menu=txt();shot('v6_fight_menu_%d'%turn)
    print('MOVES:',[x for x in menu[8:18] if x])
    p.button('a',8);seen=[];anims=set();crit=0
    for t in range(900):
        p.tick()
        if m[0xd05e]:crit=1
        anims.add(m[0xd07c])
        b=box()
        if b and (not seen or seen[-1]!=b):seen.append(b)
        if t==120:shot('v6_macabre_anim_%d'%turn)
        if 'FIGHT' in b and t>200:break
    lines=[s for s in seen if 'MACABRE' in s or 'ritical' in s]
    print('turn',turn,'enemy HP',h0,'->',hp(),'texts',lines[:3],'anim ids',sorted(anims)[:8],'crit',crit)
    results.append((h0,hp()))
assert results[0][1]==1 and results[1]==(1,1),results
pp=m[0xd02d]&0x3f;print('MACABRE PP in battle',pp);assert pp==8
print('PASS MACABRE leaves enemy at 1 HP')
# fight menu shows PP x/10 for MACABRE (GetMaxPP through the death-move table)
to_menu();p.button('a',8);p.tick(40);menu=' '.join(txt());print('menu:',menu[-120:]);assert '8/10' in menu.replace(' ','') or '8/ 10' in menu
print('PASS MACABRE max PP 10');p.button('b',8);p.tick(30)
# run
for i in range(20):
    if m[0xd057]==0:break
    b=box()
    if 'FIGHT' in b:p.button('down',8);p.tick(10);p.button('right',8);p.tick(10);p.button('a',8);p.tick(150)
    else:p.button('a',8);p.tick(150)
print('after battle party PP',list(m[0xd16b+29:0xd16b+33]),'HP',m[0xd16c]<<8|m[0xd16d])
save('v6_after_macabre')
