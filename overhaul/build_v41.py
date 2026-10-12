# Creepy Black Mu v41: CONSUME (part 4 of the BLACK TAMER mechanics).
#   Outside battles BLACK's party-menu entry offers CONSUME (shown like a field move; BANE is BLACK's "field move").
#   CONSUME: "Consume which #MON?" -> pick a party member (not BLACK, PRETA or AZHI) -> "Take which move?" -> pick one of
#   its moves -> BLACK learns it (the game's own LearnMove: with 4 moves BLACK forgets one of them; BANE can't be
#   forgotten) -> "BLACK consumed <MON>!": the POKeMON is gone, BLACK gains its whole experience total; a new level
#   recomputes BLACK's stats at level + 9 ("BLACK grew to level N!"). No level cap besides the game's Lv100.
#   Cancelling the move choice or LearnMove keeps everything as it was.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V40_SHA='9b79453a00034a6c7c1676c63bc7acddb7367018b0f0dc680085a132e9b4233d'
rom=Rom('Creepy_Black_Mu_v40.gb',V40_SHA)
r=rom.r;R=bytes(r)
BANE,BLK,PRETA,AZHI=0xaa,0x7f,0xb6,0xb7
PRINTTEXT,PARTYMENU,ADDNTIMES,COPYDATA=0x3c94,0x142b,0x3abb,0x00b5
TEXTBOX,PLACESTRING,MENUINPUT,MOVENAME,SAVESCR,LOADSCR,LOADMON,CALCSTATS=0x194f,0x1982,0x3af2,0x3089,0x3753,0x375f,0x13ab,0x396a
PARTYMONNAME=0x15e0
BANK=0x2f;CODE=0x5400
assert not any(R[fo(BANK,CODE):fo(BANK,0x8000)])
labels={}

# ---- bank 1: field-move tables with CONSUME (BANE) as entry 10
FMD=fo(1,0x781c);old_fmd=R[FMD:FMD+28];assert old_fmd[-1]==0xff and len(old_fmd)==28
FMN=fo(1,0x7786);names=R[FMN:FMN+0x48];end=names.index(enc('SOFTBOILED')+b'\x50')+len('SOFTBOILED')+1
old_names=names[:end];assert old_names.count(b'\x50')==9     # CUT FLY (empty 3rd) SURF STRENGTH FLASH DIG TELEPORT SOFTBOILED = names 1-9
B1=0x7d80
assert not any(R[fo(1,B1):fo(1,0x8000)])
new_fmd=old_fmd[:-1]+bytes([BANE,0x0a,0x0b,0xff])
new_names=old_names+enc('CONSUME')+b'\x50'
c1,L1=asm(f'''
fm_data: db {','.join(str(x) for x in new_fmd)}
fm_names: db {','.join(str(x) for x in new_names)}
ishm41:                          ; LearnMove's "is it an HM?" check: BANE can't be forgotten either
    cp {BANE}
    scf
    ret z
    jp $307a
''',B1)
rom.put(fo(1,B1),c1,'Bank 1: field-move tables with CONSUME (BANE), BANE unforgettable')
labels['bank1']={k:hex(v) for k,v in L1.items()}
def find_in(bank,lo,hi,pat):
    s=R[fo(bank,lo):fo(bank,hi)];i=s.find(pat);assert i>=0 and s.find(pat,i+1)<0,(pat.hex(),i);return fo(bank,lo)+i
a=find_in(1,0x77cf,0x781c,bytes.fromhex('211c78'))
rom.data(a+1,bytes.fromhex(le(L1['fm_data'])),'GetMonFieldMoves: field-move table with CONSUME','1c78')
a=find_in(1,0x76da,0x7786,bytes.fromhex('218677'))
rom.data(a+1,bytes.fromhex(le(L1['fm_names'])),'DisplayFieldMoveMonMenu: names with CONSUME','8677')
a=find_in(1,0x6e3c,0x7000,bytes.fromhex('cd7a30'))
rom.hook(a,'cd'+le(L1['ishm41']),'LearnMove: BANE can\'t be forgotten','cd7a30',provides=('f',))

# ---- texts (2F)
def tx(*parts):
    out=bytearray();inside=False
    for p in parts:
        if isinstance(p,tuple):
            if inside:out.append(0x50);inside=False
            if p[0]=='ram':out+=bytes([1,p[1]&255,p[1]>>8])
            else:out+=bytes([9,p[1]&255,p[1]>>8,0x13])
        else:
            if not inside:out.append(0);inside=True
            out+={'line':b'\x4f','cont':b'\x55','para':b'\x51'}.get(p,None) or enc(p)
    if not inside:out.append(0)
    out+=b'\x58';return bytes(out)
T={'t_which':tx('Consume which','line','#MON?'),
   't_cant':tx('BLACK can\'t','line','consume that.'),
   't_take':tx('Take which move?'),
   't_knows':tx('BLACK already','line','knows that move.'),
   't_ate':tx('BLACK consumed','line',('ram',0xcd6d),'!'),
   't_grew':tx('BLACK grew to','line','level ',('num',0xd45a),'!')}
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())

SRC=f'''
consume:                         ; from BLACK's party submenu (wWhichPokemon = BLACK)
    ld a,[$cf92]
    ld [$d457],a                 ; BLACK's slot
    ld hl,t_which
    call {PRINTTEXT:#x}
    xor a
    ld [$d07d],a
    call {PARTYMENU:#x}
    ret c
    ld a,[$cf91]
    cp {BLK}
    jp z,.cant
    cp {PRETA}
    jp z,.cant
    cp {AZHI}
    jp z,.cant
    ld a,[$cf92]
    ld [$d458],a                 ; the victim's slot
    call pick_move
    and a
    ret z
    ld [$d459],a
    ld b,a                       ; BLACK knows it already?
    ld a,[$d457]
    ld hl,$d173
    ld de,44
    call mul_add
    ld c,4
.k: ld a,[hl+]
    cp b
    jp z,.knows
    dec c
    jr nz,.k
    ld a,[$d459]                 ; LearnMove on BLACK
    ld [$d0e0],a
    ld [$d11e],a
    call {MOVENAME:#x}
    ld hl,$cd6d
    ld de,$cf4b
    ld bc,11
    call {COPYDATA:#x}
    ld a,[$d457]
    ld [$cf92],a
    farcall $6e3c,1              ; LearnMove (its b result is lost in the far call: look at BLACK's moves instead)
    ld a,[$d459]
    ld b,a
    ld a,[$d457]
    ld hl,$d173
    ld de,44
    call mul_add
    ld c,4
.l2:ld a,[hl+]
    cp b
    jr z,.learned
    dec c
    jr nz,.l2
    ret                          ; gave up learning: nothing consumed
.learned:
    ld a,[$d458]                 ; "BLACK consumed <MON>!"
    ld hl,$d2b5
    call {PARTYMONNAME:#x}
    ld hl,t_ate
    call {PRINTTEXT:#x}
    call eat
    jp grow
.cant:
    ld hl,t_cant
    jp {PRINTTEXT:#x}
.knows:
    ld hl,t_knows
    jp {PRINTTEXT:#x}

mul_add:                         ; hl += a * de
    and a
    ret z
.l: add hl,de
    dec a
    jr nz,.l
    ret

pick_move:                       ; the victim's moves in a menu: a = move id, 0 = cancelled
    call {SAVESCR:#x}
    ld hl,t_take
    call {PRINTTEXT:#x}
    ld hl,$c3a0+2*20+4
    ld b,8
    ld c,12
    call {TEXTBOX:#x}
    ld a,[$d458]
    ld hl,$d173
    ld de,44
    call mul_add
    ld b,0                       ; b = number of moves
    ld de,$c3a0+3*20+6
.n: ld a,[hl+]
    and a
    jr z,.menu
    push hl
    push de
    push bc
    ld [$d11e],a
    call {MOVENAME:#x}
    pop bc
    pop hl
    push hl
    push bc
    ld de,$cd6d
    call {PLACESTRING:#x}
    pop bc
    pop de
    ld hl,40
    add hl,de
    ld d,h
    ld e,l
    pop hl
    inc b
    ld a,b
    cp 4
    jr nz,.n
.menu:
    ld a,b
    and a
    jr z,.none
    dec a
    ld [$cc28],a                 ; wMaxMenuItem
    ld hl,$cc24
    ld a,3
    ld [hl+],a                   ; wTopMenuItemY
    ld a,5
    ld [hl+],a                   ; wTopMenuItemX
    xor a
    ld [hl+],a                   ; wCurrentMenuItem
    inc hl
    inc hl
    ld a,3
    ld [hl+],a                   ; wMenuWatchedKeys: A, B
    xor a
    ld [hl],a                    ; wLastMenuItem
    ld hl,$fff6
    set 1,[hl]                   ; double-spaced menu
    call {MENUINPUT:#x}
    ld hl,$fff6
    res 1,[hl]
    push af
    call {LOADSCR:#x}
    pop af
    bit 1,a
    jr nz,.none
    ld a,[$d458]
    ld hl,$d173
    ld de,44
    call mul_add
    ld a,[$cc26]
    ld e,a
    ld d,0
    add hl,de
    ld a,[hl]
    ret
.none:
    call {LOADSCR:#x}
    xor a
    ret

eat:                             ; BLACK += the victim's experience (capped at Lv100), the victim leaves the party
    ld a,[$d458]
    ld hl,$d179                  ; party mon 1 exp (+14)
    ld de,44
    call mul_add
    ld a,[hl+]
    ld b,a
    ld a,[hl+]
    ld c,a
    ld a,[hl]
    ld e,a                       ; victim exp = b:c:e
    ld a,[$d457]
    ld hl,$d17b                  ; BLACK exp low byte (+16)
    push de
    ld de,44
    call mul_add
    pop de
    ld a,[hl]
    add e
    ld [hl-],a
    ld a,[hl]
    adc c
    ld [hl-],a
    ld a,[hl]
    adc b
    ld [hl],a
    jr c,.cap
    cp $13                       ; Lv100 (slow growth) = $1312D0
    jr c,.ok
    jr nz,.cap
    inc hl
    ld a,[hl]
    cp $12
    dec hl
    jr c,.ok
    jr nz,.cap
    inc hl
    inc hl
    ld a,[hl]
    dec hl
    dec hl
    cp $d0
    jr c,.ok
.cap:
    ld [hl],$13
    inc hl
    ld [hl],$12
    inc hl
    ld [hl],$d0
.ok:
    ld a,[$d458]                 ; remove the victim
    ld [$cf92],a
    xor a
    ld [$cf95],a
    farcall $7b61,1
    ld hl,$d164                  ; BLACK's slot again (it moves up if the victim was before it)
    ld c,0
.f: ld a,[hl+]
    cp {BLK}
    jr z,.got
    inc c
    jr .f
.got:
    ld a,c
    ld [$d457],a
    ret

grow:                            ; new level from the experience; stats at level + 9
    ld a,[$d457]
    ld [$cf92],a
    xor a
    ld [$cc49],a
    call {LOADMON:#x}
    farcall $4f43,$16            ; CalcLevelFromExperience -> d
    ld a,[$d457]
    ld hl,$d16b
    ld bc,44
    call {ADDNTIMES:#x}
    push hl
    ld bc,33
    add hl,bc
    ld a,[hl]
    cp d
    pop hl
    ret nc                       ; no new level
    ld a,d
    ld [$d45a],a
    push hl
    ld bc,3
    add hl,bc
    ld [hl],d                    ; box level
    pop hl
    push hl
    ld bc,33
    add hl,bc
    ld [hl],d                    ; level
    ld a,d
    add 9
    ld [$d127],a                 ; stats as if 9 levels higher
    ld a,{BLK}
    ld [$d0b5],a
    call $155d                   ; GetMonHeader (base stats for CalcStats; keeps hl)
    pop hl
    push hl
    ld bc,35                     ; max HP low byte: remember the old max HP
    add hl,bc
    ld a,[hl-]
    ld c,a
    ld b,[hl]
    push bc
    ld d,h
    ld e,l                       ; de = stats (max HP)
    ld bc,$ffee
    add hl,bc                    ; hl = stat exp - 1
    ld b,1
    call {CALCSTATS:#x}
    pop bc                       ; old max HP
    pop hl                       ; struct
    push hl
    ld de,35
    add hl,de
    ld a,[hl-]
    sub c
    ld c,a
    ld a,[hl]
    sbc b
    ld b,a                       ; bc = max HP gain
    pop hl
    inc hl
    inc hl
    ld a,[hl]
    add c
    ld [hl-],a
    ld a,[hl]
    adc b
    ld [hl],a                    ; current HP += gain
    ld hl,t_grew
    jp {PRINTTEXT:#x}
{TXT}
'''
code,L=asm(SRC,CODE)
rom.put(fo(BANK,CODE),code,'Bank 2F: v41 CONSUME (victim, move, LearnMove, experience, level + 9 stats)')
labels['bank2f']={k:hex(v) for k,v in L.items() if not k.startswith('t_')}

# ---- bank 4: the field-move dispatch (v25 hook at 4:71C4) knows entry 10 = CONSUME
B4=0x7b20
assert not any(R[fo(4,B4):fo(4,B4)+0x30])
c4,L4=asm(f'''
fm41:                            ; hl = handler from the 9-entry table; entry 10 reads the bytes cb 57 (F:71DA)
    ld a,h
    cp $57
    jr nz,.old
    ld a,l
    cp $cb
    jr nz,.old
    ld hl,consume4
    ret
.old:
    jp $53c0                     ; v25: Dig/Teleport/Fly blocked in the chamber
consume4:
    farcall {L['consume']:#x},{BANK:#x}
    jp $70f5                     ; back to the party menu
''',B4)
rom.put(fo(4,B4),c4,'Bank 4: field-move dispatch: CONSUME')
rom.hook(fo(4,0x71c4),'cd'+le(L4['fm41']),'Party menu field move: CONSUME (entry 10)','cdc053',provides=('a','f','h','l'))
labels['bank4']={k:hex(v) for k,v in L4.items()}
rom.finish('Creepy_Black_Mu_v41.gb','manifest_v41.json','CREEPY MU V41',extra=dict(labels=labels))
