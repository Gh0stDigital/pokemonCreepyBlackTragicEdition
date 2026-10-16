Creepy Black — Mu Overhaul v71: notoriety and the bribed gate guards
====================================================================
Built from v70 by build_v71.py.

1. NOTORIETY (D85C, 0-255, saved; D85D/D85E are its helpers; all three are unused event-flag bytes, cleared by NEW GAME).
   +1 every time you win a TRAINER battle in which you used CURSE and the trainer is still alive afterwards: ordinary trainers, gym trainers, gym leaders, the rival, scripted
   grunts. Not counted: kills (CURSE finished them), battles without CURSE, wild battles, lost battles, the MIRAGE and the ritual battles.
   Mechanics: the game's kill routine (2E:41db) sets D85E bit 0; the battle start (14:6a50, where D452 is cleared) clears D85E; the after-battle hook (2D:5fc0, post2) adds 1 when
   the last battle was a trainer's (D713 >= $C8), D452 is set and D85E is 0, then marks D85E = 2 so later map loads don't count it again.
2. THE GUARDS OF THE FOUR SAFFRON GATE HOUSES (ROUTE 5, 6, 7, 8) check you when you step in front of them (the tiles the thirsty-guard check used), coming from the route side:
     - notoriety 0-2: nothing changes (after a murder the usual police bulletin still shows);
     - notoriety 3 and up: the bulletin first (if you have murdered), then a suspicion speech in three tiers (3-9 "you seem to fit some of the description", 10-24 "you match the
       description very well", 25+ "it's you, the killer"), then "My silence costs ¥N. Pay?" YES/NO. N = 100 x notoriety, at most ¥6000.
     - YES with enough money: the fee is deducted, "Hah! Couldn't possibly be you. Go right ahead."; the guard doesn't ask again during this visit. NO, or not enough money: you are sent back
       exactly like the thirsty guard does it.
     - Leaving the gate house and coming back is a new visit (every map load clears the paid flag D85D), so you pay again. Coming OUT of SAFFRON (previous map = SAFFRON) is free, and
       BLACK is never charged.
   The check runs at the start of each gate's map script 0, before the drink-flag test (a new text id 4 per gate: new text table, header text pointer repointed).
Tests: t79_v71.py gates (4 gates: pay, refuse, too poor, notoriety 2, BLACK, out of SAFFRON, same-visit repeat, tiers/fee cap, new visit, bulletin) and notor (spared / normal / killed
ordinary trainer, gym trainer, leader BROCK, two battles in a row).
Not covered: other guards (Route 22/23 badge guards, the other gate houses) are unchanged.
