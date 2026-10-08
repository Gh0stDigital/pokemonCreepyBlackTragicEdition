# Builds a ready-made save for Creepy_Black_Mu_v14.gb: GHOST route (Mr. Mu answer "Trainer"), CHARMANDER starter,
# just after Oak hands over the POKeDEX. Plays the normal game scripts in the emulator from the test chain's
# after_rival state; only the walking between Pallet / Viridian is shortened with warps (the Mart parcel and Oak's
# Pokedex scenes run as in the game). Writes Creepy_Black_Mu_v14.sav (32 KiB cartridge RAM).
from harness import *
import sys
OUT=sys.argv[1] if len(sys.argv)>1 else 'Creepy_Black_Mu_v14.sav'
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
seen=[]
def T(n):
    for _ in range(n):
        p.tick();b=clean(box())
        if b and (not seen or seen[-1]!=b):seen.append(b)
def warps_to(mapid,warpid):
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=warpid;m[0xd3af+4*i+3]=mapid
def go(d,n=1):
    for _ in range(n):p.button(d,8);T(24)
import io
from collections import deque
def bfs_to(y,x,maxn=400):
    def snap():
        f=io.BytesIO();p.save_state(f);f.seek(0);return f.read()
    def rest(b):p.load_state(io.BytesIO(b))
    start=(m[0xd361],m[0xd362]);prev={start:None};st={start:snap()};q=deque([start]);mp=m[0xd35e]
    while q and (y,x) not in prev and len(prev)<maxn:
        c=q.popleft()
        for d,(dy,dx) in (('up',(-1,0)),('down',(1,0)),('left',(0,-1)),('right',(0,1))):
            n=(c[0]+dy,c[1]+dx)
            if n in prev:continue
            rest(st[c]);p.button(d,8);p.tick(24)
            if m[0xd35e]!=mp or m[0xd057] or box():continue
            if (m[0xd361],m[0xd362])==n:prev[n]=(c,d);st[n]=snap();q.append(n)
    assert (y,x) in prev,('no path',(y,x))
    path=[];c=(y,x)
    while prev[c]:c,d=prev[c];path.append(d)
    rest(st[start])
    for d in reversed(path):p.button(d,8);T(24)
    T(10)
def talk_until(cond,limit=80):
    for i in range(limit):
        if cond():return True
        p.button('a',8);T(90)
    return cond()
load('after_rival');m[0xd887]=0
print('start',pos(),'party',list(m[0xd164:0xd16a]),'Mu answer',m[0xd450])
assert m[0xd450]==1 and list(m[0xd164:0xd166])==[0xb0,0x1f]
for i in range(15):
    if m[0xd35e]==0:break
    go('down')
T(60);print('Pallet',pos())
warps_to(0x2a,0)                                             # lab door -> Viridian Mart
for i in range(4):
    if m[0xd35e]==0x2a:break
    go('up')
T(120);print('Mart',pos())
talk_until(lambda:any('PARCEL' in s for s in seen) and not box(),60)
print('mart texts',[s for s in seen if 'PARCEL' in s][:2])
m[0xd70b]|=0x02                                              # Viridian counts as visited (we skipped its streets)
for i in range(6):p.button('b',8);T(60)
print('in mart',pos(),box()[:40])
bfs_to(7,3)
for i in range(6):
    if m[0xd35e]!=0x2a:break
    go('down')
T(120);print('Pallet',pos())                                   # back out at a Pallet door
bfs_to(12,12)
for i in range(4):
    if m[0xd35e]==0x28:break
    go('up')
T(60);print('Lab',pos())
for i in range(12):
    if m[0xd361]<=3:break
    go('up')
p.button('up',8);T(30);seen.clear()
talk_until(lambda:any('POKéDEX' in s for s in seen) and not box() and m[0xcd6b]==0,120)
T(300)
print('lab texts',[s for s in seen if s.endswith(('!','.','?'))][:12])
print('bag',list(m[0xd31d:0xd31d+9]),'pos',pos())
# start menu must now show POKeDEX
p.button('start',8);T(60);menu=' '.join(txt());print('menu',clean(menu)[:80])
assert 'POKéDEX' in menu
for i in range(8):
    if '▲SAVE' in ' '.join(txt()):break
    p.button('down',8);T(30)
p.button('a',8);T(200)
p.button('a',8)
for i in range(900):
    T(1)
    if i%120==60 and 'SAVE' in seen[-1] and 'saved' not in seen[-1].lower():p.button('a',8)
assert any('saved' in s.lower() for s in seen),seen[-5:]
for i in range(4):p.button('b',8);T(60)
sram=bytes(m[bk,ad] for bk in range(4) for ad in range(0xa000,0xc000))
open(OUT,'wb').write(sram);print('wrote',OUT,len(sram))
print('party',list(m[0xd164:0xd16a]),'hunger',m[0xd455],'D450',m[0xd450],'D451',m[0xd451],'pos',pos())
print('last lab texts',[s for s in seen if s.endswith(('!','.','?'))][-6:])
# check: fresh emulator + the .sav -> CONTINUE
import harness
from pyboy import PyBoy
p.stop(save=False)
harness.p=PyBoy(ROM,window='null',sound_emulated=False);harness.p.set_emulation_speed(0);harness.m=harness.p.memory
p=harness.p;m=harness.m;data=open(OUT,'rb').read()
for bk in range(4):
    for i in range(0x2000):m[bk,0xa000+i]=data[bk*0x2000+i]
p.tick(300)
for i in range(40):
    t=' '.join(txt())
    if 'CONTINUE' in t:break
    p.button('start' if i%2 else 'a',8);p.tick(120)
p.button('a',8);p.tick(200);p.button('a',8);p.tick(400)
for i in range(10):
    if m[0xd35e]==0x28 and not box():break
    p.button('a',8);p.tick(120)
p.button('start',8);p.tick(60);menu=' '.join(txt())
print('after CONTINUE',pos(),'party',list(m[0xd164:0xd16a]),'D450',m[0xd450],'D451',m[0xd451],'hunger',m[0xd455])
assert pos()[0]==0x28 and list(m[0xd164:0xd166])==[0xb0,0x1f] and m[0xd450]==1 and m[0xd451]==1 and 'POKéDEX' in menu
print('PASS save loads: Oaks lab, CHARMANDER + GHOST, GHOST route, POKeDEX')
p.screen.image.save(qa/'save_v14_loaded.png')
