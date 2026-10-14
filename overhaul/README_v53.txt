Creepy Black Mu v53 (on v52): Tower 7F channelers, the secret door after AGATHA's talk, the altar stash.

SHA-256: 2d25a8c8df32c0bf7ae8b3f83ccda01daf747bdcb8644002e7d877ae9aa5f24a

Picture: qa_ref/v53_channelers.png (the hall with the channelers; near the top AGATHA, the girl and the graves).

1. Channelers (SHAMANESS 1-10). Once the consort has arrived (AGATHA quest stage 5) and until the ritual is over (D467 < 6) ten
   channelers stand in the Tower 7F hall, five on each side (x 9 and x 12, rows 12, 10, 8, 6, 4; pairs from the entrance up).
   Each tells one part of the lore: 1 The Ancient Clan, 2 The God of the Abyss, 3 The Division, 4 The Four Warriors, 5 The Eight
   Dragons, 6 The Forbidden Art, 7 The Sacred Grounds, 8 The Ancient Trials, 9 The Lavender Cult, 10 The Forgotten God (the
   user's texts, "SHAMANESS n:" + title, then the story).
   The Game Boy draws ten sprites at most (40 OAM entries, the player included), so only the channelers within two steps of
   the player are drawn - they appear as you walk up the hall (never more than six at once, plus AGATHA, the girl and the player).
2. The secret door. At stage 5 AGATHA stands in front of the graves. Her talk now: "AGATHA: You have brought her. Good. The way
   to the ritual room is open now. I will step aside..." - after it she walks up and left, and the graves turn into the stairway
   (D466 bit3 = talked, bit5 = walking, bit4 = door open). Later visits (and every visit once the ritual has begun): open, AGATHA
   beside it, "The ritual room is open. Go when you are ready." Before stage 5 nothing changed.
3. The altar. Entering the TOWER CHAMBER before the ritual is over (D467 < 3) takes PRETA and AZHI out of the party (SRAM 1:BA00,
   D466 bit6); they come back when you leave the chamber (party, else the box) and, if the ritual ends inside, before BLACK joins
   (so black_join gives no second PRETA/AZHI and v50's Lv50 boost applies). The three stands keep their fossil sprites until the
   ritual is over (RIT >= 3), awakened or not; if MR. MU awakened the POKeMON (D460 >= 2 for PRETA, 4 for AZHI) the DOME / AMBER stand
   plays its cry and says "<NAME> stands still on the stand."; otherwise (and for the HELIX stand) the usual "rests on the stand".

Technical:
- Code in bank 30:4C00 (ch53, ag53, stash53/restore53, the stands, objsel53 + texts) and bank 18:6EC0 (object list, text table,
  7F script, chamber script, stubs); 2D:7FD5 give_tmp (v38 add_mon on a struct at D8A4).
- Sprites: 15 is the limit (D4E4 / D504 tables). Slots used: six new objects 10-15, object 9 (AGATHA beside the door, free before the
  ritual), object 4 (FUJI, its hide toggle D5AE bit3 cleared while the channelers stand) and the two girl objects that are not the
  consort; AGATHA stays object 5 until the ritual is over. ch53 runs every frame after the old scripts (v16's tail jp 4D05 ->
  tail53) and writes picture, position, screen position (only when standing: sprites hidden before have none), facing, tile slot
  (object 10's), text id (10-19) and clears the trainer byte.
- The long object list (15 objects) slows the overworld (a step takes 34 instead of 25 frames), so LoadMapHeader (0:112E -> 30:objsel53)
  gives Tower 7F the long list only at stage 5 before the ritual ends; otherwise the old nine objects (as in v52). The text table has
  19 entries (the old 9, then the lore stubs).
- Door: 18:7A50 (v19 block) -> script53; it also restores the stash after leaving the chamber. AGATHA's talk: 2D agatha25 .old ->
  ag53 (stage 5: the new text, sets bit3). After MoveSprite wJoyIgnore (CD6B) is cleared by hand.
- Chamber: script (header +7) -> script_ch (stash53, fossil sprites hidden from RIT 3, then 2D chamber_tick); texts 2-4 -> TX_ASM stubs.
- Tests: t61_v53.py lore, door, altar, ritualstash. t33/t34's tower() set D466 |= 0x18 (door open) from v53 on and their BFS waits 40 frames per
  step. run_v53.sh = run_v52.sh + t61. The v53 chamber test ROM (stage 5, saved with the old open door) now starts with the
  door closed: talk to AGATHA to see the new scene.
Static: check_hooks.py 138 hooks, 0 problems.
Regression (run_v53.sh): 530 PASS, 1 FAIL: t53 tower (BLUE's Tower fight uses GHOST, which refuses in the Tower since v51: a test issue, fixed in the v54 test files by fighting with the map id set elsewhere). t61 modes (lore, door, altar, ritualstash) pass.
