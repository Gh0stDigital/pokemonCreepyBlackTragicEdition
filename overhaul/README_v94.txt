Creepy Black Mu v94 (on v93): the climax evolution scene is RED -> BLACK only
SHA-256: fd1925a2a6384d5261019b80b4b773fd09694319daeffd8a4de1c7dc6d0767c6

The evolution screen of the climax no longer flickers through the GHOST sprite: one run of the game's evolution animation (bank 1E:7E34) from RED's picture (86) to BLACK (7F);
the text ("GHOST has transcended and become BLACK.") and everything after are unchanged. evo78 (2D:4B60) is rewritten in place (v78 ran the animation twice, RED -> GHOST -> BLACK).
Test: t102_v94.py evo (picture loader hook: v93 loads 86, 1F, 86, 7F; v94 86, 7F). run_v94.sh = run_v93.sh + t102.
