Creepy Black Mu v44 (on v43): the POKeMON LEAGUE as BLACK, part 1 (LORELEI, BRUNO, LANCE; BLUE comes later).

SHA-256: e61d17f6783fd2ac33c4eed682d05d699a5a757687747e6ae1fe0ad2cc2a9ff6

Only when the player is BLACK (D46C). Pictures: qa_ref/v44_moonstone.png.

LORELEI, BRUNO and LANCE fight with their usual teams, but the MOON STONE protects them:
  - CURSE, MACABREBLADE, BLACK FLAME, MACABRE and BANE can't be used against them: choosing one makes a light flash
    (screen white, twice), then "A strange power blocks the move <MOVE>!", then the trainer's own line:
      LORELEI: Hmph. So the MOON STONE does resist you. Your darkness freezes here!
      BRUNO: Hah! The MOON STONE's power holds you! No tricks! Face my raw strength!
      LANCE: I see... The MOON STONE's light resists your darkness. Face my dragons like a trainer!
    The move menu comes back (no turn is lost); their POKeMON must be beaten by conventional means.
  - When their last POKeMON is down: another flash, "The MOON STONE shatters!", the POKeMON out is called back
    ("<MON> good! Come back!") and BLACK is sent out ("Go! BLACK!", BLACK's own back picture), then the usual after-win
    phase. There BANE is mandatory: any other move, ITEM or RUN -> "AGATHA's words echo within you: 'You must destroy
    them all!' 'Destroy all the intruders!'" and the menu comes back. BANE kills the trainer as in v39 (a random
    POKeMON the player hasn't caught joins); the room counts as beaten and the way on opens.
AGATHA's room is empty as BLACK: she is gone and her "beaten" flag (D865 bit 1) is set, so the way to LANCE is open.
Not BLACK, or any other trainer: unchanged.

Technical (code in 2F:6400):
- F:545D (MoveSelectionMenu stores the chosen move) -> call home 0x39 (new far stub) -> 2F sel44: stores the move as
  before; blocked -> texts, return address -> F:546D (LoadScreenTilesFromBuffer1 + MoveSelectionMenu, like "no PP").
  Move-menu items are 1-based while the menu is open (the game decrements cc26 before storing).
- F:7DCC (after-win phase check, called at F:46EC) now far-calls 2F ph44, which does the shatter + SwitchPlayerMon (F:5279,
  with wBattleMonSpecies2 = wcf91 = BLACK as the PKMN menu does, or the back picture stays the old one) and then
  phase2 (2D:6100) as before.
- F:7E19 (battle-menu hook, v23) -> 2E:7800 tramp44 -> 2F menu44 (phase: only FIGHT), then v23's 2E:59DB as before;
  refused -> back to the battle menu (F:4EDE). Temp flag D459.
- 1D:642D (AGATHA's room script: exit block) -> 1D:7E00 ag44 (BLACK: flag + sprite hidden).
- Class ids: LORELEI 2C, BRUNO 21, AGATHA 2E, LANCE 2F (opponent = class + C8).

Tests: t52_v44.py block (LORELEI/BRUNO/LANCE: flash, texts, no turn lost; MACABRE and BLACK FLAME too; SCRATCH still
works), shatter (LORELEI: flash + shatter, BLACK out with its back picture, RUN/ITEM/SCRATCH refused in the phase, BANE
kills, the way to BRUNO opens), agatha (empty room, way to LANCE), normal (not BLACK: CURSE as before, AGATHA there).
run_v44.sh = run_v43.sh + t52.
Static: check_hooks.py 114 hooks, 0 problems.
Regression (run_v44.sh): PASS=356 FAIL=0 (v43 suite + 37 t52 checks; every test keeps its v43 count).
t28_v14 koga_kill still stops on its old test-side "no path" assertion (also on v40-v43).
