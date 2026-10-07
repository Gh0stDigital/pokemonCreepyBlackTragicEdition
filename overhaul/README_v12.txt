Creepy Black — Mu Overhaul v12: rival BLUE on the GHOST route
==============================================================

ROM:     Creepy_Black_Mu_v12.gb
SHA-256: fc69b434678ec34ddb41073fccbfe30eb30029b347036539c528545f8d24d5c8
Input:   Creepy_Black_Mu_v11.gb. build_v12.py asserts every byte it replaces; manifest_v12.json logs them.
Dialogue: dialogue_v12.json.

NEW SAVED RAM: D463 rival mode — 0 normal, 1 shock, 2 hero.

RULES
-----
1. CURSE can't kill BLUE (classes RIVAL1/RIVAL2) — only the Champion (RIVAL3) is excepted.
   CURSE still kills his POKéMON as usual. In the base game's after-win "curse the trainer"
   phase, using CURSE on BLUE now shows "GHOST hesitates..." / "BLUE ran away!" and the battle ends
   (no murder flag, no gravestone). Before, scripted trainers like BLUE just got "But, it failed!"
   in a loop.
2. When CURSE was used in a battle with BLUE (RIVAL1/RIVAL2), his defeat text is
   "My POKéMON... They... died!? / What did you do to them!?" (bank 6, like the v2 frightened texts).
   This also applies at Silph Co (the brief said "before Silph Co"; easy to change).
3. Shock mode: the first such battle on the GHOST route while the Pokémon Tower rival is not yet
   beaten sets D463 = 1. It also turns off the encounters in between:
   - Cerulean: EVENT_BEAT_CERULEAN_RIVAL set.
   - S.S. Anne: its 2F script is set to "done".
   - Route 22: the "rival wants a battle" flag is cleared.
   - Pokémon Tower 2F in shock mode:
     - Before the battle: grief text ("My POKéMON... That thing of yours killed them... I came here to
       mourn them. And you show up with that monster!? I won't let you get away with it!").
     - After the battle: "You bastard! I'll never forgive you!", then he leaves.
     - If the first CURSE happens in the Tower battle itself, shock mode starts there and the
       after-battle text is already the "bastard" one.
4. Silph Co 7F on the GHOST route:
   - In shock mode: "That creature you carry is dangerous. It killed my POKéMON... This time I'll
     avenge them!"
   - Otherwise: "TEAM ROCKET told me everything. You carry a dangerous POKéMON weapon. It has to
     be destroyed!"
5. Hero mode: winning the Silph Co battle on the GHOST route sets D463 = 2.
   - Route 22's second rival battle never triggers (its "wants a battle" flag is cleared on entry).
   - Champion: the trainer number is moved to 4-6, which are copies of his three Champion teams
     with the Lv65 starter ace replaced by Lv70 MEWTWO.

VERIFIED IN PYBOY (t25_blue.py, run_v12.sh)
-------------------------------------------
- Tower, CURSE on his team:
  - "My POKéMON... They... died!?", "GHOST hesitates...", "BLUE ran away!", "You bastard!".
  - Murder flag 0 and no gravestones.
  - D463 = 1; Cerulean event set, S.S. Anne script 4, Route 22 flag cleared.
- Tower with shock from an earlier battle: grief pre-battle text, then the battle. Without shock:
  the normal "What brings you here?" text.
- Silph Co, no shock: "TEAM ROCKET told me everything..." text.
- Silph Co, shock: avenge text; won with CURSE (hesitates, ran away); D463 = 2.
- Route 22 in hero mode: the rival flag is cleared on entry.
- Champion in hero mode: trainer no. 4, party PIDGEOT/ALAKAZAM/RHYDON/GYARADOS/ARCANINE + Lv70 MEWTWO.

NOTES / OPEN QUESTIONS
----------------------
- Champion + CURSE behaves as in the base game: his POKéMON die, the frightened text plays, and
  CURSE on him in the trainer phase counts as a murder (D453 = 1). The Champion room script then
  continues normally ("Why did I lose?...") as if he were alive.
- After Silph Co, BLUE's normal after-battle line ("I'm moving on up...") still plays.
