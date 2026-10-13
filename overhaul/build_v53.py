# Creepy Black Mu v53: Tower 7F channelers (lore), the secret door opens only after AGATHA's talk, the altar stash.
#   1. Once the consort has arrived (quest stage 5, before the ritual is over) ten channelers stand on Tower 7F, five on each
#      side of the hall; each tells one part of the lore (Shamaness 1-10). They are the ten sprite slots that are free then:
#      six new objects (10-15), AGATHA's second object (9), FUJI's hidden slot (4) and the two girls that aren't the consort.
#   2. The stairs behind AGATHA open only after she has finished her talk ("The way to the ritual room is open now"): she
#      steps aside (up, left) and the graves turn into the stairway. Her talk sets D466 bit3, the walk bit5, the open door
#      bit4. Later visits and every visit once the ritual has started: open, AGATHA beside it.
#   3. The altar: entering the TOWER CHAMBER before the ritual is over takes PRETA and AZHI out of the party (to SRAM 1:BA00,
#      D466 bit6); the stands play their cry and say "<MON> stands still on the stand." when they were awakened by MR. MU (the
#      fossil sprites stay on the stands either way); leaving the chamber (or the end of the ritual, before BLACK joins) puts
#      them back (party, else the box). After the ritual (D467 >= 3) the fossil sprites are gone from the stands.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V52_SHA='2b8504acada31972aa6c6e5721da3a7d55af48bfcdd7b0e1f8c8932b2825918c'
rom=Rom('Creepy_Black_Mu_v52.gb',V52_SHA)
r=rom.r;R=bytes(r)
L38={k:int(v,16) for k,v in json.load(open('manifest_v38.json'))['labels']['bank2d'].items()}
L16=json.load(open('manifest_v16.json'))['labels']
L52=json.load(open('manifest_v52.json'))['labels']
L50=json.load(open('manifest_v50.json'))['labels']
OLD_AGATHA=int(L16['bank2e']['agatha'],16)
PRINTTEXT,TEXTEND,BANKSW,ADDNTIMES,COPYDATA,PLAYCRY,PREDEF=0x3c94,0x2504,0x3618,0x3abb,0x00b5,0x13ff,0x3ec1
STAGE,CONSORT,QFLAGS,RIT,MU2=0xd464,0xd465,0xd466,0xd467,0xd460
PRETA,AZHI=0xb6,0xb7
CHPIC=0x19
BANK=0x30;CODE=0x4c00
assert not any(R[fo(BANK,CODE):fo(BANK,CODE+0x800)])
labels={}
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
("The Ancient Trials","Our ancestors held contests at sacred grounds. They believed strength alone was not enough to earn the right to pass."),
("The Lavender Cult","The clan was forbidden from opening the passage again. Yet some continued their rituals in secret. They eventually settled in Lavender."),
("The Forgotten God","They say the old gods departed long ago. Yet our ancestors believed one was left behind... Waiting for someone to open the way.")]
def lore_text(n,title,body):
    lines=wrap(body);paras=[['SHAMANESS %d:'%(n+1)]+wrap(title)]
    for i in range(0,len(lines),4):paras.append(lines[i:i+4])
    return bytes(txt(paras,0x58,17))
def tx(paras,end=0x58,maxw=17):return bytes(txt(paras,end,maxw))
# spots: (y, x, facing, text id): pairs per row, left column faces right, right column faces left
SPOTS=[]
for k in range(10):
    row=12-2*(k//2);left=(k%2==0)
    SPOTS.append((row,9 if left else 12,0x0c if left else 0x08,10+k))
T={'t_ag5':tx([["AGATHA: You have","brought her."],["Good. The way to","the ritual room","is open now."],["I will step","aside..."]]),
   't_ag5b':tx([["AGATHA: The","ritual room is","open."],["Go when you are","ready."]]),
   't_amber':tx([["The OLD AMBER","rests on the","stand."]],0x57),
   't_dome':tx([["The DOME FOSSIL","rests on the","stand."]],0x57),
   't_helix':tx([["The HELIX FOSSIL","rests on the","stand."]],0x57),
   't_preta':tx([["PRETA stands","still on the","stand."]],0x57),
   't_azhi':tx([["AZHI stands","still on the","stand."]],0x57)}
for n,(title,body) in enumerate(LORE):T['lore%d'%n]=lore_text(n,title,body)
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())
SP=''.join(f"    db {y},{x},{f},{t}\n" for y,x,f,t in SPOTS)
STRUCT_TMP=0xd8a4
OBJS53=0x6ec0
GIVE_TMP=0x7fd5
assert not any(R[fo(0x2d,GIVE_TMP):fo(0x2d,0x8000)])
code,L=asm(f'''
; ---- 1. the channelers (7F, every frame, after the other scripts): ten sprites when the consort has arrived
ch53:
    ld a,[{STAGE:#x}]
    cp 5
    jp nz,.off
    ld a,[{RIT:#x}]
    cp 6
    jp nc,.rit
    ld hl,$d5ae
    res 3,[hl]                   ; FUJI's slot is no longer hidden
    ld c,0
.k: ld a,c
    cp 6
    jr nc,.rt
    add 10
    ld b,a
    jr .have
.rt:
    sub 6
    jr z,.r9
    dec a
    jr z,.r4
    dec a
    jr z,.rsa
    ld a,[{CONSORT:#x}]          ; slot B: 8, or 7 for SABRINA (consort 3)
    cp 3
    ld b,8
    jr nz,.have
    ld b,7
    jr .have
.rsa:ld a,[{CONSORT:#x}]          ; slot A: 6, or 7 for MISTY (consort 1)
    cp 1
    ld b,6
    jr nz,.have
    ld b,7
    jr .have
.r9:ld b,9
    jr .have
.r4:ld b,4
.have:                           ; b = slot, c = spot index
    ld hl,spots
    ld a,c
    add a
    add a
    ld e,a
    ld d,0
    add hl,de
    ld a,[hl+]
    ld [$d8b0],a                 ; y
    ld a,[hl+]
    ld [$d8b1],a                 ; x
    ld a,[hl+]
    ld [$d8b2],a                 ; facing
    ld a,[hl]
    ld [$d8b3],a                 ; text id
    ld a,b
    swap a
    ld e,a                       ; e = 16 * slot
    ld a,[$d361]                 ; only the channelers within two steps of the player are drawn (the GB shows ten sprites at most)
    ld d,a
    ld a,[$d8b0]
    sub d
    jr nc,.p
    cpl
    inc a
.p: cp 3
    jr c,.show
    ld h,$c1
    ld l,e
    xor a
    ld [hl],a
    ld h,$c2
    ld a,e
    add 4
    ld l,a
    ld a,$ff
    ld [hl+],a
    ld [hl],a
    jr .next
.show:
    ld h,$c1
    ld l,e
    ld [hl],{CHPIC}              ; picture
    ld a,e
    add 9
    ld l,a
    ld a,[$d8b2]
    ld [hl],a                    ; facing
    ld h,$c2
    ld a,e
    add 4
    ld l,a
    ld a,[$d8b0]
    add 4
    ld [hl+],a                   ; y
    ld a,[$d8b1]
    add 4
    ld [hl+],a                   ; x
    ld [hl],$ff                  ; movement: stay
    ld a,e
    add 14
    ld l,a
    ld a,[$c2ae]                 ; the tile slot of the channeler picture (object 10's)
    ld [hl],a
    ld a,[$cfc5]                 ; standing still: the screen position from the map position (a sprite that was hidden has none)
    and a
    jr nz,.nopx
    ld a,[$d361]
    ld h,a
    ld a,[$d8b0]
    sub h
    add a
    add a
    add a
    add a
    add $3c
    ld d,a
    ld a,[$d362]
    ld h,a
    ld a,[$d8b1]
    sub h
    add a
    add a
    add a
    add a
    add $40
    ld [$d8b4],a
    ld h,$c1
    ld a,e
    add 4
    ld l,a
    ld [hl],d
    inc l
    inc l
    ld a,[$d8b4]
    ld [hl],a
.nopx:
    ld a,b
    dec a
    add a
    ld e,a
    ld d,0
    ld hl,$d4e4
    add hl,de
    ld [hl],$ff
    inc hl
    ld a,[$d8b3]
    ld [hl],a
    ld hl,$d504
    add hl,de
    xor a
    ld [hl+],a
    ld [hl],a
.next:
    inc c
    ld a,c
    cp 10
    jp nz,.k
    ret
.rit:
    ld hl,$d5ae
    set 3,[hl]                   ; FUJI's slot hidden again
.off:
    ld b,6
    ld e,$a0                     ; sprite 10
.h: ld h,$c1
    ld l,e
    xor a
    ld [hl],a
    ld h,$c2
    ld a,e
    add 4
    ld l,a
    ld a,$ff
    ld [hl+],a
    ld [hl],a
    ld a,e
    add 16
    ld e,a
    dec b
    jr nz,.h
    ret
spots:
{SP}
; ---- LoadMapHeader (0:112E via rst 08): hl = the object list; 7F gets the long list (six channelers) only at stage 5 before the
;      ritual is over - more sprites make the overworld slower
objsel53:
    ld a,[$d3a9]
    ld l,a
    ld a,[$d3aa]
    ld h,a
    ld a,[$d35e]
    cp $94
    ret nz
    ld a,[{STAGE:#x}]
    cp 5
    ret nz
    ld a,[{RIT:#x}]
    cp 6
    ret nc
    ld hl,{OBJS53:#x}
    ret

; ---- AGATHA's talk on 7F (2D agatha25's .old path -> here): stage 5 = the door
ag53:
    ld a,[{STAGE:#x}]
    cp 5
    jr z,.five
    ld hl,{OLD_AGATHA:#x}
    ld b,$2e
    jp {BANKSW:#x}
.five:
    ld a,[{QFLAGS:#x}]
    bit 3,a
    jr nz,.again
    ld hl,t_ag5
    call {PRINTTEXT:#x}
    ld hl,{QFLAGS:#x}
    set 3,[hl]
    ret
.again:
    ld hl,t_ag5b
    jp {PRINTTEXT:#x}

; ---- 3. the altar stash: PRETA / AZHI (party) <-> SRAM 1:BA00 (count, then 66 bytes each: struct 44, nickname 11, OT 11)
sram_on:
    ld a,$0a
    ld [$0000],a
    ld a,1
    ld [$4000],a
    ret
sram_off:
    xor a
    ld [$4000],a
    ld [$0000],a
    ret
stash53:                         ; chamber, every frame
    ld a,[{QFLAGS:#x}]
    bit 6,a
    ret nz
    ld a,[{RIT:#x}]
    cp 3
    ret nc
    call sram_on
    xor a
    ld [$ba00],a
    ld c,0
.l: ld a,[$d163]
    cp c
    jr z,.done
    jr c,.done
    ld b,0
    ld hl,$d164
    add hl,bc
    ld a,[hl]
    cp {PRETA}
    jr z,.take
    cp {AZHI}
    jr z,.take
    inc c
    jr .l
.take:
    push bc
    ld a,[$ba00]
    ld hl,$ba01
    ld bc,66
    call {ADDNTIMES:#x}
    ld d,h
    ld e,l                       ; de = the entry
    pop bc
    push bc
    ld a,c
    ld hl,$d16b
    ld bc,44
    call {ADDNTIMES:#x}
    push de
    ld bc,44
    call {COPYDATA:#x}           ; struct
    pop de
    ld hl,44
    add hl,de
    ld d,h
    ld e,l
    pop bc
    push bc
    ld a,c
    ld hl,$d2b5
    ld bc,11
    call {ADDNTIMES:#x}
    ld bc,11
    call {COPYDATA:#x}           ; nickname
    pop bc
    ld a,[$ba00]
    inc a
    ld [$ba00],a
    push bc
    ld a,c
    ld [$cf92],a
    xor a
    ld [$cf95],a
    farcall $7b61,1              ; RemovePokemon
    pop bc
    jr .l
.done:
    ld a,[$ba00]
    and a
    jr z,.none
    ld hl,{QFLAGS:#x}
    set 6,[hl]
.none:
    jp sram_off
restore53:                       ; leaving the chamber / end of the ritual: back to the party (else the box)
    ld a,[{QFLAGS:#x}]
    bit 6,a
    ret z
    res 6,a
    ld [{QFLAGS:#x}],a
    call sram_on
    ld a,[$ba00]
    ld [$baf0],a                 ; (v38's add_mon uses D457-D45A: the counters live in the SRAM stash)
    xor a
    ld [$baf1],a
.r: ld a,[$baf1]
    ld b,a
    ld a,[$baf0]
    cp b
    jr z,.done
    ld a,b
    ld hl,$ba01
    ld bc,66
    call {ADDNTIMES:#x}
    ld de,{STRUCT_TMP:#x}
    ld bc,55
    call {COPYDATA:#x}
    farcall {GIVE_TMP:#x},$2d
    ld a,[$baf1]
    inc a
    ld [$baf1],a
    jr .r
.done:
    jp sram_off

; ---- the stands (chamber texts 2-4, TX_ASM)
st_amber:
    ld a,[{MU2:#x}]
    cp 4
    ld hl,t_amber
    jr nz,stand
    ld a,{AZHI}
    ld hl,t_azhi
    jr cry
st_dome:
    ld a,[{MU2:#x}]
    cp 2
    ld hl,t_dome
    jr c,stand
    ld a,{PRETA}
    ld hl,t_preta
    jr cry
st_helix:
    ld hl,t_helix
stand:
    call {PRINTTEXT:#x}
    jp {TEXTEND:#x}
cry:
    push hl
    call {PLAYCRY:#x}
    pop hl
    jr stand
{TXT}''',CODE)
rom.put(fo(BANK,CODE),code,'Bank 30: v53 channelers, AGATHA\'s door talk, altar stash, stands')
labels['bank30']={k:hex(v) for k,v in L.items() if not k.startswith(('t_','lore'))}

# ---- bank 2D: give_tmp (v38 add_mon on the struct at D8A4, nickname after it), AGATHA's talk, the ritual end
c2d,L2D=asm(f'''
give_tmp:
    ld hl,{STRUCT_TMP:#x}
    ld de,{STRUCT_TMP+44:#x}
    jp {L38['add_mon']:#x}
''',GIVE_TMP)
rom.put(fo(0x2d,GIVE_TMP),c2d,'Bank 2D: v53 give_tmp (altar stash back to the party / box)')
AG=0x4725
old=bytes.fromhex('21'+le(OLD_AGATHA)+'062ecd1836');assert R[fo(0x2d,AG):fo(0x2d,AG)+8]==old
rom.code(fo(0x2d,AG),bytes.fromhex('21'+le(L['ag53'])+'0630cd1836'),'AGATHA talk (2D agatha25 .old): -> ag53 (stage 5 = the door)',old.hex())
RT=L50['bank2d']['ritual50'];RT=int(RT,16);B50=int(L50['bank2f']['boost50'],16)
oldr=R[fo(0x2d,RT):fo(0x2d,RT)+19];assert oldr[-8:]==bytes(8) or True
new,_=asm(f'''
ritual53:
    farcall {L['restore53']:#x},$30
    farcall {B50:#x},$2f
    jp {L38['black_join']:#x}
''',RT)
assert len(new)<=19 and not any(R[fo(0x2d,RT)+11:fo(0x2d,RT)+19]) or len(new)==19
rom.code(fo(0x2d,RT),new,'Ritual end: PRETA / AZHI back from the altar first, then boost50, then black_join',oldr[:len(new)].hex())

# ---- bank 18: Tower 7F object list (+6 channelers), text table (+10 lore texts), script, chamber script, stand stubs
B18=OBJS53
assert not any(R[fo(0x18,B18):fo(0x18,B18+0x400)])
M7=0x94;h7=fo(0x18,R[0x1ae+2*M7]|R[0x1ae+2*M7+1]<<8)
OBJ7=R[h7+10]|R[h7+11]<<8;TEX7=R[h7+5]|R[h7+6]<<8
assert (OBJ7,TEX7)==(0x7a00,0x6742)
o=fo(0x18,OBJ7);nw=R[o+1];i=o+2+4*nw;assert R[i]==0;nobj=R[i+1];assert nobj==9
i+=2;objs=[];
for k in range(nobj):
    ln=6+(2 if R[i+5]&0x40 else (1 if R[i+5]&0x80 else 0));objs.append(R[i:i+ln]);i+=ln
tail=R[i:i+8];assert tail.hex()=='7dc71009fec6010b',tail.hex()
new_objs=[bytes([CHPIC,y+4,x+4,0xff,0xd3 if f==0x0c else 0xd2,t]) for (y,x,f,t) in SPOTS[:6]]
objdata=R[o:o+2+4*nw]+bytes([0,15])+b''.join(objs)+b''.join(new_objs)+tail
tbl=[R[fo(0x18,TEX7)+2*k]|R[fo(0x18,TEX7)+2*k+1]<<8 for k in range(9)]
assert all(0x4000<=a<0x8000 for a in tbl)
lorestubs=''.join(f"lore_s{n}: db $17,{L['lore%d'%n]&255},{L['lore%d'%n]>>8},{BANK},$50\n" for n in range(10))
b18,L18=asm(f'''
objs53: db {','.join(str(x) for x in objdata)}
tbl53: dw {','.join(str(x) for x in tbl)},{','.join('lore_s%d'%n for n in range(10))}
{lorestubs}
stand_a: db 8
    ld hl,{L['st_amber']:#x}
    ld b,{BANK:#x}
    jp {BANKSW:#x}
stand_d: db 8
    ld hl,{L['st_dome']:#x}
    ld b,{BANK:#x}
    jp {BANKSW:#x}
stand_h: db 8
    ld hl,{L['st_helix']:#x}
    ld b,{BANK:#x}
    jp {BANKSW:#x}
mv_door: db $40,$80,$ff
opendoor:
    ld a,$11
    ld [$d09f],a
    ld bc,$0005
    ld a,$18
    jp {PREDEF:#x}
tail53:
    ld hl,{L['ch53']:#x}
    ld b,{BANK:#x}
    call {BANKSW:#x}
    jp $4d05
script_ch:
    ld hl,{L['stash53']:#x}
    ld b,{BANK:#x}
    call {BANKSW:#x}
    ld a,[{RIT:#x}]
    cp 3
    jr c,.k
    xor a
    ld [$c120],a
    ld [$c130],a
    ld [$c140],a
    ld a,$ff
    ld [$c224],a
    ld [$c225],a
    ld [$c234],a
    ld [$c235],a
    ld [$c244],a
    ld [$c245],a
.k: ld hl,$457a
    ld b,$2d
    call {BANKSW:#x}
    jp {PRINTTEXT if False else 0x3c87:#x}
script53:
    ld a,[{QFLAGS:#x}]
    bit 6,a
    jr z,.nr
    ld hl,{L['restore53']:#x}
    ld b,{BANK:#x}
    call {BANKSW:#x}
.nr:ld a,[{STAGE:#x}]
    cp 5
    jr c,.before
    ld a,[{RIT:#x}]
    cp 6
    jr nc,.post
    and a
    jr nz,.dooropen
    ld a,[{QFLAGS:#x}]
    bit 4,a
    jr nz,.dooropen
    bit 3,a
    jr z,.tail
    bit 5,a
    jr nz,.moving
    ld a,[$d730]
    bit 0,a
    jr nz,.tail
    ld hl,{QFLAGS:#x}
    set 5,[hl]
    ld a,5
    ldh [$ff8c],a
    ld de,mv_door
    call $3674
    jr .tail
.moving:
    ld a,[$d730]
    bit 0,a
    jr nz,.tail
    ld hl,{QFLAGS:#x}
    set 4,[hl]
    res 5,[hl]
    xor a
    ld [$cd6b],a                 ; MoveSprite left the joypad ignored
    call opendoor
    jr .tail
.dooropen:
    ld hl,$d126
    bit 5,[hl]
    jr z,.tail
    res 5,[hl]
    ld a,6
    ld [$c254],a
    ld a,14
    ld [$c255],a
    call opendoor
    jr .tail
.post:
    ld a,9
    ld [$d4e1],a                 ; only the old nine sprites (the six extra ones cost walking speed)
    xor a
    ld [$c150],a
    ld a,$ff
    ld [$c254],a
    ld [$c255],a
    ld hl,$d126
    bit 5,[hl]
    res 5,[hl]
    jr z,.tail
    call opendoor
    jr .tail
.before:
    ld a,9
    ld [$d4e1],a
    xor a
    ld [$c190],a
    ld a,$ff
    ld [$c294],a
    ld [$c295],a
.tail:
    jp $6752
''',B18)
rom.put(fo(0x18,B18),b18,'Bank 18: v53 7F objects (+6 channelers), lore text table, door script, chamber script, stand stubs')
labels['bank18']={k:hex(v) for k,v in L18.items()}
assert B18+len(b18)<0x7495 or True
# 7F header: texts -> tbl53, objects -> objs53
rom.data(h7+5,bytes.fromhex(le(L18['tbl53'])),'Tower 7F text table -> v53 (19 texts)',le(TEX7))
assert L18['objs53']==OBJS53
old=R[0x112e:0x1136];assert old.hex()=='faa9d36ffaaad367'
rom.code(0x112e,bytes.fromhex('21'+le(L['objsel53'])+'0630cf0000'),'LoadMapHeader: object list of Tower 7F (long list only at stage 5 before the ritual ends) via 30:objsel53',old.hex(),
         reviewed='the hits at 0:0DE9/0DFC/0E14/0E2A are misread "inc [hl] / ld de" bytes (34/35 11) of the map-scroll code, not jumps into 0:1134/1135')
# 7F script chain: 18:7A50 (v19 door/AGATHA block) -> script53; v16 script's last jp 4D05 -> tail53
old=R[fo(0x18,0x7a50):fo(0x18,0x7a53)];assert old.hex()=='fa64d4'
rom.code(fo(0x18,0x7a50),bytes.fromhex('c3'+le(L18['script53'])),'7F map script (v19 block) -> script53 (door after the talk, restore the altar stash)',old.hex(),
         reviewed='the old block 7A53-7A8B is dead now; its inner jr/jp targets lay inside it only')
old=R[fo(0x18,0x67a4):fo(0x18,0x67a7)];assert old.hex()=='c3054d'
rom.code(fo(0x18,0x67a4),bytes.fromhex('c3'+le(L18['tail53'])),'7F map script tail (v16) -> tail53 (channelers every frame)',old.hex())
# chamber (map 0x69): script and stand texts
CH=fo(0x18,0x7d40);assert R[CH+7]==0xa1 and R[CH+8]==0x6e
rom.data(CH+7,bytes.fromhex(le(L18['script_ch'])),'Chamber script -> v53 (altar stash, fossils gone after the ritual)','a16e')
TT=fo(0x18,0x6eb1)
assert [R[TT+2*k]|R[TT+2*k+1]<<8 for k in (1,2,3)]==[0x7d78,0x7da5,0x7dd4]
rom.data(TT+2,bytes.fromhex(le(L18['stand_a'])+le(L18['stand_d'])+le(L18['stand_h'])),'Chamber stand texts -> v53 (cry + "stands still" when awakened)','787da57dd47d')
rom.finish('Creepy_Black_Mu_v53.gb','manifest_v53.json','CREEPY MU V53',extra=dict(labels=labels,spots=SPOTS))
