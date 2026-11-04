Creepy Black Mu v101 (on v100): the town SHAMANESSES are gone once the player is BLACK
SHA-256: 0409c8bdafe3a2ffa05282c19d52bb2984c507a41aecf1621ab036298c85c3c7

After the ritual (the player is BLACK, D46C = 1) none of the ten town shamanesses (v63/v66) is added to her town any more, whether
you talked to her or not, and nothing of her is left after a START menu redraw. Before the climax nothing changes (GHOST route,
talked flag D840/D841, gone after the next map load).

Code: sham101 (31:7D00) is the new start of app66 (31:4900, from InitMapSprites): D46C set -> app66's own ".wipe" path (31:4993, the
"talked to: gone" case), else its first two instructions and on at 31:4904.

Test: t71_v63.py town <map> black now expects NO shamaness from v101 (all ten towns, also after a START menu redraw);
town <map> without 'black' = RED, she is there and talks (control). t71 fix (also committed earlier): its BLK switch was
overwritten by t46's species constant BLK, so every t71 run used to play as BLACK; the switch is AS_BLACK now.
