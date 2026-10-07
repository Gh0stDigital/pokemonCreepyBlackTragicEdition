# v7: with PRETA in the party, Pokemon Tower ghosts are identified (SILPH SCOPE effect); without it they stay GHOST.
from harness import *
import random,sys
WITH=(sys.argv[1] if len(sys.argv)>1 else 'with')=='with'
random.seed(4)
load('v6_with_preta')
for i in range(4):p.button('b',8);p.tick(60)
if not WITH:m[0xd163]=2;m[0xd166]=0xff
assert not any(m[0xd31e+2*i]==0x48 for i in range(m[0xd31d])),'has real SILPH SCOPE'
for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x90      # house door -> POKEMON TOWER 3F
for i in range(6):
    if m[0xd35e]==0x90:break
    walk('down',1)
p.tick(120);print('map',pos(),'party',list(m[0xd164:0xd168]),flush=True)
assert m[0xd35e]==0x90
for i in range(1500):
    if m[0xd057]:break
    m[0xd0db]=0;m[0xd455]=255;walk(random.choice(['up','down','left','right']),1)
assert m[0xd057]==1,pos()
seen=[]
for i in range(30):
    b=box()
    if b and (not seen or seen[-1]!=b):seen.append(b)
    if 'FIGHT' in b:break
    p.button('a',8);p.tick(90)
shot('v7_tower_%s'%('preta' if WITH else 'nopreta'))
texts=[''.join(c for c in s if c not in '│─┌┐└┘|').strip() for s in seen]
for t in texts:print('  TEXT:',t)
nick=''.join(cm.get(v,'?') for v in m[0xcfda:0xcfe0]).split('@')[0] if False else ''.join(cm.get(v,'') for v in m[0xcfda:0xcfe4])
print('enemy species',hex(m[0xcfe5]),'name area',nick)
ghost=any("GHOST" in t and "ID" in t for t in texts) or 'GHOST' in ' '.join(txt()[:3])
if WITH:assert not ghost;print('PASS PRETA unveils the ghost')
else:assert ghost;print('PASS no PRETA: still GHOST')
