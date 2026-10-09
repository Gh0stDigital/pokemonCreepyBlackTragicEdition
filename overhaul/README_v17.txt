Creepy Black — Mu Overhaul v17: AGATHA / consort placement, no Mr. Mu hint
=========================================================================

ROM:      Creepy_Black_Mu_v17.gb
SHA-256:  eb1805db25d8291f93c64947eda0868a76ecffaf7e235efb616335a164a3152b
Input:    Creepy_Black_Mu_v16.gb. build_v17.py (patchlib) asserts every byte it replaces; manifest_v17.json logs them.
Test ROM: Creepy_Black_Mu_v17_test.gb (build_v17_test.py) = v17 + the built-in "just got the POKeDEX" save.

1. Pokemon Tower 7F: AGATHA stands on MR. FUJI's right (x11, was x9 on his left).
2. The chosen girl (MISTY/ERIKA/SABRINA) stands on AGATHA's left (x10). That is FUJI's spot: she only appears
   once FUJI has been rescued and has gone home (his 7F object is hidden then, toggle 43), so they never overlap.
3. AGATHA's "you already woke some of them" note no longer has "That one's work, I suppose." (it hinted at Mr. Mu).

Note: v16's 7F screenshot showing AGATHA, FUJI and a girl together came from a test that forced the girl flag
with FUJI still there; in the game the girl can only be there after the rescue. The v17 tests hide FUJI and the
ROCKETs the way the real rescue does (toggles 40-43 = D5AE bits 0-3).

VERIFIED IN PYBOY: t31_v16.py (all modes, now position-aware: AGATHA x11, girl x10; Mu note without the hint),
run_v17.sh full regression, t29 on the test ROM.
