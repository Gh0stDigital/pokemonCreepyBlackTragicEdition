# Fossil Aerodactyl (AZHI since v10) variant: look + an AZHI move against the player's stand-in.
from harness import *
load('mirage_battle_start_only_ghost')
for i in range(40):
    if 'FIGHT' in box() and m[0xd014]==0x79:break
    p.button('a',8);p.tick(160)
sp=m[0xcfe5];shot('aero_battle');print('enemy',hex(m[0xcfe5]),'lvl',m[0xcff3],'moves',[hex(x) for x in m[0xcfed:0xcff1]])
if sp!=0xb7:print('SKIP: the chain\'s Mirage rolled species %s, not the fossil Aerodactyl/AZHI (t24_v10 covers AZHI)'%hex(sp));raise SystemExit
p.button('a',8);p.tick(40);p.button('a',8);seen=[];black=0
for i in range(900):
    p.tick(1)
    if m[0xff47]==0xff:black+=1
    if i%60==30 and box():p.button('a',8)
    if i%20==0:
        b=' '.join(''.join(c for c in box() if c not in '│─┌┐└┘|').split())
        if b and (not seen or seen[-1]!=b):seen.append(b)
print(seen[-4:],'black',black)
import os
if os.path.basename(ROM).replace('.gb','').split('_v')[-1].isdigit() and int(os.path.basename(ROM).replace('.gb','').split('_v')[-1])>=10:
    assert sp==0xb7 and any(('AZHI used '+mv) in s or ('AZHI flew' in s) for s in seen for mv in ('BLACK FLAME','FLY','DRAGONBREATH','FIRE BLAST'));print('PASS AZHI attacks with one of its moves')
else:
    assert sp==0xb7 and any('BLACK FLAME' in s for s in seen);print('PASS Fossil Aerodactyl uses BLACK FLAME')
