# Creepy Black Mu v96 (on v95):
#   1. Indoor maps with two four-tile pictures already (VICTORY ROAD: item ball $3D + boulder $3F) get no gravestones at map load: a gravestone ($49) was a third
#      four-tile picture, only two VRAM slots exist ($8780/$87C0), so the item balls (or boulders) drew another picture's tiles.  The killed trainer stays hidden
#      instead (predef 0x13 -> killed74 -> frame40 -> kill_chk2 hides it every frame, as right after the battle).  Outdoor maps and every other indoor map as before.
#   2. The Champion's battle (BLUE, class $2B) plays the victory music again (v86 had silenced it with the League / OAK / BILL battles).
from patchlib import *
from patchguard import fo
from sm83asm import asm
V95_SHA='a40d294ca5c61ec55006fa219e4cb9033d26a66b15b0f0f7e7ae8291e1a3bb9a'
rom=Rom('Creepy_Black_Mu_v95.gb',V95_SHA)
R=bytes(rom.r)
def lh(a):return a.to_bytes(2,'little').hex()
# 1. map-load gravestones (3:4E85 loop: call 4DFB / call 0:1688 (far call 2D:7E40 load40) / jr z / ld [de],$49)
assert R[0x1688:0x1690].hex()=='21407e062dc31836'
A=0x4c00
assert not any(R[fo(0x2d,A):fo(0x2d,A)+0x40])
c,L=asm(f'''
grave96:                         ; load40, then: NZ (= becomes a gravestone) only if the map has room for a third four-tile picture
    call $7e40
    ret z
    ld a,[$d35e]
    cp $25
    jr c,.yes                    ; outdoor maps: their sprite set decides (v72)
    ld hl,$c110
    ld a,[$d4e1]
    and a
    jr z,.yes
    ld c,a
    ld b,0                       ; b = the first four-tile picture seen
.l: ld a,[hl]
    cp $3d
    jr c,.n
    cp $47
    jr z,.n
    cp $49
    jr z,.n
    ld d,a
    ld a,b
    and a
    jr z,.first
    cp d
    jr nz,.no                    ; a second, different four-tile picture: no slot left for a gravestone
    jr .n
.first:
    ld b,d
.n: ld a,l
    add $10
    ld l,a
    dec c
    jr nz,.l
.yes:
    or 1
    ret
.no:
    xor a
    ret
''',A,{})
rom.put(fo(0x2d,A),c,'Bank 2D: v96 grave96 (no map-load gravestone where two four-tile pictures already fill the slots)')
rom.code(0x1689,bytes.fromhex(lh(L['grave96'])),'0:1688 map-load gravestone far call: load40 -> grave96',lh(0x7e40),reviewed='operand of ld hl in the far-call stub; grave96 calls load40 first and keeps e (the sprite offset); d is reloaded by the caller')
# 2. BLUE's victory music: the quiet-class list 21 2C 2E 2F 2B 1A -> 2B replaced by 21 (a duplicate)
Q=fo(0x32,0x5233);assert R[Q:Q+7].hex()=='212c2e2f2b1aff'
rom.data(Q+4,bytes([0x21]),'vict86 quiet list: BLUE (RIVAL3 $2B) plays the victory music again','2b')
rom.finish('Creepy_Black_Mu_v96.gb','manifest_v96.json','CREEPY MU V96')
