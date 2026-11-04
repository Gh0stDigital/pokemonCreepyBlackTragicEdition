# Creepy Black Mu v99 (on v98): CINNABAR GYM
#   1. The seven quiz trainers can be killed with CURSE like every other trainer (they vanish at once, gravestones on the next visit).
#      All kill bits were taken, so they get index $23B0+n -> D886 bit n (n = object - 2; D886 = the last event-flag byte, unused, NEW GAME clears it):
#      the kill set/test routine 3:4DB9 now keeps d and uses D410 as the base for any high byte ($1xx -> D430.. as before, $23Bn -> D886),
#      kill_chk2 (2D:6425) gets a helper with the same rule; v34's phase2 table gives the quiz battles these indices (was 0 = "But, it failed!");
#      the map-load / per-frame gravestone table of CINNABAR GYM (2D:7180 entry A6) lists the seven.
#   2. A quiz machine whose trainer is dead: "ERROR! DESIGNATED TRAINER MISSING." (no question; quiz n belongs to object n+2 = D886 bit n).
#   3. BLAINE: when a quiz trainer has been killed (any D886 bit), his pre-battle speech is a surprised, knowing one (OAK and FUJI's twisted project);
#      spared after CURSE was used in the battle (D452, his kill bit clear), he tells about FUJI and OAK at the POKeMON MANSION before the badge text.
from patchlib import *
from patchguard import fo
from sm83asm import asm
V98_SHA='91749b673d7a5a43d5111b4c3204728c741b5522332f4d40dbbdacf6f0ad4d38'
rom=Rom('Creepy_Black_Mu_v98.gb',V98_SHA)
R=bytes(rom.r)
def lh(a):return a.to_bytes(2,'little').hex()
def T(paras,end=0x58):return bytes(txt(paras,end,17))
CK=0xd886
HI=0x23;LO=0xb0          # index (HI<<8)|(LO+n): (0x23B0+n)>>3 = 0x476, D410+0x476 = D886
assert (((HI<<8)|LO)>>3)+0xd410==CK
# ---- 1a. kill set/test 3:4DB9: ld a,d / and a / jr z,+3 / ld hl,D410 / nop nop   (d is kept: the 16-bit shift that follows divides de by 8)
o=fo(3,0x4db9);assert R[o:o+9].hex()=='7aa7280516002130d4' and R[o+9:o+12].hex()=='7be607'
assert R[o+12:o+24].hex()=='4fcb3acb1bcb3acb1bcb3acb1b'[:24]
rom.code(o,bytes.fromhex('7aa728032110d40000'),'Kill bit set/test: base D410 + index/8 for every high byte ($1xx as before, $23Bn -> D886)',R[o:o+9].hex(),
         reviewed='same entry, same registers out (hl base, d/e shifted by the code that follows); $1xx indices give the same byte as before')
# ---- 1b. kill_chk2 2D:6425 -> helper
A2D=0x4c40
assert not any(R[fo(0x2d,A2D):fo(0x2d,A2D)+0x40])
c2d,L2D=asm(f'''
kc99:                           ; d:e = kill index -> hl = its byte base (D4A4 / D430 / D886), e fixed for D886
    ld hl,$d4a4
    ld a,d
    and a
    ret z
    ld hl,$d430
    cp {HI}
    ret nz
    ld hl,{CK:#x}
    ld a,e
    and 7
    ld e,a
    ret
gtA6:                            ; CINNABAR GYM: object, kill index lo, hi (the seven quiz trainers)
''' + ''.join(f'    db {k},{LO+k-2},{HI}\n' for k in range(2,9)) + '    db 0\n',A2D,{})
rom.put(fo(0x2d,A2D),c2d,'Bank 2D: v99 kc99 (kill_chk2 base helper) + CINNABAR GYM gravestone table')
o=fo(0x2d,0x6425);assert R[o:o+10].hex()=='21a4d47aa728032130d4'
rom.code(o,bytes.fromhex('cd'+lh(L2D['kc99']))+bytes(7),'kill_chk2: kill bit base through kc99 (D886 for the CINNABAR quiz trainers)',R[o:o+10].hex(),reviewed='kc99 sets hl / a like the replaced code and fixes e for the D886 range')
o=fo(0x2d,0x7180)+2*0xa6;assert R[o:o+2]==b'\0\0'
rom.data(o,bytes.fromhex(lh(L2D['gtA6'])),'Gravestone table: CINNABAR GYM -> the seven quiz trainers','0000')
# ---- 1c. phase2 table: the quiz battles get their kill index
S=fo(0x2d,0x615c);tab=bytearray(R[S:S+0x40])
SETS={(0xd0,9):2,(0xd3,4):3,(0xd0,10):4,(0xd3,5):5,(0xd0,11):6,(0xd3,6):7,(0xd0,12):8}
done=0
for i in range(0,0x40,5):
    if tab[i]==0xff:break
    if tab[i]==0xa6:
        k=SETS[(tab[i+1],tab[i+2])];assert tab[i+3:i+5]==b'\0\0'
        rom.data(S+i+3,bytes([LO+k-2,HI]),'phase2: CINNABAR quiz trainer (class %02X set %d, object %d) -> kill index %04X'%(tab[i+1],tab[i+2],k,(HI<<8)|(LO+k-2)),'0000');done+=1
assert done==7
# ---- 2. quiz machine: trainer dead -> error text
A7=0x6ce0
assert not any(R[fo(7,A7):fo(7,A7)+0x60])
c7,L7=asm(f'''
quiz99:                          ; (7:6A36, in the quiz's TX_ASM) the machine's trainer (object q+2) dead -> error, end the text
    xor a
    ld [$da38],a
    ld a,[{CK:#x}]
    ld c,a
    ld a,[$cd3d]
    and $0f
    ld b,a
.m: srl c
    dec b
    jr nz,.m
    bit 0,c                      ; c = D886 >> q: bit 0 = bit q
    jr z,.alive
    pop hl
    ld hl,t_err
    call $3c94
    jp $2504
.alive:
    ld a,[$cd3d]
    ret
t_err: db {','.join(str(x) for x in T([["ERROR!"],["DESIGNATED","TRAINER MISSING."]]))}
''',A7,{})
rom.put(fo(7,A7),c7,'Bank 7: v99 quiz99 (CINNABAR quiz machine of a dead trainer: error text)')
o=fo(7,0x6a36);assert R[o:o+7].hex()=='afea38dafa3dcd'
rom.code(o,bytes.fromhex('cd'+lh(L7['quiz99']))+bytes(4),'CINNABAR quiz: dead trainer -> ERROR text (quiz99)',R[o:o+7].hex(),reviewed='quiz99 repeats xor a / ld [DA38],a / ld a,[CD3D] for the code that follows; the error path drops the return and ends the text')
# ---- 3. BLAINE
SHOCK=T([["BLAINE: Hah!","So it's you..."],["I heard the","cries of my","students."],["I've heard the","rumors, too. A","child with a","GHOST that kills."],
         ["OAK and FUJI...","So their twisted","project really","came together."],["I never thought","I'd see it walk","into my GYM!"],["Very well! Show","me what they","made of you!"]])
LORE=T([["BLAINE: ...You","spared me."],["Hmph. Then you","deserve to hear","the truth."],["Long ago, FUJI","and OAK worked","together in the","#MON MANSION."],
        ["FUJI was obsessed","with souls and","what waits after","death."],["OAK wanted to","know how far a","#MON could be","pushed."],
        ["I was there. I","burned what I","could... but not","everything."],["That mansion","still holds many","secrets."],["Secrets that are","best left buried.","Remember that."]])
B32=0x32;T32=0x7c00
assert not any(R[fo(B32,T32):fo(B32,T32)+0x400])
t32,L32=asm(f'''
shock99: db {','.join(str(x) for x in SHOCK)}
lore99: db {','.join(str(x) for x in LORE)}
''',T32,{})
rom.put(fo(B32,T32),t32,"Bank 32: v99 BLAINE's shock speech + the spared lore")
A1=0x68c0
assert not any(R[fo(0x1d,A1):fo(0x1d,A1)+0x40])
c1,L1=asm(f'''
bl99:                            ; (1D:58FD) BLAINE's pre-battle speech: a quiz trainer is dead -> the shock speech
    ld a,[{CK:#x}]
    and $7f
    ld hl,$5914
    jr z,.p
    ld hl,far_s
.p: jp $3c94
far_s: db $17,{L32['shock99']&255},{L32['shock99']>>8},{B32},$50
t10_99: db 8                     ; text 10 (after the battle, before the badge): spared after CURSE -> the lore first
    ld a,[$d452]
    and a
    jr z,.o
    ld a,[$d4a7]
    bit 7,a                      ; BLAINE's kill bit (index 31)
    jr nz,.o
    ld hl,far_l
    call $3c94
.o: ld hl,$5925
    call $3c94
    jp $2504
far_l: db $17,{L32['lore99']&255},{L32['lore99']>>8},{B32},$50
''',A1,{})
rom.put(fo(0x1d,A1),c1,"Bank 1D: v99 BLAINE text choosers (shock speech, spared lore)")
o=fo(0x1d,0x58fd);assert R[o:o+6].hex()=='211459cd943c'
rom.code(o,bytes.fromhex('cd'+lh(L1['bl99'])+'000000'),"BLAINE pre-battle speech -> bl99",R[o:o+6].hex(),reviewed='bl99 loads hl itself and tail-jumps to PrintText; the following ld hl,5919 is untouched')
o=fo(0x1d,0x7c1c+18);assert R[o:o+2].hex()=='2559'
rom.data(o,bytes.fromhex(lh(L1['t10_99'])),"CINNABAR GYM text 10 (BLAINE after the battle) -> t10_99",'2559')
rom.finish('Creepy_Black_Mu_v99.gb','manifest_v99.json','CREEPY MU V99')
