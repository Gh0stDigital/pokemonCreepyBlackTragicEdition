Creepy Black Mu v96 (on v95): VICTORY ROAD item balls, BLUE's victory music
SHA-256: 3e6ba0459eb7e07b829d3a73547f730e64249cfc5020ba8c6379ed745cc491ff

1. VICTORY ROAD: once trainers there were killed, item balls (or boulders) were drawn with another picture's tiles. Indoor maps have only two VRAM slots for
   four-tile pictures (780/7C0); VICTORY ROAD already uses both (item ball $3D + boulder $3F) and a gravestone ($49) was a third, so two pictures shared a slot.
   Now an indoor map whose objects already hold two different four-tile pictures gets no map-load gravestone: the killed trainer stays hidden (as right after the
   battle; predef 0x13 hides it every frame). Other maps keep their gravestones (MT. MOON checked). Code: grave96 (2D:4C00) wraps load40 behind the far-call stub 0:1688.
2. BLUE (the Champion, class $2B) plays the victory music again at the end of his battle (removed from v86's quiet list at 32:5233); the Elite Four, OAK and BILL stay silent.
Tests: t103_v96.py vr (v95 fails) / blue (v95 fails), t94_v86 fanfare (LORELEI silent, ordinary trainer plays it). run_v96.sh = run_v95.sh + t103.
