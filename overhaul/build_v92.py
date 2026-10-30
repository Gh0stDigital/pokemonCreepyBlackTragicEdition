# Creepy Black Mu v92: the Mansion MR. MU talks more (on v91).
#   First talk: "I didn't expect to see you here ... the key to the GYM?" -> he gives the SECRET KEY (not again if the bag has one);
#   then he checks the bag for the OLD AMBER: with it "you are quite resourceful ..." + the v52 AMBER question; without it nothing more.
#   Later talks: a warning about digging too deep in the mansion (after the AMBER was given to him: one more kind line).
#   Once the AMBER question was answered (D885 bit1) he is gone after the next map load (D460 = 4). Giving the AMBER no longer
#   removes him at once (D460 stays 3 until the next map load). D885: bit0 key/intro done, bit1 question answered, bit2 AMBER given.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V91_SHA='32624ec9639b60dcba59d009b5a157ae3ecc60e28d2baf2007c95d949d192bf8'
rom=Rom('Creepy_Black_Mu_v91.gb',V91_SHA)
R=bytes(rom.r)
L38={k:int(v,16) for k,v in json.load(open('manifest_v38.json'))['labels']['bank2d'].items()}
M2=json.load(open('manifest_v2.json'))['labels_bank2e']
BLACK_ON,BLACK_OFF=int(M2['black_on'],16),int(M2['black_off'],16)
M52=json.load(open('manifest_v52.json'))['labels']
GIVE_AZHI=int(M52['bank2d']['give_azhi'],16)
PRINTTEXT,TEXTSCRIPTEND,MENU,PLAYSOUND,BANKSW=0x3c94,0x2504,0x3af2,0x23de,0x3618
MU2,FL=0xd460,0xd885
AMBER,SKEY,HEALED=0x1f,0x2b,0xe8
def tx(paras,end=0x58,maxw=17):return bytes(txt(paras,end,maxw))
T={'t_intro':tx([["Oh, <PLAYER>.","I didn't expect","to see you here."],
                 ["This place holds","many old secrets","that scientists","would rather","forget."],
                 ["I'm not sure what","you hope to find","here..."],
                 ["Oh? The key to","the GYM?","Hmm, I see..."],
                 ["Take this, then."]]),
   't_intro2':tx([["Oh, <PLAYER>.","I didn't expect","to see you here."],
                  ["This place holds","many old secrets","that scientists","would rather","forget."],
                  ["I'm not sure what","you hope to find","here..."],
                  ["Oh? The key to","the GYM? You are","carrying it","already. Good."]]),
   't_gave':tx([["<PLAYER> received","SECRET KEY!"]]),
   't_after':tx([["This is what you","need, right?","Go on, take it."],["You need it to","complete your","journey, after","all."]]),
   't_nokey':tx([["...but your pack","is full."],["Make room, then","come back to me."]]),
   't_check':tx([["My, <PLAYER>.","You are quite","resourceful."],["You have the","AMBER in your","possession too","now..."],["Could you humor","me with an answer","to another","question?"]]),
   't_question':tx([["OLD AMBER! A drop","of sap that holds","the breath of the","sky."],["Tell me","something."],["If the dead could","speak..."],["do you believe","they would ask","to return?"]]),
   't_menu':tx([[" THEY WOULD NOT"," THEY WOULD"]],0x57,18),
   't_no':tx([["Hm."],["Then why carry","a drop of sap","from so long ago?"]]),
   't_full':tx([["...I see."],["But you have no","room for it."],["Make room in your","party first."]]),
   't_yes':tx([["...I see."],["Then perhaps this","shouldn't remain","amber."]]),
   't_got':tx([["Something stirred","inside the","amber..."],["<PLAYER> received","AZHI!"]]),
   't_warn':tx([["Be careful not to","dig too deep in","this mansion."],["Many of the old","experiments still","linger here."]]),
   't_warn2':tx([["Be careful not to","dig too deep in","this mansion."],["Many of the old","experiments still","linger here."],["If something is","troubling you,","don't worry too","hard."],["Just focus on the","goal at hand and","everything will","work out."]])}
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())
BANK=0x32;CODE=0x7000
assert not any(R[fo(BANK,CODE):fo(BANK,CODE+0x700)])
code,L=asm(f'''
; bag scan: a = item id, returns z = found
hasitem:
    ld b,a
    ld a,[$d31d]
    and a
    jr nz,.has
    or 1
    ret
.has:
    ld c,a
    ld hl,$d31e
.l: ld a,[hl+]
    cp b
    ret z
    inc hl
    dec c
    jr nz,.l
    or 1
    ret
mu92:
    ld a,[{FL:#x}]
    bit 0,a
    jr nz,.checked
    ld a,{SKEY}
    call hasitem
    jr nz,.give
    ld hl,t_intro2
    call {PRINTTEXT:#x}
    jr .done0
.give:
    ld a,[$d31d]
    cp 20
    jr c,.room
    ld hl,t_intro
    call {PRINTTEXT:#x}
    ld hl,t_nokey
    call {PRINTTEXT:#x}
    jp {TEXTSCRIPTEND:#x}
.room:
    ld hl,t_intro
    call {PRINTTEXT:#x}
    ld bc,{SKEY<<8|1:#x}
    call $3e82
    ld hl,t_gave
    call {PRINTTEXT:#x}
    ld hl,t_after
    call {PRINTTEXT:#x}
.done0:
    ld hl,{FL:#x}
    set 0,[hl]
    ld a,{AMBER}
    call hasitem
    jp nz,.end
    ld hl,t_check
    call {PRINTTEXT:#x}
    jr .ask
.checked:
    bit 1,a
    jp nz,.warn
    ld a,{AMBER}
    call hasitem
    jp nz,.warn
    ld hl,t_check
    call {PRINTTEXT:#x}
.ask:
    ld hl,t_question
    call {PRINTTEXT:#x}
    ld hl,t_menu
    call {PRINTTEXT:#x}
    xor a
    ld [$cc26],a
    ld [$cc2a],a
    ld [$cc35],a
    ld [$cc37],a
    ld [$cc4a],a
    ld a,$0e
    ld [$cc24],a
    ld a,1
    ld [$cc25],a
    ld [$cc28],a
    ld [$cc29],a
    ldh a,[$f6]
    res 1,a
    ldh [$f6],a
    call {MENU:#x}
    ld a,[$cc26]
    and a
    jr nz,.yes
    ld hl,{FL:#x}
    set 1,[hl]
    ld hl,t_no
    call {PRINTTEXT:#x}
    jp {TEXTSCRIPTEND:#x}
.yes:
    ld a,[$d163]
    cp 6
    jr c,.rm2
    ld hl,t_full
    call {PRINTTEXT:#x}
    jp {TEXTSCRIPTEND:#x}
.rm2:
    ld hl,t_yes
    call {PRINTTEXT:#x}
    ld a,{AMBER}
    ldh [$db],a
    farcall $7f51,5              ; RemoveItemByID
    farcall {BLACK_ON:#x},$2e
    ld a,{HEALED}
    ld [$c0ee],a
    call {PLAYSOUND:#x}
    ld d,200
.w: ld c,1
    call $3773
    ld a,[$c026]
    cp {HEALED}
    jr nz,.wd
    dec d
    jr nz,.w
.wd:
    ld a,[$d35b]
    ld [$c0ee],a
    call {PLAYSOUND:#x}
    farcall {BLACK_OFF:#x},$2e
    farcall {GIVE_AZHI:#x},$2d
    ld hl,{FL:#x}
    set 1,[hl]
    set 2,[hl]
    ld hl,t_got
    call {PRINTTEXT:#x}
    jp {TEXTSCRIPTEND:#x}
.warn:
    ld a,[{FL:#x}]
    bit 2,a
    ld hl,t_warn
    jr z,.pw
    ld hl,t_warn2
.pw:
    call {PRINTTEXT:#x}
.end:
    jp {TEXTSCRIPTEND:#x}
{TXT}''',CODE)
rom.put(fo(BANK,CODE),code,'Bank 32: v92 Mansion MR. MU talk (key, AMBER check, warnings)')
# Mansion text 4 stub (11:7519, v74): its final "ld hl,mu52" -> mu92
STUB=fo(0x11,0x752a);assert R[STUB:STUB+2].hex()=='3e48' and R[STUB-1]==0x21
rom.data(STUB,bytes.fromhex(L['mu92'].to_bytes(2,'little').hex()),'Mansion MU text stub -> v92 talk','3e48')
assert R[STUB+2]==6 and R[STUB+3]==0x30
rom.data(STUB+3,bytes([BANK]),'Mansion MU text stub bank 30 -> 32','30')
# map load: after the question was answered, MR. MU is gone (D460 3 -> 4)
ML=R[fo(0x2e,0x4000):fo(0x2e,0x4003)];assert ML.hex()=='c3b042'
M=0x7700
assert not any(R[fo(0x2e,M):fo(0x2e,M+0x20)])
mc,_=asm(f'''
m92:
    ld a,[{FL:#x}]
    bit 1,a
    jr z,.o
    ld a,[{MU2:#x}]
    cp 3
    jr nz,.o
    inc a
    ld [{MU2:#x}],a
.o: jp $42b0
''',M,{})
rom.put(fo(0x2e,M),mc,'Bank 2E: v92 map load: MR. MU leaves the Mansion after the question')
rom.code(fo(0x2e,0x4000),bytes([0xc3,M&255,M>>8]),'Map load chain -> v92 first',ML.hex())
rom.finish('Creepy_Black_Mu_v92.gb','manifest_v92.json','CREEPY MU V92')
