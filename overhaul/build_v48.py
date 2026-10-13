# Creepy Black Mu v48: Black Tamer mechanics redux, part 2 (BLACK's new moves, inverted animations).
#   1. GHOST WALK (move AB): a two-turn move like FLY (typeless, 90 power, 95% accuracy, 15 PP). Turn 1: "<mon> faded into
#      dark!" with TELEPORT's animation in an inverted (negative) palette; turn 2: CUT's animation, inverted.
#   2. DAMNATION (move AC, 1 PP): HYPER BEAM's animation (charge + shot in one), then it works like CURSE on the target and
#      kills every other POKeMON of the trainer at the same time: the battle is won at once (BLUE replaces each line, v45).
#      AZHI is immune like to CURSE; in MIRAGE battles only the target is cursed. The MOON STONE blocks it (v44 list).
#   3. BLACK knows METAMORPHOSIS, CURSE, GHOST WALK, DAMNATION (v47's per-step fix puts them back with full PP).
#   4. Inverted animations: MACABRE = CRABHAMMER's animation, BLACK FLAME = FIRE BLAST's, both in a negative palette.
#   5. AZHI knows SKY ATTACK instead of FIRE BLAST (new AZHIs and the MIRAGE trainer's AZHI); a new AZHI's BLACK FLAME has
#      its 10 PP (v38's struct had 0).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V47_SHA='2aa24b869b140f5f4071365ac8308266ebd84d368c8bcb6cd351a7356297e1d3'
rom=Rom('Creepy_Black_Mu_v47.gb',V47_SHA)
r=rom.r;R=bytes(r)
L38=json.load(open('manifest_v38.json'))['labels']
L39={k:int(v,16) for k,v in json.load(open('manifest_v39.json'))['labels']['bank2f'].items()}
L44={k:int(v,16) for k,v in json.load(open('manifest_v44.json'))['labels']['bank2f'].items()}
L45={k:int(v,16) for k,v in json.load(open('manifest_v45.json'))['labels']['bank2f'].items()}
L47={k:int(v,16) for k,v in json.load(open('manifest_v47.json'))['labels']['bank2f'].items()}
DELAY,PREDEF,BANKSW=0x3773,0x3ec1,0x3618
CURSE,MBLADE,BFLAME,MACABRE,META,GWALK,DAMN=0xa5,0xa7,0xa8,0xa9,0xaa,0xab,0xac
AZHI=0xb7
SLASH,FIRE_BLAST,CRABHAMMER,THUNDERBOLT,CUT,HYPER_BEAM,TELEPORT,SKY_ATTACK,FLY,DIG=0xa3,0x7e,0x98,0x55,0x0f,0x3f,0x64,0x8f,0x13,0x5b
FLY_EFFECT,TYPELESS=0x2b,0x1b
FLASH=(0x2e,0x44c7)
labels={}
def tx(*parts,end=0x58):
    out=bytearray();inside=False
    for p in parts:
        if not inside:out.append(0);inside=True
        if p in ('line','cont','para'):out+={'line':b'\x4f','cont':b'\x55','para':b'\x51'}[p]
        else:assert shown(p)<=17,p;out+=enc(p)
    out+=bytes([end]);return bytes(out)

# ---- moves AB / AC: data (E:7D30 table, entry = id - A7) and names (after METAMORPHOSIS)
MT=fo(0xe,0x7d30)
def mrow(mv):return MT+(mv-0xa7)*6
assert R[mrow(META):mrow(META)+6]==bytes([META,0x55,0,0x1b,0xff,10])
assert not any(R[mrow(GWALK):mrow(DAMN)+6]) and R[fo(0xe,0x7d60)]==0xff
rom.data(mrow(GWALK),bytes([GWALK,FLY_EFFECT,90,TYPELESS,242,15]),'Move data AB = GHOST WALK (FLY effect, 90, typeless, 95%, 15 PP)',bytes(6))
rom.data(mrow(DAMN),bytes([DAMN,0x01,1,TYPELESS,0xff,1]),'Move data AC = DAMNATION (CURSE effect, 1 PP)',bytes(6))
NM=0xb0636+len('METAMORPHOSIS')+1
assert R[NM-1]==0x50 and not any(R[NM:NM+0x20])
names=enc('GHOST WALK')+b'\x50'+enc('DAMNATION')+b'\x50'
rom.data(NM,names,'Move names AB/AC: GHOST WALK, DAMNATION',bytes(len(names)))
# GHOST WALK / FLY: the effect handlers test the effect id, not the move (two-turn, invulnerable on turn 1)

BANK=0x2f;CODE=0x7800
assert not any(R[fo(BANK,CODE):fo(BANK,0x8000)])
T={'t_faded':tx('line','faded into dark!')}
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())
FORBID=list(R[fo(BANK,L44['forbid']):fo(BANK,L44['forbid'])+6])
assert FORBID==[CURSE,MBLADE,BFLAME,MACABRE,META,0xff],FORBID
FORBID=FORBID[:-1]+[DAMN,0xff]
code,L=asm(f'''
; ---- move animations (F:7F53 hook, the move id in wAnimationID): the overhaul moves get other moves' animations
anim48:
    ld a,[$d07c]
    ld b,a
    cp {MBLADE}
    jr c,.play
    ld hl,amap
.l: ld a,[hl+]
    cp $ff
    jr z,.def
    cp b
    ld a,[hl+]
    jr nz,.l
    jr .play
.def:
    ld a,{SLASH}
.play:
    push bc
    ld [$d07c],a                 ; = PlayMoveAnimation (F:6FED): Delay3, predef MoveAnimation
    call $3e22
    ld a,8
    call {PREDEF:#x}
    pop bc
    ld a,b                       ; MACABREBLADE / BLACK FLAME end with the black flash (as v10)
    cp {MBLADE}
    ret c
    cp {MACABRE}
    ret nc
    ld hl,{FLASH[1]:#x}
    ld b,{FLASH[0]:#x}
    jp {BANKSW:#x}
amap: db {MBLADE},{SLASH},{BFLAME},{FIRE_BLAST},{MACABRE},{CRABHAMMER},{META},{THUNDERBOLT},{GWALK},{CUT},{DAMN},{HYPER_BEAM},$ff

; ---- negative palette (MoveAnimation, after SetAnimationPalette): the attacker's move + this animation in invtab
inv48_on:
    ldh a,[$f3]
    and a
    ld a,[$cfd2]
    jr z,.p
    ld a,[$cfcc]
.p: ld c,a
    ld a,[$d07c]
    ld b,a
    ld hl,invtab
.l: ld a,[hl+]
    cp $ff
    ret z
    cp c
    ld a,[hl+]
    jr nz,.l
    cp b
    jr nz,.l
    ldh a,[$47]
    cpl
    ldh [$47],a
    ldh a,[$48]
    cpl
    ldh [$48],a
    ldh a,[$49]
    cpl
    ldh [$49],a
    ret
inv48_off:                       ; end of MoveAnimation: an inverted battle palette goes back to normal
    ldh a,[$47]
    cp $1b
    ret nz
    ld a,$e4
    ldh [$47],a
    ret
invtab: db {BFLAME},{FIRE_BLAST},{MACABRE},{CRABHAMMER},{GWALK},{CUT},{GWALK},{TELEPORT},$ff

; ---- before the player's move (home 0x29, was v39 bane_move): DAMNATION
pre48:
    ld a,[$ccdc]
    cp {DAMN}
    jp nz,{L39['bane_move']:#x}
    ld a,[$cfe5]
    cp {AZHI}
    ret z                        ; AZHI: like CURSE, no curse kill
    ld a,1
    ld [$cc39],a                 ; the curse kill on the target (as CURSE)
    ld a,[$d057]
    cp 2
    ret nz
    ld a,[$d45d]                 ; MIRAGE battle: only the target
    and a
    ret nz
    ld a,[$cfe5]
    push af
    ld a,[$cfe8]                 ; every other POKeMON of the trainer dies with it
    ld c,a
    ld b,0
.n: ld a,b
    cp c
    jr z,.nx
    ld a,[$d89c]
    cp b
    jr z,.done
    jr c,.done
    push bc
    ld a,b
    ld hl,$d8a5
    ld de,44
.m: and a
    jr z,.at
    add hl,de
    dec a
    jr .m
.at:ld a,[hl+]
    or [hl]
    jr z,.dead
    xor a
    ld [hl-],a
    ld [hl],a
    pop bc
    push bc
    ld hl,$d89d
    ld e,b
    ld d,0
    add hl,de
    ld a,[hl]
    ld [$cfe5],a
    call {L45['kill45']:#x}        ; BLUE: this line is replaced too (v45; it checks rival / curse flag itself)
.dead:
    pop bc
.nx:inc b
    jr .n
.done:
    pop af
    ld [$cfe5],a
    ret
forbid48: db {','.join(str(x) for x in FORBID)}
{TXT}''',CODE)
rom.put(fo(BANK,CODE),code,'Bank 2F: v48 animations (map, negative palette), DAMNATION, MOON STONE list')
labels['bank2f']={k:hex(v) for k,v in L.items()}

# animations: F:7F53 (v10 anim, called from F:5804 / F:689F with a = move id) -> ld [wAnimationID],a / tail far jump anim48
assert R[fo(0xf,0x7f53):fo(0xf,0x7f58)]==bytes.fromhex('fea7daed6f')
rom.code(fo(0xf,0x7f53),bytes.fromhex('ea7cd0 21'+le(L['anim48'])+'062f c31836'.replace(' ','')),'Move animation (both sides) -> 2F anim48 (map + negative palette)',
         R[fo(0xf,0x7f53):fo(0xf,0x7f5e)].hex(),reviewed='v10 anim routine replaced from its entry; its only jr target (7F68) is inside the old routine and now unreachable')
# negative palette: bank 1E stubs around MoveAnimation (4D65 call SetAnimationPalette, 4D98 call WaitForSoundToFinish)
B1E=0x7fd1
assert not any(R[fo(0x1e,B1E):fo(0x1e,0x8000)])
c1e,L1E=asm(f'''
inv_on:
    call $4e30
    ld hl,{L['inv48_on']:#x}
    ld b,{BANK:#x}
    jp {BANKSW:#x}
inv_off:
    call $3782
    ld hl,{L['inv48_off']:#x}
    ld b,{BANK:#x}
    jp {BANKSW:#x}
''',B1E)
rom.put(fo(0x1e,B1E),c1e,'Bank 1E: v48 negative-palette stubs')
rom.hook(fo(0x1e,0x4d65),'cd'+le(L1E['inv_on']),'MoveAnimation: negative palette for the marked moves','cd304e',provides=('a','f','b','c','h','l'))
rom.hook(fo(0x1e,0x4d98),'cd'+le(L1E['inv_off']),'MoveAnimation end: normal palette back','cd8237',provides=('a','f','b','c','h','l'),
         reviewed='4D98 is the start of the replaced call itself (jr z / pushed return address land on the call, not inside it); a is reset by the xor a that follows')

# home 0x29 (before the player's move): bane_move -> pre48 (DAMNATION, then bane_move)
assert R[0x29:0x30]==bytes.fromhex('21'+le(L39['bane_move'])+'062f18d9')
rom.data(0x2a,bytes.fromhex(le(L['pre48'])),'Home 0x29 stub -> pre48 (DAMNATION), then bane_move',le(L39['bane_move']))
# MOON STONE: sel44's forbidden list -> forbid48 (+ DAMNATION)
a=fo(BANK,L44['sel44']);s=R[a:a+0x60];i=s.find(bytes.fromhex('21'+le(L44['forbid'])));assert i>0
rom.data(a+i+1,bytes.fromhex(le(L['forbid48'])),'MOON STONE: DAMNATION blocked too',le(L44['forbid']))

# ---- GHOST WALK's charge text: ChargeMoveEffectText's TX_ASM (F:79C4) rewritten shorter (ret z per move), new default
CT=fo(0xf,0x79c4)
old=bytes.fromhex('fa3dcdfe0d21f0792821fe4c21f579281afe8221fa792813fe8f21ff79280cfe1321047a2805fe5b21097ac9')
assert R[CT:CT+len(old)]==old
FT=0x7e99
assert not any(R[fo(0xf,FT):fo(0xf,FT)+7])
rom.put(fo(0xf,FT),bytes([0x17])+bytes.fromhex(le(L['t_faded']))+bytes([BANK,0x50]),'Bank F: TX_FAR "faded into dark!" (GHOST WALK)')
new=bytes.fromhex('fa3dcd'+''.join('fe%02x21%sc8'%(mv,le(t)) for mv,t in ((0x0d,0x79f0),(0x4c,0x79f5),(0x82,0x79fa),(SKY_ATTACK,0x79ff),(FLY,0x7a04),(DIG,0x7a09)))+'21'+le(FT)+'c9')
assert len(new)<=len(old)
rom.code(CT,new+bytes(len(old)-len(new)),'Charge text: GHOST WALK "faded into dark!"',old,
         reviewed='hits at F:79CC-79E8 are the old routine\'s own jr z to its ret; F:455F/F:475E are operand bytes of "ld [$cd6a],a / call $4679" misread')

# ---- BLACK's moves: v47's table + the BLACK struct
SM=[META,CURSE,GWALK,DAMN];SP=[10,1,15,1]
BM=fo(BANK,L47['bmoves']);assert R[BM:BM+8]==bytes([META,CURSE,0,0,10,1,0,0])
rom.data(BM,bytes(SM+SP),'BLACK moves: METAMORPHOSIS, CURSE, GHOST WALK, DAMNATION',R[BM:BM+8])
SB=fo(0x2d,int(L38['bank2d']['s_black'],16))
rom.data(SB+8,bytes(SM),'BLACK struct: four moves',R[SB+8:SB+12])
rom.data(SB+29,bytes(SP),'BLACK struct: PP',R[SB+29:SB+33])

# ---- AZHI: SKY ATTACK instead of FIRE BLAST (ritual struct, MIRAGE trainer's AZHI)
SA=fo(0x2d,int(L38['bank2d']['s_azhi'],16))
assert R[SA+8:SA+12]==bytes([BFLAME,FLY,0x52,FIRE_BLAST])
rom.data(SA+11,bytes([SKY_ATTACK]),'AZHI struct: SKY ATTACK',bytes([FIRE_BLAST]))
assert R[SA+32]&0x3f==5
assert R[SA+29]==0
rom.data(SA+29,bytes([10]),'AZHI struct: BLACK FLAME PP 10 (v38 gave 0: its PP helper only knew the old move table)',b'\x00')
MZ=fo(0xe,0x7cc7)
assert R[MZ:MZ+4]==bytes([BFLAME,FLY,0x52,FIRE_BLAST])
rom.data(MZ+3,bytes([SKY_ATTACK]),'MIRAGE AZHI: SKY ATTACK',bytes([FIRE_BLAST]))
rom.finish('Creepy_Black_Mu_v48.gb','manifest_v48.json','CREEPY MU V48',extra=dict(labels=labels))
