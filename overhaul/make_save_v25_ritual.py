# Test-only save for v25: the chamber right after MR. MU's ritual (????? in the party, standing in front of his grave inside
# the circle, RIT=3), made by playing the ritual in the emulator (t35_v25.py ritual_state) and saving through the START menu.
# Writes Creepy_Black_Mu_v25_ritual.sav.
import sys;sys.argv=['t35_v25.py','none']
exec(open('t35_v25.py').read().split("if MODE=='items':")[0])
ritual_state()
print('party',[hex(x) for x in party()],'pos',pos(),'RIT',m[RIT])
assert m[RIT]==3 and party()[-1]==MIR
p.button('start',8);T(90)
for i in range(8):
    if '▲SAVE' in ' '.join(txt()):break
    p.button('down',8);T(30)
p.button('a',8);T(200);p.button('a',8)
for i in range(900):
    T(1)
    if i%120==60 and seen and 'SAVE' in seen[-1] and 'saved' not in seen[-1].lower():p.button('a',8)
assert any('saved' in s.lower() for s in seen)
open('Creepy_Black_Mu_v25_ritual.sav','wb').write(bytes(m[bk,ad] for bk in range(4) for ad in range(0xa000,0xc000)))
print('saved at',pos(),'RIT',m[RIT])
