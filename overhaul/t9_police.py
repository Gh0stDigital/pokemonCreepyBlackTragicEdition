from harness import *
import sys
state=sys.argv[1]
load(state);p.tick(30)
if len(sys.argv)>2:m[0xd453]=int(sys.argv[2])
for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x46
for i in range(6):
    if m[0xd35e]==0x46:break
    walk('down',1)
p.tick(120);print(state,'killed flag',m[0xd453],'map',pos(),flush=True)
walk('up',1);walk('up',1);press('left',30);print('player',pos(),'box',bool(box()),flush=True)
if not box():press('a',60)
seen=[]
for i in range(30):
    b=box()
    if b and (not seen or seen[-1]!=b):seen.append(b)
    if i>3 and not b:break
    press('a',120)
    if 'lookout' in ' '.join(seen) and len(seen)%5==0:shot('police_alert_'+state)
for s in seen:print('  TEXT:',''.join(c for c in s if c not in '│─┌┐└┘|').strip(),flush=True)
print('RESULT',state,'ALERT SHOWN' if 'lookout' in ' '.join(seen) else 'no alert',flush=True)
