Creepy Black — Mu Overhaul v68: the MIRAGE encounter chance
============================================================
Built from v67 by build_v68.py (one patch: the roll at 2E:4310 jumps to m68 at 2E:4280).

1. The chance now grows with the victims. Every CURSE use (trainer or POKeMON; counter D45C, saturating at 255) adds 164/256 of one point, so
   chance (out of 256) = victims * 164 / 256, capped at 64 = 25%. The cap is reached at 100 victims (1 victim: 0, 2: 1, 10: 6, 50: 32, 99: 63, 100+: 64).
   Before (v3-v67) every victim added 2 and the 25% cap came after 32.
2. As BLACK (D46C) the MIRAGE never appears in wild encounters (the roll isn't made; the normal wild POKeMON comes).
   Everything else about the MIRAGE is unchanged (it still needs GHOST in the party, a free box slot, no Mirage battle running).

Notes: "victim" = one use of CURSE (the counter v3 made); NPCs cursed on the map only happen as BLACK, when there are no MIRAGE encounters anyway.
Tests: t76_v68.py (the chance read at the roll for 1/2/10/50/99/100/255 victims; no roll at 0 victims; no roll as BLACK even at 100). t28 mirage_rate still passes.
