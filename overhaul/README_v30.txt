Creepy Black Mu v30 (on v29): GHOST's hunger warns you, and it eats the Pokemon next to it.

Steps left until GHOST feeds = 6 x hunger - step counter (the v2 engine: 1 hunger every 6 steps, feeds at 0).
At exactly these step counts a message pops up while walking:
  100  "GHOST seems to be getting restless..."
   50  "<victim> seems anxious about something."   (the Pokemon it will eat; the player's name if it will eat you)
   25  "You sense a malicious intent..."
Victim: the party member right in front of GHOST (the slot above it); if GHOST leads, the one just below it.
GHOST alone: it eats the player - black screen, GENGAR's cry (was GHOST's), save erased, back to the title screen.
GHOST not in the party (deposited for a MIRAGE fight): the old rule, the last member.
Unchanged: drain, feeding, hunger 12 after a meal, the engine is off for BLACK.

Code: hunger2 (2D:5E00) replaces the v2 engine (2E:4100) through v25's hunger_wrap; the messages are DisplayTextID text
ids F1-F3, printed by npc_talk2 (DisplayTextID's init far call, then v28's npc_talk).
Tests: t39_v30.py warn (100/99/50/51/25) / eat (slot in front, GHOST leading) / player (GENGAR cry, restart, SRAM erased).
