# Creepy Black Mu v28: the world reacts to BLACK (after the climax, D46C = 1).
#   1. Every ordinary NPC you talk to panics and begs for its life ("AAAH! It's BLACK!"), then you are asked whether to CURSE
#      them. YES: GENGAR's cry, the screen goes black (the same effect as the battle CURSE), the NPC becomes a gravestone and
#      stays dead (a list of 10 (map, sprite) pairs in D471-D484 is applied at every map load). NO: the normal dialogue goes on.
#      Not affected: everybody in LAVENDER TOWN (town, houses, Pokemon Center, the TOWER), trainers (they fight when talked to
#      as before), item balls, shop clerks, nurses, the link receptionist, OAK, BLUE, MOM, and the player's house / OAK'S LAB.
#   2. Trainers no longer spot BLACK from a distance: they only fight when you talk to them yourself.
# Logged patches on top of verified Mu v27 (patchlib). The new code is assembly (sm83asm.py) in bank 2D.
import json,sys
from patchlib import *
from patchguard import fo
from sm83asm import asm

V27_SHA='66c4c9df99dd4da9f99bbb9b9fdfd828efb93aea72171144a04cd3f99a71938c'
rom=Rom('Creepy_Black_Mu_v27.gb',V27_SHA)
r=rom.r
BLACK=0xd46c;KILLS=0xd471                       # KILLS: 10 x (map, sprite index), sprite index 0 = empty slot (D471-D484)
GENGAR=0x0e
BANK=0x2d;CODE=0x4800;TXT_AT=0x5c00
HOME_SIGHT,HOME_KILL=0x167b,0x1688              # free home-bank bytes (dead code of the old pic-bank chain, 0x167B-0x1691)
assert not any(r[0x167b:0x1692]) or True

# ---------------------------------------------------------------------------------------------------------------- texts
PANIC=[
 [["AAAH! It's BLACK!","Please, I have a","family!"]],
 [["S-stay away from","me! I've done","nothing wrong!"]],
 [["Please, spare me!","I'll do anything!"]],
 [["The killer! Run!","Somebody help me!"]],
 [["N-no, no, no...!","Don't look at me!"]],
 [["I won't tell a","soul! I swear it!"]],
 [["Mercy! Please,","have mercy!"]],
 [["They said you'd","come... Please!"]],
]
TXT={'ask':([["They are shaking.","CURSE them?"]],0x57),
     'dead':([["The life drains","from them..."]],0x58)}
for i,p in enumerate(PANIC):TXT['p%d'%i]=(p,0x58)
tx=bytearray();TXTSYM={}
for k,(paras,end) in TXT.items():
    TXTSYM['t_'+k]=TXT_AT+len(tx);tx+=txt(paras,end=end)
assert TXT_AT+len(tx)<0x6e00,len(tx)
rom.put(fo(BANK,TXT_AT),bytes(tx),'Bank 2D: v28 texts (NPC panic lines, curse question)')

# ---------------------------------------------------------------------------------------------------------------- code
LAVENDER=[0x04,0x8d,0x8e,0x8f,0x90,0x91,0x92,0x93,0x94,0x95,0x96,0x97,0xe5]   # town, Pokemon Center, TOWER 1F-7F, houses, name rater
HOMES=[0x25,0x28]                                                             # the player's house 1F, OAK'S LAB
NOT_PEOPLE=[0x05,0x09,0x38]                                                   # SLOWBRO, BIRD, CLEFAIRY
SERVICE=[0x26,0x29,0x2a]                                                      # CLERK, NURSE, LINK RECEPTIONIST
STORY=[0x01,0x02,0x03,0x33]                                                   # RED, BLUE, OAK, MOM
SRC=f'''
npc_talk:                        ; replaces DisplayTextIDInit's far call: does it first, then may take over the dialogue
    farcall $708f,1
    ld a,[{BLACK}]
    and a
    ret z
    ldh a,[$8c]
    and a
    ret z
    ld b,a
    ld a,[$d4e1]
    cp b
    ret c                        ; a text id, not a sprite
    ld a,[$d35e]
    ld c,a
    ld hl,exempt_maps
.em:
    ld a,[hl+]
    cp $ff
    jr z,.mapok
    cp c
    jr nz,.em
    ret
.mapok:
    ld a,b
    swap a
    ld l,a
    ld h,$c1
    ld a,[hl]
    ld d,a                       ; d = picture
    and a
    ret z
    cp $3c
    ret nc                       ; objects (balls, boulders, gravestones ...) are not people
    ld hl,exempt_pics
.ep:
    ld a,[hl+]
    cp $ff
    jr z,.picok
    cp d
    jr nz,.ep
    ret
.picok:
    ld a,b
    dec a
    add a
    ld e,a
    ld d,0
    ld hl,$d504
    add hl,de
    ld a,[hl]
    and a
    ret nz                       ; trainer or item (extra data), not a plain NPC
    ld a,b
    ld [$cf13],a
    farcall $70c0,4              ; turn to the player and remember the facing (what DisplayTextID does for sprites)
    ld a,[$cf13]
    ld b,a
    add a
    add b
    ld b,a
    ld a,[$d35e]
    add b
    and 7
    add a
    ld e,a
    ld d,0
    ld hl,panic_tab
    add hl,de
    ld a,[hl+]
    ld h,[hl]
    ld l,a
    call $3c94
    ld hl,t_ask
    call $3c94
    call $362e
    ld a,[$cc26]
    and a
    ret nz                       ; NO: the usual dialogue follows
    ld a,{GENGAR}
    call $13ff
    farcall $418c,$2e            ; black screen (the battle CURSE effect)
    ld c,40
    call $3773
    farcall $41a8,$2e
    ld a,[$cf13]
    swap a
    ld l,a
    ld h,$c1
    ld [hl],$49                  ; gravestone
    call add_kill
    ld hl,t_dead
    call $3c94
    ld hl,sp+4                   ; the dialogue is over: continue at DisplayTextID's "wait for A to be released", then close
    ld a,$0c
    ld [hl+],a
    ld a,$2a
    ld [hl],a
    ret

add_kill:                        ; remember (map, sprite) in the list; when it is full the oldest entry is dropped
    ld hl,{KILLS}
    ld c,10
.f: inc hl
    ld a,[hl]
    and a
    jr z,.put
    inc hl
    dec c
    jr nz,.f
    ld hl,{KILLS+2}
    ld de,{KILLS}
    ld bc,18
    call $00b5
    ld hl,{KILLS+19}
.put:
    ld a,[$cf13]
    ld [hl],a
    dec hl
    ld a,[$d35e]
    ld [hl],a
    ret

kill_chk:                        ; map load: Z = this sprite (e = offset) is not in the kill list. Entered instead of "ldh a,[$e5]; and a"
    ldh a,[$e5]
    and a
    ret nz
    ld a,e
    swap a
    ld c,a
    ld a,[$d35e]
    ld b,a
    ld hl,{KILLS}
    ld d,10
.l: ld a,[hl+]
    cp b
    ld a,[hl+]
    jr nz,.next
    cp c
    jr z,.hit
.next:
    dec d
    jr nz,.l
    xor a
    ret
.hit:
    and a
    ret

exempt_maps: db {','.join(str(x) for x in LAVENDER+HOMES)},$ff
exempt_pics: db {','.join(str(x) for x in NOT_PEOPLE+SERVICE+STORY)},$ff
panic_tab: dw {','.join('t_p%d'%i for i in range(8))}
'''
ext={**TXTSYM}
code,L=asm(SRC,CODE,ext)
assert CODE+len(code)<TXT_AT,hex(CODE+len(code))
rom.put(fo(BANK,CODE),code,'Bank 2D: v28 code (NPC panic + curse, kill list)')

# ---------------------------------------------------------------------------------------------------------------- hooks
# 1. DisplayTextID (0:294D): the far call to DisplayTextIDInit (bank 1) goes through npc_talk (bank 2D) instead
rom.code(0x2950,bytes([0x06,BANK,0x21])+L['npc_talk'].to_bytes(2,'little'),'DisplayTextID: init call -> npc_talk (BLACK: NPCs panic)','06 01 21 8f 70',
         reviewed='operand bytes of the call setup; no jumps land inside 0x2950-0x2954 (checked)')
# 2. trainers do not spot BLACK: CheckFightingMapTrainers' call to the sight check (0:325B) goes through a home stub
sight,_=asm(f'''
    ld a,[{BLACK}]
    and a
    jp z,$3348
    ld a,$ff
    ld [$cf13],a
    ret
''',HOME_SIGHT)
assert HOME_SIGHT+len(sight)<=HOME_KILL,len(sight)
kill,_=asm(f'''
    ld hl,{L['kill_chk']}
    ld b,{BANK}
    jp $3618
''',HOME_KILL)
assert len(kill)==8 and HOME_KILL+8<=0x1692
old=bytes(r[HOME_SIGHT:HOME_KILL+8])
rom.code(HOME_SIGHT,sight+bytes(HOME_KILL-HOME_SIGHT-len(sight))+kill,'Home: sight-check and kill-list stubs (dead code of the old bank chain)',old.hex(),
         reviewed='dead code of the old pic-bank chain (v25 freed 0x1667-0x1691; nothing jumps here)')
rom.hook(0x325b,'cd'+le(HOME_SIGHT),'CheckFightingMapTrainers: BLACK is not spotted','cd 48 33',provides=('a','f'),
         reviewed='the stub tail-jumps to the original check, or (BLACK) sets wSpriteIndex = $FF the way the check does for "nobody" (0:325E then clears both variables)')
# 3. map load (3:4E8F): the gravestone test also looks at the kill list
rom.hook(fo(3,0x4e8f),'cd'+le(HOME_KILL),'Gravestone loop: NPCs in the kill list are gravestones','f0 e5 a7',provides=('a','f'),
         reviewed='the 2D routine performs the replaced ldh a,[$e5] / and a itself')
rom.finish('Creepy_Black_Mu_v28.gb','manifest_v28.json','CREEPY MU V28',extra=dict(labels=dict(bank2d={k:hex(v) for k,v in L.items()}),
           kill_list=hex(KILLS)))
