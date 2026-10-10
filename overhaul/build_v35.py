# Creepy Black Mu v35: killed trainers vanish from the map right away again - from CERULEAN on too.
#   Every frame the overworld sprite code (1:50AA) asks predef 0x12 (hidden object?) and predef 0x13 (killed trainer?)
#   whether to draw a sprite. Predef 0x13 is the base hack's 3:4DFB, which only knows the base kill list (D486, built
#   from the early-route table) - so trainers up to MT. MOON vanished the moment CURSE killed them, but the trainers that
#   got a kill index in v29 (from NUGGET BRIDGE / CERULEAN on) kept standing until the map was reloaded.
#   Predef 0x13 now points to killed13 (2D): the base check first, then (sprite not a gravestone yet) the v29/v34 trainer
#   table and the v28 NPC kill list (kill_chk2). Killed = hidden, exactly like the early trainers; gravestones appear on
#   the next map load as before.
#   v34's extra gravestone pass right after every battle is taken out again (the after-battle stub calls v31's post2
#   directly): the base game's "vanish now, gravestone when you come back" is kept for every trainer.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V34_SHA='f9040003b627db663f4a73fe30fe274fa0e61cd611a1218132fe807264eb5063'
rom=Rom('Creepy_Black_Mu_v34.gb',V34_SHA)
r=rom.r;R=bytes(r)
BANK=0x2d;CODE=0x6200
KC2=int(json.load(open('manifest_v29.json'))['labels']['bank2d']['kill_chk2'],16)
POST2=int(json.load(open('manifest_v31.json'))['labels']['bank2d']['post2'],16)
POST3=int(json.load(open('manifest_v34.json'))['labels']['bank2d']['post3'],16)
PRE=fo(0x13,0x7e79)+3*0x13
assert R[PRE:PRE+3]==bytes([3,0xfb,0x4d])

code,L=asm(f'''
killed13:                        ; predef 0x13: hDividend2 (ffe5) = 1 -> don't draw this sprite (killed trainer)
    farcall $4dfb,3              ; the base check (D486 list)
    ldh a,[$e5]
    and a
    ret nz
    ldh a,[$da]                  ; current sprite offset
    ld e,a
    ld d,$c1
    ld a,[de]
    cp $49
    ret z                        ; already a gravestone: draw it (ffe5 stays 0)
    call {KC2}                   ; v29/v34 trainer table + v28 NPC list: NZ = killed
    ld a,0
    jr z,.o
    inc a
.o: ldh [$e5],a
    ret
''',CODE)
assert CODE+len(code)<0x6400
rom.put(fo(BANK,CODE),code,'Bank 2D: v35 predef 0x13 (killed trainer? base list + v29/v34 table + NPC list)')
rom.data(PRE,bytes([BANK])+L['killed13'].to_bytes(2,'little'),'Predef 0x13 -> killed13 (2D): every killed trainer vanishes at once','03fb4d')
rom.data(0xc5,POST2.to_bytes(2,'little'),'After-battle stub -> post2 again (no extra gravestone pass)',POST3.to_bytes(2,'little'))
rom.finish('Creepy_Black_Mu_v35.gb','manifest_v35.json','CREEPY MU V35',extra=dict(labels=dict(bank2d={k:hex(v) for k,v in L.items()})))
