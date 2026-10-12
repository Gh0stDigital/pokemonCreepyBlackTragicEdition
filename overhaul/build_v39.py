# Creepy Black Mu v39: BANE in battle (part 2 of the BLACK TAMER mechanics).
#   Move AA (free since v11 removed DRAGONBREATH) = BANE: BLACK's move (new BLACK struct; older saves are switched from
#   CURSE to BANE on the next step).
#   - BANE on a POKeMON (wild or a trainer's, BLACK out): "BLACK used BANE!", the screen goes black, the POKeMON's cry,
#     a black POKe BALL stands where it was, it joins the party (full -> the current PC box) with its battle data.
#     Wild: the battle ends (escape flag); trainer: it counts as fainted (the trainer goes on / loses).
#     No effect on PRETA, AZHI, GHOST, ????? (and in MIRAGE battles), or when party and box are full.
#   - BANE on a human: the after-win trainer phase now also starts when BLACK is out; the trainer dies as before
#     (gravestone etc., BLUE still can't), then turns into a random POKeMON not caught yet: black screen, its cry,
#     a black POKe BALL, "The trainer became <MON>!", it joins the party (or the PC box) at the last POKeMON's level.
#   New code/data in bank 2F (an empty bank: 2F-3F were never used).
import json
from PIL import Image,ImageDraw
from patchlib import *
from patchguard import fo
from sm83asm import asm

V38_SHA='c511ada7c0669642d7827b9034e4bf2ed2f786cae9f6807808d582f915dd7488'
rom=Rom('Creepy_Black_Mu_v38.gb',V38_SHA)
r=rom.r;R=bytes(r)
L38=json.load(open('manifest_v38.json'))['labels']
BANE,CURSE,BLK=0xaa,0xa5,0x7f
RIVAL1,RIVAL2=25,42
PRINTTEXT,DELAY,PLAYCRY,COPYVID,PALNORMAL,RANDOM,GETMONNAME,ADDPARTYMON=0x3c94,0x3773,0x13ff,0x1875,0x3e27,0x3eb0,0x2fcf,0x395b
BANK=0x2f;CODE=0x4000
assert not any(R[fo(BANK,0x4000):fo(BANK,0x8000)])
labels={}

# ---- move AA = BANE: data (effect 55 = Splash "nothing happened" if it ever runs as a plain move) and name
rom.data(fo(0xe,0x7d42),bytes([BANE,0x55,0,0x1b,0xff,10]),'Move data AA = BANE (handled before the move runs)',bytes(6))
assert R[0xb0635]==0x50 and not any(R[0xb0636:0xb0640])
rom.data(0xb0636,enc('BANE')+b'\x50','Move name AA = BANE',bytes(5))
# new BLACKs know BANE
SB=fo(0x2d,int(L38['bank2d']['s_black'],16))
assert R[SB+8]==CURSE
rom.data(SB+8,bytes([BANE]),'BLACK struct: BANE instead of CURSE',bytes([CURSE]))
rom.data(SB+29,bytes([10]),'BLACK struct: BANE PP 10',bytes([R[SB+29]]))

# ---- the black POKe BALL (7x7 tiles, column-major like every front picture)
im=Image.new('L',(56,56),0);d=ImageDraw.Draw(im)
cx,cy,rad=28,40,11
d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),fill=3)
d.rectangle((cx-rad,cy-1,cx+rad,cy),fill=1)                      # grey band
d.ellipse((cx-4,cy-4,cx+3,cy+3),fill=1);d.ellipse((cx-2,cy-2,cx+1,cy+1),fill=3)   # button
d.arc((cx-rad+3,cy-rad+3,cx+rad-3,cy+rad-3),200,250,fill=2)       # dull highlight
ball=bytearray()
for tx in range(7):
    for ty in range(7):
        for y in range(8):
            lo=hi=0
            for x in range(8):c=im.getpixel((tx*8+x,ty*8+y));lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
            ball+=bytes([lo,hi])
assert len(ball)==49*16
Image.eval(im,lambda v:255-v*85).resize((224,224),Image.NEAREST).save(ROOT/'qa_ref'/'v39_black_ball.png')

# ---- dex number -> internal species (for "a random POKeMON not caught yet")
DEX=0x4102e
d2s={}
for sp in range(1,0xbf):
    n=R[DEX+sp-1]
    if 1<=n<=151 and n not in d2s:d2s[n]=sp
assert len(d2s)==151,len(d2s)
dex2sp=bytes(d2s[n] for n in range(1,152))

def ram_text(*parts):
    """('ram',addr) / plain strings / ('line'|'cont'|'para') -> TX bytes, ends with a prompt"""
    out=bytearray();inside=False
    for p in parts:
        if isinstance(p,tuple) and p[0]=='ram':
            if inside:out.append(0x50);inside=False
            out+=bytes([1,p[1]&255,p[1]>>8])
        else:
            if not inside:out.append(0);inside=True
            out+={'line':b'\x4f','cont':b'\x55','para':b'\x51'}.get(p,None) or enc(p)
    if not inside:out.append(0)
    out+=b'\x58';return bytes(out)
NAME=0xcd6d
T={
 't_used':ram_text('BLACK used BANE!'),
 't_party':ram_text(('ram',NAME),'line','joined your party.'),
 't_box':ram_text(('ram',NAME),'line','was sent to the PC.'),
 't_full':ram_text('The PC is full.','line','BANE failed.'),
 't_human':ram_text('The trainer became','line',('ram',NAME),'!'),
}
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())

SRC=f'''
; ================= BANE on a POKeMON (ExecutePlayerMove start, via F:7DD8 -> home 0x29) =================
bane_move:
    ld a,[$ccdc]
    cp {BANE}
    ret nz
    ld a,[$d057]
    and a
    ret z
    ld a,[$d014]
    cp {BLK}
    ret nz
    ld a,[$d45d]                 ; MIRAGE battle: no effect
    and a
    ret nz
    ld a,[$cfe5]
    ld hl,immune
.i: ld b,[hl]
    inc hl
    inc b
    jr z,.ok
    dec b
    cp b
    ret z
    jr .i
.ok:
    call room
    jr nc,.go
    ld hl,t_used
    call {PRINTTEXT:#x}
    ld hl,t_full
    jp {PRINTTEXT:#x}
.go:
    ld hl,t_used
    call {PRINTTEXT:#x}
    ld a,[$cfe5]
    call black_ball
    ld a,[$cfe5]
    ld [$cf91],a
    ld [$d11e],a
    ld a,[$cff3]
    ld [$d127],a
    call give                     ; party (battle data) or box
    ld a,[$d057]
    dec a
    jr nz,.trainer
    ld a,1                        ; wild: the battle ends like an escape
    ld [$d078],a
    ld hl,sp+6
    ld a,$cb                      ; F:7DCB = ret
    ld [hl+],a
    ld a,$7d
    ld [hl],a
    ret
.trainer:
    xor a                         ; the trainer's POKeMON is gone: counts as fainted (b = 0 at F:7DC9)
    ld [$cfe6],a
    ld [$cfe7],a
    ld hl,sp+6
    ld a,$c9
    ld [hl+],a
    ld a,$7d
    ld [hl],a
    ret

room:                             ; carry = party and box full
    ld a,[$d163]
    cp 6
    ccf
    ret nc
    ld a,[$da80]
    cp 20
    ccf
    ret

black_ball:                       ; a = species whose cry plays: black screen, cry, black ball in the enemy picture
    push af
    ld a,$ff
    ldh [$47],a
    ldh [$48],a
    ld c,20
    call {DELAY:#x}
    pop af
    call {PLAYCRY:#x}
    ld c,20
    call {DELAY:#x}
    ld de,ball
    ld hl,$9000
    ld bc,${BANK:02x}31
    call {COPYVID:#x}
    call {PALNORMAL:#x}
    ld c,40
    jp {DELAY:#x}

give:                             ; wcf91 = species, d127 = level: party (cc49=$10: no naming) else box
    ld a,[$d163]
    cp 6
    jr nc,.box
    ld a,$10
    ld [$cc49],a
    call {ADDPARTYMON:#x}
    xor a
    ld [$cc49],a
    call name_cf91                ; name -> cd6d (AddPartyMon used that buffer)
    ld a,[$d163]                  ; nickname = species name
    dec a
    ld hl,$d2b5
    ld bc,11
    call $3abb
    ld d,h
    ld e,l
    ld hl,{NAME:#x}
    ld bc,11
    call $00b5
    ld hl,t_party
    jp {PRINTTEXT:#x}
.box:
    call name_cf91
    farcall $6ad5,3               ; SendNewMonToBox (uses wEnemyMon)
    ld a,[$cf91]
    call set_owned
    call name_cf91
    ld hl,t_box
    jp {PRINTTEXT:#x}
name_cf91:
    ld a,[$cf91]
    ld [$d11e],a
    jp {GETMONNAME:#x}

set_owned:                        ; a = species: POKeDEX owned + seen
    ld [$d11e],a
    farcall $501a,$10             ; IndexToPokedex
    ld a,[$d11e]
    dec a
    ld c,a
    srl a
    srl a
    srl a
    ld e,a
    ld d,0
    ld a,c
    and 7
    ld b,a
    ld a,1
.s: dec b
    bit 7,b
    jr nz,.d
    add a
    jr .s
.d: ld b,a
    ld hl,$d2f7
    add hl,de
    ld a,[hl]
    or b
    ld [hl],a
    ld hl,$d30a
    add hl,de
    ld a,[hl]
    or b
    ld [hl],a
    ret

; ================= BANE on a human (trainer phase, F:5043 -> F:7FE8 stub) =================
bane_phase:
    farcall $4b00,$2e              ; v12 curse_trainer: the kill as before (BLUE hesitates)
    ld a,[$d014]
    cp {BLK}
    ret nz
    ld a,[$d031]
    cp {RIVAL1}
    ret z
    cp {RIVAL2}
    ret z
    call room
    ret c
    call rand_uncaught
    ld [$cf91],a
    ld [$d11e],a
    push af
    call {GETMONNAME:#x}
    pop af
    call black_ball
    ld hl,t_human
    call {PRINTTEXT:#x}
    ld a,[$cff3]
    and a
    jr nz,.lv
    ld a,5
.lv:ld [$d127],a
    ld a,[$cf91]
    ld [$d11e],a
    ld a,[$d163]
    cp 6
    jr nc,.box
    ld a,[$d057]                  ; out-of-battle style: random DVs, level-up moves
    push af
    xor a
    ld [$d057],a
    call give
    pop af
    ld [$d057],a
    ret
.box:
    ld a,[$cf91]
    ld [$cfd8],a                  ; wEnemyMonSpecies2
    farcall $6be7,$0f             ; LoadEnemyMonData
    ld a,[$cf91]
    ld [$d11e],a
    jp give

rand_uncaught:                    ; a = internal species of a random POKeMON not owned yet (any if all are)
    ld b,0
.l: push bc
    call {RANDOM:#x}
    pop bc
    cp 151
    jr nc,.n
    ld c,a
    srl a
    srl a
    srl a
    ld e,a
    ld d,0
    ld hl,$d2f7
    add hl,de
    ld a,c
    and 7
    ld d,a
    ld a,[hl]
.r: dec d
    bit 7,d
    jr nz,.t
    rrca
    jr .r
.t: bit 0,a
    jr nz,.n
    ld a,c
    jr .got
.n: dec b
    jr nz,.l
.any:
    push bc
    call {RANDOM:#x}
    pop bc
    cp 151
    jr nc,.any
.got:
    ld e,a
    ld d,0
    ld hl,dex2sp
    add hl,de
    ld a,[hl]
    ret

immune: db $b6,$b7,$1f,$7a,$79,$7f,$86,$ff
{TXT}
dex2sp: db {','.join(str(x) for x in dex2sp)}
ball: db {','.join(str(x) for x in ball)}
'''
code,L=asm(SRC,CODE)
rom.put(fo(BANK,CODE),code,'Bank 2F: v39 BANE (POKeMON in battle, humans in the trainer phase), black ball, give')
labels['bank2f']={k:hex(v) for k,v in L.items() if not k.startswith(('t_','dex2sp','ball','immune'))}

# ---- hooks
# F:5726 "ld a,[wPlayerSelectedMove]" -> F:7DD8: call home 0x29 (far bane_move) / ld a,[wPlayerSelectedMove] / ret
assert R[0x29:0x30]==bytes(7)
rom.put(0x29,bytes.fromhex('21'+le(L['bane_move'])+'06%02x18%02x'%(BANK,(0x09-0x30)&0xff)),'Home 0x29: far stub -> 2F bane_move')
assert R[fo(0xf,0x7dc9):fo(0xf,0x7dcc)]==bytes.fromhex('0600c9')
rom.put(fo(0xf,0x7dd8),bytes.fromhex('cd2900 fadccc c9'.replace(' ','')),'Bank F: BANE check before the player\'s move')
rom.hook(fo(0xf,0x5726),'cdd87d','ExecutePlayerMove: BANE on a POKeMON','fadccc',provides=('a','f','b','c','d','e','h','l'))
# trainer phase: F:7FE8 stub -> 2F bane_phase (which calls the v12 curse_trainer first)
ct=R[fo(0xf,0x7fe8):fo(0xf,0x7ff0)]
assert ct[:1]==b'\x21' and ct[3:5]==bytes([0x06,0x2e]),ct.hex()
L12CT=ct[1]|ct[2]<<8
assert L12CT==0x4b00,hex(L12CT)
rom.data(fo(0xf,0x7fe9),bytes.fromhex(le(L['bane_phase'])+'06%02x'%BANK),'Trainer-phase kill stub -> 2F bane_phase (kill, then BANE for BLACK)',ct[1:5].hex())
# trainer phase also for BLACK: phase2 (2D) reports BLACK (7F) as GHOST (1F)
PH=fo(0x2d,0x6111)
P39=0x7dc0
assert not any(R[fo(0x2d,P39):fo(0x2d,P39)+0x40])
pc,PL=asm(f'''
ph_species:
    ld a,[$d014]
    cp {BLK}
    ret nz
    ld a,$1f
    ret
step39:                          ; hunger_wrap's BLACK branch: CURSE -> BANE for BLACKs from v38, then v38's black_step
    ld a,[$d46c]
    and a
    ret z
    ld hl,$d164
    ld de,$d16b
.f: ld a,[hl+]
    cp $ff
    jr z,.done
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
    ld b,4
.m: ld a,[hl]
    cp {CURSE}
    jr nz,.nx
    ld [hl],{BANE}
    push hl
    ld de,21                     ; moves +21 = PP
    add hl,de
    ld [hl],10
    pop hl
.nx:inc hl
    dec b
    jr nz,.m
.done:
    jp {int(L38['bank2d']['black_step'],16):#x}
''',P39)
rom.put(fo(0x2d,P39),pc,'Bank 2D: v39 trainer phase for BLACK + CURSE->BANE migration')
rom.data(PH,bytes.fromhex('cd'+le(PL['ph_species'])),'phase2: BLACK counts as GHOST (trainer phase -> BANE)','fa14d0')
HW=fo(0x2d,0x44c9)
assert R[HW:HW+3]==bytes.fromhex('cd'+le(int(L38['bank2d']['black_step'],16)))
rom.data(HW+1,bytes.fromhex(le(PL['step39'])),'hunger_wrap BLACK branch -> step39 (CURSE->BANE, then black_step)',le(int(L38['bank2d']['black_step'],16)))
labels['bank2d']={k:hex(v) for k,v in PL.items()}
rom.finish('Creepy_Black_Mu_v39.gb','manifest_v39.json','CREEPY MU V39',extra=dict(labels=labels))
