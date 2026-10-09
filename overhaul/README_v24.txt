Creepy Black — Mu Overhaul v24: the MIRAGE keeps its silhouette
==============================================================

ROM:      Creepy_Black_Mu_v24.gb
SHA-256:  8526a20e7b70b3592f7ad324a0a1d763fbd774df2a4fa26278a7856b0d4e612e
Input:    Creepy_Black_Mu_v23.gb. build_v24.py (patchlib) asserts every byte it replaces; manifest_v24.json logs them.
Test ROMs: Creepy_Black_Mu_v24_test.gb (built-in "just got the POKeDEX" save) and Creepy_Black_Mu_v24_chamber_test.gb
           (Tower 7F at AGATHA stage 5: walk up the stairs and talk to MR. MU).

Correction to v23: the RED+GHOST fusion picture is for the BLACK TAMER (a separate thing, not built yet), not for
the MIRAGE. The MIRAGE ????? (species 7A) in MR. MU's ritual battle now looks like the random Mirage encounters:
  front: the blacked-out silhouette (the Mirage trainer pic, 13:7FA5), copied to 2D
  back:  the same silhouette mirrored (seen from behind) and scaled to the 32x32 back-pic size, pure black
Only ?????'s header pointers changed (bank E). The fusion pics stay unused in 2D:41C0 for the BLACK TAMER.
Pictures: qa_ref/v24_mirage_pics.png (both pics), qa_ref/v24_mirage_ingame.png (ritual battle, black ball, ????? sent out).

VERIFIED IN PYBOY
- t34_v23.py ritual on v24: the whole talk + ritual battle as in v23, ????? shown as the silhouette.
- t34_v23.py sendout (new): ????? from the ritual leads a wild battle on Route 1: "Go! ?????!", back pic shown.
- t34_v23.py wild: a normal wild catch still asks for a nickname, normal ball.
- run_checks.sh: 79 hooks, 0 problems. v24 changes only pic data in free space + two header pointers.
