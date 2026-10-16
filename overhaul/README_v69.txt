Creepy Black — Mu Overhaul v69: ordinary trainers sulk after CURSE + a fix for v67/v68
======================================================================================
Built from v68 by build_v69.py.

1. SULKING TRAINERS. Every ordinary trainer (not the gym trainers, who have v67's lines) that you used CURSE on but spared (RUN in the trainer phase) has a different
   after-battle line from then on: they tell you to go away, are scared of you, some swear they won't tell anyone ("Please just go. I won't tell anyone, I swear."
   / "Nobody will hear it from me." / "Not a word, I promise." / ...). 16 lines, picked by the trainer's kill index (neighbours differ).
   A trainer who dies keeps being a gravestone; a trainer beaten without CURSE keeps the usual text; scripted trainers (rival, scripted grunts: no trainer header) are not covered.
   Storage: one bit per kill index (42 bytes) in event-flag bytes that no code and no trainer header uses: D784-D78D, D7A4-D7AE, D80A-D812, D84F-D856, D858-D85E.
   D844 = "a trainer with a header is fighting" (set before the battle by the text dispatcher, cleared by EndTrainerBattle).
2. BUG FIX (v67 and v68): after a trainer fight EndTrainerBattle did not mark the trainer as beaten, so they challenged you again. The far call I put there destroyed hl
   (the flag address) before TrainerFlagAction used it; the v67 tests set the flags by hand and missed it. The home code now pushes hl around the far call and the bank-31
   routine sets the flag itself. t77 checks that the trainer does not challenge again.
Tests: t77_v69.py sulk / normal / kill on Route 3 (kill index 1) and Route 4 (kill index 308, the high bit array).
