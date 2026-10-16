# Creepy Black Mu v68: the MIRAGE encounter chance.
#   1. The chance no longer jumps to its cap quickly: it grows with every victim (every CURSE use, counter D45C, saturating at 255) and reaches the old maximum
#      (64/256 = 25%) at 100 victims: chance = victims * 164/256 (0.64 per victim), capped at 64.   (v3-v67: 2 per victim, the cap at 32.)
#   2. As BLACK (D46C) the MIRAGE never appears in wild encounters.
# The roll is at 2E:4310..4325 (counter test + chance); it becomes a jp to m68 (2E:4280, free), which ends with a jp back to 2E:4326 (the roll itself).
from patchlib import *
from sm83asm import asm
from patchguard import fo

V67_SHA='d8ff15fe722ac08f8531e5db60f8877ee1c57f1e72cb3cebe8e1f90224bb310e'
rom=Rom('Creepy_Black_Mu_v67.gb',V67_SHA)
R=bytes(rom.r)
o=fo(0x2e,0x4310);old=R[o:o+22].hex()
assert old=='fa5cd4a7c84faf'+'c6023809fe4030050d20f51802'+'3e40',old
A=0x4280
code,_L=asm('''
m68:
    ld a,[$d46c]
    and a
    ret nz               ; BLACK: no MIRAGE
    ld a,[$d45c]
    and a
    ret z                ; no victim yet
    ld c,a
    ld hl,0
    ld de,164
.l:
    add hl,de
    dec c
    jr nz,.l
    ld a,h               ; chance = victims * 164 / 256
    cp 64
    jr c,.ok
    ld a,64
.ok:
    jp $4326
''',A,{})
rom.put(fo(0x2e,A),code,'Bank 2E: v68 MIRAGE chance (grows to 25% at 100 victims, none as BLACK)')
rom.code(o,bytes([0xc3,A&255,A>>8])+bytes(19),'Mirage roll: counter test + chance -> m68',old,
         reviewed='the replaced block is only entered from its start (mirage_start falls through); m68 ends with a jp to the roll at 2E:4326')
rom.finish('Creepy_Black_Mu_v68.gb','manifest_v68.json','CREEPY MU V68')
