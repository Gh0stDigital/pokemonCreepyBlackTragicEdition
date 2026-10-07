Creepy Black — Mu Overhaul v6: Mr. Mu in Cerulean, the DOME FOSSIL and PRETA
==========================================================================

ROM:     Creepy_Black_Mu_v6.gb
SHA-256: 94919c4f615f514fe1188a7629bee4890ea4521b57edc799705569a2268efffe
Size:    1,048,576 bytes; header and global checksums fixed.
Input:   Creepy_Black_Mu_v5.gb. build_v6.py asserts every byte it replaces; manifest_v6.json logs
         before/after bytes. Dialogue is in dialogue_v6.json (lines <= 17 columns).

WHAT'S NEW
----------
Cerulean trade house (the house with the trade man): MR. MU sits in the left chair at the table,
  facing the old woman. He is only there once the player owns Ghost (D451); otherwise the house
  is unchanged (he is hidden before the first frame is drawn).
First talk: he introduces himself properly (MR. MU, an executive of SILPH CO.), apologizes for his
  abrupt question, says he is looking for a protege to teach business, and warns that TEAM ROCKET
  is snooping around town and near MT.MOON. Later talks: a short TEAM ROCKET reminder.
If the bag holds a DOME FOSSIL he is impressed and asks:
  "Is death something we should accept... even when we have the power to undo it?"
  ACCEPT IT -> "Hm. Then why carry the remains of something that died so long ago?" (fossil kept;
               he asks again next time).
  DEFY IT   -> "...I see. Then perhaps this shouldn't remain a fossil." He takes the DOME FOSSIL,
               the screen goes black while the Pokémon-healed jingle plays, and the player receives
               PRETA. If the party is full he keeps the question for later ("Make room...").
After that he only says the hint: "Oh, one more thing. If you happen to find another fossil...
  don't be too quick to change it. Some things are more valuable as they are."
PRETA: undead Fossil Kabutops (species B6: fossil sprite, GHOST/ROCK, Kabutops cry, dex No.141 is
  marked seen + owned), Lv50, OT = player, perfect DVs (15/15/15/15/15),
  stats HP 135 / ATK 135 / DEF 125 / SPD 100 / SPC 90, moves MACABRE, CUT, SURF, STRENGTH.
  CUT/SURF/STRENGTH work in the field with the usual badges.
MACABRE (new move A9): typeless (shows TYPE/ ???), 10 PP, never misses, Slash animation,
  always leaves the target at exactly 1 HP (no critical hit text; on a 1-HP target it does nothing).

TECHNICAL NOTES
---------------
- Map 3F header (bank 7) repointed to a new object table (+ GENTLEMAN at x2,y4 facing right, text 3),
  new text table and a map script that hides object 3 (C130/C234/C235) unless Ghost is owned.
- Text script in bank 7 at 0x7100; awakening routine in bank 2E at 0x4600 (RemoveItemByID, v2
  black_on/off, MUSIC_PKMN_HEALED E8, fixed 44-byte party struct, OT name, nickname, dex flags).
- Death-move table moved to E:7D30 (A7, A8, A9); the three move-reader helpers (banks 3, E, F)
  repointed. GetMaxPP, HealParty and WriteMonMoves now also read through the helpers.
- Hooks: ApplyDamageToEnemyPokemon (F:6218) -> damage = enemy HP - 1 for A9;
  player PlayMoveAnimation call (F:5804) -> A9 plays SLASH.
- New saved RAM: D460 Cerulean Mu state (0 not met, 1 introduced, 2 PRETA given). D457 is used as
  a temp while PRETA is added.

VERIFIED IN PYBOY (run_v6.sh; warps from Pallet into the trade house by rewriting a door warp)
-----------------------------------------------------------------------------------------------
- Without Ghost: Mu is never drawn (no OAM entry at his chair in any frame) and can't be talked to.
- With Ghost: intro text (SILPH, MT.MOON), D460 = 1; second talk = Rocket reminder.
- DOME FOSSIL: ACCEPT keeps the fossil; full party keeps the fossil and D460 = 1.
- DEFY: fossil removed, black screen + healed jingle (sound E8), PRETA added with the exact struct
  above, OT name/ID = player; next talk = fossil hint.
- Wild battle with PRETA: "PRETA used MACABRE!", Slash animation (anim A3), enemy 13 -> 1 HP,
  second use 1 -> 1, no critical hit, fight menu shows TYPE/ ??? and PP 10/10.
- Status screen shows the fossil Kabutops pic, No.141, GHOST/ROCK, stats and PP x/10.
- Mom's heal restores MACABRE to 10/10.
- Full v1-v5 regression chain (run_v3.sh) passes on v6.

NOT VERIFIED / KNOWN LIMITS
---------------------------
- The trade house was reached by a test warp, not by walking from Cerulean City.
- MACABRE against a Substitute damages the substitute by (enemy HP - 1).
- Only one DOME FOSSIL is checked; the HELIX FOSSIL path is untouched (the hint is flavor for now).
