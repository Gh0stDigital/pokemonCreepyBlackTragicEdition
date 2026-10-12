Creepy Black Mu v46 (on v45): seven changes.

SHA-256: ad8f26d1a867508a7ec7d08066fbb8b6371bea253d3e43de1fe684558995d6f2

Pictures: qa_ref/v46_changes.png (BLACK already out at battle start, the BANE ball in battle, the ball on the map).

1. AGATHA's shell line no longer says her people drew its mark: "Feel its energy? It binds the hearts of those who
   truly love." (same place in the consort text, 2E:722F, same length).
2. BLACK leading at the start of a battle is simply there: the trainer picture (BLACK) does not slide away, no
   "Go! BLACK!", no send-out animation or cry; the HUD appears and the menu is ready. A normal lead, and switching
   BLACK in later, work as before.
3. BANE in battle: the black POKe BALL is the POKe BALL of the throw animation (1E anim tiles 06/07/16/17), fully black,
   lying where the POKeMON was (7x7 tiles at 2F:430C).
4. BANE on the map: the ball is the item POKe BALL sprite (4:5140), fully black, still its own sprite 47 (2F:5159; v43's
   slot handling unchanged).
5. GHOST consuming the MIRAGE grows to Lv100 at once (experience, level, stats, full HP): "GHOST consumed the MIRAGE!
   GHOST grew to level 100!".
6. CONSUME: taking a move is optional. B at "Take which move?" or giving up in the forget-a-move dialogue consumes the
   POKeMON anyway (experience gained, no move).
7. POKeMON LEAGUE gates as BLACK: the Route 22 gate and the Route 23 badge checks never stop BLACK and show no badge
   text; talking to a guard: "The guard is shaking... G-go ahead... I won't stop you!". Not BLACK: unchanged.

Technical:
- 2: F:41D4 (slide trainer pic) -> call F:7FB8 -> 2F pre46 (hl = $C405; BLACK lead: skip to 41DC, flag D45A);
  SendOutMon's message far call F:4CBC -> 2F msg46 (flag: HUDs, LoadMonBackPic, SendOutMon's battle setup, the picture
  drawn at once through AnimateSendingOutMon's out-of-battle path like YOU, then back at F:4D1F; else the message).
- 5: 2D:45FA (.nom, consume text) -> 2D:7EC0 -> 2F lv100 (GetMonHeader, CalcExperience 16:4F6A, CalcStats); the consume
  text's TX_FAR (18:6EAC) points to the new text in 2F.
- 6: 2F:542C call pick_move / and a / ret z -> call pick46 / jr z,.learned; 2F:548A ret -> nop.
- 7: Route 23 script table 14:5213 entry 0 and Route 22 gate script table 7:66AE entry 0 -> BLACK: return; Route 23
  guards' badge routine 14:5346 and the gate's text 1 (7:66EF) -> scared line as BLACK.
- Tests: t54_v46.py (start, ball, lv100, gates, agatha). t47's dark-pixel ball check kept for v39-v45; t49 refuse now
  expects "B = consumed without a move" from v46 on. run_v46.sh = run_v45.sh + t54.
Static: check_hooks.py 120 hooks, 0 problems.
