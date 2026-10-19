# Creepy Black Mu v84 (batch): see README_v84.txt
#   1. SNORLAX: METAMORPHOSIS in a wild battle sets D452 (CURSE used), so v73's "SNORLAX returned to the mountains" text is skipped (give84).
#   2. item balls on the ground turned into the black POKe BALL: ball_fix (v43) put the black ball into slot 0B ($8780) whenever another sprite (a gravestone, a boulder...)
#      held slot 0C - and 0B is the slot of every map's ITEM BALLS. ball84 picks a slot nobody uses (0C, 0B, then a free walker slot with the ball in all three standing frames).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V83_SHA='b50935836caa17a1988f1a92e7024dd1019bd7fad475cf2553704758517bab45'
rom=Rom('Creepy_Black_Mu_v83.gb',V83_SHA)
R=bytes(rom.r)
L43=json.load(open('manifest_v43.json'))['labels']
L40=json.load(open('manifest_v40.json'))['labels']
SHEET=int(L40['bank2f']['sheet'],16)
BALLFIX=int(L43['bank2f']['ball_fix'],16)
B2F=0x5c00
assert not any(R[fo(0x2f,B2F):fo(0x2f,B2F)+0x200])
o7=fo(0xf,0x7d20);assert R[o7:o7+5].hex()=='218f68062f'
KILL45=0x688f
L46=json.load(open('manifest_v46.json'))['labels']['bank2f']
MSG46=int(L46['msg46'],16)
assert R[fo(0xf,0x4cbc):fo(0xf,0x4cbc)+5].hex()=='21'+le(MSG46)+'062f'
START46=0xd45a
c2f,L=asm(f'''
give84:                          ; bane_move's  call give  (wild or trainer): CURSE used this battle (SNORLAX's "returned to the mountains" is skipped, trainers react)
    call $40b0
    ld a,1
    ld [$d452],a
    ret
slotused:                        ; c = slot -> carry = another sprite (not the black ball) uses it
    ld hl,$c110
    ld b,15
.l: ld a,[hl]
    and a
    jr z,.n
    cp $47
    jr z,.n
    push hl
    inc h
    ld a,l
    or $0e
    ld l,a
    ld a,[hl]
    pop hl
    cp c
    jr z,.y
.n: ld a,l
    add $10
    ld l,a
    dec b
    jr nz,.l
    and a
    ret
.y: scf
    ret
put64:                           ; hl = destination in VRAM: the ball's four tiles
    ld a,[$cfc4]
    bit 0,a
    jr nz,.vb
    ld d,h
    ld e,l
    ld hl,{SHEET:#x}
    ld bc,64
    ld a,$2f
    jp $1824
.vb:ld de,{SHEET:#x}
    ld b,$2f
    ld c,4
    jp $1875
ball84:                          ; after every InitMapSprites (v43 ball_fix, now conflict-free)
    ld hl,$c110
    ld b,15
.a: ld a,[hl]
    cp $47
    jr z,.have
    ld a,l
    add $10
    ld l,a
    dec b
    jr nz,.a
    ret
.have:
    ld c,$0c
    call slotused
    jr nc,.pick
    ld c,$0b
    call slotused
    jr nc,.pick
    ld c,$0a
.w: call slotused
    jr nc,.pick
    dec c
    ld a,c
    cp 2
    jr nc,.w
    ld c,$0c                     ; every slot is taken: as before
.pick:
    ld hl,$c110
    ld b,15
.p2:ld a,[hl]
    cp $47
    jr nz,.n2
    push hl
    inc h
    ld a,l
    or $0e
    ld l,a
    ld [hl],c
    pop hl
.n2:ld a,l
    add $10
    ld l,a
    dec b
    jr nz,.p2
    ld a,c
    cp $0c
    ld hl,$87c0
    jp z,put64
    cp $0b
    ld hl,$8780
    jp z,put64
    ld hl,$8000                  ; walker slot k: $8000 + (k-1)*$c0; the ball in the three standing frames (down, up, side)
    ld de,$00c0
    ld b,c
    dec b
.m: ld a,b
    and a
    jr z,.go
    add hl,de
    dec b
    jr .m
.go:push hl
    call put64
    pop hl
    ld de,64
    add hl,de
    push hl
    call put64
    pop hl
    ld de,64
    add hl,de
    jp put64
dam84:                           ; FaintEnemyPokemon prefix (F:7D20): v45's kill45, then DAMNATION lets the enemy faint visibly (cc39 off) and counts as a CURSE for the trainer
    call {KILL45:#x}
    ld a,[$ccdc]
    cp $ac
    ret nz
    ld a,1
    ld [$d452],a
    xor a
    ld [$cc39],a
    ret
slide84:                         ; BLACK's back picture slides in from the left edge (7 steps of one tile column), no ball, no cry
    ld b,1
.s: ld hl,$c405
    ld c,0
.c: ld a,c
    cp b
    jr nc,.blank
    ld a,7
    sub b
    add c                        ; the picture column that stands in screen column c
    ld e,a
    add a
    add a
    add a
    sub e                        ; 7 * column
    add $31
    ld d,a
    ld e,1
    jr .col
.blank:
    ld d,$7f
    ld e,0
.col:
    push hl
    push bc
    ld b,7
.r: ld a,d
    ld [hl],a
    add e
    ld d,a
    ld a,l
    add 20
    ld l,a
    jr nc,.k
    inc h
.k: dec b
    jr nz,.r
    pop bc
    pop hl
    inc hl
    inc c
    ld a,c
    cp 7
    jr c,.c
    ld a,1
    ldh [$ba],a
    push bc
    ld c,3
    call $3773
    pop bc
    inc b
    ld a,b
    cp 8
    jr c,.s
    ret
msg84:                           ; SendOutMon's message far call (F:4CBC): v46's quiet send-out also when BLACK is switched in later, with the slide
    ld a,[{START46:#x}]
    and a
    jr nz,.black
    ld a,[$d014]
    cp $7f
    jp nz,{MSG46:#x}
    ld a,2
    ld [{START46:#x}],a
.black:
    ld hl,$cfe6
    ld a,[hl+]
    or [hl]
    jr z,.p
    farcall $4e17,$0f
.p: farcall $4d8b,$0f
    ld a,4
    call $3ec1
    xor a
    ldh [$e1],a
    ld hl,$cc2d
    ld [hl+],a
    ld [hl],a
    ld [$cc5b],a
    ld [$d05b],a
    ld [$cfd2],a
    ld hl,$ccf1
    ld [hl+],a
    ld [hl],a
    ld hl,$d060
    ld [hl+],a
    ld [hl+],a
    ld [hl+],a
    ld [hl+],a
    ld [hl],a
    ld [$d06d],a
    ld [$ccee],a
    ld [$ccf7],a
    ld b,1
    call $3e43
    ld hl,$d067
    res 5,[hl]
    ld a,1
    ldh [$f3],a
    ld a,[{START46:#x}]
    cp 2
    jr z,.slide
    xor a
    ld [{START46:#x}],a
    ld a,[$d057]                 ; battle start lead: the picture is simply there (v46)
    push af
    xor a
    ld [$d057],a
    ld hl,$c480
    ld a,2
    call $3ec1
    pop af
    ld [$d057],a
    jr .done
.slide:
    xor a
    ld [{START46:#x}],a
    call slide84
.done:
    ld hl,sp+4
    ld a,$1f
    ld [hl+],a
    ld [hl],$4d
    ret
bane_add84:                      ; bane_npc: after the picture became 47
    call {int(L40['bank2f']['add_bane'],16):#x}
    jp ball84
''',B2F)
rom.put(fo(0x2f,B2F),c2f,'Bank 2F: v84 give84 + ball84 (conflict-free black ball slot)')
# bank 5 init_w: ld hl,ball_fix -> ball84
o=fo(5,0x7fbc);assert R[o:o+3].hex()=='21'+le(BALLFIX)
rom.data(o+1,bytes.fromhex(le(L['ball84'])),'InitMapSprites wrapper: ball_fix -> ball84',le(BALLFIX))
# bane_add (2F:606D): jp ball_fix -> jp bane_add84? (keep it simple: the call add_bane at 50C3 goes to bane_add84)
o=fo(0x2f,0x50c3);assert R[o:o+3].hex()=='cd6d60'
rom.code(o,bytes.fromhex('cd'+le(L['bane_add84'])),'bane_npc: bane_add -> bane_add84 (ball84)','cd6d60')
# bane_move (2F:4052): call give -> give84 (D452 also for wild METAMORPHOSIS)
o=fo(0x2f,0x4052);assert R[o:o+3].hex()=='cdb040'
rom.code(o,bytes.fromhex('cd'+le(L['give84'])),'bane_move: call give -> give84 (+ D452)','cdb040')
rom.data(o7+1,bytes.fromhex(le(L['dam84'])),'FaintEnemyPokemon hook: kill45 -> dam84 (DAMNATION faints visibly, CURSE flag)',le(KILL45))
rom.data(fo(0xf,0x4cbc)+1,bytes.fromhex(le(L['msg84'])),'SendOutMon message far call: msg46 -> msg84 (BLACK switched in: slide in, no ball)',le(MSG46))
# ---- 3. TOWER 7F after the ritual (RIT >= 6): no channelers (v54 ch54 still places MOM and AGATHA; ch84 hides the channeler objects after it every frame)
L54=json.load(open('manifest_v54.json'))['labels']
CH54=int(L54['bank30']['ch54'],16)
T53=fo(0x18,int(json.load(open('manifest_v53.json'))['labels']['bank18']['tail53'],16))
assert R[T53:T53+3].hex()=='21'+le(CH54)
B30=0x6f00
assert not any(R[fo(0x30,B30):fo(0x30,B30)+0x80])
c30,L30=asm(f'''
ch84:
    call {CH54:#x}
    ld a,[$d464]
    cp 5
    ret nz
    ld a,[$d467]
    cp 6
    ret c
    ld hl,objs84
    ld c,10
.l: ld a,[hl+]
    swap a
    ld e,a
    ld d,$c1
    xor a
    ld [de],a                    ; picture 0
    ld a,e
    add 4
    ld e,a
    ld d,$c2
    ld a,$ff
    ld [de],a
    inc e
    ld [de],a                    ; position ff
    dec c
    jr nz,.l
    ret
objs84: db 4,5,6,7,8,10,11,12,13,14
''',B30)
rom.put(fo(0x30,B30),c30,'Bank 30: v84 ch84 (no channelers on 7F after the ritual)')
rom.data(T53+1,bytes.fromhex(le(L30['ch84'])),'tail53: ch54 -> ch84 (hides the channelers after the ritual)',le(CH54))
# ---- 4. v80's scared-trainer lines must not replace the story fights: LORELEI/BRUNO/AGATHA/LANCE rooms, the CHAMPION's room, SILPH CO. 11F, the hideout's B4F
L80=json.load(open('manifest_v80.json'))['labels']['bank31']
RD80=int(L80['rdisp80'],16);RD69=int(L80['rdisp69'],16)
B31b=0x5a80
assert not any(R[fo(0x31,B31b):fo(0x31,B31b)+0x40])
c31,L31=asm(f'''
rdisp84:
    ld a,[$d35e]
    ld b,a
    ld hl,exm
.l: ld a,[hl+]
    cp $ff
    jp z,{RD80:#x}
    cp b
    jr nz,.l
    jp {RD69:#x}
exm: db $f5,$f6,$f7,$f8,$71,$78,$eb,$ca,$ff
''',B31b)
rom.put(fo(0x31,B31b),c31,'Bank 31: v84 rdisp84 (v80 scared lines not in the League / story maps)')
assert R[0xd1:0xd4].hex()=='21'+le(RD80)
rom.data(0xd2,bytes.fromhex(le(L31['rdisp84'])),'Home stub 0:00CE -> rdisp84',le(RD80))
# ---- 5. POKeMON LEAGUE (LORELEI / BRUNO / AGATHA / LANCE rooms) as BLACK: the player's name is BLACK there (engine texts: "BLACK defeated LORELEI!", "BLACK got ... for winning!"),
#         RED again everywhere else (BLUE's champion room included). The real name is kept in D879-D883 while swapped (D884 = swapped); BRUNO's speech says BLACK.
c2e,L2e=asm('''
name84:                          ; end of the map-load chain (2E:42B4)
    push af
    push bc
    push de
    push hl
    ld a,[$d46c]
    and a
    jr z,.restore
    ld a,[$d35e]
    cp $71
    jr z,.lg
    cp $f5
    jr c,.restore
    cp $f8
    jr nc,.restore
.lg:
    ld a,[$d884]
    and a
    jr nz,.done
    ld hl,$d158
    ld de,$d879
    ld bc,11
    call $00b5
    ld hl,blk
    ld de,$d158
    ld bc,11
    call $00b5
    ld a,1
    ld [$d884],a
    jr .done
.restore:
    ld a,[$d884]
    and a
    jr z,.done
    ld hl,$d879
    ld de,$d158
    ld bc,11
    call $00b5
    xor a
    ld [$d884],a
.done:
    pop hl
    pop de
    pop bc
    pop af
    jp $7c8b
blk: db $81,$8b,$80,$82,$8a,$50,0,0,0,0,0
''',0x5c00)
b2e=fo(0x2e,0x5c00);assert not any(R[b2e:b2e+0x80])
rom.put(b2e,c2e,'Bank 2E: v84 name84 (player name BLACK in the LEAGUE rooms)')
o=fo(0x2e,0x42b4);assert R[o:o+3].hex()=='c38b7c'
rom.code(o,bytes([0xc3,L2e['name84']&255,L2e['name84']>>8]),'Map load chain end: -> name84 (then the old jp 7C8B)','c38b7c')
# BRUNO's before-battle speech: "RED!" -> "BLACK!"
def wrap(s,w=17):
    out=[];cur=''
    for word in s.split():
        if cur and shown(cur+' '+word)>w:out.append(cur);cur=word
        else:cur=(cur+' '+word) if cur else word
    out.append(cur);return out
def convo(parts):return bytes(txt([wrap(p) for p in parts],0x58,17))
OLDB=convo(["I am BRUNO of the ELITE FOUR!","Through rigorous training, people and # can become stronger! I've weight trained with my #!",
 "I won't let a monster like you disgrace the sacred bond between trainer and #!","RED! We will grind you down with our superior power! Hoo hah!"])
NEWB=convo(["I am BRUNO of the ELITE FOUR!","Through rigorous training, people and # can become stronger! I've weight trained with my #!",
 "I won't let a monster like you disgrace the sacred bond between trainer and #!","BLACK! We will grind you down with our superior power! Hoo hah!"])
assert R[fo(0x30,0x6200):fo(0x30,0x6200)+len(OLDB)]==OLDB
TB=0x6f80
assert not any(R[fo(0x30,TB):fo(0x30,TB)+len(NEWB)+4])
rom.put(fo(0x30,TB),NEWB,"Bank 30: v84 BRUNO's speech with BLACK")
L56=json.load(open('manifest_v56.json'))['labels']['bank1d']
FS=fo(0x1d,int(L56['far_sb'],16));assert R[FS:FS+5].hex()=='17'+le(0x6200)+'3050'
rom.data(FS+1,bytes.fromhex(le(TB)),"BRUNO's speech pointer -> the BLACK text",le(0x6200))
# ---- 6. MOON STONE: flash + "The MOON STONE shatters!" right after the last POKeMON is down (start of TrainerBattleVictory, F:46AB), then the usual end sequence;
#         ph44 (after the speeches / money) no longer says it, it only calls the POKeMON back and sends BLACK out
L44=json.load(open('manifest_v44.json'))['labels']['bank2f']
E4CHK=0x6200;FLASH=int(L44['flash'],16);PH44=int(L44['ph44'],16)
def rt2(*parts):
    out=bytearray();inside=False
    for p in parts:
        if not inside:out.append(0);inside=True
        out+={'line':b'\x4f','cont':b'\x55','para':b'\x51'}.get(p,None) or enc(p)
    out+=b'\x58';return bytes(out)
TSH=rt2('The MOON STONE','line','shatters!')
b2f=fo(0x2f,0x6400);blk=R[b2f:b2f+0x400]
ti=blk.find(TSH);assert ti>=0 and blk.find(TSH,ti+1)<0
T_SHATTER=0x6400+ti
c3,L3=asm(f'''
shat84:
    ld hl,$4658                  ; the replaced  call 4658
    ld b,$0f
    db $cf
    call {E4CHK:#x}
    ret nz
    call {FLASH:#x}
    ld hl,{T_SHATTER:#x}
    jp $3c94
''',0x5c00+len(c2f))
rom.put(fo(0x2f,0x5c00)+len(c2f),c3,'Bank 2F: v84 shat84 (MOON STONE shatters at the last faint)')
o=fo(0x2f,PH44);old=R[o:o+14].hex()
assert R[o:o+3].hex()=='cd'+le(E4CHK) and R[o+5:o+8].hex()=='cd'+le(FLASH) and R[o+8:o+11].hex()=='21'+le(T_SHATTER) and R[o+11:o+14].hex()=='cd943c',old
rom.code(o+5,bytes(9),'ph44: no flash / "shatters" here any more (shat84 says it at the last faint)',R[o+5:o+14].hex())
assert not any(R[fo(0xf,0x5046):fo(0xf,0x5046)+8])
rom.put(fo(0xf,0x5046),bytes([0x21,L3['shat84']&255,L3['shat84']>>8,0x06,0x2f,0xc3,0x18,0x36]),'Bank F: v84 far stub -> 2F shat84')
o=fo(0xf,0x46ab);assert R[o:o+3].hex()=='cd5846'
rom.code(o,bytes([0xcd,0x46,0x50]),'TrainerBattleVictory: call 4658 -> call 5046 (shat84: 4658, then the MOON STONE shatters)','cd5846',
         reviewed='the stub tail-calls shat84 through Bankswitch; shat84 makes the original call to F:4658 first and returns to the caller')
rom.finish('Creepy_Black_Mu_v84.gb','manifest_v84.json','CREEPY MU V84',extra=dict(labels=dict(bank2f={k:hex(v) for k,v in L.items()})))
