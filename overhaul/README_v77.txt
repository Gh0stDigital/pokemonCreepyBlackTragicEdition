Creepy Black — Mu Overhaul v77: the ritual, five fixes
=======================================================

ROM:     Creepy_Black_Mu_v77.gb
SHA-256: d5d09c35ea328703958bc4ac75a6d1e22c1f869add1fb71df8c313422d414854
Input:   Creepy_Black_Mu_v76.gb. build_v77.py asserts every byte it replaces; manifest_v77.json logs them.

1. TOWER CHAMBER music: none until the player is BLACK. The map music read (0:1249, v51's music51) goes through music77 (bank 30:4400): map 69 and D46C = 0 -> music id FF (stop).
   When BLACK is born (the v25 flag store, now mus77r in 2D:4B00) the music id is read again (rmus77 -> music51), so the room's own song starts after the climax battle.
2. MR. MU's battle: the player (YOU, species 79, RIT 1) is "just there" like BLACK leading a battle: no slide of the trainer picture, no "Go! RED!", no summoning animation;
   the HUD and the menu follow MR. MU's "stepped into the circle" (the battle-start stub F:7FB8 -> pre77, which is v46's pre46 plus this case; v46's msg46 does the quiet send-out).
3. No victory fanfare on map 69: the two callers of PlayBattleVictoryMusic (wild F:45DF -> vicw77, trainer F:46C6 -> vict77, bank 30) skip it there; everywhere else the same fanfare plays as before
   (t85 victory). The ritual battles never reached it in the emulator (MR. MU dies mid-trainer-battle, the MIRAGE is caught, the climax ends by script), so this is a guard.
4. The three fossil sprites stay on their stands until the player is BLACK (RIT 6); before, they vanished at RIT 3 (right after MR. MU's battle). (chamber script 18:script_ch: cp 3 -> cp 6)
5. The climax battle (wild GHOST Lv100): the player gets one turn first.
   RIT 5 = battle, first menu (cm77, 2D:4B0E, replaces climax_menu's entry): shown normally, RIT -> 7 ("the player's turn is pending").
   RIT 7: PKMN / ITEM / RUN are refused ("GHOST's aura holds you here!", 2E:7820 menu77 in the battle-menu chain); FIGHT is allowed (YOU has STRUGGLE only).
   The enemy's turn (F:67C8 via rst 08 -> et77) is skipped silently while RIT = 7 and sets RIT = 8 (whichever goes first, both happen before the next menu).
   RIT 8: at the next menu GHOST takes its turn: RIT -> 5 and the old climax runs unchanged ("GHOST used CURSE!", ~5 s black, the evolution, BLACK).

Tests (t85_v77.py): chamber (no music at entry, MR. MU start without "Go!", no victory ids during the ritual), fossils (RIT 0/3/4: present, 6: gone), climax (first menu RIT 7, RUN refused,
STRUGGLE before CURSE, GHOST does nothing in between, BLACK, chamber music id back), victory (normal wild win still plays F9). t34 ritual/no/bagfull/boxfull/partyfull/wild/sendout, t35 climax/agatha/house/sprites,
t46 join/faint, t54 start/ball/lv100, t59 mu/music, t61 altar/door/ritualstash (the RIT-3 fossil check changed) pass.
