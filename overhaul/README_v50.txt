Creepy Black Mu v50 (on v49): Black Tamer mechanics redux, part 4 (PRETA and AZHI).

SHA-256: ac2cd92d4056e79c21935500c9a3fe8b1b1f5ebb55cc04b78885b4a1ee6f2f75

1. PRETA makes the opposing POKeMON a little nervous (not GHOST types): its DEFENSE counts half, so PRETA's physical
   moves (CUT, STRENGTH, ...) do double damage (capped at 999). AZHI makes it a little anxious (not GHOST types): the
   opposing POKeMON's accuracy against AZHI is halved. Works on either side (the MIRAGE's PRETA / AZHI too). No message.
2. Revival: a fainted PRETA comes back 2 turns later, a fainted AZHI 3 turns later, each with half its max HP and no
   status: "<name> rose from the dead!". After every battle PRETA and AZHI are at full HP (fainted or not).
3. Levels: the PRETA MR. MU awakens from the DOME FOSSIL is Lv25 (stats, experience and HP of a Lv25, perfect DVs, same
   moves). At the end of the ritual an owned PRETA / AZHI (party or current box) below Lv50 is raised to Lv50 (party:
   experience, level, stats, full HP; box: experience and level - stats follow when it is withdrawn); one that joins at
   the ritual is Lv50 as before.
   AZHI: the story has no AZHI before the ritual (it only joins there, Lv50), so its "Lv35 before the ritual" has no case
   yet; any AZHI below 50 that the player owns at the ritual is raised like PRETA.
4. Items have no effect on BLACK in battle either: with BLACK out, X ATTACK / DEFEND / SPEED / SPECIAL / ACCURACY,
   GUARD SPEC and DIRE HIT say "It won't have any effect." (not used up). v38 already refused the party-menu items.

Technical:
- F:7F5E-7F71 (tail of v10's animation routine, unreachable since v48): adj50 / hit50 stubs (call the original, then
  "ld hl / ld b,$2f / rst 08" to 2F). F:7F72-7F79 are still free.
- Nervous: AdjustDamageForMoveType calls F:57CD (player) / F:685F (enemy) -> adj50 -> 2F nerv50 (attacker PRETA, move type
  < $14, target types not GHOST: wDamage x2).
- Anxious: MoveHitTest's call CalcHitChance (F:66C8) -> hit50 -> 2F anx50 (defender AZHI, attacker types not GHOST: the
  attacker's wPlayer/EnemyMoveAccuracy / 2).
- Revival: v7's turn stub (F:7E36) -> 2F tick50 (D461: low nibble PRETA countdown 3, high nibble AZHI 4; 0 -> revive:
  HP = max/2, status 0, text); after battle 2D:5FC4 (v31) -> 2F post50 (both at max HP, D461 = 0), then v7's post (2E:4760:
  MIRAGE cleanup).
- PRETA Lv25: v6's awaken struct 2E:469A (v3's kab_data header: KABUTOPS base stats, slow growth: exp 19531, stats 72/70/65/52/47).
- Ritual: 2D:46B4 jp black_join -> 2D:7F80 ritual50 (far boost50, then black_join).
- Items: ItemUseXStat 3:6435, ItemUseGuardSpec 3:640D, ItemUseDireHit 3:6426, ItemUseXAccuracy 3:6344 first bytes
  (ld a,[wIsInBattle] / and a / jr|jp ...) -> ld hl,xitem50 / ld b,$2f / rst 08; 2F xitem50 sets the return address:
  not in battle -> "not the time" as before, BLACK out -> ItemUseNoEffect (3:68AD), else the item's battle code.
- Tests: t58_v50.py nervous, anxious, revive, posthp, preta25, xitem, ritual. t17 (MR. MU's PRETA level), t19 (PRETA full HP
  after the battle = its max HP) and t23 (Rare Candy on PRETA) expect the Lv25 PRETA from v50 on. run_v50.sh = run_v49.sh
  + t58.
Static: check_hooks.py 135 hooks, 0 problems.
Regression (run_v50.sh): PASS=468 FAIL=0 apart from the Lv25 PRETA's experience value, which changed afterwards (slow growth, as
v6's Lv50 struct); t58 preta25 / ritual / revive and t17 were re-run on the final ROM and pass.
Fixed on the way: post50 runs every step (0:00C0 wraps the battle check) and now only acts when a battle happened (carry);
t24_v10 (AZHI hits) and t57 (SPORE) were made robust against RNG order.
t28_v14 koga_kill still stops on its old test-side "no path" assertion (also on v40-v49).
