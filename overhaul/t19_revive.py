# v7: PRETA revives 2 turns after fainting (mid-battle) and is restored after a battle that ends while it is down.
from harness import *
import random,sys
MODE=sys.argv[1] if len(sys.argv)>1 else 'turns'
random.seed(3)
load('v6_after_macabre')
def preta_hp():return m[0xd16c]<<8|m[0xd16d]
def step(d):
    m[0xd0db]=0;a=pos();walk(d,1);return pos()!=a
for i in range(800):
    if m[0xd057]:break
    step(random.choice(['up','down','left','right']))
assert m[0xd057]==1;p.tick(30)
print('battle; party',list(m[0xd164:0xd168]),'Preta HP',preta_hp(),flush=True)
seen=[];log=[];fainted_turn=None;turn=0;revived_turn=None
for i in range(400):
    b=box();t=' '.join(txt())
    if b and (not seen or seen[-1]!=b):seen.append(b)
    if m[0xd057]==0:break
    m[0xcfe6]=3;m[0xcfe7]=0xe7                                 # enemy can't die
    if 'FIGHT' in b and 'RUN' in b:
        turn+=1;log.append((turn,m[0xd014],preta_hp(),m[0xd461]))
        if m[0xd014]==0xb6:m[0xd015]=0;m[0xd016]=0             # PRETA drops to 0 HP: faints at the end of this turn
        if MODE=='run' and fainted_turn and m[0xd014]!=0xb6:     # escape while PRETA is down
            p.button('down',8);p.tick(10);p.button('right',8);p.tick(10);p.button('a',8);p.tick(200);continue
        if revived_turn and turn>revived_turn+1:                 # done: run
            p.button('down',8);p.tick(10);p.button('right',8);p.tick(10);p.button('a',8);p.tick(200);continue
        p.button('a',8);p.tick(40);p.button('a',8);p.tick(200);continue
    if 'Choose a' in t or 'Bring out' in t or 'next' in t.lower() and 'POK' in t:
        if fainted_turn is None:fainted_turn=turn;print('PRETA fainted on turn',turn,'party HP',preta_hp(),flush=True)
        if 'Choose a' in t or 'Bring out' in t:
            p.button('down',8);p.tick(20);p.button('down',8);p.tick(20);p.button('a',8);p.tick(100)
            if 'SWITCH' in ' '.join(txt()) or 'SHIFT' in ' '.join(txt()):p.button('a',8);p.tick(100)
            continue
    if 'rose' in b and revived_turn is None:revived_turn=turn;print('REVIVE text on turn',turn,'party HP',preta_hp(),'status',m[0xd16f])
    p.button('a',8);p.tick(100)
for l in log:print('  turn %d active %s PretaHP %d count %d'%(l[0],hex(l[1]),l[2],l[3]))
for s in seen:
    if 'rose' in s or 'dead' in s or 'fainted' in s:print('  TEXT:',''.join(c for c in s if c not in '│─┌┐└┘|').strip())
print('after battle: Preta HP',preta_hp(),'max',m[0xd18d]<<8|m[0xd18e],'count',m[0xd461],'party',list(m[0xd164:0xd168]))
if MODE=='turns':
    flat=[' '.join(''.join(c for c in x if c not in '│─┌┐└┘|').split()) for x in seen]
    fi=next(i for i,x in enumerate(flat) if 'PRETA fainted!' in x);ri=next(i for i,x in enumerate(flat) if 'from the dead!' in x)
    turns=sum(1 for i in range(fi,ri) if flat[i].endswith('used SCRATCH!') and not flat[i-1].endswith('used SCRATCH!'))
    print('full turns fought by CHARMANDER between faint and revival:',turns)
    assert turns==2,turns
    print('PASS PRETA revived after %d turns'%turns)
else:
    assert fainted_turn and revived_turn is None
assert preta_hp()==135 and m[0xd164]==0xb6 and m[0xd461]==0;print('PASS PRETA at full HP after the battle')
