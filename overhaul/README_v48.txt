Creepy Black Mu v48 (on v47): Black Tamer mechanics redux, part 2 (BLACK's new moves, negative animations).

SHA-256: de46558fa472bda5e2dacf6376b227cb476af9b799cd64643ad4e9c42d0d53a0

Pictures: qa_ref/v48_negative.png (PRETA's MACABRE = CRABHAMMER, AZHI's BLACK FLAME = FIRE BLAST, BLACK's GHOST WALK turn 1
= TELEPORT, all in the negative palette).

1. GHOST WALK (move AB, 90 power, typeless like the other overhaul moves, 95% accuracy, 15 PP) is a two-turn move like
   FLY: turn 1 "BLACK faded into dark!" with TELEPORT's animation (the FLY charge), BLACK can't be hit; turn 2 the attack
   with CUT's animation. Both animations play in a negative (inverted) palette.
2. DAMNATION (move AC, 1 PP): HYPER BEAM's animation (its charge and its beam, in one turn), then it works like CURSE on
   the target and every other POKeMON of the trainer dies with it: the battle is won at once (trainer phase as after any
   win). A wild battle ends like a CURSE. BLUE: every line it kills is replaced (v45). AZHI is immune (like to CURSE); in
   MIRAGE battles only the target is cursed. The MOON STONE blocks it like the other death moves (v44).
3. BLACK knows METAMORPHOSIS, CURSE, GHOST WALK, DAMNATION (fixed; v47's step fix restores them with full PP).
4. Negative animations: PRETA's MACABRE uses CRABHAMMER's animation, AZHI's BLACK FLAME FIRE BLAST's, both inverted (on
   either side, the MIRAGE trainer's PRETA / AZHI too). MACABREBLADE keeps SLASH + the black flash.
5. AZHI knows BLACK FLAME, FLY, DRAGON RAGE, SKY ATTACK (no more FIRE BLAST): the AZHI that joins at the ritual and the
   MIRAGE's AZHI. The ritual AZHI's BLACK FLAME now has its 10 PP (v38's struct had 0).

Technical:
- Move data E:7D48 (AB: FLY effect 2B) / E:7D4E (AC: CURSE's effect 01); names after METAMORPHOSIS in 2C.
- Animations: F:7F53 (v10's move-animation remap, called by both sides with a = move id) -> ld [wAnimationID],a + tail far
  jump to 2F anim48 (map A7 SLASH, A8 FIRE BLAST, A9 CRABHAMMER, AA THUNDERBOLT, AB CUT, AC HYPER BEAM; Delay3 + predef
  MoveAnimation like PlayMoveAnimation; A7/A8 then the black flash as before).
- Negative palette: MoveAnimation (1E:4D65 call SetAnimationPalette, 1E:4D98 call WaitForSoundToFinish) -> 1E:7FD1 stubs ->
  2F inv48_on (attacker's move + this animation in invtab: BLACK FLAME/FIRE BLAST, MACABRE/CRABHAMMER, GHOST WALK/CUT,
  GHOST WALK/TELEPORT -> BGP, OBP0, OBP1 inverted) and inv48_off (BGP 1B -> E4). No flag: the charge turn's TELEPORT
  (ChargeEffect's own PlayBattleAnimation) is caught by the attacker's move.
- DAMNATION: home 0x29 (before the player's move) -> 2F pre48 (CC39 = 1 like CURSE; trainer battle: HP 0 for every other
  enemy POKeMON, v45 kill45 for each), then v39 bane_move.
- GHOST WALK's charge text: ChargeMoveEffectText's TX_ASM (F:79C4) rewritten with ret z per move (4 bytes shorter), the
  default is "faded into dark!" (TX_FAR at F:7E99 -> 2F).
- MOON STONE list: sel44's ld hl,forbid -> forbid48 (+ AC).
- Tests: t56_v48.py moves, gwalk, damnwild, damntr, macabre, normal, azhi, moon. t55 accepts the four moves from v48 on;
  t24_v10's MIRAGE AZHI moveset check expects SKY ATTACK from v48 on (its FIRE BLAST test still forces FIRE BLAST).
  run_v48.sh = run_v47.sh + t56.
Static: check_hooks.py 128 hooks, 0 problems.
Regression (run_v48.sh): PASS=423 FAIL=0 and three t24_v10 modes (bf, fireblast, dragonrage) stopped on their
"AZHI knows FIRE BLAST" assertion (the intended v48 change); after updating that check they pass (4 more PASS).
t28_v14 koga_kill still stops on its old test-side "no path" assertion (also on v40-v47).
