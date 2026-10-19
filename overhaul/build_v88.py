# Creepy Black Mu v88: PROF. OAK's end (CERULEAN CAVE).
#   1. "The MOON STONE shatters!" was printed twice when the E4-style battle (LEAGUE, BLUE, BILL, OAK) ends through METAMORPHOSIS: once at the last faint and again when the kill pass
#      runs TrainerBattleVictory a second time (d05a = 3, the after-win phase). shat88 (2F:5E00) skips the second pass.
#   2. OAK's scene before the fight (garbled picture): the CAVERN tileset animates its water tile every frame (hTileAnimations = 1) and that tile is VRAM $9140 = tile 20 of OAK's picture
#      (drawn at $9000), so a block of the picture flickered; the credits drew over the same animation. anim88 (31:5C00) switches the animation off at the start of both.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V87_SHA='fc50d2c444ba818dc12e6aba491a0097ae0c98fe24c0241fb9326e5ab2faa701'
rom=Rom('Creepy_Black_Mu_v87.gb',V87_SHA)
R=bytes(rom.r)
def lh(a):return a.to_bytes(2,'little').hex()
# ---- 1. shatters once
o5=fo(0xf,0x5046);assert R[o5:o5+8].hex()[4:6]!='' and R[o5]==0x21 and R[o5+3:o5+8].hex()=='062fc31836'
shat84=R[o5+1]|R[o5+2]<<8
A2F=0x5e00
assert not any(R[fo(0x2f,A2F):fo(0x2f,A2F)+0x20])
c2f,L2f=asm(f'''
shat88:                          ; (F:5046 via the far stub) the replaced  call 4658  always; the MOON STONE only on the first pass (d05a = 0), not in the after-win phase (3)
    ld a,[$d05a]
    cp 3
    jp nz,{shat84:#x}
    ld hl,$4658
    ld b,$0f
    db $cf
    ret
''',A2F,{})
rom.put(fo(0x2f,A2F),c2f,'Bank 2F: v88 shat88')
rom.data(o5+1,bytes.fromhex(lh(L2f['shat88'])),'F:5046 far stub -> shat88 (no second "shatters")',lh(shat84))
# ---- 2. no tile animation under the scene / the credits
import json as _j
L62=_j.load(open('manifest_v62.json'))['labels']['bank31']
A31=0x5c00
assert not any(R[fo(0x31,A31):fo(0x31,A31)+0x20])
c31,L31=asm('''
anim88:                          ; (replaces  ld a,$ff / ld [$cd6b],a  at the start of scene62 and ending62) + no water / flower animation (hTileAnimations = 0)
    xor a
    ldh [$d7],a
    ld a,$ff                     ; a = ff on return, as after the replaced instructions (scene62 stops the music with it)
    ld [$cd6b],a
    ret
end88:                           ; the same for the credits + the player's sprite is not drawn (its four OAM entries sat over the text with OBP0 = white: letters missing)
    call anim88
    ld a,$ff
    ld [$c102],a
    ret
''',A31,{})
rom.put(fo(0x31,A31),c31,'Bank 31: v88 anim88')
for nm,lab in (('scene62','anim88'),('ending62','end88')):
    o=fo(0x31,int(L62[nm],16));assert R[o:o+5].hex()=='3eff ea6bcd'.replace(' ',''),nm
    rom.code(o,bytes([0xcd])+bytes.fromhex(lh(L31[lab]))+bytes(2),nm+': ld a,$ff / ld [cd6b],a -> call anim88 (tile animations off: the water tile (VRAM $9140) was overwriting a tile of the picture / the credits)','3eff ea6bcd'.replace(' ',''),
             reviewed='the stub repeats the replaced instructions')
rom.finish('Creepy_Black_Mu_v88.gb','manifest_v88.json','CREEPY MU V88')
