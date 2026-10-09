Creepy Black — Mu Overhaul v22: fossils on the chamber's stands
===============================================================

ROM:      Creepy_Black_Mu_v22.gb
SHA-256:  d51b965e4587a9dd8799ed227b795466abcef944a8f835023fd84aedfeb67f61
Input:    Creepy_Black_Mu_v21.gb. build_v22.py (patchlib) asserts every byte it replaces; manifest_v22.json logs them.
Test ROMs: Creepy_Black_Mu_v22_test.gb (built-in "just got the POKeDEX" save) and Creepy_Black_Mu_v22_chamber_test.gb
           (test-only save on Tower 7F at AGATHA stage 5, door open).

TOWER CHAMBER: a fossil (the Mt. Moon fossil sprite 3E, standing still) sits on each stand in front of the three
statues (picture qa_ref/v22_chamber_ingame.png). Talking to them:
  top (7,11)          "The OLD AMBER rests on the stand."
  bottom-left (15,6)  "The DOME FOSSIL rests on the stand."
  bottom-right (15,16) "The HELIX FOSSIL rests on the stand."
Gen 1 has only one fossil sprite, so the three look alike; the text tells them apart.
Map 0x69 got a new header/object list/text table at bank 18:7D40 (blocks, warp, script and MR. MU as in v21).

VERIFIED IN PYBOY (t33_v19.py fossils + the other chamber modes, run_v22.sh).
