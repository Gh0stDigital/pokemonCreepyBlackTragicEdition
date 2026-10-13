# Creepy Black Mu v51: POKeMON TOWER rules and the ritual battle's look.
#   1. GHOST won't fight in POKeMON TOWER (1F-7F): a GHOST leading the party stays in its ball and the next POKeMON that can
#      fight goes out; choosing GHOST to switch in (or after a faint) says "<GHOST> refuses your command!". If GHOST is the
#      only one left able to fight it comes out but refuses every command (the turn passes).
#   2. As BLACK every town and route plays the LAVENDER TOWN music (buildings, caves, gyms ... keep theirs).
#   3. MR. MU's battle: no battle music, and MR. MU stays in the picture: no slide away, no send-out animation or cry
#      (his "stepped forward" line stays) - his HUD appears and the battle starts (the MIRAGE that comes after him is sent out as before).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V50_SHA='ac2cd92d4056e79c21935500c9a3fe8b1b1f5ebb55cc04b78885b4a1ee6f2f75'
rom=Rom('Creepy_Black_Mu_v50.gb',V50_SHA)
r=rom.r;R=bytes(r)
L39={k:int(v,16) for k,v in json.load(open('manifest_v39.json'))['labels']['bank2f'].items()}
PRINTTEXT,ADDNTIMES,BANKSW,COPYDATA=0x3c94,0x3abb,0x3618,0x00b5
GHOST,BLACKF=0x1f,0xd46c
MU_OPP=0xc8+27
LAVENDER=4
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

SONGS=R[fo(3,0x404d):fo(3,0x404d)+2*0xf8]
assert SONGS[2*LAVENDER:2*LAVENDER+2]==R[fo(3,0x404d)+8:fo(3,0x404d)+10]
NOWILL=R[fo(0xf,0x4adf):fo(0xf,0x4adf)+5];assert NOWILL[0]==0x17 and NOWILL[4]==0x50
BANK=0x30;CODE=0x4000                        # bank 2F is nearly full: v51+ code goes to bank 30 (empty)
assert not any(R[fo(BANK,CODE):fo(BANK,0x8000)])
T={'t_refuse':tx(('ram',0xcd6d),' refuses','line','your command!')}
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())
code,L=asm(f'''
; ---- 1. HasMonFainted (F:4AC2 via rst 08): z = can't be sent out (fainted, or GHOST in the TOWER while another can fight)
ghost51:
    ld a,[$cf92]
    ld hl,$d16c
    ld bc,44
    call {ADDNTIMES:#x}
    ld a,[hl+]
    or [hl]
    jr z,.fainted
    call tower
    jr nz,.ok
    ld a,[$cf92]
    ld c,a
    ld b,0
    ld hl,$d164
    add hl,bc
    ld a,[hl]
    cp {GHOST}
    jr nz,.ok
    call other                   ; another POKeMON able to fight?
    jr z,.ok                     ; no: GHOST has to come out
    ld a,[$d11d]
    and a
    jr nz,.no                    ; battle start: silently the next one
    ld a,[$cf92]
    call nick
    ld hl,t_refuse
    call {PRINTTEXT:#x}
.no:xor a
    ret
.ok:or 1
    ret
.fainted:
    ld a,[$d11d]
    and a
    jr nz,.no
    ld hl,t_nowill
    call {PRINTTEXT:#x}
    xor a
    ret
t_nowill: db {','.join(str(x) for x in NOWILL)}

tower:                           ; z = POKeMON TOWER 1F-7F
    ld a,[$d35e]
    cp $8e
    jr c,.n
    cp $95
    jr nc,.n
    xor a
    ret
.n: or 1
    ret
other:                           ; nz = a party POKeMON other than GHOST with HP left
    ld hl,$d164
    ld de,$d16c
.l: ld a,[hl+]
    cp $ff
    ret z
    cp {GHOST}
    jr z,.n
    ld a,[de]
    ld b,a
    inc de
    ld a,[de]
    dec de
    or b
    ret nz
.n: push hl
    ld hl,44
    add hl,de
    ld d,h
    ld e,l
    pop hl
    jr .l
nick:                            ; a = party slot: nickname -> wcd6d
    ld hl,$d2b5
    ld bc,11
    call {ADDNTIMES:#x}
    ld de,$cd6d
    ld bc,11
    jp {COPYDATA:#x}

; before the player's move (home 0x29, was v48 pre48): GHOST out in the TOWER refuses (the turn ends), else pre48
pre51:
    ld a,[$d014]
    cp {GHOST}
    jr nz,.go
    call tower
    jr nz,.go
    ld hl,$d009                  ; wBattleMonNick
    ld de,$cd6d
    ld bc,11
    call {COPYDATA:#x}
    ld hl,t_refuse
    call {PRINTTEXT:#x}
    ld hl,sp+6                   ; back at F:58DB (ExecutePlayerMoveDone) instead of the move
    ld a,$db
    ld [hl+],a
    ld [hl],$58
    ret
.go:ld a,$2f                     ; v48 pre48 in bank 2F, same stack (home 0x31 trampoline)
    ld hl,{int(json.load(open('manifest_v48.json'))['labels']['bank2f']['pre48'],16):#x}
    jp $0031

; ---- 2. map music (0:1249 via rst 08, replaces the read of MapSongBanks): BLACK on a town / route -> LAVENDER TOWN
music51:
    ld a,[$d35e]
    ld c,a
    cp $25
    jr nc,.own
    ld a,[{BLACKF:#x}]
    and a
    jr z,.own
    ld c,{LAVENDER}
.own:
    ld b,0
    ld hl,songs
    add hl,bc
    add hl,bc
    ld a,[hl+]
    ld [$d35b],a
    ld a,[hl]
    ld [$d35c],a
    ret

; ---- 3. MR. MU's first send-out
mu51:                            ; z = MR. MU's battle, his first send-out
    ld a,[$d059]
    cp {MU_OPP}
    ret nz
    ld a,[$d11d]
    and a
    jr z,.n
    xor a
    ret
.n: or 1
    ret
slide51:                         ; F:496C (via rst 08): the code it replaced, then MR. MU: skip the slide (back at F:497D)
    ld a,$ff
    ld [$ccdf],a
    ld hl,$d062
    res 5,[hl]
    call mu51
    ret nz
    ld hl,sp+4
    ld a,$7d
    ld [hl+],a
    ld [hl],$49
    ret
anim51:                          ; F:4A6B (via rst 08): the replaced loads; MR. MU: no picture, animation, cry (to his HUD, F:4A8F)
    ld a,[$cfd8]
    ld [$cf91],a
    ld [$d0b5],a
    call mu51
    ret nz
    ld hl,sp+4
    ld a,$8f
    ld [hl+],a
    ld [hl],$4a
    ret
songs: db {','.join(str(x) for x in SONGS)}
{TXT}''',CODE)
rom.put(fo(BANK,CODE),code,'Bank 30: v51 GHOST in the TOWER, LAVENDER music as BLACK, MR. MU\'s quiet battle')
labels['bank30']={k:hex(v) for k,v in L.items() if k!='songs'}
def rst(lab):return bytes.fromhex('21'+le(L[lab])+'06%02xcf'%BANK)

# 1. HasMonFainted (F:4AC2 ld a,[wWhichPokemon] / ld hl,wPartyMon1HP / ld bc..) -> rst 08 ghost51 / ret
old=R[fo(0xf,0x4ac2):fo(0xf,0x4ac9)];assert old.hex()=='fa92cf216cd101'
rom.code(fo(0xf,0x4ac2),rst('ghost51')+b'\xc9','HasMonFainted: GHOST won\'t fight in the TOWER',old.hex())
H29=R[0x29:0x30];assert H29[1:3]==bytes.fromhex(le(int(json.load(open('manifest_v48.json'))['labels']['bank2f']['pre48'],16)))
rom.data(0x2a,bytes.fromhex(le(L['pre51']))+bytes([0x06,BANK]),'Home 0x29 stub -> 30:pre51 (GHOST refuses in the TOWER), then pre48',H29[1:5].hex())
# 2. map music
old=R[0x1249:0x1266];assert old.hex()=='f0b8f53e03e0b8ea0020214d400909 2aea5bd37eea5cd3f1e0b8ea0020'.replace(' ','')
new=rst('music51')+bytes([0x18,0x1266-(0x1249+8)])
rom.code(0x1249,new+bytes(len(old)-len(new)),'Map music: LAVENDER TOWN on towns / routes as BLACK (30 music51)',old.hex(),
         reviewed='0x1265 is the operand of ld [$2000],a read as jr nz; 6:4E77, A:440A, D:457B are pointer tables / data bytes, not code')
# 3. MR. MU: music (2:50E3 ld a,[wCurOpponent] -> 2:7FF4), slide (F:496C), send-out (F:4A51)
assert not any(R[fo(2,0x7ff4):fo(2,0x8000)])
c2,L2=asm(f'''
mus51:
    ld a,[$d059]
    cp {MU_OPP}
    ret nz
    pop af                       ; MR. MU: leave PlayBattleMusic, the music stays stopped
    ret
''',0x7ff4)
rom.put(fo(2,0x7ff4),c2,'Bank 2: v51 no battle music for MR. MU')
rom.hook(fo(2,0x50e3),'cd'+le(L2['mus51']),'PlayBattleMusic: MR. MU -> none','fa59d0',provides=('a','f'))
old=R[fo(0xf,0x496c):fo(0xf,0x4975)];assert old.hex()=='3deadfcc2162d0cbae'
rom.code(fo(0xf,0x496c),rst('slide51')+bytes(3),'EnemySendOutFirstMon: MR. MU stays in the picture (no slide)',old.hex())
old=R[fo(0xf,0x4a6b):fo(0xf,0x4a74)];assert old.hex()=='fad8cfea91cfeab5d0'
rom.code(fo(0xf,0x4a6b),rst('anim51')+bytes(3),'EnemySendOutFirstMon: MR. MU: no picture swap, animation or cry',old.hex())
rom.finish('Creepy_Black_Mu_v51.gb','manifest_v51.json','CREEPY MU V51',extra=dict(labels=labels))
