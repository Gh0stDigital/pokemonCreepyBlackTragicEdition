Creepy Black Mu v55 (from v54): LORELEI as BLACK
SHA-256 see CLAUDE.md

- Map F5 (LORELEI's room). When the player is BLACK (D46C): new before-battle speech ("I am LORELEI of the ELITE FOUR! So, you're the dark
  trainer ... Hahaha! Are you ready?") and new defeat speech ("I don't believe it... You're no ordinary trainer! Is this really the end...?").
  The GHOST route keeps the original speeches.
- Her fight is mandatory (BANE kills her in the phase), so nothing is said afterwards as BLACK: the end-battle script skips the after-battle
  text and the exit block opens by itself (EndTrainerBattle re-runs the map-load code). Not BLACK: the after-battle text as before.
- Code: bank 30:6000 texts; bank 1D:7E30 TX_ASM choosers sb/se (trainer header words at 1D:6259 and 625D) and endtail (patched at 1D:624A).
- Tests: t63_v55.py black, normal. run_v55.sh = run_v54.sh + t63.
- BRUNO, AGATHA's room and LANCE follow the same pattern next.
