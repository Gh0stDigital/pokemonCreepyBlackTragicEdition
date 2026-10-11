Creepy Black Mu v36 (on v35): GHOST level cap, Tower 7F map fix, GIOVANNI's name, BLUE after SILPH.

1. GHOST can't go past Lv50, and AGATHA's quest needs it at Lv50 (was Lv100).
   GainExperience (15:5308, "call GetMonHeader / ld d,100") now calls lvcap (15:6A90): for GHOST (species 1F) the
   experience is capped at the Lv50 value instead of Lv100, so it reaches 50 and stops. A GHOST that is already above 50
   (older save) keeps its level and grows no further (no level drop). Every other POKeMON is unchanged (Lv100 cap).
   AGATHA's stage-3 check (2E:6963, "cp 100") is "cp 50": Lv49 = "still too weak", Lv50 = HELIX FOSSIL back.
   Rare Candy was already refused for GHOST (v9). Not changed: the Day Care (GHOST is never left there in the story).

2. The Tower 7F map turned to garbage after the START menu (since v16). The overhaul hides map objects (AGATHA, the
   girls, the second AGATHA, ...) by setting their picture ID to 0. When the map is redrawn after a menu, the game
   reloads every sprite sheet (LoadMapSpriteTilePatterns, 5:7871) and loaded one for "picture 0" from the 4 bytes in
   front of SpriteSheetPointerTable: bank 41 (= bank 1, text), 255 tiles, written from 8A40 on, right over the map tiles.
   Fix: the loader skips picture 0 (5:788D -> skip0 at 5:7F90). Same fix for every map that hides objects that way
   (MISTY/ERIKA/SABRINA's gym after she left, the player's house with the consort).

3. GIOVANNI at SILPH 11F (GHOST route): the battle engine prints "GIOVANNI:" in front of a trainer's defeat line, and
   the v18 line started with "GIOVANNI:" too ("GIOVANNI: GIOVANNI:"). The line is now just "Damn that cult..." (2E:7AEE).

4. BLUE after the SILPH CO. 7F battle (GHOST route; text 15 -> 14:6B40, text at 2D:7800). Hero mode is set as before.
   "What... what happened to you, <PLAYER>?" / "That thing isn't a normal #MON." / "And you... you're not the same
   either." / "Something dark got into you. Into both of you." / "I don't get it. But I can feel it..." /
   "Just beating you won't be enough. Not like this." / "I'll find a way to overcome that dark power!" /
   "I swear it, <PLAYER>!"   Off the GHOST route: his original "moving on up" text.

Tests: t45_v36.py (run_v36.sh = run_v35.sh + t45):
  tower       Tower 7F (stage 5, consort MISTY, objects hidden with picture 0): map tiles identical to the tileset after
              START menu open/close (four times) and the screen unchanged; MISTY's gym after she left the same;
              Pallet (nothing hidden) as before. On v35 the same check fails (tiles from bank 1 over 9000-95FF).
  agatha      stage 3: GHOST Lv49 "too weak" (stage stays 3), Lv50 -> "devotion", stage 4.
  cap         wild battle (SCRATCH, enemy at 1 HP): GHOST Lv49 just below Lv50 -> 50; GHOST Lv50 with far too much exp
              -> stays 50, exp = the Lv50 value; GHOST Lv60 -> stays 60; CHARMANDER Lv50 -> grows past 50 (normal case).
  giovanni    defeat screen "GIOVANNI:" / "Damn that cult...", never "GIOVANNI: GIOVANNI:".
  blue        GHOST route: new lines ("happened to you", "dark power"), not "moving on up", hero mode set.
  blue_normal off the GHOST route: original text.
Static: check_hooks.py 91 hooks, 0 problems.
Regression (run_v36.sh = run_v35.sh + t45): PASS=271 FAIL=0.
