# Creepy Black Mu v102 (on v101): BILL's first POKeMON is FLAREON. v61 wrote species $6A there (= MACHOP; FLAREON is $67), and t69 checked
# the same wrong number. BILL's party (E:7EF0): FLAREON 56, VAPOREON 56, JOLTEON 56, CHANSEY 56, ALAKAZAM 58, PORYGON 60.
from patchlib import *
from patchguard import fo
V101_SHA='0409c8bdafe3a2ffa05282c19d52bb2984c507a41aecf1621ab036298c85c3c7'
rom=Rom('Creepy_Black_Mu_v101.gb',V101_SHA)
R=bytes(rom.r)
NAMES=0x1c21e;FLAREON=0x67
assert R[NAMES+10*(FLAREON-1):NAMES+10*(FLAREON-1)+7].hex()=='858b8091848e8d'     # "FLAREON"
o=fo(0xe,0x7ef0)
assert R[o:o+14].hex()=='ff386a386938683828 3a953caa00'.replace(' ','')
rom.data(o+2,bytes([FLAREON]),"BILL's first POKeMON: FLAREON ($67), was MACHOP ($6A)",'6a')
rom.finish('Creepy_Black_Mu_v102.gb','manifest_v102.json','CREEPY MU V102')
