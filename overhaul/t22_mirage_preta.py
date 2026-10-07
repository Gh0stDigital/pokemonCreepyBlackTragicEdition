# v8: PRETA in a Mirage (Black Tamer) battle: not too scared, MACABRE doesn't affect the fossil,
# other moves do damage ('win' mode: CUT finishes a fossil at low HP and the Tamer is defeated).
from harness import *
import random,sys
MODE=sys.argv[1] if len(sys.argv)>1 else 'macabre'
def find_mirage(seed):
    random.seed(seed);load('v6_after_macabre');m[0xd45c]=200
    for step in range(3000):
        if m[0xd057]:
            p.tick(30)
            if m[0xd45d]:return True
            for i in range(40):
                if m[0xd057]==0:break
                if 'FIGHT' in box():p.button('down',8);p.tick(10);p.button('right',8);p.tick(10);p.button('a',8);p.tick(150)
                else:p.button('a',8);p.tick(150)
            continue
        m[0xd455]=255;walk(random.choice(['up','down','left','right']),1)
for seed in range(20,40):
    assert find_mirage(seed)
    for i in range(40):
        if 'FIGHT' in box() and m[0xd014]==0xb6:break
        p.button('a',8);p.tick(160)
    print('seed',seed,'enemy',hex(m[0xcfe5]),flush=True)
    if m[0xcfe5]==0xb6:break
print('MIRAGE party',list(m[0xd164:0xd16b]))
enemy=m[0xcfe5];hp0=m[0xcfe6]<<8|m[0xcfe7];print('enemy',hex(enemy),'HP',hp0,'my mon',hex(m[0xd014]))
assert m[0xd014]==0xb6 and enemy in (0xb6,0xb7)
if MODE=='win':m[0xcfe6]=0;m[0xcfe7]=1
p.button('a',8);p.tick(40)
if MODE=='win':p.button('down',8);p.tick(20);p.button('down',8);p.tick(20)   # SURF (CUT/STRENGTH are Normal: no effect on GHOST types)
p.button('a',8);seen=[]
for i in range(1500):
    p.tick()
    if i%20==0:
        b=' '.join(''.join(c for c in box() if c not in '│─┌┐└┘|').split())
        if b and (not seen or seen[-1]!=b):seen.append(b)
    if i%60==30 and box() and 'FIGHT' not in box():p.button('a',8)
    if m[0xd057]==0 or ('FIGHT' in box() and i>300) or 'Bring out' in box():break
hp1=m[0xcfe6]<<8|m[0xcfe7]
for s in seen:print('  TEXT:',s)
print('enemy HP',hp0,'->',hp1,'in battle',m[0xd057],'mirage',m[0xd45d])
if MODE=='macabre':
    assert hp1==hp0 and any("doesn't" in s or 'affect' in s for s in seen) and not any('too scared' in s for s in seen if 'PRETA' in s)
    print('PASS MACABRE has no effect on the fossil; PRETA not scared')
else:
    for i in range(60):
        if m[0xd057]==0:break
        assert 'Bring out' not in box(),'PRETA died'
        p.button('a',8);p.tick(120)
    p.tick(200)
    print('after: in battle',m[0xd057],'mirage',m[0xd45d],'party',list(m[0xd164:0xd16b]),'count',m[0xd163],'box',m[0xda80],'pos',pos())
    assert m[0xd057]==0 and m[0xd45d]==0 and 0x79 not in m[0xd164:0xd16b] and 0x1f in m[0xd164:0xd16b] and 0xb6 in m[0xd164:0xd16b]
    print('PASS PRETA defeats the Black Tamer with SURF; cleanup ok')
    shot('v8_after_mirage_win')
