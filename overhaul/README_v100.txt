Creepy Black Mu v100 (on v99): the consort needs BADGES
SHA-256: a2d7f8b1656f4c8b4c0eccc216b1ceba8cc96a06a6df4a4cb61ef61ae6a0d600

AGATHA's stage 4 (the HELIX FOSSIL for the one you love): when the player answers YES to "Give <NAME> the HELIX FOSSIL?"
the girl first checks the BADGES (count of D356 bits):
  ERIKA 4 BADGES, MISTY 6, SABRINA all 8.
Too few: she can't just be seen with anyone, only with a strong trainer who has proven their abilities, and names the
BADGES she wants ("Come back when you have six BADGES!" / "Perhaps when you have four BADGES..." / "Return to me with all
eight BADGES."). She takes nothing: the player keeps the shell, the quest stays at stage 4 and she can be asked again.
Enough BADGES: her v16 reply, she takes the shell and joins (stage 5), as before.

Code: bank 2E:7D00 (badge count + one stub per girl + texts); the stubs replace "ld a,HELIX / call remove_item" at the
start of v16's join_MISTY (2E:69E0) / join_ERIKA (2E:6A23) / join_SABRINA (2E:6A66); on a refusal the stub drops the
return address and prints her line, so the join text and the stage/consort writes are skipped.

Test: t105_v100.py MISTY / ERIKA / SABRINA (one BADGE short = refusal, shell kept; exactly enough = joins, control).
t31_v16.py full now gives the player six BADGES before MISTY (VERSION >= 100).
