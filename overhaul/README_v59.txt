Creepy Black Mu v59 (from v58): OAK'S LAB after the League
SHA-256 d9b1e6a9b024fb2acee21d7e0a5d5fdcabf7aa911b82f92164d26712d23295b7

- As BLACK (D46C) with D876 >= 4 (AGATHA's scene after the League is done): OAK'S LAB (map 28, bank 7) is empty. Every object is hidden each frame
  (bank 30 lab59) except the aide (object 10, picture 20), who hides in the lower-left corner (10,0) facing the wall.
- His talk (text id 10, TX_ASM chooser at 7:7F70+): the frightened speech ("P-please! Don't hurt me!" ... "I don't want to die!");
  the first time D876 becomes 5 (OAK went to BILL's cottage near CERULEAN CITY; the next chapter uses it). Before the League is done or on the
  GHOST route: the old lab and text.
- Code: bank 7:7F70 lab_s (map script wrapper) + aide_text; bank 30:7500 text, 7800 lab59.
- Tests: t67_v59.py black. run_v59.sh = run_v58.sh + t67.
