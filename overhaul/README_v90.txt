Creepy Black Mu v90 (on v89): BROCK's dialogue after the fight matches what happened to him
SHA-256 8c4a4394321e4cb94f8cb8f9b20b4240413a0c0257ce3c8ef3546be279050a96

PEWTER GYM (map 36, bank 17):
- Killed (CURSE in the trainer phase): "<PLAYER> took the BOULDERBADGE from BROCK's body." (new text id 7, same wording as the other leaders) and TM34 goes into the bag silently.
  (The base game's kill gave the badge only, with no text and no TM.)
- Survived, but CURSE was used in the battle (D452): instead of the cheerful "Wait! Take this with you!" and the TM34 lecture, a shaken BROCK: "...Please. Take this and go." /
  "<PLAYER> received TM34!" / "It's BIDE... Now go. Please. Take that thing away from me!"
- Survived, no CURSE: the original lines.
- His later talks (the advice about CERULEAN): the shaken version "...You're the one everyone fears. Go to CERULEAN GYM. Please." while D452 or D453 (murder) is set, else the original.
- Code (bank 17): killchk89 7D80 (replaces the "killed?" far call at 43DF), adv89 (446C), text choosers t4_89 / t5_89, the text table copy tab_89 (header +5).
Tests: t98_v90.py kill spare win. run_v90.sh = run_v89.sh + t98.
