Creepy Black — Mu Overhaul v8: fossils vs PRETA, Mr. Mu to the Mansion, black-and-white back sprite
====================================================================================================

ROM:     Creepy_Black_Mu_v8.gb
SHA-256: a2de63667dd7bcf8408d359b48d098d11e9ee1e69d20d382998c130c3a4e0aa9
Input:   Creepy_Black_Mu_v7.gb. build_v8.py asserts every byte it replaces; manifest_v8.json logs them.

WHAT'S NEW
----------
1. MACABRE does nothing to the Black Tamer's fossil Kabutops / Aerodactyl: "It doesn't affect Enemy
   KABUTOPS!" (hook after the player's MoveHitTest, F:57D3). PRETA is no longer "too scared" in
   Mirage battles (all other Pokémon still are), so it can use its other moves there.
   Type chart reminder: the fossils are GHOST/ROCK and GHOST/FLYING, so CUT and STRENGTH (Normal)
   don't affect them either; SURF (Water) is super effective on Kabutops and normal on Aerodactyl.
   If PRETA wins, "RED defeated BLACK TAMER!", ¥0, and the usual Mirage cleanup runs.
2. Mr. Mu moves on: once the player leaves the Cerulean trade house after receiving PRETA
   (D460 2 -> 3 on the next map load), he is gone from the trade house and stands on the entrance
   carpet of Pokémon Mansion 1F (x6,y21, facing the door). Before that, the Mansion has no Mu.
   His Mansion lines are a placeholder (dialogue_v8.json): "Ah, RED. You came. / This mansion
   remembers what was made here. / We will talk again soon."
3. Fossil Kabutops back sprite: the dark-grey rib lines are white too; it is now black and white only.

VERIFIED IN PYBOY (run_v8.sh)
-----------------------------
- Mansion 1F without PRETA: no Mu. After PRETA: leaving the house sets D460 = 3, the trade house
  is empty on return, Mu is in the Mansion and says his lines.
- Mirage vs Fossil Kabutops: "PRETA used MACABRE! It doesn't affect Enemy KABUTOPS!", HP unchanged.
- PRETA's SURF (enemy at low HP) knocked out the fossil, BLACK TAMER defeated, Ghost back in the
  party, stand-in removed, PRETA kept.
- All v6/v7 checks and the full v1-v5 chain pass.

IMPORTANT LIMIT (design question for the next version)
------------------------------------------------------
The fossils' death moves still kill PRETA in one hit. Fossil Aerodactyl is faster than PRETA, so it
always strikes first and PRETA never gets to act against it. Fossil Kabutops is slower, so PRETA
gets exactly one attack (one SURF does about 94 of its 128 HP) before it dies. PRETA then revives
after 2 turns (v7), but your other Pokémon are still killed meanwhile.
