# Creepy Black Mu v89: the early rival fight on ROUTE 22 (the first one, opponent E1 = RIVAL1): after the battle BLUE says something shocking when the player CURSEd (GHOST route).
#   The shock flags (D463 = 1, Cerulean / S.S. ANNE / ROUTE 22 skipped) and GHOST's hesitation ("BLUE ran away!") already come from v12's class-wide hooks (checked in t97);
#   what stayed was his ordinary speech after "ran away" ("I heard POKeMON LEAGUE has many tough trainers..."). r22a89 (bank 14:6BA0) = the text-1 chooser: before the battle as
#   always; after it: the shock text when D452 (CURSE used in this battle), else the original.
from patchlib import *
from patchguard import fo
from sm83asm import asm

V88_SHA='a44bd6ff4cf77ea19578f43f9cc57f5fa65d5bd68a1178778e9cdb8771674276'
rom=Rom('Creepy_Black_Mu_v88.gb',V88_SHA)
R=bytes(rom.r)
def lh(a):return a.to_bytes(2,'little').hex()
A14=0x6ba0
assert not any(R[fo(0x14,A14):fo(0x14,A14)+0x100])
shock=txt([["What was that?!"],["My #MON...","They went limp."],["That thing of","yours isn't a","#MON, is it?!"],["Stay away from","me! I'm telling","GRAMPS!"]])
# text first (its address is needed by the chooser)
c,L=asm(f'''
r22a89: db 8
    ld a,[$d7eb]
    bit 5,a
    jr z,.pre
    ld a,[$d452]
    and a
    jr nz,.shock
    ld hl,$51b2
    jr .p
.pre:
    ld hl,$51ad
    jr .p
.shock:
    ld hl,shock89
.p: call $3c94
    jp $2504
shock89: db {','.join(str(x) for x in shock)}
''',A14,{})
rom.put(fo(0x14,A14),c,'Bank 14: v89 r22a89 (ROUTE 22 text 1: BLUE after the battle, shocked when CURSE was used) + text')
o=fo(0x14,0x5175);assert R[o:o+2].hex()=='7b51'
rom.data(o,bytes.fromhex(lh(L['r22a89'])),'ROUTE 22 text 1 -> r22a89','7b51')
rom.finish('Creepy_Black_Mu_v89.gb','manifest_v89.json','CREEPY MU V89',extra=dict(labels=dict(bank14={k:hex(v) for k,v in L.items()})))
