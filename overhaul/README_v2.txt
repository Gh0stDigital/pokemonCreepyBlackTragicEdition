Creepy Black — Mu Overhaul v2
=============================

ROM:    Creepy_Black_Mu_v2.gb
SHA-256: e7855fae19f3c8c3ee1c9a3791a13e6804836b0a0f25bc67893f8e3bfd4d280d
Size:   1,048,576 bytes; header and global checksums recomputed and checked.
Input:  Creepy_Black_Mu_v1.gb (SHA-256 1bb97ea3...3df5). The clean base ROM was not
        available, so build_v2.py applies logged patches on top of v1. Every patch
        asserts the exact v1 bytes it replaces. See manifest_v2.json for before/after bytes.
Charmap: pokeblack/charmap.asm is pret/pokered's constants/charmap.asm. The build re-encodes
        every v1 dialogue block and asserts it matches the v1 ROM byte for byte.

CHANGES IN V2
-------------
1. Pallet NPC sprites
   - Pallet's outdoor sprite set (set 1, shared with Viridian, Cinnabar, Route 1/2/22) did not
     contain the v1 NPC sprites, so in v1 Mr. Mu was invisible and the shaman was a wrong graphic.
   - Set 1 slots that none of those maps use were replaced: COOLTRAINER_M -> GENTLEMAN (0x10),
     SEEL -> CHANNELER (0x19).
   - Mr. Mu uses the Gentleman sprite. The shamaness uses the Channeler sprite and now stands
     at x8,y15 on the land tile directly beside the Pallet pond, facing the water.

2. Ghost hunger (saved RAM D455 = hunger 0-255, D456 = step counter; D457-D45A temp, D45B police flag)
   - Starts at 160 when Ghost is awarded. Drops by 1 every 6 overworld steps (not during
     scripted movement, only after Ghost is acquired).
   - Feeding (only when Ghost is the active battler when the enemy faints):
       wild Pokémon +16, trainer Pokémon +48, human (trainer killed by Curse) +160, cap 255.
   - At 0 hunger Ghost eats the last non-Ghost party member: screen goes black, the victim's
     cry plays, the Pokémon is removed, and hunger is set to only 12.
   - With no other party members it eats the player: black screen, Ghost's cry, all 4 SRAM
     banks are zeroed (save erased), and the game cold-restarts.
   - Tuning values are in TUNING at the top of build_v2.py.

3. Curse frightened text: now starts on line 2, so it no longer runs past "CLASS NAME:".
   Moved to bank 6 free space (0x1AE40) and the fear table was repointed.

4. Police bulletin rewritten: after a Curse murder (D453) it shows once per map visit when a
   GUARD sprite speaks, or when script text plays on a map with a guard (gate guards talk
   through map scripts, which v1 never caught). The flag is cleared on every map load.

5. Text width: the ▼ prompt arrow overwrites column 18 of the bottom text row, so all lines are
   now at most 17 characters as displayed (# counts as "POKé"). Briefing, Mr. Mu's question,
   shaman and police text were re-wrapped at the same byte length.

VERIFIED IN PYBOY (run_all.sh + t10_wild.py, starting from a new game on v2)
-----------------------------------------------------------------------------
- Opening, Mr. Mu walk-up and choice menu, both answers saved, Mu dismissed after a building.
- Mr. Mu visible as the Gentleman; shamaness visible as the Channeler beside the water; her full
  lore displays with no clipped letters.
- Trainer answer: rival battle, Ghost awarded, hunger initialised to 160.
- Drain: 14 steps = 1 hunger per 6 steps.
- Eating: starter removed, ~95 black frames, cry sound played, screen restored, hunger 12.
- Permadeath: after an in-game save, starving with only Ghost wiped all SRAM (0 non-zero bytes);
  the game restarted with no CONTINUE.
- Trainer Curse (Viridian Forest Bug Catcher, test harness moves him next to the player):
  Curse blackout, both Pokémon killed, frightened text shown correctly, D453 set, gravestone
  table entry written, gravestone sprite shown after leaving and re-entering the forest,
  hunger fed to the 255 cap.
- Wild Curse (Route 1 Pidgey): hunger +16, murder flag stays 0, no frightened text.
- Route 5 gate guard: bulletin shown after the murder; not shown with no murder.

NOT VERIFIED / NOTES
--------------------
- Ordinary trainer battles without Curse were not re-run for v2 (the frightened-text gate
  is D452, which is reset on every battle start).
- Changing sprite set 1 also affects Viridian, Cinnabar and Routes 1, 2 and 22. Their object
  lists don't use the replaced sprites, but any script that changes a sprite to
  COOLTRAINER_M or SEEL on those maps would now show the Gentleman or Channeler instead.
- The player gets no on-screen hunger warning yet.
