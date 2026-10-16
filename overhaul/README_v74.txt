Creepy Black — Mu Overhaul v74: four fixes
===========================================

ROM:     Creepy_Black_Mu_v74.gb
SHA-256: a241a52fd2ea515cf4b1966440df6df0bdf7c4cfff270d29d2bfc2f189ee3d2b
Input:   Creepy_Black_Mu_v73.gb. build_v74.py asserts every byte it replaces; manifest_v74.json logs them.

1. CINNABAR's town sign printed "C3 ERROR." - and since v63 so did the first sign of VIRIDIAN, VERMILION, CELADON, LAVENDER (and PEWTER's/CERULEAN's read
   something else).  Cause: DisplayTextID takes a text id <= the number of sprites for a SPRITE and looks its text up in that sprite's text byte.
   v63 appended the town's shamaness as the LAST sprite, so her slot number equalled the first sign's text id, and her marker (text byte 3F = "no such text") was
   read instead of the sign's.  Now the marker is: picture 19 + byte 0 = D0 + text byte = her own slot number; the lookup gives the sign's own id back, and
   she is told from the sign by standing next to her (as before).  Only a CHANNELER picture in a town of her table counts (MR. MU in the MANSION is sprite 4 of 4 too).
   Code: bank 31:4900 app74 / wrap74 (the old v66 code is removed); v67's im67 calls app74, the DisplayTextID chain (2F:502E) calls wrap74.
2. CELADON GAME CORNER Rocket killed with CURSE: no after-battle speech.  His walk away is skipped too (a hidden sprite never finishes walking: the script waited
   for ever with the joypad ignored); the event still ends the usual way.  (12:4C26 -> gc74 at 12:7140; kill bit $1FF = D44F bit 7.)  MT. MOON's Super Nerd is
   still untouched.
3. Gravestones never walk: a killed trainer/NPC on a WALK object (POKeMON MANSION 2F/3F, any town NPC killed on the map) kept wandering as a gravestone.  Predef 0x13
   (v35 killed13) is now killed74 (2D:6220): a sprite with the gravestone picture gets movement byte 1 (C2x6) = STAY every frame.
4. POKeMON MANSION 1F statue switch: v8's MR. MU is object 4 = text id 4 = the id of the statue's hidden event, so the switch always showed MR. MU's talk (also with
   him gone), and the switch could not be pressed.  Text entry 4 (11:7519) now looks at where the player stands: facing the statue (y6,x2) -> the original switch text
   ("A secret switch! Press it?"), else MR. MU's talk (v52).

Tests (t82_v74.py): signs (all five CINNABAR signs), towns (every town's first sign: v73 fails VIRIDIAN/VERMILION/CELADON/LAVENDER/CINNABAR), gamecorner (alive: the speech;
dead: none, script finished), graves (MANSION 2F + PALLET: a gravestone stands, a living walker walks; v73 fails), statue (D460 3 and 4: the switch; MR. MU still talks).
Not tested: a full fight to the kill at the GAME CORNER (the script is started with the kill bit set, as t78 does for v70).
