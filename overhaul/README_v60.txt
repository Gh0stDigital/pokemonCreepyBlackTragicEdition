Creepy Black Mu v60 (from v59): BILL's cottage
SHA-256 e1452074130a55008cbab105c3ef5297d07a4453260fef05694cd08713ac756c

- As BLACK (D46C) with D876 >= 5 (the lab aide told where OAK went), BILL'S HOUSE (map 58, bank 7) runs bank 30 bill60 instead of the old script
  (D877 = scene sub-stage 0 hide everything / 1 BILL steps out (ShowObject toggle 62) / 2 walks down, long speech (text 2 -> chooser) and the battle /
  3 after the battle). The speech and the battle defeat speech are the user's texts; nothing is said after the win: D876 = 6 (OAK went to
  CERULEAN CAVE; the next chapter), the cottage is empty. A lost battle restarts the scene.
- BILL = trainer class 26 (the PROF.OAK slot: renamed BILL, SCIENTIST picture, party ALAKAZAM 58 / MAGNETON 56 / ELECTRODE 56 / JOLTEON 58 at E:7EF0).
  He counts as an Elite-Four-style battle (e4chk60 / tline60 in 2F:6200: MOON STONE rules + shatter + BANE; his line "OAK's MOON STONE keeps me safe!" is mine).
  No trainer header: his kill index = LANCE's via v34's scripted-trainer table (BILL'S HOUSE / class 26 set 1).
- BILL'S HOUSE is exempt from v28's NPC takeover (new exempt-map list at 2D:7E20).
- Lessons: hidden missable objects keep image index FF each frame: use the engine's ShowObject (wToggleableObjectIndex CC4D = toggle, predef 16 via 3EC1)
  instead of writing the picture; battle text pointers set from a far-called script live in that script's bank.
- Tests: t68_v60.py black, normal. run_v60.sh = run_v59.sh + t68.
