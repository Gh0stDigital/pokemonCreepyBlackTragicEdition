Creepy Black Mu v89 (on v88): ROUTE 22 - the early rival fight (BLUE)
SHA-256 c65fefc4232baeec861e26d91fef50cfcd59b713cce9aa1e320a8f32b14e6def

The optional first rival fight on ROUTE 22 (opponent E1 = RIVAL1, after the POKeDEX, before the first gym), GHOST route:
- Shock flags and GHOST's hesitation already worked there (v12's hooks are class-wide) - now covered by a test (t97 curse): CURSE in this fight = "GHOST hesitates...", "BLUE ran away!", no murder,
  shock mode (D463 = 1, Cerulean skipped (D75A bit 0), S.S. ANNE script 4, the second ROUTE 22 fight switched off).
- New: after he runs away he no longer gives his ordinary speech ("I heard POKeMON LEAGUE has many tough trainers...") when CURSE was used in the battle (D452):
  "What was that?!" / "My POKeMON... They went limp." / "That thing of yours isn't a POKeMON, is it?!" / "Stay away from me! I'm telling GRAMPS!"
  A normal win (no CURSE) keeps the original speech.
- Code: bank 14:6BA0 r22a89 = the ROUTE 22 text-1 chooser (pre-battle as before; after the battle: shock text if D452, else the original at 14:51B2), map text table entry 14:5175.
Tests: t97_v89.py curse win. run_v89.sh = run_v88.sh + t97.
