Creepy Black — Mu Overhaul v18: SILPH CO. on the GHOST route
============================================================

ROM:      Creepy_Black_Mu_v18.gb
SHA-256:  7bbcd9bf11620d3439fa2159befb987cd4100b7bb2f620d856bcb1d8ef8d51c8
Input:    Creepy_Black_Mu_v17.gb. build_v18.py (patchlib) asserts every byte it replaces; manifest_v18.json logs them.
Test ROM: Creepy_Black_Mu_v18_test.gb (build_v18_test.py) = v18 + the built-in "just got the POKeDEX" save.

All of this is GHOST route only (GHOST owned, D451); off the route SILPH CO. and the hideout are unchanged.

1. Reaching Pokemon Tower 7F (where FUJI is held) the first time:
   - the Saffron gate guards let you through (their drink flag D728.6), so SILPH CO. can be entered right away;
   - GIOVANNI leaves the Rocket Hideout under the Game Corner (beaten flag D81B.7 + his object hidden, toggle 83),
     and the SILPH SCOPE item ball he would have dropped is shown there (toggle 87), as after beating him.
     If the hideout was already cleared nothing there changes.
2. GIOVANNI at SILPH CO. 11F
   - before the battle: "So, <PLAYER>... I have been watching you for some time. I thought of making you one of us.
     You had talent. And you had that weapon. But the damage you have done... No. You can't be controlled.
     I will simply take the weapon for myself!"
   - defeat line in battle: "GIOVANNI: Damn that cult...!" (also when CURSE killed his POKeMON, instead of the
     frightened text)
   - no trainer phase after the win (the CURSE-the-trainer step) even with GHOST out: the battle just ends.
   - after the battle: "Hmph. You think you're in control? Fool. There are forces at work you can't even
     understand. They're using you, <PLAYER>. I must go... but we will meet again!" Then he leaves and ROCKET
     clears out as usual.
3. The PRESIDENT: "You saved us all! Those ROCKETs were after our MASTER BALL. It was the finest work of an old
   friend of mine. He was a genius. Then one day, he just vanished... I can't think of anyone better to have it.
   Take it." Then the MASTER BALL as usual.

VERIFIED IN PYBOY (t32_v18.py, run_v18.sh)
  unlock: gates/hideout flags set on the GHOST route only, scope ball untouched if the hideout was done; hideout
  B4F's toggle list maps GIOVANNI to the hidden toggle 83. giovanni: speech, battle with GHOST + CURSE ->
  cult line, no trainer phase, warning, he leaves, PRESIDENT story + MASTER BALL. normal: off the route, the
  original texts and the usual MASTER BALL line.
