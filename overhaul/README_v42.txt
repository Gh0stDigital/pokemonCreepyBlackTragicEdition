Creepy Black Mu v42 (on v41): a BANEd NPC can't move.

SHA-256: 8c0fff599dd64158059f132e17ed6779e8f8ab00b5c9c62c0afa37d7a96621be

v40 turned a BANEd NPC into a black POKe BALL by changing only its picture: a wandering NPC kept its movement byte
(WALK) and its ball walked around the map. Now the ball stays on the tile where the NPC stood:
  - right after the BANE and for as long as the ball waits (per frame);
  - after leaving the map and coming back (the map data reloads WALK; the map-load check sets STAY again).
Other NPCs keep their movement. Picking the ball up works as before.

Technical: the waiting ball's movement byte 1 (C2x6) = $FF (STAY). 2D:7EB0 setball/still; v40 load40's "waiting ball"
path (2D:7E4A) -> setball (picture 47 + STAY); frame40's "waiting ball: draw it" branch (2D:7E5C, jr c) -> still.

Tests: t50_v42.py still (BANE a wandering NPC with every NPC walking: the ball keeps its tile ~25 s with STAY; a spared
wandering NPC on screen still walks), reload (after leaving and coming back the ball keeps its tile, can still be picked
up). On v41 both fail (the ball walked over 4 tiles). run_v42.sh = run_v41.sh + t50.
Static: check_hooks.py 110 hooks, 0 problems.
Regression (run_v42.sh): PASS=309 FAIL=0; two older tests stop on an assertion before their checks, exactly as on v41
(t24_v10 fireblast: AZHI's FIRE BLAST does no damage in its seeded battle; t28_v14 koga_kill: no path to KOGA).
Both were already in the v40/v41 logs: test-side, not caused by v42.
