# Creepy Black Mu v49: Black Tamer mechanics redux, part 3 (what BLACK is).
#   1. POKeMON are too scared to attack BLACK: with BLACK out, the enemy's turn is "<enemy> is too scared to move!" (the
#      base game's GHOST rule, now also for BLACK) - except in the LEAGUE battles protected by the MOON STONE (v44), in
#      MIRAGE battles and for PRETA / AZHI.
#   2. Status immunity (move effects): BLACK can't be poisoned, burned, frozen, paralyzed, put to sleep or confused; PRETA
#      and AZHI can't be poisoned, paralyzed, put to sleep or confused (burn and freeze still work). A status move says
#      "It doesn't affect <target>!"; a side effect simply doesn't happen. Either side (the MIRAGE's PRETA / AZHI too).
#   3. As BLACK there are no random encounters in POKeMON TOWER (1F-7F).
#   4. As BLACK nobody serves you: POKeMON Center nurses, POKe MART clerks, the GAME CORNER prize vendor and coin clerk,
#      the BIKE SHOP, the MAGIKARP salesman, the DAY CARE, the NAME RATER, every in-game trade and the fossil revival.
#      They are too scared (the panicking NPCs still get v40's METAMORPHOSIS question first; NO -> they won't help).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V48_SHA='de46558fa472bda5e2dacf6376b227cb476af9b799cd64643ad4e9c42d0d53a0'
rom=Rom('Creepy_Black_Mu_v48.gb',V48_SHA)
r=rom.r;R=bytes(r)
L44={k:int(v,16) for k,v in json.load(open('manifest_v44.json'))['labels']['bank2f'].items()}
PRINTTEXT,BANKSW=0x3c94,0x3618
BLK,PRETA,AZHI,GHOST=0x7f,0xb6,0xb7,0x1f
BLACKF,TMP=0xd46c,0xd45a
labels={}
def tx(*parts,end=0x58):
    out=bytearray([0])
    for p in parts:
        if p in ('line','cont','para'):out+={'line':b'\x4f','cont':b'\x55','para':b'\x51'}[p]
        else:assert shown(p)<=17,p;out+=enc(p)
    out+=bytes([end]);return bytes(out)

# ---- home 0x08: rst 08 = far call (nop, then 0x09 jp Bankswitch); needed for 6-byte far calls from bank F
assert R[0x08:0x0c]==bytes.fromhex('ffc31836')
rom.data(0x08,b'\x00','Home 0x08: rst 08 = jp Bankswitch (far call: ld hl,addr / ld b,bank / rst 08)',b'\xff')

# effect ids (pokered order, checked against the effect table below)
PSN1,BRN1,FRZ1,PAR1,SLP,PSN2,BRN2,FRZ2,PAR2,CONF,PSN,PAR,CONF2=0x02,0x04,0x05,0x06,0x20,0x21,0x22,0x23,0x24,0x31,0x42,0x43,0x4c
ET=fo(0xf,0x723f)
def eff(e):return R[ET+2*(e-1)]|R[ET+2*(e-1)+1]<<8
assert eff(PSN1)==eff(PSN2)==eff(PSN)==0x7346 and eff(SLP)==0x72f3 and eff(PAR)==0x7aa8 and eff(CONF)==0x7a58 and eff(CONF2)==0x7a50
assert len({eff(BRN1),eff(FRZ1),eff(PAR1),eff(BRN2),eff(FRZ2),eff(PAR2)})==1 and eff(BRN1)==0x7403
IMM_BLACK=[PSN1,BRN1,FRZ1,PAR1,SLP,PSN2,BRN2,FRZ2,PAR2,CONF,PSN,PAR,CONF2]
IMM_PA=[PSN1,PAR1,SLP,PSN2,PAR2,CONF,PSN,PAR,CONF2]
PRIMARY=[SLP,CONF,PSN,PAR]
NOAFF=R[fo(0xf,0x5d2d):fo(0xf,0x5d32)];assert NOAFF==bytes.fromhex('17d05a2250')        # "It doesn't affect <TARGET>!"
SCARED=R[fo(0xf,0x5906):fo(0xf,0x590b)];assert SCARED==bytes.fromhex('17e3582250')      # "<enemy> is too scared to move!"
assert R[fo(0xf,0x72f2)]==0xc9

T={'t_nurse':tx('The nurse is','line','shaking...','para','She is too scared','line','to help you.'),
   't_shop':tx('The clerk is','line','shaking...','para','Too scared to','line','serve you.'),
   't_other':tx('They are shaking','line','too much to help','cont','you...'),
   't_hi':bytes.fromhex('179c652850')}
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())
BANK=0x2f;CODE=0x7900
assert not any(R[fo(BANK,CODE):fo(BANK,0x8000)])
# TX_ASM services: (map, text number) -> the text's own bank / address (its TX_ASM code starts after the 08)
SERV=[(0x48,1,'DAY CARE'),(0xe5,1,'NAME RATER'),(0xaa,1,'fossil revival'),(0x44,4,'MAGIKARP salesman'),(0x87,2,'GAME CORNER coins'),(0x42,1,'BIKE SHOP')]
serv=[]
for mp,t,name in SERV:
    p=R[0x1ae+2*mp]|R[0x1ae+2*mp+1]<<8;b=R[0xc23d+mp];o=fo(b,p);tp=R[o+5]|R[o+6]<<8
    e=tp+2*(t-1);a=R[fo(b,e)]|R[fo(b,e)+1]<<8
    assert R[fo(b,a)]==0x08,(name,hex(b),hex(a))
    serv.append(dict(map=mp,t=t,name=name,bank=b,entry=e,text=a))
SV=''.join(f'''
sv{i}:
    db 8
    ld hl,{s['text']+1:#x}
    ld b,{s['bank']:#x}
    jp svc
''' for i,s in enumerate(serv))
code,L=asm(f'''
; ---- 1. the enemy's turn (F:67C8 via rst 08): z = too scared (text printed), nz = it attacks
scared49:
    ld a,[$d014]
    cp {GHOST}
    jr z,.yes                    ; the base game's rule
    cp {BLK}
    jr nz,.no
    call {L44['e4chk']:#x}       ; LORELEI / BRUNO / LANCE (MOON STONE): they attack
    jr z,.no
    ld a,[$d45d]
    and a
    jr nz,.no
    ld a,[$cfe5]
    cp {PRETA}
    jr z,.no
    cp {AZHI}
    jr z,.no
.yes:
    ld hl,t_scared
    call {PRINTTEXT:#x}
    xor a
    ret
.no:or 1
    ret
t_scared: db {','.join(str(x) for x in SCARED)}

; ---- 2. _JumpMoveEffect (F:7227 via rst 08): the effect id -> [TMP]; immune target: skip the effect (return to F:72F2 ret)
imm49:
    ldh a,[$f3]
    and a
    ld a,[$cfd3]
    jr z,.p
    ld a,[$cfcd]
.p: ld [{TMP:#x}],a
    ld c,a
    ldh a,[$f3]
    and a
    ld a,[$cfe5]
    jr z,.t
    ld a,[$d014]
.t: ld hl,imm_black
    cp {BLK}
    jr z,.s
    ld hl,imm_pa
    cp {PRETA}
    jr z,.s
    cp {AZHI}
    ret nz
.s: ld a,[hl+]
    cp $ff
    ret z
    cp c
    jr nz,.s
    ld hl,primary
.q: ld a,[hl+]
    cp $ff
    jr z,.skip
    cp c
    jr nz,.q
    ld hl,t_noaff
    call {PRINTTEXT:#x}
.skip:
    ld hl,sp+4
    ld a,$f2
    ld [hl+],a
    ld [hl],$72
    ret
imm_black: db {','.join(str(x) for x in IMM_BLACK)},$ff
imm_pa: db {','.join(str(x) for x in IMM_PA)},$ff
primary: db {','.join(str(x) for x in PRIMARY)},$ff
t_noaff: db {','.join(str(x) for x in NOAFF)}

; ---- 4. services
; the mart greeting (0:2A82 TX_FAR -> here, TX_ASM): BLACK -> the scared clerk, else "Hi there! May I help you?"
hi49:
    db 8
    ld a,[{BLACKF:#x}]
    and a
    ld hl,t_hi
    ret z
    ld hl,t_shop
    ret
; in-game trades: predef 55 (DoInGameTradeDialogue, 1C:5AD7) -> here
trade49:
    ld a,[{BLACKF:#x}]
    and a
    jr nz,.no
    ld hl,$5ad7
    ld b,$1c
    jp {BANKSW:#x}
.no:ld hl,t_other
    jp {PRINTTEXT:#x}
; TX_ASM service texts (TX_FAR stub in their bank -> svN here): BLACK -> refused, else the original code in its bank
svc:
    ld a,[{BLACKF:#x}]
    and a
    jp z,{BANKSW:#x}
    ld hl,t_other
    ret
{SV}
{TXT}''',CODE)
rom.put(fo(BANK,CODE),code,'Bank 2F: v49 scared POKeMON, status immunity, services refused')
labels['bank2f']={k:hex(v) for k,v in L.items()}

# 1. F:67C8 (GHOST out -> scared text, jp ExecuteEnemyMoveDone) -> rst 08 scared49 / jp z,6972 / nops to F:67D8
old=bytes.fromhex('fa14d0fe1f2009210659cd943cc37269')
assert R[fo(0xf,0x67c8):fo(0xf,0x67d8)]==old
new=bytes.fromhex('21'+le(L['scared49'])+'062fcf'+'ca7269')
rom.code(fo(0xf,0x67c8),new+bytes(len(old)-len(new)),'Enemy turn: too scared of GHOST and of BLACK (not MOON STONE / MIRAGE / PRETA / AZHI)',old,
         reviewed='hits are home bytes "ld [$c4f2],a / call $1b67" (0:1ACC ...) misread as call nz,$67cd; nothing jumps into F:67C8-67D7')
# 2. F:7227 _JumpMoveEffect: ldh a,[hWhoseTurn] / and a / ld a,[wPlayerMoveEffect] / jr z / ld a,[wEnemyMoveEffect]
#    -> rst 08 imm49 (may skip the effect) / ld a,[TMP] / nop nop, then F:7232 dec a ... as before
old=bytes.fromhex('f0f3a7fad3cf2803facdcf')
assert R[fo(0xf,0x7227):fo(0xf,0x7232)]==old
new=bytes.fromhex('21'+le(L['imm49'])+'062fcf'+'fa'+le(TMP)+'0000')
assert len(new)==len(old)
rom.code(fo(0xf,0x7227),new,'_JumpMoveEffect: status immunity of BLACK / PRETA / AZHI',old)

# 3. no Tower encounters as BLACK: TryDoWildEncounter (4:78BC ld a,[wNPCMovementScriptPointerTableNum]) -> tow49
B4=0x7b80
assert not any(R[fo(4,B4):fo(4,B4)+0x20])
c4,L4=asm(f'''
tow49:
    ld a,[{BLACKF:#x}]
    and a
    jr z,.no
    ld a,[$d35e]
    cp $8e
    jr c,.no
    cp $95
    jr nc,.no
    pop af
    ld a,1                       ; "can't encounter" (TryDoWildEncounter's own exit)
    and a
    ret
.no:ld a,[$cc57]
    ret
''',B4)
rom.put(fo(4,B4),c4,'Bank 4: v49 no Tower encounters as BLACK')
rom.hook(fo(4,0x78bc),'cd'+le(L4['tow49']),'TryDoWildEncounter: no encounters in POKeMON TOWER as BLACK','fa57cc',provides=('a','f'))

# 4. services
# nurse (1:6FDF call SaveScreenTilesToBuffer1) and mart (1:6C19 ld a,[wListScrollOffset]) -> bank 1 stubs
B1=0x7e40                                    # (1:7E00-7E0E = the test ROMs' save installer)
assert not any(R[fo(1,B1):fo(1,B1)+0x30])
c1,L1=asm(f'''
nurse49:
    ld a,[{BLACKF:#x}]
    and a
    jp z,$3753
    ld hl,tf_nurse
    call {PRINTTEXT:#x}
    pop af                       ; leave DisplayPokemonCenterDialogue_
    ret
mart49:
    ld a,[{BLACKF:#x}]
    and a
    ld a,[$cc36]
    ret z
    pop af                       ; leave DisplayPokemartDialogue_ (the greeting already said it)
    ret
tf_nurse: db $17,{L['t_nurse']&255},{L['t_nurse']>>8},{BANK},$50
''',B1)
rom.put(fo(1,B1),c1,'Bank 1: v49 nurse / mart refuse BLACK')
rom.hook(fo(1,0x6fdf),'cd'+le(L1['nurse49']),'POKeMON Center nurse: BLACK refused','cd5337',provides=('a','f','h','l'))
rom.hook(fo(1,0x6c19),'cd'+le(L1['mart49']),'POKe MART: BLACK refused','fa36cc',provides=('a','f'))
rom.data(0x2a83,bytes.fromhex(le(L['hi49']))+bytes([BANK]),'Mart greeting TX_FAR -> hi49 (BLACK: scared clerk)','9c6528')
# prize vendor (14:671B ld b,$45 / call HasCoinCase...) -> bank 14 stub
B14=0x7f60
assert not any(R[fo(0x14,B14):fo(0x14,B14)+0x18])
c14,L14=asm(f'''
prize49:
    ld a,[{BLACKF:#x}]
    and a
    jr nz,.no
    ld b,$45
    jp $34d5
.no:ld hl,tf_shop
    call {PRINTTEXT:#x}
    pop af
    ret
tf_shop: db $17,{L['t_shop']&255},{L['t_shop']>>8},{BANK},$50
''',B14)
rom.put(fo(0x14,B14),c14,'Bank 14: v49 prize vendor refuses BLACK')
rom.hook(fo(0x14,0x671b),'cd'+le(L14['prize49'])+'0000','GAME CORNER prize vendor: BLACK refused','0645cdd534',provides=('a','f','b','h','l'))
# trades: predef 55 -> trade49
PD=fo(0x13,0x7e79)+3*0x55
assert R[PD:PD+3]==bytes.fromhex('1cd75a')
rom.data(PD,bytes([BANK])+bytes.fromhex(le(L['trade49'])),'Predef 55 (in-game trade) -> trade49 (BLACK refused)','1cd75a')
# TX_ASM services: a TX_FAR stub in the text's bank (5 bytes) and the map's text pointer -> the stub
FREE={}
for i,s in enumerate(serv):
    b=s['bank']
    s0=R[fo(b,0x4000):fo(b,0x8000)];end=len(s0)
    while s0[end-1]==0:end-=1
    at=FREE.get(b,0x4000+end+0x10)
    assert not any(R[fo(b,at):fo(b,at)+5])
    stub=bytes([0x17])+bytes.fromhex(le(L['sv%d'%i]))+bytes([BANK,0x50])
    rom.put(fo(b,at),stub,'Bank %X: v49 TX_FAR -> %s check'%(b,s['name']))
    rom.data(fo(b,s['entry']),bytes.fromhex(le(at)),'%s text -> BLACK check first'%s['name'],le(s['text']))
    s['stub']=hex(at);FREE[b]=at+5
labels['bank1']={k:hex(v) for k,v in L1.items()};labels['bank4']={k:hex(v) for k,v in L4.items()};labels['bank14']={k:hex(v) for k,v in L14.items()}
rom.finish('Creepy_Black_Mu_v49.gb','manifest_v49.json','CREEPY MU V49',extra=dict(labels=labels,services=[{k:(hex(v) if isinstance(v,int) else v) for k,v in s.items()} for s in serv]))
