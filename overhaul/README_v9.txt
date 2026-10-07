Creepy Black — Mu Overhaul v9: PRETA is its own Pokémon, cursed Pokémon can't be candied or Center-healed
=========================================================================================================

ROM:     Creepy_Black_Mu_v9.gb
SHA-256: 064c2117243d1340ff1b3f5e55dcac3cfb654ed1d455c46d8d0f5d2f256fa70d
Input:   Creepy_Black_Mu_v8.gb. build_v9.py asserts every byte it replaces; manifest_v9.json logs them.

WHAT'S NEW
----------
1. Species B6 is named PRETA (it was KABUTOPS). This covers the player's PRETA and the Black Tamer's
   undead fossil: "BLACK TAMER sent out PRETA!", "Enemy PRETA used MACABREBLADE!", status screen.
   (Cry and Pokédex No.141 are still borrowed from Kabutops.)
2. PRETA vs PRETA: the player's MACABRE doesn't affect the enemy PRETA (or fossil Aerodactyl) (v8),
   and now the enemy PRETA's MACABREBLADE doesn't affect the player's PRETA either:
   "It doesn't affect PRETA!" (hook after the enemy's MoveHitTest, F:6865).
   Fossil Aerodactyl's BLACK FLAME still kills PRETA.
3. GHOST, PRETA and fossil Aerodactyl (species 1F, B6, B7):
   - Rare Candy: "It won't have any effect." (level unchanged).
   - Pokémon Center: the nurse heals everyone else; these keep their HP, status and PP.
     Mom's heal, PRETA's own revival and items (Potions, Revives, Ethers) still work.

New RAM: D462 = temp flag while the nurse's HealParty runs (always 0 outside it).

VERIFIED IN PYBOY (run_v9.sh)
-----------------------------
- Black Tamer with fossil PRETA: names show PRETA; MACABRE "doesn't affect Enemy PRETA"; enemy
  MACABREBLADE "doesn't affect PRETA" twice; two SURFs (128 -> 42 -> 0) win; cleanup ok.
- Rare Candy: PRETA Lv50 and GHOST Lv1 unchanged with "It won't have any effect."; CHARMANDER levels up.
- Viridian Pokémon Center with every party member at 5 HP: CHARMANDER healed to 22, PRETA and
  GHOST stay at 5, PRETA's MACABRE stays at 3 PP.
- All earlier checks pass: run_v8.sh, run_v7.sh, run_v6.sh and the full v1-v5 chain (run_v3.sh) on v9.
  t19_revive now counts the turns fought between faint and revival from the battle text (2).

NOTE
----
In PyBoy, pressing on through the nurse's goodbye after a test warp into the Pokémon Center hangs
the emulator. It happens identically on v1, so it predates the overhaul; the test reads the result
right after "Your POKéMON are fighting fit!".
