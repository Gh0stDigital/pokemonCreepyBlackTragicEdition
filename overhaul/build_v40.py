# Creepy Black Mu v40: BANE on the map (part 3 of the BLACK TAMER mechanics).
#   Talking to an ordinary NPC as BLACK still makes them panic; the question is now "BANE them?" (was CURSE).
#   YES: the screen goes black, the cry of a random POKeMON the player hasn't caught plays, and when the light comes back
#   the NPC is a black POKe BALL lying on the ground ("Only a black ball remains..."). Talking to the ball picks it up:
#   the POKeMON (level 5 + 5 per badge, random DVs, level-up moves) joins the party, or the PC box when the party is full.
#   Trainers are unchanged: they never start a battle with BLACK by sight (v28), talking to them starts their battle.
#   Bookkeeping: the NPC goes into v28's kill list with bit 7 set on its sprite index (= BANEd: hidden, never a gravestone);
#   up to 2 balls wait on the ground (D722-D727: map, sprite, species; a third BANE collects the oldest one at once).
#   Sprite 47 (an unused duplicate "lying old man") is the black ball.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V39_SHA='1b3046fe67929504a5c561d8ecbc477754873dd6e5d5b0b4aebfc3cd833b6217'
rom=Rom('Creepy_Black_Mu_v39.gb',V39_SHA)
r=rom.r;R=bytes(r)
L39={k:int(v,16) for k,v in json.load(open('manifest_v39.json'))['labels']['bank2f'].items()}
L28={k:int(v,16) for k,v in json.load(open('manifest_v28.json'))['labels']['bank2d'].items()}
L30={k:int(v,16) for k,v in json.load(open('manifest_v30.json'))['labels']['bank2d'].items()}
KC2=int(json.load(open('manifest_v29.json'))['labels']['bank2d']['kill_chk2'],16)
PRINTTEXT,DELAY,PLAYCRY=0x3c94,0x3773,0x13ff
BLACKF,KILLS,PEND=0xd46c,0xd471,0xd722
BALLPIC=0x47
BANK=0x2f;CODE=0x5000
assert not any(R[fo(BANK,CODE):fo(BANK,0x8000)])
assert not any(R[PEND+0:PEND+0]) or True
labels={}

# ---- sprite 47 = black POKe BALL (still sprite, 4 tiles TL TR BL BR), from the item ball (4:5140)
o=fo(4,0x5140);orig=R[o:o+64]
def px(d,t,x,y):
    lo=d[t*16+y*2];hi=d[t*16+y*2+1];b=7-x;return ((hi>>b)&1)<<1|((lo>>b)&1)
grid=[[px(orig,(0 if X<8 else 1)+(0 if Y<8 else 2),X%8,Y%8) for X in range(16)] for Y in range(16)]
dark=[[(0 if c==0 else (1 if (Y==7 and 0<X<15 and grid[Y][X]!=3) else 3)) for X,c in enumerate(row)] for Y,row in enumerate(grid)]
sheet=bytearray()
for t in range(4):
    tx,ty=t&1,t>>1
    for y in range(8):
        lo=hi=0
        for x in range(8):c=dark[ty*8+y][tx*8+x];lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
        sheet+=bytes([lo,hi])
print('\n'.join(''.join(' .:#'[c] for c in row) for row in dark[:12]))
T5=fo(5,0x7b3d)+(BALLPIC-1)*4
assert R[T5:T5+4]==bytes.fromhex('40534004')

TXT={'t_ground':txt([["Only a black","ball remains..."]],0x58)}
TX=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in TXT.items())

SRC=f'''
; ================= DisplayTextID init (0:2950 -> here): BLACK talks to a black ball -> pick it up =================
npc_talk3:
    ld a,[{BLACKF}]
    and a
    jr z,.old
    ldh a,[$8c]
    and a
    jr z,.old
    ld b,a
    ld a,[$d4e1]
    cp b
    jr c,.old
    ld c,b
    call find_pending            ; hl = slot, carry = found
    jr nc,.old
    push hl
    farcall $708f,1              ; DisplayTextIDInit (as the old handler did first)
    pop hl
    call pickup
    ld hl,sp+4                   ; done: DisplayTextID waits for A to be released, then closes
    ld a,$0c
    ld [hl+],a
    ld a,$2a
    ld [hl],a
    ret
.old:                            ; v30 npc_talk2 (hunger messages, then v28's panic / BANE question), same stack
    ld a,$2d
    ld hl,{L30['npc_talk2']:#x}
    jp $0031

find_pending:                    ; c = sprite index on this map: carry + hl = its slot (map, sprite, species)
    ld hl,{PEND}
    ld b,2
.l: ld a,[$d35e]
    cp [hl]
    jr nz,.n
    inc hl
    ld a,[hl]
    dec hl
    cp c
    jr nz,.n
    push hl
    inc hl
    inc hl
    ld a,[hl]
    pop hl
    and a
    jr z,.n
    cp $bf
    jr nc,.n
    scf
    ret
.n: inc hl
    inc hl
    inc hl
    dec b
    jr nz,.l
    and a
    ret

pickup:                          ; hl = pending slot: the POKeMON joins (party or box), the slot is freed
    inc hl
    inc hl
    ld a,[hl]
    ld [hl],0
    dec hl
    ld [hl],0
    dec hl
    ld [hl],0
collect:                         ; a = species
    ld [$cf91],a
    ld [$d11e],a
    ld [$cfd8],a
    ld a,[$d356]                 ; level 5 + 5 per badge
    ld b,8
    ld c,5
.b: rrca
    jr nc,.nb
    push af
    ld a,c
    add 5
    ld c,a
    pop af
.nb:dec b
    jr nz,.b
    ld a,c
    ld [$d127],a
    ld a,[$d163]
    cp 6
    jr c,.give
    farcall $6be7,$0f            ; LoadEnemyMonData (box: SendNewMonToBox reads wEnemyMon)
    ld a,[$cf91]
    ld [$d11e],a
.give:
    jp {L39['give']:#x}

; ================= v28 YES action (2D) -> here: BANE on the map =================
bane_npc:
    call {L39['rand_uncaught']:#x}
    ld [$d457],a
    farcall $418c,$2e            ; the black screen of the battle CURSE
    ld a,[$d457]
    call {PLAYCRY:#x}
    ld c,30
    call {DELAY:#x}
    ld a,[$cf13]
    swap a
    ld l,a
    ld h,$c1
    ld [hl],{BALLPIC}            ; the NPC is a black POKe BALL now
    call add_bane
    call add_pending
    farcall $41a8,$2e            ; light back
    ld hl,t_ground
    jp {PRINTTEXT:#x}

add_bane:                        ; v28 kill list: (map, sprite | $80) = BANEd (hidden, no gravestone)
    ld hl,{KILLS}
    ld c,10
.f: inc hl
    ld a,[hl]
    and a
    jr z,.put
    inc hl
    dec c
    jr nz,.f
    ld hl,{KILLS+2}
    ld de,{KILLS}
    ld bc,18
    call $00b5
    ld hl,{KILLS+19}
.put:
    ld a,[$cf13]
    or $80
    ld [hl],a
    dec hl
    ld a,[$d35e]
    ld [hl],a
    ret

add_pending:                     ; (map, sprite, species) into a free slot; none free: the oldest is collected now
    ld hl,{PEND+2}
    ld a,[hl]
    and a
    jr z,.put0
    ld hl,{PEND+5}
    ld a,[hl]
    and a
    jr z,.put1
    ld a,[{PEND+2}]
    call collect
    ld hl,{PEND+3}
    ld de,{PEND}
    ld bc,3
    call $00b5
    xor a
    ld [{PEND+5}],a
    jr add_pending
.put0:
    ld hl,{PEND}
    jr .w
.put1:
    ld hl,{PEND+3}
.w: ld a,[$d35e]
    ld [hl+],a
    ld a,[$cf13]
    ld [hl+],a
    ld a,[$d457]
    ld [hl],a
    ret
{TX}
sheet: db {','.join(str(x) for x in sheet)}
'''
code,L=asm(SRC,CODE)
rom.put(fo(BANK,CODE),code,'Bank 2F: v40 BANE on the map (question YES, black ball, pickup)')
labels['bank2f']={k:hex(v) for k,v in L.items()}
rom.data(T5,bytes.fromhex(le(L['sheet'])+'40'+'%02x'%BANK),'Sprite 47 (unused) = black POKe BALL (bank 2F)','40534004')

# ---- 2D: map-load / per-frame checks that know BANEd NPCs and waiting balls
C2D=0x7e40
assert not any(R[fo(0x2d,C2D):fo(0x2d,0x7f00)])
c2,L2=asm(f'''
load40:                          ; map load (0:1688 stub), sprite offset e: a waiting ball keeps the ball picture
    ld a,e
    swap a
    ld c,a
    call pend2d
    jp nc,{KC2:#x}
    ld l,e
    ld h,$c1
    ld [hl],{BALLPIC}
    xor a
    ret
frame40:                         ; per frame (killed13), e = sprite offset: NZ = hide
    call {KC2:#x}
    ret nz
    ld a,e
    swap a
    ld c,a
    call pend2d
    jr c,.draw                   ; a waiting ball: draw it
    ld a,c
    or $80
    ld c,a
    ld a,[$d35e]
    ld b,a
    ld hl,{KILLS}
    ld d,10
.l: ld a,[hl+]
    cp b
    ld a,[hl+]
    jr nz,.nx
    cp c
    jr z,.hide
.nx:dec d
    jr nz,.l
.draw:
    xor a
    ret
.hide:
    or 1
    ret
pend2d:                          ; c = sprite index: carry = a ball waits for it on this map
    ld hl,{PEND}
    ld b,2
.l: ld a,[$d35e]
    cp [hl]
    jr nz,.n
    inc hl
    ld a,[hl]
    dec hl
    cp c
    jr nz,.n
    push hl
    inc hl
    inc hl
    ld a,[hl]
    pop hl
    and a
    jr z,.n
    scf
    ret
.n: inc hl
    inc hl
    inc hl
    dec b
    jr nz,.l
    and a
    ret
''',C2D)
rom.put(fo(0x2d,C2D),c2,'Bank 2D: v40 map-load / per-frame checks (BANEd NPCs hidden, waiting balls drawn)')
labels['bank2d']={k:hex(v) for k,v in L2.items()}
rom.data(0x1689,bytes.fromhex(le(L2['load40'])),'Map-load kill stub -> load40 (waiting balls), then kill_chk2',le(KC2))
rom.data(fo(0x2d,0x6216),bytes.fromhex(le(L2['frame40'])),'killed13: kill_chk2 -> frame40 (BANEd NPCs hidden)',le(KC2))

# ---- home: trampoline (a = bank, hl = address; the caller's stack is kept) and the talk entry
assert R[0x31:0x37]==bytes(6)
rom.put(0x31,bytes.fromhex('e0b8ea0020e9'),'Home 0x31: bank-switch trampoline (ldh [hLoadedROMBank],a / ld [$2000],a / jp hl)')
assert R[0x2950:0x2958]==bytes.fromhex('062d21'+le(L30['npc_talk2'])+'cd1836')
rom.code(0x2950,bytes.fromhex('06%02x21'%BANK+le(L['npc_talk3'])),'DisplayTextID init -> npc_talk3 (2F: black ball pickup, then npc_talk2)',
         '062d21'+le(L30['npc_talk2']),reviewed='operand bytes of the call setup; no jumps land inside 0x2950-0x2954 (checked in v28/v30)')

# ---- v28: the question and the YES action
ASK=0x5c00
old=txt([["They are shaking.","CURSE them?"]],0x57);new=txt([["They are shaking.","BANE them?"]],0x57)
assert R[fo(0x2d,ASK):fo(0x2d,ASK)+len(old)]==old
rom.data(fo(0x2d,ASK),new+bytes(len(old)-len(new)),'v28 question: "BANE them?"',old)
YA=0x4882;YE=0x48af
assert R[fo(0x2d,YE):fo(0x2d,YE)+2]==bytes.fromhex('f804')
stub=bytes.fromhex('21'+le(L['bane_npc'])+'06%02x cd1836'.replace(' ','')%BANK)+bytes([0x18,YE-(YA+10)])
rom.code(fo(0x2d,YA),stub,'v28 YES: BANE (black screen, cry of a random uncaught POKeMON, black ball) instead of the gravestone',
         R[fo(0x2d,YA):fo(0x2d,YA)+len(stub)].hex(),reviewed='replaced code is straight-line (no jumps into 2D:4882-488B)')
rom.finish('Creepy_Black_Mu_v40.gb','manifest_v40.json','CREEPY MU V40',extra=dict(labels=labels))
