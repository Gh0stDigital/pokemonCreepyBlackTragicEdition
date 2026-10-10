# v32. Modes:
#  immune - GHOST never eats PRETA / AZHI: [PRETA, GHOST, X] -> X; [X, AZHI, GHOST] -> X; [GHOST, PRETA, AZHI] -> the
#           player (GENGAR cry, restart); the 50-step warning names the right victim; plain [X, GHOST] still eats X
#  back   - PRETA's back picture: same outline, light-grey rib lines, no dark grey
import sys
sys.argv=[sys.argv[0]]+sys.argv[1:]
MY=sys.argv[1]
sys.argv[1]='none'
exec(open('t39_v30.py').read())
def species(order_sp):
    for i,s in enumerate(order_sp):
        if s:m[0xd164+i]=s;m[0xd16b+44*i]=s
def named(i,ch):m[0xd2b5+11*i]=ch;m[0xd2b5+11*i+1]=0x50
if MY=='immune':
    g,o=start();set_party([o,g,o]);species([0xb6,0,0]);named(2,0x80)            # PRETA, GHOST, "A"
    t=step(9,3);first=t.split('seems')[0].split()
    ok('anxious' in t and 'PRETA' not in t and first and first[-1]=='A','warning names "A", not PRETA: "%s seems anxious..."'%(first[-1] if first else '?'))
    step(1,5);p.tick(500);sp=list(m[0xd164:0xd164+m[0xd163]])
    ok(sp==[0xb6,0x1f],'[PRETA, GHOST, A]: GHOST skipped PRETA and ate A below it: %s'%[hex(x) for x in sp])
    g,o=start();set_party([o,o,g]);species([0,0xb7,0]);named(0,0x80)             # "A", AZHI, GHOST
    step(1,5);p.tick(500);sp=list(m[0xd164:0xd164+m[0xd163]])
    ok(sp==[0xb7,0x1f],'[A, AZHI, GHOST]: GHOST skipped AZHI and ate A further up: %s'%[hex(x) for x in sp])
    g,o=start();set_party([g,o]);t=step(1,5);p.tick(500)
    ok(m[0xd163]==1,'normal case [GHOST, X]: X is still eaten')
    g,o=start();set_party([g,o,o]);species([0,0xb6,0xb7])                      # GHOST, PRETA, AZHI
    cries=[];resets=[]
    p.hook_register(0,0x13ff,lambda c:cries.append(p.register_file.A),None)
    p.hook_register(0,0x0100,lambda c:resets.append(1),None)
    m[0xd455]=1;m[0xd456]=5
    for d in ('left','right','up','down'):
        p.button(d,8);p.tick(60)
        if resets:break
    p.tick(300)
    ok(0x0e in cries and resets,'[GHOST, PRETA, AZHI]: nothing edible -> GHOST eats the player (GENGAR cry, restart)')
    print('v32 immune: ALL PASS')
if MY=='back' and '_v32' not in ROM:print('v32 back: skipped on later builds (t42 checks the newer picture)')
elif MY=='back':
    import preta_back as P
    new=P.load(ROM);old=P.load(ROM.replace('v32','v31'))
    diff=[(y,x) for y in range(32) for x in range(32) if new[y][x]!=old[y][x]]
    ok(diff and all(old[y][x]==0 and new[y][x]==1 for y,x in diff),'%d white pixels became light grey, nothing else changed'%len(diff))
    ok(not any(c==2 for row in new for c in row),'no dark grey (still a light, pale fossil)')
    print('v32 back: ALL PASS')
