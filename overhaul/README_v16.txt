Creepy Black — Mu Overhaul v16: AGATHA's quest, part 1 (GHOST route)
====================================================================

ROM:      Creepy_Black_Mu_v16.gb
SHA-256:  5875e91e40856e454032edd9e4b06c7f988b5e4c60d6628425d2e7f4e74a9164
Input:    Creepy_Black_Mu_v15.gb. build_v16.py (patchlib) asserts every byte it replaces; manifest_v16.json logs them.
Test ROM: Creepy_Black_Mu_v16_test.gb (build_v16_test.py) = v16 + the built-in "just got the POKeDEX" save.

NEW SAVED RAM (cleared on NEW GAME): D464 quest stage (0 not started, 1 relics asked, 2 vessel asked, 3 GHOST power,
4 consort, 5 consort found) · D465 consort (1 MISTY, 2 ERIKA, 3 SABRINA) · D466 bit0 failed, bit1 AGATHA gone,
bit2 "you already woke some" said.

WHERE
  AGATHA stands left of MR. FUJI on Pokemon Tower 7F, only on the GHOST route (D451). The chosen girl stands on
  his right later. 7F got a new object list (AGATHA + MISTY/ERIKA/SABRINA), text table and a map script that hides
  whoever shouldn't be there. Her talk logic and all texts are in bank 2E (6800+; 6000-67FF stays free for the
  test-ROM save).

STAGES
  Before FUJI is rescued: "These ROCKET brats tied me up with old FUJI! Get rid of them, child!"
  1. After the rescue (walk back up to 7F): thanks, a pause, she senses the curse, the tribe and the accursed soul
     manipulators, the ritual, and three relics: "A shell coiled like a whirlpool, a dome-shaped shell from the deep
     sea, and a drop of old sap that holds the breath of the sky." (HELIX FOSSIL, DOME FOSSIL, OLD AMBER.)
     - DOME FOSSIL or PRETA counts for the dome; OLD AMBER or AZHI for the amber; the HELIX FOSSIL must be the fossil.
     - PRETA or AZHI owned: once, "You have already woken some of them... the ritual can still be done. Perhaps it
       is even better this way."
     - A fossil revived at the Cinnabar lab (OMANYTE, KABUTO or AERODACTYL owned in the POKeDEX): "Its soul is gone
       from the stone. Then there is nothing more I can do for you." Quest failed. Next talks: "So much of KANTO's
       old ways are lost... My ancestors must be weeping." Once you leave 7F she is gone for good (the League
       AGATHA is unchanged).
     - All three relics: she takes the fossil items (PRETA/AZHI stay with you).
  2. The vessel: a ball "that catches without fail", ROCKETs talked about SILPH CO.
     - MASTER BALL in the bag: "Let me keep it safe for you. Will you give it to AGATHA?" YES -> she keeps it.
       NO -> "Bring it to me when you are ready."
     - Got the MASTER BALL (D838.5) but it is in neither the bag nor the PC: "You used the vessel? ... There is
       nothing more I can do for you." Quest failed (same as above).
  3. GHOST below Lv100: too weak, could hide during the ritual; "Feed it only dangerous POKeMON or truly bad people."
  4. GHOST at Lv100: she gives the HELIX FOSSIL back (asks you to make room if the bag is full); its mark meant
     devotion to the one you love; give it to a girl you truly care for and bring her to LAVENDER TOWN.
     - MISTY, ERIKA and SABRINA all killed with CURSE: "You killed them all, didn't you? Then the ritual can never be
       finished." Quest failed.
  5. Talk to MISTY, ERIKA or SABRINA after beating her, with the HELIX FOSSIL: "Give <NAME> the HELIX FOSSIL?"
     YES -> her own reply, she takes it and leaves her gym; she waits beside AGATHA on Tower 7F (own line there).
     NO -> "You kept the HELIX FOSSIL." A killed girl is a gravestone and can't be asked. AGATHA then says
     "You have brought her. Good. Rest now. We will begin soon..." (placeholder for the next part).

VERIFIED IN PYBOY (t31_v16.py, run_v16.sh)
  hostage / noghost (AGATHA only on the GHOST route) · full (every stage through MISTY joining, MISTY gone from her gym,
  MISTY + AGATHA on 7F) · mu · labfail (+ gone after leaving) · ballfail · ballno · alldead · girl_normal (beaten MISTY
  before stage 4: usual line) · gyms (ERIKA/SABRINA/MISTY leave their gym only when chosen).
  Not played through: handing the shell to ERIKA or SABRINA (their gyms' tree/teleport puzzles block the test walker);
  their wrapper is the same generated code as MISTY's with their own addresses (build asserts each original text).

LIMITS / NOTES
  - "Fossil revived at the lab" is read from the POKeDEX owned flags; a fossil handed to the lab but not collected
    yet isn't seen until you collect it.
  - PRETA/AZHI are looked for in the party and the current PC box.
