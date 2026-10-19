# Creepy Black Mu v83: METAMORPHOSIS on a trainer's POKeMON behaves like CURSE towards the trainer:
#   * no faint animation / "Enemy <MON> fainted!" (the curse-kill flag CC39 = 1 skips both, as for CURSE),
#   * D452 (CURSE used this battle) is set, so the trainer reacts like to a CURSE: frightened end-of-battle text, sulking afterwards (v69), notoriety (v71),
#     BLUE's replacement POKeMON (v45 keys on CC39).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V82_SHA='074748e921748b3fefc78c9f1b45c9c686497890a169fb4fe20a61e36bab3946'
rom=Rom('Creepy_Black_Mu_v82.gb',V82_SHA)
R=bytes(rom.r)
B31=0x31;C31=0x5900
assert not any(R[fo(B31,C31):fo(B31,C31)+0x80])
c,L=asm('''
meta83:                          ; far-called from bane_move's trainer branch (2F:4069): the POKeMON is gone like after a CURSE
    xor a
    ld [$cfe6],a
    ld [$cfe7],a                 ; enemy HP 0
    inc a
    ld [$cc39],a                 ; curse kill: no faint animation, no "fainted!" text
    ld [$d452],a                 ; CURSE used in this battle
    ret
''',C31)
rom.put(fo(B31,C31),c,'Bank 31: v83 meta83 (METAMORPHOSIS on a trainer\'s POKeMON = CURSE kill + CURSE flag)')
o=fo(0x2f,0x4069);old=R[o:o+7];assert old.hex()=='afeae6cfeae7cf'
rom.code(o,bytes([0x21,L['meta83']&255,L['meta83']>>8,0x06,B31,0xcf,0]),'bane_move (trainer): far call meta83 instead of zeroing HP only',old.hex(),
         reviewed='a/b/c/hl are reloaded by the following ld hl,sp+6 / ld a,imm; the far call keeps the stack (return address at [sp+6] as before)')

# ---- pitch-black pictures: holes (white bodies, eyes, highlights) enclosed on all four sides are filled
BLK47=int(json.load(open('manifest_v47.json'))['labels']['bank2f']['blacken'],16)
C2=0x5980
assert not any(R[fo(B31,C2):fo(B31,C2)+0x200])
XMAX,SEEN=0xa0f0,0xa0f1
c2,L2=asm(f'''
fill83:                          ; far-called in place of  call blacken / ld de,$a188  (2F:7676 and 2F:7693)
    ld hl,{BLK47:#x}
    ld b,$2f
    db $cf                       ; rst 08: far call blacken (SRAM on, every non-white pixel black)
    ld hl,$a000                  ; first[56] = ff, last[56] = 0 (the free sSpriteBuffer0)
    ld b,56
    ld a,$ff
.i1: ld [hl+],a
    dec b
    jr nz,.i1
    ld b,56
    xor a
.i2: ld [hl+],a
    dec b
    jr nz,.i2
    ld d,0                       ; pass 1: first / last black row of every column
.y1:
    call rowptr
    ld e,0
.c1:
    ld a,[hl]
    ld c,a
    ld b,8
.b1:
    rl c
    jr nc,.n1
    push hl
    call mark
    pop hl
.n1:
    inc e
    dec b
    jr nz,.b1
    ld a,l
    add 112
    ld l,a
    jr nc,.k1
    inc h
.k1:
    ld a,e
    cp 56
    jr c,.c1
    inc d
    ld a,d
    cp 56
    jr c,.y1
    ld d,0                       ; pass 2: per row, white pixels between black ones whose column has black above and below -> black
.y2:
    xor a
    ld [{XMAX:#x}],a
    ld [{SEEN:#x}],a
    call rowptr
    ld e,0
.c2:
    ld a,[hl]
    ld c,a
    ld b,8
.b2:
    rl c
    jr nc,.n2
    ld a,e
    ld [{XMAX:#x}],a
.n2:
    inc e
    dec b
    jr nz,.b2
    ld a,l
    add 112
    ld l,a
    jr nc,.k2
    inc h
.k2:
    ld a,e
    cp 56
    jr c,.c2
    call rowptr
    ld e,0
.c3:
    ld b,$80
.b3:
    ld a,[hl]
    and b
    jr z,.wh
    ld a,1
    ld [{SEEN:#x}],a
    jr .n3
.wh:
    ld a,[{SEEN:#x}]
    and a
    jr z,.n3
    ld a,[{XMAX:#x}]
    cp e
    jr c,.n3
    jr z,.n3
    push hl
    ld h,$a0
    ld l,e
    ld a,[hl]
    cp d
    jr nc,.sk
    ld a,l
    add $38
    ld l,a
    ld a,[hl]
    cp d
    jr c,.sk
    jr z,.sk
    pop hl
    ld a,[hl]
    or b
    ld [hl+],a
    ld a,[hl]
    or b
    ld [hl-],a
    jr .n3
.sk:
    pop hl
.n3:
    inc e
    srl b
    jr nz,.b3
    ld a,l
    add 112
    ld l,a
    jr nc,.k3
    inc h
.k3:
    ld a,e
    cp 56
    jr c,.c3
    inc d
    ld a,d
    cp 56
    jr c,.y2
    ld de,$a188
    ret
rowptr:                          ; d = pixel row -> hl = $a188 + 2*d (the byte of tile column 0)
    ld a,d
    add a
    add $88
    ld l,a
    ld h,$a1
    ret
mark:                            ; e = x, d = y
    ld h,$a0
    ld l,e
    ld a,[hl]
    cp $ff
    jr nz,.s
    ld [hl],d
.s: ld a,l
    add $38
    ld l,a
    ld [hl],d
    ret
''',C2)
rom.put(fo(B31,C2),c2,'Bank 31: v83 fill83 (black pictures: enclosed holes filled)')
for site in (0x7676,0x7693):
    o=fo(0x2f,site);old=R[o:o+6];assert old.hex()==('cd'+le(BLK47)+'1188a1'),old.hex()
    rom.code(o,bytes([0x21,L2['fill83']&255,L2['fill83']>>8,0x06,B31,0xcf]),'black picture: far call fill83 (blacken + hole fill + ld de,$a188)',old.hex(),
             reviewed='fill83 ends with ld de,$a188 (d/e survive the far call), the next instruction is ld hl,imm16')
rom.finish('Creepy_Black_Mu_v83.gb','manifest_v83.json','CREEPY MU V83',extra=dict(labels=dict(bank31={k:hex(v) for k,v in {**L,**L2}.items()})))
