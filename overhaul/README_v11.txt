Creepy Black — Mu Overhaul v11: blacked-out Gentleman, DRAGON RAGE, BLACK FLAME spares people
================================================================================================

ROM:     Creepy_Black_Mu_v11.gb
SHA-256: 7fa2b19d9a7584dad94263fba733d5b2a64b4302e71f2c984b36ec2b76271b9f
Input:   Creepy_Black_Mu_v10.gb. build_v11.py asserts every byte it replaces; manifest_v11.json logs them.

WHAT'S NEW
----------
1. The Mirage trainer (?????) is drawn as the GENTLEMAN trainer pic blacked out: the background outside
   the figure stays white and everything inside the outline is solid black (mirage_gentleman_pic.bin,
   91 bytes, in the same bank-13 slot as the old silhouette; preview in ref/gentleman_sil.png).
2. AZHI knows BLACK FLAME, FLY, DRAGON RAGE, FIRE BLAST. DRAGONBREATH (move AA) is removed again
   (its data and name bytes are cleared).
3. BLACK FLAME now only faints Pokémon: every Pokémon on the target's side faints except GHOST,
   PRETA and AZHI. People are never harmed: hitting the player's stand-in "YOU" just says
   "It doesn't affect RED!" (no save wipe), and BLACK FLAME never touches the trainer-death flag.
   If the target itself is GHOST/PRETA/AZHI it says "It doesn't affect ..." but the rest of that
   side still faints.

VERIFIED IN PYBOY (run_v11.sh)
------------------------------
- Mirage intro shows the black Gentleman silhouette ("????? wants to fight!").
- Mirage AZHI's BLACK FLAME with PRETA out: CHARMANDER fainted, "It doesn't affect PRETA!", stand-in
  untouched. With the stand-in out: "It doesn't affect RED!", battle continues, no reset.
- Wild AZHI's BLACK FLAME (party CHARMANDER/GHOST/PRETA): CHARMANDER fainted, GHOST and PRETA kept HP.
- AZHI's moves in battle: A8 / FLY / DRAGON RAGE / FIRE BLAST; DRAGON RAGE did 40 to PRETA.
- All earlier checks pass on v11 (run_v11.sh + the v1-v5 chain). t13 'fight' now forces AZHI's
  DRAGON RAGE when the saved Mirage is AZHI, since BLACK FLAME no longer kills the stand-in.
