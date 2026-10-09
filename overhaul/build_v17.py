# Creepy Black Mu v17: AGATHA stands on FUJI's right (screen right, x11); the chosen girl stands on AGATHA's left
# (FUJI's spot, x10: she only appears after FUJI is rescued and has gone home); AGATHA's "Mu woke them" note no
# longer hints at Mr. Mu. Logged patches on top of verified Mu v16 (patchlib).
import json
from patchlib import *
from patchguard import fo

V16_SHA='5875e91e40856e454032edd9e4b06c7f988b5e4c60d6628425d2e7f4e74a9164'
rom=Rom('Creepy_Black_Mu_v16.gb',V16_SHA)
r=rom.r
L=json.load(open(ROOT/'manifest_v16.json'))['labels']
OBJ=fo(0x18,int(L['bank18']['objects'],16))
AG=OBJ+8+3*8+6                                 # 5th object (AGATHA): header 8, three ROCKETs (8 bytes each), FUJI (6)
assert r[AG:AG+6]==bytes([0x39,3+4,9+4,0xff,0xd0,5])
rom.data(AG+2,[11+4],'Tower 7F: AGATHA on FUJI\'s right (x11)',[9+4])
for i,spr in enumerate((0x1d,0x1b,0x0d)):      # MISTY, ERIKA, SABRINA
    o=AG+6*(i+1);assert r[o:o+6]==bytes([spr,3+4,11+4,0xff,0xd0,6+i])
    rom.data(o+2,[10+4],'Tower 7F: chosen girl on AGATHA\'s left (x10, FUJI\'s spot after he goes home)',[11+4])
# "Mu woke them" note without "That one's work, I suppose."
MU=fo(0x2e,int(L['bank2e']['t_mu'],16))
old=txt([["Hm? You have","already woken","some of them..."],["That one's work,","I suppose."],
         ["Don't worry. The","ritual can still","be done."],["Perhaps it is","even better","this way."]])
new=txt([["Hm? You have","already woken","some of them..."],
         ["Don't worry. The","ritual can still","be done."],["Perhaps it is","even better","this way."]])
assert bytes(r[MU:MU+len(old)])==bytes(old)
rom.data(MU,bytes(new)+bytes(len(old)-len(new)),'AGATHA: drop the line that hints at Mr. Mu',old)
rom.finish('Creepy_Black_Mu_v17.gb','manifest_v17.json','CREEPY MU V17')
