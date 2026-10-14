Creepy Black Mu v57 (from v56): LANCE as BLACK
SHA-256 ba82a763baa083e6aae83511d5790a8c6bfd9d89f95e1cfeadf60d67127d96b1

- Map 71 (LANCE's room, bank 16), same pattern as LORELEI (v55) / BRUNO (v56). As BLACK (D46C): new before-battle speech ("So... The others
  have fallen. ... Your reign of terror ends here!") and defeat speech ("Impossible... This power... ... No... This cannot be how it ends!");
  nothing is said after the fight. His after-battle text normally also sets D866 bit 6 (beat LANCE): the new end-battle tail sets that
  flag itself, so the room counts as beaten and the way to the champion stays open. GHOST route: originals unchanged.
- Code: bank 30:6400 texts; bank 16:7000 choosers sb/se (trainer header words at 16:639B / 639F) and endtail (patched at 16:6354).
- Tests: t65_v57.py black, normal. run_v57.sh = run_v56.sh + t65.
