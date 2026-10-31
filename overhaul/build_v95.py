# Creepy Black Mu v95 (on v94): a METAMORPHOSISed NPC's black ball stays put and vanishes when picked up again.
#   v74's killed74 (predef 0x13) called kill_chk2 (2D:6400) directly; v35-v73's killed13 called frame40 (2D:7E51), which does the NPC kill list /
#   waiting-ball work around it (ball = STAY every frame, hide the picked-up ball).  Since v74 a BANEd NPC kept WALKing as a black ball and its sprite
#   stayed on the map after the ball was picked up.  killed74 calls frame40 again.
from patchlib import *
from patchguard import fo
V94_SHA='fd1925a2a6384d5261019b80b4b773fd09694319daeffd8a4de1c7dc6d0767c6'
rom=Rom('Creepy_Black_Mu_v94.gb',V94_SHA)
R=bytes(rom.r)
o=fo(0x2d,0x6240)
assert R[o:o+3].hex()=='cd0064' and R[fo(0x2d,0x6215):fo(0x2d,0x6215)+3].hex()=='cd517e'
rom.code(o,bytes.fromhex('cd517e'),'killed74: call frame40 (waiting balls STAY / picked-up balls hidden, then kill_chk2) instead of kill_chk2 directly','cd0064',reviewed='same registers as the call it replaces: frame40 starts with call 6400 and returns the same Z/NZ')
rom.finish('Creepy_Black_Mu_v95.gb','manifest_v95.json','CREEPY MU V95')
