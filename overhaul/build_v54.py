# Creepy Black Mu v54: the player's "mother" among the channelers on Tower 7F after the ritual.
#   Once the player is BLACK (ritual done, D467 = 6) the channelers stay in the 7F hall and the MOM sprite stands among them
#   (left column, row 9). Talking to her: first the long confession ("I'm not really your mother..."), afterwards the short
#   one ("I'm afraid that's your consort's duty now!"). D466 bit7 = the first talk is done.
#   Slots after the ritual (AGATHA is object 9 again): channelers in 10-14, 5, 4, 6, 7, 8; MOM = object 15 (picture 33).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V53_SHA='2d25a8c8df32c0bf7ae8b3f83ccda01daf747bdcb8644002e7d877ae9aa5f24a'
rom=Rom('Creepy_Black_Mu_v53.gb',V53_SHA)
r=rom.r;R=bytes(r)
M53=json.load(open('manifest_v53.json'))
L18={k:int(v,16) for k,v in M53['labels']['bank18'].items()}
L30={k:int(v,16) for k,v in M53['labels']['bank30'].items()}
SPOTS=[tuple(x) for x in M53['spots']]
PRINTTEXT,TEXTEND,BANKSW=0x3c94,0x2504,0x3618
STAGE,CONSORT,QFLAGS,RIT=0xd464,0xd465,0xd466,0xd467
CHPIC,MOMPIC=0x19,0x33
OBJS54=0x70a3
BANK=0x30;CODE=0x5800
assert not any(R[fo(BANK,CODE):fo(BANK,CODE+0x800)])
def wrap(s,w=17):
    out=[];cur=''
    for word in s.split():
        if cur and len(cur)+1+len(word)>w:out.append(cur);cur=word
        else:cur=(cur+' '+word) if cur else word
    out.append(cur);return out
def convo(parts):return bytes(txt([wrap(p) for p in parts],0x58,17))
MOM1=["Oh! Hello, honey!","Surprised to see me here?","Hehe! Yes, it's me!","Although... I suppose I should tell you the truth.",
"I'm not really your mother.","I was assigned by the clan to watch over the vessel... And raise you as my own!",
"You certainly weren't the easiest child to care for! Hehe!","But looking at you now... All those years of hard work have finally paid off!",
"Oh, but don't worry, dear!","You can still call me your mother if you wish.","In fact... Nothing would make me happier!",
"I'm so proud of you, honey!","You will lead our clan into a new era!","And I'll always be here to support you, just as I always have!"]
MOM2=["Oh? What's that, honey?","You want me to heal you?","Hehe! I'm afraid that's your consort's duty now!",
"I no longer have the right, nor the power to do so.","My, my... You've really become a man now! Hehe!"]
T={'t_mom1':convo(MOM1),'t_mom2':convo(MOM2)}
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())
MOMSPOT=(9,9,0x0c,20)
SPOTS11=SPOTS+[MOMSPOT]
SP=''.join(f"    db {y},{x},{f},{t}\n" for y,x,f,t in SPOTS11)
code,L=asm(f'''
; ---- the channelers (every frame on 7F, stage 5, after the old scripts); v53's ch53 + the post-ritual slots and MOM
ch54:
    ld a,[{STAGE:#x}]
    cp 5
    ret nz
    ld hl,$d5ae
    res 3,[hl]                   ; FUJI's slot is not hidden
    ld a,[{RIT:#x}]
    cp 6
    ld hl,tab_pre
    ld a,10
    jr c,.go
    ld hl,tab_post
    ld a,11
.go:ld [$d8b7],a
    ld a,l
    ld [$d8b9],a
    ld a,h
    ld [$d8ba],a
    ld c,0
.k: ld a,[$d8b9]
    ld l,a
    ld a,[$d8ba]
    ld h,a
    ld e,c
    ld d,0
    add hl,de
    ld a,[hl]
    ld b,a
    cp $8a
    jr nz,.nsa
    ld a,[{CONSORT:#x}]          ; slot A: 6, or 7 for MISTY
    cp 1
    ld b,6
    jr nz,.have
    ld b,7
    jr .have
.nsa:cp $8b
    jr nz,.have
    ld a,[{CONSORT:#x}]          ; slot B: 8, or 7 for SABRINA
    cp 3
    ld b,8
    jr nz,.have
    ld b,7
.have:
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
    cp 15
    ld a,{CHPIC}
    jr nz,.pic
    ld a,[{RIT:#x}]
    cp 6
    ld a,{CHPIC}
    jr c,.pic
    ld a,{MOMPIC}                ; object 15 after the ritual: MOM
.pic:
    ld [$d8b6],a
    ld a,b
    swap a
    ld e,a                       ; e = 16 * slot
    ld a,[$d361]                 ; only people within two steps of the player are drawn (ten sprites at most)
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
    ld a,[$d8b6]
    ld [hl],a                    ; picture
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
    ld a,[$d8b6]
    cp {MOMPIC}
    jr z,.nobase                 ; MOM keeps her own tile slot (set at map load)
    ld a,e
    add 14
    ld l,a
    ld a,[$c2ae]                 ; the channeler picture's tile slot (object 10's)
    ld [hl],a
.nobase:
    ld a,[$cfc5]                 ; standing still: the screen position from the map position
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
    ld a,[$d8b7]
    cp c
    jp nz,.k
    ret
tab_pre: db 10,11,12,13,14,15,9,4,$8a,$8b
tab_post: db 10,11,12,13,14,5,4,6,7,8,15
spots:
{SP}
; ---- LoadMapHeader's object list: the long list at stage 5 (any ritual state: MOM and the channelers stay)
objsel54:
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
    ld hl,{OBJS54:#x}
    ret
; ---- MOM (text 20)
mom54:
    ld a,[{QFLAGS:#x}]
    bit 7,a
    jr nz,.two
    ld hl,t_mom1
    call {PRINTTEXT:#x}
    ld hl,{QFLAGS:#x}
    set 7,[hl]
    jp {TEXTEND:#x}
.two:
    ld hl,t_mom2
    call {PRINTTEXT:#x}
    jp {TEXTEND:#x}
{TXT}''',CODE)
rom.put(fo(BANK,CODE),code,'Bank 30: v54 ch54 (channelers + MOM), objsel54, mom54')
labels={'bank30':{k:hex(v) for k,v in L.items() if not k.startswith('t_')}}
# ---- bank 18: the long object list (v53's, with MOM as object 15 instead of channeler 6), text table (+MOM), stubs
OBJ53=L18['objs53'];o=fo(0x18,OBJ53)
old=R[o:o+0x74];  # parse: warps, signs, count, objects
nw=R[o+1];i=o+2+4*nw+2
head=R[o:i];objs=[]
for k in range(15):
    ln=6+(2 if R[i+5]&0x40 else (1 if R[i+5]&0x80 else 0));objs.append(R[i:i+ln]);i+=ln
tail=R[i:i+8];assert tail.hex()=='7dc71009fec6010b'
mom=bytes([MOMPIC,MOMSPOT[0]+4,MOMSPOT[1]+4,0xff,0xd3,MOMSPOT[3]])
assert objs[14][0]==CHPIC
objs[14]=mom
assert not any(R[fo(0x18,OBJS54):fo(0x18,OBJS54)+0x200])
tbl=[R[fo(0x18,L18['tbl53'])+2*k]|R[fo(0x18,L18['tbl53'])+2*k+1]<<8 for k in range(19)]
b18,L18n=asm(f'''
objs54: db {','.join(str(x) for x in head+b''.join(objs)+tail)}
tbl54: dw {','.join(str(x) for x in tbl)},mom_s
mom_s: db 8
    ld hl,{L['mom54']:#x}
    ld b,{BANK:#x}
    jp {BANKSW:#x}
''',OBJS54)
assert L18n['objs54']==OBJS54
rom.put(fo(0x18,OBJS54),b18,'Bank 18: v54 7F object list (MOM = object 15), text table (+ text 20)')
h7=fo(0x18,R[0x1ae+2*0x94]|R[0x1af+2*0x94]<<8)
assert (R[h7+5]|R[h7+6]<<8)==L18['tbl53']
rom.data(h7+5,bytes.fromhex(le(L18n['tbl54'])),'Tower 7F text table -> v54 (+ MOM)',le(L18['tbl53']))
# hooks: tail53's ch53 call, LoadMapHeader's object list, script53 .post's numsprites
T53=fo(0x18,L18['tail53']);assert R[T53:T53+3].hex()=='21'+le(L30['ch53'])
rom.data(T53+1,bytes.fromhex(le(L['ch54'])),'tail53: ch53 -> ch54 (post-ritual slots, MOM)',le(L30['ch53']))
assert R[0x112e:0x1131].hex()=='21'+le(L30['objsel53'])
rom.data(0x112f,bytes.fromhex(le(L['objsel54'])),'LoadMapHeader: objsel53 -> objsel54 (long list at stage 5 whatever the ritual state)',le(L30['objsel53']))
P=fo(0x18,L18['script53.post']);assert R[P:P+5].hex()=='3e09ead1d4'.replace('d1','e1') or R[P:P+5].hex()=='3e09ea e1d4'.replace(' ','')
rom.code(P,bytes(5),'script53 .post: no numsprites 9 (the long list stays)',R[P:P+5].hex())
labels['bank18']={k:hex(v) for k,v in L18n.items()}
rom.finish('Creepy_Black_Mu_v54.gb','manifest_v54.json','CREEPY MU V54',extra=dict(labels=labels))
