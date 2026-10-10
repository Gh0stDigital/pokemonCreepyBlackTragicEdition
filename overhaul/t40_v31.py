# v31: GHOST deposited for a MIRAGE battle comes back to slot 1 if it led; otherwise last as before. Modes: lead / second
from harness import *
import random,sys
MODE=sys.argv[1];random.seed(11)
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:sys.exit(1)
def party():return list(m[0xd164:0xd164+m[0xd163]])
def nick(i):return bytes(m[0xd2b5+11*i:0xd2b5+11*i+11])
load('pallet_with_ghost');m[0xd455]=200;m[0xd45c]=200
sp=party();g=sp.index(0x1f)
want_lead=MODE=='lead'
if (g==0)!=want_lead:                                   # swap slots 0 and 1 (all four tables)
    for base,n in ((0xd164,1),(0xd16b,44),(0xd273,11),(0xd2b5,11)):
        a=list(m[base:base+n]);b=list(m[base+n:base+2*n]);m[base:base+n]=b;m[base+n:base+2*n]=a
# a third member (copy of the other one, renamed "A") so the order of the others can be checked
o=[i for i in range(len(party())) if party()[i]!=0x1f][0];n=m[0xd163]
for base,sz in ((0xd16b,44),(0xd273,11),(0xd2b5,11)):m[base+sz*n:base+sz*n+sz]=list(m[base+sz*o:base+sz*o+sz])
m[0xd164+n]=m[0xd164+o];m[0xd164+n+1]=0xff;m[0xd163]=n+1;m[0xd2b5+11*n]=0x80;m[0xd2b5+11*n+1]=0x50
for i in range(m[0xd163]):                              # the others fainted before the MIRAGE: the cleanup keeps them
    if m[0xd164+i]!=0x1f:m[0xd16c+44*i]=0;m[0xd16d+44*i]=0
before=party();others=[nick(i) for i in range(len(before)) if before[i]!=0x1f]
print('party before',[hex(x) for x in before])
import io
from collections import deque
def bfs_to(y,x,maxn=900):
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
            if m[0xd35e]!=mp or m[0xd057]:continue
            if (m[0xd361],m[0xd362])==n:prev[n]=(c,d);st[n]=snap();q.append(n)
    assert (y,x) in prev,('no path',(y,x))
    path=[];c=(y,x)
    while prev[c]:c,d=prev[c];path.append(d)
    rest(st[start])
    for d in reversed(path):p.button(d,8);p.tick(24)
m[0xd455]=255
bfs_to(0,10)                                            # Pallet's north exit
for i in range(8):
    walk('up',1)
    if m[0xd35e]==0xc and pos()[2]<30:break
print('on Route 1',pos(),flush=True)
def run_out():
    for i in range(80):
        b=box()
        if m[0xd057]==0:return
        if 'FIGHT' in b and 'RUN' in b:p.button('down',8);p.tick(10);p.button('right',8);p.tick(10);p.button('a',8);p.tick(150)
        else:p.button('a',8);p.tick(150)
dep=None;battles=0
print('start pos',pos(),flush=True)
for step in range(3000):
    if m[0xd057]:
        p.tick(30);battles+=1
        if m[0xd45d]:dep=m[0xd45f];break
        run_out();m[0xd455]=200;continue
    walk_in(0xc,random.choice(['up','down','left','right']))
ok(dep is not None,'a MIRAGE battle started (after %d battles, pos %s)'%(battles,pos()))
ok(dep==(2 if want_lead else 1),'the deposit remembered the slot (D45F = %d)'%dep)
seen=[]
for i in range(200):                                     # MIRAGE: bring out the stand-in, then RUN (65 %) until it works
    b=box()
    if b and (not seen or seen[-1]!=b):seen.append(b)
    if m[0xd057]==0:break
    if 'Bring out' in b:p.button('down',8);p.tick(30);p.button('a',8);p.tick(200)
    elif 'FIGHT' in b and 'RUN' in b:p.button('down',8);p.tick(10);p.button('right',8);p.tick(10);p.button('a',8);p.tick(200)
    else:p.button('a',8);p.tick(120)
print('battle texts',[x.replace('│','').strip()[:40] for x in seen][-6:])
p.tick(200)
after=party();print('party after',[hex(x) for x in after])
ok(m[0xd057]==0 and 0x1f in after,'the battle is over and GHOST is back')
if want_lead:ok(after[0]==0x1f,'GHOST led before, so it is in slot 1 again')
else:ok(after[-1]==0x1f,'GHOST was not leading: it comes back last as before')
left=[nick(i) for i in range(len(after)) if after[i]!=0x1f]
it=iter(others)
ok(all(x in it for x in left),'the other Pokemon kept their order (%d of %d survived the MIRAGE)'%(len(left),len(others)))
print('v31 %s: ALL PASS'%MODE)
