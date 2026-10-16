# Creepy Black Mu v69: every ordinary (non-gym) trainer you used CURSE on but spared SULKS afterwards.
#   Talking to them again after the battle gives a different after-battle line: they tell you to leave, are scared of you, some swear they won't tell anyone.
#   16 different lines, picked by the trainer's kill index, so neighbours on a route don't say the same thing.
#   Gym trainers / leaders keep v67's sulk lines. Scripted trainers (no trainer header: rivals, grunts in scripted fights) are not covered.
# ALSO FIXES A v67 BUG: the far call in EndTrainerBattle destroyed hl, the flag address that TrainerFlagAction needs, so no trainer was marked beaten after a win and
#   challenged again (the v67 tests set the flags by hand and never saw it). The home code now pushes hl; r69 sets the flag itself.
# Bookkeeping: a "sulk" bit per kill index (336 bits = 42 bytes) lives in five runs of event-flag bytes that no code and no trainer header refers to
#   (D784-D78D, D7A4-D7AE, D80A-D812, D84F-D856, D858-D85E).
#   rdisp69 (the dispatcher the home stub 0:00CE calls) notes "a header trainer is fighting" (D844) before the battle and prints the line after it;
#   r69 (EndTrainerBattle's far call) sets the bit when CURSE was used (D452) and the trainer is alive.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V68_SHA='fcb986bb67fb924bfc1ded661525b3c15a1615c4b9e02a009ace2084a7d316f0'
rom=Rom('Creepy_Black_Mu_v68.gb',V68_SHA)
R=bytes(rom.r)
B31=0x31;CODE=0x7e00;TXT=0x7a00
assert not any(R[fo(B31,TXT):fo(B31,0x8000)])
L67={k:int(v,16) for k,v in json.load(open('manifest_v67.json'))['labels']['bank31'].items()}
def T(paras):return bytes(txt(paras,0x58,17))
LINES=[
 [["Please just go.","I won't tell","anyone, I swear."]],
 [["Stay away from","me. I saw what","that thing did."]],
 [["...I'm still","shaking. Leave","me alone."]],
 [["You're evil.","I won't say a","word. Just go."]],
 [["I'd rather lose","again than see","that again."]],
 [["Don't talk to","me. Don't look","at me."]],
 [["Nobody will hear","it from me.","Please, go."]],
 [["What are you?!","Get away from","me!"]],
 [["I keep seeing","its eyes... Just","leave."]],
 [["I should tell","someone... but","I'm too scared."]],
 [["Whatever you do,","do it far from","me."]],
 [["I'm done with","battles. Done.","Leave."]],
 [["My hands won't","stop shaking.","Go away."]],
 [["You frighten me.","I'll keep quiet.","Just go."]],
 [["...monster.","I won't tell. I","just want to","forget."]],
 [["Not a word, I","promise. Not a","word. Now go."]]]
assert len(LINES)==16
tx=bytearray();TA=[]
for l in LINES:TA.append(TXT+len(tx));tx+=T(l)
assert TXT+len(tx)<0x7e00
rom.put(fo(B31,TXT),bytes(tx),'Bank 31: v69 ordinary trainers\' sulk lines')
CH=[(0xd784,10),(0xd7a4,11),(0xd80a,9),(0xd84f,8),(0xd858,7)]
assert sum(n for a,n in CH)>=42
chunks=''.join(f'    dw {a:#x}\n    db {n}\n' for a,n in CH)
tl=''.join(f'    dw {a:#x}\n' for a in TA)
SRC=f'''
sulkbit:                         ; hl = kill index -> hl = the byte's address, a = the bit's mask (all other registers kept)
    push bc
    push de
    ld a,l
    srl a
    srl a
    srl a
    ld e,a
    ld a,h
    and a
    jr z,.lo
    ld a,e
    add 10
    ld e,a
.lo:
    ld a,l
    and 7
    call bitmask
    push af
    ld hl,chunks
.c:
    ld a,[hl+]
    ld c,a
    ld a,[hl+]
    ld b,a
    ld a,[hl+]
    ld d,a
    ld a,e
    cp d
    jr c,.f
    sub d
    ld e,a
    jr .c
.f:
    ld h,b
    ld l,c
    ld d,0
    add hl,de
    pop af
    pop de
    pop bc
    ret
chunks:
{chunks}
gtexts:
{tl}
; ---- the dispatcher (home stub 0:00CE far-calls this instead of v67's rdisp; same flags back: C = printed, Z = original text, NZ+NC = v14's code)
rdisp69:
    ld a,d
    and a
    jr nz,.nb
    ld a,1                       ; before the battle: a header trainer is about to fight
    ld [$d844],a
.nb:
    call rdisp
    ret c
    ret nz
    ld a,[$d845]                 ; rdisp kept the stub's D here: 0 = before the battle
    and a
    jr z,.van
    ld a,[$d4ae]
    ld h,a
    ld a,[$d4af]
    ld l,a
    or h
    jr z,.van                    ; kill index 0: can't be killed, no sulking
    call sulkbit
    and [hl]
    jr z,.van
    ld a,[$d4af]
    and 15
    ld hl,gtexts
    call pick
    call $3c94
    scf
    ret
.van:
    xor a
    ret
; ---- EndTrainerBattle's far call: v67's r2, then the sulk bookkeeping for ordinary trainers; ends with the original  ld a,[D713] / cp $C8
r69:
    ld hl,sp+6                   ; [sp+6] = the flag address the home code pushed (hl was clobbered by the far call itself): set the trainer's flag the way the original does
    ld a,[hl+]
    ld h,[hl]
    ld l,a
    ld a,[$cc55]
    ld c,a
    ld b,1
    call $31fc
    call {L67['r2']+9:#x}        ; the rest of v67's r2 (gym bookkeeping)
    ld a,[$d844]
    and a
    jr z,.end
    xor a
    ld [$d844],a
    ld a,[$d35e]
    call gymfind
    jr c,.end                    ; gyms: v67
    ld a,[$d452]
    and a
    jr z,.end                    ; no CURSE this battle
    ld a,[$d4ae]
    ld h,a
    ld a,[$d4af]
    ld l,a
    or h
    jr z,.end
    call killtest
    jr c,.end                    ; dead
    call sulkbit
    ld c,a
    ld a,[hl]
    or c
    ld [hl],a
.end:
    ld a,[$d713]
    cp $c8
    ret
'''
code,L=asm(SRC,CODE,dict(L67))
assert CODE+len(code)<=0x8000
rom.put(fo(B31,CODE),code,'Bank 31: v69 sulk bits + dispatcher/EndTrainerBattle wrappers')
# home stub 0:00CE: rdisp -> rdisp69 ; EndTrainerBattle: r2 -> r69
o=0xd1+0;assert R[0xd1:0xd4].hex()=='21'+L67['rdisp'].to_bytes(2,'little').hex()
rom.data(0xd2,L['rdisp69'].to_bytes(2,'little'),'Home stub 0:00CE -> rdisp69 (ordinary trainers\' sulk)',L67['rdisp'].to_bytes(2,'little').hex())
assert R[0x32d9:0x32df].hex()=='21'+L67['r2'].to_bytes(2,'little').hex()+'0631cf'
assert R[fo(B31,L67['r2']+9):fo(B31,L67['r2']+9)+3].hex()=='fa5ed3'
rom.code(0x32d9,bytes([0xe5,0x21])+L['r69'].to_bytes(2,'little')+bytes([0x06,B31,0xcf,0xe1,0,0]),'EndTrainerBattle: push hl around the far call (v67 lost the flag address: trainers were never marked beaten)','21'+L67['r2'].to_bytes(2,'little').hex()+'0631cf00000000',
         reviewed='hl (the flag address from ReadTrainerHeaderInfo) is pushed, r69 reads it from the stack and sets the flag, pop hl after the call; the cp $C8 flags of r69 reach the untouched jr nc')
rom.finish('Creepy_Black_Mu_v69.gb','manifest_v69.json','CREEPY MU V69',extra=dict(labels=dict(bank31={k:hex(v) for k,v in {**L67,**L}.items()})))
