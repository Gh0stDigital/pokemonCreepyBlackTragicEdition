# Creepy Black Mu v42: a BANEd NPC (the black POKe BALL on the map) can't move.
#   v40 only changed the NPC's picture to the ball (sprite 47): its movement byte stayed WALK ($FE), so a wandering
#   NPC's ball kept walking around. Now the waiting ball's movement byte 1 (C2x6) is set to STAY ($FF)
#   - per frame (v40 frame40, the "waiting ball: draw it" path): right after the BANE and as long as the ball waits;
#   - at map load (v40 load40, which gives a waiting ball its picture again): the map data would reload WALK there.
#   Every other NPC keeps its movement.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V41_SHA='4630edb47863963a8bd1595a0ec44c1b4af60927de8de31ba4e0bad85cdaa657'
rom=Rom('Creepy_Black_Mu_v41.gb',V41_SHA)
r=rom.r;R=bytes(r)
L40={k:int(v,16) for k,v in json.load(open('manifest_v40.json'))['labels']['bank2d'].items()}
BALLPIC=0x47
LOAD40,FRAME40,PEND2D=L40['load40'],L40['frame40'],L40['pend2d']
assert (LOAD40,FRAME40,PEND2D)==(0x7e40,0x7e51,0x7e7b)

C=0x7eb0
assert not any(R[fo(0x2d,C):fo(0x2d,0x7f00)])
code,L=asm(f'''
setball:                         ; load40, a waiting ball (e = sprite offset): ball picture + stay
    ld l,e
    ld h,$c1
    ld [hl],{BALLPIC}
still:                           ; frame40, a waiting ball: movement byte 1 = STAY, draw it (Z)
    ld a,e
    or 6
    ld l,a
    ld h,$c2
    ld [hl],$ff
    xor a
    ret
''',C)
rom.put(fo(0x2d,C),code,'Bank 2D: v42 waiting black ball stays put (C2x6 = FF)')

# load40: ld l,e / ld h,$c1 / ld [hl],$47 / xor a / ret -> jp setball
A=LOAD40+10
rom.code(fo(0x2d,A),bytes.fromhex('c3'+le(L['setball']))+b'\x00'*4,'load40: waiting ball -> setball (picture + STAY)',
         bytes.fromhex('6b26c13647afc9'))
# frame40: jr c,.draw (pend2d carry = a ball waits) -> jr c,still
J=FRAME40+11
rom.code(fo(0x2d,J),bytes([0x38,L['still']-(J+2)]),'frame40: waiting ball -> still (STAY, then draw)',bytes.fromhex('3818'))
rom.finish('Creepy_Black_Mu_v42.gb','manifest_v42.json','CREEPY MU V42',extra=dict(labels={'bank2d':{k:hex(v) for k,v in L.items()}}))
