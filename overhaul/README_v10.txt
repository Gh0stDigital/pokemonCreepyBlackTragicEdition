Creepy Black — Mu Overhaul v10: ?????, AZHI and the new BLACK FLAME
====================================================================

ROM:     Creepy_Black_Mu_v10.gb
SHA-256: fea56a6d600bed061effc4472af578053ed941645fcdbc2eac1510aa9a07a242
Input:   Creepy_Black_Mu_v9.gb. build_v10.py asserts every byte it replaces; manifest_v10.json logs them.

WHAT'S NEW
----------
1. The Mirage trainer class is now named "?????" ("????? wants to fight!", "????? sent out AZHI!").
2. Species B7 (the undead fossil Aerodactyl) is its own Pokémon: AZHI. GHOST/FLYING, fossil sprites,
   moves BLACK FLAME, FLY, DRAGONBREATH, FIRE BLAST. (Cry and Pokédex No.142 still borrowed.)
3. BLACK FLAME (move A8, rewritten): never misses, Fire Blast animation + black flash. The target is
   knocked out and every other Pokémon in the target's party faints too (HP 0, status cleared).
   - Used on the player: the stand-in "YOU" and any AZHI are spared; if the target IS the stand-in,
     it is the usual Mirage death (save wipe).
   - Used by the player: in a trainer battle every other enemy Pokémon (except an AZHI) faints.
4. DRAGONBREATH (new move AA): DRAGON, 60 power, 100%, 20 PP, 30% paralysis, Dragon Rage animation.
5. AZHI is unaffected by CURSE ("It doesn't affect Enemy AZHI!", no curse kill), MACABRE and
   BLACK FLAME. AZHI and PRETA are never "too scared" in Mirage battles.
6. Mirage rule change: only the death moves (MACABREBLADE, BLACK FLAME) kill outright now. AZHI's
   FLY, DRAGONBREATH and FIRE BLAST do normal damage to your Pokémon; any hit on the stand-in "YOU"
   is still fatal. Pokémon that faint in a Mirage battle are still removed permanently (PRETA revives).
7. Real Kabutops (0x5B) and Aerodactyl (0xAB) were checked: headers and front/back sprites are
   byte-identical to v1; only species B6/B7 use the undead sprites.

VERIFIED IN PYBOY (run_v10.sh)
------------------------------
- Mirage with AZHI: "????? wants to fight!", "????? sent out AZHI!", moves A8/FLY/AA/FIRE BLAST.
  BLACK FLAME: PRETA (active) and CHARMANDER fainted, stand-in kept.
  FIRE BLAST: PRETA 135 -> 90 (+burn); DRAGONBREATH: 135 -> 114. PRETA's MACABRE: "doesn't affect
  Enemy AZHI", HP unchanged.
- Wild AZHI vs GHOST's CURSE: "It doesn't affect Enemy AZHI!", HP 15 -> 15, battle continues.
- A player AZHI's BLACK FLAME knocked out a wild PIDGEY.
- Wild KABUTOPS vs a player AERODACTYL shows both original sprites.
- All earlier checks (run_v9.sh chain) and the v1-v5 chain pass on v10. Test fixes: t23_v9 samples the
  text box more often (it missed a line); t15_aero now accepts any AZHI move and skips when the chain's
  saved Mirage rolled PRETA instead of AZHI.
