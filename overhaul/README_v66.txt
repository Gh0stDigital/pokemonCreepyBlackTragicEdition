Creepy Black Mu v66 (from v65): town shamaness fixes
SHA-256 953bb05ccf54e374bdc5fa71837849058e20e12e73b4ef99ab0af6d4fc770d2c

1. SPRITE GLITCH (found and fixed). v63 added the CHANNELER picture (19) to the town sprite sets by overwriting one entry of sets 3, 4, 5, 7 and 10 in place.
   I had only checked the maps that use a fixed set. ROUTES choose their set by position (5:7A89 table: axis, threshold, set A, set B) and share these sets, so
   three routes lost a picture they use in the part of the route that picks that set: Route (map 15)'s HIKER (0E, set 3), map 16's boy (0C, set 4) and map 11's
   boy (07, set 7). Their NPCs were drawn with garbage tiles (often channeler faces) - "sometimes", depending on where on the route you were.
   Now: v63's edits of sets 3, 4, 7 are undone and 19 goes into an entry no map using the set needs (set 3: 31, set 4: 31, set 7: 05; sets 5 (35) and 10 (09) were
   already free; PEWTER / CERULEAN keep their own set 13; PALLET / VIRIDIAN / CINNABAR's set 1 had 19 already).
   New static check overhaul/check_sets.py (t74_v66.py sets): every object picture of every outdoor map (position-dependent routes too) must be in its set(s),
   compared with v62's existing violations: v63-v65 had 3 new ones, v66 has none; every shamaness town must have 19 in its set. Her tile data in VRAM was
   verified identical in all ten towns (menus, battles on the way, re-entry).
2. The shamanesses' speeches have no "SHAMANESS n:" and no title any more, only the story.
3. After you talked to her she is gone the next time the map loads (flag D840/D841, as before). When she is not added, the slot after the last real sprite is
   wiped (picture 0, position FF, no marker in the text table), so nothing of her can survive in the sprite table.
4. PALLET: the old placeholder shamaness (object 5 by the water, v1 text) is removed: its position in the object data is FF,FF and the Pallet script hides it every
   frame. SHAMANESS 1 (official text) stands on its old tile (y15 x8). She is there from the start of the game (the other nine towns need GHOST; the table has a
   "needs GHOST" byte per town). Code: bank 31 6600 app66/wrap66, 6400 pal66 (the v65 Pallet script), texts 6A00; the v63 code/texts and v65 pal65 are zeroed.
- Tests: t74_v66.py sets / pallet; t71_v63.py (all ten towns, BLACK, no GHOST) now checks for the story without name/title. run_v66.sh = run_v65.sh + t74.
