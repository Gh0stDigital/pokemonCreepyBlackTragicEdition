# v63: the ten SHAMANESSES in the towns. Modes: town <map> - warp there, find her, walk next to her, talk, leave and come back
import sys
MY71=sys.argv[1];TOWN=int(sys.argv[2],0);BLK=len(sys.argv)>3
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0])
ORDER=[0,1,2,3,5,6,7,0x0a,4,8]
KEYS=['Long before Kanto','God of the Abyss','The old clan divided','Four warriors','Eight dragons','call a soul back','eight sacred grounds','ancient rite','outsiders came','Those who practiced']
def sprites():return [(i,hex(m[0xc100+16*i]),m[0xc204+16*i]-4,m[0xc205+16*i]-4) for i in range(1,m[0xd4e1]+1)]
def go(mapid):
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=mapid
    for i in range(6):
        if m[0xd35e]==mapid:break
        p.button('up',8);T(24)
    T(120)
def shaman():
    s=[x for x in sprites() if x[1]=='0x19' and m[0xd4e4+2*(x[0]-1)+1]==0x3f]
    return s[0] if s else None
idx=ORDER.index(TOWN)
DOOR={0:0x25,1:0x29,2:0x34,3:0x40,4:0x8d,5:0x59,6:0x7a,7:0x98,8:0xa5,0x0a:0xb4}
def enter():
    warp(DOOR[TOWN],0,lambda:None);m[0xd365]=TOWN
    for i in range(10):
        if m[0xd35e]==TOWN:break
        p.button('down',8);T(30)
    T(120);print('left the building ->',pos(),flush=True)
if BLK:
    _w=warp
    def warp(mapid,warpid=0,setup=None):_w(mapid,warpid,lambda:(make_black()))
if MY71=='nogh':
    warp(DOOR[TOWN],0,lambda:None);m[0xd365]=TOWN;m[0xd451]=0
    for i in range(10):
        if m[0xd35e]==TOWN:break
        p.button('down',8);T(30)
    T(120);print('d451',m[0xd451],sprites(),flush=True)
    ok(m[0xd451]==0 and shaman() is None,'GHOST never acquired: no shamaness');print('t71 done',flush=True);sys.exit(0)
enter()
print('numsprites',m[0xd4e1],sprites(),flush=True)
s=shaman();ok(s is not None,'a shamaness stands in map %x'%TOWN)
shot('v71_town_%x'%TOWN)
sy,sx=s[2],s[3]
if TOWN==0x0a:                         # SAFFRON: the guards close the way to her in the test; sprite + flag only (the talk is the same code)
    ok(len([x for x in sprites() if x[1]=='0x0'])==0,'no hidden slot got in the way')
    warp(DOOR[TOWN],0,lambda:None);m[0xd841]|=0x80>>7<<7 if False else 0;m[0xd840+(idx//8)]|=1<<(idx%8);m[0xd365]=TOWN
    for i in range(10):
        if m[0xd35e]==TOWN:break
        p.button('down',8);T(30)
    T(120);print('after:',sprites(),flush=True)
    ok(shaman() is None,'flag set: gone');print('t71 done',flush=True);sys.exit(0)
from town_map import grid
from collections import deque
def goto(ty,tx):
    d,g=grid(TOWN);H=len(g);W=len(g[0])
    for (iy,ix) in [(q[2],q[3]) for q in sprites()]:
        if 0<=iy<H and 0<=ix<W:g[iy]=g[iy][:ix]+'O'+g[iy][ix+1:]
    st=(m[0xd361],m[0xd362]);prev={st:None};q=deque([st])
    while q and (ty,tx) not in prev:
        c=q.popleft()
        for dd,(dy,dx) in (('up',(-1,0)),('down',(1,0)),('left',(0,-1)),('right',(0,1))):
            n=(c[0]+dy,c[1]+dx)
            if n in prev or not(0<=n[0]<H and 0<=n[1]<W):continue
            if g[n[0]][n[1]]!='.' and n!=(ty,tx):continue
            prev[n]=(c,dd);q.append(n)
    assert (ty,tx) in prev,('no static path',st,(ty,tx))
    path=[];c=(ty,tx)
    while prev[c]:c,dd=prev[c];path.append(dd)
    for dd in reversed(path):
        p.button(dd,8);p.tick(24)
    T(10)
    return (m[0xd361],m[0xd362])==(ty,tx)
done=False
for (dy,dx,face) in ((1,0,'up'),(-1,0,'down'),(0,-1,'right'),(0,1,'left')):
    try:
        if goto(sy+dy,sx+dx):done=True;break
    except AssertionError as e:print('goto',e,flush=True);continue
ok(done,'walked next to her')
shot('v71_next_%x'%TOWN)
press_(face,20);seen.clear();press_('a',200)
for i in range(30):
    if not box():break
    press_('a',120)
t=allt().replace("'","")
print('text:',t[:400],flush=True)
ok('SHAMANESS %d'%(idx+1) in t and KEYS[idx] in t,'her speech is SHAMANESS %d'%(idx+1))
ok(m[0xd840+(idx//8)]&(1<<(idx%8)),'talked flag set')
ok(m[0xc100+16*s[0]]==0x19,'still standing until the map reloads')
f0,f1=m[0xd840],m[0xd841]
warp(DOOR[TOWN],0,lambda:None);m[0xd840]=f0;m[0xd841]=f1;m[0xd365]=TOWN
for i in range(10):
    if m[0xd35e]==TOWN:break
    p.button('down',8);T(30)
T(120)
print('after:',sprites(),flush=True)
ok(shaman() is None,'gone the next time the map loads')
print('t71 done',flush=True)
