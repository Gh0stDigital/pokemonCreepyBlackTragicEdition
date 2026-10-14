# Creepy Black Mu v63: the ten SHAMANESSES in the ten towns (GHOST route: from the moment GHOST is acquired).
#   One channeler stands in each of PALLET, VIRIDIAN, PEWTER, CERULEAN, VERMILION, CELADON, FUCHSIA, SAFFRON, LAVENDER and CINNABAR and
#   tells one part of the lore (SHAMANESS 1-10). After you talked to her she is gone the next time the map is loaded.
#   - The sprite is appended to the map's sprites at every InitMapSprites (a marker byte in the text table of the new slot keeps a
#     redraw from adding her twice). SAFFRON already has all 15 slots: she takes the place of its last guard (same tile).
#   - Her talk goes through DisplayTextID's chain (2F:502E); she is found by slot, marker and being next to the player (the
#     first sign's text id equals her slot number). Talked flags: D840 / D841 (unused saved event bytes).
#   - Sprite sets: picture 19 replaces one unused entry in the sets of LAVENDER, VERMILION, CELADON, SAFFRON, FUCHSIA; PEWTER and
#     CERULEAN (set 2 is shared with routes that use every entry) get their own set 13 (copy of set 2 with 19 for the HIKER).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V62_SHA='4a541de8de294626f6fb6605286fb99e9f5d9da38a054407ea612c8f98698128'
rom=Rom('Creepy_Black_Mu_v62.gb',V62_SHA)
r=rom.r;R=bytes(r)
B31=0x31;CODE=0x5000;TXT=0x5800
assert not any(R[fo(B31,CODE):fo(B31,CODE+0x1000)])

def wrap(s,w=17):
    out=[];cur=''
    for word in s.split():
        if cur and len(cur)+1+len(word)>w:out.append(cur);cur=word
        else:cur=(cur+' '+word) if cur else word
    out.append(cur);return out
LORE=[("The Ancient Clan","Long before Kanto had a name, a clan lived upon these lands. They were said to hear voices from beyond the living world."),
("The God of the Abyss","Our ancestors worshipped a god who dwelled beyond the living world. They called it the God of the Abyss. It was said to hold dominion over the souls of the dead."),
("The Division","The old clan divided over the Abyss. Some wished to seal it away. Others believed it held the secret to eternal life."),
("The Four Warriors","Four warriors once stood against the darkness. Only one name survived the ages. Even that name... has been forgotten."),
("The Eight Dragons","Eight dragons were said to guard the boundaries of this land. Our ancestors built shrines where each had fallen."),
("The Forbidden Art","Our clan once knew how to call a soul back from the Abyss. But the bodies they returned to... were not always human."),
("The Sacred Grounds","The eight sacred grounds still remain. People gather there to test their strength now. How strange that no one remembers why."),
("The Forgotten Ritual","There is an ancient rite to unite the living with the dead. Only those with the sacred conditions of the chosen are meant to survive such a ritual."),
("The Lavender Cult","Long ago, outsiders came from distant lands and conquered our ancestors' homeland. They feared the clan's strange arts and declared their ancient traditions forbidden. Many of that cult's descendants are said to have settled in Lavender Town."),
("The Forgotten God","Those who practiced the old ways were hunted and shunned. Many abandoned their beliefs to survive. Others fled into hiding, preserving their sacred rites in secret and continued to worship the old god.")]
def lore_text(n,title,body):
    lines=wrap(body);paras=[['SHAMANESS %d:'%(n+1)]+wrap(title)]
    for i in range(0,len(lines),4):paras.append(lines[i:i+4])
    return bytes(txt(paras,0x58,17))
tx=bytearray();TA=[]
for n,(t,b) in enumerate(LORE):
    TA.append(TXT+len(tx));tx+=lore_text(n,t,b)
assert TXT+len(tx)<0x6000
rom.put(fo(B31,TXT),bytes(tx),'Bank 31: v63 the ten SHAMANESS speeches')

# (map, step y, step x, text index): the entry also gets the flag byte (D840 / D841) and mask
TOWNS=[(0x00,7,14,0),(0x01,12,28,1),(0x02,10,12,2),(0x03,20,18,3),(0x05,14,12,4),(0x06,11,24,5),(0x07,9,10,6),(0x0a,22,19,7),(0x04,6,12,8),(0x08,4,14,9)]
tab=''
for m,y,x,i in TOWNS:
    tab+=f'    db {m},{y+4},{x+4},{0x40+i//8},{1<<(i%8)},{i}\n'
SRC=f'''
app63:                           ; (from InitMapSprites) append the shamaness of this town
    ld a,[$d451]
    and a
    ret z
    ld a,[$d35e]
    ld c,a
    ld hl,tab63
.f: ld a,[hl]
    cp $ff
    ret z
    cp c
    jr z,.found
    ld de,6
    add hl,de
    jr .f
.found:
    push hl
    inc hl
    inc hl
    inc hl
    ld a,[hl+]
    ld e,a
    ld d,$d8
    ld a,[hl]
    ld b,a
    ld a,[de]
    and b
    pop hl
    ret nz                       ; she has been talked to: gone
    ld a,[$d4e1]
    ld e,a
    and a
    jr z,.add
    dec a
    add a
    inc a
    ld c,a
    ld b,0
    push hl
    ld hl,$d4e4
    add hl,bc
    ld a,[hl]
    pop hl
    cp $3f
    ret z                        ; marker: already added (redraw)
.add:
    ld a,e
    cp 15
    jr z,.slot                   ; all slots used: take the last one
    inc a
    ld [$d4e1],a
.slot:
    ld b,a
    swap a
    ld e,a
    ld d,$c1
    ld a,$19
    ld [de],a
    inc d
    ld a,e
    add 4
    ld e,a
    inc hl
    ld a,[hl+]
    ld [de],a
    inc e
    ld a,[hl]
    ld [de],a
    inc e
    ld a,$ff
    ld [de],a
    ld a,b
    dec a
    add a
    ld e,a
    ld d,0
    ld hl,$d4e4
    add hl,de
    ld a,$d0
    ld [hl+],a
    ld [hl],$3f
    ld hl,$d504
    add hl,de
    xor a
    ld [hl+],a
    ld [hl],a
    ret

wrap63:                          ; 2F:502E: DisplayTextID chain; her talk, else on to the old code (v28 NPC talk)
    ldh a,[$8c]
    and a
    jp z,.orig
    ld b,a
    ld a,[$d4e1]
    cp b
    jp nz,.orig
    ld a,b
    dec a
    add a
    inc a
    ld e,a
    ld d,0
    ld hl,$d4e4
    add hl,de
    ld a,[hl]
    cp $3f
    jp nz,.orig
    ld a,b
    swap a
    add 4
    ld l,a
    ld h,$c2
    ld a,[$d361]
    add 4
    ld d,a
    ld a,[$d362]
    add 4
    ld e,a
    ld a,[hl+]
    sub d
    jr nc,.a1
    cpl
    inc a
.a1:ld c,a
    ld a,[hl]
    sub e
    jr nc,.a2
    cpl
    inc a
.a2:add c
    cp 1
    jp nz,.orig                  ; the sign that shares her number
    ld a,b
    ld [$cf13],a
    farcall $708f,1
    farcall $70c0,4              ; she turns to the player
    ld a,[$d35e]
    ld c,a
    ld hl,tab63
.g: ld a,[hl]
    cp c
    jr z,.got
    ld de,6
    add hl,de
    jr .g
.got:
    push hl
    ld de,5
    add hl,de
    ld a,[hl]
    add a
    ld e,a
    ld d,0
    ld hl,tpt63
    add hl,de
    ld a,[hl+]
    ld h,[hl]
    ld l,a
    call $3c94
    pop hl
    inc hl
    inc hl
    inc hl
    ld a,[hl+]
    ld e,a
    ld d,$d8
    ld a,[de]
    ld b,[hl]
    or b
    ld [de],a                    ; talked: gone the next time the map is loaded
    ld hl,sp+4
    ld a,$0c
    ld [hl+],a
    ld a,$2a
    ld [hl],a
    ret
.orig:
    ld a,$2d
    ld hl,$5f19
    jp $0031

tab63:
{tab}    db $ff
tpt63: dw {','.join(hex(a) for a in TA)}
'''
code,L=asm(SRC,CODE,{})
assert CODE+len(code)<TXT,hex(CODE+len(code))
rom.put(fo(B31,CODE),code,'Bank 31: v63 app63 (append the shamaness), wrap63 (her talk)')

# ---- bank 5 (sprite loader): InitMapSprites entry stub + set lookup stub + set 13 (PEWTER / CERULEAN)
S5A,S5B,SET13=0x7fd0,0x7fe0,0x7f79
for a,n in ((S5A,0x30),(SET13,11)):assert not any(R[fo(5,a):fo(5,a)+n]),hex(a)
c5,L5=asm(f'''
im63:
    ld hl,{L['app63']:#x}
    ld b,{B31}
    call $3618
    jp $7fb0
set63:                           ; replaces ld de,$7ab9 / add e / ld e,a / jr nc / inc d: PEWTER and CERULEAN use set 13
    ld de,$7ab9
    add e
    ld e,a
    jr nc,.a
    inc d
.a: ld a,[$d35e]
    cp 2
    jr z,.n
    cp 3
    ret nz
.n: ld de,{SET13:#x}
    ret
''',S5A)
assert S5A+len(c5)<=0x8000,hex(S5A+len(c5))
rom.put(fo(5,S5A),c5,'Bank 5: v63 InitMapSprites stub and sprite-set lookup stub')
s2=bytes(R[fo(5,0x7ab9+11):fo(5,0x7ab9+22)]);assert s2.hex()=='0418 0c0e 0502 3106 073d49'.replace(' ','')
s13=bytes(0x19 if b==0x0e else b for b in s2)
rom.put(fo(5,SET13),s13,'Bank 5: v63 sprite set 13 (set 2 with the CHANNELER for the HIKER)')
rom.hook(fo(5,0x785b),'c3'+le(L5['im63']),'InitMapSprites: entry -> v63 stub (append the shamaness)','c3b07f',
         reviewed='a jp replaced by a jp; the stub calls the bank-31 routine (no registers needed by InitMapSprites) and continues at the old target')
rom.hook(fo(5,0x79ac),'cd'+le(L5['set63'])+'0000000000','InitOutsideMapSprites: set address lookup -> set63','11b97a835f3001'+'14',provides=('d','e'),
         reviewed='the stub redoes the replaced code (de = 7AB9 + a) and may point de at set 13; no jump lands inside 79AD-79B3')
# sets: the CHANNELER replaces one unused picture
def setpic(idx,old):
    o=fo(5,0x7ab9)+(idx-1)*11
    k=list(R[o:o+11]).index(old)
    rom.data(o+k,bytes([0x19]),f'sprite set {idx}: picture {old:02X} -> 19 (CHANNELER)',bytes([old]))
for idx,old in ((3,0x0e),(4,0x0c),(5,0x35),(7,0x07),(10,0x09)):setpic(idx,old)
# maps 2 and 3 use set 13
t=fo(5,0x7a64);assert R[t+2]==2 and R[t+3]==2
rom.data(t+2,bytes([13,13]),'MapSpriteSets: PEWTER / CERULEAN -> set 13',bytes([2,2]))

# ---- DisplayTextID chain: 2F:502E  ld a,2d / ld hl,5f19 / jp 0031
o=fo(0x2f,0x502e);assert R[o:o+8].hex()=='3e2d21195fc33100'
rom.hook(o,'3e31'+'21'+le(L['wrap63'])+'c33100','DisplayTextID chain: -> v63 wrap63 (the shamaness talks)','3e2d21195fc33100',
         reviewed='same call shape as before (ld a,bank / ld hl,routine / jp 0031); wrap63 falls back to the old target')
# BLACK's NPC takeover (v28) leaves channelers alone (the first sign shares the shamaness's slot number)
o=fo(0x2d,0x7e1b);assert R[o:o+2].hex()=='ff00'
rom.data(o,bytes([0x19,0xff]),'v28 exempt_pics: + 19 (CHANNELER)','ff00')
rom.finish('Creepy_Black_Mu_v63.gb','manifest_v63.json','CREEPY MU V63',extra=dict(labels=dict(bank31={k:hex(v) for k,v in L.items()})))
