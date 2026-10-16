# Creepy Black Mu v74: four fixes.
#   1. CINNABAR sign "C3 ERROR." (and every other town's first sign since v63): a sign whose text id is <= the number of sprites is taken for a sprite
#      by DisplayTextID, which then looks the text up in that sprite's own text byte. v63 appended the town shamaness as the LAST sprite, so her slot number
#      equalled the town sign's text id and her marker byte (3F, "no such text") was read instead of the sign's text. The marker is now (byte0 = D0, text byte =
#      her own slot number): the translation gives the sign's id back, and wrap66 tells her from the sign by standing next to her, as before.
#   2. CELADON GAME CORNER Rocket: when CURSE killed him (v34 kill bit $1FF = D44F bit 7) the after-battle speech (text 13) is skipped, and so is his walk
#      (his hidden sprite never finished walking, so the script waited for ever with the joypad ignored); the event still ends the usual way (he is hidden).
#   3. Walking trainers/NPCs that became gravestones (POKeMON MANSION 2F/3F, any WALK sprite) kept wandering: killed13's "already a gravestone" branch now
#      sets the movement byte (C2x6) to STAY every frame (v35 predef 0x13 -> killed74).
#   4. POKeMON MANSION 1F: v8's MR. MU is object 4 = text id 4, the same id as the STATUE SWITCH's hidden event, so the switch always showed MR. MU's talk (even when he
#      was gone). Text entry 4 now tells them apart by where the player stands (statue: y6 x2): the statue gets its original switch code (11:435B) back.
import json,re
from patchlib import *
from patchguard import fo
from sm83asm import asm

V73_SHA='789db83fc9afcfe85773d64029e3441291ed206edf028661189cfd7ae72a580c'
rom=Rom('Creepy_Black_Mu_v73.gb',V73_SHA)
R=bytes(rom.r)
def lhex(a):return a.to_bytes(2,'little').hex()
# ------------------------------------------------------------------ 1. shamaness marker (bank 31)
B31=0x31
L66={k:int(v,16) for k,v in json.load(open('manifest_v66.json'))['labels']['bank31'].items()}
src66=open('build_v66.py').read()
S=src66[src66.index("app66:                           ; (from InitMapSprites)"):src66.index("\ntab66:")]
assert '{' not in S
a0='''    ld a,[$d4e1]
    ld e,a
    and a
    jr z,.add
    dec a
    add a
    inc a
    ld c,a
    ld b,0
    push hl
    ld hl,$d4e4
    add hl,bc
    ld a,[hl]
    pop hl
    cp $3f
    ret z                        ; marker: already added (redraw)
.add:'''
a1='''    ld a,[$d4e1]
    ld e,a
    and a
    jr z,.add
    push hl
    ld a,e                       ; marker: the last slot is a CHANNELER picture, byte 0 = D0 and its text byte = its own slot number (=> she was added: redraw)
    swap a
    ld l,a
    ld h,$c1
    ld a,[hl]
    cp $19
    jr nz,.nm
    ld a,e
    dec a
    add a
    inc a
    ld c,a
    ld b,0
    ld hl,$d4e4
    add hl,bc
    ld a,[hl-]
    cp e
    jr nz,.nm
    ld a,[hl]
    cp $d0
    jr nz,.nm
    pop hl
    ret
.nm:pop hl
.add:'''
assert S.count(a0)==1
S=S.replace(a0,a1)
b0='''    ld a,$d0
    ld [hl+],a
    ld [hl],$3f'''
b1='''    ld a,$d0
    ld [hl+],a
    ld [hl],b                    ; text byte = her slot number: the sign that shares it is looked up under its own id'''
assert S.count(b0)==1
S=S.replace(b0,b1)
c0='''    ld a,[$d4e1]
    cp b
    jp nz,.orig
    ld a,b
    dec a'''
c1='''    ld a,[$d4e1]
    cp b
    jp nz,.orig
    ld a,b                       ; only a CHANNELER picture in a town of the table can be her (MR. MU in the MANSION is sprite 4 of 4 as well)
    swap a
    ld l,a
    ld h,$c1
    ld a,[hl]
    cp $19
    jp nz,.orig
    ld a,[$d35e]
    ld c,a
    ld hl,tab66
.t: ld a,[hl]
    cp c
    jr z,.tok
    cp $ff
    jp z,.orig
    ld de,7
    add hl,de
    jr .t
.tok:
    ld a,b
    dec a'''
assert S.count(c0)==1
S=S.replace(c0,c1)
d0='''    ld a,[hl]
    cp $3f
    jp nz,.orig'''
d1='''    ld a,[hl]
    cp b
    jp nz,.orig
    dec hl
    ld a,[hl]
    cp $d0
    jp nz,.orig'''
assert S.count(d0)==1
S=S.replace(d0,d1)
CODE=0x4900
assert not any(R[fo(B31,CODE):fo(B31,CODE)+0x200])
code,L=asm(S,CODE,{'tab66':L66['tab66'],'tpt66':L66['tpt66']})
assert len(code)<0x200,len(code)
rom.put(fo(B31,CODE),code,'Bank 31: v74 app74 / wrap74 (shamaness marker = D0 + her slot number)')
L67={k:int(v,16) for k,v in json.load(open('manifest_v67.json'))['labels']['bank31'].items()}
o=fo(B31,L67['im67']);assert R[o:o+6].hex()=='cd'+le(L66['app66'])+'c3'+le(L67['gymhide']),R[o:o+6].hex()
rom.data(o+1,bytes.fromhex(le(L['app66'])),'v67 im67 (InitMapSprites stub): call app66 -> app74',le(L66['app66']))
o=fo(0x2f,0x502e);assert R[o:o+8].hex()=='3e3121'+le(L66['wrap66'])+'c33100'
rom.data(o+3,bytes.fromhex(le(L['wrap66'])),'DisplayTextID chain -> wrap74',le(L66['wrap66']))
# the old code is dead: remove it (tab66/tpt66 stay where they are)
oldlen=L66['tab66']-L66['app66']
o=fo(B31,L66['app66']);old=R[o:o+oldlen]
rom.data(o,bytes(oldlen),'Bank 31: v66 app66/wrap66 removed',old.hex())
# ------------------------------------------------------------------ 2. GAME CORNER Rocket (bank 18)
GC=0x7140
assert not any(R[fo(0x12,GC):fo(0x12,GC)+24])
gc,_=asm('''
gc74:
    ld a,[$d44f]
    bit 7,a
    jr nz,.dead
    ld a,$0d             ; (the replaced  ld a,$0d / ldh [$8c],a / call DisplayTextID)
    ldh [$8c],a
    jp $294d
.dead:                   ; the Rocket is dead: no after-battle speech and no walking away (a hidden sprite never finishes its walk: the script would wait for ever,
    pop af               ; with the joypad ignored); straight to the "script 2" step, which hides him and ends the event
    jp $4c54
''',GC,{})
rom.put(fo(0x12,GC),gc,'Bank 12: v74 GAME CORNER Rocket: dead = no speech, no walk')
o=fo(0x12,0x4c26);assert R[o:o+7].hex()=='3e0de08ccd4d29',R[o:o+7].hex()
rom.hook(o,'cd'+lhex(GC)+'00000000','Game Corner Rocket after battle: speech through gc74 (skipped, with his walk, when he is dead)','3e0de08ccd4d29',reviewed='the stub repeats the replaced instructions and tail-jumps to DisplayTextID, or drops its return address and jumps to the script-2 step (4C54 = ld a,2 / ld [D65F],a / ret)')
# ------------------------------------------------------------------ 3. gravestones never walk (bank 2D)
L29={k:int(v,16) for k,v in json.load(open('manifest_v29.json'))['labels']['bank2d'].items()}
KC2=L29['kill_chk2'];K=0x6220
assert not any(R[fo(0x2d,K):fo(0x2d,K)+48])
kc,KL=asm(f'''
killed74:                        ; predef 0x13 (v35 killed13) + gravestones stand still
    farcall $4dfb,3
    ldh a,[$e5]
    and a
    ret nz
    ldh a,[$da]                  ; current sprite offset
    ld e,a
    ld d,$c1
    ld a,[de]
    cp $49
    jr nz,.k
    ld a,e                       ; a gravestone: movement byte 1 (C2x6) = STAY, then draw it (ffe5 = 0)
    or 6
    ld l,a
    ld h,$c2
    ld [hl],$ff
    xor a
    ret
.k: call {KC2}                   ; v29/v34 trainer table + v28 NPC list: NZ = killed
    ld a,0
    jr z,.o
    inc a
.o: ldh [$e5],a
    ret
''',K,{})
rom.put(fo(0x2d,K),kc,'Bank 2D: v74 killed74 (killed13 + gravestones stay put)')
PRE=fo(0x13,0x7e79)+3*0x13
assert R[PRE:PRE+3]==bytes([0x2d,0x00,0x62])
rom.data(PRE+1,bytes.fromhex(lhex(KL['killed74'])),'Predef 0x13 -> killed74','0062')
# ------------------------------------------------------------------ 4. MANSION 1F: the statue switch is not MR. MU
M=0x751a
assert R[fo(0x11,0x7519):fo(0x11,0x7519)+9].hex()=='08213e480630c31836' and not any(R[fo(0x11,0x7522):fo(0x11,0x7522)+30])
mc,_=asm('''
    ld a,[$d361]
    cp 6
    jr nz,.mu
    ld a,[$d362]
    cp 2
    jp z,$435b                   ; the statue switch's own text code (11:435A TX_ASM)
.mu:ld hl,$483e
    ld b,$30
    jp $3618
''',M,{})
assert len(mc)<=0x7540-M
rom.data(fo(0x11,M),mc+bytes(9-len(mc)) if len(mc)<9 else mc,'Mansion 1F text 4: statue (y6,x2) -> the switch, else MR. MU','213e480630c31836'+'00'*(len(mc)-8))
rom.finish('Creepy_Black_Mu_v74.gb','manifest_v74.json','CREEPY MU V74',extra=dict(labels=dict(bank31={k:hex(v) for k,v in L.items()},bank2d={k:hex(v) for k,v in KL.items()})))
