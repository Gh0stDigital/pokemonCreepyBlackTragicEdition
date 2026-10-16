# Creepy Black Mu v72: the SNORLAX (and item balls) on the routes drew the wrong pictures.
#   Gen-1 outdoor sprite sets are loaded in order: entries 1-9 are the 12-tile walkers (VRAM slots 2-10), entries 10 and 11 the two four-tile pictures (slots 0B/0C).
#   An object finds its VRAM slot as (its picture's position in the set) + 1, so a four-tile picture only works at position 10 or 11.
#   The hack's own set 12 (a copy of vanilla set 8 with the gravestone 49 added) was [... 21, 43 SNORLAX, 3D BALL, 49 GRAVESTONE]: SNORLAX sat at position 9
#   (slot 10, a walker slot: it showed whatever walker had been there, a GUARD / CHANNELER = "a normal NPC"), the BALL at position 10 (slot 0B, where the loader had put SNORLAX's
#   tiles: item balls on ROUTES 13-17 looked like Snorlax pieces) and the third four-tile picture overwrote the ball tiles in slot 0C.
#   Fixes: set 12 = [... 21, 05, 3D, 49] (vanilla set 8's walker 05 back in position 9: valid order, gravestones kept; no Snorlax needed on ROUTES 13/14/15/17/16 west);
#   ROUTE 12 south of y 21 uses the vanilla set 8 [... 05, 3D, 43 SNORLAX] (position-set table F4, B: 12 -> 8). ROUTE 16 east already used set 5 (Snorlax at 11).
#   Known limit: ROUTE 12's south half has no gravestone picture (three four-tile pictures cannot fit two slots): see README_v72.
from patchlib import *
from patchguard import fo

V71_SHA='259eda58e913ee29e97f542dfca03c284a10516cf8df765a1a2b435cba24a5ef'
rom=Rom('Creepy_Black_Mu_v71.gb',V71_SHA)
R=bytes(rom.r)
SETS=fo(5,0x7ab9);F=fo(5,0x7a89)
o=SETS+11*11
assert R[o:o+11].hex()=='120c0a0607 0f2f21433d49'.replace(' ',''),R[o:o+11].hex()
rom.data(o+8,bytes([0x05]),'Sprite set 12: position 9 = walker 05 (was SNORLAX 43, which only works at position 10/11)','43')
assert R[F+3*4:F+3*4+4].hex()=='0215030c'
rom.data(F+3*4+3,bytes([0x08]),'ROUTE 12 south set (position table F4, B): 12 -> 8 (vanilla set 8 ends 3D, 43 SNORLAX)','0c')
# 3. ROUTE 12 south (set 8) has no gravestone picture (three four-tile pictures: SNORLAX, BALL, GRAVESTONE do not fit the two four-tile slots). A killed trainer's
#    picture 49 was looked up past the end of the 11-byte set and drew garbage tiles (slot $95). InitOutsideMapSprites' lookup (5:7A01..7A07) now stops after the
#    set: an object with picture 49 that is not in the set is hidden (picture 0) instead of drawn with garbage; every other picture behaves as before.
from sm83asm import asm
G5=0x7f9c;H5=0x7ff1
assert not any(R[fo(5,G5):fo(5,G5)+20]) and not any(R[fo(5,H5):fo(5,H5)+15])
stub,_=asm('''
g72:
    jr nz,.nf
    inc c
    jp $7a08
.nf:
    ld a,c
    cp 11
    jp c,$7a01             ; still inside the set: keep looking
    jp $7ff1
''',G5,{})
stub2,_=asm('''
h72:
    ld a,b
    cp $49
    jp nz,$7a01            ; any other missing picture: the old (garbage) behaviour
    xor a
    ld [hl],a              ; a gravestone the set doesn't have: hide the object
    ld c,a
    jp $7a08
''',H5,{})
assert len(stub)<=20 and len(stub2)<=15,(len(stub),len(stub2))
rom.put(fo(5,G5),stub,'Bank 5: v72 sprite slot lookup stub')
rom.put(fo(5,H5),stub2,'Bank 5: v72 sprite slot lookup stub, not found (gravestone -> hidden)')
o=fo(5,0x7a05);assert R[o:o+3].hex()=='20fa0c'
rom.hook(o,bytes([0xc3,G5&255,G5>>8]),'InitOutsideMapSprites picture lookup: bounded, hides a missing gravestone','20fa0c',provides=('c','f'),
         reviewed='the stub reproduces  jr nz,7A01 / inc c  and continues at 7A08 (the instruction after the replaced bytes); only the not-found case is new')
rom.finish('Creepy_Black_Mu_v72.gb','manifest_v72.json','CREEPY MU V72')
