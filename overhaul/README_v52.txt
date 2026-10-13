Creepy Black Mu v52 (on v51): where MR. MU is, and the AMBER -> AZHI awakening at the POKeMON MANSION.

SHA-256: 2b8504acada31972aa6c6e5721da3a7d55af48bfcdd7b0e1f8c8932b2825918c

1. Cerulean (DOME FOSSIL -> PRETA): MR. MU is gone from the trade house for good once the DOME FOSSIL can't reach him, i.e.
   AGATHA took it (quest stage 2+ before PRETA was awakened) or a KABUTO was revived at the CINNABAR lab.
2. Mansion (OLD AMBER -> AZHI): the same rule for the OLD AMBER (AGATHA took it, or an AERODACTYL was revived at the lab).
3. MR. MU is at the POKeMON MANSION only after he awakened the DOME FOSSIL and left Cerulean (D460 = 3), and until he
   awakened the AMBER (D460 = 4 = gone).
4. New: the Mansion MR. MU awakens the OLD AMBER like the DOME FOSSIL: "OLD AMBER! ... If the dead could speak... do you
   believe they would ask to return?" THEY WOULD NOT = nothing happens (ask again any time); THEY WOULD = black screen, the
   jingle, "RED received AZHI!" - AZHI Lv35, perfect DVs, BLACK FLAME / FLY / DRAGON RAGE / SKY ATTACK, joins the party
   (party full: "make room"). v50's ritual raises it to Lv50 (it counts as an owned AZHI). No AZHI in the POKeDEX (v14).

Technical: bank 30:4800 cer52 / man52 (visibility, z = show) and mu52 (the talk, TX_ASM); Cerulean script 7:7600 and Mansion
script (11:7500, header +7) call them through a far call; Mansion text entry 4 -> 11:text52 (TX_ASM stub). AZHI struct (Lv35)
and give_azhi (v38 add_mon) in 2D:7FA0. The jingle wait is bounded (the Mansion's audio never reported it finished).
Tests: t60_v52.py cerulean, mansion, azhi. run_v52.sh = run_v51.sh + t60. Static: check_hooks.py 136 hooks, 0 problems.
