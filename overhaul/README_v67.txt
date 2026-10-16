Creepy Black Mu v67 (from v66): SHOCK MODE for the gyms
SHA-256 d8ff15fe722ac08f8531e5db60f8877ee1c57f1e72cb3cebe8e1f90224bb310e

1. SHOCK. A gym trainer killed with CURSE puts the whole gym into shock (D839 bit g: 0 PEWTER, 1 CERULEAN, 2 VERMILION, 3 CELADON, 4 FUCHSIA, 5 SAFFRON, 6 CINNABAR
   (its quiz trainers can't be killed), 7 VIRIDIAN). While the LEADER is alive:
   - gym trainers who haven't fought yet say a new line before the battle (three variants: "What did you do to our teammate?! I'll avenge them!" /
     "You killed one of us! MURDERER! ..." / "Our friend is dead because of YOU! ..."), then fight;
   - gym trainers already beaten tell you to get out ("MURDERER! Get out of our gym!" / "Our teammate is dead... Leave!" / "I can't even look at you! GO!");
   - the LEADER has his / her own line for the dead student (BROCK, MISTY, LT.SURGE, ERIKA, KOGA, SABRINA, BLAINE, GIOVANNI), printed instead of the usual speech.
   If the LEADER is dead, v14's revenge line keeps priority (unchanged).
2. SULK. A gym trainer you beat while using CURSE on their POKeMON but spared (RUN in the trainer phase) tells you, when talked to again, "You are evil... Just leave." (three
   variants). One bit per gym trainer in D83A-D83F (a gym trainer / leader table of 42 kill indices in bank 31). A normal win (no CURSE) leaves the usual after-battle text.
   Shock wins over sulk. (The leaders' after-battle scripts are untouched.)
3. ABANDONED GYMS. When the leader has been killed (kill bit) the next map that is not a gym arms the gym (D842 bit g); from then on every map load / redraw of that gym hides everybody
   but the grave (object 1): picture 0, position FF. During the visit of the kill nobody leaves (v14: the trainers still swear revenge).
- How: TalkToTrainer's before / after text calls (0:3234 and the new hook at 0:322C) go through the home stub at 0:00CE (v14's gym dispatcher, now: push hl, de / ld d,c / far call
  bank 31 rdisp / pop / ret c = printed here, jp nz,7A00 = v14's code, jp 3C94 = the original text). The trainer header lives in the map's bank, so rdisp gets "before / after" in D.
  EndTrainerBattle (0:32D9..32E2) far-calls r2 (set the trainer's flag as before, then shock / sulk bookkeeping; its final cp $C8 feeds the untouched jr nc). The leaders don't use
  TalkToTrainer: their pre-battle "ld hl,TEXT / call PrintText" (7 sites; CINNABAR can't be shocked) goes through a 13-byte stub in the gym's bank (TX_FAR to bank 31 when the shock bit is set).
  InitMapSprites' stub (5:7FD0) now calls im67 (the shamanesses, then gymhide / armall).
- Lessons: a routine in a switched bank must never write the MBC bank register itself (the next opcode comes from the new bank): v67's first build did and "worked" by luck while hiding
  MISTY. ReadTrainerHeaderInfo reads the header from whatever bank is mapped. Far-call stubs: Bankswitch clobbers a, b, c (and hl is the vehicle); d, e and the flags survive.
- Tests: t75_v67.py shock (CERULEAN: JR TRAINER killed -> D839, other trainer / beaten trainer / MISTY texts), sulk, normal, abandon, leaders (PEWTER both ways; the harness could not
  reach the other leaders), t28_v14.py misty_kill / misty_win / brock_kill (v14's revenge line still works; koga_kill's walk fails on v66 as well). run_v67.sh = run_v66.sh + t75.
