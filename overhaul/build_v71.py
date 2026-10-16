# Creepy Black Mu v71: NOTORIETY and the bribed gate guards.
#   1. Notoriety (D85C, 0-255): +1 every time you leave a trainer alive after using CURSE in the battle (every trainer: ordinary, gym trainers and leaders, the rival, scripted grunts).
#      A kill does not count, a battle without CURSE does not count. (D85C / D85D are unused event-flag bytes beside the v69 sulk bits; NEW GAME clears them.)
#   2. The guards of the four SAFFRON gate houses (ROUTE 5, 6, 7, 8) now check you when you step in front of them, coming from the route side (not out of SAFFRON):
#        notoriety < 3: nothing changes (the police bulletin still shows after a murder, as before);
#        notoriety >= 3: the bulletin (if you have murdered), then three tiers of suspicion (3-9, 10-24, 25+), a fee = 100 x notoriety (at most 6000) as a YES/NO:
#          YES + enough money: the fee is paid, "couldn't possibly be you", you walk on (D85D = paid; it is reset by every map load, so leaving the gate house and coming
#            back means paying again);  NO or not enough money: sent back like the thirsty guard does it.
#        BLACK is never charged (the guards are scared, v46).
#   The check replaces  ld a,[D728] / bit 6,a / ret nz  at the start of each gate's map script 0; the dialogue is a new text id 4 (new text table per gate).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V70_SHA='d180c227515d5f02a1486f9bd7ca7f2afc5fe43357550fb3575bf6fa4e779ee6'
rom=Rom('Creepy_Black_Mu_v70.gb',V70_SHA)
R=bytes(rom.r)
L67={k:int(v,16) for k,v in json.load(open('manifest_v67.json'))['labels']['bank31'].items()}
L69={k:int(v,16) for k,v in json.load(open('manifest_v69.json'))['labels']['bank31'].items()}
NOT=0xd85c;PAID=0xd85d;DUE=0xd843
for a in (NOT,PAID,DUE):assert not R[a]-R[a] or True
# ------------------------------------------------------------------------------------------------ bank 32: texts + routines
B32=0x32;TXT=0x4400
def line_ok(l):assert shown(l)<=17,l
def T(paras):
    for p in paras:
        for l in p:line_ok(l)
    return bytes(txt(paras,0x58,17))
TX={}
TX['s1']=T([["Hmm... you seem","to fit some of","the description."],["I can't risk","letting you pass","so easily..."],["Unless you can","make it worth my","while."]])
TX['s2']=T([["You match the","description very","well, you know."],["I really should","not let you pass."],["But a man has","bills to pay..."]])
TX['s3']=T([["...It's you. The","killer from the","bulletin."],["Everyone knows.","I should call it","in."],["But my silence","has a price."]])
TX['paid']=T([["Hah! Couldn't","possibly be you.","Go right ahead."]])
TX['poor']=T([["Not enough? Then","you're not going","anywhere."]])
TX['no']=T([["Then turn back.","I can't let you","through."]])
# fee text: "My silence costs" / <BCD> . Pay?
for l in ("My silence costs",". Pay?"):line_ok(l)
FEE={n:bytes([0])+enc("My silence costs")+bytes([0x4f])+enc("\u00a5%d00. Pay?"%n)+bytes([0x58]) for n in range(3,61)}
TX['police']=bytes([0x17,0x48,0x6c,0x06,0x50])
tx=bytearray();TA={}
for k,v in TX.items():TA[k]=TXT+len(tx);tx+=v
FT=[]
for n in range(3,61):FT.append(TXT+len(tx));tx+=FEE[n]
TA['feetab']=TXT+len(tx);tx+=b''.join(a.to_bytes(2,'little') for a in FT)
assert TXT+len(tx)<0x5400
rom.put(fo(B32,TXT),bytes(tx),'Bank 32: v71 bribe texts')
SRC=f'''
bcheck:                          ; far-called from a gate's script: DUE = 1 when the guard wants his bribe
    xor a
    ld [{DUE:#x}],a
    ld a,[$d46c]
    and a
    ret nz                       ; BLACK
    ld a,[{NOT:#x}]
    cp 3
    ret c
    ld a,[{PAID:#x}]
    and a
    ret nz                       ; paid during this visit
    ld a,[$d365]
    cp $0a
    ret z                        ; coming out of SAFFRON
    ld a,1
    ld [{DUE:#x}],a
    ret
bdialog:                         ; far-called from the gate guard's text id 4 (TX_ASM); DUE = 1 afterwards: send the player back
    xor a
    ld [{DUE:#x}],a
    ld a,[$d453]
    and a
    jr z,.nb
    ld a,[$d45b]
    and a
    jr nz,.nb
    ld a,1
    ld [$d45b],a                 ; the usual bulletin first
    ld hl,{TA['police']:#x}
    call $3c94
.nb:
    ld a,[{NOT:#x}]
    cp 10
    ld hl,{TA['s1']:#x}
    jr c,.say
    cp 25
    ld hl,{TA['s2']:#x}
    jr c,.say
    ld hl,{TA['s3']:#x}
.say:
    call $3c94
    ld a,[{NOT:#x}]
    cp 61
    jr c,.c
    ld a,60
.c:
    ld c,a
    xor a
.l:
    add 1
    daa
    dec c
    jr nz,.l                     ; a = notoriety (max 60) as BCD = the fee's hundreds and thousands
    ld [$d458],a
    xor a
    ld [$d457],a
    ld [$d459],a
    ld a,[$d85c]
    cp 61
    jr c,.f
    ld a,60
.f:
    sub 3
    add a
    ld e,a
    ld d,0
    ld hl,{TA['feetab']:#x}
    add hl,de
    ld a,[hl+]
    ld h,[hl]
    ld l,a
    call $3c94
    call $362e
    ld a,[$cc26]
    and a
    jr nz,.no
    ld a,[$d347]
    and a
    jr nz,.ok
    ld a,[$d458]
    ld b,a
    ld a,[$d348]
    cp b
    jr c,.poor
.ok:
    ld a,[$d458]
    ld b,a
    ld a,[$d348]
    sub b
    daa
    ld [$d348],a
    jr nc,.paid
    ld a,[$d347]
    sub 1
    daa
    ld [$d347],a
.paid:
    ld a,1
    ld [{PAID:#x}],a
    ld hl,{TA['paid']:#x}
    call $3c94
    ret
.poor:
    ld hl,{TA['poor']:#x}
    jr .refuse
.no:
    ld hl,{TA['no']:#x}
.refuse:
    call $3c94
    ld a,1
    ld [{DUE:#x}],a
    ret
'''
CODE32=0x4000
code32,L32=asm(SRC,CODE32,{})
assert CODE32+len(code32)<TXT
rom.put(fo(B32,CODE32),code32,'Bank 32: v71 gate bribe routines')
# ------------------------------------------------------------------------------------------------ bank 7: per-gate stubs + text tables
B7=7;A7=0x7619
assert not any(R[fo(B7,A7):fo(B7,A7)+487])
GATES=[ # map, script-0 entry, coords list, facing, push-back routine, cur-script var, header, old text table, (guard text) 
 (0x46,0x5f60,0x5f9f,2,0x5f53,0xd662),
 (0x49,0x605e,0x609c,1,0x60b1,0xd636),
 (0x4c,0x6138,0x6177,8,0x6121,0xd663),
 (0x4f,0x61fe,0x623c,2,0x61e7,0xd637)]
p=A7;stubs=[];tables=[]
for mp,entry,coords,face,push,var in GATES:
    assert R[fo(B7,entry):fo(B7,entry)+6].hex()=='fa28d7cb77c0',hex(mp)
    h=R[0x1ae+2*mp]|R[0x1ae+2*mp+1]<<8;ho=fo(B7,h);old_tab=R[ho+5]|R[ho+6]<<8
    stub_src=f'''
g:
    ld hl,{coords:#x}
    call $3501
    jr nc,.van
    ld hl,{L32['bcheck']:#x}
    ld b,{B32}
    db $cf
    ld a,[{DUE:#x}]
    and a
    jr z,.van
    ld a,{face}
    ld [$d528],a
    xor a
    ldh [$b4],a
    ld a,4
    ldh [$8c],a
    call $294d
    ld a,[{DUE:#x}]
    and a
    jr z,.van
    call {push:#x}
    ld a,1
    ld [{var:#x}],a
    or 1
    ret
.van:
    ld a,[$d728]
    bit 6,a
    ret
'''
    s,_=asm(stub_src,p,{});stubs.append((mp,entry,p,s));p+=len(s)
# shared TX_ASM text 4
tx4=p;t4,_=asm(f'''
x:
    db $08
    ld hl,{L32['bdialog']:#x}
    ld b,{B32}
    db $cf
    jp $2504
''',p,{});p+=len(t4)
tabs=[]
for mp,entry,coords,face,push,var in GATES:
    h=R[0x1ae+2*mp]|R[0x1ae+2*mp+1]<<8;ho=fo(B7,h);old_tab=R[ho+5]|R[ho+6]<<8
    ot=fo(B7,old_tab);ent=[R[ot+2*i]|R[ot+2*i+1]<<8 for i in range(3)]
    tab=b''.join(e.to_bytes(2,'little') for e in ent)+tx4.to_bytes(2,'little')
    tabs.append((mp,ho,old_tab,p,tab));p+=len(tab)
assert p<=A7+487,p-A7
blob=b''.join(s for _,_,_,s in stubs)+t4+b''.join(t for *_,t in tabs)
rom.put(fo(B7,A7),blob,'Bank 07: v71 gate bribe stubs + text tables')
for (mp,entry,sa,s),(mp2,ho,old_tab,ta,tab) in zip(stubs,tabs):
    rom.hook(fo(B7,entry),bytes([0xcd,sa&255,sa>>8,0xc0,0,0]),'Saffron gate %02x script 0: bribe check before the drink flag test'%mp,'fa28d7cb77c0',provides=('f','a'),
             reviewed='the stub ends with the original  ld a,[D728] / bit 6,a  so the flags (Z = no drink given) reach the following ret nz / the vanilla code; it may also return NZ to end the script')
    rom.data(ho+5,ta.to_bytes(2,'little'),'Gate %02x header: text table with the new text id 4'%mp,old_tab.to_bytes(2,'little').hex())
# ------------------------------------------------------------------------------------------------ notoriety
# D85E: bit 0 = a kill happened in this battle, bit 1 = this battle has been counted. Cleared at every battle start (14:6a50, where D452 is cleared).
KILLM=0xd85e
# (a) the kill routine (3:7f8e -> far call 2E:41db) marks the kill
K2E=0x42d0
kcode,_=asm(f"""
k71:
    ld a,1
    ld [{KILLM:#x}],a
    ld a,[$d451]
    jp $41de
""",K2E,{})
assert not any(R[fo(0x2e,K2E):fo(0x2e,K2E)+len(kcode)])
rom.put(fo(0x2e,K2E),kcode,'Bank 2E: v71 kill marker')
assert R[fo(0x2e,0x41db):fo(0x2e,0x41de)].hex()=='fa51d4' and R[fo(0x2e,0x41de)]==0xa7
rom.code(fo(0x2e,0x41db),bytes([0xc3,K2E&255,K2E>>8]),'Kill extension 2E:41db: mark the kill for the notoriety counter','fa51d4',
         reviewed='the stub repeats ld a,[D451] and jumps back to the following and a')
# (b) battle start: clear the marker with D452
o=fo(0x14,0x6a50);assert R[o:o+10].hex()=='afea52d4f0d7ead4d0c9' and not any(R[o+10:o+13])
rom.code(o,bytes.fromhex('afea52d4ea5ed8f0d7ead4d0c9'),'Battle start: also clear the notoriety kill marker','afea52d4f0d7ead4d0c9000000',
         reviewed='the routine is only called from its start; three bytes longer into zero padding')
# (c) end of a battle (2D:5fc0 = post2, called by the home stub 0:00C0 after every battle): a trainer battle won with CURSE used and no kill = notoriety + 1
N2D=0x4a00
ncode,_=asm(f"""
notor:
    ld a,[$d713]
    cp $c8
    jr c,.out                    ; a wild battle
    ld a,[$d452]
    and a
    jr z,.out                    ; no CURSE used
    ld a,[{KILLM:#x}]
    and a
    jr nz,.out                   ; killed, or already counted
    ld a,[$d057]
    cp $ff
    jr z,.out                    ; lost
    ld a,[$d45d]
    and a
    jr nz,.out                   ; the MIRAGE
    ld a,[$d467]
    cp 1
    jr z,.out
    cp 2
    jr z,.out
    cp 5
    jr z,.out                    ; the ritual battles
    ld a,[{NOT:#x}]
    inc a
    jr z,.mark
    ld [{NOT:#x}],a
.mark:
    ld a,2
    ld [{KILLM:#x}],a
.out:
    ld a,[$d45f]
    ret
""",N2D,{})
assert not any(R[fo(0x2d,N2D):fo(0x2d,N2D)+len(ncode)])
rom.put(fo(0x2d,N2D),ncode,'Bank 2D: v71 notoriety counter')
assert R[fo(0x2d,0x5fc0):fo(0x2d,0x5fc0)+3].hex()=='fa5fd4'
rom.hook(fo(0x2d,0x5fc0),bytes([0xcd,N2D&255,N2D>>8]),'After every battle (post2): notoriety counter','fa5fd4',provides=('a','f'),
         reviewed='notor ends with the original ld a,[D45F] / ret; everything else it touches is restored by the following push af')
# ------------------------------------------------------------------------------------------------ bank 2E: map load clears "paid"
ML=R[fo(0x2e,0x4000):fo(0x2e,0x4003)];assert ML[0]==0xc3;NEXT=ML[1]|ML[2]<<8
M71=0x42b0
mcode,_=asm(f'''
m71:
    xor a
    ld [{PAID:#x}],a
    jp {NEXT:#x}
''',M71,{})
rom.put(fo(0x2e,M71),mcode,'Bank 2E: v71 map load clears the bribe-paid flag')
rom.code(fo(0x2e,0x4000),bytes([0xc3,M71&255,M71>>8]),'Map load chain: clear the bribe-paid flag',ML.hex())
rom.finish('Creepy_Black_Mu_v71.gb','manifest_v71.json','CREEPY MU V71',extra=dict(labels=dict(bank32={k:hex(v) for k,v in L32.items()})))
