# Creepy Black Mu v93 (on v92): the ritual's HUD levels and sounds, GHOST battle quiet start, OAK leaves PALLET, BLUE's Route 22 gate on the BLACK TAMER path.
#   1. YOU shows Lv10 (was 50), MR. MU shows Lv68: the HUD only (the level is read for the HUD in two places, hooked); stats and damage are unchanged.
#   2. MR. MU's death plays no faint sounds (the fall + thud).  3. The MASTER BALL catch of ????? is silent (the speakers are muted from the toss on; restored in the chamber).
#   4. The GHOST battle (RIT 5/7/8) starts as quietly as MR. MU's (no slide, "Go!", summon animation or cry for the player).
#   5. As BLACK OAK is gone from PALLET (outdoors) and from his lab.  6. Route 22: GHOST acquired + eight badges also switches the rival's "wants a battle" flag off.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V92_SHA='e7a57553bef1ec4f4c8e34225ebaf5fd62fa3d9f15382c3f9bf07e35e3bbd8d0'
rom=Rom('Creepy_Black_Mu_v92.gb',V92_SHA)
R=bytes(rom.r)
def lh(a):return a.to_bytes(2,'little').hex()
RIT,BLACKF,GHOSTACQ=0xd467,0xd46c,0xd451
YOU,MU,SEND_LV_YOU,SEND_LV_MU=0x79,0x20,10,68
BANK,CODE=0x32,0x7800
o=fo(0x18,0x6fc2);assert R[o]==0x21 and R[o+3]==6 and R[o+4:o+7]==bytes([0x30,0xcd,0x18]);CH=R[o+1]|R[o+2]<<8;assert CH==0x4da7
o=fo(6,0x6d72);assert R[o:o+6].hex()=='2100640631cf';PAL=0x6400
o=fo(7,0x7f70);assert R[o:o+6].hex()=='210054063' '2cd'.replace(' ','');LAB=0x5400
assert not any(R[fo(BANK,CODE):fo(BANK,CODE+0x200)])
code,L=asm(f'''
; (F:4DBC) the player's HUD level: the original copy of 11 bytes, then YOU shows Lv{SEND_LV_YOU}
ply93:
    ld hl,$d022
    ld de,$cfb9
    ld bc,$000b
    call $00b5
    ld a,[$d014]
    cp {YOU}
    ret nz
    ld a,{SEND_LV_YOU}
    ld [$cfb9],a
    ret
; (F:4E45) the enemy's HUD level (hl = $c3b8 as the code before it left it): MR. MU shows Lv{SEND_LV_MU}
en93:
    ld a,[$cff3]
    ld [$cfb9],a
    ld a,[$cfe5]
    cp {MU}
    jr nz,.o
    ld a,{SEND_LV_MU}
    ld [$cfb9],a
.o: ld hl,$c3b8
    ret
; (F:45C9) the enemy's faint sounds (fall, thud): none for MR. MU in the ritual
faint93:
    ld a,[$cfe5]
    cp {MU}
    jr nz,.n
    ld a,[{RIT:#x}]
    cp 1
    ret z
.n: ld a,$9e
    call $377a
.w: ld a,[$c02a]
    cp $9e
    jr z,.w
    ld a,$95
    call $23de
    jp $3782
; (F:7FB8 stub) v77's pre77 + the GHOST battle (RIT 5 / 7 / 8)
pre93:
    ld hl,$c405
    xor a
    ld [$d45a],a
    ld a,[$cf91]
    cp $7f
    jr z,.q
    cp {YOU}
    ret nz
    ld a,[{RIT:#x}]
    cp 1
    jr z,.q
    cp 5
    jr z,.q
    cp 7
    jr z,.q
    cp 8
    ret nz
.q: ld a,1
    ld [$d45a],a
    ld hl,sp+4
    ld a,$dc
    ld [hl+],a
    ld [hl],$41
    ret
; chamber map script (every frame): after the ritual the speakers come back (muted for the catch), then the old script
chm93:
    ld a,[{RIT:#x}]
    cp 3
    jr c,.o
    ldh a,[$26]
    bit 7,a
    jr nz,.o
    ld a,$80
    ldh [$26],a
    ld a,$77
    ldh [$24],a
    ld a,$ff
    ldh [$25],a
.o: ld hl,{CH:#x}
    ld b,$30
    jp $3618
; PALLET map script (every frame): as BLACK OAK (picture 3, object 1) is gone, then pal66
pal93:
    ld a,[{BLACKF:#x}]
    and a
    jr z,.o
    ld a,[$c110]
    cp 3
    jr nz,.o
    ld a,$ff
    ld [$c112],a
    ld [$c214],a
    ld [$c215],a
    ld [$c216],a
.o: ld hl,{PAL:#x}
    ld b,$31
    jp $3618
; OAK'S LAB map script (every frame): as BLACK OAK (picture 3) is gone; then lab86
lab93:
    ld a,[{BLACKF:#x}]
    and a
    jp z,{LAB:#x}
    ld c,1
.l: ld a,c
    swap a
    ld l,a
    ld h,$c1
    ld a,[hl]
    cp 3
    jr nz,.n
    inc l
    inc l
    ld a,$ff
    ld [hl],a
    ld a,c
    swap a
    add 4
    ld l,a
    ld h,$c2
    ld a,$ff
    ld [hl+],a
    ld [hl],a
.n: inc c
    ld a,c
    cp 12
    jr nz,.l
    jp {LAB:#x}
''',CODE)
rom.put(fo(BANK,CODE),code,'Bank 32: v93 ritual HUD levels / silent faint / GHOST battle start / OAK gone (PALLET, lab) / chamber speakers')

J=lambda n:bytes.fromhex(lh(L[n]))
# 1. HUD levels
o=fo(0xf,0x4dbc);assert R[o:o+12].hex()=='2122d011b9cf010b00cdb500'
rom.code(o,bytes.fromhex('21')+J('ply93')+bytes([6,BANK,0xcf])+bytes(6),'Player HUD level: the copy + YOU shows Lv10 (ply93)',R[o:o+12].hex(),reviewed='the far routine repeats the 11-byte copy; hl/de/bc are loaded again by the code that follows')
o=fo(0xf,0x4e45);assert R[o:o+6].hex()=='faf3cfeab9cf'
rom.code(o,bytes.fromhex('21')+J('en93')+bytes([6,BANK,0xcf]),'Enemy HUD level: MR. MU shows Lv68 (en93)',R[o:o+6].hex(),reviewed='en93 sets wLoadedMonLevel and hl = $c3b8 (the value popped just before) for the PrintLevel call that follows')
# 2. faint sounds
o=fo(0xf,0x45c9);assert R[o:o+20].hex()=='3e9ecd7a37fa2ac0fe9e28f93e95cdde23cd8237'
rom.code(o,bytes.fromhex('21')+J('faint93')+bytes([6,BANK,0xcf])+bytes(14),'Enemy faint sounds -> faint93 (none for MR. MU)',R[o:o+20].hex(),reviewed='faint93 repeats the sounds and the wait loop; the jr at 45DD follows')
# 3. MASTER BALL catch silent: bank 1 prefix, predef 08 entry
P=fo(0x13,0x7e79)
WR=0x7d60
assert not any(R[fo(1,WR):fo(1,WR+0x20)]) and R[P+24:P+27].hex()=='01207d'
rom.put(fo(1,WR),bytes.fromhex('fa67d4fe022003af e026c3207d'.replace(' ','')),'Bank 1: v93 predef 08 prefix (MASTER BALL toss in the ritual: APU off)')
rom.data(P+24,bytes([1,WR&255,WR>>8]),'Predef 08 MoveAnimation -> v93 prefix','01207d')
o=fo(0x18,0x6fc2)
rom.data(o+1,bytes.fromhex(lh(L['chm93']))+bytes([6,BANK]),'Chamber script -> chm93 (speakers back after the ritual)',R[o+1:o+5].hex())
# 4. GHOST battle quiet start
o=fo(0xf,0x7fb8);assert R[o:o+8].hex()=='2117440630c31836'
rom.data(o+1,bytes.fromhex(lh(L['pre93']))+bytes([6,BANK]),'Battle start stub -> pre93 (quiet start also in the GHOST battle)',R[o+1:o+5].hex())
# 5. OAK gone
o=fo(6,0x6d72);rom.data(o+1,bytes.fromhex(lh(L['pal93']))+bytes([6,BANK]),'Pallet script far call -> pal93',R[o+1:o+5].hex())
o=fo(7,0x7f70);rom.data(o+1,bytes.fromhex(lh(L['lab93'])),'OAK\'S LAB script wrapper -> lab93',lh(LAB))
# 6. Route 22 gate
G=fo(0x14,0x6b60);assert R[G:G+18].hex()=='fa63d447fa6cd4b0280521ebd7cbbec3b24e'
cg,LG=asm(f'''
gate86:
    ld a,[$d463]
    ld b,a
    ld a,[{BLACKF:#x}]
    or b
    jr nz,.clr
    ld a,[{GHOSTACQ:#x}]
    and a
    jr z,.go
    ld a,[$d356]
    cp $ff
    jr nz,.go
.clr: ld hl,$d7eb
    res 7,[hl]
.go:jp $4eb2
''',0x6b60)
assert len(cg)<=0x20 and not any(R[G+18:G+0x20])
old=R[G:G+len(cg)]
rom.code(G,cg,'Route 22 gate: also GHOST acquired + eight badges (BLACK TAMER path)',old.hex(),reviewed='map header script entry rewritten from its first byte; jp 4EB2 as before')
rom.finish('Creepy_Black_Mu_v93.gb','manifest_v93.json','CREEPY MU V93')
