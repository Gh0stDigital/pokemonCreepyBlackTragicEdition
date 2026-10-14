# Creepy Black Mu v61: BILL's team and picture. FLAREON 56, VAPOREON 56, JOLTEON 56, CHANSEY 56, ALAKAZAM 58, PORYGON 60 (last); the PSYCHIC trainer picture.
from patchlib import *
from patchguard import fo
V60_SHA='e1452074130a55008cbab105c3ef5297d07a4453260fef05694cd08713ac756c'
rom=Rom('Creepy_Black_Mu_v60.gb',V60_SHA)
R=bytes(rom.r)
PARTY=0x7ef0
old=R[fo(0xe,PARTY):fo(0xe,PARTY)+14];assert old.hex()=='ff3a953836388d3a6800'+'00000000'
new=bytes([0xff,56,0x6a,56,0x69,56,0x68,56,0x28,58,0x95,60,0xaa,0])
rom.data(fo(0xe,PARTY),new,"BILL's party: FLAREON, VAPOREON, JOLTEON, CHANSEY, ALAKAZAM, PORYGON",old)
PM=0x39952;o=PM+5*25
assert R[o:o+2].hex()=='7d62' and R[PM+5*18:PM+5*18+2].hex()=='2857'
rom.data(o,bytes.fromhex('2857'),"Class 26 (BILL) picture = the PSYCHIC trainer's",'7d62')
rom.finish('Creepy_Black_Mu_v61.gb','manifest_v61.json','CREEPY MU V61')
