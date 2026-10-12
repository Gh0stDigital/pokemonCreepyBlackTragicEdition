Creepy Black Mu v40 (on v39): BANE on the map (part 3 of the BLACK TAMER mechanics).

SHA-256: 9b79453a00034a6c7c1676c63bc7acddb7367018b0f0dc680085a132e9b4233d

As BLACK, an ordinary NPC still panics when talked to; the question is now "BANE them?" (v28 asked CURSE).
  NO: the usual dialogue. YES: the screen goes black, the cry of a random POKeMON the player hasn't caught plays, and when
  the light comes back the NPC is a black POKe BALL lying on the ground ("Only a black ball remains...").
  Talking to the ball picks it up: the POKeMON joins the party (full: the PC box) at level 5 + 5 per badge, random DVs,
  level-up moves, no nickname prompt. The NPC is gone for good (hidden; no gravestone), the tile is free.
  A ball that isn't picked up stays where it is, also after leaving the map. Two balls can wait; a third BANE collects the
  oldest one at once ("<MON> joined your party.").
Trainers are unchanged: they never start a battle by sight (v28); talking to one starts its battle (no question). Exempt
NPCs (LAVENDER TOWN, clerks, nurses, OAK, BLUE, MOM, the player's house, OAK'S LAB) are unchanged.

Technical: sprite 47 (an unused "lying old man" duplicate) = the black ball (bank 2F sheet, darkened from the item ball).
v28's kill list gets (map, sprite|$80) for BANEd NPCs: the map-load pass (0:1688 -> 2D load40) gives a waiting ball its
picture and never makes BANEd NPCs gravestones; the per-frame check (killed13 -> 2D frame40) hides BANEd NPCs, draws
waiting balls. Waiting balls: D722-D727 (2 x map, sprite, species; unused WRAM inside the saved block, no code touches
D720-D727). DisplayTextID's init (0:2950) -> 2F npc_talk3 (pickup), otherwise on to v30's npc_talk2 through a new home
trampoline at 0x31 (ldh [hLoadedROMBank],a / ld [$2000],a / jp hl: same stack). v28's YES action (2D:4882) -> 2F bane_npc.

Tests: t48_v40.py (bane, persist, overflow, trainer); t36 panic hands over to t48 on v40+. run_v40.sh = run_v39.sh + t48.
Static: check_hooks.py 109 hooks, 0 problems.
