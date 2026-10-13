# Creepy Black Mu v47: Black Tamer mechanics redux, part 1.
#   1. BANE is renamed METAMORPHOSIS (move AA). In battle it plays the THUNDERBOLT animation first, then the black
#      screen, the cry and the black POKe BALL as before. On the map ("METAMORPHOSIS?") it works as before, no animation.
#   2. Every POKeMON gained through METAMORPHOSIS (battle, trainer phase, black ball on the map) is marked (party/box
#      struct byte 7, the unused "catch rate" copy, = MARK) and is pitch black: battle back picture, status-screen front
#      picture, party-menu icon.
#   3. CONSUME is gone: BLACK's party-menu entry is CURSE. CURSE eats a party member (not BLACK, PRETA, AZHI) and BLACK gains
#      its experience (levels as before); no move is taken any more.
#   4. BLACK's moves are METAMORPHOSIS and CURSE (fixed; every step outside battle puts them back with full PP, so older
#      BLACKs with BANE or consumed moves are switched too). v39's CURSE -> BANE migration is replaced.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V46_SHA='ad8f26d1a867508a7ec7d08066fbb8b6371bea253d3e43de1fe684558995d6f2'
rom=Rom('Creepy_Black_Mu_v46.gb',V46_SHA)
r=rom.r;R=bytes(r)
L38=json.load(open('manifest_v38.json'))['labels']
L39={k:int(v,16) for k,v in json.load(open('manifest_v39.json'))['labels']['bank2f'].items()}
L39d={k:int(v,16) for k,v in json.load(open('manifest_v39.json'))['labels']['bank2d'].items()}
L41={k:int(v,16) for k,v in json.load(open('manifest_v41.json'))['labels']['bank2f'].items()}
L41b1={k:int(v,16) for k,v in json.load(open('manifest_v41.json'))['labels']['bank1'].items()}
PRINTTEXT,ADDNTIMES,COPYVID,DELAY,PREDEF,BANKSW=0x3c94,0x3abb,0x1875,0x3773,0x3ec1,0x3618
META,CURSE,BLK=0xaa,0xa5,0x7f
THUNDERBOLT=0x55
MARK=0x01                                   # byte 7 of a party/box struct: no species has catch rate 1 (and no overhaul struct)
BS=fo(0xe,0x43e4);assert R[BS]==1 and R[BS+28*149]==150
assert MARK not in {R[BS+28*i+8] for i in range(150)} and R[0x425b+8]!=MARK
for k in ('s_black','s_preta','s_azhi'):assert R[fo(0x2d,int(L38['bank2d'][k],16))+7]!=MARK
assert R[0x147]==0x13                       # MBC3: SRAM bank register at $4000 (no upper ROM bits)
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
def find1(bank,lo,hi,pat):
    s=R[fo(bank,lo):fo(bank,hi)];i=s.find(pat);assert i>=0 and s.find(pat,i+1)<0,(hex(bank),pat.hex(),i);return fo(bank,lo)+i

# ---- 1. the name
NM=0xb0636
assert R[NM:NM+5]==enc('BANE')+b'\x50' and not any(R[NM+5:NM+0x20])
rom.data(NM,enc('METAMORPHOSIS')+b'\x50','Move name AA: BANE -> METAMORPHOSIS',R[NM:NM+14])

BANK=0x2f;CODE=0x7600
assert not any(R[fo(BANK,CODE):fo(BANK,0x8000)])
T={'t_used':tx('BLACK used','line','METAMORPHOSIS!'),
   't_full':tx('The PC is full.','line','It failed!'),
   't_ask':tx('They are shaking.','line','METAMORPHOSIS?',end=0x57)}
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())
SMOVES=[META,CURSE,0,0]
def maxpp(mv):
    if mv==0:return 0
    if mv<0xa7:return R[fo(0xe,0x4000)+(mv-1)*6+5]
    return R[fo(0xe,0x7d30)+(mv-0xa7)*6+5]
SPP=[maxpp(x) for x in SMOVES]
assert SPP==[10,1,0,0],SPP
G=L39['give'];ENDS=[]
for i in range(fo(BANK,G),fo(BANK,L39['name_cf91'])):
    if R[i]==0x21 and R[i+3:i+6]==bytes.fromhex('c3943c'):ENDS.append((i,R[i+1]|R[i+2]<<8))
assert len(ENDS)==2,ENDS
(TP,tpart),(TB,tbox)=ENDS

code,L=asm(f'''
; ---- 1. METAMORPHOSIS in battle: THUNDERBOLT's animation, then v39's black screen / cry / black ball (a = species)
meta_ball:
    push af
    ldh a,[$f3]
    push af
    xor a
    ldh [$f3],a                  ; the player's move: from BLACK to the target
    ld a,{THUNDERBOLT}
    ld [$d07c],a                 ; wAnimationID
    ld c,3
    call {DELAY:#x}
    ld a,8                       ; predef MoveAnimation
    call {PREDEF:#x}
    pop af
    ldh [$f3],a
    pop af
    jp {L39['black_ball']:#x}

; ---- 2. the mark: give (v39) ends here (party: the last member; box: SendNewMonToBox puts the new one first)
mark_party:
    ld a,[$d163]
    dec a
    ld hl,$d16b+7
    ld bc,44
    call {ADDNTIMES:#x}
    ld [hl],{MARK}
    ld hl,{tpart:#x}
    jp {PRINTTEXT:#x}
mark_box:
    ld a,{MARK}
    ld [$da96+7],a
    ld hl,{tbox:#x}
    jp {PRINTTEXT:#x}

; every non-white pixel of the merged picture in SRAM (sSpriteBuffer1, 7x7 tiles) -> black
blacken:
    ld a,$0a
    ld [$0000],a
    xor a
    ld [$4000],a
    ld hl,$a188
    ld bc,392
.l: ld a,[hl+]
    or [hl]
    ld [hl-],a
    ld [hl+],a
    inc hl
    dec bc
    ld a,b
    or c
    jr nz,.l
    ret

; LoadMonBackPic's tail (F:720E -> here): a marked POKeMON out -> black picture in vBackPic, then the copy to vSprites
back47:
    ld a,[$cc2f]
    ld c,a
    ld b,0
    ld hl,$d164
    add hl,bc
    ld a,[$cfd9]
    cp [hl]
    jr nz,.copy
    ld a,c
    ld hl,$d16b+7
    ld bc,44
    call {ADDNTIMES:#x}
    ld a,[hl]
    cp {MARK}
    jr nz,.copy
    call blacken
    ld de,$a188
    ld hl,$9310
    ld c,$31
    ld b,{BANK:#x}
    call {COPYVID:#x}
.copy:
    ld hl,$8000
    ld de,$9310
    ld c,$31
    ld b,{BANK:#x}
    jp {COPYVID:#x}

; status screen (bank 4 stub, after LoadFlippedFrontSpriteByMonIndex, wLoadedMon marked): black front picture
front47:
    call blacken
    ld de,$a188
    ld hl,$9000
    ld c,$31
    ld b,{BANK:#x}
    jp {COPYVID:#x}

; ---- 4. BLACK's moves: METAMORPHOSIS, CURSE, full PP (every step outside battle; replaces v39's CURSE -> BANE)
mig47:
    ld hl,$d164
    ld de,$d16b
.f: ld a,[hl+]
    cp $ff
    ret z
    cp {BLK}
    jr z,.got
    push hl
    ld hl,44
    add hl,de
    ld d,h
    ld e,l
    pop hl
    jr .f
.got:
    ld hl,8
    add hl,de
    ld de,bmoves
    ld b,4
.m: ld a,[de]
    ld [hl+],a
    inc de
    dec b
    jr nz,.m
    ld bc,17
    add hl,bc
    ld b,4
.p: ld a,[de]
    ld [hl+],a
    inc de
    dec b
    jr nz,.p
    ret
bmoves: db {','.join(str(x) for x in SMOVES+SPP)}
{TXT}''',CODE)
rom.put(fo(BANK,CODE),code,'Bank 2F: v47 METAMORPHOSIS (animation, mark, black pictures), BLACK moves')
labels['bank2f']={k:hex(v) for k,v in L.items()}

# give's two endings (ld hl,t_party / jp PrintText, ld hl,t_box / jp PrintText) -> mark first
rom.code(TP,bytes.fromhex('c3'+le(L['mark_party'])),'give (party): mark the new member first',R[TP:TP+3].hex())
rom.code(TB,bytes.fromhex('c3'+le(L['mark_box'])),'give (box): mark the new box POKeMON first',R[TB:TB+3].hex())

# METAMORPHOSIS animation: bane_move's and bane_phase's call black_ball -> meta_ball
for at in (0x4040,0x4167):
    assert R[fo(BANK,at):fo(BANK,at)+3]==bytes.fromhex('cd'+le(L39['black_ball']))
    rom.code(fo(BANK,at),bytes.fromhex('cd'+le(L['meta_ball'])),'METAMORPHOSIS: THUNDERBOLT animation before the black ball','cd'+le(L39['black_ball']))
# texts: "BLACK used METAMORPHOSIS!", "The PC is full. It failed!"
for old,new in ((tx('BLACK used BANE!'),'t_used'),(tx('The PC is full.','line','BANE failed.'),'t_full')):
    a=find1(BANK,0x4000,0x4400,old);ta=0x4000+a-fo(BANK,0x4000)
    refs=[i for i in range(fo(BANK,0x4000),fo(BANK,0x4200)) if R[i:i+3]==bytes([0x21,ta&255,ta>>8])]
    assert refs,new
    for i in refs:rom.code(i,bytes.fromhex('21'+le(L[new])),'METAMORPHOSIS text: '+new,R[i:i+3].hex())
# map question (2D:4874 ld hl,$5C00): TX_FAR to "They are shaking. METAMORPHOSIS?"
old=txt([["They are shaking.","BANE them?"]],0x57)
assert R[fo(0x2d,0x5c00):fo(0x2d,0x5c00)+len(old)]==old
rom.data(fo(0x2d,0x5c00),bytes([0x17])+bytes.fromhex(le(L['t_ask']))+bytes([BANK,0x50]),'Map question -> "METAMORPHOSIS?" (TX_FAR to 2F)',old[:5])

# ---- 2. black pictures
# battle back picture: LoadMonBackPic's copy to vSprites (F:720E ld hl,$8000 / ld de,$9310 / ld c,$31) -> 2F back47
rom.code(fo(0xf,0x720e),bytes.fromhex('21'+le(L['back47'])+'062fc31836'),'LoadMonBackPic: marked POKeMON -> black back picture','2100801110930e31')
# status screen: bank 4 stub after LoadFlippedFrontSpriteByMonIndex
B4=0x7b60
assert not any(R[fo(4,B4):fo(4,B4)+0x20])
c4,L4=asm(f'''
st47:
    call $13b3
    ld a,[$cf9f]                 ; wLoadedMon + 7
    cp {MARK}
    ret nz
    ld hl,{L['front47']:#x}
    ld b,{BANK:#x}
    jp {BANKSW:#x}
''',B4)
rom.put(fo(4,B4),c4,'Bank 4: v47 status screen black front picture')
rom.hook(fo(4,0x6aba),'cd'+le(L4['st47']),'StatusScreen: marked POKeMON -> black front picture','cdb313',provides=('a','f','b','c','d','e','h','l'))
# party icons: WriteMonPartySpriteOAMByPartyIndex's call WriteMonPartySpriteOAM (1C:58B9) -> icon47 (OBP1 = black)
B1C=0x7cc0
assert not any(R[fo(0x1c,B1C):fo(0x1c,B1C)+0x40])
c1c,L1C=asm(f'''
icon47:
    call $5901
    ldh a,[$8c]
    ld hl,$d16b+7
    ld bc,44
    call {ADDNTIMES:#x}
    ld a,[hl]
    cp {MARK}
    ret nz
    ldh a,[$8c]
    swap a
    add 3
    ld l,a
    ld h,$c3
    ld b,4
.l: set 4,[hl]
    push hl
    ld de,$cc5b-$c300
    add hl,de
    set 4,[hl]
    pop hl
    ld a,l
    add 4
    ld l,a
    dec b
    jr nz,.l
    ld a,$ff
    ldh [$49],a
    ret
''',B1C)
rom.put(fo(0x1c,B1C),c1c,'Bank 1C: v47 black party icons (OBP1)')
rom.hook(fo(0x1c,0x58b9),'cd'+le(L1C['icon47']),'Party icon: marked POKeMON -> black (OBP1)','cd0159',provides=('a','f','b','c','d','e','h','l'))

# ---- 3. CURSE instead of CONSUME (field-move name, prompt), no move taken
FN=find1(1,0x7d80,0x7de3,enc('CONSUME')+b'\x50')
rom.data(FN,enc('CURSE')+b'\x50\x50\x50','Field move name: CONSUME -> CURSE',enc('CONSUME')+b'\x50')
old=tx('Consume which','line','#MON?');a=find1(BANK,0x5400,0x5800,old)
new=tx('Curse which','line','#MON?');rom.data(a,new+bytes(old[len(new):]),'CURSE prompt: "Curse which #MON?"',old)
assert R[fo(BANK,0x542c):fo(BANK,0x5431)]==bytes.fromhex('cd'+le(int(json.load(open('manifest_v46.json'))['labels']['bank2f']['pick46'],16))+'285a')
rom.code(fo(BANK,0x542c),bytes.fromhex('c38b540000'),'CURSE (party menu): consume at once, no move taken',R[fo(BANK,0x542c):fo(BANK,0x5431)].hex())

# ---- 4. BLACK's moves: the struct for new BLACKs and the per-step fix (hunger_wrap's BLACK branch, 2D:44C9)
SB=fo(0x2d,int(L38['bank2d']['s_black'],16))
assert R[SB+8:SB+12]==bytes([META,0,0,0]) and R[SB+29:SB+33]==bytes([10,0,0,0])
rom.data(SB+8,bytes(SMOVES),'BLACK struct: METAMORPHOSIS, CURSE',R[SB+8:SB+12])
rom.data(SB+29,bytes(SPP),'BLACK struct: PP',R[SB+29:SB+33])
S2D=0x7f60
assert not any(R[fo(0x2d,S2D):fo(0x2d,S2D)+0x10])
c2d,L2D=asm(f'''
step47:
    ld a,[$d46c]
    and a
    ret z
    farcall {L['mig47']:#x},{BANK:#x}
    jp {int(L38['bank2d']['black_step'],16):#x}
''',S2D)
rom.put(fo(0x2d,S2D),c2d,'Bank 2D: v47 BLACK step (moves, then black_step)')
HW=fo(0x2d,0x44c9)
rom.data(HW+1,bytes.fromhex(le(L2D['step47'])),'hunger_wrap BLACK branch -> step47 (fixed moves, full PP)',le(L39d['step39']))
labels['bank4']={k:hex(v) for k,v in L4.items()};labels['bank1c']={k:hex(v) for k,v in L1C.items()};labels['bank2d']={k:hex(v) for k,v in L2D.items()}
rom.finish('Creepy_Black_Mu_v47.gb','manifest_v47.json','CREEPY MU V47',extra=dict(labels=labels,mark=MARK))
