Creepy Black — Mu Overhaul v19: the secret chamber behind AGATHA (prototype for the climax)
========================================================================================

ROM:      Creepy_Black_Mu_v19.gb
SHA-256:  d072bc51443a85ebf0868a560157a99c34d923f6055c4943a6bc45eda354d990
Input:    Creepy_Black_Mu_v18.gb. build_v19.py (patchlib) asserts every byte it replaces; manifest_v19.json logs them.
Test ROMs:
  Creepy_Black_Mu_v19_test.gb          v19 + the usual built-in "just got the POKeDEX" save.
  Creepy_Black_Mu_v19_chamber_test.gb  v19 + a TEST-ONLY built-in save (make_save_v19_chamber.py): GHOST route, FUJI
                                       rescued, AGATHA's quest at stage 5 with MISTY, standing on Tower 7F below the
                                       open stairs. Its quest flags were set directly, not played through.

THE NEW MAP (id 0x69, one of the base game's unused map ids)
  TOWER CHAMBER, Pokemon Tower tileset (0F), 11x11 blocks, Pokemon Tower music, no wild POKeMON.
  Round room (altar_layout.py; picture: qa_ref/v19_chamber_layout.png):
    - a ring of graves around a round stone floor,
    - the purification-circle pattern in the centre; MR. MU stands on it (placeholder line:
      "So, you found this place. Come closer, child of the GHOST..."),
    - four small shrines on the diagonals, two statues on either side of the stairs,
    - stairs at the bottom lead back to Tower 7F.
  All map data (header, blocks, objects, warps, text, script) is in bank 18 at 7500; the map header pointer, bank and
  music for 0x69 are set; its wild data, hidden objects, toggles and gravestone list were already empty.

THE SECRET DOOR (Tower 7F)
  From AGATHA's quest stage 5 (the girl has come): when 7F loads, the graves behind AGATHA's spot are swapped for a
  stairway (block 11 at block 0,5 via ReplaceTileBlock), the stairs step (1,11) is a second 7F warp into the chamber,
  and AGATHA stands beside the opening at (2,10) instead of in front of it (a second AGATHA object, same text).
  Before stage 5, 7F is exactly as in v18.

VERIFIED IN PYBOY (t33_v19.py, run_v19.sh)
  closed: before stage 5 no stairs, AGATHA in front, second AGATHA hidden.
  chamber: stairs open, AGATHA beside them; up the stairs -> map 0x69 at the stairs step; MR. MU at the centre
  talks; no wild POKeMON; walked to the four edges of the circle; down the stairs -> 7F (1,11) -> (2,11).
  saveload: SAVE inside the chamber -> power cycle -> CONTINUE in the chamber at the same spot, stairs still work.
  Test ROMs: t29 on v19_test; the chamber test ROM CONTINUEs on 7F and the stairs lead into the chamber.

NOTES
  - The centre block is 2x2 steps; MR. MU stands on its top-left step (a block has no single middle step).
  - Nothing else uses map 0x69; the full v18 regression still passes on v19.
