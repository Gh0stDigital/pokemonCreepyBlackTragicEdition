# Creepy Black Mu v85: the player's name stays BLACK after the POKeMON LEAGUE (v84 put RED back when you left the League rooms).
#   name85 replaces v84's name84 at the end of the map-load chain: the first time BLACK (D46C) loads a League room (F5-F7, 71) the real name is backed up (D879-D883)
#   and D158 becomes BLACK for good (D884 = 1); nothing restores it. BLUE's own champion speeches say RED literally (v58), unchanged.
from patchlib import *
from patchguard import fo
from sm83asm import asm

V84_SHA='b0124759a16851c0902e9cde21f24158bbed366cb4b2b2802f7b2ab308b8d244'
rom=Rom('Creepy_Black_Mu_v84.gb',V84_SHA)
R=bytes(rom.r)
B=fo(0x2e,0x5d00);assert not any(R[B:B+0x80])
c,L=asm('''
name85:
    push af
    push bc
    push de
    push hl
    ld a,[$d46c]
    and a
    jr z,.done
    ld a,[$d884]
    and a
    jr nz,.done
    ld a,[$d35e]
    cp $71
    jr z,.lg
    cp $f5
    jr c,.done
    cp $f8
    jr nc,.done
.lg:
    ld hl,$d158
    ld de,$d879
    ld bc,11
    call $00b5
    ld hl,blk
    ld de,$d158
    ld bc,11
    call $00b5
    ld a,1
    ld [$d884],a
.done:
    pop hl
    pop de
    pop bc
    pop af
    jp $7c8b
blk: db $81,$8b,$80,$82,$8a,$50,0,0,0,0,0
''',0x5d00)
rom.put(B,c,'Bank 2E: v85 name85 (the name becomes BLACK in the LEAGUE and stays)')
o=fo(0x2e,0x42b4);assert R[o:o+3].hex()=='c3005c'
rom.code(o,bytes([0xc3,L['name85']&255,L['name85']>>8]),'Map load chain end: name84 -> name85','c3005c')
rom.finish('Creepy_Black_Mu_v85.gb','manifest_v85.json','CREEPY MU V85')
