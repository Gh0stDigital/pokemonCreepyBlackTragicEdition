# Creepy Black Mu v30: GHOST's hunger gives warnings, and it eats the Pokemon next to it.
#   Steps left until GHOST feeds = 6 * hunger - step counter (the v2 engine takes 1 hunger every 6 steps and feeds when it
#   reaches 0). At exactly 100 / 50 / 25 steps left a message pops up:
#     100  "GHOST seems to be getting restless..."
#      50  "<victim> seems anxious about something."   (the Pokemon that will be eaten; the player's name if it is you)
#      25  "You sense a malicious intent..."
#   Victim: the party member right in front of GHOST (the slot above it); if GHOST leads, the one just below it. No other
#   member: GHOST eats the player (black screen, GENGAR's cry, save erased, back to the title screen) as before, but with
#   GENGAR's cry instead of GHOST's. Without GHOST in the party (deposited for a MIRAGE fight) the old rule stays: the last
#   member. Everything else (drain, feeding, hunger 12 after a meal, off for BLACK) is unchanged.
# Hooks: hunger_wrap (2D:44C9, v25) far-calls hunger2 instead of the v2 engine (2E:4100); DisplayTextID's init far call
# goes to npc_talk2, which prints a hunger message (text id F1-F3) or continues into v28's npc_talk.
# Logged patches on top of verified Mu v29 (patchlib); new code in bank 2D (sm83asm).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V29_SHA='f7de0e9dd4627fa85621ac320c41a0d5dc285fafe064e7e84e79c79e57718e68'
rom=Rom('Creepy_Black_Mu_v29.gb',V29_SHA)
r=rom.r;R=bytes(r)
BANK=0x2d;CODE=0x5e00
GHOST,GENGAR=0x1f,0x0e
HUNGER,STEP,TEMP=0xd455,0xd456,0xd457
MSGID=0xf1                                            # text ids F1-F3 = hunger messages (no map text table is that long)
NPC_TALK=int(json.load(open('manifest_v28.json'))['labels']['bank2d']['npc_talk'],16)
HUNGER_WRAP=int(json.load(open('manifest_v25.json'))['labels']['bank2d']['hunger_wrap'],16)
assert R[fo(BANK,NPC_TALK):fo(BANK,NPC_TALK)+8]==bytes.fromhex('218f700601cd1836')        # farcall DisplayTextIDInit
assert R[fo(BANK,HUNGER_WRAP)+5:fo(BANK,HUNGER_WRAP)+10]==bytes.fromhex('2100 41062e'.replace(' ',''))

TXT={
 'restless':[["GHOST seems to","be getting","restless..."]],
 'malice':[["You sense a","malicious","intent..."]],
}
SRC=f'''
hunger2:                          ; one overworld step (v2 rules + warnings + new victim)
    ld a,[$d451]
    and a
    ret z
    ld a,[$d730]
    bit 7,a
    ret nz
    ld hl,{STEP}
    inc [hl]
    ld a,[hl]
    cp 6
    jr c,.warn
    ld [hl],0
    ld hl,{HUNGER}
    ld a,[hl]
    and a
    jr z,eat
    dec [hl]
    jr z,eat
.warn:                            ; steps left = 6*hunger - counter
    ld a,[{HUNGER}]
    ld l,a
    ld h,0
    ld d,h
    ld e,l
    add hl,hl
    add hl,de
    add hl,hl
    ld a,[{STEP}]
    ld e,a
    ld a,l
    sub e
    ld l,a
    ld a,h
    sbc 0
    ret nz
    ld a,l
    ld b,1
    cp 100
    jr z,.msg
    inc b
    cp 50
    jr z,.msg
    inc b
    cp 25
    ret nz
.msg:
    ld a,b
    ld [{TEMP}],a
    cp 2
    jr nz,.show
    call victim                   ; the victim's name for "... seems anxious"
    ld hl,$d158
    cp $ff
    jr z,.name
    ld bc,11
    ld hl,$d2b5
.nm:and a
    jr z,.name
    add hl,bc
    dec a
    jr .nm
.name:
    ld de,$cd6d
    ld bc,11
    call $00b5
.show:
    ld a,[{TEMP}]
    add {MSGID-1}
    ldh [$8c],a
    jp $294d

eat:
    call victim
    cp $ff
    jr z,eat_player
    ld [$cf92],a
    ld e,a
    ld d,0
    ld hl,$d164
    add hl,de
    ld a,[hl]
    ld [{TEMP}],a
    farcall $418c,$2e             ; black screen
    ld a,[{TEMP}]
    call $13ff                    ; the victim's cry
    xor a
    ld [$cf95],a
    farcall $7b61,1               ; RemovePokemon (wWhichPokemon)
    ld c,40
    call $3773
    farcall $41a8,$2e
    ld a,12
    ld [{HUNGER}],a
    ret
eat_player:
    farcall $418c,$2e
    ld a,{GENGAR}
    call $13ff                    ; GENGAR's cry
    ld c,120
    call $3773
    ld a,$0a                      ; erase all 4 SRAM banks, cold restart (as v2)
    ld [$0000],a
    ld b,4
.bank:
    dec b
    ld a,b
    ld [$4000],a
    ld hl,$a000
.fill:
    xor a
    ld [hl+],a
    ld a,h
    cp $c0
    jr nz,.fill
    ld a,b
    and a
    jr nz,.bank
    xor a
    ld [$0000],a
    jp $0100

victim:                           ; a = party index GHOST will eat, $FF = the player
    ld a,[$d163]
    ld b,a
    ld hl,$d164
    ld c,0
.f: ld a,c
    cp b
    jr nc,.noghost
    ld a,[hl+]
    cp {GHOST}
    jr z,.g
    inc c
    jr .f
.g: ld a,c
    and a
    jr z,.below
    dec a                         ; the one in front of GHOST
    ret
.below:
    ld a,b
    cp 2
    jr c,.player
    ld a,1                        ; GHOST leads: the one just below
    ret
.noghost:                         ; GHOST not in the party: the last member (v2 rule)
    ld a,b
    and a
    jr z,.player
    dec a
    ret
.player:
    ld a,$ff
    ret

npc_talk2:                        ; DisplayTextID init: hunger message pending?
    farcall $708f,1
    ldh a,[$8c]
    sub {MSGID}
    jp c,{NPC_TALK+8}
    cp 3
    jp nc,{NPC_TALK+8}
    and a
    ld hl,t_restless
    jr z,.p
    dec a
    ld hl,t_anxious
    jr z,.p
    ld hl,t_malice
.p: call $3c94
    ld hl,sp+4                    ; done: DisplayTextID continues at "wait for A released", then closes
    ld a,$0c
    ld [hl+],a
    ld a,$2a
    ld [hl],a
    ret
t_anxious:
    db $01,$6d,$cd,$00,$4f
    db {",".join(str(x) for x in enc("seems anxious"))},$55
    db {",".join(str(x) for x in enc("about something."))},$58
t_restless:
    db {",".join(str(x) for x in txt(TXT["restless"]))}
t_malice:
    db {",".join(str(x) for x in txt(TXT["malice"]))}
'''
code,L=asm(SRC,CODE)
assert CODE+len(code)<0x6400,hex(CODE+len(code))
rom.put(fo(BANK,CODE),code,'Bank 2D: v30 hunger engine (warnings, victim next to GHOST, GENGAR cry) + hunger message printer')
rom.data(fo(BANK,HUNGER_WRAP)+5,bytes.fromhex('21'+le(L['hunger2'])+'06%02x'%BANK),'hunger_wrap: far call hunger2 (2D) instead of the v2 engine (2E:4100)','210041062e')
rom.code(0x2950,bytes([0x06,BANK,0x21])+L['npc_talk2'].to_bytes(2,'little'),'DisplayTextID: init call -> npc_talk2 (hunger messages, then v28 npc_talk)',
         bytes([0x06,BANK,0x21])+NPC_TALK.to_bytes(2,'little'),reviewed='operand bytes of the call setup; no jumps land inside 0x2950-0x2954 (checked in v28)')
rom.finish('Creepy_Black_Mu_v30.gb','manifest_v30.json','CREEPY MU V30',extra=dict(labels=dict(bank2d={k:hex(v) for k,v in L.items()})))
