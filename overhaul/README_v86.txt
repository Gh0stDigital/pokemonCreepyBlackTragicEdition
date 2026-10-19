Creepy Black Mu v86 (on v85): Route 22 rival, no fanfares at the end, GHOST WALK scales, Hall of Fame / OAK'S LAB fixes
SHA-256 3247fc1665b96a56b3ec4f206ca86342b1cf76acaa7102a55800c9d7db341c92

1. Route 22 rival after the 8th badge: the v12 gate (shock / hero mode: no rival) also covers BLACK (D46C), bank 14:6B60 gate86 (map header script pointer 14:4007).
2. No victory fanfare after the LEAGUE (LORELEI, BRUNO, AGATHA, LANCE), BLUE the champion, and OAK / BILL (trainer classes 21 2C 2E 2F 2B 1A): bank 32 vict86 replaces
   v77's vict77 (F:46C6); the CHAMBER rule stays. The HALL OF FAME is silent for BLACK (music86, 0:1249 chain -> music77 first).
3. GHOST WALK (AB): power = 20 + level * 1.5 (BLACK's level, cap 250; Lv5 = 27, Lv50 = 95, Lv100 = 170) instead of a flat 90 (gpow86, F:5784 move-data far call; every other move unchanged).
4. BLUE's object is hidden the moment he is beaten (s3_86, 1D:7F80), before the walk into the HALL OF FAME. AGATHA keeps facing up in the Hall of Fame (hof86, 30:4500)
   (she was drawn with a side pose once the scene was over).
5. OAK'S LAB scientists (BLACK, after the League): a redraw (text / menu) handed the aide another picture's VRAM slot (he turned into BLUE): app86 (31:5AA0, before app75) gives
   the object list's pictures back before the sprite loader runs. After his speech (every talk) he asks "They are shaking. METAMORPHOSIS?" (aide86 via ext86, 7:7FE0):
   YES = v40's map METAMORPHOSIS on object 10 (black ball, POKeMON to pick up, lab86 leaves the ball alone); NO = nothing.
NOT REPRODUCED: "GHOST WALK text uses another move's text" (battle charge text, field move texts and the move menu were checked; the charge text reads the move number it is shown for).
Tests: t94_v86.py gate gw fanfare hof lab. run_v86.sh = run_v85.sh + t94.
