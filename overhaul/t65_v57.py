# v57: LANCE as BLACK. Modes:
#  black  - BLACK route: the new before-battle speech; after the last POKeMON her new defeat speech, the MOON STONE shatters, BANE kills her;
#           afterwards NO dialogue and the way to LANCE is open by itself (D863 bit 1 set, the exit block open)
#  normal - GHOST route: the original speeches ("Welcome to the POKeMON LEAGUE"), the after-battle text is still shown
import sys
MY65=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY65
if MODE=='black':
    def setup():
        make_black();lead(CHAR);strong(0)
        b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35
    to_battle(0x71,None,None,setup,one=True)
    t=allt().replace('  ',' ');print('before:',t[:700])
    keys=['others have fallen','I am LANCE, leader','BUSHI','dragon trainer','destroy you, BLACK','countless lives','reign of terror']
    print([k for k in keys if k not in t])
    ok(all(k in t for k in keys),'the new before-battle speech')
    ok('ancestors' not in t,'not the original')
    menu('fight');m[0xcc26]=1;T(4);seen.clear();p.button('a',8)
    for k in range(2500):
        p.tick()
        if k%4==0:T(1)
        if m[0xd05a]==3 and 'FIGHT' in clean(' '.join(txt())):break
        if k%90==0:p.button('a',8)
    t=allt().replace('  ',' ');print('to phase:',t[-500:])
    i=t.find('Impossible');print('DEFEAT CTX',t[max(0,i-60):i+40])
    ok("Impossible" in t and "ancestors" in t and "cannot be how" in t,'the new defeat speech')
    use_move(0,300,in_moves=True)
    for i in range(30):
        if m[0xd057]==0:break
        press_('a',100)
    for i in range(6):press_('a',60)
    T(120);seen.clear();T(200)
    ok(m[0xd057]==0 and m[0xd866]&0x40,'LANCE is dead, his room counts as beaten')
    ok(not box() and not allt().strip(),'no dialogue after the battle (%r)'%allt()[:60])
    print('pos',pos())
    for k in range(8):p.button('up',8);T(40)
    print('pos after',pos())
    ok(m[0xd35e]==0x78,"nothing blocks the way: LANCE's exit leads to the champion's room")
elif MODE=='normal':
    def setup():lead(GHOST)
    to_battle(0x71,None,None,setup)
    t=allt().replace('  ',' ');print('normal:',t[-400:],m[0xd46c])
    print([k in t for k in ('sacred bond','grind you','LANCE','I am LANCE of the ELITE FOUR!')])
    ok('destroy you, BLACK' not in t and 'LANCE' in t,'GHOST route: the original before-battle speech (not the new one)')
