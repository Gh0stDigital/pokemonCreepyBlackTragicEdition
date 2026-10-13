Creepy Black Mu v51 (on v50): POKeMON TOWER rules and MR. MU's battle look.

SHA-256: ba7656647511a5906e865a1fbaa99596daa01f41f5f766271c8c62dcec21939b

1. GHOST won't fight in POKeMON TOWER (1F-7F, maps 8E-94). A GHOST leading the party stays in its ball at battle start and
   the first POKeMON that can fight goes out. Choosing GHOST when switching says "GHOST refuses your command!". If GHOST is the
   only one able to fight it comes out but every move says "GHOST refuses your command!" (the turn passes, nothing happens).
   Elsewhere GHOST fights as before.
2. As BLACK every town and route (maps 00-24) plays the LAVENDER TOWN music; buildings, caves, gyms ... keep their own.
3. MR. MU's battle (the ritual): no battle music; his picture stays in the battle frame - no slide away, no send-out
   animation or cry ("MR. MU stepped forward" stays, his HUD appears).

Technical (code in bank 30, the next empty bank - bank 2F is full):
- HasMonFainted F:4AC2 -> rst 08 ghost51 (z = can't be sent out: fainted / GHOST in the TOWER while another can fight);
  home 0x29 (before the player's move) -> pre51 (GHOST out in the TOWER: refuse text, back to F:58DB), else v48 pre48.
- Map music: 0:1249 (read of MapSongBanks on map load) -> music51: BLACK on maps < $25 reads the LAVENDER entry.
- MR. MU: PlayBattleMusic (2:50E3) -> 2:7FF4 mus51; EnemySendOutFirstMon F:496C (slide) and F:4A6B (picture/cry) -> slide51 / anim51.
- Tests: t59_v51.py lead, switch, only, music, mu. run_v51.sh = run_v50.sh + t59.
Static: check_hooks.py 136 hooks, 0 problems.
