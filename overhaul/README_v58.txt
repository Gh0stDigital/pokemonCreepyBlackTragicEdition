Creepy Black Mu v58 (from v57): BLUE (the Champion) as BLACK, and the end of the POKeMON LEAGUE
SHA-256 a2a2e78a23c31a6deadffdf3f85d1d17727411ff3e06f7307f4d7d0a11ba4afd

Champion's room (map 78), as BLACK (D46C):
- the cut-scene starts by itself while BLUE is alive (D64C = 1); BLUE's new before-battle and defeat speeches
- BLUE counts as an Elite Four battle (MOON STONE: forbidden moves refused with his line, it shatters after his last POKeMON,
  BANE kills him). He has no trainer header: his kill index is LANCE's (v34 scripted-trainer table, map 78 / RIVAL3 sets 1-3).
- after the battle: no OAK, no Hall of Fame sequence, the Elite Four's beaten flags are NOT reset; the player walks 4 steps up into the
  Hall of Fame by himself; BLUE's object is gone for good.
Hall of Fame (map 76), as BLACK: own script (bank 30 hof58). D876 = stage (0 none, 1 BLUE beaten, 2 walking in, 3 AGATHA walking in, 4 done).
  The player walks 3 steps in, AGATHA (OAK's object turned into picture 39, InitMapSprites for her tiles) comes in through the door and speaks
  her "after the Elite Four" speech; then the player is free. Later talks: the last three lines. AGATHA's picture is exempt from the v28 NPC
  takeover (new exempt list at 2D:7E10). GHOST route: everything as before.
Also: LANCE's defeat speech has the "Agatha... Was this your plan all along...?" line.
Notes: an object list at another address than the header's crashed LoadMapHeader's follow-up (arrival at 0,0), so no list swap; the walk must not
  leave simulated joypad steps over the warp (4 ups from y=3 end exactly on the warp).
Code: bank 1D:7EA8 champ58/rival58/def58/s3_58; bank 16:7100 hof_s + AGATHA text chooser; bank 30:6700 texts, 6E00 hof58; bank 2F:6100 e4chk58/tline58.
Tests: t66_v58.py black, normal. run_v58.sh = run_v57.sh + t66.
