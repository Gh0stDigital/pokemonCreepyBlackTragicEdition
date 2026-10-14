# Creepy Black Mu v58: BLUE (the Champion) as BLACK, and the end of the POKeMON LEAGUE.
#   Champion's room (map 78, bank 1D), as BLACK (D46C):
#     - the cut-scene starts by itself (D64C = 1) while the Champion is alive; BLUE's before-battle and defeat speeches are new
#     - BLUE is treated like the Elite Four (MOON STONE: forbidden moves refused, it shatters after his last POKeMON, BANE kills him)
#     - after the battle: NO Oak, no Hall of Fame, no reset of the Elite Four flags (they stay beaten); the player walks into the
#       next room by himself; BLUE's object is gone for good
#   Hall of Fame room (map 76, bank 16), as BLACK: its own script. The player walks in a few steps, AGATHA enters (her sprite replaces
#     OAK's object in a BLACK-only object list), speaks (her "after the Elite Four" speech), and the player is free to move again.
#     Later talks: the last three lines. D876 = scene stage (0 none, 1 BLUE beaten, 2 walking, 3 AGATHA walking in, 4 done).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V57_SHA='ba82a763baa083e6aae83511d5790a8c6bfd9d89f95e1cfeadf60d67127d96b1'
rom=Rom('Creepy_Black_Mu_v57.gb',V57_SHA)
r=rom.r;R=bytes(r)
M44=json.load(open('manifest_v44.json'))['labels']['bank2f']
M54=json.load(open('manifest_v54.json'))['labels']['bank30']
PRINTTEXT,TEXTEND,BANKSW=0x3c94,0x2504,0x3618
BLACKF,STAGE=0xd46c,0xd876
BLUE=0x2b
def wrap(s,w=17):
    out=[];cur=''
    for word in s.split():
        if cur and shown(cur+' '+word)>w:out.append(cur);cur=word
        else:cur=(cur+' '+word) if cur else word
    out.append(cur);return out
def convo(parts):return bytes(txt([wrap(p) for p in parts],0x58,17))
T={'t_before':convo(["RED... No... BLACK...","So, it really has come down to this.",
  "I don't know what's become of you. But I guess it doesn't matter anymore.",
  "I always knew we'd face each other one last time... But never like this.",
  "It seems I'm the only one left who can stop you!","This won't be like our other battles, BLACK!",
  "This time, I'll put an end to this nightmare!","Prepare yourself!"]),
 't_defeat':convo(["...RED...","How did things end up this way?","I wonder... If things had been different...",
  "Could we have just been two rivals, trying to be the best?","Maybe... Deep down...","That's all I ever wanted..."]),
 't_agatha':convo(["Hahaha! Yes... It is done!","Those fools are no more! For too long, I've endured their arrogance!",
  "Our ancestors are smiling upon us this day!","But BLACK... Your work is not yet finished.",
  "I had hoped it wouldn't come to this... But for our victory to be complete, it must be done!",
  "You must find the traitor of our clan... OAK!",
  "I thought the old fool was no longer a threat. But those MOON STONES the trainers carried...",
  "He must still be involved!","OAK must be eliminated!",
  "Once you've dealt with him, return to the # TOWER.","There, we shall begin the final ritual!"]),
 't_again':convo(["OAK must be eliminated!","Once you've dealt with him, return to the # TOWER.","There, we shall begin the final ritual!"])}
B30=0x30;TXT30=0x6700;CODE30=0x6e00
assert not any(R[fo(B30,TXT30):fo(B30,0x7400)])
c30t,L30t=asm(''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items()),TXT30)
assert TXT30+len(c30t)<CODE30
rom.put(fo(B30,TXT30),c30t,'Bank 30: v58 BLUE / AGATHA texts')

# ---- bank 16 (Hall of Fame): chooser stubs + BLACK object list; addresses first (code in bank 30 needs obj58)
B16=0x7100
assert not any(R[fo(0x16,B16):fo(0x16,0x8000)])
HOFS=0x649e;TXT=0x656a
code30,L30=asm(f'''
; ---- Hall of Fame map script as BLACK. OAK's object (picture 03) becomes AGATHA's (picture 39) on the first frame of every visit
;      (picture, InitMapSprites for her tiles); she is hidden until the scene (stage 1-3) and stands at (4,5) afterwards (stage 4).
hof58:
    ld a,[$c110]
    cp 3
    jr nz,.ready
    ld a,$39
    ld [$c110],a
    ld hl,$785b
    ld b,5
    call {BANKSW:#x}
    ld a,[{STAGE:#x}]
    cp 4
    jr c,.ready
    ld b,5
    ld c,4
    call place58
    xor a
    ld [$c119],a
    ret
.ready:
    ld a,[{STAGE:#x}]
    and a
    jr z,.hide
    cp 1
    jr z,.s1
    cp 2
    jr z,.s2
    cp 3
    jr z,.s3
    ret                             ; 4: she stands there
.hide:
    xor a
    ld [$c110],a
    ld a,$ff
    ld [$c214],a
    ld [$c215],a
    ret
.s1:
    call .hide
    ld a,$ff
    ld [$cd6b],a
    ld hl,$ccd3
    ld de,walk58
    call $354e
    dec a
    ld [$cd38],a
    call $34c8
    ld a,2
    ld [{STAGE:#x}],a
    ret
.s2:
    ld a,[$cd38]
    and a
    ret nz
    ld b,7                          ; AGATHA comes in through the door the player used
    ld c,4
    call place58
    ld a,4
    ld [$c119],a
    ld a,1
    ldh [$8c],a
    ld de,mv58
    call $3674
    ld a,3
    ld [{STAGE:#x}],a
    ret
.s3:
    ld a,[$d730]
    bit 0,a
    ret nz
    xor a
    ld [$cd6b],a
    ld [$c109],a                    ; the player turns to her
    ld a,1
    ldh [$8c],a
    call $294d
    ld a,4
    ld [{STAGE:#x}],a
    ret
; AGATHA (object 1) shown at map y = b, x = c
place58:
    ld a,$39
    ld [$c110],a
    ld a,b
    add 4
    ld [$c214],a
    ld a,c
    add 4
    ld [$c215],a
    ld a,$ff
    ld [$c216],a
    ld a,[$d361]
    ld d,a
    ld a,b
    sub d
    add a
    add a
    add a
    add a
    add $3c
    ld [$c114],a
    ld a,[$d362]
    ld d,a
    ld a,c
    sub d
    add a
    add a
    add a
    add a
    add $40
    ld [$c116],a
    ret
walk58: db $40,3,$ff
mv58: db $40,$40,$ff
''',CODE30)
rom.put(fo(B30,CODE30),code30,'Bank 30: v58 hof58 (the Hall of Fame scene as BLACK)')
c16,L16=asm(f'''
hof_s:
    ld a,[{BLACKF:#x}]
    and a
    jp z,{HOFS:#x}
    ld hl,{L30['hof58']:#x}
    ld b,{B30}
    jp {BANKSW:#x}
ag_text: db 8
    ld a,[{BLACKF:#x}]
    and a
    ld hl,$656c
    jr z,.p
    ld a,[{STAGE:#x}]
    cp 4
    ld hl,far_long
    jr c,.p
    ld hl,far_short
.p: call {PRINTTEXT:#x}
    jp {TEXTEND:#x}
far_long: db $17,{L30t['t_agatha']&255},{L30t['t_agatha']>>8},{B30},$50
far_short: db $17,{L30t['t_again']&255},{L30t['t_again']>>8},{B30},$50
''',B16)
assert B16+len(c16)<0x7200
assert L16['hof_s']==B16
rom.put(fo(0x16,B16),c16,'Bank 16: v58 Hall of Fame script / text choosers (BLACK)')

# ---- map headers: Hall of Fame script (+7) and text table entry; Champion's room script (+7)
HH=fo(0x16,0x6492);assert R[HH+7:HH+9].hex()=='9e64'
rom.data(HH+7,bytes.fromhex(le(L16['hof_s'])),'Hall of Fame map script -> v58 (BLACK: the AGATHA scene)','9e64')
assert R[fo(0x16,TXT):fo(0x16,TXT)+2].hex()=='6c65'
rom.data(fo(0x16,TXT),bytes.fromhex(le(L16['ag_text'])),'Hall of Fame text 1 -> v58 chooser (OAK / AGATHA)','6c65')

# ---- bank 1D: Champion's room
B1D=0x7ea8
assert not any(R[fo(0x1d,B1D):fo(0x1d,0x8000)])
c1d,L1d=asm(f"""
champ58:
    ld a,[{BLACKF:#x}]
    and a
    jp z,$5f1d
    ld a,[$d867]
    bit 1,a
    jr z,.live
    xor a                            ; BLUE is dead: his object is gone
    ld [$c110],a
    ld a,$ff
    ld [$c214],a
    ld [$c215],a
    jp $5f1d
.live:
    ld a,[$d64c]
    and a
    jp nz,$5f1d
    ld a,1                           ; the cut-scene starts by itself
    ld [$d64c],a
    jp $5f1d
rival58: db 8
    ld a,[{BLACKF:#x}]
    and a
    ld hl,far_b
    jr nz,.p
    ld a,[$d867]
    bit 1,a
    ld hl,$60f4
    jr z,.p
    ld hl,$6103
.p: call {PRINTTEXT:#x}
    jp {TEXTEND:#x}
def58: db 8
    ld a,[{BLACKF:#x}]
    and a
    ld hl,$60f9
    jr z,.p
    ld hl,far_d
.p: call {PRINTTEXT:#x}
    jp {TEXTEND:#x}
far_b: db $17,{L30t['t_before']&255},{L30t['t_before']>>8},{B30},$50
far_d: db $17,{L30t['t_defeat']&255},{L30t['t_defeat']>>8},{B30},$50
; script 3 (BLUE beaten): the usual one unless BLACK
s3_58:
    ld a,[{BLACKF:#x}]
    and a
    jp z,$5fbb
    ld a,[$d057]
    cp $ff
    jp z,$5f29
    call $2456
    ld hl,$d867
    set 1,[hl]                       ; the Champion is beaten (the Elite Four's flags stay as they are)
    ld a,1
    ld [{STAGE:#x}],a
    ld a,$ff
    ld [$cd6b],a
    ld hl,$ccd3
    ld de,walk
    call $354e
    dec a
    ld [$cd38],a
    call $34c8
    ld a,10                          ; the cleanup script waits for the walk
    ld [$d64c],a
    ret
walk: db $40,4,$ff
""",B1D)
rom.put(fo(0x1d,B1D),c1d,"Bank 1D: v58 Champion's room as BLACK (scene start, speeches, no Oak / Hall of Fame)")
CH=fo(0x1d,0x5f11);assert R[CH+7:CH+9].hex()=='1d5f'
rom.data(CH+7,bytes.fromhex(le(L1d['champ58'])),"Champion's room script -> v58",'1d5f')
assert R[fo(0x1d,0x60e1):fo(0x1d,0x60e1)+3].hex()=='fa67d8'
rom.code(fo(0x1d,0x60e1),bytes.fromhex('c3'+le(L1d['rival58']+1)),"BLUE's talk text: jp rival58 (BLACK: new before-battle speech)",'fa67d8',
         reviewed='TX_ASM entry replaced by a jump to a routine that does the same for the old case')
assert R[fo(0x1d,0x5f8d):fo(0x1d,0x5f8d)+2].hex()=='f960'
rom.data(fo(0x1d,0x5f8d),bytes.fromhex(le(L1d['def58'])),"Champion fight: defeat text -> v58 chooser",'f960')
assert R[fo(0x1d,0x5f37):fo(0x1d,0x5f37)+2].hex()=='bb5f'
rom.data(fo(0x1d,0x5f37),bytes.fromhex(le(L1d['s3_58'])),"Champion's room script 3 (BLUE beaten) -> v58",'bb5f')

# ---- bank 2F: BLUE counts as an Elite Four battle for the MOON STONE (e4chk / tline)
def ram_text(*parts):
    out=bytearray();inside=False
    for p in parts:
        if not inside:out.append(0);inside=True
        if p in ('line','cont','para'):out+={'line':b'\x4f','cont':b'\x55','para':b'\x51'}[p]
        else:
            assert shown(p)<=17,p;out+=enc(p)
    out+=b'\x58';return bytes(out)
T2F=0x6100
assert not any(R[fo(0x2f,T2F):fo(0x2f,0x6400)])
tblu=ram_text('BLUE: Heh...','line',"The MOON STONE's",'cont','power shields me!','para','Face me as a','line','trainer, BLACK!')
c2f,L2f=asm(f"""
e4chk58:
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
    cp {BLUE}
    ret z
.no:or 1
    ret
tline58:
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
    ld hl,t_blu
    ret
t_blu: db {','.join(str(x) for x in tblu)}
""",T2F)
rom.put(fo(0x2f,T2F),c2f,'Bank 2F: v58 e4chk58 / tline58 (BLUE too)')
for site in (0x640e,0x64bc,0x6502,0x790b):
    o=fo(0x2f,site);assert R[o:o+3].hex()=='cd5264'
    rom.data(o+1,bytes.fromhex(le(L2f['e4chk58'])),'call e4chk -> e4chk58 (v58)','5264')
o=fo(0x2f,0x6436);assert R[o:o+3].hex()=='cd6e64'
rom.data(o+1,bytes.fromhex(le(L2f['tline58'])),'call tline -> tline58 (v58)','6e64')

# ---- BLUE has no trainer header (scripted): his kill index = LANCE's (already dead on the BLACK route; there is no free bit left), via v34's table
STAB=fo(0x2d,0x615c)
j=0
while R[STAB+j]!=0xff:j+=5
assert j==60 and not any(R[STAB+j+1:STAB+j+16]),j
LH=fo(0x16,0x6397);lidx=R[LH+10]|R[LH+11]<<8;assert lidx==0x1b3,hex(lidx)
ents=b''.join(bytes([0x78,200+BLUE,sn,lidx&255,lidx>>8]) for sn in (1,2,3))+b'\xff'
rom.code(STAB+j,ents,"v34 scripted-trainer table: the Champion (map 78, RIVAL3 sets 1-3) -> LANCE's kill index (so BANE / CURSE can kill BLUE)",'ff'+'00'*15)
rom.finish('Creepy_Black_Mu_v58.gb','manifest_v58.json','CREEPY MU V58',extra=dict(labels=dict(bank1d={k:hex(v) for k,v in L1d.items()},bank16={k:hex(v) for k,v in L16.items()},bank30={k:hex(v) for k,v in L30.items()},bank2f={k:hex(v) for k,v in L2f.items()})))
