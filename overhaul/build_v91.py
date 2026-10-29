# Creepy Black Mu v91: cave tile bug (MT. MOON, ROCK TUNNEL, CERULEAN CAVE, VICTORY ROAD ... = the CAVERN tileset) fixed.
#   v20 / v21 wrote the TOWER CHAMBER's 15 custom blocks (slots 6E-7C) at 1B:4CA0-4D8F, believing the Tower blockset (1B:45C0) had 176 slots. It has 110 ($6E): 1B:4CA0 is the CAVERN
#   TILESET'S GRAPHICS (tiles 0-14), so every cave drew 15 wrong tiles (walls / floor) since v20.
#   Fix: the original 240 bytes are back at 1B:4CA0; the Tower tileset (gfx 1B:4000, $5C0 bytes, + blocks 1B:45C0 with the 15 chamber blocks as slots 6E-7C) is copied to bank 32:6000
#   and the Tower tileset header (0:C872: bank, blocks ptr, gfx ptr) points there.
from patchlib import *
from patchguard import fo

V90_SHA='8c4a4394321e4cb94f8cb8f9b20b4240413a0c0257ce3c8ef3546be279050a96'
rom=Rom('Creepy_Black_Mu_v90.gb',V90_SHA)
R=bytes(rom.r)
R1=open('Creepy_Black_Mu_v1.gb','rb').read()
def lh(a):return a.to_bytes(2,'little').hex()
cs,ce=fo(0x1b,0x4ca0),fo(0x1b,0x4d90)
orig=R1[cs:ce];assert R1[cs:ce]==open('Creepy_Black_Mu_v19.gb','rb').read()[cs:ce]
chamber=R[cs:ce]                                  # the 15 blocks v20/v21 put there (slots 6E-7C)
gfx=R[fo(0x1b,0x4000):fo(0x1b,0x45c0)]
blocks=R[fo(0x1b,0x45c0):cs]                     # the Tower's own 110 blocks (slots 00-6D)
assert len(gfx)==0x5c0 and len(blocks)==0x6e*16
NB,NA=0x32,0x6000
assert not any(R[fo(NB,NA):fo(NB,NA)+0xe00])
rom.put(fo(NB,NA),gfx+blocks+chamber,'Bank 32: v91 Tower tileset copy (gfx $5C0 + 110 blocks + the 15 chamber blocks)')
rom.data(cs,orig,'1B:4CA0: the CAVERN gfx tiles 0-14 are back (v20/v21 had overwritten them with chamber blocks)',chamber)
h=0xc872;assert R[h:h+7].hex()=='1bc045004 0c717'.replace(' ','')
rom.data(h,bytes([NB])+bytes.fromhex(lh(NA+0x5c0)+lh(NA)),'Tower tileset header: bank 32, blocks 6000+5C0, gfx 6000','1bc04500 40'.replace(' ',''))
rom.finish('Creepy_Black_Mu_v91.gb','manifest_v91.json','CREEPY MU V91')
