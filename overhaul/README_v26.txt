Creepy Black — Mu Overhaul v26: BLACK's back picture without the "square"
========================================================================

ROM:      Creepy_Black_Mu_v26.gb
SHA-256:  28580d1b047e392589b94a79f80a121da23b4579ee20ef874c5916ba2f11ca00
Input:    Creepy_Black_Mu_v25.gb. build_v26.py (patchlib) asserts every byte it replaces; manifest_v26.json logs them.
Test ROMs: Creepy_Black_Mu_v26_ritual_test.gb (save in the chamber right after MR. MU's ritual: walk out of the circle),
           Creepy_Black_Mu_v26_chamber_test.gb (Tower 7F, AGATHA stage 5), Creepy_Black_Mu_v26_test.gb (POKeDEX save).

The v25 back picture (battle intro and the stand-in YOU) used the whole 32x32 area: RED's back view is cropped flat at the
edges and the GHOST halo filled the rest, so it read as a dithered square. Now the silhouette is scaled to 80%, centred
with a margin (2 px bottom margin raised to 4) and has a smaller halo (red_ghost_fusion.fuse_back_soft(r, 0.8, 2, 4)), so
the outer 2 px of the picture are empty. Picture: qa_ref/v26_back_compare.png (RED left, BLACK right), variants tried:
qa_ref/v26_back_variants.png. Only the picture and its three pointers changed (BLACK header, YOU-as-BLACK header, the
LoadPlayerBackPic stub); the new 143-byte-class picture is at 2D:6E00.

VERIFIED IN PYBOY (t35_v25.py on v26)
- backpic (new): the picture's outer 2 px are empty and the silhouette is solid (321 dark pixels).
- sprites, you: the BLACK back picture still shows in the battle intro and for YOU-as-BLACK (RED's otherwise);
  the map sprite sheet is unchanged. climax: the whole climax still passes (consume, battle, CURSE, 5.4 s black, evolution).
- run_checks.sh: 85 hooks, 0 problems. (Not the whole v3-v25 chain: v26 changes picture data and three pointers only.)
