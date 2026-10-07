from harness import *
load('only_ghost')
def sram_name():return [m[1,a] for a in range(0xa598,0xa5a3)]
# Save the game: START -> POKeMON, ITEM, RED, SAVE
press('start',60)
for i in range(3):press('down',20)
press('a',150)
for i in range(12):
    t=''.join(txt())
    if 'saved' in t.lower():break
    press('a',150)
p.tick(200);print('SRAM player name after save',sram_name())
assert 0x50 in sram_name(),'save did not reach SRAM'
press('b',60);press('b',60)
m[0xd455]=1;m[0xd456]=5
black=0
p.button('right',8)
for f in range(900):
    p.tick(1)
    if m[0xff47]==0xff:black+=1
nz=sum(1 for b in range(4) for a in range(0xa000,0xc000) if m[b,a])
print('black frames',black,'SRAM name after',sram_name(),'nonzero SRAM bytes (all 4 banks)',nz)
p.tick(1500);shot('v2_after_death_title')
press('start');press('a',300);shot('v2_after_death_menu');menu=[x for x in txt() if x];print('menu:',menu)
assert nz==0 and not any('CONTINUE' in x for x in menu);print('PASS permadeath wipe')
