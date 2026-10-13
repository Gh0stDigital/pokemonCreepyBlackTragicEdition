Creepy Black Mu v47 (on v46): Black Tamer mechanics redux, part 1.

SHA-256: 2aa24b869b140f5f4071365ac8308266ebd84d368c8bcb6cd351a7356297e1d3

Pictures: qa_ref/v47_black_pokemon.png (a marked CHARMANDER: black back picture in battle, black status screen, black
party icon next to BLACK's normal one).

1. BANE is now METAMORPHOSIS (move AA, same effect).
   - In battle: "BLACK used METAMORPHOSIS!", THUNDERBOLT's animation, then the black screen, the target's cry and the
     black POKe BALL as before (also when a trainer becomes a POKeMON in the trainer phase).
   - On the map: "They are shaking. METAMORPHOSIS?" - no animation, the rest as before.
   - "The PC is full. It failed!" when party and box are full.
2. Every POKeMON gained through METAMORPHOSIS (battle, trainer phase, black ball picked up on the map) is pitch black:
   - battle back picture (every pixel that isn't white is black),
   - status-screen front picture (party, PC box summary),
   - party-menu icon (drawn with the second sprite palette set to black).
   No new species: the POKeMON is marked in its own data (party/box struct byte 7, the unused catch-rate copy, = 1;
   no species and no overhaul struct uses 1), so the mark survives the PC, the Day Care and saving.
3. CONSUME is gone. BLACK's party-menu entry is CURSE: "Curse which POKeMON?" -> pick a party member (not BLACK, PRETA,
   AZHI) -> "BLACK consumed <MON>!": it is gone and BLACK gains its experience (new levels, stats at level + 9 as
   before). No move is taken any more.
4. BLACK's moves are METAMORPHOSIS and CURSE (METAMORPHOSIS first, so the battle cursor starts on it). They are fixed:
   every step outside battle puts them back with full PP (BLACK can't use the POKeMON Center), so an older BLACK with BANE
   or consumed moves is switched too. BLACK's CURSE in battle works like GHOST's (the battle ends with the curse kill).

Technical:
- Move name 2C:4636 "METAMORPHOSIS"; v39 texts repointed (bane_move / give): t_used, t_full; the map question at 2D:5C00 is
  a TX_FAR to the new text in 2F.
- v39 black_ball callers (2F:4040 bane_move, 2F:4167 bane_phase) -> meta_ball (2F): THUNDERBOLT (wAnimationID 55,
  predef 8), then black_ball.
- Mark: v39 give's two endings (party / box) -> mark_party / mark_box (2F) set byte 7 = 1 (party: the new last member;
  box: SendNewMonToBox puts it first at DA96).
- Back picture: LoadMonBackPic's copy to vSprites (F:720E) -> 2F back47: party mon wPlayerMonNumber marked (and it is the
  battle mon) -> blacken the merged picture in SRAM (A188, 784 bytes: lo = hi = lo | hi), copy to $9310, then the old copy.
- Status screen: 4:6ABA call LoadFlippedFrontSpriteByMonIndex -> 4:7B60 st47: wLoadedMon+7 (CF9F) marked -> 2F front47
  (blacken, copy to $9000).
- Icons: 1C:58B9 call WriteMonPartySpriteOAM -> 1C:7CC0 icon47: marked -> OAM palette bit (OBP1) on its 4 sprites in the
  shadow OAM and in the saved copy (CC5B) the animation restores from; OBP1 = FF. Nothing else on the map or in the party
  menu uses OBP1 (checked: no OAM entry has the palette bit there).
- CURSE: field-move name "CONSUME" -> "CURSE" (bank 1), prompt text, 2F:542C call pick46 / jr z -> jp .learned (no move).
- Moves: BLACK struct (2D s_black) = AA, A5 / PP 10, 1; hunger_wrap's BLACK branch (2D:44C9) -> 2D:7F60 step47 -> 2F mig47
  (moves + PP from bmoves every step), then v38 black_step. Replaces v39 step39 (CURSE -> BANE).
- Tests: t55_v47.py meta, back, status, icon, curse, moves, map, bcurse, normal. t49 (CONSUME) is skipped from v47 on;
  t46/t47/t48/t52/t54 accept the new name in their texts. run_v47.sh = run_v46.sh + t55.
Static: check_hooks.py 126 hooks, 0 problems.
Regression (run_v47.sh): PASS=403 FAIL=0 (v46 suite without t49's CONSUME checks + 24 t55 checks).
t28_v14 koga_kill still stops on its old test-side "no path" assertion (also on v40-v46).
