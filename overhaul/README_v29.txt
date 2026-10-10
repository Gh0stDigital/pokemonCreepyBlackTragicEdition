Creepy Black Mu v29 (on v28): CURSE kills every trainer; the RAM corruption behind the late-game glitches is gone.

The bug (in the base hack, present in every earlier version)
  TalkToTrainer (0:3201) reads a trainer's kill index from offset 0xA of its trainer header into D4AE/AF. Only 23 of the
  game's 322 headers had one (the early routes up to Mt. Moon). In the other 299 that word is still the vanilla duplicate
  of the end-battle text pointer ($4000-$7FFF). CURSE treated it as killable and set bit (pointer) of the array at D4A4,
  i.e. one bit in DCA4-E4A3: PC box Pokemon data, the stack, and through echo RAM the sprite tables, OAM buffer and the
  screen tile map. No gravestone list knew those trainers, so they never died. From NUGGET BRIDGE on (the first trainers
  without an index) CURSE "stopped working" and every curse corrupted RAM somewhere.

The fix
  - killmap.py finds all 322 headers and the map each belongs to (through the map text tables: TX_ASM "ld hl,<header>").
  - The 299 headers get unique indices: 34-79 (free bits of D4A4-D4AD) and $100-$1FB (new array D430-D44F = 32 bytes of
    pokered's unused "ds 128" after wDestinationWarpID, inside the saved block, referenced by nothing). Header 11:6886
    (used by no map text) gets 0 = not killable.
  - 3:4DB9 (set/reset/test kill bit) rewritten in place (same 55 bytes): index >= $100 -> D430 array.
  - Map load: kill_chk2 (2D:6400) = the v28 NPC kill list, then a map -> (sprite, kill index) table for every trainer;
    a killed trainer is a gravestone. The home stub 0:1688 now calls kill_chk2.
  - NEW GAME clears D430-D4AD (was D450-D4AD).
  Saves made on older versions keep any bits the old bug already flipped (box data etc.); new kills are clean.

Tests: t38_v29.py table / nugget (Route 24 trainer: new index, bit in D430, PC box untouched, exactly one kill byte,
gravestone after re-entering, others alive) / forest (base index still works); t37 now also covers D430-D44F.
Regression (run_v29.sh: v3-v28 suites + t38): 191 PASS, 0 FAIL
