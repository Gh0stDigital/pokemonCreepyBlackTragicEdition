# Creepy Black Mu v46: seven changes.
#   1. AGATHA no longer says the mark on the shell is drawn by her people: she talks about the energy in it.
#   2. BLACK leading at battle start is simply there: the trainer picture (= BLACK) does not slide away, no "Go! BLACK!",
#      no send-out animation, no cry; the HUD appears and the battle starts. (Switching in later works as before.)
#   3. BANE in battle: the black POKe BALL is the POKe BALL of the throw animation, fully black, lying where the POKeMON was.
#   4. BANE on the map: the ball lying there is the item POKe BALL sprite, fully black (still its own sprite 47).
#   5. GHOST consuming the MIRAGE grows to Lv100 at once ("GHOST grew to level 100!").
#   6. CONSUME: taking a move is optional - B at "Take which move?" (or giving up in LearnMove) consumes without a move.
#   7. POKeMON LEAGUE gates as BLACK: no badge checks (Route 22 gate, Route 23); the guards are too scared to stop BLACK.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V45_SHA='fcdc320b406621314689ea57c2966ec12db3789c2644caab8cbb58aadab9df07'
rom=Rom('Creepy_Black_Mu_v45.gb',V45_SHA)
r=rom.r;R=bytes(r)
PRINTTEXT,ADDNTIMES,CALCSTATS=0x3c94,0x3abb,0x396a
GHOST=0x1f
START46=0xd45a
labels={}
def px(d,t,x,y):
    lo=d[t*16+y*2];hi=d[t*16+y*2+1];b=7-x;return ((hi>>b)&1)<<1|((lo>>b)&1)

# ---- 1. AGATHA's shell text (2E:722F, inside the consort text): same length, padded with spaces
A1=0xbb22f
old=enc('See the mark on')+b'\x4f'+enc('it? My people')+b'\x55'+enc('drew it for')+b'\x51'+enc('devotion to the')+b'\x4f'+enc('one you love.')
assert R[A1:A1+len(old)]==old
lines=['Feel its energy?','It binds the','hearts of those','who truly love.']
new=enc(lines[0].ljust(17))+b'\x4f'+enc(lines[1].ljust(17))+b'\x55'+enc(lines[2].ljust(17))+b'\x51'+enc(lines[3])
new+=enc(' '*(len(old)-len(new)))
assert len(new)==len(old)
rom.data(A1,new,"AGATHA: the shell's energy binds those who truly love (no 'my people drew it')",old)

BANK=0x2f;CODE=0x7400
assert not any(R[fo(BANK,CODE):fo(BANK,CODE+0x400)])
def ram_text(*parts):
    out=bytearray();inside=False
    for p in parts:
        if not inside:out.append(0);inside=True
        if p in ('line','cont','para'):out+={'line':b'\x4f','cont':b'\x55','para':b'\x51'}[p]
        else:assert shown(p)<=17,p;out+=enc(p)
    return bytes(out)
T={'t_consume':ram_text('GHOST consumed','line','the MIRAGE!','para','GHOST grew to','line','level 100!')+b'\x57'}
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())
code,L=asm(f'''
; ---- 2. battle start (F:41D4 -> F:7FB8 -> here): hl = $C405 for the slide; BLACK leading: no slide (return to 41DC)
pre46:
    ld hl,$c405
    xor a
    ld [{START46:#x}],a
    ld a,[$cf91]
    cp $7f
    ret nz
    ld a,1
    ld [{START46:#x}],a
    ld hl,sp+4
    ld a,$dc
    ld [hl+],a
    ld [hl],$41
    ret
; SendOutMon's message far call (F:4CBC) -> here. First send-out of a BLACK lead: no message, the HUD and battle setup
; as SendOutMon does them, then back at F:4D1F (no send-out animation, no cry).
msg46:
    ld a,[{START46:#x}]
    and a
    jr nz,.black
    ld hl,$4e59
    ld b,$16
    jp $3618
.black:
    xor a
    ld [{START46:#x}],a
    ld hl,$cfe6
    ld a,[hl+]
    or [hl]
    jr z,.p
    farcall $4e17,$0f
.p: farcall $4d8b,$0f
    ld a,4
    call $3ec1
    xor a
    ldh [$e1],a
    ld hl,$cc2d
    ld [hl+],a
    ld [hl],a
    ld [$cc5b],a
    ld [$d05b],a
    ld [$cfd2],a
    ld hl,$ccf1
    ld [hl+],a
    ld [hl],a
    ld hl,$d060
    ld [hl+],a
    ld [hl+],a
    ld [hl+],a
    ld [hl+],a
    ld [hl],a
    ld [$d06d],a
    ld [$ccee],a
    ld [$ccf7],a
    ld b,1
    call $3e43
    ld hl,$d067
    res 5,[hl]
    ld a,1
    ldh [$f3],a
    ld a,[$d057]                 ; draw BLACK's picture at once (AnimateSendingOutMon's out-of-battle path, like YOU)
    push af
    xor a
    ld [$d057],a
    ld hl,$c480
    ld a,2
    call $3ec1
    pop af
    ld [$d057],a
    ld hl,sp+4
    ld a,$1f
    ld [hl+],a
    ld [hl],$4d
    ret

; ---- 5. GHOST consumed the MIRAGE (2D:45FA -> 2D stub -> here): GHOST becomes Lv100 (experience, stats, full HP)
lv100:
    ld hl,$d164
    ld c,0
.f: ld a,[hl+]
    cp $ff
    ret z
    cp {GHOST}
    jr z,.got
    inc c
    jr .f
.got:
    ld a,c
    ld hl,$d16b
    ld bc,44
    call {ADDNTIMES:#x}
    push hl
    ld a,{GHOST}
    ld [$d0b5],a
    call $155d
    ld d,100
    farcall $4f6a,$16
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
    ld bc,3
    add hl,bc
    ld [hl],100
    pop hl
    push hl
    ld bc,33
    add hl,bc
    ld [hl],100
    ld a,100
    ld [$d127],a
    ld a,{GHOST}
    ld [$d0b5],a
    call $155d
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

; ---- 6. CONSUME: pick_move, z = no move taken (B) -> consume without a move
pick46:
    call $54b3
    and a
    ret
{TXT}''',CODE)
rom.put(fo(BANK,CODE),code,'Bank 2F: v46 (BLACK out at battle start, GHOST Lv100, CONSUME without a move)')
labels['bank2f']={k:hex(v) for k,v in L.items()}

# 2: F:41D4 ld hl,$C405 / ld a,9 / call SlideTrainerPicOffScreen -> call 7FB8 (pre46 sets hl) / ld a,9 / call slide
assert R[fo(0xf,0x7fb8):fo(0xf,0x7fc0)]==bytes(8)
rom.put(fo(0xf,0x7fb8),bytes.fromhex('21'+le(L['pre46'])+'062fc31836'),'Bank F: v46 far stub -> pre46')
rom.code(fo(0xf,0x41d4),bytes.fromhex('cdb87f3e09cd0a49'),'StartBattle: slide trainer pic -> pre46 first (BLACK: no slide)','2105c43e09cd0a49')
rom.code(fo(0xf,0x4cbc),bytes.fromhex('21'+le(L['msg46'])+'062f'),'SendOutMon: message far call -> msg46 (BLACK lead: quiet send-out)','21594e0616')

# 3: the black ball in battle (2F:430C, 7x7 tiles, column by column) = the throw ball (1E anim tiles 06/07/16/17), black
ANIM=fo(0x1e,0x41fe)
def atile(t):return [[px(R[ANIM:],t,x,y) for x in range(8)] for y in range(8)]
q=[atile(t) for t in (6,7,0x16,0x17)]
tb=[q[0][y]+q[1][y] for y in range(8)]+[q[2][y]+q[3][y] for y in range(8)]
cols=[x for x in range(16) if any(tb[y][x] for y in range(16))];rows=[y for y in range(16) if any(tb[y])]
img=[[0]*56 for _ in range(56)]
ox=28-(cols[0]+cols[-1]+1)//2;oy=52-rows[-1]-1
for y in range(16):
    for x in range(16):
        if tb[y][x]:img[oy+y][ox+x]=3
ball=bytearray()
for tx in range(7):
    for ty in range(7):
        for y in range(8):
            lo=hi=0
            for x in range(8):c=img[ty*8+y][tx*8+x];lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
            ball+=bytes([lo,hi])
BALL=fo(0x2f,0x430c)
rom.data(BALL,bytes(ball),'BANE in battle: the throw POKe BALL, fully black (7x7 tiles)',R[BALL:BALL+784])

# 4: the ball on the map (sprite 47 sheet, 2F:5159) = the item POKe BALL sprite (4:5140), fully black
IB=fo(4,0x5140);orig=R[IB:IB+64]
sheet=bytearray()
for t in range(4):
    for y in range(8):
        lo=hi=0
        for x in range(8):c=3 if px(orig,t,x,y) else 0;lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
        sheet+=bytes([lo,hi])
SH=fo(0x2f,0x5159)
rom.data(SH,bytes(sheet),'BANE on the map: sprite 47 = the item POKe BALL, fully black',R[SH:SH+64])

# 5: 2D:45FA (ld a,5 / ldh [$8c],a / jp $294D: the consume text) -> 2D stub: lv100, then the text
S2D=0x7ec0
assert not any(R[fo(0x2d,S2D):fo(0x2d,S2D+0x10)])
c2d,L2D=asm(f'''
consume46:
    farcall {L['lv100']:#x},$2f
    ld a,5
    ldh [$8c],a
    jp $294d
''',S2D)
rom.put(fo(0x2d,S2D),c2d,'Bank 2D: v46 MIRAGE consumed -> GHOST Lv100, then the text')
rom.code(fo(0x2d,0x45fa),bytes.fromhex('c3'+le(S2D))+b'\x00'*4,'MIRAGE consumed: GHOST Lv100 first','3e05e08cc34d29',
         reviewed='2D:45FA is the .nom label (jumped to): the jp now sits at that very address, 45FD-4600 are never reached')
rom.data(fo(0x18,0x6ead),bytes.fromhex(le(L['t_consume']))+bytes([BANK]),'Consume text -> "GHOST consumed the MIRAGE! GHOST grew to level 100!"',
         R[fo(0x18,0x6ead):fo(0x18,0x6ead)+3])

# 6: CONSUME: call pick_move / and a / ret z -> call pick46 / jr z,.learned ; LearnMove given up: ret -> nop (eat anyway)
LEARNED=0x548b
rom.code(fo(BANK,0x542c),bytes.fromhex('cd'+le(L['pick46']))+bytes([0x28,(LEARNED-0x5431)&255]),'CONSUME: no move taken -> consume anyway','cdb354a7c8')
rom.code(fo(BANK,0x548a),b'\x00','CONSUME: LearnMove given up -> consume anyway','c9')

# 7: badge checks as BLACK. Route 23 (bank 14): script 0 skipped, guards' badge talk -> scared line.
def gate(bank,at,script_tbl,script0,talk):
    t=ram_text('The guard is','line','shaking...','para','G-go ahead...','line',"I won't stop you!")+b'\x57'
    c,LL=asm(f'''
scr:
    ld a,[$d46c]
    and a
    ret nz
    jp {script0:#x}
{talk}
scared: db {','.join(str(x) for x in t)}
''',at)
    return c,LL
c14,L14=gate(0x14,0x7f00,0x5213,0x5219,f'''
guard:                         ; 14:5346 (badge check of the Route 23 guards), a = badge number
    ld [$cd3d],a
    ld a,[$d46c]
    and a
    jp z,$5349
    ld hl,scared
    jp {PRINTTEXT:#x}
''')
assert not any(R[fo(0x14,0x7f00):fo(0x14,0x7f00+len(c14))])
rom.put(fo(0x14,0x7f00),c14,'Bank 14: v46 Route 23 as BLACK (no badge checks, scared guards)')
rom.data(fo(0x14,0x5213),bytes.fromhex(le(L14['scr'])),'Route 23 script 0 -> BLACK: skip the badge check','1952')
rom.code(fo(0x14,0x5346),bytes.fromhex('c3'+le(L14['guard'])),'Route 23 guards: BLACK -> scared line','ea3dcd')
c7,L7=gate(7,0x7f00,0x66ae,0x66b4,f'''
guard:                         ; Route 22 gate text 1 (TX_ASM)
    db 8
    ld a,[$d46c]
    and a
    jp z,$66f2
    ld hl,scared
    call {PRINTTEXT:#x}
    jp $2504
''')
assert not any(R[fo(7,0x7f00):fo(7,0x7f00+len(c7))])
rom.put(fo(7,0x7f00),c7,'Bank 7: v46 Route 22 gate as BLACK (no badge check, scared guard)')
rom.data(fo(7,0x66ae),bytes.fromhex(le(L7['scr'])),'Route 22 gate script 0 -> BLACK: skip the badge check','b466')
rom.data(fo(7,0x66ef),bytes.fromhex(le(L7['guard'])),'Route 22 gate text 1 -> BLACK: scared guard','f166')
labels['bank14']={k:hex(v) for k,v in L14.items()};labels['bank7']={k:hex(v) for k,v in L7.items()};labels['bank2d']={k:hex(v) for k,v in L2D.items()}
rom.finish('Creepy_Black_Mu_v46.gb','manifest_v46.json','CREEPY MU V46',extra=dict(labels=labels))
