# Creepy Black Mu v67: SHOCK MODE for the gyms.
#   1. A gym trainer killed with CURSE puts the whole gym into SHOCK (D839 bit g: 0 PEWTER, 1 CERULEAN, 2 VERMILION, 3 CELADON, 4 FUCHSIA, 5 SABRINA's,
#      6 CINNABAR (quiz trainers can't be killed), 7 VIRIDIAN). While the LEADER is alive: the gym trainers who haven't fought yet say a new "what did you do to our
#      teammate / I'll avenge them" line before the battle, the ones already beaten tell you to get out; the LEADER has his/her own line for the dead students.
#      If the LEADER is dead, v14's revenge line keeps priority (nothing changes there).
#   2. SULK: a gym trainer (or leader) you beat while using CURSE on their POKeMON but spared (RUN in the trainer phase) tells you, when talked to again,
#      how evil you are and to leave (D83A-D83F: one bit per gym trainer / leader).
#   3. When the leader has been killed (kill bit) every other person in the gym is gone from the next visit on (D842 bit g is set by the first map loaded after the
#      kill that is not a gym; the gym's map load / redraws then hide everyone but the grave (object 1): picture 0, position FF). Not during the visit of the kill (v14).
# Texts are printed from bank 31. TalkToTrainer's before / after text calls go through the home stub at 0:00CE (it was v14's gym dispatcher), which far-calls
# bank 31 `rdisp`; the flags it returns say "printed" / "print the original" / "v14's per-bank code (bank:7A00) decides". EndTrainerBattle (0:32D9) far-calls `r2`, which does the original
# "set the trainer's flag" + the shock / sulk bookkeeping.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V66_SHA='953bb05ccf54e374bdc5fa71837849058e20e12e73b4ef99ab0af6d4fc770d2c'
rom=Rom('Creepy_Black_Mu_v66.gb',V66_SHA)
r=rom.r;R=bytes(r)
B31=0x31;CODE=0x7000;TXT=0x7600
assert not any(R[fo(B31,CODE):fo(B31,0x8000)])
L66={k:int(v,16) for k,v in json.load(open('manifest_v66.json'))['labels']['bank31'].items()}

# ---------------------------------------------------------------------------------------------------------------- data
GYMS=[(0x36,0,12),(0x41,1,26),(0x5c,2,27),(0x86,3,28),(0x9d,4,29),(0xb2,5,30),(0xa6,6,31),(0x2d,7,32)]   # map, shock bit, leader kill index
TRAINERS=[13]+[436,437]+[438,439,440]+list(range(261,268))+list(range(499,505))+list(range(445,452))+list(range(491,499))   # gym trainers' kill indices (v29)
assert len(TRAINERS)==1+2+3+7+6+7+8
LEADERS=[g[2] for g in GYMS]
STAB=TRAINERS+LEADERS
NT=len(TRAINERS);assert len(STAB)<=48
def T(paras,end=0x58):return bytes(txt(paras,end,17))
TX={}
TX['ts0']=T([["What did you do","to our teammate?!"],["I'll avenge them!"]])
TX['ts1']=T([["You killed one of","us! MURDERER!"],["I won't let you","get away with it!"]])
TX['ts2']=T([["Our friend is","dead because of","YOU!"],["You'll pay for","this!"]])
TX['ta0']=T([["MURDERER! Get out","of our gym!"]])
TX['ta1']=T([["Our teammate is","dead... Leave!"]])
TX['ta2']=T([["I can't even look","at you! GO!"]])
TX['sk0']=T([["You are evil...","Just leave."]])
TX['sk1']=T([["Don't look at me.","What a monster...","Go away."]])
TX['sk2']=T([["Your cruelty","sickens me.","Please leave."]])
LB={ # leader's line when a gym trainer was killed ahead of time
 0:[["You killed my","student!"],["The rock stands.","Your sin won't!"]],
 1:[["You killed my","friend!"],["The water will","wash you away,","murderer!"]],
 2:[["You killed one of","my boys!"],["I'll fry you,","you monster!"]],
 3:[["My flowers wilt","at your sins..."],["You killed one of","my students!"]],
 4:[["A ninja dead by","your hand..."],["I won't make it","quick, fiend!"]],
 5:[["I foresaw the","death of my","disciple..."],["Now you will","join them!"]],
 6:[["Hahaha! You","killed my men!"],["I'll burn you","to ashes!"]],
 7:[["You killed my","men? Fool!"],["Now you face","the BOSS!"]]}
for g,p in LB.items():TX['lb%d'%g]=T(p)
TX['la']=T([["You are a","MURDERER! Leave","my gym!"]])
tx=bytearray();TXA={}
for k,v in TX.items():TXA[k]=TXT+len(tx);tx+=v
assert TXT+len(tx)<0x7e00
rom.put(fo(B31,TXT),bytes(tx),'Bank 31: v67 gym shock / sulk texts')

# ---------------------------------------------------------------------------------------------------------------- code
gt=''.join(f'    db {m},{g},{k&255},{k>>8}\n' for m,g,k in GYMS)
st=''.join(f'    dw {k}\n' for k in STAB)
SRC=f'''
; ---- helpers (all keep every register but a and the flags)
bitmask:                         ; a = n (0-7) -> a = 1 << n   (uses b)
    ld b,a
    ld a,1
    inc b
    jr .e
.l: add a
.e: dec b
    jr nz,.l
    ret
killtest:                        ; hl = kill index -> carry = the kill bit is set
    push bc
    push de
    ld a,h
    and a
    ld de,$d4a4
    jr z,.g
    ld de,$d430
.g: ld a,l
    srl a
    srl a
    srl a
    add e
    ld e,a
    jr nc,.n
    inc d
.n: ld a,l
    and 7
    ld b,a
    inc b
    ld a,[de]
.s: rrca
    dec b
    jr nz,.s
    pop de
    pop bc
    ret
gymfind:                         ; a = map -> carry = a gym, hl -> its entry (map, shock bit, leader index lo, hi)
    push bc
    ld c,a
    ld hl,gtab
.l: ld a,[hl]
    cp $ff
    jr z,.nf
    cp c
    jr z,.f
    inc hl
    inc hl
    inc hl
    inc hl
    jr .l
.f: pop bc
    scf
    ret
.nf:pop bc
    and a
    ret
stabfind:                        ; hl = kill index -> carry = a gym trainer / leader, b = its position in the table
    push de
    ld de,stab
    ld b,0
.l: ld a,[de]
    inc de
    ld c,a
    ld a,[de]
    inc de
    cp $ff
    jr z,.nf
    cp h
    jr nz,.nx
    ld a,c
    cp l
    jr z,.f
.nx:inc b
    jr .l
.f: pop de
    scf
    ret
.nf:pop de
    and a
    ret
pick:                            ; hl = table of words, a = index -> hl = the word (uses a, de)
    add a
    ld e,a
    ld d,0
    add hl,de
    ld a,[hl+]
    ld h,[hl]
    ld l,a
    ret
var3:                            ; a = (low byte of the fought trainer's kill index) mod 3
    ld a,[$d4af]
    and 3
    cp 3
    ret nz
    xor a
    ret

; ---- EndTrainerBattle (0:32D9, far call): the original "set the trainer's flag", then the shock / sulk bookkeeping; ends like the original (a = class, cp $c8)
r2:
    ld a,[$cc55]
    ld c,a
    ld b,1
    call $31fc
    ld a,[$d35e]
    call gymfind
    jr nc,.done
    push hl
    ld a,[$d4ae]
    ld h,a
    ld a,[$d4af]
    ld l,a
    call stabfind
    pop de                       ; de -> gym entry
    jr nc,.done
    call killtest
    jr nc,.spared
    ld a,b                       ; killed with CURSE: the leader's own kill is v14's business
    cp {NT}
    jr nc,.done
    inc de
    ld a,[de]
    call bitmask
    ld c,a
    ld a,[$d839]
    or c
    ld [$d839],a
    jr .done
.spared:
    ld a,[$d452]                 ; CURSE was used this battle but the trainer lives: sulks from now on
    and a
    jr z,.done
    ld a,b
    srl a
    srl a
    srl a
    ld e,a
    ld d,0
    ld hl,$d83a
    add hl,de
    ld a,b
    and 7
    call bitmask
    ld c,a
    ld a,[hl]
    or c
    ld [hl],a
.done:
    ld a,[$d713]
    cp $c8
    ret

; ---- TalkToTrainer's text (called through the home stub 0:00CE with the original text pointer on the stack; flags back to the stub: C = printed it here,
;      Z = nothing new (the stub prints the original text), NZ and NC = v14's revenge code (leader dead, trainer not beaten) decides)
rdisp:
    ld a,d                       ; the stub passes C (0 = before the battle, else the trainer has been beaten) in D: the trainer header lives in the map's
    ld [$d845],a                 ; bank, which is not mapped here
    ld a,[$d35e]
    call gymfind
    jp nc,.van
    inc hl
    ld a,[hl+]
    ld [$d846],a                 ; this gym's shock bit
    ld a,[hl+]
    ld c,a
    ld a,[hl]
    ld b,a
    ld h,b
    ld l,c                       ; bc = hl = the leader's kill index
    call killtest
    jp c,.dead                   ; the leader is dead: v14's revenge line decides (before the battle only)
    ld a,[$d846]
    ld e,a
    ld a,[$d839]
    inc e
.sh:rrca
    dec e
    jr nz,.sh
    db $9f                       ; sbc a,a
    ld d,a                       ; d = $FF when the gym is in shock
    ld a,[$d4ae]
    cp b
    jr nz,.nl
    ld a,[$d4af]
    cp c
    jr nz,.nl
    ld e,1                       ; e = 1: the leader
    jr .go
.nl:ld e,0
.go:ld a,[$d845]
    and a
    jr nz,.after
    ld a,d                       ; before the battle: only a shocked gym says anything new
    and a
    jp z,.van
    ld a,e
    and a
    jr nz,.lb
    call var3
    ld hl,tshock
    call pick
    jr .say
.lb:ld a,[$d846]
    ld hl,lshock
    call pick
    jr .say
.after:
    ld a,d
    and a
    jr z,.sulk
    ld a,e
    and a
    jr nz,.la
    call var3
    ld hl,tafter
    call pick
    jr .say
.la:ld hl,{TXA['la']:#x}
    jr .say
.sulk:
    ld a,[$d4ae]
    ld h,a
    ld a,[$d4af]
    ld l,a
    call stabfind
    jr nc,.van
    ld a,b
    srl a
    srl a
    srl a
    ld e,a
    ld d,0
    ld hl,$d83a
    add hl,de
    ld a,b
    and 7
    call bitmask
    and [hl]
    jr z,.van
    call var3
    ld hl,tsulk
    call pick
.say:
    call $3c94                   ; PrintText, from bank 31
    scf
    ret
.dead:
    ld a,[$d845]
    and a
    jr nz,.van
    or 1                         ; NZ, NC: v14's code
    ret
.van:
    xor a                        ; Z, NC: the original text
    ret

; ---- map load / redraw: a gym whose leader died is abandoned once the player has been out of it (D842 bit g = armed; set by armall on the next non-gym map):
;      everybody but the grave (object 1) is gone. During the visit in which the leader died nobody leaves (v14: the trainers swear revenge).
gymhide:
    ld a,[$d35e]
    call gymfind
    jp nc,armall
    inc hl
    ld a,[hl+]
    ld e,a                       ; the gym's bit
    ld a,[hl+]
    ld c,a
    ld a,[hl]
    ld h,a
    ld l,c
    call killtest
    ret nc                       ; the leader lives
    ld a,e
    call bitmask
    ld c,a
    ld a,[$d842]
    and c
    ret z                        ; not armed: the leader died during this visit
    ld a,[$d4e1]
    cp 2
    ret c
    ld b,a
    ld c,2
.l: ld a,c
    swap a
    ld e,a
    ld d,$c1
    xor a
    ld [de],a
    inc d
    ld a,e
    add 4
    ld e,a
    ld a,$ff
    ld [de],a
    inc e
    ld [de],a
    inc c
    ld a,b
    cp c
    jr nc,.l
    ret
armall:                          ; not a gym: every gym whose leader is dead becomes abandoned
    ld hl,gtab
.l: ld a,[hl]
    cp $ff
    ret z
    push hl
    inc hl
    ld a,[hl+]
    ld e,a
    ld a,[hl+]
    ld c,a
    ld a,[hl]
    ld h,a
    ld l,c
    call killtest
    jr nc,.n
    ld a,e
    call bitmask
    ld c,a
    ld a,[$d842]
    or c
    ld [$d842],a
.n: pop hl
    inc hl
    inc hl
    inc hl
    inc hl
    jr .l
im67:                            ; InitMapSprites stub (5:7FD0): the town shamanesses (v63/v66), then the abandoned gyms
    call {L66['app66']:#x}
    jp gymhide

gtab:
{gt}    db $ff
stab:
{st}    dw $ffff
tshock: dw {','.join('%#x'%TXA['ts%d'%i] for i in range(3))}
tafter: dw {','.join('%#x'%TXA['ta%d'%i] for i in range(3))}
tsulk:  dw {','.join('%#x'%TXA['sk%d'%i] for i in range(3))}
lshock: dw {','.join('%#x'%TXA['lb%d'%i] for i in range(8))}
'''
code,L=asm(SRC,CODE,{})
assert CODE+len(code)<TXT,hex(CODE+len(code))
rom.put(fo(B31,CODE),code,'Bank 31: v67 gym shock mode (r2, rdisp, gymhide, tables)')

# ---------------------------------------------------------------------------------------------------------------- hooks
# 1. home 0:00CE: v14's gym dispatcher -> push hl, de / ld d,c / far call rdisp / pop de, hl / ret c (printed) / jp nz 7A00 (v14 revenge) / jp PrintText (original)
o=0xce;old=R[o:o+18];assert old.hex()=='f0b8fe172809fe1228 05fe1dc2943cc3007a'.replace(' ',''),old.hex()
new=bytes([0xe5,0xd5,0x51,0x21])+L['rdisp'].to_bytes(2,'little')+bytes([0x06,B31,0xcf,0xd1,0xe1,0xd8,0xc2,0x00,0x7a,0xc3,0x94,0x3c])
rom.code(o,new+bytes(18-len(new)),'Home 0:00CE: TalkToTrainer text dispatch -> far call to bank 31 rdisp (shock / sulk; v14 revenge as fallback)',old.hex(),
         reviewed='v14 stub body replaced; its only entry is 0:00CE (call from TalkToTrainer); the stub reproduces the old tail jp 7A00 / jp PrintText')
# 2. TalkToTrainer's after-battle text: jp PrintText -> the same dispatcher
o=0x322c;assert R[o:o+3].hex()=='c3943c'
rom.hook(o,'c3ce00','TalkToTrainer: after-battle text through the dispatcher','c3943c',
         reviewed='a tail jp replaced by a tail jp; the dispatcher ends in PrintText (or returns to the caller like it)')
# 3. EndTrainerBattle: ld b,1 / call 31FC / ld a,[D713] / cp C8  -> far call to r2 (which ends with the same cp C8; the jr nc after it is untouched)
o=0x32d9;old=R[o:o+10];assert old.hex()=='0601cdfc31fa13d7fec8',old.hex()
rom.code(o,bytes([0x21])+L['r2'].to_bytes(2,'little')+bytes([0x06,B31,0xcf])+bytes(4),'EndTrainerBattle: set flag + class test -> far call to bank 31 r2 (shock / sulk bookkeeping)',old.hex(),
         reviewed='r2 repeats the replaced instructions; the flags of its final cp $C8 reach the untouched jr nc')
# 4. InitMapSprites stub (5:7FD0): app66 -> im67 (app66, then the abandoned gyms)
o=fo(5,0x7fd0);assert R[o:o+3].hex()=='21'+le(L66['app66'])
rom.data(o+1,L['im67'].to_bytes(2,'little'),'InitMapSprites stub -> im67 (shamanesses, abandoned gyms)',le(L66['app66']))

# 5. The LEADERS do not use TalkToTrainer: each gym's text script prints the pre-battle speech with  ld hl,TEXT / call PrintText  (right before  ld hl,D72D / set 6 / set 7).
#    That call goes through a small stub in the gym's bank: shocked gym (D839 bit g) -> TX_FAR to the leader's own line in bank 31, else the original text.
LEADER_CALLS=[(0x17,0x4477,0),(0x17,0x47a5,1),(0x17,0x4b51,2),(0x17,0x514c,5),(0x12,0x4a30,3),(0x1d,0x5553,4),(0x1d,0x4aa3,7)]   # bank, the call, shock bit
FREE={0x17:0x7d0c,0x12:0x7b26,0x1d:0x7f48}
for bank,call_at,g in LEADER_CALLS:
    o=fo(bank,call_at);assert R[o:o+3].hex()=='cd943c' and R[o+3:o+6].hex()=='212dd7',(hex(bank),hex(call_at))
    a=FREE[bank];far=a+13;assert not any(R[fo(bank,a):fo(bank,a)+18])
    stub=bytes([0xfa,0x39,0xd8,0xcb,0x47+8*g,0x28,0x03,0x21])+far.to_bytes(2,'little')+bytes([0xc3,0x94,0x3c])
    assert len(stub)==13
    stub+=bytes([0x17])+TXA['lb%d'%g].to_bytes(2,'little')+bytes([B31,0x50])
    rom.put(fo(bank,a),stub,'Bank %02X: v67 leader pre-battle text stub (gym shock bit %d)'%(bank,g))
    rom.hook(o,'cd'+le(a),'Gym leader (shock bit %d): pre-battle text through the shock stub'%g,'cd943c',provides=('h','l'),reviewed='the stub swaps hl (the text) on purpose and tail-jumps to PrintText; nothing else changes')
    FREE[bank]=a+18
rom.finish('Creepy_Black_Mu_v67.gb','manifest_v67.json','CREEPY MU V67',extra=dict(labels=dict(bank31={k:hex(v) for k,v in L.items()})))
