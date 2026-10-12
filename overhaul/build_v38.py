# Creepy Black Mu v38: the BLACK TAMER becomes a party member (part 1 of the BLACK TAMER mechanics).
#   1. Evolution scene: the evolution animation starts from RED's trainer picture (new hidden species 86 = RED's front
#      picture, bank 4) and ends on the BLACK TAMER picture (species 7F).
#   2. Trainer card: the BLACK TAMER picture (2D:41C0) instead of RED once the player is BLACK.
#   3. End of the ritual: BLACK (species 7F, Lv1, perfect DVs, stats computed as if level 10 = "level + 9") joins the
#      party in slot 1; PRETA and AZHI are given too unless already owned (party or current box); party full -> box.
#   4. BLACK can't faint (HP stays at 1: the five "player mon fainted?" checks in bank F), gains no battle experience
#      (GainExperience skips it), can't be deposited (PC) or left at the Day Care, no item works on it (POTION, stones,
#      TMs, PP items, vitamins, RARE CANDY: "It won't have any effect."), the Name Rater won't rename it, and poison
#      outside battle can't kill it (status cleared at 4 HP or less).
#   New home far stubs live in the unused bytes after the RST vectors (0x01-0x3F): no code ever executes RST 00-38.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V37_SHA='c7593900fa2c1b0bfd26d930700ff3db403c59096eb2e31346cb73495c102fc5'
rom=Rom('Creepy_Black_Mu_v37.gb',V37_SHA)
r=rom.r;R=bytes(r)
def w(o):return R[o]|R[o+1]<<8
L25={k:int(v,16) for k,v in json.load(open('manifest_v25.json'))['labels']['bank2d'].items()}
PRINTTEXT,COPYDATA,ADDNTIMES,PARTYMENU,BANKSWITCH=0x3c94,0x00b5,0x3abb,0x142b,0x3618
BLK,REDSP,PRETA,AZHI,GHOST=0x7f,0x86,0xb6,0xb7,0x1f
BLACKF,RIT=0xd46c,0xd467
CURSE=0xa5
labels={}
def pp(mv):return R[fo(0xe,0x4000+(mv-1)*6)+5] if mv else 0

# ---------------------------------------------------------------------------------------------------------------
# party structs (44 bytes) built here: BLACK Lv1 (stats as level 10), AZHI Lv50; PRETA copied from v6's awaken struct
def struct(species,level,types,catch,moves,exp,stats):
    s=bytes([species])+stats[0].to_bytes(2,'big')+bytes([level,0]+types+[catch]+moves)+b'\0\0'+exp.to_bytes(3,'big')+bytes(10)+b'\xff\xff'
    s+=bytes([pp(m) for m in moves])+bytes([level])+b''.join(x.to_bytes(2,'big') for x in stats)
    assert len(s)==44;return s
def calc(base,L):
    return [((base[0]+15)*2*L)//100+L+10]+[((b+15)*2*L)//100+5 for b in base[1:]]
BLACK_BASE=[100,110,100,110,160]                                # v25 header of species 7F
EFF=10                                                          # BLACK is level 1 but as strong as level 10
black=struct(BLK,1,[8,8],3,[CURSE,0,0,0],1,calc(BLACK_BASE,EFF))
L3=json.load(open('manifest_v3.json'))['labels']['bankE'];AD=fo(0xe,int(L3['aero_data'],16))
azb=list(R[AD:AD+5]);azt=list(R[AD+5:AD+7]);azm=list(R[AD+11:AD+15]);assert azm==[0xa8,0x13,0x52,0x7e] and R[AD+15]==5
azhi=struct(AZHI,50,azt,45,azm,5*50**3//4,calc(azb,50))
PS=fo(0x2e,0x469a);preta=bytes(R[PS:PS+44]);assert preta[0]==PRETA and preta[33]==50 and preta[8:12]==bytes([0xa9,0x0f,0x39,0x46])
print('BLACK stats',calc(BLACK_BASE,EFF),'AZHI stats',calc(azb,50))

# ---------------------------------------------------------------------------------------------------------------
# texts (bank 2D)
TXT={
 'noeffect':[["It won't have any","effect."]],
 'nobox':[["BLACK can't be","stored away."]],
 'daycare':[["BLACK won't leave","your side."]],
}
T38=0x7f00;tx=bytearray();TS={}
for k,v in TXT.items():TS['t_'+k]=T38+len(tx);tx+=txt(v,end=0x58)
assert not any(R[fo(0x2d,T38):fo(0x2d,T38)+len(tx)])
rom.put(fo(0x2d,T38),bytes(tx),'Bank 2D: v38 texts')

# ---------------------------------------------------------------------------------------------------------------
# bank 2D code
C38=0x7b00
assert not any(R[fo(0x2d,C38):fo(0x2d,T38)])
ext={**TS}
code,L=asm(f'''
; ---- UncompressMonSprite's bank choice: species 86 (RED's trainer picture) lives in bank 4
bank_for38:
    ld a,[$cf91]
    cp {REDSP}
    jp nz,{L25['bank_for']}
    ld a,4
    ld [$d470],a
    ret

; ---- far stub targets (home RST-gap stubs): every one returns through Bankswitch, which keeps hl and the flags
alive_chk:                       ; "player mon fainted?" (bank F): BLACK keeps 1 HP
    ld a,[$d014]
    cp {BLK}
    jr nz,.c
    ld hl,$d015
    ld a,[hl+]
    or [hl]
    jr nz,.c
    ld [hl],1
.c: ld hl,$d015
    ld a,[hl+]
    or [hl]
    ret

item_party:                      ; party menu of an item (bank 3): BLACK -> "It won't have any effect." + cancel
    call {PARTYMENU:#x}
    ret c
    ld a,[$cf91]
    cp {BLK}
    jr z,.no
    and a
    ret
.no:
    ld hl,t_noeffect
    call {PRINTTEXT:#x}
    scf
    ret

name_ot:                         ; Name Rater (bank 7): BLACK counts as "not your #MON" (no rename)
    ld a,[$cf91]
    cp {BLK}
    jr z,.no
    farcall $5a30,7
    ret
.no:
    scf
    ret

deposit:                         ; PC deposit (bank 8): BLACK can't be stored
    ld a,[$cf91]
    cp {BLK}
    jr z,.no
    jp $1408                     ; the replaced "ld a,[wcf91] / call PlayCry"
.no:
    ld hl,t_nobox
    call {PRINTTEXT:#x}
    ld hl,sp+4                   ; back to the PC menu (8:54E8)
    ld a,$e8
    ld [hl+],a
    ld a,$54
    ld [hl],a
    ret

; ---- end of the ritual (replaces do_post's "ld a,6 / ld [RIT],a / ret"): BLACK joins, PRETA and AZHI too
black_join:
    ld a,6
    ld [{RIT}],a
    ld hl,s_black
    ld de,n_black
    call add_mon
    call to_front
    ld b,{PRETA}
    call has_species
    jr nz,.a
    ld hl,s_preta
    ld de,n_preta
    call add_mon
.a: ld b,{AZHI}
    call has_species
    ret nz
    ld hl,s_azhi
    ld de,n_azhi
    jp add_mon

has_species:                     ; b = species: nz if it is in the party or the current box
    ld hl,$d164
.p: ld a,[hl+]
    cp $ff
    jr z,.box
    cp b
    jr nz,.p
    jr .yes
.box:
    ld a,[$da80]
    and a
    ret z
    ld c,a
    ld hl,$da81
.q: ld a,[hl+]
    cp b
    jr z,.yes
    dec c
    jr nz,.q
    xor a
    ret
.yes:
    or 1
    ret

add_mon:                         ; hl = 44-byte struct, de = nickname: party, else current box (if room)
    ld a,l
    ld [$d457],a
    ld a,h
    ld [$d458],a
    ld a,e
    ld [$d459],a
    ld a,d
    ld [$d45a],a
    ld a,[$d163]
    cp 6
    jr nc,.box
    ld c,a
    inc a
    ld [$d163],a
    ld b,0
    ld hl,$d164
    add hl,bc
    ld a,[$d457]
    ld e,a
    ld a,[$d458]
    ld d,a
    ld a,[de]
    ld [hl+],a
    ld [hl],$ff
    ld a,c
    push af
    ld hl,$d16b
    ld bc,44
    call {ADDNTIMES:#x}
    ld d,h
    ld e,l
    push de
    call src_struct
    ld bc,44
    call {COPYDATA:#x}
    pop hl
    call set_otid
    pop af
    push af
    ld hl,$d273
    call put_ot
    pop af
    ld hl,$d2b5
    jp put_nick
.box:
    ld a,[$da80]
    cp 20
    ret nc
    ld c,a
    inc a
    ld [$da80],a
    ld b,0
    ld hl,$da81
    add hl,bc
    ld a,[$d457]
    ld e,a
    ld a,[$d458]
    ld d,a
    ld a,[de]
    ld [hl+],a
    ld [hl],$ff
    ld a,c
    push af
    ld hl,$da96
    ld bc,33
    call {ADDNTIMES:#x}
    ld d,h
    ld e,l
    push de
    call src_struct
    ld bc,33
    call {COPYDATA:#x}
    pop hl
    call set_otid
    pop af
    push af
    ld hl,$dd2a
    call put_ot
    pop af
    ld hl,$de06
put_nick:                        ; a = index, hl = nickname table
    ld bc,11
    call {ADDNTIMES:#x}
    ld d,h
    ld e,l
    ld a,[$d459]
    ld l,a
    ld a,[$d45a]
    ld h,a
    ld bc,11
    jp {COPYDATA:#x}
put_ot:                          ; a = index, hl = OT name table: the player's name
    ld bc,11
    call {ADDNTIMES:#x}
    ld d,h
    ld e,l
    ld hl,$d158
    ld bc,11
    jp {COPYDATA:#x}
src_struct:
    ld a,[$d457]
    ld l,a
    ld a,[$d458]
    ld h,a
    ret
set_otid:                        ; hl = struct: OT ID = the player's
    ld bc,12
    add hl,bc
    ld a,[$d359]
    ld [hl+],a
    ld a,[$d35a]
    ld [hl],a
    ret

to_front:                        ; move the last party member to slot 1 (swap down step by step)
    ld a,[$d163]
    dec a
.l: and a
    ret z
    push af
    ld hl,$d164
    ld bc,1
    call swap
    pop af
    push af
    ld hl,$d16b
    ld bc,44
    call swap
    pop af
    push af
    ld hl,$d273
    ld bc,11
    call swap
    pop af
    push af
    ld hl,$d2b5
    ld bc,11
    call swap
    pop af
    dec a
    jr .l
swap:                            ; a = i: swap entries i-1 and i of the table at hl (entry size bc)
    push bc
    dec a
    call {ADDNTIMES:#x}
    pop bc
    ld d,h
    ld e,l
    push hl
    ld h,d
    ld l,e
    add hl,bc
    ld d,h
    ld e,l
    pop hl
.s: ld a,[de]
    ld b,a
    ld a,[hl]
    ld [de],a
    ld a,b
    ld [hl+],a
    inc de
    dec c
    jr nz,.s
    ret

; ---- every step (hunger_wrap's BLACK branch): poison outside battle can't kill BLACK
black_step:
    ld a,[{BLACKF}]
    and a
    ret z                        ; not BLACK: hunger_wrap goes on to the hunger engine
    pop hl                       ; BLACK: return from hunger_wrap itself
    ld a,[$d163]
    and a
    ret z
    ld c,a
    ld hl,$d164
    ld de,$d16b
.f: ld a,[hl+]
    cp {BLK}
    jr z,.got
    push hl
    ld hl,44
    add hl,de
    ld d,h
    ld e,l
    pop hl
    dec c
    jr nz,.f
    ret
.got:
    ld h,d
    ld l,e
    inc hl
    ld a,[hl+]
    and a
    ret nz
    ld a,[hl]
    cp 5
    ret nc
    inc hl
    inc hl
    ld [hl],0                    ; status (byte 4) cleared
    ret

s_black: db {','.join(str(x) for x in black)}
s_preta: db {','.join(str(x) for x in preta)}
s_azhi: db {','.join(str(x) for x in azhi)}
n_black: db {','.join(str(x) for x in enc('BLACK').ljust(11,b'P'))}
n_preta: db {','.join(str(x) for x in enc('PRETA').ljust(11,b'P'))}
n_azhi: db {','.join(str(x) for x in enc('AZHI').ljust(11,b'P'))}
''',C38,ext)
assert C38+len(code)<=T38,hex(C38+len(code))
rom.put(fo(0x2d,C38),code,'Bank 2D: v38 BLACK party member (join, checks, far stub targets)')
labels['bank2d']={k:hex(v) for k,v in L.items()}

# ---------------------------------------------------------------------------------------------------------------
# home: far stubs in the gaps after the RST vectors (each RST byte itself stays; nothing executes RST 00-38)
assert all(R[a]==0 for g in (0x01,0x09,0x11,0x19,0x21) for a in range(g,g+7))
rom.put(0x09,bytes.fromhex('c3'+le(BANKSWITCH)),'Home 0x09: shared "jp Bankswitch" for the v38 far stubs')
STUBS={}
for at,name in ((0x01,'alive_chk'),(0x11,'item_party'),(0x19,'name_ot'),(0x21,'deposit')):
    jr=(0x09-(at+7))&0xff
    rom.put(at,bytes.fromhex('21'+le(L[name])+'062d18%02x'%jr),'Home 0x%02X: far stub -> 2D %s'%(at,name));STUBS[name]=at
labels['home']={k:hex(v) for k,v in STUBS.items()}

# ---------------------------------------------------------------------------------------------------------------
# 1. evolution scene: species 86 = RED's trainer picture
rom.data(0x165a,bytes.fromhex(le(L['bank_for38'])),'UncompressMonSprite bank choice -> bank_for38 (species 86 in bank 4)',le(L25['bank_for']))
def hdr(stats,types,catch,exp,dims,front,back,moves,growth):
    return bytes(stats)+bytes(types)+bytes([catch,exp,dims])+bytes.fromhex(le(front)+le(back))+bytes(moves)+bytes([growth])+bytes(8)
red_hdr=hdr([1,1,1,1,1],[0,0],0,0,0x77,0x6f2a,0x6f2a,[0,0,0,0],0)
HE=0x7eb0
assert not any(R[fo(0xe,0x7ea5):fo(0xe,0x8000)])
hc,HL=asm(f'''
hdr38:
    ld a,[$d0b5]
    cp {REDSP}
    jp nz,$7e41
    ld hl,red_hdr
    ld de,$d0b9
    ld b,27
.l: ld a,[hl+]
    ld [de],a
    inc de
    dec b
    jr nz,.l
    ld a,{REDSP}
    ld [$d0b8],a
    ret
red_hdr: db {','.join(str(x) for x in red_hdr)}
''',HE)
rom.put(fo(0xe,HE),hc,'Bank E: header for species 86 (RED trainer picture, evolution scene)')
rom.code(0x15c6,bytes.fromhex('cd'+le(HE)),'GetMonHeader exit -> v38 header (species 86), then v25/v23/v3','cd417e',
         reviewed='same site as v3/v23/v25; hits are operand/data bytes')
DEX=0x4102e
rom.data(DEX+REDSP-1,[152],'Species 86: dex slot 152 like BLACK (the front-picture loader refuses dex 0)','00')
CRY=0x39484;gcry=bytes(R[CRY+3*(0x0e-1):CRY+3*0x0e])
rom.data(CRY+3*(REDSP-1),gcry,'Species 86 cry = GENGAR (never heard: evolution plays the new species)',R[CRY+3*(REDSP-1):CRY+3*REDSP])
for a in (0x4514,0x453f):
    rom.data(fo(0x2d,a),bytes([REDSP]),'Climax evolution: start from RED (species 86) instead of GHOST','1f')

# 2. trainer card
TC=0x7b00
assert not any(R[fo(4,0x7af6):fo(4,0x7c00)])
tc,TL=asm(f'''
tcard:
    ld a,[{BLACKF}]
    and a
    ld de,$6f2a
    ld bc,$0401
    ret z
    ld de,$41c0
    ld bc,$2d01
    ret
''',TC)
rom.put(fo(4,TC),tc,'Bank 4: trainer card picture (BLACK TAMER when BLACK)')
rom.hook(fo(4,0x74e6),'cd'+le(TC)+'000000','DrawTrainerInfo: BLACK TAMER picture','112a6f 010104',provides=('a','f','b','c','d','e'))

# 3. end of the ritual
DP=fo(0x2d,0x46b4)
rom.data(DP,bytes.fromhex('c3'+le(L['black_join'])+'000000'),'do_post end -> black_join (BLACK, PRETA, AZHI join)','3e06ea67d4c9')

# 4a. can't faint: the five "player mon fainted?" checks in bank F
for a in (0x4236,0x453a,0x454d,0x45e7,0x4df1):
    rom.hook(fo(0xf,a),'cd'+le(STUBS['alive_chk'])+'0000','Player mon fainted? check: BLACK keeps 1 HP','2115d02ab6',provides=('a','f','b','c','h','l'))
# 4b. items: the party menu of EvoStone / Medicine / PP items / TMs
for a in (0x5da8,0x5e33,0x6662,0x681a):
    rom.hook(fo(3,a),'cd'+le(STUBS['item_party']),'Item party menu: no item works on BLACK','cd2b14',provides=('a','f','b','c','h','l','d','e'))
# 4c. Name Rater
rom.hook(fo(7,0x5a95),'cd'+le(STUBS['name_ot']),'Name Rater: BLACK can\'t be renamed','cd305a',provides=('a','f','b','c','h','l'))
# 4d. PC deposit
rom.hook(fo(8,0x55da),'cd'+le(STUBS['deposit'])+'000000','PC deposit: BLACK can\'t be stored','fa91cf cd0814',provides=('a','f','b','c','h','l','d','e'))
# 4e/f. bank 15: Day Care and battle experience
B15=0x6ac0
assert not any(R[fo(0x15,B15):fo(0x15,0x6b40)])
c15,L15=asm(f'''
dc_menu:                         ; Day Care party menu: BLACK stays
    call {PARTYMENU:#x}
    ret c
    ld a,[$cf91]
    cp {BLK}
    jr z,.no
    and a
    ret
.no:
    ld hl,t_dc
    call {PRINTTEXT:#x}
    scf
    ret
exp_skip:                        ; GainExperience: BLACK never gains experience in battle
    call $3ec1
    ld a,[$cf92]
    ld e,a
    ld d,0
    ld hl,$d164
    add hl,de
    ld a,[hl]
    cp {BLK}
    ret nz
    ld c,0
    ret
t_dc: db $17
    dw {TS['t_daycare']:#x}
    db $2d,$50
''',B15)
rom.put(fo(0x15,B15),c15,'Bank 15: v38 Day Care / battle experience (BLACK)')
rom.hook(fo(0x15,0x62a4),'cd'+le(L15['dc_menu']),'Day Care: BLACK can\'t be left there','cd2b14',provides=('a','f','h','l'))
rom.hook(fo(0x15,0x5271),'cd'+le(L15['exp_skip']),'GainExperience: BLACK gains no battle experience','cdc13e',provides=('a','f','c','d','e','h','l'))
labels['bank15']={k:hex(v) for k,v in L15.items()}
# 4g. poison outside battle: hunger_wrap's "BLACK -> ret" becomes black_step
HW=fo(0x2d,L25['hunger_wrap'])
rom.data(HW,bytes.fromhex('cd'+le(L['black_step'])+'0000'),'hunger_wrap: BLACK branch -> black_step (poison can\'t kill BLACK)','fa6cd4a7c0')
rom.finish('Creepy_Black_Mu_v38.gb','manifest_v38.json','CREEPY MU V38',extra=dict(labels=labels))
