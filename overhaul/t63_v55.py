# v55: LORELEI as BLACK. Modes:
#  black  - BLACK route: the new before-battle speech; after the last POKeMON her new defeat speech, the MOON STONE shatters, BANE kills her;
#           afterwards NO dialogue and the way to BRUNO is open by itself (D863 bit 1 set, the exit block open)
#  normal - GHOST route: the original speeches ("Welcome to the POKeMON LEAGUE"), the after-battle text is still shown
import sys
MY63=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY63
if MODE=='black':
    def setup():
        make_black();lead(CHAR);strong(0)
        b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35
    to_battle(0xf5,3,5,setup,one=True)
    t=allt().replace('  ',' ');print('before:',t[:700])
    keys=['I am LORELEI of the ELITE','dark trainer','battles for souls','look the part','icy','will freeze','Hahaha','Are you ready']
    print([k for k in keys if k not in t])
    ok(all(k in t for k in keys),'the new before-battle speech')
    ok('Welcome to the' not in t,'not the original')
    menu('fight');m[0xcc26]=1;T(4);seen.clear();p.button('a',8)
    for k in range(2500):
        p.tick()
        if k%4==0:T(1)
        if m[0xd05a]==3 and 'FIGHT' in clean(' '.join(txt())):break
        if k%90==0:p.button('a',8)
    t=allt().replace('  ',' ');print('to phase:',t[-500:])
    i=t.find('believe');print('DEFEAT CTX',t[max(0,i-60):i+40])
    ok("believe it" in t and "ordinary trainer" in t and "really the end" in t,'the new defeat speech')
    use_move(0,300,in_moves=True)
    for i in range(30):
        if m[0xd057]==0:break
        press_('a',100)
    for i in range(6):press_('a',60)
    T(120);seen.clear();T(200)
    ok(m[0xd057]==0 and m[0xd863]&2,'LORELEI is dead, her room counts as beaten')
    ok(not box() and not allt().strip(),'no dialogue after the battle (%r)'%allt()[:60])
    print('block',[hex(m[0xc6e8+(m[0xd369]+6)*(2+3)+3+k]) for k in range(1,5)])
    bfs_to(0,4,maxn=400)
    for k in range(4):p.button('up',8);T(40)
    ok(m[0xd35e]==0xf6,'the way to BRUNO opens by itself')
elif MODE=='normal':
    def setup():lead(GHOST)
    to_battle(0xf5,3,5,setup)
    t=allt().replace('  ',' ');print('normal:',t[:500])
    ok('dark trainer' not in t and ('Welcome' in t or 'LORELEI' in t),'GHOST route: the original before-battle speech')
