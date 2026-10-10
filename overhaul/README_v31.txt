Creepy Black Mu v31 (on v30): GHOST gets its lead slot back after a MIRAGE battle.

A MIRAGE battle deposits GHOST in the PC (v3) and withdraws it afterwards; a withdrawn Pokemon always lands in the last
party slot, so a leading GHOST used to come back last. Now:
  - the deposit remembers whether GHOST was leading: D45F = 2 (led) or 1 (didn't) - stub 2E:7CC0, hooked at 2E:4364;
  - after the battle the cleanup runs as before (home stub 0:00C4 now far-calls post2 at 2D:5FC0, which calls the old
    cleanup 2E:4760), then a GHOST that led is moved back to slot 1; the others keep their order (species, data, OT,
    nicknames all moved together).
A GHOST that wasn't leading still comes back last (unchanged). The other temporary removals already kept the slot:
the Pokemon Center heal (v13) and MR. MU's ritual (v23).
Tests: t40_v31.py lead / second (a real MIRAGE encounter on Route 1, RUN, party order checked).
