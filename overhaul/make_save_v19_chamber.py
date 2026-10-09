# Test-only save for the v19 chamber: the chain's GHOST-route save, with AGATHA's quest set to stage 5 (MISTY has come)
# and FUJI rescued, standing on Pokemon Tower 7F below the opened stairs. Flags are set directly (not played through).
# Writes Creepy_Black_Mu_v19_chamber.sav.
import sys;sys.argv=['t33_v19.py','none']
exec(open('t33_v19.py').read().split("if MODE=='closed'")[0])
m[0xd75e]|=0xcc                                   # MISTY beaten (badge event, TM) for consistency
m[0xd356]|=0x02;m[0xd72a]|=0x02
tower(5)
for k,v in ((0xd75e,0xcc),):m[k]|=v
m[0xd356]|=0x02;m[0xd72a]|=0x02
bfs_to(4,11)
p.button('start',8);T(90)
for i in range(8):
    if '▲SAVE' in ' '.join(txt()):break
    p.button('down',8);T(30)
p.button('a',8);T(200);p.button('a',8)
for i in range(900):
    T(1)
    if i%120==60 and seen and 'SAVE' in seen[-1] and 'saved' not in seen[-1].lower():p.button('a',8)
assert any('saved' in s.lower() for s in seen)
open('Creepy_Black_Mu_v19_chamber.sav','wb').write(bytes(m[bk,ad] for bk in range(4) for ad in range(0xa000,0xc000)))
print('saved at',pos(),'stage',m[0xd464],'consort',m[0xd465])
