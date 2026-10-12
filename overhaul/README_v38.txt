Creepy Black Mu v38 (on v37): the BLACK TAMER becomes a party member (part 1 of the BLACK TAMER mechanics).

SHA-256: c511ada7c0669642d7827b9034e4bf2ed2f786cae9f6807808d582f915dd7488

1. Evolution scene (end of the ritual): the animation now starts on RED's trainer picture and ends on the BLACK TAMER.
   RED's front picture (4:6F2A) is a hidden species 86 (header in bank E 7EB0, picture bank 4 via bank_for38, dex slot
   152 like BLACK - the front-picture loader refuses dex 0 and silently swapped in RHYDON, which crashed the scene).
2. Trainer card: the BLACK TAMER picture (2D:41C0) once the player is BLACK (4:74E6 -> 4:7B00).
3. End of the ritual (do_post -> black_join, 2D:7B00..): BLACK joins as party slot 1 - species 7F, Lv1, perfect DVs,
   stats of a Lv10 (43/30/28/30/40 = level 1 computed as level 10), OT = the player, moves: CURSE (placeholder until
   BANE, v39). PRETA (Lv50, v6's struct) and AZHI (Lv50, BLACK FLAME/FLY/DRAGON RAGE/FIRE BLAST, perfect DVs) join
   unless already owned (party or current box); a full party sends them to the current box.
4. BLACK's rules:
   - can't faint: the five "player mon fainted?" checks in bank F keep BLACK at 1 HP (and the battle goes on);
   - gains no battle experience (GainExperience skips it; it will only grow by consuming, v41);
   - no item works on it: the party menu of every item routine (stones, POTIONs/vitamins/RARE CANDY, PP items, TMs)
     answers "It won't have any effect." and cancels;
   - can't be stored (PC deposit: "BLACK can't be stored away.") or left at the Day Care ("BLACK won't leave your side.");
   - the Name Rater won't rename it ("That is a truly impeccable name!");
   - poison outside battle can't kill it (poison is cleared at 4 HP or less, every step while BLACK).
   Home far stubs: the unused bytes after the RST vectors (0x01-0x27; 0x09 = shared jp Bankswitch). No code executes RST.

Tests: t46_v38.py (join, owned, card, faint, exp, items, pc, daycare, poison; each with its normal case), t35 climax now
expects BLACK + CHARMANDER + PRETA + AZHI. run_v38.sh = run_v37.sh + t46. Static: check_hooks.py 107 hooks, 0 problems
(one reviewed operand misread at 2D:44C9).
Known (unchanged from before): in the Day Care menu the first party slot can't be picked (also on v37).
Regression (run_v38.sh = run_v37.sh + t46): PASS=292 FAIL=0.
