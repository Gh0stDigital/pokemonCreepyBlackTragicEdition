# Creepy Black Mu v60: BILL's cottage after OAK's aide (BLACK, D876 = 5): BILL comes out of his machine, tells where OAK went, and fights.
#   - class 26 (PROF.OAK slot, unused) becomes "BILL" (SCIENTIST picture, ALAKAZAM / MAGNETON / ELECTRODE / JOLTEON); he counts as an Elite-Four-style
#     battle (MOON STONE: forbidden moves refused, it shatters, BANE kills him); his kill index is LANCE's (scripted, v34 table)
#   - scene (bank 30 bill60, D877 = sub-stage 0..4): everything hidden, BILL appears at the machine and walks down, long speech, battle;
#     after the win nothing is said: D876 = 6 (OAK went to CERULEAN CAVE) and the cottage is empty
#   - the cottage map is exempt from v28's NPC takeover
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V59_SHA='d9b1e6a9b024fb2acee21d7e0a5d5fdcabf7aa911b82f92164d26712d23295b7'
rom=Rom('Creepy_Black_Mu_v59.gb',V59_SHA)
r=rom.r;R=bytes(r)
M44=json.load(open('manifest_v44.json'))['labels']['bank2f']
M58=json.load(open('manifest_v58.json'))['labels']
PRINTTEXT,TEXTEND,BANKSW=0x3c94,0x2504,0x3618
BLACKF,STAGE,SUB=0xd46c,0xd876,0xd877
CLASS=26;OPP=200+CLASS
def wrap(s,w=17):
    out=[];cur=''
    for word in s.split():
        if cur and shown(cur+' '+word)>w:out.append(cur);cur=word
        else:cur=(cur+' '+word) if cur else word
    out.append(cur);return out
def convo(parts):return bytes(txt([wrap(p) for p in parts],0x58,17))
T={'t_before':convo(["Oh! Hey there!","Whoa... What happened to you?!","I've never seen anything like it!","Are you even human anymore?",
 "Say... You're looking for PROF.OAK, aren't you?","He was here not long ago. We were working on a special project together!",
 "He's gone to CERULEAN CAVE to finish our work.","Hmm... You know, OAK warned me you might come looking for him.",
 "He said you were dangerous...","Now that I see you for myself, I think I understand why!",
 "But this transformation of yours... It's fascinating!","Just imagine what I could learn from studying you!",
 "Hmm... On second thought...","Maybe it'd be best if I didn't let you leave!","Sorry, pal! Nothing personal!",
 "But I can't let a specimen like you get away!"]),
 't_defeat':convo(["Oh man... You're really something else!","I guess it's too late to ask you to spare me, huh...?","Heh... Good thing I made that backup before you came..."]),
 't_lose':convo(["Nothing personal, pal!"])}
B30=0x30;TXT30=0x7a00;CODE30=0x7e00
assert not any(R[fo(B30,TXT30):fo(B30,0x8000)])
t30,L30t=asm(''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items()),TXT30)
assert TXT30+len(t30)<CODE30,hex(TXT30+len(t30))
rom.put(fo(B30,TXT30),t30,"Bank 30: v60 BILL's speeches")

# ---- trainer class 26: BILL (name, picture, party)
PM=0x39952;o=PM+5*(CLASS-1)
rom.data(o,bytes.fromhex(le(0x627d)+'000000'),'Class 26 pic = SCIENTIST pic, no prize money',R[o:o+5])
TN=0x39a3d;names=bytes(R[TN:TN+420]).split(b'\x50')[:47];old=b'\x50'.join(names)+b'\x50'
assert names[CLASS-1]==enc('OAK')
names[CLASS-1]=enc('BILL');new=b'\x50'.join(names)+b'\x50'
pad=len(old)
while R[TN+pad]==0x50:pad+=1
assert len(new)<=pad,(len(new),pad)
rom.data(TN,new.ljust(pad,b'\x50'),'Trainer class names: OAK (26) -> BILL',R[TN:TN+pad])
PARTY=0x7ef0
assert not any(R[fo(0xe,PARTY):fo(0xe,PARTY+16)])
party=bytes([0xff,58,0x95,56,0x36,56,0x8d,58,0x68,0])
rom.put(fo(0xe,PARTY),party,"Bank E: v60 BILL's party (ALAKAZAM 58, MAGNETON 56, ELECTRODE 56, JOLTEON 58)")
TDP=0x39d79;o=TDP+2*(CLASS-1)
rom.data(o,bytes.fromhex(le(PARTY)),'Class 26 party -> BILL',R[o:o+2])
# class 26 is used by no map object / trainer header
w=lambda a:R[a]|R[a+1]<<8
def objects(o):
    p=o+1;p+=1+4*R[p];p+=1+3*R[p];n=R[p];p+=1;out=[]
    for i in range(n):
        t=R[p+5];size=6+(2 if t&0x40 else 0)+(1 if t&0x80 else 0);out.append((p,t));p+=size
    return out
for mp in range(0xf8):
    bank=R[0xc23d+mp];hp=w(0x1ae+2*mp)
    if hp<0x4000 or bank==0 or mp==0x0b:continue
    hh=fo(bank,hp);n=bin(R[hh+9]&15).count('1');oo=fo(bank,w(hh+10+11*n))
    for p,t in objects(oo):assert not (t&0x40 and R[p+6]==OPP),('class 26 used on map',hex(mp))

# ---- bank 30: the scene
code30,L30=asm(f'''
bill60:
    ld a,[{STAGE:#x}]
    cp 6
    jp nc,.empty
    ld a,[{SUB:#x}]
    and a
    jp z,.s0
    cp 1
    jp z,.s1
    cp 2
    jp z,.s2
    cp 3
    jp z,.s3
    ret
.hide13:
    ld c,1
.hl:ld a,c
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
    inc c
    ld a,c
    cp 4
    jr nz,.hl
    ret
.empty:
    jp .hide13
.s0:
    call .hide13
    ld a,$ff
    ld [$cd6b],a
    ld a,1
    ld [{SUB:#x}],a
    ret
.s1:
    call .hide13
    ld c,40                         ; a moment, then BILL steps out of his machine
    call $3773
    ld a,$62                        ; the engine's own ShowObject for BILL (toggle 62)
    ld [$cc4d],a
    ld a,$16
    call $3ec1
    ld b,4
    ld c,4
    call place60
    xor a
    ld [$c129],a
    ld a,2
    ldh [$8c],a
    ld de,mv60
    call $3674
    ld a,2
    ld [{SUB:#x}],a
    ret
.s2:
    ld a,[$d730]
    bit 0,a
    ret nz
    ld a,8
    ld [$c129],a                    ; faces the player
    xor a
    ld [$cd6b],a
    ld a,2
    ldh [$8c],a
    call $294d                      ; his speech (text 2 -> chooser)
    ld hl,{L30t['t_defeat']:#x}
    ld de,{L30t['t_lose']:#x}
    call $3396
    ld a,{OPP}
    ld [$d059],a
    ld a,1
    ld [$d05d],a
    ld hl,$d72d
    set 6,[hl]
    set 7,[hl]
    xor a
    ldh [$b4],a
    ld a,3
    ld [{SUB:#x}],a
    ret
.s3:                                ; back from the battle
    ld a,[$d057]
    cp $ff
    jr nz,.won
    xor a                           ; lost: the scene starts again next time
    ld [{SUB:#x}],a
    ret
.won:
    call .hide13
    ld a,6
    ld [{STAGE:#x}],a
    ld a,4
    ld [{SUB:#x}],a
    ret
; BILL (object 2) shown at map y = b, x = c
place60:
    ld a,$0c
    ld [$c120],a
    ld a,b
    add 4
    ld [$c224],a
    ld a,c
    add 4
    ld [$c225],a
    ld a,$ff
    ld [$c226],a
    xor a
    ld [$c122],a
    ld a,[$d361]
    ld d,a
    ld a,b
    sub d
    add a
    add a
    add a
    add a
    add $3c
    ld [$c124],a
    ld a,[$d362]
    ld d,a
    ld a,c
    sub d
    add a
    add a
    add a
    add a
    add $40
    ld [$c126],a
    ret
mv60: db 0,0,$ff
''',CODE30)
rom.put(fo(B30,CODE30),code30,'Bank 30: v60 bill60 (the scene in BILL\'s cottage)')

# ---- bank 7: the cottage's script wrapper (BLACK from stage 5 on) and BILL's text chooser (text 2)
B7=0x7fa8
assert not any(R[fo(7,B7):fo(7,0x8000)]),'bank 7 space'
c7,L7=asm(f'''
bill_s:
    ld a,[{BLACKF:#x}]
    and a
    jp z,$677a
    ld a,[{STAGE:#x}]
    cp 5
    jp c,$677a
    ld hl,{L30['bill60']:#x}
    ld b,{B30}
    jp {BANKSW:#x}
bill_text: db 8
    ld a,[{BLACKF:#x}]
    and a
    jr z,.old
    ld a,[{STAGE:#x}]
    cp 5
    jr nz,.old
    ld hl,far_b
    call {PRINTTEXT:#x}
    jp {TEXTEND:#x}
.old:
    jp $7841
far_b: db $17,{L30t['t_before']&255},{L30t['t_before']>>8},{B30},$50
''',B7)
assert B7+len(c7)<=0x8000
assert R[fo(7,0x7840)]==8
rom.put(fo(7,B7),c7,"Bank 7: v60 BILL's cottage script wrapper + BILL's text chooser")
HH=fo(7,0x676e);assert R[HH+7:HH+9].hex()=='7a67'
rom.data(HH+7,bytes.fromhex(le(L7['bill_s'])),"BILL's house script -> v60",'7a67')
TT=fo(7,0x6844+2);assert R[TT:TT+2].hex()=='4078'
rom.data(TT,bytes.fromhex(le(L7['bill_text'])),"BILL's house text 2 (BILL) -> v60 chooser (the v15 wrapper stays the old path)",'4078')

# ---- v28's NPC takeover: BILL'S HOUSE (map 58) is exempt (the speech is started through sprite 2)
EX=0x7e20
assert not any(R[fo(0x2d,EX):fo(0x2d,EX)+20])
old_m=R[fo(0x2d,0x48ff):fo(0x2d,0x48ff)+16]
assert old_m[-1]==0xff and old_m[:-1].count(0xff)==0
rom.put(fo(0x2d,EX),old_m[:-1]+bytes([0x58,0xff]),'Bank 2D: v60 exempt maps (v28 list + BILL\'S HOUSE)')
o=fo(0x2d,0x481b);assert R[o:o+3].hex()=='21ff48'
rom.data(o+1,bytes.fromhex(le(EX)),'v28 npc_talk: exempt_maps -> v60 list','ff48')

# ---- bank 2F: BILL counts as an Elite Four battle for the MOON STONE (e4chk / tline)
def ram_text(*parts):
    out=bytearray();inside=False
    for p in parts:
        if not inside:out.append(0);inside=True
        if p in ('line','cont','para'):out+={'line':b'\x4f','cont':b'\x55','para':b'\x51'}[p]
        else:
            assert shown(p)<=17,p;out+=enc(p)
    out+=b'\x58';return bytes(out)
T2F=0x6200
assert not any(R[fo(0x2f,T2F):fo(0x2f,0x6400)])
tbil=ram_text('BILL: Heh...','line',"OAK's MOON STONE",'cont','keeps me safe!','para',"Let's see what","line",'you can do!')
c2f,L2f=asm(f"""
e4chk60:
    ld a,[{BLACKF:#x}]
    and a
    jr z,.no
    ld a,[$d057]
    cp 2
    jr nz,.no
    ld a,[$d031]
    cp $2c
    ret z
    cp $21
    ret z
    cp $2f
    ret z
    cp $2b
    ret z
    cp {CLASS}
    ret z
.no:or 1
    ret
tline60:
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
    ld hl,t_bil
    ret
t_bil: db {','.join(str(x) for x in tbil)}
""",T2F)
rom.put(fo(0x2f,T2F),c2f,'Bank 2F: v60 e4chk60 / tline60 (BILL too)')
E58=int(M58['bank2f']['e4chk58'],16);TL58=int(M58['bank2f']['tline58'],16)
for site in (0x640e,0x64bc,0x6502,0x790b):
    o=fo(0x2f,site);assert R[o:o+3].hex()=='cd'+le(E58)
    rom.data(o+1,bytes.fromhex(le(L2f['e4chk60'])),'call e4chk58 -> e4chk60 (v60)',le(E58))
o=fo(0x2f,0x6436);assert R[o:o+3].hex()=='cd'+le(TL58)
rom.data(o+1,bytes.fromhex(le(L2f['tline60'])),'call tline58 -> tline60 (v60)',le(TL58))

# ---- BILL has no trainer header (scripted): his kill index = LANCE's (v34 table)
STAB=fo(0x2d,0x615c)
j=0
while R[STAB+j]!=0xff:j+=5
assert j==75 and not any(R[STAB+j+1:STAB+j+6]),j
LH=fo(0x16,0x6397);lidx=R[LH+10]|R[LH+11]<<8;assert lidx==0x1b3
rom.code(STAB+j,bytes([0x58,OPP,1,lidx&255,lidx>>8,0xff]),"v34 scripted-trainer table: BILL (map 58, class 26 set 1) -> LANCE's kill index",'ff'+'00'*5)
rom.finish('Creepy_Black_Mu_v60.gb','manifest_v60.json','CREEPY MU V60',extra=dict(labels=dict(bank7={k:hex(v) for k,v in L7.items()},bank30={k:hex(v) for k,v in L30.items()},bank2f={k:hex(v) for k,v in L2f.items()})))
