# Creepy Black Mu v77: the ritual, five fixes.
#   1. TOWER CHAMBER (map 69): no music until the player has become BLACK (map music id FF = stop; set again when BLACK is born, so the room's music starts after the battle).
#   2. MR. MU's battle: the player (YOU) is not "sent out": no slide of the trainer picture, no "Go! RED!", no summoning animation; the HUD appears after MR. MU's cut-in (v46's BLACK path).
#   3. No victory music in the chamber (both victory-music callers, wild F:45E2 and trainer F:46CB, skip it on map 69).
#   4. The three fossil sprites stay on their stands until the player is BLACK (RIT 6; was: gone from RIT 3 = right after MR. MU's battle).
#   5. The climax battle (GHOST Lv100): the player gets one turn first. First battle menu: normal (FIGHT only: PKMN / ITEM / RUN are refused), GHOST's own move is skipped
#      (silently), and at the NEXT menu GHOST takes its turn: CURSE, the black screen, BLACK is born (as before). RIT: 5 battle, 7 the player's turn is pending, 8 it was played.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V76_SHA='6a369425166c88f932aac998f751053fee06f8a160e7869492e2b757b2cd3a2f'
rom=Rom('Creepy_Black_Mu_v76.gb',V76_SHA)
R=bytes(rom.r)
def lh(a):return a.to_bytes(2,'little').hex()
RIT,BLACK=0xd467,0xd46c
L51=json.load(open('manifest_v51.json'))['labels']['bank30']
L25=json.load(open('manifest_v25.json'))['labels']['bank2d']
L49=json.load(open('manifest_v49.json'))['labels']['bank2f']
L46=json.load(open('manifest_v46.json'))['labels']['bank2f']
music51=int(L51['music51'],16);climax=int(L25['climax_menu'],16);scared49=int(L49['scared49'],16);pre46=int(L46['pre46'],16)
# ---------------------------------------------------------------- bank 30 code
A30=0x4400
assert not any(R[fo(0x30,A30):fo(0x30,A30)+0x180])
c30,L30=asm(f'''
music77:                         ; (0:1249 via rst 08) v51's map music, then: the TOWER CHAMBER is silent until BLACK
    call {music51}
    ld a,[$d35e]
    cp $69
    ret nz
    ld a,[{BLACK:#x}]
    and a
    ret nz
    ld a,$ff                    ; music id FF = stop all music
    ld [$d35b],a
    ret
rmus77:                          ; BLACK was just born: the room's own music again (plays after the battle)
    jp {music51}
pre77:                           ; (F:41D4 stub) v46's pre46 + the player in MR. MU's battle (YOU, RIT 1) is "just there" too
    ld hl,$c405
    xor a
    ld [0xd45a],a
    ld a,[$cf91]
    cp $7f
    jr z,.q
    cp $79
    ret nz
    ld a,[{RIT:#x}]
    cp 1
    ret nz
.q: ld a,1
    ld [0xd45a],a
    ld hl,sp+4
    ld a,$dc
    ld [hl+],a
    ld [hl],$41
    ret
et77:                            ; (F:67C8 via rst 08) the enemy's turn: climax battle, the player's turn is pending -> GHOST skips this one silently
    ld a,[{RIT:#x}]
    cp 7
    jr nz,.n
    ld a,8
    ld [{RIT:#x}],a
    xor a                        ; z: no attack (ExecuteEnemyMoveDone)
    ret
.n: ld hl,{scared49:#x}
    ld b,$2f
    jp $3618
vicw77:                          ; (F:45DF via rst 08) the wild-victory part:  call $4658 (low-health alarm off) + the fanfare (not in the chamber)
    xor a
    ld [$d083],a
    ld [$c02a],a
    inc a
    ld [$ccf6],a
    ld a,[$d35e]
    cp $69
    ret z
    ld a,$ff
    ld [$c0ee],a
    call $377a
    ld c,8
    ld a,$f9
    call $23ce
    jp $3e22
vict77:                          ; (F:46C6 via rst 08) the trainer-victory fanfare (id in D468; not in a link battle, not in the chamber); hl = the text after it
    ld a,[$d12b]
    cp 4
    jr z,.n
    ld a,[$d35e]
    cp $69
    jr z,.n
    ld a,$ff
    ld [$c0ee],a
    call $377a
    ld c,8
    ld a,[0xd468]
    call $23ce
    call $3e22
.n: ld hl,$4714
    ret
''',A30,{})
rom.put(fo(0x30,A30),c30,'Bank 30: v77 chamber music, quiet send-out in MR. MU battle, climax enemy turn, victory music off in the chamber')
# 1. map music
o=0x1249;assert R[o:o+7].hex()=='21'+lh(music51)+'0630cf18'
rom.code(o+1,bytes.fromhex(lh(L30['music77'])),'Map music read -> music77 (TOWER CHAMBER silent until BLACK)',lh(music51),reviewed='operand of the v51 far-call stub')
# BLACK is born: ld a,1 / ld [BLACK],a  ->  call mus77r (also refreshes the map music)
A2D=0x4b00
assert not any(R[fo(0x2d,A2D):fo(0x2d,A2D)+0x60])
c2d,L2D=asm(f'''
mus77r:
    ld a,1
    ld [{BLACK:#x}],a
    farcall {L30['rmus77']},$30
    ret
cm77:                            ; the climax battle's menu hook (was climax_menu): turn 1 = the player's, then GHOST's
    call $375f
    ld a,[{RIT:#x}]
    cp 5
    jr z,.first
    cp 8
    ret nz
    ld a,5                       ; the player has had his turn: GHOST acts (the climax as before)
    ld [{RIT:#x}],a
    jp {climax+9:#x}
.first:
    ld a,[$d057]
    and a
    ret z
    ld a,7                       ; the first menu is shown normally: FIGHT only, GHOST's move is skipped
    ld [{RIT:#x}],a
    ret
''',A2D,{})
assert R[fo(0x2d,climax):fo(0x2d,climax)+12].hex()=='cd5f37fa67d4fe05c0fa57d0',R[fo(0x2d,climax):fo(0x2d,climax)+12].hex()
rom.put(fo(0x2d,A2D),c2d,'Bank 2D: v77 mus77r (BLACK flag + music) and cm77 (climax: the player acts first)')
o=0x4556+0x2d*0x4000-0x4000+0x0;o=R.find(bytes.fromhex('3e01ea6cd4afea5cd4'),0x2d*0x4000)
rom.code(o,bytes.fromhex('cd'+lh(L2D['mus77r'])+'0000'),'BLACK born: flag + music refresh through mus77r','3e01ea6cd4',reviewed='a flag store replaced by a call that stores it')
# climax stub F:7FF8 -> cm77
o=fo(0xf,0x7ff8);assert R[o:o+8].hex()=='21'+lh(climax)+'062dc31836'
rom.data(o+1,bytes.fromhex(lh(L2D['cm77'])),'Climax battle-menu stub -> cm77',lh(climax))
# 5b. the enemy's turn F:67C8: scared49 -> et77 (bank 30)
o=fo(0xf,0x67c8);assert R[o:o+6].hex()=='21'+lh(scared49)+'062fcf'
rom.code(o+1,bytes.fromhex(lh(L30['et77'])+'0630'),'Enemy turn: et77 (climax: GHOST skips the player-turn) -> scared49',lh(scared49)+'062f',reviewed='operand and bank of the v49 far call')
# 2. battle start stub F:7FB8: pre46 (2F) -> pre77 (30)
o=fo(0xf,0x7fb8);assert R[o:o+8].hex()=='21'+lh(pre46)+'062fc31836'
rom.data(o+1,bytes.fromhex(lh(L30['pre77'])+'0630'),'Battle start stub -> pre77 (quiet start also for MR. MU\'s battle)',lh(pre46)+'062f')
# 3. victory music
o=fo(0xf,0x45df);assert R[o:o+8].hex()=='cd58463ef9cd1947'
rom.code(o,bytes.fromhex('21'+lh(L30['vicw77'])+'0630cf'+'0000'),'Wild victory music: no fanfare in the chamber (vicw77)','cd58463ef9cd1947',
         reviewed='the far routine repeats call 4658 and ld a,F9 / PlayBattleVictoryMusic; 45E7 (call 0001, jump target of the trainer branch) is untouched')
o=fo(0xf,0x46c6);assert R[o:o+12].hex()=='fa2bd1fe0478c41947211447'
rom.code(o,bytes.fromhex('78ea68d4'+'21'+lh(L30['vict77'])+'0630cf'+'0000'),'Trainer victory music: no fanfare in the chamber (vict77)','fa2bd1fe0478c4194721 1447'.replace(' ',''),
         reviewed='the far routine repeats the link check, the fanfare and sets hl = F:4714 for the PrintText after it')
# 4. fossils stay until BLACK: chamber script cp 3 -> cp 6
L53=json.load(open('manifest_v53.json'))['labels']['bank18']
o=fo(0x18,int(L53['script_ch'],16));assert R[o+8:o+13].hex()=='fa67d4fe03'
rom.code(o+12,bytes([6]),'Chamber script: the fossil sprites go when the player is BLACK (RIT 6), not at RIT 3','03',reviewed='immediate of cp')
# 5c. menu: PKMN / ITEM / RUN refused while the player's turn is pending (RIT 7). 2E chain 7800: jp z,59db -> jp z,menu77
B2E=0x7820
assert not any(R[fo(0x2e,B2E):fo(0x2e,B2E)+0x60])
t=bytes(txt([["GHOST's aura","holds you here!"]],0x58))
c2e,L2E=asm(f'''
menu77:                          ; (2E chain, a = menu choice in D468: 0 FIGHT) RIT 7: FIGHT only
    ld a,[{RIT:#x}]
    cp 7
    jp nz,$59db
    ld a,[0xd468]
    and a
    ret z
    ld hl,t_block3
    call $3c94
    ld de,$4ede
    jp $59c8
t_block3: db {','.join(str(x) for x in t)}
''',B2E,{})
rom.put(fo(0x2e,B2E),c2e,'Bank 2E: v77 menu77 (climax battle: FIGHT only on the first turn)')
o=fo(0x2e,0x780c);assert R[o:o+3].hex()=='cadb59'
rom.code(o+1,bytes.fromhex(lh(L2E['menu77'])),'2E battle-menu chain: menu -> menu77 (RIT 7 limits)','db59',reviewed='jp z target')
rom.finish('Creepy_Black_Mu_v77.gb','manifest_v77.json','CREEPY MU V77',extra=dict(labels=dict(bank30={k:hex(v) for k,v in L30.items()},bank2d={k:hex(v) for k,v in L2D.items()},bank2e={k:hex(v) for k,v in L2E.items()})))
