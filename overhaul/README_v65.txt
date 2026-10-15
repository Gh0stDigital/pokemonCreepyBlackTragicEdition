Creepy Black Mu v65 (from v64): MR. MU's first meeting in PALLET TOWN, reworked
SHA-256 6d89bbd8beff2f41476ea1f2452d29ef5b76947f19eadfa0e97117ee60a280ea

- Leaving the house (first step outside, D454 = 0, player y >= 6) starts the meeting by itself: the player is frozen (MoveSprite's D730 bit 0 while he walks,
  wJoyIgnore before) until MR. MU has walked up (2 steps left from x8 to x6, facing the player) and finished his talk. Spamming the D-pad does nothing (t73).
- New speech, no name: "Hello young lad. Sorry to intrude on you so suddenly..." / "But I couldn't help but notice..." / "You are about to start a journey as a
  TRAINER, right?" / "You certainly have the look about you." / "I was wondering if you could humor an old man's question." - then the question and the
  THE TRAINER / THE POKeMON menu exactly as before (D450 = answer; "I see. Remember your answer." on a second talk). Far text in bank 31 6200; the old
  text slot in bank 6 (6967) is now a TX_FAR stub. (The user's wording had typos; "I just was wondering" became "I was wondering" so it fits four lines.)
- Afterwards he stands at his post (6,6) until the player enters another building or leaves town (bank 2E mapload: D454 2 -> 3, as before). Then he is gone
  for good: picture 0 and position FF every frame, and his object is off the map in the object data (y/x = FF), so no sprite is left anywhere in PALLET.
  The script puts him on the map only for the meeting (pal65 place) and, if a save is loaded while he waits (state 2), back at his post.
- The Pallet map script body (bank 6 6D72-6DE9) is replaced by a far call to bank 31 pal65 + the old tail (bit 4 of D74B, jp 4E60); the shamaness (object 5)
  is still hidden once GHOST is acquired (that code moved into pal65). GHOST route: answering THE TRAINER still gives GHOST after the first rival battle and MR. MU
  still turns up in the CERULEAN house later (v6 code untouched).
- Tests: t73_v65.py intro (meeting by itself, frozen player, new speech, no name, menu, answer saved, he waits, loaded-save case, building -> gone for good).
  run_v65.sh = run_v64.sh + t73. The early chain (t1, t2 both answers, t_sprites, t3, t4, t17 Cerulean MU) was re-run on v65; the full v54-v64 regressions are still outstanding.
