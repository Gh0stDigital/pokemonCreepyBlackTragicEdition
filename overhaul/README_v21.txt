Creepy Black — Mu Overhaul v21: centre ring and statue triangle in the chamber
==============================================================================

ROM:      Creepy_Black_Mu_v21.gb
SHA-256:  63b8b00c4aba9782a37626819104247b85276ec36fce671a970c55fbcb37b93b
Input:    Creepy_Black_Mu_v20.gb. build_v21.py (patchlib) asserts every byte it replaces; manifest_v21.json logs them.
Test ROMs: Creepy_Black_Mu_v21_test.gb (built-in "just got the POKeDEX" save) and Creepy_Black_Mu_v21_chamber_test.gb
           (test-only save on Tower 7F at AGATHA stage 5, door open).

TOWER CHAMBER (altar_layout_v21.py; pictures qa_ref/v21_chamber_layout.png, qa_ref/v21_chamber_ingame.png):
  - a thin ring of the purification pattern around the single centre tile (11,11), where MR. MU stands; the ring
    tiles are walkable;
  - a triangle (point up) of three POKeMON statues around the centre, each with a gravestone in front of it (the
    tile below): at (5-7,11), (13-15,6) and (13-15,16);
  - the four diagonal shrines of v19/v20 are gone (the triangle replaces them); the ring of graves, the two statues
    by the stairs and the stairs are unchanged.
  8 more new blocks in the Tower blockset's unused slots 75-7C (v20's 6E-74 stay; 7D-AF still free). Map data at
  bank 18:7600; the v20 data at 18:7C00 and v19's at 18:7500 are no longer referenced.

VERIFIED IN PYBOY (t33_v19.py on v21, run_v21.sh): door at stage 5, into the chamber, MR. MU at the centre talks, walked
around the circle, back to 7F, save + power cycle + CONTINUE inside.
