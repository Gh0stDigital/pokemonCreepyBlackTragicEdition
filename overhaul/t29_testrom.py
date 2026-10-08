# Test ROM with the built-in save (run with CB_ROM=Creepy_Black_Mu_v14_test.gb):
#  1. empty cartridge RAM -> CONTINUE loads Oak's lab, CHARMANDER + GHOST, GHOST route, POKeDEX
#  2. NEW GAME still starts Oak's intro
#  3. a cartridge that already has a save is not overwritten
import harness
from harness import *
from pyboy import PyBoy
def boot(sram=None):
    global p,m
    harness.p.stop(save=False)
    harness.p=PyBoy(ROM,window='null',sound_emulated=False);harness.p.set_emulation_speed(0);harness.m=harness.p.memory
    p=harness.p;m=harness.m
    if sram:
        for bk in range(4):
            for i in range(0x2000):m[bk,0xa000+i]=sram[bk*0x2000+i]
    p.tick(300)
    for i in range(40):
        if 'NEW GAME' in ' '.join(txt()):return
        p.button('start' if i%2 else 'a',8);p.tick(120)
    raise SystemExit('FAIL no title menu')
boot();t=' '.join(txt());print('menu',[x for x in txt() if x][:4])
assert 'CONTINUE' in t
p.button('a',8);p.tick(200);p.button('a',8);p.tick(400)
for i in range(10):
    if m[0xd35e]==0x28 and not box():break
    p.button('a',8);p.tick(120)
p.button('start',8);p.tick(60);menu=' '.join(txt())
print('loaded',pos(),'party',list(m[0xd164:0xd16a]),'D450',m[0xd450],'D451',m[0xd451])
assert pos()[0]==0x28 and list(m[0xd164:0xd166])==[0xb0,0x1f] and m[0xd450]==1 and m[0xd451]==1 and 'POKéDEX' in menu
print('PASS empty cartridge: CONTINUE starts the built-in GHOST-route save after the POKeDEX')
boot()
p.button('down',8);p.tick(30);p.button('a',8)
seen=''
for i in range(600):
    p.tick();seen+=' '+box()
    if 'Hello' in seen or 'world' in seen:break
print('new game text',box()[:60]);assert 'Hello' in seen or 'world' in seen
print('PASS NEW GAME still starts Oak\'s intro')
sav=bytearray(open('Creepy_Black_Mu_v14.sav','rb').read());sav[0x2000+0x598]=0x92        # existing save named differently
boot(bytes(sav))
name=[m[1,0xa598+i] for i in range(3)];print('sram name bytes',[hex(x) for x in name])
assert name[0]==0x92
print('PASS an existing save is left alone')
