# Creepy Black Mu v66: fixes for the town shamanesses (v63) and the old Pallet placeholder.
#   1. SPRITE GLITCH: v63 put the CHANNELER picture (19) into the sprite sets by overwriting one entry of sets 3, 4, 5, 7, 10. I had only checked the maps with a
#      fixed set; ROUTES pick their set by position (5:7A89 table) and share these sets: Route 8's HIKER (0E in set 3), Route 12/13's boy (0C in set 4) and
#      Route 5/6's boy (07 in set 7) lost their pictures in the part of the route that uses that set and were drawn with garbage tiles (and channeler-like
#      faces). Now only entries that NO map using the set needs are replaced (set 3: 31, set 4: 31, set 5: 35 (as before), set 7: 05, set 10: 09 (as before));
#      the old edits are undone. t74 checks every outdoor map's pictures against its set(s) (also the position-dependent ones) and compares with v62.
#   2. The speeches have no "SHAMANESS n:" / title any more, only the story.
#   3. Once talked to she is gone the next time the map loads (as before); additionally the slot above the last real sprite is wiped when she is not added
#      (no stale picture / marker byte can survive).
#   4. PALLET: the old placeholder shamaness by the water (object 5, v1 text) is removed (its position is FF,FF in the object data and it is hidden every frame);
#      SHAMANESS 1's official speech is told by the new shamaness standing on its old tile (y15 x8). She is there from the start of the game (the others
#      need GHOST); the table has a "needs GHOST" byte per town.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V65_SHA='6d89bbd8beff2f41476ea1f2452d29ef5b76947f19eadfa0e97117ee60a280ea'
rom=Rom('Creepy_Black_Mu_v65.gb',V65_SHA)
r=rom.r;R=bytes(r)
B31=0x31
L63={k:int(v,16) for k,v in json.load(open('manifest_v63.json'))['labels']['bank31'].items()}
L65={k:int(v,16) for k,v in json.load(open('manifest_v65.json'))['labels']['bank31'].items()}
CODE=0x6600;TXT=0x6a00
assert not any(R[fo(B31,CODE):fo(B31,0x8000)])
# ---- texts: only the story
def wrap(s,w=17):
    out=[];cur=''
    for word in s.split():
        if cur and len(cur)+1+len(word)>w:out.append(cur);cur=word
        else:cur=(cur+' '+word) if cur else word
    out.append(cur);return out
src63=open('build_v63.py').read()
ns={'wrap':wrap}
exec(src63[src63.index('LORE=['):src63.index('def lore_text')],ns)
LORE=ns['LORE']
def body(b):
    lines=wrap(b);return [lines[i:i+4] for i in range(0,len(lines),4)]
tx=bytearray();TA=[]
for t,b in LORE:
    TA.append(TXT+len(tx));tx+=bytes(txt(body(b),0x58,17))
assert TXT+len(tx)<0x7e00
rom.put(fo(B31,TXT),bytes(tx),'Bank 31: v66 the ten SHAMANESS speeches (story only)')
# ---- code
TOWNS=[(0x00,15,8,0,0),(0x01,12,28,1,1),(0x02,10,12,2,1),(0x03,20,18,3,1),(0x05,14,12,4,1),(0x06,11,24,5,1),(0x07,9,10,6,1),(0x0a,22,19,7,1),(0x04,6,12,8,1),(0x08,4,14,9,1)]
tab=''.join(f'    db {m},{y+4},{x+4},{0x40+i//8},{1<<(i%8)},{i},{req}\n' for m,y,x,i,req in TOWNS)
SRC=f'''
app66:                           ; (from InitMapSprites) append the shamaness of this town
    ld a,[$d35e]
    ld c,a
    ld hl,tab66
.f: ld a,[hl]
    cp $ff
    ret z
    cp c
    jr z,.found
    ld de,7
    add hl,de
    jr .f
.found:
    push hl
    ld de,6
    add hl,de
    ld a,[hl]
    pop hl
    and a
    jr z,.nreq
    ld a,[$d451]                 ; (all towns but PALLET: from the moment GHOST is acquired)
    and a
    ret z
.nreq:
    push hl
    inc hl
    inc hl
    inc hl
    ld a,[hl+]
    ld e,a
    ld d,$d8
    ld a,[hl]
    ld b,a
    ld a,[de]
    and b
    pop hl
    jr nz,.wipe                  ; talked to: gone
    ld a,[$d4e1]
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
.add:
    ld a,e
    cp 15
    jr z,.slot                   ; all slots used: take the last one
    inc a
    ld [$d4e1],a
.slot:
    ld b,a
    swap a
    ld e,a
    ld d,$c1
    ld a,$19
    ld [de],a
    inc d
    ld a,e
    add 4
    ld e,a
    inc hl
    ld a,[hl+]
    ld [de],a
    inc e
    ld a,[hl]
    ld [de],a
    inc e
    ld a,$ff
    ld [de],a
    ld a,b
    dec a
    add a
    ld e,a
    ld d,0
    ld hl,$d4e4
    add hl,de
    ld a,$d0
    ld [hl+],a
    ld [hl],$3f
    ld hl,$d504
    add hl,de
    xor a
    ld [hl+],a
    ld [hl],a
    ret
.wipe:                           ; she is not added: nothing of her may be left in the slot after the last real sprite
    ld a,[$d4e1]
    cp 15
    ret nc
    inc a
    ld b,a
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
    ld a,b
    dec a
    add a
    ld e,a
    ld d,0
    ld hl,$d4e4
    add hl,de
    xor a
    ld [hl+],a
    ld [hl],a
    ret

wrap66:                          ; 2F:502E: DisplayTextID chain; her talk, else on to the old code (v28 NPC talk)
    ldh a,[$8c]
    and a
    jp z,.orig
    ld b,a
    ld a,[$d4e1]
    cp b
    jp nz,.orig
    ld a,b
    dec a
    add a
    inc a
    ld e,a
    ld d,0
    ld hl,$d4e4
    add hl,de
    ld a,[hl]
    cp $3f
    jp nz,.orig
    ld a,b
    swap a
    add 4
    ld l,a
    ld h,$c2
    ld a,[$d361]
    add 4
    ld d,a
    ld a,[$d362]
    add 4
    ld e,a
    ld a,[hl+]
    sub d
    jr nc,.a1
    cpl
    inc a
.a1:ld c,a
    ld a,[hl]
    sub e
    jr nc,.a2
    cpl
    inc a
.a2:add c
    cp 1
    jp nz,.orig                  ; the sign that shares her number
    ld a,b
    ld [$cf13],a
    farcall $708f,1
    farcall $70c0,4
    ld a,[$d35e]
    ld c,a
    ld hl,tab66
.g: ld a,[hl]
    cp c
    jr z,.got
    ld de,7
    add hl,de
    jr .g
.got:
    push hl
    ld de,5
    add hl,de
    ld a,[hl]
    add a
    ld e,a
    ld d,0
    ld hl,tpt66
    add hl,de
    ld a,[hl+]
    ld h,[hl]
    ld l,a
    call $3c94
    pop hl
    inc hl
    inc hl
    inc hl
    ld a,[hl+]
    ld e,a
    ld d,$d8
    ld a,[de]
    ld b,[hl]
    or b
    ld [de],a                    ; talked: gone the next time the map is loaded
    ld hl,sp+4
    ld a,$0c
    ld [hl+],a
    ld a,$2a
    ld [hl],a
    ret
.orig:
    ld a,$2d
    ld hl,$5f19
    jp $0031

tab66:
{tab}    db $ff
tpt66: dw {','.join(hex(a) for a in TA)}
'''
code,L=asm(SRC,CODE,{})
assert CODE+len(code)<TXT
rom.put(fo(B31,CODE),code,'Bank 31: v66 app66 / wrap66 (the town shamanesses)')
# ---- Pallet script: the placeholder (object 5) is hidden always
src65=open('build_v65.py').read()
S65=src65[src65.index("SRC='''")+7:src65.index("'''\ncode,L=asm")]
old_head=S65[S65.index('pal65:'):S65.index('.nogh:')+6]
new_head='''pal66:                           ; Pallet map script (every frame), called from bank 6 6D72
    xor a
    ld [$c150],a                 ; the old placeholder shamaness (object 5) is gone for good
    ld a,$ff
    ld [$c254],a
    ld [$c255],a
'''
S66=S65.replace(old_head,new_head).replace('pal65','pal66').replace('move65','move66')
PCODE=0x6400
assert CODE+len(code)<=TXT and not any(R[fo(B31,PCODE):fo(B31,0x6600)])
pcode,PL=asm(S66,PCODE,{})
rom.put(fo(B31,PCODE),pcode,'Bank 31: v66 pal66 (Pallet script: MR. MU meeting; no placeholder shamaness)')
# ---- hooks to the new code
o=fo(6,0x6d72);assert R[o:o+6].hex()=='21'+le(L65['pal65'])+'0631cf',R[o:o+6].hex()
rom.data(o+1,bytes.fromhex(le(PL['pal66'])),'Pallet script far call -> pal66','21'[:0]+le(L65['pal65']))
o=fo(5,0x7fd0);assert R[o:o+3].hex()=='21'+le(L63['app63'])
rom.data(o+1,bytes.fromhex(le(L['app66'])),'InitMapSprites stub -> app66',le(L63['app63']))
o=fo(0x2f,0x502e);assert R[o:o+8].hex()=='3e3121'+le(L63['wrap63'])+'c33100'
rom.data(o+3,bytes.fromhex(le(L['wrap66'])),'DisplayTextID chain -> wrap66',le(L63['wrap63']))
# ---- remove the old code and texts (v63 app63/wrap63/tables, v63 texts, v65 pal65)
o=fo(B31,0x5000);old=R[o:o+0x163];assert any(old)
rom.data(o,bytes(len(old)),'Bank 31: v63 app63/wrap63 removed',old.hex())
o=fo(B31,0x5800);n=0x5efc-0x5800;old=R[o:o+n];assert not any(R[o+n:o+n+16])
rom.data(o,bytes(n),'Bank 31: v63 shamaness texts removed',old.hex())
o=fo(B31,0x6000);old=R[o:o+0xc0];assert not any(R[o+0xc0:o+0x100])
rom.data(o,bytes(0xc0),'Bank 31: v65 pal65 removed',old.hex())
# ---- the placeholder object in PALLET: position FF,FF
o=fo(6,0x6d17);seg=R[o:o+100];k=seg.find(bytes.fromhex('19130cffd209'));assert k>0
rom.data(o+k+1,bytes([0xff,0xff]),'Pallet object 5 (old placeholder shamaness): position FF,FF','130c')
# ---- sprite sets: undo v63's edits of 3, 4, 7 and use entries no map needs
def setpic(idx,old,new):
    o=fo(5,0x7ab9)+(idx-1)*11
    k=list(R[o:o+11]).index(old);rom.data(o+k,bytes([new]),f'sprite set {idx}: {old:02X} -> {new:02X}',bytes([old]))
SETS=fo(5,0x7ab9)
def setbytes(idx):return list(R[SETS+(idx-1)*11:SETS+idx*11])
for idx,had,orig,new in ((3,0x19,0x0e,0x31),(4,0x19,0x0c,0x31),(7,0x19,0x07,0x05)):
    s=setbytes(idx);k=s.index(had)
    rom.data(SETS+(idx-1)*11+k,bytes([orig]),f'sprite set {idx}: v63 edit undone ({had:02X} -> {orig:02X})',bytes([had]))
    k2=s.index(new);assert k2!=k
    rom.data(SETS+(idx-1)*11+k2,bytes([0x19]),f'sprite set {idx}: {new:02X} -> 19 (CHANNELER; no map using the set has it)',bytes([new]))
rom.finish('Creepy_Black_Mu_v66.gb','manifest_v66.json','CREEPY MU V66',extra=dict(labels=dict(bank31={**{k:hex(v) for k,v in L.items()},**{k:hex(v) for k,v in PL.items()}})))
