Creepy Black Mu v63 (from v62): the ten SHAMANESSES in the ten towns
SHA-256 0015301cb0e5c92d91631d9f24b2328e7af329d8ed3edb84aee8def5eeabd5f0

- One shamaness (the CHANNELER picture, 19) stands in each town once GHOST has been acquired (D451 <> 0): PALLET 1 (The Ancient Clan), VIRIDIAN 2 (The God
  of the Abyss), PEWTER 3 (The Division), CERULEAN 4 (The Four Warriors), VERMILION 5 (The Eight Dragons), CELADON 6 (The Forbidden Art), FUCHSIA 7 (The
  Sacred Grounds), SAFFRON 8 (The Forgotten Ritual), LAVENDER 9 (The Lavender Cult), CINNABAR 10 (The Forgotten God). The texts are the user's (8 = the
  revised one; "that cult's descendants" fixed). The assignment of texts to towns is my choice (LAVENDER gets the cult).
- Talk to her (A, next to her): she turns to you and tells her part (same layout as the Tower 7F channelers: "SHAMANESS n:" + title, then the story).
  The talked flag (D840 bit n for 1-8, D841 for 9-10; unused saved event bytes) is set; she stays until the map is loaded again, then she is gone for good.
- Mechanics (bank 31, 5000): app63 runs at every InitMapSprites (5:785B stub at 5:7FD0): it appends her as the next sprite (D4E1 + 1, picture 19, STAY,
  facing down, text byte 3F in the new slot's D4E4 entry as a marker so a redraw doesn't add her twice). SAFFRON has all 15 slots used: she replaces the
  last guard (slot 15, the second guard in front of the SILPH door, same tile). wrap63 (the DisplayTextID chain, 2F:502E) recognises her by slot,
  marker and being next to the player (the first sign's text id equals her slot number), then does the talk itself (the v28 NPC takeover is not reached;
  BLACK can talk to her too; v28's exempt picture list got 19 so the sign that shares her number is not treated as a panicking NPC).
- Spots (step y,x): PALLET 7,14; VIRIDIAN 12,28; PEWTER 10,12; CERULEAN 20,18; VERMILION 14,12; CELADON 11,24; FUCHSIA 9,10; SAFFRON 22,19; LAVENDER 6,12; CINNABAR 4,14.
- Sprite sets (5:7AB9, 11 pictures each): picture 19 replaces an unused entry in the sets of LAVENDER (0E), VERMILION (0C), CELADON (35), SAFFRON (07), FUCHSIA (09);
  PALLET / VIRIDIAN / CINNABAR already have it. PEWTER and CERULEAN share set 2 with routes that use every entry, so they get their own set 13 (set 2 with
  19 for the HIKER) at 5:7F79; the set lookup (5:79AC) is a stub that points at it for maps 2 and 3 (the map table now says 13 for them).
- Tests: t71_v63.py town <map> for every town (a shamaness stands there, walk next to her, A: her speech, talked flag, gone after the map is loaded
  again); town 1 black (BLACK talks to her, no panic); nogh 1 (no GHOST -> none). SAFFRON: the guards close the way to her in the harness, so only the sprite
  and the flag (gone) are tested there; the talk is the same code as everywhere else. run_v63.sh = run_v62.sh + t71. Full v54-v62 regressions never completed
  (only targeted tests), t36 panic/exempt rerun on v63.
- Not changed: the Tower 7F lore texts 8-10 (v53) still have their old wording.
