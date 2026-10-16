# Creepy Black Mu v70: a scripted grunt you killed with CURSE no longer talks afterwards.
#   NUGGET BRIDGE (ROUTE 24): the Rocket's after-battle script (wRoute24CurScript 3) sets D7EF bit 1 (EVENT_BEAT_ROUTE24_ROCKET) and then shows his text;
#   CERULEAN CITY: the thief's after-battle script (wCeruleanCityCurScript 4) sets D75B bit 7 (EVENT_BEAT_CERULEAN_ROCKET_THIEF) and then shows text 2, whose
#   "beaten" branch prints his speech, gives TM28 and calls 1D:4872 (fade, the house guard moves: objects 7 shown, 9 and 6 hidden).
#   Now, when the grunt's kill bit is set (v34: $1FC thief = D44F bit 4, $1FD Rocket = D44F bit 5) the DisplayTextID call is skipped. The flags set before it still fire;
#   for the thief the event's world change (1D:4872) is run directly. The TM28 is not given (it is part of his speech).
from patchlib import *
from patchguard import fo
from sm83asm import asm

V69_SHA='61abed96f2b3276a2376b5aa71b069ce7c9706094a3a8febc0191ef1a4e9e6bc'
rom=Rom('Creepy_Black_Mu_v69.gb',V69_SHA)
R=bytes(rom.r)
# Route 24 (bank 14): 14:543b  call DisplayTextID  -> call s24
A24=0x7100
s24,_=asm('''
s24:
    ld a,[$d44f]
    bit 5,a
    ret nz               ; the Rocket is dead: no words
    jp $294d
''',A24,{})
rom.put(fo(0x14,A24),s24,'Bank 14: v70 NUGGET BRIDGE Rocket: dead = no after-battle text')
o=fo(0x14,0x543b);assert R[o:o+3].hex()=='cd4d29'
rom.hook(o,'cd'+le(A24),'Route 24 Rocket after battle: text through s24 (skipped when he is dead)','cd4d29',reviewed='the stub ends in the original jp DisplayTextID or returns; nothing after the call reads a register')
# Cerulean (bank 6): 06:54bd  call DisplayTextID -> call s03
A03=0x7000
s03,_=asm('''
s03:
    ld a,[$d44f]
    bit 4,a
    jp z,$294d
    ld hl,$4872          ; the thief is dead: no speech, no TM28; the event's world change still happens (fade, the guard leaves the house)
    ld b,$1d
    jp $3618
''',A03,{})
rom.put(fo(6,A03),s03,'Bank 06: v70 CERULEAN thief: dead = no after-battle text, the event goes on')
o=fo(6,0x54bd);assert R[o:o+3].hex()=='cd4d29'
rom.hook(o,'cd'+le(A03),'Cerulean thief after battle: text through s03 (skipped when he is dead)','cd4d29',reviewed='the stub ends in the original jp DisplayTextID or a far call; nothing after the call reads a register')
rom.finish('Creepy_Black_Mu_v70.gb','manifest_v70.json','CREEPY MU V70')
