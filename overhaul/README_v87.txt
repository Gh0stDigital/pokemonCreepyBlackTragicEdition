Creepy Black Mu v87 (on v86): BILL's cottage, the consort at home, LAVENDER in the house, the CERULEAN cave guard
SHA-256 fc50d2c444ba818dc12e6aba491a0097ae0c98fe24c0241fb9326e5ab2faa701

1. BILL (scene before the fight): he steps out of the machine, walks 2 down and 2 left and stands directly in front of the player (6,2), facing down (was beside him, facing left).
   His sprite glitched before the battle: a redraw (the text box) handed his VRAM slot to another picture. app87 (bank 31:5B00, before app86 in the InitMapSprites chain) gives the
   object list's pictures back before the sprite loader runs (cottage as BLACK at D876 = 5, and the player's house as BLACK after the ritual).
2. BILL is gone before he can be seen after the battle: the engine's HideObject (predef 11 in this ROM, toggle 62) runs when the battle starts (bill87, bank 30:4540), so the map comes
   back without him. A lost battle restarts the scene (ShowObject as before).
3. The consort in the player's house: same cause as 1 (MOM's hidden picture shifted her slot after the heal text) - fixed by app87.
4. As BLACK the player's house plays the LAVENDER theme like the rest of the world (music51: maps < $26); after the heal jingle the map music (LAVENDER) comes back.
5. CERULEAN CAVE guard (CERULEAN CITY object 10 at (12,4), toggle 8 = D5A7 bit 0): hidden when BLUE is beaten as BLACK (1D s3_87) and, for older saves, by the CERULEAN CITY script
   (06:7100 cer87) whenever D46C and D876 >= 1.
Tests: t95_v87.py bill house cer normal blue. run_v87.sh = run_v86.sh + t95.
