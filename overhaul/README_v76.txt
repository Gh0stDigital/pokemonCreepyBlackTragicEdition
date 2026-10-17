Creepy Black — Mu Overhaul v76: no encounters on TOWER 7F, the ritual room's stands
====================================================================================

ROM:     Creepy_Black_Mu_v76.gb
SHA-256: 6a369425166c88f932aac998f751053fee06f8a160e7869492e2b757b2cd3a2f
Input:   Creepy_Black_Mu_v75.gb. build_v76.py asserts every byte it replaces; manifest_v76.json logs them.

1. POKeMON TOWER 7F (map 94): no wild encounters for anybody (v49 removed them only for BLACK). TryDoWildEncounter's hook (4:78BC) now calls tow76 (bank 4:7BC0):
   7F -> "can't encounter", every other map -> v49's tow49 as before (BLACK: none in the Tower 1F-7F; 1F-6F as before otherwise).
2. TOWER CHAMBER (the ritual room, map 69): the HELIX FOSSIL stands on the top (middle) stand, the DOME FOSSIL / PRETA on the left one, the OLD AMBER / AZHI on the right one
   (before: AMBER top, HELIX right). Only the two stand objects' positions changed (object 2 OLD AMBER -> y15 x16, object 4 HELIX -> y7 x11); their texts, the awakened cries,
   the fossil hiding after the ritual and the altar stash follow the objects (text ids 2 AMBER / 3 DOME / 4 HELIX).

Tests: t84_v76.py tower7f (400 steps with the wild rate forced to 255: v75 meets a POKeMON, v76 none; the check ran on every step), t61_v53.py altar (stands by their new places: AMBER right,
HELIX top, DOME left, cries / texts as before), t34 ritual + t35 climax pass. t33 fossils (old test, its walker is blocked by the v53 channelers since v53) was updated for the new places but cannot reach the room.
