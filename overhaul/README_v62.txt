Creepy Black Mu v62 (from v61): CERULEAN CAVE - the final confrontation with PROF. OAK
SHA-256 4a541de8de294626f6fb6605286fb99e9f5d9da38a054407ea612c8f98698128

- As BLACK (D46C) with D876 = 6 (BILL is dead), CERULEAN CAVE B1F (map E3, bank 11) runs bank 31 cave62 every frame (wrapper at 11:7600 on the
  header script): object 1 (the MEWTWO spot, 27/13, across the water: SURF) becomes PROF. OAK (picture 3, ShowObject toggle D1, InitMapSprites for
  his tiles). His text (id 1) is a chooser: at D876 = 6 it only sets D877 = 10 (the scene is requested); the map script then plays it.
- The scene (31 scene62): music stops, fade to white, the screen is cleared, sprites cleared, BG transfer to 9800, OAK's picture (13:615F) is drawn
  centred like the first scene of the game, font / text box tiles reloaded, his speech (the user's text), fade, the map is reloaded; then the battle
  starts (class 26, trainer no. 2; D877 = 11).
- Trainer class 26 now has two parties: no. 1 BILL, no. 2 PROF.OAK (MR. MIME 60, VENUSAUR 62, ARTICUNO 64, ZAPDOS 64, MOLTRES 64, MEW 70 last; E:7EFE).
  GetTrainerInformation (0:35B6-35D5) is a far call to 31 gti62: the class picture table (copied to bank 31) and the name; at D876 >= 6 class 26 = the OAK
  picture (13:615F) and the name PROF.OAK (BILL: the PSYCHIC picture).
- OAK is an Elite-Four-style battle (e4chk60): forbidden moves are refused with HIS line ("So... I was right! The MOON STONES aren't the only things...",
  tline62 in 2F:6300), no MOON STONE flash / "shatters" text for him (ph62 skips to the BLACK switch), BANE is mandatory. His defeat speech is the user's.
  No trainer header: his kill index = LANCE's (v34 table, map E3 / class 26 set 2).
- After the win (back on the cave map with D877 = 11): D876 = 7, the LAVENDER TOWN theme (the table entry the v51 music code uses), a clean credits screen
  (clear, font, BG 9800), the game's own CREDITS (1D:418E), SaveGameData (1C:7847), then a restart (jp 1F81): the title screen; CONTINUE resumes in the cave.
- Test notes: his spot is across the water, so t70 requests the scene by writing D877 = 10 (what his text does). A bug found on the way: OAK's party must start
  at E:7EFE (7EFD is BILL's party terminator). Texts printed by PrintText from a map script need wJoyIgnore = 0.
- Tests: t70_v62.py scene / block / normal (+ t68, t69 still pass). run_v62.sh = run_v61.sh + t70.
