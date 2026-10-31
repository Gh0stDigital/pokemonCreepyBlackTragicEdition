# Creepy Black Mu v94 (on v93): the climax evolution scene is RED -> BLACK only (v78's detour through the GHOST sprite is gone).
from patchlib import *
from patchguard import fo
V93_SHA='40257145a00edb4eb616c5b2f3923a488adf059ef4521f4533aed0b64c2e59b0'
rom=Rom('Creepy_Black_Mu_v93.gb',V93_SHA)
R=bytes(rom.r)
RED,BLK=0x86,0x7f
A=0x4b60
o=fo(0x2d,A)
old=R[o:o+25]
assert old.hex().startswith('3e86 ea e9 ce 3e1f ea ea ce'.replace(' ','')),old.hex()
# evo78: ld a,RED / ld [cee9],a / ld a,GHOST / ld [ceea],a / farcall 1E:7E34 / ld a,GHOST / ld [cee9],a / ld a,BLK / ld [ceea],a / farcall / ret
print(R[o:o+0x30].hex())
new=bytes.fromhex('3e86ea e9ce 3e7f eaeace'.replace(' ',''))   # ld a,RED / ld [cee9],a / ld a,BLK / ld [ceea],a
k=old.hex().find('21347e061e')  # the farcall bytes (ld hl,7E34 / ld b,1E / call 3618)
call=R[o+10:o+10+8]
assert call.hex()=='21347e061ecd1836',call.hex()
tail=new+call+b'\xc9'
n=R[o:o+0x30].find(b'\xc9')+1                       # the old routine ends at its first ret after the second call
rom.code(o,tail+bytes(n-len(tail)),'evo78: RED -> BLACK in one evolution animation (no GHOST sprite)',R[o:o+n].hex(),reviewed='the routine sets cee9/ceea itself and makes the same far call once')
rom.finish('Creepy_Black_Mu_v94.gb','manifest_v94.json','CREEPY MU V94')
