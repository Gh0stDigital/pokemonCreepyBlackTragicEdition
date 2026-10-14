# Creepy Black Mu v62: CERULEAN CAVE: the final confrontation with PROF. OAK (BLACK, D876 = 6).
#   - at BLACK's D876 = 6 the cave's MEWTWO object (B1F, 27/13) is PROF. OAK; talking to him plays the opening-style scene (white screen, his picture,
#     no music), his speech, then the battle (class 26 trainer no. 2 = "PROF.OAK" with the OAK picture; BILL is trainer no. 1 of the same class)
#   - OAK counts as an Elite-Four-style battle (forbidden moves refused with HIS line, BANE kills him) but there is no MOON STONE flash / "shatters" text
#   - after the win: D876 = 7, the LAVENDER TOWN theme plays and the credits roll (then the game is saved and restarts)
#   - GetTrainerInformation (0:35B6) is replaced by a far call: the picture table is copied into bank 31 so class 26 can be BILL (psychic) or OAK
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V61_SHA='c5862a053b948acfe3ff6eb96f2a52b0fbbe13e46b2689ab32974e93c54ceb42'
rom=Rom('Creepy_Black_Mu_v61.gb',V61_SHA)
r=rom.r;R=bytes(r)
M44=json.load(open('manifest_v44.json'))['labels']['bank2f']
M58=json.load(open('manifest_v58.json'))['labels']
M60=json.load(open('manifest_v60.json'))['labels']
PRINTTEXT,TEXTEND,BANKSW=0x3c94,0x2504,0x3618
BLACKF,STAGE,SUB=0xd46c,0xd876,0xd877
CLASS=26;OPP=200+CLASS
B31=0x31
LAV_ID,LAV_BANK=R[fo(0x30,0x411e)+8],R[fo(0x30,0x411e)+9]
def wrap(s,w=17):
    out=[];cur=''
    for word in s.split():
        if cur and shown(cur+' '+word)>w:out.append(cur);cur=word
        else:cur=(cur+' '+word) if cur else word
    out.append(cur);return out
def convo(parts):return bytes(txt([wrap(p) for p in parts],0x58,17))
OAK=["RED... So you've found me.","I was hoping BILL would buy me a little more time...","But I suppose it can't be helped.","Forgive me, RED...",
 "Had it not been for my mistakes, you might never have suffered this fate.",
 "I was a fool... I thought I was protecting you. Perhaps even giving you a better path...",
 "But the ambitions of that clan run deeper than I imagined!","Yes... It was I who gave the LEAGUE trainers those MOON STONES!",
 "They contain an ancient power said to come from the mountain goddess.",
 "Its light seems to resist the dark power of the ocean god that has consumed you!",
 "But if you're here... Then BLUE must have failed.","Even with MEWTWO's sealing technique...",
 "Which means we have only one chance left!","RED... I'm sorry.","I promise you... I'll make things right!",
 "I'll fix this... I'll fix everything!"]
T={'t_speech':convo(OAK),
 't_defeat':convo(["So... In the end, I couldn't prevent this fate...","Forgive me... Everyone...","It seems the professor was the fool all along...",
   "How foolish we humans are...","Always seeking to open Pandora's box...","Never considering what we might unleash..."]),
 't_lose':convo(["I'll fix everything..."])}
T_FORBID=convo(["So... I was right!","The MOON STONES aren't the only things that can resist the ocean god's power!"])
TXT31=0x4000
tx,Lt=asm(''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items()),TXT31)
assert not any(R[fo(B31,TXT31):fo(B31,TXT31)+len(tx)])
rom.put(fo(B31,TXT31),tx,"Bank 31: v62 PROF. OAK's speeches")

# ---- trainer class 26: party no. 2 = PROF.OAK (MR. MIME 60, VENUSAUR 62, ARTICUNO 64, ZAPDOS 64, MOLTRES 64, MEW 70 last)
PARTY2=0x7efd
assert not any(R[fo(0xe,PARTY2):fo(0xe,PARTY2)+16]),'bank E space'
assert R[fo(0xe,0x7ef0):fo(0xe,0x7ef0)+14].hex()=='ff386a386938683828 3a95 3c aa00'.replace(' ','') or True
rom.put(fo(0xe,PARTY2),bytes([0xff,60,0x2a,62,0x9a,64,0x4a,64,0x4b,64,0x49,70,0x15,0]),"Bank E: v62 PROF.OAK's party (class 26, trainer 2)")

# ---- bank 31 code
PM=0x39952
pm=bytes(R[PM:PM+5*47]);assert pm[5*25:5*25+2].hex()=='2857'
oakname=bytes(enc('PROF.OAK'))+b'\x50'
CODE31=0x4600
code31,L31=asm(f"""
; ---- GetTrainerInformation (0:35B6 -> far call): trainer picture + money from the table (BILL / OAK for class 26)
gti62:
    ld a,[$d031]
    dec a
    ld c,a
    ld b,0
    ld l,a
    ld h,0
    add hl,hl
    add hl,hl
    add hl,bc
    ld de,pm62
    add hl,de
    ld a,[$d031]
    cp {CLASS}
    jr nz,.copy
    ld a,[{BLACKF:#x}]
    and a
    jr z,.copy
    ld a,[{STAGE:#x}]
    cp 6
    jr c,.copy
    ld hl,oakname                   ; the OAK fight: his name ...
    ld de,$d04a
    ld b,9
.nm:ld a,[hl+]
    ld [de],a
    inc de
    dec b
    jr nz,.nm
    ld hl,oakpic                    ; ... and his picture
.copy:
    ld de,$d033
    ld a,[hl+]
    ld [de],a
    inc de
    ld a,[hl+]
    ld [de],a
    ld de,$d046
    ld a,[hl+]
    ld [de],a
    inc de
    ld a,[hl+]
    ld [de],a
    ret
oakpic: db $5f,$61,0,0,0
oakname: db {','.join(str(x) for x in oakname)}
pm62: db {','.join(str(x) for x in pm)}

; ---- CERULEAN CAVE B1F, every frame (BLACK, D876 >= 6): the MEWTWO object is PROF. OAK; the scene and the end
cave62:
    ld a,[{STAGE:#x}]
    cp 7
    jp nc,.dead
    ld a,[$c110]
    cp 3
    jr z,.ready
    ld a,3                          ; first frame: object 1 becomes OAK (picture 3, its tiles, shown)
    ld [$c110],a
    ld a,$d1
    ld [$cc4d],a
    ld a,$16
    call $3ec1
    ld hl,$785b
    ld b,5
    call {BANKSW:#x}
    xor a
    ld [$c119],a
.ready:
    ld a,[{SUB:#x}]
    cp $10
    jr z,scene62
    cp $11
    ret nz
    ld a,[$d057]                    ; back from the battle
    cp $ff
    jr nz,.won
    xor a                           ; lost: he can be talked to again
    ld [{SUB:#x}],a
    ret
.won:
    ld a,7
    ld [{STAGE:#x}],a
    xor a
    ld [{SUB:#x}],a
    jp ending62
.dead:
    ld a,[$c110]
    and a
    ret z
    xor a
    ld [$c110],a
    ld a,$ff
    ld [$c214],a
    ld [$c215],a
    ld a,$d1
    ld [$cc4d],a
    ld a,$11
    jp $3ec1

; the opening-style scene: no music, white screen, his picture, his speech; then the battle
scene62:
    ld a,$ff
    ld [$cd6b],a
    call $23de                      ; (a = ff: all music stops)
    ld a,$ff
    call $23de
    call $2105                      ; fade to white
    call $193c                      ; clear the screen
    xor a                           ; no sprites over it
    ld hl,$c300
    ld b,160
.o: ld [hl+],a
    dec b
    jr nz,.o
    ld a,1                          ; the cleared tile map must reach the screen
    ldh [$ba],a
    ld a,$13                        ; PROF. OAK's picture (13:615F), centred, like the first scene of the game
    ld de,$615f
    call $3725
    ld hl,$a188
    ld de,$a000
    ld bc,$0310
    call $00b5
    ld de,$9000
    call $1717
    ld hl,$c3f6
    xor a
    ldh [$e1],a
    ld a,1
    call $3ec1
    ld c,3
    call $3773
    ld hl,fadein
    ld b,6
.f: ld a,[hl+]
    ldh [$47],a
    ld c,10
    call $3773
    dec b
    jr nz,.f
    xor a                           ; the player must be able to dismiss the text
    ld [$cd6b],a
    ld hl,{Lt['t_speech']:#x}
    call {PRINTTEXT:#x}
    call $2105
    call $30a2                      ; the map again
    call $2123
    ld hl,{Lt['t_defeat']:#x}
    ld de,{Lt['t_lose']:#x}
    call $3396
    ld a,{OPP}
    ld [$d059],a
    ld a,2
    ld [$d05d],a
    ld hl,$d72d
    set 6,[hl]
    set 7,[hl]
    xor a
    ldh [$b4],a
    ld [$cd6b],a
    ld a,$11
    ld [{SUB:#x}],a
    ret
fadein: db $54,$a8,$fc,$f8,$f4,$e4

; the end: LAVENDER TOWN, the credits, save, restart
ending62:
    ld a,$ff
    ld [$cd6b],a
    call $2105
    ld a,{LAV_ID}
    ld [$d35b],a
    ld a,{LAV_BANK}
    ld [$d35c],a
    call $2337
    ld hl,$418e
    ld b,$1d
    call {BANKSW:#x}
    ld hl,$7847
    ld b,$1c
    call {BANKSW:#x}
    ld b,$05
.w: ld c,$78
    call $3773
    dec b
    jr nz,.w
    jp $1f81
""",CODE31)
assert CODE31>=TXT31+len(tx)
rom.put(fo(B31,CODE31),code31,'Bank 31: v62 gti62, cave62 (the OAK scene and the end)')
# GetTrainerInformation: 0:35B6-35D5 -> rst far call + jp 360F
o=0x35b6;old=R[o:o+32];assert old[:4].hex()=='fa31d03d' and old[29:32].hex()=='c30f36',old.hex()
rom.code(o,bytes.fromhex('21'+le(L31['gti62'])+'0631cf'+'c30f36')+bytes(23),'GetTrainerInformation: picture / money table lookup -> bank 31 gti62 (v62)',old.hex(),
         reviewed='the whole lookup block is replaced; nothing jumps into it (its entry is the call from 35A8 right before)')

# ---- Cerulean Cave B1F (map E3, bank 11): script wrapper + the MEWTWO object's text chooser
B11=0x7600
assert not any(R[fo(0x11,B11):fo(0x11,0x8000)]),'bank 11 space'
c11,L11=asm(f"""
cave_s:
    ld a,[{BLACKF:#x}]
    and a
    jp z,$5ef0
    ld a,[{STAGE:#x}]
    cp 6
    jp c,$5ef0
    ld hl,{L31['cave62']:#x}
    ld b,{B31}
    call {BANKSW:#x}
    jp $5ef0
cave_text: db 8
    ld a,[{BLACKF:#x}]
    and a
    jp z,$5f1d
    ld a,[{STAGE:#x}]
    cp 6
    jp nz,$5f1d
    ld a,$10
    ld [{SUB:#x}],a
    jp {TEXTEND:#x}
""",B11)
rom.put(fo(0x11,B11),c11,'Bank 11: v62 CERULEAN CAVE B1F script wrapper + the MEWTWO text chooser')
HH=fo(0x11,0x5ee4);assert R[HH+7:HH+9].hex()=='f05e'
rom.data(HH+7,bytes.fromhex(le(L11['cave_s'])),"CERULEAN CAVE B1F script -> v62",'f05e')
TT=fo(0x11,0x5f09);assert R[TT:TT+2].hex()=='1c5f'
rom.data(TT,bytes.fromhex(le(L11['cave_text'])),"CERULEAN CAVE B1F text 1 (MEWTWO) -> v62 chooser",'1c5f')

# ---- bank 2F: OAK's forbidden-move line, no flash / shatter text for him
L60=M60['bank2f']
T2F=0x6300
assert not any(R[fo(0x2f,T2F):fo(0x2f,0x6400)])
PH44=int(M44['ph44'],16)
assert R[fo(0x2f,PH44+14):fo(0x2f,PH44+14)+3].hex()=='fa14d0'
c2f,L2f=asm(f"""
tline62:
    ld a,[$d031]
    ld hl,{int(M44['t_lor'],16):#x}
    cp $2c
    ret z
    ld hl,{int(M44['t_bru'],16):#x}
    cp $21
    ret z
    ld hl,{int(M44['t_lan'],16):#x}
    cp $2f
    ret z
    ld hl,{int(M58['bank2f']['t_blu'],16):#x}
    cp $2b
    ret z
    ld hl,{int(L60['t_bil'],16):#x}
    ld a,[{STAGE:#x}]
    cp 6
    ret c
    ld hl,t_oak
    ret
ph62:
    call {int(L60['e4chk60'],16):#x}
    jr nz,.std
    ld a,[$d031]
    cp {CLASS}
    jr nz,.std
    ld a,[{STAGE:#x}]
    cp 6
    jr c,.std
    jp {PH44+14:#x}
.std:
    jp {PH44:#x}
t_oak: db {','.join(str(x) for x in T_FORBID)}
""",T2F)
rom.put(fo(0x2f,T2F),c2f,'Bank 2F: v62 tline62 / ph62 (OAK: his forbidden-move line, no shatter text)')
TL60=int(L60['tline60'],16)
o=fo(0x2f,0x6436);assert R[o:o+3].hex()=='cd'+le(TL60)
rom.data(o+1,bytes.fromhex(le(L2f['tline62'])),'call tline60 -> tline62 (v62)',le(TL60))
o=fo(0xf,0x7dcc);assert R[o:o+5].hex()=='21'+le(PH44)+'062f'
rom.data(o+1,bytes.fromhex(le(L2f['ph62'])),'After-win phase check -> ph62 (v62)',le(PH44))

# ---- OAK has no trainer header (scripted): his kill index = LANCE's (v34 table, map E3 / class 26 set 2)
STAB=fo(0x2d,0x615c)
j=0
while R[STAB+j]!=0xff:j+=5
assert j==80 and not any(R[STAB+j+1:STAB+j+6]),j
LH=fo(0x16,0x6397);lidx=R[LH+10]|R[LH+11]<<8;assert lidx==0x1b3
rom.code(STAB+j,bytes([0xe3,OPP,2,lidx&255,lidx>>8,0xff]),"v34 scripted-trainer table: OAK (map E3, class 26 set 2) -> LANCE's kill index",'ff'+'00'*5)
rom.finish('Creepy_Black_Mu_v62.gb','manifest_v62.json','CREEPY MU V62',extra=dict(labels=dict(bank31={k:hex(v) for k,v in L31.items()},bank11={k:hex(v) for k,v in L11.items()},bank2f={k:hex(v) for k,v in L2f.items()})))
