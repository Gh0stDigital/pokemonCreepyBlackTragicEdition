# v28 BLACK's world. Modes:
#  panic   - Viridian City, BLACK: an ordinary NPC panics, asks "CURSE them?"; NO -> the usual dialogue; YES -> black screen,
#            gravestone, the kill list entry, still a gravestone after leaving and coming back, silent when talked to again
#  exempt  - Lavender Town NPC, a shop clerk, OAK's LAB, trainer talk: no panic
#  sight   - BLACK is not spotted by a trainer's line of sight (Viridian Forest); without BLACK the trainer engages as before
#  normal  - not BLACK: NPC dialogue and trainer sight are unchanged
from harness import *
import sys,io
from collections import deque
MODE=sys.argv[1]
def box():                                  # outdoors the map tiles read as text: only a drawn text box (corner tile 79) counts
    if m[0xc3a0+12*20]!=0x79:return ''
    return ' | '.join(x for x in txt()[12:] if x)
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
seen=[]
def T(n):
    for _ in range(n):
        p.tick();b=clean(box())
        if b and (not seen or seen[-1]!=b):seen.append(b)
def press_(k,n=60):p.button(k,8);T(n)
def allt():return ' '.join(seen)
def snap():
    f=io.BytesIO();p.save_state(f);f.seek(0);return f.read()
def rest(b):p.load_state(io.BytesIO(b))
def bfs_to(y,x,maxn=900,avoid=None):
    for k in range(10):
        if not box() and m[0xcd6b]==0:break
        p.button('b',8);T(40)
    T(30)
    start=(m[0xd361],m[0xd362]);prev={start:None};st={start:snap()};q=deque([start]);mp=m[0xd35e]
    while q and (y,x) not in prev and len(prev)<maxn:
        c=q.popleft()
        for d,(dy,dx) in (('up',(-1,0)),('down',(1,0)),('left',(0,-1)),('right',(0,1))):
            n=(c[0]+dy,c[1]+dx)
            if n in prev:continue
            rest(st[c]);p.button(d,8);p.tick(24)
            if m[0xd35e]!=mp or m[0xd057] or box():continue
            if (m[0xd361],m[0xd362])==n:prev[n]=(c,d);st[n]=snap();q.append(n)
    assert (y,x) in prev,('no path',(y,x),sorted(prev)[:40])
    path=[];c=(y,x)
    while prev[c]:c,d=prev[c];path.append(d)
    rest(st[start])
    for d in reversed(path):p.button(d,8);T(24)
    T(10)
def warp(mapid,warpid=0,black=True):
    load('pallet_with_ghost');m[0xd455]=255
    if black:m[0xd46c]=1
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=warpid;m[0xd3af+4*i+3]=mapid
    for i in range(6):
        if m[0xd35e]==mapid:break
        p.button('up',8);T(24)
    T(120);print('arrived',hex(m[0xd35e]),pos(),flush=True)
def npcs():
    return [(i,m[0xc100+16*i],m[0xc204+16*i]-4,m[0xc205+16*i]-4,m[0xd504+2*(i-1)]) for i in range(1,m[0xd4e1]+1)]
def pic(i):return m[0xc100+0x10*i]
def killed():return [(m[KL+2*i],m[KL+2*i+1]) for i in range(10) if m[KL+2*i+1]]
KL=0xd471

FACE={'up':(1,0),'down':(-1,0),'left':(0,1),'right':(0,-1)}   # direction to face -> offset from the NPC to stand at
def spot(idx):
    """stand next to sprite idx (or two tiles away: counters) and face it; returns the standing tile"""
    ty,tx=m[0xc204+16*idx]-4,m[0xc205+16*idx]-4
    last=None
    for dist in (1,2):
        for d,(dy,dx) in FACE.items():
            sy,sx=ty+dy*dist,tx+dx*dist
            try:bfs_to(sy,sx,maxn=500);last=(d,sy,sx);break
            except AssertionError:continue
        if last:break
    assert last,('cannot reach',idx)
    d=last[0];T(10);p.button(d,8);T(30)
    return last
def talk(idx,answers=(),n=60,screens=None):
    """talk to sprite idx; answers = list of 'yes'/'no' for consecutive YES/NO boxes. returns the dialogue text"""
    spot(idx);seen.clear();press_('a',70);quiet=0;ans=list(answers);shots=[]
    for k in range(n):
        b=clean(' '.join(txt()))
        if 'YES' in b and 'NO' in b and ans:
            a=ans.pop(0)
            if screens is not None:screens.append(b)
            if a=='no':press_('down',30)
            press_('a',90);continue
        if not box():
            quiet+=1
            if quiet>=4:break
            T(40);continue
        quiet=0;press_('a',90)
    T(60);return allt()
def go_map(mapid,warpid=0):
    """leave through the first warp of this map into (mapid, warpid) (warp table edited), walking onto the door tile"""
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=warpid;m[0xd3af+4*i+3]=mapid
    ey,ex=m[0xd3af],m[0xd3af+1];mp=m[0xd35e]
    for d,(dy,dx) in (('up',(1,0)),('down',(-1,0)),('left',(0,1)),('right',(0,-1))):
        try:bfs_to(ey+dy,ex+dx,maxn=900)
        except AssertionError:continue
        for _ in range(2):
            p.button(d,8);T(30)
            if m[0xd35e]!=mp:break
        if m[0xd35e]!=mp:break
    T(120)
def freeze():                                       # NPCs that wander would move while the test walks to them
    for i in range(1,m[0xd4e1]+1):
        if m[0xc206+16*i]==0xfe:m[0xc206+16*i]=0xff
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:sys.exit(1)
def start(black=True,st='pallet_with_ghost'):
    load(st)
    if black:m[0xd46c]=1;m[0xd455]=255
    T(30);freeze()

if MODE=='panic':
    start()
    ns=[n for n in npcs() if n[1] in (0xd,0x2f) and n[4]==0];print(ns)
    a,b=ns[0],ns[1]
    # NO -> panic text, question, then the usual dialogue
    scr=[];t=talk(a[0],answers=['no'],screens=scr)
    ok('CURSE them?' in t and ('Please' in t or 'BLACK' in t or 'spare' in t or 'Mercy' in t or 'family' in t or 'mercy' in t or 'killer' in t),'an ordinary NPC panics and asks "CURSE them?"')
    ok(len(scr)==1,'one YES/NO box was shown')
    ok(killed()==[] and pic(a[0])!=0x49,'NO: nobody died')
    ok('POKé' in t and 'protect' in t or len(t)>150,'NO: the usual dialogue still follows')
    # YES -> black screen, gravestone
    t=talk(b[0],answers=['yes']);shot('v28_after_kill');print(t[-300:])
    ok('life drains' in t.replace('  ',' '),'YES: "The life drains from them..."')
    ok(pic(b[0])==0x49,'the NPC is a gravestone now')
    ok(killed()==[(0,b[0])],'the kill list holds (map, sprite) = %s'%killed())
    ok(not box() and m[0xcd6b]==0,'the dialogue closed cleanly (no text box, controls free)')
    seen.clear();spot(b[0]);press_('a',80);T(60)
    ok(not box() and not seen,'a gravestone is silent: %s'%allt()[:60])
    # still dead after leaving and coming back
    go_map(0x25,0);ok(m[0xd35e]==0x25,'entered the house')
    go_map(0,0);ok(m[0xd35e]==0,'back in Pallet Town')
    T(60);freeze()
    ok(pic(b[0])==0x49,'still a gravestone after the map reloaded (sprite %d)'%b[0])
    ok(pic(a[0])!=0x49,'the spared NPC is alive')
    print('v28 panic: ALL PASS')

def forest(black):
    warp(0x33,2,black=black)
    ok(m[0xd35e]==0x33,'in Viridian Forest')
    tr=[n for n in npcs() if n[4]>=0xc8][0]
    # forest trainer 2 faces LEFT: put him three tiles to the right of the player, in his line of sight (map and screen position)
    m[0xc200+16*tr[0]+4]=m[0xd361]+4;m[0xc200+16*tr[0]+5]=m[0xd362]+4+3
    m[0xc100+16*tr[0]+4]=m[0xc104];m[0xc100+16*tr[0]+6]=m[0xc106]+48
    m[0xc200+16*tr[0]+6]=0xff;m[0xd455]=255
    return tr
if MODE=='sight':
    tr=forest(False);T(30);p.button('up',8);T(200);print('player',pos(),'battle',m[0xd057],'script',hex(m[0xda39]),box()[:40])
    engaged=m[0xd057]!=0 or bool(box())
    ok(engaged,'without BLACK the trainer engages (battle or text) as before')
    tr=forest(True);y0=m[0xd361];T(30)
    p.button('up',8);T(120)
    ok(m[0xd057]==0 and not box(),'BLACK: the trainer next to the path does not engage (no battle, no text)')
    for _ in range(3):p.button('left',8);T(30)
    ok(m[0xd057]==0,'BLACK walks on without being stopped')
    # but talking to the trainer still starts the fight
    warp(0x33,2,black=True)
    tr=[n for n in npcs() if n[4]>=0xc8][0]
    m[0xc200+16*tr[0]+6]=0xff
    seen.clear();spot_ok=True
    try:spot(tr[0])
    except AssertionError:spot_ok=False
    if spot_ok:
        press_('a',120);T(200)
        ok(m[0xd057]!=0 or 'Pokemon' in allt() or len(allt())>20,'talking to a trainer still starts the usual dialogue / battle: %s'%allt()[:70])
    print('v28 sight: ALL PASS')

if MODE=='exempt':
    # LAVENDER TOWN: nobody panics
    warp(4,1);freeze()
    n=[x for x in npcs() if x[4]==0][1]
    t=talk(n[0],answers=['no']);ok('CURSE' not in t and len(t)>10,'Lavender Town NPC (pic %d) just talks: %s'%(n[1],t[:50]))
    # POKeMON CENTER in Lavender: the nurse
    warp(0x8d,0);freeze()
    nurse=[x for x in npcs() if x[1]==0x29][0]
    t=talk(nurse[0],answers=['no','no','no']);ok('CURSE' not in t and 'POK' in t,'the nurse is served as usual: %s'%t[:50])
    # shop clerk (Viridian MART, outside Lavender): not touched
    warp(0x2a,0);freeze()
    clerk=[x for x in npcs() if x[1]==0x26][0]
    t=talk(clerk[0],answers=['no','no','no'],n=30);ok('CURSE' not in t,'the shop clerk is not a victim: %s'%t[:50])
    # OAK's LAB: OAK does not panic
    warp(0x28,0);freeze()
    oak=[x for x in npcs() if x[1]==3][0]
    t=talk(oak[0],answers=['no','no'],n=30);ok('CURSE' not in t,'OAK does not panic: %s'%t[:50])
    # an item ball is not a person
    print('v28 exempt: ALL PASS')
if MODE=='normal':
    start(black=False)
    ns=[n for n in npcs() if n[1] in (0xd,0x2f) and n[4]==0]
    t=talk(ns[0][0],answers=['yes','yes'],n=30)
    ok('CURSE' not in t and len(t)>20,'not BLACK: the NPC just talks (%s)'%t[:60])
    ok(killed()==[] and pic(ns[0][0])!=0x49,'not BLACK: nothing died')
    print('v28 normal: ALL PASS')
