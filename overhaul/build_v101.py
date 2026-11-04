# Creepy Black Mu v101 (on v100): the town SHAMANESSES are gone once the player is BLACK.
# app66 (31:4900, called from InitMapSprites) appends this town's shamaness. It now starts with sham101 (31:7D00): when D46C (BLACK) is set it
# jumps to app66's own ".wipe" path (31:4993, the "talked to: gone" case = nothing of her is left in the slot after the last real sprite),
# else it runs app66's first two instructions (ld a,[D35E] / ld c,a) and goes on at 31:4904 as before.
from patchlib import *
from patchguard import fo
V100_SHA='a2d7f8b1656f4c8b4c0eccc216b1ceba8cc96a06a6df4a4cb61ef61ae6a0d600'
rom=Rom('Creepy_Black_Mu_v100.gb',V100_SHA)
R=bytes(rom.r)
B=0x31;APP=0x4900;WIPE=0x4993;STUB=0x7d00
assert R[fo(B,WIPE):fo(B,WIPE)+6].hex()=='fae1d4fe0fd0'          # .wipe: ld a,[$d4e1] / cp 15 / ret nc
assert R[fo(B,APP+4):fo(B,APP+7)].hex()=='214467'               # ld hl,tab66 follows
le=lambda a:'%02x %02x'%(a&255,a>>8)
stub=bytes.fromhex('fa 6c d4 a7 c2 '+le(WIPE)+' fa 5e d3 4f c3 '+le(APP+4))
rom.put(fo(B,STUB),stub,'Bank 31: sham101 (no shamaness as BLACK)')
rom.code(fo(B,APP),bytes.fromhex('c3 '+le(STUB)+' 00'),'app66: start with sham101','fa 5e d3 4f')
rom.finish('Creepy_Black_Mu_v101.gb','manifest_v101.json','CREEPY MU V101')
