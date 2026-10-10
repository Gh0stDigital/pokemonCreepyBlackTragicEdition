# v30 GHOST hunger warnings and victim. Modes:
#  warn   - 100 steps left: "GHOST seems to be getting restless...", 50: "<victim> seems anxious about something.",
#           25: "You sense a malicious intent...", 99 / 51: no message
#  eat    - GHOST in slot 2: it eats slot 1 (the one in front of it); GHOST leading: it eats slot 2 (just below)
#  player - GHOST alone: it eats the player with GENGAR's cry, the save is erased, the game restarts
from harness import *
import sys
MODE=sys.argv[1]
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
def box():
    if m[0xc3a0+12*20]!=0x79:return ''
    return ' | '.join(x for x in txt()[12:] if x)
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:sys.exit(1)
cm_rev={v:k for k,v in cm.items()}
def name(i):return ''.join(cm.get(x,'') for x in m[0xd2b5+11*i:0xd2b5+11*i+11] if x!=0x50)
def set_party(order):
    """order = list of current party indices (repeat allowed) -> new party in that order"""
    mons=[bytes(m[0xd16b+44*i:0xd16b+44*i+44]) for i in range(6)];sp=list(m[0xd164:0xd16a])
    ot=[bytes(m[0xd273+11*i:0xd273+11*i+11]) for i in range(6)];nk=[bytes(m[0xd2b5+11*i:0xd2b5+11*i+11]) for i in range(6)]
    m[0xd163]=len(order)
    for j,i in enumerate(order):
        m[0xd164+j]=sp[i];m[0xd16b+44*j:0xd16b+44*j+44]=mons[i];m[0xd273+11*j:0xd273+11*j+11]=ot[i];m[0xd2b5+11*j:0xd2b5+11*j+11]=nk[i]
    m[0xd164+len(order)]=0xff
def start():
    load('pallet_with_ghost');p.tick(30)
    sp=list(m[0xd164:0xd164+m[0xd163]]);g=sp.index(0x1f);o=[i for i in range(len(sp)) if i!=g][0]
    return g,o
def step(h,c):
    """set hunger h / counter c, take one real step; returns the texts shown"""
    m[0xd455]=h;m[0xd456]=c;seen=[]
    for d in ('left','right','up','down'):
        y,x=m[0xd361],m[0xd362]
        p.button(d,8)
        for _ in range(60):
            p.tick();b=clean(box())
            if b and (not seen or seen[-1]!=b):seen.append(b)
        if (m[0xd361],m[0xd362])!=(y,x) or seen:break
    for k in range(6):
        if not box():break
        p.button('a',8)
        for _ in range(60):
            p.tick();b=clean(box())
            if b and (not seen or seen[-1]!=b):seen.append(b)
    p.tick(30);return ' '.join(seen)
if MODE=='warn':
    g,o=start();set_party([o,g])                     # GHOST second: the victim is the first
    victim=name(0)
    t=step(17,1);ok('restless' in t,'100 steps left: "%s"'%t[-60:])
    t=step(17,2);ok(not t,'99 steps left: no message (%s)'%t[-40:])
    t=step(9,3);ok('anxious' in t and victim in t,'50 steps left: "%s" (victim %s)'%(t[-60:],victim))
    t=step(9,2);ok(not t,'51 steps left: no message')
    t=step(5,4);ok('malicious' in t,'25 steps left: "%s"'%t[-60:])
    ok(m[0xd163]==2,'nobody was eaten by the warnings')
    print('v30 warn: ALL PASS')
if MODE=='eat':
    g,o=start();set_party([o,g,o])                   # A, GHOST, A2
    m[0xd2b5]=0x80;m[0xd2b6]=0x50                    # first one renamed "A" to tell them apart
    t=step(1,5);p.tick(500)                          # the meal (black screen + cry) takes a while
    sp=list(m[0xd164:0xd164+m[0xd163]])
    ok(m[0xd163]==2 and sp[0]==0x1f,'GHOST in slot 2 ate slot 1 (the one in front of it): party %s'%[hex(x) for x in sp])
    ok(name(0)!='A' and name(1)!='A','the eaten one was slot 1 ("A")')
    ok(m[0xd455]==12,'hunger is 12 after the meal (got %d)'%m[0xd455])
    g,o=start();set_party([g,o,o]);m[0xd2b5+11]=0x80;m[0xd2b5+12]=0x50   # GHOST leads, slot 2 = "A"
    t=step(1,5);p.tick(500)                          # the meal (black screen + cry) takes a while
    sp=list(m[0xd164:0xd164+m[0xd163]])
    ok(m[0xd163]==2 and sp[0]==0x1f and name(1)!='A','GHOST leading ate slot 2 (just below it): party %s'%[hex(x) for x in sp])
    print('v30 eat: ALL PASS')
if MODE=='player':
    g,o=start();set_party([g])
    cries=[];resets=[]
    p.hook_register(0,0x13ff,lambda c:cries.append(p.register_file.A),None)
    p.hook_register(0,0x0100,lambda c:resets.append(1),None)
    m[0xd455]=1;m[0xd456]=5
    for d in ('left','right','up','down'):
        p.button(d,8);p.tick(60)
        if resets:break
    p.tick(400)
    ok(0x0e in cries,"GENGAR's cry played (cries %s)"%[hex(c) for c in cries])
    ok(bool(resets),'the game restarted')
    blank=all(m[1,0xa598+i] in (0,0xff) for i in range(64))
    ok(blank,'the save (SRAM bank 1) is erased')
    print('v30 player: ALL PASS')
