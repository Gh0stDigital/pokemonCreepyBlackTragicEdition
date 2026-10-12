Creepy Black Mu v41 (on v40): CONSUME (part 4 of the BLACK TAMER mechanics).

SHA-256: 4630edb47863963a8bd1595a0ec44c1b4af60927de8de31ba4e0bad85cdaa657

Outside battles, BLACK's entry in the POKeMON menu offers CONSUME (listed like a field move: BANE counts as BLACK's field
move, shown as CONSUME).
  CONSUME -> "Consume which #MON?" -> choose a party member. BLACK, PRETA and AZHI can't be consumed ("BLACK can't
  consume that.").
  -> "Take which move?" -> a menu of its moves (B = cancel: nothing happens).
  -> BLACK learns the move through the game's own LearnMove: with 4 moves it asks which one to forget; BANE can't be
     forgotten ("HM techniques can't be deleted!"); giving up keeps everything as it was. A move BLACK already knows is
     refused ("BLACK already knows that move.").
  -> "BLACK consumed <MON>!": the POKeMON leaves the party for good and BLACK gains its whole experience total (capped at
     the Lv100 value). A new level ("BLACK grew to level N!") recomputes BLACK's stats at level + 9 (still "as strong as
     9 levels higher"), current HP grows with max HP. Battles still give BLACK no experience (v38).

Technical: bank 1 field-move tables copied to 1:7D80 with entry (BANE, name 10 = CONSUME) and the name list + CONSUME;
GetMonFieldMoves / DisplayFieldMoveMonMenu repointed. The party-menu dispatch (4:71C4, v25's hook) -> 4:7B20 fm41: entry 10
reads the bytes CB 57 as its handler -> consume4 -> 2F consume, then back to the party menu (4:70F5). LearnMove's IsMoveHM
call -> 1:ishm41 (BANE counts as an HM). LearnMove's result is read from BLACK's move list (a far call loses register b).

Tests: t49_v41.py (consume, full, refuse, normal); run_v41.sh = run_v40.sh + t49.
Static: check_hooks.py 110 hooks, 0 problems (reviewed: 4:71C4 returns the handler in hl on purpose).
