# Creepy Black Mu v44: the POKeMON LEAGUE as BLACK (part 1: LORELEI, BRUNO, LANCE; AGATHA's room is empty; BLUE later).
#   As BLACK (D46C), in the battles against LORELEI (class 2C), BRUNO (21) and LANCE (2F):
#   - the "forbidden" moves (CURSE A5, MACABREBLADE A7, BLACK FLAME A8, MACABRE A9, BANE AA) can't be chosen: a light
#     flashes, "A strange power blocks the move <MOVE>!", then the trainer comments on the MOON STONE in their own way;
#     the move menu comes back (no turn lost). Their POKeMON must be beaten by conventional means.
#   - when their last POKeMON is down: another flash, "The MOON STONE shatters!", the POKeMON out is called back and
#     BLACK is sent out, then the usual after-win phase (BANE on the trainer). There BANE is the only choice: any other
#     move, ITEM or RUN -> "AGATHA's words echo within you: 'You must destroy them all!' 'Destroy all the intruders!'".
#   - AGATHA's room is empty: she is hidden and her "beaten" flag (D865 bit 1) is set, so the way to LANCE is open.
#   Everything else (other trainers, not BLACK) is unchanged.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V43_SHA='ffc97a4d7a823e6f5e46936f4c323f027c7b6695de2108fb308cd62d038e0cee'
rom=Rom('Creepy_Black_Mu_v43.gb',V43_SHA)
r=rom.r;R=bytes(r)
BLK,BANE=0x7f,0xaa
LORELEI,BRUNO,LANCE=0x2c,0x21,0x2f
FORBID=[0xa5,0xa7,0xa8,0xa9,0xaa]
PRINTTEXT,DELAY,MOVENAME=0x3c94,0x3773,0x3089
SWITCHMON=0x5279                       # F: SwitchPlayerMon (retreat, Go!, LoadBattleMonFromParty, SendOutMon)
assert R[fo(0xf,SWITCHMON):fo(0xf,SWITCHMON)+3]==bytes.fromhex('21d14e')
NAME=0xcd6d
FLAG=0xd459                            # temp (D457-D45A): menu choice refused

def ram_text(*parts):
    out=bytearray();inside=False
    for p in parts:
        if isinstance(p,tuple) and p[0]=='ram':
            if inside:out.append(0x50);inside=False
            out+=bytes([1,p[1]&255,p[1]>>8])
        else:
            if not inside:out.append(0);inside=True
            if p in ('line','cont','para'):out+={'line':b'\x4f','cont':b'\x55','para':b'\x51'}[p]
            else:
                assert shown(p)<=17,p;out+=enc(p)
    if not inside:out.append(0)
    out+=b'\x58';return bytes(out)
T={
 't_block':ram_text('A strange power','line','blocks the move','cont',('ram',NAME),'!'),
 't_lor':ram_text('LORELEI: Hmph.','line','So the MOON STONE','cont','does resist you.','para','Your darkness','line','freezes here!'),
 't_bru':ram_text('BRUNO: Hah!','line',"The MOON STONE's",'cont','power holds you!','para','No tricks! Face','line','my raw strength!'),
 't_lan':ram_text('LANCE: I see...','line',"The MOON STONE's",'cont','light resists','cont','your darkness.','para','Face my dragons','line','like a trainer!'),
 't_shatter':ram_text('The MOON STONE','line','shatters!'),
 't_agatha':ram_text("AGATHA's words",'line','echo within you:','para',"'You must destroy",'line',"them all!'",'para',"'Destroy all the",'line',"intruders!'"),
}
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())

BANK=0x2f;CODE=0x6400
assert not any(R[fo(BANK,CODE):fo(BANK,CODE+0x400)])
code,L=asm(f'''
; ---- F:545D (MoveSelectionMenu: the chosen move is stored) -> home 0x39 -> here.
;      Entry stack: [sp] Bankswitch, [sp+2] old bank, [sp+4] = F:5460 (xor a / ret). Blocked: [sp+4] = F:546D
;      (LoadScreenTilesFromBuffer1 + MoveSelectionMenu again, like "no PP left").
sel44:
    ld a,[$cc26]
    ld c,a
    ld b,0
    ld hl,$d01c
    add hl,bc
    ld a,[hl]
    ld [$ccdc],a
    call e4chk
    ret nz
    ld a,[$d05a]
    cp 3
    jr z,.phase
    ld a,[$ccdc]
    ld hl,forbid
.f: ld b,[hl]
    inc hl
    inc b
    ret z
    dec b
    cp b
    jr nz,.f
    ld [$d11e],a
    call {MOVENAME:#x}
    call flash
    ld hl,t_block
    call {PRINTTEXT:#x}
    call tline
    call {PRINTTEXT:#x}
    jr .back
.phase:
    ld a,[$ccdc]
    cp {BANE}
    ret z
    ld hl,t_agatha
    call {PRINTTEXT:#x}
.back:
    ld hl,sp+4
    ld a,$6d
    ld [hl+],a
    ld [hl],$54
    ret

; z = an Elite Four battle (LORELEI / BRUNO / LANCE) and the player is BLACK
e4chk:
    ld a,[$d46c]
    and a
    jr z,.no
    ld a,[$d057]
    cp 2
    jr nz,.no
    ld a,[$d031]
    cp {LORELEI}
    ret z
    cp {BRUNO}
    ret z
    cp {LANCE}
    ret z
.no:or 1
    ret

tline:
    ld a,[$d031]
    ld hl,t_lor
    cp {LORELEI}
    ret z
    ld hl,t_bru
    cp {BRUNO}
    ret z
    ld hl,t_lan
    ret

; a light flashes: everything white for a moment, twice
flash:
    ldh a,[$47]
    ld d,a
    ldh a,[$48]
    ld e,a
    ldh a,[$49]
    ld b,a
    push bc
    push de
    call .white
    ld c,4
    call {DELAY:#x}
    pop de
    pop bc
    push bc
    push de
    call .back
    ld c,4
    call {DELAY:#x}
    call .white
    ld c,10
    call {DELAY:#x}
    pop de
    pop bc
.back:
    ld a,d
    ldh [$47],a
    ld a,e
    ldh [$48],a
    ld a,b
    ldh [$49],a
    ret
.white:
    xor a
    ldh [$47],a
    ldh [$48],a
    ldh [$49],a
    ret

; ---- F:7DCC (after-win phase check, before phase2) -> here, then phase2 (2D:6100) as before.
;      Elite Four as BLACK: flash, "The MOON STONE shatters!", BLACK is sent out (so the phase starts with BANE).
ph44:
    call e4chk
    jr nz,.go
    call flash
    ld hl,t_shatter
    call {PRINTTEXT:#x}
    ld a,[$d014]
    cp {BLK}
    jr z,.go
    ld hl,$d164
    ld c,0
.l: ld a,[hl+]
    cp $ff
    jr z,.go
    cp {BLK}
    jr z,.sw
    inc c
    jr .l
.sw:ld a,c
    ld [$cf92],a
    ld a,{BLK}                   ; like the PKMN menu: wBattleMonSpecies2 / wcf91 = the new one (back picture)
    ld [$cfd9],a
    ld [$cf91],a
    farcall {SWITCHMON:#x},$0f
.go:
    ld hl,$6100
    ld b,$2d
    jp $3618

; ---- battle menu (F:7E16 -> 2E tramp44 -> here): in the phase only FIGHT is allowed. FLAG = 1: refused
menu44:
    xor a
    ld [{FLAG:#x}],a
    call e4chk
    ret nz
    ld a,[$d05a]
    cp 3
    ret nz
    ld a,[$d468]
    and a
    ret z
    ld hl,t_agatha
    call {PRINTTEXT:#x}
    ld a,1
    ld [{FLAG:#x}],a
    ret

forbid: db {','.join(str(x) for x in FORBID)},255
{TXT}''',CODE)
rom.put(fo(BANK,CODE),code,'Bank 2F: v44 Elite Four as BLACK (MOON STONE blocks, shatter, BANE only)')
labels={'bank2f':{k:hex(v) for k,v in L.items()}}

# home 0x39: far stub to sel44 (21 lo hi 06 2f, jr 0x09 = jp Bankswitch)
assert R[0x39:0x40]==bytes(7) and R[0x09:0x0c]==bytes.fromhex('c31836')
rom.put(0x39,bytes.fromhex('21'+le(L['sel44'])+'062f18c9'),'Home 0x39: far stub -> 2F sel44 (v44)')
# F:545D: ld [wPlayerSelectedMove],a / xor a / ret -> call 0039 / xor a / ret
rom.code(fo(0xf,0x545d),bytes.fromhex('cd3900afc9'),'MoveSelectionMenu: chosen move -> sel44 (Elite Four blocks)','eadcccafc9')
# F:7DCC: ld hl,phase2 / ld b,2D -> ph44 in 2F (which calls phase2 itself)
rom.code(fo(0xf,0x7dcc),bytes.fromhex('21'+le(L['ph44'])+'062f'),'After-win phase check -> ph44 (MOON STONE shatters, BLACK out)','210061062d',
         reviewed='0:03AA is the middle of ld [$cd6b],a (misaligned decode), not a jump into F:7DCD')

# 2E: trampoline in front of v23's menu check (2E:59DB): refused -> back to the battle menu (F:4EDE)
T2E=0x7800
assert not any(R[fo(0x2e,T2E):fo(0x2e,T2E+0x20)])
c2e,L2E=asm(f'''
tramp44:
    ld hl,{L['menu44']:#x}
    ld b,$2f
    call $3618
    ld a,[{FLAG:#x}]
    and a
    jp z,$59db
    ld de,$4ede
    jp $59c8
''',T2E)
rom.put(fo(0x2e,T2E),c2e,'Bank 2E: v44 battle-menu trampoline (Elite Four phase: FIGHT only)')
rom.code(fo(0xf,0x7e19),bytes.fromhex('21'+le(L2E['tramp44'])),'Battle menu hook -> tramp44 (then v23 check)','21db59')
labels['bank2e']={k:hex(v) for k,v in L2E.items()}

# 1D: AGATHA's room as BLACK: she is gone, her room counts as beaten (the exit to LANCE opens)
T1D=0x7e00
assert not any(R[fo(0x1d,T1D):fo(0x1d,T1D+0x20)])
c1d,L1D=asm(f'''
ag44:
    ld a,[$d46c]
    and a
    jp z,$6443
    ld hl,$d865
    set 1,[hl]
    xor a
    ld [$c110],a
    ld a,$ff
    ld [$c214],a
    ld [$c215],a
    jp $6443
''',T1D)
rom.put(fo(0x1d,T1D),c1d,"Bank 1D: v44 AGATHA's room as BLACK (empty, way open)")
rom.code(fo(0x1d,0x642d),'cd'+le(L1D['ag44']),"AGATHA's room script -> ag44",'cd4364')
labels['bank1d']={k:hex(v) for k,v in L1D.items()}
rom.finish('Creepy_Black_Mu_v44.gb','manifest_v44.json','CREEPY MU V44',extra=dict(labels=labels))
