Creepy Black Mu v45 (on v44): BLUE replaces the POKeMON the player CURSEd.

SHA-256: fcdc320b406621314689ea57c2966ec12db3789c2644caab8cbb58aadab9df07

Whenever CURSE kills one of BLUE's POKeMON (any of his battles: RIVAL1, RIVAL2, Champion), that POKeMON's whole
evolution line is gone from his later teams for good. A random POKeMON from the original 149 takes its place in
every later battle:
  - never MEW or MEWTWO, never one of the lines BLUE uses in any of his teams, never a line already used as another
    replacement (so his teams have no duplicates);
  - at the level of the POKeMON it replaces, and at the evolution stage that level allows (level evolutions at their
    own level, stone evolutions at Lv32, trade evolutions at Lv36): e.g. a rolled CHARMANDER is a CHARIZARD at Lv37;
  - CURSing a replacement replaces it again;
  - the battle where the kill happens is not changed; hero mode's MEWTWO can be replaced too.
BLACK's BANE does not trigger it (BANE on BLUE only matters in his final battle, which comes next).
Lines that were never killed stay exactly as before.

BLUE's 11 lines (all his teams): SQUIRTLE, BULBASAUR, CHARMANDER, PIDGEY, ABRA, RATTATA, GROWLITHE, EXEGGCUTE,
MAGIKARP, RHYHORN, MEWTWO. 124 possible replacements.

Technical:
- Saved table D86A-D874 (one byte per BLUE line, index in blue_fam: the replacement species, 0 = none). These are
  event-flag bytes that no code operand and no trainer header uses; NEW GAME clears them with the other event flags.
- Kill: FaintEnemyPokemon's far call at F:7D20 (to 2E:41C2) -> 2F kill45 (CURSE flag CC39 set, trainer battle, not the
  after-win phase, opponent RIVAL1/2/3): rolls the replacement, then far-jumps to 2E:41C2 as before.
- Load: ReadTrainer's two AddPartyMon calls (E:5CCF, E:5CE6) -> E:7EE0 stub -> 2F load45 (wcf91 = the replacement's
  stage for wCurEnemyLevel), then AddPartyMon (stats and moves made for the new species as usual).
- Tables in 2F (6800): blue_fam, cand (internal species), base_tab (species -> line base), stage_tab (6 bytes per
  species: min level + species for each stage along its branch). Evolution data read from EvosMovesPointerTable
  (E:70D1 in this ROM). TrainerDataPointers E:5D79 (index = class - 1).

Tests: t53_v45.py tower (CURSE the Tower team: every killed line gets a valid, different replacement), normal (no
kills: SILPH team unchanged), silph (PIDGEY line replaced: the slot holds the replacement at the same level and its
stage, the rest unchanged), chain (CURSE the replacement: a new one is rolled), champion (hero Champion: MEWTWO's slot
holds the Lv70 replacement). run_v45.sh = run_v44.sh + t53.
Static: check_hooks.py 116 hooks, 0 problems.
