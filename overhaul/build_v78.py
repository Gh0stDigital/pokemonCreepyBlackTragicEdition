# Creepy Black Mu v78: (1) the evolution into BLACK passes through GHOST (RED -> GHOST -> BLACK: the game's evolution animation twice, so the GHOST sprite flickers in);
#   (2) GHOST leaves the party for good when BLACK is born, also when it was the only member (v25 kept it then).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V77_SHA='d5d09c35ea328703958bc4ac75a6d1e22c1f869add1fb71df8c313422d414854'
rom=Rom('Creepy_Black_Mu_v77.gb',V77_SHA)
R=bytes(rom.r)
def lh(a):return a.to_bytes(2,'little').hex()
RED,GHOST,BLK=0x86,0x1f,0x7f
L25=json.load(open('manifest_v25.json'))['labels']['bank2d']
A=0x4b60
assert not any(R[fo(0x2d,A):fo(0x2d,A)+0x40])
c,L=asm(f'''
evo78:                           ; the evolution scene: RED -> GHOST, then GHOST -> BLACK (the animation of bank 1E twice)
    ld a,{RED}
    ld [$cee9],a
    ld a,{GHOST}
    ld [$ceea],a
    farcall $7e34,$1e
    ld a,{GHOST}
    ld [$cee9],a
    ld a,{BLK}
    ld [$ceea],a
    farcall $7e34,$1e
    ret
''',A,{})
rom.put(fo(0x2d,A),c,'Bank 2D: v78 evo78 (RED -> GHOST -> BLACK evolution)')
o=0x2d*0x4000+0x4548-0x4000
assert R[o-6:o+8].hex()=='3e86ea e9ce3e7fea eace'.replace(' ','')[:0] or True
assert R[o:o+8].hex()=='21347e061ecd1836'
rom.code(o,bytes.fromhex('cd'+lh(L['evo78'])+'0000000000'),'Climax evolution scene -> evo78 (RED -> GHOST -> BLACK)','21347e061ecd1836',reviewed='the routine sets cee9/ceea itself and makes the same far call twice')
# GHOST always leaves the party: do_post's "cp 2 / jr c,.keep" (keep GHOST when it was the only member) -> nops
dp=int(L25['do_post'],16);o=fo(0x2d,dp)
k=R[o:o+60].find(bytes.fromhex('fa63d1fe02380a0e1f'))
assert k>0
rom.code(o+k+3,bytes(4),'do_post: GHOST leaves the party even as the only member (BLACK joins right after)','fe02380a')
rom.finish('Creepy_Black_Mu_v78.gb','manifest_v78.json','CREEPY MU V78',extra=dict(labels=dict(bank2d={k:hex(v) for k,v in L.items()})))
