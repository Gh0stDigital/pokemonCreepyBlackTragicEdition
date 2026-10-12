Creepy Black Mu v43 (on v42): the black ball on the map is the POKe BALL of the battle throw, blacked out.

SHA-256: ffc97a4d7a823e6f5e46936f4c323f027c7b6695de2108fb308cd62d038e0cee

A BANEd NPC turns into the POKe BALL that the battle's throw animation shows (as it lies after landing), all black,
with the seam between the halves (light grey) and the shine (dark grey) kept so it still reads as a ball.
Picture: qa_ref/v43_ball_before_after.png (left v42, right v43).

Bug fixed on the way: since v40 the ball never showed as a ball on outdoor maps. Outdoor maps only load their own
sprite set; the loader looked picture 47 up in the set, missed, and gave the ball a garbage graphics slot, so it was
drawn with some other sprite's tiles (in Pallet Town a bald head). Indoors it showed v40's item-ball copy.

Technical:
- Sprite 47's sheet (2F:5159) = MoveAnimationTiles0 tiles 06/07/16/17 (the toss ball's frame block at 1E:712A),
  blacked out and centred.
- 2F:6000 ball_fix: every sprite with picture 47 gets four-tile slot 0C ($87C0), or 0B ($8780) when another sprite uses
  0C, and the ball tiles are copied there (CopyVideoData while the font is loaded, else a direct copy, like the game's
  own loader).
- InitMapSprites (5:785B, map load and every redraw after menus/text) -> 5:7FB0 init_w: the original code, then
  ball_fix (all registers and the carry flag kept: MIRAGE code needs them; a first build lost them and the game
  reset after a MIRAGE battle, caught by t40). bane_npc's call to add_bane (2F:50C3) -> bane_add: add_bane, then ball_fix (the ball shows at once).

Tests: t51_v43.py look (Pallet: after the BANE and after coming back the ball's slot holds the ball tiles, no other
sprite shares it, the spared NPC's graphics are unchanged), indoor (BLUE's house: same). Both fail on v42.
run_v43.sh = run_v42.sh + t51.
Static: check_hooks.py 112 hooks, 0 problems.
Regression (run_v43.sh): PASS=319 FAIL=0 (v42 suite + 9 t51 checks; every test keeps at least its v42 count).
t28_v14 koga_kill still stops on its old test-side "no path" assertion (also on v40-v42).
