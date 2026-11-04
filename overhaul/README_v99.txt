Creepy Black Mu v99 (on v98): CINNABAR GYM - quiz trainers die like everyone else, BLAINE knows who you are
SHA-256: 91f12bd1225367fe909e411886da0c694b71cf8d0bd6ca3bb6df1cd352b97dd2

1. Quiz trainers can be killed. The seven CINNABAR GYM quiz trainers (objects 2-8) are scripted fights (no trainer header), so CURSE
   used to fail on them. They now get kill indices $23B0-$23B6 in v34's phase-2 table (map A6), i.e. bits 0-6 of D886 (an unused
   saved event-flag byte, cleared by NEW GAME): the set/test routine 3:4DB9 now keeps the high byte and uses base D410
   ((idx>>3)+D410), so $23B0+n = D886 bit n. kill_chk2 (2D:6425) calls kc99 (2D:4C40), which reads that range; the gravestone table
   for map A6 (2D:7180+2*A6) points to gtA6. A killed quiz trainer vanishes at once (per-frame predef 0x13) and is a gravestone on
   the next visit, like any other NPC.
2. Quiz machines: quiz99 (7:6CE0, called from 7:6A36) - if the machine's trainer is dead the machine prints
   "ERROR! DESIGNATED TRAINER MISSING." and asks nothing (no gate, no battle). Machines of living trainers work as before.
3. BLAINE's shock speech: bl99 (1D:68C0, from 1D:58FD) - when any quiz trainer is dead (D886 & 7F) BLAINE is surprised but not
   shocked: he heard the rumors, OAK and FUJI's twisted project must have come together (text 32:7C00 shock99).
   Otherwise his usual speech.
4. BLAINE's lore: text 10 is now t10_99 - when he was beaten with CURSE (D452) and spared (kill bit D4A7.7 clear) he tells how FUJI
   and OAK worked together in the POKeMON MANSION (souls / pushing POKeMON), he burned what he could, and the MANSION holds secrets
   best left buried (32:7C00 lore99), then his usual badge text. A normal win: badge text only.

Test: t104_v99.py kill / spare / quiz / blaine / lore (each with a control case).
