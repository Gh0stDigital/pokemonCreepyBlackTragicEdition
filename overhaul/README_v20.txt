Creepy Black — Mu Overhaul v20: the chamber has one centre tile
==============================================================

ROM:      Creepy_Black_Mu_v20.gb
SHA-256:  9203c4809f4f90014020dc59f95afda5b9d337ca3079a78461456be60b71113c
Input:    Creepy_Black_Mu_v19.gb. build_v20.py (patchlib) asserts every byte it replaces; manifest_v20.json logs them.
Test ROMs: Creepy_Black_Mu_v20_test.gb (built-in "just got the POKeDEX" save) and Creepy_Black_Mu_v20_chamber_test.gb
           (test-only save on Tower 7F at AGATHA stage 5, door open; same save as v19's chamber test ROM).

The TOWER CHAMBER (map 0x69) is redrawn per walking tile instead of per 2x2 block (altar_layout_v20.py, picture
qa_ref/v20_chamber_layout.png): 12x12 blocks (24x24 walking tiles), a round floor centred on ONE tile (11,11) that
carries the purification-circle pattern, MR. MU standing on it; ring of graves, four shrines on the diagonals,
two statues by the stairs, stairs at (19,11).
The combinations the Tower blockset lacked are 7 new blocks in its unused slots 6E-74 (no map with the Tower tileset
uses 6E-AF; the build checks that). Every other Tower floor and AGATHA's League room are unchanged. The new map data
is at bank 18:7C00; the v19 chamber data at 18:7500 is no longer referenced.

VERIFIED IN PYBOY (t33_v19.py on v20, run_v20.sh): stairs open at stage 5; up the stairs -> chamber at (19,11);
MR. MU at (11,11) talks; walked to the four edges of the circle; back down -> 7F; save in the chamber -> power
cycle -> CONTINUE in the chamber.
