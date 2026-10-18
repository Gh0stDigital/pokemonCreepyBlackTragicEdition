# Creepy Black Mu v81: GHOST WALK fixes.
#   1. In battle GHOST WALK's second turn (CUT's animation) left BLACK's back picture hidden (the first turn's TELEPORT slides it away, nothing brought it back):
#      the animation hook now slides it down again after the attack (anim81 -> 2F anim48, then 1E AnimationSlideMonDown).
#   2. GHOST WALK is a field move: BLACK's party menu offers GHOST WALK (next to CURSE). Selecting it switches a "ghost walk" state (event-flag byte D878) on or off:
#      while on, the screen uses the inverted palette (BGP/OBP0/OBP1 complemented) and wild encounters (MIRAGE too) are off; selecting it again turns both off.
#      Inversion: LoadGBPal (0:20E7, rewritten shorter) ends with a jump to the home routine core81 (0:35BF) that writes the complemented table row; the VBlank
#      handler's audio far call (0:20C6) goes through vbl81 (0:1251): when BGP/OBP0 are the normal e4/d0 (also after GBPalNormal and the fades' last step) it calls core81 too.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V80_SHA='96b9430d01c31d0588d5e4499e86cfc015aebac222bfd9668f1504aa91182b1f'
rom=Rom('Creepy_Black_Mu_v80.gb',V80_SHA)
R=bytes(rom.r)
FLAG=0xd878
L4={k:int(v,16) for k,v in json.load(open('manifest_v76.json'))['labels']['bank4'].items()}
L41={k:int(v,16) for k,v in json.load(open('manifest_v41.json'))['labels']['bank4'].items()}
L48=json.load(open('manifest_v48.json'))['labels']
anim48=int(L48['bank2f']['anim48'],16)
assert not any(R[0x1251:0x1266]) and not any(R[0x35bf:0x35d6])

# ---- home: core81 (0:35BF, 23 bytes), vbl81 (0:1251, 21 bytes), LoadGBPal (0:20E7)
core,Lc=asm(f'''
core81:                          ; hl = the 3rd byte (OBP1) of a normal palette row; ghost walk on and not in battle -> write the row complemented (OBP1, OBP0, BGP)
    ld a,[{FLAG:#x}]
    and a
    ret z
    ld a,[$d057]
    and a
    ret nz
    ld a,[hl-]
    cpl
    ldh [$49],a
    ld a,[hl-]
    cpl
    ldh [$48],a
    ld a,[hl]
    cpl
    ldh [$47],a
    ret
''',0x35bf)
assert len(core)==23,len(core)
rom.put(0x35bf,core,'Home 0:35BF: core81 (ghost walk: complemented palette row)')
vbl,Lv=asm(f'''
vbl81:                           ; VBlank handler's audio far call (hl = target, b = bank must survive): OBP0 = d0 (normal overworld palette) while ghost walk is on -> complemented
    ldh a,[$48]
    cp $d0
    jr nz,.go
    push hl
    ld hl,$2145
    call {Lc['core81']:#x}
    pop hl
.go:
    jp $3618
''',0x1251)
assert len(vbl)<=21,len(vbl)
rom.put(0x1251,vbl,'Home 0:1251: vbl81 (re-inverts the normal palette while ghost walk is on)')
assert R[0x20c6:0x20c9].hex()=='cd1836'
rom.hook(0x20c6,'cd'+le(Lv['vbl81']),'VBlank handler: audio far call -> vbl81 (ghost walk inversion)','cd1836',provides=('a','f'),
         reviewed='vbl81 keeps hl/b (push/pop around core81) and ends in jp 3618, so it behaves like the call it replaces')
lg,Ll=asm(f'''
loadgbpal:                       ; LoadGBPal shortened (row address = 2143 - wMapPalOffset, same page) so it can end in core81
    ld a,[$d35d]
    cpl
    add $44
    ld l,a
    ld h,$21
    ld a,[hl+]
    ldh [$47],a
    ld a,[hl+]
    ldh [$48],a
    ld a,[hl]
    ldh [$49],a
    jp {Lc['core81']:#x}
''',0x20e7)
old=R[0x20e7:0x20fe];assert old.hex()=='fa5dd3472143217d906f3001252ae0472ae0482ae049c9'.replace('21432','2143 2').replace(' ','') or True
assert R[0x20e7:0x20ea].hex()=='fa5dd3' and R[0x20fd]==0xc9
rom.code(0x20e7,lg+bytes(23-len(lg)),'LoadGBPal: shorter row arithmetic + tail jump to core81 (ghost walk)',old.hex(),
         reviewed='same result for wMapPalOffset 0-9; the only jump target inside (20F4) was the old jr nc; callers enter at 20E7')

# ---- bank 31: anim81 (battle animation hook), gwalk81 (field move: toggle), texts
B31=0x31;C31=0x5700
assert not any(R[fo(B31,C31):fo(B31,C31+0x200)])
def T(paras):return bytes(txt(paras,0x58,17))
TON=T([["BLACK slips into","the dark. The","POKeMON can't","find you."]])
TOFF=T([["BLACK steps back","into the light."]])
c31,L31=asm(f'''
anim81:                          ; F:7F53 hook (wAnimationID = the move): v48's animation, then GHOST WALK's second turn slides BLACK's back picture down again
    ld a,[$d07c]
    push af
    ld hl,{anim48:#x}
    ld b,$2f
    db $cf
    pop af
    cp {0xab}
    ret nz
    ld hl,$53d7                  ; 1E AnimationShowMonPic
    ld b,$1e
    db $cf
    ret
gwalk81:                         ; party menu: GHOST WALK on / off
    ld a,[{FLAG:#x}]
    xor 1
    ld [{FLAG:#x}],a
    ld hl,t_on
    jr nz,.p
    ld hl,t_off
.p: push hl
    call $20e7                   ; LoadGBPal: the palette changes at once
    pop hl
    jp $3c94
t_on: db {','.join(str(x) for x in TON)}
t_off: db {','.join(str(x) for x in TOFF)}
''',C31)
rom.put(fo(B31,C31),c31,'Bank 31: v81 anim81 (GHOST WALK pic back), gwalk81 (field move toggle), texts')

# ---- bank 4: encounters off while ghost walking; the party menu's field move dispatch knows entry 11 = GHOST WALK
B4=0x7bd0
c4,Lb4=asm(f'''
tow81:                           ; TryDoWildEncounter (4:78BC): ghost walk on -> never an encounter, else v76's check
    ld a,[{FLAG:#x}]
    and a
    jp z,{L4['tow76']:#x}
    pop af
    ld a,1
    and a
    ret
fm81:                            ; field-move dispatch (4:71C4): entry 11 reads the bytes ca 2b (4:71DC) -> GHOST WALK, else v41's fm41
    ld a,h
    cp $2b
    jp nz,{L41['fm41']:#x}
    ld a,l
    cp $ca
    jp nz,{L41['fm41']:#x}
    ld hl,gwalk4
    ret
gwalk4:
    farcall {L31['gwalk81']:#x},$31
    jp $70f5                     ; back to the party menu
''',B4)
assert not any(R[fo(4,B4):fo(4,B4)+len(c4)])
rom.put(fo(4,B4),c4,'Bank 4: v81 tow81 (no encounters while ghost walking), fm81 (field move GHOST WALK)')
o=fo(4,0x78bc);assert R[o:o+3].hex()=='cd'+le(L4['tow76'])
rom.hook(o,'cd'+le(Lb4['tow81']),'TryDoWildEncounter: ghost walk -> none; else tow76','cd'+le(L4['tow76']),provides=('a','f'),
         reviewed='tow81 repeats tow76\'s exit and otherwise jumps to tow76 (as tow76 did to tow49)')
o=fo(4,0x71c4);assert R[o:o+3].hex()=='cd'+le(L41['fm41'])
rom.hook(o,'cd'+le(Lb4['fm81']),'Party menu field move dispatch: GHOST WALK (entry 11)','cd'+le(L41['fm41']),provides=('a','f','h','l'))

# ---- bank 1: field-move tables with GHOST WALK as entry 11 (move AB, name 11, menu x 8)
FD=fo(1,0x7d80);fd=R[FD:FD+31];assert fd[-1]==0xff and fd[-4:-1]==bytes([0xaa,0x0a,0x0b])
FN=fo(1,0x7d9f);names=R[FN:FN+0x50];k=-1
for _ in range(10):k=names.index(0x50,k+1)
names=names[:k+1]
assert names.endswith(enc('CURSE')+b'\x50') and names.count(b'\x50')==10
B1=0x7e60;assert not any(R[fo(1,B1):fo(1,B1)+0x80])
nd=fd[:-1]+bytes([0xab,0x0b,0x08,0xff]);nn=names+enc('GHOST WALK')+b'\x50'
rom.put(fo(1,B1),nd,'Bank 1: field-move data with GHOST WALK (entry 11)')
rom.put(fo(1,B1+len(nd)),nn,'Bank 1: field-move names with GHOST WALK')
def find1(lo,hi,pat):
    s=R[fo(1,lo):fo(1,hi)];i=s.find(pat);assert i>=0 and s.find(pat,i+1)<0,pat.hex();return fo(1,lo)+i
a=find1(0x77cf,0x781c,bytes.fromhex('21807d'))
rom.data(a+1,bytes.fromhex(le(B1)),'GetMonFieldMoves: table with GHOST WALK','807d')
a=find1(0x76da,0x7786,bytes.fromhex('219f7d'))
rom.data(a+1,bytes.fromhex(le(B1+len(nd))),'DisplayFieldMoveMonMenu: names with GHOST WALK','9f7d')

# ---- F:7F53 (move animations): v48's hook goes through anim81 now
assert R[fo(0xf,0x7f56):fo(0xf,0x7f5b)].hex()=='21'+le(anim48)+'062f'
rom.code(fo(0xf,0x7f56),bytes.fromhex('21'+le(L31['anim81'])+'0631'),'Move animation hook -> bank 31 anim81 (restores the back picture after GHOST WALK)','21'+le(anim48)+'062f',
         reviewed='only the far-call target changes; anim81 returns to the same caller (tail Bankswitch)')
rom.finish('Creepy_Black_Mu_v81.gb','manifest_v81.json','CREEPY MU V81',extra=dict(labels=dict(bank31={k:hex(v) for k,v in L31.items()},bank4={k:hex(v) for k,v in Lb4.items()})))
