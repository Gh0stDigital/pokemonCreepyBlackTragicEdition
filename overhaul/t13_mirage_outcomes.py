# From "player is out" in a Mirage battle: FIGHT (scared -> killed -> wipe), RUN success, RUN failure.
from harness import *
import sys
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
def prep():
    load('mirage_battle_start')
    for i in range(60):
        if 'Bring out' in box():break
        p.button('a',8);p.tick(160)
    p.button('down',8);p.tick(30);p.button('a',8);p.tick(240)
    assert m[0xd014]==0x79
def sram_has_save():return any(m[1,a] for a in range(0xa598,0xa5a3))
def watch(n,label):
    seen=[];black=0;reset=False
    for i in range(n):
        p.tick(1)
        if m[0xff47]==0xff:black+=1
        if i%60==30 and box():p.button('a',8)
        if i%20==0:
            b=box()
            if b and (not seen or seen[-1]!=b):seen.append(b)
        if m[0xd057]==0 and i>200 and not reset:break
    return seen,black
# put a real save into SRAM first so the wipe is observable
prep()
for b in range(4):
    for a in range(0xa000,0xa010):m[b,a]=0x55
mode=sys.argv[1]
if mode=='fight':
    m[0xcffa]=0;m[0xcffb]=1                          # slow the enemy so the player acts first
    if m[0xcfe5]==0xb7:                              # v11+: BLACK FLAME spares the stand-in; test a sure hit instead
        m[0xcfed]=m[0xcfee]=m[0xcfef]=m[0xcff0]=0x52 # DRAGON RAGE (never misses, 40 damage)
    p.button('a',8);p.tick(40);p.button('a',8)       # FIGHT -> TACKLE
    seen,black=watch(900,'fight')
    for s in seen:print('  TEXT:',clean(s))
    nz=sum(1 for b in range(4) for a in range(0xa000,0xc000,3) if m[b,a])
    print('black',black,'SRAM nonzero sampled',nz,'title text:',[x for x in txt() if x][:3])
    assert any('too scared' in clean(s) for s in seen) and nz==0;print('PASS player FIGHT: too scared, hit, save wiped')
else:
    results=[]
    for delay in (0,3,6):
        prep()
        for b in range(4):
            for a in range(0xa000,0xa010):m[b,a]=0x55
        p.tick(delay)
        p.button('down',8);p.tick(10);p.button('right',8);p.tick(10);p.button('a',8)   # RUN
        seen,black=watch(1500,'run')
        t=' '.join(clean(s) for s in seen)
        esc='Got away' in t;nz=sum(1 for b in range(4) for a in range(0xa000,0xa010) if m[b,a])
        results.append(esc)
        print('delay',delay,'escaped' if esc else 'caught','| black',black,'| sram kept' if nz else '| sram wiped',flush=True)
        if esc and 'esc' not in [r for r in results[:-1] if r]:
            for k in range(6):p.button('a',8);p.tick(100)
            save('mirage_escaped')
            print('   after escape party',list(m[0xd164:0xd16b]),'count',m[0xd163],'box',m[0xda80],list(m[0xda81:0xda83]),'flags',m[0xd45d],m[0xd45f],'opp',m[0xd059])
        if not esc:print('   texts:',[clean(s)[:40] for s in seen][-4:])
    print('escape rate in sample',sum(results),'/',len(results))
