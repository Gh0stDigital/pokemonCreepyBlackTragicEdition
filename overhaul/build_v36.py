# Creepy Black Mu v36: small fixes and updates.
#   1. GHOST's level is capped at 50 (GainExperience caps its experience at Lv50 instead of Lv100; a GHOST already above
#      50 keeps its level and grows no further), and AGATHA's quest needs GHOST at Lv50 (was Lv100).
#   2. Pokemon Tower 7F (and the player's house / the girls' gyms) no longer turn into garbage after the START menu:
#      the overhaul hides map objects by setting their picture ID to 0, and LoadMapSpriteTilePatterns (5:7871, run
#      again whenever the map is redrawn after a menu) loaded a sprite sheet for picture 0 from the 4 bytes in front of
#      SpriteSheetPointerTable (bank 41 = 1, 255 tiles), over the map tiles. Picture 0 is now skipped.
#   3. GIOVANNI's SILPH defeat line no longer says "GIOVANNI: GIOVANNI:" (the battle engine prints the name already).
#   4. BLUE after the SILPH CO. battle on the GHOST route: he doesn't understand what happened to you, sees you've been
#      corrupted, and vows to find a way to overcome your dark power.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V35_SHA='dc9dd28c7d8a5e3420b3ac3d40a4e42d855d883f18d0b2813de7412982ae65f9'
rom=Rom('Creepy_Black_Mu_v35.gb',V35_SHA)
r=rom.r;R=bytes(r)
def w(o):return R[o]|R[o+1]<<8
labels={}
GHOST=0x1f;CAP=50
PRINTTEXT,TEXTSCRIPTEND=0x3c94,0x2504

# ---- 1a. level cap: GainExperience (15:5308) "call GetMonHeader / ld d,MAX_LEVEL" -> lvcap (same bank)
LV=0x6a90
assert not any(R[fo(0x15,0x6a7e):fo(0x15,0x6b00)])
code,L=asm(f'''
lvcap:                           ; d = highest level this mon may reach (CalcExperience caps its exp there)
    call $155d                   ; GetMonHeader (the replaced call)
    ld d,100
    ld a,[$d0b5]                 ; wCurSpecies
    cp ${GHOST:02x}
    ret nz
    push hl
    ld hl,sp+4                   ; the exp pointer GainExperience pushed (its lowest byte, exp+2)
    ld a,[hl+]
    ld h,[hl]
    ld l,a
    push bc
    ld bc,$11                    ; exp+2 -> level (party struct +$21)
    add hl,bc
    pop bc
    ld a,[hl]
    pop hl
    ld d,{CAP}
    cp {CAP+1}
    ret c                        ; Lv50 or below: cap at 50
    ld d,a                       ; already above 50 (older save): keep its level, no more growth
    ret
''',LV)
rom.put(fo(0x15,LV),code,'Bank 15: v36 GHOST level cap (Lv50)')
rom.hook(fo(0x15,0x5308),'cd'+le(L['lvcap'])+'0000','GainExperience: GHOST max level 50','cd5d15 1664',provides=('a','d','f'))
labels['bank15']={k:hex(v) for k,v in L.items()}

# ---- 1b. AGATHA's stage 3 asks for Lv50 (cp 100 / jr nc,strong)
GF=0x6963                                                    # v16 'gf': ld hl,D18C / ld a,c / ld bc,44 / call AddNTimes / ld a,[hl] / cp 100
assert R[fo(0x2e,GF):fo(0x2e,GF)+7]==bytes.fromhex('218cd179012c00') and R[fo(0x2e,GF)+10:fo(0x2e,GF)+12]==bytes.fromhex('7efe')
rom.data(fo(0x2e,GF)+12,bytes([CAP]),"AGATHA's quest: GHOST must be Lv50 (was Lv100)",'64')

# ---- 2. LoadMapSpriteTilePatterns (5:7871): skip picture ID 0 (an object an overhaul map script hid). The stub is in
#         bank 5 itself (it drops its return address and jumps to .nextSpriteSlot).
B5=0x7f90
assert not any(R[fo(5,0x7f79):fo(5,0x8000)])
code5,L5=asm(f'''
skip0:                           ; hl = this slot's picture ID (C2xE, copied from C2xD); 0 = hidden object
    ld a,[hl]
    and a
    jr z,.none
    ld de,$c21d                  ; the replaced instruction
    ret
.none:
    pop de                       ; drop our return address
    jp $795a                     ; LoadMapSpriteTilePatterns.nextSpriteSlot
''',B5)
rom.put(fo(5,B5),code5,'Bank 5: v36 sprite loader skips picture 0 (hidden object)')
rom.hook(fo(5,0x788d),'cd'+le(L5['skip0']),'LoadMapSpriteTilePatterns: skip picture 0 (no garbage over the map tiles)','111dc2',
         provides=('a','f'))
labels['bank5']={k:hex(v) for k,v in L5.items()}

# ---- 3. GIOVANNI's SILPH defeat text: the battle engine already prints "GIOVANNI:" on line 1
GL=0x7aee
old=txt([["GIOVANNI: Damn","that cult...!"]])
new=txt([["","Damn that cult..."]])
assert R[fo(0x2e,GL):fo(0x2e,GL)+len(old)]==old and len(new)<=len(old)
rom.data(fo(0x2e,GL),new+bytes(len(old)-len(new)),'GIOVANNI SILPH defeat text without his name (engine prints it)',old)

# ---- 4. BLUE after the SILPH CO. 7F battle, GHOST route: corrupted, he vows to overcome the dark power
BLUE=[["What... what","happened to you,","<PLAYER>?"],
      ["That thing isn't","a normal #MON."],
      ["And you...","you're not the","same either."],
      ["Something dark","got into you.","Into both of","you."],
      ["I don't get it.","But I can feel","it..."],
      ["Just beating you","won't be enough.","Not like this."],
      ["I'll find a way","to overcome that","dark power!"],
      ["I swear it,","<PLAYER>!"]]
BT=0x7800
assert not any(R[fo(0x2d,BT):fo(0x2d,BT)+0x200])
bt=txt(BLUE,end=0x57)
rom.put(fo(0x2d,BT),bt,'Bank 2D: v36 BLUE after the SILPH battle (GHOST route)')
TP15=fo(0x14,0x5d3f)+2*14
AFTER=w(TP15);HERO=0x4bd1
assert R[fo(0x14,AFTER):fo(0x14,AFTER)+12]==bytes.fromhex('08'+'21'+le(HERO)+'062e cd1836 21d25e'.replace(' ',''))
W14=0x6b40
assert not any(R[fo(0x14,W14):fo(0x14,W14)+0x40])
code14,L14=asm(f'''
after:
    db 8                         ; TX_ASM
    farcall ${HERO:04x},$2e      ; v12 hero mode (GHOST route)
    ld hl,$5ed2                  ; the original "moving on up" text
    ld a,[$d451]
    and a
    jr z,.p
    ld hl,blue
.p: call ${PRINTTEXT:04x}
    jp ${TEXTSCRIPTEND:04x}
blue:
    db $17
    dw ${BT:04x}
    db $2d,$50
''',W14)
rom.put(fo(0x14,W14),code14,'Bank 14: v36 SILPH 7F BLUE after-battle wrapper')
rom.data(TP15,bytes.fromhex(le(L14['after'])),'SILPH 7F text 15 (BLUE after a win) -> v36 wrapper',le(AFTER))
labels['bank14']={k:hex(v) for k,v in L14.items()}

rom.finish('Creepy_Black_Mu_v36.gb','manifest_v36.json','CREEPY MU V36',extra=dict(labels=labels))
