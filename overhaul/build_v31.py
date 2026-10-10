# Creepy Black Mu v31: GHOST gets its lead slot back after a MIRAGE battle.
#   A MIRAGE battle deposits GHOST in the PC (v3) and withdraws it afterwards; a withdrawn Pokemon always lands in the last
#   party slot. Now the deposit remembers whether GHOST was leading (D45F = 2 instead of 1) and, after the withdrawal, a
#   GHOST that led goes back to slot 1 (the others keep their order). A GHOST that wasn't leading comes back last as before.
#   (The other temporary removals already keep the slot: the Pokemon Center heal (v13) and MR. MU's ritual (v23).)
# Logged patches on top of verified Mu v30 (patchlib).
from patchlib import *
from patchguard import fo
from sm83asm import asm

V30_SHA='b14fa33f93ffc14d8327aada199e047ef568924090a41d325e40c9252a6764d0'
rom=Rom('Creepy_Black_Mu_v30.gb',V30_SHA)
r=rom.r;R=bytes(r)
GHOST=0x1f;DEP=0xd45f
BANK=0x2d;CODE=0x5fc0;STUB2E=0x7cc0
assert R[fo(0x2e,0x4364):fo(0x2e,0x4369)]==bytes.fromhex('3e01ea5fd4')    # deposit: D45F = 1
assert R[0xc4:0xc9]==bytes.fromhex('216047062e')                            # home: far call mirage_post (2E:4760)

# 2E stub: D45F = 2 when the deposited GHOST was slot 1 (wWhichPokemon still holds its slot after RemovePokemon)
s2e,_=asm(f'''
    ld a,[$cf92]
    and a
    ld a,1
    jr nz,.s
    inc a
.s: ld [{DEP}],a
    ret
''',STUB2E)
rom.put(fo(0x2e,STUB2E),s2e,'Bank 2E: MIRAGE deposit remembers whether GHOST led (D45F = 1 / 2)')
rom.hook(fo(0x2e,0x4364),'cd'+le(STUB2E)+'0000','MIRAGE deposit: remember the lead slot','3e01ea5fd4',provides=('a',))

code,L=asm(f'''
post2:                           ; after every battle: MIRAGE cleanup, then GHOST back to the front if it led
    ld a,[{DEP}]
    push af
    farcall $4760,$2e
    pop af
    cp 2
    ret nz
ghost_front:                     ; move GHOST to slot 1, the others keep their order
    ld hl,$d164
    ld c,0
.f: ld a,[hl+]
    cp $ff
    ret z
    cp {GHOST}
    jr z,.g
    inc c
    jr .f
.g: ld a,c
    and a
    ret z
.l: push bc
    ld hl,$d164
    ld b,1
    call swp
    pop bc
    push bc
    ld hl,$d16b
    ld b,44
    call swp
    pop bc
    push bc
    ld hl,$d273
    ld b,11
    call swp
    pop bc
    push bc
    ld hl,$d2b5
    ld b,11
    call swp
    pop bc
    dec c
    jr nz,.l
    ret
swp:                             ; swap entries c-1 and c (b bytes each) of the table at hl
    ld e,b
    ld d,0
    ld a,c
.m: dec a
    jr z,.k
    add hl,de
    jr .m
.k: ld d,h                       ; de = entry c-1, hl = entry c
    ld e,l
    ld a,l
    add b
    ld l,a
    jr nc,.x
    inc h
.x: ld a,[de]
    ld c,a
    ld a,[hl]
    ld [de],a
    ld a,c
    ld [hl+],a
    inc de
    dec b
    jr nz,.x
    ret
''',CODE)
assert CODE+len(code)<0x6400,hex(CODE+len(code))
rom.put(fo(BANK,CODE),code,'Bank 2D: v31 MIRAGE cleanup wrapper + GHOST back to slot 1')
rom.data(0xc4,bytes.fromhex('21'+le(L['post2'])+'06%02x'%BANK),'Home after-battle stub: far call post2 (2D) instead of mirage_post','216047062e')
rom.finish('Creepy_Black_Mu_v31.gb','manifest_v31.json','CREEPY MU V31',extra=dict(labels=dict(bank2d={k:hex(v) for k,v in L.items()})))
