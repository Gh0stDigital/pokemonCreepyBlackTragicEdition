Creepy Black — Mu Overhaul v25: the climax (GHOST consumes the MIRAGE, BLACK is born)
====================================================================================

ROM:      Creepy_Black_Mu_v25.gb
SHA-256:  8e06876abf0db4af57388b0319d0f169076470037bd6d305c96b0a5baa26c8e9
Input:    Creepy_Black_Mu_v24.gb. build_v25.py (patchlib + sm83asm.py, a small assembler built from ref/instruction_set.py)
          asserts every byte it replaces; manifest_v25.json logs them.
Test ROMs: Creepy_Black_Mu_v25_ritual_test.gb  = built-in save in the TOWER CHAMBER right after MR. MU's ritual (????? in
                                                 the party): walk out of the circle to start the climax
           Creepy_Black_Mu_v25_chamber_test.gb = Tower 7F at AGATHA stage 5 (door open)
           Creepy_Black_Mu_v25_test.gb         = "just got the POKeDEX" save

THE CLIMAX (after MR. MU's battle, GHOST route)
1. ????? is in the party with a hollowed-out GENTLEMAN party-menu icon (outline of the GENTLEMAN map sprite, 2 frames).
2. TOWER CHAMBER: every item is disabled outside battles (POTION, ESCAPE ROPE, TMs, ...) and so are DIG / TELEPORT / FLY:
   "Something prevents you from using that here." (In battle everything works as before: the MASTER BALL.)
3. First step out of the inner circle (any tile more than 2.4 tiles from MR. MU's grave): GENGAR's cry (placeholder for an
   unused sound), a flash, "GHOST consumed the MIRAGE!" - ????? leaves the party. Two more steps: a battle starts.
4. The battle: the player alone (as YOU, Lv50) against a wild Lv100 GHOST. Before any command GHOST uses CURSE ("GHOST used
   CURSE!"), the screen goes black for about 5.4 s, then fades in to the evolution screen: GHOST turns into the RED+GHOST
   silhouette (the game's own evolution animation), "GHOST has transcended and become BLACK." / "You are now BLACK."
   Then the battle ends.
5. BLACK: the player is renamed BLACK; the battle back picture (also YOU's) and the walking map sprite are the blacked-out
   RED+GHOST fusion with the GHOST aura (flag D46C; bike/surf sprites are unchanged). GHOST leaves the party (it stays only if
   it was the last member, so the party is never empty). The hunger engine is switched off for BLACK (it would have eaten the
   party), the Mirage counter is reset.
6. Back on Tower 7F AGATHA walks up to the player (below the stairs), celebrates, says the consort waits at the player's home
   in PALLET TOWN, and sends BLACK to destroy the POKeMON LEAGUE and consume all of them; she steps back. Talk to her again:
   MR. MU's story (devoted to the clan, worked to perfect you, felt shame and guilt for failing the ceremony - "It was not
   even his fault..." - she stops: "No. The past does not matter now. Today we should celebrate!"). Third time (and ever
   after): "My ancestors are smiling today! ... They sing of the day KANTO is rid of its outsiders!"
7. The consort (MISTY / ERIKA / SABRINA, whoever joined AGATHA) stands in the player's house 1F (5,6); talking to her heals the
   party. Before the ritual is done nobody waits there, and she is gone from Tower 7F.

TECHNICAL
- New saved RAM: D467 ritual stage (v23: 0-3; v25: 4 = ????? consumed / counting steps, 5 = GHOST battle, 6 = BLACK done),
  D46A step counter, D46B AGATHA talk (0 intro, 1 lore next, 2 final), D46C BLACK, D46D/D46E last y/x, D46F Tower 7F scene
  (0 start, 1 AGATHA walking, 2 walking back, 3 done), D470 scratch (picture bank).
- All new code/data is in bank 2D (4400 code, 5800 texts, 7000 BLACK sprite sheet), bank 18 (chamber/7F scripts), bank 12
  (house objects). Species 7F = BLACK (name, dex slot 152, header, GENGAR cry); its front/back pictures are the fusion pictures
  v23 left in 2D:41C0 / 2D:42BD.
- UncompressMonSprite (0:1659): the pic bank now comes from a 2D routine (so YOU can switch to the BLACK back picture); the
  freed home-bank bytes hold the walking-sprite stub. LoadWalkingPlayerSpriteGraphics (0:1077), LoadPlayerBackPic (F:6D84),
  GetPartyMonSpriteID (1C:5927), GetMonHeader exit (E:7E41 extension) are hooked for BLACK / the icon.
- Party icons: the 30-entry table at 1C:57F2 moved to 1C:7B9C with 4 new entries (tiles 2C/2E frame 1, 6C/6E frame 2); the
  two loaders point to it (34 entries). ????? returns icon base tile 2C.
- Items: UseItem_ (3:58F8) 8-byte far stub; field moves: 4:71C4 stub (Fly 71DA, Dig 7279, Teleport 7291 handlers).
- The climax hooks DisplayBattleMenu (F:4EDE): at the first menu with RIT=5 the 2D routine does the whole scene and then
  redirects the return address to F:5155 (the "ran from battle" exit), so the battle ends cleanly.
- Hunger: the home stub at 0:00E0 calls hunger_wrap (2D), which returns when BLACK.
- Tests: t35_v25.py (items, icon, climax, sprites, you, agatha, house, normal; run_v25.sh).

VERIFIED IN PYBOY (t35_v25.py)
- items: POTION and ESCAPE ROPE refused with the text, bag unchanged; DIG / TELEPORT / FLY refused from the party menu.
- icon: ????? uses tiles 2C/2E (VRAM matches the generated hollow gentleman), GHOST keeps 28/2A.
- climax: inside the circle nothing happens; first step out -> ????? gone, text; two steps later the wild Lv100 GHOST battle
  with the player alone; CURSE text, black for 326 frames (5.4 s), the evolution frames and texts; afterwards BLACK=1, RIT=6,
  name BLACK, party = the original one without GHOST and ?????.
- sprites: BLACK walking sheet in VRAM (chamber and Pallet after a battle); the intro back picture is the BLACK silhouette
  (RED's normal otherwise).
- you: the stand-in YOU is drawn with the BLACK back picture when BLACK.
- agatha: arrives on 7F, walks up, the whole intro, steps back, joypad free; the girls are gone; lore; final line (repeats).
- house: the right consort (sprite 1D / 1B / 0D) at (5,6), the others hidden; nobody before the ritual; talk heals (3 -> 22 HP).
- normal: POTION works outside the chamber; hunger drains normally (BLACK=0) and not for BLACK.
- Static: run_checks.sh (85 hooks, 0 problems); test_sm83asm.py (assembler round-trips real ROM code byte for byte).
- The earlier suites (run_v24.sh and below) pass on v25 (see the end of this file for the run).

NOT DONE YET / NOTES
- Placeholder: the consume sound is GENGAR's cry. BLACK's own cry is the same.
- The trainer card and Oak's intro still show RED; surfing/biking sprites are RED's.
- After this: BLACK's journey (destroy the POKeMON LEAGUE) is for the next chapters.
