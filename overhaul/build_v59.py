# Creepy Black Mu v59: back to PALLET TOWN after the League: OAK'S LAB is empty, one frightened researcher hides in a corner and says where OAK went.
#   As BLACK (D46C) with D876 >= 4 (AGATHA's scene after the League is done): every object in the lab is hidden except the aide (object 10),
#   who stands in the lower-left corner. His talk: the fear speech; the first time D876 = 5 ("OAK is at BILL's"). Otherwise the lab is as before.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V58_SHA='a2a2e78a23c31a6deadffdf3f85d1d17727411ff3e06f7307f4d7d0a11ba4afd'
rom=Rom('Creepy_Black_Mu_v58.gb',V58_SHA)
r=rom.r;R=bytes(r)
PRINTTEXT,TEXTEND,BANKSW=0x3c94,0x2504,0x3618
BLACKF,STAGE=0xd46c,0xd876
def wrap(s,w=17):
    out=[];cur=''
    for word in s.split():
        if cur and shown(cur+' '+word)>w:out.append(cur);cur=word
        else:cur=(cur+' '+word) if cur else word
    out.append(cur);return out
def convo(parts):return bytes(txt([wrap(p) for p in parts],0x58,17))
AIDE=["...!","P-please! Don't hurt me!","Everyone fled when they heard you were coming!","P-PROF.OAK? You're looking for him?!",
      "He's not here! I swear!","He went to see BILL at his cottage near CERULEAN CITY!","Something about finishing a project...",
      "That's all I know! Please!","I don't want to die!"]
B30=0x30;TXT30=0x7500;CODE30=0x7800
assert not any(R[fo(B30,TXT30):fo(B30,TXT30+0x400)])
t30,L30t=asm("t_aide: db "+",".join(str(x) for x in convo(AIDE)),TXT30)
rom.put(fo(B30,TXT30),t30,"Bank 30: v59 the aide's speech")
code30,L30=asm(f'''
; OAK'S LAB, every frame (BLACK after the League): everybody gone but the aide (object 10), hiding in the lower-left corner
lab59:
    ld a,[{BLACKF:#x}]
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
''',CODE30)
rom.put(fo(B30,CODE30),code30,"Bank 30: v59 lab59 (OAK'S LAB after the League)")
B7=0x7f70
assert not any(R[fo(7,B7):fo(7,0x8000)])
c7,L7=asm(f'''
lab_s:
    ld hl,{L30['lab59']:#x}
    ld b,{B30}
    call {BANKSW:#x}
    jp $4b0e
aide_text: db 8
    ld a,[{BLACKF:#x}]
    and a
    jp z,$540c
    ld a,[{STAGE:#x}]
    cp 4
    jp c,$540c
    ld hl,far_aide
    call {PRINTTEXT:#x}
    ld a,[{STAGE:#x}]
    cp 4
    jr nz,.e
    ld a,5
    ld [{STAGE:#x}],a
.e: jp {TEXTEND:#x}
far_aide: db $17,{L30t['t_aide']&255},{L30t['t_aide']>>8},{B30},$50
''',B7)
assert B7+len(c7)<=0x8000
rom.put(fo(7,B7),c7,"Bank 7: v59 OAK'S LAB script wrapper + the aide's text chooser")
HH=fo(7,0x4b02);assert R[HH+7:HH+9].hex()=='0e4b'
rom.data(HH+7,bytes.fromhex(le(L7['lab_s'])),"OAK'S LAB script -> v59 (empty lab after the League as BLACK)",'0e4b')
TT=fo(7,0x5082+18);assert R[TT:TT+2].hex()=='0b54'
rom.data(TT,bytes.fromhex(le(L7['aide_text'])),"OAK'S LAB text 10 (the aide) -> v59 chooser",'0b54')
assert R[fo(7,0x540b):fo(7,0x540b)+1]==b'\x08'
rom.finish('Creepy_Black_Mu_v59.gb','manifest_v59.json','CREEPY MU V59',extra=dict(labels=dict(bank7={k:hex(v) for k,v in L7.items()},bank30={k:hex(v) for k,v in L30.items()})))
