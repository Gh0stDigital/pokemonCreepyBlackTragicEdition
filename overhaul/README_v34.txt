Creepy Black Mu v34 (on v33): cursed trainers turn into gravestones right away; the scripted grunts can be killed.

1. A killed trainer is a gravestone right after the battle. Before, the kill was recorded but the trainer kept standing
   until you left the map and came back (the base game only checks gravestones when a map loads) - very visible from
   CERULEAN on (gym trainers, NUGGET BRIDGE). Now, after every real battle (home stub 0:00C0, carry = a battle took
   place), post3 (2D) runs the gravestone pass 3:4E85 and reloads the map sprites' tiles (5:785B).
2. Scripted trainers (battle started by a map script, not TalkToTrainer) had no kill index and inherited the index of
   the last trainer talked to: the NUGGET BRIDGE Rocket after its five trainers was never killed, an already dead
   trainer was "killed" again instead. The trainer phase (F:46EC -> v18 check at F:7DCC, now a far call to phase2)
   looks the battle up by (map, opponent, trainer no.):
     CERULEAN Rocket thief $1FC, NUGGET BRIDGE Rocket $1FD, MT. MOON B2F Super Nerd $1FE, GAME CORNER Rocket $1FF
       (the last free bits of D430-D44F) -> killable, gravestone (map table rebuilt at 2D:7180);
     CINNABAR GYM quiz trainers, GIOVANNI in the Rocket hideout -> 0: "But, it failed!" (no stale kill).
   Everything else keeps the index TalkToTrainer / the v14 leader engage set. v18's rule (no trainer phase for
   GIOVANNI at SILPH 11F) is unchanged.
Tests: t43_v34.py instant 23 / 41 / 33 (NUGGET BRIDGE, CERULEAN GYM trainer, VIRIDIAN FOREST: gravestone right after
the battle, others untouched). The full CERULEAN flow (BLUE, then the bridge with every trainer by sight and CURSE) was
played in the emulator: the Rocket got $1FD and all six bridge kills were gravestones (qa_ref/v34_instant_graves.png).
