Creepy Black — Mu Overhaul v15: BLUE at Nugget Bridge and the killer, BILL's soul-tribe story
============================================================================================

ROM:     Creepy_Black_Mu_v15.gb
SHA-256: 174e9328c2f56f25d39e5a03b30c28659fdeec6eeef515ecffca6c2eb55d77b3
Input:   Creepy_Black_Mu_v14.gb. build_v15.py (patchlib) asserts every byte it replaces; manifest_v15.json logs them.
Test ROM: Creepy_Black_Mu_v15_test.gb (build_v15_test.py) = v15 + the built-in "just got the POKeDEX" save
         (CONTINUE on an empty cartridge; NEW GAME and existing saves untouched).

1. BLUE AT NUGGET BRIDGE (Cerulean City, GHOST route)
   Cerulean text 1 (BLUE's before/after-battle text) goes through a wrapper (6:7500 -> 2E:5400).
   - At least one murder (D453) and BLUE not in shock mode -> his opening line becomes:
       "Hey! Have you heard? Some trainer is going around killing people and POKeMON too!
        The POLICE can't catch him. If he came for you, could you defend yourself?
        Let me test you! Show me you're ready!"
   - GHOST kills his team in this battle -> shock mode starts here (the v12 rule: first CURSE on his team
     before the Tower). After the battle, instead of his BILL chat:
       "... My POKeMON... They're dead... That GHOST of yours killed them!
        Wait... You... Are YOU the killer!? Stay away from me!"
     (without a murder the same grief line, minus the killer question)
   - Won without GHOST (murder route) -> "Hmph! You really have gotten stronger. But don't get cocky!
     Watch your back, and keep an eye out for that killer... and whatever else is out there!",
     then his usual "I went to BILL's..." text.
   - No murder and no GHOST: original lines.

2. BILL'S STORY
   Right after BILL hands over the S.S. TICKET (and his usual S.S. ANNE line), once:
     "Say... Can I tell you something odd? Long before the LEAGUE, KANTO had an old tribe. They believed
      the souls of people and POKeMON could be caught and bent to their will. Their descendants are said
      to have settled in LAVENDER TOWN. I've been testing their old ideas with science! My teleporter
      turns POKeMON into data... So what is a soul? Maybe just data, too... I learned a lot of this from
      my mentor, PROF.OAK."
   Later talks show his normal line only. (Bill's house text 2 -> wrapper at 7:7840 that runs his
   original script and then the story.) For every route.

3. FIX (bug since v12): shock mode was meant to skip the Cerulean BLUE battle but set D75B bit 7, which in
   this ROM is "beat the Cerulean Rocket thief" (his trigger at 6:54C8). So BLUE still appeared at
   Cerulean and the Rocket thief's battle was switched off. BLUE's real flag is D75A bit 0 (his trigger
   at 6:54F7 and text 1). Shock mode now sets D75A bit 0 and leaves the thief alone.
   Note: a v12-v14 save already in shock mode keeps the thief flag it got.

VERIFIED IN PYBOY (t30_v15.py, run_v15.sh)
   cer_curse: killer pre-battle text, GHOST kills his team, shock mode (D463 = 1, S.S. Anne skipped, Route 22
   flag clear), "Are YOU the killer!?", no BILL chat. cer_curse_nomurder: grief line without the killer
   question. cer_win: killer pre-battle text, "gotten stronger" + usual BILL chat, mode stays 0.
   cer_normal: original lines. cer_shock_skip: no BLUE at Cerulean in shock mode. bill: real cell-separator
   scene, S.S. TICKET, story once after the S.S. ANNE line, second talk normal. t25 (Tower) now checks
   D75A.0 set and the thief flag untouched. t29 on the test ROM.
