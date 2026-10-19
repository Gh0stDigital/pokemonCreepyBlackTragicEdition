Creepy Black Mu v88 (on v87): PROF. OAK's end in the CERULEAN CAVE (scene picture, battle end, credits)
SHA-256 a44bd6ff4cf77ea19578f43f9cc57f5fa65d5bd68a1178778e9cdb8771674276

1. Garbled picture in OAK's scene: the CAVERN tileset animates its water tile every frame (hTileAnimations $FFD7 = 1) and that tile is VRAM $9140 = tile 20 of the
   picture the scene draws at $9000, so a block of OAK's picture changed every few frames. anim88 (bank 31:5C00) switches the animation off at the start of the scene (scene62)
   and of the ending (ending62); both start with the old "ld a,$ff / ld [$cd6b],a" which anim88 repeats.
2. Credits: the player's four OAM entries stayed on screen with OBP0 = white and covered letters in the middle of the staff roll ("SATOSI TAJIRI", "KEN ! GIMORI", "JUNICI MASUDA").
   end88 (the ending's start) also hides the player's sprite (image index $FF). The original staff roll is unchanged.
3. "The MOON STONE shatters!" printed a second time after the METAMORPHOSIS kill of an E4-style trainer (LEAGUE, BLUE, BILL, OAK): TrainerBattleVictory runs again in the
   after-win phase (d05a = 3). shat88 (2F:5E00, via the F:5046 far stub) skips the MOON STONE text in that pass.
Not reproduced: a blank screen / freeze in the scene (the scene, the fight and the credits run completely in the emulator tests). If the scene still looks wrong on your device,
tell me what it shows.
Tests: t96_v88.py oak lorelei. run_v88.sh = run_v87.sh + t96.
