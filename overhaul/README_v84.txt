Creepy Black Mu v84 (on v83): a batch of fixes.
SHA-256: b0124759a16851c0902e9cde21f24158bbed366cb4b2b2802f7b2ab308b8d244

1. SNORLAX: METAMORPHOSIS on a wild POKeMON now sets D452 (CURSE used this battle) like CURSE does, so v73's "SNORLAX returned to the mountains" text is skipped
   after ensnaring him (give84 replaces the call to `give` in bane_move, 2F:4052). Trainer fights were already covered by v83.
2. Item balls on the ground turning into the black POKe BALL: v43's ball_fix put the black ball into four-tile slot 0B ($8780) whenever another sprite (a gravestone,
   a boulder...) held slot 0C - but 0B is where EVERY outdoor set puts the item ball picture ($3D), so the item balls drew the black ball's tiles. ball84 asks which
   slots are really used by other sprites on the map and takes 0C, else 0B, else a free walker slot (the ball tiles written into its three standing frames).
3. DAMNATION: the enemy faints visibly again ("Enemy <MON> fainted!" + the faint animation) and the battle is won at once (the rest of the team has 0 HP, trainer phase /
   wild battle over); D452 is set so the trainer reacts like to a CURSE. dam84 (FaintEnemyPokemon prefix F:7D20) runs v45's kill45 (BLUE's replacement still sees the curse flag)
   and then clears the curse-kill flag CC39 for DAMNATION so the faint animation/text are not skipped.
4. BLACK switched in during a battle (after a faint or from the PKMN menu): no "Go! BLACK!", no ball, no cry - the back picture slides in from the left edge column by column
   (msg84 = v46's quiet send-out for the battle start + slide84 for later switch-ins). The battle start lead is unchanged (v46).
5. TOWER 7F after the ritual (RIT >= 6): the channelers are gone; AGATHA, MOM and the rest stay (ch84 hides objects 4-8 and 10-14 every frame after v54's ch54).
6. POKeMON LEAGUE as BLACK: the player's name is BLACK in the LORELEI / BRUNO / AGATHA / LANCE rooms (F5-F7, 71 = LANCE) - "BLACK defeated LORELEI!", "BLACK got ... for winning!" -
   and RED again everywhere else (the CHAMPION's room: BLUE keeps calling the player RED). name84 (end of the map-load chain, 2E:42B4): swaps D158 <-> BLACK, the real
   name is kept in D879-D883, D884 = swapped. BRUNO's speech says "BLACK! We will grind you down..." (was a literal RED).
7. MOON STONE: "The MOON STONE shatters!" (flash + text) now comes right after the last POKeMON is down (start of TrainerBattleVictory, F:46AB -> F:5046 -> 2F shat84), then the usual
   end of battle (BLACK defeated ..., her/his speech, money); the POKeMON out is then called back and BLACK slides in for the phase (ph44 no longer prints the shatter text).
8. FIX of a v80 side effect: v80's scared-trainer lines also replaced the League members' (and the CHAMPION's / SILPH 11F / hideout B4F bosses') speeches as BLACK
   (t63 failed on v80). rdisp84 (home stub 0:00CE) skips maps F5-F8, 71, 78, EB, CA.
Tests: t91_v84.py balls / free / snorlax / slide, t92_v84.py damn / damnwild / names / league / bruno; t87_v79 hall expects no channelers from v84. run_v84.sh = run_v83.sh + t91 + t92.
Technical: bank 2F:5C00 give84 / slotused / put64 / ball84 / dam84 / slide84 / msg84 / bane_add84 / shat84; bank 30:6F00 ch84, 30:6F80 BRUNO text; bank 31:5A80 rdisp84; bank 2E:5C00 name84;
F:5046 stub; patches: bank 5 init_w operand, 2F:50C3, 2F:4052, F:7D20 operand, F:4CBC operand, 18:tail53 operand, 0:00D2, 2E:42B4, F:46AB, ph44 nops.
Regression notes: t53_v45 tower hangs (no output within the timeout) on v83 as well - not caused by v84; t62_v54 mom now expects no channelers (v84). 170 hooks checked, 0 problems.
