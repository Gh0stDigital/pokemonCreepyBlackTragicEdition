Creepy Black Mu v39 (on v38): BANE in battle (part 2 of the BLACK TAMER mechanics).

SHA-256: 1b3046fe67929504a5c561d8ecbc477754873dd6e5d5b0b4aebfc3cd833b6217

Move AA (free since v11 dropped DRAGONBREATH) is BANE; BLACK knows it (new BLACKs; a v38 BLACK's CURSE becomes BANE on
the next step). All new code/data is in bank 2F (banks 2F-3F were never used by the game).

BANE on a POKeMON (BLACK out, wild or a trainer's):
  "BLACK used BANE!" -> the screen goes black -> the POKeMON's cry -> a black POKe BALL stands in its place ->
  "<MON> joined your party." (full party: "<MON> was sent to the PC.", POKeDEX owned).
  The POKeMON keeps its battle data (level, DVs, moves, HP); no nickname prompt (nickname = species name).
  Wild: the battle ends (like an escape). A trainer's: it counts as fainted, the trainer sends the next one / loses.
  No effect (the move then does nothing): PRETA, AZHI, GHOST, ?????, in MIRAGE battles, or party + box full.
BANE on a human (the after-win trainer phase, which now also starts with BLACK out):
  the trainer dies as before (kill bit, vanishes, gravestone on re-entry; BLUE still can't), then turns into a random
  POKeMON the player hasn't caught: black screen, its cry, the black POKe BALL, "The trainer became <MON>!", it joins the
  party (or the PC box) at the level of the trainer's last POKeMON, random DVs and level-up moves.
Technical: F:5726 (ExecutePlayerMove) -> F:7DD8 -> home 0x29 -> 2F bane_move; it leaves the move through F:7DCB (ret,
escape flag D078 = 1) or F:7DC9 (ld b,0 = enemy fainted). F:7FE8 (trainer-phase kill stub) -> 2F bane_phase (calls v12's
curse_trainer first). phase2 (2D:6111) reports BLACK as GHOST. AddPartyMon with wMonDataLocation = $10 = player party
without the naming screen. The black POKe BALL: qa_ref/v39_black_ball.png (7x7 tiles written to vFrontPic).

Tests: t47_v39.py (wild, wildbox, immune, trainer, migrate); run_v39.sh = run_v38.sh + t47.
Static: check_hooks.py 109 hooks, 0 problems.
