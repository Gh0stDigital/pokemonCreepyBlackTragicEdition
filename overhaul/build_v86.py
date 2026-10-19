# Creepy Black Mu v86: BLUE on Route 22 gone for BLACK / shock / hero, no victory fanfare after League / BLUE / ending battles, Hall of Fame silent,
#   GHOST WALK's power grows with BLACK's level, (Hall of Fame AGATHA / BLUE sprite and the OAK LAB scientists: see below).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V85_SHA='e3b0587001f22fa070482c328299c1c9ea73bfadb798cc007c364d5b9dd34e5b'
rom=Rom('Creepy_Black_Mu_v85.gb',V85_SHA)
R=bytes(rom.r)
def lh(a):return a.to_bytes(2,'little').hex()
BLACK=0xd46c
A32=0x5200
assert not any(R[fo(0x32,A32):fo(0x32,A32)+0x400])
c32,L32=asm(f'''
vict86:                          ; (F:46C6 via rst 08) trainer-victory fanfare as v77's vict77, but none after the League / BLUE / OAK / BILL (class in the list)
    ld a,[$d12b]
    cp 4
    jr z,.n
    ld a,[$d35e]
    cp $69
    jr z,.n
    ld a,[$d031]
    ld hl,quiet
.l: cp [hl]
    jr z,.n
    inc hl
    ld b,[hl]
    inc b
    jr nz,.l
    ld a,$ff
    ld [$c0ee],a
    call $377a
    ld c,8
    ld a,[0xd468]
    call $23ce
    call $3e22
.n: ld hl,$4714
    ret
quiet: db $21,$2c,$2e,$2f,$2b,$1a,$ff
music86:                         ; (0:1249 via rst 08) music77, then the HALL OF FAME is silent for BLACK
    farcall {int(json.load(open('manifest_v77.json'))['labels']['bank30']['music77'],16):#x},$30
    ld a,[$d35e]
    cp $76
    ret nz
    ld a,[{BLACK:#x}]
    and a
    ret z
    ld a,$ff
    ld [$d35b],a
    ret
gpow86:                          ; (F:5784) the original move-data far call, then GHOST WALK (AB) gets power 20 + level * 1.5 (cap 250)
    ld hl,$4000
    ld de,$ccdc
    ld b,$1c
    call $3618
    ld a,[$cfd2]
    cp $ab
    ret nz
    ld a,[$d022]
    ld c,a
    srl a
    add c
    add 20
    jr nc,.o
    ld a,250
.o: ld [$cfd4],a
    ret
''',A32,{})
rom.put(fo(0x32,A32),c32,'Bank 32: v86 vict86 / music86 / gpow86 / gate86')
J=lambda n:bytes.fromhex(lh(L32[n]))
# 1. victory fanfare
o=fo(0xf,0x46c6);assert R[o:o+12].hex()=='78ea68d4'+'21'+lh(int(json.load(open('manifest_v77.json'))['labels']['bank30']['vict77'],16))+'0630cf0000'
rom.code(o+5,J('vict86')+b'\x06\x32','vict77 -> vict86 (no fanfare after League/BLUE/OAK/BILL battles)',R[o+5:o+9].hex(),reviewed='operand and bank of the far call')
# 2. Hall of Fame silent
o=0x1249;m77=int(json.load(open('manifest_v77.json'))['labels']['bank30']['music77'],16)
assert R[o:o+7].hex()=='21'+lh(m77)+'0630cf18'
rom.code(o+1,J('music86')+b'\x06\x32','Map music -> music86 (HALL OF FAME silent as BLACK)',lh(m77)+'0630',reviewed='operand and bank of the far-call stub')
# 3. GHOST WALK power
o=fo(0xf,0x5784);assert R[o:o+11].hex()=='2100401 1dccc061ccd1836'.replace(' ','')
rom.code(o,bytes.fromhex('21'+lh(L32['gpow86'])+'0632cf'+'00'*5),'Move data far call -> gpow86 (GHOST WALK power by level)',R[o:o+11].hex(),reviewed='the stub repeats the original far call')
# 4. Route 22 rival gate (bank 14): the v12 gate plus BLACK
G14=0x6b60
assert not any(R[fo(0x14,G14):fo(0x14,G14)+0x20])
cg,LG=asm(f'''
gate86:
    ld a,[$d463]
    ld b,a
    ld a,[{BLACK:#x}]
    or b
    jr z,.go
    ld hl,$d7eb
    res 7,[hl]
.go:jp $4eb2
''',G14,{})
rom.put(fo(0x14,G14),cg,'Bank 14: v86 Route 22 gate (shock / hero / BLACK: no rival)')
o=fo(0x14,0x4007);g=int.from_bytes(R[o:o+2],'little');assert R[fo(0x14,g):fo(0x14,g)+5].hex()=='fa63d4a728',R[fo(0x14,g):fo(0x14,g)+5].hex()
rom.code(o,bytes.fromhex(lh(LG['gate86'])),'Route 22 map script -> gate86',lh(g),reviewed='map header script pointer')

# 5. BLUE's sprite goes the moment he is beaten (1D: s3_86 before v58's s3_58) and AGATHA keeps facing the player (30: hof86)
L58=json.load(open('manifest_v58.json'))['labels']
STAGE=0xd876
A1D=0x7f80
assert not any(R[fo(0x1d,A1D):fo(0x1d,0x8000)])
s3_58=int(L58['bank1d']['s3_58'],16)
c1d,L1d=asm(f'''
s3_86:
    ld a,[{BLACK:#x}]
    and a
    jr z,.o
    ld a,[$d057]
    cp $ff
    jr z,.o
    xor a
    ld [$c110],a
    ld a,$ff
    ld [$c214],a
    ld [$c215],a
.o: jp {s3_58:#x}
''',A1D,{})
rom.put(fo(0x1d,A1D),c1d,"Bank 1D: v86 s3_86 (BLUE's object is hidden at once)")
o=fo(0x1d,0x5f37);assert R[o:o+2]==s3_58.to_bytes(2,'little')
rom.data(o,bytes.fromhex(lh(L1d['s3_86'])),"Champion's room script 3 -> s3_86",lh(s3_58))
hof58=int(L58['bank30']['hof58'],16)
A30=0x4500
assert not any(R[fo(0x30,A30):fo(0x30,A30)+0x20])
c30,L30=asm(f'''
hof86:
    call {hof58:#x}
    ld a,[{STAGE:#x}]
    cp 4
    ret nz
    ld a,4
    ld [$c119],a
    ret
''',A30,{})
rom.put(fo(0x30,A30),c30,'Bank 30: v86 hof86 (AGATHA faces up in the Hall of Fame)')
o=fo(0x16,0x7100);assert R[o:o+12].hex()=='fa6cd4a7ca9e6421006e0630'
rom.data(o+8,bytes.fromhex(lh(L30['hof86'])),'Hall of Fame script -> hof86',lh(hof58))

# 6. OAK'S LAB as BLACK: pictures given back before the sprite loader (the aide drew BLUE's tiles after a redraw), the aide's METAMORPHOSIS question
L67=json.load(open('manifest_v67.json'))['labels']['bank31']
L75=json.load(open('manifest_v75.json'))['labels']['bank31']
A31=0x5aa0
assert not any(R[fo(0x31,A31):fo(0x31,A31)+0x40])
c31,L31=asm(f'''
app86:                           ; (from im67, before app75) OAK'S LAB after the League: the object list's pictures as at the map load, so every redraw hands out the same slots
    ld a,[$d35e]
    cp $28
    jr nz,.o
    ld a,[{BLACK:#x}]
    and a
    jr z,.o
    ld a,[{STAGE:#x}]
    cp 4
    jr c,.o
    ld hl,lpic86
    ld de,$c110
    ld b,11
.l: ld a,[hl+]
    ld [de],a
    ld a,e
    add 16
    ld e,a
    dec b
    jr nz,.l
    ld hl,$d471                  ; the aide is a black ball (BANEd: map 28, sprite 10 | $80): his picture stays the ball's
    ld c,10
.k: ld a,[hl+]
    cp $28
    ld a,[hl+]
    jr nz,.nx
    cp $8a
    jr nz,.nx
    ld a,$47
    ld [$c1a0],a
    jr .o
.nx:dec c
    jr nz,.k
.o: jp {int(L75['app75'],16):#x}
lpic86: db 2,$3d,$3d,$3d,3,$41,$41,3,$d,$20,$20
''',A31,{})
rom.put(fo(0x31,A31),c31,'Bank 31: v86 app86 (OAK LAB pictures as at the map load)')
o=fo(0x31,int(L67['im67'],16));assert R[o+1:o+3]==int(L75['app75'],16).to_bytes(2,'little')
rom.data(o+1,bytes.fromhex(lh(L31['app86'])),'im67: call app75 -> app86',lh(int(L75['app75'],16)))

# 7. the lab's every-frame script (lab59 copy: the aide is left alone once he is a black ball) and the aide's question after his speech
BANE_NPC=int(json.load(open('manifest_v40.json'))['labels']['bank2f']['bane_npc'],16)
T_ASK=int(json.load(open('manifest_v47.json'))['labels']['bank2f']['t_ask'],16)
A32b=0x5400
assert not any(R[fo(0x32,A32b):fo(0x32,A32b)+0x200])
c32b,L32b=asm(f'''
lab86:                           ; OAK'S LAB, every frame (BLACK after the League): everybody gone but the aide (object 10), hiding in the lower-left corner
    ld a,[{BLACK:#x}]
    and a
    ret z
    ld a,[{STAGE:#x}]
    cp 4
    ret c
    ld c,1
.l: ld a,c
    cp 10
    jr z,.n
    swap a
    ld l,a
    ld h,$c1
    xor a
    ld [hl],a
    ld a,c
    swap a
    add 4
    ld l,a
    ld h,$c2
    ld a,$ff
    ld [hl+],a
    ld [hl],a
.n: inc c
    ld a,c
    cp 12
    jr nz,.l
    ld hl,$d471                  ; v28 kill list: (map, sprite | $80) = BANEd, then the aide is a black ball and stays one
    ld c,10
.k: ld a,[hl+]
    cp $28
    ld a,[hl+]
    jr nz,.nx
    cp $8a
    ret z
.nx:dec c
    jr nz,.k
    ld a,$20
    ld [$c1a0],a
    ld a,8                          ; facing left (into the corner)
    ld [$c1a9],a
    ld a,14
    ld [$c2a4],a
    ld a,4
    ld [$c2a5],a
    ld a,$ff
    ld [$c2a6],a
    ld a,[$cfc5]
    and a
    ret nz
    ld a,[$d361]
    ld b,a
    ld a,10
    sub b
    add a
    add a
    add a
    add a
    add $3c
    ld [$c1a4],a
    ld a,[$d362]
    ld b,a
    xor a
    sub b
    add a
    add a
    add a
    add a
    add $40
    ld [$c1a6],a
    ret
aide86:                          ; after the aide's speech: "They are shaking. METAMORPHOSIS?" (v28's question); YES = v40's map METAMORPHOSIS on object 10
    ld a,10
    ld [$cf13],a
    ld hl,ask86
    call $3c94
    call $362e
    ld a,[$cc26]
    and a
    ret nz
    ld hl,{BANE_NPC:#x}
    ld b,$2f
    jp $3618
ask86: db $17,{T_ASK&255},{T_ASK>>8},$2f,$50
''',A32b,{})
rom.put(fo(0x32,A32b),c32b,'Bank 32: v86 lab86 / aide86')
# lab_s (7:7F70): ld hl,lab59 -> lab86 (bank 32)
o=fo(7,0x7f70);assert R[o:o+5].hex()=='2100780630'
rom.data(o+1,bytes.fromhex(lh(L32b['lab86']))+b'\x06\x32','lab_s: lab59 -> lab86','00780630')
# the chooser's end (7:7F8D c3 04 25) -> ext86 in bank 7 free space
E7=0x7fe0
assert not any(R[fo(7,E7):fo(7,0x8000)])
o=fo(7,0x7f9d);assert R[o-3:o+3].hex()=='ea76d8c30425',R[o-3:o+3].hex()
c7b,L7b=asm(f'''
ext86:
    ld hl,{L32b['aide86']:#x}
    ld b,$32
    call $3618
    jp $2504
''',E7,{})
rom.put(fo(7,E7),c7b,'Bank 7: v86 ext86 (the aide asks about METAMORPHOSIS)')
rom.code(o,bytes([0xc3])+bytes.fromhex(lh(L7b['ext86'])),'aide text end: jp TextScriptEnd -> ext86','c30425',reviewed='the stub ends with the same jump')
rom.finish('Creepy_Black_Mu_v86.gb','manifest_v86.json','CREEPY MU V86')
