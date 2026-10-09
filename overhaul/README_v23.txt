Creepy Black — Mu Overhaul v23: MR. MU's last talk and the ritual battle
=======================================================================

ROM:      Creepy_Black_Mu_v23.gb
SHA-256:  04fb2d3cdb63ffe4cb3b9776da5bb12d6426d58393833d0158250e4aeadcd4d0
Input:    Creepy_Black_Mu_v22.gb. build_v23.py (patchlib) asserts every byte it replaces; manifest_v23.json logs them.
Test ROMs: Creepy_Black_Mu_v23_test.gb (built-in "just got the POKeDEX" save) and Creepy_Black_Mu_v23_chamber_test.gb
           (test-only save on Tower 7F at AGATHA stage 5, door open: walk up the stairs and talk to MR. MU).

THE TALK (TOWER CHAMBER, MR. MU in the centre)
  MR. MU: we meet again, for the last time; sorry for following and testing you; the successor search was no lie;
  he had to be sure you were worthy; he has watched you longer than you know... "it would be more fitting to say
  that I gave birth to you" (no more said); the LAVENDER people, the BLACK TAMER chosen in each age; he was a
  candidate but failed the transformation, believing he was unworthy and could not accept death; you have that
  resolve and will lead humanity beyond death; it was never his destiny and he can now accept his end gladly;
  the MIRAGE that stalks you is his missing half, he has no hold over it; to draw it into the ritual circle you
  must kill him; it will be more restless than ever and seek a replacement; you will know what to do.
  "AGATHA kept the vessel for this night. Take it." -> <PLAYER> received the MASTER BALL!
  (AGATHA took the MASTER BALL at quest stage 2; MR. MU gives it back here.)
  Question: "Is there life after death?" YES -> "Then perhaps we will meet again." NO -> "Then this is truly
  goodbye." Either way: "That was no test. There is no right answer. I only wished to know." The answer changes
  nothing. "End me with your own hands!" -> battle.
  Before the talk: with 20 item kinds in the bag, or a full party AND a full PC box, MR. MU asks you to make room
  and nothing happens.

THE BATTLE
  "MR. MU wants to fight!" (trainer class 27, unused CHIEF, renamed MR. MU, GENTLEMAN picture).
  Your party is put aside; you fight alone as YOU (the player stand-in, Lv50, 200 HP) with STRUGGLE only.
  - PKMN / ITEM / RUN: "MR. MU: No! You must kill me with your own hands!"
  - MR. MU never attacks ("MR. MU doesn't fight back."). STRUGGLE's recoil hurts you (about 50 HP in 4 turns),
    never enough to lose. No EXP.
  - "MR. MU died with a smile..." -> "The circle trembles... The MIRAGE appeared!" ????? (Lv50, the RED+GHOST
    fusion picture from red_ghost_fusion.py) comes out. Now FIGHT / PKMN / RUN and every item but the MASTER BALL:
    "It can't be harmed... Only the MASTER BALL can hold it!" ????? never attacks ("????? stares at you...").
  - MASTER BALL: the ball turns pure black when it catches ?????, "All right! ????? was caught!" (no POKeDEX page,
    no nickname question). The battle ends.
AFTER
  Your party comes back exactly as it was and ????? joins it (or the current PC box if the party is full), named
  ?????, with the player as OT. The MASTER BALL is used up. MR. MU is a gravestone in the centre (kill index 33),
  silent like every gravestone; the ritual can't start again.
  ????? for now: GHOST/GHOST, base 60/65/60/110/130, NIGHT SHADE, CONFUSE RAY, HYPNOSIS, DREAM EATER (placeholders).

TECHNICAL
- New saved RAM: D467 ritual (0 -, 1 MR. MU battle, 2 MIRAGE phase, 3 done). Temps D468/D469 (battle hooks only).
- Party swap: the whole party block D163-D2F6 goes to SRAM bank 1 B600 (unused: the save layout ends at B523); the
  catch is copied to B800 before the party comes back (chamber map script, first run after the battle).
- Species 20 = MR. MU (pic = GENTLEMAN trainer pic copied to A:7EFC), 7A = ????? (front/back in 2D:41C0, the bank
  choice in UncompressMonSprite 0:1659 rewritten one case denser to add 7A -> 2D). Headers from a new GetMonHeader
  exit routine (E:7DE0, falls through to the v3 one). Both use dex slot 152 like GHOST (outside the 151 entries).
- Battle hooks: bank F only had small gaps left, so each hook is a 5-8 byte stub (7E0D, 7E41, 7E78, 7FB2) that jumps
  into one shared far call to bank 2E (2E:5820). The 2E routine can redirect the battle by rewriting the hooked
  return address ([sp+6]): menu F:5000, SelectEnemyMove F:5629, enemy-fainted text F:4603, sent-out text F:4A65,
  UseBagItem F:50DF, ExecuteEnemyMove F:6792. GainExperience 15:524F is skipped in the battle.
- The MIRAGE phase marks the battle as wild (D057 = 1) so the MASTER BALL can be thrown; dex slot 152 is marked owned
  so no POKeDEX page follows. Predef 08 (MoveAnimation) -> bank 1 wrapper: after the toss animation that caught ?????
  OBP0/OBP1 = FF (black ball). Predef 4F (AskName) -> wrapper: ????? uses AskName's own GHOST path (no nickname).
- Gravestone list moved to 2E:5F00 with MR. MU added (chamber object 1, kill index 33 = D4A8 bit 1).
- 2E:6000-67FF stays free for the test ROMs' built-in save.

VERIFIED IN PYBOY (t34_v23.py, run_v23.sh)
- ritual: the whole talk (all key lines, the MASTER BALL handed over, YES), battle vs MR. MU with YOU alone,
  PKMN/ITEM/RUN refused, 4 STRUGGLE turns, MR. MU never attacked, died (kill bit), no EXP; the MIRAGE ?????
  appeared; FIGHT/PKMN/RUN/POTION refused; MASTER BALL caught it with OBP0 = FF at "was caught", no nickname
  prompt; party back unchanged + ????? (nickname ?????), MASTER BALL gone, MR. MU's object is the gravestone
  sprite, talking to it does nothing and the battle can't restart.
- no: answering NO gives the "goodbye" line and the same battle.
- partyfull: party of 6 -> ????? goes to the PC box, the party comes back unchanged.
- bagfull / boxfull: MR. MU asks to make room, no battle, bag/party unchanged.
- wild (normal case): a wild catch with a MASTER BALL still shows the POKeDEX page and asks for a nickname, and the
  ball keeps its normal palette.
- Static: run_checks.sh (79 hooks, 0 problems). Full run_v23.sh: every earlier suite passes on v23 (t33 chamber now
  skips the old v19 MR. MU line; his talk is t34's job).
NOT DONE YET
- The random Mirage encounters (trainer class 13 "?????") still use v11's blacked-out GENTLEMAN picture: trainer
  pics must live in bank 13, which is full. ????? the caught Pokemon uses the fusion pictures.
- What ????? does after the ritual (moves, story) is up to the next chapter.
