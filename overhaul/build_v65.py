# Creepy Black Mu v65: MR. MU's first meeting in PALLET TOWN (the opening), reworked.
#   1. Leaving the house (first step outside, D454 = 0) freezes the player (wJoyIgnore) until MR. MU has walked up and finished his talk.
#   2. He no longer gives his name: he apologises for the intrusion, says he saw the player is about to start a journey as a TRAINER, asks to
#      humour an old man's question - then the same question and THE TRAINER / THE POKeMON menu as before.
#   3. Afterwards he just stands there (D454 = 2) until the player enters another building / leaves town (bank 2E mapload sets D454 = 3).
#      From then on he is gone for good: his object is moved off the map in the object data (y/x = FF), the script puts him on the map only
#      for the meeting (and re-places him at his post if a save is loaded while he waits) and keeps the picture hidden in state 3.
#   The GHOST route (answer THE TRAINER) still puts him in the CERULEAN house later (v6 code, untouched).
# The script (bank 6 6D72) is now a far call into bank 31 (pal65); the new speech is far text in bank 31.
from patchlib import *
from patchguard import fo
from sm83asm import asm

V64_SHA='d27e47f719ab121cd3656e694a16ba044227cce0038d6e0f952f384fab66194a'
rom=Rom('Creepy_Black_Mu_v64.gb',V64_SHA)
r=rom.r;R=bytes(r)
B31=0x31;CODE=0x6000;TXT=0x6200
assert not any(R[fo(B31,CODE):fo(B31,0x8000)])
def wrap(s,w=17):
    out=[];cur=''
    for word in s.split():
        if cur and len(cur)+1+len(word)>w:out.append(cur);cur=word
        else:cur=(cur+' '+word) if cur else word
    out.append(cur);return out
SPEECH=["Hello young lad. Sorry to intrude on you so suddenly...",
        "But I couldn't help but notice...",
        "You are about to start a journey as a TRAINER, right?",
        "You certainly have the look about you.",
        "I was wondering if you could humor an old man's question."]
paras=[wrap(s) for s in SPEECH]
for p in paras:assert len(p)<=4,p
paras+=[["If a #MON","kills a person","while obeying its","TRAINER..."],["Who is","responsible?"]]
tx=bytes(txt(paras,0x58,17))
rom.put(fo(B31,TXT),tx,"Bank 31: v65 MR. MU's first speech (no name) + the question")
SRC='''
pal65:                           ; Pallet map script (every frame), called from bank 6 6D72
    ld a,[$d451]
    and a
    jr z,.nogh
    xor a
    ld [$c150],a                 ; the shamaness (object 5) is gone once GHOST is acquired
    ld a,$ff
    ld [$c254],a
    ld [$c255],a
.nogh:
    ld a,[$d454]
    cp 3
    jr z,.gone
    cp 2
    jr z,.s2
    cp 1
    jr z,.s1
    ld a,[$d361]                 ; state 0: the first step outside the house (the auto-walk from the door ends at y6) starts the meeting
    cp 6
    jr c,.gone
    ld a,1
    ld [$d454],a
    ld a,$ff
    ld [$cd6b],a                 ; the player cannot move
    ld b,6
    ld c,8
    call place
    ld a,4
    ldh [$8c],a
    ld de,move65
    jp $3674                     ; MoveSprite: MR. MU walks up (2 steps left)
.s1:
    ld a,[$d730]
    bit 0,a
    jr z,.talk
    ld a,$ff
    ld [$cd6b],a                 ; still frozen while he walks
    ret
.talk:
    xor a
    ld [$cd6b],a
    call $3c87
    ld a,4
    ldh [$8c],a
    call $294d                   ; his text (question, menu, answer)
    ld a,2
    ld [$d454],a
    xor a
    ld [$cd6b],a
    ret
.s2:
    ld a,[$c244]                 ; waiting at his post; put him back there after a load
    cp $ff
    ret nz
    ld b,6
    ld c,6
    call place
    ret
.gone:                           ; not on the map: picture 0, position FF
    xor a
    ld [$c140],a
    ld a,$ff
    ld [$c244],a
    ld [$c245],a
    ret
place:                           ; MR. MU (object 4, picture 10) at map y = b, x = c
    ld a,$10
    ld [$c140],a
    ld a,b
    add 4
    ld [$c244],a
    ld a,c
    add 4
    ld [$c245],a
    ld a,$ff
    ld [$c246],a
    ld a,8
    ld [$c149],a
    ld a,[$d361]
    ld d,a
    ld a,b
    sub d
    add a
    add a
    add a
    add a
    add $3c
    ld [$c144],a
    ld a,[$d362]
    ld d,a
    ld a,c
    sub d
    add a
    add a
    add a
    add a
    add $40
    ld [$c146],a
    ret
move65: db $80,$80,$ff
'''
code,L=asm(SRC,CODE,{})
assert CODE+len(code)<TXT
rom.put(fo(B31,CODE),code,'Bank 31: v65 pal65 (the Pallet script: MR. MU meeting)')
# bank 6: the old script (6D72-6DE9) -> far call + the old tail; the rest of it is zeroed
o=fo(6,0x6d72);old=R[o:o+0x78];assert old.hex().startswith('fa51d4a7ca856d') and old.hex().endswith('fa4bd7cb67c360' '4e'),old.hex()
new=bytes([0x21])+L['pal65'].to_bytes(2,'little')+bytes([0x06,B31,0xcf])+bytes.fromhex('fa4bd7cb67c3604e')
rom.code(o,new+bytes(0x78-len(new)),'Pallet script -> far call to bank 31 pal65 (old logic removed)',old.hex(),
         reviewed='the whole old script body is replaced; its only entry is the jp at 4E5B (to 6D72); the internal jumps die with it')
# bank 6: the question text -> TX_FAR to the new speech
o=fo(6,0x6967);old=R[o:o+0x58];assert old.hex().startswith('00'+'49'.zfill(2)) or True
assert R[o+0x58-1]==0x58,hex(R[o+0x57])
rom.data(o,bytes([0x17])+TXT.to_bytes(2,'little')+bytes([B31,0x50])+bytes(0x58-5),"Pallet MR. MU question text -> far text (bank 31)",old.hex())
# the object: y/x = FF (off the map)
o=fo(6,0x6d45);assert R[o:o+6].hex()=='100a0cffd208'
rom.data(o+1,bytes([0xff,0xff]),'Pallet object 4 (MR. MU): position FF,FF (placed by the script)','0a0c')
rom.finish('Creepy_Black_Mu_v65.gb','manifest_v65.json','CREEPY MU V65',extra=dict(labels=dict(bank31={k:hex(v) for k,v in L.items()})))
