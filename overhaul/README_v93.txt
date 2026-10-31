Creepy Black Mu v93 (on v92): the ritual's HUD levels and sounds, a quiet GHOST battle start, OAK leaves his lab, BLUE's Route 22 gate on the BLACK TAMER path
SHA-256: 40257145a00edb4eb616c5b2f3923a488adf059ef4521f4533aed0b64c2e59b0

1. HUD levels (aesthetic only): in the ritual battle YOU (RED) shows Lv10 and MR. MU Lv68.  Only the level printed in the two HUD routines changes (F:4DBC ply93, F:4E45 en93, bank 32:7800);
   the real levels, stats and damage are untouched (STRUGGLE still takes the same 4 turns, YOU keeps the same HP).  Species-based: YOU (79) anywhere shows Lv10, MR. MU (20) Lv68.
2. MR. MU's death plays no faint sounds (the fall + thud at F:45C9 -> faint93; any other trainer still plays them).
3. The MASTER BALL catch of ????? is silent: the predef 08 prefix (1:7D60) turns the sound hardware off (NR52) when the ball is thrown in the ritual (RIT 2); the engine switches it back on at the battle
   end (stop-all-music) and the chamber script (chm93 via 18:6FC2) does so too if needed.
4. The GHOST battle (RIT 5 / 7 / 8) starts as quietly as MR. MU's: no slide, "Go! RED!", summon animation or cry for the player (pre93 replaces pre77 at the F:7FB8 stub).
5. OAK leaves: as BLACK (D46C) every OAK object (picture 3) in OAK'S LAB is removed (lab93, 7:7F71 -> lab93 -> v86's lab86); PALLET TOWN's outdoor OAK is hidden too (pal93, Pallet script far call 6:6D73).
   (After the League the old lab59 still empties the whole lab.)
6. Route 22: GHOST acquired (D451) and all eight badges (D356 = FF) also switch the rival's "wants a battle" flag off (like shock / hero mode / BLACK did before): no BLUE on the BLACK TAMER path (gate86, 14:6B60, rewritten in place).
Tests: t101_v93.py ritual (HUD, silent death, silent catch, speakers back) / control (an ordinary trainer's faint still plays) / climax (no "Go! RED!", no send-out sound) / oak / gate.
run_v93.sh = run_v92.sh + t101.  t85 climax has pre-existing timing FAILs on v92 as well (RIT is already 7 when it checks for 5).
