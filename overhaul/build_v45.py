# Creepy Black Mu v45: BLUE replaces the POKeMON the player CURSEd.
#   Every time CURSE kills one of BLUE's POKeMON (any rival battle: RIVAL1 19, RIVAL2 2A, RIVAL3 2B), its whole evolution
#   line is gone from his later teams for good: a random POKeMON from the original 149 (no MEW / MEWTWO, none of the lines
#   BLUE uses in any of his teams, none already used as a replacement) takes that line's place in every later battle,
#   at the same level and at the evolution stage that level allows (level evolutions at their level, stones at Lv32,
#   trade evolutions at Lv36). CURSing a replacement replaces it again. The current battle is not changed.
#   Saved: D86A.. one byte per BLUE line (its replacement species, 0 = none) - event-flag bytes no code or trainer header
#   uses (NEW GAME clears them with the other event flags).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V44_SHA='e61d17f6783fd2ac33c4eed682d05d699a5a757687747e6ae1fe0ad2cc2a9ff6'
rom=Rom('Creepy_Black_Mu_v44.gb',V44_SHA)
r=rom.r;R=bytes(r)
RIVALS=(0x19,0x2a,0x2b)
RANDOM=0x3eb0
STONE_LV,TRADE_LV=32,36
EXCLUDE={0x1f,0x79,0x7a,0x7f,0x86,0xb6,0xb7}           # overhaul species: GHOST, stand-in, ?????, BLACK, RED, PRETA, AZHI
TBL=0xd86a

# ---- evolution data (EvosMovesPointerTable, E:70D1 in this ROM = vanilla 705C + 117)
EVT=0x70d1
def evos(s):
    a=R[fo(0xe,EVT)+2*(s-1)]|R[fo(0xe,EVT)+2*(s-1)+1]<<8;o=fo(0xe,a);out=[]
    while R[o]:
        t=R[o]
        if t==1:out.append((R[o+1],R[o+2]));o+=3
        elif t==2:out.append((STONE_LV,R[o+3]));o+=4
        elif t==3:out.append((TRADE_LV,R[o+2]));o+=3
        else:raise ValueError((hex(s),t))
    return out
DEX=R[0x4102e:0x4102e+190]                             # internal species -> dex number
assert DEX[0x99-1]==1 and DEX[0xb0-1]==4 and DEX[0x83-1]==150 and DEX[0x15-1]==151
species=[s for s in range(1,191) if 1<=DEX[s-1]<=151 and s not in EXCLUDE]
assert len(species)==151,len(species)
E={s:evos(s) for s in species}
pre={}
for s,l in E.items():
    for lv,t in l:pre[t]=s
def base(s):
    while s in pre:s=pre[s]
    return s
def path(s):                                          # (min level, species) from the line's base through s to its end
    up=[s]
    while up[0] in pre:up.insert(0,pre[up[0]])
    st=[(0,up[0])]
    for a,b in zip(up,up[1:]):st.append((dict((t,lv) for lv,t in E[a])[b],b))
    while E[st[-1][1]]:lv,t=E[st[-1][1]][0];st.append((lv,t))
    return st[:3]

# ---- BLUE's teams (TrainerDataPointers E:5D79, index class-1) -> his evolution lines
TDP=0x5d79
ptr=lambda c:R[fo(0xe,TDP+2*(c-1))]|R[fo(0xe,TDP+2*(c-1))+1]<<8
NPART={0x19:9,0x2a:15,0x2b:6}
blue=[]
for c in RIVALS:
    o=fo(0xe,ptr(c))
    for n in range(NPART[c]):
        if R[o]==0xff:
            o+=1
            while R[o]:blue.append(R[o+1]);o+=2
        else:
            o+=1
            while R[o]:blue.append(R[o]);o+=1
        o+=1
fams=[]
for s in blue:
    assert s in E,hex(s)
    if base(s) not in fams:fams.append(base(s))
NFAM=len(fams);print('BLUE lines',NFAM,[hex(x) for x in fams])
assert NFAM<=14                                         # D86A-D877 are free
cand=[s for s in species if DEX[s-1]<=149 and base(s) not in fams]
print('candidates',len(cand))
assert 0<len(cand)<256

base_tab=bytes(base(s) if s in E else 0 for s in range(256))
stage_tab=bytearray()
for s in range(256):
    st=path(s) if s in E else []
    rec=bytearray()
    for lv,t in st:rec+=bytes([lv,t])
    stage_tab+=rec.ljust(6,b'\xff')
assert len(stage_tab)==256*6

BANK=0x2f;CODE=0x6800
assert not any(R[fo(BANK,CODE):fo(BANK,CODE+0xc00)])
def db(b):return ','.join(str(x) for x in b)
code,L=asm(f'''
; z = the opponent is BLUE (RIVAL1 / RIVAL2 / RIVAL3)
rival:
    ld a,[$d059]
    sub $c8
    cp $19
    ret z
    cp $2a
    ret z
    cp $2b
    ret

; a = species -> a = its line's base species
base:
    ld e,a
    ld d,0
    ld hl,base_tab
    add hl,de
    ld a,[hl]
    ret

; a = species -> carry: a = index k of BLUE's line it belongs to (his own line, or the line it replaces)
fam_k:
    call base
    ld b,a
    ld hl,blue_fam
    ld c,0
.l: ld a,[hl+]
    cp $ff
    jr z,.tbl
    cp b
    jr z,.f
    inc c
    jr .l
.tbl:
    ld c,0
.t: ld a,c
    cp {NFAM}
    jr z,.no
    ld e,a
    ld d,0
    ld hl,{TBL:#x}
    add hl,de
    ld a,[hl]
    and a
    jr z,.n
    push bc
    call base
    pop bc
    cp b
    jr z,.f
.n: inc c
    jr .t
.no:and a
    ret
.f: ld a,c
    scf
    ret

; a = replacement species -> a = its stage for level [wCurEnemyLevel]
stage:
    ld l,a
    ld h,0
    add hl,hl
    ld d,h
    ld e,l
    add hl,hl
    add hl,de
    ld de,stage_tab
    add hl,de
    ld a,[$d127]
    ld c,a
    inc hl
    ld e,[hl]
    inc hl
    ld b,2
.s: ld a,[hl+]
    cp $ff
    jr z,.d
    ld d,a
    ld a,c
    cp d
    jr c,.d
    ld e,[hl]
    inc hl
    dec b
    jr nz,.s
.d: ld a,e
    ret

; ---- ReadTrainer (E:5CCF / E:5CE6, just before AddPartyMon): BLUE's killed lines -> their replacement
load45:
    call rival
    ret nz
    ld a,[$cf91]
    call fam_k
    ret nc
    ld e,a
    ld d,0
    ld hl,{TBL:#x}
    add hl,de
    ld a,[hl]
    and a
    ret z
    call stage
    ld [$cf91],a
    ret

; ---- FaintEnemyPokemon (F:7D20): CURSE killed one of BLUE's POKeMON -> roll its line's replacement
kill45:
    push de
    ld a,[$cc39]
    and a
    jr z,.out
    ld a,[$d057]
    cp 2
    jr nz,.out
    ld a,[$d05a]
    cp 3
    jr z,.out
    call rival
    jr nz,.out
    ld a,[$cfe5]
    ld [$d45a],a
    call fam_k
    jr nc,.out
    ld [$d459],a
    ld a,40
    ld [$d458],a
.roll:
    call {RANDOM:#x}
.m: cp {len(cand)}
    jr c,.ok
    sub {len(cand)}
    jr .m
.ok:ld e,a
    ld d,0
    ld hl,cand
    add hl,de
    ld a,[hl]
    ld [$d457],a
    call base
    ld b,a
    ld a,[$d45a]
    push bc
    call base
    pop bc
    cp b
    jr z,.again
    ld c,0
.v: ld a,c
    cp {NFAM}
    jr z,.store
    ld e,a
    ld d,0
    ld hl,{TBL:#x}
    add hl,de
    ld a,[hl]
    and a
    jr z,.vn
    push bc
    call base
    pop bc
    cp b
    jr z,.again
.vn:inc c
    jr .v
.store:
    ld a,[$d459]
    ld e,a
    ld d,0
    ld hl,{TBL:#x}
    add hl,de
    ld a,[$d457]
    ld [hl],a
    jr .out
.again:
    ld hl,$d458
    dec [hl]
    jr nz,.roll
.out:
    pop de
    ld hl,$41c2
    ld b,$2e
    jp $3618

blue_fam: db {db(fams)},255
cand: db {db(cand)}
base_tab: db {db(base_tab)}
stage_tab: db {db(stage_tab)}
''',CODE)
assert len(code)<0xc00
rom.put(fo(BANK,CODE),code,'Bank 2F: v45 BLUE replaces CURSEd POKeMON (tables + load/kill hooks)')

# bank E: stub before AddPartyMon in ReadTrainer
SE=0x7ee0
assert not any(R[fo(0xe,SE):fo(0xe,SE+0x10)])
stub=bytes.fromhex('e521'+le(L['load45'])+'062fcd1836e1c35b39')
rom.put(fo(0xe,SE),stub,'Bank E: v45 ReadTrainer stub (BLUE replacements, then AddPartyMon)')
for site in (0x5ccf,0x5ce6):
    assert R[fo(0xe,site)-1]==0xe5 and R[fo(0xe,site)+3]==0xe1
    rom.code(fo(0xe,site),'cd'+le(SE),'ReadTrainer: AddPartyMon -> v45 stub (%04X)'%site,'cd5b39')
# F:7D20: farcall 2E:41C2 -> kill45 (which far-jumps to 2E:41C2 itself)
rom.code(fo(0xf,0x7d20),bytes.fromhex('21'+le(L['kill45'])+'062f'),'FaintEnemyPokemon hook -> kill45 (BLUE replacement roll)','21c241062e')
labels={'bank2f':{k:hex(v) for k,v in L.items() if not k.startswith(('base_tab','stage_tab'))}}
rom.finish('Creepy_Black_Mu_v45.gb','manifest_v45.json','CREEPY MU V45',
           extra=dict(labels=labels,blue_fams=[hex(x) for x in fams],cand=[hex(x) for x in cand],tbl=hex(TBL)))
