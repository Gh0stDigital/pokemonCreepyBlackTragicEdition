Creepy Black Mu v35 (on v34): trainers killed with CURSE vanish from the map right away again - from CERULEAN on too.

The real bug: every frame the overworld sprite code (1:50AA) asks predef 0x12 (hidden object?) and predef 0x13
(killed trainer?) whether to draw a sprite. Predef 0x13 is the base hack's 3:4DFB, which only knows the base kill list
(D486, built from the early-route table at map load). So trainers up to MT. MOON vanished the moment CURSE killed them,
while every trainer that only got a kill index in v29 (NUGGET BRIDGE, CERULEAN GYM and everything after) kept standing
until the map was reloaded.
Fix: predef 0x13 -> killed13 (2D:6200): the base check, then - if the sprite is not a gravestone already - the v29/v34
trainer table and the v28 NPC kill list (kill_chk2). Killed = not drawn, like the early trainers; on the next map load
the trainer is a gravestone (unchanged).
v34's extra gravestone pass right after every battle is removed again (after-battle stub 0:00C5 -> v31's post2): the
base game's "vanish now, gravestone when you come back" applies to every trainer. v34's scripted-grunt kill indices stay.
Tests: t44_v35.py vanish 23 / 41 / 33 - right after the battle the killed trainer is not drawn (image FF), a living
trainer next to the player still is, and after re-entering the map the killed one is a gravestone.
Regression (run_v35.sh, v33 suite + t44): PASS=251 FAIL=0. Creepy_Black_Mu_v35_mysave2_test.gb = v35 + the user's second save (Creepy_Black_Mu_user2.sav: Cerulean, BOULDERBADGE, GHOST).
