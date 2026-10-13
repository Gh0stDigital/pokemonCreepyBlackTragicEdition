# Creepy Black Mu v50: Black Tamer mechanics redux, part 4 (PRETA and AZHI).
#   1. PRETA makes the opposing POKeMON nervous (not GHOST types): its defense counts half -> PRETA's physical moves do
#      double damage. AZHI makes it anxious (not GHOST types): the opposing POKeMON's accuracy is halved against AZHI.
#      Either side (the MIRAGE's PRETA / AZHI too).
#   2. Revival: a fainted PRETA comes back 2 turns later, a fainted AZHI 3 turns later, each with half its HP
#      ("<name> rose from the dead!"). After every battle both are at full HP again.
#   3. Levels: the PRETA MR. MU awakens is Lv25 (was 50). At the end of the ritual a PRETA / AZHI already owned (party or
#      current box) below Lv50 is raised to Lv50; one that joins there is Lv50 as before.
#   4. Items have no effect on BLACK in battle either: X items (X ACCURACY too), GUARD SPEC and DIRE HIT with BLACK out -> "It won't have any
#      effect." (v38 already refused the party-menu items).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V49_SHA='aa20ca46756462e41f7d424ffdb6b3f26f34a5dded5257fd2a8d56e8887f6837'
rom=Rom('Creepy_Black_Mu_v49.gb',V49_SHA)
r=rom.r;R=bytes(r)
L38={k:int(v,16) for k,v in json.load(open('manifest_v38.json'))['labels']['bank2d'].items()}
PRINTTEXT,ADDNTIMES,CALCSTATS,GETHEADER,BANKSW=0x3c94,0x3abb,0x396a,0x155d,0x3618
PRETA,AZHI,BLK=0xb6,0xb7,0x7f
GHOSTTYPE=0x08
COUNT=0xd461                                 # v7's PRETA countdown: low nibble PRETA, high nibble AZHI now
labels={}
def tx(*parts,end=0x58):
    out=bytearray();inside=False
    for p in parts:
        if isinstance(p,tuple):
            if inside:out.append(0x50);inside=False
            out+=bytes([1,p[1]&255,p[1]>>8])
        else:
            if not inside:out.append(0);inside=True
            if p in ('line','cont','para'):out+={'line':b'\x4f','cont':b'\x55','para':b'\x51'}[p]
            else:assert shown(p)<=17,p;out+=enc(p)
    if not inside:out.append(0)
    out+=bytes([end]);return bytes(out)

BANK=0x2f;CODE=0x7b80
assert not any(R[fo(BANK,CODE):fo(BANK,0x8000)])
T={'t_rose':tx(('ram',0xcd6d),' rose','line','from the dead!')}
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())
code,L=asm(f'''
; ---- 1a. PRETA: after AdjustDamageForMoveType (F stub): physical move by PRETA vs a non-GHOST target -> damage x2
nerv50:
    ldh a,[$f3]
    and a
    jr nz,.enemy
    ld a,[$d014]
    cp {PRETA}
    ret nz
    ld a,[$cfd5]                 ; wPlayerMoveType
    ld hl,$cfea                  ; target types
    jr .chk
.enemy:
    ld a,[$cfe5]
    cp {PRETA}
    ret nz
    ld a,[$cfcf]                 ; wEnemyMoveType
    ld hl,$d019
.chk:
    cp $14
    ret nc                       ; special move: the defense stat isn't used
    ld a,[hl+]
    cp {GHOSTTYPE}
    ret z
    ld a,[hl]
    cp {GHOSTTYPE}
    ret z
    ld hl,$d0d7                  ; wDamage (big endian) x2, at most 999
    ld a,[hl+]
    ld l,[hl]
    ld h,a
    add hl,hl
    ld a,h
    cp $03
    jr c,.ok
    jr nz,.cap
    ld a,l
    cp $e8
    jr c,.ok
.cap:
    ld hl,999
.ok:ld a,h
    ld [$d0d7],a
    ld a,l
    ld [$d0d8],a
    ret

; ---- 1b. AZHI: after CalcHitChance (F stub): the attacker (not GHOST) aims at AZHI -> its move accuracy halved
anx50:
    ldh a,[$f3]
    and a
    jr nz,.enemy
    ld a,[$cfe5]                 ; the player attacks the enemy
    cp {AZHI}
    ret nz
    ld hl,$d019                  ; the attacker's (player's) types
    ld de,$cfd6                  ; wPlayerMoveAccuracy
    jr .chk
.enemy:
    ld a,[$d014]
    cp {AZHI}
    ret nz
    ld hl,$cfea
    ld de,$cfd0                  ; wEnemyMoveAccuracy
.chk:
    ld a,[hl+]
    cp {GHOSTTYPE}
    ret z
    ld a,[hl]
    cp {GHOSTTYPE}
    ret z
    ld a,[de]
    srl a
    ld [de],a
    ret

; ---- 2. revival, every turn (MainInBattleLoop, replaces v7's tick): fainted PRETA (2 turns) / AZHI (3 turns) -> half HP
tick50:
    ld c,0
.l: ld b,0
    ld hl,$d164
    add hl,bc
    ld a,[hl]
    cp $ff
    ret z
    ld de,$0f03                  ; PRETA: low nibble, start at 3 (two turns pass)
    cp {PRETA}
    jr z,.got
    ld de,$f004                  ; AZHI: high nibble, start at 4
    cp {AZHI}
    jr nz,.nx
.got:
    push bc
    push de
    ld a,c
    ld hl,$d16c
    ld bc,44
    call {ADDNTIMES:#x}
    ld a,[hl+]
    or [hl]
    pop de
    pop bc
    jr nz,.nx                    ; alive
    ld a,[{COUNT:#x}]
    and d
    bit 7,d
    jr z,.lo
    swap a
.lo:and a
    jr nz,.cnt
    ld a,e
.cnt:
    dec a
    push af
    bit 7,d
    jr z,.lo2
    swap a
.lo2:
    ld b,a
    ld a,d
    cpl
    ld e,a
    ld a,[{COUNT:#x}]
    and e
    or b
    ld [{COUNT:#x}],a
    pop af
    jr nz,.nx                    ; still waiting
    push bc
    call revive
    pop bc
.nx:inc c
    jr .l

revive:                          ; c = party slot: HP = max HP / 2 (at least 1), no status, the message
    push bc
    ld a,c
    ld hl,$d16b
    ld bc,44
    call {ADDNTIMES:#x}
    push hl
    ld bc,34
    add hl,bc
    ld a,[hl+]
    ld e,[hl]
    srl a
    rr e
    ld d,a
    or e
    jr nz,.h
    inc e
.h: pop hl
    push hl
    inc hl
    ld a,d
    ld [hl+],a
    ld [hl],e
    pop hl
    ld bc,4
    add hl,bc
    ld [hl],0
    pop bc
    ld a,c
    ld hl,$d2b5
    ld bc,11
    call {ADDNTIMES:#x}
    ld de,$cd6d
    ld bc,11
    call $00b5
    ld hl,t_rose
    jp {PRINTTEXT:#x}

; ---- 2b. after every battle (2D:5FC4, replaces v7's post): PRETA and AZHI at full HP, then v7's post (MIRAGE cleanup)
post50:                          ; (runs every step: 0:00C0 wraps the overworld's battle check; carry = a battle happened)
    jr nc,.done
    xor a
    ld [{COUNT:#x}],a
    ld c,0
.l: ld b,0
    ld hl,$d164
    add hl,bc
    ld a,[hl]
    cp $ff
    jr z,.done
    cp {PRETA}
    jr z,.h
    cp {AZHI}
    jr nz,.nx
.h: push bc
    ld a,c
    ld hl,$d16b
    ld bc,44
    call {ADDNTIMES:#x}
    push hl
    ld bc,34
    add hl,bc
    ld a,[hl+]
    ld d,a
    ld e,[hl]
    pop hl
    inc hl
    ld a,d
    ld [hl+],a
    ld [hl],e
    pop bc
.nx:inc c
    jr .l
.done:
    ld hl,$4760
    ld b,$2e
    jp {BANKSW:#x}

; ---- 3. end of the ritual (before v38 black_join): an owned PRETA / AZHI below Lv50 -> Lv50
boost50:
    ld c,0
.l: ld b,0
    ld hl,$d164
    add hl,bc
    ld a,[hl]
    cp $ff
    jr z,.box
    cp {PRETA}
    jr z,.p
    cp {AZHI}
    jr nz,.nx
.p: push bc
    ld [$d0b5],a
    ld a,c
    ld hl,$d16b
    ld bc,44
    call {ADDNTIMES:#x}
    push hl
    ld bc,33
    add hl,bc
    ld a,[hl]
    pop hl
    cp 50
    jr nc,.skip
    call lv50
.skip:
    pop bc
.nx:inc c
    jr .l
.box:
    ld a,[$da80]
    and a
    ret z
    ld c,0
.b: ld a,[$da80]
    cp c
    ret z
    ld b,0
    ld hl,$da81
    add hl,bc
    ld a,[hl]
    cp {PRETA}
    jr z,.bp
    cp {AZHI}
    jr nz,.bn
.bp:push bc
    ld [$d0b5],a
    ld a,c
    ld hl,$da96
    ld bc,33
    call {ADDNTIMES:#x}
    push hl
    inc hl
    inc hl
    inc hl
    ld a,[hl]
    cp 50
    jr nc,.bs
    ld [hl],50
    call exp50
    pop hl
    push hl
    ld bc,14
    add hl,bc
    ldh a,[$96]
    ld [hl+],a
    ldh a,[$97]
    ld [hl+],a
    ldh a,[$98]
    ld [hl],a
.bs:pop hl
    pop bc
.bn:inc c
    jr .b

exp50:                           ; wd0b5 = species: hExperience = its experience for Lv50
    call {GETHEADER:#x}
    ld d,50
    farcall $4f6a,$16
    ret
lv50:                            ; hl = party struct, wd0b5 = species: Lv50 (experience, levels, stats, full HP)
    push hl
    call exp50
    pop hl
    push hl
    ld bc,14
    add hl,bc
    ldh a,[$96]
    ld [hl+],a
    ldh a,[$97]
    ld [hl+],a
    ldh a,[$98]
    ld [hl],a
    pop hl
    push hl
    inc hl
    inc hl
    inc hl
    ld [hl],50
    pop hl
    push hl
    ld bc,33
    add hl,bc
    ld [hl],50
    ld a,50
    ld [$d127],a
    pop hl
    push hl
    ld a,[hl]
    ld [$d0b5],a
    call {GETHEADER:#x}
    pop hl
    push hl
    ld bc,34
    add hl,bc
    ld d,h
    ld e,l
    ld bc,$ffee
    add hl,bc
    ld b,1
    call {CALCSTATS:#x}
    pop hl
    push hl
    ld bc,34
    add hl,bc
    ld a,[hl+]
    ld b,a
    ld c,[hl]
    pop hl
    inc hl
    ld [hl],b
    inc hl
    ld [hl],c
    ret

; ---- 4. battle items on BLACK (X items, GUARD SPEC, DIRE HIT; rst 08 from their first bytes): no effect
xitem50:
    ld hl,sp+4
    ld a,[hl+]
    ld h,[hl]
    ld l,a
    ld de,xtab
.f: ld a,[de]
    inc de
    cp l
    ld a,[de]
    inc de
    jr nz,.n
    cp h
    jr z,.got
.n: inc de
    inc de
    inc de
    inc de
    jr .f
.got:
    ld h,d
    ld l,e
    ld a,[$d057]
    and a
    jr z,.set                    ; not in battle: "not the time" as before
    inc hl
    inc hl
    ld a,[$d014]
    cp {BLK}
    jr nz,.set                   ; another POKeMON out: the item works as before
    ld hl,noeff
.set:
    ld a,[hl+]
    ld h,[hl]
    ld l,a
    push hl
    ld hl,sp+6
    pop de
    ld [hl],e
    inc hl
    ld [hl],d
    ret
noeff: dw $68ad
xtab: dw $643b,$643b,$6444, $6413,$68b2,$6414, $642c,$68b2,$642d, $634a,$68b2,$634b
{TXT}''',CODE)
rom.put(fo(BANK,CODE),code,'Bank 2F: v50 PRETA / AZHI (nervous, anxious, revival, full HP after battle, Lv50 at the ritual)')
labels['bank2f']={k:hex(v) for k,v in L.items()}

# F stubs in v10's dead animation bytes (F:7F5E-7F79, unreachable since v48 replaced its entry)
FS=fo(0xf,0x7f5e)
old=R[FS:FS+20];assert old.hex()=='0978feaa3e5228023ea3c5cded6fc178fea9d021'
cf,LF=asm(f'''
adj50:
    call $647b
    ld hl,{L['nerv50']:#x}
    ld b,{BANK:#x}
    rst $08
    ret
hit50:
    call $66fa
    ld hl,{L['anx50']:#x}
    ld b,{BANK:#x}
    rst $08
    ret
''',0x7f5e)
assert len(cf)==20
rom.code(FS,cf,'Bank F: v50 stubs (AdjustDamageForMoveType / CalcHitChance, then 2F) in v10\'s dead animation code',old.hex(),
         reviewed='F:7F5E-7F79 is the tail of v10\'s animation routine, unreachable since v48 jumps away at its entry (its only jr target 7F68 was internal)')
for at in (0x57cd,0x685f):
    rom.hook(fo(0xf,at),'cd'+le(LF['adj50']),'AdjustDamageForMoveType -> + PRETA nervous (x2)','cd7b64',provides=('a','f','b','c','h','l'))
rom.hook(fo(0xf,0x66c8),'cd'+le(LF['hit50']),'CalcHitChance -> + AZHI anxious (accuracy / 2)','cdfa66',provides=('a','f','b','c','d','e','h','l'))

# revival: v7's turn stub (F:7E36 far call 2E:4700 tick) -> 2F tick50; after battle (2D:5FC4 far call 2E:4760) -> post50
assert R[fo(0xf,0x7e36):fo(0xf,0x7e3b)]==bytes.fromhex('210047062e')
rom.data(fo(0xf,0x7e37),bytes.fromhex(le(L['tick50']))+b'\x06'+bytes([BANK]),'Turn start: PRETA / AZHI revival (tick50)','0047062e')
assert R[fo(0x2d,0x5fc4):fo(0x2d,0x5fc9)]==bytes.fromhex('216047062e')
rom.data(fo(0x2d,0x5fc5),bytes.fromhex(le(L['post50']))+b'\x06'+bytes([BANK]),'After battle: PRETA / AZHI full HP (post50), then v7 post','6047062e')

# PRETA from MR. MU: v6's awaken struct (2E:469A) Lv50 -> Lv25 (KABUTOPS base stats, perfect DVs, slow growth)
PS=fo(0x2e,0x469a);s=bytearray(R[PS:PS+44])
BS=fo(0xe,0x43e4);hd=R[BS+28*140:BS+28*141];assert hd[0]==141
KD=fo(0xe,0x7ca4);assert list(R[KD:KD+5])==list(hd[1:6]) and R[KD+15]==5   # v3 kab_data = PRETA's header: KABUTOPS stats, SLOW growth
base=list(hd[1:6])
def calc(L):return [((base[0]+15)*2*L)//100+L+10]+[((b+15)*2*L)//100+5 for b in base[1:]]
assert [s[34+2*i]<<8|s[35+2*i] for i in range(5)]==calc(50) and s[3]==s[33]==50
st=calc(25);s[3]=s[33]=25;s[1:3]=st[0].to_bytes(2,'big');s[14:17]=(5*25**3//4).to_bytes(3,'big')     # PRETA's header (v3 kab_data) grows SLOW, like v6's Lv50 struct
for i,v in enumerate(st):s[34+2*i:36+2*i]=v.to_bytes(2,'big')
rom.data(PS,bytes(s),'PRETA from MR. MU: Lv25 (stats %s)'%st,R[PS:PS+44])
# the ritual: 2D:46B4 jp black_join -> 2D stub: boost50 first
S2D=0x7f80
assert not any(R[fo(0x2d,S2D):fo(0x2d,S2D)+0x10])
c2d,L2D=asm(f'''
ritual50:
    farcall {L['boost50']:#x},{BANK:#x}
    jp {L38['black_join']:#x}
''',S2D)
rom.put(fo(0x2d,S2D),c2d,'Bank 2D: v50 ritual end: owned PRETA / AZHI to Lv50, then black_join')
assert R[fo(0x2d,0x46b4):fo(0x2d,0x46b7)]==bytes.fromhex('c3'+le(L38['black_join']))
rom.code(fo(0x2d,0x46b4),bytes.fromhex('c3'+le(L2D['ritual50'])),'Ritual end -> ritual50 (Lv50 for owned PRETA / AZHI)','c3'+le(L38['black_join']))
# battle items: ItemUseXStat (3:6435 ld a,[wIsInBattle] / and a / jr nz), ItemUseGuardSpec (3:640D ... jp z,NotTime),
# ItemUseDireHit (3:6426), ItemUseXAccuracy (3:6344) -> ld hl,xitem50 / ld b,$2f / rst 08 (+ nop): xitem50 picks where to go on
for at,old in ((0x6435,'fa57d0a72009'),(0x640d,'fa57d0a7cab268'),(0x6426,'fa57d0a7cab268'),(0x6344,'fa57d0a7cab268')):
    new=bytes.fromhex('21'+le(L['xitem50'])+'062fcf');new+=bytes(len(bytes.fromhex(old))-len(new))
    rom.code(fo(3,at),new,'Battle item on BLACK: no effect (3:%04X)'%at,old)
labels['bankF']={k:hex(v) for k,v in LF.items()};labels['bank2d']={k:hex(v) for k,v in L2D.items()}
rom.finish('Creepy_Black_Mu_v50.gb','manifest_v50.json','CREEPY MU V50',extra=dict(labels=labels))
