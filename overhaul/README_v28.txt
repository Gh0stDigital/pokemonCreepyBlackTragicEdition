Creepy Black Mu v28 (on v27): the world reacts to BLACK (D46C = 1).
- Ordinary NPCs panic when talked to, then "CURSE them?": YES = Gengar cry, black screen, gravestone (kept in a list of
  10 (map, sprite) pairs at D471-D484, applied at every map load); NO = the usual dialogue.
- Not affected: Lavender Town (town, houses, Center, Tower), trainers, item balls, clerks, nurses, link receptionist,
  OAK, BLUE, MOM, player's house, OAK'S LAB.
- Trainers no longer spot BLACK; they fight only when talked to.
Hooks: DisplayTextID init call -> 2D npc_talk; 0:325B sight check via home stub 0:167B; 3:4E8F gravestone test via 0:1688.
Tests: t36_v28.py (panic/exempt/sight/normal), t37_kills_save.py (save/continue/new game), run_v28.sh.
