Creepy Black — Mu Overhaul v7: PRETA's sight, cleaner back sprite, PRETA's revival
==================================================================================

ROM:     Creepy_Black_Mu_v7.gb
SHA-256: 95a2107114dc7246cda7dfbba4cc56fde37fdb144fa2a8e4456b36caedbc8a45
Input:   Creepy_Black_Mu_v6.gb. build_v7.py asserts every byte it replaces; manifest_v7.json logs them.

WHAT'S NEW
----------
1. SILPH SCOPE effect: while PRETA (species B6) is anywhere in the party, Pokémon Tower ghosts are
   identified exactly as if the SILPH SCOPE were in the bag ("Wild GASTLY appeared!" instead of
   "GHOST appeared! Darn! The GHOST can't be ID'd!"). Both game checks are hooked: IsGhostBattle
   (F:5920) and PrintBeginningBattleText (16:4DD8).
2. Fossil Kabutops back sprite: the light-grey patches on its back are now white (38 px). The
   dark-grey rib lines and black outline/spine are unchanged. Kept as kab_back_v7.bin.
3. PRETA's revival: if PRETA faints, after 2 more turns it rises at full HP with no status
   ("PRETA rose from the dead!", uses its nickname) and can be sent out again. If the battle
   ends while it is still down, it is restored to full HP right after the battle. This runs
   before the Mirage cleanup, so PRETA is never permanently lost to the Black Tamer.
   Turns are counted at the start of each battle-loop pass (MainInBattleLoop, F:4233).

New saved RAM: D461 PRETA revival countdown (cleared after every battle).

VERIFIED IN PYBOY (run_v7.sh)
-----------------------------
- Pokémon Tower 3F with PRETA: "Wild GASTLY appeared!"; same save without PRETA: GHOST, can't be ID'd.
- PRETA fainted on turn 1, the switched-in CHARMANDER fought turns 2 and 3, then "PRETA rose from the
  dead!", party HP 0 -> 135, status 0, countdown back to 0.
- Fainted PRETA, then ran from battle: HP 135 after the battle.
- All v6 checks and the v1-v5 chain still pass. (t15_aero needs the Mirage roll to give Aerodactyl;
  in this run's regenerated states it gave Kabutops, which also failed identically on v6.)

KNOWN LIMITS
------------
- If PRETA is your last Pokémon standing when it faints, you black out as usual (the battle can't
  continue with nobody out); it is restored to full HP after the blackout.
- The revival timer counts battle-loop passes; in trainer battles the enemy sending in its next
  Pokémon can count as a turn.
