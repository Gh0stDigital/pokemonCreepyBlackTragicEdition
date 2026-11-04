Creepy Black Mu v103 (on v102): BLACK's battle back picture has a white eye
SHA-256: 77f3a31d1e52100ff981ad5289adec0c1592d20deea135cbbbb3efbca240c914

BLACK's back picture (2D:7A00, used by BLACK's species header, YOU-as-BLACK and the battle intro stub) now shows one white eye on
the right side of the head, toward the opponent: a side view with the same slanted eye as his map sprite's side frames (two pixels,
then one lower toward the front) at (row 9, x 17-18) and (row 10, x 19). Everything else (silhouette, halo, 28x28 fit) is v37's.
Rewritten in place (114 bytes, v37's 112 + two free bytes). Grid: assets/BlackBackEye/black_back_v103.json.

Test: t54_v46.py start (BLACK's picture on screen, 49 tiles; CHARMANDER control) passes; qa_ref/v103_black_eye_battle.png.
