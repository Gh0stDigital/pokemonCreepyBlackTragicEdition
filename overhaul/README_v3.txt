Creepy Black — Mu Overhaul v3: the Mirage Black Tamer
=====================================================

ROM:     Creepy_Black_Mu_v3.gb
SHA-256: 221da20e1a68559cbdbf2525be08bbb6375e3403771fc9eb6139399501b956ab
Size:    1,048,576 bytes; header and global checksums verified.
Input:   Creepy_Black_Mu_v2.gb (e7855fae...d280d). build_v3.py asserts every byte it replaces;
         manifest_v3.json logs before/after bytes for all patches. Includes everything from v2.

HOW IT WORKS
------------
Ghost-use counter (D45C, saved): +1 every time Ghost's Curse is used (max 255).
Mirage chance: on every random wild encounter, chance = min(uses x 2, 64) / 256
  (about 0.8% per Curse use, capped at 25% after 32 uses). Only after Ghost is acquired,
  never in the Safari Zone, and not if Ghost is in the party and the current PC box is full.
Encounter: the wild battle becomes a trainer battle against BLACK TAMER (unused class 13),
  drawn as the player's front sprite as a solid black silhouette.
  His team is one Lv50 undead fossil, 50/50: KABUTOPS (Kabutops fossil sprite, GHOST/ROCK,
  MACABREBLADE) or AERODACTYL (Aerodactyl fossil sprite, GHOST/FLYING, BLACK FLAME).
  Both use the real Kabutops/Aerodactyl cries.
Ghost is deposited into the current PC box right before the battle and withdrawn back
  into the party afterwards.
Your Pokémon are always "too scared to move" (your attacks never happen).
"You": a stand-in party member named after the player, shown with the player's back sprite,
  is added in the last slot. It's sent out first if you have no other Pokémon, or when
  all your Pokémon are dead. It can't attack (too scared), only RUN: 166/256 = 65%.
Death moves (never miss, unaffected by type, always kill, with a black flash):
  - Hits one of your Pokémon -> it faints. After the battle every Pokémon that was alive at
    the start and died in the fight is permanently removed from the party.
  - Hits you -> black screen, the fossil's cry, full save wipe, cold restart.
Escaping: dead Pokémon removed, stand-in removed, Ghost returned, flags cleared.
Tuning: TUNING in build_v3.py (per_curse, chance_cap, run_success).

TECHNICAL NOTES
---------------
- Move IDs A7 MACABREBLADE / A8 BLACK FLAME: names appended after STRUGGLE in bank 2C; move data
  in bank E, served through hooks at every battle/AI/PP move-data reader (F:6403, F:6BC6,
  E:58C6, 3:77AF).
- Species B6/B7 (the Kabutops/Aerodactyl fossil pic IDs) get full headers from a hook at the end
  of GetMonHeader; their dex mapping is set to 141/142 so the "seen" flag write is safe.
- Stand-in uses unused species 79 (MISSINGNO slot, sprite bank C = the player's back pic).
- Hooks: PrintGhostText (scared), TryRunningFromBattle (65%), ApplyDamageToPlayerPokemon
  (kill/wipe), enemy PlayMoveAnimation (Slash / Fire Blast visuals + black flash),
  TryDoWildEncounter exit (Mirage roll), both overworld NewBattle calls (cleanup).
- New saved RAM: D45C counter, D45D Mirage active, D45E alive-at-start mask, D45F Ghost deposited.

VERIFIED IN PYBOY (run_v3.sh, starting from a new game)
--------------------------------------------------------
- All v2 checks still pass (opening, Mu, sprites, Ghost award, hunger drain/eat/permadeath,
  trainer Curse + gravestone + frightened text, wild Curse, police alert on/off).
- Curse use raises the Ghost-use counter.
- With a high counter a Route 1 encounter became the Black Tamer battle; Ghost moved to box 1,
  stand-in appended; silhouette trainer pic and "BLACK TAMER wants to fight!" shown.
- Fossil Kabutops Lv50 used MACABREBLADE: starter fainted; player sent out as "RED" with the
  player back sprite; Fossil Aerodactyl Lv50 used BLACK FLAME.
- "RED is too scared to move!" shown when the player acts first.
- RUN: escapes and "Can't escape!" both happen; a failed run is followed by the death move and
  a full SRAM wipe.
- After escaping: dead starter removed, stand-in removed, Ghost back in party, box restored.
- Ghost-only party: the player is sent out first; escaping restores Ghost.

NOT VERIFIED / KNOWN LIMITS
---------------------------
- The run rate was sampled only a few times (it uses the game's battle RNG against 166/256).
- If you open STATS on the stand-in mid-battle, it shows dex No.000 and the back sprite.
- Items (Potions etc.) can still be used during the fight; they can't save you from a death move.
- Kabutops/Aerodactyl get marked as "seen" in the Pokédex when the fossils appear.
