# Walk Route 1 grass with a high Ghost-use counter until a Mirage Black Tamer battle starts.
from harness import *
import random,sys
random.seed(7)
START=sys.argv[1] if len(sys.argv)>1 else 'pallet_with_ghost';TAG='' if START=='pallet_with_ghost' else '_'+START
load(START);m[0xd455]=200
print('party',list(m[0xd164:0xd16a]),'box count',m[0xda80],flush=True)
m[0xd45c]=200          # heavy Ghost use -> capped chance (64/256)
for i in range(12):
    if pos()[1]<=10:break
    walk('left',1)
for i in range(30):
    if m[0xd35e]==0xc and pos()[2]<30:break
    walk('up',1)
def run_from_wild():
    for i in range(40):
        b=box()
        if m[0xd057]==0:return
        if 'FIGHT' in b and 'RUN' in b:p.button('down',8);p.tick(10);p.button('right',8);p.tick(10);p.button('a',8);p.tick(150)
        else:p.button('a',8);p.tick(150)
battles=0
for step in range(3000):
    if m[0xd057]:
        p.tick(30);battles+=1
        if m[0xd45d]:
            print('MIRAGE after',battles,'battles; opponent',hex(m[0xd059]),'trainerNo',m[0xd05d],flush=True)
            break
        run_from_wild();m[0xd455]=200;continue
    walk(random.choice(['up','down','left','right']),1)
else:raise SystemExit('FAIL no mirage found')
print('party now',list(m[0xd164:0xd16b]),'count',m[0xd163],'box count',m[0xda80],'box species',list(m[0xda81:0xda81+m[0xda80]+1]),'mask',bin(m[0xd45e]),'deposited',m[0xd45f])
save('mirage_battle_start'+TAG)
for i in range(14):p.tick(20);shot('mirage_intro%s_%02d'%(TAG,i))
