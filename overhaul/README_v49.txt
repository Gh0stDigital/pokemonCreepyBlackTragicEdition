Creepy Black Mu v49 (on v48): Black Tamer mechanics redux, part 3 (what BLACK is).

SHA-256: aa20ca46756462e41f7d424ffdb6b3f26f34a5dded5257fd2a8d56e8887f6837

1. POKeMON are too scared to attack BLACK. With BLACK out, the enemy's turn is "<enemy> is too scared to move!" (the
   base game's rule for GHOST, now also for BLACK), wild or trainer (BLUE too). Exceptions: the LEAGUE battles protected
   by the MOON STONE (LORELEI / BRUNO / LANCE, v44) - their POKeMON attack BLACK; MIRAGE battles; PRETA / AZHI.
2. Status immunity: BLACK can't be poisoned (TOXIC too), burned, frozen, paralyzed, put to sleep or confused. PRETA and
   AZHI can't be poisoned, paralyzed, put to sleep or confused - burn and freeze still work on them. A status move says
   "It doesn't affect <target>!"; a side effect (e.g. THUNDERBOLT's paralysis) simply doesn't happen. This works on
   either side (the MIRAGE's PRETA / AZHI too).
3. As BLACK there are no random encounters in POKeMON TOWER 1F-7F.
4. As BLACK nobody serves you - they are too scared:
   - POKeMON Center nurses ("The nurse is shaking... She is too scared to help you."), no healing;
   - POKe MART clerks ("The clerk is shaking... Too scared to serve you."), no buy/sell menu;
   - GAME CORNER prize vendor and coin clerk, BIKE SHOP, MAGIKARP salesman;
   - DAY CARE, NAME RATER, every in-game trade, the fossil revival at the lab ("They are shaking too much to help you...").
   Panicking NPCs (v28) still get the METAMORPHOSIS question first; NO -> they won't help. Not BLACK: all unchanged.
   (PCs and vending machines still work.)

Technical:
- Home 0x08 = 00: "rst 08" is now a 6-byte far call (ld hl,addr / ld b,bank / rst 08 -> nop -> 0x09 jp Bankswitch).
- 1: F:67C8 (GHOST out -> scared text) -> rst 08 2F scared49 / jp z,ExecuteEnemyMoveDone (7 nops to F:67D8).
- 2: F:7227 _JumpMoveEffect -> rst 08 2F imm49 (effect id -> D45A, reloaded right after; immune target: [sp+4] = F:72F2
  "ret", so the effect handler is skipped; status moves print the "doesn't affect" text first).
- 3: 4:78BC TryDoWildEncounter -> 4:7B80 tow49 (BLACK, map 8E-94: "can't encounter").
- 4: nurse 1:6FDF and mart 1:6C19 -> bank-1 stubs (1:7E40; 1:7E00-7E0E is the test ROMs' save installer); the mart greeting
  TX_FAR at 0:2A82 -> 2F hi49 (TX_ASM: BLACK -> the scared clerk); prize vendor 14:671B -> 14:7F60; in-game trades: predef
  55 -> 2F trade49; DAY CARE (48/1), NAME RATER (E5/1), fossil scientist (AA/1), MAGIKARP salesman (44/4), GAME CORNER coin
  clerk (87/2), BIKE SHOP (42/1): their text pointers -> a TX_FAR stub in their own bank -> 2F svN (TX_ASM: BLACK ->
  refused, else Bankswitch to the original TX_ASM code).
- Tests: t57_v49.py scared, moon, status, bstatus, tower, services. t36 exempt (nurse) and t46 daycare (DAY CARE / NAME
  RATER as BLACK, plus the normal case without BLACK) expect the refusal from v49 on. run_v49.sh = run_v48.sh + t57.
  The GAME CORNER coin clerk is not walked to in the test (no path for the walker behind the counter): same stub as the
  others.
Static: check_hooks.py 132 hooks, 0 problems.
Regression (run_v49.sh): PASS=454 FAIL=0 (v48 suite + 27 t57 checks).
t28_v14 koga_kill still stops on its old test-side "no path" assertion (also on v40-v48).
