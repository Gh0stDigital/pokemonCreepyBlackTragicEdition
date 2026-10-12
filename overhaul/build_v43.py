# Creepy Black Mu v43: the black ball on the map (sprite 47, a BANEd NPC) uses the POKe BALL of the battle throw animation
#   (MoveAnimationTiles0 tiles 06/07/16/17, frame block at 1E:712A), as it lies after landing, blacked out: black body,
#   the seam between the halves and the old shine kept in grey so it still reads as a ball. Replaces v40's item-ball copy.
import json
from patchlib import *
from patchguard import fo

V42_SHA='8c0fff599dd64158059f132e17ed6779e8f8ab00b5c9c62c0afa37d7a96621be'
rom=Rom('Creepy_Black_Mu_v42.gb',V42_SHA)
r=rom.r;R=bytes(r)
SHEET=int(json.load(open('manifest_v40.json'))['labels']['bank2f']['sheet'],16)
ANIM=fo(0x1e,0x41fe)
FB=fo(0x1e,0x712a)
assert R[FB:FB+17]==bytes([4,0,0,6,0,0,8,7,0,8,0,0x16,0,8,8,0x17,0])   # the toss ball's frame block (TL 06, TR 07, BL 16, BR 17)

def tile(t):
    o=ANIM+t*16
    return [[((R[o+y*2+1]>>(7-x))&1)<<1|((R[o+y*2]>>(7-x))&1) for x in range(8)] for y in range(8)]
q=[tile(t) for t in (6,7,0x16,0x17)]
ball=[q[0][y]+q[1][y] for y in range(8)]+[q[2][y]+q[3][y] for y in range(8)]

# blacken: inside the outline everything black, except the seam (where the dark top meets the light bottom) and the shine
new=[[0]*16 for _ in range(16)]
for Y in range(16):
    for X in range(16):
        c=ball[Y][X]
        if c==0:continue
        if c==1 and Y<8:new[Y][X]=2                            # the shine on the top half (rows 6-7)
        elif c==1 and ball[Y-1][X]==2:new[Y][X]=1              # seam: first light pixel under the dark top half
        else:new[Y][X]=3
# centre it horizontally (the ball sits at columns 1-12)
cols=[X for X in range(16) if any(new[Y][X] for Y in range(16))]
sh=(16-(cols[-1]-cols[0]+1))//2-cols[0]
new=[[new[Y][X-sh] if 0<=X-sh<16 else 0 for X in range(16)] for Y in range(16)]
print('\n'.join(''.join(' .:#'[c] for c in row) for row in new))

sheet=bytearray()
for t in range(4):
    tx,ty=t&1,t>>1
    for y in range(8):
        lo=hi=0
        for x in range(8):c=new[ty*8+y][tx*8+x];lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
        sheet+=bytes([lo,hi])
o=fo(0x2f,SHEET)
rom.data(o,bytes(sheet),'Sprite 47 (black ball on the map) = the battle-throw POKe BALL, blacked out',R[o:o+64])

# ---- the ball needs graphics in VRAM: outdoor maps only load their sprite set, so picture 47 was never loaded there
#      (the loader looked 47 up in the set, missed, and gave the ball a garbage slot = some other sprite's tiles).
#      ball_fix (2F): every sprite with picture 47 gets four-tile slot 0C ($87C0; 0B = $8780 if 0C belongs to another
#      sprite) and the ball tiles are copied there. Run after every InitMapSprites (map load, redraw after menus/text)
#      and right after the BANE.
from sm83asm import asm
B2F=0x6000
assert not any(R[fo(0x2f,B2F):fo(0x2f,B2F+0x200)])
ADD_BANE=int(json.load(open('manifest_v40.json'))['labels']['bank2f']['add_bane'],16)
c2f,L=asm(f'''
ball_fix:
    ld hl,$c110
    ld b,15
    ld c,$0c
.p1:ld a,[hl]
    and a
    jr z,.n1
    cp $47
    jr z,.n1
    push hl
    inc h
    ld a,l
    or $0e
    ld l,a
    ld a,[hl]
    pop hl
    cp $0c
    jr nz,.n1
    ld c,$0b
.n1:ld a,l
    add $10
    ld l,a
    dec b
    jr nz,.p1
    ld hl,$c110
    ld b,15
    ld d,0
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
    ld d,1
.n2:ld a,l
    add $10
    ld l,a
    dec b
    jr nz,.p2
    ld a,d
    and a
    ret z
    ld hl,$87c0
    ld a,c
    cp $0c
    jr z,.d
    ld hl,$8780
.d: ld a,[$cfc4]
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
bane_add:                        ; bane_npc: after the picture became 47
    call {ADD_BANE:#x}
    jp ball_fix
''',B2F)
rom.put(fo(0x2f,B2F),c2f,'Bank 2F: v43 ball_fix (black ball graphics in a four-tile sprite slot)')
rom.code(fo(0x2f,0x50c3),'cd'+le(L['bane_add']),'bane_npc: call add_bane -> bane_add (+ ball graphics)','cd'+le(ADD_BANE))
W5=0x7fb0
assert not any(R[fo(5,W5):fo(5,W5+0x20)])
c5,L5=asm(f'''
init_w:
    call $797b                   ; InitOutsideMapSprites
    jr c,.out
    call $785f                   ; indoor part of InitMapSprites
.out:
    ld hl,{L['ball_fix']:#x}
    ld b,$2f
    jp $3618
''',W5)
rom.put(fo(5,W5),c5,'Bank 5: v43 InitMapSprites wrapper (then ball_fix)')
rom.code(fo(5,0x785b),'c3'+le(W5),'InitMapSprites -> init_w (ball graphics after every sprite load)','cd7b79')
rom.finish('Creepy_Black_Mu_v43.gb','manifest_v43.json','CREEPY MU V43',extra=dict(labels={'bank2f':{k:hex(v) for k,v in L.items()},'bank5':{k:hex(v) for k,v in L5.items()}}))
