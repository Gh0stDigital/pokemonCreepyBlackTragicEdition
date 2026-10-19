# Creepy Black Mu v87: BILL's cottage (position, sprite glitch, gone after the battle), the consort's sprite at home, LAVENDER music in the player's house,
#   the CERULEAN guard goes when BLUE is beaten.
#   1. app87 (bank 31, before app86): the player's house (BLACK, ritual done) and BILL's cottage (BLACK, scene stage) get the object list's pictures back before the sprite loader
#      runs on a redraw (the consort / BILL were drawn with another sprite's tiles after a text box).
#   2. BILL ends the walk directly in front of the player (6,2) facing down (was beside him, facing left); the engine's HideObject (toggle 62) runs when the battle starts, so he is gone
#      when the map comes back (lost: the scene shows him again).
#   3. As BLACK the player's house plays the LAVENDER theme too (music51: maps < $26); the consort's heal puts it back.
#   4. BLUE beaten as BLACK (1D s3_87) hides the guard in front of the CERULEAN CAVE (object 10, toggle 8); the CERULEAN CITY script (06:7100 cer87) does it for older saves.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V86_SHA='3247fc1665b96a56b3ec4f206ca86342b1cf76acaa7102a55800c9d7db341c92'
rom=Rom('Creepy_Black_Mu_v86.gb',V86_SHA)
R=bytes(rom.r)
def lh(a):return a.to_bytes(2,'little').hex()
BLACK,STAGE,SUB,RIT=0xd46c,0xd876,0xd877,0xd467
L60=json.load(open('manifest_v60.json'))['labels']['bank30']
L51=json.load(open('manifest_v51.json'))['labels']['bank30']
L67=json.load(open('manifest_v67.json'))['labels']['bank31']
# ---- 1. app87
A31=0x5b00
assert not any(R[fo(0x31,A31):fo(0x31,A31)+0x60])
app86=int(json.load(open('manifest_v86.json'))['labels']['bank31']['app86'],16) if 'labels' in json.load(open('manifest_v86.json')) else 0x5aa0
c31,L31=asm(f'''
app87:                           ; (from im67) the house / the cottage: the object list's pictures as at the map load
    ld a,[$d35e]
    cp $25
    jr z,.house
    cp $58
    jr nz,.o
    ld a,[{BLACK:#x}]
    and a
    jr z,.o
    ld a,[{STAGE:#x}]
    cp 5
    jr nz,.o
    ld hl,lpic58
    ld b,3
    jr .go
.house:
    ld a,[{BLACK:#x}]
    and a
    jr z,.o
    ld a,[{RIT:#x}]
    cp 6
    jr c,.o
    ld hl,lpic25
    ld b,4
.go:ld de,$c110
.l: ld a,[hl+]
    ld [de],a
    ld a,e
    add 16
    ld e,a
    dec b
    jr nz,.l
.o: jp {app86:#x}
lpic25: db $33,$1d,$1b,$0d
lpic58: db 5,$0c,$0c
''',A31,{})
rom.put(fo(0x31,A31),c31,'Bank 31: v87 app87 (house / cottage pictures as at the map load)')
o=fo(0x31,int(L67['im67'],16));assert R[o+1:o+3]==app86.to_bytes(2,'little'),R[o:o+3].hex()
rom.data(o+1,bytes.fromhex(lh(L31['app87'])),'im67: call app86 -> app87',lh(app86))
# ---- 2. BILL
b60=int(L60['bill60'],16)
s=R[fo(0x30,b60):fo(0x30,b60)+0x130]
i=s.find(bytes.fromhex('11'+lh(int(L60['mv60'],16))+'cd7436'));assert i>0
A30=0x4540
assert not any(R[fo(0x30,A30):fo(0x30,A30)+0x40])
c30,L30=asm(f'''
mv87: db 0,0,$80,$80,$ff
bill87:                          ; the battle starts: BILL's object goes (HideObject, toggle 62), the SUB state as before
    ld a,3
    ld [{SUB:#x}],a
    ld a,$62
    ld [$cc4d],a
    ld a,$11
    call $3ec1
    ret
''',A30,{})
rom.put(fo(0x30,A30),c30,'Bank 30: v87 mv87 / bill87')
rom.data(fo(0x30,b60)+i+1,bytes.fromhex(lh(L30['mv87'])),'BILL walks down 2, left 2 (mv87)',lh(int(L60['mv60'],16)))
j=s.find(bytes.fromhex('3e08ea29c1'));assert j>0
rom.data(fo(0x30,b60)+j+1,b'\x00','BILL faces down (not left)',b'\x08')
k=s.find(bytes.fromhex('3e03ea77d8c9'));assert k>0
rom.code(fo(0x30,b60)+k,bytes([0xc3])+bytes.fromhex(lh(L30['bill87']))+bytes(3),'bill60 .s2 end: jp bill87 (HideObject at the battle start)','3e03ea77d8c9',reviewed='the stub repeats ld a,3 / ld [D877],a / ret')
# ---- 3. house music
m=fo(0x30,int(L51['music51'],16));assert R[m:m+6].hex()=='fa5ed34ffe25'
rom.data(m+5,b'\x26','music51: LAVENDER also in the player\'s house (maps < $26)',b'\x25')
# ---- 4. CERULEAN guard
A1D=0x7fa0
assert not any(R[fo(0x1d,A1D):fo(0x1d,A1D)+0x20])
s3_86=0x7f80
assert R[fo(0x1d,0x5f37):fo(0x1d,0x5f37)+2]==s3_86.to_bytes(2,'little')
c1d,L1d=asm(f'''
s3_87:
    ld a,[{BLACK:#x}]
    and a
    jr z,.o
    ld a,[$d057]
    cp $ff
    jr z,.o
    ld hl,$d5a7                  ; toggle 8 = the guard in front of the CERULEAN CAVE: hidden
    set 0,[hl]
.o: jp {s3_86:#x}
''',A1D,{})
rom.put(fo(0x1d,A1D),c1d,'Bank 1D: v87 s3_87 (BLUE beaten: the CERULEAN CAVE guard goes)')
rom.data(fo(0x1d,0x5f37),bytes.fromhex(lh(L1d['s3_87'])),"Champion's room script 3 -> s3_87",lh(s3_86))
A6=0x7100
assert not any(R[fo(6,A6):fo(6,A6)+0x30])
hh=fo(6,int.from_bytes(R[0x1ae+6:0x1ae+8],'little'));assert R[hh+7:hh+9].hex()=='8054'
c6,L6=asm(f'''
cer87:                           ; CERULEAN CITY script: BLACK after BLUE (D876 >= 1): the cave guard is gone (also for saves from before v87)
    ld a,[{BLACK:#x}]
    and a
    jr z,.o
    ld a,[{STAGE:#x}]
    and a
    jr z,.o
    ld hl,$d5a7
    set 0,[hl]
    xor a
    ld [$c1a0],a
    ld a,$ff
    ld [$c2a4],a
    ld [$c2a5],a
.o: jp $5480
''',A6,{})
rom.put(fo(6,A6),c6,'Bank 6: v87 cer87 (CERULEAN CITY script wrapper)')
rom.data(hh+7,bytes.fromhex(lh(L6['cer87'])),'CERULEAN CITY map script -> cer87','8054')
rom.finish('Creepy_Black_Mu_v87.gb','manifest_v87.json','CREEPY MU V87',extra=dict(labels=dict(bank31={k:hex(v) for k,v in L31.items()})))
